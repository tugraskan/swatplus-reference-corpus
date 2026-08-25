---
kind: procedure
symbol: cond_real
title: cond_real
status: filled
source_hash: fb0ea444fd246583
version_label: SWAT+ 62.0.0
args:
  ic: '`ic` selects which condition column in `d_tbl%alt` to test, so it tells the routine
    which rule set applies to the current comparison.'
  var_cur: '`var_cur` is the computed current value for that condition; it is compared against
    the table value to decide whether each alternative stays active.'
  var_tbl: '`var_tbl` is the decision-table limit or target value for the selected condition,
    and it is the reference used in every comparison.'
  idtbl: '`idtbl` identifies the decision table upstream, but this routine does not use it
    in the logic; it is only referenced in a dummy check to suppress an unused-argument warning.'
locals:
  ialt: '`ialt` is the loop index over alternatives in the active decision table. It starts
    at 0 and is then advanced through `1` to `d_tbl%alts` to test each alternative in turn.'
uses:
  conditional_module: '`conditional_module` provides the shared active decision-table pointer
    `d_tbl` and its condition arrays. This routine must read `d_tbl%alts` to know how many
    alternatives exist, inspect `d_tbl%alt(ic,ialt)` to get the operator for the current condition/alternative,
    and update `d_tbl%act_hit(ialt)` so the rest of the conditional-action system can see
    which alternatives still pass.'
---

<!-- facts:header -->

`cond_real` checks one real-valued condition against each alternative in the active decision table and turns off any alternative whose comparison fails.

## Bottom Line

This subroutine is part of SWAT+ conditional logic. For a given condition index, it compares the current real value (`var_cur`) against the table threshold/value (`var_tbl`) for every active alternative in `d_tbl`, and it marks an alternative inactive by setting `d_tbl%act_hit(ialt)` to `'n'` when the comparison rule is not satisfied.

It matters because later conditional processing depends on `act_hit` to decide which alternatives remain eligible for actions. `conditions` calls this routine after it has assembled the relevant real-valued condition metric for the current decision-table condition.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cond_real` runs inside the conditional-decision workflow after `conditions` has prepared a real-valued condition metric and the matching table limit for the current condition. Its result feeds later decision-table evaluation by pruning alternatives in `d_tbl%act_hit`, which affects whether downstream conditional actions are allowed to execute.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load the conditional decision-table module and prepare to scan all alternatives. | The routine uses `conditional_module`, declares its inputs, initializes the loop counter `ialt`, and includes a no-op test on `idtbl` only to quiet the unused-argument warning. |
| 2. Loop over every alternative defined for the active decision table. | For each alternative index from 1 through `d_tbl%alts`, the routine considers the condition operator stored in `d_tbl%alt(ic,ialt)` and only continues if that alternative is still marked active in `d_tbl%act_hit(ialt)`. |
| 3. Enforce the '<' operator by rejecting values that are not strictly less than the table value. | If the operator for this condition is `<`, the routine turns the alternative off when `var_cur >= var_tbl`. |
| 4. Enforce the '>' operator by rejecting values that are not strictly greater than the table value. | If the operator is `>`, the routine turns the alternative off when `var_cur <= var_tbl`. |
| 5. Enforce the '<=' operator by rejecting values above the table value. | If the operator is `<=`, the routine turns the alternative off when `var_cur > var_tbl`. |
| 6. Enforce the '>=' operator by rejecting values below the table value. | If the operator is `>=`, the routine turns the alternative off when `var_cur < var_tbl`. |
| 7. Enforce the '=' operator by rejecting values that do not match exactly. | If the operator is `=`, the routine turns the alternative off when `var_cur /= var_tbl`. |
| 8. Enforce the '/=' operator by rejecting values that match exactly. | If the operator is `/=`, the routine turns the alternative off when `var_cur == var_tbl`. |
| 9. Finish the alternative scan and return to the caller. | After all alternatives are processed, the routine ends without creating new outputs beyond the updated `d_tbl%act_hit` flags. |

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
| `d_tbl%act_hit(ialt)` | When `d_tbl%alt(ic,ialt)` names a comparison operator and the corresponding comparison with `var_cur` and `var_tbl` fails. | `d_tbl%act_hit(ialt)` is changed from `'y'` to `'n'` to mark that alternative as no longer eligible because its real-valued condition does not satisfy the required relation. |

## File I/O

<!-- facts:io -->


## Lineage

`cond_real` was introduced in commit df07e3f with the full comparison loop against `d_tbl%alt(ic,ialt)` and updates to `d_tbl%act_hit(ialt)`. Commit c7c8e22 kept the routine logic intact while preserving the same comparison cases after importing the source. Commit 39fabde only changed the local declaration of `ialt` to initialize it to 0. Commit bd18ad4 added the unused-argument suppression (`if (idtbl < 0) continue`) and marked `idtbl` as unused in the comment; the comparison behavior did not change.

- df07e3f established the real-condition filter: a per-alternative pass over `d_tbl%alts` that flips `d_tbl%act_hit(ialt)` to `'n'` when `<`, `>`, `<=`, `>=`, `=`, or `/=` comparisons fail.
- 39fabde made `ialt` explicitly initialized to 0, a defensive local-variable change with no effect on the comparison logic.
- bd18ad4 added a no-op conditional on `idtbl` to silence an unused-variable warning; this does not alter runtime behavior of the condition checks.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cond_real' has no extracted documentation comment.
