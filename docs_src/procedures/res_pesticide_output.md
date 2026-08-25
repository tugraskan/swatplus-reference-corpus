---
kind: procedure
symbol: res_pesticide_output
title: res_pesticide_output
status: filled
source_hash: 74c8e43edf04f99c
version_label: SWAT+ 62.0.0
args:
  j: '`j` is the reservoir sequence index for the current reservoir output object. It selects
    which reservoir slot in the `respst_*` arrays to update and which reservoir object name/id
    to write, with the corresponding object index computed as `iob = sp_ob1%res + j - 1`.'
locals:
  ipest: Loop index over the pesticides in `cs_db%num_pests`; each pass processes one pesticide's
    daily, monthly, yearly, and average-annual balance for the current reservoir.
  iob: Reservoir object index in `ob` for the current `j`; it is derived from the first reservoir
    object offset `sp_ob1%res` so output lines can report the correct GIS id and object name.
  const: Temporary scaling factor used when converting accumulated monthly or yearly totals
    to average-per-day values. It is set from the number of days in the month or from `time%day_end_yr`,
    then used in the division-like normalization expressions.
uses:
  output_ls_pesticide_module: '`output_ls_pesticide_module` is imported by the routine, so
    it is part of the output-side dependency set that must be present for this reservoir pesticide
    reporting procedure to compile and run, even though no specific symbols from it were extracted
    here.'
  res_pesticide_module: '`res_pesticide_module` owns the summary arrays and baseline reset
    value that this routine updates and prints. The monthly, yearly, and average-annual pesticide
    balances are stored in `respst_m`, `respst_y`, and `respst_a`, and each period is reset
    to `res_pestbz` after it is finalized.'
  plant_module: '`plant_module` is imported here as part of the reservoir pesticide output
    environment, but the extracted source does not show any direct symbol use from it. Its
    presence matters only because this routine is compiled within the broader plant/reservoir
    reporting set.'
  plant_data_module: '`plant_data_module` is imported as part of the same reporting stack,
    but the extracted source shows no direct reference to its symbols inside this routine.
    It matters because the procedure is built in the model''s shared plant-data/reporting
    context.'
  time_module: '`time_module` provides the simulation clock and end-of-period flags that control
    every output branch here. The routine only writes the daily, monthly, yearly, or average-annual
    records when `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `time%end_mo`, `time%end_yr`,
    `time%end_sim`, `time%yrs_prt`, and `time%days_prt` indicate the appropriate reporting
    moment.'
  basin_module: '`basin_module` supplies the print-control structure `pco`, which gates whether
    each reporting interval is active and whether CSV duplicates are also written. Without
    `pco%day_print`, `pco%int_day_cur`, `pco%int_day`, `pco%pest%d`, `pco%pest%m`, `pco%pest%y`,
    `pco%pest%a`, and `pco%csvout`, the routine would not know which reservoir pesticide outputs
    to emit.'
  output_landscape_module: '`output_landscape_module` is imported alongside the output routines,
    so it is part of the surrounding output infrastructure for this procedure even though
    no direct symbols from it were extracted. That matters because this routine writes landscape-style
    reservoir output records.'
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_pests` for the pesticide
    loop and `cs_db%pests(ipest)` for the human-readable pesticide name written to each record.
    It tells the routine how many pesticide outputs exist and how to label them.'
  hydrograph_module: '`hydrograph_module` provides the reservoir object index base `sp_ob1%res`
    and the object array `ob`, which are needed to locate the correct reservoir entry and
    write its GIS id and name on each output line.'
---

<!-- facts:header -->

Writes reservoir pesticide balance outputs for each reservoir object and each simulated pesticide. It emits daily, monthly, yearly, and average-annual records when the corresponding print flags are enabled.

## Bottom Line

`res_pesticide_output` loops over reservoir objects (`j = 1, sp_ob%res`) and pesticides (`ipest = 1, cs_db%num_pests`) to publish reservoir pesticide balance results. It uses the current simulation time, reservoir identity, and the pesticide name database to format output rows for the active reporting intervals.

For each pesticide it accumulates daily values into monthly, yearly, and average-annual summary states, then writes those summaries to the reservoir pesticide output units when the print controls in `pco` request them. At month-end and simulation-end it also resets the running totals so the next accumulation period starts cleanly.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after reservoir outputs have been prepared and for each reservoir index `j` while total constituents are present (`cs_db%num_tot > 0`). It sits in the reservoir reporting path and turns the accumulated pesticide balance states into daily, monthly, yearly, and end-of-simulation output files that downstream postprocessing and users rely on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute the reservoir object index | The routine maps the reservoir sequence index `j` to the corresponding object index `iob` using the first reservoir object offset `sp_ob1%res`. This selects the correct reservoir metadata for the output row. |
| 2. Loop over all pesticides | The routine iterates from pesticide 1 through `cs_db%num_pests`, processing each pesticide balance separately for the current reservoir. |
| 3. Accumulate the daily balance into the month total | For each pesticide, the daily reservoir pesticide balance `respst_d(j)%pest(ipest)` is added into the running monthly summary `respst_m(j)%pest(ipest)`. |
| 4. Optionally write daily pesticide output | When daily printing is enabled by `pco%day_print` and the day interval matches `pco%int_day_cur == pco%int_day`, the routine writes a daily record to unit 2816 and, if CSV output is enabled, duplicates it to unit 2820. |
| 5. At month end, roll monthly totals into yearly totals | When `time%end_mo == 1`, the routine adds the completed monthly total into `respst_y(j)%pest(ipest)`, computes the number of days in the month as `const`, and normalizes the monthly summary by dividing through that day count. |
| 6. Optionally write monthly pesticide output | If monthly pesticide output is enabled with `pco%pest%m == "y"`, the routine writes the month-end record to unit 2817 and, when CSV output is enabled, to unit 2821. |
| 7. Reset the monthly accumulator | After the month-end record is handled, the routine resets `respst_m(j)%pest(ipest)` to `res_pestbz` so the next month starts from a clean baseline. |
| 8. At year end, roll yearly totals into average-annual totals | When `time%end_yr == 1`, the routine adds the completed yearly total into `respst_a(j)%pest(ipest)`, sets `const` to `time%day_end_yr`, and normalizes the yearly summary by that value. |
| 9. Optionally write yearly pesticide output | If yearly pesticide output is enabled with `pco%pest%y == "y"`, the routine writes the year-end record to unit 2818 and, when CSV output is enabled, to unit 2822. |
| 10. At simulation end, write average-annual output and reset the annual state | When `time%end_sim == 1` and average-annual output is enabled with `pco%pest%a == "y"`, the routine converts `respst_a(j)%pest(ipest)` to an average using `time%yrs_prt` and `time%days_prt`, writes the final record to unit 2819 and optionally to 2823, then resets `respst_a(j)%pest(ipest)` to `res_pestbz`. |
| 11. Return after finishing all pesticides | After all pesticides are processed, the routine exits with `return` and ends the subroutine. |
| 12. Format output records | The shared format label 100 defines the fixed-width output layout used by the non-CSV writes to units 2816, 2817, 2818, and 2819. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `No candidate outside references were resolved to `output_ls_pesticide_module` in the context packet.` | `No resolved components were provided for `output_ls_pesticide_module` in the context packet.` |
| [sym:res_pesticide_module] | `respst_m, respst_d, respst_y, respst_a, res_pestbz` | `respst_m(j)%pest(ipest), respst_d(j)%pest(ipest), respst_y(j)%pest(ipest), respst_a(j)%pest(ipest)` |
| [sym:plant_module] | `No candidate outside references were resolved to `plant_module` in the context packet.` | `No resolved components were provided for `plant_module` in the context packet.` |
| [sym:plant_data_module] | `No candidate outside references were resolved to `plant_data_module` in the context packet.` | `No resolved components were provided for `plant_data_module` in the context packet.` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%pest%d, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:output_landscape_module] | `No candidate outside references were resolved to `output_landscape_module` in the context packet.` | `No resolved components were provided for `output_landscape_module` in the context packet.` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipest)` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%res, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `respst_m(j)%pest(ipest)` | Each pesticide loop iteration starts by adding the current daily balance to the running monthly accumulator. | This monthly summary grows during the month by collecting each day's reservoir pesticide balance before month-end output and normalization. |
| `respst_y(j)%pest(ipest)` | When `time%end_mo == 1`, after the monthly total is added to the yearly summary and normalized by the month length. | This yearly summary stores the accumulated monthly pesticide balance for the reservoir and is used as the source for year-end reporting and average-annual aggregation. |
| `respst_a(j)%pest(ipest)` | When `time%end_sim == 1` and average-annual output is requested, after the final average is written. | This average-annual summary is converted to a per-day/per-year average for final output and then reset to the baseline value so the summary state does not persist beyond the report. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits affected `res_pesticide_output`. The initial addition in `df07e3f` introduced the routine and its daily, monthly, yearly, and average-annual pesticide output logic. Commit `39fabde` initialized the local variables `ipest`, `iob`, and `const` to zero values. Commit `2fe89fd` changed the CSV writes from `G0.3` to `G0.6` precision and kept the end-of-simulation reset of `respst_a(j)%pest(ipest)` after the average-annual record is written.

- Added the reservoir pesticide reporting subroutine with the current loop structure, output gating, accumulation, and reset behavior.
- Initialized the local loop/index/temporary variables to avoid uninitialized use.
- Increased CSV output numeric precision for the daily, monthly, yearly, and average-annual pesticide records from `G0.3` to `G0.6`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_pesticide_output' has no extracted documentation comment.
- algorithm_steps revised: reordered steps to follow the source flow more closely and split record formatting into its own step.
- `plant_module`, `plant_data_module`, and `output_ls_pesticide_module` had no resolved symbol references in the context packet; their descriptions are based on import presence only.
- Source uses `//` in numeric-looking assignments (`respst_m`, `respst_y`, `respst_a`); the surrounding lineage diff shows this is existing source text, but its exact intent is uncertain from the extracted packet alone.
