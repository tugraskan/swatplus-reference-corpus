---
kind: procedure
symbol: sd_channel_output
title: sd_channel_output
status: filled
source_hash: 68fbcb984ca2cd32
version_label: SWAT+ 62.0.0
args:
  ichan: Channel index to summarize and print. The routine uses `ichan` to select the channel's
    daily, monthly, yearly, and average-annual accumulators and to map to the corresponding
    object record through `sp_ob1%chandeg + ichan - 1`.
locals:
  iob: Derived object index for the channel in `ob`; initialized from `sp_ob1%chandeg + ichan
    - 1` so the routine can fetch the correct object name, GIS id, and hydrograph data.
  ii: Loop counter over subdaily time steps when writing the detailed hydrograph output to
    unit 2508.
  const: Temporary divisor used to convert monthly and yearly summed quantities into averages
    over the number of days in the period.
uses:
  sd_channel_module: '`wtemp` is the stream water temperature value appended to every channel
    output record, so this module provides one of the reported diagnostics for each print
    period.'
  basin_module: '`basin_module` holds the print-control flags that decide whether daily, monthly,
    yearly, or average-annual output is written, and whether CSV companions are also produced.
    Without `pco`, this routine would not know which branches to execute.'
  time_module: '`time_module` supplies the current simulation date and end-of-period markers
    that gate each output branch and provide the timestamp fields written to the files. It
    also provides `time%step` for the subdaily hydrograph loop and `time%yrs_prt` for the
    final average-annual conversion.'
  hydrograph_module: '`hydrograph_module` supplies the channel hydrograph accumulators and
    object metadata that are printed or updated here. The routine writes `ob(iob)%name`, `ob(iob)%gis_id`,
    and `ob(iob)%hyd_flo(1,ii)`, and it updates `ch_in_*`, `ch_out_*`, and `ch_stor`-related
    summary states for the selected channel.'
  water_body_module: '`water_body_module` provides the daily, monthly, yearly, and average-annual
    channel water-body summaries that are printed and accumulated here. The routine reports
    channel area, precipitation, evaporation, and seepage from these structures and resets
    month-end water-body state after it has been written.'
---

<!-- facts:header -->

Writes SWAT+ stream-channel output for daily, monthly, yearly, and average-annual reporting. It also accumulates daily values into monthly, yearly, and average-annual summary states.

## Bottom Line

sd_channel_output collects channel water and hydrograph totals for the requested channel `ichan`, then writes them to the configured output units when the relevant print flags are on. It handles daily, monthly, yearly, and average-annual channel reporting, plus a subdaily hydrograph listing when daily printing is enabled and subdaily steps exist.

The routine matters because it is the point where channel diagnostics are both summarized across time periods and emitted to the model's output files. It also resets monthly state after month-end and converts yearly and final average-annual accumulators into per-day or per-year averages before writing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` during the channel-output phase after the model has advanced time, updated channel hydrographs, and populated daily and period accumulators. Its output feeds the model's channel reporting files and depends on the accumulators being current before month-end, year-end, and end-of-simulation writes occur.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the channel index to the corresponding object record. | Compute `iob` from `sp_ob1%chandeg + ichan - 1` so the routine can access the correct object connectivity entry for this channel. |
| 2. Accumulate daily values into the monthly summaries. | Add the current day's inflow, outflow, and water-body quantities to the month-to-date accumulators for the selected channel. |
| 3. Optionally write subdaily hydrograph output. | If daily printing is active, the current day is at an output interval, and subdaily steps exist, loop over `time%step` and write each subdaily hydrograph value to unit 2508. |
| 4. Write daily channel output when requested. | On the daily print interval, write the daily channel summary to unit 2500 and, if CSV output is enabled, write the same data in CSV form to unit 2504. |
| 5. Convert monthly sums to averages and write month-end output. | At month end, compute the month-length divisor, accumulate monthly values into yearly totals, divide monthly inflow and outflow by the number of days, divide the monthly water-body state by the month length, write monthly output when requested, and then reset monthly hydrograph and water-body state using `chaz` and `wbodz`. |
| 6. Convert yearly sums to averages and write yearly output. | At year end, divide yearly inflow and outflow by `time%day_end_yr`, add the yearly values into the average-annual totals, divide the yearly water-body state by the year length, and write yearly output and CSV output when requested. |
| 7. Finalize average-annual output at simulation end. | At the end of the simulation, divide average-annual inflow, outflow, and water-body values by `time%yrs_prt` and write the final average-annual records to the standard and CSV output units when requested. |
| 8. Return to the caller. | Exit the subroutine after all requested output records and accumulator updates have been completed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `wtemp` |  |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%sd_chan%d, pco%csvout, pco%sd_chan%m, pco%sd_chan%y, pco%sd_chan%a` |
| [sym:time_module] | `time` | `time%step, time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt` |
| [sym:hydrograph_module] | `sp_ob1, ob, ch_in_m, ch_out_m, ch_in_y, ch_out_y, ch_in_d, ch_out_d, ch_stor, ch_in_a, ch_out_a, chaz` | `sp_ob1%chandeg, ob(iob)%name, ob(iob)%hyd_flo(1,ii), ch_in_m(ichan)%flo, ch_out_m(ichan)%flo, ch_in_y(ichan)%flo, ch_out_y(ichan)%flo` |
| [sym:water_body_module] | `ch_wat_d, ch_wat_m, ch_wat_y, ch_wat_a, wbodz` | `ch_wat_d(ichan)%area_ha, ch_wat_d(ichan)%precip, ch_wat_d(ichan)%evap, ch_wat_d(ichan)%seep, ch_wat_m(ichan)%area_ha, ch_wat_m(ichan)%precip, ch_wat_m(ichan)%evap, ch_wat_m(ichan)%seep, ch_wat_y(ichan)%area_ha, ch_wat_y(ichan)%precip, ch_wat_y(ichan)%evap, ch_wat_y(ichan)%seep, ch_wat_a(ichan)%area_ha, ch_wat_a(ichan)%precip, ch_wat_a(ichan)%evap, ch_wat_a(ichan)%seep` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ch_in_m(ichan)` | At the end of every call, before any period-specific output branches run. | `ch_in_m(ichan)` accumulates the current day's inflow into the month-to-date total, then is later divided by the month length at month end and reset to `chaz` after monthly output is written. |
| `ch_out_m(ichan)` | At the end of every call, before any period-specific output branches run. | `ch_out_m(ichan)` accumulates the current day's outflow into the month-to-date total, then is later divided by the month length at month end and reset to `chaz` after monthly output is written. |
| `ch_wat_m(ichan)` | At the end of every call, before any period-specific output branches run. | `ch_wat_m(ichan)` accumulates the current day's water-body summary, is converted to a monthly average by dividing by the month length, and is reset to `wbodz` after the monthly record is written. |
| `ch_in_y(ichan)` | When `time%end_mo == 1`. | `ch_in_y(ichan)` receives the month-to-date inflow total so the yearly accumulator can build from monthly sums. |
| `ch_out_y(ichan)` | When `time%end_mo == 1`. | `ch_out_y(ichan)` receives the month-to-date outflow total so the yearly accumulator can build from monthly sums. |
| `ch_wat_y(ichan)` | When `time%end_mo == 1`. | `ch_wat_y(ichan)` receives the month-to-date water-body summary, then later becomes a monthly-averaged state by division with the month length. |
| `ch_in_m(ichan)%flo` | When `time%end_mo == 1`. | `ch_in_m(ichan)%flo` is divided by the number of days in the current month to convert the month-total inflow into a daily mean before monthly output. |
| `ch_out_m(ichan)%flo` | When `time%end_mo == 1`. | `ch_out_m(ichan)%flo` is divided by the number of days in the current month to convert the month-total outflow into a daily mean before monthly output. |
| `ch_in_y(ichan)%flo` | When `time%end_yr == 1`. | `ch_in_y(ichan)%flo` is divided by `time%day_end_yr` to convert the yearly inflow total into a daily mean before yearly output and average-annual accumulation. |
| `ch_out_y(ichan)%flo` | When `time%end_yr == 1`. | `ch_out_y(ichan)%flo` is divided by `time%day_end_yr` to convert the yearly outflow total into a daily mean before yearly output and average-annual accumulation. |
| `ch_in_a(ichan)` | When `time%end_yr == 1`. | `ch_in_a(ichan)` accumulates the yearly inflow summary so that the final average-annual value can be computed at simulation end. |
| `ch_out_a(ichan)` | When `time%end_yr == 1`. | `ch_out_a(ichan)` accumulates the yearly outflow summary so that the final average-annual value can be computed at simulation end. |
| `ch_wat_a(ichan)` | When `time%end_yr == 1` and again when `time%end_sim == 1`. | `ch_wat_a(ichan)` first accumulates yearly water-body summaries into the average-annual total, then is divided by `time%yrs_prt` at simulation end to produce the final average-annual water-body state. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four source-backed changes. The initial commit `df07e3f` added `sd_channel_output` with daily, monthly, yearly, and average-annual output branches, subdaily hydrograph output, and monthly/yearly accumulator resets. Commit `39fabde` initialized local variables `iob`, `ii`, and `const`. Commit `889136d` fixed a typo in the annual accumulator comment, changing "varaibles" to "variables". Commit `2fe89fd` changed the CSV writers for units 2504, 2505, 2506, and 2507 from `G0.3` to `G0.6` formatting.

- df07e3f introduced the full procedure structure: channel-object mapping, daily/monthly/yearly/average-annual output branches, subdaily hydrograph writes, and accumulator resets.
- 39fabde changed only local-variable initialization, giving `iob`, `ii`, and `const` explicit zero initial values.
- 889136d changed only a comment in the end-of-simulation annual block and did not alter execution behavior.
- 2fe89fd changed the CSV output format width on the four CSV units from `G0.3` to `G0.6`, increasing numeric precision in those files.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'sd_channel_output' has no extracted documentation comment.
