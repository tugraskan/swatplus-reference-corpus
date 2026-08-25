---
kind: procedure
symbol: wetland_output
title: wetland_output
status: filled
source_hash: 47e51504fb0e0b8b
version_label: SWAT+ 62.0.0
args:
  j: '`j` selects which wetland/HRU slot to report. The routine converts it to the corresponding
    object index with `iob = sp_ob1%hru + j - 1`, so every write uses the `j`th wetland state
    and the associated `ob(iob)` label fields.'
locals:
  const: '`const` is a scratch real used only in the monthly branch to hold the number of
    days in the current month (`float(ndays(time%mo + 1) - ndays(time%mo))`). It is then used
    as the divisor for monthly average flow values.'
  iob: '`iob` is the resolved object index for the current wetland/HRU entry. It lets the
    routine look up `ob(iob)%gis_id` and `ob(iob)%name` for output records.'
uses:
  time_module: '`time_module` provides the current day, month, year, end-of-month, end-of-year,
    and end-of-simulation flags that control when each output branch runs and what timestamps
    are written to the files.'
  basin_module: '`pco` supplies the print-control switches that gate daily, monthly, yearly,
    and average-annual reservoir-style reporting, plus the CSV-output toggle that causes the
    routine to emit the parallel comma-delimited records.'
  reservoir_module: '`reservoir_module` is imported here because the wetland output code uses
    reservoir-style print controls and output infrastructure patterns consistent with that
    module boundary, even though this source span does not directly reference a resolved reservoir
    symbol.'
  hydrograph_module: '`hydrograph_module` holds the wetland discharge and storage arrays being
    summarized, along with the object table used to tag each record. The routine reads and
    resets `wet_in_*`, `wet_out_*`, and `wet` data from that shared hydrologic state.'
  water_body_module: '`water_body_module` supplies the wetland water-body storage arrays and
    the `wbodz` scratch water-body value used to reset monthly and yearly accumulators after
    they are written.'
---

<!-- facts:header -->

Writes daily, monthly, yearly, and average-annual wetland summary output for one HRU-like wetland object. It records water volume plus inflow and outflow totals, and optionally emits CSV-formatted duplicates.

## Bottom Line

`wetland_output` is the wetland reporting routine for a single index `j`. It computes the wetland object index, checks the current print controls and simulation end flags, then writes wetland water balance summaries to the configured output units for daily, monthly, yearly, and average-annual reporting.

It also accumulates period totals in `wet_in_*`, `wet_out_*`, and `wet_wat_*`, resets period accumulators after each report interval, and normalizes some monthly or annual values before writing. The results feed the model's wetland output files rather than changing the hydrologic simulation itself.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine inside the HRU loop after `hru_output` and `hru_carbon_output`, and only when `hru(ihru)%dbs%surf_stor > 0`. That means upstream setup has already established the wetland-related hydrograph and water-body arrays, and downstream reporting depends on these writes to populate the wetland daily/monthly/yearly/average-annual output files.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Resolve the wetland object index | Compute `iob = sp_ob1%hru + j - 1` so the routine can label the record with the correct object connectivity entry for this wetland/HRU. |
| 2. Write daily wetland output when daily printing is enabled | If day printing is active and the daily interval matches, and reservoir daily output is enabled, write the daily wetland summary to unit 2548 and optionally the CSV version to unit 2552. |
| 3. Accumulate daily values into month totals and reset daily inflow/outflow | Add daily inflow, outflow, and water-body values to the monthly accumulators, then reset `wet_in_d(j)` and `wet_out_d(j)` to `resmz`; the daily water-body reset is commented out. |
| 4. On month end, compute month length and roll monthly totals into yearly accumulators | When `time%end_mo == 1`, compute the month length with `float(ndays(time%mo + 1) - ndays(time%mo))`, add monthly inflow and outflow to yearly totals, add monthly water storage to yearly storage, and normalize the monthly flow components by the month length. |
| 5. Write monthly wetland output when monthly printing is enabled | If monthly reservoir output is enabled, write the monthly wetland summary to unit 2549 and optionally the CSV version to unit 2553. |
| 6. Reset monthly accumulators after month-end reporting | Set monthly inflow and outflow back to `resmz` and monthly water storage back to `wbodz` so the next month starts from a clean accumulator state. |
| 7. On year end, roll yearly totals into average-annual accumulators | When `time%end_yr == 1`, add yearly inflow, outflow, and water storage into the average-annual accumulators. |
| 8. Write yearly wetland output when yearly printing is enabled | If yearly reservoir output is enabled, write the yearly wetland summary to unit 2550 and optionally the CSV version to unit 2554. |
| 9. Reset yearly accumulators after year-end reporting | Set yearly inflow and outflow back to `resmz` and yearly water storage back to `wbodz` so the next year starts with fresh accumulators. |
| 10. On simulation end, compute and write average-annual wetland output | When the simulation ends and average-annual output is enabled, divide accumulated inflow, outflow, and water storage by `time%yrs_prt`, then write the average-annual record to unit 2551 and optionally the CSV version to unit 2555. |
| 11. Return to caller | Exit the subroutine after all enabled output branches have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%res%d, pco%csvout, pco%res%m, pco%res%y, pco%res%a` |
| [sym:reservoir_module] | `reservoir_module state and types` | `not specifically referenced by any resolved outside symbol in this source span` |
| [sym:hydrograph_module] | `sp_ob1, ob, wet_in_m, wet_out_m, wet, wet_in_d, wet_out_d, wet_in_y, wet_out_y, wet_in_a, wet_out_a, resmz` | `sp_ob1%hru, ob(iob)%name, wet_in_m(j)%flo, wet_out_m(j)%flo` |
| [sym:water_body_module] | `wet_wat_d, wet_wat_m, wet_wat_y, wet_wat_a, wbodz` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet_in_m(j)` | When `pco%day_print == 'y' .and. pco%int_day_cur == pco%int_day`, inside the `pco%res%d == 'y'` daily branch | Adds the current day's wetland inflow to the monthly inflow accumulator before daily inflow is reset. |
| `wet_out_m(j)` | When `pco%day_print == 'y' .and. pco%int_day_cur == pco%int_day`, inside the `pco%res%d == 'y'` daily branch | Adds the current day's wetland outflow to the monthly outflow accumulator before daily outflow is reset. |
| `wet_wat_m(j)` | When `pco%day_print == 'y' .and. pco%int_day_cur == pco%int_day`, inside the `pco%res%d == 'y'` daily branch | Adds the current day's wetland water-body value to the monthly water-storage accumulator. |
| `wet_in_d(j)` | Always after the daily output branch runs | Resets daily inflow to `resmz` so the next day starts from the baseline water-object state. |
| `wet_out_d(j)` | Always after the daily output branch runs | Resets daily outflow to `resmz` so the next day starts from the baseline water-object state. |
| `wet_in_y(j)` | When `time%end_mo == 1` | Adds the completed month's inflow to the yearly inflow accumulator. |
| `wet_out_y(j)` | When `time%end_mo == 1` | Adds the completed month's outflow to the yearly outflow accumulator. |
| `wet_wat_y(j)` | When `time%end_mo == 1` | Adds the completed month's water-storage accumulator to the yearly water-storage total. |
| `wet_in_m(j)%flo` | When `time%end_mo == 1` | Divides the monthly inflow's `flo` component by the number of days in the month to make the monthly flow output an average rate. |
| `wet_out_m(j)%flo` | When `time%end_mo == 1` | Divides the monthly outflow's `flo` component by the number of days in the month to make the monthly flow output an average rate. |
| `wet_in_a(j)` | When `time%end_yr == 1` | Adds the finished year's inflow total to the average-annual inflow accumulator. |
| `wet_out_a(j)` | When `time%end_yr == 1` | Adds the finished year's outflow total to the average-annual outflow accumulator. |
| `wet_wat_a(j)` | When `time%end_yr == 1` | Adds the finished year's water-storage total to the average-annual water-storage accumulator. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage evidence shows five behavior-changing commits for `wetland_output`. The file was first adjusted in 39fabde to initialize `const` and `iob`. In 72206bc, `j` became an `intent(in)` argument and the monthly reset block stopped assigning wetland output state back to `resmz`/`wbodz`. In c5ed7bb, the yearly-reset and average-annual logic was changed so `wet_in_y`, `wet_out_y`, and `wet_wat_y` are restored after year-end reporting and average-annual totals are computed from `wet_in_a` and `wet_out_a` instead of the yearly values. In 85aa04e, the commented-out monthly normalization of yearly flow values replaced active division. In 2fe89fd, the CSV write format changed from `G0.3` to `G0.6` for all CSV output units.

- 39fabde initialized `const` and `iob` in the subroutine, establishing zeroed starting state for the scratch constant and object index.
- 72206bc changed `j` to an intent(in) argument and removed the monthly reset of wetland output state to `resmz`/`wbodz`, altering how the routine preserves monthly values after reporting.
- c5ed7bb restored yearly-state resets after output and switched average-annual accumulation to divide `wet_in_a` and `wet_out_a` by `time%yrs_prt`, changing how end-of-simulation averages are computed.
- 85aa04e stopped dividing `wet_in_y%flo` and `wet_out_y%flo` by 12 at year-end by commenting those lines out, leaving the yearly flow components unnormalized there.
- 2fe89fd increased CSV numeric precision for all wetland CSV outputs from `G0.3` to `G0.6`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wetland_output' has no extracted documentation comment.
- algorithm_steps revised: reordered steps to match the source flow and split the month-end/year-end/average-annual branches into distinct algorithm steps.
