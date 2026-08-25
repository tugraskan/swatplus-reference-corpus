---
kind: procedure
symbol: basin_reservoir_output
title: basin_reservoir_output
status: filled
source_hash: 147271014e35b7fd
version_label: SWAT+ 62.0.0
locals:
  ires: Loop counter for reservoir objects. It starts at 0, is set by `do ires = 1, sp_ob%res`,
    and is reused in the output records as the reservoir index written for the current pass.
  const: Temporary scalar used to hold the number of days in the current month. It is set
    from `float (ndays(time%mo + 1) - ndays(time%mo))` and used to convert monthly reservoir
    water totals into an average before they are added to yearly totals and written.
uses:
  time_module: '`time_module` provides the simulation clock and end-of-period flags that control
    when each reporting block runs. The routine uses the current day, month, day-of-month,
    and year in every record, then checks `time%end_mo`, `time%end_yr`, `time%end_sim`, and
    `time%yrs_prt` to decide when to summarize monthly, yearly, and average-annual reservoir
    outputs.'
  basin_module: '`basin_module` supplies the basin print control settings and basin name used
    in the output rows. `pco` decides whether daily, monthly, yearly, and average-annual reservoir
    reports are enabled and whether CSV copies are also written, while `bsn%name` identifies
    the basin in each record.'
  reservoir_module: '`reservoir_module` is the source of the per-reservoir hydrologic totals
    that this routine aggregates. `res(ires)`, `res_in_d(ires)`, and `res_out_d(ires)` are
    summed into basin totals, and `resmz` is used as the zero-value initializer and reset
    value for those hydrologic accumulators.'
  hydrograph_module: '`hydrograph_module` matters because it owns the basin and reservoir
    hydrologic summary types that this routine updates. The routine accumulates `res`, `res_in_d`,
    `res_out_d`, `bres`, `bres_in_d`, `bres_out_d`, and the corresponding monthly, yearly,
    and average-annual summaries, and it uses `sp_ob%res` to know how many reservoir objects
    to process.'
  water_body_module: '`water_body_module` matters because it owns the basin and reservoir
    water-body summary types used for storage or water-state reporting. The routine accumulates
    `res_wat_d(ires)` into `bres_wat_d`, then propagates monthly, yearly, and average-annual
    water-body summaries through `bres_wat_m`, `bres_wat_y`, and `bres_wat_a`, with `wbodz`
    providing the zero/reset water-body state.'
---

<!-- facts:header -->

Aggregates reservoir water and flow outputs across all reservoirs, then writes daily, monthly, yearly, and average-annual basin reservoir reports. It also resets the period-specific reservoir accumulators after they are printed.

## Bottom Line

`basin_reservoir_output` is the basin-level reservoir reporting routine. It loops over every reservoir object, builds basin totals from the per-reservoir hydrology and water-body states, and then writes those totals to the configured daily, monthly, yearly, and average-annual output files when the matching print flags are enabled.

The routine matters because it is the place where reservoir outputs are summarized, period-averaged, and cleared for the next accumulation cycle. Later basin reporting depends on the totals it computes here, and the final average-annual values depend on `time%yrs_prt` and the end-of-simulation flag.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after the model has advanced the current time step and populated reservoir hydrology and water-body state arrays. `command` calls it when `sp_ob%res > 0`, and the outputs it writes are used by the basin reservoir reporting files for daily, monthly, yearly, and simulation-average summaries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize basin daily summary state | Reset the basin reservoir flow and water-body summary objects to zero-equivalent starting states before accumulating any reservoir contributions for the current step. |
| 2. Accumulate per-reservoir totals | Loop over every reservoir indexed by `sp_ob%res`, add each reservoir's flow and water-body values into the basin totals, and clear the per-reservoir daily inflow and outflow accumulators after they are counted. |
| 3. Roll daily totals into monthly totals | Add the daily basin inflow, outflow, and water-body totals into the monthly basin accumulators so they can be printed or later averaged at the end of the month. |
| 4. Write daily reservoir output when daily printing is enabled | If daily printing is active and the basin reservoir daily print code is enabled, write the daily basin reservoir record to unit 2100 and, when CSV output is enabled, write the same record to unit 2104. |
| 5. End-of-month averaging, yearly rollup, and monthly output | At the end of each month, compute the month length, roll monthly inflow and outflow into yearly totals, convert monthly water-body output to an average using the number of days in the month, write the monthly record if enabled, then reset the monthly basin accumulators. |
| 6. End-of-year averaging, annual rollup, and yearly output | At the end of each year, add yearly inflow and outflow to the average-annual accumulators, average yearly water-body output over 12 months, write the yearly record if enabled, then reset the yearly basin accumulators. |
| 7. Final average-annual output at simulation end | When the simulation ends and average-annual reservoir output is enabled, divide the accumulated annual inflow, outflow, and water-body totals by the number of printed years, write the average-annual record to unit 2103, and optionally write the CSV copy to unit 2107. |
| 8. Return to caller | Return after all requested reservoir summaries have been accumulated, written, and reset for the next period. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco, bsn` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%res_bsn%d, bsn%name, pco%csvout, pco%res_bsn%m, pco%res_bsn%y, pco%res_bsn%a` |
| [sym:reservoir_module] | `res, res_in_d, res_out_d, resmz` | `res, res_in_d, res_out_d, resmz` |
| [sym:hydrograph_module] | `sp_ob, res, res_in_d, res_out_d, bres, resmz, bres_in_d, bres_out_d, bres_in_m, bres_out_m, bres_in_y, bres_out_y, bres_in_a, bres_out_a` | `sp_ob%res` |
| [sym:water_body_module] | `res_wat_d, bres_wat_d, wbodz, bres_wat_m, bres_wat_y, bres_wat_a` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bres` | At routine start, before reservoir accumulation begins. | `bres` is cleared to the zero-equivalent hydrologic state `resmz`, so it can accumulate the basin-wide reservoir flow total for the current time step from all reservoirs. |
| `bres_in_d` | At routine start, before reservoir accumulation begins. | `bres_in_d` is reset to `resmz` so the routine can rebuild the basin daily reservoir inflow total from the individual `res_in_d(ires)` values. |
| `bres_out_d` | At routine start, before reservoir accumulation begins. | `bres_out_d` is reset to `resmz` so the routine can rebuild the basin daily reservoir outflow total from the individual `res_out_d(ires)` values. |
| `bres_wat_d` | At routine start, before reservoir accumulation begins. | `bres_wat_d` is initialized to `wbodz` so the basin daily water-body summary can be built from the per-reservoir `res_wat_d(ires)` values. |
| `res_in_d(ires)` | Inside the reservoir loop for each `ires` from 1 to `sp_ob%res`. | Each reservoir's daily inflow total is added into the basin daily inflow summary and then cleared back to `resmz` so the same daily contribution is not counted again later. |
| `res_out_d(ires)` | Inside the reservoir loop for each `ires` from 1 to `sp_ob%res`. | Each reservoir's daily outflow total is added into the basin daily outflow summary and then cleared back to `resmz` after it has been included in the basin total. |
| `bres_in_m` | At the end of the daily accumulation step, before any month-end reset. | The basin monthly inflow accumulator grows by the current day's basin inflow total so monthly output can report the month-to-date inflow. |
| `bres_out_m` | At the end of the daily accumulation step, before any month-end reset. | The basin monthly outflow accumulator grows by the current day's basin outflow total so monthly output can report the month-to-date outflow. |
| `bres_wat_m` | At the end of the daily accumulation step, before any month-end reset. | The basin monthly water-body accumulator grows by the current day's basin water-body summary so monthly output can report the month-to-date water state. |
| `bres_in_y` | At each end-of-month event (`time%end_mo == 1`). | The basin yearly inflow accumulator is incremented by the completed month's inflow total so the year-end report can sum all months in the year. |
| `bres_out_y` | At each end-of-month event (`time%end_mo == 1`). | The basin yearly outflow accumulator is incremented by the completed month's outflow total so the year-end report can sum all months in the year. |
| `bres_wat_y` | At each end-of-month event, after monthly water-body totals have been converted to a monthly mean. | The basin yearly water-body accumulator receives the month-averaged water-body value so yearly output reflects the average monthly reservoir state over the year. |
| `bres_in_a` | At each end-of-year event (`time%end_yr == 1`). | The average-annual inflow accumulator is increased by the completed year's inflow total so the final simulation-average report can be computed. |
| `bres_out_a` | At each end-of-year event (`time%end_yr == 1`). | The average-annual outflow accumulator is increased by the completed year's outflow total so the final simulation-average report can be computed. |
| `bres_wat_a` | At each end-of-year event, after yearly water-body totals have been converted to a yearly mean. | The average-annual water-body accumulator receives the year-mean water-body value so the final simulation-average reservoir report can be formed. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `basin_reservoir_output`: `df07e3f` introduced the routine with the current reservoir aggregation and output structure; `39fabde` initialized `ires` and `const` to zero values; `0d9bb63` temporarily removed the `pco%res_bsn%a` guard from the average-annual print block and `10e5ddc` did the same again after it had been restored; and `2fe89fd` changed the CSV writes for units 2104, 2105, 2106, and 2107 from `G0.3` to `G0.6` formatting.

- `df07e3f` added the reservoir basin aggregation loop, period rollups, print gating, resets, and all six output paths for daily, monthly, yearly, and average-annual reservoir summaries.
- `39fabde` changed the local initialization so `ires` starts at 0 and `const` starts at 0.0 instead of being uninitialized.
- `0d9bb63` removed the `pco%res_bsn%a` condition from the average-annual print block, causing the final average-annual output to run whenever `time%end_sim == 1`.
- `10e5ddc` again removed the `pco%res_bsn%a` condition from the average-annual print block, matching the same unconditional end-of-simulation behavior for that revision.
- `2fe89fd` increased the CSV numeric precision for reservoir output units 2104, 2105, 2106, and 2107 from `G0.3` to `G0.6` while leaving the formatted non-CSV writes unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_reservoir_output' has no extracted documentation comment.
- algorithm_steps revised: condensed the original four draft steps into eight source-backed steps to match the actual control flow and period-specific output/reset behavior.
- reservoir_module ownership is ambiguous in the extracted refs: the routine uses `res`, `res_in_d`, `res_out_d`, and `resmz`, which are listed under hydrograph_module in the resolved outside reference table, while reservoir_module had no candidate refs resolved.
