"""Prose fill via the Claude API.

Fills `todo` pages and refreshes `stale` ones. The model receives a fact
sheet (numbered source slice + parser facts) and returns only prose, as
JSON constrained by a schema (structured outputs). Two rules are enforced
by construction and checked afterwards:

- prose references symbols, never file:line locations;
- structured notes may only name args/locals/modules the parser sees
  (grounding check runs on every filled page before it is saved).
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic

from ..docs.grounding import check_page
from ..docs.pages import STATUS_FILLED, Page, load_page
from ..parser.facts import FactStore, Symbol
from ..source.config import Config

FILL_SCHEMA = {
    "type": "object",
    "properties": {
        "short_description": {
            "type": "string",
            "description": "One- or two-sentence summary of what this symbol does.",
        },
        "bottom_line": {
            "type": "string",
            "description": "Two short paragraphs: what it computes and why it matters.",
        },
        "where_it_fits": {
            "type": "string",
            "description": "Where this runs in the SWAT+ control flow and what consumes its results.",
        },
        "algorithm": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "step": {"type": "string"},
                    "behavior": {"type": "string"},
                },
                "required": ["step", "behavior"],
                "additionalProperties": False,
            },
        },
        "arg_notes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["name", "note"],
                "additionalProperties": False,
            },
        },
        "local_notes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["name", "note"],
                "additionalProperties": False,
            },
        },
        "use_notes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["name", "note"],
                "additionalProperties": False,
            },
        },
        "variable_notes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["name", "note"],
                "additionalProperties": False,
            },
        },
        "state_changes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "target": {"type": "string"},
                    "condition": {"type": "string"},
                    "meaning": {"type": "string"},
                },
                "required": ["target", "condition", "meaning"],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "short_description",
        "bottom_line",
        "where_it_fits",
        "algorithm",
        "arg_notes",
        "local_notes",
        "use_notes",
        "variable_notes",
        "state_changes",
    ],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """\
You are documenting the SWAT+ hydrological model's Fortran source for \
scientists and model users. You write from evidence: every claim must be \
supported by the source and facts provided.

Hard rules:
- NEVER cite file names or line numbers in prose (no "file.f90:123"). \
Refer to code by symbol name in backticks; links are generated later.
- Only name identifiers that appear in the provided source or fact sheet.
- In arg_notes/local_notes/use_notes/variable_notes, `name` must exactly \
match an identifier from the fact sheet (lowercase). Do not invent entries.
- Prefer hydrological meaning over restating code: say what a variable \
represents physically, not just how it is assigned.
- If the evidence does not support a section, return an empty array or a \
short honest statement — never guess."""


def build_fact_sheet(cfg: Config, store: FactStore, sym: Symbol) -> str:
    src_path = cfg.abs_source_dir / sym.file
    lines = src_path.read_text(encoding="utf-8", errors="replace").splitlines()
    slice_lines = lines[sym.start_line - 1 : sym.end_line]
    numbered = "\n".join(
        f"{n:5d} | {l}" for n, l in enumerate(slice_lines, start=sym.start_line)
    )

    parts = [f"# Symbol: {sym.qualified} ({sym.kind}) in {sym.file}", ""]
    if sym.args:
        parts.append("## Arguments")
        parts += [f"- {a.name}: {a.decl or 'undeclared'}" for a in sym.args]
    if sym.locals:
        parts.append("## Locals")
        parts += [f"- {v.name}: {v.decl}" for v in sym.locals]
    if sym.variables:
        parts.append("## Module variables")
        parts += [f"- {v.name}: {v.decl}" for v in sym.variables]
    if sym.uses:
        parts.append("## Modules used")
        for u in sym.uses:
            only = f" (only: {', '.join(u.only)})" if u.only else ""
            parts.append(f"- {u.module}{only}")
    if sym.calls:
        parts.append("## Calls")
        for c in sym.calls:
            callee = store.get(c)
            sig = f"({', '.join(a.name for a in callee.args)})" if callee else ""
            parts.append(f"- {c}{sig}")
    callers = store.callers_of(sym.name)
    if callers:
        parts.append("## Called by")
        parts += [f"- {c.name}" for c in callers[:30]]
    members = store.members_of(sym.name)
    if members:
        parts.append("## Contains")
        parts += [f"- {m.kind} {m.name}" for m in members]

    parts += ["", "## Source", "```fortran", numbered, "```"]
    return "\n".join(parts)


PAGE_BODY = """\
<!-- facts:header -->

{short_description}

## Bottom Line

{bottom_line}

## Arguments

<!-- facts:arguments -->

## Where It Fits

{where_it_fits}

<!-- facts:calls -->

## Algorithm

{algorithm}

## Modules Used

<!-- facts:uses -->

## Local Variables

<!-- facts:locals -->

## State Changes

{state_changes}

## File I/O

<!-- facts:io -->"""

MODULE_PAGE_BODY = """\
<!-- facts:header -->

{short_description}

## Bottom Line

{bottom_line}

## Where It Fits

{where_it_fits}

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->"""


def result_to_page(page: Page, sym: Symbol, data: dict) -> None:
    def table(rows: list[dict], cols: list[tuple[str, str]]) -> str:
        if not rows:
            return "*Not documented.*"
        out = ["| " + " | ".join(t for _, t in cols) + " |",
               "| " + " | ".join("---" for _ in cols) + " |"]
        for r in rows:
            out.append(
                "| " + " | ".join(
                    str(r.get(k, "")).replace("\n", " ").replace("|", "\\|")
                    for k, _ in cols
                ) + " |"
            )
        return "\n".join(out)

    algorithm = table(data.get("algorithm", []), [("step", "Step"), ("behavior", "What happens")])
    state = table(
        [
            {"target": f"`{s['target']}`", "condition": s["condition"], "meaning": s["meaning"]}
            for s in data.get("state_changes", [])
        ],
        [("target", "Target"), ("condition", "When"), ("meaning", "Meaning")],
    )

    template = MODULE_PAGE_BODY if sym.kind == "module" else PAGE_BODY
    page.body = template.format(
        short_description=data.get("short_description", "").strip(),
        bottom_line=data.get("bottom_line", "").strip(),
        where_it_fits=data.get("where_it_fits", "").strip(),
        algorithm=algorithm,
        state_changes=state,
    )

    def notes_map(key: str) -> dict:
        return {
            e["name"].lower(): e["note"].strip()
            for e in data.get(key, [])
            if e.get("name") and e.get("note")
        }

    page.extra = {}
    if notes_map("arg_notes"):
        page.extra["args"] = notes_map("arg_notes")
    if notes_map("local_notes"):
        page.extra["locals"] = notes_map("local_notes")
    if notes_map("use_notes"):
        page.extra["uses"] = notes_map("use_notes")
    if sym.kind == "module" and notes_map("variable_notes"):
        page.extra["variables"] = notes_map("variable_notes")

    page.status = STATUS_FILLED
    page.source_hash = sym.source_hash


def drop_ungrounded_notes(store: FactStore, page: Page) -> list[str]:
    """Remove structured-note entries the parser can't see; return findings."""
    dropped = []
    for finding in check_page(store, page):
        if finding.level == "error" and finding.code.startswith("unknown-"):
            for key in ("args", "locals", "uses", "variables"):
                notes = page.extra.get(key) or {}
                for entry in list(notes):
                    if f"`{entry}`" in finding.message:
                        notes.pop(entry, None)
                        dropped.append(f"{key}:{entry}")
    return dropped


def fill_page(
    cfg: Config,
    store: FactStore,
    client: anthropic.Anthropic,
    page: Page,
    model: str | None = None,
    dry_run: bool = False,
) -> str:
    sym = store.get(page.symbol)
    if sym is None:
        return f"SKIP {page.name}: no symbol in fact store"
    fact_sheet = build_fact_sheet(cfg, store, sym)
    if dry_run:
        return f"DRY {page.name}: prompt {len(fact_sheet)} chars"

    response = client.messages.create(
        model=model or cfg.fill.model,
        max_tokens=cfg.fill.max_tokens,
        system=SYSTEM_PROMPT,
        output_config={"format": {"type": "json_schema", "schema": FILL_SCHEMA}},
        messages=[
            {
                "role": "user",
                "content": (
                    "Document this symbol. Return the JSON fields; prose in "
                    "GitHub Markdown, identifiers in backticks.\n\n" + fact_sheet
                ),
            }
        ],
    )
    if response.stop_reason == "refusal":
        return f"REFUSED {page.name}"
    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
    result_to_page(page, sym, data)
    dropped = drop_ungrounded_notes(store, page)
    page.save()
    note = f" (dropped ungrounded: {', '.join(dropped)})" if dropped else ""
    return f"FILLED {page.name}{note}"


def run_fill(
    cfg: Config,
    store: FactStore,
    paths: list[Path],
    model: str | None = None,
    dry_run: bool = False,
) -> list[str]:
    client = anthropic.Anthropic()
    pages = [load_page(p) for p in paths]
    results: list[str] = []
    with ThreadPoolExecutor(max_workers=cfg.fill.concurrency) as pool:
        futures = [
            pool.submit(fill_page, cfg, store, client, page, model, dry_run)
            for page in pages
        ]
        for fut in futures:
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001 — one page failing shouldn't kill the run
                results.append(f"ERROR {type(exc).__name__}: {exc}")
    return results
