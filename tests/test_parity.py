"""Phase 6: the field-level parity harness.

The harness is the thing cutover rests on, so these tests care about two
properties above all:

* it **reports agreement honestly** -- an approved correction is listed, not
  normalised away; and
* it **actually fails** when something new diverges. A harness that cannot go
  red is worse than no harness, because it reads as evidence.
"""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from swatplus_reference.parser.ast_index import build_ast_index
from swatplus_reference.parser.parity import (
    APPROVED_CORRECTIONS,
    compare_indexes,
    format_report,
)
from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner
from swatplus_reference.parser.semantic import (
    annotate_project_dataflow,
    resolve_project_calls,
)


PINNED_SOURCE = (
    Path(__file__).resolve().parents[1] / "external" / "swatplus-cb442f7c05fc" / "src"
)


def _semantic(index):
    resolve_project_calls(index)
    annotate_project_dataflow(index)
    return index


def _both(source_dir: Path):
    config = BuildConfig(source_dir=source_dir)
    return (
        _semantic(build_ast_index(config)),
        _semantic(FortranScanner(config).scan()),
    )


# --- behaviour on a small, fully-agreeing tree ----------------------------


@pytest.fixture
def agreeing(tmp_path):
    (tmp_path / "m.f90").write_text(
        """\
module shared_state
  real :: albday = 0.
  real :: petval = 0.
end module shared_state

subroutine s(a)
  use shared_state
  real :: a
  integer :: i
  do i = 1, 3
    if (a > 0.) then
      albday = petval * a
    else
      albday = 0.
    end if
  end do
  call helper(a)
end subroutine s
""",
        encoding="utf-8",
    )
    return _both(tmp_path)


def test_two_agreeing_parsers_report_no_difference(agreeing):
    report = compare_indexes(*agreeing)
    assert report.failures() == []
    assert report.unexpected == []
    assert report.approved == []
    procedures = next(c for c in report.categories if c.name == "procedures")
    assert procedures.shared == 1
    assert procedures.identical == 1


def test_a_new_difference_is_unexpected_and_fails(agreeing):
    """The harness must go red when something diverges that nobody approved."""

    ast, rich = agreeing
    rich = copy.deepcopy(rich)
    # Change a byte-sensitive field on one statement.
    rich.procedures[0].control_steps[0].summary = "tampered"

    report = compare_indexes(ast, rich)
    assert report.failures(), "a changed summary must fail the harness"
    (difference,) = report.unexpected
    assert difference.category == "procedures"
    assert difference.field == "control_steps"
    assert difference.approved is False
    assert "control_steps" in format_report(report)
    assert "UNEXPECTED" in format_report(report)


def test_a_record_only_one_parser_found_fails(agreeing):
    ast, rich = agreeing
    rich = copy.deepcopy(rich)
    rich.procedures = []

    report = compare_indexes(ast, rich)
    problems = report.failures()
    assert any("only in fparser2" in problem for problem in problems)


def test_a_missing_record_fails_in_the_other_direction(agreeing):
    ast, rich = agreeing
    ast = copy.deepcopy(ast)
    ast.procedures = []

    report = compare_indexes(ast, rich)
    problems = report.failures()
    assert any("missing from fparser2" in problem for problem in problems)


def test_case_differences_in_names_are_not_differences(agreeing):
    """Fortran is case-insensitive, so a name's case is not a disagreement."""

    ast, rich = agreeing
    rich = copy.deepcopy(rich)
    procedure = rich.procedures[0]
    procedure.args = [arg.upper() for arg in procedure.args]
    procedure.uses[0].module = procedure.uses[0].module.upper()

    report = compare_indexes(ast, rich)
    assert report.failures() == []


def test_byte_sensitive_fields_are_never_normalised(agreeing):
    """Raw text, summaries, spans and I/O fields are compared verbatim.

    The plan names these as byte-sensitive contracts that the harness may not
    normalise, so a whitespace-only change in any of them must still fail.
    """

    ast, _ = agreeing
    for mutate in (
        lambda p: setattr(p.control_steps[0], "raw", p.control_steps[0].raw + " "),
        lambda p: setattr(p.assignments[0], "expression", p.assignments[0].expression + " "),
        lambda p: setattr(p.variables[0], "declaration", p.variables[0].declaration + " "),
        lambda p: setattr(p.location, "end_line", (p.location.end_line or 0) + 1),
    ):
        tampered = copy.deepcopy(ast)
        mutate(tampered.procedures[0])
        report = compare_indexes(tampered, ast)
        assert report.failures(), mutate


# --- the pinned tree ------------------------------------------------------


@pytest.fixture(scope="module")
def pinned_report():
    if not PINNED_SOURCE.exists():
        pytest.skip("pinned SWAT+ source tree not present")
    return compare_indexes(*_both(PINNED_SOURCE))


def test_pinned_tree_has_no_unexpected_difference(pinned_report):
    """The Phase 6 exit gate, as one assertion.

    Every difference between the two parsers on the pinned tree is an approved,
    explained correction. Anything else fails, and the message says what.
    """

    assert pinned_report.failures() == []


def test_pinned_tree_loses_no_record_in_either_direction(pinned_report):
    assert pinned_report.missing_records() == []
    for category in pinned_report.categories:
        assert category.ast_only == [], category.name
        assert category.rich_only == [], category.name


def test_pinned_tree_category_totals(pinned_report):
    totals = {c.name: (c.shared, c.identical) for c in pinned_report.categories}
    assert totals["modules"] == (66, 66)
    assert totals["types"] == (514, 514)
    assert totals["procedures"] == (734, 722)
    # Lower than before cross-file unit binding: operations that each carried
    # their own `unit_<unit>` sentinel now join the file they actually belong to.
    assert totals["io_files"] == (986, 983)
    # Higher for the same reason: a family whose writes all sat behind sentinels
    # now has a named file to belong to.
    assert totals["output_families"] == (92, 92)


def test_every_pinned_difference_carries_its_explanation(pinned_report):
    """A correction is recorded with a reason, not silently tolerated."""

    assert pinned_report.approved, "expected the documented corrections to appear"
    for difference in pinned_report.approved:
        assert difference.reason
        assert len(difference.reason) > 40, difference

    differing_fields = {(d.category, d.field) for d in pinned_report.approved}
    assert differing_fields == {
        ("procedures", "assignments"),
        ("procedures", "control_steps"),
        ("procedures", "io"),
        ("procedures", "reads"),
        ("procedures", "writes"),
        ("io_files", "operations"),
    }


def test_approved_corrections_are_not_a_blanket_exemption(pinned_report):
    """Each correction names the files it covers, so a new file still fails.

    This is what stops the table from becoming a way to make parity look better
    than it is: approval is scoped to a category, a field and an owner.
    """

    for correction in APPROVED_CORRECTIONS:
        assert correction.owners, correction
        assert correction.fields, correction
        assert "*" not in correction.owners

    # Every approved difference on the pinned tree falls inside a declared set.
    for difference in pinned_report.approved:
        assert any(
            difference.category == c.category
            and difference.field in c.fields
            and difference.owner in c.owners
            for c in APPROVED_CORRECTIONS
        ), difference


def test_no_approved_correction_is_stale(pinned_report):
    """Every declared correction is still doing work.

    A correction whose files no longer differ is an exemption nobody needs, and
    leaving it in place would quietly cover a future regression in that file.
    """

    observed = {(d.category, d.field, d.owner) for d in pinned_report.approved}
    for correction in APPROVED_CORRECTIONS:
        used = {
            (correction.category, f, o)
            for f in correction.fields
            for o in correction.owners
        } & observed
        assert used, f"no longer needed: {correction.category} {sorted(correction.fields)}"


# --- Phase 7: consumers run on either engine ------------------------------


def test_rich_store_builds_from_either_engine(tmp_path):
    """`RichStore.build` selects the parser; everything after it is shared.

    That sharing is what makes the Phase 7 gate meaningful: running the
    consumers on the fparser2 index only proves something if the index travels
    the same enrichment path the scanner's does.
    """

    from swatplus_reference.parser.rich import AST_ENGINE, SCANNER_ENGINE, RichStore

    (tmp_path / "m.f90").write_text(
        """\
module shared_state
  real :: albday = 0.
end module shared_state

subroutine s(a)
  use shared_state
  real :: a
  albday = a
  call helper(a)
end subroutine s
""",
        encoding="utf-8",
    )
    scanner = RichStore.build(tmp_path, engine=SCANNER_ENGINE)
    walked = RichStore.build(tmp_path, engine=AST_ENGINE)

    report = compare_indexes(walked.index, scanner.index)
    assert report.failures() == []

    # Both carry the enrichment, not just the raw parse.
    for store in (scanner, walked):
        assert store.scan_call_identity
        assert store.index.metadata.get("swatplus_reference_outside_state_refs")
        procedure = store.index.procedures[0]
        assert procedure.identity
        assert procedure.writes == ["albday"]


def test_an_unknown_engine_is_refused(tmp_path):
    from swatplus_reference.parser.rich import RichStore

    (tmp_path / "m.f90").write_text("subroutine s()\nend subroutine s\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unknown parser engine"):
        RichStore.build(tmp_path, engine="guess")


def test_documentation_projects_from_the_ast_engine(tmp_path):
    """The projected fact store is the same whichever parser produced it."""

    from swatplus_reference.parser.documentation import parse_documentation
    from swatplus_reference.parser.rich import AST_ENGINE, SCANNER_ENGINE

    (tmp_path / "m.f90").write_text(
        """\
module shared_state
  real :: albday = 0.
end module shared_state

subroutine s(a)
  use shared_state
  real :: a
  integer :: eof
  albday = a
  open (107, file = "demo.in")
  read (107,*,iostat=eof) a
  close (107)
end subroutine s
""",
        encoding="utf-8",
    )
    scanned, _ = parse_documentation(tmp_path, "test", engine=SCANNER_ENGINE)
    walked, _ = parse_documentation(tmp_path, "test", engine=AST_ENGINE)

    assert walked.symbols.keys() == scanned.symbols.keys()
    for name, symbol in walked.symbols.items():
        other = scanned.symbols[name]
        assert (symbol.start_line, symbol.end_line) == (other.start_line, other.end_line), name
        assert symbol.source_hash == other.source_hash, name
        assert [v.name for v in symbol.locals] == [v.name for v in other.locals], name
        assert symbol.reads == other.reads and symbol.writes == other.writes, name


# --- Phase 8: the cutover -------------------------------------------------


def test_fparser2_is_the_default_engine():
    """The cutover, as one assertion.

    Everything downstream reads this default, so it is the single place the
    switch actually happens.
    """

    from swatplus_reference.parser.rich import AST_ENGINE, DEFAULT_ENGINE

    assert DEFAULT_ENGINE == AST_ENGINE == "fparser2"


def test_every_entry_point_shares_the_default():
    """No entry point may carry its own idea of the default.

    Two defaults out of sync is how a cutover looks finished while half the
    pipeline still runs the old parser -- the baseline kept reporting
    `fortran-scanner-v6` for exactly that reason.
    """

    import inspect

    from swatplus_reference.parser.documentation import parse_documentation
    from swatplus_reference.parser.rich import DEFAULT_ENGINE, RichStore

    for func in (RichStore.build, RichStore.from_index, parse_documentation):
        default = inspect.signature(func).parameters["engine"].default
        assert default == DEFAULT_ENGINE, func.__qualname__


def test_the_scanner_is_still_selectable(tmp_path):
    """The compatibility period: the legacy engine must remain reachable."""

    from swatplus_reference.parser.rich import SCANNER_ENGINE, RichStore

    (tmp_path / "m.f90").write_text(
        "subroutine s()\n  integer :: i\n  i = 1\nend subroutine s\n", encoding="utf-8"
    )
    store = RichStore.build(tmp_path, engine=SCANNER_ENGINE)
    assert store.engine == SCANNER_ENGINE
    assert store.index.procedures[0].name == "s"


def test_config_selects_the_engine(tmp_path):
    from swatplus_reference.source.config import load_config

    base = (Path(__file__).resolve().parents[1] / "swatref.toml").read_text()
    default = tmp_path / "default.toml"
    default.write_text(base, encoding="utf-8")
    assert load_config(default).docs_engine == "fparser2"

    legacy = tmp_path / "legacy.toml"
    legacy.write_text(base.replace("[docs]\n", '[docs]\nengine = "scanner"\n', 1), encoding="utf-8")
    assert load_config(legacy).docs_engine == "scanner"


def test_each_engine_stamps_its_own_identity(tmp_path):
    """A snapshot says which parser produced it, so caches never cross.

    `has_current_contract` compares against the engine asked about, so a store
    built by one engine is rebuilt rather than reused when the other is
    configured -- the guard that stops a stale cache serving pre-cutover facts.
    """

    from swatplus_reference.parser.rich import (
        AST_ENGINE,
        SCANNER_ENGINE,
        RichStore,
        parser_version,
    )

    (tmp_path / "m.f90").write_text(
        "subroutine s()\n  integer :: i\n  i = 1\nend subroutine s\n", encoding="utf-8"
    )
    assert parser_version(AST_ENGINE) != parser_version(SCANNER_ENGINE)

    for engine in (AST_ENGINE, SCANNER_ENGINE):
        store = RichStore.build(tmp_path, engine=engine)
        saved = tmp_path / f"{engine}.json"
        store.save(saved, provenance={"resolved_commit": "0" * 40})

        reloaded = RichStore.load(saved)
        assert reloaded.engine == engine
        assert reloaded.has_current_contract(engine), engine
        other = SCANNER_ENGINE if engine == AST_ENGINE else AST_ENGINE
        assert not reloaded.has_current_contract(other), engine

        roundtrip = tmp_path / f"{engine}-roundtrip.json"
        reloaded.save(roundtrip, provenance={"resolved_commit": "0" * 40})
        assert RichStore.load(roundtrip).has_current_contract(engine), engine
