---
kind: procedure
symbol: icl
title: icl
status: filled
source_hash: 6012b2def02323b2
version_label: SWAT+ 62.0.0
args:
  id: '`id` is the Julian day value being converted into a month-relative day index. The function
    subtracts `ndays(time%mo)` from `id`, so `id` must already be a year-day count aligned
    with the current simulation month.'
locals:
  icl: '`icl` is the function result variable. It holds the converted day-of-month offset
    computed from `id` and the month-specific `ndays(time%mo)` value, and that value is returned
    to the caller.'
uses:
  time_module: '`time_module` provides the global `time` state, especially `time%mo`, which
    tells `icl` which month is currently active. Without that module state, the function could
    not choose the correct month index when subtracting from `id`.'
---

<!-- facts:header -->

`icl` converts a Julian day count into a day-of-month offset using the current simulation month. It is a small time helper that relies on `time_module` to decide which month-specific `ndays` entry to subtract.

## Bottom Line

`icl` takes the incoming day index `id` and subtracts the cumulative day count for the current month, returning the day position within that month rather than the year. In practice, it is a calendar conversion helper that depends on `time%mo` from `time_module` so the calculation uses the simulation's current month.

The code has an `if (time%mo .le. 2)` branch, but both branches do the same subtraction. That means the present behavior is identical for early-year and later months; the routine still matters because other code can call it for a month-relative day value.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`icl` runs as a simple calendar conversion utility during time handling. The current month value is prepared upstream in `time_module` before this function is used, and later model logic depends on the returned month-relative day value when it needs to work with dates by month instead of by year day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. test current month | Check whether the simulation month is in January or February by testing `time%mo .le. 2`. This branch exists in the source, although both paths currently use the same calculation. |
| 2. subtract month offset | Compute the function result as `id - ndays(time%mo)`. This converts the incoming Julian day into a day index relative to the current month by removing the cumulative days that occurred before that month. |
| 3. return result | Return the computed `icl` value to the caller and end the function. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%mo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits affected `icl.f90`. The initial addition commit, `df07e3f`, introduced the function and its current month-based subtraction logic. The later commit, `94b6dec`, preserved the same computation but added the explicit `end function icl` terminator and kept the documentation block/source structure in place.

- `df07e3f` added `icl.f90` with the current `id - ndays(time%mo)` calculation and the `time_module` dependency.
- `94b6dec` did not change the arithmetic, but it completed the function with an explicit `end function icl` line.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'icl' has no extracted documentation comment.
- algorithm_steps revised: condensed the no-op branch structure into a month check followed by a single subtraction step because both branches perform the same assignment in the source.
- The source comment says this routine determines the month and day given a Julian date, but the extracted logic only returns `id - ndays(time%mo)`; that is the behavior documented here.
