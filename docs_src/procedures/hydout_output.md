---
kind: procedure
symbol: hydout_output
title: hydout_output
status: filled
source_hash: 8a7cb9f37023c172
version_label: SWAT+ 62.0.0
args:
  iout: '`iout` selects which outflow slot of `ob(icmd)` this call is reporting. The caller
    loops over `1:ob(icmd)%src_tot`, so `iout` identifies the specific outflow object/type,
    hydro type, fraction, and summary accumulators to print and update.'
uses:
  time_module: '`time_module` supplies the current date and end-of-period flags that decide
    when daily, monthly, yearly, and end-of-simulation output should happen. Its `time` state
    also provides the averaging divisor `time%yrs_prt` for the average-annual record.'
  basin_module: '`basin_module` supplies the print-control switches that gate each output
    branch, including daily, monthly, yearly, annual, and CSV printing. Without `pco`, this
    routine would not know whether to write anything or whether to reset on the current day
    interval.'
  hydrograph_module: '`hydrograph_module` provides the active command object `ob(icmd)` plus
    the source hydrograph values and metadata for the selected outflow. Those fields are the
    content written to the output files and the monthly/yearly/annual accumulators that this
    routine updates.'
---

<!-- facts:header -->

Writes hydrologic summary output for one routed outflow pathway. It accumulates daily values, then reports monthly, yearly, and average-annual totals when the relevant end-of-period flags are set.

## Bottom Line

`hydout_output` is the hydrologic reporting routine for a single outflow index `iout`. Each time it runs, it uses the current simulation date, the active command object, and the selected hydrograph fraction/value to write daily records when daily printing is enabled, then roll those values into monthly, yearly, and average-annual summaries.

The routine also resets the period accumulators at month and year boundaries so later calls start a new tally. Its output is controlled by print-code flags in `pco` and written to fixed unit numbers for plain text and optional CSV records.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine inside the outflow loop after it has chosen the active command object `icmd`, found each outflow index `iout`, and computed `ht1 = ob(icmd)%frac_out(iout) * ob(icmd)%hd(ihtyp)`. The results feed the model's hydrologic reporting files and the period accumulators `hout_m`, `hout_y`, and `hout_a` used for later month, year, and simulation-end summaries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check for daily-print conditions. | The routine first tests whether daily printing is active for the current day interval by requiring `pco%day_print == 'y'` and `pco%int_day_cur == pco%int_day`. It then checks the hydrologic daily print code `pco%hyd%d` before writing anything for the daily branch. |
| 2. Write daily hyd output records. | When the daily branch is enabled, the routine writes a plain-text daily record to unit 2580 and, if CSV output is enabled, a CSV-formatted record to unit 2584. Both records report the current date, object name and type, outflow type information, fraction, and the daily hydro value `ht1`. |
| 3. Accumulate the daily value into the monthly sum. | After the daily output decision, the routine adds the daily hydro value to `ob(icmd)%hout_m(iout)`. This keeps a running monthly total regardless of whether the daily record was printed. |
| 4. On month end, write monthly output and roll the totals upward. | If `time%end_mo == 1`, the routine checks `pco%hyd%m` and writes the monthly total to unit 2581, with an optional CSV copy on unit 2585. It then adds the monthly total into `ob(icmd)%hout_y(iout)` and clears the monthly accumulator by setting `ob(icmd)%hout_m(iout) = hz`. |
| 5. On year end, write yearly output and roll the totals upward. | If `time%end_yr == 1`, the routine checks `pco%hyd%y` and writes the yearly total to unit 2582, with an optional CSV copy on unit 2586. It then adds the yearly total into `ob(icmd)%hout_a(iout)` and clears the yearly accumulator by setting `ob(icmd)%hout_y(iout) = hz`. |
| 6. On simulation end, write average-annual output. | When `time%end_sim == 1` and average-annual hyd printing is enabled, the routine divides `ob(icmd)%hout_a(iout)` by `time%yrs_prt` and writes the final average-annual record to unit 2583, with an optional CSV copy on unit 2587. |
| 7. Return to the caller. | The routine ends with a simple return after writing any applicable records and updating the period accumulators. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%hyd%d, pco%csvout, pco%hyd%m, pco%hyd%y, pco%hyd%a` |
| [sym:hydrograph_module] | `ob, icmd, ht1, hz` | `ob(icmd)%name, ob(icmd)%typ, ob(icmd)%obtyp_out(iout), ob(icmd)%obtypno_out(iout), ob(icmd)%htyp_out(iout), ob(icmd)%frac_out(iout), ob(icmd)%hout_m(iout), ob(icmd)%hout_y(iout), ob(icmd)%hout_a(iout)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ob(icmd)%hout_m(iout)` | `ob(icmd)%hout_m(iout)` changes every time the routine runs, by adding `ht1`; it is then reset to `hz` when `time%end_mo == 1`. | This field stores the running monthly hydro sum for the selected outflow. The daily value is accumulated here so the month-end print can report the month total, after which the accumulator is cleared for the next month. |
| `ob(icmd)%hout_y(iout)` | `ob(icmd)%hout_y(iout)` changes when `time%end_mo == 1`, by adding the completed monthly total; it is then reset to `hz` when `time%end_yr == 1`. | This field stores the running yearly hydro sum for the selected outflow. It collects each month's total so the year-end print can report the yearly total, then it is cleared to start a new year. |
| `ob(icmd)%hout_a(iout)` | `ob(icmd)%hout_a(iout)` changes when `time%end_yr == 1`, by adding the completed yearly total; it is then divided by `time%yrs_prt` and printed when `time%end_sim == 1` and `pco%hyd%a == 'y'`. | This field stores the simulation-long hydro sum for the selected outflow. It accumulates yearly totals so the final average-annual record can be computed from the full simulation period. |

## File I/O

<!-- facts:io -->


## Lineage

`hydout_output` was added in `df07e3f` as a new procedure that writes daily, monthly, yearly, and average-annual hyd output and maintains monthly/yearly/annual accumulators. In `94b6dec`, the source was brought in from the Bitbucket version with the same output logic, and `2fe89fd` changed the CSV format specifiers for the optional CSV writes from `G0.3` to `G0.6` on units 2584, 2585, 2586, and 2587.

- df07e3f introduced the routine and its period-based hyd output flow, including the daily-to-monthly-to-yearly accumulation and final average-annual report.
- 94b6dec imported the routine into the repository with the same control flow and output branches shown in the extracted source.
- 2fe89fd updated the CSV output formatting on the optional CSV files so numeric fields are written with `G0.6` instead of `G0.3`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hydout_output' has no extracted documentation comment.
