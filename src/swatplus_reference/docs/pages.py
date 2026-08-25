"""Markdown page model.

One tracked `.md` file per documented symbol, with YAML frontmatter for the
structured fields and plain Markdown prose for everything else. Two rules
keep pages durable across SWAT+ releases:

1. Prose references symbols, never line numbers. Inline `[sym:name]`
   references are resolved to page + source links at render time.
2. Parser-owned facts are never stored in the page. `<!-- facts:NAME -->`
   markers are expanded from the current fact store at render time.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER_RX = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

# Frontmatter `status` values
STATUS_TODO = "todo"          # page exists, prose not written yet
STATUS_FILLED = "filled"      # prose written and reviewed
STATUS_STALE = "stale"        # this page's own symbol changed
STATUS_AFFECTED = "affected"  # own symbol unchanged, but a call-graph neighbor changed


@dataclass
class Page:
    path: Path
    kind: str = ""            # procedure | module | type | io | output_family
    symbol: str = ""          # anchor into the fact store ("" for io pages)
    source_symbols: list[str] = field(default_factory=list)  # routines a symbol-less
    #                           page derives from (io: reader; output_family: opener+writer)
    title: str = ""
    status: str = STATUS_TODO
    source_hash: str = ""     # fact-store hash (own symbol, or composite of source_symbols)
    version_label: str = ""   # source baseline against which the prose was written
    grounding_allow: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)  # kind-specific frontmatter
    body: str = ""

    @property
    def name(self) -> str:
        return self.path.stem

    def frontmatter(self) -> dict:
        fm = {
            "kind": self.kind,
            "symbol": self.symbol,
            "source_symbols": self.source_symbols,
            "title": self.title,
            "status": self.status,
            "source_hash": self.source_hash,
            "version_label": self.version_label,
        }
        if self.grounding_allow:
            fm["grounding_allow"] = self.grounding_allow
        fm.update(self.extra)
        return {k: v for k, v in fm.items() if v not in ("", None, [])}

    def dumps(self) -> str:
        fm = yaml.safe_dump(
            self.frontmatter(), sort_keys=False, allow_unicode=True, width=88
        )
        return f"---\n{fm}---\n\n{self.body.strip()}\n"

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self.dumps(), encoding="utf-8")


KNOWN_KEYS = {
    "kind",
    "symbol",
    "source_symbols",
    "title",
    "status",
    "source_hash",
    "version_label",
    "grounding_allow",
}


def load_page(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RX.match(text)
    fm: dict = {}
    body = text
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
        body = text[m.end() :]
    extra = {k: v for k, v in fm.items() if k not in KNOWN_KEYS}
    return Page(
        path=path,
        kind=fm.get("kind", ""),
        symbol=fm.get("symbol", ""),
        source_symbols=list(fm.get("source_symbols", []) or []),
        title=fm.get("title", path.stem),
        status=fm.get("status", STATUS_TODO),
        source_hash=fm.get("source_hash", ""),
        version_label=fm.get("version_label", ""),
        grounding_allow=list(fm.get("grounding_allow", []) or []),
        extra=extra,
        body=body.strip(),
    )


def load_all(docs_dir: Path) -> list[Page]:
    pages = []
    for path in sorted(docs_dir.rglob("*.md")):
        if path.name in {"index.md", "SUMMARY.md"}:
            continue
        pages.append(load_page(path))
    return pages


def page_dir(kind: str) -> str:
    return {
        "procedure": "procedures",
        "subroutine": "procedures",
        "function": "procedures",
        "program": "procedures",
        "module": "modules",
        "type": "types",
        "io": "io",
        "output_family": "output_families",
    }[kind]
