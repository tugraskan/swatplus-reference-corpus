---
kind: procedure
symbol: res_cs_output
title: res_cs_output
status: filled
source_hash: 81cb5a439946b0c0
version_label: SWAT+ 62.0.0
args:
  j: '`j` selects which reservoir object this call reports on. The routine uses it to index
    the reservoir constituent arrays (`rescs_d`, `rescs_m`, `rescs_y`, `rescs_a`) and to locate
    the matching reservoir GIS id via `ob(sp_ob1%res + j - 1)%gis_id`.'
locals:
  ics: '`ics` is the loop index over constituent species. It is initialized to 0 and used
    to traverse `1..cs_db%num_cs` when accumulating and printing each constituent''s balance
    terms.'
  iob: '`iob` holds the reservoir object index in `ob`. It is initialized to 0 and set to
    `sp_ob1%res + j - 1` so the routine can fetch the reservoir GIS id for output records.'
  const: '`const` is a scaling divisor used to convert accumulated mass and concentration
    totals into period averages at month-end and year-end. It is initialized to 0. and assigned
    either the number of days in the month or `time%day_end_yr` before division.'
uses:
  output_ls_pesticide_module: '`output_ls_pesticide_module` is imported by the procedure,
    so it is part of the compilation and shared-state context for output routines even though
    no direct symbol use was extracted here.'
  res_pesticide_module: '`res_pesticide_module` is imported alongside the reservoir constituent
    output state, so it matters as part of the reservoir output environment even though no
    direct reference was extracted for this routine.'
  res_cs_module: '`res_cs_module` supplies the reservoir constituent balance arrays that this
    routine updates and prints. The daily arrays are summed into monthly totals, monthly totals
    into yearly totals, and yearly totals into average-annual totals for every constituent
    species, along with volume for the first constituent slot.'
  plant_module: '`plant_module` is imported by the routine but no extracted source line in
    this packet shows a direct plant symbol use. It still matters as part of the shared model
    context for output routines.'
  plant_data_module: '`plant_data_module` is imported by the routine but no extracted source
    line in this packet shows a direct use. It remains part of the shared model state available
    to this output code.'
  time_module: '`time_module` provides the current simulation date and period-end flags that
    control when daily, monthly, yearly, and average-annual outputs are written and when accumulated
    values are rolled up or reset.'
  basin_module: '`basin_module` provides the print-control flags that enable or suppress each
    report interval and CSV duplication, so the routine only writes the requested reservoir
    constituent output streams.'
  output_landscape_module: '`output_landscape_module` is imported by the routine as part of
    the broader output framework, even though no direct symbol use was extracted in this packet.'
  constituent_mass_module: '`constituent_mass_module` supplies `cs_db%num_cs`, which sets
    the constituent loop bounds and determines how many reservoir species are accumulated
    and written in each record.'
  hydrograph_module: '`hydrograph_module` supplies `sp_ob1` and `ob`, which let the routine
    map the reservoir index `j` to the correct reservoir object and GIS identifier for the
    output records.'
---

<!-- facts:header -->

Writes reservoir constituent-mass balance output at daily, monthly, yearly, and average-annual intervals. It accumulates daily results into monthly, yearly, and simulation-total reservoirs and emits text or CSV records when the corresponding print codes are enabled.

## Bottom Line

res_cs_output collects reservoir constituent mass-balance values for the reservoir indexed by `j`, adds the current day's values into the monthly totals, and, at month-end and year-end, rolls those totals into yearly and average-annual accumulators. It is the reservoir-specific output routine for the constituent-mass subsystem.

The routine also writes formatted output records for daily, monthly, yearly, and average-annual reports, with optional CSV duplicates when `pco%csvout == 'y'`. Its results feed the reservoir constituent reporting stream driven by `command`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` inside the reservoir loop, after the reservoir state for the current timestep has already been computed and the model knows whether the current day is a month-end, year-end, or simulation end. Its output and accumulator updates feed the reservoir constituent reporting files that are later consumed as the model's summarized reservoir mass-balance results.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the reservoir index to the object list | Computes `iob = sp_ob1%res + j - 1` so the routine can fetch the reservoir GIS identifier associated with reservoir `j`. |
| 2. Accumulate daily values into monthly totals | Adds each daily constituent balance term from `rescs_d(j)` into the monthly accumulator `rescs_m(j)` for every constituent species, then adds daily volume to the first volume slot. |
| 3. Emit daily reservoir output when enabled | If daily reservoir constituent output is requested, writes the day-level balance record to unit 6040 and optionally duplicates it to the CSV unit 6041. |
| 4. Check for month-end processing | Tests `time%end_mo` to decide whether monthly totals should be rolled into yearly storage and reported. |
| 5. Roll monthly totals into yearly totals | Adds the monthly accumulator `rescs_m(j)` into the yearly accumulator `rescs_y(j)` for each constituent species and volume. |
| 6. Convert month-accumulated mass and concentration to monthly averages | Divides monthly mass, concentration, and volume totals by the number of days in the month stored in `const` to form average monthly values before printing. |
| 7. Emit monthly output when enabled | Writes the monthly reservoir constituent record to unit 6042 and, if CSV output is enabled, to unit 6043. |
| 8. Reset monthly accumulators after month-end output | Zeros the monthly constituent accumulators and volume so the next month starts with a clean slate. |
| 9. Check for year-end processing | Tests `time%end_yr` to decide whether yearly totals should be rolled into the simulation-total accumulators and reported. |
| 10. Roll yearly totals into simulation totals | Adds the yearly accumulator `rescs_y(j)` into the all-years accumulator `rescs_a(j)` for every constituent species and volume. |
| 11. Convert yearly-accumulated mass and concentration to yearly averages | Divides yearly mass, concentration, and volume totals by `time%day_end_yr` to prepare average yearly output. |
| 12. Emit yearly output when enabled | Writes the yearly reservoir constituent record to unit 6044 and, if CSV output is enabled, to unit 6045. |
| 13. Reset yearly accumulators after year-end output | Zeros the yearly constituent accumulators and volume so the next year starts from zero. |
| 14. Emit average-annual output at simulation end | If the simulation has ended and average-annual output is enabled, divides the simulation-total accumulator by `time%nbyr` and writes the final record to unit 6046, with optional CSV output to unit 6047. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `No specific symbols from `output_ls_pesticide_module` were resolved in the extracted context.` |  |
| [sym:res_pesticide_module] | `No specific symbols from `res_pesticide_module` were resolved in the extracted context.` |  |
| [sym:res_cs_module] | `rescs_m, rescs_d, rescs_y, rescs_a` | `rescs_m(j)%cs(ics)%inflow, rescs_d(j)%cs(ics)%inflow, rescs_m(j)%cs(ics)%outflow, rescs_d(j)%cs(ics)%outflow, rescs_m(j)%cs(ics)%seep, rescs_d(j)%cs(ics)%seep, rescs_m(j)%cs(ics)%settle, rescs_d(j)%cs(ics)%settle, rescs_m(j)%cs(ics)%rctn, rescs_d(j)%cs(ics)%rctn, rescs_m(j)%cs(ics)%prod, rescs_d(j)%cs(ics)%prod, rescs_m(j)%cs(ics)%fert, rescs_d(j)%cs(ics)%fert, rescs_m(j)%cs(ics)%irrig, rescs_d(j)%cs(ics)%irrig, rescs_m(j)%cs(ics)%div, rescs_d(j)%cs(ics)%div, rescs_m(j)%cs(ics)%mass, rescs_d(j)%cs(ics)%mass, rescs_m(j)%cs(ics)%conc, rescs_d(j)%cs(ics)%conc, rescs_m(j)%cs(1)%volm, rescs_d(j)%cs(1)%volm, rescs_y(j)%cs(ics)%inflow, rescs_y(j)%cs(ics)%outflow, rescs_y(j)%cs(ics)%seep, rescs_y(j)%cs(ics)%settle, rescs_y(j)%cs(ics)%rctn, rescs_y(j)%cs(ics)%prod, rescs_y(j)%cs(ics)%fert, rescs_y(j)%cs(ics)%irrig, rescs_y(j)%cs(ics)%div, rescs_y(j)%cs(ics)%mass, rescs_y(j)%cs(ics)%conc, rescs_y(j)%cs(1)%volm, rescs_a(j)%cs(ics)%inflow, rescs_a(j)%cs(ics)%outflow, rescs_a(j)%cs(ics)%seep, rescs_a(j)%cs(ics)%settle, rescs_a(j)%cs(ics)%rctn, rescs_a(j)%cs(ics)%prod, rescs_a(j)%cs(ics)%fert, rescs_a(j)%cs(ics)%irrig, rescs_a(j)%cs(ics)%div, rescs_a(j)%cs(ics)%mass, rescs_a(j)%cs(ics)%conc, rescs_a(j)%cs(1)%volm` |
| [sym:plant_module] | `No specific symbols from `plant_module` were resolved in the extracted context.` |  |
| [sym:plant_data_module] | `No specific symbols from `plant_data_module` were resolved in the extracted context.` |  |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%cs_res%d, pco%csvout, pco%cs_res%m, pco%cs_res%y, pco%cs_res%a` |
| [sym:output_landscape_module] | `No specific symbols from `output_landscape_module` were resolved in the extracted context.` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%res` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rescs_m(j)%cs(ics)%inflow` | Every call, before any print checks | `rescs_m(j)%cs(ics)%inflow` is incremented by the current day's inflow so the monthly accumulator carries the running sum of daily inflow for each constituent. |
| `rescs_m(j)%cs(ics)%outflow` | Every call, before any print checks | `rescs_m(j)%cs(ics)%outflow` is incremented by the current day's outflow so the monthly accumulator stores the running monthly total for each constituent. |
| `rescs_m(j)%cs(ics)%seep` | Every call, before any print checks | `rescs_m(j)%cs(ics)%seep` is incremented by the daily seepage amount to build the month-to-date seepage total. |
| `rescs_m(j)%cs(ics)%settle` | Every call, before any print checks | `rescs_m(j)%cs(ics)%settle` is incremented by the daily settling loss so the monthly total reflects all settling over the month. |
| `rescs_m(j)%cs(ics)%rctn` | Every call, before any print checks | `rescs_m(j)%cs(ics)%rctn` is incremented by the daily reaction-loss term to accumulate monthly reaction removal. |
| `rescs_m(j)%cs(ics)%prod` | Every call, before any print checks | `rescs_m(j)%cs(ics)%prod` is incremented by the daily reaction-production term to accumulate monthly production. |
| `rescs_m(j)%cs(ics)%fert` | Every call, before any print checks | `rescs_m(j)%cs(ics)%fert` is incremented by any fertilizer addition term so the monthly accumulator records all fertilizer inputs. |
| `rescs_m(j)%cs(ics)%irrig` | Every call, before any print checks | `rescs_m(j)%cs(ics)%irrig` is incremented by the daily irrigation removal term to accumulate the month-to-date irrigation effect. |
| `rescs_m(j)%cs(ics)%div` | Every call, before any print checks | `rescs_m(j)%cs(ics)%div` is incremented by the daily diversion term to track monthly gains or losses through diversion. |
| `rescs_m(j)%cs(ics)%mass` | Every call, before any print checks | `rescs_m(j)%cs(ics)%mass` is incremented by the daily end-of-day mass so the monthly store can later be averaged and/or rolled up. |
| `rescs_m(j)%cs(ics)%conc` | Every call, before any print checks | `rescs_m(j)%cs(ics)%conc` is incremented by the daily concentration so the monthly accumulator can later be averaged. |
| `rescs_m(j)%cs(1)%volm` | Every call, before any print checks | `rescs_m(j)%cs(1)%volm` is incremented by the daily reservoir water volume so monthly and later annual volume summaries can be produced. |
| `rescs_y(j)%cs(ics)%inflow` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%inflow` receives the current month's inflow total, rolling monthly inflow into the yearly accumulator. |
| `rescs_y(j)%cs(ics)%outflow` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%outflow` receives the current month's outflow total, rolling monthly outflow into the yearly accumulator. |
| `rescs_y(j)%cs(ics)%seep` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%seep` receives the current month's seepage total so yearly seepage can be reported. |
| `rescs_y(j)%cs(ics)%settle` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%settle` receives the current month's settling total so yearly settling can be reported. |
| `rescs_y(j)%cs(ics)%rctn` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%rctn` receives the current month's reaction-loss total so yearly reaction output is preserved. |
| `rescs_y(j)%cs(ics)%prod` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%prod` receives the current month's production total so yearly production can be accumulated. |
| `rescs_y(j)%cs(ics)%fert` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%fert` receives the current month's fertilizer term so yearly fertilizer totals are available. |
| `rescs_y(j)%cs(ics)%irrig` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%irrig` receives the current month's irrigation term so yearly irrigation totals are available. |
| `rescs_y(j)%cs(ics)%div` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%div` receives the current month's diversion term so yearly diversion totals are available. |
| `rescs_y(j)%cs(ics)%mass` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%mass` receives the current month's averaged mass term after monthly rollup. |
| `rescs_y(j)%cs(ics)%conc` | When `time%end_mo == 1` | `rescs_y(j)%cs(ics)%conc` receives the current month's averaged concentration term after monthly rollup. |
| `rescs_y(j)%cs(1)%volm` | When `time%end_mo == 1` | `rescs_y(j)%cs(1)%volm` receives the current month's accumulated volume so yearly volume summaries can be formed. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit `df07e3f` as a new reservoir constituent-output subroutine. Commit `39fabde` changed the local initializations for `ics`, `iob`, and `const` from uninitialized declarations to explicit zero initialization. Commit `2fe89fd` changed the CSV format specifier in the daily, monthly, yearly, and average-annual CSV writes from `G0.3` to `G0.6`.

- df07e3f added the full `res_cs_output` subroutine, including the daily-to-monthly, monthly-to-yearly, and yearly-to-average-annual accumulation logic plus the four output blocks.
- 39fabde made `ics`, `iob`, and `const` explicitly start at zero, removing reliance on implicit/uninitialized local values.
- 2fe89fd increased CSV numeric precision for the reservoir constituent output files written to units 6041, 6043, 6045, and 6047.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_cs_output' has no extracted documentation comment.
- No direct symbol uses were extracted from output_ls_pesticide_module, res_pesticide_module, plant_module, plant_data_module, or output_landscape_module in the provided context; their imported presence is documented conservatively.
- algorithm_steps revised: merged the repeated accumulator and print phases into 14 model-oriented steps while preserving source line citations from the source block.
