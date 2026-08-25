---
kind: procedure
symbol: cond_real_c
title: cond_real_c
status: filled
source_hash: 58c9242f2110a913
version_label: SWAT+ 62.0.0
args:
  op: Comparison operator to apply between `var_cur` and `var_tbl`; only `<`, `>`, `<=`, `>=`,
    `=`, and `/=` are handled.
  var_cur: Current real value being tested against the decision-table threshold.
  var_tbl: Real decision-table value that `var_cur` is compared with.
uses:
  reservoir_conditions_module: '`cond_real_c` writes the module variable `hit` in `reservoir_conditions_module`;
    that shared flag is the routine’s only output and is how the surrounding reservoir-condition
    search records whether the tested comparison passed or failed.'
---

<!-- facts:header -->

Checks whether a real-valued condition matches a comparison operator and leaves the reservoir-condition hit flag unchanged unless the test fails.

## Bottom Line

`cond_real_c` is a small comparison helper used by reservoir condition-table logic. It evaluates one real variable against a table value using the operator passed in `op` and, when the comparison is not satisfied, it marks the shared `hit` flag as `'n'`.

It matters because `res_rel_conds` uses this routine while scanning condition sets for reservoir release rules. A failed comparison flips `hit` away from the default `'y'`, which prevents the current condition set from being treated as satisfied.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside reservoir release-condition evaluation after `res_rel_conds` has selected a condition expression and loaded the operator, current state value, and table threshold for a specific variable such as `stor`, `inflo`, `pdsi`, or `day`. Its result feeds the broader condition-set check in `res_rel_conds`, which uses `hit` to decide whether the current rule set remains satisfied while searching for the active reservoir module.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. test `<` condition | If the operator is `<`, the routine checks whether the current value is actually less than the table value; if it is not, it marks the shared hit flag as failed. |
| 2. test `>` condition | If the operator is `>`, the routine checks whether the current value is actually greater than the table value; if it is not, it marks the shared hit flag as failed. |
| 3. test `<=` condition | If the operator is `<=`, the routine checks whether the current value is at most the table value; if it is greater, it marks the shared hit flag as failed. |
| 4. test `>=` condition | If the operator is `>=`, the routine checks whether the current value is at least the table value; if it is smaller, it marks the shared hit flag as failed. |
| 5. test `=` condition | If the operator is `=`, the routine checks for exact equality between the current value and the table value; if they differ, it marks the shared hit flag as failed. |
| 6. test `/=` condition | If the operator is `/=`, the routine checks that the current value is not equal to the table value; if they are equal, it marks the shared hit flag as failed. |
| 7. return | Returns to the caller after possibly updating the shared hit flag; no value is returned directly because the routine communicates through module state. |

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
| `hit` | When a comparison implied by `op` fails for `var_cur` versus `var_tbl`. | The routine sets the shared `hit` flag to `'n'` to record that the tested subcondition did not match the requested operator relation. If the comparison succeeds, `hit` is left unchanged, so the caller can keep treating the current condition set as still active. |

## File I/O

<!-- facts:io -->


## Lineage

Two lineage commits were resolved for `cond_real_c`. The initial addition commit `df07e3f` introduced the subroutine with its operator-based real comparisons and shared `hit` flag update. The later commit `c7c8e22` shows the same routine body with only formatting/comment-preservation changes in the extracted diff, not a behavior change.

- `df07e3f` added `cond_real_c` as a comparison helper that sets the shared `hit` flag to `'n'` when a real-valued condition fails.
- `c7c8e22` did not change the extracted comparison logic; the diff shows the same operator tests and `hit = "n"` assignments after the source was brought in from bitbucket.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cond_real_c' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into 7 steps by grouping each operator check with its failure assignment, while keeping source line references within the visible source block.
