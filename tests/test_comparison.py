from pathlib import Path

from swatplus_reference.comparison.run import (
    _build_preview,
    _input_contract_changes_markdown,
    _input_contract_diff,
    _input_file_inventory,
    _schema_diff,
    _symbol_diff,
)
from swatplus_reference.comparison.schema_semantic import (
    MAX_COMPARISON_DEPTH,
    _semantic_field_diff,
    _semantic_schema_diff,
    _semantic_section_diff,
    _split_type_source,
    _strip_and_normalize,
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
    pages = [
        Page(
            path=cfg.abs_docs_dir / "procedures" / "demo_calc.md",
            kind="procedure",
            symbol="demo_calc",
            title="demo_calc",
            status="filled",
            body=(
                "<!-- facts:arguments -->\n\n"
                "<!-- facts:locals -->\n\n"
                "<!-- facts:calls -->\n\n"
                "<!-- facts:uses -->\n\n"
                "<!-- facts:io -->\n\n"
                "<!-- facts:assignments -->\n\n"
                "<!-- facts:state_touched -->\n"
            ),
        ),
        Page(
            path=cfg.abs_docs_dir / "procedures" / "demo_select.md",
            kind="procedure",
            symbol="demo_select",
            title="demo_select",
            status="filled",
            body="<!-- facts:select_cases -->\n",
        ),
        Page(
            path=cfg.abs_docs_dir / "modules" / "demo_module.md",
            kind="module",
            symbol="demo_module",
            title="demo_module",
            status="filled",
            body=(
                "<!-- facts:variables -->\n\n"
                "<!-- facts:members -->\n\n"
                "<!-- facts:types -->\n"
            ),
        ),
    ]
    for page in pages:
        page.save()
    (tmp_path / "mkdocs.yml").write_text(
        "site_name: test\n"
        "docs_dir: docs\n"
        "site_dir: site\n"
        "markdown_extensions:\n"
        "  - pymdownx.superfences:\n"
        "      custom_fences:\n"
        "        - name: mermaid\n"
        "          format: !!python/name:pymdownx.superfences.fence_code_format\n",
        encoding="utf-8",
    )
    store, rich = parse_documentation(FIXTURES, commit)
    normal_dir = render_site(cfg, store, rich)
    relative_pages = [page.path.relative_to(cfg.abs_docs_dir) for page in pages]
    normal_pages = {
        path.as_posix(): (normal_dir / path).read_text(encoding="utf-8")
        for path in relative_pages
    }
    monkeypatch.setattr(
        "swatplus_reference.comparison.run._run_logged",
        lambda *args, **kwargs: {"success": True, "returncode": 0},
    )

    result = _build_preview(cfg, comparison, store, rich, commit)

    preview_dir = tmp_path / "work" / "candidate" / "preview" / "docs"
    preview_pages = {
        path.as_posix(): (preview_dir / path).read_text(encoding="utf-8")
        for path in relative_pages
    }
    assert result["success"] is True
    preview_config = (tmp_path / "work" / "candidate" / "preview" / "mkdocs.yml").read_text(
        encoding="utf-8"
    )
    assert "!!python/name:pymdownx.superfences.fence_code_format" in preview_config
    assert preview_pages == normal_pages
    calc = preview_pages["procedures/demo_calc.md"]
    assert "### Control-flow outline" in calc
    assert "| Target | Statement | Meaning | Source |" in calc
    assert "| Module | Source | Only | Why it matters here |" in calc
    assert "| Statement | Unit | File | Resolved File |" in calc
    assert "| Module | Symbol | Declaration | Source | Components |" in calc
    assert "*No assignments recorded.*" not in calc
    assert "**Cases:** `low`, `mid`, `high`" in preview_pages[
        "procedures/demo_select.md"
    ]
    module = preview_pages["modules/demo_module.md"]
    assert "| Variable | Declared | Meaning | Units | Description | Initial |" in module
    assert "| Component | Type | Units | Description | Notes |" in module


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


# --------------------------------------------------------------------------
# Condition comparison ignores reformatting, not content
#
# Between SWAT+ main and dev, `salt_fertilizer.frt` was reported as a changed
# read contract with zero field edits, no block change and no reader change.
# The whole source difference was `do isalti=1,...` -> `do isalti = 1, ...`.
# --------------------------------------------------------------------------

from swatplus_reference.comparison.run import (  # noqa: E402
    _condition_key,
    _contract_change_details,
    _is_material_contract_change,
)


def _entry(condition: str) -> dict:
    return {
        "contract": [
            {
                "procedure": "salt_fert_read",
                "reader": "salt_fert_read.f90",
                "open_condition": "if (.not. i_exist) then / else > do",
                "reads": [{"condition": condition, "fields": ["a", "b"]}],
            }
        ]
    }


def test_reformatting_a_do_header_is_not_a_contract_change():
    base = _entry("if (.not. i_exist) then / else > do > do isalti=1,db_mx%fertparm")
    cand = _entry("if (.not. i_exist) then / else > do > do isalti = 1, db_mx%fertparm")
    assert _contract_change_details(base, cand)["conditions_changed"] is False


def test_a_changed_bound_is_still_a_contract_change():
    base = _entry("do isalti = 1, db_mx%fertparm")
    cand = _entry("do isalti = 1, db_mx%saltparm")
    assert _contract_change_details(base, cand)["conditions_changed"] is True


def test_a_changed_operator_is_still_a_contract_change():
    assert _condition_key("if (a > b) then") != _condition_key("if (a >= b) then")


def test_a_changed_loop_variable_is_still_a_contract_change():
    assert _condition_key("do i = 1, n") != _condition_key("do j = 1, n")


def test_normalisation_never_merges_two_identifiers():
    """Dropping all whitespace would make `do i` and a variable `doi` equal.
    Space between two word characters must survive."""
    assert _condition_key("do i = 1, n") != _condition_key("doi = 1, n")
    assert _condition_key("end do") != _condition_key("enddo")


def test_the_stored_condition_is_left_byte_exact():
    """Only the comparison is normalised; the contract itself is rendered
    verbatim and must not be rewritten."""
    cand = _entry("do isalti = 1,  db_mx%fertparm")
    details = _contract_change_details(_entry("do isalti=1,db_mx%fertparm"), cand)
    assert details["conditions_changed"] is False
    assert cand["contract"][0]["reads"][0]["condition"] == "do isalti = 1,  db_mx%fertparm"


def test_a_reformat_only_entry_is_not_reported_at_all():
    """Suppressing the flag is not enough: an entry whose every flag is false
    still costs a reviewer the click to find that out."""
    base = _entry("do isalti=1,db_mx%fertparm")
    cand = _entry("do isalti = 1, db_mx%fertparm")
    details = _contract_change_details(base, cand)
    assert _is_material_contract_change(details) is False


def test_a_real_field_change_is_still_reported():
    base = _entry("do i = 1, n")
    cand = _entry("do i = 1, n")
    cand["contract"][0]["reads"][0]["fields"] = ["a", "c"]
    details = _contract_change_details(base, cand)
    assert details["field_edits"]
    assert _is_material_contract_change(details) is True


def test_a_changed_read_role_is_reported_rather_than_slipping_through():
    """`role` is part of the stored contract but was covered by no flag, so a
    role-only change would have been listed with nothing explaining it."""
    base = _entry("do i = 1, n")
    cand = _entry("do i = 1, n")
    cand["contract"][0]["reads"][0]["role"] = "header"
    details = _contract_change_details(base, cand)
    assert details["roles_changed"] is True
    assert _is_material_contract_change(details) is True


# --------------------------------------------------------------------------
# Output contracts
#
# Writes outnumber reads ~3:1 in SWAT+ and had no diff at all, so a release
# that added, dropped or re-columned an output file produced no report line.
# --------------------------------------------------------------------------

from pathlib import Path  # noqa: E402

from swatplus_reference.comparison.run import (  # noqa: E402
    _io_blocks,
    _output_contract_diff,
    _output_file_inventory,
)
from swatplus_reference.parser.ast_index import build_ast_index  # noqa: E402
from swatplus_reference.parser.schema_config import BuildConfig  # noqa: E402

WRITER = """\
      subroutine emit
      integer :: i = 0
      real :: flow = 0.
      real :: sed = 0.
      open (107,file="demo.out")
      write (107,*) "name", "flow"
      do i = 1, 3
        write (107,*) flow, sed
      end do
      end subroutine emit
"""


def _index(tmp_path: Path, body: str, name: str = "emit.f90"):
    (tmp_path / name).write_text(body)
    return build_ast_index(BuildConfig(source_dir=tmp_path))


def test_write_blocks_are_grouped_like_read_blocks(tmp_path):
    index = _index(tmp_path, WRITER)
    proc = index.procedures[0]
    assert [op.kind for op in _io_blocks(proc, kind="read")[0][1]] == []
    assert [op.kind for op in _io_blocks(proc, kind="write")[0][1]] == ["write", "write"]


def test_an_output_file_is_inventoried_with_its_written_fields(tmp_path):
    inventory = _output_file_inventory(_index(tmp_path, WRITER))
    assert "demo.out" in inventory["files"]
    entry = inventory["files"]["demo.out"]
    assert entry["contract"][0]["writes"], "writes must be keyed as writes, not reads"


def test_outputs_carry_no_schema_certification(tmp_path):
    """The schema describes inputs. An output must not be reported as needing
    schema review just because no schema mentions it."""
    entry = _output_file_inventory(_index(tmp_path, WRITER))["files"]["demo.out"]
    assert "certification" not in entry
    assert "review_needed" not in entry


def test_an_added_output_file_is_reported(tmp_path):
    b = tmp_path / "b"; b.mkdir()
    c = tmp_path / "c"; c.mkdir()
    base = _index(b, WRITER.replace('"demo.out"', '"old.out"'))
    cand = _index(c, WRITER)
    diff = _output_contract_diff(base, cand)
    assert set(diff["added"]) == {"demo.out"}
    assert set(diff["removed"]) == {"old.out"}
    assert diff["summary"]["added"] == 1


def test_a_changed_write_column_is_reported(tmp_path):
    b = tmp_path / "b"; b.mkdir()
    c = tmp_path / "c"; c.mkdir()
    base = _index(b, WRITER)
    cand = _index(c, WRITER.replace("write (107,*) flow, sed", "write (107,*) flow, sed, i"))
    diff = _output_contract_diff(base, cand)
    assert "demo.out" in diff["changed"]
    edits = diff["changed"]["demo.out"]["changes"]["field_edits"]
    assert any("i" in edit["added"] for edit in edits)


def test_an_unchanged_output_is_not_reported(tmp_path):
    b = tmp_path / "b"; b.mkdir()
    c = tmp_path / "c"; c.mkdir()
    diff = _output_contract_diff(_index(b, WRITER), _index(c, WRITER))
    assert diff["summary"] == {
        **diff["summary"],
        "added": 0,
        "removed": 0,
        "changed": 0,
    }


def test_a_unit_opened_in_another_file_is_now_named(tmp_path):
    """This asserted the opposite before the parser bound units across files:
    a unit opened in one file and written in another could not be named, and
    the write was counted as unresolved. It resolves now, so the output file
    appears under its real name."""
    (tmp_path / "opener.f90").write_text(
        "      subroutine opener\n"
        '      open (140,file="split.out")\n'
        "      end subroutine opener\n"
    )
    (tmp_path / "writer.f90").write_text(
        "      subroutine writer\n"
        "      real :: flow = 0.\n"
        "      write (140,*) flow\n"
        "      end subroutine writer\n"
    )
    inventory = _output_file_inventory(
        build_ast_index(BuildConfig(source_dir=tmp_path))
    )

    assert "split.out" in inventory["files"]
    assert inventory["coverage"]["unresolved_units"] == 0
    assert any(
        b["reader"] == "writer.f90" for b in inventory["files"]["split.out"]["blocks"]
    )


def test_a_unit_that_cannot_be_named_is_still_counted_not_invented(tmp_path):
    """Binding across files does not make every unit nameable: one never opened
    anywhere has no filename in the source. It must stay counted as unresolved
    rather than reach the report under a `unit_NNN` pseudo-filename."""
    (tmp_path / "w.f90").write_text(
        "      subroutine w\n      write (9100,*) 1\n      end subroutine w\n"
    )
    inventory = _output_file_inventory(
        build_ast_index(BuildConfig(source_dir=tmp_path))
    )

    assert not any(name.startswith("unit_") for name in inventory["files"])
    assert inventory["coverage"]["unresolved_units"] == 1
    assert inventory["unresolved_open_blocks"][0]["unit"] == "unit_9100"


def test_coverage_is_reported_so_zero_changes_is_not_read_as_no_changes(tmp_path):
    inventory = _output_file_inventory(_index(tmp_path, WRITER))
    coverage = inventory["coverage"]
    assert coverage["resolved_output_files"] == 1
    assert coverage["resolved_write_statements"] == 2
    assert coverage["unresolved_units"] == 0


def test_a_unit_carried_as_a_dummy_argument_is_also_unresolved():
    """PR 254 passes unit numbers into a helper as arguments (`u_txt`, `u_csv`).
    The index's sentinel is `unit_<whatever was written>`, so a non-numeric unit
    is just as unresolved as a numeric one and must not reach the report as a
    filename."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "helper.f90").write_text(
            "      subroutine emit_pair(u_txt)\n"
            "      integer, intent(in) :: u_txt\n"
            "      write (u_txt,*) 1\n"
            "      end subroutine emit_pair\n"
        )
        inventory = _output_file_inventory(
            build_ast_index(BuildConfig(source_dir=root))
        )

    assert inventory["files"] == {}
    assert inventory["unresolved_open_blocks"][0]["unit"] == "unit_u_txt"


# --------------------------------------------------------------------------
# Semantic schema diff tests
# --------------------------------------------------------------------------


def _field(name: str, ftype: str = "integer", doc: str | None = None) -> dict:
    return {
        "position": 0,
        "fortran_name": name,
        "fortran_type": ftype,
        "numeric": ftype in ("integer", "real", "double precision"),
        "units": None,
        "doc": doc,
    }


def test_split_type_source_separates_file_and_line_range():
    assert _split_type_source("module.f90:191-196") == ("module.f90", "191-196")
    assert _split_type_source("module.f90:42") == ("module.f90", "42")
    assert _split_type_source("module.f90") == ("module.f90", None)
    assert _split_type_source(None) == (None, None)
    assert _split_type_source("") == (None, None)


def test_strip_metadata_removes_reader_line_and_reader():
    payload = {
        "reader_line": 42,
        "reader": "some_reader.f90",
        "fields": [_field("x")],
        "nested": {"reader_line": 10, "name": "inner"},
    }
    result = _strip_and_normalize(payload)
    assert "reader_line" not in result
    assert "reader" not in result
    assert "reader_line" not in result["nested"]
    assert result["fields"] == [_field("x")]
    assert result["nested"]["name"] == "inner"


def test_semantic_diff_ignores_reader_line_changes():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "reader": "test_read.f90",
                "type_source": "module.f90:191-196",
                "fields": [_field("x", "integer")],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 58,
                "reader": "test_read.f90",
                "type_source": "module.f90:191-196",
                "fields": [_field("x", "integer")],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 0
    assert result["summary"]["documentation_only_changes"] == 0
    assert result["summary"]["source_location_only_changes"] == 1
    assert result["summary"]["uncertain_changes"] == 0
    assert "test.dat" in result["semantic_sections"]["files"]["source_location_only_changes"]


def test_semantic_diff_ignores_type_source_line_range_changes():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "type_source": "module.f90:191-196",
                "fields": [_field("x", "integer")],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "type_source": "module.f90:190-195",
                "fields": [_field("x", "integer")],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 0
    assert result["summary"]["source_location_only_changes"] == 1


def test_semantic_diff_ignores_nested_block_line_number_changes():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "type_source": "module.f90:191-196",
                "fields": [_field("x")],
                "blocks": [
                    {
                        "reader_line": 50,
                        "type_source": "module.f90:191-196",
                        "fields": [_field("y", "real")],
                    }
                ],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 58,
                "type_source": "module.f90:191-196",
                "fields": [_field("x")],
                "blocks": [
                    {
                        "reader_line": 62,
                        "type_source": "module.f90:191-196",
                        "fields": [_field("y", "real")],
                    }
                ],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 0
    assert result["summary"]["source_location_only_changes"] == 1


def test_semantic_diff_ignores_nested_runtime_section_line_number_changes():
    base = {
        "runtime_arity": {
            "test.ini": {
                "reader_line": 31,
                "sections": [
                    {
                        "name": "row_count_pass",
                        "reader_line": 31,
                        "count_source": "until_eof_group",
                        "fields": [_field("titldum", "character")],
                    }
                ],
            }
        }
    }
    candidate = {
        "runtime_arity": {
            "test.ini": {
                "reader_line": 32,
                "sections": [
                    {
                        "name": "row_count_pass",
                        "reader_line": 32,
                        "count_source": "until_eof_group",
                        "fields": [_field("titldum", "character")],
                    }
                ],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 0
    assert result["summary"]["source_location_only_changes"] == 1


def test_semantic_diff_field_rename_is_structural():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "fields": [_field("old_name", "integer")],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "fields": [_field("new_name", "integer")],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 1
    assert result["summary"]["documentation_only_changes"] == 0
    assert result["summary"]["source_location_only_changes"] == 0


def test_semantic_diff_field_type_change_is_structural():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "fields": [_field("x", "integer")],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "fields": [_field("x", "real")],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 1
    assert result["summary"]["documentation_only_changes"] == 0


def test_semantic_diff_field_reorder_is_structural():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "fields": [_field("a"), _field("b")],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "fields": [_field("b"), _field("a")],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 1


def test_semantic_diff_doc_only_change_is_documentation():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "fields": [_field("x", "integer", doc="old doc")],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "fields": [_field("x", "integer", doc="new doc")],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 0
    assert result["summary"]["documentation_only_changes"] == 1
    assert result["summary"]["source_location_only_changes"] == 0


def test_semantic_diff_reader_file_change_is_source_organization():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "reader": "old_reader.f90",
                "fields": [_field("x")],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "reader": "new_reader.f90",
                "fields": [_field("x")],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 0
    assert result["summary"]["source_organization_changes"] == 1
    assert "test.dat" in result["semantic_sections"]["files"]["source_organization_changes"]


def test_semantic_diff_type_source_file_change_is_source_organization():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "type_source": "old_module.f90:191-196",
                "fields": [_field("x")],
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 42,
                "type_source": "new_module.f90:191-196",
                "fields": [_field("x")],
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 0
    assert result["summary"]["source_organization_changes"] == 1
    assert "test.dat" in result["semantic_sections"]["files"]["source_organization_changes"]


def test_semantic_diff_added_file_is_structural():
    base = {"files": {}}
    candidate = {"files": {"new.dat": {"reader_line": 1, "fields": [_field("x")]}}}
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 1
    assert result["semantic_sections"]["files"]["added"] == ["new.dat"]


def test_semantic_diff_removed_file_is_structural():
    base = {"files": {"old.dat": {"reader_line": 1, "fields": [_field("x")]}}}
    candidate = {"files": {}}
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 1
    assert result["semantic_sections"]["files"]["removed"] == ["old.dat"]


def test_semantic_diff_field_added_is_structural():
    base = {"files": {"test.dat": {"reader_line": 1, "fields": [_field("x")]}}}
    candidate = {
        "files": {
            "test.dat": {"reader_line": 1, "fields": [_field("x"), _field("y")]}
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 1


def test_semantic_diff_field_removed_is_structural():
    base = {
        "files": {
            "test.dat": {"reader_line": 1, "fields": [_field("x"), _field("y")]}
        }
    }
    candidate = {"files": {"test.dat": {"reader_line": 1, "fields": [_field("x")]}}}
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 1


def test_semantic_diff_repeat_group_change_is_structural():
    base = {
        "files": {
            "test.dat": {
                "reader_line": 1,
                "fields": [_field("nspu")],
                "repeat": {
                    "count_field": "nspu",
                    "count_expr": "nspu",
                    "fields": [_field("elem_cnt")],
                },
            }
        }
    }
    candidate = {
        "files": {
            "test.dat": {
                "reader_line": 1,
                "fields": [_field("nspu")],
                "repeat": {
                    "count_field": "nspu",
                    "count_expr": "nspu",
                    "fields": [_field("elem_cnt"), _field("extra")],
                },
            }
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 1


def test_semantic_diff_undeterministic_metadata_only_changes():
    """When only reader_line and type_source line range differ, the semantic
    diff should report zero structural changes."""
    base = {
        "files": {
            "a.con": {
                "reader_line": 100,
                "type_source": "mod.f90:50-60",
                "fields": [_field("x", "real", doc="old")],
            },
            "b.con": {
                "reader_line": 200,
                "type_source": "mod.f90:70-80",
                "fields": [_field("y", "integer", doc="same")],
            },
        }
    }
    candidate = {
        "files": {
            "a.con": {
                "reader_line": 105,
                "type_source": "mod.f90:49-59",
                "fields": [_field("x", "real", doc="old")],
            },
            "b.con": {
                "reader_line": 200,
                "type_source": "mod.f90:70-80",
                "fields": [_field("y", "integer", doc="same")],
            },
        }
    }
    result = _semantic_schema_diff(base, candidate)
    assert result["summary"]["structural_changes"] == 0
    assert result["summary"]["documentation_only_changes"] == 0
    assert result["summary"]["source_location_only_changes"] == 1


def _semantic_categories(base_entry, candidate_entry, section="files"):
    result = _semantic_schema_diff(
        {section: {"test.dat": base_entry}},
        {section: {"test.dat": candidate_entry}},
    )
    details = result["semantic_sections"][section]["entry_details"]["test.dat"]
    return result, set(details["categories"]), details["changes"]


def test_semantic_nested_source_locations_and_reader_move_stay_separate():
    base = {
        "blocks": [{
            "reader": "old.f90",
            "reader_line": 11,
            "type_source": "module.f90:20-25",
            "fields": [_field("x")],
        }]
    }
    candidate = {
        "blocks": [{
            "reader": "new.f90",
            "reader_line": 12,
            "type_source": "module.f90:21-26",
            "fields": [_field("x")],
        }]
    }
    result, categories, changes = _semantic_categories(base, candidate)
    assert categories == {"source_location", "source_organization"}
    assert {change["path"] for change in changes} == {
        "/blocks/0/reader",
        "/blocks/0/reader_line",
        "/blocks/0/type_source",
    }
    assert result["summary"]["source_location_only_changes"] == 0


def test_semantic_nested_type_source_path_and_line_change_keeps_both():
    base = {"sections": [{"type_source": "old.f90:1-2"}]}
    candidate = {"sections": [{"type_source": "new.f90:3-4"}]}
    _, categories, changes = _semantic_categories(
        base, candidate, section="runtime_arity"
    )
    assert categories == {"source_location", "source_organization"}
    assert [change["category"] for change in changes] == [
        "source_organization", "source_location"
    ]


def test_semantic_nested_docs_in_repeat_and_variant_are_documentation_only():
    for key, before_value, after_value in (
        ("repeat", {"fields": [_field("x", doc="old")]},
         {"fields": [_field("x", doc="new")]}),
        ("variants", {"a": {"fields": [_field("x", doc="old")]}},
         {"a": {"fields": [_field("x", doc="new")]}}),
    ):
        result, categories, changes = _semantic_categories(
            {key: before_value}, {key: after_value}
        )
        assert categories == {"documentation"}
        assert changes[0]["path"].endswith("/doc")
        assert result["summary"]["documentation_only_changes"] == 1


def test_semantic_runtime_section_structural_change_and_line_shift():
    base = {"sections": [{"reader_line": 10, "fields": [_field("x")]}]}
    candidate = {
        "sections": [{
            "reader_line": 11,
            "fields": [_field("x"), _field("y")],
        }]
    }
    result, categories, _ = _semantic_categories(
        base, candidate, section="runtime_arity"
    )
    assert categories == {"structural", "source_location"}
    assert result["summary"]["structural_changes"] == 1
    assert result["summary"]["source_location_only_changes"] == 0


def test_semantic_mixed_structural_documentation_and_location_are_retained():
    base = {
        "reader_line": 1,
        "fields": [_field("old", doc="old doc")],
    }
    candidate = {
        "reader_line": 2,
        "fields": [_field("new", doc="new doc")],
    }
    result, categories, changes = _semantic_categories(base, candidate)
    assert categories == {"structural", "documentation", "source_location"}
    assert {change["path"] for change in changes} == {
        "/reader_line", "/fields/0/fortran_name", "/fields/0/doc"
    }
    assert result["summary"]["documentation_changes"] == 1
    assert result["summary"]["documentation_only_changes"] == 0


def test_semantic_location_and_documentation_preserve_doc_only_headline():
    result, categories, _ = _semantic_categories(
        {"reader_line": 1, "doc": "old"},
        {"reader_line": 2, "doc": "new"},
    )
    assert categories == {"documentation", "source_location"}
    assert result["summary"]["documentation_only_changes"] == 1
    assert result["summary"]["source_location_only_changes"] == 0


def test_semantic_reader_move_and_doc_change_preserve_both():
    result, categories, _ = _semantic_categories(
        {"reader": "old.f90", "doc": "old"},
        {"reader": "new.f90", "doc": "new"},
    )
    assert categories == {"documentation", "source_organization"}
    assert result["summary"]["documentation_only_changes"] == 0
    assert result["summary"]["source_organization_changes"] == 1


def test_semantic_unknown_with_known_change_remains_uncertain():
    _, categories, changes = _semantic_categories(
        {"future_key": "old", "reader_line": 1},
        {"future_key": "new", "reader_line": 2},
    )
    assert categories == {"uncertain", "source_location"}
    assert {change["path"] for change in changes} == {
        "/future_key", "/reader_line"
    }


def test_semantic_absent_key_and_explicit_null_do_not_disappear():
    result, categories, changes = _semantic_categories(
        {"future_key": None}, {}
    )
    assert categories == {"uncertain"}
    assert result["summary"]["changed_schema_entries"] == 1
    assert changes[0]["base_present"] is True
    assert changes[0]["candidate_present"] is False
    assert changes[0]["base"] is None


def test_semantic_named_field_reorder_is_structural():
    fields = [
        {"name": "a", "fortran_type": "integer"},
        {"name": "b", "fortran_type": "real"},
    ]
    _, categories, changes = _semantic_categories(
        {"fields": fields}, {"fields": list(reversed(fields))}
    )
    assert categories == {"structural"}
    assert [change["path"] for change in changes] == ["/fields/@order"]


def test_semantic_repeat_and_tagged_variant_structure_changes():
    cases = (
        ({"repeat": {"fields": [_field("x")]}},
         {"repeat": {"fields": [_field("x"), _field("y")]}}),
        ({"variants": {"a": {"tag": "a"}}},
         {"variants": {"a": {"tag": "b"}}}),
    )
    for base, candidate in cases:
        result, categories, _ = _semantic_categories(base, candidate)
        assert categories == {"structural"}
        assert result["summary"]["structural_changes"] == 1


def test_semantic_identical_schemas_have_zero_changes():
    schema = {
        "files": {"test.dat": {"reader_line": 1, "fields": [_field("x")]}},
        "runtime_arity": {},
    }
    result = _semantic_schema_diff(schema, schema)
    assert result["summary"]["changed_schema_entries"] == 0
    assert result["summary"]["unique_changed_input_files"] == 0
    assert result["semantic_sections"]["files"]["unchanged_count"] == 1


def test_semantic_entry_counts_can_exceed_unique_filenames():
    base = {
        "files": {"same.ini": {"reader_line": 1}},
        "runtime_arity": {"same.ini": {"reader_line": 5}},
    }
    candidate = {
        "files": {"same.ini": {"reader_line": 2}},
        "runtime_arity": {"same.ini": {"reader_line": 6}},
    }
    result = _semantic_schema_diff(base, candidate)
    summary = result["summary"]
    assert summary["changed_schema_entries"] == 2
    assert summary["unique_changed_input_files"] == 1
    assert summary["source_location_only_changes"] == 2
    assert summary["unique_input_files_by_category"]["source_location"] == 1


def test_semantic_release_pair_artifacts_match_expected_categories():
    import json

    root = Path(__file__).resolve().parents[1] / "schema_artifacts" / "releases"
    base = json.loads((root / "swatplus-61.0.1.json").read_text(encoding="utf-8"))
    candidate = json.loads((root / "swatplus-61.0.2.json").read_text(encoding="utf-8"))
    result = _semantic_schema_diff(base, candidate)
    summary = result["summary"]
    assert summary["changed_schema_entries"] == 71
    assert summary["unique_changed_input_files"] == 71
    assert summary["structural_changes"] == 1
    assert summary["documentation_only_changes"] == 1
    assert summary["source_location_only_changes"] == 69
    assert summary["source_organization_changes"] == 0
    assert summary["uncertain_changes"] == 0
    assert result["semantic_sections"]["files"]["structural_changes"] == ["codes.bsn"]
    assert result["semantic_sections"]["files"]["documentation_only_changes"] == [
        "sediment.cha"
    ]


def test_semantic_missing_type_source_keeps_provenance_evidence():
    result, categories, changes = _semantic_categories(
        {"fields": [_field("x")]},
        {"fields": [_field("x")], "type_source": "module.f90:1-2"},
    )
    assert categories == {"source_organization"}
    assert result["summary"]["source_organization_changes"] == 1
    assert changes[0]["path"] == "/type_source"
    assert changes[0]["base_present"] is False
    assert changes[0]["candidate"] == "module.f90:1-2"


def test_semantic_empty_type_source_is_not_silently_ignored():
    _, categories, changes = _semantic_categories(
        {"type_source": ""}, {"type_source": None}
    )
    assert categories == {"uncertain"}
    assert changes[0]["path"] == "/type_source"
    assert changes[0]["reason"] == "value_type_change"
    assert _split_type_source("") == (None, None)


def test_semantic_malformed_type_source_preserves_whole_path():
    malformed = "module.f90:not-a-range"
    assert _split_type_source(malformed) == (malformed, None)
    _, categories, changes = _semantic_categories(
        {"type_source": malformed},
        {"type_source": "module.f90:10-20"},
    )
    assert categories == {"source_organization", "source_location"}
    assert all(change["path"] == "/type_source" for change in changes)


def test_semantic_type_source_splits_last_numeric_suffix_after_colons():
    windows_path = "C:\\source\\model:archive\\module.f90"
    assert _split_type_source(windows_path + ":12-34") == (
        windows_path, "12-34"
    )
    _, categories, changes = _semantic_categories(
        {"type_source": windows_path + ":12-34"},
        {"type_source": windows_path + ":13-35"},
    )
    assert categories == {"source_location"}
    assert changes[0]["path"] == "/type_source"


def test_semantic_duplicate_field_names_fall_back_to_positions():
    base_fields = [
        {"name": "same", "fortran_type": "integer"},
        {"name": "same", "fortran_type": "real"},
    ]
    _, categories, changes = _semantic_categories(
        {"fields": base_fields},
        {"fields": list(reversed(base_fields))},
    )
    assert categories == {"structural"}
    assert {change["path"] for change in changes} == {
        "/fields/0/fortran_type", "/fields/1/fortran_type"
    }


def test_semantic_depth_limit_reports_bounded_uncertainty():
    import json

    def nested(value):
        for _ in range(MAX_COMPARISON_DEPTH + 10):
            value = {"blocks": value}
        return value

    result, categories, changes = _semantic_categories(
        nested({"doc": "old"}), nested({"doc": "new"})
    )
    assert categories == {"uncertain"}
    assert result["summary"]["uncertain_changes"] == 1
    assert changes[0]["reason"] == "comparison_depth_limit_exceeded"
    assert changes[0]["limit"] == MAX_COMPARISON_DEPTH
    assert changes[0]["path"].startswith("/blocks/")
    assert "base" not in changes[0] and "candidate" not in changes[0]
    json.dumps(result, sort_keys=True)


def test_semantic_dict_to_list_change_is_explicitly_structural():
    _, categories, changes = _semantic_categories(
        {"repeat": {"count_field": "n"}},
        {"repeat": [{"count_field": "n"}]},
    )
    assert categories == {"structural"}
    assert changes[0]["path"] == "/repeat"
    assert changes[0]["reason"] == "schema_shape_change"
    assert (changes[0]["base_type"], changes[0]["candidate_type"]) == (
        "dict", "list"
    )


def test_semantic_list_to_dict_change_is_explicitly_structural():
    _, categories, changes = _semantic_categories(
        {"sections": [{"name": "row"}]},
        {"sections": {"name": "row"}},
    )
    assert categories == {"structural"}
    assert changes[0]["path"] == "/sections"
    assert changes[0]["reason"] == "schema_shape_change"
    assert (changes[0]["base_type"], changes[0]["candidate_type"]) == (
        "list", "dict"
    )


def test_semantic_scalar_and_container_changes_are_structural():
    for base_value, candidate_value, base_type, candidate_type in (
        ("old", {"name": "new"}, "str", "dict"),
        ("old", ["new"], "str", "list"),
        ({"name": "old"}, "new", "dict", "str"),
        (["old"], "new", "list", "str"),
    ):
        _, categories, changes = _semantic_categories(
            {"blocks": base_value}, {"blocks": candidate_value}
        )
        assert categories == {"structural"}
        assert changes[0]["path"] == "/blocks"
        assert changes[0]["reason"] == "schema_shape_change"
        assert (changes[0]["base_type"], changes[0]["candidate_type"]) == (
            base_type, candidate_type
        )


def test_semantic_non_field_list_reordering_is_structural():
    for base_list, candidate_list in (
        ([{"name": "a"}, {"name": "b"}],
         [{"name": "b"}, {"name": "a"}]),
        (["a", "a", "b"], ["a", "b", "a"]),
    ):
        _, categories, changes = _semantic_categories(
            {"sections": base_list}, {"sections": candidate_list}
        )
        assert categories == {"structural"}
        assert [change["path"] for change in changes] == ["/sections/@order"]


def test_semantic_ordering_is_deterministic_across_mapping_insertion_orders():
    import json

    base = {"files": {
        "z.dat": {"reader_line": 1, "doc": "old"},
        "a.dat": {"reader_line": 2, "doc": "old"},
    }}
    candidate = {"files": {
        "a.dat": {"doc": "new", "reader_line": 3},
        "z.dat": {"doc": "new", "reader_line": 4},
    }}
    reordered_base = {"files": {
        name: dict(reversed(list(entry.items())))
        for name, entry in reversed(list(base["files"].items()))
    }}
    reordered_candidate = {"files": {
        name: dict(reversed(list(entry.items())))
        for name, entry in reversed(list(candidate["files"].items()))
    }}
    serialize = lambda left, right: json.dumps(
        _semantic_schema_diff(left, right),
        sort_keys=True,
        ensure_ascii=False,
    )
    assert serialize(base, candidate) == serialize(base, candidate)
    assert serialize(base, candidate) == serialize(
        reordered_base, reordered_candidate
    )
