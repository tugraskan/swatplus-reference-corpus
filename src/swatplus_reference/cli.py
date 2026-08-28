"""Build SWAT+ documentation and machine-readable schemas from pinned source."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .docs.pages import STATUS_STALE, STATUS_TODO, Page, load_all, page_dir
from .parser.facts import FactStore
from .parser.fortran import parse_tree
from .parser.rich import RichStore
from .parser.schema_model import ModuleDoc, ProcedureDoc, DerivedTypeDoc
from .provenance.records import SourceProvenance, write_provenance
from .source.config import Config, load_config
from .source.fetch import fetch_profile, resolve_profile


def _rich_kind(record) -> str:
    if isinstance(record, ModuleDoc):
        return "module"
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


def get_store(cfg: Config, refresh: bool = False) -> FactStore:
    activate_docs_source(cfg)
    path = cfg.abs_facts_path
    if path.exists() and not refresh:
        store = FactStore.load(path)
        if store.source_ref == cfg.source_ref:
            return store
    if not cfg.abs_source_dir.exists():
        sys.exit(
            f"source dir {cfg.abs_source_dir} not found — run `swatref source fetch {cfg.docs_source}` first"
        )
    print(f"parsing {cfg.abs_source_dir} ...", file=sys.stderr)
    store = parse_tree(cfg.abs_source_dir, cfg.source_ref)
    store.save(path)
    print(
        f"parsed {len(store.symbols)} symbols "
        f"({len(store.fallback_files)} files via fallback scanner)",
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
    rich_store = None
    if rich_path.exists() and not args.refresh:
        try:
            rich_store = RichStore.load(
                rich_path, expected_source_ref=provenance.resolved_commit
            )
            print(f"rich parse already exists at {rich_path}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"rebuilding stale rich parse: {exc}", file=sys.stderr)
    if rich_store is None:
        rich_store = RichStore.build(cfg.abs_source_dir)
        rich_store.save(rich_path, provenance=provenance.to_dict())
        print(f"rich parse written to {rich_path}")
    if args.snapshot is not None:
        snapshot_dir = cfg.resolve(Path(args.snapshot))
        snapshot_name = f"{provenance.profile}-{provenance.resolved_commit[:12]}.rich.json"
        snapshot_path = snapshot_dir / snapshot_name
        rich_store.save(snapshot_path, provenance=provenance.to_dict())
        write_provenance(
            snapshot_path.with_suffix(".provenance.json"),
            provenance,
            artifact=snapshot_path.name,
            format="swatplus-reference-rich-v1",
        )
        print(f"portable snapshot written to {snapshot_path}")
    return 0


def cmd_facts_diff(cfg: Config, args) -> int:
    thin_store = get_store(cfg, refresh=args.refresh_thin)
    rich_store = RichStore.build(cfg.abs_source_dir)
    rich_index = _rich_report_index(rich_store)

    thin_names = set(thin_store.symbols.keys())
    rich_names = set(rich_index.keys())

    thin_only = sorted(thin_names - rich_names)
    rich_only = sorted(rich_names - thin_names)

    disagreements = []
    kind_collisions = []
    for name in sorted(thin_names & rich_names):
        thin_sym = thin_store.symbols.get(name)
        rich_obj = rich_index.get(name)
        if not thin_sym or not rich_obj:
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
    return 0


def _report_is_current(report) -> bool:
    return not any(
        (report.stale, report.affected, report.todo, report.orphaned, report.missing)
    )


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
    from .parser.fortran import parse_tree

    store = get_store(cfg)
    old_dir = Path(args.old_source_dir)
    if not old_dir.exists():
        sys.exit(f"--old-source-dir {old_dir} not found")
    print(f"parsing old source {old_dir} ...", file=sys.stderr)
    old_store = parse_tree(old_dir, "old")

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
    rich = None
    if rich_path.exists():
        try:
            rich = RichStore.load(rich_path, expected_source_ref=store.source_ref)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            # Rich data is strictly additive. An absent, stale, or unreadable
            # side input must always leave the ordinary thin render intact.
            print(f"ignoring rich parse: {exc}", file=sys.stderr)
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

    p = sub.add_parser("status")
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument(
        "--require-current",
        action="store_true",
        help="fail when any page is stale, affected, todo, orphaned, or missing",
    )

    sub.add_parser("mark-stale")

    p = sub.add_parser("new")
    p.add_argument("--kind", choices=["module", "subroutine", "function", "program"])

    p = sub.add_parser("check")
    p.add_argument("--strict", action="store_true", help="warnings also fail")
    p.add_argument("--verbose", "-v", action="store_true")

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
        "status": cmd_status,
        "mark-stale": cmd_mark_stale,
        "new": cmd_new,
        "check": cmd_check,
        "fill": cmd_fill,
        "refill": cmd_refill,
        "apply-delta": cmd_apply_delta,
        "batch": cmd_batch,
        "render": cmd_render,
    }[args.command]
    return handler(cfg, args)


if __name__ == "__main__":
    sys.exit(main())
