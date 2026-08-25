---
kind: procedure
symbol: gwflow_soil
title: gwflow_soil
status: filled
source_hash: ab4f8654b41ae914
version_label: SWAT+ 62.0.0
args:
  hru_id: '`hru_id` selects the HRU whose connected grid cells, soil profile, and output accumulators
    are processed by this call.'
locals:
  k: Loop index over the groundwater grid cells connected to the current HRU.
  s: Loop index over solute species when solute transfer is enabled.
  jj: Loop index over soil layers in the current HRU profile.
  cell_id: The specific groundwater cell linked to the current HRU connection being processed.
  hru_q: The groundwater volume, in m3, transferred from one cell into the HRU soil profile
    for the current cell.
  hru_soilz: The total depth of the HRU soil profile, used as the comparison depth for deciding
    whether the water table is inside the soil.
  vadose_z: The current thickness of the cell vadose zone, computed from groundwater elevation
    minus head.
  poly_area: The portion of the cell area that lies within this HRU, used to scale the transfer
    volume.
  solmass: Per-solute mass available for transfer from the groundwater cell into the HRU soil
    profile.
  water_depth: Per-layer saturated thickness used to distribute the transferred groundwater
    through the HRU soil layers.
  water_depth_tot: Total saturated thickness across all eligible HRU soil layers, used as
    the denominator for layer fractions.
  sol_thick: Thickness of the current soil layer, converted to meters for layer-depth comparisons.
  layer_fraction: Fraction of the total saturated soil depth assigned to the current layer,
    used to apportion water, solute, and heat.
  layer_transfer: The amount of water, solute, or heat assigned to the current HRU soil layer
    after proportional splitting.
  hru_area_m2: The HRU area in square meters, used to convert transferred volume into a soil-water
    depth increment.
  heat_flux: The groundwater heat content transferred with the water volume, capped by available
    groundwater heat storage.
  soil_volm: The volume of water stored in the current soil layer, used to convert added heat
    into a new temperature.
  soil_heat: The current heat content of the layer’s soil water before and after the groundwater
    heat addition.
uses:
  gwflow_module: This module provides the groundwater cell state, the HRU-to-cell connectivity,
    and the groundwater summary arrays that `gwflow_soil` reads and updates. Without `gw_state`,
    `hru_cells`, `cells_fract`, and the summary arrays, the routine could not determine which
    cells contribute to an HRU or record the water and heat removed from groundwater.
  soil_module: This module supplies the HRU soil profile geometry and current storage/temperature
    state that receive the transferred groundwater. The routine needs layer depths to decide
    which layers are saturated, then updates `st` and `tmp` in those same soil layers.
  hydrograph_module: The HRU object provides `area_ha`, which is converted to square meters
    to distribute the transferred water and solute on an area basis. That area is also used
    to express solute addition to soil in kg/ha.
  hru_module: This module holds `gwsoilq`, the HRU-level groundwater-to-soil flux accumulator
    written by this routine for later output and accounting.
  time_module: The time module is imported by this routine’s source, and its presence matters
    because groundwater/HRU summaries are part of the time-stepped model state even though
    no direct use of `time` is visible in the extracted lines.
---

<!-- facts:header -->

Moves groundwater stored in connected grid cells into an HRU’s soil profile when the water table rises into the soil. It also updates groundwater water, heat, and solute accounting for that transfer.

## Bottom Line

When groundwater-to-soil exchange is enabled, `gwflow_soil` walks the grid cells connected to one HRU, checks whether each active cell’s water table lies inside the HRU soil profile, and if so computes a transfer volume from that cell into the HRU soil layers. It then records the loss from the groundwater side and adds the water to the soil-layer storage in the HRU.

The routine also carries heat and solute effects with the same transfer logic: it debits groundwater heat summaries, adds solute mass to HRU soil pools, and adjusts soil-layer temperature from the added groundwater heat. The results feed later groundwater balance and HRU output accounting, including `gwflow_simulate` and `gwsoilq`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU water-routing in `swr_percmain` when basin groundwater flow is enabled. `swr_percmain` prepares the current HRU index and calls `gwflow_soil` before the first-soil-layer infiltration logic, and the results are then used in groundwater balance calculations and HRU soil-state updates that affect later simulation outputs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute HRU-scale geometry and check the feature flag | Convert the HRU area from hectares to square meters, derive the HRU soil profile thickness from the deepest soil layer, and skip all work unless `gw_soil_flag == 1`. |
| 2. Loop over groundwater cells linked to the HRU | Traverse each grid cell connected to the HRU by using `hru_num_cells(hru_id)` and `hru_cells(hru_id,k)` to identify the current `cell_id`. |
| 3. Process only active cells | For each connected cell, require `gw_state(cell_id)%stat == 1`, then compute the vadose-zone thickness as groundwater surface elevation minus current head. |
| 4. Transfer groundwater only when the water table is within the soil profile | If `vadose_z < hru_soilz`, compute the cell area inside the HRU, then calculate groundwater volume `hru_Q` from the excess saturated thickness, cell area, and specific yield. |
| 5. Debit groundwater water summaries | Subtract the transferred water from the daily, yearly, and monthly groundwater hydrology summary arrays using a negative sign to represent water leaving the aquifer. |
| 6. Transfer groundwater heat when heat accounting is enabled | If `gw_heat_flag == 1`, compute transferred heat from groundwater temperature, density, heat capacity, and `hru_Q`, cap it by available groundwater heat storage, and subtract it from daily and yearly heat summaries. |
| 7. Determine which HRU soil layers receive the groundwater | Initialize the per-layer depth arrays, then scan each soil layer to compute the saturated thickness in that layer and the total saturated depth across all eligible layers. |
| 8. Distribute water, solute, and heat through the soil layers | For each soil layer, compute its fraction of the saturated profile, convert the assigned water volume to a soil-water depth increment, add that water to `soil(... )%st`, accumulate `gwsoilq`, optionally add solute mass to `hru_soil`, and optionally raise soil temperature using the added heat. |
| 9. Finish the cell and HRU loops | After all eligible layers and cells have been processed, exit the conditional blocks and return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, hru_num_cells, hru_cells, cells_fract` | `gw_state(cell_id)%elev, gw_state(cell_id)%head, gw_state(cell_id)%area, gw_state(cell_id)%spyd, gw_hyd_ss(cell_id)%soil, gw_hyd_ss_yr(cell_id)%soil, gw_hyd_ss_mo(cell_id)%soil, gw_heat_ss(cell_id)%soil, gw_heat_ss_yr(cell_id)%soil` |
| [sym:soil_module] | `soil` | `soil(hru_id)%nly, soil(hru_id)%phys(jj)%thick, soil(hru_id)%phys(jj)%st, soil(hru_id)%phys(jj)%tmp` |
| [sym:hydrograph_module] | `ob` | `ob(hru_id)%area_ha` |
| [sym:hru_module] | `gwsoilq` |  |
| [sym:time_module] | `time` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_hyd_ss(cell_id)%soil` | When `gw_soil_flag == 1`, `gw_state(cell_id)%stat == 1`, and `vadose_z < hru_soilz`. | `gw_hyd_ss(cell_id)%soil` is decremented by the transferred groundwater volume so the cell’s daily water summary records water leaving the aquifer and entering the soil profile. |
| `gw_hyd_ss_yr(cell_id)%soil` | When `gw_soil_flag == 1`, `gw_state(cell_id)%stat == 1`, `vadose_z < hru_soilz`, and the cell is processed in the current HRU loop. | `gw_hyd_ss_yr(cell_id)%soil` accumulates the same negative soil-transfer volume at yearly scale for groundwater water-balance reporting. |
| `gw_hyd_ss_mo(cell_id)%soil` | When `gw_soil_flag == 1`, `gw_state(cell_id)%stat == 1`, `vadose_z < hru_soilz`, and the cell is processed in the current HRU loop. | `gw_hyd_ss_mo(cell_id)%soil` accumulates the same negative soil-transfer volume at monthly scale for groundwater water-balance reporting. |
| `gw_heat_ss(cell_id)%soil` | When `gw_heat_flag == 1` under the same water-transfer conditions. | `gw_heat_ss(cell_id)%soil` is reduced by the heat removed from groundwater and moved into the HRU soil profile. |
| `gw_heat_ss_yr(cell_id)%soil` | When `gw_heat_flag == 1` under the same water-transfer conditions. | `gw_heat_ss_yr(cell_id)%soil` accumulates the yearly negative heat transfer so heat balance summaries reflect groundwater-to-soil exchange. |
| `soil(hru_id)%phys(jj)%st` | For each HRU soil layer when water is transferred from an active connected cell with `vadose_z < hru_soilz`. | `soil(hru_id)%phys(jj)%st` increases by the layer’s share of transferred groundwater, expressed as an added soil-water depth in millimeters. |
| `gwsoilq(hru_id)` | For each HRU soil layer when water transfer occurs and the model is updating HRU output accounting. | `gwsoilq(hru_id)` accumulates the layer-transfer depth so the HRU has a total groundwater-to-soil flux for output and later balance checks. |
| `hru_soil(hru_id,jj,s)` | When `gw_solute_flag == 1` and solute transfer is enabled for a layer receiving groundwater. | `hru_soil(hru_id,jj,s)` gains the layer’s share of the transferred solute mass, converted to kg/ha for soil nutrient or salt pools. |
| `soil(hru_id)%phys(jj)%tmp` | When `gw_heat_flag == 1` and groundwater heat is being moved into the soil layer. | `soil(hru_id)%phys(jj)%tmp` is recalculated from the layer’s updated heat content so the soil temperature reflects the added groundwater heat. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits changed `gwflow_soil`: the 2024 initialization commit gave the local loop counters and transfer variables explicit zero initial values; the 2024 refactor/merge added `time_module` and new heat-transfer variables and logic; the 2024 tab-fix commit only adjusted whitespace on `vadose_z`; and the 2026 bug fix changed solute handling so each cell’s solute transfer is accumulated instead of overwritten, and removed the trailing newline issue.

- 39fabde initialized the procedure’s local counters and transfer variables with explicit zero values, changing startup state but not the transfer formulas.
- e6ca4de added `time_module`, `heat_flux`, `soil_volm`, and `soil_heat`, and introduced the groundwater-heat transfer path alongside the existing water-transfer logic.
- 5563825 changed solute accumulation from assignment to additive accumulation in `gwsol_ss(cell_id)%solute(s)%soil`, fixing repeated-cell transfers so they sum correctly.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_soil' has no extracted documentation comment.
