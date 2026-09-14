"""Phase 4 semantic relationships over either parser's ProjectIndex."""
from __future__ import annotations

from pathlib import Path

from swatplus_reference.parser.ast_index import build_ast_index
from swatplus_reference.parser.rich import RichStore
from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_model import (
    CallRef,
    ModuleDoc,
    ProcedureDoc,
    ProjectIndex,
    SourceLocation,
    UseRef,
)
from swatplus_reference.parser.semantic import resolve_project_calls


def _loc(path: str, line: int = 1) -> SourceLocation:
    return SourceLocation(path, line)


def _module(name: str) -> ModuleDoc:
    return ModuleDoc(name, _loc(f"{name}.f90"))


def _procedure(
    name: str,
    *,
    kind: str = "subroutine",
    module: str | None = None,
    path: str | None = None,
    parent: str | None = None,
    uses: list[UseRef] | None = None,
    calls: list[CallRef] | None = None,
) -> ProcedureDoc:
    return ProcedureDoc(
        name,
        kind,
        _loc(path or (f"{module}.f90" if module else f"{name}.f90")),
        module=module,
        parent=parent,
        uses=uses or [],
        calls=calls or [],
    )


def _call(name: str, *, kind: str = "subroutine") -> CallRef:
    return CallRef(name, f"call {name}()", _loc("caller.f90", 8), kind=kind)


def test_use_association_disambiguates_duplicate_procedure_names():
    left_module, right_module = _module("left"), _module("right")
    left = _procedure("work", module="left")
    right = _procedure("work", module="right")
    call = _call("work")
    caller = _procedure("caller", uses=[UseRef("left")], calls=[call])
    index = ProjectIndex(
        "test",
        ".",
        modules=[left_module, right_module],
        procedures=[left, right, caller],
    )

    resolve_project_calls(index)

    assert call.resolved is True
    assert call.resolved_target == left.identity
    assert call.resolution_candidates == [left.identity]
    assert left.called_by == ["caller"]
    assert right.called_by == []


def test_equally_visible_imports_fail_closed_and_report_candidate_identities():
    modules = [_module("left"), _module("right")]
    targets = [_procedure("work", module="left"), _procedure("work", module="right")]
    call = _call("work")
    caller = _procedure(
        "caller", uses=[UseRef("left"), UseRef("right")], calls=[call]
    )
    index = ProjectIndex("test", ".", modules=modules, procedures=[*targets, caller])

    resolve_project_calls(index)

    assert call.resolved is False
    assert call.resolved_target is None
    assert call.resolution_candidates == sorted(target.identity for target in targets)
    assert [flag.code for flag in caller.review_flags] == ["ambiguous_call"]
    assert all(target.called_by == [] for target in targets)

    # Re-resolution replaces its own diagnostic instead of accumulating copies.
    resolve_project_calls(index)
    assert [flag.code for flag in caller.review_flags] == ["ambiguous_call"]


def test_only_and_non_only_renames_resolve_the_local_spelling():
    module = _module("library")
    target = _procedure("remote_work", module="library")
    only_call = _call("local_only")
    broad_call = _call("local_broad")
    hidden_remote_call = _call("remote_work")
    caller = _procedure(
        "caller",
        uses=[
            UseRef("library", only=["local_only => remote_work"]),
            UseRef("library", renames=["local_broad => remote_work"]),
        ],
        calls=[only_call, broad_call, hidden_remote_call],
    )
    index = ProjectIndex("test", ".", modules=[module], procedures=[target, caller])

    resolve_project_calls(index)

    assert only_call.resolved_target == target.identity
    assert broad_call.resolved_target == target.identity
    # The non-ONLY rename hides the remote spelling, and the ONLY import does
    # not expose it either.
    assert hidden_remote_call.resolved is False
    assert target.called_by == ["caller"]


def test_same_module_definition_shadows_an_imported_name():
    local_module, imported_module = _module("local"), _module("imported")
    local = _procedure("work", module="local")
    imported = _procedure("work", module="imported")
    call = _call("work")
    caller = _procedure(
        "caller",
        module="local",
        uses=[UseRef("imported")],
        calls=[call],
    )
    index = ProjectIndex(
        "test",
        ".",
        modules=[local_module, imported_module],
        procedures=[local, imported, caller],
    )

    resolve_project_calls(index)

    assert call.resolved_target == local.identity
    assert local.called_by == ["caller"]
    assert imported.called_by == []


def test_direct_internal_procedure_shadows_same_module_definition():
    module = _module("local")
    module_target = _procedure("work", module="local")
    call = _call("work")
    host = _procedure("host", module="local", calls=[call])
    internal_target = _procedure("work", module="local", parent="host")
    index = ProjectIndex(
        "test", ".", modules=[module], procedures=[module_target, host, internal_target]
    )

    resolve_project_calls(index)

    assert call.resolved_target == internal_target.identity
    assert internal_target.called_by == ["host"]
    assert module_target.called_by == []


def test_module_use_is_host_associated_into_its_procedure():
    library = _module("library")
    client = _module("client")
    client.uses.append(UseRef("library", only=["work"]))
    target = _procedure("work", module="library")
    call = _call("work")
    caller = _procedure(
        "caller", module="client", path="client.f90", calls=[call]
    )
    index = ProjectIndex(
        "test", ".", modules=[library, client], procedures=[target, caller]
    )

    resolve_project_calls(index)

    assert call.resolved_target == target.identity
    assert target.called_by == ["caller"]


def test_call_kind_must_match_definition_kind():
    subroutine = _procedure("worker")
    function = _procedure("value", kind="function")
    wrong_subroutine = _call("value")
    wrong_function = _call("worker", kind="function")
    caller = _procedure("caller", calls=[wrong_subroutine, wrong_function])

    resolve_project_calls(
        ProjectIndex("test", ".", procedures=[subroutine, function, caller])
    )

    assert wrong_subroutine.resolved is False
    assert wrong_function.resolved is False
    assert subroutine.called_by == []
    assert function.called_by == []


def test_type_bound_call_is_not_guessed_from_its_object_name():
    mistaken_target = _procedure("worker")
    call = _call("worker%run")
    caller = _procedure("caller", calls=[call])

    resolve_project_calls(
        ProjectIndex("test", ".", procedures=[mistaken_target, caller])
    )

    assert call.resolved is False
    assert call.resolved_target is None
    assert call.resolution_candidates == []
    assert mistaken_target.called_by == []


def test_resolution_preserves_source_spelling_and_observation_identity():
    target = _procedure("worker")
    call = _call("WoRkEr")
    caller = _procedure("Caller", calls=[call])
    store = RichStore(ProjectIndex("test", ".", procedures=[target, caller]))
    before = store.call_observations()
    identity = store.call_observation_identity()

    store.resolve_calls()

    assert call.name == "WoRkEr"
    assert store.call_observations() == before
    assert store.call_observation_identity() == identity


def test_shared_resolver_operates_on_ast_built_index(tmp_path: Path):
    (tmp_path / "m.f90").write_text(
        """\
module m
contains
  subroutine caller()
    call worker()
  end subroutine caller
  subroutine worker()
  end subroutine worker
end module m
""",
        encoding="utf-8",
    )
    index = build_ast_index(BuildConfig(source_dir=tmp_path))
    caller = next(
        item for item in index.procedures if item.name.lower() == "caller"
    )
    target = next(item for item in index.procedures if item.name.lower() == "worker")
    assert caller.calls[0].resolved is False

    resolve_project_calls(index)

    assert caller.calls[0].resolved_target == target.identity
    assert target.called_by == ["caller"]


def test_call_paths_are_deterministic_maximal_identity_chains():
    leaf = _procedure("leaf")
    left = _procedure("left", calls=[_call("leaf")])
    right = _procedure("right", calls=[_call("leaf")])
    root = _procedure("root", calls=[_call("right"), _call("left")])
    index = ProjectIndex("test", ".", procedures=[root, right, leaf, left])

    resolve_project_calls(index)

    assert root.call_paths == [
        [root.identity, left.identity, leaf.identity],
        [root.identity, right.identity, leaf.identity],
    ]
    assert left.call_paths == [[left.identity, leaf.identity]]
    assert right.call_paths == [[right.identity, leaf.identity]]
    assert leaf.call_paths == []


def test_call_paths_retain_one_cycle_closure_and_terminate():
    call_b = _call("b")
    call_a = _call("a")
    a = _procedure("a", calls=[call_b])
    b = _procedure("b", calls=[call_a])
    index = ProjectIndex("test", ".", procedures=[a, b])

    resolve_project_calls(index)

    assert a.call_paths == [[a.identity, b.identity, a.identity]]
    assert b.call_paths == [[b.identity, a.identity, b.identity]]


def test_recursive_call_path_is_a_single_closing_edge():
    recursive_call = _call("walk")
    procedure = _procedure("walk", calls=[recursive_call])

    resolve_project_calls(ProjectIndex("test", ".", procedures=[procedure]))

    assert procedure.call_paths == [[procedure.identity, procedure.identity]]


def test_duplicate_call_observations_create_one_derived_path_without_mutation():
    target = _procedure("worker")
    first = _call("worker")
    second = _call("worker")
    second.location = _loc("caller.f90", 9)
    caller = _procedure("caller", calls=[first, second])
    store = RichStore(ProjectIndex("test", ".", procedures=[caller, target]))
    observations = store.call_observations()

    store.resolve_calls()

    assert caller.call_paths == [[caller.identity, target.identity]]
    assert store.call_observations() == observations


def test_unresolved_and_ambiguous_calls_create_no_path_edges():
    modules = [_module("left"), _module("right")]
    targets = [_procedure("work", module="left"), _procedure("work", module="right")]
    caller = _procedure(
        "caller",
        uses=[UseRef("left"), UseRef("right")],
        calls=[_call("work"), _call("missing")],
    )
    index = ProjectIndex("test", ".", modules=modules, procedures=[caller, *targets])

    resolve_project_calls(index)

    assert caller.call_paths == []


# ==========================================================================
# Phase 4 slice 3: shared state derived from the index, not from a re-read
# ==========================================================================


def _dataflow(tmp_path, source: str, procedure: str = "s"):
    """Scan one file and return (reads, writes) for *procedure*."""

    (tmp_path / "m.f90").write_text(source, encoding="utf-8")
    store = RichStore.build(tmp_path)
    store.resolve_calls()
    found = next(p for p in store.index.procedures if p.name == procedure)
    return found.reads, found.writes


def test_shared_state_separates_reads_from_writes(tmp_path):
    reads, writes = _dataflow(
        tmp_path,
        """\
module shared_state
  real :: albday = 0.
  real :: petval = 0.
  real :: total = 0.
end module shared_state

subroutine s()
  use shared_state
  real :: cover
  cover = 1.
  albday = 0.23 * petval
  total = total + albday
end subroutine s
""",
    )
    # `albday` and `total` are written; `petval` is only read. A name written is
    # not also reported as a plain read of itself, so `total` is not in reads.
    assert writes == ["albday", "total"]
    assert reads == ["petval"]


def test_a_local_never_masquerades_as_shared_state(tmp_path):
    reads, writes = _dataflow(
        tmp_path,
        """\
module shared_state
  real :: albday = 0.
end module shared_state

subroutine s()
  use shared_state
  real :: albday
  albday = 1.
end subroutine s
""",
    )
    # The procedure declares its own `albday`, shadowing the module's.
    assert (reads, writes) == ([], [])


def test_a_use_import_is_not_a_read(tmp_path):
    """`use hru_module, only: hru` reads nothing -- it imports a name.

    A line-by-line reading treats `use` as a keyword line and counts every
    identifier on it as a read, so every imported name became a read of shared
    state whether or not the procedure ever touched it.
    """

    reads, writes = _dataflow(
        tmp_path,
        """\
module hru_module
  real :: hru = 0.
  real :: irrn = 0.
end module hru_module

subroutine s()
  use hru_module, only : hru, irrn
  real :: x
  x = 1.
end subroutine s
""",
    )
    assert (reads, writes) == ([], [])


def test_identifiers_inside_a_format_literal_are_not_reads(tmp_path):
    """`100 format (1x,'   hru','   day')` reads no variable.

    The identifiers live inside quoted literals. A reading that scans the line
    for identifiers without tracking quotes counts them as shared-state reads.
    """

    reads, writes = _dataflow(
        tmp_path,
        """\
module hru_module
  real :: hru = 0.
  real :: day = 0.
end module hru_module

subroutine s()
  use hru_module
  integer :: n
  n = 1
100 format (1x,'         hru','         day')
end subroutine s
""",
    )
    assert (reads, writes) == ([], [])


def test_semicolon_chained_assignments_are_all_writes(tmp_path):
    """`a = 0; b = 0; c = 0` writes three variables and reads none.

    Matching one assignment per physical line finds only `a`, and counts the
    remainder of the line as its right-hand side -- so `b` and `c` were recorded
    as reads of the very variables they assign.
    """

    reads, writes = _dataflow(
        tmp_path,
        """\
module flags
  integer :: gwflag_day = 0
  integer :: gwflag_mon = 0
  integer :: gwflag_yr = 0
end module flags

subroutine s()
  use flags
  gwflag_day = 0; gwflag_mon = 0; gwflag_yr = 0
end subroutine s
""",
    )
    assert writes == ["gwflag_day", "gwflag_mon", "gwflag_yr"]
    assert reads == []


def test_a_host_does_not_absorb_its_contained_procedures_state(tmp_path):
    """A host procedure's line span covers the procedures it contains.

    Reading that span line by line credits the host with everything its
    contained procedures touch. The contained procedure is its own documented
    symbol with its own facts, so the access belongs there.
    """

    source = """\
module shared_state
  real :: albday = 0.
  real :: petval = 0.
end module shared_state

subroutine s()
  use shared_state
  real :: x
  x = 1.
contains
  subroutine inner()
    albday = petval
  end subroutine inner
end subroutine s
"""
    host_reads, host_writes = _dataflow(tmp_path, source, "s")
    inner_reads, inner_writes = _dataflow(tmp_path, source, "inner")

    assert (host_reads, host_writes) == ([], [])
    assert inner_writes == ["albday"]
    assert inner_reads == ["petval"]


def test_a_continued_statement_is_read_as_one_statement(tmp_path):
    """A statement split across lines contributes its whole right-hand side.

    Classifying each physical line on its own loses the continuation: the
    fragment carries no assignment, so its identifiers were attributed by the
    fallback rule instead of as reads of the statement they belong to.
    """

    reads, writes = _dataflow(
        tmp_path,
        """\
module shared_state
  real :: albday = 0.
  real :: petval = 0.
  real :: snomlt = 0.
end module shared_state

subroutine s()
  use shared_state
  albday = petval + &
           snomlt
end subroutine s
""",
    )
    assert writes == ["albday"]
    assert reads == ["petval", "snomlt"]


def test_both_parsers_derive_the_same_shared_state(tmp_path):
    """The derivation reads the index, so either parser's index yields the same.

    This is the property that makes the annotation shareable at all: it consumes
    records, not source text, so the AST path gets it without reimplementation.
    """

    (tmp_path / "m.f90").write_text(
        """\
module shared_state
  real :: albday = 0.
  real :: petval = 0.
end module shared_state

subroutine s()
  use shared_state
  real :: cover
  cover = 1.
  albday = 0.23 * petval * cover
end subroutine s
""",
        encoding="utf-8",
    )
    scanner = RichStore.build(tmp_path)
    scanner.resolve_calls()

    from swatplus_reference.parser.semantic import annotate_project_dataflow

    ast_index = build_ast_index(BuildConfig(source_dir=tmp_path))
    annotate_project_dataflow(ast_index)

    scanned = next(p for p in scanner.index.procedures if p.name == "s")
    walked = next(p for p in ast_index.procedures if p.name == "s")
    assert (scanned.reads, scanned.writes) == (["petval"], ["albday"])
    assert (walked.reads, walked.writes) == (scanned.reads, scanned.writes)


def test_derived_shared_state_stays_out_of_the_frozen_export(tmp_path):
    """`reads`/`writes` are internal: the v3 wire shape must not grow."""

    from swatplus_reference.parser.rich import _export_field_names
    from swatplus_reference.parser.schema_model import ProcedureDoc, ProgramDoc

    for record_type in (ProcedureDoc, ProgramDoc):
        exported = _export_field_names(record_type)
        assert "reads" not in exported
        assert "writes" not in exported
