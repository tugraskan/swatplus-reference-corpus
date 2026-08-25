---
kind: procedure
symbol: cond_integer_c
title: cond_integer_c
status: filled
source_hash: fe6c37d73615e79f
version_label: SWAT+ 62.0.0
args:
  op: '`op` selects which comparison to apply: `<`, `>`, `<=`, `>=`, `=`, or `/=`. The routine
    uses it to choose the single integer test that can invalidate the condition.'
  var_cur: '`var_cur` is the current integer value being checked, such as the current day
    passed in from `res_rel_conds`. It is compared against `var_tbl` to decide whether the
    condition passes or fails.'
  var_tbl: '`var_tbl` is the integer threshold or target value from the decision table. It
    is the value that `var_cur` must satisfy under `op` for the condition to remain a hit.'
uses:
  reservoir_conditions_module: '`reservoir_conditions_module` provides the shared `hit` flag
    that this routine updates. That flag is part of the reservoir-condition evaluation state,
    so changing it here directly affects whether the caller continues evaluating release conditions.'
---

<!-- facts:header -->

`cond_integer_c` evaluates an integer decision-table condition against the current value and marks the shared `hit` flag false when the test fails.

## Bottom Line

This subroutine is the integer-condition checker used by reservoir release rules. It compares the current integer value `var_cur` to a table value `var_tbl` under the operator in `op`, and it writes `hit = "n"` when the comparison does not hold.

It matters because the surrounding reservoir-condition workflow stops scanning conditions as soon as `hit` is no longer `"y"`. That allows `res_rel_conds` to decide whether a reservoir release rule is satisfied or whether release should be forced to zero.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside reservoir release-condition evaluation after `res_rel_conds` has selected an integer condition, converted the table value to an integer, and passed in the current value to test. Its result feeds the shared `hit` state that `res_rel_conds` checks to stop scanning conditions and, if none match, set release to zero.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | If the operator is `<`, require `var_cur` to be strictly less than `var_tbl`; otherwise mark the condition as not hit by setting `hit = "n"`. |
| 2. if | If the operator is `>`, require `var_cur` to be strictly greater than `var_tbl`; otherwise set `hit = "n"`. |
| 3. if | If the operator is `<=`, require `var_cur` to be less than or equal to `var_tbl`; otherwise set `hit = "n"`. |
| 4. if | If the operator is `>=`, require `var_cur` to be greater than or equal to `var_tbl`; otherwise set `hit = "n"`. |
| 5. if | If the operator is `=`, require exact equality between `var_cur` and `var_tbl`; otherwise set `hit = "n"`. |
| 6. if | If the operator is `/=`, require `var_cur` and `var_tbl` to differ; otherwise set `hit = "n"`. |
| 7. return | Return to the caller after possibly updating the shared `hit` flag. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_conditions_module] | `hit` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hit` | When the selected comparison fails for the given `op` and integer values. | `hit` is changed to `"n"` to record that the current condition did not pass. The caller uses this to stop further condition checking and treat the release rule as unmet. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed this file. `df07e3f` added `cond_integer_c.f90` with the integer comparison logic and the shared `hit` update. `c7c8e22` preserved the same logic and only carried the file forward into the newer source drop without changing the routine behavior shown in the diff.

- `df07e3f` introduced the subroutine and its six operator branches that set `hit = "n"` on failed integer comparisons.
- `c7c8e22` updated the source snapshot but did not change the visible comparison logic or state update behavior in this routine.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cond_integer_c' has no extracted documentation comment.
