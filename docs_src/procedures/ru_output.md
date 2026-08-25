---
kind: procedure
symbol: ru_output
title: ru_output
status: filled
source_hash: 394e487e78ff2164
version_label: SWAT+ 62.0.0
args:
  iru: Selects which routing unit in the RU object block this call should report; the routine
    maps `iru` to the global object index `iob = sp_ob1%ru + iru - 1` and then uses that unit's
    `ru_d`, `ru_m`, `ru_y`, and `ru_a` entries.
locals:
  iob: Holds the absolute object index for the routing unit being printed. It starts at 0,
    then is set from `sp_ob1%ru + iru - 1` so the routine can look up `ob(iob)%name` and `ob(iob)%typ`
    for output labels.
uses:
  time_module: The `time` state determines when each reporting branch fires and supplies the
    day, month, year, and end-of-period flags written to every record. `time%yrs_prt` is also
    needed to compute the average annual value at simulation end.
  basin_module: The `pco` print-control flags decide whether daily, monthly, yearly, and average-annual
    RU output should be written at all, and whether CSV companion records are emitted for
    each interval.
  hydrograph_module: The hydrograph state provides the routing-unit output arrays being accumulated
    and written, plus the object connectivity table used to attach each record to the correct
    RU name and type.
---

<!-- facts:header -->

Writes routing-unit output for daily, monthly, yearly, and average-annual print schedules. It reports the current routing unit state using the object labels and time fields selected by the model print controls.

## Bottom Line

ru_output writes the routing-unit hydrologic summary for one RU index `iru`. It uses the current simulation time, object connectivity labels, and basin print codes to decide whether to emit daily, monthly, yearly, and end-of-simulation average-annual records.

The routine also rolls the cumulative routing-unit totals forward: daily values are accumulated into monthly totals, monthly totals into yearly totals, and yearly totals into the average-annual total before the values are reset for the next reporting interval.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from the main `command` loop after upstream code has already advanced time, set the print flags in `pco`, and populated the RU hydrograph outputs. Its writes feed the routing-unit report files that later analysis and postprocessing depend on, especially the daily, monthly, yearly, and average-annual RU summaries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Resolve the routing-unit object index | The routine declares `iob`, initializes it to 0, and maps the input RU index `iru` to the absolute object index with `iob = sp_ob1%ru + iru - 1` so later writes can use the correct object name and type. |
| 2. Accumulate the current day into the monthly total | Before any printing tests, the routine adds the current daily RU output `ru_d(iru)` into the running monthly accumulator `ru_m(iru)`. |
| 3. Write daily RU output when daily printing is enabled | If daily printing is active for the current day interval and RU daily output is enabled, the routine writes a daily record to unit 2600 and, when CSV output is requested, a comma-separated copy to unit 2604. |
| 4. Roll monthly totals into the yearly accumulator and reset monthly state | At end of month, the routine adds `ru_m(iru)` into `ru_y(iru)`, writes monthly output to unit 2601 and optional CSV unit 2605 when monthly RU output is enabled, then resets `ru_m(iru)` to `hz` for the next month. |
| 5. Roll yearly totals into the average-annual accumulator and reset yearly state | At end of year, the routine adds `ru_y(iru)` into `ru_a(iru)`, writes yearly output to unit 2602 and optional CSV unit 2606 when yearly RU output is enabled, then resets `ru_y(iru)` to `hz` for the next year. |
| 6. Compute and write the final average-annual RU value | At simulation end, if average-annual RU output is enabled, the routine divides `ru_a(iru)` by `time%yrs_prt` to form the average annual value and writes it to unit 2603 and optional CSV unit 2607. |
| 7. Return to the caller | The routine exits after all requested output records and state roll-ups have been completed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%ru%d, pco%csvout, pco%ru%m, pco%ru%y, pco%ru%a` |
| [sym:hydrograph_module] | `sp_ob1, ob, ru_m, ru_d, ru_y, ru_a, hz` | `sp_ob1%ru, ob(iob)%name, ob(iob)%typ` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ru_m(iru)` | When the routine starts, before any output-condition tests, it executes `ru_m(iru) = ru_m(iru) + ru_d(iru)`. | `ru_m(iru)` is the running monthly sum of daily RU output. Each call adds the current day's `ru_d(iru)` so that, at month end, the routine can write the monthly total and then reset the accumulator. |
| `ru_y(iru)` | When `time%end_mo == 1`, after `ru_y(iru) = ru_y(iru) + ru_m(iru)` has executed. | `ru_y(iru)` stores the running yearly sum of monthly RU totals. It is incremented at each month end so the year-end output can report the accumulated annual total before the yearly accumulator is cleared. |
| `ru_a(iru)` | When `time%end_yr == 1`, after `ru_a(iru) = ru_a(iru) + ru_y(iru)` has executed, and again at `time%end_sim == 1` when `ru_a(iru)` is divided by `time%yrs_prt`. | `ru_a(iru)` accumulates yearly RU totals across the simulation and then becomes the average annual value at the end of the run. It is the basis for the final average-annual RU printout. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four behavior-changing commits plus one formatting-only cleanup. The routine was introduced in df07e3f, iob was initialized in 39fabde, CSV writes were changed from G0.3 to G0.6 in 2fe89fd, and bd18ad4 added external declarations for soil carbon/nutrient write routines that are not used elsewhere in the shown source. dab22e1 only commented out unused format labels.

- df07e3f added the full ru_output routine with its daily, monthly, yearly, and average-annual printing branches and the ru_m/ru_y/ru_a roll-up logic.
- 39fabde changed `iob` from an uninitialized local to `integer :: iob = 0`, making the object-index variable explicitly initialized before assignment.
- 2fe89fd increased the CSV output precision for units 2604, 2605, 2606, and 2607 from `G0.3` to `G0.6` without changing the record content.
- bd18ad4 added `external :: soil_carbvar_write, soil_nutcarb_write` declarations near the top of the procedure; the visible control flow and output branches were otherwise unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ru_output' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into seven source-backed steps to match the actual control flow and state roll-up in ru_output.
- Source shows external declarations for soil_carbvar_write and soil_nutcarb_write, but no calls to them were extracted in this routine.
