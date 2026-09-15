"""Freeze the portable wire contracts and their loading paths.

See `tests/contracts/README.md` for what each fixture guarantees and how to
regenerate one when a contract change is intended.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from swatplus_reference.parser.rich import (
    RICH_EXPORT_SCHEMA,
    RICH_MODEL_VERSION,
    DEFAULT_ENGINE,
    SCANNER_ENGINE,
    parser_version,
    SNAPSHOT_FORMAT,
    SNAPSHOT_METADATA_KEY,
    RichStore,
)
from swatplus_reference.parser.schema_model import (
    DerivedTypeDoc,
    ProcedureDoc,
    ProjectIndex,
    SourceLocation,
)


FIXTURES = Path(__file__).parent / "fixtures"
CONTRACTS = Path(__file__).parent / "contracts"
V1 = CONTRACTS / "rich-v1.snapshot.json"
V2 = CONTRACTS / "rich-v2.snapshot.json"
V3 = CONTRACTS / "rich-v3.snapshot.json"
CONTRACT_COMMIT = "c" * 40
CONTRACT_SOURCE = {
    "profile": "contract",
    "repository": "https://example.test/swatplus",
    "requested_ref": "contract",
    "configured_commit": CONTRACT_COMMIT,
    "resolved_commit": CONTRACT_COMMIT,
}


def _calls(payload: dict) -> list[dict]:
    return [call for procedure in payload["procedures"] for call in procedure["calls"]]


def test_v3_export_matches_the_checked_in_contract(tmp_path):
    """A wire change must show up as a reviewed diff of the fixture."""

    rebuilt = tmp_path / "rich.json"
    RichStore.build(FIXTURES).save(rebuilt, provenance=CONTRACT_SOURCE)

    assert rebuilt.read_bytes().replace(b"\r\n", b"\n") == V3.read_bytes().replace(
        b"\r\n", b"\n"
    )


def test_v3_contract_declares_every_version_identifier():
    snapshot = json.loads(V3.read_text(encoding="utf-8"))["metadata"][
        SNAPSHOT_METADATA_KEY
    ]

    assert SNAPSHOT_FORMAT == 3
    assert RICH_EXPORT_SCHEMA == "swatplus-reference-rich-v3"
    assert RICH_MODEL_VERSION == "project-index-v2"
    # The identity names the engine that produced the snapshot. Since the
    # Phase 8 cutover that is fparser2; `scanner` keeps its own identity so a
    # cache built by one engine is never reused for the other.
    assert DEFAULT_ENGINE == "fparser2"
    assert parser_version(DEFAULT_ENGINE) == "fparser-ast-v1"
    assert parser_version("scanner") == "fortran-scanner-v6"
    assert snapshot["format"] == SNAPSHOT_FORMAT
    assert snapshot["export"] == RICH_EXPORT_SCHEMA
    assert snapshot["model"] == RICH_MODEL_VERSION
    assert snapshot["parser"] == parser_version(DEFAULT_ENGINE)
    assert snapshot["source"]["resolved_commit"] == CONTRACT_COMMIT


def test_v1_snapshot_still_loads_with_its_unfiltered_calls():
    """v1 carries candidates later contracts drop; loading must not lose them."""

    payload = json.loads(V1.read_text(encoding="utf-8"))
    assert payload["metadata"][SNAPSHOT_METADATA_KEY]["format"] == 1
    assert "export" not in payload["metadata"][SNAPSHOT_METADATA_KEY]
    unresolved = [
        call
        for call in _calls(payload)
        if call["kind"] == "function" and not call["resolved"]
    ]
    assert unresolved, "the v1 fixture must exercise the filtered-out candidates"

    store = RichStore.load(V1, expected_source_ref=CONTRACT_COMMIT)

    assert store.get("demo_calc") is not None
    assert store.get_of_kind("demo_state", "type", file="demo_module.f90") is not None
    loaded = [
        call
        for procedure in store.index.procedures
        for call in procedure.calls
        if call.kind == "function" and not call.resolved
    ]
    assert len(loaded) == len(unresolved)


def test_v2_snapshot_remains_readable():
    """The original v2 fixture stays frozen after v3 fields are introduced."""

    payload = json.loads(V2.read_text(encoding="utf-8"))
    snapshot = payload["metadata"][SNAPSHOT_METADATA_KEY]
    assert snapshot["format"] == 2
    assert snapshot["export"] == "swatplus-reference-rich-v2"
    assert "identity" not in payload["procedures"][0]
    store = RichStore.load(V2)
    assert store.get("demo_calc") is not None
    assert store.engine == SCANNER_ENGINE


def test_v1_converts_to_a_valid_but_incomplete_v3_snapshot(tmp_path):
    """The documented conversion path, including what it cannot recover.

    Re-saving a v1 snapshot produces a well-formed v3 envelope, but fields v1
    never carried stay empty: an assignment's ``target``/``expression`` were
    discarded by the v1 producer and cannot be invented from the payload. A
    complete v3 needs a re-scan of the pinned source, not a conversion.
    """

    converted = tmp_path / "converted.json"
    RichStore.load(V1).save(converted, provenance=CONTRACT_SOURCE)

    payload = json.loads(converted.read_text(encoding="utf-8"))
    snapshot = payload["metadata"][SNAPSHOT_METADATA_KEY]
    assert snapshot["format"] == SNAPSHOT_FORMAT
    assert snapshot["export"] == RICH_EXPORT_SCHEMA
    assert RichStore.load(converted).get("demo_calc") is not None

    converted_assignments = [
        assignment
        for procedure in payload["procedures"]
        for assignment in procedure["assignments"]
    ]
    assert converted_assignments, "the fixture must exercise assignments"
    assert all(item["target"] is None for item in converted_assignments)
    assert all(item["expression"] is None for item in converted_assignments)

    fresh = json.loads(V3.read_text(encoding="utf-8"))
    assert any(
        assignment["target"] is not None
        for procedure in fresh["procedures"]
        for assignment in procedure["assignments"]
    ), "a re-scan is what fills the fields a conversion cannot"


@pytest.mark.parametrize(
    "mutation,message",
    [
        ({"format": 99}, "supported formats"),
        ({"export": "swatplus-reference-rich-v99"}, "supported export schemas"),
        ({"export": None}, "names no export schema"),
        ({"format": 2}, "format 2 requires 'swatplus-reference-rich-v2'"),
    ],
)
def test_reader_refuses_an_unsupported_version(tmp_path, mutation, message):
    payload = json.loads(V3.read_text(encoding="utf-8"))
    snapshot = payload["metadata"][SNAPSHOT_METADATA_KEY]
    for key, value in mutation.items():
        if value is None:
            del snapshot[key]
        else:
            snapshot[key] = value
    unsupported = tmp_path / "unsupported.json"
    unsupported.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        RichStore.load(unsupported)


def test_format_one_is_still_accepted_without_an_export_schema(tmp_path):
    """Requiring the export identifier must not retroactively break v1."""

    payload = json.loads(V1.read_text(encoding="utf-8"))
    accepted = tmp_path / "v1.json"
    accepted.write_text(json.dumps(payload), encoding="utf-8")

    assert RichStore.load(accepted).get("demo_calc") is not None


def test_assignments_carry_their_two_sides_apart():
    """The structured fields exist so consumers stop re-parsing `raw`."""

    payload = json.loads(V3.read_text(encoding="utf-8"))
    by_name = {procedure["name"]: procedure for procedure in payload["procedures"]}
    subscripted = [
        assignment
        for assignment in by_name["demo_zero"]["assignments"]
        if assignment["target"] == "ds%flow"
    ]

    assert len(subscripted) == 1
    assignment = subscripted[0]
    assert assignment["target_root"] == "ds"
    assert assignment["expression"] == "0."
    # The originals keep their meaning and position for existing readers.
    assert assignment["kind"] == "assignment"
    assert assignment["summary"] == "Sets ds%flow"
    assert assignment["raw"].strip() == "ds%flow = 0."


def test_named_records_carry_a_stable_identity():
    """A bare name cannot address a record; identity includes kind and file."""

    payload = json.loads(V3.read_text(encoding="utf-8"))
    by_name = {item["name"]: item for item in payload["procedures"]}
    types = {item["name"]: item for item in payload["types"]}

    assert by_name["demo_calc"]["identity"] == "subroutine:demo_calc:demo_calc.f90"
    assert types["demo_state"]["identity"] == (
        "type:demo_state:demo_module.f90:demo_module"
    )
    # demo_zero lives in a different file from demo_calc, and the identity says so.
    assert by_name["demo_zero"]["identity"] == (
        "subroutine:demo_zero:demo_module.f90:demo_module"
    )

    every = [
        record["identity"]
        for key in ("modules", "programs", "procedures", "types")
        for record in payload[key]
    ]
    assert all(every), "every named record needs an identity"
    assert len(set(every)) == len(every), "identities must be unique"


def test_same_named_records_in_different_scopes_have_distinct_identities():
    location = SourceLocation("shared.f90", 1, 2)
    records = [
        ProcedureDoc("step", "subroutine", location, parent="host_a"),
        ProcedureDoc("step", "subroutine", location, parent="host_b"),
    ]
    types = [
        DerivedTypeDoc("state", location, module="module_a"),
        DerivedTypeDoc("state", location, module="module_b"),
    ]
    store = RichStore(ProjectIndex("fixture", ".", procedures=records, types=types))

    store.stamp_identities()

    identities = [item.identity for item in [*records, *types]]
    assert all(identities)
    assert len(set(identities)) == len(identities)


def test_identity_survives_a_v1_conversion(tmp_path):
    """Identity is derivable from what v1 already carried, so it is not lost."""

    converted = tmp_path / "converted.json"
    RichStore.load(V1).save(converted, provenance=CONTRACT_SOURCE)

    payload = json.loads(converted.read_text(encoding="utf-8"))
    identities = {item["name"]: item["identity"] for item in payload["procedures"]}
    assert identities["demo_calc"] == "subroutine:demo_calc:demo_calc.f90"
