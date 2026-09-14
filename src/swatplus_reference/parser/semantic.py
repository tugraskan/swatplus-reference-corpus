"""Semantic relationships shared by scanner- and AST-built project indexes.

The source parsers own observations.  This module only derives relationships
from those observations and must never rewrite, delete, or reorder them.
"""
from __future__ import annotations

import re
from collections.abc import Iterable

from .schema_model import (
    CallRef,
    ModuleDoc,
    ProcedureDoc,
    ProgramDoc,
    ProjectIndex,
    ReviewFlag,
    UseRef,
    record_identity,
    record_scope,
)
from .source_text import strip_fortran_comment


CALL_RESOLUTION_FLAG_CODES = frozenset({"ambiguous_call"})


def _key(value: str | None) -> str:
    return (value or "").lower()


def _call_name(value: str) -> str:
    """Return a lookup key without changing the source spelling on CallRef."""

    return re.sub(r"\s+", "", value).lower()


def _procedure_identity(procedure: ProcedureDoc) -> str:
    if procedure.identity is None:
        procedure.identity = record_identity(
            procedure.kind,
            procedure.name,
            procedure.location.path,
            record_scope(procedure.module, procedure.parent),
        )
    return procedure.identity


def _unique(candidates: Iterable[ProcedureDoc]) -> list[ProcedureDoc]:
    unique: dict[str, ProcedureDoc] = {}
    for candidate in candidates:
        unique.setdefault(_procedure_identity(candidate), candidate)
    return list(unique.values())


def _rename(item: str) -> tuple[str, str] | None:
    clean = strip_fortran_comment(item.strip()).strip()
    if "=>" not in clean:
        return None
    local, remote = (part.strip().lower() for part in clean.split("=>", 1))
    return (local, remote) if local and remote else None


def _remote_name(use: UseRef, visible_name: str) -> str | None:
    """Map a locally visible USE name to its definition name.

    An ONLY list exposes only named entries.  A non-ONLY rename hides the
    remote spelling while importing every other public name unchanged.
    """

    visible_name = visible_name.lower()
    if use.only:
        for item in use.only:
            renamed = _rename(item)
            if renamed:
                local, remote = renamed
                if visible_name == local:
                    return remote
                continue
            clean = strip_fortran_comment(item.strip()).strip().lower()
            match = re.match(r"[a-z_]\w*", clean, re.I)
            if match and visible_name == match.group(0):
                return visible_name
        return None

    renamed_remotes: set[str] = set()
    for item in use.renames:
        renamed = _rename(item)
        if not renamed:
            continue
        local, remote = renamed
        renamed_remotes.add(remote)
        if visible_name == local:
            return remote
    return None if visible_name in renamed_remotes else visible_name


def _same_lexical_area(left: ProcedureDoc, right: ProcedureDoc) -> bool:
    return (
        _key(left.module) == _key(right.module)
        and _key(left.location.path) == _key(right.location.path)
    )


class _CallResolver:
    def __init__(self, index: ProjectIndex):
        self.modules_by_name: dict[str, list[ModuleDoc]] = {}
        self.procedures_by_name: dict[str, list[ProcedureDoc]] = {}
        for module in index.modules:
            self.modules_by_name.setdefault(_key(module.name), []).append(module)
        for procedure in index.procedures:
            _procedure_identity(procedure)
            self.procedures_by_name.setdefault(_key(procedure.name), []).append(procedure)

    @staticmethod
    def _matches_kind(procedure: ProcedureDoc, call: CallRef) -> bool:
        return _key(procedure.kind) == _key(call.kind)

    def _lexical_candidates(
        self, holder: ProcedureDoc, name: str, call: CallRef
    ) -> list[ProcedureDoc]:
        candidates = []
        for target in self.procedures_by_name.get(name, []):
            if not self._matches_kind(target, call) or not _same_lexical_area(
                holder, target
            ):
                continue
            if target is holder:
                candidates.append(target)  # recursive call
            elif _key(target.parent) == _key(holder.name):
                candidates.append(target)  # direct internal procedure
            elif holder.parent and _key(target.parent) == _key(holder.parent):
                candidates.append(target)  # sibling internal procedure
            elif (
                holder.parent
                and not target.parent
                and _key(target.name) == _key(holder.parent)
            ):
                candidates.append(target)  # host procedure
        return _unique(candidates)

    def _module_candidates(
        self, holder: ProcedureDoc, name: str, call: CallRef
    ) -> list[ProcedureDoc]:
        if not holder.module:
            return []
        return _unique(
            target
            for target in self.procedures_by_name.get(name, [])
            if self._matches_kind(target, call)
            and not target.parent
            and _key(target.module) == _key(holder.module)
        )

    def _host_uses(self, holder: ProcedureDoc | ProgramDoc) -> list[UseRef]:
        uses = list(holder.uses)
        if isinstance(holder, ProcedureDoc):
            if holder.module:
                for module in self.modules_by_name.get(_key(holder.module), []):
                    if _key(module.location.path) == _key(holder.location.path):
                        uses.extend(module.uses)
            parent_name = holder.parent
            visited: set[tuple[str, str, str]] = set()
            while parent_name:
                parents = [
                    candidate
                    for candidate in self.procedures_by_name.get(_key(parent_name), [])
                    if _same_lexical_area(holder, candidate)
                ]
                if len(parents) != 1:
                    break
                parent = parents[0]
                marker = (
                    _key(parent.name),
                    _key(parent.parent),
                    _key(parent.location.path),
                )
                if marker in visited:
                    break
                visited.add(marker)
                uses.extend(parent.uses)
                parent_name = parent.parent
        return uses

    def _import_candidates(
        self, holder: ProcedureDoc | ProgramDoc, name: str, call: CallRef
    ) -> list[ProcedureDoc]:
        candidates: list[ProcedureDoc] = []
        for use in self._host_uses(holder):
            if use.intrinsic:
                continue
            remote_name = _remote_name(use, name)
            if remote_name is None:
                continue
            for module in self.modules_by_name.get(_key(use.module), []):
                for target in self.procedures_by_name.get(remote_name, []):
                    if (
                        self._matches_kind(target, call)
                        and not target.parent
                        and _key(target.module) == _key(module.name)
                        and _key(target.location.path) == _key(module.location.path)
                    ):
                        candidates.append(target)
        return _unique(candidates)

    def _global_candidates(self, name: str, call: CallRef) -> list[ProcedureDoc]:
        return _unique(
            target
            for target in self.procedures_by_name.get(name, [])
            if self._matches_kind(target, call)
            and not target.module
            and not target.parent
        )

    def candidates(
        self, holder: ProcedureDoc | ProgramDoc, call: CallRef
    ) -> list[ProcedureDoc]:
        name = _call_name(call.name)
        # A type-bound dispatch needs declared-type/component semantics.  A
        # bare-name resolver must not mistake the object for a procedure.
        if not name or "%" in name:
            return []
        tiers: list[list[ProcedureDoc]] = []
        if isinstance(holder, ProcedureDoc):
            tiers.extend(
                [
                    self._lexical_candidates(holder, name, call),
                    self._module_candidates(holder, name, call),
                ]
            )
        tiers.extend(
            [
                self._import_candidates(holder, name, call),
                self._global_candidates(name, call),
            ]
        )
        return next((tier for tier in tiers if tier), [])


def resolve_project_calls(index: ProjectIndex) -> None:
    """Resolve call observations without changing their source identities.

    Resolution is fail-closed and follows visibility tiers: lexical internal
    procedures, same-module procedures, USE-associated procedures (including
    ONLY and rename rules), then external/global definitions.  Only a single
    kind-correct candidate creates an edge.
    """

    resolver = _CallResolver(index)
    holders: list[ProcedureDoc | ProgramDoc] = [*index.procedures, *index.programs]

    for target in index.procedures:
        target.called_by = []
    for holder in holders:
        holder.review_flags = [
            flag
            for flag in holder.review_flags
            if flag.code not in CALL_RESOLUTION_FLAG_CODES
        ]
        for call in holder.calls:
            candidates = resolver.candidates(holder, call)
            identities = sorted(_procedure_identity(item) for item in candidates)
            call.resolution_candidates = identities
            call.resolved = len(candidates) == 1
            call.resolved_target = identities[0] if call.resolved else None
            if len(candidates) > 1:
                holder.review_flags.append(
                    ReviewFlag(
                        code="ambiguous_call",
                        severity="warning",
                        message=(
                            f"{call.kind} call {call.name!r} has {len(candidates)} "
                            "equally visible definitions"
                        ),
                        location=call.location,
                        target=call.name,
                    )
                )
                continue
            if not call.resolved:
                continue
            target = candidates[0]
            caller = holder.name.lower()
            if caller not in target.called_by:
                target.called_by.append(caller)

    for procedure in index.procedures:
        procedure.called_by.sort()

    derive_project_call_paths(index)


def derive_project_call_paths(index: ProjectIndex) -> None:
    """Populate deterministic, cycle-safe paths over exact resolved targets.

    A path contains its root identity and at least one resolved target identity,
    and ends at a leaf or a cycle closure. Direct edges remain available on
    ``CallRef``; storing every prefix here would duplicate them and materially
    inflate the portable snapshot. Repeated observations of the same edge do
    not duplicate a derived path; the observations themselves remain untouched.

    Traversal follows simple paths. When an edge returns to an identity already
    in the current path, that one closing edge is retained and recursion stops.
    Thus recursive and mutually-recursive graphs are visible but always finite.
    """

    by_identity = {
        _procedure_identity(procedure): procedure for procedure in index.procedures
    }
    adjacency: dict[str, list[str]] = {}
    for identity, procedure in by_identity.items():
        targets = {
            call.resolved_target
            for call in procedure.calls
            if call.resolved and call.resolved_target in by_identity
        }
        adjacency[identity] = sorted(target for target in targets if target is not None)

    for root_identity, procedure in by_identity.items():
        paths: list[list[str]] = []

        def visit(identity: str, path: list[str], visited: set[str]) -> None:
            for target in adjacency[identity]:
                next_path = [*path, target]
                if target in visited:
                    paths.append(next_path)
                    continue
                if adjacency[target]:
                    visit(target, next_path, {*visited, target})
                else:
                    paths.append(next_path)

        visit(root_identity, [root_identity], {root_identity})
        procedure.call_paths = paths


# --------------------------------------------------------------------------
# Shared state: which module variables each procedure reads and writes
# --------------------------------------------------------------------------

_IDENTIFIER = re.compile(r"[A-Za-z_]\w*")


def _identifiers(text: str | None) -> set[str]:
    return {match.group(0).lower() for match in _IDENTIFIER.finditer(text or "")}


def annotate_project_dataflow(index: ProjectIndex) -> None:
    """Derive `reads`/`writes` from the index's own records.

    Module variables are the shared state that carries data between routines, so
    a procedure's own arguments and locals are excluded: a local name must never
    masquerade as shared state.

    This reads nothing from disk. The facts come from the records the parser
    already produced -- assignment targets and expressions, and the statement
    text on control steps, calls and I/O operations -- which is what plan
    decision 2 requires of a projection: derived from the canonical
    ``ProjectIndex``, never from a second parse.

    Deriving it from statements rather than from physical lines also drops four
    classes of false positive that a line-by-line reading cannot avoid:

    * a ``use m, only: hru`` import counted ``hru`` as a read, though an import
      reads nothing;
    * a ``format`` statement counted the identifiers inside its quoted literals,
      so ``100 format (1x,'   hru','  day')`` read ``hru`` and ``day``;
    * ``a = 0; b = 0`` matched only the first target and counted the rest of the
      line as reads, so ``b`` was a read of the variable it actually writes; and
    * a host procedure's line span covers its contained procedures, so it
      absorbed their state access as well as its own.

    Continuations move the other way: a statement split across lines used to be
    classified one physical line at a time, so a joined statement now
    contributes reads that the fragments lost.
    """

    module_variables = {
        variable.name.lower() for module in index.modules for variable in module.variables
    }
    if not module_variables:
        return

    for holder in (*index.procedures, *index.programs):
        local = {argument.lower() for argument in getattr(holder, "args", ())}
        local |= {variable.name.lower() for variable in getattr(holder, "variables", ())}
        candidates = module_variables - local

        reads: set[str] = set()
        writes: set[str] = set()

        for assignment in getattr(holder, "assignments", ()):
            root = (assignment.target_root or "").lower()
            if root in candidates:
                writes.add(root)
            # Only the right-hand side is read. A subscript on the left selects
            # where to store, and was never counted as a read.
            reads |= _identifiers(assignment.expression) & candidates

        for record in (
            *holder.control_steps,
            *holder.calls,
            *getattr(holder, "io", ()),
        ):
            reads |= _identifiers(record.raw) & candidates

        # A variable written is not also reported as a plain read of itself.
        reads -= writes
        holder.reads = sorted(reads)
        holder.writes = sorted(writes)
