---
kind: procedure
symbol: basin_aqu_pest_output
title: basin_aqu_pest_output
status: filled
source_hash: ab819e2cb8ed4db3
version_label: SWAT+ 62.0.0
locals:
  ipest: '`ipest` is the pesticide index used to loop over all simulated pesticides in `cs_db%num_pests`
    and select the matching element in each output structure.'
  iaq: '`iaq` is the aquifer-object index used to step through all aquifer instances in `sp_ob%aqu`
    when summing daily pesticide results.'
  iob: '`iob` stores the object index for the basin aquifer output target, set from `sp_ob1%aqu`
    and then used to fetch `ob(iob)%name` for the output record label.'
  const: '`const` is a temporary conversion factor used when normalizing monthly and yearly
    totals by the number of days in the period.'
  stor_init: '`stor_init` holds the starting storage value copied from `baqupst_d%pest(ipest)%stor_final`
    so the monthly and yearly output objects can be reset with the correct initial pesticide
    storage after each period closes.'
uses:
  output_ls_pesticide_module: '`output_ls_pesticide_module` is imported in the source, so
    it is part of the routine''s dependency set, but the provided context does not show any
    directly used symbols from that module.'
  aqu_pesticide_module: '`aqu_pesticide_module` provides the pesticide process and output
    types that this routine reads, accumulates, resets, and writes. The basin-level outputs
    `baqupst_d`, `baqupst_m`, `baqupst_y`, and `baqupst_a`, along with `aqupst_d` and `aqu_pestbz`,
    are the core state objects this routine updates.'
  plant_module: '`plant_module` is imported by the source, but the extracted lines do not
    show a direct plant symbol use inside this routine. It remains a declared dependency of
    the compilation unit.'
  plant_data_module: '`plant_data_module` is also imported without any extracted direct symbol
    use here. It matters only as a compilation dependency in the supplied evidence.'
  time_module: '`time_module` supplies the calendar and period-end flags that gate each output
    branch. The routine uses these values to decide whether to write daily, monthly, yearly,
    or average-annual pesticide summaries and to stamp each record with the current date.'
  basin_module: '`basin_module` provides `pco`, the print-control structure. Its day, month,
    year, average-annual, and CSV switches determine which pesticide output files are written
    at each point in the simulation.'
  output_landscape_module: '`output_landscape_module` is imported in the source but no direct
    symbols from it are visible in the extracted lines. It is therefore a declared dependency
    without a shown in-routine use.'
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_pests` for the loop
    bound and `cs_db%pests(ipest)` for the pesticide name written into each record. Without
    this database the routine could not iterate over or label the pesticide outputs.'
  hydrograph_module: '`hydrograph_module` provides the aquifer count and object naming used
    to drive the loops and label the records. `sp_ob%aqu` sets how many aquifer objects are
    aggregated, `sp_ob1%aqu` identifies the basin aquifer object index, and `ob(iob)%name`
    is written to each output line.'
---

<!-- facts:header -->

Writes basin-level aquifer pesticide balance summaries to the standard pesticide output files. It aggregates daily pesticide process states across aquifer objects, then emits daily, monthly, yearly, and average-annual records when the configured print flags are enabled.

## Bottom Line

`basin_aqu_pest_output` is the basin-level pesticide reporting routine for aquifer objects. It loops over every simulated pesticide and every aquifer, combines the per-aquifer daily pesticide process totals into basin summaries, and carries those summaries forward into month, year, and simulation-average accumulators.

The routine matters because it is the point where aquifer pesticide mass-balance state is both reset for the next time step and written to output files. Its records are controlled by `pco` print switches and simulation time flags, so downstream documentation and diagnostics depend on these writes being aligned with the model calendar.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model's output phase after the daily aquifer pesticide process arrays have been populated for the current time step. `command` calls it when aquifer objects and pesticide constituents exist, and later model reporting depends on the records it writes plus the monthly, yearly, and average-annual accumulators it updates.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Identify the basin aquifer output object and begin the pesticide loop. | The routine sets `iob` from `sp_ob1%aqu`, then loops over every pesticide index from 1 to `cs_db%num_pests` so it can build a separate basin summary for each pesticide. |
| 2. Build the daily basin pesticide balance. | For each pesticide, the routine initializes `baqupst_d%pest(ipest)` from `aqu_pestbz`, then adds each aquifer object's daily pesticide state from `aqupst_d(iaq)%pest(ipest)` across `sp_ob%aqu`. After each addition it resets that aquifer object's `stor_init` to its `stor_final` so the next time step starts from the new ending storage. |
| 3. Accumulate daily totals into the monthly basin state. | The daily basin pesticide balance is added into the monthly accumulator `baqupst_m%pest(ipest)` so the month-end summary can be formed later. |
| 4. Write daily pesticide output when daily printing is enabled. | If daily printing is enabled in `pco` and the current day matches the configured print interval, the routine writes a daily pesticide balance record to unit 3000 and, if CSV output is enabled, writes the CSV companion record to unit 3004. |
| 5. Close out the month when the simulation day marks month end. | At month end, the routine adds the monthly state into the yearly accumulator, normalizes the monthly total by the number of days in the month, copies the ending daily storage into the monthly `stor_final`, writes monthly output when enabled, then resets the monthly accumulator to `aqu_pestbz` and stores the correct `stor_init` for the next month. |
| 6. Close out the year when the simulation day marks year end. | At year end, the routine adds the yearly state into the average-annual accumulator, scales the yearly total by `time%day_end_yr`, copies the ending daily storage into the yearly `stor_final`, writes yearly output when enabled, then resets the yearly accumulator and its `stor_init` for the next year. |
| 7. Produce the average-annual end-of-simulation pesticide record. | At the end of the simulation, the routine converts the accumulated average-annual total to a mean using `time%yrs_prt` and `time%days_prt`, copies the final daily storage into the average-annual `stor_final`, writes the final summary to unit 3003 and optional CSV unit 3007, then resets the average-annual accumulator. |
| 8. Finish the pesticide loop and return. | After all pesticide indices are processed, the routine exits the loop and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `No candidate outside references were resolved to `output_ls_pesticide_module` in the context packet.` |  |
| [sym:aqu_pesticide_module] | `baqupst_d, aqupst_d, baqupst_m, baqupst_y, baqupst_a, aqu_pestbz` | `baqupst_d%pest(ipest), aqupst_d(iaq)%pest(ipest), aqupst_d(iaq)%pest(ipest)%stor_init, aqupst_d(iaq)%pest(ipest)%stor_final, baqupst_m%pest(ipest), baqupst_y%pest(ipest), baqupst_m%pest(ipest)%stor_final, baqupst_d%pest(ipest)%stor_final, baqupst_m%pest(ipest)%stor_init, baqupst_a%pest(ipest), baqupst_y%pest(ipest)%stor_final, baqupst_y%pest(ipest)%stor_init, baqupst_a%pest(ipest)%stor_final` |
| [sym:plant_module] | `No candidate outside references were resolved to `plant_module` in the context packet.` |  |
| [sym:plant_data_module] | `No candidate outside references were resolved to `plant_data_module` in the context packet.` |  |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%yrs_prt, time%days_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%pest%d, pco%csvout, pco%pest%m, pco%pest%y, pco%pest%a` |
| [sym:output_landscape_module] | `No candidate outside references were resolved to `output_landscape_module` in the context packet.` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipest)` |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob` | `sp_ob1%aqu, sp_ob%aqu, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `baqupst_d%pest(ipest)` | For every pesticide index at the start of the daily balance calculation. | `baqupst_d%pest(ipest)` is rebuilt from the zeroed pesticide balance object and then updated with the summed daily aquifer pesticide processes for the current time step. |
| `aqupst_d(iaq)%pest(ipest)%stor_init` | Inside the aquifer loop for each pesticide, once that aquifer's daily contribution has been included. | `aqupst_d(iaq)%pest(ipest)%stor_init` is advanced to the current `stor_final` so the next time step begins with the correct starting storage for that aquifer and pesticide. |
| `baqupst_m%pest(ipest)` | At every simulated day, after the daily basin balance has been assembled. | `baqupst_m%pest(ipest)` accumulates the day's basin pesticide balance so month-end reporting can summarize the whole month. |
| `baqupst_y%pest(ipest)` | At year end, after the monthly accumulator has been transferred to the annual accumulator. | `baqupst_y%pest(ipest)` accumulates the year-level pesticide balance so the simulation-average output can be formed at the end of the run. |
| `baqupst_m%pest(ipest)%stor_final` | Only when `time%end_mo == 1`. | `baqupst_m%pest(ipest)%stor_final` is set to the current daily ending storage so the month-end record reports the correct terminal pesticide storage. |
| `baqupst_m%pest(ipest)%stor_init` | Only when `time%end_mo == 1`, after the month-end output is written. | `baqupst_m%pest(ipest)%stor_init` is reset from `stor_init`, which was captured from the daily balance ending storage, so the next month starts from the correct initial storage value. |
| `baqupst_a%pest(ipest)` | Only when `time%end_yr == 1`. | `baqupst_a%pest(ipest)` accumulates the yearly summary into the average-annual total that will be normalized at the end of the simulation. |
| `baqupst_y%pest(ipest)%stor_final` | Only when `time%end_yr == 1`. | `baqupst_y%pest(ipest)%stor_final` is updated from the daily ending storage so the year-end summary carries the correct terminal storage. |
| `baqupst_y%pest(ipest)%stor_init` | Only when `time%end_yr == 1`, after yearly output is written. | `baqupst_y%pest(ipest)%stor_init` is reset for the next year using the captured ending storage from the daily balance. |
| `baqupst_a%pest(ipest)%stor_final` | Only when `time%end_sim == 1`. | `baqupst_a%pest(ipest)%stor_final` is set from the current daily ending storage so the average-annual record includes the final terminal storage. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits show the routine's evolution. `df07e3f` introduced `basin_aqu_pest_output` with the full daily, monthly, yearly, and end-of-simulation pesticide reporting logic. `39fabde` changed the local initializations of `ipest`, `iaq`, `iob`, `const`, and `stor_init` to explicit zero values. `2fe89fd` updated the CSV write formats for the four CSV output units from `G0.3` to `G0.6`. The source span also shows the existing annual reset behavior, including the final `baqupst_a%pest(ipest) = aqu_pestbz` reset, remaining in place across those changes.

- df07e3f added the complete basin aquifer pesticide output routine, including accumulation of daily aquifer pesticide balances and writes to the daily, monthly, yearly, and average-annual output units.
- 39fabde changed only the local variable initialization style for `ipest`, `iaq`, `iob`, `const`, and `stor_init`; it did not change the output algorithm itself.
- 2fe89fd changed only the CSV formatting precision for units 3004, 3005, 3006, and 3007 from `G0.3` to `G0.6`, increasing numeric output precision without changing what data are written.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_aqu_pest_output' has no extracted documentation comment.
