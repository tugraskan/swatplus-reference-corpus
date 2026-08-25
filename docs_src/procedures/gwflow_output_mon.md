---
kind: procedure
symbol: gwflow_output_mon
title: gwflow_output_mon
status: filled
source_hash: 56bb65d59718d2b7
version_label: SWAT+ 62.0.0
locals:
  i: Loop index for cells and HRUs; also reused to point to the active cell serving an observation
    well.
  j: Declared locally but not used in the visible source for this routine.
  k: Loop index for groundwater observation wells.
  s: Loop index for solute species when averaging, writing, and clearing solute monthly totals.
  iob: Temporary object index into `ob`; used to map HRU pumping output records to the correct
    hydrograph object entry.
  gis_id: Per-cell GIS identifier written to the monthly cell output row; taken from `cell_gis_id(i)`.
  wtdepth: Monthly groundwater depth below land surface, computed as `gw_state(i)%elev - gw_state(i)%hdmo`
    for the cell output record.
  day_mo_r: Real-valued copy of `time%day_mo` used as the divisor when converting monthly
    sums to daily averages.
  obs_temp: Temporary monthly observation-well groundwater temperature; set to -99 until the
    heat module is active.
  obs_no3: Temporary monthly observation-well nitrate concentration from solute 1; set to
    -99 until the solute module is active.
  obs_p: Temporary monthly observation-well phosphorus concentration from solute 2; set to
    -99 until the solute module is active.
  obs_name: Formatted observation-well label such as `obs_0001`, written with the observation
    output record.
uses:
  gwflow_module: This module owns the groundwater state and monthly accumulators that the
    routine averages, writes, and resets. Without `gw_state`, `gw_hyd_ss_mo`, and `gw_hyd_grid_mo`,
    there would be no month-end groundwater heads, flux totals, or basin balance values to
    report.
  hydrograph_module: This module supplies the mapping from HRU indices to hydrologic objects
    and names. `sp_ob` and `sp_ob1` determine how many HRUs are iterated for pumping output,
    and `ob(iob)%name`/`ob(iob)%gis_id` provide the identifiers written to the HRU pumping
    records.
  sd_channel_module: The module is imported in the routine interface, but the extracted source
    shows no direct use of its symbols here; it does not affect the visible monthly output
    logic.
  time_module: The month-end decision and the date fields written to every record come from
    `time`. The routine only runs on `time%end_mo == 1` and stamps each record with `time%day`,
    `time%mo`, `time%day_mo`, and `time%yrc`.
  basin_module: The basin name is written into the basin and solute balance lines, so `bsn%name`
    provides the human-readable basin identifier for monthly balance output.
---

<!-- facts:header -->

Writes monthly groundwater output in SWAT+ long format at the end of each month. It reports per-cell averages, observation-well values, HRU pumping totals, and basin/grid groundwater and solute monthly balances.

## Bottom Line

This routine only runs when `time%end_mo == 1`, so it is the month-end reporting/reset point for the groundwater flow system. It converts the month’s accumulated heads, fluxes, and solute values into monthly averages, writes the requested output records, and then clears the monthly accumulators for the next month.

The monthly reports cover cell-level groundwater state, optional observation wells, optional HRU pumping, basin-wide groundwater balance, and optional solute balance. Because the routine also zeroes the monthly sums afterward, later model steps rely on it to both publish the month’s results and prepare the accumulation arrays for the next month.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`gwflow_simulate` calls this routine at the end of each simulated month, after daily groundwater output has already been produced and while the month-end accumulators are still intact. Its results feed the monthly output files and the reset of monthly groundwater, pumping, and solute accumulation arrays that the next month’s daily calculations depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Enter only at month end. | The routine checks `time%end_mo`; if it is not the end of the month, it does nothing. When it is month end, it converts `time%day_mo` to a real divisor for averaging monthly totals. |
| 2. Average monthly groundwater head and optional temperature. | It divides each cell’s accumulated monthly groundwater head by the number of days in the month. If groundwater heat output is enabled, it also divides monthly groundwater temperature sums by the day count and then clears the temperature monthly accumulator for the next month. |
| 3. Average monthly solute concentration if solutes are active. | When solute output is enabled, it loops over each solute species and each cell, divides the monthly concentration sums by the day count, and then resets those concentration accumulators to zero for the next month. |
| 4. Write HRU pumping output and clear the pumping sum. | If pumping output is enabled, it loops across HRUs, writes a record for each HRU with a positive monthly pumping total, and uses `sp_ob1%hru` plus the HRU index to map into `ob`. After the loop it clears `hru_pump_mo` to start the next month at zero. |
| 5. Average monthly groundwater flux components for each cell. | It divides the monthly groundwater-source/sink sums for each cell by the month length to convert them to average daily values for all listed flux components. |
| 6. Write monthly cell-level groundwater output. | If monthly cell output is enabled, it loops over active cells, gets the GIS identifier from `cell_gis_id(i)`, computes water-table depth from the averaged head, and writes one long-format record per active cell with the monthly groundwater state and flux averages. |
| 7. Write monthly observation-well output. | If observation-well output is enabled, it loops over observation wells, maps each well to its cell, fills optional temperature and solute values when those modules are active, formats the well name as `obs_nnnn`, and writes one monthly observation record per well. |
| 8. Reset monthly groundwater head and flux accumulators. | It clears the monthly groundwater head sum and all monthly groundwater flux components for every cell so the next month starts with zeroed accumulators. |
| 9. Clear monthly solute flux accumulators. | When solute tracking is active, it loops over cells and solutes and zeros the monthly solute transport accumulators for each species. |
| 10. Write monthly basin groundwater balance. | If monthly groundwater balance output is enabled, it writes the basin-level monthly groundwater totals, including change in storage and all groundwater flux components, to the basin balance file. |
| 11. Reset monthly basin groundwater accumulators. | It clears the basin monthly groundwater totals so the next month can accumulate independently. |
| 12. Write and clear monthly solute balance by species. | When solutes are active, it writes each solute’s basin monthly balance record if monthly output is enabled, then zeros every solute basin accumulator for that species. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss_mo, gw_hyd_grid_mo` | `gw_state(i)%hdmo, gw_hyd_ss_mo(i)%rech, gw_hyd_ss_mo(i)%gwet, gw_hyd_ss_mo(i)%gwsw, gw_hyd_ss_mo(i)%swgw, gw_hyd_ss_mo(i)%satx, gw_hyd_ss_mo(i)%soil, gw_hyd_ss_mo(i)%latl, gw_hyd_ss_mo(i)%bndr, gw_hyd_ss_mo(i)%ppag, gw_hyd_ss_mo(i)%ppdf, gw_hyd_ss_mo(i)%ppex, gw_hyd_ss_mo(i)%tile, gw_hyd_ss_mo(i)%resv, gw_hyd_ss_mo(i)%wetl, gw_hyd_ss_mo(i)%canl, gw_hyd_ss_mo(i)%fpln, gw_hyd_ss_mo(i)%pond, gw_hyd_ss_mo(i)%phyt, gw_state(i)%elev, gw_hyd_grid_mo%chng, gw_hyd_grid_mo%rech, gw_hyd_grid_mo%gwet, gw_hyd_grid_mo%gwsw, gw_hyd_grid_mo%swgw, gw_hyd_grid_mo%satx, gw_hyd_grid_mo%soil, gw_hyd_grid_mo%latl, gw_hyd_grid_mo%bndr, gw_hyd_grid_mo%ppag, gw_hyd_grid_mo%ppex, gw_hyd_grid_mo%tile, gw_hyd_grid_mo%resv, gw_hyd_grid_mo%wetl, gw_hyd_grid_mo%canl, gw_hyd_grid_mo%fpln, gw_hyd_grid_mo%pond, gw_hyd_grid_mo%phyt, gw_hyd_grid_mo%ppdf` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(iob)%name` |
| [sym:sd_channel_module] | `No imported `sd_channel_module` state or type is referenced in the visible lines of this routine.` |  |
| [sym:time_module] | `time` | `time%end_mo, time%day_mo, time%day, time%mo, time%yrc` |
| [sym:basin_module] | `bsn` | `bsn%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_state(i)%hdmo` | When `time%end_mo == 1`, before the monthly cell output is written. | The monthly groundwater head sum is divided by the number of days in the month and then reset to zero after the month-end reports are written, so it becomes the month’s average head rather than a running sum. |
| `gwheat_state(i)%tpmo` | When `time%end_mo == 1` and `gw_heat_flag == 1`. | The monthly groundwater temperature sum is converted to a monthly average and then cleared so the next month begins with no carried-over heat total. |
| `gwsol_state(i)%solute(s)%cnmo` | When `time%end_mo == 1` and `gw_solute_flag == 1`. | Each solute’s monthly concentration sum is averaged over the month and then reset so the next month can accumulate fresh solute values. |
| `hru_pump_mo` | When `time%end_mo == 1` and `gwflag_pump == 1`. | The HRU pumping totals are written for the month and then cleared to zero, so the next month’s pumping can accumulate independently. |
| `gw_hyd_ss_mo(i)%rech` | When `time%end_mo == 1`. | The monthly recharge total is converted to its monthly-average form for output, then cleared for the next month’s accumulation. |
| `gw_hyd_ss_mo(i)%gwet` | When `time%end_mo == 1`. | The monthly groundwater ET total is converted to an average and then cleared after the month-end report is produced. |
| `gw_hyd_ss_mo(i)%gwsw` | When `time%end_mo == 1`. | The groundwater-to-surface-water exchange total is averaged and then zeroed so the next month starts clean. |
| `gw_hyd_ss_mo(i)%swgw` | When `time%end_mo == 1`. | The surface-water-to-groundwater exchange total is averaged for output and then cleared. |
| `gw_hyd_ss_mo(i)%satx` | When `time%end_mo == 1`. | The saturation-excess flux total is averaged and then reset after monthly reporting. |
| `gw_hyd_ss_mo(i)%soil` | When `time%end_mo == 1`. | The groundwater-to-soil flux total is averaged and then cleared for the next month. |
| `gw_hyd_ss_mo(i)%latl` | When `time%end_mo == 1`. | The lateral groundwater exchange total is averaged and then reset to zero after output. |
| `gw_hyd_ss_mo(i)%bndr` | When `time%end_mo == 1`. | The boundary exchange total is averaged for the month-end record and then cleared. |
| `gw_hyd_ss_mo(i)%ppag` | When `time%end_mo == 1`. | The allocation-driven pumping total is averaged and then reset so it does not carry into the next month. |
| `gw_hyd_ss_mo(i)%ppdf` | When `time%end_mo == 1`. | The pumping-deficit total is averaged and then cleared after monthly output. |
| `gw_hyd_ss_mo(i)%ppex` | When `time%end_mo == 1`. | The external pumping total is averaged and then zeroed for the next month. |
| `gw_hyd_ss_mo(i)%tile` | When `time%end_mo == 1`. | The tile drainage monthly total is averaged and then cleared after the report is written. |
| `gw_hyd_ss_mo(i)%resv` | When `time%end_mo == 1`. | The reservoir exchange monthly total is averaged and then reset to zero. |
| `gw_hyd_ss_mo(i)%wetl` | When `time%end_mo == 1`. | The wetland exchange monthly total is averaged and then cleared. |
| `gw_hyd_ss_mo(i)%canl` | When `time%end_mo == 1`. | The canal exchange monthly total is averaged and then reset for the next month. |
| `gw_hyd_ss_mo(i)%fpln` | When `time%end_mo == 1`. | The floodplain exchange monthly total is averaged and then cleared after output. |
| `gw_hyd_ss_mo(i)%pond` | When `time%end_mo == 1`. | The pond seepage monthly total is averaged and then reset to zero. |
| `gw_hyd_ss_mo(i)%phyt` | When `time%end_mo == 1`. | The phreatophyte transpiration monthly total is averaged and then cleared after reporting. |
| `gwsol_ss_sum_mo(i)%solute(s)%rech` | When `time%end_mo == 1` and `gw_solute_flag == 1`. | The monthly solute recharge accumulator is written in the solute balance output, then cleared so the next month starts from zero. |
| `gwsol_ss_sum_mo(i)%solute(s)%gwsw` | When `time%end_mo == 1` and `gw_solute_flag == 1`. | The monthly solute groundwater-to-surface-water accumulator is written in the solute balance output, then cleared for the next month. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved source-backed lineage commits show two behavior changes to `gwflow_output_mon`. In 2a5e8de, the monthly cell-output path was updated to compute `gis_id` with grid-type-aware logic instead of a fixed expression, and the monthly cell rows continued to use the same long-format write structure. In 3cc92b5, the routine switched monthly cell output to `cell_gis_id(i)` and `cell_name(i)`, and the monthly long-format write layout changed from `a4,i4.4` style cell labeling to `a12` cell names.

- 2a5e8de added structured-vs-unstructured handling for monthly cell GIS IDs and guarded the `gis_id` assignment before the `out_gwcell_mon` write.
- 3cc92b5 replaced the ad hoc GIS-ID logic with `cell_gis_id(i)` and changed the monthly cell output format and label field from generated `gw_####` text to `cell_name(i)`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_output_mon' has no extracted documentation comment.
- sd_channel_module is imported but not referenced in the extracted lines for this routine.
- algorithm_steps revised: condensed the original four-step draft into twelve source-backed month-end actions to match the actual control flow.
- Lineage evidence was resolved; behavior changes were inferred only from the provided diffs.
