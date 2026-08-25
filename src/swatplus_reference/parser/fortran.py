"""Extract facts from a Fortran tree.

AST-first: each file is parsed with fparser2 (F2008). Files that fparser2
cannot parse fall back to a line-oriented scanner so the pipeline never
loses a file; fallback files are recorded in the fact store so the
degradation is visible.
"""

from __future__ import annotations

import re
from pathlib import Path

from fparser.common.readfortran import FortranStringReader
from fparser.common.sourceinfo import FortranFormat
from fparser.two import Fortran2003 as f03
from fparser.two.parser import ParserFactory
from fparser.two.utils import FortranSyntaxError, walk

from .facts import (
    Argument,
    Component,
    FactStore,
    IoStatement,
    LocalVar,
    Symbol,
    UseDep,
    hash_slice,
)

_PARSER = None


def _parser():
    global _PARSER
    if _PARSER is None:
        _PARSER = ParserFactory().create(std="f2008")
    return _PARSER


def parse_tree(source_dir: Path, source_ref: str = "") -> FactStore:
    store = FactStore(source_ref=source_ref)
    for path in sorted(source_dir.rglob("*.f90")):
        rel = path.relative_to(source_dir).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            parse_file_ast(store, rel, text)
        except (FortranSyntaxError, Exception) as exc:  # noqa: BLE001
            store.parse_errors[rel] = f"{type(exc).__name__}: {exc}"
            store.fallback_files.append(rel)
            parse_file_fallback(store, rel, text)
    annotate_dataflow(store, source_dir)
    return store


# --------------------------------------------------------------------------
# Data-flow: which module variables each procedure reads / writes
# --------------------------------------------------------------------------

_IDENT = re.compile(r"[A-Za-z_]\w*")
# an assignment: a variable reference, then a single `=` not part of a
# comparison / pointer-assign / declaration
_ASSIGN = re.compile(
    r"^\s*([A-Za-z_]\w*(?:\s*\([^=]*\))?(?:%[A-Za-z_]\w*(?:\s*\([^=]*\))?)*)"
    r"\s*=\s*(?!=)(.*)$"
)
_KEYWORD_LINE = re.compile(
    r"^\s*(if|do|else|end|call|where|select|case|type|use|implicit|"
    r"return|cycle|exit|contains|module|subroutine|function|program|"
    r"allocate|deallocate|print|write|read|open|close|format|interface|"
    r"public|private|integer|real|double|character|logical|complex|"
    r"dimension|parameter|save|data|common|external|intrinsic)\b",
    re.IGNORECASE,
)


def _classify_line(line: str) -> tuple[str | None, list[str]]:
    """Return (write_base | None, [read identifiers]) for one code line."""
    code = line.split("!", 1)[0]
    if not code.strip() or "::" in code:
        return None, []
    if not _KEYWORD_LINE.match(code):
        m = _ASSIGN.match(code)
        if m:
            lhs, rhs = m.group(1), m.group(2)
            base = _IDENT.match(lhs.strip())
            write = base.group(0).lower() if base else None
            reads = [t.lower() for t in _IDENT.findall(rhs)]
            return write, reads
    # keyword line or non-assignment expression: everything is a read
    return None, [t.lower() for t in _IDENT.findall(code)]


def annotate_dataflow(store: FactStore, source_dir: Path) -> None:
    """Populate `reads`/`writes` on each procedure with the module variables
    it references. Module variables are the shared state that carries data
    between routines; a routine's own args/locals are excluded so a local
    name never masquerades as shared state."""
    module_vars = {
        v.name for s in store.symbols.values() if s.kind == "module" for v in s.variables
    }
    if not module_vars:
        return
    file_cache: dict[str, list[str]] = {}
    for sym in store.symbols.values():
        if sym.kind not in ("subroutine", "function", "program"):
            continue
        lines = file_cache.get(sym.file)
        if lines is None:
            try:
                lines = (source_dir / sym.file).read_text(
                    encoding="utf-8", errors="replace"
                ).splitlines()
            except OSError:
                continue
            file_cache[sym.file] = lines
        local = {a.name for a in sym.args} | {v.name for v in sym.locals}
        candidates = module_vars - local
        reads: set[str] = set()
        writes: set[str] = set()
        for raw in lines[sym.start_line - 1 : sym.end_line]:
            write, rd = _classify_line(raw)
            if write and write in candidates:
                writes.add(write)
            reads.update(t for t in rd if t in candidates)
        # a variable written is not also counted as a plain read of the same
        reads -= writes
        sym.reads = sorted(reads)
        sym.writes = sorted(writes)


# --------------------------------------------------------------------------
# AST path
# --------------------------------------------------------------------------

_SCOPE_CLASSES = (
    f03.Module,
    f03.Subroutine_Subprogram,
    f03.Function_Subprogram,
    f03.Main_Program,
)


def parse_file_ast(store: FactStore, rel: str, text: str) -> None:
    reader = FortranStringReader(text, ignore_comments=True)
    # .f90 files are free-form by definition; never trust content sniffing
    # (files whose first line starts in column 6 get misread as fixed-form).
    reader.set_format(FortranFormat(True, False))
    tree = _parser()(reader)
    lines = text.splitlines()

    for node in walk(tree, _SCOPE_CLASSES):
        sym = _symbol_for_scope(node, rel, lines)
        if sym is None:
            continue
        # A module's contained procedures are separate symbols; keep the
        # module symbol focused on its own spec part.
        if isinstance(node, f03.Module):
            _fill_module(sym, node)
        else:
            _fill_procedure(sym, node)
        store.add(sym)

    # Derived types defined at module level become their own symbols too.
    for node in walk(tree, f03.Derived_Type_Def):
        stmt = node.children[0]
        name = str(walk(stmt, f03.Type_Name)[0]).lower()
        start, end = _span(node, lines)
        parent = _enclosing_module(node)
        store.add(
            Symbol(
                kind="type",
                name=name,
                file=rel,
                start_line=start,
                end_line=end,
                parent=parent,
                components=parse_components(lines, start, end),
                source_hash=hash_slice(lines, start, end),
            )
        )


def _symbol_for_scope(node, rel: str, lines: list[str]) -> Symbol | None:
    stmt = node.children[0]
    kind_map = {
        f03.Module: "module",
        f03.Subroutine_Subprogram: "subroutine",
        f03.Function_Subprogram: "function",
        f03.Main_Program: "program",
    }
    kind = kind_map[type(node)]
    names = walk(stmt, f03.Name)
    if not names:
        return None
    name = str(names[0]).lower()
    start, end = _span(node, lines)
    return Symbol(
        kind=kind,
        name=name,
        file=rel,
        start_line=start,
        end_line=end,
        parent=_enclosing_module(node),
        source_hash=hash_slice(lines, start, end),
    )


def _enclosing_module(node) -> str:
    parent = getattr(node, "parent", None)
    while parent is not None:
        if isinstance(parent, f03.Module):
            names = walk(parent.children[0], f03.Name)
            return str(names[0]).lower() if names else ""
        parent = getattr(parent, "parent", None)
    return ""


def _span(node, lines: list[str]) -> tuple[int, int]:
    first = last = None
    for stmt in walk(node):
        item = getattr(stmt, "item", None)
        if item is not None and getattr(item, "span", None):
            lo, hi = item.span
            first = lo if first is None else min(first, lo)
            last = hi if last is None else max(last, hi)
    if first is None:
        return 1, len(lines)
    return first, last


def _stmt_line(node) -> int:
    cur = node
    while cur is not None:
        item = getattr(cur, "item", None)
        if item is not None and getattr(item, "span", None):
            return item.span[0]
        cur = getattr(cur, "parent", None)
    return 0


def _own_statements(node, cls):
    """Statements of *node* excluding those inside contained subprograms."""
    inner: set[int] = set()
    for sub in walk(node, (f03.Subroutine_Subprogram, f03.Function_Subprogram)):
        if sub is not node:
            inner.update(id(x) for x in walk(sub, cls))
    return [x for x in walk(node, cls) if id(x) not in inner]


def _fill_common(sym: Symbol, node) -> None:
    for use in _own_statements(node, f03.Use_Stmt):
        mod_names = walk(use, f03.Name)
        if not mod_names:
            continue
        only = [str(n).lower() for n in walk(use, f03.Only_List) for n in walk(n, f03.Name)]
        sym.uses.append(UseDep(module=str(mod_names[0]).lower(), only=only))


def _decl_entities(decl) -> tuple[str, list[str]]:
    """Return (type+attrs text, [entity names]) for a declaration stmt."""
    type_spec, attrs, entities = decl.children
    prefix = str(type_spec).lower()
    if attrs is not None:
        prefix += ", " + str(attrs).lower()
    names = []
    for ent in walk(entities, f03.Entity_Decl):
        names.append(str(ent.children[0]).lower())
    if not names:  # e.g. plain Name list
        names = [str(n).lower() for n in walk(entities, f03.Name)]
    return prefix, names


def _fill_procedure(sym: Symbol, node) -> None:
    stmt = node.children[0]
    args = [str(a).lower() for a in walk(stmt, f03.Dummy_Arg_List) for a in walk(a, f03.Name)]
    arg_set = set(args)
    sym.args = [Argument(name=a) for a in args]

    _fill_common(sym, node)

    for decl in _own_statements(node, f03.Type_Declaration_Stmt):
        prefix, names = _decl_entities(decl)
        intent = ""
        m = re.search(r"intent\s*\(\s*(in|out|inout)\s*\)", prefix)
        if m:
            intent = m.group(1)
        for name in names:
            if name in arg_set:
                for a in sym.args:
                    if a.name == name:
                        a.decl, a.intent = prefix, intent
            else:
                sym.locals.append(LocalVar(name=name, decl=prefix))

    for call in _own_statements(node, f03.Call_Stmt):
        target = str(call.children[0]).lower()
        if target not in sym.calls:
            sym.calls.append(target)

    io_classes = {
        f03.Open_Stmt: "open",
        f03.Read_Stmt: "read",
        f03.Write_Stmt: "write",
        f03.Close_Stmt: "close",
        f03.Rewind_Stmt: "rewind",
        f03.Backspace_Stmt: "backspace",
    }
    for cls, kind in io_classes.items():
        for st in _own_statements(node, cls):
            sym.io.append(
                IoStatement(
                    kind=kind,
                    unit=_io_spec(st, ("UNIT",)),
                    file_expr=_io_spec(st, ("FILE",)),
                    line=_stmt_line(st),
                )
            )
    sym.io.sort(key=lambda i: i.line)


def _io_spec(stmt, keys: tuple[str, ...]) -> str:
    text = str(stmt)
    for key in keys:
        m = re.search(rf"{key}\s*=\s*([^,)]+)", text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    # positional first spec: open(107, file=...) / write (unit, fmt)
    m = re.match(r"\w+\s*\(([^,()]+)", text)
    if m and keys == ("UNIT",):
        return m.group(1).strip()
    return ""


def _fill_module(sym: Symbol, node) -> None:
    _fill_common(sym, node)
    spec = None
    for child in node.children:
        if isinstance(child, f03.Specification_Part):
            spec = child
            break
    if spec is None:
        return
    for decl in walk(spec, f03.Type_Declaration_Stmt):
        # skip declarations inside derived type definitions
        anc = decl.parent
        inside_type = False
        while anc is not None and anc is not spec:
            if isinstance(anc, f03.Derived_Type_Def):
                inside_type = True
                break
            anc = anc.parent
        if inside_type:
            continue
        prefix, names = _decl_entities(decl)
        for name in names:
            sym.variables.append(LocalVar(name=name, decl=prefix))


# --------------------------------------------------------------------------
# Fallback path (line-oriented, for files fparser2 rejects)
# --------------------------------------------------------------------------

_RX_UNIT = re.compile(
    r"^\s*(?:(?:pure|elemental|recursive)\s+)*"
    r"(module(?!\s+procedure)|program|subroutine|"
    r"(?:[\w() =*]+\s+)?function)\s+(\w+)",
    re.IGNORECASE,
)
_RX_END = re.compile(r"^\s*end\s*(module|program|subroutine|function)?\b", re.IGNORECASE)
_RX_USE = re.compile(r"^\s*use\s+(\w+)(?:\s*,\s*only\s*:\s*(.+))?", re.IGNORECASE)
_RX_CALL = re.compile(r"^\s*call\s+(\w+)", re.IGNORECASE)


_COMPONENT_DECL = re.compile(r"^\s*(.+?)::\s*(.+?)\s*$")
_TYPE_HDR_RE = re.compile(r"^\s*type\b(?!\s*\()", re.IGNORECASE)


def parse_components(lines: list[str], start: int, end: int) -> list[Component]:
    """Extract a derived type's components from its raw source slice.

    Reads the raw text (not the AST, which drops comments) so the SWAT+
    inline `!units |description` annotations are captured. Handles multi-name
    declarations and the `!!`/`!` comment conventions; skips the `type ... /
    end type` lines and any `contains`/procedure bindings.
    """
    out: list[Component] = []
    for raw in lines[start:end - 1]:  # exclude the `type NAME` and `end type` lines
        stripped = raw.strip()
        if not stripped or _TYPE_HDR_RE.match(stripped) or stripped.lower().startswith(
            ("end type", "contains", "procedure", "generic", "private", "sequence")
        ):
            continue
        code, _, comment = raw.partition("!")
        comment = comment.lstrip("!").strip()
        units, desc = "", comment
        if "|" in comment:
            u, _, d = comment.partition("|")
            units, desc = u.strip(), d.strip()
        m = _COMPONENT_DECL.match(code)
        if not m:
            continue
        decl = m.group(1).strip()
        for entity in _split_entities(m.group(2)):
            name = re.split(r"[(\s=*]", entity, 1)[0].strip().lower()
            if name:
                out.append(Component(name=name, decl=decl, units=units, description=desc))
    return out


def _split_entities(rhs: str) -> list[str]:
    """Split a declaration RHS on commas that are not inside parentheses."""
    parts, depth, cur = [], 0, ""
    for ch in rhs:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def parse_file_fallback(store: FactStore, rel: str, text: str) -> None:
    lines = text.splitlines()
    stack: list[Symbol] = []

    def close(sym: Symbol, line_no: int) -> None:
        sym.end_line = line_no
        sym.source_hash = hash_slice(lines, sym.start_line, sym.end_line)
        store.add(sym)

    for i, raw in enumerate(lines, start=1):
        line = raw.split("!")[0].rstrip()
        if not line.strip():
            continue
        m = _RX_UNIT.match(line)
        if m:
            kind_word = m.group(1).lower()
            kind = "function" if kind_word.endswith("function") else kind_word
            parent = stack[-1].name if stack and stack[-1].kind == "module" else ""
            stack.append(
                Symbol(
                    kind=kind,
                    name=m.group(2).lower(),
                    file=rel,
                    start_line=i,
                    end_line=i,
                    parent=parent,
                )
            )
            continue
        if _RX_END.match(line) and stack:
            word = (_RX_END.match(line).group(1) or "").lower()
            if not word or word == stack[-1].kind or (
                word == "function" and stack[-1].kind == "function"
            ):
                close(stack.pop(), i)
                continue
        if not stack:
            continue
        cur = stack[-1]
        m = _RX_USE.match(line)
        if m:
            only = [
                s.strip().split("=>")[0].strip().lower()
                for s in (m.group(2) or "").split(",")
                if s.strip()
            ]
            cur.uses.append(UseDep(module=m.group(1).lower(), only=only))
            continue
        m = _RX_CALL.match(line)
        if m and m.group(1).lower() not in cur.calls:
            cur.calls.append(m.group(1).lower())

    while stack:  # unterminated units still get recorded
        close(stack.pop(), len(lines))
