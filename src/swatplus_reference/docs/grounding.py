"""Grounding checks: prose must not contradict the parse.

Checks (per page):

- ERROR  broken-sym-ref: an inline `[sym:name]` reference names a symbol
  that does not exist in the fact store.
- ERROR  wrong-symbol: frontmatter `symbol` is missing from the fact store.
- ERROR  unknown-arg/local/variable/use note: a frontmatter prose mapping
  (args/locals/variables/uses) names something the parser cannot see on
  that symbol.
- WARNING unknown-backtick: a backticked token in prose looks like a code
  identifier but is not resolvable in the page's scope (page symbol's args,
  locals, calls, used modules and their variables, or any global symbol).
  Warnings can be silenced per page via frontmatter `grounding_allow`.

The asymmetry is deliberate: structured fields are machine-written and must
be exact; free prose gets latitude because backticks also mark literals.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..parser.facts import FactStore
from .pages import Page

BACKTICK_RX = re.compile(r"`([A-Za-z_][A-Za-z0-9_]*)`")
SYM_REF_RX = re.compile(r"\[sym:([A-Za-z_]\w*)\]")

# Fortran keywords / common literals that show up in backticks legitimately.
_STOPWORDS = {
    "y", "n", "a", "b", "d", "m", "if", "do", "end", "use", "call", "then",
    "else", "real", "integer", "character", "logical", "allocatable",
    "intent", "in", "out", "inout", "dimension", "type", "module",
    "subroutine", "function", "program", "contains", "implicit", "none",
    "return", "exit", "cycle", "select", "case", "open", "read", "write",
    "close", "rewind", "backspace", "allocate", "deallocate", "null",
    "true", "false", "csv", "txt",
}


@dataclass
class Finding:
    page: str
    level: str  # "error" | "warning"
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper():7} {self.page}: [{self.code}] {self.message}"


def page_scope(store: FactStore, page: Page) -> set[str]:
    """Identifiers legitimately mentionable on this page."""
    scope: set[str] = set(store.symbols)  # every global symbol
    sym = store.get(page.symbol) if page.symbol else None
    if sym is not None:
        scope.update(a.name for a in sym.args)
        scope.update(v.name for v in sym.locals)
        scope.update(v.name for v in sym.variables)
        scope.update(sym.calls)
        for use in sym.uses:
            scope.update(use.only)
            mod = store.get(use.module)
            if mod is not None:
                scope.update(v.name for v in mod.variables)
                scope.update(m.name for m in store.members_of(mod.name))
    # names of every module variable are fair game on io/output pages,
    # which describe cross-cutting file formats
    if page.kind in {"io", "output_family"}:
        for mod in store.by_kind("module"):
            scope.update(v.name for v in mod.variables)
    return scope


def check_page(store: FactStore, page: Page) -> list[Finding]:
    findings: list[Finding] = []
    name = page.path.name

    if page.symbol and store.get(page.symbol) is None:
        findings.append(
            Finding(name, "error", "wrong-symbol",
                    f"frontmatter symbol `{page.symbol}` not found in fact store")
        )
        return findings

    for m in SYM_REF_RX.finditer(page.body):
        if store.get(m.group(1)) is None:
            findings.append(
                Finding(name, "error", "broken-sym-ref",
                        f"[sym:{m.group(1)}] does not resolve")
            )

    sym = store.get(page.symbol) if page.symbol else None
    if sym is not None:
        # Files the AST parser couldn't handle went through the line-oriented
        # fallback, which extracts no declarations — prose notes about
        # locals/args/variables there can't be verified, only flagged.
        degraded = sym.file in store.fallback_files
        checks = [
            ("args", {a.name for a in sym.args}),
            ("locals", {v.name for v in sym.locals}),
            ("variables", {v.name for v in sym.variables}),
            ("uses", {u.module for u in sym.uses}),
        ]
        allow = {a.lower() for a in page.grounding_allow}
        for key, known in checks:
            notes = page.extra.get(key) or {}
            level = "warning" if degraded and key != "uses" else "error"
            for entry in notes:
                if entry.lower() in allow:
                    continue  # explicitly vouched for (e.g. local type components)
                if entry.lower() not in known:
                    findings.append(
                        Finding(name, level, f"unknown-{key.rstrip('s')}-note",
                                f"frontmatter {key} entry `{entry}` is not on "
                                f"`{sym.name}` in the fact store")
                    )

        # Derived-type component notes: each type must be a member type of the
        # module, and each named component must exist on that type.
        if sym.kind == "module":
            member_types = {m.name: m for m in store.members_of(sym.name) if m.kind == "type"}
            for tname, comps in (page.extra.get("type_components") or {}).items():
                mt = member_types.get(tname.lower())
                if mt is None:
                    if not degraded:
                        findings.append(Finding(name, "error", "unknown-type-note",
                            f"type_components names `{tname}`, not a type of `{sym.name}`"))
                    continue
                comp_names = {c.name for c in mt.components}
                for cname in (comps or {}):
                    if cname.lower() not in comp_names and cname.lower() not in allow:
                        findings.append(Finding(name, "error", "unknown-component-note",
                            f"type_components `{tname}` has no component `{cname}`"))

    allow = {a.lower() for a in page.grounding_allow}
    scope = {s.lower() for s in page_scope(store, page)}
    seen: set[str] = set()
    for m in BACKTICK_RX.finditer(page.body):
        tok = m.group(1)
        low = tok.lower()
        if low in seen or low in _STOPWORDS or low in allow or len(tok) < 3:
            continue
        seen.add(low)
        if "_" not in tok and not any(c.isdigit() for c in tok) and low == tok and len(tok) < 6:
            continue  # short plain words are usually literals, not identifiers
        if low not in scope:
            findings.append(
                Finding(name, "warning", "unknown-backtick",
                        f"`{tok}` not resolvable in this page's scope")
            )
    return findings


def check_all(store: FactStore, pages: list[Page]) -> list[Finding]:
    findings: list[Finding] = []
    for page in pages:
        findings.extend(check_page(store, page))
    return findings
