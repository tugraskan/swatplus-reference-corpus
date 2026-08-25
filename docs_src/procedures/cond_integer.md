---
kind: procedure
symbol: cond_integer
title: cond_integer
status: filled
source_hash: 6ea6164f4932a5ed
version_label: SWAT+ 62.0.0
args:
  ic: '`ic` selects which condition row in `d_tbl%alt` is being evaluated, so it chooses the
    operator set that controls the comparison for this pass.'
  var_cur: '`var_cur` is the current integer value extracted by the caller and tested against
    the table threshold for each alternative.'
  var_tbl: '`var_tbl` is the integer threshold from the decision table; it is compared with
    `var_cur` to decide whether each alternative stays active.'
locals:
  ialt: '`ialt` is the loop index over decision-table alternatives. It starts at 0, then counts
    from 1 through `d_tbl%alts` while the routine checks each alternative for the selected
    condition.'
uses:
  conditional_module: '`conditional_module` provides the shared decision-table state that
    this routine filters. `d_tbl%alts` sets the number of alternatives to inspect, `d_tbl%alt(ic,ialt)`
    supplies the operator stored for the current condition and alternative, and `d_tbl%act_hit(ialt)`
    is the per-alternative hit flag that this routine may turn from `y` to `n` when the integer
    comparison fails.'
---

<!-- facts:header -->

`cond_integer` checks one integer condition against a decision-table threshold and invalidates any alternatives that fail the comparison. It is a small rule-filtering routine used while evaluating conditional actions.

## Bottom Line

`cond_integer` is part of SWAT+’s conditional-decision logic. Given a current integer value (`var_cur`), a table value (`var_tbl`), and a condition index (`ic`), it scans every alternative for that condition and turns off any alternative whose operator does not match the observed comparison.

The routine matters because it updates `d_tbl%act_hit(ialt)`, which marks whether each alternative still satisfies all required rules. Later condition-processing and action execution depend on those hit flags to decide whether a table action should remain eligible.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`conditions` calls `cond_integer` after it has chosen the current object (`ob_num`), read the current integer value into `ivar_cur`, and converted the decision-table limit into `ivar_tbl` from `d_tbl%cond(ic)%lim_const`. This routine runs during condition evaluation, before action selection, and its result controls whether a decision-table alternative remains eligible for later model actions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the alternative index and begin scanning the decision table. | The routine initializes `ialt` and loops over every alternative recorded in `d_tbl%alts`. |
| 2. Skip alternatives that are already inactive or have no operator for this condition. | Only alternatives with a real operator other than `'-'` and a current hit flag of `y` are evaluated further. |
| 3. Enforce the strict-less-than operator. | If the table operator is `<`, the alternative fails when `var_cur` is greater than or equal to `var_tbl`, and `d_tbl%act_hit(ialt)` is set to `n`. |
| 4. Enforce the strict-greater-than operator. | If the table operator is `>`, the alternative fails when `var_cur` is less than or equal to `var_tbl`, and the hit flag is cleared. |
| 5. Enforce the less-than-or-equal operator. | If the table operator is `<=`, the alternative fails when `var_cur` is greater than `var_tbl`. |
| 6. Enforce the greater-than-or-equal operator. | If the table operator is `>=`, the alternative fails when `var_cur` is less than `var_tbl`. |
| 7. Enforce equality. | If the table operator is `=`, the alternative fails when `var_cur` and `var_tbl` are not equal. |
| 8. Enforce inequality. | If the table operator is `/=`, the alternative fails when `var_cur` and `var_tbl` are equal. |
| 9. Continue until all alternatives are processed, then return. | The loop ends after all alternatives have been tested, and the subroutine returns with any failed alternatives marked inactive. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:conditional_module] | `d_tbl` | `d_tbl%alts, d_tbl%alt(ic,ialt), d_tbl%act_hit(ialt)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `d_tbl%act_hit(ialt)` | When `d_tbl%alt(ic,ialt)` is one of `<`, `>`, `<=`, `>=`, `=`, or `/=` and the current integer comparison does not satisfy that operator. | `d_tbl%act_hit(ialt)` changes from `y` to `n` to record that this alternative no longer satisfies all required conditions for the current decision-table pass. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The procedure was introduced in df07e3f as a new file containing the integer-condition loop and hit-flag updates. Commit 39fabde did not change the algorithm; it only initialized `ialt` to 0 in the declaration.

- df07e3f added `cond_integer` with the alternative-scan logic that compares `var_cur` and `var_tbl` against the operator in `d_tbl%alt(ic,ialt)` and clears `d_tbl%act_hit(ialt)` on mismatch.
- 39fabde changed only the local initialization of `ialt` from an uninitialized integer declaration to `integer :: ialt = 0`; the filtering behavior remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cond_integer' has no extracted documentation comment.
