---
kind: procedure
symbol: wet_cs_output
title: wet_cs_output
status: filled
source_hash: 6a949f55976fc54d
version_label: SWAT+ 62.0.0
args:
  j: Wetland/object index for the current HRU output slot. The routine uses `j` to pick the
    wetland constituent arrays (`wetcs_d`, `wetcs_m`, `wetcs_y`, `wetcs_a`) and to derive
    the associated object number `iob = sp_ob1%hru + j - 1`.
locals:
  ics: Loop index over constituent types in `cs_db%num_cs`; initialized to 0 but used immediately
    to accumulate, average, and reset per-constituent wetland outputs.
  iob: Derived object index for the current wetland HRU. It maps the input `j` to the corresponding
    hydrograph object record used for `ob(iob)%gis_id`.
  const: Scalar divisor used to convert accumulated monthly or yearly totals into averages
    for mass and concentration. It is set from month length or year length before division.
uses:
  output_ls_pesticide_module: The procedure `use`s this module, but the context packet did
    not resolve any specific symbols from it. It may contribute output-related state elsewhere,
    but no directly cited component is available here.
  res_pesticide_module: The procedure `use`s this module, but the context packet did not resolve
    any specific symbols from it. No direct symbol use is evidenced in the packet, so its
    concrete role cannot be stated beyond being an imported dependency.
  res_cs_module: These arrays hold the wetland constituent balance records that this routine
    updates and prints. The daily array feeds monthly accumulation, the monthly array feeds
    yearly accumulation, and the yearly array feeds all-years accumulation; their per-constituent
    balance fields and `volm` field are the core data being reported and reset.
  plant_module: The module is imported, but the packet contains no resolved symbol references
    from it. No concrete contribution to `wet_cs_output` can be pinned down from the evidence
    provided.
  plant_data_module: The module is imported, but the packet contains no resolved symbol references
    from it. No concrete contribution to `wet_cs_output` can be pinned down from the evidence
    provided.
  time_module: 'The current simulation date controls every branch in this routine: daily writes
    use the present day fields, month-end logic is triggered by `time%end_mo`, year-end logic
    by `time%end_yr`, and average-annual output by `time%end_sim`. The month and year counters
    are also used to compute averaging divisors.'
  basin_module: Printing codes in `pco%cs_res` and `pco%csvout` determine whether daily, monthly,
    yearly, and average-annual outputs are written, and whether the CSV companion files are
    produced. Without these flags the routine would still accumulate totals but would not
    emit the corresponding records.
  output_landscape_module: The module is imported, but the packet contains no resolved symbol
    references from it. No direct state usage is evidenced in the source lines provided.
  constituent_mass_module: The number of constituent types in `cs_db%num_cs` sets the bounds
    of every accumulation, averaging, and write loop. It determines how many wetland constituent
    records are updated and how many values are emitted in each output line.
  hydrograph_module: The wetland HRU index is translated into an object connectivity record
    via `sp_ob1%hru`, and `ob(iob)%gis_id` is written with each output line. This ties each
    wetland constituent report back to the spatial object identity used elsewhere in the model.
---

<!-- facts:header -->

Aggregates and writes wetland constituent-mass outputs for a wetland HRU. It records daily, monthly, yearly, and average-annual balances for each constituent.

## Bottom Line

This subroutine updates the wetland constituent summary arrays for one wetland HRU index `j`. It adds the day’s values into monthly totals, rolls monthly totals into yearly totals at month end, rolls yearly totals into all-years totals at year end, and optionally writes those results to fixed-format and CSV output files.

It matters because it is the wetland constituent reporting point for the simulation. The routine preserves running totals in `wetcs_m`, `wetcs_y`, and `wetcs_a`, while also emitting the current-day, monthly, yearly, and average-annual values controlled by `pco%cs_res` and `pco%csvout`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after HRU/wetland outputs are being processed and only when the current HRU has surface storage and `cs_db%num_cs > 0`. It depends on the daily wetland constituent state already being populated elsewhere in the model, and later reporting behavior depends on the accumulated monthly, yearly, and all-years totals it leaves in `wetcs_m`, `wetcs_y`, and `wetcs_a`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the wetland index to a hydrograph object | Derives `iob = sp_ob1%hru + j - 1` so the current wetland HRU can be tied to the correct object record and GIS id. |
| 2. Accumulate daily constituent values into monthly totals | Loops over all constituent types and adds each daily wetland balance field from `wetcs_d` into the corresponding `wetcs_m` monthly accumulator; volume is accumulated separately. |
| 3. Write daily wetland output if enabled | When `pco%cs_res%d` is enabled, writes the daily record to unit 6090 and, if `pco%csvout` is also enabled, writes the CSV version to unit 6091. |
| 4. On month end, roll monthly totals into yearly totals | If `time%end_mo == 1`, adds the monthly accumulators from `wetcs_m` into the yearly accumulators in `wetcs_y`, including water volume. |
| 5. Compute month-length divisor and average monthly mass and concentration | Computes the month length in days as `const` using `ndays` and converts the monthly mass, concentration, and volume values in `wetcs_m` to averages by dividing by that length. |
| 6. Write monthly wetland output if enabled, then clear monthly accumulators | When `pco%cs_res%m` is enabled, writes monthly records to units 6092 and 6093. After output, zeros the monthly constituent and volume accumulators so the next month starts fresh. |
| 7. On year end, roll yearly totals into all-years totals | If `time%end_yr == 1`, adds the yearly accumulators from `wetcs_y` into the all-years accumulators in `wetcs_a`, including water volume. |
| 8. Compute year-length divisor and average yearly mass and concentration | Uses `time%day_end_yr` as the divisor and converts the yearly mass, concentration, and volume values in `wetcs_y` to averages. |
| 9. Write yearly wetland output if enabled, then clear yearly accumulators | When `pco%cs_res%y` is enabled, writes yearly records to units 6094 and 6095. After output, zeros the yearly constituent and volume accumulators. |
| 10. On simulation end, compute average annual output and write it | If `time%end_sim == 1` and `pco%cs_res%a` is enabled, divides `wetcs_a` by `time%nbyr` to form average annual values and writes them to units 6096 and 6097. |
| 11. Return to caller | Ends the subroutine after all requested wetland constituent outputs have been accumulated and written. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `None resolved to this module from the provided context.` |  |
| [sym:res_pesticide_module] | `None resolved to this module from the provided context.` |  |
| [sym:res_cs_module] | `wetcs_m, wetcs_d, wetcs_y, wetcs_a` | `wetcs_m(j)%cs(ics)%inflow, wetcs_d(j)%cs(ics)%inflow, wetcs_m(j)%cs(ics)%outflow, wetcs_d(j)%cs(ics)%outflow, wetcs_m(j)%cs(ics)%seep, wetcs_d(j)%cs(ics)%seep, wetcs_m(j)%cs(ics)%settle, wetcs_d(j)%cs(ics)%settle, wetcs_m(j)%cs(ics)%rctn, wetcs_d(j)%cs(ics)%rctn, wetcs_m(j)%cs(ics)%prod, wetcs_d(j)%cs(ics)%prod, wetcs_m(j)%cs(ics)%fert, wetcs_d(j)%cs(ics)%fert, wetcs_m(j)%cs(ics)%irrig, wetcs_d(j)%cs(ics)%irrig, wetcs_m(j)%cs(ics)%mass, wetcs_d(j)%cs(ics)%mass, wetcs_m(j)%cs(ics)%conc, wetcs_d(j)%cs(ics)%conc, wetcs_m(j)%cs(1)%volm, wetcs_d(j)%cs(1)%volm, wetcs_y(j)%cs(ics)%inflow, wetcs_y(j)%cs(ics)%outflow, wetcs_y(j)%cs(ics)%seep, wetcs_y(j)%cs(ics)%settle, wetcs_y(j)%cs(ics)%rctn, wetcs_y(j)%cs(ics)%prod, wetcs_y(j)%cs(ics)%fert, wetcs_y(j)%cs(ics)%irrig, wetcs_y(j)%cs(ics)%mass, wetcs_y(j)%cs(ics)%conc, wetcs_y(j)%cs(1)%volm, wetcs_a(j)%cs(ics)%inflow, wetcs_a(j)%cs(ics)%outflow, wetcs_a(j)%cs(ics)%seep, wetcs_a(j)%cs(ics)%settle, wetcs_a(j)%cs(ics)%rctn, wetcs_a(j)%cs(ics)%prod, wetcs_a(j)%cs(ics)%fert, wetcs_a(j)%cs(ics)%irrig, wetcs_a(j)%cs(ics)%mass, wetcs_a(j)%cs(ics)%conc, wetcs_a(j)%cs(1)%volm` |
| [sym:plant_module] | `None resolved to this module from the provided context.` |  |
| [sym:plant_data_module] | `None resolved to this module from the provided context.` |  |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%cs_res%d, pco%csvout, pco%cs_res%m, pco%cs_res%y, pco%cs_res%a` |
| [sym:output_landscape_module] | `None resolved to this module from the provided context.` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%hru` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wetcs_m(j)%cs(ics)%inflow` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Adds the current day's wetland constituent inflow for constituent `ics` into the running monthly total `wetcs_m(j)%cs(ics)%inflow`. |
| `wetcs_m(j)%cs(ics)%outflow` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Adds the current day's wetland constituent outflow into the monthly accumulator for that constituent. |
| `wetcs_m(j)%cs(ics)%seep` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Accumulates daily seepage losses into the monthly wetland constituent balance. |
| `wetcs_m(j)%cs(ics)%settle` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Accumulates daily settling loss into the monthly wetland constituent balance. |
| `wetcs_m(j)%cs(ics)%rctn` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Accumulates daily chemical reaction loss into the monthly wetland constituent balance. |
| `wetcs_m(j)%cs(ics)%prod` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Accumulates daily chemical production into the monthly wetland constituent balance. |
| `wetcs_m(j)%cs(ics)%fert` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Accumulates fertilizer-applied constituent mass into the monthly wetland constituent balance. |
| `wetcs_m(j)%cs(ics)%irrig` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Accumulates irrigation-related constituent transfer into the monthly wetland constituent balance. |
| `wetcs_m(j)%cs(ics)%mass` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Accumulates daily constituent mass in wetland water into the monthly total for each constituent. |
| `wetcs_m(j)%cs(ics)%conc` | Always, once per call; inside `do ics = 1, cs_db%num_cs`. | Accumulates daily constituent concentration into the monthly total for each constituent; later divided by month length to form an average. |
| `wetcs_m(j)%cs(1)%volm` | Always, once per call. | Accumulates daily water volume into the monthly volume total for the first constituent slot, then later divides that volume by month length and resets it to zero at month end. |
| `wetcs_y(j)%cs(ics)%inflow` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated inflow into the yearly wetland constituent total. |
| `wetcs_y(j)%cs(ics)%outflow` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated outflow into the yearly wetland constituent total. |
| `wetcs_y(j)%cs(ics)%seep` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated seepage into the yearly wetland constituent total. |
| `wetcs_y(j)%cs(ics)%settle` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated settling into the yearly wetland constituent total. |
| `wetcs_y(j)%cs(ics)%rctn` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated reaction loss into the yearly wetland constituent total. |
| `wetcs_y(j)%cs(ics)%prod` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated production into the yearly wetland constituent total. |
| `wetcs_y(j)%cs(ics)%fert` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated fertilizer contribution into the yearly wetland constituent total. |
| `wetcs_y(j)%cs(ics)%irrig` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated irrigation transfer into the yearly wetland constituent total. |
| `wetcs_y(j)%cs(ics)%mass` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated constituent mass into the yearly total, then later divides yearly mass by year length before writing. |
| `wetcs_y(j)%cs(ics)%conc` | Only when `time%end_mo == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current month’s accumulated concentration into the yearly total, then later divides yearly concentration by year length before writing. |
| `wetcs_y(j)%cs(1)%volm` | Only when `time%end_mo == 1`. | Adds the monthly accumulated volume into the yearly volume total, then later divides yearly volume by year length and clears the monthly value. |
| `wetcs_a(j)%cs(ics)%inflow` | Only when `time%end_yr == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current year’s accumulated inflow into the all-years wetland constituent total. |
| `wetcs_a(j)%cs(ics)%outflow` | Only when `time%end_yr == 1`; inside `do ics = 1, cs_db%num_cs`. | Adds the current year’s accumulated outflow into the all-years wetland constituent total. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure first appears in commit df07e3f as a new source file implementing wetland constituent output accumulation and reporting. Commit 35b029c removed one extra blank line at the end of the file, 39fabde initialized local variables `ics`, `iob`, and `const`, and 2fe89fd changed the CSV write formats on units 6091, 6093, 6095, and 6097 from `G0.3` to `G0.6`.

- df07e3f introduced the entire `wet_cs_output` subroutine, including daily/monthly/yearly/all-years accumulation and output to units 6090-6097.
- 35b029c made only a formatting cleanup by removing a trailing blank line before the `format` statement.
- 39fabde changed local initialization so `ics`, `iob`, and `const` start at zero values, reducing dependence on undefined initial state.
- 2fe89fd increased CSV numeric precision for wetland constituent outputs by switching the CSV formats from `G0.3` to `G0.6` on units 6091, 6093, 6095, and 6097.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wet_cs_output' has no extracted documentation comment.
- Source shows `use output_ls_pesticide_module`, `use res_pesticide_module`, `use plant_module`, `use plant_data_module`, and `use output_landscape_module`, but no direct symbols from those modules were resolved in the provided context.
- The source accumulates monthly and yearly totals, then averages only mass, concentration, and volume before writing the corresponding period outputs.
- algorithm_steps revised: merged the monthly and yearly update/output phases into a more detailed step list aligned with the visible control flow and source line ranges.
- lineage_summary and lineage_impacts were derived only from the resolved Git lineage diffs provided in the packet.
