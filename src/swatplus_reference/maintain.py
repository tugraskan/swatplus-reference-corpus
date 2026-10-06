"""Reviewed documentation maintenance: propose, preview, then apply.

`swatref docs refill` revises stale pages and writes them in one step.
`swatref docs maintain` splits that so nothing reaches ``docs_src/`` unseen:

1. ``propose`` diffs each stale page's symbol between the base profile (the
   source its prose was written against) and the candidate (the docs
   source), generates a delta once, splices it into the page in memory, and
   grounds the result. It writes only the proposal file, which records both
   exact commits and, per page, the original and proposed bytes, the source
   diff, the delta, and the grounding findings.
2. ``show`` prints a stored proposal again. Nothing is generated.
3. ``apply`` re-verifies a stored proposal (the candidate commit, every
   page's current bytes, every symbol's current hash, and grounding) and only
   if all of it holds writes exactly the proposed bytes of the ready pages.
   It never generates.

Gating, the delta prompt, the splice, and the grounding check are refill's
own, so both paths follow one contract. Pages whose own source did not change
but a neighbour's did (``affected``) are listed for review and never
proposed; stale pages without a symbol (io and output-family pages) and
orphaned pages are listed for a manual update. The proposal is meant to be
committed with the pages it changes, as the record of why each one changed.
"""

from __future__ import annotations

import difflib
import hashlib
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .docs.grounding import Finding, check_page
from .docs.pages import load_all, load_page, parse_page
from .docs.staleness import compute_status
from .generation import refill
from .parser.facts import FactStore
from .parser.fortran import fparser_version
from .provenance.records import SourceProvenance
from .source.config import Config

FORMAT = "swatref-maintain-proposal/1"

# Page statuses in a proposal. Only READY pages are ever written.
READY = "ready"
REJECTED = "rejected"  # the merged page has grounding errors
REFUSED = "refused"    # wrong baseline, or the generator declined
SKIPPED = "skipped"    # not stale, symbol gone, or outside the docs directory
ERROR = "error"
STATUSES = (READY, REJECTED, REFUSED, SKIPPED, ERROR)
FAILED = (REJECTED, REFUSED, ERROR)


class Declined(Exception):
    """The generator produced no delta for a page; the message says why."""


Generator = Callable[[refill.DeltaRequest], dict]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _inside(path: Path, root: Path) -> bool:
    return path.resolve().is_relative_to(root.resolve())


# --------------------------------------------------------------------------
# Delta generators
# --------------------------------------------------------------------------

def model_generator(cfg: Config, model: str | None = None) -> tuple[Generator, dict]:
    """Deltas from the Claude API: the same request `refill` makes."""
    import anthropic

    client = anthropic.Anthropic()

    def generate(req: refill.DeltaRequest) -> dict:
        delta = refill.request_delta(client, cfg, req.prompt, model)
        if delta is None:
            raise Declined("the model declined")
        return delta

    return generate, {"kind": "model", "model": model or cfg.fill.model}


def deltas_generator(path: Path, root: Path) -> tuple[Generator, dict]:
    """Deltas from a hand-authored ``{symbol: delta}`` JSON (key-free)."""
    raw = path.read_bytes()
    deltas = json.loads(raw)

    def generate(req: refill.DeltaRequest) -> dict:
        if req.page.symbol not in deltas:
            raise Declined(f"no delta for `{req.page.symbol}` in {path.name}")
        return deltas[req.page.symbol]

    return generate, {"kind": "deltas_file", "path": _rel(path, root), "sha256": _sha256(raw)}


# --------------------------------------------------------------------------
# Propose
# --------------------------------------------------------------------------

def _patch(before: str, after: str, path: str) -> str:
    return "\n".join(difflib.unified_diff(
        before.splitlines(), after.splitlines(),
        fromfile=f"a/{path}", tofile=f"b/{path}", lineterm="",
    ))


def _propose_page(
    cfg: Config,
    store: FactStore,
    old_store: FactStore,
    old_source_dir: Path,
    generate: Generator,
    path: Path,
) -> dict:
    entry: dict = {"path": _rel(path, cfg.root), "status": ERROR}
    try:
        if not _inside(path, cfg.abs_docs_dir):
            entry.update(status=SKIPPED, reason="not under the docs directory")
            return entry
        original = path.read_bytes()
        page = load_page(path)
        entry.update(symbol=page.symbol, page_sha256=_sha256(original))
        req = refill.prepare_delta(cfg, store, old_store, old_source_dir, page)
        if req.outcome:
            entry.update(status=REFUSED if req.outcome == "REFUSED" else SKIPPED,
                         reason=req.reason)
            return entry
        entry.update(
            old_source_hash=page.source_hash,
            new_source_hash=req.sym.source_hash,
            evidence=[{"kind": "source_diff", "file": req.sym.file, "diff": req.diff}],
        )
        delta = generate(req)
        dropped, findings = refill.merge_delta(cfg, store, page, req.sym, delta)
        proposed = page.dumps()
        errors = [asdict(f) for f in findings if f.level == "error"]
        entry.update(
            delta=delta,
            changed_fields=[k for k, v in delta.items() if v],
            dropped_notes=dropped,
            grounding={
                "errors": errors,
                "warnings": [asdict(f) for f in findings if f.level != "error"],
            },
            patch=_patch(original.decode("utf-8"), proposed, entry["path"]),
            proposed=proposed,
            proposed_sha256=_sha256(proposed.encode("utf-8")),
        )
        if errors:
            entry.update(status=REJECTED, reason="grounding errors; will not be applied")
        else:
            entry["status"] = READY
    except Declined as exc:
        entry.update(status=REFUSED, reason=str(exc))
    except Exception as exc:  # noqa: BLE001 — one page failing shouldn't kill the run
        entry.update(status=ERROR, reason=f"{type(exc).__name__}: {exc}")
    return entry


def propose(
    cfg: Config,
    store: FactStore,
    old_store: FactStore,
    old_source_dir: Path,
    base: SourceProvenance,
    candidate: SourceProvenance,
    generate: Generator,
    generator: dict,
    paths: list[Path] | None = None,
    limit: int | None = None,
) -> dict:
    """Build a proposal for every stale symbol page (or just ``paths``). Writes nothing.

    ``store``/``cfg`` describe the candidate; ``old_store``/``old_source_dir``
    the base. Each page's delta is generated exactly once, here.
    """
    report = compute_status(store, load_all(cfg.abs_docs_dir))
    if paths:
        targets = list(paths)
    else:
        stale = [p.path for p in report.stale if p.symbol]
        targets = stale[:limit] if limit else stale

    def one(path: Path) -> dict:
        return _propose_page(cfg, store, old_store, old_source_dir, generate, path)

    with ThreadPoolExecutor(max_workers=cfg.fill.concurrency) as pool:
        pages = list(pool.map(one, targets))

    manual = [
        {"path": _rel(p.path, cfg.root),
         "reason": "stale, but has no symbol; refill revises symbol pages only"}
        for p in report.stale if not p.symbol
    ] + [
        {"path": _rel(p.path, cfg.root),
         "reason": "its source no longer exists in the candidate"}
        for p in report.orphaned
    ]
    return {
        "format": FORMAT,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base": base.to_dict(),
        "candidate": candidate.to_dict(),
        "docs": {
            "dir": _rel(cfg.abs_docs_dir, cfg.root),
            "engine": cfg.docs_engine,
            "fparser": fparser_version(),
            "version_label": cfg.version_label,
        },
        "generator": generator,
        "pages": pages,
        "review_only": [
            {"path": _rel(p.path, cfg.root), "symbol": p.symbol,
             "changed": report.affected_by.get(p.path.name, [])}
            for p in report.affected
        ],
        "manual": manual,
    }


def has_failures(proposal: dict) -> bool:
    """True when a stale page could not be proposed (refused, rejected, or errored)."""
    return any(p["status"] in FAILED for p in proposal["pages"])


def write_proposal(path: Path, proposal: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(proposal, indent=2, ensure_ascii=False) + "\n"
    path.write_bytes(text.encode("utf-8"))


def load_proposal(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"no proposal at {path}; run `swatref docs maintain propose` first"
        )
    proposal = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(proposal, dict) or proposal.get("format") != FORMAT:
        raise ValueError(f"{path} is not a {FORMAT} proposal")
    return proposal


# --------------------------------------------------------------------------
# Preview
# --------------------------------------------------------------------------

def _indent(text: str, by: int) -> list[str]:
    return [" " * by + line for line in text.splitlines()]


def render(proposal: dict) -> str:
    """The human preview of a proposal: exactly what apply would write, and why."""
    base, cand, gen = proposal["base"], proposal["candidate"], proposal["generator"]
    out = [
        f"Proposal: {base['profile']} @ {base['resolved_commit'][:12]} -> "
        f"{cand['profile']} @ {cand['resolved_commit'][:12]}",
        f"Deltas from {gen.get('model') or gen.get('path')}, {proposal['created_at']}",
        "",
    ]
    for p in proposal["pages"]:
        head = f"{p['status'].upper()} {p['path']}"
        if p["status"] != READY:
            out.append(f"{head}: {p.get('reason', '')}")
            out += [f"  {Finding(**f)}" for f in p.get("grounding", {}).get("errors", [])]
            out.append("")
            continue
        out.append(head)
        out.append(f"  Why: the source of `{p['symbol']}` changed:")
        for evidence in p["evidence"]:
            out += _indent(evidence["diff"], 4)
        out.append("  Proposed change:")
        out += _indent(p["patch"], 4)
        if p["dropped_notes"]:
            out.append(f"  Drops notes the parser no longer sees: {', '.join(p['dropped_notes'])}")
        out += [f"  {Finding(**f)}" for f in p["grounding"]["warnings"]]
        out.append("")
    if proposal["review_only"]:
        out.append("Review only (a dependency changed; these pages are not rewritten):")
        out += [f"  {r['path']}  (changed: {', '.join(r['changed'])})"
                for r in proposal["review_only"]]
        out.append("")
    if proposal["manual"]:
        out.append("Needs a manual update:")
        out += [f"  {m['path']}  ({m['reason']})" for m in proposal["manual"]]
        out.append("")
    counts = Counter(p["status"] for p in proposal["pages"])
    summary = ", ".join(f"{counts[s]} {s}" for s in STATUSES if counts[s]) or "no stale pages"
    out.append(
        f"{summary}; {len(proposal['review_only'])} for review only; "
        f"{len(proposal['manual'])} need a manual update"
    )
    if counts[READY]:
        out.append("Apply exactly these changes with `swatref docs maintain apply`.")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# Apply
# --------------------------------------------------------------------------

def _verify(entry: dict, target: Path, docs_dir: Path, store: FactStore) -> tuple[str, list[str]]:
    """``("write", warnings)``, ``("already", [])``, or ``("problem", reasons)``."""
    proposed = entry["proposed"].encode("utf-8")
    if not _inside(target, docs_dir):
        return "problem", ["is not under the docs directory"]
    if _sha256(proposed) != entry["proposed_sha256"]:
        return "problem", ["proposed content does not match its recorded hash"]
    if not target.exists():
        return "problem", ["page no longer exists"]
    sym = store.get(entry["symbol"])
    if sym is None or sym.source_hash != entry["new_source_hash"]:
        return "problem", [f"the source of `{entry['symbol']}` changed since the proposal"]
    current = _sha256(target.read_bytes())
    if current == entry["proposed_sha256"]:
        return "already", []
    if current != entry["page_sha256"]:
        return "problem", ["page changed since the proposal"]
    findings = check_page(store, parse_page(target, entry["proposed"]))
    errors = [str(f) for f in findings if f.level == "error"]
    if errors:
        return "problem", errors
    return "write", [str(f) for f in findings]


def apply(
    cfg: Config, store: FactStore, candidate: SourceProvenance, proposal: dict
) -> tuple[bool, list[str]]:
    """Write the ready pages of a stored proposal, or nothing if any check fails.

    ``store`` and ``candidate`` describe the docs source now. Every ready page
    is verified before the first write; apply never generates.
    """
    planned = proposal["candidate"]
    if (planned["profile"], planned["resolved_commit"]) != (
        candidate.profile, candidate.resolved_commit
    ):
        return False, [
            f"REFUSED: the proposal was made for {planned['profile']} @ "
            f"{planned['resolved_commit'][:12]}, but the docs source is now "
            f"{candidate.profile} @ {candidate.resolved_commit[:12]}. Nothing was "
            "written; run `swatref docs maintain propose` again."
        ]

    lines: list[str] = []
    problems: list[str] = []
    writes: list[tuple[Path, bytes]] = []
    for entry in proposal["pages"]:
        if entry["status"] != READY:
            lines.append(f"NOT APPLIED {entry['path']}: {entry['status']} in the proposal")
            continue
        target = cfg.root / entry["path"]
        try:
            action, detail = _verify(entry, target, cfg.abs_docs_dir, store)
        except (KeyError, TypeError) as exc:
            action, detail = "problem", [f"proposal entry is incomplete ({exc})"]
        if action == "problem":
            problems.append(f"REFUSED {entry['path']}: " + "\n  ".join(detail))
        elif action == "already":
            lines.append(f"ALREADY APPLIED {entry['path']}")
        else:
            writes.append((target, entry["proposed"].encode("utf-8")))
            lines.append(f"APPLIED {entry['path']}" + "".join(f"\n  {w}" for w in detail))

    if problems:
        return False, problems + [
            f"{len(problems)} page(s) failed verification. Nothing was written; "
            "run `swatref docs maintain propose` again."
        ]
    for target, data in writes:
        target.write_bytes(data)
    lines.append(f"{len(writes)} page(s) written")
    return True, lines
