---
kind: procedure
symbol: chg_par
title: chg_par
status: filled
source_hash: e5b4196c5e5680ba
version_label: SWAT+ 62.0.0
args:
  val_cur: '`val_cur` is the current parameter value when the change is relative to the existing
    setting, such as additive, percent, or multiplicative updates.'
  chg_typ: '`chg_typ` selects the change rule to apply; the routine branches on `absval`,
    `abschg`, `pctchg`, or `relchg`.'
  chg_val: '`chg_val` is the user-supplied change amount, either the new absolute value, an
    increment, a percent, or a relative factor depending on `chg_typ`.'
  absmin: '`absmin` is the lower bound used to prevent the returned parameter value from dropping
    below the allowed minimum.'
  absmax: '`absmax` is the upper bound used to prevent the returned parameter value from exceeding
    the allowed maximum.'
locals:
  chg_par: '`chg_par` is the function result; it holds the candidate updated parameter value
    before and after bounding.'
  amin1: '`amin1` is the upper-bounding function used to cap the candidate value at `absmax`
    after the lower bound has already been applied.'
---

<!-- facts:header -->

Computes a new parameter value from a current value and a user-specified change mode, then constrains the result to absolute bounds.

## Bottom Line

`chg_par` is a small calibration helper that turns an existing parameter value into a new one according to `chg_typ`. It supports four change modes: set an absolute value, add an absolute increment, apply a percent change, or apply a relative multiplier.

After the change is computed, the function clamps the result between `absmin` and `absmax`. Callers use that bounded result when updating parameters such as curve number and plant or HRU calibration values.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`chg_par` runs whenever calibration, scheduling, or action logic needs to convert a requested change into a valid parameter value. Its callers prepare the current value, the change type, the change magnitude, and the allowed bounds, and downstream model behavior depends on the bounded result when parameters like `cn2` or plant traits are updated.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. choose change mode | Branch on `chg_typ` to decide how to transform the current parameter value. |
| 2. set absolute value | If the mode is `absval`, ignore the current value and use `chg_val` directly as the new parameter value. |
| 3. add absolute increment | If the mode is `abschg`, add the requested increment in `chg_val` to the current value. |
| 4. apply percent change | If the mode is `pctchg`, convert the percentage in `chg_val` to a multiplier and scale the current value by it. |
| 5. apply relative change | If the mode is `relchg`, treat `chg_val` as a fractional factor and scale the current value by `1 + chg_val`. |
| 6. enforce lower bound | Raise the candidate value to at least `absmin` so the result cannot fall below the allowed minimum. |
| 7. enforce upper bound | Cap the candidate value at `absmax` using `amin1`, ensuring the final result does not exceed the allowed maximum. |
| 8. return result | Return the bounded parameter value to the caller as the function result. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits touched `chg_par`. Commit df07e3f added the file with the function, its inline purpose comments, the four change modes, and the final min/max bounding. Commit 889136d only corrected a typo in the purpose comment from "paramter" to "parameter" without changing behavior.

- df07e3f introduced `chg_par` as a reusable parameter-change helper with absolute, additive, percent, and relative update modes plus hard bounds on the output.
- 889136d made a documentation-only typo fix in the function header; the executable logic was unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'chg_par' has no extracted documentation comment.
