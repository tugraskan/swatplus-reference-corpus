"""The one source/location layer: physical Fortran lines in, logical statements out.

Every parser in this package needs the same three things from raw source text:
where a comment starts, where a statement ends, and which physical lines a
logical statement spans. Those answers used to be re-derived in four modules --
`schema_fortran` did it correctly with a quote-aware scanner, while `fortran`,
`documentation` and `refs` each split on a bare ``!``, which truncates any line
whose string literal contains one. Centralising them here is what makes a later
parser swap comparable: both parsers consume the same notion of "a statement".

The contract frozen here is deliberately narrow and is covered case by case in
`tests/test_source_layer.py`:

* A ``!`` inside a string literal is not a comment. Doubled quotes (``''``)
  escape within a literal.
* A trailing ``&`` continues a statement; a leading ``&`` on the continuation is
  removed. Comment-only and blank lines between continuation lines are skipped
  without breaking the join, matching Fortran's own rule.
* ``text`` is the joined code with the comment removed and the outer edges
  trimmed. Interior spacing is left exactly as written -- it is part of the
  byte-sensitive ``raw``/``summary``/``condition`` strings the schema resolver
  matches on. Ordinary continuation pieces are joined with one space;
  character-literal pieces are joined directly and keep significant spaces
  around their continuation markers. ``raw`` is the exact physical lines the
  statement spans, comments and all, joined with ``\\n``.
* Several statements separated by ``;`` each become their own logical line,
  sharing the physical span and ``raw`` of the line that carries them.
* ``start`` and ``end`` are 1-based inclusive physical line numbers, so a span
  can address GitHub's ``#L<start>-L<end>`` directly.
* Case is preserved. Callers lower-case at the point of comparison instead.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class LogicalLine:
    """One Fortran statement and the physical lines it occupies."""

    text: str
    start: int
    end: int
    raw: str


def _split_fortran_comment(
    line: str, initial_quote: str | None = None
) -> tuple[str, str, str | None]:
    """Stateful implementation used for continued character literals."""

    quote = initial_quote
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
            return line[:idx], line[idx + 1 :], quote
        idx += 1
    return line, "", quote


def split_fortran_comment(line: str) -> tuple[str, str]:
    """Split a physical line into (code, comment) respecting string literals.

    A bare ``line.split("!")`` truncates ``write (*,*) "! ERROR: ..."`` at the
    first character of the message. Quotes are tracked so that only a ``!``
    outside a literal starts a comment; a doubled quote inside a literal is an
    escaped quote, not the end of it.
    """

    code, comment, _quote = _split_fortran_comment(line)
    return code, comment


def strip_fortran_comment(line: str) -> str:
    """Return just the code half of a physical line."""

    return split_fortran_comment(line)[0]


def split_statements(code: str) -> list[str]:
    """Split one line's code on ``;`` separators outside string literals.

    Fortran allows several statements on a line. A ``;`` inside a literal --
    ``"row(s); expected "`` -- is text, not a separator, so the same quote
    tracking as :func:`split_fortran_comment` applies. Empty pieces are dropped,
    so a trailing ``;`` yields no phantom statement.
    """

    parts: list[str] = []
    buffer: list[str] = []
    quote: str | None = None
    idx = 0
    while idx < len(code):
        char = code[idx]
        if quote:
            if char == quote:
                if idx + 1 < len(code) and code[idx + 1] == quote:
                    buffer.append(code[idx : idx + 2])
                    idx += 2
                    continue
                quote = None
        elif char in {"'", '"'}:
            quote = char
        elif char == ";":
            parts.append("".join(buffer))
            buffer = []
            idx += 1
            continue
        buffer.append(char)
        idx += 1
    parts.append("".join(buffer))
    return [part for part in (piece.strip() for piece in parts) if part]


def _emit(output: list[LogicalLine], text: str, start: int, end: int, raw: str) -> None:
    """Append one entry per statement on the joined line.

    Fortran allows ``a = 1; b = 2``. Each statement becomes its own logical
    line so none is lost, and they share the physical span and ``raw`` of the
    line that carries them -- the span is a property of the source text, not of
    how many statements were written on it.
    """

    for statement in split_statements(text):
        output.append(LogicalLine(text=statement, start=start, end=end, raw=raw))


def logical_lines(lines: list[str]) -> list[LogicalLine]:
    """Join continuations into logical statements with their physical spans."""

    output: list[LogicalLine] = []
    buffer: list[str] = []
    raw_buffer: list[str] = []
    start_line = 1
    continuing = False
    continued_quote: str | None = None

    for number, raw in enumerate(lines, start=1):
        physical = raw.rstrip("\n")
        if continuing and (
            not physical.strip() or physical.lstrip().startswith("!")
        ):
            # Fortran lets a comment-only or blank line sit inside a continued
            # statement. Keep it in `raw` so the physical span stays contiguous,
            # but do not let it terminate the join. A whole-line comment stays a
            # comment even when the continued statement is inside a character
            # literal, so the quote state deliberately does not advance here.
            raw_buffer.append(physical)
            continue

        was_continuing = continuing
        initial_quote = continued_quote if was_continuing else None
        code, _comment, ending_quote = _split_fortran_comment(
            physical, initial_quote
        )
        stripped = code.rstrip()
        if not continuing and not stripped.strip():
            continue

        if not continuing:
            start_line = number
            buffer = []
            raw_buffer = []

        piece = stripped.strip()
        if was_continuing and piece.startswith("&"):
            piece = piece[1:]
            if initial_quote is None:
                piece = piece.lstrip()

        if piece.endswith("&"):
            piece = piece[:-1]
            if ending_quote is None:
                piece = piece.rstrip()
            continuing = True
            continued_quote = ending_quote
        else:
            continuing = False
            continued_quote = None

        if buffer and initial_quote is None:
            buffer.append(" ")
        buffer.append(piece)
        raw_buffer.append(physical)

        if not continuing:
            text = "".join(buffer).strip()
            if text:
                _emit(output, text, start_line, number, "\n".join(raw_buffer))

    if continuing and buffer:
        text = "".join(buffer).strip()
        if text:
            _emit(
                output,
                text,
                start_line,
                start_line + len(raw_buffer) - 1,
                "\n".join(raw_buffer),
            )
    return output


_FIXED_COMMENT_MARKERS = frozenset({"c", "C", "*", "!"})


def fixed_form_logical_lines(lines: list[str]) -> list[LogicalLine]:
    """Join fixed-form statements while preserving physical source spans.

    Columns 1-5 hold an optional statement label, column 6 marks a
    continuation, and columns 7-72 hold the statement. Unlike free form, the
    continuation is announced by the following line, so intervening blank and
    comment lines are held until the next code line determines whether they
    belong to the current statement's raw span.
    """

    output: list[LogicalLine] = []
    pieces: list[str] = []
    raw_buffer: list[str] = []
    between: list[str] = []
    start_line: int | None = None
    end_line: int | None = None
    quote: str | None = None

    def flush() -> None:
        nonlocal pieces, raw_buffer, start_line, end_line, quote
        if start_line is not None and end_line is not None:
            text = "".join(pieces).strip()
            if text:
                _emit(output, text, start_line, end_line, "\n".join(raw_buffer))
        pieces = []
        raw_buffer = []
        start_line = None
        end_line = None
        quote = None

    for number, raw in enumerate(lines, start=1):
        physical = raw.rstrip("\n")
        if not physical.strip() or (
            physical and physical[0] in _FIXED_COMMENT_MARKERS
        ):
            if start_line is not None:
                between.append(physical)
            continue

        label_field = physical[:5]
        continuation = len(physical) > 5 and physical[5] not in {" ", "0"}
        statement_field = physical[6:72] if len(physical) > 6 else ""
        initial_quote = quote if continuation and start_line is not None else None
        code, _comment, ending_quote = _split_fortran_comment(
            statement_field, initial_quote
        )

        # A `!` in the statement field is also a fixed-form comment line when
        # it is not continuing an open character literal.
        if not code.strip() and not (continuation and initial_quote is not None):
            if start_line is not None:
                between.append(physical)
            continue

        if continuation and start_line is not None:
            raw_buffer.extend(between)
            raw_buffer.append(physical)
            pieces.append(code.rstrip())
            end_line = number
            quote = ending_quote
            between = []
            continue

        flush()
        between = []
        label = label_field.strip()
        statement = code.strip()
        pieces = [f"{label} {statement}" if label else statement]
        raw_buffer = [physical]
        start_line = end_line = number
        quote = ending_quote

    flush()
    return output


def clean_doc_line(line: str) -> str:
    """Strip the comment marker off a documentation line."""

    stripped = line.strip()
    if stripped.startswith("!>"):
        return stripped[2:].strip()
    if stripped.startswith("!!"):
        return stripped[2:].strip()
    if stripped.startswith("!"):
        return stripped[1:].strip()
    return stripped


def inline_doc_from_raw(raw: str) -> str:
    """Collect the inline comments attached to a statement's physical lines.

    The quote state carries across physical lines for the same reason
    :func:`logical_lines` carries it. A ``!`` reached while a character literal
    is still open is text, and a ``!`` after that literal closes on a later
    line is a real comment. Splitting each physical line on its own gets both
    wrong: it invents documentation out of literal text and drops the comments
    that follow a continued literal. Whole-line comments are skipped before the
    scanner sees them, matching :func:`logical_lines`, so they are neither
    inline documentation nor a reason to advance the quote state.
    """

    comments: list[str] = []
    quote: str | None = None
    for physical in raw.splitlines():
        if physical.lstrip().startswith("!"):
            continue
        code, comment, quote = _split_fortran_comment(physical, quote)
        if not code.strip() or not comment.strip():
            continue
        comments.append(clean_doc_line("!" + comment.strip()))
    return "\n".join(comment for comment in comments if comment).strip()


_LABEL_RE = re.compile(r"^(\d+)\s+(\S.*)$")


def split_statement_label(text: str) -> tuple[str | None, str]:
    """Separate a leading statement label from the statement it labels.

    Fortran lets any statement carry a numeric label -- ``99 close (107)``,
    ``10  enddo``, ``26  lsu_num_cells(k) = cell_count``. Every pattern that
    anchors on the statement keyword (``^end``, ``^close``, the assignment
    target) fails on the labelled spelling, so the label is peeled off before
    such a pattern is applied. The caller keeps the original text for ``raw``:
    the label is part of the source, it just is not part of the statement's
    grammar.
    """

    match = _LABEL_RE.match(text.strip())
    if not match:
        return None, text
    return match.group(1), match.group(2)


def split_assignment(text: str) -> tuple[str, str, str] | None:
    """Split an assignment into ``(target, operator, expression)``.

    The split point is the first ``=`` or ``=>`` at paren depth zero and outside
    any character literal. Depth is what a pattern cannot track: SWAT+ writes
    targets whose own subscripts contain parentheses --
    ``gw_chan_info(channel)%cells(gw_chan_info(channel)%ncon)`` -- and a
    bracketed subscript group of the form ``\\([^()]*\\)`` stops at the first
    inner ``)``, so the whole statement fails to match and the assignment is
    lost rather than mis-split.

    Comparison operators are not assignments: ``==``, ``/=``, ``<=``, ``>=`` and
    ``=>``'s lookalikes are skipped, and ``=>`` itself is reported as its own
    operator so a pointer association stays distinguishable.

    This finds the split point; it does not decide that the statement is an
    assignment. ``do i = 1, n`` splits happily into ``do i`` and ``1, n``. The
    caller is expected to already know the statement's grammar -- the AST path
    calls this only for a node fparser2 parsed as an assignment -- which is what
    lets the split stay purely textual and therefore byte-exact. None means no
    top-level ``=`` was found at all, which the caller can report as "the AST
    says assignment, the bytes do not" rather than dropping the statement.
    """

    depth = 0
    quote: str | None = None
    idx = 0
    while idx < len(text):
        char = text[idx]
        if quote:
            if char == quote:
                if idx + 1 < len(text) and text[idx + 1] == quote:
                    idx += 2
                    continue
                quote = None
            idx += 1
            continue
        if char in {"'", '"'}:
            quote = char
        elif char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        elif char == "=" and depth == 0:
            previous = text[idx - 1] if idx else ""
            following = text[idx + 1] if idx + 1 < len(text) else ""
            if previous in {"=", "/", "<", ">"} or following == "=":
                # part of ==, /=, <=, >= -- a comparison, not an assignment
                idx += 1
                continue
            if following == ">":
                target, expression = text[:idx], text[idx + 2 :]
                if not target.strip():
                    return None
                return target.strip(), "=>", expression.strip()
            target, expression = text[:idx], text[idx + 1 :]
            if not target.strip() or not expression.strip():
                return None
            return target.strip(), "=", expression.strip()
        idx += 1
    return None


def strip_string_literals(text: str) -> str:
    """Remove every character literal, keeping the code around it.

    Fortran quotes with either ``'`` or ``"``, and a literal ends only at its
    own kind of quote. One left-to-right scan is what gets that right. Two
    independent substitutions cannot: run an ``'...'`` pattern over
    ``x = "don't" // 'y'`` and it pairs the apostrophe inside the double-quoted
    literal with the opening quote of ``'y'``, matching straight through the
    text between them and leaving ``x = "dony'``.

    A doubled quote inside a literal is an escaped quote, not the end of it, so
    ``'it''s'`` is removed whole. The quotes go with the literal, which keeps
    the result parseable as code by the callers that scan it for identifiers.
    """

    out: list[str] = []
    quote: str | None = None
    idx = 0
    while idx < len(text):
        char = text[idx]
        if quote:
            if char == quote:
                if idx + 1 < len(text) and text[idx + 1] == quote:
                    idx += 2
                    continue
                quote = None
            idx += 1
            continue
        if char in {"'", '"'}:
            quote = char
            idx += 1
            continue
        out.append(char)
        idx += 1
    return "".join(out)


# A binary `*` or `/` whose right operand carries a leading sign. The operator
# is captured with the character before it so `**` and `//` cannot match: their
# second character is not a word character or a closing bracket, and their first
# is never followed directly by a sign.
_SIGNED_OPERAND_RE = re.compile(
    r"([\w)\]])(\s*)([*/])(\s*)([-+])(\s*)"
    r"([A-Za-z_]\w*|\d[\d.]*(?:[eEdD][-+]?\d+)?)"
    r"(?![\w(%.])"
)


def normalize_nonstandard_signs(lines: list[str]) -> tuple[list[str], list[int]]:
    """Parenthesise a signed operand so a standard parser will accept it.

    **For parser input only.** The result must never reach a consumer: every
    raw string, source hash and location still comes from the unchanged lines.
    Callers pass the original list to the source layer and this result to
    fparser2.

    SWAT+ writes ``if ((Q*-1) >= ...)`` and ``cell_adv = heat_cell(i) * -1``.
    Two operators in a row is not valid Fortran -- gfortran accepts it, fparser2
    rejects the whole file -- and ``a * -b`` and ``a * (-b)`` denote the same
    value for ``*`` and ``/``, so inserting the parentheses is a rewrite of
    spelling rather than of meaning.

    Deliberately narrow:

    * ``**`` is excluded. Exponentiation is right-associative and unary minus
      binds looser than it, so ``a ** -b ** c`` means ``a ** (-(b ** c))``;
      wrapping the operand instead would give ``a ** ((-b) ** c)`` and silently
      change the value. ``//`` is excluded because it concatenates strings.
    * The operand must be a bare name or number. ``a * -b(i)`` is left alone
      because the parenthesis belongs around the whole reference, and wrapping
      only the name would produce ``a * (-b)(i)``.
    * Comments and character literals are untouched, so a ``*-`` inside a
      message or a commented-out line stays exactly as written.

    Anything not matched is left for the parser to reject, which keeps the
    failure visible instead of quietly half-repairing a file.

    Returns the rewritten lines and the 1-based numbers of those that changed.
    Line count is preserved, so every physical span stays valid.
    """

    out: list[str] = []
    changed: list[int] = []
    quote: str | None = None
    for number, raw in enumerate(lines, start=1):
        code, comment, ending_quote = _split_fortran_comment(raw, quote)
        rewritten, count = _rewrite_outside_literals(code, quote)
        if count:
            changed.append(number)
            tail = raw[len(code) :]
            out.append(rewritten + tail)
        else:
            out.append(raw)
        quote = ending_quote
    return out, changed


def _rewrite_outside_literals(code: str, quote: str | None) -> tuple[str, int]:
    """Apply the sign rewrite to the code between character literals only.

    A literal is copied through untouched, so ``msg = 'a*-1'`` keeps its text.
    The segments are rewritten independently, which is safe because the pattern
    is anchored on the character before the operator and a literal boundary can
    never supply one.
    """

    pieces: list[str] = []
    count = 0
    buffer: list[str] = []
    idx = 0
    while idx < len(code):
        char = code[idx]
        if quote:
            buffer.append(char)
            if char == quote:
                if idx + 1 < len(code) and code[idx + 1] == quote:
                    buffer.append(code[idx + 1])
                    idx += 2
                    continue
                quote = None
                pieces.append("".join(buffer))
                buffer = []
            idx += 1
            continue
        if char in {"'", '"'}:
            segment, hits = _SIGNED_OPERAND_RE.subn(
                r"\1\2\3\4(\5\6\7)", "".join(buffer)
            )
            pieces.append(segment)
            count += hits
            buffer = [char]
            quote = char
            idx += 1
            continue
        buffer.append(char)
        idx += 1
    if quote:
        pieces.append("".join(buffer))
    else:
        segment, hits = _SIGNED_OPERAND_RE.subn(
            r"\1\2\3\4(\5\6\7)", "".join(buffer)
        )
        pieces.append(segment)
        count += hits
    return "".join(pieces), count
