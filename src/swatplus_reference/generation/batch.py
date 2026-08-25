"""Bulk fill via the Anthropic Message Batches API (50% cheaper).

The batch path and the interactive path (`fill.py`) share everything that
matters: the same fact-sheet prompt, the same JSON schema, and the same
grounded merge (`result_to_page` + `drop_ungrounded_notes`). Batch is the
right tool for corpus-scale work — initial backfills, version bumps with
many stale pages; interactive fill is for the tail.

Workflow:

    swatref docs batch submit [--limit N] [PAGE ...]   # build + submit requests
    swatref docs batch status [BATCH_ID]               # poll progress
    swatref docs batch merge BATCH_ID                  # fetch results into pages

Submission state (batch id -> page paths) is recorded under
`.swatref/docs/batches/<id>.json` so merge works in a later session.
"""

from __future__ import annotations

import json
from pathlib import Path

import anthropic

from ..docs.pages import Page, load_page
from ..parser.facts import FactStore
from ..source.config import Config
from .fill import FILL_SCHEMA, SYSTEM_PROMPT, build_fact_sheet, drop_ungrounded_notes, result_to_page


def _batch_dir(cfg: Config) -> Path:
    return cfg.abs_facts_path.parent / "batches"


def build_request(cfg: Config, store: FactStore, page: Page, model: str | None) -> dict:
    sym = store.get(page.symbol)
    fact_sheet = build_fact_sheet(cfg, store, sym)
    return {
        "custom_id": page.symbol,
        "params": {
            "model": model or cfg.fill.model,
            "max_tokens": cfg.fill.max_tokens,
            "system": SYSTEM_PROMPT,
            "output_config": {
                "format": {"type": "json_schema", "schema": FILL_SCHEMA}
            },
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Document this symbol. Return the JSON fields; prose in "
                        "GitHub Markdown, identifiers in backticks.\n\n" + fact_sheet
                    ),
                }
            ],
        },
    }


def submit(
    cfg: Config,
    store: FactStore,
    paths: list[Path],
    model: str | None = None,
    dry_run: bool = False,
) -> str:
    pages = [load_page(p) for p in paths]
    pages = [p for p in pages if p.symbol and store.get(p.symbol)]
    requests = [build_request(cfg, store, p, model) for p in pages]
    if dry_run:
        total = sum(len(json.dumps(r)) for r in requests)
        print(f"DRY: {len(requests)} requests, ~{total // 1024} KiB payload")
        return ""

    client = anthropic.Anthropic()
    batch = client.messages.batches.create(requests=requests)

    state = {
        "batch_id": batch.id,
        "model": model or cfg.fill.model,
        "pages": {p.symbol: str(p.path) for p in pages},
    }
    out = _batch_dir(cfg) / f"{batch.id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(f"submitted {len(requests)} requests as {batch.id} ({batch.processing_status})")
    print(f"state: {out}")
    return batch.id


def load_state(cfg: Config, batch_id: str) -> dict:
    path = _batch_dir(cfg) / f"{batch_id}.json"
    if not path.exists():
        raise SystemExit(f"no submission state at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def status(cfg: Config, batch_id: str | None) -> None:
    client = anthropic.Anthropic()
    if batch_id:
        ids = [batch_id]
    else:
        ids = sorted(p.stem for p in _batch_dir(cfg).glob("*.json"))
        if not ids:
            print("no recorded batches")
            return
    for bid in ids:
        batch = client.messages.batches.retrieve(bid)
        counts = batch.request_counts
        print(
            f"{bid}: {batch.processing_status} "
            f"(processing={counts.processing} succeeded={counts.succeeded} "
            f"errored={counts.errored} expired={counts.expired})"
        )


def merge(cfg: Config, store: FactStore, batch_id: str) -> list[str]:
    state = load_state(cfg, batch_id)
    page_by_symbol = state["pages"]
    client = anthropic.Anthropic()

    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status != "ended":
        raise SystemExit(f"{batch_id} is still {batch.processing_status}; try later")

    results: list[str] = []
    for result in client.messages.batches.results(batch_id):
        symbol = result.custom_id
        page_path = page_by_symbol.get(symbol)
        if page_path is None:
            results.append(f"SKIP {symbol}: not in submission state")
            continue
        if result.result.type != "succeeded":
            results.append(f"{result.result.type.upper()} {symbol}")
            continue
        message = result.result.message
        if message.stop_reason == "refusal":
            results.append(f"REFUSED {symbol}")
            continue
        sym = store.get(symbol)
        if sym is None:
            results.append(f"SKIP {symbol}: no longer in fact store")
            continue
        try:
            text = next(b.text for b in message.content if b.type == "text")
            data = json.loads(text)
        except (StopIteration, json.JSONDecodeError) as exc:
            results.append(f"BAD-JSON {symbol}: {exc}")
            continue
        page = load_page(Path(page_path))
        result_to_page(page, sym, data)
        dropped = drop_ungrounded_notes(store, page)
        page.save()
        note = f" (dropped ungrounded: {', '.join(dropped)})" if dropped else ""
        results.append(f"FILLED {symbol}{note}")
    return results
