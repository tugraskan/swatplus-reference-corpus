"""Deterministic Phase 0 baseline for the parser migration."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import asdict, fields, is_dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Iterable

from ..docs.grounding import check_all
from ..docs.pages import Page
from ..docs.staleness import (
    MAX_DATAFLOW_FANOUT,
    MAX_WRITERS_FOR_DATAFLOW,
    compute_status,
)
from .documentation import RICH_DOCUMENTATION_PRODUCER
from .facts import FactStore, composite_source_hash
from .fortran import fparser_version
from .rich import (
    FPARSER_DIAGNOSTICS_METADATA_KEY,
    RICH_EXPORT_SCHEMA,
    RICH_MODEL_VERSION,
    parser_version,
    SNAPSHOT_FORMAT,
    RichStore,
)
from .schema_model import SourceLocation, record_identity, record_scope


BASELINE_FORMAT = "swatplus-reference-parser-baseline-v1"

# Reviewed in Phase 1; see reports/parser-baseline/BUDGETS.md for the evidence.
# The snapshot stays plain JSON because git already absorbs it -- three versions
# of it cost under 6 MiB of pack -- so this is a tripwire for a model change
# that blows the shape up, not a storage workaround.
SNAPSHOT_BYTE_BUDGET = 64 * 1024 * 1024


def baseline_failures(payload: dict[str, Any]) -> list[str]:
    """Do not accept a reproducible baseline that violates a Phase 0 gate."""
    failures = []
    calls = payload["calls"]
    if calls["observations_before_resolution"] != calls["observations_after_resolution"]:
        failures.append("call observation count changed during resolution")
    if calls["identity_before_resolution"] != calls["identity_after_resolution"]:
        failures.append("call observations changed during resolution")
    at_scan = calls["identity_at_scan"]
    if at_scan is not None and at_scan != calls["identity_after_resolution"]:
        failures.append("call observations changed between the source scan and the baseline")
    if not payload["diagnostics"]["rich_projection_matches"]:
        failures.append("rich and projected parser diagnostics differ")
    if not payload["regression_cases"]["all_verified"]:
        failures.append("a named source regression case failed")
    docs = payload["documentation"]
    if docs["hash_mismatches"]:
        failures.append("reviewed page source hashes changed")
    if any(docs["page_status"][bucket] for bucket in ("stale", "todo", "orphaned", "missing")):
        failures.append("documentation has hard drift buckets")
    if docs["grounding"]["errors"]:
        failures.append("documentation has grounding errors")
    if any(counts.get("unresolved", 0) for counts in payload["schemas"].values()):
        failures.append("schema contains unresolved files")
    for name, artifact in sorted(payload["artifacts"].items()):
        if name.endswith(".rich.json") and artifact["bytes"] > SNAPSHOT_BYTE_BUDGET:
            failures.append(
                f"{name} is {artifact['bytes'] / 1024 / 1024:.1f} MiB, over the "
                f"{SNAPSHOT_BYTE_BUDGET / 1024 / 1024:.0f} MiB snapshot budget"
            )
    return failures


def contract_drift(tracked_report: Path, candidate: dict[str, Any]) -> list[str]:
    """Name the toolchain contracts that moved under a byte comparison.

    A dependency upgrade changes recorded versions and error text throughout the
    tracked artifacts. Reporting the specific contract keeps that failure from
    looking like a parser regression.
    """
    try:
        previous = json.loads(tracked_report.read_text(encoding="utf-8"))["contracts"]
    except (OSError, ValueError, KeyError):
        return []
    current = candidate["contracts"]
    return [
        f"{key}: {previous.get(key, 'absent')!r} -> {current.get(key, 'absent')!r}"
        for key in sorted(set(previous) | set(current))
        if previous.get(key) != current.get(key)
    ]


def dumps_baseline(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def normalized_bytes(path: Path) -> bytes:
    """Hash tracked text as Git stores it, independent of checkout EOLs."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def peak_process_memory_bytes() -> int:
    """Peak resident process memory at the end of parsing, without tracing."""
    import sys

    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        class Counters(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                *[(name, ctypes.c_size_t) for name in (
                    "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                    "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
                    "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage",
                )],
            ]

        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [
            wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD,
        ]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        if not psapi.GetProcessMemoryInfo(
            kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        return counters.PeakWorkingSetSize
    import resource

    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(peak if sys.platform == "darwin" else peak * 1024)


def _canonical(row: Any) -> str:
    return json.dumps(row, sort_keys=True, separators=(",", ":"))


def _category(rows: Iterable[Any]) -> dict[str, Any]:
    ordered = sorted((_canonical(row) for row in rows))
    body = "\n".join(ordered).encode("utf-8")
    return {
        "count": len(ordered),
        "identity_sha256": hashlib.sha256(body).hexdigest(),
    }


def _location(location: SourceLocation | None) -> dict[str, Any] | None:
    if location is None:
        return None
    return {
        "path": location.path,
        "line": location.line,
        "end_line": location.end_line,
    }


def _holder(
    kind: str,
    name: str,
    location: SourceLocation,
    module: str | None = None,
    parent: str | None = None,
) -> str:
    # The same formula the exported records carry, so a baseline owner string
    # and a record's `identity` are joinable rather than merely similar.
    return record_identity(kind, name, location.path, record_scope(module, parent))


def _all_locations(value: Any, owner: str = "project") -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, SourceLocation):
        rows.append({"owner": owner, **(_location(value) or {})})
    elif is_dataclass(value):
        for item in fields(value):
            if item.name == "metadata":
                continue
            rows.extend(_all_locations(getattr(value, item.name), f"{owner}.{item.name}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            rows.extend(_all_locations(item, f"{owner}[{index}]"))
    elif isinstance(value, dict):
        for key in sorted(value, key=str):
            rows.extend(_all_locations(value[key], f"{owner}.{key}"))
    return rows


def _artifact(path: Path) -> dict[str, Any]:
    content = normalized_bytes(path)
    return {
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def _schema_counts(path: Path) -> dict[str, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        key: len(value)
        for key, value in sorted(payload.items())
        if isinstance(value, (dict, list))
    }


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "unavailable"


def _fanout(rows: Iterable[tuple[str, str]]) -> dict[str, Any]:
    targets: dict[str, set[str]] = defaultdict(set)
    for source, target in rows:
        targets[source].add(target)
    counts = {source: len(items) for source, items in sorted(targets.items())}
    maximum = max(counts.values(), default=0)
    return {
        "sources": len(counts),
        "edges": sum(counts.values()),
        "maximum": maximum,
        "maximum_sources": sorted(
            source for source, count in counts.items() if count == maximum
        ),
        "by_source": counts,
        "identity_sha256": _category(
            (source, target)
            for source, targets_for_source in targets.items()
            for target in targets_for_source
        )["identity_sha256"],
    }


def _graph_baseline(store: FactStore, pages: list[Page]) -> dict[str, Any]:
    call_edges = {
        (symbol.name, target)
        for symbol in store.symbols.values()
        for target in symbol.calls
    }
    dependency_edges = {
        (dependency, symbol.name)
        for symbol in store.symbols.values()
        for dependency in symbol.depends_on
        if dependency != symbol.name
    }

    readers: dict[str, set[str]] = defaultdict(set)
    writers: dict[str, set[str]] = defaultdict(set)
    for symbol in store.symbols.values():
        for variable in symbol.reads:
            readers[variable].add(symbol.name)
        for variable in symbol.writes:
            writers[variable].add(symbol.name)

    candidate_by_writer: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for variable, variable_writers in writers.items():
        if len(variable_writers) > MAX_WRITERS_FOR_DATAFLOW:
            continue
        for writer in variable_writers:
            for reader in readers.get(variable, set()):
                if reader != writer:
                    candidate_by_writer[writer].add((reader, variable))
    applied = {
        (writer, reader, variable)
        for writer, candidates in candidate_by_writer.items()
        if len({reader for reader, _ in candidates}) <= MAX_DATAFLOW_FANOUT
        for reader, variable in candidates
    }
    candidates = {
        (writer, reader, variable)
        for writer, writer_candidates in candidate_by_writer.items()
        for reader, variable in writer_candidates
    }
    suppressed = sorted(
        writer
        for writer, writer_candidates in candidate_by_writer.items()
        if len({reader for reader, _ in writer_candidates}) > MAX_DATAFLOW_FANOUT
    )
    documented = {page.symbol.lower() for page in pages if page.symbol}
    return {
        "call": _fanout(call_edges),
        "declared_dependency": {
            **_fanout(dependency_edges),
            "fanout_cap": None,
            "documented_targets": _fanout(
                (source, target) for source, target in dependency_edges
                if target in documented
            ),
        },
        "heuristic_dataflow": {
            "candidate_edges": len(candidates),
            "candidate_identity_sha256": _category(candidates)["identity_sha256"],
            "applied_edges": len(applied),
            "applied_identity_sha256": _category(applied)["identity_sha256"],
            "fanout_cap": MAX_DATAFLOW_FANOUT,
            "max_writers": MAX_WRITERS_FOR_DATAFLOW,
            "suppressed_sources": suppressed,
            "candidate_fanout": _fanout((s, t) for s, t, _ in candidates),
            "applied_fanout": _fanout((s, t) for s, t, _ in applied),
            "documented_targets": _fanout(
                (s, t) for s, t, _ in applied if t in documented
            ),
        },
    }


def _thin_rich_comparisons(thin: FactStore, store: FactStore, rich: RichStore) -> list[dict]:
    rows = []
    for key in sorted(thin.symbols.keys() & store.symbols.keys()):
        left = thin.symbols[key]
        right = rich.get_of_kind(left.name, left.kind, file=left.file)
        if right is None:
            continue
        comparisons = {
            "span": (left.end_line - left.start_line + 1,
                     (right.location.end_line or right.location.line) - right.location.line + 1),
            "use_count": (len(left.uses), len(getattr(right, "uses", []))),
        }
        if hasattr(right, "args"):
            comparisons["arg_count"] = (len(left.args), len(right.args))
        for field, (thin_value, rich_value) in sorted(comparisons.items()):
            rows.append({"symbol_key": key, "field": field,
                         "thin": thin_value, "rich": rich_value})
    return rows


def _regression_summary(
    path: Path, source_dir: Path, store: FactStore, comparisons: list[dict]
) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    dependents: dict[str, set[str]] = defaultdict(set)
    for symbol in store.symbols.values():
        for dependency in symbol.depends_on:
            if dependency != symbol.name:
                dependents[dependency.lower()].add(symbol.name.lower())
    checks = []
    for case in cases:
        source_exists = (source_dir / case["file"]).is_file()
        symbol_key = case.get("symbol_key")
        symbol_exists = not symbol_key or symbol_key.lower() in store.symbols
        expected_fallback = bool(case.get("expected_fparser_fallback"))
        fallback_matches = (
            case["file"] in store.fallback_files if expected_fallback else True
        )
        # A file whose signed operand is parenthesised for the parser must both
        # stay out of the fallback set and keep reporting the rewrite. Asserting
        # only "no longer falls back" would pass just as well if the rewrite
        # were dropped and the file silently stopped being parsed at all.
        expected_normalized = case.get("expected_normalized_lines")
        normalized_matches = expected_normalized is None or (
            store.normalized_files.get(case["file"]) == expected_normalized
            and case["file"] not in store.fallback_files
        )
        expectation = case.get("comparison")
        comparison_matches = expectation is None or {
            "symbol_key": symbol_key, **expectation
        } in comparisons
        # A case that asserts nothing beyond "the file is still there" cannot
        # fail when the behavior it names regresses, so every case carries at
        # least one of these expectations.
        expected_keys = case.get("expected_symbol_keys") or []
        symbol_keys_match = all(key.lower() in store.symbols for key in expected_keys)
        minimum_dependents = case.get("expected_min_dependents")
        dependents_match = minimum_dependents is None or len(
            dependents[(symbol_key or "").lower()]
        ) >= minimum_dependents
        checks.append(
            {
                "id": case["id"],
                "source_exists": source_exists,
                "symbol_exists": symbol_exists,
                "fallback_matches": fallback_matches,
                "normalized_matches": normalized_matches,
                "comparison_matches": comparison_matches,
                "symbol_keys_match": symbol_keys_match,
                "dependents_match": dependents_match,
                "asserts_behavior": bool(
                    expectation
                    or expected_fallback
                    or expected_normalized is not None
                    or expected_keys
                    or minimum_dependents is not None
                ),
            }
        )
    return {
        "count": len(cases),
        "identity_sha256": _category(cases)["identity_sha256"],
        "all_verified": all(all(value for key, value in row.items() if key != "id") for row in checks),
        "checks": checks,
    }


def build_parser_baseline(
    *,
    root: Path,
    source_dir: Path,
    source: dict[str, str],
    store: FactStore,
    rich: RichStore,
    pages: list[Page],
    artifacts: dict[str, Path],
    regression_cases: Path,
    schema_paths: dict[str, Path],
    thin: FactStore | None = None,
) -> dict[str, Any]:
    """Build the normalized, byte-stable Phase 0 baseline."""

    observations_before = len(rich.call_observations())
    identity_before = rich.call_observation_identity()
    rich.resolve_calls()
    identity_after = rich.call_observation_identity()
    index = rich.index
    modules = [
        ("module", item.name, _location(item.location)) for item in index.modules
    ]
    programs = [
        ("program", item.name, _location(item.location)) for item in index.programs
    ]
    procedures = [
        (item.kind, item.name, _location(item.location), item.module, item.parent)
        for item in index.procedures
    ]
    derived_types = [
        ("type", item.name, _location(item.location), item.module)
        for item in index.types
    ]

    source_docs = []
    variables = []
    arguments = []
    uses = []
    call_observations = []
    resolved_call_edges = []
    reverse_call_edges = []
    assignments = []
    control_steps = []
    select_cases = []
    io_operations = []
    review_flags = []

    holders = [
        *(('module', item) for item in index.modules),
        *(('program', item) for item in index.programs),
        *((item.kind, item) for item in index.procedures),
        *(('type', item) for item in index.types),
    ]
    for kind, item in holders:
        owner = _holder(
            kind,
            item.name,
            item.location,
            getattr(item, "module", None),
            getattr(item, "parent", None),
        )
        if getattr(item, "doc", ""):
            source_docs.append((owner, item.doc))
        for variable in getattr(item, "variables", []):
            variables.append(
                (owner, asdict(variable))
            )
        for component in getattr(item, "components", []):
            variables.append(
                (owner, asdict(component))
            )
        for position, argument in enumerate(getattr(item, "args", [])):
            arguments.append((owner, position, argument))
        for use in getattr(item, "uses", []):
            uses.append(
                (owner, use.module, use.only, use.intrinsic, _location(use.location))
            )
        for call in getattr(item, "calls", []):
            observation = (
                owner,
                call.name.lower(),
                call.kind,
                call.raw,
                _location(call.location),
                call.resolved,
            )
            call_observations.append(observation)
            if call.resolved and call.resolved_target:
                resolved_call_edges.append((owner, call.resolved_target))
                reverse_call_edges.append((call.resolved_target, owner))
        for step in getattr(item, "assignments", []):
            assignments.append(
                (
                    owner,
                    step.kind,
                    step.summary,
                    step.raw,
                    _location(step.location),
                    step.target,
                    step.target_root,
                    step.expression,
                )
            )
        for step in getattr(item, "control_steps", []):
            control_steps.append(
                (
                    owner,
                    step.kind,
                    step.summary,
                    step.raw,
                    _location(step.location),
                    step.depth,
                    step.block_id,
                    step.parent_id,
                    step.branch_of,
                    step.end_line,
                )
            )
        for select in getattr(item, "select_cases", []):
            select_cases.append(
                (owner, select.subject, select.cases, _location(select.location))
            )
        for operation in getattr(item, "io", []):
            io_operations.append(
                (
                    owner,
                    operation.kind,
                    operation.unit,
                    operation.file_expr,
                    operation.file_resolved,
                    operation.fields,
                    operation.condition,
                    operation.raw,
                    _location(operation.location),
                )
            )
        for flag in getattr(item, "review_flags", []):
            review_flags.append(
                (owner, flag.code, flag.severity, flag.message, _location(flag.location))
            )
    for owner, flags in [
        ("project", index.review_flags),
        *((f"io:{item.key}", item.review_flags) for item in index.io_files),
        *((f"output:{item.key}", item.review_flags) for item in index.output_families),
    ]:
        review_flags.extend((owner, asdict(flag)) for flag in flags)

    outside_state = []
    for owner, records in sorted(
        (index.metadata or {}).get("swatplus_reference_outside_state_refs", {}).items()
    ):
        for record in records:
            outside_state.append((owner, record))

    dataflow_reads = [
        (key, variable)
        for key, symbol in sorted(store.symbols.items())
        for variable in symbol.reads
    ]
    dataflow_writes = [
        (key, variable)
        for key, symbol in sorted(store.symbols.items())
        for variable in symbol.writes
    ]
    dependencies = [
        (key, dependency)
        for key, symbol in sorted(store.symbols.items())
        for dependency in symbol.depends_on
    ]
    source_hashes = [
        (
            key,
            symbol.kind,
            symbol.name,
            symbol.file,
            symbol.start_line,
            symbol.end_line,
            symbol.source_hash,
        )
        for key, symbol in sorted(store.symbols.items())
    ]
    collisions = [
        (
            name,
            sorted(
                (
                    type(item).__name__,
                    item.location.path,
                    item.location.line,
                )
                for item in records
            ),
        )
        for name, records in sorted(rich.records_by_name.items())
        if len(records) > 1
    ]
    diagnostics = [
        (path, store.parse_errors.get(path, ""), path in store.fallback_files)
        for path in sorted(set(store.parse_errors) | set(store.fallback_files))
    ]

    io_files = [
        (item.key, item.display_name, item.procedures)
        for item in index.io_files
    ]
    output_families = [
        (item.key, item.display_name, item.base, item.opened_by, item.written_by)
        for item in index.output_families
    ]
    output_files = [
        (
            family.key,
            item.name,
            item.frequency,
            item.fmt,
            item.unit,
            _location(item.open_location),
            item.open_condition,
        )
        for family in index.output_families
        for item in family.files
    ]

    facts = {
        "arguments": _category(arguments),
        "assignments": _category(assignments),
        "call_observations": _category(call_observations),
        "control_steps": _category(control_steps),
        "dataflow_reads": _category(dataflow_reads),
        "dataflow_writes": _category(dataflow_writes),
        "declared_dependencies": _category(dependencies),
        "derived_types": _category(derived_types),
        "io_files": _category(io_files),
        "io_operations": _category(io_operations),
        "locations": _category(_all_locations(index)),
        "modules": _category(modules),
        "name_collisions": _category(collisions),
        "outside_state_refs": _category(outside_state),
        "output_families": _category(output_families),
        "output_files": _category(output_files),
        "parser_diagnostics": _category(diagnostics),
        "procedures": _category(procedures),
        "programs": _category(programs),
        "resolved_call_edges": _category(set(resolved_call_edges)),
        "reverse_call_edges": _category(set(reverse_call_edges)),
        "review_flags": _category(review_flags),
        "select_cases": _category(select_cases),
        "source_docs": _category(source_docs),
        "source_files": _category(
            {**asdict(item), **_artifact(source_dir / item.path)} for item in index.files
        ),
        "source_hashes": _category(source_hashes),
        "variables_and_components": _category(variables),
        "uses": _category(uses),
        "call_paths": _category(
            (item.identity, path)
            for item in index.procedures
            for path in item.call_paths
        ),
        "locals": _category(
            (key, asdict(local)) for key, symbol in store.symbols.items()
            for local in symbol.locals
        ),
        "select_case_labels": _category(
            (owner, subject, label, location)
            for owner, subject, labels, location in select_cases for label in labels
        ),
    }

    calls = [call for _, item in holders for call in getattr(item, "calls", [])]
    repeated_groups = Counter(
        (owner, call.name.lower(), call.kind)
        for kind, item in holders
        for owner in [
            _holder(
                kind,
                item.name,
                item.location,
                getattr(item, "module", None),
                getattr(item, "parent", None),
            )
        ]
        for call in getattr(item, "calls", [])
    )
    repeated_sites = sum(count - 1 for count in repeated_groups.values() if count > 1)
    exported_calls = [
        call for call in calls if call.kind != "function" or call.resolved
    ]

    status = compute_status(store, pages)
    findings = check_all(store, pages)
    status_counts = {
        "affected": len(status.affected),
        "filled": len(status.filled),
        "missing": len(status.missing),
        "orphaned": len(status.orphaned),
        "stale": len(status.stale),
        "todo": len(status.todo),
    }
    page_rows = [
        (
            page.path.relative_to(root).as_posix(),
            page.kind,
            page.symbol,
            page.source_symbols,
            page.status,
            page.source_hash,
        )
        for page in pages
    ]

    rich_diagnostics = (index.metadata or {}).get(
        FPARSER_DIAGNOSTICS_METADATA_KEY, {}
    )
    comparisons = _thin_rich_comparisons(thin, store, rich) if thin is not None else []
    disagreements = [row for row in comparisons if row["thin"] != row["rich"]]
    page_hashes = {}
    for page in pages:
        if not page.source_hash:
            continue
        symbol = store.get(page.symbol) if page.symbol else None
        current = symbol.source_hash if symbol else composite_source_hash(store, page.source_symbols)
        page_hashes[page.path.relative_to(root).as_posix()] = {
            "recorded": page.source_hash, "current": current,
        }
    return {
        "format": BASELINE_FORMAT,
        "source": source,
        "contracts": {
            "documentation_producer": RICH_DOCUMENTATION_PRODUCER,
            "fparser_version": _package_version("fparser"),
            "rich_export": RICH_EXPORT_SCHEMA,
            "rich_model": RICH_MODEL_VERSION,
            # The engine that produced this store, not a fixed constant:
            # the baseline has to say which parser it is a baseline of.
            "rich_parser": parser_version(rich.engine),
            "snapshot_format": SNAPSHOT_FORMAT,
        },
        "facts": facts,
        "calls": {
            "observations_before_resolution": observations_before,
            "observations_after_resolution": len(calls),
            # Identities, not counts: resolution cannot change a list length, so
            # only the full observation tuples can show that it left the
            # scanner's source evidence alone.
            "identity_at_scan": rich.scan_call_identity,
            "identity_before_resolution": identity_before,
            "identity_after_resolution": identity_after,
            "resolved": sum(call.resolved for call in calls),
            "unresolved_explicit_subroutine": sum(
                call.kind == "subroutine" and not call.resolved for call in calls
            ),
            "unresolved_function_candidates": sum(
                call.kind == "function" and not call.resolved for call in calls
            ),
            "ambiguous": sum(
                len(call.resolution_candidates) > 1 for call in calls
            ),
            "ambiguity_model_supported": True,
            "repeated_sites": repeated_sites,
            "portable_exported": len(exported_calls),
        },
        "graphs": _graph_baseline(store, pages),
        "documentation": {
            "pages": len(pages),
            "hashed_pages": sum(bool(page.source_hash) for page in pages),
            "page_kinds": dict(sorted(Counter(page.kind for page in pages).items())),
            "page_status": status_counts,
            "page_identity_sha256": _category(page_rows)["identity_sha256"],
            "page_hashes": page_hashes,
            "hash_mismatches": sorted(
                path for path, hashes in page_hashes.items()
                if hashes["recorded"] != hashes["current"]
            ),
            "grounding": {
                "errors": sum(item.level == "error" for item in findings),
                "warnings": sum(item.level == "warning" for item in findings),
                "identity_sha256": _category(
                    (item.page, item.level, item.code, item.message)
                    for item in findings
                )["identity_sha256"],
            },
        },
        "diagnostics": {
            "fallback_files": sorted(store.fallback_files),
            "normalized_files": {
                key: list(store.normalized_files[key])
                for key in sorted(store.normalized_files)
            },
            "parse_error_files": sorted(store.parse_errors),
            "thin_rich_disagreements": disagreements,
            "fparser_version": rich_diagnostics.get("fparser_version"),
            "rich_projection_matches": rich_diagnostics
            == {
                "fallback_files": sorted(store.fallback_files),
                "normalized_files": {
                    key: list(store.normalized_files[key])
                    for key in sorted(store.normalized_files)
                },
                "parse_errors": dict(sorted(store.parse_errors.items())),
                "fparser_version": fparser_version(),
            },
        },
        "schemas": {
            name: _schema_counts(path) for name, path in sorted(schema_paths.items())
        },
        "artifacts": {
            name: _artifact(path) for name, path in sorted(artifacts.items())
        },
        "regression_cases": _regression_summary(
            regression_cases, source_dir, store, comparisons
        ),
        "performance_reference": "reports/parser-baseline/PERFORMANCE.md",
        "known_limitations": "reports/parser-baseline/KNOWN_LIMITATIONS.md",
    }
