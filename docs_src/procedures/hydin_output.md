---
kind: procedure
symbol: hydin_output
title: hydin_output
status: filled
source_hash: 31cb9aad3d8d3b4b
version_label: SWAT+ 62.0.0
locals:
  iin: '`iin` is the inner-loop counter over the receiving hydrograph slots for the current
    object `icmd`. It indexes the per-input arrays such as `ob(icmd)%hin_d(iin)`, `ob(icmd)%hin_m(iin)`,
    `ob(icmd)%hin_y(iin)`, and `ob(icmd)%hin_a(iin)` so the routine can process each incoming
    hydrograph separately.'
uses:
  hydrograph_module: '`hydrograph_module` supplies the object list and all hydrograph storage
    that this routine updates and prints. `sp_ob%objs` and `ob(icmd)%rcv_tot` define the nested
    loop bounds, while `ob(icmd)%name`, `typ`, inlet descriptors, and `hin_d/m/y/a` hold the
    labels and accumulators written to the hydin output files.'
  time_module: '`time_module` provides the simulation clock and end-of-period flags that gate
    each print branch. The day, month, year, and simulation-ending fields are written into
    every record and determine whether daily, monthly, yearly, or average-annual output should
    occur.'
  basin_module: '`basin_module` contains the print-control switches that enable or suppress
    each hydin output stream. `pco%day_print`, `pco%int_day_cur`, and `pco%int_day` control
    daily output timing, `pco%hyd%d/m/y/a` control which hydin files are active, and `pco%csvout`
    selects whether matching CSV rows are also written.'
---

<!-- facts:header -->

Writes hydrograph input summaries for every receiving object at daily, monthly, yearly, and average-annual endpoints. It updates the running month, year, and simulation-average accumulators in `ob(icmd)%hin_*` while emitting plain-text and optional CSV records.

## Bottom Line

`hydin_output` walks every spatial object and each of its receiving hydrograph slots, then reports hydrologic inflow totals at the output intervals enabled in `pco%hyd` and `pco%csvout`. The routine does not take arguments; it relies on shared simulation state from `hydrograph_module`, `time_module`, and `basin_module` to decide when to print and which accumulation bucket to update.

Its main job is bookkeeping: daily inflow is added into the monthly bucket, monthly inflow is rolled into the yearly bucket, yearly inflow is rolled into the simulation-average bucket, and the daily/monthly/yearly buckets are reset to the zero-value `hz` after they are transferred upward. The result is a set of synchronized hydin output files that match the current simulation clock and print settings.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hydin_output` runs from `command` after the model has finished the other scheduled output calls for the current time step. `command` has already established the active spatial-object counts, print settings, and current `time` values, and the results here feed the hydin output files that document daily through average-annual inflows for later analysis.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over spatial objects and receiving inflows | Iterate over every object in `sp_ob%objs`, then over each receiving hydrograph slot `1..ob(icmd)%rcv_tot` for that object. |
| 2. Emit daily hydin output when daily printing is active | If daily printing is enabled (`pco%day_print == 'y'` and `pco%int_day_cur == pco%int_day`), write the daily inflow record to unit 2560 when `pco%hyd%d == 'y'`, and write the matching CSV row to unit 2564 when `pco%csvout == 'y'`. |
| 3. Roll daily inflow into the monthly accumulator and reset daily storage | Add the current daily inflow `ob(icmd)%hin_d(iin)` into `ob(icmd)%hin_m(iin)`, then clear the daily bucket by assigning `hz` to `ob(icmd)%hin_d(iin)`. |
| 4. Emit monthly hydin output at month end | When `time%end_mo == 1`, write the monthly summary to unit 2561 if `pco%hyd%m == 'y'`, optionally write the CSV row to unit 2565, then add the monthly total into `ob(icmd)%hin_y(iin)` and reset the monthly bucket to `hz`. |
| 5. Roll monthly inflow into the yearly accumulator and reset monthly storage | Transfer the finished monthly total into `ob(icmd)%hin_y(iin)` and clear `ob(icmd)%hin_m(iin)` so the next month starts from zero. |
| 6. Emit yearly hydin output at year end | When `time%end_yr == 1`, write the yearly summary to unit 2562 if `pco%hyd%y == 'y'`, optionally write the CSV row to unit 2566, then add the yearly total into `ob(icmd)%hin_a(iin)` and reset the yearly bucket to `hz`. |
| 7. Roll yearly inflow into the average-annual accumulator and reset yearly storage | Transfer the finished yearly total into `ob(icmd)%hin_a(iin)` and clear `ob(icmd)%hin_y(iin)` so later years do not double-count the completed year. |
| 8. Emit average-annual hydin output at simulation end | When `time%end_sim == 1` and average-annual hydin output is enabled (`pco%hyd%a == 'y'`), divide `ob(icmd)%hin_a(iin)` by `time%yrs_prt`, then write the result to unit 2563 and optionally to CSV unit 2567. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, ob, icmd, hz` | `sp_ob%objs, ob(icmd)%rcv_tot, ob(icmd)%name, ob(icmd)%typ, ob(icmd)%obtyp_in(iin), ob(icmd)%obtypno_in(iin), ob(icmd)%htyp_in(iin), ob(icmd)%frac_in(iin), ob(icmd)%hin_d(iin), ob(icmd)%hin_m(iin), ob(icmd)%hin_y(iin), ob(icmd)%num, ob(icmd)%hin_a(iin)` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%hyd%d, pco%csvout, pco%hyd%m, pco%hyd%y, pco%hyd%a` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ob(icmd)%hin_m(iin)` | When `time%end_sim == 1` and `pco%hyd%a == 'y'`. | `ob(icmd)%hin_m(iin)` is not changed in the average-annual block itself; it is reset earlier at month end. The relevant annual state change for this routine is that the accumulated average-annual total is finalized by dividing `ob(icmd)%hin_a(iin)` by `time%yrs_prt`, so the monthly bucket is already zeroed by the time average-annual output is written. |
| `ob(icmd)%hin_d(iin)` | When daily output logic runs, regardless of whether daily printing is enabled; the reset follows `ob(icmd)%hin_m(iin) = ob(icmd)%hin_m(iin) + ob(icmd)%hin_d(iin)`. | The daily inflow value is transferred into the monthly accumulator and then cleared to `hz`, so the same daily amount is not counted again on the next step. |
| `ob(icmd)%hin_y(iin)` | When `time%end_mo == 1` after the monthly output record is written or skipped. | The current month total is added into the yearly accumulator and then `ob(icmd)%hin_m(iin)` is reset to `hz`, closing the month and starting the next one at zero. |
| `ob(icmd)%hin_a(iin)` | When `time%end_yr == 1` after the yearly output record is written or skipped. | The current year total is added into the simulation-average accumulator and then `ob(icmd)%hin_y(iin)` is reset to `hz`, so the next year begins with a clean yearly bucket. |

## File I/O

<!-- facts:io -->


## Lineage

`hydin_output` was introduced in `df07e3f` with daily, monthly, yearly, and average-annual hydin output logic plus the `hz`-based resets between accumulation levels. `39fabde` initialized the local loop counter `iin` to 0. `2fe89fd` changed the CSV formatting on units 2564, 2565, 2566, and 2567 from `G0.3` to `G0.6`, increasing numeric precision in the CSV outputs.

- df07e3f added the full subroutine and its day/month/year/average-annual accumulation-and-print workflow.
- 39fabde changed only the local declaration by initializing `iin` to zero.
- 2fe89fd increased CSV output precision on the four hydin CSV units from `G0.3` to `G0.6`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hydin_output' has no extracted documentation comment.
