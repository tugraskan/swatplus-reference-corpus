"""Build the documentation contract from the rich Fortran scanner.

The reviewed corpus still consumes :class:`FactStore` because that compact
surface is useful for grounding, hashes, and page status.  The important
boundary is that the facts are now a *projection* of the rich ``ProjectIndex``;
SWAT+ is scanned once and the old fparser2 path is only a comparison tool.
"""

from __future__ import annotations

import re
from pathlib import Path

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
from .rich import RichStore
from .schema_model import (
    DerivedTypeDoc,
    ModuleDoc,
    ProcedureDoc,
    ProgramDoc,
    VariableRef,
)


RICH_DOCUMENTATION_PRODUCER = "rich-v1"

_INTENT_RE = re.compile(r"\bintent\s*\(\s*(inout|in|out)\s*\)", re.I)
_IDENT_RE = re.compile(r"[A-Za-z_]\w*")
_ASSIGN_RE = re.compile(
    r"^\s*([A-Za-z_]\w*(?:\s*\([^=]*\))?(?:%[A-Za-z_]\w*(?:\s*\([^=]*\))?)*)"
    r"\s*=\s*(?!=)(.*)$"
)
_KEYWORD_LINE_RE = re.compile(
    r"^\s*(if|do|else|end|call|where|select|case|type|use|implicit|"
    r"return|cycle|exit|contains|module|subroutine|function|program|"
    r"allocate|deallocate|print|write|read|open|close|format|interface|"
    r"public|private|integer|real|double|character|logical|complex|"
    r"dimension|parameter|save|data|common|external|intrinsic)\b",
    re.I,
)
_DERIVED_TYPE_RE = re.compile(
    r"\b(?:type|class)\s*\(\s*([A-Za-z_]\w*)\s*\)", re.I
)


def _split_units_description(doc: str) -> tuple[str, str]:
    if "|" not in doc:
        return "", doc.strip()
    units, description = doc.split("|", 1)
    return units.strip(), description.strip()


def _intent(declaration: str) -> str:
    match = _INTENT_RE.search(declaration or "")
    return match.group(1).lower() if match else ""


def _source_lines(source_dir: Path, path: str, cache: dict[str, list[str]]) -> list[str]:
    if path not in cache:
        cache[path] = (source_dir / path).read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
    return cache[path]


def _hash_record(source_dir: Path, record, cache: dict[str, list[str]]) -> str:
    lines = _source_lines(source_dir, record.location.path, cache)
    end = record.location.end_line or record.location.line
    return hash_slice(lines, record.location.line, end)


def _variable_type_dependencies(variables: list[VariableRef]) -> set[str]:
    dependencies: set[str] = set()
    for variable in variables:
        match = _DERIVED_TYPE_RE.search(variable.vartype or variable.declaration or "")
        if match:
            dependencies.add(match.group(1).lower())
    return dependencies


def _classify_line(line: str) -> tuple[str | None, list[str]]:
    """Return the root written on a line and identifiers read by that line."""

    code = line.split("!", 1)[0]
    if not code.strip() or "::" in code:
        return None, []
    if not _KEYWORD_LINE_RE.match(code):
        match = _ASSIGN_RE.match(code)
        if match:
            lhs, rhs = match.group(1), match.group(2)
            base = _IDENT_RE.match(lhs.strip())
            write = base.group(0).lower() if base else None
            return write, [token.lower() for token in _IDENT_RE.findall(rhs)]
    return None, [token.lower() for token in _IDENT_RE.findall(code)]


def _resolve_calls(rich: RichStore) -> None:
    """Resolve calls without deleting or deduplicating parsed observations.

    ``CallRef`` records are source observations: repeated calls and unresolved
    function-style candidates still carry useful locations and raw text.  The
    documentation call graph is a separate, deduplicated projection built by
    :func:`_resolved_call_names`.
    """

    procedures = {procedure.name.lower(): procedure for procedure in rich.index.procedures}
    functions = {
        procedure.name.lower()
        for procedure in rich.index.procedures
        if procedure.kind == "function"
    }
    holders = [*rich.index.procedures, *rich.index.programs]
    for target in rich.index.procedures:
        target.called_by = []
    for holder in holders:
        resolved_names: list[str] = []
        for call in holder.calls:
            name = call.name.lower()
            root = name.split("%", 1)[0]
            call.name = name
            call.resolved = (
                root in functions if call.kind == "function" else root in procedures
            )
            if call.resolved:
                resolved_names.append(root)
        for name in dict.fromkeys(resolved_names):
            target = procedures[name]
            caller = holder.name.lower()
            if caller not in target.called_by:
                target.called_by.append(caller)
    for procedure in rich.index.procedures:
        procedure.called_by.sort()


def _resolved_call_names(calls) -> list[str]:
    """Return stable graph edges while leaving call-site observations intact."""

    return list(
        dict.fromkeys(
            call.name.lower().split("%", 1)[0]
            for call in calls
            if call.resolved
        )
    )


def _procedure_symbol(
    source_dir: Path,
    procedure: ProcedureDoc,
    cache: dict[str, list[str]],
) -> Symbol:
    declared = {variable.name.lower(): variable for variable in procedure.variables}
    args: list[Argument] = []
    arg_names = {name.lower() for name in procedure.args}
    for name in procedure.args:
        variable = declared.get(name.lower())
        declaration = variable.declaration if variable else ""
        args.append(
            Argument(
                name=name.lower(),
                decl=declaration,
                intent=_intent(declaration),
                line=variable.location.line if variable else 0,
            )
        )
    locals_ = [
        LocalVar(
            name=variable.name.lower(),
            decl=variable.declaration,
            line=variable.location.line,
        )
        for variable in procedure.variables
        if variable.name.lower() not in arg_names
    ]
    dependencies = {use.module.lower() for use in procedure.uses}
    if procedure.module:
        dependencies.add(procedure.module.lower())
    dependencies.update(_variable_type_dependencies(procedure.variables))
    return Symbol(
        kind=procedure.kind,
        name=procedure.name.lower(),
        file=procedure.location.path,
        start_line=procedure.location.line,
        end_line=procedure.location.end_line or procedure.location.line,
        parent=(procedure.module or procedure.parent or "").lower(),
        args=args,
        locals=locals_,
        uses=[
            UseDep(
                module=use.module.lower(),
                only=[name.lower() for name in use.only],
                line=use.location.line if use.location else 0,
            )
            for use in procedure.uses
        ],
        calls=_resolved_call_names(procedure.calls),
        io=[
            IoStatement(
                kind=operation.kind,
                unit=operation.unit or "",
                file_expr=operation.file_expr or operation.file_resolved or "",
                line=operation.location.line,
            )
            for operation in procedure.io
        ],
        depends_on=sorted(dependencies),
        source_hash=_hash_record(source_dir, procedure, cache),
    )


def _module_symbol(
    source_dir: Path,
    module: ModuleDoc,
    cache: dict[str, list[str]],
) -> Symbol:
    dependencies = {use.module.lower() for use in module.uses}
    dependencies.update(_variable_type_dependencies(module.variables))
    return Symbol(
        kind="module",
        name=module.name.lower(),
        file=module.location.path,
        start_line=module.location.line,
        end_line=module.location.end_line or module.location.line,
        uses=[
            UseDep(
                module=use.module.lower(),
                only=[name.lower() for name in use.only],
                line=use.location.line if use.location else 0,
            )
            for use in module.uses
        ],
        variables=[
            LocalVar(
                name=variable.name.lower(),
                decl=variable.declaration,
                line=variable.location.line,
            )
            for variable in module.variables
        ],
        depends_on=sorted(dependencies),
        source_hash=_hash_record(source_dir, module, cache),
    )


def _type_symbol(
    source_dir: Path,
    derived: DerivedTypeDoc,
    cache: dict[str, list[str]],
) -> Symbol:
    components: list[Component] = []
    dependencies = _variable_type_dependencies(derived.components)
    if derived.module:
        dependencies.add(derived.module.lower())
    for variable in derived.components:
        units, description = _split_units_description(variable.doc)
        components.append(
            Component(
                name=variable.name.lower(),
                decl=variable.declaration,
                units=units,
                description=description,
                line=variable.location.line,
            )
        )
    return Symbol(
        kind="type",
        name=derived.name.lower(),
        file=derived.location.path,
        start_line=derived.location.line,
        end_line=derived.location.end_line or derived.location.line,
        parent=(derived.module or "").lower(),
        components=components,
        depends_on=sorted(dependencies),
        source_hash=_hash_record(source_dir, derived, cache),
    )


def _program_symbol(
    source_dir: Path,
    program: ProgramDoc,
    cache: dict[str, list[str]],
) -> Symbol:
    return Symbol(
        kind="program",
        name=program.name.lower(),
        file=program.location.path,
        start_line=program.location.line,
        end_line=program.location.end_line or program.location.line,
        uses=[
            UseDep(
                module=use.module.lower(),
                only=[name.lower() for name in use.only],
                line=use.location.line if use.location else 0,
            )
            for use in program.uses
        ],
        calls=_resolved_call_names(program.calls),
        depends_on=sorted(use.module.lower() for use in program.uses),
        source_hash=_hash_record(source_dir, program, cache),
    )


def _annotate_dataflow(store: FactStore, source_dir: Path) -> None:
    module_vars = {
        variable.name
        for symbol in store.symbols.values()
        if symbol.kind == "module"
        for variable in symbol.variables
    }
    cache: dict[str, list[str]] = {}
    for symbol in store.symbols.values():
        if symbol.kind not in {"subroutine", "function", "program"}:
            continue
        try:
            lines = _source_lines(source_dir, symbol.file, cache)
        except OSError:
            continue
        local = {argument.name for argument in symbol.args} | {
            variable.name for variable in symbol.locals
        }
        candidates = module_vars - local
        reads: set[str] = set()
        writes: set[str] = set()
        for raw in lines[symbol.start_line - 1 : symbol.end_line]:
            write, line_reads = _classify_line(raw)
            if write in candidates:
                writes.add(write)
            reads.update(name for name in line_reads if name in candidates)
        reads -= writes
        symbol.reads = sorted(reads)
        symbol.writes = sorted(writes)


def project_documentation_facts(
    rich: RichStore,
    source_dir: Path,
    source_ref: str = "",
    diagnostics: FactStore | None = None,
) -> FactStore:
    """Project a rich scan into the stable page/grounding fact contract.

    During parser comparison, ``diagnostics`` is the fparser2 result for the
    same source. Its error and fallback records must remain visible even though
    the rich model supplies the documentation facts.
    """

    source_dir = source_dir.resolve()
    _resolve_calls(rich)
    store = FactStore(source_ref=source_ref, producer=RICH_DOCUMENTATION_PRODUCER)
    if diagnostics is not None:
        store.parse_errors = dict(diagnostics.parse_errors)
        store.fallback_files = sorted(set(diagnostics.fallback_files))
    cache: dict[str, list[str]] = {}
    for module in rich.index.modules:
        store.add(_module_symbol(source_dir, module, cache))
    for program in rich.index.programs:
        store.add(_program_symbol(source_dir, program, cache))
    for procedure in rich.index.procedures:
        store.add(_procedure_symbol(source_dir, procedure, cache))
    for derived in rich.index.types:
        store.add(_type_symbol(source_dir, derived, cache))
    _annotate_dataflow(store, source_dir)
    return store


def parse_documentation(
    source_dir: Path,
    source_ref: str = "",
    diagnostics: FactStore | None = None,
) -> tuple[FactStore, RichStore]:
    """Scan SWAT+ once and return both documentation views of that scan."""

    rich = RichStore.build(source_dir)
    return (
        project_documentation_facts(
            rich, source_dir, source_ref, diagnostics=diagnostics
        ),
        rich,
    )
