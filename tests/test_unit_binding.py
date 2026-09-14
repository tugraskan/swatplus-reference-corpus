"""Cross-file I/O unit binding.

SWAT+ opens an output unit centrally and writes to it from elsewhere, so a
per-file unit table leaves ~96% of write statements with the index's
`unit_<unit>` sentinel. These pin both what the pass recovers and, just as
importantly, the three things it must refuse to guess.
"""

from pathlib import Path

from swatplus_reference.parser.ast_index import build_ast_index
from swatplus_reference.parser.schema_config import BuildConfig


def _index(tmp_path: Path, files: dict[str, str]):
    for name, body in files.items():
        (tmp_path / name).write_text(body)
    return build_ast_index(BuildConfig(source_dir=tmp_path))


def _named(index) -> dict[str, list[str]]:
    """filename -> kinds of operation recorded against it."""
    return {
        (f.display_name or f.key): [op.kind for op in f.operations]
        for f in index.io_files
    }


OPENER = """\
      subroutine opener
      open (140,file="split.out")
      end subroutine opener
"""
WRITER = """\
      subroutine writer
      real :: flow = 0.
      write (140,*) flow
      end subroutine writer
"""


def test_a_unit_opened_in_another_file_is_bound(tmp_path):
    index = _index(tmp_path, {"opener.f90": OPENER, "writer.f90": WRITER})
    named = _named(index)
    assert "split.out" in named
    assert "write" in named["split.out"]
    assert not any(k.startswith("unit_") for k in named)


def test_a_unit_opened_against_two_files_stays_unresolved(tmp_path):
    """Unit 107 is SWAT+'s input scratch unit, opened against 147 different
    files. Binding project-wide would name it after whichever was scanned last,
    so a unit with more than one filename must resolve to none of them."""
    index = _index(
        tmp_path,
        {
            "a.f90": '      subroutine a\n      open (107,file="one.in")\n      end subroutine a\n',
            "b.f90": '      subroutine b\n      open (107,file="two.in")\n      end subroutine b\n',
            "c.f90": "      subroutine c\n      write (107,*) 1\n      end subroutine c\n",
        },
    )
    named = _named(index)
    assert "unit_107" in named
    assert named.get("one.in") == ["open"]
    assert named.get("two.in") == ["open"]


def test_a_unit_never_opened_stays_unresolved(tmp_path):
    """Writing to an unopened unit is legal Fortran and gets a compiler-default
    file. There is no filename in the source, so the sentinel is the answer."""
    index = _index(tmp_path, {"w.f90": "      subroutine w\n      write (9000,*) 1\n      end subroutine w\n"})
    assert "unit_9000" in _named(index)


# --------------------------------------------------------------------------
# Opens routed through a helper
# --------------------------------------------------------------------------

HELPER = """\
      subroutine open_output_file(iunit, filename)
      integer, intent(in) :: iunit
      character(len=*), intent(in) :: filename
      character(len=512) :: full_path
      full_path = get_output_filename(filename)
      open (iunit, file=trim(full_path))
      end subroutine open_output_file
"""


def test_a_unit_opened_through_a_helper_is_bound(tmp_path):
    """The unit and filename are literals at the call site; the open itself
    names only dummy arguments."""
    index = _index(
        tmp_path,
        {
            "helper.f90": HELPER,
            "caller.f90": '      subroutine caller\n'
                          '      call open_output_file(8348, "hru_cbn_lyr.txt")\n'
                          '      end subroutine caller\n',
            "writer.f90": "      subroutine w\n      write (8348,*) 1\n      end subroutine w\n",
        },
    )
    named = _named(index)
    assert "hru_cbn_lyr.txt" in named
    assert "write" in named["hru_cbn_lyr.txt"]


def test_binding_forwards_through_a_wrapper(tmp_path):
    """`open_cb_wide_pair` opens nothing itself: it passes its own arguments to
    `open_output_file`, and the literals are one level further out."""
    index = _index(
        tmp_path,
        {
            "helper.f90": HELPER,
            "wrap.f90": "      subroutine wide_pair(u_txt, fname_txt)\n"
                        "      integer, intent(in) :: u_txt\n"
                        "      character(len=*), intent(in) :: fname_txt\n"
                        "      call open_output_file(u_txt, fname_txt)\n"
                        "      end subroutine wide_pair\n",
            "caller.f90": '      subroutine caller\n'
                          '      call wide_pair(4566, "hru_pool_day.txt")\n'
                          '      end subroutine caller\n',
            "writer.f90": "      subroutine w\n      write (4566,*) 1\n      end subroutine w\n",
        },
    )
    assert "hru_pool_day.txt" in _named(index)


def test_a_helper_called_with_a_variable_unit_binds_nothing(tmp_path):
    """Only literals bind. A unit still held in a variable at the call site
    would need the value, which means running the model."""
    index = _index(
        tmp_path,
        {
            "helper.f90": HELPER,
            "caller.f90": '      subroutine caller\n'
                          "      integer :: iu = 0\n"
                          '      call open_output_file(iu, "maybe.txt")\n'
                          '      end subroutine caller\n',
            "writer.f90": "      subroutine w\n      write (7777,*) 1\n      end subroutine w\n",
        },
    )
    assert "unit_7777" in _named(index)


def test_a_collision_between_two_output_files_is_reported(tmp_path):
    """SWAT+ opens unit 4814 against two different .csv files. Neither name can
    be used, and staying silent about it would hide a real conflict."""
    index = _index(
        tmp_path,
        {
            "helper.f90": HELPER,
            "caller.f90": '      subroutine caller\n'
                          '      call open_output_file(4814, "channel_sd_subday.csv")\n'
                          '      call open_output_file(4814, "sd_chanbud_yr.csv")\n'
                          '      end subroutine caller\n',
        },
    )
    flags = [f for f in index.review_flags if f.code == "io_unit_bound_to_several_files"]
    assert len(flags) == 1
    assert "channel_sd_subday.csv" in flags[0].message
    assert "sd_chanbud_yr.csv" in flags[0].message


def test_an_input_scratch_unit_is_not_reported_as_a_collision(tmp_path):
    """Reusing one unit for a run of input files -- open, read, close, open the
    next -- is ordinary Fortran. Flagging it would bury the output collisions."""
    index = _index(
        tmp_path,
        {
            "a.f90": '      subroutine a\n      open (107,file="one.in")\n'
                     "      read (107,*) 1\n      close (107)\n      end subroutine a\n",
            "b.f90": '      subroutine b\n      open (107,file="two.in")\n'
                     "      read (107,*) 1\n      close (107)\n      end subroutine b\n",
        },
    )
    assert [f for f in index.review_flags if f.code == "io_unit_bound_to_several_files"] == []


def test_a_resolved_filename_is_never_overwritten(tmp_path):
    """A local open is the authority for its own file; the project pass only
    fills in sentinels."""
    index = _index(
        tmp_path,
        {
            "local.f90": '      subroutine local\n      open (300,file="local.out")\n'
                         "      write (300,*) 1\n      end subroutine local\n",
            "other.f90": '      subroutine other\n      open (300,file="other.out")\n'
                         "      end subroutine other\n",
        },
    )
    named = _named(index)
    assert "write" in named["local.out"]
