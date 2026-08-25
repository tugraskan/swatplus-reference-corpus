---
kind: procedure
symbol: gwflow_output_yr
title: gwflow_output_yr
status: filled
source_hash: 70f2e6c65066a768
version_label: SWAT+ 62.0.0
locals:
  i: Loop index for cells and HRUs; it drives the per-cell yearly output, accumulator updates,
    and zeroing passes.
  j: Declared but not used in the visible source for this routine.
  k: Loop index for groundwater observation wells when yearly observation output is written.
  s: Loop index for solutes; it selects which solute-specific yearly totals are averaged,
    written, and cleared.
  iob: Index into the `ob` array for HRU pumping output; it maps an HRU index to the corresponding
    object record.
  gis_id: Cell GIS identifier written to the yearly cell output; it is taken from `cell_gis_id(i)`
    for each active cell.
  wtdepth: Computed water-table depth for the yearly cell output, equal to `gw_state(i)%elev
    - gw_state(i)%hdyr` after `hdyr` is averaged.
  day_yr_r: Real-valued form of `time%day_end_yr`, used as the divisor when converting yearly
    accumulated sums into daily averages.
  obs_temp: Temporary yearly groundwater temperature for an observation well; set to `-99.`
    unless heat output is enabled.
  obs_no3: Temporary yearly nitrate concentration for an observation well; set from `gwsol_state(i)%solute(1)%cnyr`
    when solute output is enabled.
  obs_p: Temporary yearly phosphorus concentration for an observation well; set from `gwsol_state(i)%solute(2)%cnyr`
    when solute output is enabled.
  obs_name: Formatted observation-well label like `obs_0001` that is written with the yearly
    observation output record.
uses:
  gwflow_module: '`gwflow_module` owns all the groundwater state and yearly summary arrays
    that this routine averages, writes, accumulates into AA storage, and resets. Without those
    module arrays, the annual groundwater cell, basin, heat, and solute outputs could not
    be produced.'
  hydrograph_module: This module supplies the observation-well mapping and the annual observation
    accumulators that yearly groundwater output updates. Those values are what let the routine
    write per-well yearly records and carry them forward for average-annual summaries.
  sd_channel_module: This module provides the HRU pumping totals that are written in yearly
    long format and then accumulated into the average-annual pump totals before being cleared.
  time_module: '`time_module` controls the year-end gate and provides the date fields written
    into every yearly output record. `time%end_yr` decides whether the routine runs, and `time%day`,
    `time%mo`, `time%day_mo`, `time%yrc`, and `time%day_end_yr` are used in the calculations
    and record headers.'
  basin_module: '`basin_module` provides `bsn%name`, which is written in the basin-level yearly
    water, heat, and solute balance records to identify the basin being reported.'
---

<!-- facts:header -->

Writes the annual groundwater output block for SWAT+ long-format reporting. It outputs per-cell yearly averages plus basin water, heat, solute, and HRU pumping summaries, then clears the yearly accumulators for the next year.

## Bottom Line

`gwflow_output_yr` runs only at the end of a simulation year. It converts the year's accumulated groundwater head, flux, heat, and solute totals into annual averages, writes the yearly output records, and then resets the yearly storage so the next year starts clean.

The routine also rolls yearly values into average-annual accumulators such as `gw_hyd_ss_aa` and `gw_head_sum_aa`. That matters because the final average-annual reporting later in the run depends on these updated summaries.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `gwflow_simulate` when `time%end_yr == 1`, after the year's daily and monthly groundwater calculations have already accumulated totals in the yearly state arrays. Its outputs feed the annual long-format files and the average-annual accumulation path that is finalized later at the end of the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Return immediately unless the current timestep is the end of a year. | The routine checks `time%end_yr`; if it is not 1, the subroutine exits without changing any annual outputs or accumulators. Otherwise it converts `time%day_end_yr` to a real divisor in `day_yr_r`. |
| 2. Convert annual groundwater head totals to yearly averages. | For every cell, the accumulated yearly groundwater head in `gw_state(i)%hdyr` is divided by the number of days in the year. This turns the running sum into an annual average head before output and further accumulation. |
| 3. Convert annual groundwater temperature totals when heat output is enabled, then clear the yearly temperature accumulator. | If `gw_heat_flag == 1`, the routine averages `gwheat_state(i)%tpyr` over the year for each cell, then resets that yearly temperature accumulator to zero so the next year starts from a clean sum. |
| 4. Convert annual solute concentration totals when solute output is enabled, then clear each yearly solute accumulator. | If `gw_solute_flag == 1`, the routine loops over solutes and cells, divides `gwsol_state(i)%solute(s)%cnyr` by the number of days in the year, and then resets the yearly concentration sum to zero for the next year. |
| 5. Convert yearly groundwater flux sums to average daily fluxes. | For each cell, yearly sums in `gw_hyd_ss_yr` are divided by `day_yr_r` so the yearly output reports average daily rates for recharge, ET, groundwater-surface exchange, lateral flow, boundary exchange, pumping components, and landscape exchange terms. |
| 6. Write the yearly long-format groundwater-cell records for active cells. | If yearly groundwater output is enabled, the routine loops over active cells, computes `gis_id` from `cell_gis_id(i)`, computes `wtdepth` from the averaged head, and writes one long-format record per active cell to `out_gwcell_yr`. |
| 7. Roll yearly cell averages into average-annual accumulators. | The routine adds each cell's averaged yearly head into `gw_head_sum_aa` and adds each yearly flux component into `gw_hyd_ss_aa`. These accumulators preserve the running multi-year average-annual totals. |
| 8. Write yearly observation-well output and update observation AA accumulators. | When observation output is enabled, the routine maps each observation well to its cell, optionally pulls yearly heat and solute values, writes the yearly observation record, and adds the values into `gw_obs_temp_aa` and `gw_obs_sol_aa` for later average-annual reporting. |
| 9. Reset the yearly groundwater head accumulator for the next year. | After output and AA accumulation are complete, the routine zeroes `gw_state(i)%hdyr` so the next year begins a fresh running head sum. |
| 10. Convert and retain yearly heat-flux sums when heat output is enabled. | If heat output is enabled, the yearly heat-flux totals in `gw_heat_ss_yr` are converted from joules to megajoules per day by dividing by 1,000,000 and by `day_yr_r`. The values are kept until they are cleared later in the routine. |
| 11. Convert and retain yearly solute-flux sums when solute output is enabled. | If solute output is enabled, the routine converts the yearly solute flux totals in `gwsol_ss_sum` from grams to kilograms per day by dividing by 1000 and by `day_yr_r`. The values are kept until they are cleared later in the routine. |
| 12. Write yearly HRU pumping output and accumulate it into AA totals. | If pumping output is enabled, the routine loops through HRUs, writes a yearly pumping record for positive values, adds each yearly pump amount into `hru_pump_aa`, and then clears `hru_pump_yr` for the next year. |
| 13. Clear the yearly groundwater, heat, and solute flux accumulators for the next year. | The routine zeroes `gw_hyd_ss_yr`, `gw_heat_ss_yr`, and `gwsol_ss_sum` component by component so the next year's accumulation starts from zero for every flux path. |
| 14. Write basin-level yearly water, heat, and solute balances, then clear their annual totals. | If yearly output is enabled, the routine writes basin water balance to `out_gwbal_yr`, heat balance to `out_heatbal_yr` when heat output is active, and solute balances to `out_solbal_yr+s` when solute output is active. It then clears the basin-level yearly accumulators for the next year. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss_yr, gw_head_sum_aa, gw_hyd_ss_aa, gw_heat_ss_yr` | `gw_state(i)%hdyr, gw_hyd_ss_yr(i)%rech, gw_hyd_ss_yr(i)%gwet, gw_hyd_ss_yr(i)%gwsw, gw_hyd_ss_yr(i)%swgw, gw_hyd_ss_yr(i)%satx, gw_hyd_ss_yr(i)%soil, gw_hyd_ss_yr(i)%latl, gw_hyd_ss_yr(i)%bndr, gw_hyd_ss_yr(i)%ppag, gw_hyd_ss_yr(i)%ppdf, gw_hyd_ss_yr(i)%ppex, gw_hyd_ss_yr(i)%tile, gw_hyd_ss_yr(i)%resv, gw_hyd_ss_yr(i)%wetl, gw_hyd_ss_yr(i)%canl, gw_hyd_ss_yr(i)%fpln, gw_hyd_ss_yr(i)%pond, gw_hyd_ss_yr(i)%phyt, gw_state(i)%elev, gw_hyd_ss_aa(i)%rech, gw_hyd_ss_aa(i)%gwet, gw_hyd_ss_aa(i)%gwsw, gw_hyd_ss_aa(i)%swgw, gw_hyd_ss_aa(i)%satx, gw_hyd_ss_aa(i)%soil, gw_hyd_ss_aa(i)%latl, gw_hyd_ss_aa(i)%ppag, gw_hyd_ss_aa(i)%ppex, gw_hyd_ss_aa(i)%tile, gw_hyd_ss_aa(i)%resv, gw_hyd_ss_aa(i)%wetl, gw_hyd_ss_aa(i)%fpln, gw_hyd_ss_aa(i)%canl, gw_hyd_ss_aa(i)%pond, gw_hyd_ss_aa(i)%phyt, gw_heat_ss_yr(i)%rech, gw_heat_ss_yr(i)%gwet, gw_heat_ss_yr(i)%gwsw, gw_heat_ss_yr(i)%swgw, gw_heat_ss_yr(i)%satx, gw_heat_ss_yr(i)%soil, gw_heat_ss_yr(i)%latl, gw_heat_ss_yr(i)%disp, gw_heat_ss_yr(i)%bndr, gw_heat_ss_yr(i)%ppag, gw_heat_ss_yr(i)%ppex, gw_heat_ss_yr(i)%tile, gw_heat_ss_yr(i)%resv, gw_heat_ss_yr(i)%wetl, gw_heat_ss_yr(i)%canl, gw_heat_ss_yr(i)%fpln, gw_heat_ss_yr(i)%pond` |
| [sym:hydrograph_module] | `hydrograph_module` | `gw_obs_cells(k), gw_obs_temp_aa(k), gw_obs_sol_aa(k,1), gw_obs_sol_aa(k,2)` |
| [sym:sd_channel_module] | `sd_channel_module` | `hru_pump_yr(i), hru_pump_aa(i)` |
| [sym:time_module] | `time` | `time%end_yr, time%day_end_yr, time%day, time%mo, time%day_mo, time%yrc` |
| [sym:basin_module] | `bsn` | `bsn` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_state(i)%hdyr` | When `time%end_yr == 1`, before writing yearly output | The running yearly groundwater-head sum is divided by the number of days in the year to become an annual average head, then later reset to zero for the next year. |
| `gwheat_state(i)%tpyr` | When `time%end_yr == 1` and `gw_heat_flag == 1` | The running yearly groundwater-temperature sum is converted to an annual average temperature, written into observation output if needed, and then cleared for the next year. |
| `gwsol_state(i)%solute(s)%cnyr` | When `time%end_yr == 1` and `gw_solute_flag == 1` | The running yearly solute concentration sum is divided by the number of days in the year to form an annual average concentration, then cleared for the next year. |
| `gw_hyd_ss_yr(i)%rech` | When `time%end_yr == 1` | The yearly recharge total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%gwet` | When `time%end_yr == 1` | The yearly groundwater-ET total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%gwsw` | When `time%end_yr == 1` | The yearly groundwater-to-surface-water exchange total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%swgw` | When `time%end_yr == 1` | The yearly surface-water-to-groundwater exchange total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%satx` | When `time%end_yr == 1` | The yearly saturation-excess flow total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%soil` | When `time%end_yr == 1` | The yearly groundwater-to-soil exchange total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%latl` | When `time%end_yr == 1` | The yearly lateral-flow total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%bndr` | When `time%end_yr == 1` | The yearly boundary-exchange total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%ppag` | When `time%end_yr == 1` | The yearly allocation-driven pumping total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%ppdf` | When `time%end_yr == 1` | The yearly pumping-deficit total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%ppex` | When `time%end_yr == 1` | The yearly external-pumping total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%tile` | When `time%end_yr == 1` | The yearly tile-drainage total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%resv` | When `time%end_yr == 1` | The yearly reservoir-exchange total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%wetl` | When `time%end_yr == 1` | The yearly wetland-exchange total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%canl` | When `time%end_yr == 1` | The yearly canal-exchange total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%fpln` | When `time%end_yr == 1` | The yearly floodplain-exchange total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%pond` | When `time%end_yr == 1` | The yearly recharge-pond seepage total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_hyd_ss_yr(i)%phyt` | When `time%end_yr == 1` | The yearly phreatophyte transpiration total is converted to an average daily rate for output, then cleared to zero later in the routine. |
| `gw_head_sum_aa(i)` | When `time%end_yr == 1` | The annual-average accumulator receives the year's averaged groundwater head so it can later support average-annual reporting. |
| `gw_hyd_ss_aa(i)%rech` | When `time%end_yr == 1` | The average-annual groundwater recharge accumulator is increased by the year's averaged recharge before yearly flux arrays are cleared. |
| `gw_hyd_ss_aa(i)%gwet` | When `time%end_yr == 1` and `gw_heat_flag == 1` | The average-annual groundwater-ET accumulator is increased by the year's averaged heat-related or groundwater flux counterpart before annual reset. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The yearly output routine was introduced in the 2026-03-31 gwflow re-merge as a stub, then the 2026-04-02 output redesign expanded it to SWAT+ long-format output with print.prt integration and standardized formats, and the 2026-04-16 robustness pass added the `gis_id` handling used in the yearly cell write logic before the 2026-06-02 rework switched yearly cell and observation records to `cell_gis_id`/`cell_name` and updated the long-format `a12` cell-name field.

- 9d9069c introduced `gwflow_output_yr` as an empty yearly-output stub within the new gwflow output file.
- 7ff5029 replaced the stub with real yearly long-format reporting, added basin/obs/pump outputs, and integrated `basin_module` plus standardized output formats.
- 2a5e8de added local `gis_id` handling for yearly output and guarded it by grid type.
- 3cc92b5 changed yearly cell and observation writes to use `cell_gis_id(i)` and `cell_name(i)`, and widened format 140 to `a12` for the yearly long-format cell name field.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_output_yr' has no extracted documentation comment.
- algorithm_steps revised: merged the source-driven flow into 14 steps matching the visible yearly-output sequence, keeping every source_lines citation within the provided line-number block.
- `hydrograph_module` and `sd_channel_module` had no resolved candidate outside references in the packet; their role is inferred from the yearly observation and pumping writes in the routine body.
- `j` is declared in the source but not used in the visible yearly routine body; this may be a leftover from sibling output routines.
