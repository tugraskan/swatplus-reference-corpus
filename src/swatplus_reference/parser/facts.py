"""Symbol-anchored fact store.

Everything the parser can extract mechanically lives here, keyed by symbol
name — never by line number. Line numbers are stored as facts *about* a
symbol so renderers can resolve `symbol -> file:line` at build time; prose
never embeds them.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Argument:
    name: str
    decl: str = ""  # declared type + attributes, e.g. "real, intent (in)"
    intent: str = ""
    line: int = 0


@dataclass
class LocalVar:
    name: str
    decl: str = ""
    line: int = 0


@dataclass
class UseDep:
    module: str
    only: list[str] = field(default_factory=list)
    line: int = 0


@dataclass
class IoStatement:
    kind: str  # open/read/write/close ...
    unit: str = ""
    file_expr: str = ""
    line: int = 0


@dataclass
class Component:
    """One field of a derived type, with its source-authored units/description.

    SWAT+ annotates each component inline (`real :: flo = 0. !mm |lateral flow`),
    so units and description come from the source itself — no LLM needed.
    """

    name: str
    decl: str = ""         # declared type + attributes
    units: str = ""        # left of the `|` in the inline comment
    description: str = ""  # right of the `|` (or the whole comment if no `|`)
    line: int = 0


@dataclass
class Symbol:
    """A documented unit: module, subroutine, function, or derived type."""

    kind: str  # "module" | "subroutine" | "function" | "type" | "program"
    name: str  # lowercase canonical name
    file: str  # path relative to the source root
    start_line: int
    end_line: int
    parent: str = ""  # enclosing module name, if any
    args: list[Argument] = field(default_factory=list)
    locals: list[LocalVar] = field(default_factory=list)
    uses: list[UseDep] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)  # explicit `call` targets
    io: list[IoStatement] = field(default_factory=list)
    variables: list[LocalVar] = field(default_factory=list)  # module-level vars
    components: list[Component] = field(default_factory=list)  # derived-type fields
    reads: list[str] = field(default_factory=list)   # module vars this symbol reads
    writes: list[str] = field(default_factory=list)  # module vars this symbol writes
    # Modules and derived types whose declaration changes may affect this
    # symbol even when its own source slice is byte-identical.
    depends_on: list[str] = field(default_factory=list)
    source_hash: str = ""  # sha256 of the symbol's own source slice

    @property
    def qualified(self) -> str:
        return f"{self.parent}::{self.name}" if self.parent else self.name


@dataclass
class FactStore:
    source_ref: str = ""
    # Identifies the parser contract that produced this cache. Old fact files
    # omit the field and therefore load as ``thin-v1``; the CLI rebuilds those
    # once with the rich scanner before using them for documentation.
    producer: str = "thin-v1"
    symbols: dict[str, Symbol] = field(default_factory=dict)  # keyed by name
    parse_errors: dict[str, str] = field(default_factory=dict)  # file -> reason
    fallback_files: list[str] = field(default_factory=list)

    def add(self, sym: Symbol) -> None:
        # Names collide across kinds (e.g. a derived type and a subroutine
        # both called salt_balance). Documentation anchors on procedures and
        # modules, so those win the bare-name slot; types keep a kind-
        # qualified key so nothing is lost.
        existing = self.symbols.get(sym.name)
        if existing is not None and existing.kind != "type" and sym.kind == "type":
            self.symbols[f"type::{sym.name}"] = sym
            return
        if existing is not None and existing.kind == "type" and sym.kind != "type":
            self.symbols[f"type::{sym.name}"] = existing
        self.symbols[sym.name] = sym

    def get(self, name: str) -> Symbol | None:
        return self.symbols.get(name.lower())

    def by_kind(self, kind: str) -> list[Symbol]:
        return sorted(
            (s for s in self.symbols.values() if s.kind == kind),
            key=lambda s: s.name,
        )

    def callers_of(self, name: str) -> list[Symbol]:
        name = name.lower()
        return sorted(
            (s for s in self.symbols.values() if name in s.calls),
            key=lambda s: s.name,
        )

    def members_of(self, module: str) -> list[Symbol]:
        module = module.lower()
        return sorted(
            (s for s in self.symbols.values() if s.parent == module),
            key=lambda s: s.name,
        )

    def readers_of(self, variable: str) -> list[Symbol]:
        variable = variable.lower()
        return sorted(
            (s for s in self.symbols.values() if variable in s.reads),
            key=lambda s: s.name,
        )

    def writers_of(self, variable: str) -> list[Symbol]:
        variable = variable.lower()
        return sorted(
            (s for s in self.symbols.values() if variable in s.writes),
            key=lambda s: s.name,
        )

    # -- persistence ------------------------------------------------------

    def to_json(self) -> str:
        def enc(obj):
            if hasattr(obj, "__dataclass_fields__"):
                return {k: getattr(obj, k) for k in obj.__dataclass_fields__}
            raise TypeError(type(obj))

        return json.dumps(
            {
                "source_ref": self.source_ref,
                "producer": self.producer,
                "symbols": {
                    key: enc_symbol(self.symbols[key])
                    for key in sorted(self.symbols)
                },
                "parse_errors": dict(sorted(self.parse_errors.items())),
                "fallback_files": sorted(self.fallback_files),
            },
            indent=1,
            default=enc,
        )

    @classmethod
    def from_json(cls, text: str) -> "FactStore":
        raw = json.loads(text)
        store = cls(
            source_ref=raw.get("source_ref", ""),
            producer=raw.get("producer", "thin-v1"),
        )
        store.parse_errors = raw.get("parse_errors", {})
        store.fallback_files = raw.get("fallback_files", [])
        for name, s in raw.get("symbols", {}).items():
            store.symbols[name] = Symbol(
                kind=s["kind"],
                name=s["name"],
                file=s["file"],
                start_line=s["start_line"],
                end_line=s["end_line"],
                parent=s.get("parent", ""),
                args=[Argument(**a) for a in s.get("args", [])],
                locals=[LocalVar(**v) for v in s.get("locals", [])],
                uses=[UseDep(**u) for u in s.get("uses", [])],
                calls=s.get("calls", []),
                io=[IoStatement(**i) for i in s.get("io", [])],
                variables=[LocalVar(**v) for v in s.get("variables", [])],
                components=[Component(**c) for c in s.get("components", [])],
                reads=s.get("reads", []),
                writes=s.get("writes", []),
                depends_on=s.get("depends_on", []),
                source_hash=s.get("source_hash", ""),
            )
        return store

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.to_json().encode("utf-8"))

    @classmethod
    def load(cls, path: Path) -> "FactStore":
        return cls.from_json(path.read_text(encoding="utf-8"))


def enc_symbol(sym: Symbol) -> dict:
    def enc_list(items):
        return [
            {k: getattr(it, k) for k in it.__dataclass_fields__} for it in items
        ]

    return {
        "kind": sym.kind,
        "name": sym.name,
        "file": sym.file,
        "start_line": sym.start_line,
        "end_line": sym.end_line,
        "parent": sym.parent,
        "args": enc_list(sym.args),
        "locals": enc_list(sym.locals),
        "uses": enc_list(sym.uses),
        "calls": sym.calls,
        "io": enc_list(sym.io),
        "variables": enc_list(sym.variables),
        "components": enc_list(sym.components),
        "reads": sym.reads,
        "writes": sym.writes,
        "depends_on": sym.depends_on,
        "source_hash": sym.source_hash,
    }


def composite_source_hash(store: "FactStore", symbols: list[str]) -> str | None:
    """A stable hash of several symbols' source hashes, for pages that derive
    from routines rather than a single symbol (io / output-family pages).

    Returns None if any named symbol is absent from the store — the caller
    treats that as orphaned (e.g. a reader routine removed in a prior release).
    """
    parts = []
    for name in sorted(set(s.lower() for s in symbols)):
        sym = store.get(name)
        if sym is None:
            return None
        parts.append(f"{name}:{sym.source_hash}")
    if not parts:
        return ""
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]


def hash_slice(lines: list[str], start_line: int, end_line: int) -> str:
    """Content hash of a symbol's own source slice (1-based inclusive lines).

    Whitespace-insensitive at line ends so editor churn doesn't mark pages
    stale; anything that changes tokens does.
    """
    body = "\n".join(l.rstrip() for l in lines[start_line - 1 : end_line])
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]
