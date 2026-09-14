"""Tests for RichStore: build, lookup, and cross-check against thin parser."""
from __future__ import annotations

import json
from dataclasses import fields

import pytest
from pathlib import Path

from swatplus_reference.parser.rich import (
    RICH_EXPORT_SCHEMA,
    SNAPSHOT_FORMAT,
    _EXPORT_FIELDS,
    _INTENTIONALLY_INTERNAL_EXPORT_FIELDS,
    RichStore,
)
from swatplus_reference.parser.fortran import parse_tree
from swatplus_reference.parser.schema_model import (
    CallRef,
    ProjectIndex,
    ProcedureDoc,
    DerivedTypeDoc,
    SourceLocation,
)

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
    contract = data["metadata"]["swatplus_reference_rich_snapshot"]
    assert contract["format"] == SNAPSHOT_FORMAT
    assert contract["export"] == RICH_EXPORT_SCHEMA


def test_portable_export_classifies_every_model_field():
    for record_type, exported_names in _EXPORT_FIELDS.items():
        declared_names = {item.name for item in fields(record_type)}
        internal_names = set(
            _INTENTIONALLY_INTERNAL_EXPORT_FIELDS.get(record_type, ())
        )
        assert set(exported_names).isdisjoint(internal_names)
        assert set(exported_names) | internal_names == declared_names


def test_rich_store_save_and_load_round_trip_with_source_provenance(tmp_path):
    store = RichStore.build(FIXTURES)
    out = tmp_path / "rich.json"
    source_ref = "0123456789abcdef0123456789abcdef01234567"
    store.save(
        out,
        provenance={
            "profile": "fixture",
            "repository": "https://example.test/swatplus",
            "requested_ref": "fixture-tag",
            "configured_commit": source_ref,
            "resolved_commit": source_ref,
        },
    )

    loaded = RichStore.load(out, expected_source_ref=source_ref)
    assert loaded.get_of_kind("demo_calc", "subroutine", file="demo_calc.f90")
    assert loaded.outside_state_refs_for("demo_calc", "subroutine", "demo_calc.f90")
    assert json.loads(out.read_text())["source_root"] == "."


def test_rich_store_rejects_snapshot_for_other_source(tmp_path):
    out = tmp_path / "rich.json"
    RichStore.build(FIXTURES).save(
        out,
        provenance={"resolved_commit": "a" * 40},
    )

    import pytest

    with pytest.raises(ValueError, match="expected"):
        RichStore.load(out, expected_source_ref="b" * 40)


def test_rich_store_loads_v1_and_rejects_unknown_snapshot_formats(tmp_path):
    import pytest

    out = tmp_path / "rich.json"
    RichStore.build(FIXTURES).save(out)
    payload = json.loads(out.read_text(encoding="utf-8"))
    contract = payload["metadata"]["swatplus_reference_rich_snapshot"]

    contract["format"] = 1
    out.write_text(json.dumps(payload), encoding="utf-8")
    assert RichStore.load(out).get("demo_calc") is not None

    contract["format"] = 99
    out.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="supported formats"):
        RichStore.load(out)


def test_v2_export_keeps_real_calls_and_drops_unresolved_function_candidates(
    tmp_path,
):
    location = SourceLocation("calls.f90", 1, 20)
    caller = ProcedureDoc(
        name="caller",
        kind="subroutine",
        location=location,
        calls=[
            CallRef(
                "array_value",
                "x = array_value(i)",
                SourceLocation("calls.f90", 2),
                kind="function",
            ),
            CallRef(
                "real_function",
                "x = real_function(i)",
                SourceLocation("calls.f90", 3),
                kind="function",
            ),
            CallRef(
                "real_function",
                "y = real_function(j)",
                SourceLocation("calls.f90", 4),
                kind="function",
            ),
            CallRef(
                "external_subroutine",
                "call external_subroutine()",
                SourceLocation("calls.f90", 5),
            ),
        ],
    )
    target = ProcedureDoc(
        name="real_function",
        kind="function",
        location=SourceLocation("calls.f90", 10, 12),
    )
    store = RichStore(
        ProjectIndex(
            project_name="test", source_root=".", procedures=[caller, target]
        )
    )
    out = tmp_path / "rich.json"

    store.save(out)

    calls = json.loads(out.read_text(encoding="utf-8"))["procedures"][0]["calls"]
    assert [(call["name"], call["location"]["line"]) for call in calls] == [
        ("real_function", 3),
        ("real_function", 4),
        ("external_subroutine", 5),
    ]
    assert target.called_by == ["caller"]


def test_rich_store_type_procedure_collision():
    proc = ProcedureDoc(
        name="cs_balance",
        kind="subroutine",
        location=SourceLocation(path="test.f90", line=10, end_line=20),
    )
    type_doc = DerivedTypeDoc(
        name="cs_balance",
        location=SourceLocation(path="test.f90", line=30, end_line=40),
    )
    project_index = ProjectIndex(
        project_name="test",
        source_root=".",
        modules=[],
        procedures=[proc],
        types=[type_doc],
    )
    store = RichStore(index=project_index)

    assert store.get("cs_balance") is proc
    assert store.get_of_kind("cs_balance", "subroutine") is proc
    assert store.get_of_kind("cs_balance", "type") is type_doc
    assert store.get_of_kind("cs_balance", "module") is None


def test_rich_store_type_type_collision_disambiguated_by_file():
    """Two DerivedTypeDoc named 'field' in different files are disambiguated by file param."""
    hru_type = DerivedTypeDoc(
        name="field",
        location=SourceLocation(path="hru_module.f90", line=41, end_line=46),
    )
    ru_type = DerivedTypeDoc(
        name="field",
        location=SourceLocation(path="ru_module.f90", line=25, end_line=30),
    )

    project_index = ProjectIndex(
        project_name="test",
        source_root=".",
        modules=[],
        procedures=[],
        types=[hru_type, ru_type],
    )
    store = RichStore(index=project_index)

    assert store.get_of_kind("field", "type", file="hru_module.f90") is hru_type
    assert store.get_of_kind("field", "type", file="ru_module.f90") is ru_type


def test_build_preserves_every_scanner_call_observation():
    """The scan-to-store path must not drop or reorder a single call site.

    This is the Phase 0 promise that the baseline's identity gate reports on,
    checked here against the scanner's own output rather than against a later
    copy of the already-resolved store.
    """
    from swatplus_reference.parser.schema_config import BuildConfig
    from swatplus_reference.parser.schema_fortran import FortranScanner

    scanned = RichStore(FortranScanner(BuildConfig(source_dir=FIXTURES)).scan())
    expected = scanned.call_observations()

    built = RichStore.build(FIXTURES)

    assert expected
    assert built.call_observations() == expected
    assert built.scan_call_identity == built.call_observation_identity()


@pytest.mark.parametrize("mutation", ["drop", "change_location"])
def test_build_pins_calls_before_outside_state_enrichment(monkeypatch, mutation):
    from swatplus_reference.parser import rich as rich_module
    from swatplus_reference.parser.schema_config import BuildConfig
    from swatplus_reference.parser.schema_fortran import FortranScanner

    scanned = RichStore(FortranScanner(BuildConfig(source_dir=FIXTURES)).scan())
    raw_identity = scanned.call_observation_identity()
    real_extract = rich_module.extract_outside_state_refs
    changed = []

    def corrupt_during_enrichment(procedure, *args):
        refs = real_extract(procedure, *args)
        if procedure.calls and not changed:
            if mutation == "drop":
                procedure.calls.pop()
            else:
                procedure.calls[0].location.line += 1
            changed.append(True)
        return refs

    monkeypatch.setattr(rich_module, "extract_outside_state_refs", corrupt_during_enrichment)
    built = RichStore.build(FIXTURES)

    assert changed
    assert built.scan_call_identity == raw_identity
    assert built.scan_call_identity != built.call_observation_identity()


def test_resolve_calls_rejects_a_resolution_that_drops_observations(monkeypatch):
    store = RichStore.build(FIXTURES)
    real = RichStore.call_observations
    seen = {"count": 0}

    def losing_a_call(self):
        rows = real(self)
        seen["count"] += 1
        # Stand in for a future resolution step that "tidies" the call list:
        # the invariant must fail loudly rather than silently shrinking the
        # portable export.
        return rows if seen["count"] == 1 else rows[:-1]

    monkeypatch.setattr(RichStore, "call_observations", losing_a_call)
    with pytest.raises(RuntimeError, match="changed source observations"):
        store.resolve_calls()


def test_call_observation_identity_ignores_resolution_but_tracks_source():
    store = RichStore.build(FIXTURES)
    identity = store.call_observation_identity()

    for procedure in store.index.procedures:
        for call in procedure.calls:
            call.resolved = not call.resolved
    assert store.call_observation_identity() == identity

    target = next(item for item in store.index.procedures if item.calls)
    target.calls[0].location.line += 1
    assert store.call_observation_identity() != identity
