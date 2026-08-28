from pathlib import Path

from swatplus_reference.docs.pages import Page, load_page
from swatplus_reference.docs.render import Renderer, render_site
from swatplus_reference.parser.rich import RichStore

FIXTURES = Path(__file__).parent / "fixtures"


def make_page(cfg, body, **kw):
    page = Page(
        path=cfg.abs_docs_dir / "procedures" / "demo_calc.md",
        kind="procedure",
        symbol="demo_calc",
        title="demo_calc",
        status=kw.pop("status", "filled"),
        version_label=kw.pop("version_label", "TEST 1.0"),
        body=body,
        **kw,
    )
    page.save()
    return page


def test_page_roundtrip(cfg):
    page = make_page(
        cfg,
        "Hello `wrk`.",
        extra={"locals": {"wrk": "working value"}},
        grounding_allow=["odd_one"],
    )
    loaded = load_page(page.path)
    assert loaded.symbol == "demo_calc"
    assert loaded.extra["locals"] == {"wrk": "working value"}
    assert loaded.grounding_allow == ["odd_one"]
    assert loaded.body == "Hello `wrk`."


def test_fact_injection(cfg, store):
    page = make_page(
        cfg,
        "<!-- facts:header -->\n\n<!-- facts:arguments -->\n\n"
        "<!-- facts:calls -->\n\n<!-- facts:locals -->\n\n<!-- facts:io -->\n\n"
        "See [sym:demo_zero] and [sym:nonexistent_thing].",
        extra={"args": {"frac": "storage fraction"}, "locals": {"wrk": "accumulator"}},
    )
    out = Renderer(cfg, store, [page]).render_page(page)
    # header resolves current line numbers from the fact store
    sym = store.get("demo_calc")
    assert f"demo_calc.f90:{sym.start_line}-{sym.end_line}" in out
    # prose meaning merged with parser declaration
    assert "| `frac` | `real, intent(in)` | in | storage fraction |" in out
    assert "| `wrk` |" in out and "accumulator" in out
    # symbol ref resolves to source when no page exists; unknown stays plain
    assert "https://example.test/src/demo_module.f90" in out
    assert "`nonexistent_thing`" in out
    # io table carries a line-anchored source link
    assert "#L" in out


def test_block_arguments_enriched_with_rich_store(cfg, store):
    rich = RichStore.build(FIXTURES)
    page = make_page(
        cfg,
        "<!-- facts:arguments -->\n\n",
    )
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "Units" in out
    assert "Description" in out
    assert "none" in out
    assert "fraction applied to storage" in out
    assert "](https://example.test/src/demo_calc.f90#" in out


def test_rich_table_cells_escape_pipe_characters(cfg, store):
    rich = RichStore.build(FIXTURES)
    proc = rich.get_of_kind("demo_calc", "subroutine", file="demo_calc.f90")
    assert proc is not None
    frac = next(v for v in proc.variables if v.name == "frac")
    frac.doc = "none | description with | pipe"
    page = make_page(
        cfg,
        "<!-- facts:arguments -->\n\n",
        extra={"args": {"frac": "meaning with | pipe"}},
    )
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "description with &#124; pipe" in out
    assert "meaning with &#124; pipe" in out


def test_block_arguments_fallback_without_rich_store(cfg, store):
    page = make_page(
        cfg,
        "<!-- facts:arguments -->\n\n",
        extra={"args": {"frac": "storage fraction"}},
    )
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "| `frac` | `real, intent(in)` | in | storage fraction |" in out
    assert "Units" not in out
    assert "Description" not in out


def test_block_locals_enriched_with_rich_store(cfg, store):
    rich = RichStore.build(FIXTURES)
    page = make_page(
        cfg,
        "<!-- facts:locals -->\n\n",
    )
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "Units" in out
    assert "Description" in out
    assert "Initial" in out
    assert "counter" in out
    assert "working value" in out
    assert "0." in out
    assert "](https://example.test/src/demo_calc.f90#" in out


def test_block_locals_fallback_without_rich_store(cfg, store):
    page = make_page(
        cfg,
        "<!-- facts:locals -->\n\n",
        extra={"locals": {"j": "loop counter", "wrk": "workspace"}},
    )
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "| `j` |" in out and "loop counter" in out
    assert "| `wrk` |" in out and "workspace" in out
    assert "Units" not in out
    assert "Description" not in out
    assert "Initial" not in out


def make_module_page(cfg, body, **kw):
    page = Page(
        path=cfg.abs_docs_dir / "modules" / "demo_module.md",
        kind="module",
        symbol="demo_module",
        title="demo_module",
        status=kw.pop("status", "filled"),
        version_label=kw.pop("version_label", "TEST 1.0"),
        body=body,
        **kw,
    )
    page.save()
    return page


def test_block_variables_enriched_with_rich_store(cfg, store):
    rich = RichStore.build(FIXTURES)
    page = make_module_page(cfg, "<!-- facts:variables -->\n\n")
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "number of basins" in out
    assert "ha" in out
    assert "total basin area" in out
    assert "0" in out
    assert "0." in out
    assert "](https://example.test/src/demo_module.f90#" in out


def test_block_variables_fallback_without_rich_store(cfg, store):
    page = make_module_page(
        cfg,
        "<!-- facts:variables -->\n\n",
        extra={"variables": {"basin_count": "number of watersheds"}},
    )
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "| `basin_count` |" in out
    assert "number of watersheds" in out
    assert "Units" not in out
    assert "Initial" not in out


def test_block_uses_enriched_with_rich_store(cfg, store):
    rich = RichStore.build(FIXTURES)
    page = make_page(cfg, "<!-- facts:uses -->\n\n")
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "| Module | Source | Only | Why it matters here |" in out
    assert out.count("[`demo_calc.f90:") == 2


def test_block_uses_fallback_without_rich_store(cfg, store):
    page = make_page(cfg, "<!-- facts:uses -->\n\n")
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "| Module | Only | Why it matters here |" in out
    assert "| Module | Source | Only | Why it matters here |" not in out


def test_block_io_enriched_with_rich_store(cfg, store):
    rich = RichStore.build(FIXTURES)
    page = make_page(cfg, "<!-- facts:io -->\n\n")
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "demo.in" in out
    assert "wrk" in out
    assert "| Statement | Unit | File | Resolved File | Fields | Condition | Source |" in out


def test_block_io_fallback_without_rich_store(cfg, store):
    page = make_page(cfg, "<!-- facts:io -->\n\n")
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "| Statement | Unit | File | Source |" in out
    assert "Resolved File" not in out


def make_select_page(cfg, body, **kw):
    page = Page(
        path=cfg.abs_docs_dir / "procedures" / "demo_select.md",
        kind="procedure",
        symbol="demo_select",
        title="demo_select",
        status=kw.pop("status", "filled"),
        version_label=kw.pop("version_label", "TEST 1.0"),
        body=body,
        **kw,
    )
    page.save()
    return page


def test_block_assignments_with_rich_store(cfg, store):
    rich = RichStore.build(FIXTURES)
    page = make_page(
        cfg,
        "<!-- facts:assignments -->\n\n",
        extra={"state_changes": {"total_area": "published total"}},
    )
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "wrk = wrk + dstate(j)%stor * frac" in out
    assert "total_area = wrk" in out
    assert "published total" in out
    assert "](https://example.test/src/demo_calc.f90#" in out


def test_block_assignments_without_rich_store(cfg, store):
    page = make_page(cfg, "<!-- facts:assignments -->\n\n")
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "*No assignments recorded.*" in out


def test_block_select_cases_with_rich_store(cfg, store):
    rich = RichStore.build(FIXTURES)
    page = make_select_page(cfg, "<!-- facts:select_cases -->\n\n")
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "low" in out
    assert "mid" in out
    assert "high" in out
    assert "default" not in out
    assert "](https://example.test/src/demo_select.f90#" in out


def test_block_select_cases_empty_without_matching_select(cfg, store):
    page = make_page(cfg, "<!-- facts:select_cases -->\n\n")
    rich = RichStore.build(FIXTURES)
    out = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "**Subject:**" not in out
    assert "**Cases:**" not in out


def test_render_site_writes_indexes(cfg, store):
    make_page(cfg, "<!-- facts:header -->")
    out_dir = render_site(cfg, store)
    assert (out_dir / "procedures" / "demo_calc.md").exists()
    assert (out_dir / "procedures" / "index.md").exists()
    assert (out_dir / "index.md").exists()


def test_status_badge_on_todo(cfg, store):
    page = make_page(cfg, "<!-- facts:header -->", status="todo")
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "Status: todo" in out


def test_header_distinguishes_current_source_from_older_prose(cfg, store):
    page = make_page(
        cfg,
        "<!-- facts:header -->",
        version_label="OLDER SOURCE",
    )
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "**Source revision:** TEST 1.0" in out
    assert "**Prose baseline:** OLDER SOURCE" in out


def test_header_preserves_original_version_line_when_revisions_match(cfg, store):
    page = make_page(cfg, "<!-- facts:header -->")
    out = Renderer(cfg, store, [page]).render_page(page)
    assert "**Version:** TEST 1.0" in out
    assert "**Source revision:**" not in out
    assert "**Prose baseline:**" not in out
