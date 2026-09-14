"""Nesting semantics for control steps.

The convention these tests pin down: a construct is recorded at the depth it
opens *at*, its body one deeper, and its `else`/`else if`/`case` arms at the
construct's own depth rather than inside it. That is what lets a consumer
rebuild the block tree from `block_id`, `parent_id` and `branch_of`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from swatplus_reference.parser.schema_config import BuildConfig
from swatplus_reference.parser.schema_fortran import FortranScanner


def _steps(tmp_path: Path, body: str):
    source = tmp_path / "sample.f90"
    source.write_text(
        "      subroutine sample\n" + body + "\n      end subroutine sample\n",
        encoding="utf-8",
    )
    index = FortranScanner(BuildConfig(source_dir=tmp_path)).scan()
    procedure = next(item for item in index.procedures if item.name == "sample")
    return {step.location.line: step for step in procedure.control_steps}


def test_nested_constructs_form_a_walkable_tree(tmp_path):
    steps = _steps(
        tmp_path,
        "\n".join(
            [
                "      do i = 1, n",            # 2
                "        if (a > 0) then",      # 3
                "          call inner ()",      # 4
                "        end if",               # 5
                "      end do",                 # 6
            ]
        ),
    )

    loop, branch, call = steps[2], steps[3], steps[4]
    assert (loop.kind, loop.depth, loop.parent_id) == ("loop", 0, None)
    assert loop.block_id is not None and loop.end_line == 6

    # The if opens inside the loop, so it sits one deeper and names it as parent.
    assert (branch.kind, branch.depth) == ("if", 1)
    assert branch.parent_id == loop.block_id
    assert branch.block_id is not None and branch.end_line == 5

    # The body of the if is deeper again, and its parent is the if, not the loop.
    assert (call.kind, call.depth) == ("call", 2)
    assert call.parent_id == branch.block_id


@pytest.mark.parametrize(
    "else_if_arm", ["else if (b > 0) then", "elseif (b > 0) then"]
)
def test_arms_sit_at_their_constructs_depth_not_inside_it(tmp_path, else_if_arm):
    steps = _steps(
        tmp_path,
        "\n".join(
            [
                "      if (a > 0) then",        # 2
                "        call first ()",        # 3
                f"      {else_if_arm}",         # 4
                "        call second ()",       # 5
                "      else",                   # 6
                "        call third ()",        # 7
                "      end if",                 # 8
            ]
        ),
    )

    opener = steps[2]
    for line in (4, 6):
        arm = steps[line]
        # Same depth as the construct, and pointing at it -- an arm belongs to
        # the construct without being nested one level inside it.
        assert arm.depth == opener.depth, line
        assert arm.branch_of == opener.block_id, line
        assert arm.block_id is None, line
    # Every arm's body is one deeper and owned by the construct.
    for line in (3, 5, 7):
        assert steps[line].depth == opener.depth + 1, line
        assert steps[line].parent_id == opener.block_id, line


def test_select_case_arms_behave_like_if_arms(tmp_path):
    steps = _steps(
        tmp_path,
        "\n".join(
            [
                "      select case (k)",        # 2
                "      case (1)",               # 3
                "        call one ()",          # 4
                "      case default",           # 5
                "        call other ()",        # 6
                "      end select",             # 7
            ]
        ),
    )

    opener = steps[2]
    assert opener.kind == "select" and opener.end_line == 7
    for line in (3, 5):
        assert steps[line].branch_of == opener.block_id
        assert steps[line].depth == opener.depth
    assert steps[4].depth == opener.depth + 1
    assert steps[4].parent_id == opener.block_id


def test_single_line_if_opens_no_block(tmp_path):
    """`if (cond) stmt` has no `then`, so nothing after it is nested."""

    steps = _steps(
        tmp_path,
        "\n".join(
            [
                "      if (a > 0) call guarded ()",  # 2
                "      call after ()",               # 3
            ]
        ),
    )

    assert steps[2].kind == "if"
    assert steps[2].block_id is None
    assert steps[2].end_line is None
    # The following statement must not have been swallowed into a phantom block.
    assert steps[3].depth == 0
    assert steps[3].parent_id is None


@pytest.mark.parametrize("closer", ["end do", "enddo", "END DO"])
def test_both_end_spellings_close_the_block(tmp_path, closer):
    steps = _steps(
        tmp_path,
        "\n".join(
            [
                "      do i = 1, n",       # 2
                "        call inner ()",   # 3
                f"      {closer}",         # 4
                "      call after ()",     # 5
            ]
        ),
    )

    assert steps[2].end_line == 4
    assert steps[5].depth == 0, "the loop must be closed before the next statement"


def test_unbalanced_ends_do_not_corrupt_the_nesting(tmp_path):
    """A stray end is ignored, and an unclosed construct keeps end_line unset."""

    steps = _steps(
        tmp_path,
        "\n".join(
            [
                "      end if",            # 2 - closes nothing
                "      call after ()",     # 3
                "      do i = 1, n",       # 4 - never closed
                "        call inner ()",   # 5
            ]
        ),
    )

    assert steps[3].depth == 0 and steps[3].parent_id is None
    assert steps[4].end_line is None
    assert steps[5].depth == 1 and steps[5].parent_id == steps[4].block_id


def test_nesting_resets_between_procedures(tmp_path):
    source = tmp_path / "two.f90"
    source.write_text(
        "\n".join(
            [
                "      subroutine first",
                "      do i = 1, n",
                "        call inner ()",
                "      end subroutine first",
                "      subroutine second",
                "      call plain ()",
                "      end subroutine second",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    index = FortranScanner(BuildConfig(source_dir=tmp_path)).scan()
    second = next(item for item in index.procedures if item.name == "second")

    # `first` leaves a loop open; that must not leak into the next procedure.
    assert [step.depth for step in second.control_steps] == [0]
    assert second.control_steps[0].parent_id is None
