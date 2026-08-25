from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import shutil
import unittest
import uuid

from swatplus_reference.parser.schema_fortran import (
    FortranScanner,
    extract_fields_from_io,
    logical_lines,
    split_io_statement,
)
from swatplus_reference.parser.schema_config import BuildConfig


@contextmanager
def temp_dir():
    root = Path.cwd() / ".test_tmp"
    root.mkdir(exist_ok=True)
    path = root / f"case_{uuid.uuid4().hex}"
    path.mkdir()
    try:
        yield str(path)
    finally:
        shutil.rmtree(path, ignore_errors=True)


SAMPLE = """\
!> Main SWAT+ driver used by the fixture.
program swatplus
  use basin_read_module
  call basin_read()
end program swatplus

!> Reads basin input files and initializes basin state.
module basin_read_module
  implicit none

  !> Basin input file metadata.
  type :: basin_file
    character(len=32) :: filename = "basin.bsn"
    integer :: unit = 107
  end type basin_file

contains

  !> Open and read basin inputs, then hand off to object setup.
  subroutine basin_read()
    type(basin_file) :: file_info
    integer :: eof
    open(unit=file_info%unit, file=file_info%filename, status="old")
    read(file_info%unit, *, iostat=eof) header
    if (eof == 0) then
      call basin_objects_init()
    end if
    close(file_info%unit)
  end subroutine basin_read

  subroutine basin_objects_init()
    call external_setup()
  end subroutine basin_objects_init

end module basin_read_module
"""


class FortranScannerTests(unittest.TestCase):
    def test_logical_lines_does_not_duplicate_final_line(self) -> None:
        self.assertEqual(
            ["call x()"],
            [line.text for line in logical_lines(["call x()"])],
        )

    def test_type_component_wrapped_inline_comment_attributed_correctly(self) -> None:
        # SWAT+ wraps a field's inline "!units |desc" comment onto the next gutter
        # line. That continuation belongs to the field above, not the field below.
        source_text = """\
module plant_data_module
  type plant_db
    real :: frgrw1 = 0.05            !none              |fraction of the growing season corresponding to the
                                     !                  |  1st point on optimal leaf area development curve
    real :: laimx1 = 0.05            !none              |frac of max leaf area index corresponding to the
                                     !                  |  1st point on optimal leaf area development curve
  end type plant_db
end module plant_data_module
"""
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "plant_data_module.f90").write_text(source_text, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            project = FortranScanner(config).scan()
            comps = {c.name: c for t in project.types for c in t.components}

            # Each field keeps its own inline comment plus its own continuation line,
            # in order, and does not borrow the previous field's continuation.
            self.assertEqual(
                "none              |fraction of the growing season corresponding to the\n"
                "|  1st point on optimal leaf area development curve",
                comps["frgrw1"].doc,
            )
            self.assertEqual(
                "none              |frac of max leaf area index corresponding to the\n"
                "|  1st point on optimal leaf area development curve",
                comps["laimx1"].doc,
            )

    def test_star_kind_declaration_inside_derived_type_is_not_dropped(self) -> None:
        # Old-style `integer*8` / `character*10` kind specs (no parens) must
        # parse like their modern equivalents, not be silently skipped --
        # SWAT+ uses this form for at least one production record type
        # (`object_connectivity%gis_id` in hydrograph_module.f90).
        source_text = """\
module rec_module
  type record_id
    integer*8 :: gis_id = 0
    real*8 :: precise = 0.d0
    character*10 :: code
    integer :: ordinary = 0
  end type record_id
end module rec_module
"""
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "rec.f90").write_text(source_text, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            project = FortranScanner(config).scan()

            record_id = next(t for t in project.types if t.name == "record_id")
            names = [c.name for c in record_id.components]
            self.assertEqual(names, ["gis_id", "precise", "code", "ordinary"])
            by_name = {c.name: c for c in record_id.components}
            self.assertEqual(by_name["gis_id"].vartype, "integer")
            self.assertEqual(by_name["precise"].vartype, "real")
            self.assertEqual(by_name["code"].vartype, "character")

    def test_closed_up_endtype_closes_the_type(self) -> None:
        # `endtype` (no space) is legal Fortran and SWAT+ uses it in
        # gwflow_module.f90. Failing to match it swallows every later
        # module declaration into the still-open type -- which cost that
        # module 341 of its 436 variables and gave one type 283 components.
        source_text = """\
module gw_module
  type first_type
    integer :: a = 0
    real :: b = 0.
  endtype first_type

  integer, dimension (:), allocatable :: after_one

  type second_type
    real :: c = 0.
  end type second_type

  real, allocatable :: after_two(:)
endmodule gw_module
"""
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "gw.f90").write_text(source_text, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            project = FortranScanner(config).scan()

            first = next(t for t in project.types if t.name == "first_type")
            self.assertEqual([c.name for c in first.components], ["a", "b"])
            second = next(t for t in project.types if t.name == "second_type")
            self.assertEqual([c.name for c in second.components], ["c"])

            # Declarations after a closed-up endtype belong to the module.
            module = next(m for m in project.modules if m.name == "gw_module")
            self.assertEqual(
                [v.name for v in module.variables], ["after_one", "after_two"]
            )


class SplitIoStatementTests(unittest.TestCase):
    """Neither "first `)`" nor "greedy to last `)`" finds an I/O statement's
    true control-list boundary when either side has its own nested parens.
    Only real paren-depth tracking does; these pin the two failure shapes a
    single regex can't tell apart, plus the ordinary case both must still get
    right."""

    def test_plain_read_no_nested_parens(self) -> None:
        kind, control, remainder = split_io_statement(
            "      read (107,*,iostat=eof) titldum"
        )
        self.assertEqual(kind, "read")
        self.assertEqual(control, "107,*,iostat=eof")
        self.assertEqual(remainder, " titldum")

    def test_field_with_its_own_parens_does_not_leak_into_control_list(self) -> None:
        # A naive greedy match extends to the *last* ")" in the line -- here
        # that's the one closing "manure_om(it)", not the control list's own
        # close, which would truncate the control list and the field.
        _kind, control, remainder = split_io_statement(
            "      read (107,*,iostat=eof) manure_om(it)%name, manure_om(it)%frac_water"
        )
        self.assertEqual(control, "107,*,iostat=eof")
        self.assertEqual(
            remainder.strip(), "manure_om(it)%name, manure_om(it)%frac_water"
        )

    def test_parenthesized_unit_does_not_truncate_the_control_list(self) -> None:
        # A naive "first )" match stops at the close of "split_fields(1)"
        # itself, before the control list (and thus the whole statement)
        # actually ends -- the shape of an internal read from an array
        # element, e.g. SWAT+'s `read(split_fields(N),*) var` idiom.
        _kind, control, remainder = split_io_statement(
            "        read(split_fields(1),*) cell_id_in"
        )
        self.assertEqual(control, "split_fields(1),*")
        self.assertEqual(remainder, " cell_id_in")

    def test_both_nested_parens_at_once(self) -> None:
        _kind, control, remainder = split_io_statement(
            "        read(split_fields(4),*) gw_state(i)%stat"
        )
        self.assertEqual(control, "split_fields(4),*")
        self.assertEqual(remainder.strip(), "gw_state(i)%stat")

    def test_extract_fields_from_io_matches(self) -> None:
        self.assertEqual(
            extract_fields_from_io("        read(split_fields(4),*) gw_state(i)%stat"),
            ["gw_state(i)%stat"],
        )
        self.assertEqual(
            extract_fields_from_io("        read(split_fields(3),*) cell_gis_id(i)"),
            ["cell_gis_id(i)"],
        )


class InternalReadAttributionTests(unittest.TestCase):
    def test_internal_read_unit_and_fields_parse_correctly(self) -> None:
        # `read(split_fields(N),*) var` reads from a CHARACTER array element
        # (Fortran internal I/O), not a file unit. The scanner must still
        # capture the target correctly...
        source_text = """\
subroutine cell_read
  character (len=200) :: split_line_buf = ""
  character (len=40), dimension (30) :: split_fields
  integer :: cell_gis_id_val = 0
  real :: elev_val = 0.
  open (107,file="cells.gw")
  read (107,'(a)') split_line_buf
  read (split_fields(3),*) cell_gis_id_val
  read (split_fields(5),*) elev_val
  close (107)
end subroutine cell_read
"""
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "cell_read.f90").write_text(source_text, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            project = FortranScanner(config).scan()
            proc = next(p for p in project.procedures if p.name == "cell_read")
            internal_reads = [op for op in proc.io if op.unit and "(" in op.unit]
            self.assertEqual(len(internal_reads), 2)
            self.assertEqual(internal_reads[0].unit, "split_fields(3)")
            self.assertEqual(internal_reads[0].fields, ["cell_gis_id_val"])
            self.assertEqual(internal_reads[1].fields, ["elev_val"])


class SelectCaseCaptureTests(unittest.TestCase):
    """A ``select case`` block's string-literal labels are the closed
    vocabulary a dispatcher recognizes (e.g. a decision table's COND_VAR /
    ACT_TYP names) -- something a read statement's field list can't express
    at all. These pin the capture against the shapes that actually occur in
    the pinned source: a plain select, a ``case default`` that contributes
    nothing, a nested select emitting its own separate entry, and the
    doubled-paren spelling SWAT+ itself uses for some subjects."""

    SOURCE = """\
subroutine dtbl_fixture_read
  character (len=40) :: typ = ""
  character (len=40) :: option = ""
  select case (typ)
  case ("plant")
    option = "a"
  case ("harvest", "harvest_kill")
    option = "b"
  case default
    option = "c"
  end select
  select case (typ)
  case ("release")
    select case (option)
    case ("weir")
      option = "d"
    case ("meas")
      option = "e"
    end select
  end select
  select case ((typ))
  case ("*")
    option = "f"
  end select
end subroutine dtbl_fixture_read
"""

    def _scan(self):
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "dtbl_fixture_read.f90").write_text(self.SOURCE, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            project = FortranScanner(config).scan()
            return next(p for p in project.procedures if p.name == "dtbl_fixture_read")

    def test_case_labels_captured_and_default_contributes_nothing(self) -> None:
        proc = self._scan()
        self.assertEqual(len(proc.select_cases), 4)
        first = proc.select_cases[0]
        self.assertEqual(first.subject, "typ")
        self.assertEqual(first.cases, ["plant", "harvest", "harvest_kill"])

    def test_nested_select_emits_its_own_entry(self) -> None:
        # A block is emitted when its own `end select` closes it, so the
        # inner (nested) block appears before the outer one that contains it.
        proc = self._scan()
        inner = proc.select_cases[1]
        outer = proc.select_cases[2]
        self.assertEqual(outer.subject, "typ")
        self.assertEqual(outer.cases, ["release"])
        self.assertEqual(inner.subject, "option")
        self.assertEqual(inner.cases, ["weir", "meas"])

    def test_doubled_parens_preserved_from_source(self) -> None:
        # SWAT+ itself writes `select case ((expr))` in several spots
        # (conditions.f90's lim_op dispatch) -- the extra parens are part of
        # the subject expression, not a scanning artifact, so pin that they
        # survive rather than get silently stripped to just "expr".
        proc = self._scan()
        last = proc.select_cases[3]
        self.assertEqual(last.subject, "(typ)")
        self.assertEqual(last.cases, ["*"])


class ConditionTrailElseBranchTests(unittest.TestCase):
    """A read inside an `if` branch and a sibling read inside its `else`
    previously got an IDENTICAL condition trail -- the stack only ever
    recorded the opening `if (...) then`, with nothing marking that a later
    read had crossed into the `else`. That makes an if-branch read and an
    else-branch read of a genuinely different shape structurally
    indistinguishable from source alone, which a keyed-row detector needs to
    tell apart."""

    SOURCE = """\
subroutine branch_read
  character (len=10) :: tag = ""
  integer :: a = 0, b = 0
  if (tag == "range") then
    read (107,*) tag, a
  else
    read (107,*) b
  end if
end subroutine branch_read
"""

    def _scan(self):
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "branch_read.f90").write_text(self.SOURCE, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            project = FortranScanner(config).scan()
            return next(p for p in project.procedures if p.name == "branch_read")

    def test_if_and_else_reads_get_different_trails(self) -> None:
        proc = self._scan()
        if_read = next(op for op in proc.io if op.fields == ["tag", "a"])
        else_read = next(op for op in proc.io if op.fields == ["b"])
        self.assertNotEqual(if_read.condition, else_read.condition)
        self.assertIn('if (tag == "range") then', if_read.condition)
        self.assertNotIn("else", if_read.condition)
        self.assertIn("else", else_read.condition)

    def test_original_if_context_preserved_in_else_trail(self) -> None:
        # The else branch's trail keeps the opening `if` text rather than
        # replacing it outright, so generated docs still show what condition
        # is being negated, not just a bare "else".
        proc = self._scan()
        else_read = next(op for op in proc.io if op.fields == ["b"])
        self.assertIn('if (tag == "range") then', else_read.condition)


class ConditionTrailUnspacedEndKeywordTests(unittest.TestCase):
    """The end-of-block check only matched `end if`/`end do`/`end select`
    with a space -- valid free-form Fortran also spells these `endif`/
    `enddo`/`endselect` with none, which is how gwflow_read.f90 (and roughly
    40% of the pinned source tree) writes every closing statement. Without
    matching that spelling, the condition stack never popped for those
    procedures: it grew for the whole procedure body and a read long after a
    loop closed still carried that loop (and everything nested inside it) in
    its trail, corrupting `_in_do_loop` for every later read."""

    SOURCE = """\
subroutine unspaced_end_read
  integer :: i = 0, n = 3, a = 0, b = 0
  if (n > 0) then
    do i = 1, n
      read (107,*) a
    enddo
  endif
  read (107,*) b
end subroutine unspaced_end_read
"""

    def _scan(self):
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "unspaced_end_read.f90").write_text(self.SOURCE, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            project = FortranScanner(config).scan()
            return next(p for p in project.procedures if p.name == "unspaced_end_read")

    def test_do_loop_read_is_in_the_loop(self) -> None:
        proc = self._scan()
        a_read = next(op for op in proc.io if op.fields == ["a"])
        self.assertIn("do i = 1, n", a_read.condition)
        self.assertIn("if (n > 0) then", a_read.condition)

    def test_read_after_unspaced_endif_enddo_has_an_empty_trail(self) -> None:
        # Both closing statements use the no-space spelling; a read after
        # both must show neither the `if` nor the `do` in its trail.
        proc = self._scan()
        b_read = next(op for op in proc.io if op.fields == ["b"])
        self.assertFalse(b_read.condition)


class ProcedureLocalDerivedTypeTests(unittest.TestCase):
    """A `type ... end type` declared inside a subroutine's own
    specification part (co2_read.f90's real shape: `type co2_annual`
    nested inside `subroutine co2_read`, never module-level -- the only
    pinned-source example) was silently dropped: type-collection only
    fired when scanning outside any procedure. That left the type out of
    `project.types` entirely, so a read into a variable of that type failed
    downstream with "unknown derived type", and -- since `type_stack` was
    never pushed either -- the type's own component lines fell through to
    the ordinary variable-declaration path and were misattributed as plain
    procedure-local variables instead of type components."""

    SOURCE = """\
subroutine local_type_read
  type point
    integer :: x = 0
    integer :: y = 0
  end type point
  type (point) :: p
  open (107,file="points.dat")
  read (107,*) p
end subroutine local_type_read
"""

    def _scan(self):
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "local_type_read.f90").write_text(self.SOURCE, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            return FortranScanner(config).scan()

    def test_procedure_local_type_is_collected(self) -> None:
        project = self._scan()
        self.assertIn("point", [t.name for t in project.types])

    def test_local_type_components_are_not_misattributed_to_the_procedure(self) -> None:
        project = self._scan()
        point = next(t for t in project.types if t.name == "point")
        self.assertEqual([c.name for c in point.components], ["x", "y"])
        proc = next(p for p in project.procedures if p.name == "local_type_read")
        proc_var_names = [v.name for v in proc.variables]
        self.assertNotIn("x", proc_var_names)
        self.assertNotIn("y", proc_var_names)
        self.assertIn("p", proc_var_names)


class ConditionTrailCaseBranchTests(unittest.TestCase):
    """Same problem as the if/else case, for `select case`: a read in one
    `case` branch and a read in another previously got an IDENTICAL trail
    (just the opening `select case (...)`), with no way to tell which branch
    a given read belongs to. Unlike if/elseif (a handful of branches at
    most), a select case can have dozens (SWAT+'s COND_VAR dispatch has 55),
    so each case's trail must REPLACE the previous case's, not accumulate
    every case label scanned so far."""

    SOURCE = """\
subroutine keyed_read
  character (len=25) :: split_fields(2) = ""
  integer :: yr = 0, cell = 0, dbg = 0
  select case (trim(split_fields(1)))
  case ("head_output_time")
    read (split_fields(2),*) yr
  case ("observation_cell")
    read (split_fields(2),*) cell
  case ("detail_debug_cell")
    read (split_fields(2),*) dbg
  end select
end subroutine keyed_read
"""

    def _scan(self):
        with temp_dir() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "keyed_read.f90").write_text(self.SOURCE, encoding="utf-8")
            config = BuildConfig(project_name="Fixture", source_dir=source, output_dir=root / "site")
            project = FortranScanner(config).scan()
            return next(p for p in project.procedures if p.name == "keyed_read")

    def test_each_case_branch_gets_its_own_trail(self) -> None:
        proc = self._scan()
        yr_read = next(op for op in proc.io if op.fields == ["yr"])
        cell_read = next(op for op in proc.io if op.fields == ["cell"])
        dbg_read = next(op for op in proc.io if op.fields == ["dbg"])
        self.assertIn("case (\"head_output_time\")", yr_read.condition)
        self.assertIn("case (\"observation_cell\")", cell_read.condition)
        self.assertIn("case (\"detail_debug_cell\")", dbg_read.condition)

    def test_trail_does_not_accumulate_earlier_case_labels(self) -> None:
        # The third branch's trail must not still be carrying the first two
        # cases' labels -- only its own.
        proc = self._scan()
        dbg_read = next(op for op in proc.io if op.fields == ["dbg"])
        self.assertNotIn("head_output_time", dbg_read.condition)
        self.assertNotIn("observation_cell", dbg_read.condition)
        self.assertIn("select case", dbg_read.condition)


if __name__ == "__main__":
    unittest.main()

