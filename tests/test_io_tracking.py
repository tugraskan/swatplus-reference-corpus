from __future__ import annotations

from pathlib import Path

from swatplus_reference.docs.pages import Page, STATUS_FILLED, load_page
from swatplus_reference.docs.staleness import compute_status
from swatplus_reference.parser.facts import FactStore, Symbol, composite_source_hash


def store_with(readers: dict[str, str]) -> FactStore:
    s = FactStore(source_ref="t")
    for name, h in readers.items():
        s.add(Symbol(kind="subroutine", name=name, file=f"{name}.f90",
                     start_line=1, end_line=3, source_hash=h))
    return s


def io_page(tmp, name, source_symbols, source_hash) -> Page:
    return Page(path=Path(tmp) / "io" / f"{name}.md", kind="io",
                source_symbols=source_symbols, title=name, status=STATUS_FILLED,
                source_hash=source_hash, body="doc")


def test_composite_hash_stable_and_order_independent():
    store = store_with({"a": "h1", "b": "h2"})
    assert composite_source_hash(store, ["a", "b"]) == composite_source_hash(store, ["b", "a"])
    # changes when a source hash changes
    h_before = composite_source_hash(store, ["a", "b"])
    store.get("a").source_hash = "h1new"
    assert composite_source_hash(store, ["a", "b"]) != h_before
    # None when a source symbol is missing
    assert composite_source_hash(store, ["a", "gone"]) is None


def test_io_page_filled_when_reader_unchanged(tmp_path):
    store = store_with({"aqu_read": "r1"})
    h = composite_source_hash(store, ["aqu_read"])
    page = io_page(tmp_path, "aquifer.aqu", ["aqu_read"], h)
    r = compute_status(store, [page])
    assert page in r.filled and not r.stale and not r.orphaned


def test_io_page_stale_when_reader_changes(tmp_path):
    store = store_with({"aqu_read": "r1"})
    page = io_page(tmp_path, "aquifer.aqu", ["aqu_read"],
                   composite_source_hash(store, ["aqu_read"]))
    store.get("aqu_read").source_hash = "r2"  # reader changed
    r = compute_status(store, [page])
    assert page in r.stale


def test_io_page_orphaned_when_reader_removed(tmp_path):
    store = store_with({"aqu_read": "r1"})
    page = io_page(tmp_path, "aquifer.aqu", ["aqu_read"],
                   composite_source_hash(store, ["aqu_read"]))
    del store.symbols["aqu_read"]  # prior release: reader doesn't exist
    r = compute_status(store, [page])
    assert page in r.orphaned


def test_output_family_tracks_opener_and_writer(tmp_path):
    store = store_with({"header_aquifer": "o1", "aquifer_output": "w1"})
    srcs = ["aquifer_output", "header_aquifer"]
    page = Page(path=tmp_path / "output_families" / "aquifer.md",
                kind="output_family", source_symbols=srcs, title="aquifer_*",
                status=STATUS_FILLED, source_hash=composite_source_hash(store, srcs),
                body="x")
    assert compute_status(store, [page]).filled == [page]
    store.get("aquifer_output").source_hash = "w2"  # writer changed
    assert page in compute_status(store, [page]).stale


def test_source_symbols_roundtrip(tmp_path):
    (tmp_path / "io").mkdir()
    page = io_page(tmp_path, "aquifer.aqu", ["aqu_read"], "abc123")
    page.save()
    loaded = load_page(page.path)
    assert loaded.source_symbols == ["aqu_read"]
    assert loaded.source_hash == "abc123"


def test_page_without_source_still_untracked(tmp_path):
    # a symbol-less page with no source_symbols stays filled (legacy behaviour)
    store = FactStore()
    page = Page(path=tmp_path / "io" / "x.md", kind="io", status=STATUS_FILLED, body="x")
    r = compute_status(store, [page])
    assert page in r.filled
