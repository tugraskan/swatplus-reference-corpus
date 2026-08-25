---
kind: procedure
symbol: aqu_pesticide_output
title: aqu_pesticide_output
status: filled
source_hash: 15155d7975e4d8de
version_label: SWAT+ 62.0.0
args:
  j: '`j` selects which aquifer object in the sequential aquifer output arrays is being processed.
    The routine maps that index to the actual aquifer object with `iob = sp_ob1%aqu + j -
    1` and then updates and prints pesticide summaries for that object.'
locals:
  ipest: 'Loop index over pesticides. It runs from 1 to `cs_db%num_pests` so the routine can
    process every simulated pesticide for the current aquifer object. Initial value: `0`.'
  iob: 'Derived aquifer object index used to look up object metadata such as `ob(iob)%gis_id`
    and `ob(iob)%name`. It is computed from the first aquifer object offset and the caller’s
    sequential index. Initial value: `0`.'
  const: 'A time-length factor used when converting the monthly or yearly accumulated pesticide
    totals into averaged values. For monthly output it is set from the number of days in the
    month; for yearly output it is set from `time%day_end_yr`. Initial value: `0.`.'
  stor_init: 'Temporary holder for the pesticide ending storage at the end of a time step.
    The routine uses it to seed the next period’s `stor_init` after resetting the monthly
    or yearly accumulator. Initial value: `0.`.'
uses:
  output_ls_pesticide_module: This module is referenced by the routine, so its public output
    definitions and any associated landscape pesticide output state are part of the compile-time
    dependency set even though no specific symbols were resolved from it in the packet.
  aqu_pesticide_module: '`aqu_pesticide_module` provides the shared pesticide accumulator
    types and the saved arrays (`aqupst_d`, `aqupst_m`, `aqupst_y`, `aqupst_a`, and `aqu_pestbz`)
    that this routine reads, updates, resets, and writes. Without that module, the routine
    would have no storage for the daily/monthly/yearly/average-annual pesticide summaries
    it reports.'
  plant_module: '`plant_module` is listed as a dependency, but the extracted source for this
    routine does not show any direct references to plant-state symbols. It still matters because
    the subroutine compiles in a broader landscape/HRU output context where plant-related
    modules may supply shared interfaces or derived types used by surrounding code.'
  plant_data_module: '`plant_data_module` is also a compile-time dependency, but no direct
    symbol use was extracted in this routine. It matters because the output routine is part
    of a landscape reporting family that is built alongside plant and crop data handling.'
  time_module: '`time_module` supplies all timestamp and period-boundary flags used to decide
    when to write daily, monthly, yearly, and end-of-simulation pesticide summaries. The routine
    depends on `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `time%end_mo`, `time%end_yr`,
    `time%day_end_yr`, `time%end_sim`, `time%yrs_prt`, and `time%days_prt` to label output
    and to trigger period rollups.'
  basin_module: '`basin_module` provides the print control structure `pco`, which gates whether
    each output class is emitted and whether CSV duplicates are written. The routine uses
    those flags to decide if daily, monthly, yearly, and average-annual pesticide records
    should be printed at all.'
  output_landscape_module: This module is imported as part of the landscape output subsystem,
    so it matters to the routine’s output placement even though no direct symbol references
    were extracted from it in the source snippet.
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_pests` for the pesticide
    loop bound and `cs_db%pests(ipest)` for the pesticide name written to every record. That
    module is what lets the routine iterate over the simulated pesticide list and label each
    output row correctly.'
  hydrograph_module: '`hydrograph_module` provides the aquifer object offset (`sp_ob1%aqu`)
    and object metadata (`ob(iob)%name`, plus `ob(iob)%gis_id` from the same object table)
    needed to associate each output row with the correct aquifer object. The routine cannot
    produce object-labeled output without that mapping.'
---

<!-- facts:header -->

Writes aquifer pesticide balance outputs for each pesticide in each aquifer object. It reports daily, monthly, yearly, and average-annual summaries depending on print settings.

## Bottom Line

For each aquifer object index `j`, this subroutine walks through every simulated pesticide and updates the running monthly, yearly, and average-annual summary records from the current day’s aquifer pesticide balance state.

It then writes those summaries to the configured text output units, with optional CSV-formatted duplicates when `pco%csvout` is enabled. The results are the aquifer pesticide output tables used by the SWAT+ reporting workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` during aquifer output processing, after the model has already populated the aquifer pesticide balance arrays and print-control state for the current timestep. Its results feed the SWAT+ output files for daily, monthly, yearly, and average-annual aquifer pesticide reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the sequential aquifer index to the object table | The routine converts the caller’s aquifer sequence index `j` into the actual object index `iob` using the first aquifer offset `sp_ob1%aqu`. That lets the output records use the right aquifer name and GIS identifier. |
| 2. Loop over simulated pesticides | The routine iterates from pesticide 1 through `cs_db%num_pests`, so every simulated pesticide associated with the aquifer object is handled in turn. |
| 3. Accumulate daily totals into the monthly bucket | Each pesticide’s current daily balance `aqupst_d(j)%pest(ipest)` is added into the running monthly summary `aqupst_m(j)%pest(ipest)` before any period-boundary checks occur. |
| 4. Write daily pesticide output when the day-print gate is open | If daily printing is enabled and the current print interval matches, the routine writes the daily pesticide balance to unit 3008 and optionally duplicates it to unit 3012 in CSV form. |
| 5. Roll monthly totals at month end | When `time%end_mo == 1`, the routine adds the monthly bucket to the yearly bucket, converts the monthly total to an average using the month length in `const`, stores the current ending storage, optionally writes monthly output, then resets the monthly accumulator to `aqu_pestbz` and seeds its `stor_init` from the day-end storage. |
| 6. Accumulate yearly totals and print year-end output | When `time%end_yr == 1`, the routine adds the yearly bucket into the average-annual bucket, scales the yearly bucket by the year length in `const`, records the current ending storage, optionally writes yearly output, then resets the yearly accumulator and stores the next period’s initial storage. |
| 7. Produce average-annual output at end of simulation | At the end of the simulation, if average-annual printing is enabled, the routine divides the average-annual bucket by `time%yrs_prt`, scales it by `time%days_prt`, stores the final ending storage, and writes the average-annual record to unit 3011 with an optional CSV duplicate on unit 3015. |
| 8. Finish pesticide loop and return | After all pesticides are processed for the aquifer object, the routine exits the loop and returns to its caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `No specific imported symbols were resolved for this module in the provided evidence.` | `No specific imported symbols were resolved for this module in the provided evidence.` |
| [sym:aqu_pesticide_module] | `aqupst_m, aqupst_d, aqupst_y, aqupst_a, aqu_pestbz` | `aqupst_m(j)%pest(ipest), aqupst_d(j)%pest(ipest), aqupst_y(j)%pest(ipest), aqupst_m(j)%pest(ipest)%stor_final, aqupst_d(j)%pest(ipest)%stor_final, aqupst_m(j)%pest(ipest)%stor_init, aqupst_a(j)%pest(ipest), aqupst_y(j)%pest(ipest)%stor_final, aqupst_y(j)%pest(ipest)%stor_init, aqupst_a(j)%pest(ipest)%stor_final` |
| [sym:plant_module] | `No specific imported symbols were resolved for this module in the provided evidence.` | `No specific imported symbols were resolved for this module in the provided evidence.` |
| [sym:plant_data_module] | `No specific imported symbols were resolved for this module in the provided evidence.` | `No specific imported symbols were resolved for this module in the provided evidence.` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%pest%d, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:output_landscape_module] | `No specific imported symbols were resolved for this module in the provided evidence.` | `No specific imported symbols were resolved for this module in the provided evidence.` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipest)` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%aqu, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `aqupst_m(j)%pest(ipest)` | `aqupst_m(j)%pest(ipest)` changes every loop iteration before the print checks, because the routine adds the current daily aquifer pesticide balance into the monthly accumulator. | This state stores the running monthly pesticide balance for aquifer object `j` and pesticide `ipest`. It is updated continuously so the month-end output can report the accumulated period total before the accumulator is reset. |
| `aqupst_y(j)%pest(ipest)` | `time%end_mo == 1`. | At the end of each month, the monthly accumulator is added into the yearly accumulator so the year-to-date pesticide summary includes the completed month. |
| `aqupst_m(j)%pest(ipest)%stor_final` | `time%end_mo == 1` after the monthly summary has been written or skipped. | The monthly bucket’s `stor_final` is copied from the current day’s ending storage so the monthly summary reflects the storage state at month close. |
| `aqupst_m(j)%pest(ipest)%stor_init` | `time%end_mo == 1` immediately before the monthly bucket is reset. | The routine saves the current day-end storage into `stor_init` so the next monthly period starts from the correct initial pesticide storage after the accumulator is cleared. |
| `aqupst_a(j)%pest(ipest)` | `time%end_yr == 1`. | At year end, the yearly accumulator is added into the average-annual accumulator so the simulation-wide annual summary can be formed. |
| `aqupst_y(j)%pest(ipest)%stor_final` | `time%end_yr == 1` after yearly accumulation and scaling. | The yearly bucket’s ending storage is set from the current day’s aquifer storage so the annual output record carries the correct final storage value. |
| `aqupst_y(j)%pest(ipest)%stor_init` | `time%end_yr == 1` immediately before the yearly bucket is reset. | The routine stores the current day-end storage as the next yearly period’s initial storage after the accumulator is cleared to `aqu_pestbz`. |
| `aqupst_a(j)%pest(ipest)%stor_final` | `time%end_sim == 1 .and. pco%pest%a == 'y'`. | At the end of the simulation, the average-annual bucket’s ending storage is set from the current day’s aquifer storage so the final average-annual record reports the correct final state. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved. `df07e3f` added `aqu_pesticide_output.f90` with the full aquifer pesticide reporting loop and all daily, monthly, yearly, and average-annual write branches. `39fabde` only changed local variable initialization in this routine, setting `ipest`, `iob`, `const`, and `stor_init` to zero/default values. `2fe89fd` changed only the CSV output formats on units 3012, 3013, 3014, and 3015 from `G0.3` to `G0.6`.

- df07e3f introduced the routine and its complete aquifer pesticide output workflow, including accumulation, period-end resets, and file writes.
- 39fabde made the local loop/index and temporary storage variables explicitly initialized, without changing the output logic.
- 2fe89fd increased CSV numeric precision for the daily, monthly, yearly, and average-annual pesticide CSV outputs.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'aqu_pesticide_output' has no extracted documentation comment.
- algorithm_steps revised: reordered and split the original draft into source-matched execution phases; source_lines now cite only visible line ranges from the provided source block.
- `output_ls_pesticide_module`, `plant_module`, and `plant_data_module` were imported but no direct symbol references were resolved in the context packet; their descriptions are therefore conservative.
- The source shows `ob(iob)%gis_id` is written, but the ownership table in the packet did not provide a component breakdown for that field; the description relies on the visible source use.
