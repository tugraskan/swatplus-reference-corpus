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
