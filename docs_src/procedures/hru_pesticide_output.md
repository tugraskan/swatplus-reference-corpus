---
kind: procedure
symbol: hru_pesticide_output
title: hru_pesticide_output
status: filled
source_hash: a0f4cb221a5dcc0f
version_label: SWAT+ 62.0.0
args:
  ihru: '`ihru` is the HRU index passed in by the caller; the routine copies it to `j` and
    uses it to select the correct HRU balance arrays (`hpestb_* (j)`) and the matching object
    connectivity record (`ob(iob)`).'
locals:
  ipest: Loop index over pesticide entries; the routine runs from `1` to `cs_db%num_pests`
    so each simulated pesticide is processed in turn.
  j: Local HRU index derived from `ihru`; used to index the HRU pesticide balance arrays for
    the current object.
  iob: Index of the corresponding hydrograph/object connectivity record for this HRU, computed
    as `sp_ob1%hru + j - 1` so the output can print the object GIS ID and name.
  const: Conversion factor used when closing monthly and yearly summaries; it stores the number
    of days in the reporting span before the accumulated balance is normalized with division
    and re-scaling.
uses:
  output_ls_pesticide_module: '`output_ls_pesticide_module` provides the per-HRU pesticide
    balance structures (`hpestb_d`, `hpestb_m`, `hpestb_y`, `hpestb_a`) and the zeroed template
    `pestbz`. This routine reads the current daily balance, accumulates it into period totals,
    writes those totals, and then resets the arrays back to the zero template.'
  plant_module: '`plant_module` is imported by the routine, but the extracted source lines
    do not show any direct symbol from it being used. It still matters because the routine
    is part of the plant/HRU output stack and may depend on plant-state declarations in the
    full source context beyond the extracted references.'
  plant_data_module: '`plant_data_module` is imported by the routine, but no resolved symbol
    from that module appears in the extracted body. It matters here as supporting plant/HRU
    data context for the broader output routine, even though the visible lines do not name
    a specific field.'
  time_module: '`time_module` supplies the current simulation calendar and end-of-period flags
    that gate every report branch. The routine uses the day/month/year stamps for each record
    and uses `end_mo`, `end_yr`, `end_sim`, `yrs_prt`, and `days_prt` to decide when to aggregate,
    normalize, print, and reset the monthly, yearly, and average-annual pesticide totals.'
  basin_module: '`basin_module` provides the print-control flags that turn pesticide output
    on or off for each time scale. `pco%day_print`, `pco%int_day_cur`, and `pco%int_day` gate
    daily output timing, while `pco%pest%d`, `pco%pest%m`, `pco%pest%y`, `pco%pest%a`, and
    `pco%csvout` decide whether the routine writes the standard and CSV records.'
  output_landscape_module: '`output_landscape_module` is imported but no explicit symbol from
    it appears in the extracted lines. It likely participates in the broader landscape output
    framework that this HRU routine belongs to, even though the visible code does not directly
    reference one of its named objects.'
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_pests` to bound
    the pesticide loop and `cs_db%pests(ipest)` to print the pesticide name/label alongside
    each balance value. Without that database the routine would not know how many pesticides
    to iterate over or how to identify them in the output files.'
  hydrograph_module: '`hydrograph_module` supplies the HRU-to-object mapping and the object
    metadata used in each output record. `sp_ob1%hru` establishes the starting HRU offset
    for `iob`, and `ob(iob)%name`/`ob(iob)%gis_id` provide the object identity fields written
    to the report rows.'
---

<!-- facts:header -->

Writes HRU pesticide balance output for each simulated pesticide at daily, monthly, yearly, and average-annual reporting points. It records the HRU/object identifiers plus the current balance totals to fixed output units and optional CSV units.

## Bottom Line

`hru_pesticide_output` is the HRU-level pesticide reporting routine. For each pesticide in `cs_db%num_pests`, it gathers the current HRU object indices, checks the active print flags in `pco`, and writes daily, monthly, yearly, and average-annual pesticide balance records to the configured output units.

It also rolls balances forward between time periods: daily pesticide mass contributes to the monthly total, monthly total contributes to the yearly total, and yearly total contributes to the average-annual total. At each period boundary it emits the corresponding report and then resets the accumulated balance back to `pestbz` for the next interval.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs whenever `command` is processing an HRU with pesticides available (`cs_db%num_tot > 0`). `command` passes in `ihru`, and `hru_pesticide_output` then uses the current simulation time and print-control settings to emit the HRU pesticide balances that downstream output files and post-processing depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the caller’s HRU index to local object indices. | Copy `ihru` to `j` and compute `iob = sp_ob1%hru + j - 1` so the routine can index the HRU balance arrays and the corresponding object metadata. |
| 2. Loop over each simulated pesticide. | Iterate `ipest` from 1 through `cs_db%num_pests` and add the current daily pesticide balance into the monthly accumulator. |
| 3. Write daily pesticide output when daily printing is enabled. | If `pco%day_print` and `pco%int_day_cur` match the daily print schedule and `pco%pest%d == "y"`, write the daily balance to unit 2800 and, if requested, to CSV unit 2804. |
| 4. Close the month, normalize monthly totals, print, and reset monthly state. | At `time%end_mo == 1`, add the monthly total into `hpestb_y`, compute the month-length factor in `const`, scale the monthly balance, write monthly output to units 2801 and 2805 when enabled, and reset `hpestb_m` to `pestbz`. |
| 5. Close the year, normalize yearly totals, print, and reset yearly state. | At `time%end_yr == 1`, add the yearly accumulator into `hpestb_a`, scale the yearly balance by `time%day_end_yr`, write yearly output to units 2802 and 2806 when enabled, and leave the yearly accumulator ready for reuse. |
| 6. Compute and print average-annual output at simulation end. | At `time%end_sim == 1` and when `pco%pest%a == "y"`, divide the annual accumulator by `time%yrs_prt`, scale by `time%days_prt`, write the average-annual record to units 2803 and 2807, and reset `hpestb_a` to `pestbz`. |
| 7. Finish the pesticide loop and return to caller. | After all pesticides are processed, exit the loop and return to the caller; the format statement at label 100 supplies the shared non-CSV record layout. |
| 8. Normalize monthly balance to a daily-equivalent value. | Accumulate monthly totals into yearly totals, compute the number of days in the current month span, and divide the monthly balance by that day count before output. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `hpestb_m, hpestb_d, hpestb_y, hpestb_a, pestbz` | `hpestb_m(j)%pest(ipest), hpestb_d(j)%pest(ipest), hpestb_y(j)%pest(ipest), hpestb_a(j)%pest(ipest)` |
| [sym:plant_module] | `plant_module` | `No candidate outside references were resolved to `plant_module` in the context packet.` |
| [sym:plant_data_module] | `plant_data_module` | `No candidate outside references were resolved to `plant_data_module` in the context packet.` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%pest%d, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:output_landscape_module] | `output_landscape_module` | `No candidate outside references were resolved to `output_landscape_module` in the context packet.` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipest)` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%hru, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpestb_m(j)%pest(ipest)` | When `time%end_mo == 1` after the monthly accumulation step. | The monthly pesticide balance is first added into the yearly accumulator, then converted to a day-normalized monthly value for output, and finally reset to the zero template `pestbz` so the next month starts clean. |
| `hpestb_y(j)%pest(ipest)` | When `time%end_yr == 1` after the yearly accumulation step. | The monthly accumulator has already been rolled into the yearly total, and the yearly balance is then scaled to a daily-equivalent value for yearly reporting. |
| `hpestb_a(j)%pest(ipest)` | When `time%end_sim == 1` and average-annual output is enabled with `pco%pest%a == "y"`. | The accumulated annual pesticide balance is converted to an average-annual value for final reporting and then reset to `pestbz` so the stored state does not carry forward past the simulation end. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show the routine was added in `df07e3f` with the current HRU pesticide output workflow, then later modified by `35b029c` to increase the format width from 14 to 16 exponential fields, `39fabde` to initialize local scalars `ipest`, `j`, `iob`, and `const`, and `2fe89fd` to switch the CSV writes from `G0.3` to `G0.6` precision and keep the averaging/reset logic intact.

- `df07e3f` introduced `hru_pesticide_output` with daily, monthly, yearly, and average-annual pesticide balance writes plus the month/year/simulation accumulation-and-reset structure.
- `35b029c` changed the shared format statement from 14 to 16 `e12.4` fields so the standard output could carry the full record payload.
- `39fabde` initialized the local working variables (`ipest`, `j`, `iob`, `const`) at declaration time but did not alter the output algorithm.
- `2fe89fd` increased CSV numeric precision from `G0.3` to `G0.6` for all four CSV output units, leaving the accumulation and reset behavior unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_pesticide_output' has no extracted documentation comment.
- algorithm_steps revised: reordered and expanded to match the visible source flow and added the month-end normalization step.
- Source shows `plant_module` and `output_landscape_module` are imported but no resolved symbols from them appear in the extracted body; their exact runtime role is therefore uncertain from this packet alone.
