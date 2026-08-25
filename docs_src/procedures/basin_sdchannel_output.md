---
kind: procedure
symbol: basin_sdchannel_output
title: basin_sdchannel_output
status: filled
source_hash: 61cd95cf9f5250ee
version_label: SWAT+ 62.0.0
locals:
  ichan: Loop counter over the swat-deg channel objects; it indexes `ch_stor`, `ch_in_d`,
    `ch_out_d`, and `ch_wat_d` while the routine sums basin totals.
  const: Temporary divisor used to convert accumulated monthly or yearly water-body totals
    into daily averages before writing the period report.
uses:
  time_module: The `time_module` controls when each output block runs. `time%day`, `time%mo`,
    `time%day_mo`, and `time%yrc` provide the date fields written to each record, while `time%end_mo`,
    `time%end_yr`, `time%end_sim`, `time%day_end_yr`, and `time%yrs_prt` decide when month-end,
    year-end, and average-annual summaries should be produced and how the annual average is
    normalized.
  basin_module: The `basin_module` supplies the basin print switches and basin label used
    to gate and tag the output. `pco%day_print`, `pco%int_day_cur`, and `pco%int_day` control
    whether daily printing is active, `pco%sd_chan_bsn%d/%m/%y/%a` choose the output periods,
    `pco%csvout` enables the CSV companion files, and `bsn%name` is written into each record
    as the basin identifier.
  hydrograph_module: The `hydrograph_module` provides the channel-degradation counts and the
    basin-level hydrograph accumulators this routine updates. `sp_ob%chandeg` sets the loop
    bound, `ch_stor`, `ch_in_d`, `ch_out_d`, and `ch_wat_d` are the per-object daily values
    being summed, and `bch_stor_d`, `bch_in_d`, `bch_out_d`, `bch_in_m`, `bch_out_m`, `bch_in_y`,
    `bch_out_y`, `bch_in_a`, and `bch_out_a` are the basin summary states that receive the
    results.
  water_body_module: The `water_body_module` supplies the basin water-body accumulators used
    alongside the hydrograph totals. `wbodz` seeds the basin water-body summaries, `ch_wat_d`
    provides the per-channel daily water-body contribution, and `bch_wat_d`, `bch_wat_m`,
    `bch_wat_y`, and `bch_wat_a` hold the basin-level totals or averages written by this routine.
---

<!-- facts:header -->

Aggregates swat-deg channel outputs for the basin and writes daily, monthly, yearly, and average annual reports. It also produces optional CSV versions of those reports when configured.

## Bottom Line

This subroutine totals the swat-deg channel results across all channel-degradation objects (`sp_ob%chandeg`) and stores basin-level summaries in `bch_stor_*`, `bch_in_*`, `bch_out_*`, and `bch_wat_*` variables. Those summaries are then written to the basin channel output files for the active print intervals.

The routine matters because it is the basin-level reporting step for swat-deg channels: it uses the current simulation time and print controls to decide whether to emit daily, monthly, yearly, or end-of-simulation averages, and it resets the month/year accumulators after writing period totals.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `command` after the model has computed basin and channel-degradation results for the current time step, and only when `sp_ob%chandeg > 0`. It runs during the output phase to collect basin totals and emit period reports; later reporting depends on the accumulators it updates and resets, especially the monthly and yearly basin channel-water summaries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize basin daily summaries. | The routine zeroes or seeds the basin daily storage and flow summaries from `chaz`, and seeds basin water-body daily output from `wbodz` before any channel totals are added. |
| 2. Sum all swat-deg channel objects. | It loops from `1` to `sp_ob%chandeg` and adds each channel object's storage, inflow, outflow, and water-body contribution into the basin daily totals. |
| 3. Accumulate daily totals into month totals. | The daily inflow, outflow, and water-body values are added into the month-running basin accumulators so they can later be written at month end. |
| 4. Write daily basin output when daily printing is active. | If daily printing is enabled and the swat-deg daily interval is requested, the routine writes the basin daily channel report to unit 4900 and optionally writes the CSV version to unit 4904. |
| 5. Roll monthly totals into yearly totals and compute monthly averages. | At month end, the routine adds the monthly basin totals into the yearly accumulators, computes the month length with `ndays`, and divides the monthly water total by that length to produce a daily average value. |
| 6. Write monthly basin output when monthly printing is active. | If monthly swat-deg output is enabled, the routine writes the monthly report to unit 4901 and optionally to the CSV unit 4905. |
| 7. Reset month accumulators after month-end reporting. | After the monthly report is written, the routine clears the monthly inflow, outflow, and water-body accumulators back to their zero states for the next month. |
| 8. Roll yearly totals into annual totals and compute yearly averages. | At year end, the routine adds yearly basin totals into the average-annual accumulators, sets the divisor from `time%day_end_yr`, and converts yearly water total to a daily average. |
| 9. Write yearly basin output when yearly printing is active. | If yearly swat-deg output is enabled, the routine writes the yearly report to unit 4902 and optionally to the CSV unit 4906. |
| 10. Reset year accumulators after year-end reporting. | After the yearly report is written, the routine clears the yearly inflow, outflow, and water-body accumulators back to their zero states for the next year. |
| 11. Normalize and write average-annual basin output at simulation end. | At the end of the simulation, if average-annual output is enabled, the routine divides the accumulated totals by `time%yrs_prt` and writes the basin average-annual report to unit 4903 and optionally to unit 4907. |
| 12. Return to caller. | The routine ends after the reporting logic is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco, bsn` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%sd_chan_bsn%d, bsn%name, pco%csvout, pco%sd_chan_bsn%m, pco%sd_chan_bsn%y, pco%sd_chan_bsn%a` |
| [sym:hydrograph_module] | `sp_ob, ch_stor, ch_in_d, ch_out_d, bch_stor_d, chaz, bch_in_d, bch_out_d, bch_in_m, bch_out_m, bch_in_y, bch_out_y, bch_in_a, bch_out_a` | `sp_ob%chandeg` |
| [sym:water_body_module] | `ch_wat_d, bch_wat_d, wbodz, bch_wat_m, bch_wat_y, bch_wat_a` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bch_stor_d` | At the start of the routine, before the channel loop. | `bch_stor_d` is initialized from `chaz` and then increased by each `ch_stor(ichan)` value, so it becomes the basin daily channel-storage summary for the current time step. |
| `bch_in_d` | At the start of the routine, before the channel loop. | `bch_in_d` is initialized from `chaz` and then increased by each `ch_in_d(ichan)` value, so it becomes the basin daily inflow summary for the current time step. |
| `bch_out_d` | At the start of the routine, before the channel loop. | `bch_out_d` is initialized from `chaz` and then increased by each `ch_out_d(ichan)` value, so it becomes the basin daily outflow summary for the current time step. |
| `bch_wat_d` | At the start of the routine, before the channel loop. | `bch_wat_d` is initialized from `wbodz` and then increased by each `ch_wat_d(ichan)` value, so it becomes the basin daily water-body summary for the current time step. |
| `bch_in_m` | Every time the routine runs, after daily totals are computed. | `bch_in_m` is incremented by the current daily inflow total so the routine can accumulate monthly inflow before the month-end report. |
| `bch_out_m` | Every time the routine runs, after daily totals are computed. | `bch_out_m` is incremented by the current daily outflow total so the routine can accumulate monthly outflow before the month-end report. |
| `bch_wat_m` | Every time the routine runs, after daily totals are computed. | `bch_wat_m` is incremented by the current daily water-body total so the routine can accumulate monthly water totals before the month-end report. |
| `bch_in_y` | When `time%end_mo == 1`. | `bch_in_y` is increased by the finished monthly inflow total, carrying monthly inflow forward into the yearly accumulator. |
| `bch_out_y` | When `time%end_mo == 1`. | `bch_out_y` is increased by the finished monthly outflow total, carrying monthly outflow forward into the yearly accumulator. |
| `bch_wat_y` | When `time%end_mo == 1`. | `bch_wat_y` is increased by the finished monthly water-body total, carrying monthly water totals forward into the yearly accumulator. |
| `bch_in_a` | When `time%end_yr == 1`. | `bch_in_a` is increased by the yearly inflow total so the routine can build the average-annual inflow across all printed years. |
| `bch_out_a` | When `time%end_yr == 1`. | `bch_out_a` is increased by the yearly outflow total so the routine can build the average-annual outflow across all printed years. |
| `bch_wat_a` | When `time%end_yr == 1`. | `bch_wat_a` is increased by the yearly water-body total so the routine can build the average-annual water summary across all printed years. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved five commits. The procedure was added in df07e3f with daily, monthly, yearly, and average-annual basin swat-deg channel reporting. 39fabde initialized `ichan` and `const` to zero. d70017a commented out `use channel_module`, leaving the routine to rely on the other imported modules. 2fe89fd changed the CSV writes from `G0.3` to `G0.6` for the daily, monthly, yearly, and average-annual CSV outputs.

- df07e3f introduced the routine and its reporting logic: summing channel-degradation outputs, using time/print controls, writing units 4900-4907, and resetting monthly and yearly accumulators.
- 39fabde changed local initialization by setting `ichan = 0` and `const = 0.` at declaration time.
- d70017a removed the active `channel_module` import by commenting it out, but did not change the routine's output algorithm.
- 2fe89fd increased CSV numeric formatting precision from `G0.3` to `G0.6` in the four CSV output writes.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_sdchannel_output' has no extracted documentation comment.
