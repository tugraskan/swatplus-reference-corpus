---
kind: procedure
symbol: aqu_cs_output
title: aqu_cs_output
status: filled
source_hash: 07ac36920a547307
version_label: SWAT+ 62.0.0
args:
  iaq: '`iaq` selects which aquifer object to process. The routine uses it to index the aquifer
    balance arrays (`acsb_d`, `acsb_m`, `acsb_y`, `acsb_a`) and to map that aquifer to the
    corresponding hydrograph object number for output labels.'
locals:
  const: '`const` holds the time-span used to convert accumulated mass-like monthly or yearly
    totals into averages before printing. It is set from month length or year length and then
    used as a divisor for `mass`, `conc`, and `srbd`.'
  iob: '`iob` stores the hydrograph/object index for the aquifer being reported. It is derived
    from `sp_ob1%aqu + iaq - 1` and is used to fetch `ob(iob)%gis_id` for output records.'
  ics: '`ics` is the constituent loop index. It steps through all simulated constituents in
    `cs_db%num_cs` so the routine can accumulate, average, print, and zero each constituent''s
    aquifer balance fields.'
uses:
  time_module: The `time` state determines which reporting branches run and provides the date
    fields written to every record. Its end-of-month, end-of-year, and end-of-simulation flags
    gate monthly, yearly, and average-annual outputs, while its calendar fields label each
    output row.
  basin_module: The `pco` print-code state turns each aquifer constituent output interval
    on or off. Its `cs_aqu` flags decide whether daily, monthly, yearly, or average-annual
    aquifer constituent files are written, and `csvout` adds CSV-formatted duplicates of those
    same records.
  aquifer_module: This module owns the aquifer constituent balance arrays that the routine
    both accumulates and prints. The routine reads daily values from `acsb_d`, rolls them
    into `acsb_m`, `acsb_y`, and `acsb_a`, and then writes those same fields to the output
    files.
  hydrograph_module: The hydrograph object mapping identifies which basin object corresponds
    to aquifer `iaq`, so the output can carry the correct GIS identifier. Without `sp_ob1`
    and `ob`, the routine could not label each aquifer record with `ob(iob)%gis_id`.
  cs_aquifer: The aquifer constituent balance type defines the fields this routine reports
    and accumulates. Those fields are the actual source of the daily, monthly, yearly, and
    average-annual aquifer mass-balance outputs.
  constituent_mass_module: The constituent database count controls how many constituent records
    are looped over in every accumulation, averaging, and write statement. If `cs_db%num_cs`
    is zero, the constituent output loops do not execute.
---

<!-- facts:header -->

Writes aquifer constituent mass-balance outputs at daily, monthly, yearly, and average-annual intervals.

## Bottom Line

This subroutine prints aquifer constituent balance output for one aquifer object (`iaq`). It gathers the current daily balances, and when a reporting period ends it also writes monthly, yearly, and simulation-average annual summaries, with optional CSV copies controlled by `pco%csvout` and the aquifer print codes in `pco%cs_aqu`.

The routine matters because it is the aggregation and reporting point for aquifer constituent fluxes and storage terms. It rolls daily totals into monthly accumulators, monthly totals into yearly accumulators, and yearly totals into simulation totals, then resets the lower-level accumulators after each period so later output records and downstream reporting reflect the correct period totals.

## Arguments

<!-- facts:arguments -->

## Where It Fits

The caller `command` invokes this routine inside the aquifer-object output loop after other aquifer output routines and only when simulated constituents exist (`cs_db%num_cs > 0`). This routine depends on upstream model steps having already populated `acsb_d` for the current day; its monthly, yearly, and average-annual accumulations then feed the later output records written at month end, year end, and simulation end.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the aquifer index to the corresponding object connectivity index. | Computes `iob = sp_ob1%aqu + iaq - 1` so the routine can fetch the correct aquifer object metadata, including the GIS identifier used in output records. |
| 2. Roll daily constituent balances into the monthly accumulators. | Loops over all simulated constituents and adds each daily aquifer balance component from `acsb_d(iaq)%cs(ics)` into the corresponding monthly accumulator in `acsb_m(iaq)%cs(ics)`. |
| 3. Write daily aquifer constituent output when daily printing is enabled. | If `pco%cs_aqu%d == 'y'`, writes the daily aquifer constituent record to unit 6060 and, when CSV output is enabled, also writes a CSV-formatted copy to unit 6061. |
| 4. On month end, roll monthly totals into yearly totals and prepare monthly averages. | When `time%end_mo == 1`, adds the completed monthly totals from `acsb_m(iaq)%cs` into `acsb_y(iaq)%cs`, computes the month length with `float(ndays(time%mo + 1) - ndays(time%mo))`, and divides monthly `mass`, `conc`, and `srbd` by that length so the monthly print shows averages for those variables. |
| 5. Write monthly aquifer constituent output when monthly printing is enabled. | If `pco%cs_aqu%m == 'y'`, writes the monthly record to unit 6062 and, when CSV output is enabled, also writes a CSV-formatted copy to unit 6063. |
| 6. Clear the monthly accumulators after the month-end report. | Resets all monthly constituent fields in `acsb_m(iaq)%cs(ics)` to zero so the next month starts with empty accumulators. |
| 7. On year end, roll yearly totals into simulation-total accumulators and prepare yearly averages. | When `time%end_yr == 1`, adds yearly totals from `acsb_y(iaq)%cs` into `acsb_a(iaq)%cs`, sets `const = time%day_end_yr`, and divides yearly `mass`, `conc`, and `srbd` by that divisor so the yearly print reports averages for those variables. |
| 8. Write yearly aquifer constituent output when yearly printing is enabled. | If `pco%cs_aqu%y == 'y'`, writes the yearly record to unit 6064 and, when CSV output is enabled, also writes a CSV-formatted copy to unit 6065. |
| 9. Clear the yearly accumulators after the year-end report. | Resets all yearly constituent fields in `acsb_y(iaq)%cs(ics)` to zero so the next year starts with empty accumulators. |
| 10. At simulation end, compute average-annual values from the simulation-total accumulators. | When `time%end_sim == 1` and average-annual output is enabled, divides each simulation-total constituent accumulator in `acsb_a(iaq)%cs` by `time%nbyr` to form average annual values. |
| 11. Write average-annual aquifer constituent output when enabled. | Writes the average-annual record to unit 6066 and, when CSV output is enabled, also writes a CSV-formatted copy to unit 6067. |
| 12. Return to the caller. | Ends the subroutine after all requested aquifer constituent outputs have been produced. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%cs_aqu%d, pco%csvout, pco%cs_aqu%m, pco%cs_aqu%y, pco%cs_aqu%a` |
| [sym:aquifer_module] | `acsb_d, acsb_m, acsb_y, acsb_a` | `acsb_d(iaq)%cs(ics)%csgw, acsb_d(iaq)%cs(ics)%rchrg, acsb_d(iaq)%cs(ics)%seep, acsb_d(iaq)%cs(ics)%irr, acsb_d(iaq)%cs(ics)%div, acsb_d(iaq)%cs(ics)%sorb, acsb_d(iaq)%cs(ics)%rctn, acsb_d(iaq)%cs(ics)%mass, acsb_d(iaq)%cs(ics)%conc, acsb_d(iaq)%cs(ics)%srbd, acsb_m(iaq)%cs(ics)%csgw, acsb_m(iaq)%cs(ics)%rchrg, acsb_m(iaq)%cs(ics)%seep, acsb_m(iaq)%cs(ics)%irr, acsb_m(iaq)%cs(ics)%div, acsb_m(iaq)%cs(ics)%sorb, acsb_m(iaq)%cs(ics)%rctn, acsb_m(iaq)%cs(ics)%mass, acsb_m(iaq)%cs(ics)%conc, acsb_m(iaq)%cs(ics)%srbd, acsb_y(iaq)%cs(ics)%csgw, acsb_y(iaq)%cs(ics)%rchrg, acsb_y(iaq)%cs(ics)%seep, acsb_y(iaq)%cs(ics)%irr, acsb_y(iaq)%cs(ics)%div, acsb_y(iaq)%cs(ics)%sorb, acsb_y(iaq)%cs(ics)%rctn, acsb_y(iaq)%cs(ics)%mass, acsb_y(iaq)%cs(ics)%conc, acsb_y(iaq)%cs(ics)%srbd, acsb_a(iaq)%cs(ics)%csgw, acsb_a(iaq)%cs(ics)%rchrg, acsb_a(iaq)%cs(ics)%seep, acsb_a(iaq)%cs(ics)%irr, acsb_a(iaq)%cs(ics)%div, acsb_a(iaq)%cs(ics)%sorb, acsb_a(iaq)%cs(ics)%rctn, acsb_a(iaq)%cs(ics)%mass, acsb_a(iaq)%cs(ics)%conc, acsb_a(iaq)%cs(ics)%srbd` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%aqu` |
| [sym:cs_aquifer] | `acsb_m, acsb_d, acsb_y, acsb_a` | `acsb_m(iaq)%cs(ics)%csgw, acsb_d(iaq)%cs(ics)%csgw, acsb_m(iaq)%cs(ics)%rchrg, acsb_d(iaq)%cs(ics)%rchrg, acsb_m(iaq)%cs(ics)%seep, acsb_d(iaq)%cs(ics)%seep, acsb_m(iaq)%cs(ics)%irr, acsb_d(iaq)%cs(ics)%irr, acsb_m(iaq)%cs(ics)%div, acsb_d(iaq)%cs(ics)%div, acsb_m(iaq)%cs(ics)%sorb, acsb_d(iaq)%cs(ics)%sorb, acsb_m(iaq)%cs(ics)%rctn, acsb_d(iaq)%cs(ics)%rctn, acsb_m(iaq)%cs(ics)%mass, acsb_d(iaq)%cs(ics)%mass, acsb_m(iaq)%cs(ics)%conc, acsb_d(iaq)%cs(ics)%conc, acsb_m(iaq)%cs(ics)%srbd, acsb_d(iaq)%cs(ics)%srbd, acsb_y(iaq)%cs(ics)%csgw, acsb_y(iaq)%cs(ics)%rchrg, acsb_y(iaq)%cs(ics)%seep, acsb_y(iaq)%cs(ics)%irr, acsb_y(iaq)%cs(ics)%div, acsb_y(iaq)%cs(ics)%sorb, acsb_y(iaq)%cs(ics)%rctn, acsb_y(iaq)%cs(ics)%mass, acsb_y(iaq)%cs(ics)%conc, acsb_y(iaq)%cs(ics)%srbd, acsb_a(iaq)%cs(ics)%csgw, acsb_a(iaq)%cs(ics)%rchrg, acsb_a(iaq)%cs(ics)%seep, acsb_a(iaq)%cs(ics)%irr, acsb_a(iaq)%cs(ics)%div, acsb_a(iaq)%cs(ics)%sorb, acsb_a(iaq)%cs(ics)%rctn, acsb_a(iaq)%cs(ics)%mass, acsb_a(iaq)%cs(ics)%conc, acsb_a(iaq)%cs(ics)%srbd` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `acsb_m(iaq)%cs(ics)%csgw` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%csgw` into `acsb_m(iaq)%cs(ics)%csgw` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%csgw` becomes the running monthly total of groundwater loading from the daily aquifer balance values, so the month-end report can print the accumulated month. |
| `acsb_m(iaq)%cs(ics)%rchrg` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%rchrg` into `acsb_m(iaq)%cs(ics)%rchrg` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%rchrg` becomes the running monthly total of recharge mass from the daily aquifer balance values, so the month-end report can print the accumulated month. |
| `acsb_m(iaq)%cs(ics)%seep` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%seep` into `acsb_m(iaq)%cs(ics)%seep` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%seep` becomes the running monthly total of seepage mass from the daily aquifer balance values, so the month-end report can print the accumulated month. |
| `acsb_m(iaq)%cs(ics)%irr` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%irr` into `acsb_m(iaq)%cs(ics)%irr` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%irr` becomes the running monthly total of irrigation-removal mass from the daily aquifer balance values, so the month-end report can print the accumulated month. |
| `acsb_m(iaq)%cs(ics)%div` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%div` into `acsb_m(iaq)%cs(ics)%div` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%div` becomes the running monthly total of diversion mass from the daily aquifer balance values, so the month-end report can print the accumulated month. |
| `acsb_m(iaq)%cs(ics)%sorb` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%sorb` into `acsb_m(iaq)%cs(ics)%sorb` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%sorb` becomes the running monthly total of sorption-transfer mass from the daily aquifer balance values, so the month-end report can print the accumulated month. |
| `acsb_m(iaq)%cs(ics)%rctn` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%rctn` into `acsb_m(iaq)%cs(ics)%rctn` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%rctn` becomes the running monthly total of reaction-transfer mass from the daily aquifer balance values, so the month-end report can print the accumulated month. |
| `acsb_m(iaq)%cs(ics)%mass` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%mass` into `acsb_m(iaq)%cs(ics)%mass` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%mass` becomes the running monthly total of aquifer stored mass from the daily aquifer balance values, and it is later converted to a monthly average at month end. |
| `acsb_m(iaq)%cs(ics)%conc` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%conc` into `acsb_m(iaq)%cs(ics)%conc` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%conc` becomes the running monthly total of groundwater concentration from the daily aquifer balance values, and it is later converted to a monthly average at month end. |
| `acsb_m(iaq)%cs(ics)%srbd` | Each time the routine runs, before any reporting branches, it adds `acsb_d(iaq)%cs(ics)%srbd` into `acsb_m(iaq)%cs(ics)%srbd` inside `do ics=1,cs_db%num_cs`. | `acsb_m(iaq)%cs(ics)%srbd` becomes the running monthly total of sorbed mass from the daily aquifer balance values, and it is later converted to a monthly average at month end. |
| `acsb_y(iaq)%cs(ics)%csgw` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%csgw` into `acsb_y(iaq)%cs(ics)%csgw` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%csgw` becomes the running yearly total of groundwater loading accumulated from completed monthly totals. |
| `acsb_y(iaq)%cs(ics)%rchrg` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%rchrg` into `acsb_y(iaq)%cs(ics)%rchrg` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%rchrg` becomes the running yearly total of recharge mass accumulated from completed monthly totals. |
| `acsb_y(iaq)%cs(ics)%seep` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%seep` into `acsb_y(iaq)%cs(ics)%seep` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%seep` becomes the running yearly total of seepage mass accumulated from completed monthly totals. |
| `acsb_y(iaq)%cs(ics)%irr` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%irr` into `acsb_y(iaq)%cs(ics)%irr` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%irr` becomes the running yearly total of irrigation-removal mass accumulated from completed monthly totals. |
| `acsb_y(iaq)%cs(ics)%div` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%div` into `acsb_y(iaq)%cs(ics)%div` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%div` becomes the running yearly total of diversion mass accumulated from completed monthly totals. |
| `acsb_y(iaq)%cs(ics)%sorb` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%sorb` into `acsb_y(iaq)%cs(ics)%sorb` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%sorb` becomes the running yearly total of sorption-transfer mass accumulated from completed monthly totals. |
| `acsb_y(iaq)%cs(ics)%rctn` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%rctn` into `acsb_y(iaq)%cs(ics)%rctn` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%rctn` becomes the running yearly total of reaction-transfer mass accumulated from completed monthly totals. |
| `acsb_y(iaq)%cs(ics)%mass` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%mass` into `acsb_y(iaq)%cs(ics)%mass` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%mass` becomes the running yearly total of aquifer stored mass accumulated from completed monthly totals, and it is later converted to a yearly average at year end. |
| `acsb_y(iaq)%cs(ics)%conc` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%conc` into `acsb_y(iaq)%cs(ics)%conc` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%conc` becomes the running yearly total of groundwater concentration accumulated from completed monthly totals, and it is later converted to a yearly average at year end. |
| `acsb_y(iaq)%cs(ics)%srbd` | When `time%end_mo == 1`, the routine adds `acsb_m(iaq)%cs(ics)%srbd` into `acsb_y(iaq)%cs(ics)%srbd` inside `do ics=1,cs_db%num_cs`. | `acsb_y(iaq)%cs(ics)%srbd` becomes the running yearly total of sorbed mass accumulated from completed monthly totals, and it is later converted to a yearly average at year end. |
| `acsb_a(iaq)%cs(ics)%csgw` | When `time%end_yr == 1`, the routine adds `acsb_y(iaq)%cs(ics)%csgw` into `acsb_a(iaq)%cs(ics)%csgw` inside `do ics=1,cs_db%num_cs`. | `acsb_a(iaq)%cs(ics)%csgw` becomes the running simulation-total groundwater loading accumulated from completed yearly totals. |
| `acsb_a(iaq)%cs(ics)%rchrg` | When `time%end_yr == 1`, the routine adds `acsb_y(iaq)%cs(ics)%rchrg` into `acsb_a(iaq)%cs(ics)%rchrg` inside `do ics=1,cs_db%num_cs`. | `acsb_a(iaq)%cs(ics)%rchrg` becomes the running simulation-total recharge mass accumulated from completed yearly totals. |
| `acsb_a(iaq)%cs(ics)%seep` | When `time%end_yr == 1`, the routine adds `acsb_y(iaq)%cs(ics)%seep` into `acsb_a(iaq)%cs(ics)%seep` inside `do ics=1,cs_db%num_cs`. | `acsb_a(iaq)%cs(ics)%seep` becomes the running simulation-total seepage mass accumulated from completed yearly totals. |
| `acsb_a(iaq)%cs(ics)%irr` | When `time%end_yr == 1`, the routine adds `acsb_y(iaq)%cs(ics)%irr` into `acsb_a(iaq)%cs(ics)%irr` inside `do ics=1,cs_db%num_cs`. | `acsb_a(iaq)%cs(ics)%irr` becomes the running simulation-total irrigation-removal mass accumulated from completed yearly totals. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The routine was introduced in c7c8e22 as a full aquifer constituent output subroutine that accumulates daily balances into monthly, yearly, and simulation-total summaries and writes units 6060-6067. 2405a68 and c639a8c only changed the module import between `cs_aquifer` and `cs_aquifer_module`. 39fabde initialized `const`, `iob`, and `ics` to zero. f1e61a3 and 2fe89fd changed the CSV format descriptor for units 6061, 6063, 6065, and 6067 from `G0.3` to `G0.6` and fixed indentation; the core output logic stayed the same.

- c7c8e22 established the routine's daily/monthly/yearly/average-annual accumulation flow and its output files on units 6060-6067.
- 2405a68 changed the import to `cs_aquifer_module` for compilation, but did not alter the routine's accumulation or output behavior.
- c639a8c reverted the module name back to `cs_aquifer`, again affecting only compilation wiring.
- 39fabde initialized `const`, `iob`, and `ics`, making their starting values explicit without changing the algorithm.
- f1e61a3 fixed indentation in the CSV write statement; no functional change to the output logic.
- 2fe89fd increased CSV numeric precision from `G0.3` to `G0.6` on the CSV output units, changing formatted output detail only.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'aqu_cs_output' has no extracted documentation comment.
