from __future__ import annotations

import json
from pathlib import Path
from copy import deepcopy

import pytest
from jsonschema import Draft202012Validator, ValidationError

from swatplus_reference.docs.pages import Page
from swatplus_reference.parser.baseline import (
    BASELINE_FORMAT,
    _artifact,
    baseline_failures,
    build_parser_baseline,
)
from swatplus_reference.parser.documentation import parse_documentation
from swatplus_reference.parser.facts import FactStore, Symbol


FIXTURES = Path(__file__).parent / "fixtures"


def test_phase_zero_baseline_is_deterministic_and_complete(tmp_path):
    diagnostics = FactStore()
    store, rich = parse_documentation(
        FIXTURES, "a" * 40, diagnostics=diagnostics
    )
    docs = tmp_path / "docs_src" / "procedures"
    docs.mkdir(parents=True)
    page = Page(
        path=docs / "demo_calc.md",
        kind="procedure",
        symbol="demo_calc",
        status="filled",
        source_hash=store.get("demo_calc").source_hash,
    )
    page.save()

    artifact = tmp_path / "artifact.json"
    artifact.write_text("{}\n", encoding="utf-8")
    schema = tmp_path / "schema.json"
    schema.write_text('{"files": {}, "unresolved": []}\n', encoding="utf-8")
    regressions = tmp_path / "regression-cases.json"
    regressions.write_text(
        json.dumps(
            {
                "cases": [
                    {
                        "id": "fixture",
                        "file": "demo_calc.f90",
                        "symbol_key": "demo_calc",
                        "expected_symbol_keys": ["demo_calc"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    arguments = {
        "root": tmp_path,
        "source_dir": FIXTURES,
        "source": {
            "profile": "fixture",
            "repository": "https://example.test/swatplus",
            "requested_ref": "fixture",
            "configured_commit": "a" * 40,
            "resolved_commit": "a" * 40,
        },
        "store": store,
        "rich": rich,
        "pages": [page],
        "artifacts": {"artifact.json": artifact},
        "regression_cases": regressions,
        "schema_paths": {"base": schema},
    }

    first = build_parser_baseline(**arguments)
    second = build_parser_baseline(**arguments)

    assert first == second
    assert first["format"] == BASELINE_FORMAT
    assert first["calls"]["observations_before_resolution"] == first["calls"][
        "observations_after_resolution"
    ]
    assert first["calls"]["ambiguity_model_supported"] is True
    assert first["calls"]["ambiguous"] == 0
    assert first["facts"]["locations"]["count"] > 0
    assert first["documentation"]["grounding"]["errors"] == 0
    assert first["diagnostics"]["rich_projection_matches"] is True
    assert first["regression_cases"]["all_verified"] is True
    schema_contract = json.loads(
        (Path(__file__).parents[1] / "reports/parser-baseline/baseline.schema.json")
        .read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema_contract)
    validator.validate(first)
    invalid = deepcopy(first)
    invalid["calls"]["resolved"] = "not a number"
    with pytest.raises(ValidationError):
        validator.validate(invalid)
    invalid = deepcopy(first)
    del invalid["facts"]["source_hashes"]
    with pytest.raises(ValidationError):
        validator.validate(invalid)

    # This fixture has only one reviewed page, so missing pages must prevent
    # accepting it as a release baseline even though it reproduces exactly.
    assert "documentation has hard drift buckets" in baseline_failures(first)
    invalid = deepcopy(first)
    invalid["documentation"]["hash_mismatches"] = ["procedures/demo_calc.md"]
    invalid["diagnostics"]["rich_projection_matches"] = False
    invalid["regression_cases"]["all_verified"] = False
    failures = baseline_failures(invalid)
    assert "reviewed page source hashes changed" in failures
    assert "rich and projected parser diagnostics differ" in failures
    assert "a named source regression case failed" in failures


def test_artifact_hashes_ignore_only_checkout_line_endings(tmp_path):
    lf = tmp_path / "lf.json"
    crlf = tmp_path / "crlf.json"
    lf.write_bytes(b'{"value": 1}\n')
    crlf.write_bytes(b'{"value": 1}\r\n')
    assert _artifact(lf) == _artifact(crlf)
    crlf.write_bytes(b'{"value": 2}\r\n')
    assert _artifact(lf) != _artifact(crlf)


def test_span_comparison_matches_same_named_types_by_file():
    from swatplus_reference.parser.baseline import _thin_rich_comparisons
    from swatplus_reference.parser.facts import Symbol
    from swatplus_reference.parser.rich import RichStore
    from swatplus_reference.parser.schema_model import DerivedTypeDoc, ProjectIndex, SourceLocation

    thin = FactStore()
    thin.add(Symbol("type", "shared", "right.f90", 7, 29))
    rich = RichStore(ProjectIndex("fixture", ".", types=[
        DerivedTypeDoc("shared", SourceLocation("wrong.f90", 5, 13)),
        DerivedTypeDoc("shared", SourceLocation("right.f90", 7, 29)),
    ]))
    rows = _thin_rich_comparisons(thin, thin, rich)
    assert {"symbol_key": "shared", "field": "span", "thin": 23, "rich": 23} in rows


def test_baseline_cli_checks_snapshot_and_refuses_bad_hash_rebaseline(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from swatplus_reference import cli
    from swatplus_reference.provenance.records import SourceProvenance
    from swatplus_reference.source.config import Config
    from swatplus_reference.parser.fortran import parse_tree

    commit = "a" * 40
    cfg = Config(root=tmp_path, source_dir=FIXTURES.resolve(), source_ref=commit)
    source = SourceProvenance("fixture", "https://example.test/swatplus", "fixture", commit, commit)
    thin = parse_tree(FIXTURES, commit)
    store, _ = parse_documentation(FIXTURES, commit, diagnostics=thin)
    pages = []
    for symbol in store.symbols.values():
        if symbol.kind == "type":
            continue
        page = Page(
            path=cfg.abs_docs_dir / f"{symbol.name}.md", symbol=symbol.name,
            kind="module" if symbol.kind == "module" else "procedure",
            status="filled", source_hash=symbol.source_hash,
        )
        page.save()
        pages.append(page)
    (tmp_path / "README.md").write_text(
        f"- {len(pages):,} filled pages;\n- 0 grounding errors; and\n"
        "- 0 non-blocking identifier warnings.\n", encoding="utf-8"
    )
    report_dir = tmp_path / "reports/parser-baseline"
    report_dir.mkdir(parents=True)
    contract = Path(__file__).parents[1] / "reports/parser-baseline/baseline.schema.json"
    (report_dir / "baseline.schema.json").write_bytes(contract.read_bytes())
    (report_dir / "regression-cases.json").write_text(
        '{"cases": [{"id": "calc", "file": "demo_calc.f90", "symbol_key": "demo_calc",'
        ' "expected_symbol_keys": ["demo_calc"]}]}',
        encoding="utf-8",
    )
    tracked = tmp_path / "snapshots/rich/fixture.rich.json"
    tracked.parent.mkdir(parents=True)
    report_path = report_dir / "fixture.json"
    monkeypatch.setattr(cli, "activate_docs_source", lambda _: source)
    monkeypatch.setattr(cli, "_baseline_paths", lambda *args: (report_path, tracked, {}, {}))

    assert cli.cmd_baseline(cfg, SimpleNamespace(write=True)) == 0
    assert cli.cmd_baseline(cfg, SimpleNamespace(write=False)) == 0
    original = tracked.read_bytes()
    tracked.write_bytes(original + b" ")
    assert cli.cmd_baseline(cfg, SimpleNamespace(write=False)) == 1
    assert tracked.read_bytes() == original + b" "

    pages[0].source_hash = "old-hash"
    pages[0].save()
    original_report = report_path.read_bytes()
    assert cli.cmd_baseline(cfg, SimpleNamespace(write=True)) == 1
    assert report_path.read_bytes() == original_report
    assert tracked.read_bytes() == original + b" "


def _cases(tmp_path, *cases):
    path = tmp_path / "regression-cases.json"
    path.write_text(json.dumps({"cases": list(cases)}), encoding="utf-8")
    return path


def test_regression_case_that_asserts_nothing_is_not_verified(tmp_path):
    from swatplus_reference.parser.baseline import _regression_summary

    store = FactStore()
    store.add(Symbol("subroutine", "demo_calc", "demo_calc.f90", 1, 20))

    inert = _regression_summary(
        _cases(tmp_path, {"id": "inert", "file": "demo_calc.f90", "symbol_key": "demo_calc"}),
        FIXTURES, store, [],
    )
    assert inert["checks"][0]["asserts_behavior"] is False
    assert inert["all_verified"] is False

    asserting = _regression_summary(
        _cases(tmp_path, {
            "id": "real", "file": "demo_calc.f90", "symbol_key": "demo_calc",
            "expected_symbol_keys": ["demo_calc"],
        }),
        FIXTURES, store, [],
    )
    assert asserting["all_verified"] is True


def test_regression_case_expectations_fail_when_the_behavior_regresses(tmp_path):
    from swatplus_reference.parser.baseline import _regression_summary

    store = FactStore()
    store.add(Symbol("subroutine", "salt_balance", "salt_module.f90", 1, 20))
    store.add(Symbol("module", "hub", "hub.f90", 1, 20))
    for index in range(3):
        store.add(Symbol("module", f"user_{index}", "u.f90", 1, 2, depends_on=["hub"]))

    # The collision case fails while the qualified type key is absent, which is
    # exactly the regression that kind-plus-file matching corrected.
    summary = _regression_summary(
        _cases(tmp_path, {
            "id": "collision", "file": "salt_module.f90", "symbol_key": "salt_balance",
            "expected_symbol_keys": ["salt_balance", "type::salt_balance"],
        }),
        FIXTURES, store, [],
    )
    assert summary["checks"][0]["symbol_keys_match"] is False
    assert summary["all_verified"] is False

    hub = _regression_summary(
        _cases(tmp_path, {
            "id": "hub", "file": "hub.f90", "symbol_key": "hub",
            "expected_min_dependents": 3,
        }),
        FIXTURES, store, [],
    )
    assert hub["checks"][0]["dependents_match"] is True

    trimmed = _regression_summary(
        _cases(tmp_path, {
            "id": "hub", "file": "hub.f90", "symbol_key": "hub",
            "expected_min_dependents": 4,
        }),
        FIXTURES, store, [],
    )
    assert trimmed["checks"][0]["dependents_match"] is False


def test_call_identity_gate_detects_changed_observations():
    payload = {
        "calls": {
            "observations_before_resolution": 3,
            "observations_after_resolution": 3,
            "identity_at_scan": "a" * 64,
            "identity_before_resolution": "a" * 64,
            "identity_after_resolution": "a" * 64,
        },
        "diagnostics": {"rich_projection_matches": True},
        "regression_cases": {"all_verified": True},
        "documentation": {
            "hash_mismatches": [],
            "page_status": {"stale": 0, "todo": 0, "orphaned": 0, "missing": 0},
            "grounding": {"errors": 0},
        },
        "schemas": {},
        "artifacts": {},
    }
    assert baseline_failures(payload) == []

    # Equal counts but different content: the count-only gate could not see this.
    drifted = deepcopy(payload)
    drifted["calls"]["identity_after_resolution"] = "b" * 64
    failures = baseline_failures(drifted)
    assert "call observations changed during resolution" in failures
    assert "call observation count changed during resolution" not in failures

    scanned = deepcopy(payload)
    scanned["calls"]["identity_at_scan"] = "c" * 64
    assert (
        "call observations changed between the source scan and the baseline"
        in baseline_failures(scanned)
    )

    # A store loaded from a snapshot has no scan to pin, which must not fail.
    loaded = deepcopy(payload)
    loaded["calls"]["identity_at_scan"] = None
    assert baseline_failures(loaded) == []


def test_contract_drift_names_the_dependency_that_moved(tmp_path):
    from swatplus_reference.parser.baseline import contract_drift

    tracked = tmp_path / "baseline.json"
    tracked.write_text(
        json.dumps({"contracts": {"fparser_version": "0.2.4", "snapshot_format": 2}}),
        encoding="utf-8",
    )
    candidate = {"contracts": {"fparser_version": "0.2.5", "snapshot_format": 2}}

    assert contract_drift(tracked, candidate) == ["fparser_version: '0.2.4' -> '0.2.5'"]
    assert contract_drift(tracked, {"contracts": {"fparser_version": "0.2.4", "snapshot_format": 2}}) == []
    assert contract_drift(tmp_path / "absent.json", candidate) == []


def test_baseline_cli_reports_a_schema_breach_as_a_gate_failure(tmp_path, monkeypatch, capsys):
    """A broken contract must read like a gate result, not an internal error."""
    from types import SimpleNamespace
    from swatplus_reference import cli
    from swatplus_reference.provenance.records import SourceProvenance
    from swatplus_reference.source.config import Config

    commit = "a" * 40
    cfg = Config(root=tmp_path, source_dir=FIXTURES.resolve(), source_ref=commit)
    source = SourceProvenance("fixture", "https://example.test/swatplus", "fixture", commit, commit)
    report_dir = tmp_path / "reports/parser-baseline"
    report_dir.mkdir(parents=True)
    (report_dir / "regression-cases.json").write_text('{"cases": []}', encoding="utf-8")
    (tmp_path / "README.md").write_text("", encoding="utf-8")
    tracked = tmp_path / "snapshots/rich/fixture.rich.json"
    tracked.parent.mkdir(parents=True)
    monkeypatch.setattr(cli, "activate_docs_source", lambda _: source)
    monkeypatch.setattr(
        cli, "_baseline_paths", lambda *args: (report_dir / "fixture.json", tracked, {}, {})
    )

    # No schema on disk at all.
    assert cli.cmd_baseline(cfg, SimpleNamespace(write=False)) == 1
    assert "Phase 0 gate failed: cannot read" in capsys.readouterr().out

    (report_dir / "baseline.schema.json").write_text("{ not json", encoding="utf-8")
    assert cli.cmd_baseline(cfg, SimpleNamespace(write=False)) == 1
    assert "is not valid JSON" in capsys.readouterr().out

    (report_dir / "baseline.schema.json").write_text(
        json.dumps({"type": "object", "required": ["absent_key"]}), encoding="utf-8"
    )
    assert cli.cmd_baseline(cfg, SimpleNamespace(write=False)) == 1
    out = capsys.readouterr().out
    assert "baseline does not match its schema" in out
    assert "absent_key" in out


@pytest.mark.parametrize("write", [False, True])
@pytest.mark.parametrize("breach", [
    "missing_calls", "missing_documentation", "wrong_calls_type",
    "wrong_status_type", "wrong_root_type",
])
def test_invalid_baseline_stops_before_invariants_or_publication(
    tmp_path, monkeypatch, capsys, write, breach
):
    from types import SimpleNamespace
    from swatplus_reference import cli
    from swatplus_reference.parser import baseline as baseline_module
    from swatplus_reference.provenance.records import SourceProvenance
    from swatplus_reference.source.config import Config

    reference_dir = Path(__file__).parents[1] / "reports/parser-baseline"
    payload = json.loads((reference_dir / "main-cb442f7c05fc.json").read_text(encoding="utf-8"))
    if breach == "missing_calls":
        del payload["calls"]
    elif breach == "missing_documentation":
        del payload["documentation"]
    elif breach == "wrong_calls_type":
        payload["calls"] = None
    elif breach == "wrong_status_type":
        payload["documentation"]["page_status"] = []
    else:
        payload = []

    commit = "a" * 40
    cfg = Config(root=tmp_path, source_dir=FIXTURES.resolve(), source_ref=commit)
    source = SourceProvenance("fixture", "https://example.test/swatplus", "fixture", commit, commit)
    report_dir = tmp_path / "reports/parser-baseline"
    report_dir.mkdir(parents=True)
    (report_dir / "baseline.schema.json").write_bytes((reference_dir / "baseline.schema.json").read_bytes())
    report = report_dir / "fixture.json"
    snapshot = tmp_path / "snapshots/rich/fixture.rich.json"
    snapshot.parent.mkdir(parents=True)
    reviewed = {
        report: b'{"reviewed": true}\n',
        snapshot: b"reviewed snapshot\n",
        snapshot.with_suffix(".provenance.json"): b"reviewed provenance\n",
        report_dir / "PERFORMANCE.md": b"reviewed performance\n",
    }
    for path, content in reviewed.items():
        path.write_bytes(content)
    monkeypatch.setattr(cli, "activate_docs_source", lambda _: source)
    monkeypatch.setattr(cli, "_baseline_paths", lambda *args: (report, snapshot, {}, {}))
    monkeypatch.setattr(baseline_module, "build_parser_baseline", lambda **kwargs: payload)
    monkeypatch.setattr(
        baseline_module, "baseline_failures",
        lambda _: pytest.fail("invariants must not inspect an invalid baseline"),
    )
    # README is deliberately absent: its checks must also wait for validation.
    assert cli.cmd_baseline(cfg, SimpleNamespace(write=write)) == 1
    assert "Phase 0 gate failed: baseline does not match its schema" in capsys.readouterr().out
    assert all(path.read_bytes() == content for path, content in reviewed.items())


def test_snapshot_size_budget_is_enforced_not_just_documented():
    """The Phase 1 storage decision is a gate, so it has to be able to fail."""
    from swatplus_reference.parser.baseline import (
        SNAPSHOT_BYTE_BUDGET,
        baseline_failures,
    )

    tracked = json.loads(
        (Path(__file__).parents[1] / "reports/parser-baseline/main-cb442f7c05fc.json")
        .read_text(encoding="utf-8")
    )
    assert not baseline_failures(tracked)

    snapshot_key = next(
        key for key in tracked["artifacts"] if key.endswith(".rich.json")
    )
    assert tracked["artifacts"][snapshot_key]["bytes"] <= SNAPSHOT_BYTE_BUDGET

    over = deepcopy(tracked)
    over["artifacts"][snapshot_key]["bytes"] = SNAPSHOT_BYTE_BUDGET + 1
    failures = baseline_failures(over)
    assert any("over the" in failure and snapshot_key in failure for failure in failures)
