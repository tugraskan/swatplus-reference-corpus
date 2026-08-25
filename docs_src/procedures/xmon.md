---
kind: procedure
symbol: xmon
title: xmon
status: filled
source_hash: 2fadbb31071aa0cf
version_label: SWAT+ 62.0.0
args:
  jd: Input Julian day of year to convert. The routine scans month-end boundaries until it
    finds the month containing `jd`.
  mo: Returned month number corresponding to `jd`. xmon sets this when `jd` falls on or before
    the current month-end boundary.
  day_mo: Returned day-of-month within the resolved month. xmon computes it by subtracting
    the prior month boundary from `jd`.
locals:
  m1: Temporary index into `ndays` for the next month boundary; `m1 = i_mo + 1` lets the routine
    compare `jd` against the end of month `i_mo`.
  nda: Holds the Julian day for the last day of the current candidate month, read from `ndays(m1)`
    so the routine can test whether `jd` is inside that month.
  i_mo: Loop counter that iterates through months 1 through 12 while searching for the month
    that contains `jd`.
uses:
  time_module: The `time_module` provides the `ndays` month-boundary table that xmon uses
    to map a Julian day to month and day-of-month; without that shared calendar array, the
    conversion cannot be performed.
---

<!-- facts:header -->

Converts a Julian day-of-year into the corresponding month and day-of-month using leap-year month boundaries.

## Bottom Line

xmon is a date-conversion helper used throughout SWAT+ time setup and monthly aggregation. Given a Julian day (`jd`), it finds the matching month and computes the day within that month.

It matters because several routines need a consistent month/day breakdown before they can initialize calendar state or accumulate monthly statistics.

## Arguments

<!-- facts:arguments -->

## Where It Fits

xmon runs wherever SWAT+ needs to turn a day-of-year into calendar month/day values. Upstream callers such as `time_read` and `time_control` supply the starting day of simulation or time window, and later routines such as `cli_tmeas` and `plant_init` depend on the month result to aggregate monthly climate values or step through a year correctly.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. scan months | Loop through month numbers 1 to 12, preparing to test each month boundary against the input Julian day. |
| 2. load boundary | Fetch the Julian day for the end of the current month from `ndays(i_mo + 1)` and store it in `nda`. |
| 3. compare day | Check whether the input day has reached or passed the end of the current month; if so, this is the containing month. |
| 4. return month | Set `mo` to the current month number and compute `day_mo` as the offset from the previous month boundary, then return immediately. |
| 5. finish search | If no earlier return occurred, exit the loop and return control to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `ndays` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in 94b6dec as a new source file implementing Julian-day-to-month conversion with the `time_module` month-boundary table. In 39fabde, the local counters were initialized to zero (`m1`, `nda`, `i_mo`) but the algorithm and interface did not change.

- 94b6dec added the xmon subroutine and its month/day conversion logic using `ndays` from time_module.
- 39fabde changed only local variable initialization to zero for `m1`, `nda`, and `i_mo`; control flow and outputs stayed the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'xmon' has no extracted documentation comment.
