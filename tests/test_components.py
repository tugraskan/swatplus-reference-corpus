from __future__ import annotations

from pathlib import Path

from swatplus_reference.docs.grounding import check_page
from swatplus_reference.docs.pages import Page
from swatplus_reference.docs.render import Renderer
from swatplus_reference.parser.facts import Component, FactStore, Symbol
from swatplus_reference.parser.fortran import parse_components, parse_file_ast
from swatplus_reference.source.config import Config

TYPE_SRC = """\
      module demo_types_module
      implicit none
      type demo_state
        real :: flo = 0.        !mm         |lateral flow
        real :: dep_wt = 0.     !m          |depth to water table
        character(len=13) :: nm = "x"   !! none | record name
        type (other), dimension(:), allocatable :: kids   ! child records
      end type demo_state
      end module demo_types_module
"""


def test_parse_components_units_and_desc():
    store = FactStore()
    parse_file_ast(store, "demo_types_module.f90", TYPE_SRC)
    t = store.get("demo_state")
    assert t is not None and t.kind == "type"
    by = {c.name: c for c in t.components}
    assert set(by) == {"flo", "dep_wt", "nm", "kids"}
    assert by["flo"].units == "mm" and by["flo"].description == "lateral flow"
    assert by["dep_wt"].decl == "real"
    # `!!` comment with `|` split too
    assert by["nm"].units == "none" and by["nm"].description == "record name"
    # comment with no `|` -> all description, no units
    assert by["kids"].units == "" and by["kids"].description == "child records"
    # allocatable/derived decl captured
    assert "allocatable" in by["kids"].decl


def test_split_entities_respects_parens():
    store = FactStore()
    src = ("module m\ntype t\n  real, dimension(:,:) :: a, b\nend type t\nend module m\n")
    parse_file_ast(store, "m.f90", src)
    names = {c.name for c in store.get("t").components}
    assert names == {"a", "b"}


def _module_with_type() -> tuple[FactStore, Symbol]:
    store = FactStore()
    t = Symbol(kind="type", name="demo_state", file="m.f90", start_line=2, end_line=5,
               parent="demo_module",
               components=[Component("flo", "real", "mm", "lateral flow"),
                           Component("stor", "real", "mm", "storage")])
    m = Symbol(kind="module", name="demo_module", file="m.f90", start_line=1, end_line=9)
    store.add(t)
    store.add(m)
    return store, m


def test_block_types_renders_source_and_notes(tmp_path):
    store, m = _module_with_type()
    cfg = Config(root=tmp_path, source_link_base="https://x/src", docs_dir=tmp_path)
    page = Page(path=tmp_path / "modules" / "demo_module.md", kind="module",
                symbol="demo_module", title="demo_module", status="filled",
                extra={"type_components": {"demo_state": {"flo": "reviewed flo note"}},
                       "type_summaries": {"demo_state": "A state record."}})
    out = Renderer(cfg, store, [page]).block_types(page, m)
    assert "### " in out and "demo_state" in out
    assert "A state record." in out                 # summary
    assert "| `flo` | `real` | mm | lateral flow | reviewed flo note |" in out
    assert "| `stor` | `real` | mm | storage |  |" in out  # real component, no note


def test_grounding_flags_bad_component_note(tmp_path):
    store, m = _module_with_type()
    page = Page(path=tmp_path / "modules" / "demo_module.md", kind="module",
                symbol="demo_module", status="filled",
                extra={"type_components": {"demo_state": {"phantom": "n"}}})
    codes = {f.code for f in check_page(store, page) if f.level == "error"}
    assert "unknown-component-note" in codes


def test_grounding_flags_bad_type_note(tmp_path):
    store, m = _module_with_type()
    page = Page(path=tmp_path / "modules" / "demo_module.md", kind="module",
                symbol="demo_module", status="filled",
                extra={"type_components": {"not_a_type": {"flo": "n"}}})
    codes = {f.code for f in check_page(store, page) if f.level == "error"}
    assert "unknown-type-note" in codes


def test_components_survive_json_roundtrip():
    store = FactStore()
    parse_file_ast(store, "demo_types_module.f90", TYPE_SRC)
    loaded = FactStore.from_json(store.to_json())
    assert [c.name for c in loaded.get("demo_state").components] == \
           [c.name for c in store.get("demo_state").components]
    assert loaded.get("demo_state").components[0].units == "mm"
