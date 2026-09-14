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
        "site_name: test\ndocs_dir: docs\nsite_dir: site\n",
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
