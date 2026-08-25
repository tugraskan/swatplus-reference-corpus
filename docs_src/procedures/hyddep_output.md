---
kind: procedure
symbol: hyddep_output
title: hyddep_output
status: filled
source_hash: de233810cd05bea8
version_label: SWAT+ 62.0.0
uses:
  hydrograph_module: This module supplies the current command object (`ob(icmd)`) and the
    hyd output structures (`ht1`, `hz`) that the routine reads and updates. `ob(icmd)%name`
    and `%typ` are written as record labels, while `ob(icmd)%hdep_m`, `%hdep_y`, and `%hdep_a`
    are the accumulation targets that hold the period totals being reported.
  time_module: This module provides the current simulation date and end-of-period flags that
    control when each report fires. `time%day`, `%mo`, `%day_mo`, and `%yrc` are written into
    every record, while `time%end_mo`, `%end_yr`, `%end_sim`, and `%yrs_prt` determine monthly,
    yearly, and final average-annual rollover behavior.
  basin_module: This module holds the print-control switches that gate every output branch.
    `pco%day_print` and `pco%int_day_cur == pco%int_day` decide whether the daily branch is
    eligible, `pco%hyd%d`, `%m`, `%y`, `%a` enable the respective hydro output periods, and
    `pco%csvout` adds the CSV-formatted duplicate writes.
---

<!-- facts:header -->

Writes hydrograph-dependent depth output for daily, monthly, yearly, and average-annual reporting. It also accumulates daily values into monthly, yearly, and simulation-average totals for the current object.

## Bottom Line

hyddep_output is the hydrograph depth reporting routine. It writes the current daily hyd value `ht1` and the running depth accumulators `ob(icmd)%hdep_m`, `ob(icmd)%hdep_y`, and `ob(icmd)%hdep_a` to the hydro output streams when the matching print flags are enabled.

The routine also rolls values forward across periods: daily `ht1` is added into the monthly sum, the monthly sum is added into the yearly sum at month end, and the yearly sum is added into the average-annual sum at year end. At the end of the simulation, it divides the accumulated average-annual total by `time%yrs_prt` before writing the final result.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after the selected object has been identified as a hyd-capable command and `ob(icmd)%rcv_tot > 0`. `command` and the object-control routines prepare `icmd`, `ob(icmd)`, `ht1`, and the time/print-control state before this call. Its outputs feed the hydro reporting files for daily, monthly, yearly, and average-annual summaries, and its accumulator updates are what make the later period-end reports possible.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether daily hyd printing is active for the current day. | The routine first requires `pco%day_print == 'y'` and `pco%int_day_cur == pco%int_day`. If those conditions are met, it then checks whether daily hyd output is enabled with `pco%hyd%d == 'y'`. |
| 2. Write the daily hyd record when enabled. | When the daily branch is active, the routine writes the current date, object name, object type, and `ht1` to unit 2700, and optionally writes the same record to unit 2704 if CSV output is enabled. |
| 3. Add the daily hyd value into the monthly accumulator. | After the daily write, the routine adds `ht1` into `ob(icmd)%hdep_m` so the monthly total keeps accumulating through the month. |
| 4. At month end, write the monthly summary if monthly hyd output is enabled. | When `time%end_mo == 1`, the routine checks `pco%hyd%m == 'y'` and writes the month-end summary using `ob(icmd)%hdep_m` to unit 2701, with a CSV duplicate to unit 2705 when requested. |
| 5. Roll the monthly total into the yearly accumulator and clear the monthly accumulator. | Still inside the month-end block, the routine adds `ob(icmd)%hdep_m` to `ob(icmd)%hdep_y` and then resets `ob(icmd)%hdep_m` to `hz` for the next month. |
| 6. At year end, write the yearly summary if yearly hyd output is enabled. | When `time%end_yr == 1`, the routine checks `pco%hyd%y == 'y'` and writes the year-end summary using `ob(icmd)%hdep_y` to unit 2702, with a CSV duplicate to unit 2706 when requested. |
| 7. Roll the yearly total into the average-annual accumulator and clear the yearly accumulator. | After the year-end write path, the routine adds `ob(icmd)%hdep_y` to `ob(icmd)%hdep_a` and then resets `ob(icmd)%hdep_y` to `hz` for the next year. |
| 8. At simulation end, compute and write the average-annual summary if enabled. | When `time%end_sim == 1` and `pco%hyd%a == 'y'`, the routine divides `ob(icmd)%hdep_a` by `time%yrs_prt` and writes the final average-annual record to unit 2703, with a CSV duplicate to unit 2707 when requested. |
| 9. Return to the caller. | The routine ends without calling any other procedures. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ob, icmd, ht1, hz` | `ob(icmd)%name, ob(icmd)%typ, ob(icmd)%hdep_m, ob(icmd)%hdep_y, ob(icmd)%hdep_a` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%hyd%d, pco%csvout, pco%hyd%m, pco%hyd%y, pco%hyd%a` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ob(icmd)%hdep_m` | After every daily output branch, before month-end processing. | `ob(icmd)%hdep_m` is incremented by `ht1` each time the routine runs so the current month's depth output accumulates from daily values until it is written at month end. |
| `ob(icmd)%hdep_y` | When `time%end_mo == 1`, after the optional monthly write. | `ob(icmd)%hdep_y` is increased by the finished monthly total `ob(icmd)%hdep_m` so yearly accumulation includes all months in the year. |
| `ob(icmd)%hdep_a` | When `time%end_yr == 1`, after the optional yearly write. | `ob(icmd)%hdep_a` is increased by the finished yearly total `ob(icmd)%hdep_y` so the simulation-average total can be formed at the end of the run. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `hyddep_output`. df07e3f introduced the routine with daily, monthly, yearly, and average-annual output branches and the accumulator resets. 94b6dec preserved that logic while importing the source into the repository and keeping the same record structure. 2fe89fd changed only the CSV write format descriptors from `G0.3` to `G0.6` on the CSV output units 2704, 2705, 2706, and 2707.

- df07e3f added `hyddep_output` as a new subroutine that writes hyd depth outputs at daily, monthly, yearly, and simulation-average time steps and maintains `hdep_m`, `hdep_y`, and `hdep_a` rollups.
- 94b6dec brought the same procedure into the current source tree with the established output and accumulator behavior unchanged.
- 2fe89fd increased CSV numeric precision for the hyd depth CSV writes on units 2704, 2705, 2706, and 2707 by switching the format descriptor from `G0.3` to `G0.6`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hyddep_output' has no extracted documentation comment.
