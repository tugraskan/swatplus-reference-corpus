---
kind: procedure
symbol: gwflow_output_aa
title: gwflow_output_aa
status: filled
source_hash: aae3d03a0f9fe587
version_label: SWAT+ 62.0.0
locals:
  i: Loop index for HRUs, cells, and observation wells, depending on the section being written;
    also used to select the current cell or HRU record.
  j: Loop index reserved for general iteration support; in this routine it is declared but
    not used in the visible source block.
  k: Loop index for observation wells and for transit-time cell arrays; it selects each well
    or cell in those output sections.
  s: Loop index over groundwater solute species when writing the solute average-annual balance
    files.
  iob: Derived hydrograph object index for the current HRU pumping record; it maps an HRU
    loop position to the corresponding `ob` entry.
  num_months: Declared local integer, but no visible use appears in the source block; its
    role is uncertain from this routine alone.
  gis_id: Per-cell GIS identifier written to the long-format cell output; it is obtained from
    `cell_gis_id(i)` for each active cell.
  wtdepth: Computed water-table depth for the current cell, defined as ground elevation minus
    average annual groundwater head.
  nbyr_r: Real-valued copy of `time%nbyr`, used as the divisor that converts accumulated totals
    into average annual values.
  obs_temp: Average annual groundwater temperature reported for an observation well when heat
    output is enabled; otherwise set to the missing sentinel `-99`.
  obs_no3: Average annual nitrate mass or concentration output for an observation well when
    solute output is enabled; otherwise set to `-99`.
  obs_p: Average annual phosphorus mass or concentration output for an observation well when
    solute output is enabled; otherwise set to `-99`.
  obs_name: Formatted observation-well label built as `obs_####` for the current well index
    and written to the observation output file.
  temp_array: Scratch array used to collect per-cell groundwater transit times before calling
    `gwflow_write_cell_array` for channel and tile transit output.
uses:
  gwflow_module: '`gwflow_module` provides the accumulated groundwater state, balance totals,
    per-cell head sums, and transit-time arrays that this routine converts into average-annual
    output. Without these shared arrays and totals, there would be nothing to summarize or
    write.'
  hydrograph_module: '`hydrograph_module` supplies the HRU/object mapping needed to translate
    pumping output from HRU indices into object IDs and names. It also provides the observation-well
    cell mapping through the shared object connectivity context used by this routine.'
  sd_channel_module: The routine imports `sd_channel_module`, but the provided source block
    does not show any direct references to its symbols. The import appears to be part of the
    broader groundwater output environment, possibly retained for shared output state or consistency
    with related gwflow routines, but no specific resolved symbol from that module is used
    in the visible code.
  time_module: '`time_module` supplies the current date, end-of-simulation markers, and simulation-year
    count used to gate execution to the last day and to format the records that are written.
    It also provides the divisor `time%nbyr` for average-annual normalization.'
  basin_module: '`basin_module` provides the basin name written into the basin balance and
    solute/heat summary headers, identifying the watershed for the output records.'
---

<!-- facts:header -->

Writes average-annual groundwater output at the end of the simulation. It emits long-format HRU pumping, observation-well, cell-level, basin water/heat/solute balance, and groundwater transit-time summaries.

## Bottom Line

`gwflow_output_aa` is the end-of-simulation average-annual groundwater output routine. It runs only on the last simulation day, converts accumulated totals by `time%nbyr`, and writes long-format reports for HRU pumping, observation wells, active-cell groundwater summaries, basin water balance, basin heat balance, and basin solute balances.

It matters because `gwflow_simulate` calls it at the final time step to produce the final groundwater diagnostics used for reporting and post-processing. It also collects groundwater transit-time arrays and sends them to `gwflow_write_cell_array` for output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`gwflow_output_aa` runs at the very end of `gwflow_simulate`, after the yearly output stage and only when `time%yrc == time%yrc_end` and `time%day == time%day_end`. It relies on the upstream daily, monthly, and yearly accumulation work done earlier in the groundwater workflow, and its outputs are the final average-annual summary files consumed after the simulation ends.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Gate execution to the last simulation day | Return immediately unless both `time%yrc == time%yrc_end` and `time%day == time%day_end`, so the routine only writes outputs at the end of the simulation. |
| 2. Set the annual divisor and allocate scratch storage | Convert `time%nbyr` to the real divisor `nbyr_r` and allocate `temp_array(ncell)` for later transit-time output. |
| 3. Write average annual HRU pumping records | If pumping output is enabled, loop over HRUs and write one long-format record for each HRU with positive annual pumping, dividing `hru_pump_aa(i)` by `nbyr_r`. |
| 4. Write average annual observation-well records | If observation output is enabled, loop over observation wells, set missing-value defaults, optionally compute heat and solute averages, build the `obs_####` name, and write one record per well. |
| 5. Write active-cell average annual groundwater summaries | For each active cell, resolve the GIS ID from `cell_gis_id(i)`, compute water-table depth from `gw_state(i)%elev` and the averaged head sum, and write the per-cell long-format groundwater report. |
| 6. Normalize and write basin groundwater balance | Add the final storage-change term to `gw_hyd_grid_aa%chng`, divide the accumulated groundwater balance terms by `nbyr_r`, and write the basin groundwater balance record when annual output is enabled. |
| 7. Normalize and write basin heat balance | Add the final heat-storage change, divide the accumulated heat balance terms by `nbyr_r`, and write the basin heat balance record when annual output is enabled. |
| 8. Normalize and write basin solute balances | For each solute species, add the final storage-change term, divide the accumulated solute fluxes by `nbyr_r`, and write one basin solute balance record when annual output is enabled. |
| 9. Reset the soft-calibration month state | Set `sim_month = 1` so a subsequent simulation starts from the initial monthly state. |
| 10. Write groundwater transit-time arrays | If transit-time output is enabled, copy channel transit times into `temp_array` and call `gwflow_write_cell_array`; if tile transit-time output is enabled, repeat the copy and call for tile times. |
| 11. Release temporary storage and return | Deallocate `temp_array` if it was allocated, then return from the subroutine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss_aa, gw_hyd_grid_aa, gw_heat_grid_aa, gw_head_sum_aa` | `gw_state(i)%elev, gw_hyd_ss_aa(i)%rech, gw_hyd_ss_aa(i)%gwet, gw_hyd_ss_aa(i)%gwsw, gw_hyd_ss_aa(i)%swgw, gw_hyd_ss_aa(i)%satx, gw_hyd_ss_aa(i)%soil, gw_hyd_ss_aa(i)%latl, gw_hyd_ss_aa(i)%ppag, gw_hyd_ss_aa(i)%ppex, gw_hyd_ss_aa(i)%tile, gw_hyd_ss_aa(i)%resv, gw_hyd_ss_aa(i)%wetl, gw_hyd_ss_aa(i)%fpln, gw_hyd_ss_aa(i)%canl, gw_hyd_ss_aa(i)%pond, gw_hyd_ss_aa(i)%phyt, gw_hyd_grid_aa%chng, gw_hyd_grid_aa%rech, gw_hyd_grid_aa%gwet, gw_hyd_grid_aa%gwsw, gw_hyd_grid_aa%swgw, gw_hyd_grid_aa%satx, gw_hyd_grid_aa%soil, gw_hyd_grid_aa%latl, gw_hyd_grid_aa%bndr, gw_hyd_grid_aa%ppag, gw_hyd_grid_aa%ppdf, gw_hyd_grid_aa%ppex, gw_hyd_grid_aa%tile, gw_hyd_grid_aa%resv, gw_hyd_grid_aa%wetl, gw_hyd_grid_aa%canl, gw_hyd_grid_aa%fpln, gw_hyd_grid_aa%pond, gw_hyd_grid_aa%phyt, gw_heat_grid_aa%chng, gw_heat_grid_aa%rech, gw_heat_grid_aa%gwet, gw_heat_grid_aa%gwsw, gw_heat_grid_aa%swgw, gw_heat_grid_aa%satx, gw_heat_grid_aa%soil, gw_heat_grid_aa%latl, gw_heat_grid_aa%disp, gw_heat_grid_aa%bndr, gw_heat_grid_aa%ppag, gw_heat_grid_aa%ppex, gw_heat_grid_aa%tile, gw_heat_grid_aa%resv, gw_heat_grid_aa%wetl, gw_heat_grid_aa%canl, gw_heat_grid_aa%fpln, gw_heat_grid_aa%pond` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(iob)%name` |
| [sym:sd_channel_module] | `No candidate outside references were resolved to `sd_channel_module` in the context packet.` | `None were resolved from `sd_channel_module` in the visible source.` |
| [sym:time_module] | `time` | `time%yrc, time%yrc_end, time%day, time%day_end, time%nbyr, time%mo, time%day_mo` |
| [sym:basin_module] | `bsn` | `bsn%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_hyd_grid_aa%chng` | Executed only on the last day of the final simulation year, when `gwflag_aa == 1` and the cell is active (`gw_state(i)%stat == 1`) for per-cell output. | `gw_hyd_grid_aa%chng` is updated to include the net storage change over the full run, using `vaft_grid - vbef_grid`, so the basin groundwater summary reports total average-annual storage change rather than a per-year sum. |
| `gw_hyd_grid_aa%rech` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%rech` is divided by `nbyr_r` so the accumulated recharge total is converted to an average annual basin flux for reporting. |
| `gw_hyd_grid_aa%gwet` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%gwet` is divided by `nbyr_r` so the accumulated groundwater evapotranspiration becomes an average annual basin flux. |
| `gw_hyd_grid_aa%gwsw` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%gwsw` is divided by `nbyr_r` so groundwater discharge to channels is reported as an average annual rate. |
| `gw_hyd_grid_aa%swgw` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%swgw` is divided by `nbyr_r` so channel seepage to groundwater is reported as an average annual rate. |
| `gw_hyd_grid_aa%satx` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%satx` is divided by `nbyr_r` so saturation-excess flow is reported as an average annual basin flux. |
| `gw_hyd_grid_aa%soil` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%soil` is divided by `nbyr_r` so groundwater exchange with the soil profile is reported as an average annual rate. |
| `gw_hyd_grid_aa%latl` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%latl` is divided by `nbyr_r` so intercell lateral groundwater flow is reported as an average annual rate. |
| `gw_hyd_grid_aa%bndr` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%bndr` is divided by `nbyr_r` so boundary exchange is reported as an average annual basin flux. |
| `gw_hyd_grid_aa%ppag` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%ppag` is divided by `nbyr_r` so allocation-driven pumping is reported as an average annual rate. |
| `gw_hyd_grid_aa%ppdf` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%ppdf` is divided by `nbyr_r` so unmet pumping demand is reported as an average annual rate. |
| `gw_hyd_grid_aa%ppex` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%ppex` is divided by `nbyr_r` so external pumping is reported as an average annual rate. |
| `gw_hyd_grid_aa%tile` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%tile` is divided by `nbyr_r` so tile-drain exchange is reported as an average annual rate. |
| `gw_hyd_grid_aa%resv` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%resv` is divided by `nbyr_r` so reservoir exchange is reported as an average annual rate. |
| `gw_hyd_grid_aa%wetl` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%wetl` is divided by `nbyr_r` so wetland exchange is reported as an average annual rate. |
| `gw_hyd_grid_aa%canl` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%canl` is divided by `nbyr_r` so canal exchange is reported as an average annual rate. |
| `gw_hyd_grid_aa%fpln` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%fpln` is divided by `nbyr_r` so floodplain exchange is reported as an average annual rate. |
| `gw_hyd_grid_aa%pond` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%pond` is divided by `nbyr_r` so pond seepage is reported as an average annual rate. |
| `gw_hyd_grid_aa%phyt` | Executed on the last day of the simulation before writing the basin groundwater balance. | `gw_hyd_grid_aa%phyt` is divided by `nbyr_r` so phreatophyte transpiration is reported as an average annual rate. |
| `gw_heat_grid_aa%chng` | Executed on the last day of the simulation before writing the basin heat balance. | `gw_heat_grid_aa%chng` is updated with the net heat storage change over the full run, using `heat_haft_grid - heat_hbef_grid`, before average-annual heat reporting. |
| `gw_heat_grid_aa%rech` | Executed on the last day of the simulation before writing the basin heat balance. | `gw_heat_grid_aa%rech` is divided by `nbyr_r` so accumulated heat-related recharge is reported as an average annual rate. |
| `gw_heat_grid_aa%gwet` | Executed on the last day of the simulation before writing the basin heat balance. | `gw_heat_grid_aa%gwet` is divided by `nbyr_r` so groundwater evapotranspiration heat exchange is reported as an average annual rate. |
| `gw_heat_grid_aa%gwsw` | Executed on the last day of the simulation before writing the basin heat balance. | `gw_heat_grid_aa%gwsw` is divided by `nbyr_r` so groundwater discharge heat exchange to channels is reported as an average annual rate. |
| `gw_heat_grid_aa%swgw` | Executed on the last day of the simulation before writing the basin heat balance. | `gw_heat_grid_aa%swgw` is divided by `nbyr_r` so channel seepage heat exchange to groundwater is reported as an average annual rate. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows one behavior-changing commit and several formatting/guard refactors. The AA routine was introduced in the 2026-03-31 output redesign as the end-of-simulation average-annual reporter, then later commits changed how cell IDs and names are derived, how headers are formatted, and how the routine is guarded by simulation-end checks and the final-day call site.

- 9d9069f introduced `gwflow_output_aa` as a new average-annual end-of-simulation output routine.
- 72aa70a expanded the gwflow output code into long-format reporting and added the end-of-simulation AA output structure that this routine uses.
- 7ff5029 added `use basin_module, only : pco, bsn` to the gwflow output file, which brings in basin metadata used by the AA reports.
- 2a5e8de added a local `gis_id` variable and conditional GIS-ID selection, affecting the AA cell-output branch that this routine now uses.
- 3cc92b5 changed the AA cell record to use `cell_gis_id(i)` and `cell_name(i)` and widened the cell-name field to `a12`, matching the current AA cell write statement.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_output_aa' has no extracted documentation comment.
- algorithm_steps revised: aligned steps with the visible source block and split the final-day output sections into distinct write/normalize stages.
- No candidate outside references were resolved to `sd_channel_module` in the context packet.
