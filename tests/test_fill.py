from swatplus_reference.docs.grounding import check_page
from swatplus_reference.docs.pages import Page
from swatplus_reference.generation.fill import build_fact_sheet, drop_ungrounded_notes, result_to_page


def test_fill_result_to_page_and_grounding(cfg, store):
    sym = store.get("demo_calc")
    page = Page(
        path=cfg.abs_docs_dir / "procedures" / "demo_calc.md",
        kind="procedure",
        symbol="demo_calc",
        status="todo",
    )
    data = {
        "short_description": "Sums storage.",
        "bottom_line": "It sums.",
        "where_it_fits": "Daily loop.",
        "algorithm": [{"step": "1", "behavior": "sum storage"}],
        "arg_notes": [{"name": "frac", "note": "fraction"}],
        "local_notes": [
            {"name": "wrk", "note": "accumulator"},
            {"name": "hallucinated", "note": "should be dropped"},
        ],
        "use_notes": [{"name": "demo_module", "note": "state"}],
        "variable_notes": [],
        "state_changes": [],
    }
    result_to_page(page, sym, data)
    dropped = drop_ungrounded_notes(store, page)

    assert page.status == "filled"
    assert page.source_hash == sym.source_hash
    assert "hallucinated" not in page.extra["locals"]
    assert dropped == ["locals:hallucinated"]
    assert [f for f in check_page(store, page) if f.level == "error"] == []


def test_batch_request_matches_interactive_prompt(cfg, store):
    from swatplus_reference.generation.batch import build_request

    page = Page(
        path=cfg.abs_docs_dir / "procedures" / "demo_calc.md",
        kind="procedure",
        symbol="demo_calc",
        status="todo",
    )
    req = build_request(cfg, store, page, model=None)
    assert req["custom_id"] == "demo_calc"
    params = req["params"]
    assert params["model"] == cfg.fill.model
    assert params["output_config"]["format"]["type"] == "json_schema"
    # same fact sheet the interactive path sends
    assert build_fact_sheet(cfg, store, store.get("demo_calc")) in params["messages"][0]["content"]


def test_fact_sheet_contents(cfg, store):
    sheet = build_fact_sheet(cfg, store, store.get("demo_calc"))
    assert "## Arguments" in sheet and "- frac:" in sheet
    assert "## Calls" in sheet and "demo_zero" in sheet
    assert "```fortran" in sheet and "subroutine demo_calc" in sheet
