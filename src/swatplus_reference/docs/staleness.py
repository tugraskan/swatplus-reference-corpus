"""Staleness tracking, with soft call-graph propagation.

Each filled page records `source_hash` — the fact store's hash of the
symbol's own source slice at the time the prose was written. On a new
SWAT+ ref, re-parse and compare: only pages whose symbol actually changed
are marked `stale` and re-filled. Unrelated edits in the same file do not
invalidate a page.

Because a page's prose also *describes* the symbols it calls and is called
by, a change to a neighbour can make prose drift even when the page's own
source is untouched. Such pages are marked `affected` (a soft
review signal, not `stale`): for every stale symbol S, both its callers
(they describe calling S) and its callees (their "called from S" context may
have shifted) are flagged. Affected pages are surfaced for review, never
force-regenerated — `refill` targets `stale` only.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..parser.facts import FactStore, composite_source_hash
from .pages import (
    STATUS_AFFECTED,
    STATUS_FILLED,
    STATUS_STALE,
    STATUS_TODO,
    Page,
)


@dataclass
class StatusReport:
    filled: list[Page]
    stale: list[Page]      # this page's own symbol changed
    affected: list[Page]   # a call-graph neighbour changed; prose may lag
    todo: list[Page]       # never filled
    orphaned: list[Page]   # page's symbol no longer exists in the source
    missing: list[str]     # symbols in the fact store with no page
    # affected page name -> the changed neighbour symbols that triggered it
    affected_by: dict[str, list[str]] = field(default_factory=dict)

    def summary(self) -> str:
        return (
            f"filled={len(self.filled)} stale={len(self.stale)} "
            f"affected={len(self.affected)} todo={len(self.todo)} "
            f"orphaned={len(self.orphaned)} missing-pages={len(self.missing)}"
        )


def _neighbours(store: FactStore, symbol: str) -> set[str]:
    """Symbols whose prose references `symbol`: its callers and its callees."""
    out = {c.name for c in store.callers_of(symbol)}
    sym = store.get(symbol)
    if sym is not None:
        out.update(c.lower() for c in sym.calls)
    out.discard(symbol.lower())
    return out


# A change to a routine that writes a variable only a handful of routines ever
# write is a change to that variable's *meaning* — flag its readers. A variable
# written all over (a shared accumulator) has no single owner, so one writer
# changing does not redefine it; propagating there is noise.
MAX_WRITERS_FOR_DATAFLOW = 3
# Data-flow is a useful signal when specific and noise when diffuse: a hub
# routine (top-level orchestrator / reader) writes so much state that flagging
# every reader says nothing. If a single change would data-flow-flag more than
# this many pages, it is treated as a hub and data-flow propagation is skipped
# for it (its direct call-graph neighbours are still flagged).
MAX_DATAFLOW_FANOUT = 12


def compute_status(
    store: FactStore,
    pages: list[Page],
    max_writers: int = MAX_WRITERS_FOR_DATAFLOW,
    max_fanout: int = MAX_DATAFLOW_FANOUT,
) -> StatusReport:
    filled: list[Page] = []
    stale: list[Page] = []
    todo: list[Page] = []
    orphaned: list[Page] = []

    page_by_symbol: dict[str, Page] = {}
    covered: set[str] = set()
    for page in pages:
        if page.symbol:
            covered.add(page.symbol.lower())
            page_by_symbol[page.symbol.lower()] = page
            sym = store.get(page.symbol)
            if sym is None:
                orphaned.append(page)
                continue
            if page.status == STATUS_TODO or not page.source_hash:
                todo.append(page)
            elif page.source_hash != sym.source_hash:
                stale.append(page)
            else:
                filled.append(page)
        elif page.source_symbols:
            # io / output-family pages: track the composite hash of the
            # routines they derive from (reader; opener + writer).
            if page.status == STATUS_TODO or not page.source_hash:
                todo.append(page)
                continue
            current = composite_source_hash(store, page.source_symbols)
            if current is None:
                orphaned.append(page)  # a source routine is gone (e.g. prior release)
            elif current != page.source_hash:
                stale.append(page)
            else:
                filled.append(page)
        else:
            # symbol-less pages with no declared source can't be tracked
            (todo if page.status == STATUS_TODO else filled).append(page)

    # Soft propagation: a stale symbol's neighbours are "affected" (only pages
    # that are otherwise filled — stale/todo/orphaned win). Two edge kinds:
    # call-graph (callers/callees) and data-flow (readers of a narrowly-written
    # variable the changed symbol writes).
    filled_names = {p.path.name for p in filled}
    affected_by: dict[str, list[str]] = {}

    def flag(target_symbol: str, trigger: str) -> None:
        page = page_by_symbol.get(target_symbol)
        if page is None or page.path.name not in filled_names:
            return
        affected_by.setdefault(page.path.name, []).append(trigger)

    # reverse data-flow index, built once
    var_readers: dict[str, list[str]] = {}
    var_writers: dict[str, list[str]] = {}
    for s in store.symbols.values():
        for v in s.reads:
            var_readers.setdefault(v, []).append(s.name)
        for v in s.writes:
            var_writers.setdefault(v, []).append(s.name)

    stale_symbols = [p.symbol.lower() for p in stale if p.symbol]
    for changed in stale_symbols:
        for neighbour in _neighbours(store, changed):
            flag(neighbour, changed)
        sym = store.get(changed)
        if sym is None:
            continue
        # gather data-flow candidates first, then apply only if not a hub
        candidates: list[tuple[str, str]] = []
        for var in sym.writes:
            if len(var_writers.get(var, [])) > max_writers:
                continue  # broadly-written: no single owner, propagating is noise
            for reader in var_readers.get(var, []):
                if reader != changed:
                    candidates.append((reader, f"{changed} (via {var})"))
        if len({r for r, _ in candidates}) <= max_fanout:
            for reader, trigger in candidates:
                flag(reader, trigger)

    affected: list[Page] = []
    if affected_by:
        remaining_filled = []
        for page in filled:
            if page.path.name in affected_by:
                affected.append(page)
            else:
                remaining_filled.append(page)
        filled = remaining_filled
    for name in affected_by:
        affected_by[name] = sorted(set(affected_by[name]))

    documentable = ("module", "subroutine", "function", "program")
    missing = [
        s.name
        for kind in documentable
        for s in store.by_kind(kind)
        if s.name not in covered
    ]
    return StatusReport(filled, stale, affected, todo, orphaned, missing, affected_by)


def apply_status(store: FactStore, pages: list[Page]) -> list[Page]:
    """Rewrite page frontmatter status to match reality. Returns changed pages."""
    report = compute_status(store, pages)
    changed: list[Page] = []

    def set_status(page: Page, status: str) -> None:
        if page.status != status:
            page.status = status
            changed.append(page)

    for page in report.stale:
        set_status(page, STATUS_STALE)
    for page in report.affected:
        set_status(page, STATUS_AFFECTED)
    for page in report.filled:
        # a page that was flagged stale/affected but no longer is reverts clean
        if page.status in (STATUS_STALE, STATUS_AFFECTED):
            set_status(page, STATUS_FILLED)

    for page in changed:
        page.save()
    return changed
