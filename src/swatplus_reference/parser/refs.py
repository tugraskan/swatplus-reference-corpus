"""Resolve procedure references to variables declared by used modules.

This deliberately operates on declaration-backed identifiers only. It is not a
call graph and never contributes to documentation grounding or staleness.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re

from .schema_model import DerivedTypeDoc, ModuleDoc, ProcedureDoc, ProjectIndex, SourceLocation, VariableRef


@dataclass(frozen=True)
class ResolvedComponentRef:
    name: str
    type_name: str
    declaration: str
    location: SourceLocation


@dataclass(frozen=True)
class OutsideStateRef:
    reference: str
    symbol: str
    module: str | None
    candidates: tuple[str, ...]
    declaration: str | None
    location: SourceLocation | None
    components: tuple[ResolvedComponentRef, ...] = ()

    @property
    def ambiguous(self) -> bool:
        return self.module is None and bool(self.candidates)


def root_identifier(value: str) -> str:
    match = re.match(r"([a-z_]\w*)", value.strip(), re.I)
    return match.group(1).lower() if match else ""


def use_allows_symbol(only: list[str], root: str) -> bool:
    if not only:
        return True
    root = root.lower()
    for item in only:
        clean = item.strip().split("!", 1)[0].strip()
        if not clean:
            continue
        if "=>" in clean:
            local, remote = (part.strip().lower() for part in clean.split("=>", 1))
            if root in {local, remote}:
                return True
        elif root_identifier(clean) == root:
            return True
    return False


def module_variable(module: ModuleDoc, name: str) -> VariableRef | None:
    name = name.lower()
    return next((v for v in module.variables if v.name.lower() == name), None)


def _visible_module_variables(use, module: ModuleDoc) -> list[tuple[str, VariableRef]]:
    """Return source-visible name and declaration for one USE statement."""
    if not use.only:
        return [(variable.name.lower(), variable) for variable in module.variables]
    visible: list[tuple[str, VariableRef]] = []
    for item in use.only:
        clean = item.strip().split("!", 1)[0].strip()
        if not clean:
            continue
        if "=>" in clean:
            local, remote = (part.strip() for part in clean.split("=>", 1))
            variable = module_variable(module, remote)
            if variable:
                visible.append((local.lower(), variable))
            continue
        variable = module_variable(module, clean)
        if variable:
            visible.append((variable.name.lower(), variable))
    return visible


def _dtype_for_vartype(project: ProjectIndex, vartype: str | None, module: str) -> DerivedTypeDoc | None:
    if not vartype:
        return None
    match = re.search(r"\b(?:type|class)\s*\(\s*([^)]+?)\s*\)", vartype, re.I)
    if not match:
        return None
    wanted = match.group(1).strip().lower()
    for dtype in project.types:
        if (dtype.module or "").lower() == module.lower() and dtype.name.lower() == wanted:
            return dtype
    return next((dtype for dtype in project.types if dtype.name.lower() == wanted), None)


def resolve_ref_components(
    project: ProjectIndex, module_name: str, variable: VariableRef, reference: str
) -> tuple[ResolvedComponentRef, ...]:
    parts = [part.strip().split("(", 1)[0] for part in reference.split("%")]
    if len(parts) <= 1:
        return ()
    vartype = variable.vartype
    resolved: list[ResolvedComponentRef] = []
    for component_name in parts[1:]:
        dtype = _dtype_for_vartype(project, vartype, module_name)
        if dtype is None:
            break
        component = next((c for c in dtype.components if c.name.lower() == component_name.lower()), None)
        if component is None:
            break
        type_name = f"{dtype.module}::{dtype.name}" if dtype.module else dtype.name
        resolved.append(
            ResolvedComponentRef(
                name=component.name,
                type_name=type_name,
                declaration=component.declaration,
                location=component.location,
            )
        )
        vartype = component.vartype
    return tuple(resolved)


def resolve_outside_refs(
    proc: ProcedureDoc, project: ProjectIndex, references: list[str]
) -> list[OutsideStateRef]:
    """Resolve source references through USE visibility; retain ambiguity."""
    modules = {module.name.lower(): module for module in project.modules}
    resolved: list[OutsideStateRef] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    for reference in references:
        root = root_identifier(reference)
        if not root:
            continue
        candidates: list[tuple[str, VariableRef]] = []
        for use in proc.uses:
            module = modules.get(use.module.lower())
            if module:
                candidates.extend(
                    (module.name, variable)
                    for visible_name, variable in _visible_module_variables(use, module)
                    if visible_name == root
                )
        candidate_names = tuple(sorted({name for name, _ in candidates}, key=str.lower))
        key = (reference.lower(), candidate_names)
        if not candidates or key in seen:
            continue
        seen.add(key)
        if len(candidates) != 1:
            resolved.append(
                OutsideStateRef(reference, root, None, candidate_names, None, None)
            )
            continue
        module_name, variable = candidates[0]
        resolved.append(
            OutsideStateRef(
                reference=reference,
                symbol=variable.name,
                module=module_name,
                candidates=(),
                declaration=variable.declaration,
                location=variable.location,
                components=resolve_ref_components(project, module_name, variable, reference),
            )
        )
    return resolved


def outside_state_ref_record(ref: OutsideStateRef) -> dict:
    return asdict(ref)


def outside_state_ref_from_record(record: dict) -> OutsideStateRef:
    location = record.get("location")
    components = tuple(
        ResolvedComponentRef(
            name=item["name"],
            type_name=item["type_name"],
            declaration=item["declaration"],
            location=SourceLocation(**item["location"]),
        )
        for item in record.get("components", [])
    )
    return OutsideStateRef(
        reference=record["reference"],
        symbol=record["symbol"],
        module=record.get("module"),
        candidates=tuple(record.get("candidates", [])),
        declaration=record.get("declaration"),
        location=SourceLocation(**location) if location else None,
        components=components,
    )


def _code(line: str) -> str:
    line = re.sub(r"'(?:''|[^'])*'", "", line)
    return line.split("!", 1)[0]


def candidate_outside_refs(proc: ProcedureDoc, project: ProjectIndex, source_dir: Path) -> list[str]:
    """Find used-module variable references in the procedure's source span."""
    path = source_dir / proc.location.path
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    local_names = {variable.name.lower() for variable in proc.variables}
    local_names.update(arg.lower() for arg in proc.args)
    modules = {module.name.lower(): module for module in project.modules}
    visible_roots: set[str] = set()
    for use in proc.uses:
        module = modules.get(use.module.lower())
        if module is None:
            continue
        visible_roots.update(
            visible_name
            for visible_name, _ in _visible_module_variables(use, module)
            if visible_name not in local_names
        )
    if not visible_roots:
        return []
    # One matcher per procedure is deliberate: compiling one expression for
    # every imported variable made a complete rich parse impractically slow.
    roots = "|".join(re.escape(root) for root in sorted(visible_roots, key=lambda x: (-len(x), x)))
    pattern = re.compile(
        rf"(?<![\w%])(?P<reference>(?P<root>{roots})(?!\w)"
        r"(?:\s*\([^\n)]*\))?(?:\s*%\s*[a-z_]\w*(?:\s*\([^\n)]*\))?)*)",
        re.I,
    )
    candidates: list[str] = []
    seen: set[str] = set()
    for line in lines[proc.location.line - 1 : proc.location.end_line]:
        code = _code(line)
        for match in pattern.finditer(code):
            reference = re.sub(r"\s+", "", match.group("reference"))
            key = reference.lower()
            if key not in seen:
                seen.add(key)
                candidates.append(reference)
    return candidates


def extract_outside_state_refs(
    proc: ProcedureDoc, project: ProjectIndex, source_dir: Path
) -> list[OutsideStateRef]:
    return resolve_outside_refs(proc, project, candidate_outside_refs(proc, project, source_dir))
