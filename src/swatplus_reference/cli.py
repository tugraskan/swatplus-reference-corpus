"""Build SWAT+ documentation and machine-readable schemas from pinned source."""

from __future__ import annotations

import argparse
import json
import platform
import re
import sys
import time
from pathlib import Path

from .docs.pages import STATUS_STALE, STATUS_TODO, Page, load_all, page_dir
from .parser.documentation import (
    RICH_DOCUMENTATION_PRODUCER,
    parse_documentation,
)
from .parser.facts import FactStore
from .parser.fortran import fparser_version, parse_tree
from .parser.rich import (
    DEFAULT_ENGINE,
    FPARSER_DIAGNOSTICS_METADATA_KEY,
    RICH_EXPORT_SCHEMA,
    RichStore,
)
from .parser.schema_model import DerivedTypeDoc, ModuleDoc, ProcedureDoc, ProgramDoc
from .provenance.records import SourceProvenance, write_provenance
from .source.config import Config, load_config
from .source.fetch import fetch_profile, resolve_profile


def _rich_kind(record) -> str:
    if isinstance(record, ModuleDoc):
        return "module"
    if isinstance(record, ProgramDoc):
        return "program"
    if isinstance(record, DerivedTypeDoc):
        return "type"
    if isinstance(record, ProcedureDoc):
        return record.kind
    return "unknown"


def _rich_report_key(record, colliding_type_names: set[str]) -> str:
    name = record.name.lower()
    if isinstance(record, DerivedTypeDoc) and name in colliding_type_names:
        return f"type::{name}"
    return name


def _rich_report_index(rich_store: RichStore) -> dict[str, object]:
    records = [
        *rich_store.index.modules,
        *rich_store.index.programs,
        *rich_store.index.procedures,
        *rich_store.index.types,
    ]
    non_type_names = {
        record.name.lower()
        for record in records
        if not isinstance(record, DerivedTypeDoc)
    }
    type_names = {
        record.name.lower()
        for record in rich_store.index.types
    }
    colliding_type_names = type_names & non_type_names
    index: dict[str, object] = {}
    for record in records:
        index.setdefault(_rich_report_key(record, colliding_type_names), record)
    return index


def activate_docs_source(cfg: Config) -> SourceProvenance:
    """Verify the selected docs profile and expose its exact commit to builders."""
    source_dir, provenance = resolve_profile(cfg, cfg.docs_source)
    profile = cfg.source_profile(cfg.docs_source)
    cfg.source_dir = source_dir
    cfg.source_ref = provenance.resolved_commit
    cfg.source_repo_url = profile.repository
    cfg.source_link_base = profile.source_link_base(provenance.resolved_commit)
    if not profile.label:
        cfg.version_label = f"SWAT+ {profile.ref} @ {provenance.resolved_commit[:12]}"
    write_provenance(
        cfg.root / ".swatref" / "sources" / f"{profile.name}.json",
        provenance,
        consumer="docs",
    )
    return provenance


def _parse_docs_with_diagnostics(
    source_dir: Path, source_ref: str, engine: str = DEFAULT_ENGINE
) -> tuple[FactStore, RichStore]:
    """Build rich documentation facts and retain fparser2 degradation data.

    The diagnostic pass stays: it records which files a plain fparser2 read
    rejects, which is degradation evidence the documentation path must keep
    showing whichever engine produced the facts.
    """

    diagnostics = parse_tree(source_dir, source_ref)
    return parse_documentation(
        source_dir,
        source_ref,
        diagnostics=diagnostics,
        engine=engine,
    )


def get_store(cfg: Config, refresh: bool = False) -> FactStore:
    provenance = activate_docs_source(cfg)
    path = cfg.abs_facts_path
    rich_path = cfg.root / ".swatref" / "docs" / "rich.json"
    if path.exists() and not refresh:
        store = FactStore.load(path)
        if (
            store.source_ref == cfg.source_ref
            and store.producer == RICH_DOCUMENTATION_PRODUCER
            and rich_path.exists()
        ):
            try:
                cached_rich = RichStore.load(rich_path, expected_source_ref=cfg.source_ref)
                expected_diagnostics = {
                    "fallback_files": sorted(set(store.fallback_files)),
                    "parse_errors": dict(sorted(store.parse_errors.items())),
                    # A cache produced by a different fparser is not
                    # interchangeable with one produced by the pinned version,
                    # so an upgrade rebuilds rather than being reused silently.
                    "fparser_version": fparser_version(),
                }
                if (
                    cached_rich.has_current_contract(cfg.docs_engine)
                    and cached_rich.index.metadata.get(FPARSER_DIAGNOSTICS_METADATA_KEY)
                    == expected_diagnostics
                ):
                    return store
            except (OSError, ValueError, json.JSONDecodeError):
                pass
    if not cfg.abs_source_dir.exists():
        sys.exit(
            f"source dir {cfg.abs_source_dir} not found — run `swatref source fetch {cfg.docs_source}` first"
        )
    print(f"parsing {cfg.abs_source_dir} ...", file=sys.stderr)
    store, rich = _parse_docs_with_diagnostics(
        cfg.abs_source_dir, cfg.source_ref, cfg.docs_engine
    )
    store.save(path)
    rich.save(rich_path, provenance=provenance.to_dict())
    print(
        f"rich-parsed {len(store.symbols)} documentation symbols; "
        f"{len(store.fallback_files)} fparser fallback files; "
        f"wrote {path} and {rich_path}",
        file=sys.stderr,
    )
    return store


def cmd_fetch(cfg: Config, args) -> int:
    provenance = fetch_profile(cfg, cfg.docs_source)
    print(json.dumps(provenance.to_dict(), indent=2, sort_keys=True))
    return 0


def cmd_parse(cfg: Config, args) -> int:
    store = get_store(cfg, refresh=True)
    for f, err in store.parse_errors.items():
        print(f"fallback: {f}: {err.splitlines()[0][:100]}")
    return 0


def cmd_rich_parse(cfg: Config, args) -> int:
    provenance = activate_docs_source(cfg)
    rich_path = cfg.root / ".swatref" / "docs" / "rich.json"
    get_store(cfg, refresh=args.refresh)
    rich_store = RichStore.load(
        rich_path, expected_source_ref=provenance.resolved_commit
    )
    print(f"rich documentation parse is current at {rich_path}")
    if args.snapshot is not None:
        snapshot_dir = cfg.resolve(Path(args.snapshot))
        snapshot_name = f"{provenance.profile}-{provenance.resolved_commit[:12]}.rich.json"
        snapshot_path = snapshot_dir / snapshot_name
        rich_store.save(snapshot_path, provenance=provenance.to_dict())
        write_provenance(
            snapshot_path.with_suffix(".provenance.json"),
            provenance,
            artifact=snapshot_path.name,
            format=RICH_EXPORT_SCHEMA,
        )
        print(f"portable snapshot written to {snapshot_path}")
    return 0


def cmd_facts_diff(cfg: Config, args) -> int:
    from .parser.fortran import parse_tree

    activate_docs_source(cfg)
    thin_store = parse_tree(cfg.abs_source_dir, cfg.source_ref)
    get_store(cfg, refresh=False)
    rich_store = RichStore.load(
        cfg.root / ".swatref" / "docs" / "rich.json",
        expected_source_ref=cfg.source_ref,
    )
    rich_index = _rich_report_index(rich_store)

    thin_names = set(thin_store.symbols.keys())
    rich_names = set(rich_index.keys())

    thin_only = sorted(thin_names - rich_names)
    rich_only = sorted(rich_names - thin_names)

    disagreements = []
    kind_collisions = []
    for name in sorted(thin_names & rich_names):
        thin_sym = thin_store.symbols.get(name)
        if not thin_sym:
            continue
        rich_obj = rich_store.get_of_kind(thin_sym.name, thin_sym.kind, file=thin_sym.file)
        if rich_obj is None:
            kind_collisions.append((name, f"no rich {thin_sym.kind} match in {thin_sym.file}"))
            continue

        rich_kind = _rich_kind(rich_obj)

        # Check for kind collision
        if thin_sym.kind != rich_kind:
            kind_collisions.append((name, f"kind: thin={thin_sym.kind} rich={rich_kind}"))
            continue

        diffs = []
        if hasattr(rich_obj, 'args') and len(thin_sym.args) != len(rich_obj.args):
            diffs.append(f"arg_count: thin={len(thin_sym.args)} rich={len(rich_obj.args)}")
        if hasattr(rich_obj, 'uses') and len(thin_sym.uses) != len(rich_obj.uses):
            diffs.append(f"use_count: thin={len(thin_sym.uses)} rich={len(rich_obj.uses)}")
        if hasattr(rich_obj, 'locals') and len(thin_sym.locals) != len(rich_obj.locals):
            diffs.append(f"local_count: thin={len(thin_sym.locals)} rich={len(rich_obj.locals)}")
        if hasattr(rich_obj, 'location') and hasattr(rich_obj.location, 'line'):
            thin_span = thin_sym.end_line - thin_sym.start_line + 1
            rich_end = rich_obj.location.end_line or rich_obj.location.line
            rich_span = rich_end - rich_obj.location.line + 1
            if thin_span != rich_span:
                diffs.append(f"span: thin={thin_span} rich={rich_span}")

        if diffs:
            disagreements.append((name, "; ".join(diffs)))

    # Write report under reports/
    report_dir = cfg.root / "reports" / "docs"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"rich-vs-thin-{cfg.source_ref[:12]}.md"

    lines = []
    lines.append(f"# Rich vs Thin Diff — SWAT+ {cfg.source_ref[:12]}\n")
    lines.append(f"## Summary\n")
    lines.append(f"- Thin-only: {len(thin_only)}")
    lines.append(f"- Rich-only: {len(rich_only)}")
    lines.append(f"- Disagreements: {len(disagreements)}")
    lines.append(f"- Kind collisions: {len(kind_collisions)}\n")

    lines.append("## Thin-only symbols\n")
    for n in thin_only:
        lines.append(f"- `{n}`")

    lines.append("\n## Rich-only symbols\n")
    for n in rich_only:
        lines.append(f"- `{n}`")

    lines.append("\n## Kind collisions\n")
    for name, msg in kind_collisions:
        lines.append(f"- `{name}`: {msg}")

    lines.append("\n## Disagreements\n")
    for name, msg in disagreements:
        lines.append(f"- `{name}`: {msg}")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"diff report written to {report_path}")
    print(f"thin_only={len(thin_only)} rich_only={len(rich_only)} disagreements={len(disagreements)} kind_collisions={len(kind_collisions)}")
    return 0


def _baseline_paths(
    cfg: Config, source_ref: str
) -> tuple[Path, Path, dict[str, Path], dict[str, Path]]:
    short_ref = source_ref[:12]
    report_dir = cfg.root / "reports" / "parser-baseline"
    report_path = report_dir / f"{cfg.docs_source}-{short_ref}.json"
    snapshot_name = f"{cfg.docs_source}-{short_ref}.rich.json"
    tracked_snapshot = cfg.root / "snapshots" / "rich" / snapshot_name
    tracked_snapshot_provenance = tracked_snapshot.with_suffix(".provenance.json")
    _, schema_path, range_path, schema_provenance = _schema_paths(cfg)
    reports_dir = cfg.resolve(cfg.schema.reports_dir)
    version = cfg.schema.version
    artifacts = {
        tracked_snapshot.relative_to(cfg.root).as_posix(): tracked_snapshot,
        tracked_snapshot_provenance.relative_to(cfg.root).as_posix(): tracked_snapshot_provenance,
        schema_path.relative_to(cfg.root).as_posix(): schema_path,
        range_path.relative_to(cfg.root).as_posix(): range_path,
        schema_provenance.relative_to(cfg.root).as_posix(): schema_provenance,
        (reports_dir / f"swatplus-{version}-editor-schema-report.json")
        .relative_to(cfg.root)
        .as_posix(): reports_dir / f"swatplus-{version}-editor-schema-report.json",
        (reports_dir / f"swatplus-{version}-field-map.json")
        .relative_to(cfg.root)
        .as_posix(): reports_dir / f"swatplus-{version}-field-map.json",
        (reports_dir / f"swatplus-{version}-field-map.md")
        .relative_to(cfg.root)
        .as_posix(): reports_dir / f"swatplus-{version}-field-map.md",
        (reports_dir / f"swatplus-{version}-range-crosswalk.json")
        .relative_to(cfg.root)
        .as_posix(): reports_dir / f"swatplus-{version}-range-crosswalk.json",
        (reports_dir / f"swatplus-{version}-range-crosswalk.md")
        .relative_to(cfg.root)
        .as_posix(): reports_dir / f"swatplus-{version}-range-crosswalk.md",
    }
    schemas = {"base": schema_path, "ranges": range_path}
    return report_path, tracked_snapshot, artifacts, schemas


def _performance_markdown(elapsed: float, peak_bytes: int) -> str:
    return (
        "# Phase 0 parser performance reference\n\n"
        "This is an observational baseline, not a byte-reproducibility gate. "
        "CI verifies the deterministic facts and artifacts instead.\n\n"
        f"- Platform: `{platform.system()} {platform.machine()}`\n"
        f"- Python: `{platform.python_version()}`\n"
        "- Workload: one complete rich scan, fparser2 diagnostic pass, and "
        "documentation projection\n"
        f"- Elapsed time: **{elapsed:.2f} seconds**\n"
        f"- Peak process resident memory at parse completion: **{peak_bytes / (1024 * 1024):.2f} MiB**\n"
        "- Measurement: OS peak working set/RSS, including interpreter overhead; "
        "no allocation tracing is enabled\n"
        "- Source: pinned SWAT+ commit recorded in the JSON baseline\n"
    )


# A rendered GitHub source link: .../blob/<commit>/<path>#L<start>[-L<end>]
_SOURCE_LINK_RE = re.compile(r"/blob/(?P<commit>[0-9a-f]{7,40})/")


def cmd_verify_consumers(cfg: Config, args) -> int:
    """Run every documentation consumer against the fparser2-produced index.

    Phase 7's exit gate is that all consumers pass "without invoking the legacy
    scanner", so this builds the facts with the AST engine and then drives the
    real consumer code -- projection, staleness, rendering, grounding and the
    source-link audit -- rather than re-implementing their checks. Where the
    scanner is used at all it is only to produce the comparison baseline, and
    each gate says which index it ran on.
    """

    import dataclasses
    import json
    import shutil

    from .docs.grounding import check_all
    from .docs.links import audit_source_links, count_source_links
    from .docs.pages import load_all
    from .docs.render import render_site
    from .docs.staleness import compute_status
    from .parser.documentation import parse_documentation
    from .parser.rich import AST_ENGINE, SCANNER_ENGINE

    provenance = activate_docs_source(cfg)
    source_dir = cfg.abs_source_dir
    if not source_dir.exists():
        sys.exit(
            f"source dir {source_dir} not found — run `swatref source fetch {cfg.docs_source}` first"
        )
    pages = load_all(cfg.abs_docs_dir)

    results: list[tuple[str, bool, str]] = []

    def gate(name: str, ok: bool, detail: str) -> None:
        results.append((name, ok, detail))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

    outcomes: dict[str, dict] = {}
    for engine in (AST_ENGINE, SCANNER_ENGINE):
        print(f"\nbuilding facts with engine={engine} ...", flush=True)
        store, rich = parse_documentation(source_dir, cfg.source_ref, engine=engine)
        status = compute_status(store, pages)
        findings = check_all(store, pages)
        outcomes[engine] = {
            "symbols": len(store.symbols),
            "status": {
                "filled": len(status.filled),
                "stale": len(status.stale),
                "affected": len(status.affected),
                "orphaned": len(status.orphaned),
                "missing": len(status.missing),
            },
            "errors": sum(1 for f in findings if f.level == "error"),
            "warnings": sum(1 for f in findings if f.level == "warning"),
            "store": store,
            "rich": rich,
        }

    ast, scanner = outcomes[AST_ENGINE], outcomes[SCANNER_ENGINE]
    print(f"\nconsumer gates on the {AST_ENGINE} index:")

    gate(
        "projection builds a fact store",
        ast["symbols"] == scanner["symbols"] and ast["symbols"] > 0,
        f"{ast['symbols']} symbols (scanner: {scanner['symbols']})",
    )
    gate(
        "grounding reports no errors",
        ast["errors"] == 0,
        f"{ast['errors']} errors, {ast['warnings']} warnings",
    )
    gate(
        "grounding warnings match the scanner baseline",
        ast["warnings"] == scanner["warnings"],
        f"{ast['warnings']} vs {scanner['warnings']}",
    )
    gate(
        "page status is unchanged",
        ast["status"] == scanner["status"],
        f"{ast['status']}",
    )

    # Render from the AST facts into a scratch tree, then audit the links that
    # rendering produced. This is the real renderer and the real audit.
    render_root = cfg.root / ".swatref" / "verify-consumers"
    if render_root.exists():
        shutil.rmtree(render_root)
    render_root.mkdir(parents=True, exist_ok=True)
    rendered = render_site(
        dataclasses.replace(cfg, render_dir=render_root), ast["store"], ast["rich"]
    )
    link_findings = audit_source_links(rendered, source_dir, cfg.source_link_base)
    checked = count_source_links(rendered, cfg.source_link_base)
    gate(
        "every page renders",
        any(rendered.rglob("*.md")),
        f"rendered into {_rel(rendered, cfg.root)}",
    )
    gate(
        "every source link resolves",
        not link_findings and checked > 0,
        f"{len(link_findings)} invalid across {checked:,} links",
    )
    # The plan asks that every generated GitHub URL use the configured source
    # commit, so read the rendered links back and check the SHA in them rather
    # than checking the template they were built from.
    commit = provenance.resolved_commit
    wrong_commit = 0
    sampled = 0
    for rendered_page in rendered.rglob("*.md"):
        for match in _SOURCE_LINK_RE.finditer(rendered_page.read_text(encoding="utf-8")):
            sampled += 1
            if match.group("commit") != commit:
                wrong_commit += 1
    gate(
        "every source link uses the pinned commit",
        sampled > 0 and wrong_commit == 0,
        f"{sampled:,} links at {commit[:12]}, {wrong_commit} on another commit",
    )

    if args.json:
        path = Path(args.json)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "engine": AST_ENGINE,
            "baseline_engine": SCANNER_ENGINE,
            "gates": [
                {"name": name, "passed": ok, "detail": detail}
                for name, ok, detail in results
            ],
        }
        path.write_bytes(
            (json.dumps(payload, indent=1, sort_keys=True) + "\n").encode("utf-8")
        )
        print(f"wrote {path}")

    failed = [name for name, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} consumer gates pass")
    for name in failed:
        print(f"  FAILED: {name}")
    return 1 if failed else 0


def cmd_parity(cfg: Config, args) -> int:
    """Compare the two parsers field by field and report every difference."""

    import json

    from .parser.ast_index import build_ast_index
    from .parser.parity import compare_indexes, format_report
    from .parser.schema_config import BuildConfig
    from .parser.schema_fortran import FortranScanner
    from .parser.semantic import annotate_project_dataflow, resolve_project_calls

    source_dir = cfg.source_dir.resolve()
    config = BuildConfig(source_dir=source_dir)

    print(f"parity: scanning {source_dir} with both parsers ...", flush=True)
    indexes = (build_ast_index(config), FortranScanner(config).scan())
    for index in indexes:
        # Both sides need their semantic layer, or the fields that depend on it
        # compare as differences rather than as agreement.
        resolve_project_calls(index)
        annotate_project_dataflow(index)

    report = compare_indexes(*indexes)
    print(format_report(report))

    failures = report.failures()
    if args.json:
        path = Path(args.json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(
            (json.dumps(report.to_dict(), indent=1, sort_keys=True) + "\n").encode("utf-8")
        )
        print(f"wrote {path}")

    approved = len({(d.category, d.field, d.owner) for d in report.approved})
    print(
        f"\n{len(failures)} unexpected difference(s); "
        f"{approved} approved correction(s)"
    )
    for problem in failures:
        print(f"  {problem}")
    return 1 if failures else 0


def cmd_baseline(cfg: Config, args) -> int:
    """Write or verify the deterministic Phase 0 parser baseline."""

    from .parser.baseline import (
        baseline_failures, build_parser_baseline, contract_drift, dumps_baseline,
        normalized_bytes, peak_process_memory_bytes,
    )
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError, ValidationError

    provenance = activate_docs_source(cfg)
    report_path, tracked_snapshot, artifacts, schema_paths = _baseline_paths(
        cfg, provenance.resolved_commit
    )
    candidate_dir = cfg.root / ".swatref" / "parser-baseline"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = candidate_dir / tracked_snapshot.name
    snapshot_provenance = snapshot_path.with_suffix(".provenance.json")

    started = time.perf_counter()
    print("baseline: parsing fparser2 diagnostics ...", flush=True)
    thin = parse_tree(cfg.abs_source_dir, provenance.resolved_commit)
    print("baseline: parsing rich facts and projecting documentation ...", flush=True)
    store, rich = parse_documentation(
        cfg.abs_source_dir,
        provenance.resolved_commit,
        diagnostics=thin,
        engine=cfg.docs_engine,
    )
    elapsed = time.perf_counter() - started
    peak_bytes = peak_process_memory_bytes()
    print(f"baseline: parse complete ({elapsed:.2f}s); collecting identities ...", flush=True)

    rich.save(snapshot_path, provenance=provenance.to_dict())
    write_provenance(
        snapshot_provenance,
        provenance,
        artifact=tracked_snapshot.name,
        format=RICH_EXPORT_SCHEMA,
    )
    logical_snapshot = tracked_snapshot.relative_to(cfg.root).as_posix()
    logical_provenance = tracked_snapshot.with_suffix(".provenance.json").relative_to(
        cfg.root
    ).as_posix()
    artifacts[logical_snapshot] = snapshot_path
    artifacts[logical_provenance] = snapshot_provenance

    baseline = build_parser_baseline(
        root=cfg.root,
        source_dir=cfg.abs_source_dir,
        source=provenance.to_dict(),
        store=store,
        rich=rich,
        pages=load_all(cfg.abs_docs_dir),
        artifacts=artifacts,
        regression_cases=cfg.root
        / "reports"
        / "parser-baseline"
        / "regression-cases.json",
        schema_paths=schema_paths,
        thin=thin,
    )
    text = dumps_baseline(baseline)
    print(
        f"baseline parse: {elapsed:.2f}s, peak process memory: "
        f"{peak_bytes / (1024 * 1024):.2f} MiB"
    )

    candidate_report = candidate_dir / report_path.name
    candidate_report.write_bytes(text.encode("utf-8"))
    # A contract breach is a Phase 0 gate result, not an internal error, so it
    # reads like every other failure instead of aborting on a traceback.
    failures = []
    schema_path = report_path.parent / "baseline.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(baseline)
    except OSError as exc:
        failures.append(f"cannot read {_rel(schema_path, cfg.root)}: {exc}")
    except json.JSONDecodeError as exc:
        failures.append(f"{_rel(schema_path, cfg.root)} is not valid JSON: {exc}")
    except SchemaError as exc:
        failures.append(f"{_rel(schema_path, cfg.root)} is not a valid schema: {exc.message}")
    except ValidationError as exc:
        location = "/".join(str(part) for part in exc.absolute_path) or "<root>"
        failures.append(f"baseline does not match its schema at {location}: {exc.message}")
    if failures:
        # The invariant and README checks below assume the validated shape.
        # Do not inspect malformed fields or publish any tracked artifacts.
        for failure in failures:
            print(f"Phase 0 gate failed: {failure}")
        return 1
    failures.extend(baseline_failures(baseline))
    readme = (cfg.root / "README.md").read_text(encoding="utf-8")
    docs = baseline["documentation"]
    for statement in (
        f"- {docs['page_status']['filled']:,} filled pages;",
        f"- {docs['grounding']['errors']:,} grounding errors; and",
        f"- {docs['grounding']['warnings']:,} non-blocking identifier warnings.",
    ):
        if statement not in readme:
            failures.append(f"README baseline count is missing or stale: {statement}")
    if failures:
        for failure in failures:
            print(f"Phase 0 gate failed: {failure}")
        return 1

    if args.write:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        tracked_snapshot.parent.mkdir(parents=True, exist_ok=True)
        tracked_snapshot.write_bytes(normalized_bytes(snapshot_path))
        tracked_snapshot.with_suffix(".provenance.json").write_bytes(
            normalized_bytes(snapshot_provenance)
        )
        report_path.write_bytes(text.encode("utf-8"))
        (report_path.parent / "PERFORMANCE.md").write_text(
            _performance_markdown(elapsed, peak_bytes), encoding="utf-8"
        )
        print(f"wrote {report_path}")
        return 0

    for candidate, tracked in (
        (snapshot_path, tracked_snapshot),
        (snapshot_provenance, tracked_snapshot.with_suffix(".provenance.json")),
        (candidate_report, report_path),
    ):
        if not tracked.exists() or normalized_bytes(candidate) != normalized_bytes(tracked):
            failures.append(tracked.relative_to(cfg.root).as_posix())
    if failures:
        for path in failures:
            print(f"stale baseline artifact: {path}")
        # A toolchain upgrade drifts these artifacts for a reason that has
        # nothing to do with the parser, so name it rather than leaving the
        # reader to diff a 46 MB snapshot.
        for line in contract_drift(report_path, baseline):
            print(f"contract changed: {line}")
        print("run `swatref docs baseline --write` and review the changes")
        return 1
    print(f"Phase 0 baseline is current: {report_path}")
    return 0


def cmd_status(cfg: Config, args) -> int:
    from .docs.staleness import compute_status

    store = get_store(cfg)
    pages = load_all(cfg.abs_docs_dir)
    report = compute_status(store, pages)
    print(report.summary())
    if args.verbose:
        for label, items in (
            ("stale", report.stale),
            ("todo", report.todo),
            ("orphaned", report.orphaned),
        ):
            for p in items:
                print(f"{label}: {_rel(p.path, cfg.root)}")
        for p in report.affected:
            trigger = ", ".join(report.affected_by.get(p.path.name, []))
            print(f"affected: {_rel(p.path, cfg.root)}  (changed: {trigger})")
        for name in report.missing:
            print(f"missing-page: {name}")
    if args.require_current and not _report_is_current(report):
        return 1
    if args.fail_on_affected and report.affected:
        return 1
    return 0


def _report_is_current(report) -> bool:
    """Return whether the corpus has no hard documentation drift.

    ``affected`` remains a visible review signal, but it is intentionally
    advisory unless the caller selects ``--fail-on-affected``.
    """

    return not any((report.stale, report.todo, report.orphaned, report.missing))


def _rel(path: Path, root: Path) -> str:
    """Path relative to root when possible, else the path as-is.

    docs_dir may be configured absolute or outside the config root (e.g. a
    version-bump run pointing one ref's config at another ref's page tree);
    relative_to would raise there.
    """
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def cmd_mark_stale(cfg: Config, args) -> int:
    from .docs.staleness import apply_status

    store = get_store(cfg)
    pages = load_all(cfg.abs_docs_dir)
    changed = apply_status(store, pages)
    for p in changed:
        print(f"{p.status}: {p.path.relative_to(cfg.root)}")
    print(f"{len(changed)} pages updated")
    return 0


def cmd_new(cfg: Config, args) -> int:
    from .docs.staleness import compute_status

    store = get_store(cfg)
    pages = load_all(cfg.abs_docs_dir)
    report = compute_status(store, pages)
    created = 0
    for name in report.missing:
        sym = store.get(name)
        if args.kind and sym.kind != args.kind:
            continue
        kind = "module" if sym.kind == "module" else "procedure"
        Page(
            path=cfg.abs_docs_dir / page_dir(kind) / f"{name}.md",
            kind=kind,
            symbol=name,
            title=name,
            status=STATUS_TODO,
            version_label=cfg.version_label,
            body=(
                "<!-- facts:header -->\n\n<!-- facts:members -->\n\n"
                "<!-- facts:variables -->"
                if kind == "module"
                else "<!-- facts:header -->\n\n<!-- facts:arguments -->\n\n"
                "<!-- facts:calls -->\n\n<!-- facts:uses -->\n\n"
                "<!-- facts:locals -->\n\n<!-- facts:io -->"
            ),
        ).save()
        created += 1
    print(f"created {created} todo pages")
    return 0


def cmd_check(cfg: Config, args) -> int:
    from .docs.grounding import check_all

    store = get_store(cfg)
    pages = load_all(cfg.abs_docs_dir)
    findings = check_all(store, pages)
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]
    shown = findings if (args.strict or args.verbose) else errors
    for f in shown:
        print(f)
    print(f"{len(errors)} errors, {len(warnings)} warnings across {len(pages)} pages")
    if errors or (args.strict and warnings):
        return 1
    return 0


def cmd_check_links(cfg: Config, args) -> int:
    """Verify every rendered GitHub source link against the pinned checkout."""

    from .docs.links import audit_source_links, count_source_links

    activate_docs_source(cfg)
    render_dir = cfg.abs_render_dir
    if not render_dir.exists():
        sys.exit(f"render dir {render_dir} not found — run `swatref docs render` first")
    findings = audit_source_links(render_dir, cfg.abs_source_dir, cfg.source_link_base)
    checked = count_source_links(render_dir, cfg.source_link_base)
    for finding in findings:
        print(finding)
    print(f"{len(findings)} invalid targets across {checked:,} source links")
    if not checked:
        # An empty or stale render would otherwise pass this gate in silence,
        # which is the one outcome a link audit must never report as success.
        print(f"no source links found under {_rel(render_dir, cfg.root)} — rerun `swatref docs render`")
        return 1
    return 1 if findings else 0


def cmd_fill(cfg: Config, args) -> int:
    from .generation.fill import run_fill

    store = get_store(cfg)
    paths = _fill_candidates(cfg, store, args.pages, args.limit)
    if not paths:
        print("nothing to fill")
        return 0
    print(f"filling {len(paths)} pages with {args.model or cfg.fill.model}")
    for line in run_fill(cfg, store, paths, model=args.model, dry_run=args.dry_run):
        print(line)
    return 0


def _fill_candidates(cfg: Config, store, pages_arg: list[str], limit: int | None) -> list[Path]:
    from .docs.staleness import compute_status

    if pages_arg:
        return [Path(p) for p in pages_arg]
    report = compute_status(store, load_all(cfg.abs_docs_dir))
    candidates = report.todo + report.stale
    if limit:
        candidates = candidates[:limit]
    return [p.path for p in candidates if p.symbol]


def _stale_paths(cfg: Config, store, limit: int | None) -> list[Path]:
    from .docs.staleness import compute_status

    report = compute_status(store, load_all(cfg.abs_docs_dir))
    stale = [p for p in report.stale if p.symbol]
    return [p.path for p in (stale[:limit] if limit else stale)]


def cmd_refill(cfg: Config, args) -> int:
    from .generation import refill

    store = get_store(cfg)
    old_dir = Path(args.old_source_dir)
    if not old_dir.exists():
        sys.exit(f"--old-source-dir {old_dir} not found")
    print(f"parsing old source {old_dir} ...", file=sys.stderr)
    old_store, _old_rich = parse_documentation(old_dir, "old")

    paths = [Path(p) for p in args.pages] if args.pages else _stale_paths(cfg, store, args.limit)
    if not paths:
        print("no stale pages to re-fill")
        return 0

    if args.emit_prompts:
        out = Path(args.emit_prompts)
        for line in refill.emit_delta_prompts(cfg, store, old_store, old_dir, paths, out):
            print(line)
        print(f"wrote delta prompts to {out} — fill them, then `swatref docs apply-delta`")
        return 0

    print(f"delta re-filling {len(paths)} stale pages with {args.model or cfg.fill.model}")
    for line in refill.run_refill(
        cfg, store, old_store, old_dir, paths, model=args.model, dry_run=args.dry_run
    ):
        print(line)
    return 0


def cmd_apply_delta(cfg: Config, args) -> int:
    from .generation import refill

    store = get_store(cfg)
    for line in refill.apply_delta_file(cfg, store, Path(args.deltas)):
        print(line)
    return 0


def cmd_batch(cfg: Config, args) -> int:
    from .generation import batch

    store = get_store(cfg)
    if args.action == "submit":
        paths = _fill_candidates(cfg, store, args.pages, args.limit)
        if not paths:
            print("nothing to fill")
            return 0
        batch.submit(cfg, store, paths, model=args.model, dry_run=args.dry_run)
    elif args.action == "status":
        batch.status(cfg, args.batch_id)
    elif args.action == "merge":
        if not args.batch_id:
            sys.exit("merge requires a BATCH_ID")
        for line in batch.merge(cfg, store, args.batch_id):
            print(line)
    return 0


def cmd_render(cfg: Config, args) -> int:
    from .docs.render import render_site

    store = get_store(cfg)
    rich_path = cfg.root / ".swatref" / "docs" / "rich.json"
    rich = RichStore.load(rich_path, expected_source_ref=store.source_ref)
    out = render_site(cfg, store, rich)
    print(f"rendered into {out}")
    return 0


def _repository_id(url: str) -> str:
    clean = url.removesuffix(".git").rstrip("/")
    marker = "github.com/"
    return clean.split(marker, 1)[1] if marker in clean else clean


def cmd_source(cfg: Config, argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="swatref source")
    parser.add_argument("action", choices=["show", "fetch"])
    parser.add_argument("profile", nargs="?", default=cfg.docs_source)
    args = parser.parse_args(argv)
    try:
        if args.action == "fetch":
            provenance = fetch_profile(cfg, args.profile)
        else:
            _, provenance = resolve_profile(cfg, args.profile)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(provenance.to_dict(), indent=2, sort_keys=True))
    return 0


def _schema_paths(cfg: Config) -> tuple[Path, Path, Path, Path]:
    version = cfg.schema.version
    output_dir = cfg.resolve(cfg.schema.output_dir)
    schema_path = output_dir / f"swatplus-{version}.json"
    range_path = output_dir / f"swatplus-{version}-ranges.json"
    provenance_path = output_dir / f"swatplus-{version}.provenance.json"
    return output_dir, schema_path, range_path, provenance_path


def cmd_schema_build(cfg: Config) -> int:
    from . import __version__
    from .parser.schema_fortran import FortranScanner
    from .schema.input import build_schema, dumps
    from .parser.schema_config import BuildConfig

    source_dir, provenance = resolve_profile(cfg, cfg.schema.source)
    profile = cfg.source_profile(cfg.schema.source)
    scanner_cfg = BuildConfig(source_dir=source_dir)
    project = FortranScanner(scanner_cfg).scan()
    # Keep the historical generator identifier so rebuilding 62.0.0 remains
    # byte-for-byte compatible with the already reviewed artifact.
    payload = build_schema(
        project,
        swatplus_version=cfg.schema.version,
        source_ref=profile.ref,
        source_repository=_repository_id(profile.repository),
        generator=f"swatplus-doc-builder {__version__}",
        generated_utc=None,
    )
    output_dir, schema_path, _, provenance_path = _schema_paths(cfg)
    output_dir.mkdir(parents=True, exist_ok=True)
    schema_path.write_text(dumps(payload), encoding="utf-8")
    write_provenance(
        provenance_path,
        provenance,
        artifact=schema_path.name,
        swatplus_version=cfg.schema.version,
    )
    print(f"wrote {schema_path}")
    print(f"resolved: {len(payload['files'])}; unresolved: {len(payload['unresolved'])}")
    print(f"exact source commit: {provenance.resolved_commit}")
    return 0


def cmd_schema_ranges(cfg: Config) -> int:
    from .schema.ranges import build_range_crosswalk

    output_dir, schema_path, range_path, _ = _schema_paths(cfg)
    result = build_range_crosswalk(
        cfg.resolve(cfg.schema.range_csv),
        cfg.resolve(cfg.schema.editor_report),
        schema_path,
        output_dir,
        cfg.resolve(cfg.schema.reports_dir),
    )
    print(f"wrote {range_path}")
    print(json.dumps(result.summary(), indent=2, sort_keys=True))
    return 0


def cmd_schema_field_map(cfg: Config) -> int:
    from .schema.field_map import main as field_map_main

    _, schema_path, _, _ = _schema_paths(cfg)
    return field_map_main(
        [
            "--spreadsheet",
            str(cfg.resolve(cfg.schema.range_csv)),
            "--editor-report",
            str(cfg.resolve(cfg.schema.editor_report)),
            "--schema",
            str(schema_path),
            "--output",
            str(cfg.resolve(cfg.schema.reports_dir)),
        ]
    )


def cmd_schema_editor_report(cfg: Config, editor_root: str) -> int:
    from .schema.editor_report import main as editor_report_main

    profile = cfg.source_profile(cfg.schema.source)
    _, schema_path, _, _ = _schema_paths(cfg)
    output = cfg.resolve(cfg.schema.reports_dir) / (
        f"swatplus-{cfg.schema.version}-editor-schema-report.json"
    )
    return editor_report_main(
        [
            "--official-schema",
            str(schema_path),
            "--editor-root",
            editor_root,
            "--official-source-repo",
            str(profile.abs_checkout(cfg.root)),
            "--output",
            str(output),
        ]
    )


def cmd_schema(cfg: Config, argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="swatref schema")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("build", help="generate the deterministic base input schema")
    sub.add_parser("ranges", help="apply reviewed parameter ranges")
    sub.add_parser("field-map", help="write source/spreadsheet field crosswalks")
    editor = sub.add_parser("editor-report", help="compare with a read-only Editor checkout")
    editor.add_argument("--editor-root", required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == "build":
            return cmd_schema_build(cfg)
        if args.action == "ranges":
            return cmd_schema_ranges(cfg)
        if args.action == "field-map":
            return cmd_schema_field_map(cfg)
        return cmd_schema_editor_report(cfg, args.editor_root)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    return 2


def cmd_compare(cfg: Config, argv: list[str]) -> int:
    """Run a configured, locked source impact comparison."""
    parser = argparse.ArgumentParser(prog="swatref compare")
    parser.add_argument("name", help="comparison name from swatref.toml")
    parser.add_argument(
        "--fetch", action="store_true", help="fetch and verify both locked source profiles"
    )
    parser.add_argument(
        "--skip-source-build", action="store_true", help="skip compiling both source trees"
    )
    parser.add_argument(
        "--skip-preview", action="store_true", help="skip the isolated strict MkDocs preview"
    )
    args = parser.parse_args(argv)
    try:
        from .comparison.run import run_comparison

        result = run_comparison(
            cfg,
            args.name,
            fetch=args.fetch,
            build_sources=not args.skip_source_build,
            build_preview=not args.skip_preview,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    print(f"wrote comparison report to {result.report_dir}")
    print(result.one_line_summary)
    return 0 if result.complete else 1


def _config_from_argv(argv: list[str]) -> tuple[str, list[str]]:
    """Accept --config before or after the docs/schema/source namespace."""
    args = list(argv)
    config = "swatref.toml"
    if "--config" in args:
        index = args.index("--config")
        if index + 1 >= len(args):
            raise SystemExit("--config requires a path")
        config = args[index + 1]
        del args[index : index + 2]
    return config, args


def main(argv: list[str] | None = None) -> int:
    config_path, argv = _config_from_argv(list(argv) if argv is not None else sys.argv[1:])
    if not argv or argv == ["--help"] or argv == ["-h"]:
        parser = argparse.ArgumentParser(
            prog="swatref",
            description="Build the SWAT+ reference corpus from selectable source profiles.",
        )
        parser.add_argument("--config", default="swatref.toml")
        parser.add_argument(
            "area", nargs="?", choices=["source", "docs", "schema", "compare"],
            help="source checkout, readable documentation, JSON schemas, or impact comparison",
        )
        parser.print_help()
        return 0
    cfg = load_config(config_path)
    if argv and argv[0] == "source":
        return cmd_source(cfg, argv[1:])
    if argv and argv[0] == "schema":
        return cmd_schema(cfg, argv[1:])
    if argv and argv[0] == "compare":
        return cmd_compare(cfg, argv[1:])
    if argv and argv[0] == "docs":
        argv = argv[1:]

    parser = argparse.ArgumentParser(prog="swatref docs", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("fetch")
    sub.add_parser("parse")

    p = sub.add_parser("rich-parse")
    p.add_argument("--refresh", action="store_true", help="rebuild even if rich.json exists")
    p.add_argument(
        "--snapshot",
        nargs="?",
        const="snapshots/rich",
        help=(
            "also write a portable, commit-named JSON snapshot for external consumers "
            "(default: snapshots/rich)"
        ),
    )

    p = sub.add_parser("facts-diff")
    p.add_argument("--refresh-thin", action="store_true", help="force reparse of thin store before diffing")

    p = sub.add_parser("baseline", help="write or verify the Phase 0 parser baseline")
    p.add_argument(
        "--write",
        action="store_true",
        help="replace the tracked baseline and rich snapshot after review",
    )

    p = sub.add_parser(
        "parity",
        help="compare the fparser2 and scanner indexes field by field",
    )
    p.add_argument("--json", help="also write the full report to this path")

    p = sub.add_parser(
        "verify-consumers",
        help="run every documentation consumer against the fparser2 index",
    )
    p.add_argument("--json", help="also write the gate results to this path")

    p = sub.add_parser("status")
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument(
        "--require-current",
        action="store_true",
        help="fail when any page is stale, todo, orphaned, or missing",
    )
    p.add_argument(
        "--fail-on-affected",
        action="store_true",
        help="also fail when dependency changes mark pages for review",
    )

    sub.add_parser("mark-stale")

    p = sub.add_parser("new")
    p.add_argument("--kind", choices=["module", "subroutine", "function", "program"])

    p = sub.add_parser("check")
    p.add_argument("--strict", action="store_true", help="warnings also fail")
    p.add_argument("--verbose", "-v", action="store_true")

    sub.add_parser(
        "check-links",
        help="verify rendered GitHub source links against the pinned checkout",
    )

    p = sub.add_parser("fill")
    p.add_argument("pages", nargs="*", help="specific page paths (default: all todo+stale)")
    p.add_argument("--model")
    p.add_argument("--limit", type=int)
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("refill", help="segment-aware delta re-fill of stale pages")
    p.add_argument("pages", nargs="*", help="specific page paths (default: all stale)")
    p.add_argument("--old-source-dir", required=True, help="the previous ref's src/ (for the diff)")
    p.add_argument("--model")
    p.add_argument("--limit", type=int)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--emit-prompts", metavar="DIR", help="write delta prompts here instead of calling the API (key-free)")

    p = sub.add_parser("apply-delta", help="apply a hand-authored {symbol: delta} JSON (key-free)")
    p.add_argument("deltas", help="JSON file mapping symbol -> changed fields")

    p = sub.add_parser("batch")
    p.add_argument("action", choices=["submit", "status", "merge"])
    p.add_argument("batch_id", nargs="?", help="batch id (status/merge)")
    p.add_argument("--pages", nargs="*", default=[], help="specific page paths for submit")
    p.add_argument("--model")
    p.add_argument("--limit", type=int)
    p.add_argument("--dry-run", action="store_true")

    sub.add_parser("render")

    args = parser.parse_args(argv)
    handler = {
        "fetch": cmd_fetch,
        "parse": cmd_parse,
        "rich-parse": cmd_rich_parse,
        "facts-diff": cmd_facts_diff,
        "baseline": cmd_baseline,
        "parity": cmd_parity,
        "verify-consumers": cmd_verify_consumers,
        "status": cmd_status,
        "mark-stale": cmd_mark_stale,
        "new": cmd_new,
        "check": cmd_check,
        "check-links": cmd_check_links,
        "fill": cmd_fill,
        "refill": cmd_refill,
        "apply-delta": cmd_apply_delta,
        "batch": cmd_batch,
        "render": cmd_render,
    }[args.command]
    return handler(cfg, args)


if __name__ == "__main__":
    sys.exit(main())
