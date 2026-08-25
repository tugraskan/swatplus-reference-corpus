---
kind: procedure
symbol: reservoir_output
title: reservoir_output
status: filled
source_hash: 137d23bd87366e8f
version_label: SWAT+ 62.0.0
args:
  j: '`j` selects which reservoir in the reservoir arrays to report. The routine uses `j`
    to index the daily, monthly, yearly, and average-annual reservoir output state and to
    derive the corresponding object index `iob = sp_ob1%res + j - 1` for names and GIS IDs.'
locals:
  iob: '`iob` is the resolved hydrograph-object index for the `j`th reservoir. It shifts from
    reservoir-local numbering to the shared `ob` connectivity array so the routine can print
    the correct `gis_id` and object name.'
  const: '`const` holds the number of days in the current month as a real value when monthly
    output is finalized. It is used in the monthly-end block while adjusting water-body quantities
    before they are rolled into yearly totals; the source shows it initialized to `0.` and
    set from `ndays(...) - ndays(...)`.'
uses:
  time_module: '`time_module` supplies the simulation clock and end-of-period flags that decide
    whether daily, monthly, yearly, or average-annual reservoir output should be written.
    The date fields are also printed into every record so each summary can be tied to the
    correct day, month, year, and simulation duration.'
  basin_module: '`basin_module` provides the print-control flags that gate reservoir output.
    `pco%day_print`, `pco%int_day_cur`, and `pco%int_day` control daily timing, while `pco%res%d`,
    `pco%res%m`, `pco%res%y`, `pco%res%a`, and `pco%csvout` decide which reservoir summaries
    and CSV variants are emitted.'
  reservoir_module: '`reservoir_module` is needed because it owns the reservoir-specific output
    state and object numbering used by this routine. The routine depends on the reservoir
    start index `sp_ob1%res`, the reservoir object arrays, and the zeroed summary state `resmz`
    when it resets period accumulators after printing.'
  hydrograph_module: '`hydrograph_module` matters because it contains the shared hydrologic
    output arrays and object connectivity metadata that reservoir output reports. The routine
    reads the reservoir hydrograph summaries from `res`, `res_in_*`, and `res_out_*`, and
    it uses `ob(iob)%name` together with the reservoir object index to label each line.'
  water_body_module: '`water_body_module` matters because reservoir output also reports reservoir
    water-body summaries for depth, storage, and other water-body metrics. The routine writes
    the period-specific `res_wat_*` states and resets them to `wbodz` after each period, so
    this module provides both the running values and the zeroed reset template.'
---

<!-- facts:header -->

Writes reservoir daily, monthly, yearly, and average-annual output records for each reservoir object. It gathers the current reservoir and water-body summaries and sends them to the configured output files when the print flags allow.

## Bottom Line

`reservoir_output` is the reservoir reporting subroutine. For the reservoir index `j`, it maps to the corresponding hydrologic object, checks the current print schedule and reservoir print flags, and writes the matching daily, monthly, yearly, or simulation-average summaries to the standard reservoir output units and optional CSV units.

It also rolls daily reservoir inflow, outflow, and water-body summaries into monthly, yearly, and average-annual accumulators, then clears period accumulators after each print period ends so later calls start a fresh tally.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`reservoir_output` runs once per reservoir from `command` inside the reservoir loop. Upstream setup must already have populated `sp_ob1%res`, `ob`, the reservoir output arrays, the print flags in `pco`, and the simulation time state; downstream reporting and postprocessing depend on these written records and on the reset of the period accumulators.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Resolve the reservoir object index | Convert the reservoir-local index `j` into the shared hydrograph object index `iob = sp_ob1%res + j - 1` so names and GIS IDs come from the correct object entry. |
| 2. Write daily reservoir output when daily printing is enabled | If `pco%day_print == "y"` and `pco%int_day_cur == pco%int_day`, then write the daily reservoir record to unit 2540 when `pco%res%d == "y"`, and write the CSV companion to unit 2544 when `pco%csvout == "y"`. |
| 3. Accumulate daily values into monthly totals | Add the daily inflow, outflow, and water-body summaries into the monthly accumulators `res_in_m(j)`, `res_out_m(j)`, and `res_wat_m(j)`. |
| 4. Finalize and write monthly reservoir output at month end | When `time%end_mo == 1`, compute the month length in `const`, roll monthly inflow and outflow into yearly accumulators, adjust and roll monthly water-body state into yearly totals, write monthly output to unit 2541 and optional CSV unit 2545 if `pco%res%m == "y"`, then reset monthly accumulators to `resmz` and `wbodz`. |
| 5. Finalize and write yearly reservoir output at year end | When `time%end_yr == 1`, roll yearly inflow and outflow into average-annual accumulators, adjust yearly water-body state into average-annual totals, write yearly output to unit 2542 and optional CSV unit 2546 if `pco%res%y == "y"`, then reset yearly accumulators to `resmz` and `wbodz`. |
| 6. Finalize and write average-annual reservoir output at simulation end | When `time%end_sim == 1` and `pco%res%a == "y"`, divide the accumulated average-annual totals by `time%yrs_prt`, write the simulation-average record to unit 2543 and optional CSV unit 2547, then reset the average-annual accumulators to `resmz` and `wbodz`. |
| 7. Return to caller | Exit the subroutine after all eligible reservoir output records and accumulator resets have been handled. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%res%d, pco%csvout, pco%res%m, pco%res%y, pco%res%a` |
| [sym:reservoir_module] | `sp_ob1, ob, res, res_in_d, res_out_d, res_in_m, res_out_m, res_in_y, res_out_y, res_in_a, res_out_a, resmz` | `sp_ob1%res, ob(iob)%gis_id, ob(iob)%name, res(j), res_in_d(j), res_out_d(j), res_in_m(j), res_out_m(j), res_in_y(j), res_out_y(j), res_in_a(j), res_out_a(j), resmz` |
| [sym:hydrograph_module] | `sp_ob1, ob, res, res_in_d, res_out_d, res_in_m, res_out_m, res_in_y, res_out_y, res_in_a, res_out_a, resmz` | `sp_ob1%res, ob(iob)%name` |
| [sym:water_body_module] | `res_wat_d, res_wat_m, res_wat_y, res_wat_a, wbodz` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `res_in_m(j)` | At every call, after resolving `iob` and before any print-period checks. | Adds the current daily reservoir inflow to the monthly accumulator so the month-end record can report the total inflow over the month. |
| `res_out_m(j)` | At every call, after resolving `iob` and before any print-period checks. | Adds the current daily reservoir outflow to the monthly accumulator so the month-end record can report the total outflow over the month. |
| `res_wat_m(j)` | At every call, after resolving `iob` and before any print-period checks. | Adds the current daily reservoir water-body summary to the monthly accumulator so the month-end record can report the month aggregate. |
| `res_in_y(j)` | When `time%end_mo == 1`. | Adds the completed monthly inflow total into the yearly accumulator at the end of each month so the year-end record can sum the monthly values. |
| `res_out_y(j)` | When `time%end_mo == 1`. | Adds the completed monthly outflow total into the yearly accumulator at the end of each month so the year-end record can sum the monthly values. |
| `res_wat_y(j)` | When `time%end_mo == 1`. | First converts the monthly water-body summary by the month-length factor, then adds it into the yearly accumulator so the yearly record reflects month contributions. |
| `res_in_a(j)` | When `time%end_yr == 1`. | Adds the completed yearly inflow total into the average-annual accumulator so the simulation-end average can be computed from year totals. |
| `res_out_a(j)` | When `time%end_yr == 1`. | Adds the completed yearly outflow total into the average-annual accumulator so the simulation-end average can be computed from year totals. |
| `res_wat_a(j)` | When `time%end_yr == 1`. | Adds the completed yearly water-body summary into the average-annual accumulator after the yearly water value is scaled by 12 months. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show two behavior changes and two earlier introduction commits. The initial `df07e3f` commit added `reservoir_output.f90` with daily, monthly, yearly, and average-annual reservoir reporting. `39fabde` initialized the local variables `iob` and `const` in the source. `2fe89fd` changed the CSV writes from `G0.3` to `G0.6` formatting in all four CSV output branches. `94b6dec` was the file-import commit that brought in the routine without changing its logic.

- `39fabde` changed the declarations of `iob` and `const` to initialize them to `0` and `0.` before use.
- `2fe89fd` updated the CSV output format strings for units 2544, 2545, 2546, and 2547 from `G0.3` to `G0.6`, increasing numeric precision in the exported reservoir CSV files.
- `df07e3f` introduced the full reservoir reporting workflow, including daily, monthly, yearly, and average-annual writes plus accumulator resets.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'reservoir_output' has no extracted documentation comment.
