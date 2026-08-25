---
kind: procedure
symbol: gwflow_gwet
title: gwflow_gwet
status: filled
source_hash: 09ff022ae7c722ff
version_label: SWAT+ 62.0.0
locals:
  i: Loop counter over grid cells within an LSU or HRU connection.
  j: Loop counter over HRUs listed inside an LSU.
  k: Loop counter over LSUs when LSU-cell linking is active, or over HRUs when HRU-cell linking
    is active.
  s: Declared in the source but not used in the extracted body; it appears to be a leftover
    solute counter placeholder.
  cell_id: Index of the current groundwater grid cell receiving ET demand and state updates.
  hru_id: ID of the current HRU whose remaining ET demand is being summed into an LSU total.
  ob_num: Object index for the HRU in `hydrograph_module%ob`, used to get HRU area for converting
    ET depth to volume.
  hru_gwet_volume: Intermediate groundwater-ET volume contributed by one HRU, computed from
    remaining ET depth and HRU area.
  lsu_gwet_volume: Total remaining groundwater-ET volume summed across all HRUs in one LSU
    before cell-level distribution.
  max_gwet: Maximum ET volume or depth available for the current cell before extinction-depth
    and storage limits are applied.
  et_surface: Ground surface elevation for the current cell, used as the upper bound on ET
    extraction.
  et_bottom: Lower ET limit for the current cell, computed as surface elevation minus extinction
    depth.
  gw_head: Current groundwater head in the cell, used to decide whether ET is zero, full,
    or linearly reduced.
  gwet: Cell-level groundwater ET depth in mm for the HRU-linked branch before conversion
    to volume.
  gwet_volume: Final groundwater ET volume removed from the cell after applying depth, extinction,
    and storage limits.
uses:
  gwflow_module: '`gwflow_module` provides the per-cell groundwater state, the per-cell daily/monthly/yearly
    groundwater and heat summary arrays, and the LSU/HRU-to-cell linkage arrays that determine
    which cells receive ET demand. `gwflow_gwet` reads `gw_state(cell_id)%elev`, `%exdp`,
    `%head`, and `%botm` to bound extraction, updates `%stor` to reduce available groundwater,
    and accumulates negative ET into `gw_hyd_ss`, `gw_hyd_ss_mo`, `gw_hyd_ss_yr`, `gw_heat_ss`,
    and `gw_heat_ss_yr`. It also uses `etremain`, `lsu_num_cells`, `lsu_cells_fract`, `lsu_cells`,
    `hru_num_cells`, `hru_cells_fract`, `hru_cells`, and `lsu_cells_link` to route ET demand
    to the proper grid cells.'
  maximum_data_module: '`maximum_data_module%db_mx%lsu_out` sets how many LSU output regions
    exist, which controls the outer LSU loop when LSU-cell linking is active. Without it,
    the routine would not know how many LSU-to-cell mappings to process.'
  calibration_data_module: '`calibration_data_module%lsu_out(k)%num_tot` and `%num(j)` define
    which HRUs belong to each LSU. The routine uses that membership list to sum HRU ET demand
    into an LSU total before distributing it to linked grid cells.'
  hydrograph_module: '`hydrograph_module%sp_ob1%hru`, `%sp_ob%hru`, and `ob(ob_num)%area_ha`
    supply the HRU indexing range and the HRU area needed to convert remaining ET depth into
    a groundwater-ET volume. That conversion is required in the HRU-linked branch before the
    extracted volume is applied to a cell.'
---

<!-- facts:header -->

Computes groundwater evapotranspiration from each linked cell and subtracts that volume from groundwater storage.

## Bottom Line

`gwflow_gwet` distributes the remaining evapotranspiration demand from HRUs or LSUs down to the groundwater-flow grid, converts that demand to a groundwater removal volume, and limits removal by extinction depth, land surface elevation, and available aquifer storage. It writes the withdrawal into daily groundwater source/sink summaries and reduces cell storage accordingly.

If groundwater heat is enabled, the routine also converts the groundwater ET withdrawal into a heat flux and accumulates it in the daily and yearly heat summaries. The routine matters because it is the groundwater-ET sink step in the groundwater simulation sequence, immediately after recharge and before phreatophyte transpiration.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the groundwater-sink step of `gwflow_simulate`, immediately after `gwflow_rech` and before `gwflow_phreatophyte`. `gwflow_simulate` must already have populated the groundwater cell state, ET remainder arrays, and LSU/HRU connectivity, and the volumes written here feed the groundwater water and heat summaries used later in the timestep and reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Enter the routine with implicit module state and initialize local counters and working values. | The subroutine has no arguments; it relies on imported groundwater, hydrograph, calibration, and maximum-data state. Local counters and temporary volumes are initialized to zero so the routine can safely accumulate ET for the current timestep. |
| 2. Choose the LSU-cell pathway when LSU linkage is enabled. | If `lsu_cells_link == 1`, the routine processes ET demand by LSU rather than by HRU. |
| 3. Sum remaining HRU ET demand into one LSU volume. | For each LSU, the routine loops over member HRUs from `lsu_out(k)` and converts each HRU's remaining ET depth to a volume using HRU area from `ob(ob_num)%area_ha`, then sums those HRU volumes into `lsu_gwet_volume`. |
| 4. Distribute LSU ET demand to each connected grid cell. | For each cell linked to the LSU, the routine scales the LSU ET volume by the cell fraction, finds the cell's surface and extinction-depth elevations, and resets the working groundwater-ET volume to zero before deciding how much can be removed. |
| 5. Compute the available ET withdrawal from groundwater head position. | The routine sets zero ET when head is below the extinction depth, takes the full demand when head is above the surface, and otherwise scales the demand linearly between the extinction depth and the surface when the extinction depth is nonzero. |
| 6. Cap ET by available storage and skip inactive cells. | If the cell head is above the bottom of the aquifer, the routine limits withdrawal to the cell's available storage; otherwise it forces ET to zero so no water is removed from a dry or inactive cell. |
| 7. Record LSU-based groundwater ET and reduce storage. | The routine adds negative ET volume to daily hydrology summaries, yearly hydrology summaries, and monthly hydrology summaries, then subtracts the withdrawn volume from `gw_state(cell_id)%stor`. |
| 8. Optionally convert the water withdrawal to heat flux. | When `gw_heat_flag == 1`, the routine computes a heat flux from groundwater temperature, density, heat capacity, and the groundwater-ET sink, then accumulates it in the yearly heat summary. |
| 9. Choose the HRU-cell pathway when LSU linkage is disabled. | If LSU linkage is off, the routine switches to HRU-based processing, starts from the first HRU object number, and initializes the maximum ET demand for each HRU from `etremain(k)`. |
| 10. Distribute HRU ET demand across the HRU's connected cells. | For each HRU cell, the routine scales ET by the HRU-cell fraction, applies the same extinction-depth and surface-elevation logic using the groundwater head and extinction depth, and converts the resulting ET depth to a groundwater volume using the HRU area from `ob(ob_num)%area_ha`. |
| 11. Enforce storage limits and update groundwater summaries in the HRU pathway. | The routine caps the extracted volume to available storage, writes the negative withdrawal into daily, monthly, and yearly hydrology summaries, and subtracts the withdrawn volume from cell storage. |
| 12. Optionally accumulate heat flux in the HRU pathway, then advance to the next HRU. | If heat transport is active, the routine computes and accumulates the groundwater heat sink for the cell, then increments `ob_num` so the next HRU uses the next object record. |
| 13. Finish after all LSU or HRU linked cells have been processed. | The routine ends after completing whichever linkage branch applies for the current model setup. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `etremain, gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, lsu_num_cells, lsu_cells_fract, lsu_cells, hru_num_cells, hru_cells_fract, hru_cells, lsu_cells_link` | `gw_state(cell_id)%elev, gw_state(cell_id)%exdp, gw_state(cell_id)%head, gw_state(cell_id)%botm, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%gwet, gw_hyd_ss_yr(cell_id)%gwet, gw_hyd_ss_mo(cell_id)%gwet, gw_heat_ss(cell_id)%gwet, gw_heat_ss_yr(cell_id)%gwet` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out` |
| [sym:calibration_data_module] | `lsu_out` | `lsu_out(k)%num_tot, lsu_out(k)%num(j)` |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob` | `sp_ob1%hru, sp_ob%hru, ob(ob_num)%area_ha` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_hyd_ss(cell_id)%gwet` | When `lsu_cells_link == 1` and a cell's head, extinction depth, and storage allow groundwater ET. | This daily groundwater-ET sink is accumulated as a negative volume in the cell's hydrology summary so the model records water leaving the aquifer. |
| `gw_hyd_ss_yr(cell_id)%gwet` | When `lsu_cells_link == 1` and the cell qualifies for groundwater ET extraction. | The yearly hydrology summary receives the same negative groundwater-ET volume so annual reporting can total the sink over the simulation year. |
| `gw_hyd_ss_mo(cell_id)%gwet` | When `lsu_cells_link == 1` and the cell qualifies for groundwater ET extraction. | The monthly hydrology summary receives the same negative groundwater-ET volume so monthly reporting can total the sink over the simulation month. |
| `gw_state(cell_id)%stor` | When groundwater ET is computed for a cell and the cell has head above the bottom of the aquifer. | Available groundwater storage is reduced by the extracted ET volume so the cell cannot be depleted below the remaining volume that the routine allows. |
| `gw_heat_ss(cell_id)%gwet` | When `gw_heat_flag == 1` and a groundwater-ET withdrawal has been computed for the cell. | The daily heat sink is set from groundwater temperature, density, heat capacity, and the groundwater-ET withdrawal so the model tracks heat removed with the water. |
| `gw_heat_ss_yr(cell_id)%gwet` | When `gw_heat_flag == 1` and a groundwater-ET withdrawal has been computed for the cell. | The yearly heat summary accumulates the daily groundwater-ET heat sink so annual heat accounting includes ET-related heat loss. |

## File I/O

<!-- facts:io -->


## Lineage

Five resolved commits changed `gwflow_gwet`. The routine was introduced from bitbucket in 94b6dec, later refactored in 9d9069f to use unified `gw_hyd_ss`/`gw_hyd_ss_yr` summaries instead of `gw_ss`/`gw_ss_sum`, extended in e6ca4de to add monthly water summaries and heat-flux accumulation, cleaned in 2ee1889 by removing the unused `s` local, and reformatted in 39fabde by initializing locals and adjusting indentation.

- 94b6dec introduced the initial groundwater-ET routine with LSU/HRU branching, storage capping, and daily/yearly groundwater sink updates.
- 9d9069f renamed the sink summaries from `gw_ss`/`gw_ss_sum` to `gw_hyd_ss`/`gw_hyd_ss_yr`, changing the state targets the routine updates.
- e6ca4de added `gw_hyd_ss_mo` monthly accumulation and heat-flux bookkeeping through `gw_heat_flag`, `gwheat_state(cell_id)%temp`, `gw_rho`, and `gw_cp`.
- 2ee1889 removed the unused local `s` without changing algorithm behavior.
- 39fabde initialized local working variables to zero and adjusted a continuation-line indent; behavior remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_gwet' has no extracted documentation comment.
