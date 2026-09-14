"""Bind I/O units to filenames across files.

A unit is bound to a filename by an `open`. The index binds them while walking
one file, which is enough for SWAT+ input routines -- they open and read in the
same procedure -- and not enough for output, where a unit is opened centrally
and written to from elsewhere. An operation whose unit is unbound keeps the
index's `unit_<unit>` sentinel, and roughly 96% of SWAT+ write statements
carried one.

Three populations hide behind that sentinel, and only one of them is a parser
limitation:

* **Opened through a helper.** SWAT+ funnels most output opens through
  `open_output_file(iunit, filename, recl)`, and some through a wrapper that
  forwards to it. Unit and filename are literals at the call site, so the
  binding is recoverable -- this module recovers it.
* **Never opened at all.** Units such as 9000 and 2612 are written to and
  opened nowhere in the source; Fortran gives them a compiler-default file.
  There is no filename in the source to find, so the sentinel is the correct
  answer and is left alone.
* **Reused for many files.** Unit 107 is opened against 147 different files as
  the input-reading scratch unit. Binding it project-wide would be wrong, so a
  unit that resolves to more than one filename stays unresolved.

The last two are why this is not "collect every open into one map": that map
would name 107 after whichever file happened to be scanned last.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from .schema_fortran import split_top_level_commas, string_literal
from .schema_model import ReviewFlag

# The index's sentinel for an operation whose unit it could not bind.
_SENTINEL_RE = re.compile(r"unit_(?P<unit>.+)", re.DOTALL)

# Intrinsics that hand back their argument unchanged as far as a filename is
# concerned. `get_output_filename` is SWAT+'s own: it prepends the configured
# output directory when one is set, so the literal passed in is the resolved
# *default*, which is what every filename in these reports already means.
_TRANSPARENT = ("trim", "adjustl", "adjustr", "get_output_filename")

_CALL_RE = re.compile(r"\bcall\s+(?P<name>[A-Za-z_]\w*)\s*\((?P<args>.*)\)\s*$", re.I | re.S)
_INT_RE = re.compile(r"-?\d+\Z")

# A helper chain deeper than this is not SWAT+'s shape; the cap keeps a cyclic
# or pathological call graph from spinning.
_MAX_FORWARDING_ROUNDS = 4


def _strip_transparent(expr: str) -> str:
    """Peel `trim(...)`-style wrappers off a filename expression."""
    text = (expr or "").strip()
    for _ in range(8):
        match = re.fullmatch(r"(?P<fn>[A-Za-z_]\w*)\s*\((?P<inner>.*)\)", text, re.S)
        if not match or match.group("fn").lower() not in _TRANSPARENT:
            return text
        inner = split_top_level_commas(match.group("inner"))
        if len(inner) != 1:
            return text
        text = inner[0].strip()
    return text


def _argument_index(procedure, expr: str, depth: int = 0) -> int | None:
    """Which of the procedure's own arguments does this expression come from?

    Follows local assignments backwards, so `open (iunit, file=trim(full_path))`
    with `full_path = get_output_filename(filename)` lands on `filename`. Only
    a straight chain of single-source assignments counts; anything else returns
    None and the unit simply stays unresolved.
    """
    if depth > 4:
        return None
    args = [a.lower() for a in (procedure.args or [])]
    name = _strip_transparent(expr).lower()
    if name in args:
        return args.index(name)
    for assignment in procedure.assignments:
        if (assignment.target or "").strip().lower() == name:
            return _argument_index(procedure, assignment.expression or "", depth + 1)
    return None


def _open_helpers(project) -> dict[str, tuple[int, int]]:
    """Procedures that open a unit and a filename both handed to them."""
    helpers: dict[str, tuple[int, int]] = {}
    for procedure in project.procedures:
        for operation in procedure.io:
            if operation.kind != "open" or not operation.unit:
                continue
            unit_index = _argument_index(procedure, operation.unit)
            if unit_index is None:
                continue
            file_index = _argument_index(
                procedure, operation.file_resolved or operation.file_expr or ""
            )
            if file_index is None or file_index == unit_index:
                continue
            helpers.setdefault(procedure.name.lower(), (unit_index, file_index))
    return helpers


def _call_arguments(raw: str) -> list[str] | None:
    match = _CALL_RE.search((raw or "").strip())
    if not match:
        return None
    return [part.strip() for part in split_top_level_commas(match.group("args"))]


def _forward_helpers(project, helpers: dict[str, tuple[int, int]]) -> None:
    """Grow the helper set through wrappers that pass their own arguments on.

    `open_cb_wide_pair(u_txt, u_csv, fname_txt, fname_csv, vars)` never opens
    anything itself; it calls `open_output_file(u_txt, fname_txt, rl)`. Its own
    call sites carry the literals, so it has to be treated as a helper too.
    """
    for _ in range(_MAX_FORWARDING_ROUNDS):
        added = False
        for procedure in project.procedures:
            name = procedure.name.lower()
            if name in helpers:
                continue
            args = [a.lower() for a in (procedure.args or [])]
            if not args:
                continue
            for call in procedure.calls:
                target = helpers.get(call.name.lower())
                if target is None:
                    continue
                parts = _call_arguments(call.raw)
                if parts is None or len(parts) <= max(target):
                    continue
                unit_arg = _strip_transparent(parts[target[0]]).lower()
                file_arg = _strip_transparent(parts[target[1]]).lower()
                if unit_arg in args and file_arg in args:
                    helpers[name] = (args.index(unit_arg), args.index(file_arg))
                    added = True
                    break
        if not added:
            return


def _bindings_from_call_sites(project, helpers: dict[str, tuple[int, int]], where=None):
    """unit -> every filename it is opened against through a helper."""
    found: dict[str, set[str]] = defaultdict(set)
    for procedure in project.procedures:
        for call in procedure.calls:
            target = helpers.get(call.name.lower())
            if target is None:
                continue
            parts = _call_arguments(call.raw)
            if parts is None or len(parts) <= max(target):
                continue
            unit = parts[target[0]].strip()
            filename = string_literal(_strip_transparent(parts[target[1]]))
            # Only literals bind. A unit or filename still held in a variable at
            # the call site would need the value, which is a run of the model.
            if filename and _INT_RE.fullmatch(unit):
                found[unit.lower()].add(filename)
                if where is not None:
                    where.setdefault((unit.lower(), filename), call.location)
    return found


def _bindings_from_opens(project, where=None):
    """unit -> every filename an `open` names directly, project-wide."""
    found: dict[str, set[str]] = defaultdict(set)
    for procedure in project.procedures:
        for operation in procedure.io:
            if operation.kind != "open" or not operation.unit:
                continue
            resolved = operation.file_resolved or ""
            if not resolved or _SENTINEL_RE.fullmatch(resolved):
                continue
            found[operation.unit.lower()].add(resolved)
            if where is not None:
                where.setdefault((operation.unit.lower(), resolved), operation.location)
    return found


def resolve_project_unit_files(project) -> dict[str, Any]:
    """Name the files behind `unit_<unit>` where the source says which they are.

    Runs on the completed index, because the `open` that binds a unit is
    routinely in a different file from the writes that use it. Returns a
    summary of what it bound, for the diagnostics that report coverage.
    """
    helpers = _open_helpers(project)
    _forward_helpers(project, helpers)

    where: dict[tuple[str, str], Any] = {}
    from_opens = _bindings_from_opens(project, where)
    from_calls = _bindings_from_call_sites(project, helpers, where)
    candidates: dict[str, set[str]] = defaultdict(set)
    for source in (from_opens, from_calls):
        for unit, names in source.items():
            candidates[unit] |= names

    # One unit, one filename, or nothing. See the module docstring on unit 107.
    bindings = {unit: next(iter(n)) for unit, n in candidates.items() if len(n) == 1}
    ambiguous = sorted(unit for unit, n in candidates.items() if len(n) > 1)

    # A unit opened against two different filenames is not a parser problem to
    # work around -- whichever file is opened second takes the unit, and the
    # first is left dangling. Report it where it happens instead of picking one.
    #
    # Only for units opened through the output helpers. Reusing one unit for a
    # run of input files is ordinary Fortran -- open, read, close, open the next
    # -- and units 1 and 104-108 are exactly that; flagging them would bury the
    # output collisions in noise. An output file is opened once and written to
    # for the whole run, so two files on one unit there is a real conflict.
    for unit in ambiguous:
        if len(from_calls.get(unit, ())) < 2:
            continue
        names = sorted(candidates[unit])
        location = where.get((unit, names[0]))
        if location is None:
            continue
        project.review_flags.append(
            ReviewFlag(
                code="io_unit_bound_to_several_files",
                severity="warning",
                message=(
                    f"unit {unit} is opened against "
                    + ", ".join(names)
                    + "; its filename cannot be resolved for operations elsewhere"
                ),
                location=location,
                target=location.path,
            )
        )

    rebound = 0
    for procedure in project.procedures:
        for operation in procedure.io:
            match = _SENTINEL_RE.fullmatch(operation.file_resolved or "")
            if not match:
                continue
            filename = bindings.get(match.group("unit").lower())
            if filename:
                operation.file_resolved = filename
                rebound += 1

    return {
        "helpers": sorted(helpers),
        "bound_units": len(bindings),
        "ambiguous_units": ambiguous,
        "rebound_operations": rebound,
    }
