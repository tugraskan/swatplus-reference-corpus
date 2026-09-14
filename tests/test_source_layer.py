"""Freeze the logical-source contract (Phase 2).

Everything downstream of the parser -- symbol spans, page source hashes, GitHub
line links, the schema resolver's byte-sensitive `raw`/`fields`/`condition`
strings -- rests on how physical Fortran lines become logical statements. These
tests pin that behaviour case by case so a later parser swap can be shown to
produce the same statements rather than merely similar ones.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from swatplus_reference.parser.facts import hash_slice
from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner
from swatplus_reference.parser.source_text import (
    fixed_form_logical_lines,
    inline_doc_from_raw,
    logical_lines,
    normalize_nonstandard_signs,
    split_fortran_comment,
    split_statements,
    strip_fortran_comment,
    strip_string_literals,
)


# --- comments -------------------------------------------------------------

@pytest.mark.parametrize(
    "line,code,comment",
    [
        ("x = 1  ! plain", "x = 1  ", " plain"),
        # The failure a bare split("!") produces: the message is the code.
        ('write (*,*) "! ERROR: bad"', 'write (*,*) "! ERROR: bad"', ""),
        ("y = 'a!b'  ! after", "y = 'a!b'  ", " after"),
        # A doubled quote escapes within a literal, so the ! stays inside it.
        ("y = 'it''s ! here'", "y = 'it''s ! here'", ""),
        ("x = 1 ! don't split", "x = 1 ", " don't split"),
        ("! whole line", "", " whole line"),
        ("x = 1 !! doc | units", "x = 1 ", "! doc | units"),
        ('mixed = "a" // "b!" ! tail', 'mixed = "a" // "b!" ', " tail"),
    ],
)
def test_comment_splitting_respects_string_literals(line, code, comment):
    assert split_fortran_comment(line) == (code, comment)
    assert strip_fortran_comment(line) == code


# --- statement separators -------------------------------------------------

@pytest.mark.parametrize(
    "code,expected",
    [
        ("a = 1; b = 2", ["a = 1", "b = 2"]),
        ("print*; print*", ["print*", "print*"]),
        # A ; inside a literal is text, not a separator.
        ('write(*,*) "row(s); expected"', ['write(*,*) "row(s); expected"']),
        ("x = 'it''s; here'; y = 2", ["x = 'it''s; here'", "y = 2"]),
        ("a = 1;", ["a = 1"]),          # no phantom trailing statement
        (";", []),
        ("plain", ["plain"]),
    ],
)
def test_statement_splitting_respects_string_literals(code, expected):
    assert split_statements(code) == expected


def test_multiple_statements_share_their_physical_span():
    (first, second) = logical_lines(["a = 1; b = 2"])

    assert (first.text, second.text) == ("a = 1", "b = 2")
    # The span describes the source text, not how many statements sit on it.
    assert (first.start, first.end) == (1, 1)
    assert (second.start, second.end) == (1, 1)
    assert first.raw == second.raw == "a = 1; b = 2"


# --- continuations --------------------------------------------------------

@pytest.mark.parametrize(
    "lines",
    [
        ["call foo (a, &", "          b)"],
        ["call foo (a, &", "     &    b)"],          # leading & on the next line
        ["call foo (a, &", "   ! why", "          b)"],  # comment inside
        ["call foo (a, &", "", "          b)"],          # blank line inside
        ["call foo (a, & ! trailing", "          b)"],
    ],
)
def test_continuations_join_into_one_statement(lines):
    joined = logical_lines(lines)

    assert len(joined) == 1
    assert joined[0].text == "call foo (a, b)"
    # The span covers every physical line the statement occupies, including any
    # comment or blank line sitting inside the continuation.
    assert (joined[0].start, joined[0].end) == (1, len(lines))
    assert joined[0].raw == "\n".join(lines)


def test_unterminated_continuation_still_yields_its_span():
    joined = logical_lines(["call foo (a, &", "          b, &"])

    assert len(joined) == 1
    assert (joined[0].start, joined[0].end) == (1, 2)


def test_fixed_form_columns_labels_and_continuations_are_preserved():
    lines = [
        "  100 value = 'abc'",
        "     1 // 'def'",
        "C comment inside the continuation",
        "     2 // 'ghi'",
    ]

    (joined,) = fixed_form_logical_lines(lines)

    assert joined.text == "100 value = 'abc' // 'def' // 'ghi'"
    assert (joined.start, joined.end) == (1, 4)
    assert joined.raw == "\n".join(lines)


# --- whitespace, case, and spans -----------------------------------------

def test_interior_whitespace_is_preserved_and_only_the_edges_are_trimmed():
    """Interior spacing is part of the byte-sensitive `raw`/`summary` strings."""

    (line,) = logical_lines(["   x    =     1   "])

    assert line.text == "x    =     1"
    assert line.raw == "   x    =     1   "


def test_continuation_pieces_are_joined_with_exactly_one_space():
    """Ordinary (non-character) pieces get one separating space."""

    (line,) = logical_lines(["call foo (a,   &", "        b)"])

    assert line.text == "call foo (a, b)"


def test_character_literal_continuation_adds_no_space_and_keeps_bang():
    (line,) = logical_lines(["print *, 'ab&", "&!cd'"])

    assert line.text == "print *, 'ab!cd'"


def test_character_literal_continuation_preserves_significant_spaces():
    (line,) = logical_lines(["value = 'ab  &", "&  cd'"])

    assert line.text == "value = 'ab    cd'"


def test_comment_line_inside_character_continuation_stays_a_comment():
    (line,) = logical_lines(["value = 'ab&", "! explanation", "&cd'"])

    assert line.text == "value = 'abcd'"
    assert (line.start, line.end) == (1, 3)


def test_dollar_sentinel_stays_a_comment_inside_a_continuation():
    """Match fparser2: `!$` is skipped and the next code line resumes the join."""

    (line,) = logical_lines(["integer :: x, &", "!$ y", "x = 1"])

    assert line.text == "integer :: x, x = 1"
    assert (line.start, line.end) == (1, 3)
    assert line.raw == "integer :: x, &\n!$ y\nx = 1"


def test_tabs_are_treated_as_leading_whitespace():
    (line,) = logical_lines(["\tx = 1"])

    assert line.text == "x = 1"
    assert line.raw == "\tx = 1"


def test_case_is_preserved_for_callers_to_normalise():
    (line,) = logical_lines(["CALL Foo (X)"])

    assert line.text == "CALL Foo (X)"


@pytest.mark.parametrize(
    "closer", ["end if", "endif", "ENDIF", "end do", "enddo", "end select", "endselect"]
)
def test_closed_up_end_forms_survive_as_statements(closer):
    (line,) = logical_lines([closer])

    assert line.text == closer


def test_blank_and_comment_lines_do_not_shift_following_spans():
    """A GitHub #L link is only right if the span counts physical lines."""

    lines = ["", "! a comment", "", "x = 1", "! another", "y = 2"]

    spans = [(item.text, item.start, item.end) for item in logical_lines(lines)]

    assert spans == [("x = 1", 4, 4), ("y = 2", 6, 6)]


def test_span_addresses_the_physical_slice_the_hash_uses():
    """`hash_slice` takes physical 1-based inclusive lines; spans must match."""

    lines = ["subroutine s", "  call foo (a, &", "            b)", "end subroutine s"]
    joined = logical_lines(lines)
    call = next(item for item in joined if item.text.startswith("call"))

    assert (call.start, call.end) == (2, 3)
    assert hash_slice(lines, call.start, call.end) == hash_slice(lines, 2, 3)


# --- byte-sensitive compatibility fields ---------------------------------

def _scan(tmp_path: Path, body: str):
    source = tmp_path / "sample.f90"
    source.write_text(
        "      subroutine sample\n" + body + "\n      end subroutine sample\n",
        encoding="utf-8",
    )
    index = FortranScanner(BuildConfig(source_dir=tmp_path)).scan()
    return next(item for item in index.procedures if item.name == "sample")


def test_io_raw_fields_and_condition_are_byte_exact(tmp_path):
    """The schema resolver reads these strings literally, so pin their bytes."""

    procedure = _scan(
        tmp_path,
        "\n".join(
            [
                "      if (ok == 1) then",
                '        open (107, file = "demo.in")',
                "        read (107,*,iostat=eof) alpha, beta",
                "      end if",
            ]
        ),
    )
    opened = next(item for item in procedure.io if item.kind == "open")
    read = next(item for item in procedure.io if item.kind == "read")

    assert opened.raw == 'open (107, file = "demo.in")'
    assert opened.file_expr == '"demo.in"'
    assert opened.condition == "if (ok == 1) then"
    assert read.raw == "read (107,*,iostat=eof) alpha, beta"
    assert read.fields == ["alpha", "beta"]
    assert read.condition == "if (ok == 1) then"


def test_control_step_raw_and_summary_are_byte_exact(tmp_path):
    procedure = _scan(
        tmp_path,
        "\n".join(
            [
                "      do i = 1, n",
                "        call inner (a, b)",
                "      end do",
            ]
        ),
    )
    loop, call = procedure.control_steps

    assert (loop.raw, loop.summary) == ("do i = 1, n", "do i = 1, n")
    assert (call.raw, call.summary) == ("call inner (a, b)", "call inner (a, b)")


def test_continued_statement_keeps_its_joined_text_in_raw(tmp_path):
    """`raw` on a control step is the joined statement, not one physical line."""

    procedure = _scan(
        tmp_path,
        "\n".join(
            [
                "      call inner (a, &",
                "                  b)",
            ]
        ),
    )
    (step,) = procedure.control_steps

    assert step.raw == "call inner (a, b)"
    assert step.location.line == 2
    assert step.location.end_line == 3


def test_statements_after_a_semicolon_are_not_lost(tmp_path):
    """`case ('x'); read(...)` hid the read from the I/O layer entirely."""

    procedure = _scan(
        tmp_path,
        "\n".join(
            [
                "      select case (key)",
                "      case ('ncell');   read (code_val,*) ncell",
                "      end select",
            ]
        ),
    )

    assert [item.kind for item in procedure.io] == ["read"]
    assert procedure.io[0].raw == "read (code_val,*) ncell"
    assert [step.kind for step in procedure.control_steps] == ["select", "case", "io"]


# --- inline documentation across continuations ----------------------------

# `inline_doc_from_raw` reads the same physical lines `logical_lines` joined,
# so it has to track quotes the same way. Splitting each line on its own both
# invents documentation and loses it; one test pins each direction.


def test_inline_doc_ignores_a_bang_inside_a_continued_character_literal():
    """A `!` reached while the literal is still open is text, not a comment."""

    (line,) = logical_lines(["character(len=8) :: msg = 'ab&", "&!cd'"])

    assert line.text == "character(len=8) :: msg = 'ab!cd'"
    assert inline_doc_from_raw(line.raw) == ""


def test_inline_doc_keeps_a_comment_after_a_continued_literal_closes():
    """A `!` after the literal closes on a later line is a real comment."""

    (line,) = logical_lines(["value = 'ab&", "&cd' ! real comment"])

    assert line.text == "value = 'abcd'"
    assert inline_doc_from_raw(line.raw) == "real comment"


def test_inline_doc_skips_whole_line_comments_inside_a_continuation():
    """Whole-line comments are not inline documentation, quoted or not."""

    (line,) = logical_lines(["value = 'ab&", "! explanation", "&cd' ! units"])

    assert line.text == "value = 'abcd'"
    assert inline_doc_from_raw(line.raw) == "units"


# --- character literals ---------------------------------------------------


@pytest.mark.parametrize(
    "line,expected",
    [
        ("a = b + c", "a = b + c"),
        ("100 format (1x,'   hru','   day')", "100 format (1x,,)"),
        ('1234 format(/,"  Date of Sim", 2x,i2)', "1234 format(/,, 2x,i2)"),
        # A doubled quote escapes within a literal, so the whole thing goes.
        ("y = 'it''s here' + z", "y =  + z"),
        # Mixed quoting: a literal ends only at its own kind of quote. Running
        # an `'...'` pattern over this pairs the apostrophe inside the
        # double-quoted literal with the opening quote of `'y'` and eats the
        # text between them, leaving `x = "dony'`.
        ("""x = "don't" // 'y'""", "x =  // "),
        # An unterminated literal consumes the rest of the line rather than
        # leaving quoted text behind for a caller to misread as code.
        ("msg = 'unterminated", "msg = "),
    ],
)
def test_strip_string_literals(line, expected):
    assert strip_string_literals(line) == expected


def test_strip_string_literals_leaves_a_comment_to_the_comment_splitter():
    # The two are composed by callers; each does only its own job.
    line = "x = 'a' ! why"
    assert strip_string_literals(strip_fortran_comment(line)) == "x =  "


# --- non-standard signed operands (AST input only) ------------------------


@pytest.mark.parametrize(
    "line,expected",
    [
        # The two spellings the pinned tree actually contains.
        ("if((Q*-1) >= stor) then", "if((Q*(-1)) >= stor) then"),
        ("cell_adv = heat_cell(i) * -1", "cell_adv = heat_cell(i) * (-1)"),
        ("w = a / -2.5e3", "w = a / (-2.5e3)"),
        ("p = a * +b", "p = a * (+b)"),
    ],
)
def test_normalize_parenthesises_a_signed_operand(line, expected):
    normalized, changed = normalize_nonstandard_signs([line])
    assert normalized == [expected]
    assert changed == [1]


@pytest.mark.parametrize(
    "line,why",
    [
        # Exponentiation is right-associative and unary minus binds looser, so
        # `a ** -b ** c` is `a ** (-(b ** c))`. Wrapping the operand would give
        # `a ** ((-b) ** c)` -- a different value.
        ("x = a ** -b ** c", "** would change the value"),
        ("s = a // -b", "// concatenates strings"),
        # The parenthesis belongs around the whole reference; wrapping the name
        # alone would produce `a * (-b)(i)`.
        ("y = a * -b(i)", "operand is subscripted"),
        ("z = a * -b%c", "operand has a component"),
        # Already legal, and not a binary operator.
        ("v = f(-1)", "unary minus after an opening paren is fine"),
        ("u = -1 * a", "leading unary minus is fine"),
        # Comments and literals are text.
        ("!if ((Q*-1 == 1).ge.x) then", "whole-line comment"),
        ("msg = 'a*-1'", "single-quoted literal"),
        ('msg = "a*-1"', "double-quoted literal"),
    ],
)
def test_normalize_leaves_everything_else_alone(line, why):
    normalized, changed = normalize_nonstandard_signs([line])
    assert normalized == [line], why
    assert changed == []


def test_normalize_rewrites_code_but_not_a_literal_on_the_same_line():
    line = "both = 'a*-1' // ' x' ; q = r*-2"
    normalized, changed = normalize_nonstandard_signs([line])
    assert normalized == ["both = 'a*-1' // ' x' ; q = r*(-2)"]
    assert changed == [1]


def test_normalize_preserves_line_count_and_trailing_comment():
    lines = [
        "      if((Q*-1) >= stor) then !can only remove what is there",
        "      x = 1",
    ]
    normalized, changed = normalize_nonstandard_signs(lines)
    assert len(normalized) == len(lines)
    assert changed == [1]
    assert normalized[0].endswith("!can only remove what is there")
    assert "Q*(-1)" in normalized[0]
    assert normalized[1] == lines[1]


def test_normalize_does_not_reach_into_a_continued_literal():
    """A `*-` inside a literal that spans a continuation is still text."""

    lines = [
        "      msg = 'start a*-1 &",
        "            more a*-2'",
        "      q = r*-3",
    ]
    normalized, changed = normalize_nonstandard_signs(lines)
    assert normalized[0] == lines[0]
    assert normalized[1] == lines[1]
    assert normalized[2] == "      q = r*(-3)"
    assert changed == [3]
