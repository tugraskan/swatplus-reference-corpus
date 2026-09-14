"""Phase 3 category 1-3: structural facts read off the fparser2 AST.

Two kinds of test live here.

*Unit tests* pin the behaviour the AST path is supposed to get right *because*
it reads a parse tree rather than matching regexes in source order: which scope
owns a declaration, where a scope really ends, and the spellings that mislead a
line-oriented reader.

*Parity tests* assert that on the pinned SWAT+ tree the AST path produces the
same records as the rich scanner, field for field. Parity is the point: the
migration only proceeds if the new path can be shown to lose nothing, and
"lose nothing" has to mean byte equality, not similar counts.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from swatplus_reference.parser.ast_index import build_ast_index
from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner


PINNED_SOURCE = (
    Path(__file__).resolve().parents[1] / "external" / "swatplus-cb442f7c05fc" / "src"
)

# Nothing in the pinned tree is unparseable any more. `gwflow_floodplain.f90`
# and `gwflow_heat.f90` spell a negation as `expr*-1`, which the standard does
# not allow and gfortran accepts; the AST path parenthesises the signed operand
# in the text it hands fparser2 and reads every byte it reports from the
# unchanged source. They stay listed as regression cases in
# reports/parser-baseline/regression-cases.json.
NORMALIZED_FILES = {"gwflow_floodplain.f90", "gwflow_heat.f90"}


def build(tmp_path: Path, name: str, source: str):
    (tmp_path / name).write_text(source, encoding="utf-8")
    return build_ast_index(BuildConfig(source_dir=tmp_path))


# --- scope discovery -------------------------------------------------------


def test_module_procedures_and_types_are_separate_records(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  type :: pt
    real :: x
  end type pt
  real :: mv
contains
  subroutine s(a)
    real :: a
  end subroutine s
end module m
""",
    )
    assert [m.name for m in index.modules] == ["m"]
    assert [p.name for p in index.procedures] == ["s"]
    assert [t.name for t in index.types] == ["pt"]

    module = index.modules[0]
    # The module owns `mv` only. `x` belongs to the type and `a` to the
    # subroutine, which is exactly the split a `type_stack` has to reconstruct.
    assert [v.name for v in module.variables] == ["mv"]
    assert [v.name for v in index.types[0].components] == ["x"]
    assert [v.name for v in index.procedures[0].variables] == ["a"]
    assert module.procedures == ["s"]
    assert module.types == ["pt"]


def test_scope_end_line_comes_from_the_end_statement(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
contains
  subroutine s()
    integer :: i
    i = 1
  end subroutine s
end module m
""",
    )
    proc = index.procedures[0]
    assert (proc.location.line, proc.location.end_line) == (3, 6)
    assert (index.modules[0].location.line, index.modules[0].location.end_line) == (1, 7)


def test_typed_function_is_named_after_the_function_not_its_result_type(tmp_path):
    """`type(box) function make(x)` declares `make`, not `box`.

    Reading the first `Name` in the statement -- which is what a walk over the
    node does -- returns the result type and names the procedure after it. The
    declared name sits in a fixed child position, so it is read structurally.
    """

    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  type :: box
    real :: v
  end type box
contains
  type(box) function make(x)
    real :: x
    make%v = x
  end function make
end module m
""",
    )
    assert [p.name for p in index.procedures] == ["make"]
    assert index.procedures[0].kind == "function"
    assert index.procedures[0].args == ["x"]


def test_function_prefixes_do_not_confuse_the_name(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
contains
  pure elemental integer function g(y)
    integer :: y
    g = y
  end function g
  recursive subroutine r(n)
    integer :: n
    if (n > 0) call r(n - 1)
  end subroutine r
end module m
""",
    )
    assert sorted(p.name for p in index.procedures) == ["g", "r"]


def test_interface_body_declarations_do_not_leak_into_the_module(tmp_path):
    """An interface body describes a procedure defined elsewhere.

    Its dummy-argument declarations are part of that description. fparser2
    represents the body as a `Subroutine_Body`, which is not a subprogram, so a
    naive walk up the parent chain lands on the module and files `z` as a
    module variable.
    """

    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  interface
    subroutine iface_sub(z)
      real :: z
    end subroutine iface_sub
  end interface
  real :: mv
end module m
""",
    )
    assert [v.name for v in index.modules[0].variables] == ["mv"]
    # The interface body is a declaration, not a definition: no procedure record.
    assert index.procedures == []


def test_procedure_local_derived_type_is_scoped_to_the_procedure(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
contains
  subroutine s()
    type :: local_t
      real :: q
    end type local_t
    integer :: i
    i = 0
  end subroutine s
end module m
""",
    )
    (dtype,) = index.types
    assert dtype.name == "local_t"
    assert dtype.module == "m"
    assert dtype.parent == "s"
    assert [v.name for v in dtype.components] == ["q"]
    # `q` is the type's, so the procedure keeps only its own local.
    assert [v.name for v in index.procedures[0].variables] == ["i"]


def test_contained_procedure_records_its_host(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
contains
  subroutine outer()
    integer :: i
    i = 1
  contains
    subroutine inner()
      integer :: j
      j = 2
    end subroutine inner
  end subroutine outer
end module m
""",
    )
    by_name = {p.name: p for p in index.procedures}
    assert by_name["outer"].parent is None
    assert by_name["inner"].parent == "outer"
    assert by_name["inner"].module == "m"
    # A contained procedure is not a member of the module's public surface.
    assert index.modules[0].procedures == ["outer"]
    assert [v.name for v in by_name["outer"].variables] == ["i"]
    assert [v.name for v in by_name["inner"].variables] == ["j"]


def test_program_is_its_own_record(tmp_path):
    index = build(
        tmp_path,
        "p.f90",
        """\
program p
  use m, only: s
  integer :: i
  i = 1
end program p
""",
    )
    (program,) = index.programs
    assert program.name == "p"
    assert (program.location.line, program.location.end_line) == (1, 5)
    assert [u.module for u in program.uses] == ["m"]
    assert index.files[0].programs == ["p"]


# --- byte-exact source text ------------------------------------------------


def test_declaration_text_comes_from_source_not_from_the_node(tmp_path):
    """fparser2 upper-cases and re-spaces when it prints a node.

    `real :: mv = 1.` prints as `REAL :: mv = 1.`. The schema resolver matches
    on these bytes, so the declaration has to be read from the physical source
    through the Phase 2 layer, never from `str(node)`.
    """

    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  real :: mv = 1.
end module m
""",
    )
    (var,) = index.modules[0].variables
    # Lower-case, as written. The doubled space is the shared declaration
    # helper's own output for an attribute-less declaration, and the pinned-tree
    # parity tests below show both parsers produce it identically.
    assert var.declaration == "real  :: mv = 1."
    assert "REAL" not in var.declaration
    assert var.vartype == "real"
    assert var.initial == "1."


def test_continued_declaration_keeps_its_full_physical_span(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  real, dimension(3) :: bcod = &
       (/ 1., 2., 3. /)
end module m
""",
    )
    (var,) = index.modules[0].variables
    assert (var.location.line, var.location.end_line) == (2, 3)
    assert "(/ 1., 2., 3. /)" in var.declaration


def test_inline_component_documentation_is_attached(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  !> the point type
  type :: pt
    real :: x = 0.  !mm |the x thing
  end type pt
end module m
""",
    )
    (dtype,) = index.types
    assert dtype.doc == "the point type"
    (component,) = dtype.components
    assert component.doc == "mm |the x thing"
    assert component.initial == "0."


def test_a_bang_inside_a_literal_is_not_documentation(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  character(len=20) :: msg = '! not a comment'  ! but this is
end module m
""",
    )
    (var,) = index.modules[0].variables
    assert var.initial == "'! not a comment'"
    assert var.doc == "but this is"


def test_use_only_list_is_read_from_source(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  use iso_fortran_env, only: real64, int32
  use other_mod
end module m
""",
    )
    uses = index.modules[0].uses
    assert [(u.module, u.only) for u in uses] == [
        ("iso_fortran_env", ["real64", "int32"]),
        ("other_mod", []),
    ]


def test_structural_statements_after_semicolons_keep_their_own_source(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  use first_mod, only: first_name; use second_mod, only: second_name
  integer :: first; real :: second
contains
  subroutine s()
    logical :: third; character(len=4) :: fourth
  end subroutine s
end module m
""",
    )

    module = index.modules[0]
    assert [(u.module, u.only) for u in module.uses] == [
        ("first_mod", ["first_name"]),
        ("second_mod", ["second_name"]),
    ]
    assert [(v.name, v.vartype) for v in module.variables] == [
        ("first", "integer"),
        ("second", "real"),
    ]
    assert [(v.name, v.vartype) for v in index.procedures[0].variables] == [
        ("third", "logical"),
        ("fourth", "character(len=4)"),
    ]
    assert index.review_flags == []


def test_use_rename_list_is_preserved_without_becoming_an_only_list(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  use source_mod, local_name => remote_name
end module m
""",
    )

    (use,) = index.modules[0].uses
    assert use.module == "source_mod"
    assert use.only == []
    assert use.renames == ["local_name => remote_name"]
    assert index.review_flags == []


# --- identity --------------------------------------------------------------


def test_records_carry_scope_qualified_identities(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  type :: salt_balance
    real :: v
  end type salt_balance
contains
  subroutine salt_balance_calc()
    integer :: i
    i = 1
  end subroutine salt_balance_calc
end module m
""",
    )
    assert index.modules[0].identity == "module:m:m.f90"
    assert index.types[0].identity == "type:salt_balance:m.f90:m"
    assert index.procedures[0].identity == "subroutine:salt_balance_calc:m.f90:m"


# --- diagnostics -----------------------------------------------------------


def test_a_file_fparser_rejects_is_flagged_and_keeps_its_inventory_entry(tmp_path):
    """A file the parser still cannot read degrades visibly.

    `q*-b(1)` is deliberately outside the normalisation's scope: the
    parenthesis belongs around the whole reference, and wrapping only the name
    would give `q*(-b)(1)`. So this file still fails, which is what keeps the
    degradation path exercised now that the pinned tree has nothing unparseable
    left in it.
    """

    index = build(
        tmp_path,
        "bad.f90",
        """\
subroutine bad(q, b)
  real :: q, b(3)
  q = q*-b(1)
end subroutine bad
""",
    )
    # The file stays in the inventory even though it yields no facts, so the
    # degradation is visible rather than a silently missing file.
    assert [f.path for f in index.files] == ["bad.f90"]
    assert index.procedures == []
    (flag,) = index.review_flags
    assert flag.code == "ast_parse_failed"
    assert flag.severity == "error"
    assert flag.target == "bad.f90"


def test_a_declaration_the_source_layer_cannot_read_is_flagged(tmp_path):
    """The AST says there is a declaration here; `parse_declaration` disagrees.

    The shared pattern spans one level of nesting inside a character length, so
    `character(len=len(str))` reads -- but `character(len=max(len(a),len(b)))`
    nests twice and still does not. The variable is lost by both parsers; only
    the AST path can notice, because only it has a second opinion about whether
    a declaration exists at all. That second opinion is the point of this test,
    not the particular spelling that defeats the pattern.
    """

    index = build(
        tmp_path,
        "u.f90",
        """\
function widest(a, b) result(deep)
  character(len=*), intent(in) :: a, b
  character(len=max(len(a),len(b))) :: deep
  deep = a
end function widest
""",
    )
    codes = [f.code for f in index.review_flags]
    assert codes == ["ast_declaration_unreadable"]
    flag = index.review_flags[0]
    assert flag.location is not None
    assert (flag.location.path, flag.location.line) == ("u.f90", 3)
    # The readable declaration on the line above is still captured.
    assert [v.name for v in index.procedures[0].variables] == ["a", "b"]


def test_a_clean_file_produces_no_diagnostics(tmp_path):
    index = build(
        tmp_path,
        "m.f90",
        """\
module m
  real :: mv
contains
  subroutine s(a)
    real :: a
    mv = a
  end subroutine s
end module m
""",
    )
    assert index.review_flags == []


# --- parity against the rich scanner on the pinned tree --------------------


@pytest.fixture(scope="module")
def pinned_pair():
    if not PINNED_SOURCE.exists():
        pytest.skip("pinned SWAT+ source tree not present")
    from swatplus_reference.parser.semantic import (
        annotate_project_dataflow,
        resolve_project_calls,
    )

    config = BuildConfig(source_dir=PINNED_SOURCE)
    ast_index = build_ast_index(config)
    rich_index = FortranScanner(config).scan()
    # The semantic layer is what the parity tests below compare for calls and
    # shared state; deriving it here keeps both indexes at the same stage.
    for index in (ast_index, rich_index):
        resolve_project_calls(index)
        annotate_project_dataflow(index)
    return ast_index, rich_index


def _variable_key(variable):
    return (
        variable.name.lower(),
        variable.declaration,
        variable.vartype,
        variable.initial,
        variable.doc,
        variable.location.path,
        variable.location.line,
        variable.location.end_line,
    )


def _use_key(use):
    return (
        use.module.lower(),
        tuple(name.lower() for name in use.only),
        tuple(name.lower() for name in use.renames),
        use.intrinsic,
        use.location.path if use.location else None,
        use.location.line if use.location else None,
    )


def _paired(ast_records, rich_records, key):
    ast_by_key = {key(r): r for r in ast_records}
    rich_by_key = {key(r): r for r in rich_records}
    shared = ast_by_key.keys() & rich_by_key.keys()
    return ast_by_key, rich_by_key, sorted(shared)


def test_pinned_tree_symbol_inventories_match(pinned_pair):
    ast, rich = pinned_pair

    def keys(records, kind):
        return {
            (r.location.path, r.name.lower())
            for r in records
        }

    for label, ast_records, rich_records in [
        ("modules", ast.modules, rich.modules),
        ("procedures", ast.procedures, rich.procedures),
        ("types", ast.types, rich.types),
        ("programs", ast.programs, rich.programs),
    ]:
        assert keys(ast_records, label) == keys(rich_records, label), label


def test_pinned_tree_procedure_facts_match(pinned_pair):
    ast, rich = pinned_pair
    key = lambda p: (p.location.path, p.name.lower(), p.kind, p.location.line)
    ast_by_key, rich_by_key, shared = _paired(ast.procedures, rich.procedures, key)
    assert len(shared) > 700

    for k in shared:
        a, r = ast_by_key[k], rich_by_key[k]
        assert [x.lower() for x in a.args] == [x.lower() for x in r.args], k
        assert (a.module or "").lower() == (r.module or "").lower(), k
        assert (a.parent or "").lower() == (r.parent or "").lower(), k
        assert a.doc == r.doc, k
        assert [_variable_key(v) for v in a.variables] == [
            _variable_key(v) for v in r.variables
        ], k
        assert [_use_key(u) for u in a.uses] == [_use_key(u) for u in r.uses], k


def test_pinned_tree_derived_type_facts_match(pinned_pair):
    ast, rich = pinned_pair
    key = lambda t: (t.location.path, t.name.lower(), t.location.line)
    ast_by_key, rich_by_key, shared = _paired(ast.types, rich.types, key)
    assert len(shared) > 500

    for k in shared:
        a, r = ast_by_key[k], rich_by_key[k]
        assert (a.module or "").lower() == (r.module or "").lower(), k
        assert (a.parent or "").lower() == (r.parent or "").lower(), k
        assert a.doc == r.doc, k
        assert [_variable_key(v) for v in a.components] == [
            _variable_key(v) for v in r.components
        ], k


def test_pinned_tree_module_facts_match(pinned_pair):
    ast, rich = pinned_pair
    key = lambda m: (m.location.path, m.name.lower(), m.location.line)
    ast_by_key, rich_by_key, shared = _paired(ast.modules, rich.modules, key)
    assert len(shared) == 66

    for k in shared:
        a, r = ast_by_key[k], rich_by_key[k]
        assert a.doc == r.doc, k
        assert [x.lower() for x in a.procedures] == [x.lower() for x in r.procedures], k
        assert [x.lower() for x in a.types] == [x.lower() for x in r.types], k
        assert [_variable_key(v) for v in a.variables] == [
            _variable_key(v) for v in r.variables
        ], k
        assert [_use_key(u) for u in a.uses] == [_use_key(u) for u in r.uses], k


def test_pinned_tree_has_no_unparseable_file_left(pinned_pair):
    """Every configured source file now yields AST facts.

    The two files that used to be rejected are parsed after their signed
    operand is parenthesised, and they are the only files normalised. A new
    diagnostic appearing here is a real regression, not noise.
    """

    ast, _ = pinned_pair
    assert [f for f in ast.review_flags if f.code == "ast_parse_failed"] == []

    normalized = {
        f.target for f in ast.review_flags if f.code == "ast_input_normalized"
    }
    assert normalized == NORMALIZED_FILES
    for flag in ast.review_flags:
        if flag.code == "ast_input_normalized":
            # A rewrite of spelling is not a degradation, so it is not a warning.
            assert flag.severity == "info"

    # `character(len=len(str))` at utils.f90:222 used to be unreadable by the
    # shared declaration pattern; it parses now, so no diagnostic remains.
    assert [
        f for f in ast.review_flags if f.code == "ast_declaration_unreadable"
    ] == []

    assert {f.code for f in ast.review_flags} == {
        "ast_input_normalized",
        "io_unit_bound_to_several_files",
    }

    # SWAT+ opens three output units against two different files each. Neither
    # name can be used for operations elsewhere, and the conflict is real, so it
    # is reported rather than silently resolved to one of the two.
    collisions = [
        f for f in ast.review_flags if f.code == "io_unit_bound_to_several_files"
    ]
    assert len(collisions) == 3
    assert {f.severity for f in collisions} == {"warning"}
    assert all("is opened against" in f.message for f in collisions)


def test_pinned_tree_normalized_files_report_the_unchanged_source(pinned_pair):
    """The rewrite reaches fparser2 and nothing else.

    Every raw string on a normalised line must still read `Q*-1`, not the
    `Q*(-1)` the parser was given, and the procedures must match the scanner
    that never saw the rewrite at all.
    """

    ast, rich = pinned_pair
    key = lambda p: (p.location.path, p.name.lower(), p.kind)
    ast_by_key = {key(p): p for p in ast.procedures}
    rich_by_key = {key(p): p for p in rich.procedures}

    normalized_raws = []
    for k, procedure in ast_by_key.items():
        if k[0] not in NORMALIZED_FILES:
            continue
        other = rich_by_key[k]
        assert (procedure.location.line, procedure.location.end_line) == (
            other.location.line,
            other.location.end_line,
        ), k
        assert [_variable_key(v) for v in procedure.variables] == [
            _variable_key(v) for v in other.variables
        ], k
        for record in (*procedure.control_steps, *procedure.assignments):
            if "*-" in record.raw or "* -" in record.raw:
                normalized_raws.append(record.raw)

    assert normalized_raws, "expected the signed-operand statements to be recorded"
    for raw in normalized_raws:
        assert "(-" not in raw, raw


def test_pinned_tree_every_record_carries_a_location(pinned_pair):
    """Phase 3 exit gate: no AST fact lacks a location without a diagnostic."""

    ast, _ = pinned_pair
    for records in (ast.modules, ast.programs, ast.procedures, ast.types):
        for record in records:
            assert record.location is not None
            assert record.location.path
            assert record.location.line > 0
            assert record.identity

    for record in ast.procedures:
        for variable in record.variables:
            assert variable.location.line > 0
        for use in record.uses:
            assert use.location is not None and use.location.line > 0
    for record in ast.types:
        for component in record.components:
            assert component.location.line > 0


# ==========================================================================
# Phase 3 categories 4-7: assignments, control flow, calls and I/O
# ==========================================================================


def only_procedure(index):
    (procedure,) = index.procedures
    return procedure


# --- category 4: assignments ----------------------------------------------


def test_assignment_keeps_both_sides_and_the_join_key(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s()
  use aqu_module
  aqu_d(iaq)%rchrg = aqu_d(iaq)%rchrg + 1.
end subroutine s
""",
        )
    )
    (assignment,) = proc.assignments
    assert assignment.kind == "assignment"
    assert assignment.target == "aqu_d(iaq)%rchrg"
    # The join key drops subscripts and the component chain; the full path stays
    # on `target`.
    assert assignment.target_root == "aqu_d"
    assert assignment.expression == "aqu_d(iaq)%rchrg + 1."
    assert assignment.summary == "Sets aqu_d(iaq)%rchrg"
    assert assignment.raw == "aqu_d(iaq)%rchrg = aqu_d(iaq)%rchrg + 1."


def test_a_subscript_containing_parentheses_is_still_an_assignment(tmp_path):
    """The target's own subscript contains a call-shaped expression.

    A pattern whose subscript group is `\\([^()]*\\)` stops at the first inner
    `)`, so the statement fails to match at all and the assignment is lost.
    Splitting on the first `=` at paren depth zero has no such limit.
    """

    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s()
  use gw_module
  gw_chan_info(channel)%cells(gw_chan_info(channel)%ncon) = gw_chan_cell(i)
end subroutine s
""",
        )
    )
    (assignment,) = proc.assignments
    assert assignment.target == "gw_chan_info(channel)%cells(gw_chan_info(channel)%ncon)"
    assert assignment.target_root == "gw_chan_info"
    assert assignment.expression == "gw_chan_cell(i)"


def test_pointer_association_is_its_own_kind(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s()
  use m2
  ob_ptr => ob(icmd)
end subroutine s
""",
        )
    )
    (assignment,) = proc.assignments
    assert assignment.kind == "pointer_association"
    assert assignment.summary == "Associates ob_ptr"
    assert assignment.expression == "ob(icmd)"


def test_a_labelled_assignment_is_not_named_after_its_label(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s()
  integer :: lsu_num_cells(5), k, cell_count
  k = 1
26      lsu_num_cells(k) = cell_count
end subroutine s
""",
        )
    )
    labelled = proc.assignments[-1]
    assert labelled.target == "lsu_num_cells(k)"
    assert labelled.target_root == "lsu_num_cells"
    # `raw` is the statement as written, so it keeps the label.
    assert labelled.raw == "26      lsu_num_cells(k) = cell_count"


def test_a_comparison_is_not_an_assignment(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(a, b)
  integer :: a, b
  if (a == b) then
    a = 1
  end if
end subroutine s
""",
        )
    )
    assert [a.target for a in proc.assignments] == ["a"]


# --- category 5: the block tree -------------------------------------------


def test_nested_blocks_get_depth_parents_and_end_lines(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(n)
  integer :: n, i
  do i = 1, n
    if (i > 0) then
      n = 1
    else
      n = 2
    end if
  end do
end subroutine s
""",
        )
    )
    by_line = {s.location.line: s for s in proc.control_steps}

    loop = by_line[3]
    assert (loop.kind, loop.depth, loop.block_id, loop.parent_id) == ("loop", 0, 0, None)
    assert loop.end_line == 9

    branch = by_line[4]
    assert (branch.kind, branch.depth, branch.block_id, branch.parent_id) == (
        "if",
        1,
        1,
        0,
    )
    assert branch.end_line == 8

    # An arm belongs to its construct without nesting inside it: same depth as
    # the `if`, and `branch_of` naming the construct it is an arm of.
    arm = by_line[6]
    assert (arm.kind, arm.depth, arm.block_id, arm.branch_of) == ("else", 1, None, 1)
    assert arm.parent_id == 0


def test_a_one_line_if_opens_no_block(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(n)
  integer :: n
  if (n > 0) call helper(n)
  n = 1
end subroutine s
""",
        )
    )
    (step,) = [s for s in proc.control_steps if s.kind == "if"]
    assert step.block_id is None
    # The statement after it is not nested inside anything.
    assert all(s.parent_id is None for s in proc.control_steps)


def test_a_labelled_end_statement_closes_its_block(tmp_path):
    """`10  enddo` closes the loop it ends.

    A close pattern anchored at `^end` cannot see past the label, so the loop
    stays open, swallows the enclosing construct's `end`, and leaves the outer
    block with no end line at all. Every statement after it is then recorded one
    level too deep.
    """

    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(n)
  integer :: n, r
  if (n > 0) then
    do r = 1, n
      n = n + 1
10    enddo
    n = 0
  end if
end subroutine s
""",
        )
    )
    by_line = {s.location.line: s for s in proc.control_steps}
    outer, loop = by_line[3], by_line[4]
    assert outer.end_line == 8
    assert loop.end_line == 6
    # Every construct that opened also closed.
    assert all(
        s.end_line is not None for s in proc.control_steps if s.block_id is not None
    )


def test_label_terminated_do_closes_at_its_terminal_statement(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(n)
  integer :: n, i, j
  do 100 i = 1, n
    do 100 j = 1, n
      n = n + 1
100 continue
  if (n > 0) then
    n = 0
  end if
end subroutine s
""",
        )
    )

    loops = [step for step in proc.control_steps if step.kind == "loop"]
    assert [(step.depth, step.end_line) for step in loops] == [(0, 6), (1, 6)]
    trailing_if = next(step for step in proc.control_steps if step.kind == "if")
    assert (trailing_if.depth, trailing_if.parent_id) == (0, None)


def test_fixed_form_continuation_uses_fixed_source_rules(tmp_path):
    index = build(
        tmp_path,
        "legacy.f",
        """\
      subroutine legacy()
      character*10 value
      value = 'abc'
     1 // 'def'
      end
""",
    )

    (proc,) = index.procedures
    (assignment,) = proc.assignments
    assert assignment.target == "value"
    assert assignment.expression == "'abc' // 'def'"
    assert (assignment.location.line, assignment.location.end_line) == (3, 4)
    assert assignment.raw == "value = 'abc' // 'def'"
    assert index.review_flags == []


def test_select_case_records_its_subject_and_literal_labels(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(code)
  character(len=20) :: code
  integer :: n
  select case (code)
  case ("low")
    n = 1
  case ("high", "very_high")
    n = 2
  case default
    n = 3
  end select
end subroutine s
""",
        )
    )
    (select,) = proc.select_cases
    assert select.subject == "code"
    # `case default` dispatches on no literal and contributes none.
    assert select.cases == ["low", "high", "very_high"]


def test_nested_selects_each_get_their_own_record(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(typ, opt)
  character(len=20) :: typ, opt
  integer :: n
  select case (typ)
  case ("outer")
    select case (opt)
    case ("inner")
      n = 1
    end select
  end select
end subroutine s
""",
        )
    )
    subjects = {s.subject: s.cases for s in proc.select_cases}
    assert subjects == {"typ": ["outer"], "opt": ["inner"]}


# --- category 6: calls ----------------------------------------------------


def test_explicit_calls_are_recorded_with_their_statement_text(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(n)
  integer :: n
  call helper(n)
end subroutine s
""",
        )
    )
    (call,) = [c for c in proc.calls if c.kind == "subroutine"]
    assert call.name == "helper"
    assert call.raw == "call helper(n)"
    assert call.location.line == 3
    assert call.resolved is False


def test_a_call_inside_a_character_literal_is_not_a_call(tmp_path):
    """`write (*,*) 'call setup first'` calls nothing.

    A `\\bcall\\s+(\\w+)` scan over the statement text finds `setup` in the
    message and records a call observation for it. Taking calls from `Call_Stmt`
    nodes cannot: the literal is data, and fparser2 parses it as such.
    """

    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s()
  write (*,*) 'call setup first'
end subroutine s
""",
        )
    )
    assert [c.name for c in proc.calls if c.kind == "subroutine"] == []


def test_a_call_riding_on_a_one_line_if_is_still_recorded(tmp_path):
    """The inner `Call_Stmt` carries no source item of its own.

    It is reached through the `If_Stmt` that hosts it, so it takes that
    statement's location and text.
    """

    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(n)
  integer :: n
  if (n > 0) call helper(n)
end subroutine s
""",
        )
    )
    (call,) = [c for c in proc.calls if c.kind == "subroutine"]
    assert call.name == "helper"
    assert call.location.line == 3
    assert call.raw == "if (n > 0) call helper(n)"
    # And the statement is still outlined as the `if`.
    assert [s.kind for s in proc.control_steps] == ["if"]


def test_function_candidates_exclude_keywords_and_named_subroutines(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(n)
  integer :: n
  call helper(n)
  n = compute(n) + 1
end subroutine s
""",
        )
    )
    candidates = [c.name for c in proc.calls if c.kind == "function"]
    # `helper` is already recorded as an explicit call on its own line, and
    # statement keywords never become candidates.
    assert "helper" not in candidates
    assert "compute" in candidates
    assert "if" not in candidates


# --- category 7: I/O ------------------------------------------------------


def test_io_operation_records_unit_file_and_fields(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s()
  integer :: eof
  real :: wrk
  open (107, file = "demo.in")
  read (107,*,iostat=eof) wrk
  close (107)
end subroutine s
""",
        )
    )
    kinds = [o.kind for o in proc.io]
    assert kinds == ["open", "read", "close"]

    opened, read, closed = proc.io
    assert opened.unit == "107"
    assert opened.file_expr == '"demo.in"'
    assert opened.file_resolved == "demo.in"
    # A read and close on the same unit inherit the file the open named.
    assert read.file_resolved == "demo.in"
    assert read.fields == ["wrk"]
    assert closed.file_resolved == "demo.in"


def test_io_carries_the_condition_trail_it_sits_under(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(i_exist)
  logical :: i_exist
  integer :: header
  if (i_exist) then
    header = 0
  else
    read (107,*) header
  end if
end subroutine s
""",
        )
    )
    (operation,) = proc.io
    # The arm is appended to the `if` rather than replacing it, so the trail
    # still says which branch the read fell into.
    assert operation.condition == "if (i_exist) then / else"


def test_a_labelled_io_statement_is_still_an_io_operation(tmp_path):
    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s()
  open (107, file = "carbon_layers.prt")
99 close (107)
end subroutine s
""",
        )
    )
    kinds = [(o.kind, o.raw) for o in proc.io]
    assert kinds == [
        ("open", 'open (107, file = "carbon_layers.prt")'),
        ("close", "99 close (107)"),
    ]
    # Resolved through the unit the open bound, exactly as an unlabelled close is.
    assert proc.io[-1].file_resolved == "carbon_layers.prt"


def test_statements_sharing_a_line_are_all_recorded(tmp_path):
    """`case ('ncell'); read(code_val,*) ncell` is two statements.

    fparser2 reports both at the same starting line and the source layer splits
    them in the same order, so they pair up one for one.
    """

    proc = only_procedure(
        build(
            tmp_path,
            "m.f90",
            """\
subroutine s(code_val)
  character(len=20) :: code_val
  integer :: ncell
  select case (code_val)
  case ('ncell'); read(code_val,*) ncell
  end select
end subroutine s
""",
        )
    )
    assert [o.kind for o in proc.io] == ["read"]
    assert proc.io[0].fields == ["ncell"]
    # The `case` and the `read` riding on it are both outlined.
    assert [s.kind for s in proc.control_steps] == ["select", "case", "io"]


# --- parity for categories 4-7 on the pinned tree -------------------------


def _step_identity(step):
    return (step.kind, step.summary, step.raw, step.location.line)


def _step_nesting(step):
    return (step.depth, step.block_id, step.parent_id, step.branch_of, step.end_line)


def _max_paren_depth(text: str) -> int:
    """Deepest parenthesis nesting in *text*.

    A target nested more than one deep is one the scanner's `\\([^()]*\\)`
    subscript group cannot span.
    """

    depth = deepest = 0
    for char in text:
        if char == "(":
            depth += 1
            deepest = max(deepest, depth)
        elif char == ")":
            depth -= 1
    return deepest


def _assignment_key(assignment):
    return (
        assignment.kind,
        assignment.summary,
        assignment.raw,
        assignment.location.line,
        assignment.target,
        assignment.target_root,
        assignment.expression,
    )


def _call_key(call):
    return (call.name, call.raw, call.location.line, call.kind)


def _io_key(operation):
    return (
        operation.kind,
        operation.unit,
        operation.file_expr,
        operation.file_resolved,
        operation.raw,
        operation.location.line,
        tuple(operation.fields),
        operation.condition,
    )


# Every pinned-tree difference between the two paths, and why. Each is the AST
# reading a statement the scanner's anchored patterns cannot reach; none is a
# fact the AST loses.
ASSIGNMENTS_RECOVERED = 63
LABEL_AFFECTED_FILES = {"carbon_layers_read.f90", "gwflow_pond.f90"}


@pytest.fixture(scope="module")
def pinned_procedures(pinned_pair):
    ast, rich = pinned_pair
    key = lambda p: (p.location.path, p.name.lower(), p.kind)
    ast_by_key = {key(p): p for p in ast.procedures}
    rich_by_key = {key(p): p for p in rich.procedures}
    shared = sorted(
        k for k in ast_by_key.keys() & rich_by_key.keys()
    )
    return ast_by_key, rich_by_key, shared


def test_pinned_tree_select_cases_match(pinned_procedures):
    ast_by_key, rich_by_key, shared = pinned_procedures
    for k in shared:
        a = [(s.subject, tuple(s.cases), s.location.line) for s in ast_by_key[k].select_cases]
        r = [(s.subject, tuple(s.cases), s.location.line) for s in rich_by_key[k].select_cases]
        assert a == r, k


def test_pinned_tree_assignments_are_a_superset(pinned_procedures):
    """The AST loses no assignment and recovers the ones the pattern cannot read.

    All 63 recovered statements have a target whose subscript contains
    parentheses, or a leading statement label -- the two shapes
    `ASSIGN_RE` cannot match.
    """

    ast_by_key, rich_by_key, shared = pinned_procedures
    recovered = []
    for k in shared:
        a = [_assignment_key(x) for x in ast_by_key[k].assignments]
        r = [_assignment_key(x) for x in rich_by_key[k].assignments]
        missing = [x for x in r if x not in a]
        assert missing == [], (k, missing[:2])
        recovered.extend(x for x in a if x not in r)

    assert len(recovered) == ASSIGNMENTS_RECOVERED
    for entry in recovered:
        raw, target = entry[2], entry[4]
        assert _max_paren_depth(target) > 1 or raw.strip()[0].isdigit(), entry


def test_pinned_tree_calls_match_exactly(pinned_procedures):
    """Neither path records a call the other does not.

    The scanner used to emit `character(` and `len(` as function references
    from `utils.f90:222`, because it fell through to executable handling on a
    declaration it could not read. That declaration parses now, so the two
    false candidates are gone from both readings and the call lists agree.
    """

    ast_by_key, rich_by_key, shared = pinned_procedures
    dropped, added = [], []
    for k in shared:
        a = [_call_key(c) for c in ast_by_key[k].calls]
        r = [_call_key(c) for c in rich_by_key[k].calls]
        dropped.extend(x for x in r if x not in a)
        added.extend(x for x in a if x not in r)

    assert added == []
    assert dropped == []


def test_pinned_tree_control_steps_differ_only_where_a_label_defeats_the_scanner(
    pinned_procedures,
):
    """Outside the two labelled statements, every step matches exactly.

    `gwflow_pond.f90:360` is `10  enddo`, which the scanner never recognises as
    a close, and `carbon_layers_read.f90:48` is `99 close (107)`, which it never
    recognises as I/O at all.
    """

    ast_by_key, rich_by_key, shared = pinned_procedures
    affected = set()
    for k in shared:
        a = [_step_identity(s) for s in ast_by_key[k].control_steps]
        r = [_step_identity(s) for s in rich_by_key[k].control_steps]
        if a != r or [
            _step_nesting(s) for s in ast_by_key[k].control_steps
        ] != [_step_nesting(s) for s in rich_by_key[k].control_steps]:
            affected.add(k[0])
    assert affected == LABEL_AFFECTED_FILES


def test_pinned_tree_block_tree_is_closed_everywhere(pinned_pair):
    """Every construct the AST opens also closes.

    The scanner leaves one open across the whole pinned tree -- the `if` at
    `gwflow_pond.f90:53`, whose `end if` was consumed by a loop that the
    labelled `enddo` failed to close.
    """

    ast, rich = pinned_pair
    def unclosed(index):
        return [
            (p.location.path, s.location.line)
            for p in index.procedures
            for s in p.control_steps
            if s.block_id is not None and s.end_line is None
        ]

    assert unclosed(ast) == []
    assert unclosed(rich) == [("gwflow_pond.f90", 53)]


def test_pinned_tree_io_differs_only_in_the_label_affected_files(pinned_procedures):
    ast_by_key, rich_by_key, shared = pinned_procedures
    affected = set()
    for k in shared:
        a = [_io_key(o) for o in ast_by_key[k].io]
        r = [_io_key(o) for o in rich_by_key[k].io]
        if a != r:
            affected.add(k[0])
    assert affected == LABEL_AFFECTED_FILES


def test_pinned_tree_executable_facts_carry_locations(pinned_pair):
    """Phase 3 exit gate, extended to categories 4-7."""

    ast, _ = pinned_pair
    for procedure in ast.procedures:
        for collection in (
            procedure.assignments,
            procedure.control_steps,
            procedure.calls,
            procedure.io,
            procedure.select_cases,
        ):
            for record in collection:
                assert record.location is not None
                assert record.location.path
                assert record.location.line > 0


def test_pinned_tree_reports_no_unreadable_executable_statements(pinned_pair):
    """Nothing the AST calls a statement is lost to an unreadable byte pattern."""

    ast, _ = pinned_pair
    codes = {f.code for f in ast.review_flags}
    assert "ast_assignment_unreadable" not in codes
    assert "ast_unclosed_select" not in codes
    assert "ast_unplaced_fact" not in codes


def test_pinned_tree_shared_state_matches_the_scanner(pinned_procedures):
    """Both parsers derive the same shared state from their own index.

    The derivation consumes records rather than source text, so this is really a
    test that the two indexes agree about assignments and statement text. The
    one procedure that differs is `salt_chem_soil_single`, whose
    `10    upion1 = Sul_Conc(salt_c4)` carries a statement label: the scanner's
    assignment pattern cannot match past the label, so it never records the
    write, and `upion1` shows up as a read instead. That is the same labelled
    statement limitation Phase 3 documented, surfacing in a second fact family.
    """

    ast_by_key, rich_by_key, shared = pinned_procedures
    differing = [
        k
        for k in shared
        if (ast_by_key[k].reads, ast_by_key[k].writes)
        != (rich_by_key[k].reads, rich_by_key[k].writes)
    ]
    assert [k[1] for k in differing] == ["salt_chem_soil_single"]

    key = differing[0]
    assert "upion1" in ast_by_key[key].writes
    assert "upion1" in rich_by_key[key].reads
    assert "upion1" not in rich_by_key[key].writes


def test_pinned_tree_io_files_and_output_families_match(pinned_pair):
    """The AST index closes out a scan the same way the scanner does.

    Until the aggregation was shared, the AST path produced no `io_files` and no
    `output_families` at all, so it could not stand in for the scanner. The
    three files that differ are the two labelled statements Phase 3 documented:
    `carbon_layers_read.f90`'s `99 close (107)`, which the scanner does not see
    as I/O, and `gwflow_pond.f90`, whose condition trail drifts from the
    labelled `enddo` it never closes.
    """

    ast, rich = pinned_pair
    assert ast.stats["io_files"] == rich.stats["io_files"]
    assert ast.stats["output_families"] == rich.stats["output_families"]

    ast_files = {doc.key: doc for doc in ast.io_files}
    rich_files = {doc.key: doc for doc in rich.io_files}
    assert ast_files.keys() == rich_files.keys()

    def operation_key(operation):
        return (
            operation.kind,
            operation.unit,
            operation.file_expr,
            operation.file_resolved,
            operation.raw,
            operation.location.line,
            tuple(operation.fields),
            operation.condition,
        )

    differing = {
        key
        for key in ast_files
        if [operation_key(o) for o in ast_files[key].operations]
        != [operation_key(o) for o in rich_files[key].operations]
        or ast_files[key].procedures != rich_files[key].procedures
    }
    # Named `unit_out_pond_*` until units were bound across files: the writes
    # are in `gwflow_pond.f90`, the `open` that names them in `gwflow_read.f90`.
    assert differing == {
        "carbon_layers.prt",
        "gwflow_pond_conc_day.txt",
        "gwflow_pond_mass_day.txt",
    }

    ast_families = {doc.key: doc for doc in ast.output_families}
    rich_families = {doc.key: doc for doc in rich.output_families}
    assert ast_families.keys() == rich_families.keys()
    for key, family in ast_families.items():
        other = rich_families[key]
        assert (family.base, family.opened_by, family.written_by) == (
            other.base,
            other.opened_by,
            other.written_by,
        ), key
        assert [
            (f.name, f.frequency, f.fmt, f.unit) for f in family.files
        ] == [(f.name, f.frequency, f.fmt, f.unit) for f in other.files], key
