from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


def record_scope(module: str | None = None, parent: str | None = None) -> str | None:
    """Return the lexical scope carried by a named rich-model record."""

    parts = [part.lower() for part in (module, parent) if part]
    return "/".join(parts) or None


def record_identity(
    kind: str, name: str, path: str, scope: str | None = None
) -> str:
    """Stable identity for a named record: kind, name, file, and scope.

    Bare names collide in SWAT+ -- a derived type and a procedure share
    ``salt_balance``, and same-named types live in different modules -- so a
    name alone cannot address a record. The defining file distinguishes records
    in separate files; the optional lexical scope distinguishes module members
    and contained declarations that legitimately repeat a name in one file.
    This does not disturb ``FactStore.add()``'s existing key behaviour or
    ``RichStore.get_of_kind()``'s fail-closed lookup.
    """
    base = f"{kind.lower()}:{name.lower()}:{path}"
    return f"{base}:{scope.lower()}" if scope else base


@dataclass(slots=True)
class SourceLocation:
    path: str
    line: int
    end_line: int | None = None

    def label(self) -> str:
        if self.end_line and self.end_line != self.line:
            return f"{self.path}:{self.line}-{self.end_line}"
        return f"{self.path}:{self.line}"


@dataclass(slots=True)
class ReviewFlag:
    code: str
    severity: str
    message: str
    location: SourceLocation | None = None
    target: str | None = None


@dataclass(slots=True)
class VariableRef:
    name: str
    declaration: str
    location: SourceLocation
    vartype: str | None = None
    initial: str | None = None
    doc: str = ""


@dataclass(slots=True)
class UseRef:
    module: str
    only: list[str] = field(default_factory=list)
    intrinsic: bool = False
    location: SourceLocation | None = None
    renames: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CallRef:
    name: str
    raw: str
    location: SourceLocation
    resolved: bool = False
    kind: str = "subroutine"  # "subroutine" (call stmt) or "function" (expression reference)
    # Phase 4 semantic results. These stay internal while the rich-v3 wire
    # contract is frozen: the stable identity identifies the one definition a
    # call resolved to, while candidates retains every equally-visible target
    # when resolution must fail closed.
    resolved_target: str | None = None
    resolution_candidates: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ControlStep:
    """One control-flow statement, placed in its procedure's block tree.

    The four nesting fields are what turn a flat source-order outline into a
    tree a consumer can walk: `block_id` identifies a construct, `parent_id`
    points at the construct enclosing this statement, and `branch_of` marks the
    `else`/`else if`/`case` arms that belong to a construct without being nested
    inside it. Depth counts enclosing open blocks, so a construct and the arms
    and end of that same construct all share one depth, and its body sits one
    deeper.
    """

    kind: str
    summary: str
    raw: str
    location: SourceLocation
    depth: int = 0
    # Set only on a statement that opens a block; unique within its procedure.
    block_id: int | None = None
    parent_id: int | None = None
    # For else / else if / case: the construct this arm belongs to.
    branch_of: int | None = None
    # For a block opener: the line of its matching end statement. Stays None if
    # the construct is never closed before the procedure ends.
    end_line: int | None = None


@dataclass(slots=True)
class AssignmentDoc:
    """One assignment statement, with its two sides kept apart.

    A superset of :class:`ControlStep`: ``kind``, ``summary``, ``raw`` and
    ``location`` keep their existing meaning and position so a consumer reading
    only those is unaffected. The scanner's assignment pattern already captured
    both sides and discarded them, which left every consumer re-deriving the
    target from ``raw`` with its own regex, or worse, by stripping the ``Sets ``
    prefix off the human-readable ``summary``.
    """

    kind: str
    summary: str
    raw: str
    location: SourceLocation
    # The target exactly as written, subscripts and component chain included
    # (e.g. ``gw_state(cell_id)%stor``).
    target: str | None = None
    # The bare root of that target (e.g. ``gw_state``) -- the name dataflow and
    # state-change joins actually key on.
    target_root: str | None = None
    # The right-hand side as written, untrimmed of intent.
    expression: str | None = None


@dataclass(slots=True)
class SelectCaseDoc:
    """A ``select case (subject)`` block's string-literal case labels.

    Captures the closed vocabulary a dispatcher recognizes -- e.g. SWAT+'s
    decision-table condition/action type names, or a hand-parsed file's
    legal config keys -- which a per-read-statement field list can't
    represent at all. Only ``case ('literal')`` labels are recorded; a
    ``case default`` or a non-literal case selector contributes nothing.
    """

    subject: str
    cases: list[str]
    location: SourceLocation


@dataclass(slots=True)
class IOOperation:
    kind: str
    unit: str | None
    file_expr: str | None
    file_resolved: str | None
    raw: str
    location: SourceLocation
    fields: list[str] = field(default_factory=list)
    condition: str | None = None


@dataclass(slots=True)
class DerivedTypeDoc:
    name: str
    location: SourceLocation
    module: str | None = None
    parent: str | None = None
    doc: str = ""
    components: list[VariableRef] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)
    identity: str | None = None


@dataclass(slots=True)
class ProcedureDoc:
    name: str
    kind: str
    location: SourceLocation
    module: str | None = None
    parent: str | None = None
    args: list[str] = field(default_factory=list)
    doc: str = ""
    uses: list[UseRef] = field(default_factory=list)
    variables: list[VariableRef] = field(default_factory=list)
    calls: list[CallRef] = field(default_factory=list)
    called_by: list[str] = field(default_factory=list)
    # Every maximal resolved path starting here. Entries are stable ProcedureDoc
    # identities (including this procedure as the root), not bare names. A
    # final repeated identity marks a cycle closure.
    call_paths: list[list[str]] = field(default_factory=list)
    control_steps: list[ControlStep] = field(default_factory=list)
    io: list[IOOperation] = field(default_factory=list)
    assignments: list[AssignmentDoc] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)
    select_cases: list[SelectCaseDoc] = field(default_factory=list)
    identity: str | None = None
    # Shared state this procedure touches: module variables it reads and
    # writes, derived from the records above rather than from a second reading
    # of the source. A name written is not also listed as read.
    reads: list[str] = field(default_factory=list)
    writes: list[str] = field(default_factory=list)

    @property
    def qualified_name(self) -> str:
        if self.module:
            return f"{self.module}::{self.name}"
        return self.name


@dataclass(slots=True)
class ModuleDoc:
    name: str
    location: SourceLocation
    doc: str = ""
    uses: list[UseRef] = field(default_factory=list)
    variables: list[VariableRef] = field(default_factory=list)
    procedures: list[str] = field(default_factory=list)
    types: list[str] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)
    identity: str | None = None


@dataclass(slots=True)
class ProgramDoc:
    name: str
    location: SourceLocation
    doc: str = ""
    uses: list[UseRef] = field(default_factory=list)
    calls: list[CallRef] = field(default_factory=list)
    control_steps: list[ControlStep] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)
    identity: str | None = None
    # As on ProcedureDoc. A program carries no `assignments` or `io` records, so
    # its writes cannot be derived and stay empty; the pinned tree contains no
    # program, so this has no effect there.
    reads: list[str] = field(default_factory=list)
    writes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SourceFileDoc:
    path: str
    modules: list[str] = field(default_factory=list)
    programs: list[str] = field(default_factory=list)
    procedures: list[str] = field(default_factory=list)
    types: list[str] = field(default_factory=list)


@dataclass(slots=True)
class IOFileDoc:
    key: str
    display_name: str
    operations: list[IOOperation] = field(default_factory=list)
    procedures: list[str] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)


@dataclass(slots=True)
class OutputFile:
    """A single physical output file within a time-series output family."""

    name: str
    frequency: str  # day | mon | yr | aa | unknown
    fmt: str  # txt | csv | unknown
    unit: str | None
    open_location: SourceLocation
    open_condition: str | None = None


@dataclass(slots=True)
class OutputFamilyDoc:
    """A time-series output family (e.g. hru_wb_*) auto-detected from source.

    A family groups the day/mon/yr/aa text and CSV files that share a base
    name and are opened through the SWAT+ ``open_output_file`` convention.
    """

    key: str
    display_name: str
    base: str
    opened_by: list[str] = field(default_factory=list)
    written_by: list[str] = field(default_factory=list)
    files: list[OutputFile] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)


@dataclass(slots=True)
class ProjectIndex:
    project_name: str
    source_root: str
    files: list[SourceFileDoc] = field(default_factory=list)
    modules: list[ModuleDoc] = field(default_factory=list)
    programs: list[ProgramDoc] = field(default_factory=list)
    procedures: list[ProcedureDoc] = field(default_factory=list)
    types: list[DerivedTypeDoc] = field(default_factory=list)
    io_files: list[IOFileDoc] = field(default_factory=list)
    output_families: list[OutputFamilyDoc] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
