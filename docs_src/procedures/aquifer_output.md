---
kind: procedure
symbol: aquifer_output
title: aquifer_output
status: filled
source_hash: cc4d851ea5f1414a
version_label: SWAT+ 62.0.0
args:
  iaq: '`iaq` is the 1-based aquifer index for the aquifer object being printed. It selects
    which entries of `aqu_d`, `aqu_m`, `aqu_y`, and `aqu_a` are written and updated, and it
    is combined with `sp_ob1%aqu` to locate the matching object record in `ob`.'
locals:
  const: '`const` holds the number of days in the current month, computed from `ndays(time%mo
    + 1) - ndays(time%mo)`, so the monthly storage, depth-to-water, and nitrate sums can be
    converted to monthly averages before they are added into the yearly accumulator.'
  iob: '`iob` is the object-table index for the current aquifer, computed as `sp_ob1%aqu +
    iaq - 1`. It is used to fetch the aquifer object''s GIS id and name for the output records.'
uses:
  time_module: The `time` state supplies the current day, month, and year labels written to
    every record, plus the end-of-month, end-of-year, and end-of-simulation flags that control
    which reporting branches run. `time%yrs_prt` is also needed to compute the final average
    annual aquifer output.
  basin_module: The print-code state in `pco` determines whether daily, monthly, yearly, and
    average-annual aquifer output should be emitted at all, and whether matching CSV records
    should also be written. Without these flags, the routine would still roll up accumulators
    but would not write the corresponding files.
  aquifer_module: The aquifer dynamic arrays hold the simulation values being reported and
    accumulated here. `aqu_d`, `aqu_m`, `aqu_y`, `aqu_a`, and `aquz` provide the daily state,
    the running monthly and yearly totals, the annual aggregate, and the zeroed template used
    to reset period accumulators after printing.
  hydrograph_module: The hydrograph object tables provide the spatial mapping and labels needed
    to identify which aquifer is being printed. `sp_ob1%aqu` gives the first aquifer object
    index, and `ob(iob)%name` supplies the object name written with each output row.
---

<!-- facts:header -->

Writes aquifer daily, monthly, yearly, and average-annual output records for one aquifer object.

## Bottom Line

aquifer_output formats and writes aquifer results for the aquifer indexed by `iaq`. It handles daily output when the print flags request it, then rolls daily values into monthly totals, monthly values into yearly totals, and yearly values into an average-annual total.

The routine matters because it is the point where aquifer state from `aqu_d`, `aqu_m`, `aqu_y`, and `aqu_a` is exported to the model output units and the monthly/yearly accumulators are reset for the next reporting period.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `command` inside the aquifer loop, after upstream model code has updated the daily aquifer dynamics for the current timestep. Its output records feed the model's aquifer reporting files, and its monthly/yearly resets support later reporting periods and the final average-annual summary.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute the object index and accumulate the current day into the monthly sum. | The routine maps `iaq` to the corresponding object-table index with `sp_ob1%aqu + iaq - 1`, then adds the current daily aquifer state from `aqu_d(iaq)` into the monthly accumulator `aqu_m(iaq)`. |
| 2. Write daily aquifer output when daily printing is enabled. | If daily printing is active for the current day and the aquifer daily print flag is on, the routine writes the daily record to unit 2520 and, when CSV output is enabled, writes the same data to unit 2524. |
| 3. On month end, convert the monthly totals to monthly averages. | At end of month, the routine computes the number of days in the month with `ndays`, divides the monthly storage, depth-to-water, and nitrate sums by that day count, and prepares the values for monthly reporting. |
| 4. Add the monthly aquifer state into the yearly accumulator. | The monthly aquifer record is added into `aqu_y(iaq)` so the yearly totals build up across months. |
| 5. Write monthly aquifer output when monthly printing is enabled. | If monthly aquifer output is requested, the routine writes the monthly record to unit 2521 and writes the CSV version to unit 2525 when CSV output is active. |
| 6. Reset the monthly accumulator after printing. | After the monthly report is handled, the routine clears `aqu_m(iaq)` by assigning the zeroed template `aquz` so the next month starts from a clean accumulator. |
| 7. On year end, convert the yearly totals to yearly averages. | At end of year, the routine divides the yearly storage, depth-to-water, and nitrate sums by 12 to form yearly averages before reporting. |
| 8. Add the yearly aquifer state into the average-annual accumulator. | The yearly aquifer state is accumulated into `aqu_a(iaq)` so the final average-annual summary can be computed over the simulation period. |
| 9. Write yearly aquifer output when yearly printing is enabled. | If yearly aquifer output is requested, the routine writes the yearly record to unit 2522 and writes the CSV version to unit 2526 when CSV output is enabled. |
| 10. Reset the yearly accumulator after printing. | After the yearly report is complete, the routine clears `aqu_y(iaq)` by assigning `aquz` so the next year starts with a zeroed yearly accumulator. |
| 11. On simulation end, compute the average annual aquifer values. | If the simulation has ended and average-annual aquifer output is requested, the routine divides `aqu_a(iaq)` by `time%yrs_prt` to form the final average before writing it to unit 2523. |
| 12. Write average-annual CSV output when enabled. | When CSV output is active, the routine writes the average-annual aquifer record to unit 2527 in CSV form. |
| 13. Return to the caller. | The subroutine ends after the output work is complete; the format statements used by the writes are defined at the end of the routine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%aqu%d, pco%csvout, pco%aqu%m, pco%aqu%y, pco%aqu%a` |
| [sym:aquifer_module] | `aqu_m, aqu_y, aqu_d, aqu_a, aquz` | `aqu_m(iaq)%stor, aqu_m(iaq)%dep_wt, aqu_m(iaq)%no3_st, aqu_y(iaq)%stor, aqu_y(iaq)%dep_wt, aqu_y(iaq)%no3_st` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%aqu, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `aqu_m(iaq)` | Always, at the start of the routine before any printing branches. | `aqu_m(iaq)` is incremented by the current daily aquifer state so it becomes the running monthly accumulator for the current aquifer. |
| `aqu_m(iaq)%stor` | At `time%end_mo == 1`, before the monthly record is written. | `aqu_m(iaq)%stor` is divided by the number of days in the current month to convert the monthly storage sum into a monthly average. |
| `aqu_m(iaq)%dep_wt` | At `time%end_mo == 1`, before the monthly record is written. | `aqu_m(iaq)%dep_wt` is divided by the number of days in the current month to convert the monthly depth-to-water sum into a monthly average. |
| `aqu_m(iaq)%no3_st` | At `time%end_mo == 1`, before the monthly record is written. | `aqu_m(iaq)%no3_st` is divided by the number of days in the current month to convert the monthly nitrate sum into a monthly average. |
| `aqu_y(iaq)` | At `time%end_mo == 1`, after the monthly average is formed, and again at `time%end_yr == 1` when the yearly total is rolled over. | `aqu_y(iaq)` is built up from the monthly aquifer values during the year and then used as the yearly record that feeds the average-annual accumulator. |
| `aqu_y(iaq)%stor` | At `time%end_yr == 1`, before the yearly record is written. | `aqu_y(iaq)%stor` is divided by 12 to convert the yearly storage sum into a yearly average. |
| `aqu_y(iaq)%dep_wt` | At `time%end_yr == 1`, before the yearly record is written. | `aqu_y(iaq)%dep_wt` is divided by 12 to convert the yearly depth-to-water sum into a yearly average. |
| `aqu_y(iaq)%no3_st` | At `time%end_yr == 1`, before the yearly record is written. | `aqu_y(iaq)%no3_st` is divided by 12 to convert the yearly nitrate sum into a yearly average. |
| `aqu_a(iaq)` | At `time%end_sim == 1 .and. pco%aqu%a == 'y'`, after yearly accumulation has been completed. | `aqu_a(iaq)` is divided by the number of printed years to form the final average-annual aquifer state for output. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved for `aquifer_output`. The initial add in `df07e3f` introduced the subroutine, its daily/monthly/yearly/average-annual output flow, the monthly and yearly accumulator resets, and the original CSV formatting. Commit `39fabde` initialized the local variables `const` and `iob` to zero without changing the output logic. Commit `2fe89fd` updated the CSV write format on units 2524, 2525, 2526, and 2527 from `G0.3` to `G0.6` for higher-precision CSV output.

- df07e3f added the full aquifer reporting routine, including the daily, monthly, yearly, and average-annual write branches, the accumulator normalization, and the reset to `aquz` after monthly and yearly reporting.
- 39fabde only changed local initialization by setting `const = 0.` and `iob = 0`; the reporting behavior remained the same.
- 2fe89fd changed only the CSV formatting on the four CSV output units, increasing numeric precision from `G0.3` to `G0.6` while leaving the text-file writes unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'aquifer_output' has no extracted documentation comment.
