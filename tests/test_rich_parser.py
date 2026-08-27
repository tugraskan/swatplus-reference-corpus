"""Tests for RichStore: build, lookup, and cross-check against thin parser."""
from __future__ import annotations

import json
from pathlib import Path

from swatplus_reference.parser.rich import RichStore
from swatplus_reference.parser.fortran import parse_tree

FIXTURES = Path(__file__).parent / "fixtures"


def test_rich_store_build_loads_fixtures():
    store = RichStore.build(FIXTURES)
    assert store.index.modules  # at least one module parsed


def test_rich_store_module_lookup():
    store = RichStore.build(FIXTURES)
    module = store.get("demo_module")
    assert module is not None
    assert hasattr(module, "name")


def test_rich_store_case_insensitive_lookup():
    store = RichStore.build(FIXTURES)
    upper = store.get("DEMO_MODULE")
    lower = store.get("demo_module")
    assert upper is not None
    assert lower is not None


def test_rich_store_procedure_lookup():
    store = RichStore.build(FIXTURES)
    proc = store.get("demo_calc")
    assert proc is not None


def test_rich_store_cross_check_with_thin():
    thin_store = parse_tree(FIXTURES, "test")
    rich_store = RichStore.build(FIXTURES)

    thin_names = set(thin_store.symbols.keys())
    rich_names = set(rich_store.by_name.keys())

    # Every thin symbol should exist in rich store (presence cross-check)
    for name in thin_names:
        assert rich_store.get(name) is not None, f"Symbol '{name}' missing from rich store"


def test_rich_store_save_produces_valid_json(tmp_path):
    store = RichStore.build(FIXTURES)
    out = tmp_path / "rich.json"
    store.save(out)

    assert out.exists()
    data = json.loads(out.read_text())
    assert isinstance(data, dict)
    assert "modules" in data
