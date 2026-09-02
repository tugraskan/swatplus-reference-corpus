from pathlib import Path

from swatplus_reference.comparison.run import (
    _build_preview,
    _input_contract_changes_markdown,
    _input_contract_diff,
    _input_file_inventory,
    _schema_diff,
    _symbol_diff,
)
from swatplus_reference.docs.pages import Page
from swatplus_reference.docs.render import render_site
from swatplus_reference.parser.documentation import parse_documentation
from swatplus_reference.parser.facts import FactStore, Symbol
from swatplus_reference.parser.schema_model import (
    DerivedTypeDoc,
    IOOperation,
    ModuleDoc,
    ProcedureDoc,
    ProjectIndex,
    SourceLocation,
    VariableRef,
)
from swatplus_reference.source.config import (
    ComparisonConfig,
    Config,
    SourceProfile,
    load_config,
)


FIXTURES = Path(__file__).parent / "fixtures"


def _symbol(name: str, source_hash: str, calls: list[str] | None = None) -> Symbol:
    return Symbol(
        kind="subroutine",
        name=name,
        file=f"{name}.f90",
        start_line=1,
        end_line=3,
        calls=calls or [],
        source_hash=source_hash,
    )


def _schema_project_with_read(
    filename: str,
    *,
    procedure: str = "input_read",
    file_expr: str | None = None,
    fields: list[str] | None = None,
) -> ProjectIndex:
    expr = file_expr or f"'{filename}'"
    return ProjectIndex(
        project_name="test",
        source_root=".",
        procedures=[
            ProcedureDoc(
                name=procedure,
                kind="subroutine",
                location=SourceLocation(f"{procedure}.f90", 1, 20),
                io=[
                    IOOperation(
                        kind="open",
                        unit="107",
                        file_expr=expr,
                        file_resolved=filename,
                        raw=f"open (107,file={expr})",
                        location=SourceLocation(f"{procedure}.f90", 4),
                    ),
                    IOOperation(
                        kind="read",
                        unit="107",
                        file_expr=None,
                        file_resolved=filename,
                        raw="read (107,*,iostat=eof) titldum",
                        location=SourceLocation(f"{procedure}.f90", 5),
                        fields=["titldum"],
                    ),
                    IOOperation(
                        kind="read",
                        unit="107",
                        file_expr=None,
                        file_resolved=filename,
                        raw="read (107,*,iostat=eof) one, two",
                        location=SourceLocation(f"{procedure}.f90", 8),
                        fields=fields or ["one", "two"],
                    ),
                ],
            )
        ],
    )


def _schema_project_with_indirect_water_allocation_reads() -> ProjectIndex:
    location = SourceLocation("input_file_module.f90", 1)
    dtype = DerivedTypeDoc(
        name="input_water_allocation",
        location=location,
        components=[
            VariableRef(
                name="pou",
                declaration='character(len=25) :: pou = "place_of_use.wro"',
                location=SourceLocation("input_file_module.f90", 2),
                vartype="character(len=25)",
                initial='"place_of_use.wro"',
            ),
            VariableRef(
                name="pod",
                declaration='character(len=25) :: pod = "point_of_diver.wro"',
                location=SourceLocation("input_file_module.f90", 3),
                vartype="character(len=25)",
                initial='"point_of_diver.wro"',
            ),
        ],
    )
    module = ModuleDoc(
        name="input_file_module",
        location=location,
        variables=[
            VariableRef(
                name="in_wallo",
                declaration="type (input_water_allocation) :: in_wallo",
                location=SourceLocation("input_file_module.f90", 5),
                vartype="type (input_water_allocation)",
            )
        ],
    )
    proc = ProcedureDoc(
        name="water_allocation_read",
        kind="subroutine",
        location=SourceLocation("water_allocation_read.f90", 1, 40),
        io=[
            IOOperation(
                kind="open",
                unit="107",
                file_expr="in_wallo%pou",
                file_resolved="in_wallo%pou",
                raw="open (107,file=in_wallo%pou)",
                location=SourceLocation("water_allocation_read.f90", 4),
            ),
            IOOperation(
                kind="read",
                unit="107",
                file_expr=None,
                file_resolved=None,
                raw="read (107,*) titldum",
                location=SourceLocation("water_allocation_read.f90", 5),
                fields=["titldum"],
            ),
            IOOperation(
                kind="read",
                unit="107",
                file_expr=None,
                file_resolved=None,
                raw="read (107,*) ip, pou(ip)%name, pou(ip)%pods",
                location=SourceLocation("water_allocation_read.f90", 8),
                fields=["ip", "pou(ip)%name", "pou(ip)%pods"],
            ),
            IOOperation(
                kind="open",
                unit="108",
                file_expr="in_wallo%pod",
                file_resolved="in_wallo%pod",
                raw="open (108,file=in_wallo%pod)",
                location=SourceLocation("water_allocation_read.f90", 20),
            ),
            IOOperation(
                kind="read",
                unit="108",
                file_expr=None,
                file_resolved=None,
                raw="read (108,*) ipod, pod(ipod)%name",
                location=SourceLocation("water_allocation_read.f90", 24),
                fields=["ipod", "pod(ipod)%name"],
            ),
        ],
    )
    return ProjectIndex(
        project_name="test",
        source_root=".",
        modules=[module],
        types=[dtype],
        procedures=[proc],
    )


def test_config_loads_locked_comparison(tmp_path: Path):
    path = tmp_path / "swatref.toml"
    path.write_text(
        """
[sources.base]
ref = "dev"
commit = "1111111111111111111111111111111111111111"

[sources.candidate]
ref = "refs/pull/252/head"
commit = "2222222222222222222222222222222222222222"

[docs]
source = "base"

[comparisons.pr_252]
base_source = "base"
candidate_source = "candidate"
output_dir = "reports/pr-252"
work_dir = ".swatref/pr-252"
""".strip(),
        encoding="utf-8",
    )

    comparison = load_config(path).comparison("pr_252")

    assert comparison.base_source == "base"
    assert comparison.candidate_source == "candidate"
    assert comparison.output_dir == Path("reports/pr-252")


def test_comparison_preview_matches_normal_rich_render(tmp_path, monkeypatch):
    commit = "a" * 40
    profile = SourceProfile(
        name="candidate",
        repository="https://github.com/example/swatplus",
        ref="candidate",
        commit=commit,
        checkout=FIXTURES.parent,
        subdir="fixtures",
        label="candidate",
    )
    cfg = Config(
        root=tmp_path,
        source_ref=commit,
        source_link_base=profile.source_link_base(commit),
        docs_dir=Path("docs_src"),
        render_dir=Path("normal"),
        sources={"candidate": profile},
        docs_source="candidate",
    )
    comparison = ComparisonConfig(
        name="candidate",
        base_source="candidate",
        candidate_source="candidate",
        output_dir=Path("reports/candidate"),
        work_dir=Path("work/candidate"),
    )
    page = Page(
        path=cfg.abs_docs_dir / "procedures" / "demo_calc.md",
        kind="procedure",
        symbol="demo_calc",
        title="demo_calc",
        status="filled",
        body=(
            "<!-- facts:arguments -->\n\n"
            "<!-- facts:locals -->\n\n"
            "<!-- facts:calls -->\n\n"
            "<!-- facts:io -->\n\n"
            "<!-- facts:assignments -->\n\n"
            "<!-- facts:select_cases -->\n"
        ),
    )
    page.save()
    (tmp_path / "mkdocs.yml").write_text(
        "site_name: test\ndocs_dir: docs\nsite_dir: site\n",
        encoding="utf-8",
    )
    store, rich = parse_documentation(FIXTURES, commit)
    normal_dir = render_site(cfg, store, rich)
    normal_page = (normal_dir / "procedures" / "demo_calc.md").read_text(
        encoding="utf-8"
    )
    monkeypatch.setattr(
        "swatplus_reference.comparison.run._run_logged",
        lambda *args, **kwargs: {"success": True, "returncode": 0},
    )

    result = _build_preview(cfg, comparison, store, rich, commit)

    preview_page = (
        tmp_path
        / "work"
        / "candidate"
        / "preview"
        / "docs"
        / "procedures"
        / "demo_calc.md"
    ).read_text(encoding="utf-8")
    assert result["success"] is True
    assert preview_page == normal_page
    assert "### Control-flow outline" in preview_page
    assert "| Target | Statement | Meaning | Source |" in preview_page
    assert "*No assignments recorded.*" not in preview_page


def test_symbol_diff_reports_add_remove_and_structured_changes():
    base = FactStore(symbols={
        "kept": _symbol("kept", "aaa", ["old_call"]),
        "removed": _symbol("removed", "bbb"),
    })
    candidate = FactStore(symbols={
        "kept": _symbol("kept", "ccc", ["new_call"]),
        "added": _symbol("added", "ddd"),
    })

    result = _symbol_diff(base, candidate)

    assert result["added"] == ["added"]
    assert result["removed"] == ["removed"]
    assert result["changed"][0]["symbol"] == "kept"
    assert set(result["changed"][0]["changed_fields"]) == {"calls", "source_hash"}


def test_schema_diff_separates_expected_changes_from_new_unresolved():
    base = {
        "files": {"a.dat": {"fields": [{"name": "one", "type": "real"}]}},
        "unresolved": [],
    }
    candidate = {
        "files": {
            "a.dat": {"fields": [{"name": "one", "type": "integer"}]},
            "b.dat": {"fields": []},
        },
        "unresolved": [{"file": "c.dat", "reason": "reader not found"}],
    }

    result = _schema_diff(base, candidate)

    assert result["sections"]["files"]["added"] == ["b.dat"]
    assert result["sections"]["files"]["changed"] == ["a.dat"]
    assert result["unresolved_sections"]["unresolved"]["new"] == ["c.dat"]
    assert result["summary"]["new_unresolved"] == 1


def test_schema_diff_includes_source_read_evidence_for_review_targets():
    base = {
        "files": {"c.dat": {"fields": [{"name": "old", "type": "real"}]}},
        "unresolved": [],
    }
    candidate = {
        "files": {},
        "unresolved": [{"file": "c.dat", "reason": "reader not found"}],
    }

    result = _schema_diff(
        base,
        candidate,
        base_project=_schema_project_with_read("c.dat", fields=["old"]),
        candidate_project=_schema_project_with_read("c.dat", fields=["new"]),
    )

    evidence = result["source_read_evidence"]["c.dat"]
    assert evidence["schema_diff_status"] == ["files.removed", "newly_unresolved"]
    assert evidence["review_needed"] is True
    assert evidence["candidate"]["status"] == "found"
    assert evidence["candidate"]["blocks"][0]["reads"][1]["fields"] == ["new"]


def test_schema_diff_includes_related_read_evidence_when_exact_filename_is_gone():
    base = {
        "multi_record": {"water_allocation.wro": {"sections": []}},
        "multi_record_unresolved": [],
    }
    candidate = {
        "multi_record": {},
        "multi_record_unresolved": [
            {"file": "water_allocation.wro", "reason": "reader not found"}
        ],
    }
    candidate_project = _schema_project_with_read(
        "in_wallo%pou",
        procedure="water_allocation_read",
        file_expr="in_wallo%pou",
        fields=["pou(ipou)%name", "pou(ipou)%pods"],
    )

    result = _schema_diff(
        base,
        candidate,
        base_project=_schema_project_with_read("water_allocation.wro"),
        candidate_project=candidate_project,
    )

    evidence = result["source_read_evidence"]["water_allocation.wro"]
    assert evidence["candidate"]["status"] == "not_found"
    assert evidence["candidate_related"][0]["procedure"] == "water_allocation_read"
    assert "reader procedure tokens match target" in evidence["candidate_related"][0]["match"]


def test_input_inventory_resolves_indirect_default_filenames():
    project = _schema_project_with_indirect_water_allocation_reads()
    schema = {
        "multi_record": {"place_of_use.wro": {"sections": []}},
        "files": {"point_of_diver.wro": {"fields": []}},
    }

    inventory = _input_file_inventory(project, schema)

    assert set(inventory["files"]) == {"place_of_use.wro", "point_of_diver.wro"}
    pou = inventory["files"]["place_of_use.wro"]
    assert pou["source_expressions"] == ["in_wallo%pou"]
    assert pou["certification"] == "certified"
    assert pou["blocks"][0]["resolved_default_filenames"] == ["place_of_use.wro"]
    assert pou["blocks"][0]["reads"][1]["fields"] == [
        "ip",
        "pou(ip)%name",
        "pou(ip)%pods",
    ]


def test_input_contract_same_project_has_zero_changes():
    project = _schema_project_with_indirect_water_allocation_reads()
    schema = {"files": {"place_of_use.wro": {}, "point_of_diver.wro": {}}}

    result = _input_contract_diff(project, schema, project, schema)

    assert result["summary"]["added"] == 0
    assert result["summary"]["removed"] == 0
    assert result["summary"]["changed"] == 0
    assert result["summary"]["new_unresolved_open_blocks"] == 0
    assert result["added"] == {}
    assert result["removed"] == {}
    assert result["changed"] == {}


def test_input_contract_reports_added_and_changed_read_order():
    base = _schema_project_with_read("existing.wal", fields=["one", "two"])
    candidate = ProjectIndex(
        project_name="test",
        source_root=".",
        procedures=[
            *_schema_project_with_read(
                "existing.wal", fields=["one", "inserted", "two"]
            ).procedures,
            *_schema_project_with_read("new_input.wal", fields=["alpha", "beta"]).procedures,
        ],
    )
    base_schema = {"files": {"existing.wal": {}}}
    candidate_schema = {
        "files": {"existing.wal": {}, "new_input.wal": {}}
    }

    result = _input_contract_diff(base, base_schema, candidate, candidate_schema)

    assert list(result["added"]) == ["new_input.wal"]
    assert list(result["changed"]) == ["existing.wal"]
    assert result["changed"]["existing.wal"]["changes"][
        "candidate_read_fields"
    ] == ["titldum", "one", "inserted", "two"]
    assert result["changed"]["existing.wal"]["changes"]["field_edits"] == [
        {
            "operation": "insert",
            "base_index": 2,
            "candidate_index": 2,
            "removed": [],
            "added": ["inserted"],
        }
    ]
    report = _input_contract_changes_markdown(result)
    assert "## Added inputs" in report
    assert "### `new_input.wal`" in report
    assert "## Changed input read contracts" in report
