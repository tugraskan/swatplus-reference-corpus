"""Phase 6: the field-level parity harness.

Phase 0's comparison asked whether two stores agreed on a symbol's span and a
couple of counts. That cannot answer the question cutover actually turns on --
*does the fparser2 path lose anything?* -- because equal counts hide unequal
contents, and a span can match while every statement inside it differs.

This compares the two parsers' completed indexes field by field and sorts every
difference into one of three buckets:

* **approved corrections** -- differences this project has examined, explained
  and accepted as the AST path being right. They are listed here, never
  normalised away, because the plan's exit gate asks for them to be "recorded
  as intentional improvements rather than hidden".
* **unexpected differences** -- anything else. These fail the harness.
* **agreement** -- everything that matched.

What must never be normalised is fixed by the plan and enforced by comparing it
verbatim: raw statements, I/O fields, conditions, summaries, source spans and
source hashes are byte-sensitive contracts. Only the *ordering* of a collection
and the *case* of a Fortran name may be normalised, because Fortran itself is
case-insensitive and collection order is an artifact of traversal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Sequence

from .schema_model import ProjectIndex


# --------------------------------------------------------------------------
# The approved corrections
#
# Each entry says: in this category, for this field, differences confined to
# these files are expected, and here is why. A difference in a file not listed
# is unexpected and fails, which is what stops this table from becoming a way
# to make parity look better than it is.
# --------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ApprovedCorrection:
    category: str
    fields: frozenset[str]
    owners: frozenset[str]
    reason: str


APPROVED_CORRECTIONS: tuple[ApprovedCorrection, ...] = (
    ApprovedCorrection(
        category="procedures",
        fields=frozenset({"assignments"}),
        owners=frozenset(
            {
                "climate_control.f90",
                "command.f90",
                "gwflow_read.f90",
                "hyd_connect.f90",
                "res_control.f90",
                "ru_read_elements.f90",
                "salt_chem_aqu.f90",
                "salt_chem_hru.f90",
                "salt_chem_soil_single.f90",
                "swr_percmacro.f90",
            }
        ),
        reason=(
            "The scanner's assignment pattern cannot span a target whose own "
            "subscript contains parentheses, and cannot match past a leading "
            "statement label, so it dropped those statements outright. The AST "
            "path splits at the first `=` at paren depth zero and recovers 63 "
            "assignments the scanner never recorded."
        ),
    ),
    ApprovedCorrection(
        category="procedures",
        fields=frozenset({"control_steps", "io"}),
        owners=frozenset({"carbon_layers_read.f90", "gwflow_pond.f90"}),
        reason=(
            "Statement labels. `99 close (107)` is not recognised as I/O by a "
            "pattern anchored on the keyword, and `10  enddo` is not recognised "
            "as a block close, so the loop it ends stays open and swallows the "
            "enclosing `end if` -- leaving one construct unclosed tree-wide and "
            "every statement after it one level too deep."
        ),
    ),
    ApprovedCorrection(
        category="procedures",
        fields=frozenset({"reads", "writes"}),
        owners=frozenset({"salt_chem_soil_single.f90"}),
        reason=(
            "`10    upion1 = Sul_Conc(salt_c4)` carries a statement label, so "
            "the scanner records no assignment and reports `upion1` as a read "
            "of the variable it writes. The same labelled-statement finding, "
            "surfacing in the shared-state family."
        ),
    ),
    ApprovedCorrection(
        category="io_files",
        fields=frozenset({"operations"}),
        owners=frozenset(
            {
                "carbon_layers.prt",
                # Named `unit_out_pond_conc` / `unit_out_pond_mass` until units
                # were bound across files: `gwflow_read.f90` opens them, and the
                # writes this correction is about are in `gwflow_pond.f90`.
                "gwflow_pond_conc_day.txt",
                "gwflow_pond_mass_day.txt",
            }
        ),
        reason=(
            "Downstream of the same two labelled statements: the recovered "
            "`99 close (107)` joins `carbon_layers.prt`, and the pond writes "
            "carry a different condition trail because the scanner's stack "
            "never popped the labelled `enddo`."
        ),
    ),
)


# --------------------------------------------------------------------------
# Normalisation -- deliberately minimal
# --------------------------------------------------------------------------


def _name(value: str | None) -> str:
    """Fortran is case-insensitive, so a name's case is not a difference."""

    return (value or "").lower()


def _variable(variable) -> tuple:
    # `declaration`, `initial` and `doc` are compared verbatim: they are the
    # byte-sensitive strings the schema resolver matches on.
    return (
        _name(variable.name),
        variable.declaration,
        variable.vartype,
        variable.initial,
        variable.doc,
        variable.location.line,
        variable.location.end_line,
    )


def _use(use) -> tuple:
    return (
        _name(use.module),
        tuple(_name(item) for item in use.only),
        use.intrinsic,
        use.location.line if use.location else None,
    )


def _control_step(step) -> tuple:
    # summary, raw and the whole block-tree placement, verbatim.
    return (
        step.kind,
        step.summary,
        step.raw,
        step.location.line,
        step.depth,
        step.block_id,
        step.parent_id,
        step.branch_of,
        step.end_line,
    )


def _assignment(assignment) -> tuple:
    return (
        assignment.kind,
        assignment.summary,
        assignment.raw,
        assignment.location.line,
        assignment.target,
        assignment.target_root,
        assignment.expression,
    )


def _call(call) -> tuple:
    # `name` keeps its observed spelling; only the resolution result is derived.
    return (
        call.name,
        call.raw,
        call.location.line,
        call.kind,
        call.resolved,
        call.resolved_target,
    )


def _io(operation) -> tuple:
    # fields and condition, verbatim.
    return (
        operation.kind,
        operation.unit,
        operation.file_expr,
        operation.file_resolved,
        operation.raw,
        operation.location.line,
        tuple(operation.fields),
        operation.condition,
    )


def _select_case(select) -> tuple:
    return (select.subject, tuple(select.cases), select.location.line)


def _each(extract: Callable[[Any], tuple]) -> Callable[[Any], list[tuple]]:
    return lambda records: [extract(record) for record in records]


# --------------------------------------------------------------------------
# The categories
# --------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Category:
    name: str
    select: Callable[[ProjectIndex], Sequence[Any]]
    key: Callable[[Any], tuple | str]
    # The file (or I/O key) a record belongs to, used to match an approved
    # correction against the record that differs.
    owner: Callable[[Any], str]
    fields: tuple[tuple[str, Callable[[Any], Any]], ...]


CATEGORIES: tuple[Category, ...] = (
    Category(
        name="modules",
        select=lambda index: index.modules,
        key=lambda m: (m.location.path, _name(m.name)),
        owner=lambda m: m.location.path,
        fields=(
            ("doc", lambda m: m.doc),
            ("span", lambda m: (m.location.line, m.location.end_line)),
            ("variables", lambda m: _each(_variable)(m.variables)),
            ("uses", lambda m: _each(_use)(m.uses)),
            ("procedures", lambda m: [_name(x) for x in m.procedures]),
            ("types", lambda m: [_name(x) for x in m.types]),
        ),
    ),
    Category(
        name="programs",
        select=lambda index: index.programs,
        key=lambda p: (p.location.path, _name(p.name)),
        owner=lambda p: p.location.path,
        fields=(
            ("doc", lambda p: p.doc),
            ("span", lambda p: (p.location.line, p.location.end_line)),
            ("uses", lambda p: _each(_use)(p.uses)),
            ("calls", lambda p: _each(_call)(p.calls)),
            ("control_steps", lambda p: _each(_control_step)(p.control_steps)),
        ),
    ),
    Category(
        name="types",
        select=lambda index: index.types,
        key=lambda t: (t.location.path, _name(t.name), t.location.line),
        owner=lambda t: t.location.path,
        fields=(
            ("doc", lambda t: t.doc),
            ("module", lambda t: _name(t.module)),
            ("parent", lambda t: _name(t.parent)),
            ("span", lambda t: (t.location.line, t.location.end_line)),
            ("components", lambda t: _each(_variable)(t.components)),
        ),
    ),
    Category(
        name="procedures",
        select=lambda index: index.procedures,
        key=lambda p: (p.location.path, _name(p.name), p.kind),
        owner=lambda p: p.location.path,
        fields=(
            ("args", lambda p: [_name(x) for x in p.args]),
            ("doc", lambda p: p.doc),
            ("module", lambda p: _name(p.module)),
            ("parent", lambda p: _name(p.parent)),
            ("span", lambda p: (p.location.line, p.location.end_line)),
            ("variables", lambda p: _each(_variable)(p.variables)),
            ("uses", lambda p: _each(_use)(p.uses)),
            ("assignments", lambda p: _each(_assignment)(p.assignments)),
            ("control_steps", lambda p: _each(_control_step)(p.control_steps)),
            ("calls", lambda p: _each(_call)(p.calls)),
            ("io", lambda p: _each(_io)(p.io)),
            ("select_cases", lambda p: _each(_select_case)(p.select_cases)),
            ("called_by", lambda p: sorted(_name(x) for x in p.called_by)),
            ("reads", lambda p: p.reads),
            ("writes", lambda p: p.writes),
        ),
    ),
    Category(
        name="io_files",
        select=lambda index: index.io_files,
        key=lambda f: f.key,
        owner=lambda f: f.key,
        fields=(
            ("operations", lambda f: _each(_io)(f.operations)),
            ("procedures", lambda f: [_name(x) for x in f.procedures]),
        ),
    ),
    Category(
        name="output_families",
        select=lambda index: index.output_families,
        key=lambda f: f.key,
        owner=lambda f: f.key,
        fields=(
            ("base", lambda f: f.base),
            ("opened_by", lambda f: [_name(x) for x in f.opened_by]),
            ("written_by", lambda f: [_name(x) for x in f.written_by]),
            (
                "files",
                lambda f: [
                    (x.name, x.frequency, x.fmt, x.unit, x.open_condition)
                    for x in f.files
                ],
            ),
        ),
    ),
)


# --------------------------------------------------------------------------
# The report
# --------------------------------------------------------------------------


@dataclass(slots=True)
class Disagreement:
    category: str
    field: str
    owner: str
    record: str
    approved: bool
    reason: str | None = None


@dataclass(slots=True)
class CategoryParity:
    name: str
    shared: int
    identical: int
    ast_only: list[str] = field(default_factory=list)
    rich_only: list[str] = field(default_factory=list)
    disagreements: list[Disagreement] = field(default_factory=list)


@dataclass(slots=True)
class ParityReport:
    categories: list[CategoryParity] = field(default_factory=list)

    @property
    def unexpected(self) -> list[Disagreement]:
        return [
            d
            for category in self.categories
            for d in category.disagreements
            if not d.approved
        ]

    @property
    def approved(self) -> list[Disagreement]:
        return [
            d
            for category in self.categories
            for d in category.disagreements
            if d.approved
        ]

    def missing_records(self) -> list[str]:
        """Records one parser found and the other did not, in either direction."""

        out: list[str] = []
        for category in self.categories:
            out.extend(f"{category.name}: only in fparser2: {k}" for k in category.ast_only)
            out.extend(f"{category.name}: missing from fparser2: {k}" for k in category.rich_only)
        return out

    def failures(self) -> list[str]:
        """Everything that blocks the Phase 6 exit gate."""

        problems = self.missing_records()
        problems.extend(
            f"{d.category}.{d.field}: unexpected difference in {d.record}"
            for d in self.unexpected
        )
        return problems

    def to_dict(self) -> dict[str, Any]:
        return {
            "categories": [
                {
                    "name": c.name,
                    "shared": c.shared,
                    "identical": c.identical,
                    "ast_only": c.ast_only,
                    "rich_only": c.rich_only,
                    "approved_disagreements": sorted(
                        {f"{d.field}:{d.owner}" for d in c.disagreements if d.approved}
                    ),
                    "unexpected_disagreements": sorted(
                        f"{d.field}:{d.record}" for d in c.disagreements if not d.approved
                    ),
                }
                for c in self.categories
            ],
            "approved_corrections": [
                {
                    "category": correction.category,
                    "fields": sorted(correction.fields),
                    "owners": sorted(correction.owners),
                    "reason": correction.reason,
                }
                for correction in APPROVED_CORRECTIONS
            ],
        }


def _approval(category: str, field_name: str, owner: str) -> ApprovedCorrection | None:
    for correction in APPROVED_CORRECTIONS:
        if (
            correction.category == category
            and field_name in correction.fields
            and owner in correction.owners
        ):
            return correction
    return None


def _render_key(key: tuple | str) -> str:
    return key if isinstance(key, str) else ":".join(str(part) for part in key)


def compare_indexes(ast: ProjectIndex, rich: ProjectIndex) -> ParityReport:
    """Compare two completed indexes field by field.

    Both indexes must already carry their semantic layer -- resolved calls and
    derived shared state -- or the fields that depend on it compare as
    differences rather than as agreement.
    """

    report = ParityReport()
    for category in CATEGORIES:
        ast_records = {category.key(x): x for x in category.select(ast)}
        rich_records = {category.key(x): x for x in category.select(rich)}
        shared = ast_records.keys() & rich_records.keys()

        parity = CategoryParity(
            name=category.name,
            shared=len(shared),
            identical=0,
            ast_only=sorted(_render_key(k) for k in ast_records.keys() - rich_records.keys()),
            rich_only=sorted(_render_key(k) for k in rich_records.keys() - ast_records.keys()),
        )
        for key in sorted(shared, key=_render_key):
            left, right = ast_records[key], rich_records[key]
            owner = category.owner(left)
            differing = False
            for field_name, extract in category.fields:
                if extract(left) == extract(right):
                    continue
                differing = True
                correction = _approval(category.name, field_name, owner)
                parity.disagreements.append(
                    Disagreement(
                        category=category.name,
                        field=field_name,
                        owner=owner,
                        record=_render_key(key),
                        approved=correction is not None,
                        reason=correction.reason if correction else None,
                    )
                )
            if not differing:
                parity.identical += 1
        report.categories.append(parity)
    return report


def format_report(report: ParityReport) -> str:
    """A short human-readable summary, for the CLI."""

    lines: list[str] = []
    for category in report.categories:
        approved = len({(d.field, d.owner) for d in category.disagreements if d.approved})
        unexpected = len([d for d in category.disagreements if not d.approved])
        lines.append(
            f"{category.name:17s} shared={category.shared:5d} "
            f"identical={category.identical:5d} "
            f"approved={approved:3d} unexpected={unexpected:3d}"
        )
        for key in category.ast_only:
            lines.append(f"    only in fparser2: {key}")
        for key in category.rich_only:
            lines.append(f"    missing from fparser2: {key}")
        for disagreement in category.disagreements:
            if not disagreement.approved:
                lines.append(
                    f"    UNEXPECTED {disagreement.field}: {disagreement.record}"
                )
    return "\n".join(lines)
