from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
import re

from .schema_config import BuildConfig
from .schema_model import (
    CallRef,
    ControlStep,
    DerivedTypeDoc,
    IOOperation,
    ModuleDoc,
    ProcedureDoc,
    ProgramDoc,
    ProjectIndex,
    SelectCaseDoc,
    SourceFileDoc,
    SourceLocation,
    UseRef,
    VariableRef,
)


MODULE_RE = re.compile(r"^\s*module\s+(?!procedure\b)([a-z_]\w*)\b", re.I)
PROGRAM_RE = re.compile(r"^\s*program\s+([a-z_]\w*)\b", re.I)
SUBROUTINE_RE = re.compile(
    r"^\s*(?:(?:recursive|pure|elemental|module)\s+)*subroutine\s+([a-z_]\w*)\s*(?:\((.*)\))?",
    re.I,
)
FUNCTION_RE = re.compile(
    r"^\s*(?:(?:recursive|pure|elemental|module)\s+)*(?:(?:[\w(),=*]+\s+)+)?function\s+([a-z_]\w*)\s*(?:\((.*)\))?",
    re.I,
)
# The space in `end type` / `end module` / ... is optional in Fortran, and
# SWAT+ uses the closed-up spelling (`endtype` appears 8 times in
# gwflow_module.f90). Missing one silently swallows every later declaration
# into the still-open construct, so accept both spellings.
END_PROCEDURE_RE = re.compile(r"^\s*end\s*(subroutine|function)\b(?:\s+([a-z_]\w*))?", re.I)
END_MODULE_RE = re.compile(r"^\s*end\s*module\b", re.I)
END_PROGRAM_RE = re.compile(r"^\s*end\s*program\b", re.I)
TYPE_RE = re.compile(r"^\s*type\s*(?:,\s*[^:]+)?::\s*([a-z_]\w*)\b|^\s*type\s+([a-z_]\w*)\b", re.I)
END_TYPE_RE = re.compile(r"^\s*end\s*type\b", re.I)
USE_RE = re.compile(
    r"^\s*use\s*(?:,\s*(intrinsic|non_intrinsic))?\s*(?:::\s*)?([a-z_]\w*)\s*(?:,\s*only\s*:\s*(.*))?$",
    re.I,
)
CALL_RE = re.compile(r"\bcall\s+([a-z_]\w*(?:%[a-z_]\w*)?)\b", re.I)
# Function-style invocation: an identifier immediately followed by "(".  These
# are only candidates — the analyzer keeps an edge only when the name resolves
# to an actually-defined function, which filters out array refs and intrinsics.
FUNCALL_RE = re.compile(r"\b([a-z_]\w*)\s*\(", re.I)
# Statement keywords and control constructs that take a "(" but are not calls.
FORTRAN_CALL_NONCANDIDATES = frozenset(
    {
        "if", "elseif", "else", "do", "while", "where", "forall", "select",
        "case", "selectcase", "return", "stop", "call", "allocate",
        "deallocate", "nullify", "open", "close", "read", "write", "print",
        "rewind", "backspace", "inquire", "format", "data", "common",
        "dimension", "type", "class", "use", "implicit", "function",
        "subroutine", "module", "program", "end", "endif", "enddo", "then",
        "associate", "block",
    }
)
DECL_RE = re.compile(
    r"^\s*(integer|real|double\s+precision|logical|character(?:\s*\([^)]*\))?|type\s*\([^)]+\)|class\s*\([^)]+\))"
    r"(?:\s*\*\s*\d+)?"  # old-style star-kind, e.g. `integer*8`, `character*10`
    r"(?=\s|,|::)(.*)",
    re.I,
)
# The LHS may be a plain scalar, an array element, a %chain, or any mix
# (``cell_name(i)``, ``ob(i)%typ``, ``a%b(j)%c``) -- SWAT+ assigns to
# subscripted targets constantly (1400+ times across the pinned source), and
# missing the subscript meant the whole line failed to match at all.
ASSIGN_RE = re.compile(
    r"^\s*([a-z_]\w*(?:\([^()]*\))?(?:%[a-z_]\w*(?:\([^()]*\))?)*)\s*=\s*(.+)$", re.I
)
STRING_LITERAL_RE = re.compile(r"""["']([^"']+)["']""")
IO_KEYWORD_RE = re.compile(r"^\s*(open|read|write|close|rewind|backspace)\b", re.I)
SELECT_CASE_RE = re.compile(r"^select\s+case\b", re.I)
CASE_DEFAULT_RE = re.compile(r"^case\s+default\b", re.I)
CASE_RE = re.compile(r"^case\b", re.I)
END_SELECT_RE = re.compile(r"^end\s*select\b", re.I)


@dataclass(slots=True)
class LogicalLine:
    text: str
    start: int
    end: int
    raw: str


def split_fortran_comment(line: str) -> tuple[str, str]:
    quote: str | None = None
    idx = 0
    while idx < len(line):
        char = line[idx]
        if quote:
            if char == quote:
                if idx + 1 < len(line) and line[idx + 1] == quote:
                    idx += 2
                    continue
                quote = None
        elif char in {"'", '"'}:
            quote = char
        elif char == "!":
            return line[:idx], line[idx + 1 :]
        idx += 1
    return line, ""


def clean_doc_line(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("!>"):
        return stripped[2:].strip()
    if stripped.startswith("!!"):
        return stripped[2:].strip()
    if stripped.startswith("!"):
        return stripped[1:].strip()
    return stripped


def inline_doc_from_raw(raw: str) -> str:
    comments: list[str] = []
    for physical in raw.splitlines():
        code, comment = split_fortran_comment(physical)
        if not code.strip() or not comment.strip():
            continue
        comments.append(clean_doc_line("!" + comment.strip()))
    return "\n".join(comment for comment in comments if comment).strip()


def combine_docs(*docs: str) -> str:
    return "\n".join(doc.strip() for doc in docs if doc and doc.strip()).strip()


def split_top_level_commas(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    quote: str | None = None
    for char in text:
        if quote:
            buf.append(char)
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            buf.append(char)
            continue
        if char == "(":
            depth += 1
        elif char == ")" and depth > 0:
            depth -= 1
        if char == "," and depth == 0:
            item = "".join(buf).strip()
            if item:
                parts.append(item)
            buf = []
        else:
            buf.append(char)
    item = "".join(buf).strip()
    if item:
        parts.append(item)
    return parts


def parse_args(arg_text: str | None) -> list[str]:
    if not arg_text:
        return []
    return [part.strip() for part in split_top_level_commas(arg_text) if part.strip()]


def logical_lines(lines: list[str]) -> list[LogicalLine]:
    output: list[LogicalLine] = []
    buffer: list[str] = []
    raw_buffer: list[str] = []
    start_line = 1
    continuing = False

    for number, raw in enumerate(lines, start=1):
        code, _comment = split_fortran_comment(raw.rstrip("\n"))
        stripped = code.rstrip()
        if not continuing and not stripped.strip():
            continue

        if not continuing:
            start_line = number
            buffer = []
            raw_buffer = []

        piece = stripped.strip()
        if continuing and piece.startswith("&"):
            piece = piece[1:].lstrip()

        if piece.endswith("&"):
            piece = piece[:-1].rstrip()
            continuing = True
        else:
            continuing = False

        buffer.append(piece)
        raw_buffer.append(raw.rstrip("\n"))

        if not continuing:
            text = " ".join(part for part in buffer if part).strip()
            if text:
                output.append(
                    LogicalLine(
                        text=text,
                        start=start_line,
                        end=number,
                        raw="\n".join(raw_buffer),
                    )
                )

    if continuing and buffer:
        text = " ".join(part for part in buffer if part).strip()
        if text:
            output.append(
                LogicalLine(
                    text=text,
                    start=start_line,
                    end=start_line + len(raw_buffer) - 1,
                    raw="\n".join(raw_buffer),
                )
            )
    return output


def parse_use(line: str, loc: SourceLocation) -> UseRef | None:
    match = USE_RE.match(line)
    if not match:
        return None
    only = parse_args(match.group(3))
    return UseRef(
        module=match.group(2),
        only=only,
        intrinsic=(match.group(1) or "").lower() == "intrinsic",
        location=loc,
    )


def parse_declaration(line: str, loc: SourceLocation, doc: str = "") -> list[VariableRef]:
    match = DECL_RE.match(line)
    if not match:
        return []
    vartype = re.sub(r"\s+", " ", match.group(1).strip().lower())
    rest = match.group(2).strip()
    if "::" in rest:
        attrs, names = rest.split("::", 1)
        declaration_prefix = f"{vartype} {attrs.strip()} ::".strip()
    else:
        names = rest
        declaration_prefix = vartype

    variables: list[VariableRef] = []
    for item in split_top_level_commas(names):
        name_part = item.strip()
        initial = None
        if "=" in name_part:
            name_part, initial = [part.strip() for part in name_part.split("=", 1)]
        name_part = re.sub(r"\(.*\)$", "", name_part).strip()
        name_match = re.match(r"([a-z_]\w*)", name_part, re.I)
        if not name_match:
            continue
        variables.append(
            VariableRef(
                name=name_match.group(1),
                declaration=f"{declaration_prefix} {item}".strip(),
                location=loc,
                vartype=vartype,
                initial=initial,
                doc=doc,
            )
        )
    return variables


def parse_keyword_args(text: str | None) -> dict[str, str]:
    if not text:
        return {}
    values: dict[str, str] = {}
    positional: list[str] = []
    for item in split_top_level_commas(text):
        if "=" in item:
            key, value = item.split("=", 1)
            values[key.strip().lower()] = value.strip()
        else:
            positional.append(item.strip())
    for idx, value in enumerate(positional, start=1):
        values[str(idx)] = value
    return values


def strip_quotes(text: str | None) -> str | None:
    if text is None:
        return None
    stripped = text.strip()
    if len(stripped) >= 2 and stripped[0] in {"'", '"'} and stripped[-1] == stripped[0]:
        return stripped[1:-1]
    return stripped


def extract_balanced_parens(text: str) -> tuple[str, str] | None:
    """Split ``text`` at the close paren matching its leading ``(``.

    ``text`` is left-stripped first; if it doesn't start with ``(`` after
    that, returns ``None``. On success returns ``(inside, remainder)`` where
    ``inside`` excludes the enclosing parens and ``remainder`` is whatever
    follows the matching ``)``. Returns ``None`` if the parens never balance.

    A single regex can't find the true closing paren: a greedy ``.*`` up to
    the *last* ``)`` in the line over-matches whenever the enclosed content
    itself has parens (e.g. an array-subscripted target,
    ``manure_om(it)%name``), and stopping at the *first* ``)`` under-matches
    whenever the content itself opens a paren first (e.g. an internal read's
    unit, ``read(split_fields(1),*) var``). Only walking the text and
    tracking paren depth handles both.
    """
    stripped = text.lstrip()
    if not stripped.startswith("("):
        return None
    depth = 0
    quote: str | None = None
    for i, char in enumerate(stripped):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return stripped[1:i], stripped[i + 1 :]
    return None


def split_io_statement(line: str) -> tuple[str, str, str] | None:
    """Split an I/O statement into ``(kind, control_list, remainder)``.

    ``control_list`` is the parenthesized ``(unit, fmt, iostat=..., ...)``
    right after the keyword (empty if the statement uses the unparenthesized
    ``read 100, x`` form); ``remainder`` is whatever follows it -- the
    read/write field list.
    """
    match = IO_KEYWORD_RE.match(line)
    if not match:
        return None
    kind = match.group(1).lower()
    rest = line[match.end() :]
    stripped = rest.lstrip()
    if not stripped.startswith("("):
        return kind, "", stripped
    balanced = extract_balanced_parens(stripped)
    if balanced is None:
        return kind, stripped[1:], ""
    control_list, remainder = balanced
    return kind, control_list, remainder


def extract_fields_from_io(line: str) -> list[str]:
    split = split_io_statement(line)
    if split is None:
        return []
    kind, _control_list, remainder = split
    if kind not in {"read", "write"}:
        return []
    fields = []
    for field in split_top_level_commas(remainder):
        clean = field.strip()
        if clean:
            fields.append(clean)
    return fields


class FortranScanner:
    def __init__(self, config: BuildConfig):
        self.config = config

    def scan(self) -> ProjectIndex:
        source_root = self.config.source_dir.resolve()
        project = ProjectIndex(
            project_name=self.config.project_name,
            source_root=str(source_root),
        )
        for path in self._iter_source_files(source_root):
            file_doc = self._scan_file(path, source_root, project)
            project.files.append(file_doc)
        project.stats = {
            "files": len(project.files),
            "modules": len(project.modules),
            "programs": len(project.programs),
            "procedures": len(project.procedures),
            "types": len(project.types),
        }
        return project

    def iter_source_files(self) -> list[Path]:
        """The files scan() would parse, without parsing them (for cache keys)."""
        return self._iter_source_files(self.config.source_dir.resolve())

    def _iter_source_files(self, source_root: Path) -> list[Path]:
        suffixes = {f".{ext.lstrip('.')}" for ext in self.config.extensions}
        files: list[Path] = []
        for path in source_root.rglob("*"):
            if not path.is_file() or path.suffix not in suffixes:
                continue
            rel = path.relative_to(source_root).as_posix()
            if any(fnmatch(rel, pattern) or fnmatch(path.as_posix(), pattern) for pattern in self.config.exclude):
                continue
            files.append(path)
        return sorted(files)

    def _scan_file(self, path: Path, source_root: Path, project: ProjectIndex) -> SourceFileDoc:
        rel = path.relative_to(source_root).as_posix()
        physical_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        lines = logical_lines(physical_lines)
        file_doc = SourceFileDoc(path=rel)
        module_stack: list[ModuleDoc] = []
        program_stack: list[ProgramDoc] = []
        proc_stack: list[ProcedureDoc] = []
        type_stack: list[DerivedTypeDoc] = []
        doc_by_line, doc_continuations = self._collect_doc_blocks(physical_lines)
        string_defaults: dict[str, str] = {}
        unit_files: dict[str, str] = {}
        current_conditions: list[str] = []
        select_case_stack: list[SelectCaseDoc] = []

        for logical in lines:
            line = logical.text
            loc = SourceLocation(rel, logical.start, logical.end if logical.end != logical.start else None)
            lowered = line.lower().strip()
            doc = doc_by_line.get(logical.start, "")

            if END_PROCEDURE_RE.match(line):
                if proc_stack:
                    proc_stack[-1].location.end_line = logical.end
                    proc_stack.pop()
                continue
            if END_TYPE_RE.match(line):
                if type_stack:
                    type_stack[-1].location.end_line = logical.end
                    type_stack.pop()
                continue
            if END_MODULE_RE.match(line):
                if module_stack:
                    module_stack[-1].location.end_line = logical.end
                    module_stack.pop()
                continue
            if END_PROGRAM_RE.match(line):
                if program_stack:
                    program_stack[-1].location.end_line = logical.end
                    program_stack.pop()
                continue

            if not proc_stack and not type_stack:
                module_match = MODULE_RE.match(line)
                if module_match:
                    module = ModuleDoc(name=module_match.group(1), location=loc, doc=doc)
                    project.modules.append(module)
                    file_doc.modules.append(module.name)
                    module_stack.append(module)
                    continue

                program_match = PROGRAM_RE.match(line)
                if program_match:
                    program = ProgramDoc(name=program_match.group(1), location=loc, doc=doc)
                    project.programs.append(program)
                    file_doc.programs.append(program.name)
                    program_stack.append(program)
                    continue

            type_match = TYPE_RE.match(line)
            if type_match and not lowered.startswith("type("):
                # Unlike MODULE_RE/PROGRAM_RE above, this is intentionally not
                # gated on `not proc_stack`: Fortran also allows a `type ...
                # end type` declared local to a subroutine/function's own
                # specification part (co2_read.f90's `co2`/`co2_annual`, the
                # only pinned-source example), scoped to that procedure just
                # like its other local variables. Without collecting it here,
                # it never reaches `types_by_name`, so a read into it fails
                # with "unknown derived type" -- and its component lines,
                # never pushed onto `type_stack`, fall through to the
                # variable-declaration branch below and get misattributed as
                # plain procedure-local variables instead of type components.
                type_name = type_match.group(1) or type_match.group(2)
                dtype = DerivedTypeDoc(
                    name=type_name,
                    location=loc,
                    module=module_stack[-1].name if module_stack else None,
                    doc=doc,
                )
                project.types.append(dtype)
                file_doc.types.append(dtype.name)
                if module_stack:
                    module_stack[-1].types.append(dtype.name)
                type_stack.append(dtype)
                continue

            proc_match = SUBROUTINE_RE.match(line)
            kind = "subroutine"
            if not proc_match:
                proc_match = FUNCTION_RE.match(line)
                kind = "function"
            if proc_match and not lowered.startswith("end "):
                proc = ProcedureDoc(
                    name=proc_match.group(1),
                    kind=kind,
                    location=loc,
                    module=module_stack[-1].name if module_stack else None,
                    parent=proc_stack[-1].name if proc_stack else None,
                    args=parse_args(proc_match.group(2)),
                    doc=doc,
                )
                project.procedures.append(proc)
                file_doc.procedures.append(proc.name)
                if module_stack and not proc.parent:
                    module_stack[-1].procedures.append(proc.name)
                proc_stack.append(proc)
                unit_files = {}
                current_conditions = []
                select_case_stack = []
                continue

            use_ref = parse_use(line, loc)
            if use_ref:
                target = proc_stack[-1] if proc_stack else program_stack[-1] if program_stack else module_stack[-1] if module_stack else None
                if target is not None:
                    target.uses.append(use_ref)
                continue

            variables = parse_declaration(
                line,
                loc,
                doc=combine_docs(
                    doc,
                    inline_doc_from_raw(logical.raw),
                    doc_continuations.get(logical.start, ""),
                ),
            )
            if variables:
                for variable in variables:
                    if variable.initial:
                        literal = self._string_literal(variable.initial)
                        if literal:
                            string_defaults[variable.name.lower()] = literal
                    if type_stack:
                        type_stack[-1].components.append(variable)
                    elif proc_stack:
                        proc_stack[-1].variables.append(variable)
                    elif module_stack:
                        module_stack[-1].variables.append(variable)
                continue

            assignment = ASSIGN_RE.match(line)
            if assignment:
                literal = self._string_literal(assignment.group(2))
                if literal:
                    string_defaults[assignment.group(1).lower()] = literal
                if proc_stack:
                    proc_stack[-1].assignments.append(
                        ControlStep("assignment", f"Sets {assignment.group(1)}", line, loc)
                    )

            if proc_stack:
                proc = proc_stack[-1]
                self._update_condition_stack(line, current_conditions)
                self._update_select_cases(line, loc, select_case_stack, proc)
                control = self._control_step(line, loc)
                if control:
                    proc.control_steps.append(control)
                subroutine_names = set()
                for call_match in CALL_RE.finditer(line):
                    proc.calls.append(CallRef(name=call_match.group(1), raw=line, location=loc))
                    subroutine_names.add(call_match.group(1).split("%")[0].lower())
                self._collect_function_calls(line, loc, proc, subroutine_names)
                io_op = self._io_operation(line, loc, string_defaults, unit_files)
                if io_op:
                    proc.io.append(io_op)
                    if current_conditions:
                        io_op.condition = " > ".join(current_conditions)
                continue

            if program_stack:
                program = program_stack[-1]
                control = self._control_step(line, loc)
                if control:
                    program.control_steps.append(control)
                subroutine_names = set()
                for call_match in CALL_RE.finditer(line):
                    program.calls.append(CallRef(name=call_match.group(1), raw=line, location=loc))
                    subroutine_names.add(call_match.group(1).split("%")[0].lower())
                self._collect_function_calls(line, loc, program, subroutine_names)

        return file_doc

    def _collect_function_calls(self, line, loc, holder, subroutine_names) -> None:
        """Record identifier(...) tokens as candidate function-call references.

        These are only candidates: the analyzer keeps an edge solely when the
        name resolves to a defined function, which discards array references and
        intrinsics.  Dedupe per holder so a function called on many lines does
        not flood the call list.
        """
        existing = {c.name.lower() for c in holder.calls}
        for match in FUNCALL_RE.finditer(line):
            name = match.group(1)
            lowered = name.lower()
            if lowered in FORTRAN_CALL_NONCANDIDATES:
                continue
            if lowered in subroutine_names or lowered in existing:
                continue
            existing.add(lowered)
            holder.calls.append(
                CallRef(name=name, raw=line, location=loc, kind="function")
            )

    def _collect_doc_blocks(self, lines: list[str]) -> tuple[dict[int, str], dict[int, str]]:
        """Map line -> preceding comment block, and line -> inline-comment continuation.

        SWAT+ wraps a declaration's inline ``!units |desc`` comment onto following
        gutter lines (``!        |  more desc``). Those belong to the declaration above,
        not the one below, so they are attributed as continuations of the previous code
        line rather than buffered as the next declaration's preceding block.
        """

        docs: dict[int, str] = {}
        continuations: dict[int, str] = {}
        buffer: list[str] = []
        inline_idx: int | None = None
        for idx, raw in enumerate(lines, start=1):
            stripped = raw.strip()
            if stripped.startswith("!") and not stripped.startswith("!$"):
                cleaned = clean_doc_line(stripped)
                if inline_idx is not None and cleaned.startswith("|"):
                    prev = continuations.get(inline_idx, "")
                    continuations[inline_idx] = (prev + "\n" + cleaned).strip() if prev else cleaned
                else:
                    inline_idx = None
                    buffer.append(cleaned)
                continue
            if not stripped:
                buffer = []
                inline_idx = None
                continue
            code, comment = split_fortran_comment(raw)
            if code.strip() and buffer:
                docs[idx] = "\n".join(buffer).strip()
            buffer = []
            inline_idx = idx if (code.strip() and comment.strip()) else None
        return docs, continuations

    def _string_literal(self, text: str) -> str | None:
        match = STRING_LITERAL_RE.search(text)
        if not match:
            return None
        literal = match.group(1)
        return literal if literal.strip() else None

    def _resolve_file_expression(self, expr: str | None, defaults: dict[str, str]) -> str | None:
        if not expr:
            return None
        stripped = strip_quotes(expr)
        if not stripped:
            return None
        if "//" in stripped:
            tail = stripped.rsplit("//", 1)[-1].strip()
            return self._resolve_file_expression(tail, defaults) or stripped
        wrapper = re.match(r"^(?:trim|adjustl)\((.*)\)$", stripped, re.I)
        if wrapper:
            return self._resolve_file_expression(wrapper.group(1), defaults) or stripped
        literal_match = re.fullmatch(r"""["']([^"']+)["']""", stripped)
        if literal_match and literal_match.group(1).strip():
            return literal_match.group(1)
        key = re.sub(r"\s+", "", stripped).lower()
        if key in defaults and defaults[key].strip():
            return defaults[key]
        return stripped

    def _io_operation(
        self,
        line: str,
        loc: SourceLocation,
        defaults: dict[str, str],
        unit_files: dict[str, str],
    ) -> IOOperation | None:
        split = split_io_statement(line)
        if split is None:
            return None
        kind, control_list, _remainder = split
        args = parse_keyword_args(control_list)
        unit = args.get("unit") or args.get("1")
        file_expr = args.get("file")
        file_resolved = self._resolve_file_expression(file_expr, defaults)

        if kind == "open":
            if unit and file_resolved:
                unit_files[unit.lower()] = file_resolved
        elif unit:
            file_resolved = unit_files.get(unit.lower()) or file_resolved

        if not file_resolved and unit:
            file_resolved = f"unit_{unit}"

        return IOOperation(
            kind=kind,
            unit=unit,
            file_expr=file_expr,
            file_resolved=file_resolved,
            raw=line,
            location=loc,
            fields=extract_fields_from_io(line),
        )

    def _control_step(self, line: str, loc: SourceLocation) -> ControlStep | None:
        stripped = line.strip()
        lowered = stripped.lower()
        patterns = [
            ("if", r"^if\s*\("),
            ("else", r"^else\b"),
            ("select", r"^select\s+case\b"),
            ("case", r"^case\b"),
            ("loop", r"^do\b"),
            ("where", r"^where\b"),
            ("allocation", r"^(allocate|deallocate)\s*\("),
            ("io", r"^(open|read|write|close|rewind|backspace)\b"),
            ("call", r"^call\s+"),
            ("return", r"^return\b"),
        ]
        for kind, pattern in patterns:
            if re.match(pattern, lowered):
                return ControlStep(kind=kind, summary=self._summarize_step(stripped), raw=line, location=loc)
        return None

    def _summarize_step(self, line: str) -> str:
        compact = re.sub(r"\s+", " ", line).strip()
        if len(compact) > 120:
            return compact[:117] + "..."
        return compact

    def _update_condition_stack(self, line: str, stack: list[str]) -> None:
        lowered = line.lower().strip()
        if re.match(r"^if\s*\(.*\)\s*then\b", lowered):
            stack.append(line.strip())
        elif re.match(r"^select\s+case\b", lowered):
            stack.append(line.strip())
        elif re.match(r"^do\b", lowered):
            stack.append(line.strip())
        elif re.match(r"^else\s*if\s*\(.*\)\s*then\b", lowered) or re.match(r"^else\b", lowered):
            # Same nesting depth as the `if` this closes a branch of -- append
            # to the top entry rather than push/pop (and rather than replace
            # it, which would lose the original `if (...) then` context in
            # generated docs). Without this, an if-branch read and its
            # else-branch sibling get an identical trail -- the stack only
            # ever recorded the opening `if`, never which arm a later read
            # fell into -- which makes them structurally indistinguishable
            # even though they can be a genuinely different shape (see
            # resolve_tagged_row_block, which depends on telling them apart).
            if stack:
                stack[-1] = f"{stack[-1]} / {line.strip()}"
        elif re.match(r"^case\b", lowered):
            # Same idea as else/elseif -- a read in one case branch and a read
            # in another get an identical trail otherwise, both showing just
            # the opening `select case (...)`. Unlike if/elseif (at most a
            # handful of branches in practice), a select case can have dozens
            # of branches (SWAT+'s COND_VAR dispatch has 55), so this REPLACES
            # any previously-appended case branch rather than accumulating
            # one -- each read's trail ends in the `select case (...)` text
            # plus only its OWN case line, never every case label scanned so
            # far.
            if stack:
                base = re.split(r"\s/\scase\b", stack[-1], maxsplit=1, flags=re.I)[0]
                stack[-1] = f"{base} / {line.strip()}"
        elif re.match(r"^end\s*(if|select|do)\b", lowered):
            if stack:
                stack.pop()

    def _update_select_cases(
        self,
        line: str,
        loc: SourceLocation,
        stack: list[SelectCaseDoc],
        proc: ProcedureDoc,
    ) -> None:
        """Track ``select case`` blocks and capture their string-literal labels.

        Independent of ``_update_condition_stack`` -- that stack only holds
        raw strings for building a human-readable condition trail. This one
        preserves the select's subject expression and every literal a
        ``case (...)`` branch dispatches on, which is the closed vocabulary a
        decision-table reader or a hand-parsed dispatcher recognizes. Nested
        selects (e.g. a ``select case`` on ``...%option`` inside one branch of
        an outer ``select case`` on ``...%typ``) are handled via the stack:
        each closed block emits its own ``SelectCaseDoc``.
        """
        stripped = line.strip()
        lowered = stripped.lower()
        if SELECT_CASE_RE.match(lowered):
            after_keyword = stripped[stripped.lower().index("case") + len("case") :]
            balanced = extract_balanced_parens(after_keyword)
            subject = balanced[0].strip() if balanced else ""
            stack.append(SelectCaseDoc(subject=subject, cases=[], location=loc))
            return
        if stack and CASE_RE.match(lowered) and not CASE_DEFAULT_RE.match(lowered):
            after = stripped[len("case") :].lstrip()
            balanced = extract_balanced_parens(after) if after.startswith("(") else None
            if balanced:
                stack[-1].cases.extend(STRING_LITERAL_RE.findall(balanced[0]))
            return
        if stack and END_SELECT_RE.match(lowered):
            proc.select_cases.append(stack.pop())
