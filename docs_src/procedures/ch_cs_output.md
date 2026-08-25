---
kind: procedure
symbol: ch_cs_output
title: ch_cs_output
status: filled
source_hash: 179411f2a36b6c2b
version_label: SWAT+ 62.0.0
args:
  jrch: '`jrch` identifies the channel routing element to report. The routine copies it into
    `iru`, then uses that index to select the channel constituent-mass arrays for accumulation
    and output.'
locals:
  ics: Loop index over constituent species in `cs_db%num_cs`, used to update, average, and
    write each constituent’s channel balances.
  iru: Channel routing-unit index derived from `jrch`; selects which `chcs_*` record set and
    output row to process.
  iob: Object index for the corresponding hydrograph/channel object, computed from `sp_ob1%chandeg
    + iru - 1` so the routine can print `ob(iob)%gis_id`.
  const: Temporary divisor used to convert accumulated water and concentration totals into
    period averages at month end and year end.
uses:
  output_ls_pesticide_module: '`output_ls_pesticide_module` is imported, but no resolved symbols
    from it appear in the extracted source lines. It matters here only as a shared output-module
    dependency; the packet does not show any direct use of its state in this procedure.'
  ch_cs_module: '`ch_cs_module` provides the constituent-mass storage that this routine updates
    and prints. The routine accumulates daily values into `chcs_m`, monthly values into `chcs_y`,
    and yearly values into `chcs_a`, then writes fields from the same structures to the channel
    constituent output files.'
  plant_module: '`plant_module` is imported, but no resolved plant variables or types appear
    in the extracted lines. It likely belongs to a shared output/use block, but the packet
    gives no direct evidence that this routine reads plant state.'
  plant_data_module: '`plant_data_module` is imported, but no resolved plant-data symbols
    are used in the source lines shown. It is present as a shared dependency, yet the packet
    does not show direct use in this routine.'
  time_module: '`time_module` supplies the simulation clock fields that control when monthly,
    yearly, and end-of-simulation reports are written. The routine uses `time%day`, `time%mo`,
    `time%day_mo`, `time%yrc`, `time%end_mo`, `time%end_yr`, `time%end_sim`, `time%day_end_yr`,
    and `time%nbyr` to stamp output and decide when to roll accumulators forward.'
  basin_module: '`basin_module` provides the print-code switches that gate each output tier.
    `pco%cs_chn%d`, `%m`, `%y`, and `%a` determine whether daily, monthly, yearly, and average-annual
    channel constituent output is written, and `pco%csvout` controls the CSV companion files.'
  output_landscape_module: '`output_landscape_module` is imported, but the extracted lines
    show no referenced symbols from it. It appears to be part of the broader output infrastructure
    rather than a directly used data source in this routine.'
  constituent_mass_module: '`constituent_mass_module` supplies `cs_db%num_cs`, the number
    of simulated constituent species. That value drives the loop bounds and the array sections
    written for each channel output record.'
  hydrograph_module: '`hydrograph_module` provides channel-object metadata needed to label
    the output. `sp_ob1%chandeg` converts `jrch` into the proper object index, and `ob(iob)%gis_id`
    is written as the GIS identifier for the reported channel.'
---

<!-- facts:header -->

Writes channel constituent-mass outputs for daily, monthly, yearly, and average-annual reporting. It accumulates day values into month totals, month totals into year totals, and year totals into average-annual totals while optionally writing CSV copies.

## Bottom Line

`ch_cs_output` is the channel constituent-mass reporting routine. For the channel routed by `jrch`, it maps that routing channel to the corresponding hydrograph object, adds the current day’s constituent balances into the monthly accumulator, and writes daily output when `pco%cs_chn%d` is enabled. It also mirrors that daily data to CSV when `pco%csvout` is enabled.

At month end it rolls monthly totals into yearly storage, computes monthly averages for `water` and `conc`, writes monthly output if requested, and then clears the monthly accumulator. At year end it rolls yearly totals into average-annual storage, computes yearly averages for `water` and `conc`, writes yearly output if requested, and then clears the yearly accumulator. When the simulation ends and average-annual output is enabled, it divides the accumulated totals by `time%nbyr` and writes the final average-annual report.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ch_cs_output` runs from the main command/output loop after channel routing has produced the daily constituent balances for the current `jrch`. `command` calls it only when `cs_db%num_cs > 0`, so the routine depends on constituent-mass simulation being initialized and on the channel hydrograph/object arrays already being populated. Its results feed the daily, monthly, yearly, and average-annual constituent output files that summarize channel mass and concentration behavior over the run.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the channel index to output state | Copies `jrch` into `iru` and computes `iob = sp_ob1%chandeg + iru - 1` so the routine can index the channel constituent arrays and associated GIS/object metadata. |
| 2. Accumulate daily values into the monthly storage | Loops over all constituent species and adds each daily balance field from `chcs_d(iru)%cs(ics)` into the matching monthly accumulator `chcs_m(iru)%cs(ics)`. |
| 3. Write daily channel constituent output when enabled | If daily channel output is enabled, writes the current day, month, year, routing-unit id, GIS id, and all daily constituent balance fields to unit 6030; if CSV output is enabled, writes the same data to unit 6031. |
| 4. On month end, roll monthly totals into yearly storage | When `time%end_mo == 1`, adds each monthly balance from `chcs_m(iru)%cs(ics)` into the yearly accumulator `chcs_y(iru)%cs(ics)`. |
| 5. Compute monthly averages for water and concentration | Uses `const = float(ndays(time%mo + 1) - ndays(time%mo))` as the number of days in the month, then divides monthly `water` and `conc` by that divisor to report average mass and concentration. |
| 6. Write monthly output when enabled | If monthly output is enabled, writes the monthly constituent balances to unit 6032 and optionally writes the CSV version to unit 6033. |
| 7. Clear the monthly accumulator after month-end reporting | Resets every monthly constituent balance field in `chcs_m(iru)%cs(ics)` to zero so the next month starts fresh. |
| 8. On year end, roll yearly totals into annual storage | When `time%end_yr == 1`, adds each yearly balance from `chcs_y(iru)%cs(ics)` into the average-annual accumulator `chcs_a(iru)%cs(ics)` and preserves the running totals for the full simulation. |
| 9. Compute yearly averages for water and concentration | Uses `const = time%day_end_yr` as the divisor for the year and divides yearly `water` and `conc` by that value to form annual averages. |
| 10. Write yearly output when enabled | If yearly output is enabled, writes the yearly constituent balances to unit 6034 and optionally writes the CSV version to unit 6035. |
| 11. Clear the yearly accumulator after year-end reporting | Resets every yearly constituent balance field in `chcs_y(iru)%cs(ics)` to zero so the next year starts fresh. |
| 12. On simulation end, compute average-annual values and write final output | When `time%end_sim == 1` and average-annual output is enabled, divides the accumulated annual totals by `time%nbyr`, writes the final average-annual record to unit 6036, and optionally writes the CSV version to unit 6037. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `none resolved` | `none resolved` |
| [sym:ch_cs_module] | `chcs_m, chcs_d, chcs_y, chcs_a` | `chcs_m(iru)%cs(ics)%tot_in, chcs_d(iru)%cs(ics)%tot_in, chcs_m(iru)%cs(ics)%gw_in, chcs_d(iru)%cs(ics)%gw_in, chcs_m(iru)%cs(ics)%tot_out, chcs_d(iru)%cs(ics)%tot_out, chcs_m(iru)%cs(ics)%seep, chcs_d(iru)%cs(ics)%seep, chcs_m(iru)%cs(ics)%irr, chcs_d(iru)%cs(ics)%irr, chcs_m(iru)%cs(ics)%div, chcs_d(iru)%cs(ics)%div, chcs_m(iru)%cs(ics)%water, chcs_d(iru)%cs(ics)%water, chcs_m(iru)%cs(ics)%conc, chcs_d(iru)%cs(ics)%conc, chcs_y(iru)%cs(ics)%tot_in, chcs_y(iru)%cs(ics)%gw_in, chcs_y(iru)%cs(ics)%tot_out, chcs_y(iru)%cs(ics)%seep, chcs_y(iru)%cs(ics)%irr, chcs_y(iru)%cs(ics)%div, chcs_y(iru)%cs(ics)%water, chcs_y(iru)%cs(ics)%conc, chcs_a(iru)%cs(ics)%tot_in, chcs_a(iru)%cs(ics)%gw_in, chcs_a(iru)%cs(ics)%tot_out, chcs_a(iru)%cs(ics)%seep, chcs_a(iru)%cs(ics)%irr, chcs_a(iru)%cs(ics)%div, chcs_a(iru)%cs(ics)%water, chcs_a(iru)%cs(ics)%conc` |
| [sym:plant_module] | `none resolved` | `none resolved` |
| [sym:plant_data_module] | `none resolved` | `none resolved` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%cs_chn%d, pco%csvout, pco%cs_chn%m, pco%cs_chn%y, pco%cs_chn%a` |
| [sym:output_landscape_module] | `none resolved` | `none resolved` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%chandeg` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `chcs_m(iru)%cs(ics)%tot_in` | At every call, inside the `do ics = 1, cs_db%num_cs` loop. | `chcs_m(iru)%cs(ics)%tot_in` grows by adding the current day’s `chcs_d(iru)%cs(ics)%tot_in`. This preserves a month-to-date total for each constituent. |
| `chcs_m(iru)%cs(ics)%gw_in` | At every call, inside the `do ics = 1, cs_db%num_cs` loop. | `chcs_m(iru)%cs(ics)%gw_in` grows by adding the current day’s groundwater input from `chcs_d(iru)%cs(ics)%gw_in` so the monthly accumulator retains month-to-date groundwater loading. |
| `chcs_m(iru)%cs(ics)%tot_out` | At every call, inside the `do ics = 1, cs_db%num_cs` loop. | `chcs_m(iru)%cs(ics)%tot_out` grows by adding the current day’s total channel خروج from `chcs_d(iru)%cs(ics)%tot_out`. |
| `chcs_m(iru)%cs(ics)%seep` | At every call, inside the `do ics = 1, cs_db%num_cs` loop. | `chcs_m(iru)%cs(ics)%seep` grows by adding daily seepage loss from `chcs_d(iru)%cs(ics)%seep` so the month-to-date seepage total is preserved. |
| `chcs_m(iru)%cs(ics)%irr` | At every call, inside the `do ics = 1, cs_db%num_cs` loop. | `chcs_m(iru)%cs(ics)%irr` grows by adding the day’s irrigation-related mass from `chcs_d(iru)%cs(ics)%irr`. |
| `chcs_m(iru)%cs(ics)%div` | At every call, inside the `do ics = 1, cs_db%num_cs` loop. | `chcs_m(iru)%cs(ics)%div` grows by adding daily diversion mass from `chcs_d(iru)%cs(ics)%div`. |
| `chcs_m(iru)%cs(ics)%water` | At every call, inside the `do ics = 1, cs_db%num_cs` loop. | `chcs_m(iru)%cs(ics)%water` grows by adding the day’s end-of-day channel water amount, which is later converted to an average at month end. |
| `chcs_m(iru)%cs(ics)%conc` | At every call, inside the `do ics = 1, cs_db%num_cs` loop. | `chcs_m(iru)%cs(ics)%conc` grows by adding the day’s concentration value, which is later converted to an average at month end. |
| `chcs_y(iru)%cs(ics)%tot_in` | When `time%end_mo == 1`, inside the monthly rollup loop. | `chcs_y(iru)%cs(ics)%tot_in` accumulates the finished month’s total input from `chcs_m(iru)%cs(ics)%tot_in`, preserving a year-to-date total. |
| `chcs_y(iru)%cs(ics)%gw_in` | When `time%end_mo == 1`, inside the monthly rollup loop. | `chcs_y(iru)%cs(ics)%gw_in` accumulates the finished month’s groundwater input from the monthly storage. |
| `chcs_y(iru)%cs(ics)%tot_out` | When `time%end_mo == 1`, inside the monthly rollup loop. | `chcs_y(iru)%cs(ics)%tot_out` accumulates the finished month’s total outflow into the year-to-date record. |
| `chcs_y(iru)%cs(ics)%seep` | When `time%end_mo == 1`, inside the monthly rollup loop. | `chcs_y(iru)%cs(ics)%seep` accumulates monthly seepage into the year-to-date balance. |
| `chcs_y(iru)%cs(ics)%irr` | When `time%end_mo == 1`, inside the monthly rollup loop. | `chcs_y(iru)%cs(ics)%irr` accumulates monthly irrigation mass into the year-to-date balance. |
| `chcs_y(iru)%cs(ics)%div` | When `time%end_mo == 1`, inside the monthly rollup loop. | `chcs_y(iru)%cs(ics)%div` accumulates monthly diversion mass into the year-to-date balance. |
| `chcs_y(iru)%cs(ics)%water` | When `time%end_mo == 1`, after yearly rollup and before yearly output. | `chcs_y(iru)%cs(ics)%water` is divided by the number of days in the month so the stored monthly water value becomes an average for reporting. |
| `chcs_y(iru)%cs(ics)%conc` | When `time%end_mo == 1`, after yearly rollup and before yearly output. | `chcs_y(iru)%cs(ics)%conc` is divided by the number of days in the month so the stored monthly concentration becomes an average for reporting. |
| `chcs_a(iru)%cs(ics)%tot_in` | When `time%end_yr == 1`, inside the yearly rollup loop. | `chcs_a(iru)%cs(ics)%tot_in` accumulates the year’s total input from `chcs_y(iru)%cs(ics)%tot_in` into the simulation-total storage. |
| `chcs_a(iru)%cs(ics)%gw_in` | When `time%end_yr == 1`, inside the yearly rollup loop. | `chcs_a(iru)%cs(ics)%gw_in` accumulates the year’s groundwater input into the average-annual storage. |
| `chcs_a(iru)%cs(ics)%tot_out` | When `time%end_yr == 1`, inside the yearly rollup loop. | `chcs_a(iru)%cs(ics)%tot_out` accumulates the year’s total outflow into the average-annual storage. |
| `chcs_a(iru)%cs(ics)%seep` | When `time%end_yr == 1`, inside the yearly rollup loop. | `chcs_a(iru)%cs(ics)%seep` accumulates the year’s seepage into the simulation-total storage. |
| `chcs_a(iru)%cs(ics)%irr` | When `time%end_yr == 1`, inside the yearly rollup loop. | `chcs_a(iru)%cs(ics)%irr` accumulates the year’s irrigation mass into the simulation-total storage. |
| `chcs_a(iru)%cs(ics)%div` | When `time%end_yr == 1`, inside the yearly rollup loop. | `chcs_a(iru)%cs(ics)%div` accumulates the year’s diversion mass into the simulation-total storage. |
| `chcs_a(iru)%cs(ics)%water` | When `time%end_yr == 1`, before yearly output is written. | `chcs_a(iru)%cs(ics)%water` is divided by `time%nbyr` at the end of the simulation so the final output is an average annual water value. |
| `chcs_a(iru)%cs(ics)%conc` | When `time%end_yr == 1`, before yearly output is written. | `chcs_a(iru)%cs(ics)%conc` is divided by `time%nbyr` at the end of the simulation so the final output is an average annual concentration value. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior changes for `ch_cs_output`. The initial addition in `df07e3f` introduced the routine, its daily/monthly/yearly/average-annual accumulation logic, and all output writes. `39fabde` only initialized local variables (`ics`, `iru`, `iob`, `const`, plus removed unused locals later in `2ee1889`), so it did not change runtime behavior. `2ee1889` removed unused locals `dum` and `n`. `2fe89fd` changed the CSV format descriptor for units 6031, 6033, 6035, and 6037 from `G0.3` to `G0.6`, increasing output precision for CSV writes.

- Introduced the entire channel constituent-mass reporting workflow, including daily accumulation into monthly totals, monthly rollup into yearly storage, yearly rollup into average-annual storage, zeroing after period-end reporting, and writes to units 6030-6037.
- Initialized local variables to zero and later removed two unused locals; these edits did not change the reported balances or output flow.
- Increased CSV output precision from `G0.3` to `G0.6` on units 6031, 6033, 6035, and 6037.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_cs_output' has no extracted documentation comment.
- output_ls_pesticide_module, plant_module, plant_data_module, and output_landscape_module are imported but no resolved symbols from them appear in the extracted lines; their direct use in this routine is uncertain from the packet.
- algorithm_steps revised: condensed the draft into 12 source-backed steps aligned to the actual control-flow regions and the visible line numbers.
- CSV writes use formatted G0.6 output in the current source; earlier history shows G0.3 before 2fe89fd.
