"""Phase 3: structural facts read off the fparser2 AST.

The rich scanner decides what owns a statement by matching regexes in source
order and pushing stacks. That works, but it infers structure the compiler
already knows, and every unusual spelling is a new pattern to teach it. This
module inverts the split the Phase 4 pipeline calls for:

* **fparser2 supplies the structure.** Which scope a declaration belongs to,
  where a scope ends, whether a name is a function or a type -- all of it comes
  from the parse tree, not from a regex over a line.
* **The Phase 2 source layer supplies the bytes.** Every consumer-visible
  string (``declaration``, ``raw``, doc comments) is taken from the physical
  source through :mod:`.source_text`, never from ``str(node)``. fparser2
  normalises case and spacing when it prints a node -- ``real :: mv = 1.``
  comes back as ``REAL :: mv = 1.`` -- and the schema resolver matches on those
  bytes, so printing the node would silently rewrite the contract Phase 2 froze.

This covers all seven Phase 3 categories: files, modules, programs, procedures
and derived types; arguments, locals, module variables and type components;
``use`` statements with their ``only`` lists; assignments and their component
paths; loops, conditionals, select blocks and nesting; calls and
function-reference candidates; and I/O statements with their source fields.

The executable pass (categories 4-7) runs over the file's statements in source
order, because the scanner's I/O file resolution is order-sensitive: a string
default picked up from a declaration or an earlier assignment is what a later
``open`` resolves its filename against. A statement is any node fparser2 gives
its own source item, which is exactly one node per statement -- including each
half of ``case ('ncell'); read(code_val,*) ncell`` -- so the AST and the Phase 2
source layer enumerate the same statements in the same order and can be zipped.

Facts that cannot be placed carry a :class:`ReviewFlag` rather than being
dropped, which is what the Phase 3 exit gate means by "no AST fact has a
missing location unless it carries a diagnostic explaining why".
"""

from __future__ import annotations

import re
from pathlib import Path

from fparser.common.readfortran import FortranStringReader
from fparser.common.sourceinfo import FortranFormat
from fparser.two import Fortran2003 as f03
from fparser.two.parser import ParserFactory
from fparser.two.utils import FortranSyntaxError, walk

from .schema_config import BuildConfig
from .unit_binding import resolve_project_unit_files
from .schema_fortran import (
    CASE_DEFAULT_RE,
    FORTRAN_CALL_NONCANDIDATES,
    FUNCALL_RE,
    STRING_LITERAL_RE,
    collect_doc_blocks,
    combine_docs,
    extract_balanced_parens,
    extract_fields_from_io,
    parse_declaration,
    parse_keyword_args,
    parse_use,
    populate_io_summaries,
    string_literal,
    resolve_file_expression,
    resolve_project_file_expressions,
    split_io_statement,
    summarize_step,
)
from .schema_model import (
    AssignmentDoc,
    CallRef,
    ControlStep,
    DerivedTypeDoc,
    IOOperation,
    ModuleDoc,
    ProcedureDoc,
    ProgramDoc,
    ProjectIndex,
    ReviewFlag,
    SelectCaseDoc,
    SourceFileDoc,
    SourceLocation,
    VariableRef,
    record_identity,
    record_scope,
)
from .source_files import source_files
from .source_text import (
    LogicalLine,
    fixed_form_logical_lines,
    inline_doc_from_raw,
    logical_lines,
    normalize_nonstandard_signs,
    split_assignment,
    split_statement_label,
)


AST_PARSER_VERSION = "fparser-ast-v1"

# The scopes that own facts. `Derived_Type_Def` is one of them: a component
# declaration belongs to its type, not to the module or procedure the type sits
# in, and the AST is what tells the two apart without the scanner's
# `type_stack`.
_SCOPE_CLASSES = (
    f03.Module,
    f03.Main_Program,
    f03.Subroutine_Subprogram,
    f03.Function_Subprogram,
    f03.Derived_Type_Def,
)

# An interface body describes a procedure defined elsewhere. Its dummy-argument
# declarations are part of that description, not variables of the enclosing
# module, so ownership stops here instead of walking on to the module. fparser2
# represents these bodies as `Subroutine_Body`/`Function_Body`, which are not
# subprograms, so without this boundary they would resolve to the module.
_BOUNDARY_CLASSES = (f03.Interface_Block,)

# Scope kinds, matched with `isinstance` for the same reason as `_STEP_KINDS`.
_SCOPE_KINDS: tuple[tuple[type, str], ...] = (
    (f03.Module, "module"),
    (f03.Main_Program, "program"),
    (f03.Subroutine_Subprogram, "subroutine"),
    (f03.Function_Subprogram, "function"),
    (f03.Derived_Type_Def, "type"),
)


def _scope_kind(node) -> str | None:
    for cls, kind in _SCOPE_KINDS:
        if isinstance(node, cls):
            return kind
    return None

# --------------------------------------------------------------------------
# Statement classification (Phase 3 categories 4-7)
#
# These tables say in node classes what the scanner says in regexes. Both
# readings have to agree byte for byte, so each entry below is paired with the
# pattern it replaces in `schema_fortran`.
# --------------------------------------------------------------------------

# `ControlStep.kind`, in the order `FortranScanner._control_step` tests its
# patterns. `If_Stmt` is the one-line `if (c) stmt` form: the scanner classifies
# it "if" because `^if\s*\(` is tested before `^call`, so an action statement
# riding on an `if` is outlined as the `if`, and the AST agrees by construction.
#
# Matched with `isinstance`, never `type(node) is ...`: fparser2 builds some
# node classes dynamically, so `Open_Stmt` instances are subclasses that carry
# the same `__name__` as `f03.Open_Stmt` without being that class. An identity
# or dict-by-type lookup silently misses exactly those.
_STEP_KINDS: tuple[tuple[tuple[type, ...], str], ...] = (
    ((f03.If_Then_Stmt, f03.If_Stmt), "if"),
    ((f03.Else_If_Stmt, f03.Else_Stmt), "else"),
    ((f03.Select_Case_Stmt,), "select"),
    ((f03.Case_Stmt,), "case"),
    ((f03.Nonlabel_Do_Stmt, f03.Label_Do_Stmt), "loop"),
    ((f03.Where_Stmt, f03.Where_Construct_Stmt), "where"),
    ((f03.Allocate_Stmt, f03.Deallocate_Stmt), "allocation"),
    (
        (
            f03.Open_Stmt,
            f03.Read_Stmt,
            f03.Write_Stmt,
            f03.Close_Stmt,
            f03.Rewind_Stmt,
            f03.Backspace_Stmt,
        ),
        "io",
    ),
    ((f03.Call_Stmt,), "call"),
    ((f03.Return_Stmt,), "return"),
)

# `Elsewhere_Stmt` and `End_Where_Stmt` are deliberately absent: the scanner's
# `^else(?:\s*if)?\b` does not match `elsewhere` (no word boundary after
# `else`), and nothing matches `end where`, so neither is outlined.

# The three constructs `BLOCK_OPEN_RE` recognises. A one-line `if (c) stmt`
# opens nothing, which is why `If_Stmt` is not here while `If_Then_Stmt` is.
_BLOCK_OPENERS = (
    f03.If_Then_Stmt,
    f03.Select_Case_Stmt,
    f03.Nonlabel_Do_Stmt,
    f03.Label_Do_Stmt,
)
_BLOCK_CLOSERS = (f03.End_If_Stmt, f03.End_Select_Stmt, f03.End_Do_Stmt)
# Arms belong to a construct without nesting inside it.
_BLOCK_BRANCHES = (f03.Else_If_Stmt, f03.Else_Stmt, f03.Case_Stmt)

# Statements that push, amend or pop the human-readable condition trail carried
# onto an `IOOperation.condition`.
_CONDITION_PUSH = (
    f03.If_Then_Stmt,
    f03.Select_Case_Stmt,
    f03.Nonlabel_Do_Stmt,
    f03.Label_Do_Stmt,
)
_CONDITION_AMEND = (f03.Else_If_Stmt, f03.Else_Stmt)
_CONDITION_POP = _BLOCK_CLOSERS

_IO_CLASSES = (
    f03.Open_Stmt,
    f03.Read_Stmt,
    f03.Write_Stmt,
    f03.Close_Stmt,
    f03.Rewind_Stmt,
    f03.Backspace_Stmt,
)
_ASSIGNMENT_CLASSES = (f03.Assignment_Stmt, f03.Pointer_Assignment_Stmt)

# Statements the scanner consumes and `continue`s on before reaching its
# executable block, so they contribute no control step, call or I/O record. A
# scope's own `end` is here; `end if`, `end do` and `end select` are not, because
# the block tracker needs them.
_NON_EXECUTABLE_CLASSES = (
    f03.Program_Stmt,
    f03.End_Program_Stmt,
    f03.Module_Stmt,
    f03.End_Module_Stmt,
    f03.Subroutine_Stmt,
    f03.End_Subroutine_Stmt,
    f03.Function_Stmt,
    f03.End_Function_Stmt,
    f03.Derived_Type_Stmt,
    f03.End_Type_Stmt,
    f03.Use_Stmt,
)
_DECLARATION_CLASSES = (f03.Type_Declaration_Stmt, f03.Data_Component_Def_Stmt)

_FIXED_FORM_SUFFIXES = frozenset({".f", ".for", ".ftn", ".f77"})

_PARSER = None


def _parser():
    global _PARSER
    if _PARSER is None:
        _PARSER = ParserFactory().create(std="f2008")
    return _PARSER


# --------------------------------------------------------------------------
# AST navigation
# --------------------------------------------------------------------------


def _item_span(node) -> tuple[int, int] | None:
    item = getattr(node, "item", None)
    span = getattr(item, "span", None)
    if not span:
        return None
    return int(span[0]), int(span[1])


def _stmt_line(node) -> int | None:
    """The first physical line of the statement *node* belongs to."""

    cur = node
    while cur is not None:
        span = _item_span(cur)
        if span:
            return span[0]
        cur = getattr(cur, "parent", None)
    return None


def _scope_span(node) -> tuple[int, int] | None:
    """The physical extent of a scope, opening statement through `end`.

    The opening and closing statements carry the outer bounds directly. A scope
    whose own statements lost their spans still gets a best-effort extent from
    its descendants, so a partially located scope is still placeable.
    """

    opening = _item_span(node.children[0]) if node.children else None
    closing = _item_span(node.children[-1]) if node.children else None
    if opening and closing:
        return opening[0], closing[1]

    first = last = None
    for descendant in walk(node):
        span = _item_span(descendant)
        if not span:
            continue
        first = span[0] if first is None else min(first, span[0])
        last = span[1] if last is None else max(last, span[1])
    if first is None:
        return None
    if opening:
        first = opening[0]
    if closing:
        last = closing[1]
    return first, last


def _owning_scope(node):
    """The nearest enclosing scope, or None if an interface body intervenes."""

    cur = getattr(node, "parent", None)
    while cur is not None:
        if isinstance(cur, _BOUNDARY_CLASSES):
            return None
        if isinstance(cur, _SCOPE_CLASSES):
            return cur
        cur = getattr(cur, "parent", None)
    return None


def _scope_name(node) -> str | None:
    """The declared name of a scope, read structurally.

    Deliberately not ``walk(stmt, Name)[0]``: for ``type(box) function make(x)``
    the first ``Name`` in the statement is ``box``, the function's *result type*,
    and the walk-based reading names the procedure after its type. fparser2 puts
    the declared name in a fixed child position, so read that instead.
    """

    stmt = node.children[0] if node.children else None
    if stmt is None:
        return None

    if isinstance(node, f03.Derived_Type_Def):
        names = walk(stmt, f03.Type_Name) or walk(stmt, f03.Name)
        return str(names[0]) if names else None

    if isinstance(stmt, (f03.Function_Stmt, f03.Subroutine_Stmt)):
        # (Prefix, Name, Dummy_Arg_List, Suffix)
        name = stmt.children[1]
        return str(name) if name is not None else None

    names = walk(stmt, f03.Name)
    return str(names[0]) if names else None


def _dummy_args(node) -> list[str]:
    stmt = node.children[0] if node.children else None
    if not isinstance(stmt, (f03.Function_Stmt, f03.Subroutine_Stmt)):
        return []
    arg_list = stmt.children[2]
    if arg_list is None:
        return []
    return [str(name) for name in walk(arg_list, f03.Name)]


# --------------------------------------------------------------------------
# Builder
# --------------------------------------------------------------------------


class AstIndexBuilder:
    """Build a :class:`ProjectIndex` whose structure comes from the AST."""

    def __init__(self, config: BuildConfig):
        self.config = config

    def build(self) -> ProjectIndex:
        source_root = self.config.source_dir.resolve()
        project = ProjectIndex(
            project_name=self.config.project_name,
            source_root=str(source_root),
        )
        for path in self._iter_source_files(source_root):
            rel = path.relative_to(source_root).as_posix()
            text = path.read_text(encoding="utf-8", errors="replace")
            file_doc = SourceFileDoc(path=rel)
            try:
                self._build_file(project, file_doc, rel, text)
            except (FortranSyntaxError, Exception) as exc:  # noqa: BLE001
                # A file fparser2 rejects yields no AST facts at all. Record why
                # and keep the file in the inventory; Phase 5 owns the fallback
                # that fills it back in.
                project.review_flags.append(
                    ReviewFlag(
                        code="ast_parse_failed",
                        severity="error",
                        message=f"{type(exc).__name__}: {exc}",
                        location=SourceLocation(rel, 1),
                        target=rel,
                    )
                )
            project.files.append(file_doc)

        # Cross-file filename resolution needs the completed index: a filename
        # default declared on a derived-type component in one file is what an
        # `open (107, file=in_aqu%aqu)` in another resolves against. Phase 4
        # extends this; Phase 3 keeps the reading the scanner already performs.
        resolve_project_file_expressions(project)
        # A unit is bound to a filename by an `open`, and for output that `open`
        # is routinely in a different file from the writes that use it. Binding
        # across files needs the completed index for the same reason filename
        # expressions do, and must run before the operations are grouped by
        # filename below.
        self.unit_binding = resolve_project_unit_files(project)
        # Aggregate the resolved operations into per-file and output-family
        # records, the same way the scanner closes out a scan.
        populate_io_summaries(project)

        project.stats = {
            "files": len(project.files),
            "modules": len(project.modules),
            "programs": len(project.programs),
            "procedures": len(project.procedures),
            "types": len(project.types),
            "io_files": len(project.io_files),
            "output_families": len(project.output_families),
        }
        project.metadata["ast_parser_version"] = AST_PARSER_VERSION
        return project

    def _iter_source_files(self, source_root: Path) -> list[Path]:
        from fnmatch import fnmatch

        suffixes = {f".{ext.lstrip('.').lower()}" for ext in self.config.extensions}
        files: list[Path] = []
        for path in source_files(source_root, suffixes):
            rel = path.relative_to(source_root).as_posix()
            if any(
                fnmatch(rel, pattern) or fnmatch(path.as_posix(), pattern)
                for pattern in self.config.exclude
            ):
                continue
            files.append(path)
        return files

    # -- per file ---------------------------------------------------------

    def _build_file(
        self, project: ProjectIndex, file_doc: SourceFileDoc, rel: str, text: str
    ) -> None:
        physical = text.splitlines()

        # fparser2 rejects a file outright over `a*-1`, which gfortran accepts.
        # Parenthesising the signed operand is a change of spelling, not of
        # meaning, so it is applied to the parser's input only: `physical` stays
        # the unchanged source and remains the sole origin of every raw string,
        # span and hash below. Line count is preserved, so spans still line up.
        parsed_lines, normalized = normalize_nonstandard_signs(physical)
        if normalized:
            project.review_flags.append(
                ReviewFlag(
                    code="ast_input_normalized",
                    severity="info",
                    message=(
                        "signed operand parenthesised for parsing on line(s) "
                        + ", ".join(str(line) for line in normalized)
                    ),
                    location=SourceLocation(rel, normalized[0]),
                    target=rel,
                )
            )
        # `ignore_comments=True` keeps comments out of the tree; they come back
        # from the source layer below, which is the only thing that reads them.
        reader = FortranStringReader("\n".join(parsed_lines), ignore_comments=True)
        # File extensions are authoritative here. Content sniffing can misread
        # free-form source whose first statement happens to start in column 6,
        # while forcing free form loses the fixed-form extensions BuildConfig
        # supports by default.
        fixed_form = Path(rel).suffix.lower() in _FIXED_FORM_SUFFIXES
        reader.set_format(FortranFormat(not fixed_form, False))
        tree = _parser()(reader)

        statements = (
            fixed_form_logical_lines(physical)
            if fixed_form
            else logical_lines(physical)
        )
        grouped: dict[int, list[LogicalLine]] = {}
        for statement in statements:
            grouped.setdefault(statement.start, []).append(statement)
        docs, doc_continuations = collect_doc_blocks(physical)
        ctx = _FileContext(
            rel=rel,
            docs=docs,
            doc_continuations=doc_continuations,
            project=project,
            grouped=grouped,
        )
        ctx.bind(tree)

        # Scopes first, so every later fact has a record to attach to.
        records: dict[int, object] = {}
        for node in walk(tree, _SCOPE_CLASSES):
            if _owning_scope_is_interface(node):
                continue
            record = self._emit_scope(ctx, file_doc, node)
            if record is not None:
                records[id(node)] = record

        self._attach_uses(ctx, tree, records)
        self._attach_declarations(ctx, tree, records)
        self._attach_executable_facts(ctx, tree, records)

    def _emit_scope(self, ctx: "_FileContext", file_doc: SourceFileDoc, node):
        name = _scope_name(node)
        kind = _scope_kind(node)
        span = _scope_span(node)
        if name is None:
            ctx.project.review_flags.append(
                ReviewFlag(
                    code="ast_unnamed_scope",
                    severity="warning",
                    message=f"{kind} has no readable name in the AST",
                    location=SourceLocation(ctx.rel, span[0] if span else 1),
                )
            )
            return None
        if span is None:
            # Every scope in a parsed file has statements with spans; a scope
            # without one cannot be linked, hashed, or rendered, so say so
            # rather than inventing line 1.
            ctx.project.review_flags.append(
                ReviewFlag(
                    code="ast_missing_location",
                    severity="error",
                    message=f"{kind} {name} carries no source span",
                    location=None,
                    target=name,
                )
            )
            return None

        start, end = span
        location = SourceLocation(ctx.rel, start, end if end != start else None)
        doc = ctx.docs.get(start, "")
        owner = _owning_scope(node)
        module = _enclosing_of(owner, f03.Module)
        parent_proc = _enclosing_procedure(node)

        if isinstance(node, f03.Module):
            record = ModuleDoc(name=name, location=location, doc=doc)
            record.identity = record_identity("module", name, ctx.rel)
            ctx.project.modules.append(record)
            file_doc.modules.append(name)
            return record

        if isinstance(node, f03.Main_Program):
            record = ProgramDoc(name=name, location=location, doc=doc)
            record.identity = record_identity("program", name, ctx.rel)
            ctx.project.programs.append(record)
            file_doc.programs.append(name)
            return record

        if isinstance(node, f03.Derived_Type_Def):
            record = DerivedTypeDoc(
                name=name,
                location=location,
                module=module,
                parent=parent_proc,
                doc=doc,
            )
            record.identity = record_identity(
                "type", name, ctx.rel, record_scope(module, parent_proc)
            )
            ctx.project.types.append(record)
            file_doc.types.append(name)
            if module:
                owner_module = ctx.module_named(module)
                if owner_module is not None:
                    owner_module.types.append(name)
            return record

        record = ProcedureDoc(
            name=name,
            kind=kind,
            location=location,
            module=module,
            parent=parent_proc,
            args=_dummy_args(node),
            doc=doc,
        )
        record.identity = record_identity(
            kind, name, ctx.rel, record_scope(module, parent_proc)
        )
        ctx.project.procedures.append(record)
        file_doc.procedures.append(name)
        if module and not parent_proc:
            owner_module = ctx.module_named(module)
            if owner_module is not None:
                owner_module.procedures.append(name)
        return record

    # -- facts within scopes ---------------------------------------------

    def _attach_uses(self, ctx: "_FileContext", tree, records: dict[int, object]) -> None:
        for stmt in walk(tree, f03.Use_Stmt):
            holder = self._holder_for(ctx, stmt, records, "use statement")
            if holder is None or not hasattr(holder, "uses"):
                continue
            logical = ctx.logical_for(stmt)
            if logical is None:
                continue
            location = SourceLocation(
                ctx.rel,
                logical.start,
                logical.end if logical.end != logical.start else None,
            )
            use_ref = parse_use(logical.text, location)
            if use_ref is None:
                # The AST says this is a `use`; the shared source layer could
                # not read one from the same bytes. That disagreement is a fact
                # about the parsers, not something to swallow.
                ctx.project.review_flags.append(
                    ReviewFlag(
                        code="ast_use_unreadable",
                        severity="warning",
                        message=f"use statement not parsed from source: {logical.text}",
                        location=location,
                    )
                )
                continue
            holder.uses.append(use_ref)

    def _attach_declarations(
        self, ctx: "_FileContext", tree, records: dict[int, object]
    ) -> None:
        # A type's components and a scope's variables are different node classes
        # in the AST, which is precisely the distinction the scanner had to
        # rebuild with a `type_stack`.
        decl_classes = (
            f03.Type_Declaration_Stmt,
            f03.Data_Component_Def_Stmt,
        )
        for stmt in walk(tree, decl_classes):
            holder = self._holder_for(ctx, stmt, records, "declaration")
            if holder is None:
                continue
            logical = ctx.logical_for(stmt)
            if logical is None:
                continue
            location = SourceLocation(
                ctx.rel,
                logical.start,
                logical.end if logical.end != logical.start else None,
            )
            doc = combine_docs(
                ctx.docs.get(logical.start, ""),
                inline_doc_from_raw(logical.raw),
                ctx.doc_continuations.get(logical.start, ""),
            )
            variables = parse_declaration(logical.text, location, doc=doc)
            if not variables:
                ctx.project.review_flags.append(
                    ReviewFlag(
                        code="ast_declaration_unreadable",
                        severity="warning",
                        message=(
                            "declaration not parsed from source: " f"{logical.text}"
                        ),
                        location=location,
                    )
                )
                continue
            self._place_variables(holder, variables)

    # -- categories 4-7: the executable pass -------------------------------

    def _attach_executable_facts(
        self, ctx: "_FileContext", tree, records: dict[int, object]
    ) -> None:
        """Walk the file's statements in source order, filling executable facts.

        Source order matters, and not only for tidiness: ``string_defaults``
        carries string literals forward from declarations and earlier
        assignments, and is what a later ``open (107, file=in_sim)`` resolves
        its filename against. Processing scopes independently would resolve
        against a different set of defaults than the scanner saw.
        """

        # File-scoped, exactly as the scanner scopes it: a filename default
        # declared on a module component is visible to every procedure below.
        string_defaults: dict[str, str] = {}
        # Per-scope state, created on first entry. The scanner keeps one set of
        # these and resets it whenever it opens a procedure, so a contained
        # procedure leaves its host without a block tracker; keeping one set per
        # scope is what lets a host resume its own numbering afterwards.
        scope_state: dict[int, _ScopeState] = {}

        for node in _statements_in_order(tree):
            scope = _owning_scope(node)
            if scope is None:
                continue
            holder = records.get(id(scope))
            logical = ctx.logical_for(node)
            if logical is None:
                continue

            # A declaration's string default feeds filename resolution even in
            # scopes that hold no executable facts of their own.
            if isinstance(node, _DECLARATION_CLASSES):
                _record_declaration_defaults(logical.text, string_defaults)
                continue
            if isinstance(node, _NON_EXECUTABLE_CLASSES):
                continue

            if not isinstance(holder, (ProcedureDoc, ProgramDoc)):
                continue

            state = scope_state.get(id(scope))
            if state is None:
                state = scope_state[id(scope)] = _ScopeState()

            location = SourceLocation(
                ctx.rel,
                logical.start,
                logical.end if logical.end != logical.start else None,
            )
            self._handle_statement(
                ctx, node, logical, location, holder, state, string_defaults
            )

        for state in scope_state.values():
            state.close(ctx)

    def _handle_statement(
        self,
        ctx: "_FileContext",
        node,
        logical: LogicalLine,
        location: SourceLocation,
        holder,
        state: "_ScopeState",
        string_defaults: dict[str, str],
    ) -> None:
        text = logical.text

        # Category 4: assignments. Only a procedure collects them, matching the
        # scanner; a program's assignments are not part of its record.
        if isinstance(node, _ASSIGNMENT_CLASSES) and isinstance(holder, ProcedureDoc):
            self._emit_assignment(ctx, text, location, holder, string_defaults)
        elif isinstance(node, _ASSIGNMENT_CLASSES):
            _record_assignment_default(text, string_defaults)

        # Category 5: the block tree and select-case vocabularies.
        state.update_select_cases(node, text, location, holder)
        step = _control_step(node, text, location)
        state.track_block(node, step, logical.end)
        if step is not None:
            holder.control_steps.append(step)
        state.update_conditions(node, text)

        # Category 6: calls, then the function-reference candidates left over.
        subroutine_names = self._emit_calls(node, text, location, holder)
        self._emit_function_candidates(text, location, holder, subroutine_names)

        # Category 7: I/O statements and their source fields.
        if isinstance(node, _IO_CLASSES):
            operation = self._emit_io(
                text, location, holder, state, string_defaults
            )
            if operation is not None and state.conditions:
                operation.condition = " > ".join(state.conditions)

        # A labelled DO's terminal statement is part of the loop body, so close
        # it only after the terminal statement has inherited the loop's nesting
        # and condition trail.
        state.close_label_do(node, logical.end)

    def _emit_assignment(
        self,
        ctx: "_FileContext",
        text: str,
        location: SourceLocation,
        holder: ProcedureDoc,
        string_defaults: dict[str, str],
    ) -> None:
        _label, body = split_statement_label(text)
        split = split_assignment(body)
        if split is None:
            # The AST says this is an assignment and the bytes hold no top-level
            # `=`. That disagreement is a fact about the two readings, not
            # something to swallow.
            ctx.project.review_flags.append(
                ReviewFlag(
                    code="ast_assignment_unreadable",
                    severity="warning",
                    message=f"assignment not parsed from source: {text}",
                    location=location,
                )
            )
            return
        target, operator, expression = split
        _record_assignment_default(text, string_defaults)
        pointer = operator == "=>"
        holder.assignments.append(
            AssignmentDoc(
                "pointer_association" if pointer else "assignment",
                f"{'Associates' if pointer else 'Sets'} {target}",
                text,
                location,
                target=target,
                target_root=_target_root(target),
                expression=expression,
            )
        )

    @staticmethod
    def _emit_calls(node, text: str, location: SourceLocation, holder) -> set[str]:
        """Record every explicit `call` in this statement, and name its targets.

        The calls are taken from `Call_Stmt` nodes rather than from a `call`
        pattern over the text, which is what keeps a `call` inside a character
        literal -- `write (*,*) 'call setup first'` -- from becoming a call
        observation. Scanning the statement's own subtree also catches the call
        riding on a one-line `if (n > 0) call helper(x)`, whose `Call_Stmt`
        carries no source item of its own.
        """

        names: set[str] = set()
        for call in walk(node, f03.Call_Stmt):
            designator = call.children[0]
            name = str(designator)
            holder.calls.append(CallRef(name=name, raw=text, location=location))
            names.add(name.split("%")[0].lower())
        return names

    @staticmethod
    def _emit_function_candidates(
        text: str, location: SourceLocation, holder, subroutine_names: set[str]
    ) -> None:
        """Record `identifier(...)` tokens as candidate function references.

        Deliberately still a text pattern. Without semantic analysis fparser2
        parses `a(i)` and `f(i)` into the same `Part_Ref`, so the AST cannot
        separate an array element from a function call either. Plan decision 7
        settles what to do about that: these stay observations until semantic
        resolution proves which are functions, and none may be discarded in the
        meantime because their locations are evidence.
        """

        for match in FUNCALL_RE.finditer(text):
            name = match.group(1)
            lowered = name.lower()
            if lowered in FORTRAN_CALL_NONCANDIDATES or lowered in subroutine_names:
                continue
            holder.calls.append(
                CallRef(name=name, raw=text, location=location, kind="function")
            )

    @staticmethod
    def _emit_io(
        text: str,
        location: SourceLocation,
        holder,
        state: "_ScopeState",
        string_defaults: dict[str, str],
    ) -> IOOperation | None:
        # The label is peeled off for parsing only: `raw` below keeps the
        # statement exactly as written, label included.
        _label, body = split_statement_label(text)
        split = split_io_statement(body)
        if split is None:
            return None
        kind, control_list, _remainder = split
        args = parse_keyword_args(control_list)
        unit = args.get("unit") or args.get("1")
        file_expr = args.get("file")
        file_resolved = resolve_file_expression(file_expr, string_defaults)

        if kind == "open":
            if unit and file_resolved:
                state.unit_files[unit.lower()] = file_resolved
        elif unit:
            file_resolved = state.unit_files.get(unit.lower()) or file_resolved
        if not file_resolved and unit:
            file_resolved = f"unit_{unit}"

        operation = IOOperation(
            kind=kind,
            unit=unit,
            file_expr=file_expr,
            file_resolved=file_resolved,
            raw=text,
            location=location,
            fields=extract_fields_from_io(body),
        )
        holder.io.append(operation)
        return operation

    @staticmethod
    def _place_variables(holder, variables: list[VariableRef]) -> None:
        if isinstance(holder, DerivedTypeDoc):
            holder.components.extend(variables)
        elif isinstance(holder, ProcedureDoc):
            holder.variables.extend(variables)
        elif isinstance(holder, ModuleDoc):
            holder.variables.extend(variables)

    def _holder_for(
        self, ctx: "_FileContext", stmt, records: dict[int, object], what: str
    ):
        scope = _owning_scope(stmt)
        if scope is None:
            # Either an interface body (deliberately unowned) or a construct
            # fparser2 placed outside every scope we model.
            return None
        holder = records.get(id(scope))
        if holder is None:
            line = _stmt_line(stmt)
            ctx.project.review_flags.append(
                ReviewFlag(
                    code="ast_unplaced_fact",
                    severity="warning",
                    message=f"{what} has no owning record in the AST",
                    location=SourceLocation(ctx.rel, line) if line else None,
                )
            )
        return holder


class _FileContext:
    """Everything the per-file pass needs, gathered once."""

    __slots__ = (
        "rel",
        "grouped",
        "logical_by_node",
        "docs",
        "doc_continuations",
        "project",
    )

    def __init__(
        self,
        rel: str,
        docs: dict[int, str],
        doc_continuations: dict[int, str],
        project: ProjectIndex,
        grouped: dict[int, list[LogicalLine]],
    ) -> None:
        self.rel = rel
        self.grouped = grouped
        self.logical_by_node: dict[int, LogicalLine] = {}
        self.docs = docs
        self.doc_continuations = doc_continuations
        self.project = project

    def bind(self, tree) -> None:
        """Pair every located AST statement with its source-layer statement.

        The pairing happens once for the whole file. Reusing this map in every
        fact pass keeps declarations and USE statements after a semicolon from
        repeatedly binding to the first statement on their physical line.
        """

        pending = {line: list(items) for line, items in self.grouped.items()}
        for node in _statements_in_order(tree):
            line = _stmt_line(node)
            queue = pending.get(line) if line is not None else None
            if queue:
                self.logical_by_node[id(node)] = queue.pop(0)
                continue
            self.project.review_flags.append(
                ReviewFlag(
                    code="ast_source_unmapped",
                    severity="warning",
                    message="AST statement has no matching source-layer statement",
                    location=SourceLocation(self.rel, line) if line else None,
                )
            )

    def logical_for(self, stmt) -> LogicalLine | None:
        return self.logical_by_node.get(id(stmt))

    def module_named(self, name: str) -> ModuleDoc | None:
        for module in reversed(self.project.modules):
            if module.name.lower() == name.lower() and module.location.path == self.rel:
                return module
        return None


class _ScopeState:
    """Per-procedure state the executable pass carries in source order.

    The scanner keeps one set of these and clears it on every procedure it
    opens. Keeping one set per scope means a host procedure resumes its own
    block numbering and condition trail after a contained procedure ends,
    instead of continuing with the contained procedure's cleared state.
    """

    __slots__ = ("open_blocks", "next_id", "conditions", "select_stack", "unit_files")

    def __init__(self) -> None:
        self.open_blocks: list[ControlStep] = []
        self.next_id = 0
        self.conditions: list[str] = []
        self.select_stack: list[SelectCaseDoc] = []
        self.unit_files: dict[str, str] = {}

    # -- the block tree ---------------------------------------------------

    def track_block(self, node, step: ControlStep | None, end_line: int) -> None:
        if isinstance(node, _BLOCK_CLOSERS):
            if self.open_blocks:
                self.open_blocks.pop().end_line = end_line
            self._place(step)
            return
        if isinstance(node, _BLOCK_BRANCHES):
            # An arm belongs to its construct without sitting inside it, so it
            # takes the construct's own depth and parent, not the body's.
            owner = self.open_blocks[-1] if self.open_blocks else None
            if step is not None:
                step.depth = max(len(self.open_blocks) - 1, 0)
                step.branch_of = owner.block_id if owner is not None else None
                step.parent_id = (
                    self.open_blocks[-2].block_id if len(self.open_blocks) > 1 else None
                )
            return
        self._place(step)
        if step is not None and isinstance(node, _BLOCK_OPENERS):
            step.block_id = self.next_id
            self.next_id += 1
            self.open_blocks.append(step)

    def _place(self, step: ControlStep | None) -> None:
        if step is None:
            return
        step.depth = len(self.open_blocks)
        step.parent_id = self.open_blocks[-1].block_id if self.open_blocks else None

    # -- the condition trail ----------------------------------------------

    def update_conditions(self, node, text: str) -> None:
        stripped = text.strip()
        if isinstance(node, _CONDITION_PUSH):
            self.conditions.append(stripped)
        elif isinstance(node, _CONDITION_AMEND):
            # An arm sits at the depth of the `if` it belongs to, so it amends
            # the top entry rather than pushing. Replacing it would lose the
            # opening `if (...) then` that gives the arm its context.
            if self.conditions:
                self.conditions[-1] = f"{self.conditions[-1]} / {stripped}"
        elif isinstance(node, f03.Case_Stmt):
            # Same idea, except a select can carry dozens of arms, so this
            # replaces any previously appended case rather than accumulating
            # them: a trail ends in the `select case (...)` plus this arm only.
            if self.conditions:
                base = _CASE_TRAIL_RE.split(self.conditions[-1], maxsplit=1)[0]
                self.conditions[-1] = f"{base} / {stripped}"
        elif isinstance(node, _CONDITION_POP):
            if self.conditions:
                self.conditions.pop()

    def close_label_do(self, node, end_line: int) -> None:
        """Close legacy labelled DO loops at their shared terminal statement."""

        parent = getattr(node, "parent", None)
        if not isinstance(parent, f03.Block_Label_Do_Construct):
            return
        children = list(getattr(parent, "children", ()))
        if not children or node is not children[-1]:
            return
        count = sum(isinstance(child, f03.Label_Do_Stmt) for child in children)
        for _ in range(count):
            if self.open_blocks:
                self.open_blocks.pop().end_line = end_line
            if self.conditions:
                self.conditions.pop()

    # -- select-case vocabularies -----------------------------------------

    def update_select_cases(
        self, node, text: str, location: SourceLocation, holder
    ) -> None:
        stripped = text.strip()
        if isinstance(node, f03.Select_Case_Stmt):
            after_keyword = stripped[stripped.lower().index("case") + len("case") :]
            balanced = extract_balanced_parens(after_keyword)
            subject = balanced[0].strip() if balanced else ""
            self.select_stack.append(
                SelectCaseDoc(subject=subject, cases=[], location=location)
            )
            return
        if (
            self.select_stack
            and isinstance(node, f03.Case_Stmt)
            and not CASE_DEFAULT_RE.match(stripped.lower())
        ):
            after = stripped[len("case") :].lstrip()
            balanced = extract_balanced_parens(after) if after.startswith("(") else None
            if balanced:
                self.select_stack[-1].cases.extend(
                    STRING_LITERAL_RE.findall(balanced[0])
                )
            return
        if self.select_stack and isinstance(node, f03.End_Select_Stmt):
            holder.select_cases.append(self.select_stack.pop())

    def close(self, ctx: "_FileContext") -> None:
        """Report anything still open when the scope ended."""

        for block in self.open_blocks:
            ctx.project.review_flags.append(
                ReviewFlag(
                    code="ast_unclosed_block",
                    severity="warning",
                    message=f"{block.kind} block never closed",
                    location=block.location,
                    target=block.raw,
                )
            )
        for select in self.select_stack:
            ctx.project.review_flags.append(
                ReviewFlag(
                    code="ast_unclosed_select",
                    severity="warning",
                    message=f"select case ({select.subject}) never closed",
                    location=select.location,
                )
            )


# `select case (x) / case ('a')` -- the arm appended by a previous `case`.
_CASE_TRAIL_RE = re.compile(r"\s/\scase\b", re.I)


def _statements_in_order(tree):
    """Every node fparser2 gave its own source item, in source order.

    A statement is exactly a node with an item: `walk` visits them in source
    order, one per statement, and a statement riding inside another -- the
    `Call_Stmt` of a one-line `if (c) call f()` -- carries no item of its own
    and so is reached through its host rather than counted twice.
    """

    return [node for node in walk(tree) if _item_span(node) is not None]


def _control_step(node, text: str, location: SourceLocation) -> ControlStep | None:
    for classes, kind in _STEP_KINDS:
        if isinstance(node, classes):
            stripped = text.strip()
            return ControlStep(
                kind=kind,
                summary=summarize_step(stripped),
                raw=text,
                location=location,
            )
    return None


def _target_root(target: str) -> str:
    """Reduce an assignment target to the bare name a dataflow join keys on.

    ``gw_state(cell_id)%stor`` -> ``gw_state``. The full text stays on
    ``AssignmentDoc.target``; only the join key is reduced.
    """

    return target.split("%", 1)[0].split("(", 1)[0].strip().lower()


def _record_declaration_defaults(text: str, string_defaults: dict[str, str]) -> None:
    """Carry a declaration's string initialiser into the filename defaults."""

    for variable in parse_declaration(text, SourceLocation("", 0)):
        if not variable.initial:
            continue
        literal = string_literal(variable.initial)
        if literal:
            string_defaults[variable.name.lower()] = literal


def _record_assignment_default(text: str, string_defaults: dict[str, str]) -> None:
    _label, body = split_statement_label(text)
    split = split_assignment(body)
    if split is None:
        return
    target, operator, expression = split
    if operator != "=":
        return
    literal = string_literal(expression)
    if literal is not None:
        string_defaults[target.lower()] = literal


def _enclosing_of(node, cls) -> str | None:
    """The name of the nearest enclosing *cls*, starting at *node* itself."""

    cur = node
    while cur is not None:
        if isinstance(cur, cls):
            return _scope_name(cur)
        cur = getattr(cur, "parent", None)
    return None


def _enclosing_procedure(node) -> str | None:
    cur = getattr(node, "parent", None)
    while cur is not None:
        if isinstance(cur, (f03.Subroutine_Subprogram, f03.Function_Subprogram)):
            return _scope_name(cur)
        if isinstance(cur, f03.Module):
            return None
        cur = getattr(cur, "parent", None)
    return None


def _owning_scope_is_interface(node) -> bool:
    cur = getattr(node, "parent", None)
    while cur is not None:
        if isinstance(cur, _BOUNDARY_CLASSES):
            return True
        cur = getattr(cur, "parent", None)
    return False


def build_ast_index(config: BuildConfig) -> ProjectIndex:
    """Build the AST-backed index for *config*'s source tree."""

    return AstIndexBuilder(config).build()
