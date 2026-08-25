from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner
from swatplus_reference.schema.input import (
    TARGET_FILES,
    SchemaResolver,
    analyze_procedure,
    array_multiplicity,
    build_decision_tables,
    build_multi_records,
    build_multi_sections,
    build_runtime_arity,
    build_schema,
    dumps,
    split_units_doc,
)
from swatplus_reference.parser.schema_model import SourceLocation, VariableRef


def scan_source(source: str) -> object:
    """Write one Fortran source file to a temp tree and scan it."""
    tmp = tempfile.mkdtemp()
    (Path(tmp) / "mod.f90").write_text(source, encoding="utf-8")
    cfg = BuildConfig(source_dir=Path(tmp))
    return FortranScanner(cfg).scan()


# A self-contained module exercising both read patterns, a nested derived-type
# component, a fixed-size array component, an indirect file.cio slot, and a
# hard-coded filename.
FIXTURE = """
      module input_file_module
      type input_parameter_databases
        character(len=25) :: snow = "snow.sno"
      end type input_parameter_databases
      type (input_parameter_databases) :: in_parmdb
      end module input_file_module

      module hru_module
      type nested_fracs
        real :: lig_frac = 0.12    !none   |lignin fraction
      end type nested_fracs

      type snow_parameters
        character (len=40) :: name = ""
        real :: falltmp = 0.       !deg C   |snowfall temp
        real, dimension(3) :: layers = (/1.,2.,3./)  !mm  |layer depths
        type (nested_fracs) :: fracs
      end type snow_parameters
      type (snow_parameters), dimension(:), allocatable :: snodb

      type manure_attributes
        character(len=64) :: name = " "   !! id constructed from
                                          !! region, source, and type
        real :: frac_water = 0.   !! kg/kg |frac of manure which is water
        character(len=64) :: description = " "   !! na |description
      end type manure_attributes
      type (manure_attributes), dimension(:), allocatable :: manure_om
      end module hru_module

      subroutine snowdb_read
      use input_file_module
      use hru_module
      integer :: isno = 0
      character (len=80) :: titldum = ""
      open (107,file=in_parmdb%snow)
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) snodb(isno)
      close (107)
      end subroutine snowdb_read

      subroutine manure_orgmin_read
      use hru_module
      integer :: it = 0
      open (107,file="manure_om.frt")
      read (107,*,iostat=eof) manure_om(it)%name, manure_om(it)%frac_water,     &
        manure_om(it)%description
      close (107)
      end subroutine manure_orgmin_read

      subroutine broken_read
      use hru_module
      integer :: iz = 0
      open (107,file="mystery.xyz")
      read (107,*,iostat=eof) mystery(iz)%no_such_field
      close (107)
      end subroutine broken_read
"""


# Exercises two gaps a curated 28-file TARGET_FILES tuple never surfaced:
# (1) a literal filename whose extension itself contains an underscore, and
# (2) a reader shared across several input files, where the ``open`` names one
# of the reader's own dummy arguments and each caller supplies a different
# filename (the real shape of SWAT+'s twelve ``*.con`` readers, all funneled
# through ``hyd_read_connect``).
DUMMY_ARG_FIXTURE = """
      module con_module
      type con_record
        integer :: num = 0
        character(len=16) :: name = ""
      end type con_record
      end module con_module

      module input_file_module2
      type input_con_files
        character(len=25) :: hru_con = "hru.con"
        character(len=25) :: chan_con = "channel.con"
      end type input_con_files
      type (input_con_files) :: in_con
      end module input_file_module2

      subroutine shared_con_read(con_file, obtyp)
      use con_module
      character (len=20) :: con_file
      character (len=8) :: obtyp
      type (con_record) :: rec
      open (107,file=con_file)
      read (107,*,iostat=eof) rec%num, rec%name
      close (107)
      end subroutine shared_con_read

      subroutine driver
      use input_file_module2
      call shared_con_read(in_con%hru_con, "hru     ")
      call shared_con_read(in_con%chan_con, "chan    ")
      end subroutine driver

      subroutine cs_init_read
      use con_module
      type (con_record) :: rec2
      open (105,file="initial.cha_cs")
      read (105,*,iostat=eof) rec2%num, rec2%name
      close (105)
      end subroutine cs_init_read
"""


# Mirrors gwflow_read.f90's real shape: one procedure reuses a single unit
# variable for a sequence of unrelated files, opened/read/closed one after
# another. Without pairing each read to the open that immediately preceded
# it, a "longest read wins across the whole procedure" chooser misattributes
# one file's schema to another file's name, and a file with no derived-type
# data read of its own (just a scalar config flag, like SWAT+'s codes.gw)
# wrongly inherits a sibling's schema instead of resolving to nothing.
REUSED_UNIT_FIXTURE = """
      module gw_module
      type gw_record_a
        integer :: id = 0
        real :: value_a = 0.
      end type gw_record_a
      type gw_record_b
        character(len=16) :: name = ""
        real :: value_b = 0.
        real :: value_c = 0.
      end type gw_record_b
      end module gw_module

      subroutine shared_unit_read
      use gw_module
      integer :: in_gw = 0
      character (len=80) :: titldum = ""
      type (gw_record_a) :: rec_a
      type (gw_record_b) :: rec_b
      integer :: config_flag = 0

      open (in_gw,file="codes.gw")
      read (in_gw,*,iostat=eof) titldum
      read (in_gw,*,iostat=eof) config_flag
      close (in_gw)

      open (in_gw,file="cells.gw")
      read (in_gw,*,iostat=eof) titldum
      read (in_gw,*,iostat=eof) rec_a
      close (in_gw)

      open (in_gw,file="zones.gw")
      read (in_gw,*,iostat=eof) titldum
      read (in_gw,*,iostat=eof) rec_b%name, rec_b%value_b, rec_b%value_c
      close (in_gw)
      end subroutine shared_unit_read
"""


# Mirrors recall_db.rec's real shape: a record with several sibling
# components of the *same* nested type (each flattening to the same
# name/units/tstep trio), plus one non-colliding single-component chain
# (record_type%name, a bare scalar) to confirm unambiguous chains are left
# alone even in a read that does contain a collision elsewhere.
COLLIDING_SIBLINGS_FIXTURE = """
      module recall_module
      type constituent_file_data
        character(len=25) :: name = ""
        character(len=13) :: units = ""
        character(len=13) :: tstep = ""
      end type constituent_file_data
      type recall_databases
        character(len=13) :: name = ""
        type (constituent_file_data) :: org_min
        type (constituent_file_data) :: pest
      end type recall_databases
      end module recall_module

      subroutine recall_read
      use recall_module
      integer :: k = 0
      type (recall_databases) :: recall_db(1)
      integer :: i = 0
      open (107,file="recall_db.rec")
      read (107,*,iostat=eof) k, recall_db(i)%name, recall_db(i)%org_min, &
                                   recall_db(i)%pest
      close (107)
      end subroutine recall_read
"""


class UnitDocParsingTests(unittest.TestCase):
    def test_units_before_pipe(self) -> None:
        self.assertEqual(split_units_doc("deg C   |snowfall temp"), ("deg C", "snowfall temp"))

    def test_no_pipe_is_all_description(self) -> None:
        self.assertEqual(split_units_doc("just a description"), (None, "just a description"))

    def test_empty(self) -> None:
        self.assertEqual(split_units_doc(""), (None, None))

    def test_units_taken_from_pipe_line_not_first_line(self) -> None:
        # A misattributed preceding comment (no pipe) must not become units.
        doc = "region, source, and type\nkg/kg |frac of manure which is water"
        units, desc = split_units_doc(doc)
        self.assertEqual(units, "kg/kg")
        self.assertEqual(desc, "frac of manure which is water")


class ArrayMultiplicityTests(unittest.TestCase):
    def _var(self, declaration: str, name: str) -> VariableRef:
        return VariableRef(
            name=name, declaration=declaration, location=SourceLocation("x", 1)
        )

    def test_scalar_is_one(self) -> None:
        self.assertEqual(array_multiplicity(self._var("real :: x = 0.", "x")), 1)

    def test_dimension_attr(self) -> None:
        self.assertEqual(
            array_multiplicity(self._var("real , dimension(4) :: cn", "cn")), 4
        )

    def test_name_attached_dims(self) -> None:
        self.assertEqual(array_multiplicity(self._var("real :: cn(4)", "cn")), 4)

    def test_range_dims(self) -> None:
        self.assertEqual(
            array_multiplicity(self._var("real, dimension(2:5) :: a", "a")), 4
        )

    def test_len_spec_is_not_a_dimension(self) -> None:
        self.assertEqual(
            array_multiplicity(self._var("character(len=40) :: name", "name")), 1
        )

    def test_assumed_shape_not_expanded(self) -> None:
        self.assertEqual(
            array_multiplicity(self._var("real, dimension(:) :: a", "a")), 1
        )


# A component declared `dimension(12)` reads all 12 columns when named bare
# (`%monthly`), but exactly one column when subscripted to a single element in
# the read (`%monthly(mo)`, the SWAT+ weather-generator idiom of reading one
# month per line inside `do mo = 1, 12`). Stripping the subscript before
# resolving the component -- and then array-expanding it -- turned that one
# column into 12 (weather-wgn.cli came out 168 columns instead of 14).
SUBSCRIPTED_ELEMENT_FIXTURE = """
      module wgn_module
      implicit none
      type wgn_rec
        real, dimension(12) :: monthly = 0.
        real :: elev = 0.
      end type wgn_rec
      type (wgn_rec), dimension(:), allocatable :: wgn
      end module wgn_module

      subroutine wgn_element_read
      use wgn_module
      integer :: i = 0, mo = 0
      open (114,file="element.wgn")
      do i = 1, 3
        do mo = 1, 12
          read (114,*) wgn(i)%monthly(mo), wgn(i)%elev
        end do
      end do
      close (114)
      end subroutine wgn_element_read

      subroutine wgn_wholearray_read
      use wgn_module
      integer :: i = 0
      open (115,file="wholearray.wgn")
      do i = 1, 3
        read (115,*) wgn(i)%monthly, wgn(i)%elev
      end do
      close (115)
      end subroutine wgn_wholearray_read
"""


class SubscriptedArrayElementTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(SUBSCRIPTED_ELEMENT_FIXTURE)
        self.files = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("element.wgn", "wholearray.wgn"),
        )["files"]

    def test_subscripted_element_is_one_column(self) -> None:
        names = [f["fortran_name"] for f in self.files["element.wgn"]["fields"]]
        self.assertEqual(names, ["monthly", "elev"])

    def test_bare_array_still_expands(self) -> None:
        # No regression: a component named without a subscript is still the
        # whole declared array.
        names = [f["fortran_name"] for f in self.files["wholearray.wgn"]["fields"]]
        self.assertEqual(names, [f"monthly({i})" for i in range(1, 13)] + ["elev"])


class SchemaBuildTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(FIXTURE)
        self.payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("snow.sno", "manure_om.frt", "mystery.xyz", "absent.dat"),
        )
        self.files = self.payload["files"]

    def test_derived_type_pattern_flattens_and_expands(self) -> None:
        snow = self.files["snow.sno"]
        self.assertEqual(snow["read_pattern"], "derived_type")
        self.assertEqual(snow["derived_type"], "snow_parameters")
        names = [f["fortran_name"] for f in snow["fields"]]
        # name, falltmp, layers(1..3) [array expanded], then nested lig_frac.
        self.assertEqual(
            names, ["name", "falltmp", "layers(1)", "layers(2)", "layers(3)", "lig_frac"]
        )
        self.assertEqual([f["numeric"] for f in snow["fields"]][0], False)
        self.assertTrue(all(f["numeric"] for f in snow["fields"][1:]))

    def test_derived_type_units_and_doc(self) -> None:
        snow = self.files["snow.sno"]
        falltmp = next(f for f in snow["fields"] if f["fortran_name"] == "falltmp")
        self.assertEqual(falltmp["units"], "deg C")
        self.assertEqual(falltmp["doc"], "snowfall temp")

    def test_indirect_file_cio_slot_resolves(self) -> None:
        # snow.sno is opened via file=in_parmdb%snow, not a literal.
        self.assertEqual(self.files["snow.sno"]["reader"], "mod.f90")

    def test_field_list_pattern_with_continuation(self) -> None:
        # The manure read spans an '&' continuation line; all 3 fields must appear.
        manure = self.files["manure_om.frt"]
        self.assertEqual(manure["read_pattern"], "field_list")
        names = [f["fortran_name"] for f in manure["fields"]]
        self.assertEqual(names, ["name", "frac_water", "description"])
        self.assertEqual([f["numeric"] for f in manure["fields"]], [False, True, False])

    def test_field_list_units_not_polluted_by_prior_comment(self) -> None:
        manure = self.files["manure_om.frt"]
        frac = next(f for f in manure["fields"] if f["fortran_name"] == "frac_water")
        self.assertEqual(frac["units"], "kg/kg")

    def test_unresolvable_component_is_reported_not_guessed(self) -> None:
        # mystery.xyz reads a component of an unknown type -> unresolved.
        self.assertNotIn("mystery.xyz", self.files)
        reasons = {e["file"]: e["reason"] for e in self.payload["unresolved"]}
        self.assertIn("mystery.xyz", reasons)

    def test_missing_reader_is_reported(self) -> None:
        reasons = {e["file"]: e["reason"] for e in self.payload["unresolved"]}
        self.assertIn("absent.dat", reasons)

    def test_positions_are_sequential(self) -> None:
        for entry in self.files.values():
            self.assertEqual(
                [f["position"] for f in entry["fields"]],
                list(range(len(entry["fields"]))),
            )


class DummyArgAndUnderscoreExtensionTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(DUMMY_ARG_FIXTURE)
        self.payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("hru.con", "channel.con", "initial.cha_cs"),
        )
        self.files = self.payload["files"]

    def test_underscore_extension_literal_resolves(self) -> None:
        # "initial.cha_cs" was previously invisible: the literal-filename
        # regex required an alphanumeric-only extension.
        self.assertIn("initial.cha_cs", self.files)
        names = [f["fortran_name"] for f in self.files["initial.cha_cs"]["fields"]]
        self.assertEqual(names, ["num", "name"])

    def test_dummy_arg_filename_resolves_per_call_site(self) -> None:
        # shared_con_read's `open` names its own dummy argument `con_file`;
        # each caller passes a different `file.cio` slot, so both files
        # resolve to the SAME reader and schema, not just the first one.
        self.assertIn("hru.con", self.files)
        self.assertIn("channel.con", self.files)
        self.assertEqual(self.files["hru.con"], self.files["channel.con"])
        names = [f["fortran_name"] for f in self.files["hru.con"]["fields"]]
        self.assertEqual(names, ["num", "name"])
        self.assertEqual(self.files["hru.con"]["reader"], "mod.f90")


class ReusedUnitAttributionTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(REUSED_UNIT_FIXTURE)
        self.payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("codes.gw", "cells.gw", "zones.gw"),
        )
        self.files = self.payload["files"]

    def test_each_file_gets_its_own_schema(self) -> None:
        # Without per-open attribution, "longest read wins across the whole
        # procedure" would give every file zones.gw's 3-field schema.
        self.assertEqual(
            [f["fortran_name"] for f in self.files["cells.gw"]["fields"]],
            ["id", "value_a"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in self.files["zones.gw"]["fields"]],
            ["name", "value_b", "value_c"],
        )

    def test_file_with_no_data_read_does_not_inherit_a_sibling_schema(self) -> None:
        # codes.gw only reads a scalar config flag in this procedure -- no
        # derived-type record -- so it must not resolve at all, let alone to
        # cells.gw's or zones.gw's schema.
        self.assertNotIn("codes.gw", self.files)
        reasons = {e["file"]: e["reason"] for e in self.payload["unresolved"]}
        self.assertIn("codes.gw", reasons)


# Reproduces a real misattribution: gwflow_read.f90 opens codes.gw (a
# key=value config file, no per-record schema) and, much later in the same
# procedure, does internal reads from a character array
# (`read(split_fields(N),*) var`) that belong to a DIFFERENT file's
# hand-parsed rows entirely. Those internal reads were never matched to any
# `open`'s unit (their "unit" is a parenthesized expression, not a real file
# unit), so before the fix they fell into one shared orphan bucket and the
# "try any open in the procedure" fallback wrongly attributed them to
# codes.gw -- the first file this procedure happens to open.
ORPHAN_INTERNAL_READ_FIXTURE = """
      module cell_module
      integer :: gw_state_stat = 0
      end module cell_module

      subroutine gwflow_read_like
      use cell_module
      character (len=200) :: split_line_buf = ""
      character (len=40), dimension (30) :: split_fields
      integer :: config_flag = 0

      open (107,file="codes.gw")
      read (107,*,iostat=eof) config_flag
      close (107)

      open (108,file="cells.gw")
      read (108,'(a)') split_line_buf
      read (split_fields(4),*) gw_state_stat
      close (108)
      end subroutine gwflow_read_like
"""


class OrphanInternalReadAttributionTests(unittest.TestCase):
    def test_internal_read_is_not_misattributed_to_an_earlier_file(self) -> None:
        project = scan_source(ORPHAN_INTERNAL_READ_FIXTURE)
        payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("codes.gw", "cells.gw"),
        )
        # codes.gw has no real record read -- it must not resolve at all,
        # and it must especially not pick up gw_state_stat from a read that
        # belongs (if anywhere, once a positional extractor exists) to
        # cells.gw, opened on an entirely different unit much later.
        self.assertNotIn("codes.gw", payload["files"])



RUNTIME_FILENAME_BLOCK_FIXTURE = """
      module station_module
      type station_rec
        character(len=40) :: name = ""
        character(len=80) :: filename = ""
        real :: value_a = 0.
        real :: value_b = 0.
      end type station_rec
      type (station_rec), dimension(:), allocatable :: station
      end module station_module

      subroutine station_read_like
      use station_module
      integer :: i = 1, eof = 0
      open (107,file="station.cli")
      read (107,*,iostat=eof) station(i)%name, station(i)%filename
      close (107)
      open (108,file=station(i)%filename)
      read (108,*,iostat=eof) station(i)%value_a, station(i)%value_b
      close (108)
      end subroutine station_read_like
"""


class RuntimeFilenameBlockAttributionTests(unittest.TestCase):
    def test_runtime_filename_block_does_not_borrow_sibling_filename(self) -> None:
        project = scan_source(RUNTIME_FILENAME_BLOCK_FIXTURE)
        proc = next(p for p in project.procedures if p.name == "station_read_like")
        results, reason = analyze_procedure(proc, SchemaResolver(project))
        self.assertIsNone(reason)
        self.assertEqual([result.filename for result in results], ["station.cli"])
        self.assertEqual(
            [f.fortran_name for f in results[0].schema.fields],
            ["name", "filename"],
        )

class CollidingSiblingFieldNamesTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(COLLIDING_SIBLINGS_FIXTURE)
        self.payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("recall_db.rec",),
        )
        self.fields = self.payload["files"]["recall_db.rec"]["fields"]

    def test_colliding_chains_get_prefixed(self) -> None:
        names = [f["fortran_name"] for f in self.fields]
        self.assertEqual(
            names,
            ["k", "name", "org_min.name", "org_min.units", "org_min.tstep",
             "pest.name", "pest.units", "pest.tstep"],
        )
        self.assertEqual(len(names), len(set(names)))

    def test_unambiguous_chain_in_the_same_read_is_not_prefixed(self) -> None:
        # recall_db(i)%name resolves to a single scalar field with no
        # sibling collision -- it must stay "name", not "recall_db.name",
        # even though this same read also triggers prefixing elsewhere.
        names = [f["fortran_name"] for f in self.fields]
        self.assertIn("name", names)

    def test_no_collision_no_prefix(self) -> None:
        # The dummy-arg fixture's con_record read (num, name) has no sibling
        # collision, so its field names must be untouched by this fix.
        project = scan_source(DUMMY_ARG_FIXTURE)
        payload = build_schema(
            project, swatplus_version="0.0.0", source_ref="test", generator="test",
            targets=("hru.con",),
        )
        names = [f["fortran_name"] for f in payload["files"]["hru.con"]["fields"]]
        self.assertEqual(names, ["num", "name"])


INTRINSIC_RECORD_FIXTURE = """
      module grid_module
      integer, dimension (:), allocatable :: cell_id
      real, dimension (:), allocatable :: cell_area
      integer :: ncell = 0
      end module grid_module

      subroutine grid_read
      use grid_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: i = 0
      integer :: imax = 0
      real :: depth = 0.
      integer :: nout = 0
      open (107,file="grid.gw")
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do i = 1, ncell
        read (107,*,iostat=eof) cell_id(i), cell_area(i), depth
      end do
      close (107)
      end subroutine grid_read

      subroutine counter_read
      use grid_module
      integer :: i = 0
      integer :: imax = 0
      open (107,file="counted.gw")
      read (107,*,iostat=eof) imax
      do while (eof == 0)
        read (107,*,iostat=eof) i
      end do
      close (107)
      end subroutine counter_read

      subroutine scalar_read
      use grid_module
      character (len=80) :: titldum = ""
      integer :: n_lyr = 0
      open (107,file="scalar.gw")
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) n_lyr
      close (107)
      end subroutine scalar_read

      subroutine peek_read
      use grid_module
      integer :: i = 0
      integer :: numb = 0
      integer :: nspu = 0
      character (len=16) :: namedum = ""
      integer, dimension (100) :: elem_cnt
      integer :: isp = 0
      open (107,file="peeked.def")
      do i = 1, ncell
        read (107,*,iostat=eof) numb, namedum, nspu
        backspace (107)
        read (107,*,iostat=eof) numb, namedum, nspu, (elem_cnt(isp), isp = 1, nspu)
      end do
      close (107)
      end subroutine peek_read
"""


# Mirrors the *.con family's real shape: the implied-do's count ("nout") is
# not itself a prefix field -- it's a local variable assigned from one,
# `nout = ob(i)%src_tot` (the same SWAT+ idiom hyd_read_connect.f90 uses),
# so binding it requires tracing the assignment, not a direct name match.
ASSIGNMENT_TRACED_FIXTURE = """
      module con_module
      type object_connectivity
        integer :: num = 0
        character(len=16) :: name = ""
        integer :: src_tot = 0
        character(len=3), dimension (:), allocatable :: obtyp_out
        real, dimension (:), allocatable :: frac_out
      end type object_connectivity
      type (object_connectivity), dimension(:), allocatable :: ob
      end module con_module

      subroutine hyd_read_connect_like
      use con_module
      integer :: i = 0
      integer :: nout = 0
      integer :: isp = 0
      open (107,file="hru.con")
      do i = 1, 5
        read (107,*,iostat=eof) ob(i)%num, ob(i)%name, ob(i)%src_tot
        nout = ob(i)%src_tot
        backspace (107)
        read (107,*,iostat=eof) ob(i)%num, ob(i)%name, ob(i)%src_tot,        &
          (ob(i)%obtyp_out(isp), ob(i)%frac_out(isp), isp = 1, nout)
      end do
      close (107)
      end subroutine hyd_read_connect_like

      subroutine external_count_read
      use con_module
      integer :: ipest = 0
      integer, dimension (100) :: pest_frac
      open (107,file="external.exc")
      do
        read (107,*,iostat=eof) (pest_frac(ipest), ipest = 1, cs_db_num_pests)
      end do
      close (107)
      end subroutine external_count_read

      subroutine multi_repeat_read
      use con_module
      integer :: n1 = 0
      integer :: n2 = 0
      integer :: i1 = 0
      integer :: i2 = 0
      integer, dimension (100) :: arr1
      integer, dimension (100) :: arr2
      open (107,file="multi.rep")
      do
        read (107,*,iostat=eof) n1, n2, (arr1(i1), i1 = 1, n1), (arr2(i2), i2 = 1, n2)
      end do
      close (107)
      end subroutine multi_repeat_read
"""


class RecordLayoutTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(ASSIGNMENT_TRACED_FIXTURE)
        self.payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("hru.con", "external.exc", "multi.rep"),
        )
        self.files = self.payload["files"]

    def test_count_traced_through_an_assignment(self) -> None:
        # "nout" isn't a prefix field; it's assigned from ob(i)%src_tot,
        # which IS -- the *.con files' real pattern.
        entry = self.files["hru.con"]
        self.assertTrue(entry["variable_arity"])
        self.assertEqual(
            [f["fortran_name"] for f in entry["fields"]], ["num", "name", "src_tot"]
        )
        rep = entry["repeat"]
        self.assertEqual(rep["count_field"], "src_tot")
        self.assertEqual(rep["count_expr"], "nout")
        self.assertEqual(
            [f["fortran_name"] for f in rep["fields"]], ["obtyp_out", "frac_out"]
        )

    def test_externally_governed_count_is_not_bound(self) -> None:
        # cs_db_num_pests never appears as a field in this record -- there
        # is nothing here to bind the repeat count to, so this must not
        # resolve at all rather than guess.
        self.assertNotIn("external.exc", self.files)
        reasons = {e["file"]: e["reason"] for e in self.payload["unresolved"]}
        self.assertIn("external.exc", reasons)

    def test_more_than_one_repeat_group_declines(self) -> None:
        # Two implied-dos in one record is outside what this resolves;
        # must not guess which one is "the" repeat group.
        self.assertNotIn("multi.rep", self.files)


# Mirrors chan-surf.lin: the repeat count is read by an earlier *peek* into a
# throwaway local (`nspu`), then the reader backspaces and re-reads the whole
# record. `nspu` isn't a field of the record and isn't assigned from one, so
# only the peek's column alignment ties it to the record's last fixed field.
PEEK_COUNT_FIXTURE = """
      module link_module
      type fp_link
        integer :: numb = 0
        character(len=16) :: name = ""
        integer :: obj_tot = 0
        character(len=3), dimension (:), allocatable :: obtyp
        integer, dimension (:), allocatable :: obtypno
      end type fp_link
      type (fp_link), dimension(:), allocatable :: sd_ch
      end module link_module

      subroutine overbank_like_read
      use link_module
      integer :: i = 0, ise = 0, isp = 0, nspu = 0, eof = 0
      character(len=16) :: namedum = ""
      open (107,file="chan-surf.lin")
      do ise = 1, 5
        read (107,*,iostat=eof) i, namedum, nspu
        if (nspu > 0) then
          backspace (107)
          read (107,*,iostat=eof) sd_ch(i)%numb, sd_ch(i)%name, sd_ch(i)%obj_tot, &
            (sd_ch(i)%obtyp(isp), sd_ch(i)%obtypno(isp), isp = 1, nspu)
        end if
      end do
      close (107)
      end subroutine overbank_like_read
"""


class PeekCountBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(PEEK_COUNT_FIXTURE)
        self.files = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("chan-surf.lin",),
        )["files"]

    def test_count_bound_to_last_fixed_field_via_peek(self) -> None:
        entry = self.files["chan-surf.lin"]
        self.assertTrue(entry["variable_arity"])
        self.assertEqual(
            [f["fortran_name"] for f in entry["fields"]], ["numb", "name", "obj_tot"]
        )
        rep = entry["repeat"]
        # The bound is the throwaway `nspu`, but it binds to the record's own
        # last fixed field, obj_tot, via the peek's column alignment.
        self.assertEqual(rep["count_expr"], "nspu")
        self.assertEqual(rep["count_field"], "obj_tot")
        self.assertEqual(
            [f["fortran_name"] for f in rep["fields"]], ["obtyp", "obtypno"]
        )

    def test_peek_then_reread_does_not_become_a_second_block(self) -> None:
        # The peek (`i, namedum, nspu`) targets plain throwaway locals -- it
        # never resolves to a schema at all -- so this block has exactly one
        # real candidate and must not grow a `blocks` list.
        self.assertNotIn("blocks", self.files["chan-surf.lin"])


# Mirrors print.prt's real shape (basin_print_codes_read.f90): one `open`,
# then several UNRELATED sequential scalar reads (each its own statement, no
# backspace between them), a genuine count-then-backspace-reread peek, and a
# `do`-loop of many rows that all share one record shape. Each distinct group
# must survive as its own block; the peek must collapse into its fuller
# reread; the repeated rows must collapse into a single representative --
# never one block per read statement, and never dropped in favor of a single
# "biggest wins" pick.
MULTI_GROUP_FIXTURE = """
      module demo_module
      type demo_a
        real :: alpha = 0.       !kg     |alpha value
        real :: beta = 0.        !kg     |beta value
        real :: gamma = 0.       !kg     |gamma value
        real :: delta = 0.       !kg     |delta value
      end type demo_a
      type (demo_a) :: da

      type demo_b
        character(len=16) :: mode = "" !          |output mode
        character(len=16) :: fmt = ""  !          |output format
      end type demo_b
      type (demo_b) :: db

      type demo_row
        character(len=16) :: nm = "" !          |row name
        real :: v1 = 0.              !          |value one
        real :: v2 = 0.              !          |value two
      end type demo_row
      type (demo_row), dimension(:), allocatable :: rows

      integer :: cnt = 0
      integer, dimension(:), allocatable :: items
      end module demo_module

      subroutine demo_read
      use demo_module
      character (len=80) :: header = ""
      integer :: eof = 0
      integer :: i = 0, ii = 0
      open (107,file="demo.dat")
      read (107,*,iostat=eof) header
      read (107,*,iostat=eof) da%alpha, da%beta, da%gamma, da%delta
      read (107,*,iostat=eof) header
      read (107,*,iostat=eof) db%mode, db%fmt
      read (107,*,iostat=eof) cnt
      if (cnt > 0) then
        allocate (items(cnt), source = 0)
        backspace (107)
        read (107,*,iostat=eof) cnt, (items(ii), ii = 1, cnt)
      end if
      do i = 1, 3
        read (107,*,iostat=eof) rows(i)%nm, rows(i)%v1, rows(i)%v2
      end do
      close (107)
      end subroutine demo_read
"""


class MultiGroupBlockTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(MULTI_GROUP_FIXTURE)
        self.payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("demo.dat",),
        )
        self.entry = self.payload["files"]["demo.dat"]

    def test_every_distinct_group_survives_as_its_own_block(self) -> None:
        blocks = self.entry["blocks"]
        signatures = [tuple(f["fortran_name"] for f in b["fields"]) for b in blocks]
        self.assertEqual(
            sorted(signatures),
            sorted(
                [
                    ("cnt",),  # the count/repeat block, repeat carries `items`
                    ("alpha", "beta", "gamma", "delta"),
                    ("mode", "fmt"),
                    ("nm", "v1", "v2"),
                ]
            ),
        )
        # Exactly four -- not one block per `read` statement (the `do`-loop
        # alone is three identical-shape reads that must collapse to one).
        self.assertEqual(len(blocks), 4)

    def test_repeated_row_shape_collapses_to_one_representative(self) -> None:
        blocks = self.entry["blocks"]
        row_blocks = [b for b in blocks if [f["fortran_name"] for f in b["fields"]] == ["nm", "v1", "v2"]]
        self.assertEqual(len(row_blocks), 1)

    def test_peek_then_reread_collapses_into_the_repeat_block_not_a_bare_prefix(self) -> None:
        blocks = self.entry["blocks"]
        count_block = next(b for b in blocks if [f["fortran_name"] for f in b["fields"]] == ["cnt"])
        self.assertIn("repeat", count_block)
        self.assertEqual(
            [f["fortran_name"] for f in count_block["repeat"]["fields"]], ["items"]
        )

    def test_top_level_fields_stay_the_single_richest_block_for_backward_compat(self) -> None:
        # A consumer that only reads `fields`/`repeat` (ignoring `blocks`)
        # must see exactly what the old single-"best"-schema selection would
        # have produced: the repeat/structured block beats every plain one.
        self.assertEqual([f["fortran_name"] for f in self.entry["fields"]], ["cnt"])
        self.assertTrue(self.entry["variable_arity"])
        self.assertEqual(
            [f["fortran_name"] for f in self.entry["repeat"]["fields"]], ["items"]
        )

    def test_each_block_keeps_its_own_reader_line_and_derived_type(self) -> None:
        blocks = self.entry["blocks"]
        by_signature = {
            tuple(f["fortran_name"] for f in b["fields"]): b for b in blocks
        }
        self.assertEqual(by_signature[("alpha", "beta", "gamma", "delta")]["derived_type"], "demo_a")
        self.assertEqual(by_signature[("mode", "fmt")]["derived_type"], "demo_b")
        self.assertEqual(by_signature[("nm", "v1", "v2")]["derived_type"], "demo_row")
        # Distinct groups keep distinct source lines -- proof they came from
        # separate `read` statements, not one split apart.
        lines = {b["reader_line"] for b in blocks}
        self.assertEqual(len(lines), len(blocks))


SINGLE_BLOCK_UNCHANGED_FIXTURE = """
      module single_module
      type single_rec
        integer :: n = 0    !none   |count
        real :: x = 0.      !mm     |x value
      end type single_rec
      type (single_rec) :: rec1
      end module single_module

      subroutine single_read
      use single_module
      open (107,file="single.dat")
      read (107,*) rec1%n, rec1%x
      close (107)
      end subroutine single_read
"""


class SingleBlockShapeUnchangedTests(unittest.TestCase):
    def test_a_block_with_one_candidate_gets_no_blocks_key(self) -> None:
        # The overwhelming common case (one `open`, one real record read)
        # must keep exactly the pre-existing payload shape -- no `blocks`
        # key at all -- so every already-shipped single-block schema entry
        # is byte-for-byte unaffected by this change.
        project = scan_source(SINGLE_BLOCK_UNCHANGED_FIXTURE)
        payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("single.dat",),
        )
        entry = payload["files"]["single.dat"]
        self.assertNotIn("blocks", entry)
        self.assertEqual([f["fortran_name"] for f in entry["fields"]], ["n", "x"])


# Mirrors cells.gw's real shape: a row is read into a text buffer, split into
# a character array, then read back out one column at a time -- plus one
# column (name) copied via assignment rather than a read, and two optional
# trailing columns (SWAT+'s `if(nf >= N) read(fields(N),*) var` idiom for
# "added later, absent in old files" columns).
POSITIONAL_EXTRACTION_FIXTURE = """
      module cell_module
      integer :: cell_id_val = 0
      character(len=40) :: cell_name_val = ""
      real :: cell_elev_val = 0.
      real :: cell_thck_val = 0.
      real :: cell_strk_over_val = 0.
      end module cell_module

      subroutine cell_read
      use cell_module
      character (len=200) :: split_line_buf = ""
      character (len=40), dimension (30) :: split_fields
      integer :: nf = 0
      integer :: i = 0
      open (107,file="cells.gw")
      read (107,*) header
      read (107,*) header
      do i = 1, 5
        read (107,'(a)') split_line_buf
        call split_line(split_line_buf, split_fields, nf)
        read (split_fields(1),*) cell_id_val
        cell_name_val = trim(split_fields(2))
        read (split_fields(3),*) cell_elev_val
        read (split_fields(4),*) cell_thck_val
        if (nf >= 5) read (split_fields(5),*) cell_strk_over_val
      end do
      close (107)
      end subroutine cell_read

      subroutine embedded_repeat_read
      use cell_module
      character (len=200) :: split_line_buf = ""
      character (len=40), dimension (30) :: split_fields
      integer :: ncon = 0
      integer :: j = 0
      integer, dimension (100) :: cell_con_id
      open (107,file="cellcon.gw")
      do i = 1, 5
        read (107,'(a)') split_line_buf
        call split_line(split_line_buf, split_fields, nf)
        read (split_fields(1),*) cell_id_val
        read (split_fields(2),*) ncon
        do j = 1, ncon
          read (split_fields(2+j),*) cell_con_id(j)
        end do
      end do
      close (107)
      end subroutine embedded_repeat_read

      subroutine keyed_record_read
      use cell_module
      character (len=200) :: split_line_buf = ""
      character (len=40), dimension (30) :: split_fields
      integer :: combined_yrday = 0
      integer :: obs_cell = 0
      open (107,file="outputs.gw")
      do
        read (107,'(a)',iostat=eof) split_line_buf
        if (eof /= 0) exit
        call split_line(split_line_buf, split_fields, nf)
        select case (trim(split_fields(1)))
        case ("head_output_time")
          read (split_fields(2),*) combined_yrday
        case ("observation_cell")
          read (split_fields(2),*) obs_cell
        end select
      end do
      close (107)
      end subroutine keyed_record_read
"""


class PositionalExtractionTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(POSITIONAL_EXTRACTION_FIXTURE)
        self.payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("cells.gw", "cellcon.gw", "outputs.gw"),
        )
        self.files = self.payload["files"]

    def test_columns_from_reads_and_one_assignment_resolve_in_order(self) -> None:
        entry = self.files["cells.gw"]
        self.assertEqual(entry["read_pattern"], "positional")
        self.assertEqual(
            [f["fortran_name"] for f in entry["fields"]],
            ["cell_id_val", "cell_name_val", "cell_elev_val", "cell_thck_val"],
        )
        # Known, separate gap: `if (nf >= 5) read (split_fields(5),*) ...` on
        # one line is invisible to the scanner entirely -- I/O-operation
        # detection requires the line to *start* with the keyword, and here
        # it starts with "if". So the optional 5th column this record
        # actually has is silently absent rather than wrongly included --
        # consistent with this module's find-nothing-over-guess-wrong rule,
        # but real, uncaptured coverage (also costs chancell.gw's last two
        # columns for the same reason). Fixing it means recognizing a
        # single-line if as a condition prefix to strip and reprocess the
        # remainder, not something this extractor does on its own.
        self.assertNotIn("cell_strk_over_val", [f["fortran_name"] for f in entry["fields"]])

    def test_dynamic_index_declines_not_a_wrong_prefix(self) -> None:
        # `split_fields(2+j)` is a computed index -- a data-dependent repeat
        # group, the same shape record_layout handles for list-directed
        # reads, just expressed one internal read at a time here. Not
        # implemented for this extractor; must decline rather than publish
        # just the two fixed columns as if they were the whole record.
        self.assertNotIn("cellcon.gw", self.files)

    def test_conflicting_targets_resolve_as_a_tagged_column(self) -> None:
        # Column 2 means something different in each case branch -- a
        # keyed/tagged record. Rather than decline outright, this resolves
        # as a tagged column: the select case's own literal vocabulary
        # names each variant, so nothing here is guessed.
        entry = self.files["outputs.gw"]
        self.assertEqual(entry["fields"], [])
        self.assertEqual(entry["tag_field"], "split_fields(1)")
        variants = {v["tag"]: v for v in entry["variants"]}
        self.assertEqual(set(variants), {"head_output_time", "observation_cell"})
        self.assertEqual(
            [f["fortran_name"] for f in variants["head_output_time"]["fields"]],
            ["combined_yrday"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in variants["observation_cell"]["fields"]],
            ["obs_cell"],
        )


class IntrinsicRecordReadTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(INTRINSIC_RECORD_FIXTURE)
        self.payload = build_schema(
            project,
            swatplus_version="0.0.0",
            source_ref="test",
            generator="test",
            targets=("grid.gw", "counted.gw", "scalar.gw", "peeked.def"),
        )
        self.files = self.payload["files"]

    def test_plain_intrinsic_columns_resolve(self) -> None:
        # No derived type anywhere in this read -- it used to be discarded.
        names = [f["fortran_name"] for f in self.files["grid.gw"]["fields"]]
        self.assertEqual(names, ["cell_id", "cell_area", "depth"])
        self.assertEqual(
            [f["numeric"] for f in self.files["grid.gw"]["fields"]], [True, True, True]
        )

    def test_record_counting_prepass_is_not_a_schema(self) -> None:
        # `do while (eof == 0); read (107,*) i` is the ubiquitous SWAT+
        # record-counting idiom, not a one-column record.
        self.assertNotIn("counted.gw", self.files)

    def test_scalar_config_read_outside_a_loop_is_not_a_schema(self) -> None:
        # Read once, not per record -- a config value, not a table.
        self.assertNotIn("scalar.gw", self.files)

    def test_peeked_prefix_resolves_as_a_repeat_group_not_a_bare_prefix(self) -> None:
        # The reader peeks at the fixed prefix, backspaces, then re-reads the
        # whole record with an implied-do tail bounded by "nspu" -- itself
        # one of the prefix's own bare targets. That's provable enough to
        # resolve as prefix + repeat group (see RecordLayoutTests), so this
        # must NOT fall back to publishing just the 3-column peek as if it
        # were the whole record.
        entry = self.files["peeked.def"]
        self.assertTrue(entry["variable_arity"])
        self.assertEqual(
            [f["fortran_name"] for f in entry["fields"]], ["numb", "namedum", "nspu"]
        )
        self.assertEqual(entry["repeat"]["count_field"], "nspu")
        self.assertEqual(
            [f["fortran_name"] for f in entry["repeat"]["fields"]], ["elem_cnt"]
        )


# Mirrors the shape shared by all four real *.dtl readers (dtbl_lum_read.f90,
# dtbl_res_read.f90, dtbl_scen_read.f90, dtbl_flocon_read.f90): a
# `conditional_module`-style trio of types (conditions_var, actions_var,
# decision_table), a shared `conditions` dispatcher whose select-case on
# `%cond(ic)%var` is the COND_VAR vocabulary, and a reader with the header +
# two-block shape, ending with its own `%act(iac)%typ` select-case.
DECISION_TABLE_FIXTURE = """
      module input_file_module
      implicit none
      type input_condition
        character(len=25) :: dtbl_fix = "fixture.dtl"
      end type input_condition
      type (input_condition) :: in_cond
      end module input_file_module

      module conditional_module
      implicit none
      type conditions_var
        character(len=25) :: var = ""       ! condition variable
        character(len=25) :: ob = ""        ! object variable
        integer :: ob_num = 0               ! object number
        character(len=25) :: lim_var = ""   ! limit variable
        character(len=25) :: lim_op = ""    ! limit operator
        real :: lim_const = 0.              ! limit constant
      end type conditions_var

      type actions_var
        character(len=25) :: typ = ""       ! type of action
        character(len=25) :: ob = ""        ! object variable
        integer :: ob_num = 0               ! object number
        character(len=25) :: name = ""      ! name of action
        character(len=40) :: option = ""    ! action option
        real :: const = 0.                  ! constant
        real :: const2 = 1                  ! additional constant
        character(len=25) :: file_pointer = ""! pointer for option
      end type actions_var

      type decision_table
        character (len=40) :: name = ""     ! name of the decision table
        integer :: conds = 0                ! number of conditions
        integer :: alts = 0                 ! number of alternatives
        integer :: acts = 0                 ! number of actions
        type (conditions_var), dimension(:), allocatable :: cond
        character(len=25), dimension(:,:), allocatable :: alt
        type (actions_var), dimension(:), allocatable :: act
        character(len=1), dimension(:,:), allocatable :: act_outcomes
      end type decision_table
      type (decision_table), dimension(:), allocatable :: dtbl_fix
      type (decision_table), pointer :: d_tbl
      end module conditional_module

      subroutine conditions (ob_cur, idtbl)
      use conditional_module
      implicit none
      integer :: ob_cur, idtbl
      integer :: ic = 0
      select case (d_tbl%cond(ic)%var)
      case ("sw")
        ic = 1
      case ("time")
        ic = 2
      end select
      end subroutine conditions

      subroutine dtbl_fix_read
      use conditional_module
      use input_file_module
      implicit none
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0
      integer :: i = 0
      integer :: mdtbl = 0
      integer :: ic = 0
      integer :: ial = 0
      integer :: iac = 0

      open (107,file=in_cond%dtbl_fix)
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) mdtbl
      read (107,*,iostat=eof)
      allocate (dtbl_fix(1:mdtbl))
      do i = 1, mdtbl
        read (107,*,iostat=eof) header
        read (107,*,iostat=eof) dtbl_fix(i)%name, dtbl_fix(i)%conds, dtbl_fix(i)%alts, dtbl_fix(i)%acts
        read (107,*,iostat=eof) header
        do ic = 1, dtbl_fix(i)%conds
          read (107,*,iostat=eof) dtbl_fix(i)%cond(ic), (dtbl_fix(i)%alt(ic,ial), ial = 1, dtbl_fix(i)%alts)
        end do
        read (107,*,iostat=eof) header
        do iac = 1, dtbl_fix(i)%acts
          read (107,*,iostat=eof) dtbl_fix(i)%act(iac), (dtbl_fix(i)%act_outcomes(iac,ial), ial = 1, dtbl_fix(i)%alts)
        end do
        do iac = 1, dtbl_fix(i)%acts
          select case (dtbl_fix(i)%act(iac)%typ)
          case ("plant")
            ic = 1
          case ("harvest")
            ic = 2
          end select
        end do
      end do
      close (107)
      end subroutine dtbl_fix_read
"""


class DecisionTableSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(DECISION_TABLE_FIXTURE)
        resolver = SchemaResolver(project)
        self.files, self.unresolved = build_decision_tables(
            project, resolver, targets=("fixture.dtl",)
        )

    def test_resolves_with_no_unresolved(self) -> None:
        self.assertEqual(self.unresolved, [])
        self.assertIn("fixture.dtl", self.files)

    def test_header_fields(self) -> None:
        header = self.files["fixture.dtl"]["header"]["fields"]
        self.assertEqual(
            [f["fortran_name"] for f in header], ["name", "conds", "alts", "acts"]
        )

    def test_condition_block_row_and_repeat(self) -> None:
        block = self.files["fixture.dtl"]["condition_block"]
        self.assertEqual(block["row_count_field"], "conds")
        self.assertEqual(
            [f["fortran_name"] for f in block["row"]["fields"]],
            ["var", "ob", "ob_num", "lim_var", "lim_op", "lim_const"],
        )
        self.assertEqual(block["row"]["repeat"]["count_field"], "alts")
        self.assertEqual(
            [f["fortran_name"] for f in block["row"]["repeat"]["fields"]], ["alt"]
        )

    def test_action_block_row_and_repeat(self) -> None:
        block = self.files["fixture.dtl"]["action_block"]
        self.assertEqual(block["row_count_field"], "acts")
        self.assertEqual(
            [f["fortran_name"] for f in block["row"]["fields"]],
            ["typ", "ob", "ob_num", "name", "option", "const", "const2", "file_pointer"],
        )
        self.assertEqual(block["row"]["repeat"]["count_field"], "alts")
        self.assertEqual(
            [f["fortran_name"] for f in block["row"]["repeat"]["fields"]], ["act_outcomes"]
        )

    def test_vocabulary_captured_from_select_case(self) -> None:
        vocab = self.files["fixture.dtl"]["vocabulary"]
        self.assertEqual(vocab["condition_var"], ["sw", "time"])
        self.assertEqual(vocab["action_typ"], ["plant", "harvest"])
        self.assertEqual(vocab["other"], [])

    def test_missing_file_is_unresolved(self) -> None:
        project = scan_source(DECISION_TABLE_FIXTURE)
        resolver = SchemaResolver(project)
        _files, unresolved = build_decision_tables(
            project, resolver, targets=("not_a_table.dtl",)
        )
        self.assertEqual(
            unresolved, [{"file": "not_a_table.dtl", "reason": "reader not found for filename"}]
        )


# Mirrors the real soils.sol / plant.ini shape: a header record naming several
# components of one derived-type instance, then a `do`-loop of sub-records
# naming components of that same instance, where the loop bound traces (through
# a local assignment) to a count column in the header. Includes the SWAT+
# idioms that must NOT fool the detector: a counting pre-pass over throwaway
# targets, and a peek+backspace pair where the wider read is the real header.
MULTI_RECORD_FIXTURE = """
      module soil_data_module
      implicit none
      type soil_layer
        real :: z = 0.
        real :: bd = 0.
        real :: awc = 0.
      end type soil_layer
      type soil_header
        character(len=40) :: snam = ""
        integer :: nly = 0
        character(len=1) :: hydgrp = ""
        real :: zmx = 0.
      end type soil_header
      type soil_database
        type (soil_header) :: s
        type (soil_layer), dimension(:), allocatable :: ly
      end type soil_database
      type (soil_database), dimension(:), allocatable :: soildb
      end module soil_data_module

      subroutine soil_fixture_read
      use soil_data_module
      implicit none
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0
      integer :: nlyr = 0
      integer :: lyr = 0
      integer :: mlyr = 0
      integer :: isol = 0
      integer :: j = 0
      open (107,file="fixture.sol")
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do while (eof == 0)
        read (107,*,iostat=eof) titldum, nlyr
        do lyr = 1, nlyr
          read (107,*,iostat=eof) titldum
        end do
      end do
      rewind (107)
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do isol = 1, 3
        read (107,*,iostat=eof) soildb(isol)%s%snam, soildb(isol)%s%nly
        mlyr = soildb(isol)%s%nly
        backspace 107
        read (107,*,iostat=eof) soildb(isol)%s%snam, soildb(isol)%s%nly,   &
          soildb(isol)%s%hydgrp, soildb(isol)%s%zmx
        do j = 1, mlyr
          read (107,*,iostat=eof) soildb(isol)%ly(j)%z, soildb(isol)%ly(j)%bd, &
            soildb(isol)%ly(j)%awc
        end do
      end do
      close (107)
      end subroutine soil_fixture_read
"""


class MultiRecordSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(MULTI_RECORD_FIXTURE)
        resolver = SchemaResolver(project)
        self.files, self.unresolved = build_multi_records(
            project, resolver, targets=("fixture.sol",)
        )

    def test_resolves_with_no_unresolved(self) -> None:
        self.assertEqual(self.unresolved, [])
        self.assertIn("fixture.sol", self.files)

    def test_header_is_the_wider_read_not_the_peek(self) -> None:
        # Two same-instance reads sit at the header's depth -- a 2-column peek
        # and the 4-column full read. The full read is the header; picking the
        # peek would drop hydgrp/zmx.
        header = self.files["fixture.sol"]["header"]["fields"]
        self.assertEqual(
            [f["fortran_name"] for f in header], ["snam", "nly", "hydgrp", "zmx"]
        )

    def test_sub_block_bound_traces_to_header_column(self) -> None:
        blocks = self.files["fixture.sol"]["blocks"]
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["count_field"], "nly")
        self.assertEqual(
            [f["fortran_name"] for f in blocks[0]["row"]["fields"]], ["z", "bd", "awc"]
        )

    def test_counting_prepass_does_not_become_a_block(self) -> None:
        # The `titldum, nlyr` / `titldum` pre-pass reads name throwaway
        # targets with no component access, so they never enter the pairing.
        self.assertEqual(len(self.files["fixture.sol"]["blocks"]), 1)

    def test_missing_file_is_unresolved(self) -> None:
        project = scan_source(MULTI_RECORD_FIXTURE)
        resolver = SchemaResolver(project)
        _files, unresolved = build_multi_records(
            project, resolver, targets=("not_here.sol",)
        )
        self.assertEqual(
            unresolved, [{"file": "not_here.sol", "reason": "reader not found for filename"}]
        )


# Mirrors weather-wgn.cli's shape: a station-header line spanning two roots
# (`wgn_n(i)` and `wgn(i)%...`), then a fixed 12-row monthly block whose count
# is the literal `do mo = 1, 12` (not a header column), each row reading one
# element of several `dimension(12)` components.
LITERAL_COUNT_FIXTURE = """
      module wgn_module
      implicit none
      type wgn_rec
        real :: lat = 0.
        real :: elev = 0.
        real, dimension(12) :: tmpmx = 0.
        real, dimension(12) :: pcpmm = 0.
      end type wgn_rec
      type (wgn_rec), dimension(:), allocatable :: wgn
      integer, dimension(:), allocatable :: wgn_n
      end module wgn_module

      subroutine wgn_fixture_read
      use wgn_module
      character (len=80) :: header = ""
      integer :: iwgn = 0, mo = 0, eof = 0
      open (114,file="fixture.wgn")
      do iwgn = 1, 3
        read (114,*,iostat=eof) wgn_n(iwgn), wgn(iwgn)%lat, wgn(iwgn)%elev
        read (114,*,iostat=eof) header
        do mo = 1, 12
          read (114,*,iostat=eof) wgn(iwgn)%tmpmx(mo), wgn(iwgn)%pcpmm(mo)
        end do
      end do
      close (114)
      end subroutine wgn_fixture_read
"""


class MultiRecordLiteralCountTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(LITERAL_COUNT_FIXTURE)
        resolver = SchemaResolver(project)
        self.files, self.unresolved = build_multi_records(
            project, resolver, targets=("fixture.wgn",)
        )

    def test_multi_root_header(self) -> None:
        # The header spans two roots (wgn_n and wgn); both contribute columns.
        self.assertEqual(self.unresolved, [])
        header = self.files["fixture.wgn"]["header"]["fields"]
        self.assertEqual([f["fortran_name"] for f in header], ["wgn_n", "lat", "elev"])

    def test_literal_count_block_and_element_columns(self) -> None:
        blocks = self.files["fixture.wgn"]["blocks"]
        self.assertEqual(len(blocks), 1)
        # A literal `do mo = 1, 12` count is emitted as `count`, not
        # `count_field`, and each subscripted dimension(12) component is one
        # column (not expanded to 12).
        self.assertNotIn("count_field", blocks[0])
        self.assertEqual(blocks[0]["count"], 12)
        self.assertEqual(
            [f["fortran_name"] for f in blocks[0]["row"]["fields"]], ["tmpmx", "pcpmm"]
        )


# Mirrors management.sch: a schedule header (name + two counts), an auto block
# whose rows are keyed (a base `auto_name` read, plus a backspace re-read of a
# wider `auto_name, auto_crop` row for special names), and an operations block
# read in a *called helper* (`read_ops_helper`) on the same open unit.
CROSS_PROC_KEYED_FIXTURE = """
      module sched_module
      implicit none
      type sched_ops
        character(len=40) :: op = ""
        integer :: mon = 0
        integer :: day = 0
      end type sched_ops
      type sched_rec
        character(len=40) :: name = ""
        integer :: num_ops = 0
        integer :: num_autos = 0
        type (sched_ops), dimension(:), allocatable :: ops
        character(len=40), dimension(:), allocatable :: auto_name
        character(len=40), dimension(:), allocatable :: auto_crop
      end type sched_rec
      type (sched_rec), dimension(:), allocatable :: sched
      end module sched_module

      subroutine sched_fixture_read
      use sched_module
      external :: read_ops_helper
      character (len=80) :: header = ""
      integer :: isched = 0, iauto = 0, eof = 0, m_autos = 0
      open (107,file="fixture.sch")
      read (107,*,iostat=eof) header
      do isched = 1, 3
        read (107,*,iostat=eof) sched(isched)%name, sched(isched)%num_ops, sched(isched)%num_autos
        m_autos = sched(isched)%num_autos
        do iauto = 1, m_autos
          read (107,*,iostat=eof) sched(isched)%auto_name(iauto)
          if (sched(isched)%auto_name(iauto) == "pl_hv_summer1") then
            backspace (107)
            read (107,*,iostat=eof) sched(isched)%auto_name(iauto), sched(isched)%auto_crop
          end if
        end do
        call read_ops_helper(isched)
      end do
      close (107)
      end subroutine sched_fixture_read

      subroutine read_ops_helper(isched)
      use sched_module
      integer :: isched, iop = 0
      do iop = 1, sched(isched)%num_ops
        read (107,*) sched(isched)%ops(iop)%op, sched(isched)%ops(iop)%mon, &
          sched(isched)%ops(iop)%day
      end do
      end subroutine read_ops_helper
"""


class MultiRecordCrossProcKeyedTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(CROSS_PROC_KEYED_FIXTURE)
        resolver = SchemaResolver(project)
        self.files, self.unresolved = build_multi_records(
            project, resolver, targets=("fixture.sch",)
        )

    def test_resolves(self) -> None:
        self.assertEqual(self.unresolved, [])
        self.assertIn("fixture.sch", self.files)
        header = self.files["fixture.sch"]["header"]["fields"]
        self.assertEqual(
            [f["fortran_name"] for f in header], ["name", "num_ops", "num_autos"]
        )

    def test_ops_block_pulled_from_called_helper(self) -> None:
        blocks = {b.get("count_field"): b for b in self.files["fixture.sch"]["blocks"]}
        ops = blocks["num_ops"]
        self.assertEqual(
            [f["fortran_name"] for f in ops["row"]["fields"]], ["op", "mon", "day"]
        )
        self.assertNotIn("variable_width", ops)

    def test_keyed_auto_block_is_collapsed_and_variable_width(self) -> None:
        blocks = {b.get("count_field"): b for b in self.files["fixture.sch"]["blocks"]}
        auto = blocks["num_autos"]
        # The base read and the wider backspace re-read collapse to one block;
        # the width disagreement flags it variable_width with only the
        # guaranteed auto_name column.
        self.assertTrue(auto["variable_width"])
        self.assertEqual(
            [f["fortran_name"] for f in auto["row"]["fields"]], ["auto_name"]
        )


# Mirrors manure_allo.mnu's real shape (manure_allocation_read.f90): a header
# names two counts (src_obs, trn_obs), and a single local variable (num_objs)
# is assigned from src_obs, used to allocate the source block, then
# REASSIGNED from trn_obs before the demand block's own `do` loop uses it.
# KNOWN BUG, not yet fixed (see the TARGET_FILES module comment,
# "manure_allo.mnu" entry): _find_count_field returns the FIRST assignment
# to a traced local that matches ANY header column, not the one nearest the
# read it's resolving -- so it resolves num_objs to src_obs for BOTH the
# source and demand sub-blocks. Both then key identically in
# _collapse_multi_record_blocks and collapse into one block, keeping only
# the narrower (demand) columns under the wrong count field. This fixture
# pins that CURRENT (wrong) behavior so a future fix to _find_count_field
# has a regression test to update, not rediscover.
STALE_COUNT_REASSIGNMENT_FIXTURE = """
      module mallo_module
      implicit none
      type mallo_src
        integer :: num = 0
        character(len=20) :: name = ""
        real :: stor_init = 0.
        real :: stor_max = 0.
      end type mallo_src
      type mallo_trn
        integer :: num = 0
        character(len=20) :: kind = ""
      end type mallo_trn
      type mallo_rec
        character(len=20) :: name = ""
        integer :: src_obs = 0
        integer :: trn_obs = 0
        type (mallo_src), dimension(:), allocatable :: src
        type (mallo_trn), dimension(:), allocatable :: trn
      end type mallo_rec
      type (mallo_rec), dimension(:), allocatable :: mallo
      end module mallo_module

      subroutine mallo_fixture_read
      use mallo_module
      integer :: imro = 0, i = 0, num_objs = 0, eof = 0
      open (107,file="fixture.mnu")
      do imro = 1, 2
        read (107,*,iostat=eof) mallo(imro)%name, mallo(imro)%src_obs, mallo(imro)%trn_obs
        num_objs = mallo(imro)%src_obs
        allocate (mallo(imro)%src(num_objs))
        num_objs = mallo(imro)%trn_obs
        allocate (mallo(imro)%trn(num_objs))
        do i = 1, mallo(imro)%src_obs
          read (107,*,iostat=eof) mallo(imro)%src(i)%num, mallo(imro)%src(i)%name, &
            mallo(imro)%src(i)%stor_init, mallo(imro)%src(i)%stor_max
        end do
        do i = 1, num_objs
          read (107,*,iostat=eof) mallo(imro)%trn(i)%num, mallo(imro)%trn(i)%kind
        end do
      end do
      close (107)
      end subroutine mallo_fixture_read
"""


class StaleCountReassignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(STALE_COUNT_REASSIGNMENT_FIXTURE)
        resolver = SchemaResolver(project)
        self.files, self.unresolved = build_multi_records(
            project, resolver, targets=("fixture.mnu",)
        )

    def test_reassigned_count_variable_collapses_both_blocks_under_the_wrong_key(
        self,
    ) -> None:
        # Documents the known bug: exactly one block survives (not two), and
        # it's keyed to src_obs -- the FIRST assignment to num_objs found in
        # the procedure -- even though the demand rows it actually contains
        # are counted by trn_obs. If this ever starts asserting 2 blocks,
        # _find_count_field has been made position-aware; update this test
        # (and the TARGET_FILES module comment) rather than reverting it.
        self.assertEqual(self.unresolved, [])
        blocks = self.files["fixture.mnu"]["blocks"]
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["count_field"], "src_obs")
        self.assertEqual(
            [f["fortran_name"] for f in blocks[0]["row"]["fields"]], ["num", "kind"]
        )


# Mirrors calibration.cal's real shape: a header record that is ITSELF
# variable-length (fixed fields + num_tot + an elem_cnt implied-do tail, peek-
# bound), followed by a conds-counted block whose rows are a genuinely
# different shape depending on the row's own leading value -- `if (tag ==
# "range") then` reads one layout, `else` reads a structurally different one.
TAGGED_ROW_FIXTURE = """
      module cond_module
      implicit none
      type upd_cond
        character(len=25) :: var = ""
        character(len=25) :: alt = ""
        real :: targ = 0.
        character(len=25) :: targc = ""
      end type upd_cond
      type upd_parm
        character(len=25) :: name = ""
        real :: val1 = 0.
        real :: val2 = 0.
        integer :: conds = 0
        integer :: num_tot = 0
        type (upd_cond), dimension(:), allocatable :: cond
        integer, dimension(:), allocatable :: elem_cnt
      end type upd_parm
      type (upd_parm), dimension(:), allocatable :: upd
      end module cond_module

      subroutine tagged_fixture_read
      use cond_module
      character(len=25) :: tag = ""
      integer :: i = 0, icond = 0, isp = 0, nspu = 0, eof = 0, nconds = 0
      open (107,file="fixture.cal")
      do i = 1, 3
        read (107,*,iostat=eof) upd(i)%name, upd(i)%conds, nspu
        if (nspu > 0) then
          backspace (107)
          read (107,*,iostat=eof) upd(i)%name, upd(i)%conds, upd(i)%num_tot, &
            (upd(i)%elem_cnt(isp), isp = 1, nspu)
        end if
        nconds = upd(i)%conds
        do icond = 1, nconds
          read (107,*,iostat=eof) tag
          backspace (107)
          if (tag == "range") then
            read (107,*,iostat=eof) tag, upd(i)%cond(icond)%var, upd(i)%val1, upd(i)%val2
          else
            read (107,*,iostat=eof) upd(i)%cond(icond)
          end if
        end do
      end do
      close (107)
      end subroutine tagged_fixture_read
"""


class MultiRecordTaggedRowTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(TAGGED_ROW_FIXTURE)
        resolver = SchemaResolver(project)
        self.files, self.unresolved = build_multi_records(
            project, resolver, targets=("fixture.cal",)
        )

    def test_resolves_with_no_unresolved(self) -> None:
        self.assertEqual(self.unresolved, [])
        self.assertIn("fixture.cal", self.files)

    def test_header_is_itself_variable_length(self) -> None:
        # The header record has its own repeat tail (num_tot + elem_cnt),
        # peek-bound the same way as chan-surf.lin -- carried honestly as
        # header.repeat rather than silently dropped.
        header = self.files["fixture.cal"]["header"]
        self.assertEqual(
            [f["fortran_name"] for f in header["fields"]], ["name", "conds", "num_tot"]
        )
        self.assertTrue(header["variable_arity"])
        self.assertEqual(header["repeat"]["count_field"], "num_tot")
        self.assertEqual(
            [f["fortran_name"] for f in header["repeat"]["fields"]], ["elem_cnt"]
        )

    def test_tagged_block_has_one_variant_per_branch(self) -> None:
        blocks = self.files["fixture.cal"]["blocks"]
        self.assertEqual(len(blocks), 1)
        block = blocks[0]
        self.assertEqual(block["count_field"], "conds")
        row = block["row"]
        self.assertEqual(row["tag_field"], "tag")
        variants = {v["tag"]: v for v in row["variants"]}
        self.assertEqual(set(variants), {"range", "other"})
        self.assertEqual(
            [f["fortran_name"] for f in variants["range"]["fields"]],
            ["tag", "var", "val1", "val2"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in variants["other"]["fields"]],
            ["var", "alt", "targ", "targc"],
        )

    def test_else_branch_read_does_not_also_appear_as_a_plain_block(self) -> None:
        # The else-branch read (`upd(i)%cond(icond)`) is itself a perfectly
        # valid ordinary single-read sub-block -- it must not ALSO show up as
        # a second, separate block alongside the tagged one.
        self.assertEqual(len(self.files["fixture.cal"]["blocks"]), 1)


# Mirrors water_allocation.wro: a water-allocation header, then a transfer
# block counted by `trn_obs`, where each transfer row is read twice -- first a
# narrow prefix to size `src_num`, then a backspaced full reread with a nested
# repeated source-object group and a trailing receiving-object suffix.
EMBEDDED_REPEAT_MULTI_RECORD_FIXTURE = """
      module water_allocation_module
      implicit none
      type transfer_source_objects
        character(len=10) :: typ = ""
        integer :: num = 0
        character(len=10) :: conv_typ = ""
        integer :: conv_num = 0
        character(len=25) :: dtbl_lim = ""
        real :: wdraw_lim = 0.
        real :: frac = 0.
        character(len=1) :: comp = ""
      end type transfer_source_objects
      type transfer_receiving_objects
        character(len=10) :: typ = ""
        integer :: num = 0
        integer :: frac = 0
      end type transfer_receiving_objects
      type water_transfer_objects
        character(len=10) :: trn_typ = ""
        character(len=40) :: trn_typ_name = ""
        real :: amount = 0.
        character(len=2) :: right = ""
        integer :: src_num = 0
        character(len=25) :: dtbl_src = ""
        type(transfer_source_objects), dimension(:), allocatable :: src
        type(transfer_receiving_objects) :: rcv
      end type water_transfer_objects
      type water_allocation
        character(len=25) :: name = ""
        character(len=25) :: rule_typ = ""
        integer :: trn_obs = 0
        type(water_transfer_objects), dimension(:), allocatable :: trn
      end type water_allocation
      type(water_allocation), dimension(:), allocatable :: wallo
      end module water_allocation_module

      subroutine embedded_repeat_multi_record_read
      use water_allocation_module
      implicit none
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0
      integer :: imax = 0
      integer :: iwro = 0
      integer :: itrn = 0
      integer :: num_objs = 0
      integer :: num_src = 0
      integer :: isrc = 0
      integer :: k = 0
      open (107,file="fixture.wro")
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) imax
      do iwro = 1, imax
        read (107,*,iostat=eof) header
        read (107,*,iostat=eof) wallo(iwro)%name, wallo(iwro)%rule_typ, wallo(iwro)%trn_obs
        read (107,*,iostat=eof) header
        num_objs = wallo(iwro)%trn_obs
        do itrn = 1, num_objs
          read (107,*,iostat=eof) k, wallo(iwro)%trn(itrn)%trn_typ, wallo(iwro)%trn(itrn)%trn_typ_name, &
            wallo(iwro)%trn(itrn)%amount, wallo(iwro)%trn(itrn)%right, wallo(iwro)%trn(itrn)%src_num
          num_src = wallo(iwro)%trn(itrn)%src_num
          backspace (107)
          read (107,*,iostat=eof) k, wallo(iwro)%trn(itrn)%trn_typ, wallo(iwro)%trn(itrn)%trn_typ_name, &
            wallo(iwro)%trn(itrn)%amount, wallo(iwro)%trn(itrn)%right, wallo(iwro)%trn(itrn)%src_num, &
            wallo(iwro)%trn(itrn)%dtbl_src, (wallo(iwro)%trn(itrn)%src(isrc), isrc = 1, num_src), &
            wallo(iwro)%trn(itrn)%rcv
        end do
      end do
      close (107)
      end subroutine embedded_repeat_multi_record_read
"""


class MultiRecordEmbeddedRepeatTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(EMBEDDED_REPEAT_MULTI_RECORD_FIXTURE)
        resolver = SchemaResolver(project)
        self.files, self.unresolved = build_multi_records(
            project, resolver, targets=("fixture.wro",)
        )

    def test_resolves_with_no_unresolved(self) -> None:
        self.assertEqual(self.unresolved, [])
        self.assertIn("fixture.wro", self.files)

    def test_embedded_repeat_row_keeps_prefix_repeat_and_suffix(self) -> None:
        schema = self.files["fixture.wro"]
        self.assertEqual(
            [f["fortran_name"] for f in schema["header"]["fields"]],
            ["name", "rule_typ", "trn_obs"],
        )
        self.assertEqual(len(schema["blocks"]), 1)
        block = schema["blocks"][0]
        self.assertEqual(block["count_field"], "trn_obs")
        row = block["row"]
        self.assertEqual(
            [f["fortran_name"] for f in row["fields"]],
            ["k", "trn_typ", "trn_typ_name", "amount", "right", "src_num", "dtbl_src"],
        )
        self.assertEqual(row["repeat"]["count_field"], "src_num")
        self.assertEqual(
            [f["fortran_name"] for f in row["repeat"]["fields"]],
            ["typ", "num", "conv_typ", "conv_num", "dtbl_lim", "wdraw_lim", "frac", "comp"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in row["suffix_fields"]],
            ["typ", "num", "frac"],
        )
        self.assertNotIn("variable_width", block)


# Mirrors pcp.cli's real shape: a row-count pre-pass (do while eof == 0), then
# two rereads of the same rows -- once into the station-name array (pcp_n),
# once into the measured-data filename field (pcp(i)%filename).
MULTI_SECTION_FIXTURE = """
      module input_file_module
      type input_cli
        character(len=25) :: pcp_cli = "pcp.cli"
      end type input_cli
      type (input_cli) :: in_cli
      end module input_file_module

      module climate_module
      type climate_measured_data
        character(len=50) :: filename = ""
      end type climate_measured_data
      type (climate_measured_data), dimension(:), allocatable :: pcp
      character(len=50), dimension(:), allocatable :: pcp_n
      end module climate_module

      subroutine cli_pmeas
      use input_file_module
      use climate_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0, imax = 0, i = 0
      open (107,file=in_cli%pcp_cli)
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do while (eof == 0)
        read (107,*,iostat=eof) titldum
        if (eof < 0) exit
        imax = imax + 1
      end do
      allocate (pcp(0:imax))
      allocate (pcp_n(imax))
      rewind (107)
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do i = 1, imax
        read (107,*,iostat=eof) pcp_n(i)
      end do
      rewind (107)
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do i = 1, imax
        read (107,*,iostat=eof) pcp(i)%filename
      end do
      close (107)
      end subroutine cli_pmeas
"""


class MultiSectionSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        project = scan_source(MULTI_SECTION_FIXTURE)
        resolver = SchemaResolver(project)
        self.files, self.unresolved = build_multi_sections(
            project, resolver, targets=("pcp.cli",)
        )

    def test_resolves_station_list_passes(self) -> None:
        self.assertEqual(self.unresolved, [])
        schema = self.files["pcp.cli"]
        self.assertEqual(schema["read_pattern"], "multi_section")
        self.assertEqual(
            [section["name"] for section in schema["sections"]],
            ["row_count_pass", "station_name_pass", "station_filename_pass"],
        )

    def test_station_name_and_filename_fields_are_separate_passes(self) -> None:
        sections = {section["name"]: section for section in self.files["pcp.cli"]["sections"]}
        self.assertEqual(sections["row_count_pass"]["fields"], [])
        self.assertEqual(
            [f["fortran_name"] for f in sections["station_name_pass"]["fields"]],
            ["pcp_n"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in sections["station_filename_pass"]["fields"]],
            ["filename"],
        )
        self.assertEqual(sections["station_name_pass"]["count_source"], "row_count_pass")
        self.assertEqual(sections["station_filename_pass"]["count_source"], "row_count_pass")



CONSTITUENTS_CS_FIXTURE = """
      module input_file_module
      type simulation_files
        character(len=25) :: cs_db = "constituents.cs"
      end type simulation_files
      type (simulation_files) :: in_sim
      end module input_file_module

      module constituent_mass_module
      type constituents
        integer :: num_pests = 0
        character (len=16), dimension(:), allocatable :: pests
        integer :: num_paths = 0
        character (len=16), dimension(:), allocatable :: paths
        integer :: num_metals = 0
        character (len=16), dimension(:), allocatable :: metals
        integer :: num_salts = 0
        character (len=16), dimension(:), allocatable :: salts
        integer :: num_cs = 0
        character (len=16), dimension(:), allocatable :: cs
      end type constituents
      type (constituents) :: cs_db
      end module constituent_mass_module

      subroutine constit_db_read
      use input_file_module
      use constituent_mass_module
      character (len=80) :: titldum = ""
      integer :: eof = 0, i = 0
      open (106,file=in_sim%cs_db)
      read (106,*,iostat=eof) titldum
      read (106,*,iostat=eof) cs_db%num_pests
      read (106,*,iostat=eof) (cs_db%pests(i), i = 1, cs_db%num_pests)
      read (106,*,iostat=eof) cs_db%num_paths
      read (106,*,iostat=eof) (cs_db%paths(i), i = 1, cs_db%num_paths)
      read (106,*,iostat=eof) cs_db%num_metals
      read (106,*,iostat=eof) (cs_db%metals(i), i = 1, cs_db%num_metals)
      read (106,*,iostat=eof) cs_db%num_salts
      read (106,*,iostat=eof) (cs_db%salts(i), i = 1, cs_db%num_salts)
      read (106,*,iostat=eof) cs_db%num_cs
      read (106,*,iostat=eof) (cs_db%cs(i), i = 1, cs_db%num_cs)
      close (106)
      end subroutine constit_db_read
"""


class ConstituentsCsMultiSectionSchemaTests(unittest.TestCase):
    def test_resolves_count_and_name_list_sections(self) -> None:
        project = scan_source(CONSTITUENTS_CS_FIXTURE)
        files, unresolved = build_multi_sections(
            project, SchemaResolver(project), targets=("constituents.cs",)
        )
        self.assertEqual(unresolved, [])
        sections = files["constituents.cs"]["sections"]
        self.assertEqual(
            [section["name"] for section in sections],
            [
                "pests_count",
                "pests_names",
                "paths_count",
                "paths_names",
                "metals_count",
                "metals_names",
                "salts_count",
                "salts_names",
                "cs_count",
                "cs_names",
            ],
        )
        by_name = {section["name"]: section for section in sections}
        self.assertEqual(by_name["pests_count"]["count_source"], "literal_1")
        self.assertEqual(by_name["pests_names"]["count_source"], "pests_count")
        self.assertEqual(
            [f["fortran_name"] for f in by_name["pests_count"]["fields"]],
            ["num_pests"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in by_name["pests_names"]["fields"]],
            ["pests"],
        )


CS_HRU_RUNTIME_ARITY_FIXTURE = """
      module constituent_mass_module
      type cs_soil_init_concentrations
        character(len=16) :: name = ""
        real, dimension(:), allocatable :: soil
        real, dimension(:), allocatable :: plt
      end type cs_soil_init_concentrations
      type (cs_soil_init_concentrations), dimension(:), allocatable :: cs_soil_ini
      type constituents
        integer :: num_cs = 0
      end type constituents
      type (constituents) :: cs_db
      end module constituent_mass_module

      subroutine cs_hru_read
      use constituent_mass_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0, imax = 0, ics = 0
      open (107,file="cs_hru.ini")
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do while (eof == 0)
        read (107,*,iostat=eof) titldum
        read (107,*,iostat=eof) titldum
        read (107,*,iostat=eof) titldum
        imax = imax + 1
      end do
      rewind (107)
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do ics = 1, imax
        read (107,*,iostat=eof) cs_soil_ini(ics)%name
        read (107,*,iostat=eof) cs_soil_ini(ics)%soil
        read (107,*,iostat=eof) cs_soil_ini(ics)%plt
      end do
      close (107)
      end subroutine cs_hru_read
"""



SALT_HRU_RUNTIME_ARITY_FIXTURE = """
      module constituent_mass_module
      type cs_soil_init_concentrations
        character(len=16) :: name = ""
        real, dimension(:), allocatable :: soil
        real, dimension(:), allocatable :: plt
      end type cs_soil_init_concentrations
      type (cs_soil_init_concentrations), dimension(:), allocatable :: salt_soil_ini
      type constituents
        integer :: num_salts = 0
      end type constituents
      type (constituents) :: cs_db
      end module constituent_mass_module

      subroutine salt_hru_read
      use constituent_mass_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0, imax = 0, isalti = 0
      open (107,file="salt_hru.ini")
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do while (eof == 0)
        read (107,*,iostat=eof) titldum
        read (107,*,iostat=eof) titldum
        read (107,*,iostat=eof) titldum
        imax = imax + 1
      end do
      rewind (107)
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) header
      do isalti = 1, imax
        read (107,*,iostat=eof) salt_soil_ini(isalti)%name
        read (107,*,iostat=eof) salt_soil_ini(isalti)%soil
        read (107,*,iostat=eof) salt_soil_ini(isalti)%plt
      end do
      close (107)
      end subroutine salt_hru_read
"""


PATH_HRU_RUNTIME_ARITY_FIXTURE = """
      module constituent_mass_module
      type cs_soil_init_concentrations
        character(len=16) :: name = ""
        real, dimension(:), allocatable :: soil
        real, dimension(:), allocatable :: plt
      end type cs_soil_init_concentrations
      type (cs_soil_init_concentrations), dimension(:), allocatable :: path_soil_ini
      type constituents
        integer :: num_paths = 0
      end type constituents
      type (constituents) :: cs_db
      end module constituent_mass_module

      subroutine path_hru_aqu_read
      use constituent_mass_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0, imax = 0, ipathi = 0
      open (107,file="path_hru.ini")
      read (107,*,iostat=eof) titldum
      do while (eof == 0)
        read (107,*,iostat=eof) header
        read (107,*,iostat=eof) titldum
        read (107,*,iostat=eof) titldum
        imax = imax + 1
      end do
      rewind (107)
      read (107,*,iostat=eof) titldum
      do ipathi = 1, imax
        read (107,*,iostat=eof) header
        read (107,*,iostat=eof) path_soil_ini(ipathi)%name
        read (107,*,iostat=eof) titldum, path_soil_ini(ipathi)%soil, path_soil_ini(ipathi)%plt
      end do
      close (107)
      end subroutine path_hru_aqu_read
"""

PEST_HRU_RUNTIME_ARITY_FIXTURE = """
      module constituent_mass_module
      type cs_soil_init_concentrations
        character(len=16) :: name = ""
        real, dimension(:), allocatable :: soil
        real, dimension(:), allocatable :: plt
      end type cs_soil_init_concentrations
      type (cs_soil_init_concentrations), dimension(:), allocatable :: pest_soil_ini
      type constituents
        integer :: num_pests = 0
      end type constituents
      type (constituents) :: cs_db
      end module constituent_mass_module

      subroutine pest_hru_aqu_read
      use constituent_mass_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0, imax = 0, ipest = 0, ipesti = 0
      open (107,file="pest_hru.ini")
      read (107,*,iostat=eof) titldum
      do while (eof == 0)
        read (107,*,iostat=eof) header
        read (107,*,iostat=eof) titldum
        read (107,*,iostat=eof) titldum
        imax = imax + 1
      end do
      rewind (107)
      read (107,*,iostat=eof) titldum
      do ipesti = 1, imax
        read (107,*,iostat=eof) pest_soil_ini(ipesti)%name
        do ipest = 1, cs_db%num_pests
          read (107,*,iostat=eof) titldum, pest_soil_ini(ipesti)%soil(ipest), &
                                      pest_soil_ini(ipesti)%plt(ipest)
        end do
      end do
      close (107)
      end subroutine pest_hru_aqu_read
"""

HMET_HRU_RUNTIME_ARITY_FIXTURE = """
      module constituent_mass_module
      type cs_soil_init_concentrations
        character(len=16) :: name = ""
        real, dimension(:), allocatable :: soil
        real, dimension(:), allocatable :: plt
      end type cs_soil_init_concentrations
      type (cs_soil_init_concentrations), dimension(:), allocatable :: hmet_soil_ini
      type constituents
        integer :: num_metals = 0
      end type constituents
      type (constituents) :: cs_db
      end module constituent_mass_module

      subroutine hmet_hru_aqu_read
      use constituent_mass_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0, imax = 0, ihmet = 0, ihmeti = 0
      open (107,file="hmet_hru.ini")
      read (107,*,iostat=eof) titldum
      do while (eof == 0)
        read (107,*,iostat=eof) header
        read (107,*,iostat=eof) titldum
        read (107,*,iostat=eof) titldum
        imax = imax + 1
      end do
      rewind (107)
      read (107,*,iostat=eof) titldum
      do ihmeti = 1, imax
        read (107,*,iostat=eof) header
        read (107,*,iostat=eof) hmet_soil_ini(ihmeti)%name
        do ihmet = 1, cs_db%num_metals
          read (107,*,iostat=eof) titldum, hmet_soil_ini(ihmeti)%soil(ihmet)
          read (107,*,iostat=eof) titldum, hmet_soil_ini(ihmeti)%plt(ihmet)
        end do
      end do
      close (107)
      end subroutine hmet_hru_aqu_read
"""


WATER_USE_RUNTIME_ARITY_FIXTURE = """
      module water_allocation_module
      type water_treatment_use_data
        character(len=25) :: name = ""
        real :: stor_mx
        real :: lag_days
        real :: loss_fr
        character(len=25) :: org_min = ""
        character(len=25) :: pests = ""
        character(len=25) :: paths = ""
        character(len=25) :: salts = ""
        character(len=25) :: constit = ""
        character(len=80) :: descrip = ""
      end type water_treatment_use_data
      type (water_treatment_use_data), dimension(:), allocatable :: wuse
      end module water_allocation_module

      module constituent_mass_module
      type constituents
        integer :: num_pests = 0
        integer :: num_paths = 0
      end type constituents
      type (constituents) :: cs_db
      type constituent_mass
        real, dimension(:), allocatable :: pest
        real, dimension(:), allocatable :: path
      end type constituent_mass
      type (constituent_mass), dimension(:), allocatable :: wuse_cs_efflu
      end module constituent_mass_module

      subroutine water_use_read
      use water_allocation_module
      use constituent_mass_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0, imax = 0, i = 0, iwuse = 0
      open (107,file="water_use.wal")
      read (107,*,iostat=eof) titldum
      read (107,*,iostat=eof) imax
      read (107,*,iostat=eof) header
      do iwuse = 1, imax
        read (107,*,iostat=eof) i, wuse(iwuse)%name, wuse(iwuse)%stor_mx, &
                                   wuse(iwuse)%lag_days, wuse(iwuse)%loss_fr, &
                                   wuse(iwuse)%org_min, wuse(iwuse)%pests, &
                                   wuse(iwuse)%paths, wuse(iwuse)%salts, &
                                   wuse(iwuse)%constit, wuse(iwuse)%descrip
        if (cs_db%num_pests > 0) then
          read (107,*,iostat=eof) header
          read (107,*,iostat=eof) wuse_cs_efflu(iwuse)%pest
        end if
        if (cs_db%num_paths > 0) then
          read (107,*,iostat=eof) header
          read (107,*,iostat=eof) wuse_cs_efflu(iwuse)%path
        end if
      end do
      close (107)
      end subroutine water_use_read
"""


CS_RECALL_RUNTIME_ARITY_FIXTURE = """
      module constituent_mass_module
      type constituents
        integer :: num_cs = 0
      end type constituents
      type (constituents) :: cs_db
      type recall_cs_year
        real, dimension(:), allocatable :: cs
      end type recall_cs_year
      type recall_cs_file
        character(len=16) :: name = ""
        integer :: typ = 0
        character(len=80) :: filename = ""
        integer :: pts_type = 0
        integer :: start_yr = 0
        integer :: end_yr = 0
        type(recall_cs_year), dimension(:,:), allocatable :: hd_cs
      end type recall_cs_file
      type (recall_cs_file), dimension(:), allocatable :: rec_cs
      end module constituent_mass_module

      module input_file_module
      type recall_inputs
        character(len=25) :: recall_rec = "recall.rec"
      end type recall_inputs
      type (recall_inputs) :: in_rec
      end module input_file_module

      module time_module
      type time_control
        integer :: yrc = 0
      end type time_control
      type (time_control) :: time
      end module time_module

      subroutine recall_read_cs
      use constituent_mass_module
      use input_file_module
      use time_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      character(len=16) :: ob_name = ""
      character(len=8) :: ob_typ = ""
      integer :: imax = 0
      integer :: iyr = 0
      integer :: jday = 0
      integer :: mo = 0
      integer :: day_mo = 0
      integer :: eof = 0
      logical :: i_exist
      integer :: nbyr = 0
      integer :: k = 0
      integer :: iyrs = 0
      integer :: iyr_prev = 0
      integer :: istep = 0
      integer :: ii = 0
      integer :: i = 0
      integer :: ics = 0
      integer :: jj = 0
      integer :: kk = 0

      inquire (file="cs_recall.rec", exist=i_exist)
      if (i_exist .or. in_rec%recall_rec /= "null") then
      do
        open (107,file="cs_recall.rec")
        read (107,*,iostat=eof) titldum
        if (eof < 0) exit
        read (107,*,iostat=eof) header
        if (eof < 0) exit
        do while (eof == 0)
          read (107,*,iostat=eof) i
          if (eof < 0) exit
          imax = Max(imax,i)
        end do
        rewind (107)
        read (107,*,iostat=eof) titldum
        if (eof < 0) exit
        read (107,*,iostat=eof) header
        if (eof < 0) exit
        do ii = 1, imax
          read (107,*,iostat=eof) i
          if (eof < 0) exit
          backspace (107)
          read (107,*,iostat = eof) k, rec_cs(i)%name, rec_cs(i)%typ, rec_cs(i)%filename
          if (eof < 0) exit
          if (rec_cs(i)%typ /= 4) then
            open (108,file = rec_cs(i)%filename)
            read (108,*,iostat=eof) titldum
            if (eof < 0) exit
            read (108,*,iostat=eof) nbyr
            if (eof < 0) exit
            read (108,*,iostat=eof) header
            if (eof < 0) exit
            if (rec_cs(i)%typ == 0) then
              iyrs = 1
              iyr_prev = jday
            else
              do
                read (108,*,iostat=eof) jday, mo, day_mo, iyr
                if (eof < 0) exit
                if (iyr == time%yrc) then
                  select case (rec_cs(i)%typ)
                    case (1)
                      istep = jday
                    case (2)
                      istep = mo
                    case (3)
                      istep = 1
                  end select
                  exit
                end if
              end do
              backspace (108)
              iyr_prev = iyr
              iyrs = 1
            end if
            do
              if (rec_cs(i)%typ /= 0) then
                read (108,*,iostat=eof) jday, mo, day_mo, iyr, ob_typ, ob_name, &
                     (rec_cs(i)%hd_cs(istep,iyrs)%cs(ics),ics=1,cs_db%num_cs)
              end if
              if (eof < 0) exit
            end do
            close (108)
          end if
        end do
        close (107)
        exit
      enddo
      endif
      end subroutine recall_read_cs
"""


SALT_RECALL_RUNTIME_ARITY_FIXTURE = """
      module constituent_mass_module
      type constituents
        integer :: num_salts = 0
      end type constituents
      type (constituents) :: cs_db
      type recall_salt_year
        real, dimension(:), allocatable :: salt
      end type recall_salt_year
      type recall_salt_file
        character(len=16) :: name = ""
        integer :: typ = 0
        character(len=80) :: filename = ""
        integer :: pts_type = 0
        integer :: start_yr = 0
        integer :: end_yr = 0
        type(recall_salt_year), dimension(:,:), allocatable :: hd_salt
      end type recall_salt_file
      type (recall_salt_file), dimension(:), allocatable :: rec_salt
      end module constituent_mass_module

      module time_module
      type time_control
        integer :: yrc = 0
      end type time_control
      type (time_control) :: time
      end module time_module

      subroutine recall_read_salt
      use constituent_mass_module
      use time_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      character(len=16) :: ob_name = ""
      character(len=8) :: ob_typ = ""
      integer :: imax = 0
      integer :: iyr = 0
      integer :: jday = 0
      integer :: mo = 0
      integer :: day_mo = 0
      integer :: eof = 0
      logical :: i_exist
      integer :: nbyr = 0
      integer :: k = 0
      integer :: iyrs = 0
      integer :: iyr_prev = 0
      integer :: istep = 0
      integer :: ii = 0
      integer :: i = 0
      integer :: isalt = 0
      inquire (file="salt_recall.rec", exist=i_exist)
      if (i_exist .or. "salt_recall.rec" /= "null") then
      do
        open (107,file="salt_recall.rec")
        read (107,*,iostat=eof) titldum
        if (eof < 0) exit
        read (107,*,iostat=eof) header
        if (eof < 0) exit
        do while (eof == 0)
          read (107,*,iostat=eof) i
          if (eof < 0) exit
          imax = Max(imax,i)
        end do
        rewind (107)
        read (107,*,iostat=eof) titldum
        if (eof < 0) exit
        read (107,*,iostat=eof) header
        if (eof < 0) exit
        do ii = 1, imax
          read (107,*,iostat=eof) i
          if (eof < 0) exit
          backspace (107)
          read (107,*,iostat = eof) k, rec_salt(i)%name, rec_salt(i)%typ, rec_salt(i)%filename
          if (eof < 0) exit
          if (rec_salt(i)%typ /= 4) then
            open (108,file = rec_salt(i)%filename)
            read (108,*,iostat=eof) titldum
            if (eof < 0) exit
            read (108,*,iostat=eof) nbyr
            if (eof < 0) exit
            read (108,*,iostat=eof) header
            if (eof < 0) exit
            if (rec_salt(i)%typ == 0) then
              iyrs = 1
              iyr_prev = jday
            else
              do
                read (108,*,iostat=eof) jday, mo, day_mo, iyr
                if (eof < 0) exit
                if (iyr == time%yrc) then
                  select case (rec_salt(i)%typ)
                    case (1)
                      istep = jday
                    case (2)
                      istep = mo
                    case (3)
                      istep = 1
                  end select
                  exit
                end if
              end do
              backspace (108)
              iyr_prev = iyr
              iyrs = 1
            end if
            do
              if (rec_salt(i)%typ /= 0) then
                read (108,*,iostat=eof) jday, mo, day_mo, iyr, ob_typ, ob_name, &
                     (rec_salt(i)%hd_salt(istep,iyrs)%salt(isalt),isalt=1,cs_db%num_salts)
              end if
              if (eof < 0) exit
            end do
            close (108)
          end if
        end do
        close (107)
        exit
      enddo
      endif
      end subroutine recall_read_salt
"""


WATER_CANAL_RUNTIME_ARITY_FIXTURE = """
      module maximum_data_module
      type data_max
        integer :: canal = 0
      end type data_max
      type (data_max) :: db_mx
      end module maximum_data_module

      module constituent_mass_module
      type constituent_mass
        real :: dummy = 0.
      end type constituent_mass
      type (constituent_mass), dimension(:), allocatable :: canal_cs_stor
      end module constituent_mass_module

      module water_allocation_module
      type aquifer_loss
        integer :: aqu_num = 0
        real :: frac = 0.
      end type aquifer_loss
      type water_canal_data
        character (len=25) :: name = ""
        character (len=25) :: w_sta = ""
        character (len=25) :: init = ""
        character (len=25) :: dtbl = ""
        real :: ddown_days = 0.
        real :: w = 0.
        real :: d = 0.
        real :: s = 0.
        real :: ss = 0.
        real :: sat_con = 0.
        real :: loss_fr = 0.
        real :: bed_thick = 0.
        integer :: div_id = 0
        integer :: day_beg = 0
        integer :: day_end = 0
        integer :: num_aqu = 0
        type (aquifer_loss), dimension(:), allocatable :: aqu_loss
      end type water_canal_data
      type (water_canal_data), dimension(:), allocatable :: canal
      end module water_allocation_module

      subroutine water_canal_read
      use water_allocation_module
      use maximum_data_module
      use constituent_mass_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0
      integer :: imax = 0
      logical :: i_exist
      integer :: i = 0
      integer :: ic = 0
      integer :: num_aqu = 0
      integer :: iaq = 0

      inquire (file='water_canal.wal', exist=i_exist)
      if (.not. i_exist .or. 'water_canal.wal' == "null") then
        allocate (canal(0:0))
      else
      do
        open (107,file='water_canal.wal')
        read (107,*,iostat=eof) titldum
        if (eof < 0) exit
        read (107,*,iostat=eof) imax
        read (107,*,iostat=eof) header
        db_mx%canal = imax
        if (eof < 0) exit
        allocate (canal(imax))
        allocate (canal_cs_stor(imax))
        do ic = 1, imax
          read (107,*,iostat=eof) i, canal(ic)%name, canal(ic)%w_sta, canal(ic)%init, canal(ic)%dtbl, &
              canal(ic)%ddown_days, canal(ic)%w, canal(ic)%d, canal(ic)%s, canal(ic)%ss, canal(ic)%sat_con, &
              canal(ic)%loss_fr, canal(ic)%bed_thick, canal(ic)%div_id, canal(ic)%day_beg, canal(ic)%day_end, &
              num_aqu
          if (eof < 0) exit
          backspace (107)
          allocate (canal(ic)%aqu_loss(num_aqu))
          read (107,*,iostat=eof) i, canal(ic)%name, canal(ic)%w_sta, canal(ic)%init, canal(ic)%dtbl, &
              canal(ic)%ddown_days, canal(ic)%w, canal(ic)%d, canal(ic)%s, canal(ic)%ss, canal(ic)%sat_con, &
              canal(ic)%loss_fr, canal(ic)%bed_thick, canal(ic)%div_id, canal(ic)%day_beg, canal(ic)%day_end, &
              canal(ic)%num_aqu, (canal(ic)%aqu_loss(iaq), iaq = 1, num_aqu)
        end do
      end do
      end if
      close(107)
      end subroutine water_canal_read
"""


WATER_PIPE_RUNTIME_ARITY_FIXTURE = """
      module maximum_data_module
      type data_max
        integer :: pipe = 0
      end type data_max
      type (data_max) :: db_mx
      end module maximum_data_module

      module water_allocation_module
      type aquifer_loss
        integer :: aqu_num = 0
        real :: frac = 0.
      end type aquifer_loss
      type water_transfer_data
        character (len=25) :: name = ""
        real :: stor_mx = 0.
        real :: ddown_days = 0.
        real :: loss_fr = 0.
        integer :: num_aqu = 0
        type (aquifer_loss), dimension(:), allocatable :: aqu_loss
      end type water_transfer_data
      type (water_transfer_data), dimension(:), allocatable :: pipe
      end module water_allocation_module

      subroutine water_pipe_read
      use water_allocation_module
      use maximum_data_module
      character (len=80) :: titldum = ""
      character (len=80) :: header = ""
      integer :: eof = 0
      integer :: imax = 0
      logical :: i_exist
      integer :: i = 0
      integer :: ipipe = 0
      integer :: num_aqu = 0
      integer :: iaq = 0
      inquire (file='water_pipe.wal', exist=i_exist)
      if (.not. i_exist .or. 'water_pipe.wal' == "null") then
        allocate (pipe(0:0))
      else
      do
        open (107,file='water_pipe.wal')
        read (107,*,iostat=eof) titldum
        if (eof < 0) exit
        read (107,*,iostat=eof) imax
        read (107,*,iostat=eof) header
        db_mx%pipe = imax
        if (eof < 0) exit
        allocate (pipe(imax))
        do ipipe = 1, imax
          read (107,*,iostat=eof) header
          if (eof < 0) exit
          read (107,*,iostat=eof) i, pipe(ipipe)%name, pipe(ipipe)%stor_mx, pipe(ipipe)%ddown_days, pipe(ipipe)%loss_fr, num_aqu
          if (eof < 0) exit
          allocate (pipe(ipipe)%aqu_loss(num_aqu))
          read (107,*,iostat=eof) i, pipe(ipipe)%name, pipe(ipipe)%stor_mx, pipe(ipipe)%ddown_days, pipe(ipipe)%loss_fr, pipe(ipipe)%num_aqu, (pipe(ipipe)%aqu_loss(iaq), iaq = 1, num_aqu)
        end do
      end do
      end if
      close(107)
      end subroutine water_pipe_read
"""


GWFLOW_RUNTIME_ARITY_FIXTURE = """
      module time_module
      type time_control
        integer :: nbyr = 0
      end type time_control
      type (time_control) :: time
      end module time_module

      module gwflow_module
      integer :: ncell = 0
      integer :: gw_nsolute = 0
      integer :: gw_npond = 0
      integer :: gw_nminl = 0
      integer :: grid_nrow = 0
      integer :: grid_ncol = 0
      character(len=15) :: grid_type = "unstructured"
      type solute_state
        real :: conc = 0.
      end type solute_state
      type object_solute_state
        type (solute_state), dimension(:), allocatable :: solute
      end type object_solute_state
      type (object_solute_state), dimension(:), allocatable :: gwsol_state
      type minl_state
        real, dimension(:), allocatable :: fract
      end type minl_state
      type (minl_state), dimension(:), allocatable :: gwsol_minl_state
      real, allocatable :: gw_tvh_vals(:,:)
      real, allocatable :: grid_val(:,:)
      type cell_pond_info
        integer :: id = 0
        real :: area = 0.
        integer :: chan = 0
        integer :: canal = 0
        integer :: unl = 0
        real :: bed_k = 0.
        integer :: wsta = 0
        real :: evap_co = 0.
        real, allocatable :: unl_conc(:)
      end type cell_pond_info
      type (cell_pond_info), dimension(:), allocatable :: gw_pond_info
      end module gwflow_module

      subroutine gwflow_read
      use gwflow_module
      use time_module
      integer :: in_gw = 0
      integer :: in_gw_minl = 0
      integer :: in_tvh = 0
      integer :: in_ponds = 0
      integer :: in_canal_cell = 0
      integer :: eof = 0
      integer :: i = 0
      integer :: j = 0
      integer :: m = 0
      integer :: s = 0
      integer :: canal_id = 0
      integer :: obj_tot = 0
      integer :: cell_num = 0
      real, allocatable :: con_row_buf(:)
      real :: length = 0.
      real :: stage = 0.
      integer :: cell_id = 0
      integer :: dum_id = 0
      integer :: yr_start = 0
      integer :: mo_start = 0
      integer :: dy_start = 0
      integer :: gw_ntvh = 0
      real :: single_value = 0.
      character(len=30) :: read_type = ""
      character(len=80) :: header = ""

      open(in_gw,file='cell_sol.gw')
      read(in_gw,*) header
      read(in_gw,*) header
      do i=1,ncell
        read(in_gw,*) cell_id,(gwsol_state(i)%solute(s)%conc,s=1,gw_nsolute)
      enddo
      close(in_gw)

      open(in_gw_minl,file='minerals.gw')
      read(in_gw_minl,*) header
      read(in_gw_minl,*) gw_nminl
      read(in_gw_minl,*) header
      if(grid_type == "structured") then
        do m=1,gw_nminl
          read(in_gw_minl,*) header
          read(in_gw_minl,*) read_type
          if(read_type == "single") then
            read(in_gw_minl,*) single_value
          elseif(read_type == "array") then
            do i=1,grid_nrow
              read(in_gw_minl,*) (grid_val(i,j),j=1,grid_ncol)
            enddo
          endif
        enddo
      elseif(grid_type == "unstructured") then
        do i=1,ncell
          read(in_gw_minl,*) (gwsol_minl_state(i)%fract(m),m=1,gw_nminl)
        enddo
      endif
      close(in_gw_minl)

      open(in_tvh,file='tvheads.gw')
      read(in_tvh,*) header
      read(in_tvh,*) header
      gw_ntvh = 0
      do
        read(in_tvh,*,iostat=eof) cell_id
        if(eof /= 0) exit
        gw_ntvh = gw_ntvh + 1
      enddo
      rewind(in_tvh)
      read(in_tvh,*) header
      read(in_tvh,*) header
      do i=1,gw_ntvh
        read(in_tvh,*) cell_id,(gw_tvh_vals(i,j),j=1,time%nbyr)
      enddo
      close(in_tvh)

      open(in_ponds,file='ponds.gw')
      read(in_ponds,*) header
      read(in_ponds,*) header
      gw_npond = 0
      do
        read(in_ponds,*,iostat=eof) dum_id
        if(eof /= 0) exit
        gw_npond = gw_npond + 1
      enddo
      rewind(in_ponds)
      read(in_ponds,*) header
      read(in_ponds,*) header
      do i=1,gw_npond
        read(in_ponds,*) gw_pond_info(i)%id, gw_pond_info(i)%area, gw_pond_info(i)%chan, &
                         gw_pond_info(i)%canal, gw_pond_info(i)%unl, gw_pond_info(i)%bed_k, &
                         gw_pond_info(i)%wsta, gw_pond_info(i)%evap_co, yr_start, mo_start, &
                         dy_start, (gw_pond_info(i)%unl_conc(j),j=1,gw_nsolute)
      enddo
      close(in_ponds)

      open(in_canal_cell,file='gwflow_canal.con')
      read(in_canal_cell,*) header
      do
        read(in_canal_cell,*,iostat=eof) canal_id, obj_tot
        if(eof /= 0) exit
      enddo
      rewind(in_canal_cell)
      read(in_canal_cell,*) header
      do
        read(in_canal_cell,*,iostat=eof) canal_id, obj_tot
        if(eof /= 0) exit
        backspace(in_canal_cell)
        allocate(con_row_buf(obj_tot*3))
        read(in_canal_cell,*) canal_id, obj_tot, (con_row_buf(j),j=1,obj_tot*3)
        do j=1,obj_tot
          cell_num = int(con_row_buf((j-1)*3 + 1))
          length = con_row_buf((j-1)*3 + 2)
          stage = con_row_buf((j-1)*3 + 3)
        enddo
        deallocate(con_row_buf)
      enddo
      close(in_canal_cell)
      end subroutine gwflow_read
"""
class RuntimeAritySchemaTests(unittest.TestCase):
    def test_water_use_wal_resolves_main_rows_and_optional_constituents(self) -> None:
        project = scan_source(WATER_USE_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("water_use.wal",)
        )
        self.assertEqual(unresolved, [])
        schema = files["water_use.wal"]
        self.assertEqual(
            [section["name"] for section in schema["sections"]],
            [
                "entry_count",
                "main_rows",
                "pest_concentrations",
                "pathogen_concentrations",
            ],
        )
        by_name = {section["name"]: section for section in schema["sections"]}
        self.assertEqual(by_name["main_rows"]["count_source"], "entry_count")
        self.assertEqual(
            [f["fortran_name"] for f in by_name["main_rows"]["fields"]],
            [
                "i",
                "name",
                "stor_mx",
                "lag_days",
                "loss_fr",
                "org_min",
                "pests",
                "paths",
                "salts",
                "constit",
                "descrip",
            ],
        )
        pest_field = by_name["pest_concentrations"]["fields"][0]
        self.assertEqual(pest_field["fortran_name"], "pest")
        self.assertEqual(pest_field["count_source"], "constituents.cs:pests_count")
        self.assertEqual(pest_field["count_expr"], "cs_db%num_pests")
        path_field = by_name["pathogen_concentrations"]["fields"][0]
        self.assertEqual(path_field["fortran_name"], "path")
        self.assertEqual(path_field["count_source"], "constituents.cs:paths_count")
        self.assertEqual(path_field["count_expr"], "cs_db%num_paths")


    def test_cs_recall_resolves_registry_and_nested_constituent_rows(self) -> None:
        project = scan_source(CS_RECALL_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("cs_recall.rec",)
        )
        self.assertEqual(unresolved, [])
        schema = files["cs_recall.rec"]
        self.assertEqual(
            [section["name"] for section in schema["sections"]],
            [
                "row_count_pass",
                "registry_rows",
                "nested_year_count",
                "nested_daily_rows",
                "nested_monthly_rows",
                "nested_annual_rows",
            ],
        )
        registry = schema["sections"][1]
        self.assertEqual(registry["count_source"], "row_count_pass")
        self.assertEqual(
            [field["fortran_name"] for field in registry["fields"]],
            ["k", "name", "typ", "filename"],
        )
        nested_years = schema["sections"][2]
        self.assertEqual(nested_years["count_source"], "single_record")
        self.assertEqual(nested_years["applies_when"], "typ != 4")
        self.assertEqual(nested_years["nested_file_field"], "filename")
        self.assertEqual(
            [field["fortran_name"] for field in nested_years["fields"]],
            ["nbyr"],
        )
        daily = schema["sections"][3]
        self.assertEqual(daily["count_source"], "until_eof_nested_file")
        self.assertEqual(daily["applies_when"], "typ == 1")
        self.assertEqual(daily["nested_file_field"], "filename")
        self.assertEqual(
            [field["fortran_name"] for field in daily["fields"]],
            ["jday", "mo", "day_mo", "iyr", "ob_typ", "ob_name", "cs"],
        )
        self.assertEqual(daily["fields"][-1]["count_source"], "constituents.cs:cs_count")
        self.assertEqual(daily["fields"][-1]["count_expr"], "cs_db%num_cs")
        monthly = schema["sections"][4]
        self.assertEqual(monthly["applies_when"], "typ == 2")
        self.assertEqual(monthly["nested_file_field"], "filename")
        annual = schema["sections"][5]
        self.assertEqual(annual["applies_when"], "typ == 3")
        self.assertEqual(annual["nested_file_field"], "filename")

    def test_salt_recall_resolves_registry_and_nested_salt_rows(self) -> None:
        project = scan_source(SALT_RECALL_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("salt_recall.rec",)
        )
        self.assertEqual(unresolved, [])
        schema = files["salt_recall.rec"]
        self.assertEqual(
            [section["name"] for section in schema["sections"]],
            [
                "row_count_pass",
                "registry_rows",
                "nested_year_count",
                "nested_daily_rows",
                "nested_monthly_rows",
                "nested_annual_rows",
            ],
        )
        registry = schema["sections"][1]
        self.assertEqual([field["fortran_name"] for field in registry["fields"]], ["k", "name", "typ", "filename"])
        daily = schema["sections"][3]
        self.assertEqual(daily["nested_file_field"], "filename")
        self.assertEqual(daily["applies_when"], "typ == 1")
        self.assertEqual([field["fortran_name"] for field in daily["fields"]], ["jday", "mo", "day_mo", "iyr", "ob_typ", "ob_name", "salt"])
        self.assertEqual(daily["fields"][-1]["count_source"], "constituents.cs:salts_count")
        self.assertEqual(daily["fields"][-1]["count_expr"], "cs_db%num_salts")
        self.assertEqual(schema["sections"][4]["applies_when"], "typ == 2")
        self.assertEqual(schema["sections"][5]["applies_when"], "typ == 3")

    def test_water_canal_resolves_row_tail_aquifer_losses(self) -> None:
        project = scan_source(WATER_CANAL_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("water_canal.wal",)
        )
        self.assertEqual(unresolved, [])
        schema = files["water_canal.wal"]
        self.assertEqual([section["name"] for section in schema["sections"]], ["entry_count", "canal_rows"])
        self.assertEqual(schema["sections"][0]["count_source"], "single_record")
        self.assertEqual([field["fortran_name"] for field in schema["sections"][0]["fields"]], ["imax"])
        rows = schema["sections"][1]
        self.assertEqual(rows["count_source"], "entry_count")
        self.assertEqual(rows["repeat_source"], "canal_rows:num_aqu")
        self.assertEqual(rows["repeat_expr"], "num_aqu")
        self.assertEqual(
            [field["fortran_name"] for field in rows["fields"]],
            ["i", "name", "w_sta", "init", "dtbl", "ddown_days", "w", "d", "s", "ss", "sat_con", "loss_fr", "bed_thick", "div_id", "day_beg", "day_end", "num_aqu"],
        )
        self.assertEqual([field["fortran_name"] for field in rows["repeat_fields"]], ["aqu_num", "frac"])

    def test_water_pipe_resolves_row_tail_aquifer_losses(self) -> None:
        project = scan_source(WATER_PIPE_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("water_pipe.wal",)
        )
        self.assertEqual(unresolved, [])
        schema = files["water_pipe.wal"]
        self.assertEqual([section["name"] for section in schema["sections"]], ["entry_count", "pipe_rows"])
        self.assertEqual([field["fortran_name"] for field in schema["sections"][0]["fields"]], ["imax"])
        rows = schema["sections"][1]
        self.assertEqual(rows["count_source"], "entry_count")
        self.assertEqual(rows["repeat_source"], "pipe_rows:num_aqu")
        self.assertEqual(rows["repeat_expr"], "num_aqu")
        self.assertEqual([field["fortran_name"] for field in rows["fields"]], ["i", "name", "stor_mx", "ddown_days", "loss_fr", "num_aqu"])
        self.assertEqual([field["fortran_name"] for field in rows["repeat_fields"]], ["aqu_num", "frac"])

    def test_gwflow_files_resolve_external_runtime_counts(self) -> None:
        project = scan_source(GWFLOW_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project,
            SchemaResolver(project),
            targets=("cell_sol.gw", "minerals.gw", "tvheads.gw", "ponds.gw", "gwflow_canal.con"),
        )
        self.assertEqual(unresolved, [])

        cell_sol = files["cell_sol.gw"]
        self.assertEqual([section["name"] for section in cell_sol["sections"]], ["solute_rows"])
        solute_row = cell_sol["sections"][0]
        self.assertEqual(solute_row["count_source"], "gwflow:ncell")
        self.assertEqual(
            [field["fortran_name"] for field in solute_row["fields"]],
            ["cell_id", "conc"],
        )
        self.assertEqual(solute_row["fields"][1]["count_source"], "gwflow:gw_nsolute")
        self.assertEqual(solute_row["fields"][1]["count_expr"], "gw_nsolute")

        minerals = files["minerals.gw"]
        self.assertEqual(
            [section["name"] for section in minerals["sections"]],
            [
                "mineral_count",
                "structured_mineral_modes",
                "structured_single_value_rows",
                "structured_array_rows",
                "unstructured_mineral_rows",
            ],
        )
        mineral_count = minerals["sections"][0]
        self.assertEqual(mineral_count["count_source"], "single_record")
        self.assertEqual(
            [field["fortran_name"] for field in mineral_count["fields"]],
            ["gw_nminl"],
        )
        structured_modes = minerals["sections"][1]
        self.assertEqual(structured_modes["count_source"], "gwflow:gw_nminl")
        self.assertEqual(structured_modes["applies_when"], 'grid_type == "structured"')
        self.assertEqual(
            [field["fortran_name"] for field in structured_modes["fields"]],
            ["read_type"],
        )
        structured_single = minerals["sections"][2]
        self.assertEqual(structured_single["count_source"], "structured_mineral_modes:single")
        self.assertEqual(
            structured_single["applies_when"],
            'grid_type == "structured" and read_type == "single"',
        )
        self.assertEqual(
            [field["fortran_name"] for field in structured_single["fields"]],
            ["single_value"],
        )
        structured_array = minerals["sections"][3]
        self.assertEqual(structured_array["count_source"], "gwflow:grid_nrow")
        self.assertEqual(
            structured_array["applies_when"],
            'grid_type == "structured" and read_type == "array"',
        )
        self.assertEqual(
            [field["fortran_name"] for field in structured_array["fields"]],
            ["grid_val"],
        )
        self.assertEqual(structured_array["fields"][0]["count_source"], "gwflow:grid_ncol")
        self.assertEqual(structured_array["fields"][0]["count_expr"], "grid_ncol")
        unstructured = minerals["sections"][4]
        self.assertEqual(unstructured["count_source"], "gwflow:ncell")
        self.assertEqual(unstructured["applies_when"], 'grid_type == "unstructured"')
        self.assertEqual(
            [field["fortran_name"] for field in unstructured["fields"]],
            ["fract"],
        )
        self.assertEqual(unstructured["fields"][0]["count_source"], "gwflow:gw_nminl")
        self.assertEqual(unstructured["fields"][0]["count_expr"], "gw_nminl")

        tvheads = files["tvheads.gw"]
        self.assertEqual(
            [section["name"] for section in tvheads["sections"]],
            ["row_count_pass", "head_rows"],
        )
        head_rows = tvheads["sections"][1]
        self.assertEqual(head_rows["count_source"], "row_count_pass")
        self.assertEqual(
            [field["fortran_name"] for field in head_rows["fields"]],
            ["cell_id", "gw_tvh_vals"],
        )
        self.assertEqual(head_rows["fields"][1]["count_source"], "time:nbyr")
        self.assertEqual(head_rows["fields"][1]["count_expr"], "time%nbyr")

        ponds = files["ponds.gw"]
        self.assertEqual(
            [section["name"] for section in ponds["sections"]],
            ["row_count_pass", "pond_rows"],
        )
        pond_row = ponds["sections"][1]
        self.assertEqual(
            [field["fortran_name"] for field in pond_row["fields"]],
            [
                "id",
                "area",
                "chan",
                "canal",
                "unl",
                "bed_k",
                "wsta",
                "evap_co",
                "yr_start",
                "mo_start",
                "dy_start",
                "unl_conc",
            ],
        )
        self.assertEqual(pond_row["fields"][-1]["count_source"], "gwflow:gw_nsolute")
        self.assertEqual(pond_row["fields"][-1]["count_expr"], "gw_nsolute")
        canal = files["gwflow_canal.con"]
        self.assertEqual(
            [section["name"] for section in canal["sections"]],
            ["canal_header_rows", "canal_connection_rows"],
        )
        canal_header = canal["sections"][0]
        self.assertEqual(canal_header["count_source"], "until_eof_group")
        self.assertEqual(
            [field["fortran_name"] for field in canal_header["fields"]],
            ["canal_id", "obj_tot"],
        )
        canal_rows = canal["sections"][1]
        self.assertEqual(canal_rows["count_source"], "canal_header_rows")
        self.assertEqual(canal_rows["repeat_source"], "canal_header_rows:obj_tot")
        self.assertEqual(canal_rows["repeat_expr"], "obj_tot")
        self.assertEqual(
            [field["fortran_name"] for field in canal_rows["repeat_fields"]],
            ["cell_num", "length", "stage"],
        )
    def test_cs_hru_resolves_external_constituent_arrays(self) -> None:
        project = scan_source(CS_HRU_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("cs_hru.ini",)
        )
        self.assertEqual(unresolved, [])
        schema = files["cs_hru.ini"]
        self.assertEqual(schema["read_pattern"], "runtime_arity")
        self.assertEqual(
            [section["name"] for section in schema["sections"]],
            [
                "row_count_pass",
                "entry_name",
                "soil_concentrations",
                "plant_concentrations",
            ],
        )
        by_name = {section["name"]: section for section in schema["sections"]}
        self.assertEqual(by_name["entry_name"]["count_source"], "row_count_pass")
        soil_field = by_name["soil_concentrations"]["fields"][0]
        self.assertEqual(soil_field["fortran_name"], "soil")
        self.assertTrue(soil_field["variable_arity"])
        self.assertEqual(soil_field["count_source"], "constituents.cs:cs_count")
        self.assertEqual(soil_field["count_expr"], "cs_db%num_cs + cs_db%num_cs")
        plant_field = by_name["plant_concentrations"]["fields"][0]
        self.assertEqual(plant_field["fortran_name"], "plt")
        self.assertEqual(plant_field["count_source"], "constituents.cs:cs_count")

    def test_salt_hru_resolves_external_salt_arrays(self) -> None:
        project = scan_source(SALT_HRU_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("salt_hru.ini",)
        )
        self.assertEqual(unresolved, [])
        schema = files["salt_hru.ini"]
        by_name = {section["name"]: section for section in schema["sections"]}
        soil_field = by_name["soil_concentrations"]["fields"][0]
        self.assertEqual(soil_field["fortran_name"], "soil")
        self.assertTrue(soil_field["variable_arity"])
        self.assertEqual(soil_field["count_source"], "constituents.cs:salts_count")
        self.assertEqual(soil_field["count_expr"], "cs_db%num_salts+5")
        plant_field = by_name["plant_concentrations"]["fields"][0]
        self.assertEqual(plant_field["fortran_name"], "plt")
        self.assertEqual(plant_field["count_source"], "constituents.cs:salts_count")

    def test_path_hru_resolves_combined_soil_plant_arrays(self) -> None:
        project = scan_source(PATH_HRU_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("path_hru.ini",)
        )
        self.assertEqual(unresolved, [])
        schema = files["path_hru.ini"]
        self.assertEqual(
            [section["name"] for section in schema["sections"]],
            ["row_count_pass", "entry_name", "soil_plant_concentrations"],
        )
        by_name = {section["name"]: section for section in schema["sections"]}
        combined_fields = by_name["soil_plant_concentrations"]["fields"]
        self.assertEqual([f["fortran_name"] for f in combined_fields], ["soil", "plt"])
        for field in combined_fields:
            self.assertTrue(field["variable_arity"])
            self.assertEqual(field["count_source"], "constituents.cs:paths_count")
            self.assertEqual(field["count_expr"], "cs_db%num_paths")

    def test_pest_hru_resolves_soil_plant_row_repeats(self) -> None:
        project = scan_source(PEST_HRU_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("pest_hru.ini",)
        )
        self.assertEqual(unresolved, [])
        schema = files["pest_hru.ini"]
        by_name = {section["name"]: section for section in schema["sections"]}
        rows = by_name["soil_plant_concentration_rows"]
        self.assertEqual(rows["repeat_source"], "constituents.cs:pests_count")
        self.assertEqual(rows["repeat_expr"], "cs_db%num_pests")
        self.assertEqual(
            [f["fortran_name"] for f in rows["fields"]],
            ["soil", "plt"],
        )

    def test_hmet_hru_resolves_soil_plant_row_repeats(self) -> None:
        project = scan_source(HMET_HRU_RUNTIME_ARITY_FIXTURE)
        files, unresolved = build_runtime_arity(
            project, SchemaResolver(project), targets=("hmet_hru.ini",)
        )
        self.assertEqual(unresolved, [])
        schema = files["hmet_hru.ini"]
        by_name = {section["name"]: section for section in schema["sections"]}
        rows = by_name["soil_plant_concentration_rows"]
        self.assertEqual(rows["repeat_source"], "constituents.cs:metals_count")
        self.assertEqual(rows["repeat_expr"], "cs_db%num_metals")
        self.assertEqual(
            [f["fortran_name"] for f in rows["fields"]],
            ["soil", "plt"],
        )
class DeterminismTests(unittest.TestCase):
    def test_byte_identical_without_timestamp(self) -> None:
        project = scan_source(FIXTURE)
        kwargs = dict(swatplus_version="1", source_ref="r", generator="g")
        a = dumps(build_schema(project, **kwargs))
        b = dumps(build_schema(scan_source(FIXTURE), **kwargs))
        self.assertEqual(a, b)

    def test_generated_utc_omitted_by_default(self) -> None:
        payload = build_schema(
            scan_source(FIXTURE), swatplus_version="1", source_ref="r", generator="g"
        )
        self.assertNotIn("generated_utc", payload)


class PinnedSourceSmokeTest(unittest.TestCase):
    """Runs only when the (gitignored) pinned source tree is present."""

    SOURCE = Path(__file__).resolve().parents[1] / "external" / "swatplus-62.0.0" / "src"

    def setUp(self) -> None:
        if not self.SOURCE.exists():
            self.skipTest("pinned SWAT+ source tree not present")
        project = FortranScanner(BuildConfig(source_dir=self.SOURCE)).scan()
        self.payload = build_schema(
            project, swatplus_version="62.0.0", source_ref="62.0.0", generator="test"
        )

    def test_snow_matches_known_layout(self) -> None:
        snow = self.payload["files"]["snow.sno"]
        self.assertEqual(len(snow["fields"]), 9)
        self.assertEqual(sum(f["numeric"] for f in snow["fields"]), 8)
        self.assertEqual(snow["fields"][0]["fortran_name"], "name")

    def test_plants_flattens_nested_and_extra_column(self) -> None:
        # 53 scalars + 3 nested (res_part_fracs) + pl_class = 57, 53 numeric.
        plants = self.payload["files"]["plants.plt"]
        self.assertEqual(len(plants["fields"]), 57)
        self.assertEqual(sum(f["numeric"] for f in plants["fields"]), 53)

    def test_print_matches_known_layout(self) -> None:
        prt = self.payload["files"]["print.prt"]
        self.assertEqual(prt["reader"], "basin_print_codes_read.f90")
        self.assertEqual(
            [f["fortran_name"] for f in prt["fields"]],
            ["nyskip", "day_start", "yrc_start", "day_end", "yrc_end", "int_day"],
        )

    def test_aqu_reg_def_matches_known_layout_despite_upstream_open_slot_bug(self) -> None:
        aqu_reg = self.payload["files"]["aqu_reg.def"]
        self.assertEqual(aqu_reg["reader"], "aqu_read_elements.f90")
        self.assertEqual(
            [f["fortran_name"] for f in aqu_reg["fields"]],
            ["k", "name", "area_ha", "nspu"],
        )
        self.assertTrue(aqu_reg["variable_arity"])
        self.assertEqual(
            [f["fortran_name"] for f in aqu_reg["repeat"]["fields"]],
            ["elem_cnt"],
        )

    def test_soil_plant_ini_matches_known_layout(self) -> None:
        spi = self.payload["files"]["soil_plant.ini"]
        self.assertEqual(spi["reader"], "soil_plant_init.f90")
        self.assertEqual(
            [f["fortran_name"] for f in spi["fields"]],
            ["name", "sw_frac", "nutc", "pestc", "pathc", "saltc", "hmetc", "csc"],
        )

    def test_water_balance_sft_matches_known_layout(self) -> None:
        wb = self.payload["files"]["water_balance.sft"]
        self.assertEqual(wb["reader"], "lcu_read_softcal.f90")
        self.assertEqual(
            [f["fortran_name"] for f in wb["fields"]],
            ["name", "srr", "lfr", "pcr", "etr", "tfr", "pet", "sed", "wyr", "bfr", "solp"],
        )

    def test_co2_yr_matches_known_layout(self) -> None:
        # co2_annual/co2 are declared local to co2_read.f90's own subroutine
        # body, not module-level -- the only pinned-source example of that.
        co2 = self.payload["files"]["co2_yr.dat"]
        self.assertEqual(co2["reader"], "co2_read.f90")
        self.assertEqual(
            [f["fortran_name"] for f in co2["fields"]],
            ["iyr", "co2"],
        )

    def test_manure_allo_matches_known_layout(self) -> None:
        # Confirmed 2026-08: trn(:)%withdr(isrc) -- the array a prior
        # caution flagged as an unrepresentable nested variable-length
        # column -- is never read anywhere in the pinned source; it's a
        # runtime-computed demand value (mallo_control.f90), not an input
        # column. The demand block's real, complete shape is these 5
        # columns, `withdr` correctly absent from all of them.
        mnu = self.payload["files"]["manure_allo.mnu"]
        self.assertEqual(mnu["reader"], "manure_allocation_read.f90")
        blocks_by_line = {b["reader_line"]: b for b in mnu["blocks"]}
        header = blocks_by_line[51]
        self.assertEqual(
            [f["fortran_name"] for f in header["fields"]],
            ["name", "rule_typ", "src_obs", "trn_obs"],
        )
        demand = blocks_by_line[94]
        self.assertEqual(
            [f["fortran_name"] for f in demand["fields"]],
            ["k", "ob_typ", "ob_num", "dtbl", "right"],
        )

    def test_all_curated_targets_resolve(self) -> None:
        self.assertEqual(self.payload["unresolved"], [])

    def test_all_targets_accounted_for(self) -> None:
        resolved = set(self.payload["files"])
        unresolved = {e["file"] for e in self.payload["unresolved"]}
        self.assertEqual(resolved | unresolved, set(TARGET_FILES))

    def test_widened_coverage_resolves_cleanly(self) -> None:
        # The 2026-07 widening added 63 files beyond the original 28, and the
        # final curated 62.0 set now resolves cleanly end-to-end.
        self.assertEqual(self.payload["unresolved"], [])
        self.assertEqual(len(self.payload["files"]), len(TARGET_FILES))


    def test_files_excluded_for_documented_reasons_stay_out(self) -> None:
        # These resolve if TARGET_FILES is dropped entirely (see
        # DummyArgAndUnderscoreExtensionTests / ReusedUnitAttributionTests /
        # RecordLayoutTests / PositionalExtractionTests / the module
        # docstring), but are deliberately not curated in: an
        # externally-governed repeat count, a runtime-sized (not
        # compile-time-fixed) array column, a genuinely nested/two-shape
        # record, or a data-dependent repeat group / keyed record nested
        # inside a hand-parsed file.
        excluded = {
            "cellcon.gw", "sw_group.gw",  # positional prefix + a nested, computed-index repeat
            # outputs.gw: now resolved as a tagged column -- see TARGET_FILES.
            # calibration.cal: now fully resolved -- see multi_record, not TARGET_FILES/files.
            "lum.dtl", "res_rel.dtl",  # decision tables: nested, not flat
            "pest_metabolite.pes",  # two-shape: parent header + N daughter records
            # gwflow_read.f90 family, investigated 2026-08 -- see the
            # TARGET_FILES module comment and
            # test_gwflow_read_family_candidates_stay_correctly_unresolved:
            "hru_pump.gw", "transit.gw", "soil_lyr_depths.sol",  # ambiguous single-column loop read
            "carbon_layers.prt",  # scalar config value, no row data -- same category as codes.gw
            "looping.con",  # write-only diagnostic dump, never read -- not an input file
            "chan_depth.gw", "pond_div.gw",  # opened in one procedure, rows read in another
        }
        self.assertTrue(excluded.isdisjoint(TARGET_FILES))

    def test_files_cleared_after_review_are_included(self) -> None:
        # weather-sta.cli, rout_unit.rtu, outside_rcv.wal, and carbon.bsn were
        # flagged for review by an overlay-agreement heuristic that turned
        # out to be wrong for these four; verified correct against source
        # and added.
        for f in ("weather-sta.cli", "rout_unit.rtu", "outside_rcv.wal", "carbon.bsn"):
            self.assertIn(f, self.payload["files"])

    def test_record_layout_files_resolve_against_pinned_source(self) -> None:
        # Self-describing repeat counts: *.con (indirect, via "nout =
        # ob(i)%src_tot") and the *.def/*.sft/*.lin family (direct, a bare
        # "nspu" token).
        con = self.payload["files"]["hru.con"]
        self.assertTrue(con["variable_arity"])
        self.assertEqual(con["repeat"]["count_field"], "src_tot")
        self.assertEqual(
            [f["fortran_name"] for f in con["repeat"]["fields"]],
            ["obtyp_out", "obtypno_out", "htyp_out", "frac_out"],
        )
        defn = self.payload["files"]["ch_catunit.def"]
        self.assertTrue(defn["variable_arity"])
        self.assertEqual(defn["repeat"]["count_field"], "nspu")
        self.assertEqual(defn["repeat"]["count_expr"], "nspu")
        # chan-surf.lin: count read by a peek into a throwaway local (nspu),
        # bound to the record's own last fixed field obj_tot.
        lin = self.payload["files"]["chan-surf.lin"]
        self.assertTrue(lin["variable_arity"])
        self.assertEqual(
            [f["fortran_name"] for f in lin["fields"]], ["numb", "name", "obj_tot"]
        )
        self.assertEqual(lin["repeat"]["count_field"], "obj_tot")
        self.assertEqual(lin["repeat"]["count_expr"], "nspu")
        self.assertEqual(
            [f["fortran_name"] for f in lin["repeat"]["fields"]], ["obtyp", "obtypno"]
        )
        for f in ("aqu_catunit.def", "aqu_cha.lin", "aquifer.con", "ch_reg.def",
                  "ch_sed_budget.sft", "chandeg.con", "channel.con", "delratio.con",
                  "exco.con", "gwflow.con", "hru-lte.con", "ls_reg.def", "ls_unit.def",
                  "outlet.con", "plant_gro.sft", "plant_parms.sft", "rec_catunit.def",
                  "rec_reg.def", "recall.con", "res_catunit.def", "res_reg.def",
                  "reservoir.con", "rout_unit.con", "rout_unit.def"):
            self.assertTrue(self.payload["files"][f]["variable_arity"], f)

    def test_positional_extraction_files_resolve_against_pinned_source(self) -> None:
        # cells.gw resolves fully -- all 23 columns, including the
        # assignment-derived "name" column -- while chancell.gw loses its
        # last two (dep_zone, obs) to the separate single-line-if gap.
        cells = self.payload["files"]["cells.gw"]
        self.assertEqual(cells["read_pattern"], "positional")
        self.assertEqual(len(cells["fields"]), 23)
        self.assertEqual(cells["fields"][1]["fortran_name"], "cell_name")
        for f in ("zones.gw", "chancell.gw"):
            self.assertEqual(self.payload["files"][f]["read_pattern"], "positional")

    def test_tagged_positional_column_resolves_against_pinned_source(self) -> None:
        # outputs.gw: column 2's meaning depends on column 1's value (a
        # select-case dispatch in gwflow_read.f90), resolved as a tagged
        # column rather than declined.
        entry = self.payload["files"]["outputs.gw"]
        self.assertEqual(entry["read_pattern"], "positional")
        self.assertEqual(entry["fields"], [])
        self.assertEqual(entry["tag_field"], "split_fields(1)")
        variants = {v["tag"]: v for v in entry["variants"]}
        self.assertEqual(
            set(variants), {"head_output_time", "observation_cell", "detail_debug_cell"}
        )
        self.assertEqual(
            [f["fortran_name"] for f in variants["head_output_time"]["fields"]],
            ["combined_yrday"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in variants["observation_cell"]["fields"]],
            ["gw_obs_cells_init"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in variants["detail_debug_cell"]["fields"]],
            ["gw_cell_obs_ss"],
        )

    def test_intrinsic_record_files_resolve_against_pinned_source(self) -> None:
        # Unlocked by the plain-intrinsic fallback; these name ordinary typed
        # columns and never touch a derived type.
        self.assertEqual(
            [f["fortran_name"] for f in self.payload["files"]["rescell.gw"]["fields"]],
            ["res_cell", "res_id", "res_stage"],
        )
        for f in ("floodplain.gw", "hrucell.gw", "lsucell.gw", "phreato.gw",
                  "phreato_cell.gw", "pond_cell.gw", "pumpex.gw", "solute.gw",
                  "gwflow.wetland"):
            self.assertIn(f, self.payload["files"])

    def test_recall_db_rec_included_with_disambiguated_field_names(self) -> None:
        # Held out of the initial review pass for a real bug (6 sibling
        # components of the same type collided to identical field names);
        # fixed by prefixing colliding chains with their own component name.
        names = [f["fortran_name"] for f in self.payload["files"]["recall_db.rec"]["fields"]]
        self.assertEqual(len(names), 20)
        self.assertEqual(len(names), len(set(names)))
        self.assertIn("org_min.name", names)
        self.assertIn("pest.units", names)
        self.assertIn("constit.tstep", names)

    def test_decision_tables_resolve_against_pinned_source(self) -> None:
        tables = self.payload["decision_tables"]
        self.assertEqual(self.payload["decision_tables_unresolved"], [])
        self.assertEqual(set(tables), {"flo_con.dtl", "lum.dtl", "res_rel.dtl", "scen_lu.dtl"})

        lum = tables["lum.dtl"]
        self.assertEqual(lum["reader"], "dtbl_lum_read.f90")
        self.assertEqual(
            [f["fortran_name"] for f in lum["header"]["fields"]],
            ["name", "conds", "alts", "acts"],
        )
        self.assertEqual(len(lum["condition_block"]["row"]["fields"]), 6)
        self.assertEqual(len(lum["action_block"]["row"]["fields"]), 8)
        self.assertEqual(lum["condition_block"]["row"]["repeat"]["count_field"], "alts")
        self.assertEqual(lum["action_block"]["row"]["repeat"]["count_field"], "alts")

        # COND_VAR (conditions.f90's shared runtime dispatcher) is the same
        # 55-value vocabulary for every table -- not to be confused with
        # cal_conditions.f90's unrelated, differently-scoped 8-value dispatch
        # that happens to share the same %cond(..)%var subject shape.
        for name in ("flo_con.dtl", "lum.dtl", "res_rel.dtl", "scen_lu.dtl"):
            self.assertEqual(len(tables[name]["vocabulary"]["condition_var"]), 55)

        self.assertEqual(
            tables["lum.dtl"]["vocabulary"]["action_typ"],
            [
                "plant", "harvest", "harvest_kill", "till", "irr_demand", "irr_wallo",
                "irrigate", "fertilize", "fert_future", "manure_demand", "pest_apply",
                "graze", "puddle", "burn", "lu_change", "snow_change",
            ],
        )
        self.assertEqual(tables["scen_lu.dtl"]["vocabulary"]["action_typ"], ["lu_change", "snow_change"])
        self.assertEqual(tables["flo_con.dtl"]["vocabulary"]["action_typ"], [])

        # dtbl_res_read.f90's ACT_TYP has only "release", but nests a second,
        # separate select-case on the action's own `option` (weir vs. meas)
        # -- captured, not discarded, as an "other" vocabulary entry.
        res = tables["res_rel.dtl"]
        self.assertEqual(res["vocabulary"]["action_typ"], ["release"])
        self.assertEqual(len(res["vocabulary"]["other"]), 1)
        self.assertEqual(res["vocabulary"]["other"][0]["cases"], ["weir", "meas"])

    def test_multi_record_files_resolve_against_pinned_source(self) -> None:
        mr = self.payload["multi_record"]
        self.assertEqual(self.payload["multi_record_unresolved"], [])
        self.assertEqual(
            set(mr),
            {"plant.ini", "soils.sol", "water_allocation.wro", "weather-wgn.cli", "management.sch", "calibration.cal"},
        )

        # management.sch: schedule header + an operations block read in a
        # called helper (read_mgtops) + a keyed, variable-width auto block.
        sch = mr["management.sch"]
        self.assertEqual(sch["reader"], "mgt_read_mgtops.f90")
        self.assertEqual(
            [f["fortran_name"] for f in sch["header"]["fields"]],
            ["name", "num_ops", "num_autos"],
        )
        by_count = {b.get("count_field"): b for b in sch["blocks"]}
        self.assertEqual(
            [f["fortran_name"] for f in by_count["num_ops"]["row"]["fields"]],
            ["op", "mon", "day", "husc", "op_char", "op_plant", "op3"],
        )
        self.assertTrue(by_count["num_autos"]["variable_width"])
        self.assertEqual(
            [f["fortran_name"] for f in by_count["num_autos"]["row"]["fields"]],
            ["auto_name"],
        )

        # water_allocation.wro: a water-allocation header, then a transfer
        # block whose rows contain a nested repeated source-object group plus a
        # trailing receiving-object suffix.
        wallo = mr["water_allocation.wro"]
        self.assertEqual(wallo["reader"], "water_allocation_read.f90")
        self.assertEqual(
            [f["fortran_name"] for f in wallo["header"]["fields"]],
            ["name", "rule_typ", "trn_obs"],
        )
        self.assertEqual(len(wallo["blocks"]), 1)
        block = wallo["blocks"][0]
        self.assertEqual(block["count_field"], "trn_obs")
        self.assertEqual(
            [f["fortran_name"] for f in block["row"]["fields"]],
            ["k", "trn_typ", "trn_typ_name", "amount", "right", "src_num", "dtbl_src"],
        )
        self.assertEqual(block["row"]["repeat"]["count_field"], "src_num")
        self.assertEqual(
            [f["fortran_name"] for f in block["row"]["repeat"]["fields"]],
            ["typ", "num", "conv_typ", "conv_num", "dtbl_lim", "wdraw_lim", "frac", "comp"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in block["row"]["suffix_fields"]],
            ["typ", "num", "frac"],
        )

        # weather-wgn.cli: a station header spanning two roots (wgn_n + wgn),
        # then a literal-count block of 12 monthly-stat rows, 14 columns each
        # (each a single element of a dimension(12) component -- 14, not 168).
        wgn = mr["weather-wgn.cli"]
        self.assertEqual(wgn["reader"], "cli_wgnread.f90")
        self.assertEqual(
            [f["fortran_name"] for f in wgn["header"]["fields"]],
            ["wgn_n", "lat", "long", "elev", "rain_yrs"],
        )
        self.assertEqual(len(wgn["blocks"]), 1)
        self.assertNotIn("count_field", wgn["blocks"][0])
        self.assertEqual(wgn["blocks"][0]["count"], 12)
        self.assertEqual(len(wgn["blocks"][0]["row"]["fields"]), 14)

        # soils.sol: a soil header, then `nly` layer records (14 columns each).
        soils = mr["soils.sol"]
        self.assertEqual(soils["reader"], "soil_db_read.f90")
        self.assertEqual(
            [f["fortran_name"] for f in soils["header"]["fields"]],
            ["snam", "nly", "hydgrp", "zmx", "anion_excl", "crk", "texture"],
        )
        self.assertEqual(len(soils["blocks"]), 1)
        self.assertEqual(soils["blocks"][0]["count_field"], "nly")
        self.assertEqual(
            [f["fortran_name"] for f in soils["blocks"][0]["row"]["fields"]],
            ["z", "bd", "awc", "k", "cbn", "clay", "silt", "sand", "rock", "alb",
             "usle_k", "ec", "cal", "ph"],
        )

        # plant.ini: a community header, then `plants_com` plant records.
        plant = mr["plant.ini"]
        self.assertEqual(
            [f["fortran_name"] for f in plant["header"]["fields"]],
            ["name", "plants_com", "rot_yr_ini"],
        )
        self.assertEqual(plant["blocks"][0]["count_field"], "plants_com")
        self.assertEqual(len(plant["blocks"][0]["row"]["fields"]), 8)

        # calibration.cal: the header is itself variable-length (peek-bound
        # num_tot + elem_cnt tail), then a conds-counted block whose rows are
        # a genuinely different shape depending on the row's own tag value.
        cal = mr["calibration.cal"]
        self.assertEqual(cal["reader"], "cal_parmchg_read.f90")
        self.assertEqual(
            [f["fortran_name"] for f in cal["header"]["fields"]],
            ["name", "chg_typ", "val", "conds", "lyr1", "lyr2", "year1", "year2",
             "day1", "day2", "num_tot"],
        )
        self.assertTrue(cal["header"]["variable_arity"])
        self.assertEqual(cal["header"]["repeat"]["count_field"], "num_tot")
        self.assertEqual(
            [f["fortran_name"] for f in cal["header"]["repeat"]["fields"]], ["elem_cnt"]
        )
        self.assertEqual(len(cal["blocks"]), 1)
        block = cal["blocks"][0]
        self.assertEqual(block["count_field"], "conds")
        self.assertEqual(block["row"]["tag_field"], "range")
        variants = {v["tag"]: v for v in block["row"]["variants"]}
        self.assertEqual(set(variants), {"range", "other"})
        self.assertEqual(
            [f["fortran_name"] for f in variants["range"]["fields"]],
            ["range", "var", "val1", "val2"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in variants["other"]["fields"]],
            ["var", "alt", "targ", "targc"],
        )

    def test_runtime_arity_files_resolve_against_pinned_source(self) -> None:
        ra = self.payload["runtime_arity"]
        self.assertEqual(self.payload["runtime_arity_unresolved"], [])
        self.assertEqual(
            set(ra),
            {
                "atmodep.cli",
                "cs_recall.rec",
                "salt_recall.rec",
                "water_canal.wal",
                "water_pipe.wal",
                "cs_aqu.ini",
                "cs_atmo.cli",
                "cs_channel.ini",
                "cs_hru.ini",
                "dr_hmet.del",
                "dr_path.del",
                "dr_pest.del",
                "dr_salt.del",
                "exco_hmet.exc",
                "exco_path.exc",
                "exco_pest.exc",
                "exco_salt.exc",
                "cell_sol.gw",
                "hmet_hru.ini",
                "minerals.gw",
                "out_src.wal",
                "path_hru.ini",
                "path_water.ini",
                "pest_hru.ini",
                "pest_water.ini",
                "ponds.gw",
                "gwflow_canal.con",
                "salt_atmo.cli",
                "salt_channel.ini",
                "salt_hru.ini",
                "tvheads.gw",
                "water_treat.wal",
                "water_use.wal",
            },
        )
        cs_hru = ra["cs_hru.ini"]
        self.assertEqual(cs_hru["reader"], "cs_hru_read.f90")
        by_name = {section["name"]: section for section in cs_hru["sections"]}
        self.assertEqual(
            [section["name"] for section in cs_hru["sections"]],
            [
                "row_count_pass",
                "entry_name",
                "soil_concentrations",
                "plant_concentrations",
            ],
        )
        soil_field = by_name["soil_concentrations"]["fields"][0]
        self.assertEqual(soil_field["fortran_name"], "soil")
        self.assertEqual(soil_field["count_source"], "constituents.cs:cs_count")
        self.assertEqual(soil_field["count_expr"], "cs_db%num_cs + cs_db%num_cs")
        plant_field = by_name["plant_concentrations"]["fields"][0]
        self.assertEqual(plant_field["fortran_name"], "plt")
        self.assertEqual(plant_field["count_source"], "constituents.cs:cs_count")

        salt_hru = ra["salt_hru.ini"]
        self.assertEqual(salt_hru["reader"], "salt_hru_read.f90")
        salt_by_name = {section["name"]: section for section in salt_hru["sections"]}
        salt_soil_field = salt_by_name["soil_concentrations"]["fields"][0]
        self.assertEqual(salt_soil_field["fortran_name"], "soil")
        self.assertEqual(salt_soil_field["count_source"], "constituents.cs:salts_count")
        self.assertEqual(salt_soil_field["count_expr"], "cs_db%num_salts+5")

        path_hru = ra["path_hru.ini"]
        self.assertEqual(path_hru["reader"], "path_hru_aqu_read.f90")
        path_by_name = {section["name"]: section for section in path_hru["sections"]}
        path_fields = path_by_name["soil_plant_concentrations"]["fields"]
        self.assertEqual([f["fortran_name"] for f in path_fields], ["soil", "plt"])
        for field in path_fields:
            self.assertEqual(field["count_source"], "constituents.cs:paths_count")
            self.assertEqual(field["count_expr"], "cs_db%num_paths")

        pest_hru = ra["pest_hru.ini"]
        self.assertEqual(pest_hru["reader"], "pest_hru_aqu_read.f90")
        pest_by_name = {section["name"]: section for section in pest_hru["sections"]}
        pest_rows = pest_by_name["soil_plant_concentration_rows"]
        self.assertEqual(pest_rows["repeat_source"], "constituents.cs:pests_count")
        self.assertEqual(pest_rows["repeat_expr"], "cs_db%num_pests")
        self.assertEqual(
            [f["fortran_name"] for f in pest_rows["fields"]],
            ["soil", "plt"],
        )

        hmet_hru = ra["hmet_hru.ini"]
        self.assertEqual(hmet_hru["reader"], "hmet_hru_aqu_read.f90")
        hmet_by_name = {section["name"]: section for section in hmet_hru["sections"]}
        hmet_rows = hmet_by_name["soil_plant_concentration_rows"]
        self.assertEqual(hmet_rows["repeat_source"], "constituents.cs:metals_count")
        self.assertEqual(hmet_rows["repeat_expr"], "cs_db%num_metals")
        self.assertEqual(
            [f["fortran_name"] for f in hmet_rows["fields"]],
            ["soil", "plt"],
        )
        atmo_expectations = {
            "atmodep.cli": (
                "cli_read_atmodep.f90",
                ["control_header", "aa_station_name", "aa_nh4_rf", "aa_no3_rf", "aa_nh4_dry", "aa_no3_dry"],
            ),
            "cs_atmo.cli": (
                "cli_read_atmodep_cs.f90",
                ["aa_station_name", "aa_rf_rows", "aa_dry_rows", "mo_station_name", "mo_rfmo_rows", "mo_drymo_rows"],
            ),
            "salt_atmo.cli": (
                "cli_read_atmodep_salt.f90",
                ["aa_station_name", "aa_rf_rows", "aa_dry_rows", "mo_station_name", "mo_rfmo_rows", "mo_drymo_rows"],
            ),
        }
        for filename, (reader, prefixes) in atmo_expectations.items():
            schema = ra[filename]
            self.assertEqual(schema["reader"], reader)
            names = [section["name"] for section in schema["sections"]]
            self.assertEqual(names[: len(prefixes)], prefixes)
        atmo = ra["atmodep.cli"]
        control = atmo["sections"][0]
        self.assertEqual(control["name"], "control_header")
        self.assertEqual([f["fortran_name"] for f in control["fields"]], ["num_sta", "timestep", "mo_init", "yr_init", "num"])
        mo_rf = next(section for section in atmo["sections"] if section["name"] == "mo_nh4_rfmo")
        self.assertEqual(mo_rf["fields"][0]["count_source"], "control_header:num")
        self.assertEqual(mo_rf["fields"][0]["count_expr"], "atmodep_cont%num")
        cs_atmo = ra["cs_atmo.cli"]
        cs_mo = next(section for section in cs_atmo["sections"] if section["name"] == "mo_rfmo_rows")
        self.assertEqual(cs_mo["repeat_source"], "constituents.cs:cs_count")
        self.assertEqual(cs_mo["fields"][0]["count_source"], "atmodep.cli:control_header:num")
        salt_atmo = ra["salt_atmo.cli"]
        salt_mo = next(section for section in salt_atmo["sections"] if section["name"] == "mo_rfmo_rows")
        self.assertEqual(salt_mo["repeat_source"], "constituents.cs:salts_count")
        self.assertEqual(salt_mo["fields"][0]["count_source"], "atmodep.cli:control_header:num")

        water_pipe = {section["name"]: section for section in ra["water_pipe.wal"]["sections"]}
        self.assertEqual(ra["water_pipe.wal"]["reader"], "water_pipe_read.f90")
        self.assertEqual(water_pipe["entry_count"]["fields"][0]["fortran_name"], "imax")
        self.assertEqual(water_pipe["pipe_rows"]["count_source"], "entry_count")
        self.assertEqual(water_pipe["pipe_rows"]["repeat_source"], "pipe_rows:num_aqu")
        self.assertEqual([f["fortran_name"] for f in water_pipe["pipe_rows"]["repeat_fields"]], ["aqu_num", "frac"])

        water_canal = {section["name"]: section for section in ra["water_canal.wal"]["sections"]}
        self.assertEqual(ra["water_canal.wal"]["reader"], "water_canal_read.f90")
        self.assertEqual(water_canal["entry_count"]["fields"][0]["fortran_name"], "imax")
        self.assertEqual(water_canal["canal_rows"]["count_source"], "entry_count")
        self.assertEqual(water_canal["canal_rows"]["repeat_source"], "canal_rows:num_aqu")
        self.assertEqual([f["fortran_name"] for f in water_canal["canal_rows"]["repeat_fields"]], ["aqu_num", "frac"])

        salt_recall = {section["name"]: section for section in ra["salt_recall.rec"]["sections"]}
        self.assertEqual(ra["salt_recall.rec"]["reader"], "recall_read_salt.f90")
        self.assertEqual(salt_recall["registry_rows"]["count_source"], "row_count_pass")
        self.assertEqual(salt_recall["nested_daily_rows"]["nested_file_field"], "filename")
        self.assertEqual(salt_recall["nested_daily_rows"]["fields"][-1]["count_source"], "constituents.cs:salts_count")
        self.assertEqual(salt_recall["nested_monthly_rows"]["applies_when"], "typ == 2")
        self.assertEqual(salt_recall["nested_annual_rows"]["applies_when"], "typ == 3")

        cs_recall = {section["name"]: section for section in ra["cs_recall.rec"]["sections"]}
        self.assertEqual(ra["cs_recall.rec"]["reader"], "recall_read_cs.f90")
        self.assertEqual(cs_recall["registry_rows"]["count_source"], "row_count_pass")
        self.assertEqual(
            [f["fortran_name"] for f in cs_recall["registry_rows"]["fields"]],
            ["k", "name", "typ", "filename"],
        )
        self.assertEqual(cs_recall["nested_year_count"]["applies_when"], "typ != 4")
        self.assertEqual(cs_recall["nested_year_count"]["nested_file_field"], "filename")
        self.assertEqual(cs_recall["nested_daily_rows"]["count_source"], "until_eof_nested_file")
        self.assertEqual(cs_recall["nested_daily_rows"]["nested_file_field"], "filename")
        self.assertEqual(cs_recall["nested_daily_rows"]["fields"][-1]["count_source"], "constituents.cs:cs_count")
        self.assertEqual(cs_recall["nested_monthly_rows"]["applies_when"], "typ == 2")
        self.assertEqual(cs_recall["nested_annual_rows"]["applies_when"], "typ == 3")

        gwflow_expectations = {
            "cs_recall.rec": (
                "recall_read_cs.f90",
                [
                    "row_count_pass",
                    "registry_rows",
                    "nested_year_count",
                    "nested_daily_rows",
                    "nested_monthly_rows",
                    "nested_annual_rows",
                ],
            ),
            "salt_recall.rec": (
                "recall_read_salt.f90",
                [
                    "row_count_pass",
                    "registry_rows",
                    "nested_year_count",
                    "nested_daily_rows",
                    "nested_monthly_rows",
                    "nested_annual_rows",
                ],
            ),
            "water_canal.wal": (
                "water_canal_read.f90",
                ["entry_count", "canal_rows"],
            ),
            "water_pipe.wal": (
                "water_pipe_read.f90",
                ["entry_count", "pipe_rows"],
            ),
            "cell_sol.gw": (
                "gwflow_read.f90",
                ["solute_rows"],
            ),
            "minerals.gw": (
                "gwflow_read.f90",
                [
                    "mineral_count",
                    "structured_mineral_modes",
                    "structured_single_value_rows",
                    "structured_array_rows",
                    "unstructured_mineral_rows",
                ],
            ),
            "tvheads.gw": (
                "gwflow_read.f90",
                ["row_count_pass", "head_rows"],
            ),
            "ponds.gw": (
                "gwflow_read.f90",
                ["row_count_pass", "pond_rows"],
            ),
            "gwflow_canal.con": (
                "gwflow_read.f90",
                ["canal_header_rows", "canal_connection_rows"],
            ),
        }
        for filename, (reader, section_names) in gwflow_expectations.items():
            schema = ra[filename]
            self.assertEqual(schema["reader"], reader)
            self.assertEqual(
                [section["name"] for section in schema["sections"]],
                section_names,
            )
        cell_sol = ra["cell_sol.gw"]["sections"][0]
        self.assertEqual(cell_sol["count_source"], "gwflow:ncell")
        self.assertEqual(cell_sol["fields"][1]["count_source"], "gwflow:gw_nsolute")
        minerals = {section["name"]: section for section in ra["minerals.gw"]["sections"]}
        self.assertEqual(minerals["mineral_count"]["count_source"], "single_record")
        self.assertEqual(minerals["structured_mineral_modes"]["count_source"], "gwflow:gw_nminl")
        self.assertEqual(minerals["structured_mineral_modes"]["applies_when"], 'grid_type == "structured"')
        self.assertEqual(
            minerals["structured_single_value_rows"]["applies_when"],
            'grid_type == "structured" and read_type == "single"',
        )
        self.assertEqual(
            minerals["structured_array_rows"]["fields"][0]["count_source"],
            "gwflow:grid_ncol",
        )
        self.assertEqual(minerals["unstructured_mineral_rows"]["count_source"], "gwflow:ncell")
        self.assertEqual(
            minerals["unstructured_mineral_rows"]["fields"][0]["count_source"],
            "gwflow:gw_nminl",
        )
        tvheads = ra["tvheads.gw"]["sections"][1]
        self.assertEqual(tvheads["fields"][1]["count_source"], "time:nbyr")
        self.assertEqual(tvheads["fields"][1]["count_expr"], "time%nbyr")
        ponds = ra["ponds.gw"]["sections"][1]
        self.assertEqual(ponds["fields"][-1]["count_source"], "gwflow:gw_nsolute")
        self.assertEqual(ponds["fields"][-1]["count_expr"], "gw_nsolute")
        canal = ra["gwflow_canal.con"]["sections"][1]
        self.assertEqual(canal["repeat_source"], "canal_header_rows:obj_tot")
        self.assertEqual(canal["repeat_expr"], "obj_tot")
        self.assertEqual(
            [f["fortran_name"] for f in canal["repeat_fields"]],
            ["cell_num", "length", "stage"],
        )

        single_array_expectations = {
            "dr_hmet.del": (
                "dr_read_hmet.f90",
                "delivery_ratios",
                "hmet",
                "constituents.cs:metals_count",
                "cs_db%num_metals",
            ),
            "dr_path.del": (
                "dr_path_read.f90",
                "delivery_ratios",
                "path",
                "constituents.cs:paths_count",
                "cs_db%num_paths",
            ),
            "dr_pest.del": (
                "dr_read_pest.f90",
                "delivery_ratios",
                "pest",
                "constituents.cs:pests_count",
                "cs_db%num_pests",
            ),
            "dr_salt.del": (
                "dr_read_salt.f90",
                "delivery_ratios",
                "salt",
                "constituents.cs:salts_count",
                "cs_db%num_salts",
            ),
            "exco_hmet.exc": (
                "exco_read_hmet.f90",
                "export_coefficients",
                "hmet",
                "constituents.cs:metals_count",
                "cs_db%num_metals",
            ),
            "exco_path.exc": (
                "exco_read_path.f90",
                "export_coefficients",
                "path",
                "constituents.cs:paths_count",
                "cs_db%num_paths",
            ),
            "exco_pest.exc": (
                "exco_read_pest.f90",
                "export_coefficients",
                "pest",
                "constituents.cs:pests_count",
                "cs_db%num_pests",
            ),
            "exco_salt.exc": (
                "exco_read_salt.f90",
                "export_coefficients",
                "salt",
                "constituents.cs:salts_count",
                "cs_db%num_salts",
            ),
            "cs_aqu.ini": (
                "cs_aqu_read.f90",
                "aquifer_concentrations",
                "aqu",
                "constituents.cs:cs_count",
                "cs_db%num_cs + cs_db%num_cs",
            ),
            "cs_channel.ini": (
                "cs_cha_read.f90",
                "channel_concentrations",
                "conc",
                "constituents.cs:cs_count",
                "cs_db%num_cs",
            ),
            "salt_channel.ini": (
                "salt_cha_read.f90",
                "channel_concentrations",
                "conc",
                "constituents.cs:salts_count",
                "cs_db%num_salts",
            ),
        }
        for filename, (reader, section_name, field_name, count_source, count_expr) in single_array_expectations.items():
            schema = ra[filename]
            self.assertEqual(schema["reader"], reader)
            sections = {section["name"]: section for section in schema["sections"]}
            self.assertEqual(list(sections), ["row_count_pass", "entry_name", section_name])
            field = sections[section_name]["fields"][0]
            self.assertEqual(field["fortran_name"], field_name)
            self.assertEqual(field["count_source"], count_source)
            self.assertEqual(field["count_expr"], count_expr)

        water_init_expectations = {
            "pest_water.ini": (
                "pest_cha_res_read.f90",
                "constituents.cs:pests_count",
                "cs_db%num_pests",
            ),
            "path_water.ini": (
                "path_cha_res_read.f90",
                "constituents.cs:paths_count",
                "cs_db%num_paths",
            ),
        }
        for filename, (reader, count_source, count_expr) in water_init_expectations.items():
            schema = ra[filename]
            self.assertEqual(schema["reader"], reader)
            sections = {section["name"]: section for section in schema["sections"]}
            self.assertEqual(
                list(sections),
                ["row_count_pass", "entry_name", "water_benthic_concentrations"],
            )
            fields = sections["water_benthic_concentrations"]["fields"]
            self.assertEqual([f["fortran_name"] for f in fields], ["water", "benthic"])
            for field in fields:
                self.assertEqual(field["count_source"], count_source)
                self.assertEqual(field["count_expr"], count_expr)

        wal_expectations = {
            "water_use.wal": "water_use_read.f90",
            "water_treat.wal": "water_treatment_read.f90",
            "out_src.wal": "water_osrc_read.f90",
        }
        for filename, reader in wal_expectations.items():
            schema = ra[filename]
            self.assertEqual(schema["reader"], reader)
            sections = {section["name"]: section for section in schema["sections"]}
            self.assertEqual(
                list(sections),
                [
                    "entry_count",
                    "main_rows",
                    "pest_concentrations",
                    "pathogen_concentrations",
                ],
            )
            self.assertEqual(sections["main_rows"]["count_source"], "entry_count")
            self.assertEqual(
                [f["fortran_name"] for f in sections["pest_concentrations"]["fields"]],
                ["pest"],
            )
            self.assertEqual(
                sections["pest_concentrations"]["fields"][0]["count_source"],
                "constituents.cs:pests_count",
            )
            self.assertEqual(
                [f["fortran_name"] for f in sections["pathogen_concentrations"]["fields"]],
                ["path"],
            )
            self.assertEqual(
                sections["pathogen_concentrations"]["fields"][0]["count_source"],
                "constituents.cs:paths_count",
            )


    def test_multi_section_files_resolve_against_pinned_source(self) -> None:
        ms = self.payload["multi_section"]
        self.assertEqual(self.payload["multi_section_unresolved"], [])
        self.assertEqual(
            set(ms),
            {
                "constituents.cs",
                "hmd.cli",
                "pcp.cli",
                "pet.cli",
                "slr.cli",
                "tmp.cli",
                "wnd.cli",
            },
        )

        constituents = ms["constituents.cs"]
        self.assertEqual(constituents["reader"], "constit_db_read.f90")
        self.assertEqual(
            [section["name"] for section in constituents["sections"]],
            [
                "pests_count",
                "pests_names",
                "paths_count",
                "paths_names",
                "metals_count",
                "metals_names",
                "salts_count",
                "salts_names",
                "cs_count",
                "cs_names",
            ],
        )
        constituents_by_name = {
            section["name"]: section for section in constituents["sections"]
        }
        self.assertEqual(
            constituents_by_name["pests_names"]["count_source"], "pests_count"
        )
        self.assertEqual(
            [f["fortran_name"] for f in constituents_by_name["pests_count"]["fields"]],
            ["num_pests"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in constituents_by_name["pests_names"]["fields"]],
            ["pests"],
        )

        pcp = ms["pcp.cli"]
        self.assertEqual(pcp["reader"], "cli_pmeas.f90")
        self.assertEqual(
            [section["name"] for section in pcp["sections"]],
            ["row_count_pass", "station_name_pass", "station_filename_pass"],
        )
        by_name = {section["name"]: section for section in pcp["sections"]}
        self.assertEqual(
            [f["fortran_name"] for f in by_name["station_name_pass"]["fields"]],
            ["pcp_n"],
        )
        self.assertEqual(
            [f["fortran_name"] for f in by_name["station_filename_pass"]["fields"]],
            ["filename"],
        )
        for name in ("hmd.cli", "pet.cli", "slr.cli", "tmp.cli", "wnd.cli"):
            self.assertEqual(ms[name]["read_pattern"], "multi_section")

    def test_gwflow_read_family_candidates_stay_correctly_unresolved(self) -> None:
        # The 8 files flagged unresolved-even-when-targeted alongside
        # gwflow_read.f90 (see the TARGET_FILES module comment: "Investigated
        # 2026-08"). Diagnosing why "reader not found for filename" is the
        # generic fallback -- not a specific reason -- turned up a real
        # scanner bug (fixed: see ConditionTrailUnspacedEndKeywordTests in
        # test_fortran_scanner.py) plus 8 files that are each correctly
        # unresolvable on their own merits, same as codes.gw/cellcon.gw.
        # This targets them explicitly against the real pinned source to
        # confirm neither the scanner fix nor anything else accidentally
        # resolves them to a schema -- wrong silently would be worse than
        # unresolved.
        candidates = (
            "chan_depth.gw", "hru_pump.gw", "pond_div.gw", "sw_group.gw",
            "transit.gw", "soil_lyr_depths.sol", "carbon_layers.prt", "looping.con",
        )
        project = FortranScanner(BuildConfig(source_dir=self.SOURCE)).scan()
        payload = build_schema(
            project,
            swatplus_version="62.0.0",
            source_ref="62.0.0",
            generator="test",
            targets=TARGET_FILES + candidates,
        )
        for name in candidates:
            self.assertNotIn(name, payload["files"], name)
        unresolved = {e["file"] for e in payload["unresolved"]}
        self.assertEqual(unresolved, set(candidates))


if __name__ == "__main__":
    unittest.main()
