from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


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


@dataclass(slots=True)
class CallRef:
    name: str
    raw: str
    location: SourceLocation
    resolved: bool = False
    kind: str = "subroutine"  # "subroutine" (call stmt) or "function" (expression reference)


@dataclass(slots=True)
class ControlStep:
    kind: str
    summary: str
    raw: str
    location: SourceLocation


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
    doc: str = ""
    components: list[VariableRef] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)


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
    call_paths: list[list[str]] = field(default_factory=list)
    control_steps: list[ControlStep] = field(default_factory=list)
    io: list[IOOperation] = field(default_factory=list)
    assignments: list[ControlStep] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)
    select_cases: list[SelectCaseDoc] = field(default_factory=list)

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


@dataclass(slots=True)
class ProgramDoc:
    name: str
    location: SourceLocation
    doc: str = ""
    uses: list[UseRef] = field(default_factory=list)
    calls: list[CallRef] = field(default_factory=list)
    control_steps: list[ControlStep] = field(default_factory=list)
    review_flags: list[ReviewFlag] = field(default_factory=list)


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
