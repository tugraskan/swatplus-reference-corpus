from __future__ import annotations

from pathlib import Path

from swatplus_reference.docs.pages import Page, STATUS_FILLED
from swatplus_reference.docs.staleness import compute_status
from swatplus_reference.parser.facts import FactStore, LocalVar, Symbol
from swatplus_reference.parser.fortran import _classify_line, parse_tree

FIXTURES = Path(__file__).parent / "fixtures"

SRC = """\
      module shared_state
      implicit none
      real :: albday = 0.
      real :: shared_acc = 0.
      real :: petval = 0.
      end module shared_state

      subroutine make_albedo
      use shared_state
      real :: cover = 0.
      albday = 0.23 * cover
      shared_acc = shared_acc + 1.
      end subroutine make_albedo

      subroutine use_albedo
      use shared_state
      real :: x
      x = albday * 2.
      shared_acc = shared_acc + x
      end subroutine use_albedo

      subroutine also_writes_acc
      use shared_state
      shared_acc = 0.
      end subroutine also_writes_acc

      subroutine acc_reader
      use shared_state
      real :: y
      y = shared_acc + 1.
      end subroutine acc_reader
"""

def test_classify_line():
    assert _classify_line("      albday = 0.23 * cover") == ("albday", ["cover"])
    assert _classify_line("      x = albday * 2.")[0] == "x"
    assert "albday" in _classify_line("      x = albday * 2.")[1]
    # comparison / control lines are all-reads, no write
    w, r = _classify_line("      if (albday > 0.) then")
    assert w is None and "albday" in r
    # declarations are ignored
    assert _classify_line("      real :: albday = 0.") == (None, [])


def test_reads_writes_extracted(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "shared_state.f90").write_text(SRC)
    store = parse_tree(src_dir, "t")

    mk = store.get("make_albedo")
    assert "albday" in mk.writes and "shared_acc" in mk.writes
    assert "albday" not in mk.reads  # written, not double-counted
    # 'cover' is a local, must not be treated as shared state
    assert "cover" not in mk.reads and "cover" not in mk.writes

    ua = store.get("use_albedo")
    assert "albday" in ua.reads
    assert store.readers_of("albday")[0].name == "use_albedo"
    assert {s.name for s in store.writers_of("shared_acc")} == \
        {"make_albedo", "use_albedo", "also_writes_acc"}


def _pages(tmp, store, names, changed=()) -> list[Page]:
    """Pages whose source_hash matches the store (so they read as filled),
    except `changed` symbols which are given a mismatching hash (stale)."""
    out = []
    for n in names:
        sym = store.get(n)
        h = "STALE" if n in changed else (sym.source_hash if sym else "h")
        out.append(Page(path=Path(tmp) / "procedures" / f"{n}.md", kind="procedure",
                        symbol=n, status=STATUS_FILLED, source_hash=h, body=""))
    return out


def test_narrow_variable_flags_readers(tmp_path):
    src_dir = tmp_path / "src"; src_dir.mkdir()
    (src_dir / "shared_state.f90").write_text(SRC)
    store = parse_tree(src_dir, "t")
    pages = _pages(tmp_path, store,
                   ["make_albedo", "use_albedo", "also_writes_acc", "acc_reader"],
                   changed=["make_albedo"])
    r = compute_status(store, pages, max_writers=3)
    affected = {p.symbol for p in r.affected}
    # albday has 1 writer (make_albedo) -> its reader use_albedo is flagged via data-flow
    assert "use_albedo" in affected
    assert any("via albday" in t for t in r.affected_by["use_albedo.md"])


def test_broadly_written_variable_does_not_propagate(tmp_path):
    src_dir = tmp_path / "src"; src_dir.mkdir()
    (src_dir / "shared_state.f90").write_text(SRC)
    store = parse_tree(src_dir, "t")
    pages = _pages(tmp_path, store,
                   ["make_albedo", "use_albedo", "also_writes_acc", "acc_reader"],
                   changed=["make_albedo"])
    # shared_acc has 3 writers; with max_writers=2 it is "broadly written"
    r = compute_status(store, pages, max_writers=2)
    # acc_reader (reads only shared_acc) must NOT be flagged
    assert "acc_reader" not in {p.symbol for p in r.affected}


def test_hub_fanout_cap_suppresses_dataflow(tmp_path):
    store = FactStore()
    # a hub that writes 5 narrowly-written vars, each read by a distinct page
    store.add(Symbol(kind="subroutine", name="hub", file="h.f90",
                     start_line=1, end_line=2, writes=[f"v{i}" for i in range(5)],
                     source_hash="hubOLD"))
    readers = []
    for i in range(5):
        n = f"r{i}"
        store.add(Symbol(kind="subroutine", name=n, file="h.f90",
                         start_line=1, end_line=2, reads=[f"v{i}"], source_hash="r"))
        readers.append(n)

    def fresh_pages():
        return _pages(tmp_path, store, ["hub", *readers], changed=["hub"])

    # cap below the fan-out -> data-flow suppressed for the hub
    r = compute_status(store, fresh_pages(), max_writers=3, max_fanout=3)
    assert r.affected == []
    # raise the cap -> all readers flagged
    r2 = compute_status(store, fresh_pages(), max_writers=3, max_fanout=10)
    assert len(r2.affected) == 5
