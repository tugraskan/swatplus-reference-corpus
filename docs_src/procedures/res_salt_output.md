---
kind: procedure
symbol: res_salt_output
title: res_salt_output
status: filled
source_hash: def4969fd23b51e5
version_label: SWAT+ 62.0.0
args:
  j: Reservoir sequence index for the current output call. `j` selects which reservoir's salt
    balance arrays (`ressalt_d`, `ressalt_m`, `ressalt_y`, `ressalt_a`) are updated and written
    during this invocation.
locals:
  isalt: Loop index over salt constituents in `cs_db%num_salts`; it is initialized to 0 and
    then used to traverse each salt ion when accumulating, averaging, writing, and clearing
    reservoir salt balances.
  iob: Computed reservoir-object index into `ob`; it is initialized to 0 and then set to `sp_ob1%res
    + j - 1` so the routine can write the reservoir's GIS/object identifier with the output
    records.
  const: Scratch scalar used as the divisor for monthly averaging (`float(ndays(time%mo +
    1) - ndays(time%mo))`) and yearly averaging (`time%day_end_yr`). It is initialized to
    0. and then reused as the current averaging period length.
uses:
  output_ls_pesticide_module: This module is imported by the procedure, so it is part of the
    output stack that `res_salt_output` is compiled alongside. Even though the packet did
    not resolve a specific symbol from it, it matters here because the routine belongs to
    the shared landscape output family and the import may supply output-related interfaces
    or shared context used by neighboring procedures.
  res_pesticide_module: This module is imported by the procedure, so it is part of the constituent-output
    framework that surrounds reservoir reporting. The packet did not resolve a specific symbol
    from it, but it matters here because `res_salt_output` is the salt counterpart to reservoir
    pesticide output and shares the same reservoir-output workflow.
  res_salt_module: '`res_salt_module` defines the reservoir salt balance storage that this
    subroutine updates and prints. The arrays `ressalt_d`, `ressalt_m`, `ressalt_y`, and `ressalt_a`
    hold the daily, monthly, yearly, and average-annual salt summaries for each reservoir,
    and the fields inside each `salt(isalt)` entry are the values accumulated, averaged, reset,
    and written by this routine.'
  plant_module: The module is imported by the procedure, so it participates in the broader
    plant/reservoir state environment available during compilation. The packet did not identify
    a specific plant symbol used here, so its relevance is indirect rather than through a
    named reference in this routine.
  plant_data_module: This imported module provides plant data state in the surrounding model,
    but the packet did not resolve any direct symbol usage inside `res_salt_output`. It matters
    as part of the shared model context, not because this subroutine directly reads a named
    plant-data variable.
  time_module: '`time_module` supplies the simulation clock fields that control when daily,
    monthly, yearly, and average-annual reservoir salt output is emitted. `time%day`, `time%mo`,
    `time%day_mo`, and `time%yrc` are written into each record, while `time%end_mo`, `time%end_yr`,
    `time%end_sim`, `time%day_end_yr`, and `time%nbyr` determine when totals are rolled up,
    averaged, and cleared.'
  basin_module: '`basin_module` supplies the print-control flags that gate reservoir salt
    reporting. `pco%salt_res%d`, `%m`, `%y`, and `%a` decide whether daily, monthly, yearly,
    and average-annual reservoir salt records are written, and `pco%csvout` decides whether
    the companion CSV records are produced.'
  output_landscape_module: This imported module is part of the shared output infrastructure
    for landscape-scale reporting. The packet did not resolve a direct symbol from it, but
    it matters here because this routine writes model output records and belongs to the same
    output subsystem.
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_salts`, the number
    of salt constituents to loop over. That value controls the loop bounds for accumulation,
    averaging, zeroing, and record writing so the routine reports every simulated salt ion.'
  hydrograph_module: '`hydrograph_module` provides `sp_ob1%res` and `ob`, which are used to
    map the reservoir sequence number `j` to the correct object index and GIS identifier.
    That mapping is necessary so each output record can be tied to the specific reservoir
    object being reported.'
---

<!-- facts:header -->

Outputs reservoir salt mass-balance results for one reservoir object. It rolls daily totals into monthly, yearly, and average-annual summaries and writes the selected records to the reservoir salt output units.

## Bottom Line

`res_salt_output` is the reservoir-salt reporting routine. For the reservoir index `j`, it maps that reservoir to the global object list, adds the current day’s salt balances into the running monthly totals, and writes daily output when `pco%salt_res%d` is enabled. It also, at month end, rolls monthly totals into yearly totals, computes monthly average mass/concentration by dividing by the number of days in the month, writes monthly output if requested, and clears the monthly accumulators.

At year end it rolls yearly totals into the long-term annual accumulators, computes yearly average mass/concentration by dividing by `time%day_end_yr`, writes yearly output if requested, and clears the yearly accumulators. At the end of the simulation, if average-annual reservoir-salt output is enabled, it divides the accumulated totals by `time%nbyr` and writes the final average-annual record. The routine matters because it turns the daily reservoir salt balance state in `res_salt_module` into the period summaries used by SWAT+ output files.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine inside the reservoir output loop after `reservoir_output(j)` and `res_pesticide_output(j)`, and only when `cs_db%num_salts > 0`. That means reservoir and pesticide-related setup has already been done, including the reservoir index mapping needed for `ob(iob)%gis_id`. The results feed the SWAT+ reservoir salt output files that downstream analysis uses for daily, monthly, yearly, and average-annual reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the reservoir index to the object list | Compute `iob = sp_ob1%res + j - 1` so the current reservoir output call can use the correct object connectivity entry and GIS identifier. |
| 2. Accumulate daily salt values into the monthly totals | For each salt ion, add the current day’s inflow, outflow, seepage, fertilizer, irrigation, diversion, mass, concentration, and volume into the monthly accumulator arrays `ressalt_m(j)` from `ressalt_d(j)`. |
| 3. Write daily reservoir output when enabled | If `pco%salt_res%d` is enabled, write the daily text record to unit 5040 and, when `pco%csvout` is enabled, write the matching CSV record to unit 5041 using the daily salt balances for the current reservoir. |
| 4. Roll monthly totals into yearly totals at month end | When `time%end_mo == 1`, add the completed monthly totals from `ressalt_m(j)` into `ressalt_y(j)` so yearly accumulation includes the month that just finished. |
| 5. Convert monthly mass and concentration totals to monthly averages | Compute the number of days in the month with `const = float (ndays(time%mo + 1) - ndays(time%mo))`, then divide monthly mass and concentration, plus reservoir volume, by that count so the monthly output reports averages rather than raw sums for those fields. |
| 6. Write monthly output when enabled and clear monthly accumulators | If `pco%salt_res%m` is enabled, write the monthly text record to unit 5042 and the optional CSV record to unit 5043; then reset all monthly salt fields and volume back to zero so the next month starts fresh. |
| 7. Roll yearly totals into the annual accumulator at year end | When `time%end_yr == 1`, add yearly totals from `ressalt_y(j)` into the long-term annual accumulator `ressalt_a(j)` so the simulation retains the sum across years. |
| 8. Convert yearly mass and concentration totals to yearly averages | Use `const = time%day_end_yr` as the divisor for the completed year, then divide yearly mass, concentration, and reservoir volume by that day count so yearly output represents average values. |
| 9. Write yearly output when enabled and clear yearly accumulators | If `pco%salt_res%y` is enabled, write the yearly text record to unit 5044 and the optional CSV record to unit 5045; then zero the yearly salt fields and volume for the next year. |
| 10. Produce average-annual output at the end of the simulation | If the simulation is ending and `pco%salt_res%a` is enabled, divide the annual totals by `time%nbyr`, write the average-annual text record to unit 5046, and write the optional CSV record to unit 5047. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pesticide_module] | `output_ls_pesticide_module` | `No candidate outside references were resolved to this module in the context packet.` |
| [sym:res_pesticide_module] | `res_pesticide_module` | `No candidate outside references were resolved to this module in the context packet.` |
| [sym:res_salt_module] | `ressalt_m, ressalt_d, ressalt_y, ressalt_a` | `ressalt_m(j)%salt(isalt)%inflow, ressalt_d(j)%salt(isalt)%inflow, ressalt_m(j)%salt(isalt)%outflow, ressalt_d(j)%salt(isalt)%outflow, ressalt_m(j)%salt(isalt)%seep, ressalt_d(j)%salt(isalt)%seep, ressalt_m(j)%salt(isalt)%fert, ressalt_d(j)%salt(isalt)%fert, ressalt_m(j)%salt(isalt)%irrig, ressalt_d(j)%salt(isalt)%irrig, ressalt_m(j)%salt(isalt)%div, ressalt_d(j)%salt(isalt)%div, ressalt_m(j)%salt(isalt)%mass, ressalt_d(j)%salt(isalt)%mass, ressalt_m(j)%salt(isalt)%conc, ressalt_d(j)%salt(isalt)%conc, ressalt_m(j)%salt(1)%volm, ressalt_d(j)%salt(1)%volm, ressalt_y(j)%salt(isalt)%inflow, ressalt_y(j)%salt(isalt)%outflow, ressalt_y(j)%salt(isalt)%seep, ressalt_y(j)%salt(isalt)%fert, ressalt_y(j)%salt(isalt)%irrig, ressalt_y(j)%salt(isalt)%div, ressalt_y(j)%salt(isalt)%mass, ressalt_y(j)%salt(isalt)%conc, ressalt_y(j)%salt(1)%volm, ressalt_a(j)%salt(isalt)%inflow, ressalt_a(j)%salt(isalt)%outflow, ressalt_a(j)%salt(isalt)%seep, ressalt_a(j)%salt(isalt)%fert, ressalt_a(j)%salt(isalt)%irrig, ressalt_a(j)%salt(isalt)%div, ressalt_a(j)%salt(isalt)%mass, ressalt_a(j)%salt(isalt)%conc, ressalt_a(j)%salt(1)%volm` |
| [sym:plant_module] | `plant_module` | `No candidate outside references were resolved to this module in the context packet.` |
| [sym:plant_data_module] | `plant_data_module` | `No candidate outside references were resolved to this module in the context packet.` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr` |
| [sym:basin_module] | `pco` | `pco%salt_res%d, pco%csvout, pco%salt_res%m, pco%salt_res%y, pco%salt_res%a` |
| [sym:output_landscape_module] | `output_landscape_module` | `No candidate outside references were resolved to this module in the context packet.` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%res` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ressalt_m(j)%salt(isalt)%inflow` | Always, before any output gating | This monthly accumulator is increased by the current day's inflow for each salt ion so month-end output can report the sum of daily inflows. |
| `ressalt_m(j)%salt(isalt)%outflow` | Always, before any output gating | This monthly accumulator is increased by the current day's outflow for each salt ion so month-end output can report the sum of daily outflows. |
| `ressalt_m(j)%salt(isalt)%seep` | Always, before any output gating | This monthly accumulator is increased by the current day's seepage for each salt ion so month-end output can report the sum of daily seepage losses. |
| `ressalt_m(j)%salt(isalt)%fert` | Always, before any output gating | This monthly accumulator is increased by the current day's fertilizer addition for each salt ion so month-end output can report the monthly fertilizer contribution. |
| `ressalt_m(j)%salt(isalt)%irrig` | Always, before any output gating | This monthly accumulator is increased by the current day's irrigation diversion for each salt ion so month-end output can report the monthly irrigation removal. |
| `ressalt_m(j)%salt(isalt)%div` | Always, before any output gating | This monthly accumulator is increased by the current day's diversion term for each salt ion so month-end output can report diversion-related salt exchange. |
| `ressalt_m(j)%salt(isalt)%mass` | Always, before any output gating | This monthly accumulator is increased by the current day's end-of-day mass for each salt ion so month-end output can later compute a monthly average mass. |
| `ressalt_m(j)%salt(isalt)%conc` | Always, before any output gating | This monthly accumulator is increased by the current day's end-of-day concentration for each salt ion so month-end output can later compute a monthly average concentration. |
| `ressalt_m(j)%salt(1)%volm` | Always, before any output gating | This monthly volume accumulator is increased by the current day's reservoir volume, then later averaged and reset with the other monthly fields. |
| `ressalt_y(j)%salt(isalt)%inflow` | Only when `time%end_mo == 1` | At month end, the completed monthly inflow totals are added into the yearly accumulator so the year-end record includes all months processed so far. |
| `ressalt_y(j)%salt(isalt)%outflow` | Only when `time%end_mo == 1` | At month end, the completed monthly outflow totals are added into the yearly accumulator so the year-end record includes all months processed so far. |
| `ressalt_y(j)%salt(isalt)%seep` | Only when `time%end_mo == 1` | At month end, the completed monthly seepage totals are added into the yearly accumulator so the year-end record includes all months processed so far. |
| `ressalt_y(j)%salt(isalt)%fert` | Only when `time%end_mo == 1` | At month end, the completed monthly fertilizer totals are added into the yearly accumulator so the year-end record includes all months processed so far. |
| `ressalt_y(j)%salt(isalt)%irrig` | Only when `time%end_mo == 1` | At month end, the completed monthly irrigation totals are added into the yearly accumulator so the year-end record includes all months processed so far. |
| `ressalt_y(j)%salt(isalt)%div` | Only when `time%end_mo == 1` | At month end, the completed monthly diversion totals are added into the yearly accumulator so the year-end record includes all months processed so far. |
| `ressalt_y(j)%salt(isalt)%mass` | Only when `time%end_mo == 1` | At month end, the completed monthly mass totals are added into the yearly accumulator so the year-end record includes all months processed so far. |
| `ressalt_y(j)%salt(isalt)%conc` | Only when `time%end_mo == 1` | At month end, the completed monthly concentration totals are added into the yearly accumulator so the year-end record includes all months processed so far. |
| `ressalt_y(j)%salt(1)%volm` | Only when `time%end_mo == 1` | At month end, the completed monthly volume total is added into the yearly accumulator so the year-end record includes reservoir volume in the annual totals. |
| `ressalt_a(j)%salt(isalt)%inflow` | Only when `time%end_yr == 1` | At year end, the completed yearly inflow totals are added into the long-term annual accumulator so the simulation can later compute average-annual inflow. |
| `ressalt_a(j)%salt(isalt)%outflow` | Only when `time%end_yr == 1` | At year end, the completed yearly outflow totals are added into the long-term annual accumulator so the simulation can later compute average-annual outflow. |
| `ressalt_a(j)%salt(isalt)%seep` | Only when `time%end_yr == 1` | At year end, the completed yearly seepage totals are added into the long-term annual accumulator so the simulation can later compute average-annual seepage. |
| `ressalt_a(j)%salt(isalt)%fert` | Only when `time%end_yr == 1` | At year end, the completed yearly fertilizer totals are added into the long-term annual accumulator so the simulation can later compute average-annual fertilizer contribution. |
| `ressalt_a(j)%salt(isalt)%irrig` | Only when `time%end_yr == 1` | At year end, the completed yearly irrigation totals are added into the long-term annual accumulator so the simulation can later compute average-annual irrigation removal. |
| `ressalt_a(j)%salt(isalt)%div` | Only when `time%end_yr == 1` | At year end, the completed yearly diversion totals are added into the long-term annual accumulator so the simulation can later compute average-annual diversion exchange. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved. The procedure was introduced in df07e3f as a new subroutine that accumulates daily reservoir salt balances into monthly, yearly, and average-annual totals and writes text/CSV outputs. In 39fabde, the local counters `isalt`, `iob`, and `const` were initialized to `0`/`0.`. In 2fe89fd, the CSV writes for daily, monthly, yearly, and average-annual outputs were changed from `G0.3` to `G0.6` formatting. In 35b029c, only whitespace at the end of the procedure changed; the computational logic was unchanged.

- df07e3f added the full reservoir salt output workflow: daily accumulation into monthly totals, monthly rollup into yearly totals, yearly rollup into annual totals, period-end averaging, optional CSV mirrors, and zeroing of periodic accumulators.
- 39fabde initialized the local loop/index/scratch variables `isalt`, `iob`, and `const`, reducing reliance on implicit initialization.
- 2fe89fd increased CSV numeric precision for the reservoir salt output files by switching the `G0.3` edit descriptor to `G0.6` on units 5041, 5043, 5045, and 5047.
- 35b029c made no behavioral change; it only adjusted trailing whitespace near the return/end of the subroutine.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_salt_output' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft 4-step outline into the 10 source-backed processing stages visible in the routine.
