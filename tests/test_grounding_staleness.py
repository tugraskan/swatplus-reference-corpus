from swatplus_reference.docs.grounding import check_page
from swatplus_reference.docs.pages import Page
from swatplus_reference.docs.staleness import compute_status


def page_for(cfg, **kw):
    defaults = dict(
        path=cfg.abs_docs_dir / "procedures" / "demo_calc.md",
        kind="procedure",
        symbol="demo_calc",
        status="filled",
        body="",
    )
    defaults.update(kw)
    return Page(**defaults)


def test_clean_page_has_no_errors(cfg, store):
    page = page_for(
        cfg,
        body="Uses `wrk` and calls [sym:demo_zero]; reads `basin_count`.",
        extra={"locals": {"wrk": "x"}, "args": {"frac": "y"}, "uses": {"demo_module": "z"}},
    )
    assert [f for f in check_page(store, page) if f.level == "error"] == []


def test_broken_sym_ref_is_error(cfg, store):
    page = page_for(cfg, body="See [sym:does_not_exist].")
    codes = [f.code for f in check_page(store, page) if f.level == "error"]
    assert "broken-sym-ref" in codes


def test_unknown_note_entries_are_errors(cfg, store):
    page = page_for(cfg, extra={"locals": {"phantom_var": "x"}, "uses": {"no_such_mod": "y"}})
    codes = {f.code for f in check_page(store, page) if f.level == "error"}
    assert codes == {"unknown-local-note", "unknown-use-note"}


def test_grounding_allow_silences_note_errors(cfg, store):
    page = page_for(
        cfg, extra={"locals": {"phantom_var": "x"}}, grounding_allow=["phantom_var"]
    )
    assert [f for f in check_page(store, page) if f.level == "error"] == []


def test_unknown_backtick_is_warning_only(cfg, store):
    page = page_for(cfg, body="Mentions `totally_made_up_name` here.")
    findings = check_page(store, page)
    assert [f.level for f in findings] == ["warning"]


def test_staleness_transitions(cfg, store):
    sym = store.get("demo_calc")
    fresh = page_for(cfg, source_hash=sym.source_hash)
    stale = page_for(cfg, source_hash="0" * 16)
    todo = page_for(cfg, status="todo")
    orphan = page_for(cfg, symbol="gone_symbol")

    report = compute_status(store, [fresh, stale, todo, orphan])
    assert fresh in report.filled
    assert stale in report.stale
    assert todo in report.todo
    assert orphan in report.orphaned
    # documentable symbols without pages are reported
    assert "demo_module" in report.missing
    assert "demo_zero" in report.missing
