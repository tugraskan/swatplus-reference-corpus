---
kind: procedure
symbol: basin_res_pest_output
title: basin_res_pest_output
status: filled
source_hash: 5cf2289ffa0b9f93
version_label: SWAT+ 62.0.0
locals:
  ipest: Loop index for the pesticide currently being summarized and written, from 1 to `cs_db%num_pests`.
  ires: Loop index over reservoir objects, used to accumulate each reservoir’s pesticide balance
    into the basin total.
  iob: Holds the reservoir object index used to fetch the output object name from `ob(iob)%name`;
    set from `sp_ob1%res`.
  const: Temporary scaling factor used when converting monthly and yearly accumulated balances
    into period averages by dividing by the number of days in the period.
uses:
  output_ls_pesticide_module: The module is imported but no symbol from it appears in the
    extracted source lines, so it does not affect the visible logic in this routine.
  res_pesticide_module: This module provides the pesticide balance types and shared basin/reservoir
    accumulator variables that this routine updates and writes. The routine depends on `brespst_d`,
    `brespst_m`, `brespst_y`, `brespst_a`, `respst_d`, and `res_pestbz` to build daily, monthly,
    yearly, and average-annual reservoir pesticide summaries.
  plant_module: The module is imported but no plant symbol appears in the extracted source
    lines, so it does not contribute to the shown calculations or output writes.
  plant_data_module: The module is imported but no plant-data symbol appears in the extracted
    source lines, so it does not contribute to the shown calculations or output writes.
  time_module: The current simulation date and end-of-period flags control when daily, monthly,
    yearly, and end-of-simulation outputs are emitted and when accumulators are rolled forward
    or reset.
  basin_module: The basin print-code settings determine whether each output interval is active
    and whether CSV mirror files are written for the pesticide reports.
  output_landscape_module: The module is imported but no symbol from it appears in the extracted
    source lines, so it does not affect the visible output control or data accumulation.
  constituent_mass_module: This module provides the shared constituent database used to count
    pesticides and name each pesticide in the output records.
  hydrograph_module: This module supplies the reservoir object counts and reservoir object
    names needed to select the reservoir index and label each output row.
---

<!-- facts:header -->

Computes and writes basin-level pesticide balance output for reservoirs. It aggregates pesticide results across reservoir elements and emits daily, monthly, yearly, and average-annual reports when the configured print flags are enabled.

## Bottom Line

This routine summarizes basin reservoir pesticide balances for every simulated pesticide. It starts from the basin reservoir baseline value, adds reservoir-level pesticide outputs across all reservoir objects, and keeps running daily, monthly, yearly, and simulation-average totals in the basin pesticide output structures.

When the basin print configuration says to print a given interval, it writes those balances to the corresponding reservoir pesticide output files and optional CSV files. The routine is part of the basin output workflow called from `command`, so its results feed the model’s reservoir pesticide reporting rather than any downstream numerical routing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from the basin output branch of `command`, after the model has established the current time state, reservoir counts, pesticide counts, and output print codes. It depends on those upstream settings to decide whether to print daily, monthly, yearly, or average-annual reservoir pesticide balances, and its written files are used for model reporting rather than for later simulation calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the reservoir output object and loop over pesticides | The routine sets `iob` to the reservoir object index and then iterates over every pesticide in `cs_db%num_pests`. For each pesticide, it starts the daily basin balance from `res_pestbz`. |
| 2. Accumulate daily basin balance across reservoir objects | For the current pesticide, the routine loops over all reservoir objects (`1` to `sp_ob%res`) and adds each reservoir’s `respst_d(ires)%pest(ipest)` into `brespst_d%pest(ipest)`. It also accumulates the daily amount into the monthly running total `brespst_m%pest(ipest)`. |
| 3. Write daily reservoir pesticide output when daily printing is enabled | If the basin is on a daily print day and the pesticide daily print flag is on, the routine writes the daily balance to unit 2848 and, when CSV output is enabled, writes the same record to unit 2852. |
| 4. Roll monthly totals at the end of each month | At month end, the routine adds the accumulated monthly total into the yearly total, computes the number of days in the month with `ndays`, divides the monthly accumulator by that day count, writes monthly output to unit 2849 and optional CSV unit 2853, then resets the monthly accumulator to `res_pestbz`. |
| 5. Roll yearly totals at the end of each year | At year end, the routine adds the yearly running total into the average-annual accumulator, divides the yearly accumulator by `time%day_end_yr` to form an annual average, writes yearly output to unit 2850 and optional CSV unit 2854, and keeps the annual state ready for later averaging. |
| 6. Write average-annual output at simulation end and reset the accumulator | At the end of the simulation, if average-annual pesticide output is enabled, the routine divides the annual accumulator by `time%yrs_prt`, scales it by `time%days_prt`, writes the average-annual record to unit 2851 and optional CSV unit 2855, and then resets `brespst_a%pest(ipest)` to `res_pestbz`. |
| 7. Finish the pesticide loop and return | After all pesticides are processed, the routine exits the loop, returns to its caller, and ends. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `No resolved outside references were extracted from `output_ls_pesticide_module`.` |  |
| [sym:res_pesticide_module] | `brespst_d, respst_d, brespst_m, brespst_y, brespst_a, res_pestbz` | `brespst_d%pest(ipest), respst_d(ires)%pest(ipest), brespst_m%pest(ipest), brespst_y%pest(ipest), brespst_a%pest(ipest)` |
| [sym:plant_module] | `No resolved outside references were extracted from `plant_module`.` |  |
| [sym:plant_data_module] | `No resolved outside references were extracted from `plant_data_module`.` |  |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%pest%d, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:output_landscape_module] | `No resolved outside references were extracted from `output_landscape_module`.` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipest)` |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob` | `sp_ob1%res, sp_ob%res, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `brespst_d%pest(ipest)` | At every call, before any print gating, after summing `respst_d(ires)%pest(ipest)` over all reservoir objects. | `brespst_d%pest(ipest)` is rebuilt as the current-day basin pesticide balance for that pesticide, starting from `res_pestbz` and adding each reservoir’s daily pesticide output. |
| `brespst_m%pest(ipest)` | After the daily basin balance is computed for the current pesticide, before month-end checks. | `brespst_m%pest(ipest)` accumulates the current-day basin pesticide balance into the monthly running total so the month-end summary can be formed. |
| `brespst_y%pest(ipest)` | When `time%end_mo == 1`. | `brespst_y%pest(ipest)` absorbs the completed month’s total and `brespst_m%pest(ipest)` is normalized by the number of days in the month, then reset to `res_pestbz` for the next month. |
| `brespst_a%pest(ipest)` | When `time%end_yr == 1`, and again when `time%end_sim == 1` for the average-annual branch. | `brespst_a%pest(ipest)` collects the year-end total, is converted to a year-based average at simulation end using `time%yrs_prt` and `time%days_prt`, and then is reset to `res_pestbz` after the average-annual record is written. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit `df07e3f` as a new basin reservoir pesticide output subroutine. Later commits changed the implementation in two visible ways: `39fabde` initialized the local loop variables (`ipest`, `ires`, `iob`, `const`) at declaration, and `2fe89fd` changed the CSV output format for units 2852, 2853, 2854, and 2855 from `G0.3` to `G0.6` while keeping the same write targets and adding no new control flow.

- df07e3f added the full `basin_res_pest_output` routine with daily, monthly, yearly, and average-annual pesticide balance aggregation and file writes.
- 39fabde changed only local variable initialization by assigning default values directly in the declarations.
- 2fe89fd increased CSV numeric precision for the pesticide output mirror files on units 2852, 2853, 2854, and 2855.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_res_pest_output' has no extracted documentation comment.
- algorithm_steps revised: merged the original draft’s separate update/selection items into a source-aligned sequence that follows the actual loop and print branches in lines 23-97.
