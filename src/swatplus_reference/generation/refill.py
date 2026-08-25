"""Segment-aware re-fill for stale pages.

The full-fill path (`fill.py`) regenerates *every* prose field of a page from
the new source. On a version bump that rewrites reviewed prose describing code
that never changed, and — because generation is non-deterministic — the
unchanged parts come back reworded. Delta re-fill fixes that:

1. Reconstruct the page's existing prose as a structured ``data`` dict
   (`page_to_data`, the inverse of `fill.result_to_page`).
2. Diff the symbol's old source slice against the new one.
3. Ask the model to return **only** the prose fields the diff actually
   affects; every field it omits is preserved *verbatim* from the existing
   prose (`merge_delta`).
4. Merge and write through the same grounding gate as a full fill.

Parser-owned facts (signatures, call graph, links, line numbers) are injected
at render time and never regenerated here, so the structural half of the page
was already drift-proof; this makes the prose half drift-proof too.

Key-free path: `emit_delta_prompts` writes one prompt per stale page and
`apply_delta_file` merges a hand-authored ``{symbol: delta}`` JSON — so a
Claude session (or any executor) can fill without an API key. `run_refill`
is the API-backed equivalent.
"""

from __future__ import annotations

import difflib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ..docs.pages import Page, load_page
from ..parser.facts import FactStore, Symbol
from ..source.config import Config
from .fill import (
    FILL_SCHEMA,
    SYSTEM_PROMPT,
    build_fact_sheet,
    drop_ungrounded_notes,
)

# Body section anchors written by fill.result_to_page (both templates).
_HEADER = "<!-- facts:header -->"

# Prose fields that carry over verbatim when the delta omits them.
SCALAR_FIELDS = ("short_description", "bottom_line", "where_it_fits")
LIST_FIELDS = ("algorithm", "state_changes")
NOTE_FIELDS = {
    "arg_notes": "args",
    "local_notes": "locals",
    "use_notes": "uses",
    "variable_notes": "variables",
}


# --------------------------------------------------------------------------
# Inverse of result_to_page: rendered page -> structured prose data
# --------------------------------------------------------------------------

def _section(body: str, start: str, ends: tuple[str, ...] = ()) -> str:
    """Text after the line ``start`` up to the next section (exclusive).

    A section ends at the next ``## `` heading or ``<!-- facts:`` marker (the
    generic terminators), so this is robust to migrated pages that carry extra
    sections between the fill-managed ones.
    """
    lines = body.splitlines()
    try:
        i = next(k for k, ln in enumerate(lines) if ln.strip() == start)
    except StopIteration:
        return ""
    out: list[str] = []
    for ln in lines[i + 1 :]:
        s = ln.strip()
        if s.startswith("## ") or s.startswith("<!-- facts:"):
            break
        out.append(ln)
    return "\n".join(out).strip()


def _parse_table(block: str) -> list[dict]:
    """Parse a fill.table() block back into row dicts (empty if 'Not documented')."""
    rows: list[str] = [l for l in block.splitlines() if l.strip().startswith("|")]
    if len(rows) < 2:
        return []
    header = [c.strip() for c in rows[0].strip("|").split("|")]
    out: list[dict] = []
    for r in rows[2:]:  # skip header + separator
        cells = [c.strip().replace("\\|", "|") for c in r.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        out.append(dict(zip(header, cells)))
    return out


def _unbacktick(s: str) -> str:
    s = s.strip()
    return s[1:-1] if len(s) >= 2 and s[0] == "`" and s[-1] == "`" else s


def page_to_data(page: Page) -> dict:
    """Reconstruct the structured prose ``data`` dict from a filled page.

    Round-trips with fill.result_to_page: feeding the result back through it
    reproduces the same body and extra.
    """
    body = page.body
    data: dict = {
        "short_description": _section(body, _HEADER),
        "bottom_line": _section(body, "## Bottom Line"),
        "where_it_fits": _section(body, "## Where It Fits"),
    }

    algo_block = _section(body, "## Algorithm")
    data["algorithm"] = [
        {"step": r.get("Step", ""), "behavior": r.get("What happens", "")}
        for r in _parse_table(algo_block)
    ]
    state_block = _section(body, "## State Changes")
    data["state_changes"] = [
        {
            "target": _unbacktick(r.get("Target", "")),
            "condition": r.get("When", ""),
            "meaning": r.get("Meaning", ""),
        }
        for r in _parse_table(state_block)
    ]

    for field, extra_key in NOTE_FIELDS.items():
        data[field] = [
            {"name": name, "note": note}
            for name, note in (page.extra.get(extra_key) or {}).items()
        ]
    return data


# --------------------------------------------------------------------------
# Delta merge + diff + prompt
# --------------------------------------------------------------------------

def _render_table(rows: list[dict], cols: list[tuple[str, str]]) -> str:
    if not rows:
        return "*Not documented.*"
    out = ["| " + " | ".join(t for _, t in cols) + " |",
           "| " + " | ".join("---" for _ in cols) + " |"]
    for r in rows:
        out.append("| " + " | ".join(
            str(r.get(k, "")).replace("\n", " ").replace("|", "\\|") for k, _ in cols
        ) + " |")
    return "\n".join(out)


def _replace_body_section(body: str, anchor: str, new_text: str) -> str:
    """Replace the block after ``anchor`` up to the next section, leave the rest.

    ``anchor`` is a line matched exactly (a ``## Heading`` or a marker). The
    block ends at the next ``## `` heading or ``<!-- facts:`` marker, or EOF.
    If the anchor is absent the body is returned unchanged — a delta never
    invents a section that the page does not already have.
    """
    lines = body.splitlines()
    try:
        i = next(k for k, ln in enumerate(lines) if ln.strip() == anchor)
    except StopIteration:
        return body
    j = len(lines)
    for k in range(i + 1, len(lines)):
        s = lines[k].strip()
        if s.startswith("## ") or s.startswith("<!-- facts:"):
            j = k
            break
    head = lines[: i + 1]
    tail = lines[j:]
    return "\n".join(head + ["", new_text.strip(), ""] + tail)


def splice_delta(page: Page, sym: Symbol, delta: dict) -> None:
    """Apply only the changed fields by section-level surgery.

    Every section the delta does not name — including additional curated sections
    (Theory Equations, Lineage, Review Notes, the outside-state table) and any
    unchanged prose — is preserved byte-for-byte. Note fields update individual
    entries in the frontmatter maps, leaving unnamed entries untouched.
    """
    body = page.body
    if "short_description" in delta and delta["short_description"]:
        body = _replace_body_section(body, _HEADER, delta["short_description"].strip())
    if "bottom_line" in delta and delta["bottom_line"]:
        body = _replace_body_section(body, "## Bottom Line", delta["bottom_line"].strip())
    if "where_it_fits" in delta and delta["where_it_fits"]:
        body = _replace_body_section(body, "## Where It Fits", delta["where_it_fits"].strip())
    if "algorithm" in delta and delta["algorithm"] is not None:
        body = _replace_body_section(
            body, "## Algorithm",
            _render_table(
                [{"step": s.get("step", ""), "behavior": s.get("behavior", "")}
                 for s in delta["algorithm"]],
                [("step", "Step"), ("behavior", "What happens")],
            ),
        )
    if "state_changes" in delta and delta["state_changes"] is not None:
        body = _replace_body_section(
            body, "## State Changes",
            _render_table(
                [{"target": f"`{s.get('target','')}`", "condition": s.get("condition", ""),
                  "meaning": s.get("meaning", "")} for s in delta["state_changes"]],
                [("target", "Target"), ("condition", "When"), ("meaning", "Meaning")],
            ),
        )
    page.body = body

    for field, key in NOTE_FIELDS.items():
        if field not in delta or delta[field] is None:
            continue
        current = dict(page.extra.get(key) or {})
        for entry in delta[field]:
            name = (entry.get("name") or "").lower()
            if name and entry.get("note"):
                current[name] = entry["note"].strip()
        if current:
            page.extra[key] = current

    # Derived-type component notes: [{type, component, note}] -> nested map,
    # updating individual entries and preserving the rest.
    if delta.get("type_component_notes"):
        tc = {t: dict(c) for t, c in (page.extra.get("type_components") or {}).items()}
        for entry in delta["type_component_notes"]:
            t = (entry.get("type") or "").lower()
            c = (entry.get("component") or "").lower()
            if t and c and entry.get("note"):
                tc.setdefault(t, {})[c] = entry["note"].strip()
        if tc:
            page.extra["type_components"] = tc

    page.source_hash = sym.source_hash


def symbol_source_diff(
    old_sym: Symbol | None,
    new_sym: Symbol,
    old_source_dir: Path,
    new_source_dir: Path,
) -> str:
    """Unified diff of a symbol's own source slice, old ref -> new ref."""

    def slice_of(sym: Symbol | None, root: Path) -> list[str]:
        if sym is None:
            return []
        text = (root / sym.file).read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        return [l + "\n" for l in lines[sym.start_line - 1 : sym.end_line]]

    old = slice_of(old_sym, old_source_dir)
    new = slice_of(new_sym, new_source_dir)
    diff = difflib.unified_diff(old, new, fromfile="old", tofile="new", n=2)
    return "".join(diff).strip() or "(no textual difference in the symbol slice)"


DELTA_SYSTEM = SYSTEM_PROMPT + (
    "\n\nYou are REVISING an existing page after a source change. You are given "
    "the current prose (JSON) and a unified diff of this symbol's source. Return "
    "ONLY the fields whose accuracy is affected by the diff; omit every field "
    "that is still correct — omitted fields are kept exactly as-is. Do not "
    "reword unaffected prose. Return the same JSON schema, with unaffected keys "
    "left out entirely."
)


def build_delta_prompt(existing_data: dict, diff: str, fact_sheet: str) -> str:
    return (
        "Revise only what the source change affects. Return partial JSON: just "
        "the changed fields.\n\n"
        "## Current prose (JSON)\n```json\n"
        + json.dumps(existing_data, indent=1, ensure_ascii=False)
        + "\n```\n\n## Source change (unified diff)\n```diff\n"
        + diff
        + "\n```\n\n## Current facts\n"
        + fact_sheet
    )


# --------------------------------------------------------------------------
# Apply
# --------------------------------------------------------------------------

def _apply_and_ground(store: FactStore, page: Page, sym: Symbol, delta: dict) -> list[str]:
    splice_delta(page, sym, delta)
    dropped = drop_ungrounded_notes(store, page)
    page.save()
    return dropped


def emit_delta_prompts(
    cfg: Config,
    store: FactStore,
    old_store: FactStore,
    old_source_dir: Path,
    paths: list[Path],
    out_dir: Path,
) -> list[str]:
    """Write one delta prompt per stale page (key-free executor input)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for p in paths:
        page = load_page(p)
        sym = store.get(page.symbol)
        if sym is None:
            results.append(f"SKIP {page.name}: gone in new source")
            continue
        existing = page_to_data(page)
        diff = symbol_source_diff(
            old_store.get(page.symbol), sym, old_source_dir, cfg.abs_source_dir
        )
        prompt = build_delta_prompt(existing, diff, build_fact_sheet(cfg, store, sym))
        (out_dir / f"{page.symbol}.delta.md").write_text(prompt, encoding="utf-8")
        results.append(f"PROMPT {page.symbol}")
    return results


def apply_delta_file(cfg: Config, store: FactStore, deltas_path: Path) -> list[str]:
    """Apply a hand-authored ``{symbol: {field: value}}`` delta JSON (key-free)."""
    deltas = json.loads(deltas_path.read_text(encoding="utf-8"))
    docs = cfg.abs_docs_dir
    results = []
    for symbol, delta in deltas.items():
        sym = store.get(symbol)
        if sym is None:
            results.append(f"SKIP {symbol}: not in fact store")
            continue
        page_path = _find_page(docs, symbol)
        if page_path is None:
            results.append(f"SKIP {symbol}: no page")
            continue
        page = load_page(page_path)
        dropped = _apply_and_ground(store, page, sym, delta)
        note = f" (dropped: {', '.join(dropped)})" if dropped else ""
        results.append(f"REFILLED {symbol}{note}")
    return results


def _find_page(docs_dir: Path, symbol: str) -> Path | None:
    for sub in ("procedures", "modules"):
        cand = docs_dir / sub / f"{symbol}.md"
        if cand.exists():
            return cand
    return None


def run_refill(
    cfg: Config,
    store: FactStore,
    old_store: FactStore,
    old_source_dir: Path,
    paths: list[Path],
    model: str | None = None,
    dry_run: bool = False,
) -> list[str]:
    """API-backed delta re-fill (mirrors fill.run_fill, delta prompt)."""
    import anthropic

    client = anthropic.Anthropic()

    def one(path: Path) -> str:
        page = load_page(path)
        sym = store.get(page.symbol)
        if sym is None:
            return f"SKIP {page.name}: gone in new source"
        existing = page_to_data(page)
        diff = symbol_source_diff(
            old_store.get(page.symbol), sym, old_source_dir, cfg.abs_source_dir
        )
        prompt = build_delta_prompt(existing, diff, build_fact_sheet(cfg, store, sym))
        if dry_run:
            return f"DRY {page.symbol}: delta prompt {len(prompt)} chars"
        resp = client.messages.create(
            model=model or cfg.fill.model,
            max_tokens=cfg.fill.max_tokens,
            system=DELTA_SYSTEM,
            output_config={"format": {"type": "json_schema", "schema": _partial_schema()}},
            messages=[{"role": "user", "content": prompt}],
        )
        if resp.stop_reason == "refusal":
            return f"REFUSED {page.symbol}"
        text = next(b.text for b in resp.content if b.type == "text")
        delta = json.loads(text)
        dropped = _apply_and_ground(store, page, sym, delta)
        changed = ", ".join(k for k in delta if delta[k] not in (None, [], ""))
        note = f" (dropped: {', '.join(dropped)})" if dropped else ""
        return f"REFILLED {page.symbol} [{changed}]{note}"

    results: list[str] = []
    with ThreadPoolExecutor(max_workers=cfg.fill.concurrency) as pool:
        for r in pool.map(one, paths):
            results.append(r)
    return results


def _partial_schema() -> dict:
    """FILL_SCHEMA with nothing required — the model returns only changed fields."""
    schema = json.loads(json.dumps(FILL_SCHEMA))
    schema["required"] = []
    return schema
