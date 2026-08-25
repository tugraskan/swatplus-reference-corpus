---
kind: procedure
symbol: jdt
title: jdt
status: filled
source_hash: baebdcd9b0fb9785
version_label: SWAT+ 62.0.0
args:
  numdays: Month-end day totals used to translate a month/day pair into a Julian day-of-year.
    The array must already be prepared for leap-year day counts, because the function uses
    those values directly.
  i: The month selector. If it is zero, the function leaves the result at 0; otherwise it
    chooses the month-specific offset from numdays.
  m: The day-of-month to add onto the month offset when forming the Julian day-of-year.
locals:
  jdt: jdt is the function result. It is initialized to 0 and then overwritten with the computed
    Julian day-of-year when the month input is nonzero.
uses:
  time_module: time_module is used so this date helper can participate in the model's time-handling
    context, but no specific imported symbol was resolved from that module in the extracted
    evidence.
---

<!-- facts:header -->

Returns the Julian day-of-year for a given month and day. It uses a month-end day table so management schedules can convert calendar dates into SWAT+ day numbers.

## Bottom Line

jdt is a small date-conversion function. Given a month, day, and a 13-element table of cumulative day counts, it returns the Julian day-of-year for that calendar date.

It matters because management operations store month and day separately, and downstream scheduling logic needs a single day-of-year value to compare against the simulation calendar.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs while management operations are being read and indexed. read_mgtops prepares the operation day and month values, calls jdt to convert them to a Julian day, and stores the result in each schedule operation record so later scheduling logic can match operations to the simulation calendar.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize result | Set the function result to 0 before any date logic runs, so the default outcome is a zero Julian day when the month is not valid or is left at 0. |
| 2. check for nonzero month | Only compute a Julian day when the month input is nonzero. A zero month bypasses the date conversion and leaves the default result unchanged. |
| 3. compute Jan-Feb day-of-year | For January or February, add the day-of-month directly to the month-end table entry numdays(m) to form the Julian day-of-year. |
| 4. compute Mar-Dec day-of-year | For March through December, subtract 1 from the month-end table entry before adding the day-of-month, which shifts the result to the correct Julian day numbering after February. |
| 5. return result | Return the computed Julian day-of-year to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `module use only; no imported module variables or types were extracted` | `[]` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed revisions were resolved. The initial commit df07e3f added jdt.f90 with the month/day to Julian-day conversion logic and the time_module use statement. Commit 94b6dec preserved that logic and only reformatted the source block in the diff shown; no behavioral change is visible in the resolved diff.

- df07e3f introduced the jdt function and its month/day to Julian day-of-year conversion rules, including the zero-month guard and the January-February versus March-December offset handling.
- 94b6dec shows no behavioral change in the resolved diff for jdt; the function body and conversion logic remain the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'jdt' has no extracted documentation comment.
