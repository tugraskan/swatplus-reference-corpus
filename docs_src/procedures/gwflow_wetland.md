---
kind: procedure
symbol: gwflow_wetland
title: gwflow_wetland
status: filled
source_hash: af284267f2729a67
version_label: SWAT+ 62.0.0
args:
  hru_id: Selects the HRU whose wetland is being processed. The routine uses `hru_id` to find
    the wetland surface-storage object, the connected gwflow cells, the HRU wetland conductivity,
    and the wetland output records to update.
locals:
  ires: Holds the wetland object index for this HRU, taken from `hru(hru_id)%dbs%surf_stor`,
    so the routine can use the correct wetland thickness when computing seepage or inflow.
  s: Loops over gwflow solute species when gw_solute_flag is enabled, so the routine can transfer
    each solute mass separately from groundwater to the wetland.
  icell: Counts through the gwflow cells connected to this HRU during the main exchange loop.
  cell_id: Stores the current gwflow cell index retrieved from `hru_cells(hru_id,icell)` so
    the routine can read and update that cell's groundwater state and summaries.
  wt: Holds the current groundwater head/water-table elevation for the active gwflow cell.
  wet_stage: Stores the current wetland water-surface elevation used to compare against groundwater
    head and determine inflow versus seepage.
  wet_k: Stores the wetland bottom hydraulic conductivity after converting the HRU wetland
    conductivity from mm/hr to m/day.
  wet_area: Stores the portion of wetland area hydraulically connected to the current gwflow
    cell, using the HRU cell fraction and wetland area.
  wet_seep: Accumulates total wetland seepage volume across all connected cells when the wetland
    stage is above groundwater head.
  gw_inflow: Stores groundwater inflow calculated for the current cell when groundwater head
    is above wetland stage.
  wet_inflow: Accumulates groundwater inflow from all connected cells for updating wetland
    water volume and daily inflow bookkeeping.
  gwvol_avail: Holds the maximum groundwater volume available in the current cell based on
    head, bottom elevation, area, and specific yield.
  mass_transfer: Declared for solute transfer bookkeeping, but not used in the extracted source
    beyond initialization.
  gw_mass: Declared for groundwater solute mass bookkeeping, but not used in the extracted
    source beyond initialization.
  wet_inflow_no3: Accumulates nitrate mass transferred from groundwater into the wetland across
    all connected cells.
  wet_inflow_solp: Accumulates soluble phosphorus mass transferred from groundwater into the
    wetland across all connected cells.
  solmass: Temporary per-species mass array used to compute and cap the transferred solute
    mass from each groundwater cell.
  heat_flux: Holds the heat energy removed from groundwater for the current inflow event when
    groundwater heat tracking is active.
  wet_depth: Computes the wetland water depth from wetland volume and wetland area so the
    routine can estimate wetland stage.
uses:
  gwflow_module: '`gwflow_module` provides the groundwater cell state, HRU-to-cell linkage,
    and source-sink summary arrays that this routine reads to compute exchange and writes
    to record wetland-related groundwater losses. It matters because the routine bases inflow/seepage
    on `gw_state(cell_id)%head`, `gw_state(cell_id)%botm`, `gw_state(cell_id)%area`, and `gw_state(cell_id)%spyd`,
    and stores the exchange in the daily, monthly, and yearly wetland entries of `gw_hyd_ss`,
    `gw_hyd_ss_mo`, `gw_hyd_ss_yr`, `gw_heat_ss`, and `gw_heat_ss_yr`.'
  hydrograph_module: '`hydrograph_module` holds the wetland water and water-quality output
    objects updated by this routine. It matters because the routine adds exchanged water and
    nutrients to `wet(hru_id)` and `wet_in_d(hru_id)` and uses `sp_ob1%hru` to locate the
    wetland object''s elevation within the sequential object list.'
  hru_module: '`hru_module` supplies HRU-specific wetland settings that control the exchange
    calculation. It matters because `hru(hru_id)%dbs%surf_stor` identifies the wetland object
    index and `hru(hru_id)%wet_hc` provides the wetland bottom hydraulic conductivity used
    in Darcy''s-law inflow and seepage calculations.'
  water_body_module: '`water_body_module` provides the wetland area and seepage bookkeeping
    record for the HRU. It matters because the routine converts `wet_wat_d(hru_id)%area_ha`
    into wetted area for flux calculations and stores the resulting seepage in `wet_wat_d(hru_id)%seep`.'
---

<!-- facts:header -->

Computes daily groundwater exchange between a wetland HRU and any connected gwflow cells. It also transfers associated heat and solute mass into the wetland bookkeeping arrays.

## Bottom Line

`gwflow_wetland` is the gwflow-enabled wetland exchange routine. For a single HRU, it looks up the wetland surface storage object, loops over all gwflow cells linked to that HRU, and computes either groundwater inflow to the wetland or wetland seepage back to the soil depending on whether the groundwater head is above or below the wetland stage.

When inflow occurs, the routine limits the transfer by available groundwater storage, subtracts the exchange from gwflow source-sink summaries, and adds the water, heat, nitrate, and soluble phosphorus fluxes into the wetland daily output/state arrays. Those results are later used by gwflow balance accounting and wetland water-quality bookkeeping.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `wetland_control` after the wetland water surface area has been set for the HRU and when `bsn_cc%gwflow == 1` selects gwflow-based seepage handling. Its results feed the gwflow groundwater balance through the wetland source-sink summaries and also update wetland water, nutrient, and seepage records used by later wetland and output calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Enter only when gwflow wetland exchange is enabled and identify the wetland object for the HRU. | The routine checks `gw_wet_flag` and, if active, pulls the wetland index from `hru(hru_id)%dbs%surf_stor` so later calculations use the correct wetland thickness and related state. |
| 2. Reset daily exchange accumulators before processing connected gwflow cells. | It clears the running totals for seepage, groundwater inflow, and nutrient inflow so the day's wetland exchange is rebuilt from scratch. |
| 3. Skip the rest of the routine when the HRU has no gwflow cell linkage. | The routine only proceeds when `hru_num_cells(hru_id)` is positive, because the exchange calculation requires at least one connected groundwater cell. |
| 4. Loop over each gwflow cell connected to the HRU and fetch the cell and wetland geometry needed for exchange. | For every connected cell, the routine gets the cell id, groundwater head, wetland depth and stage, wetland hydraulic conductivity, and the wetland area associated with that cell. |
| 5. Compute groundwater inflow when groundwater head is above wetland stage, and cap it by available groundwater storage. | If `wt > wet_stage`, Darcy-based inflow is computed from wetland area, conductivity, and head difference, then limited by the groundwater volume available in the cell above bedrock. |
| 6. Record groundwater-to-wetland water loss in the groundwater source-sink summaries and wetland inflow total. | The inflow is written as a negative wetland exchange in `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_mo`, and added to the wetland inflow accumulator for later wetland bookkeeping. |
| 7. Remove heat from groundwater when heat exchange is active. | When `gw_heat_flag == 1`, the routine estimates heat energy carried by the groundwater inflow, caps it by the cell's stored heat, and subtracts it from daily and yearly groundwater heat summaries. |
| 8. Transfer solute mass from groundwater to the wetland when solute exchange is active. | When `gw_solute_flag == 1`, the routine computes species mass for each groundwater solute, limits it by available cell mass, records it in groundwater solute summaries, and adds nitrate and soluble phosphorus to the wetland output totals. |
| 9. Compute wetland seepage when groundwater is below the wetland stage. | If `wt <= wet_stage`, the routine instead computes seepage from the wetland into soil layers using the same wetland area and conductivity, with wetland thickness or a fallback depth of 0.10 m. |
| 10. After all linked cells are processed, update wetland water and quality outputs. | The routine adds total groundwater inflow to `wet(hru_id)%flo` and `wet_in_d(hru_id)%flo`, stores seepage in `wet_wat_d(hru_id)%seep`, and, when solutes are active, accumulates nitrate and soluble phosphorus in the daily wetland inflow record. |
| 11. Return to the caller after the wetland exchange bookkeeping is complete. | The subroutine ends after all wetland, groundwater, heat, and solute exchange records have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, hru_num_cells, hru_cells, hru_cells_fract` | `gw_state(cell_id)%head, gw_state(cell_id)%botm, gw_state(cell_id)%area, gw_state(cell_id)%spyd, gw_hyd_ss(cell_id)%wetl, gw_hyd_ss_yr(cell_id)%wetl, gw_hyd_ss_mo(cell_id)%wetl, gw_heat_ss(cell_id)%wetl, gw_heat_ss_yr(cell_id)%wetl` |
| [sym:hydrograph_module] | `wet, sp_ob1, wet_in_d, ob` | `wet(hru_id)%flo, sp_ob1%hru, wet(hru_id)%no3, wet(hru_id)%solp, wet_in_d(hru_id)%flo, wet_in_d(hru_id)%no3, wet_in_d(hru_id)%solp` |
| [sym:hru_module] | `hru` | `hru(hru_id)%dbs%surf_stor, hru(hru_id)%wet_hc` |
| [sym:water_body_module] | `wet_wat_d` | `wet_wat_d(hru_id)%area_ha, wet_wat_d(hru_id)%seep` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_hyd_ss(cell_id)%wetl` | When `gw_wet_flag == 1`, `hru_num_cells(hru_id) > 0`, and groundwater head exceeds wetland stage for a connected cell. | This daily groundwater-source-sink accumulator receives a negative wetland exchange for the active cell, representing water leaving the aquifer and entering the wetland. |
| `gw_hyd_ss_yr(cell_id)%wetl` | When `gw_wet_flag == 1`, `hru_num_cells(hru_id) > 0`, and groundwater head exceeds wetland stage for a connected cell. | This yearly groundwater-source-sink accumulator receives the same negative wetland exchange so annual groundwater-water accounting includes wetland losses. |
| `gw_hyd_ss_mo(cell_id)%wetl` | When `gw_wet_flag == 1`, `hru_num_cells(hru_id) > 0`, and groundwater head exceeds wetland stage for a connected cell. | This monthly groundwater-source-sink accumulator receives the same negative wetland exchange so monthly groundwater-water accounting includes wetland losses. |
| `gw_heat_ss(cell_id)%wetl` | When `gw_wet_flag == 1`, `gw_heat_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | This daily groundwater heat summary is reduced by the heat carried with the inflowing groundwater so the aquifer heat budget reflects heat lost to the wetland. |
| `gw_heat_ss_yr(cell_id)%wetl` | When `gw_wet_flag == 1`, `gw_heat_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | This yearly groundwater heat summary is reduced by the same transferred heat for annual heat accounting. |
| `gwsol_ss(cell_id)%solute(s)%wetl` | When `gw_wet_flag == 1`, `gw_solute_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | The per-cell daily wetland exchange for each solute is set to the mass removed from groundwater for that species. |
| `gwsol_ss_sum(cell_id)%solute(s)%wetl` | When `gw_wet_flag == 1`, `gw_solute_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | The cumulative groundwater-to-wetland solute exchange for the cell is increased by the transferred mass for each species. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%wetl` | When `gw_wet_flag == 1`, `gw_solute_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | The monthly cumulative groundwater-to-wetland solute exchange for the cell is increased by the transferred mass for each species. |
| `wet(hru_id)%no3` | When `gw_wet_flag == 1`, `gw_solute_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | Wetland nitrate storage is increased by the nitrate mass transferred from the connected groundwater cell. |
| `wet(hru_id)%solp` | When `gw_wet_flag == 1`, `gw_solute_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | Wetland soluble phosphorus storage is increased by the phosphorus mass transferred from the connected groundwater cell. |
| `wet(hru_id)%flo` | When `gw_wet_flag == 1` and at least one connected cell has groundwater head above wetland stage. | Wetland water volume is increased by the total groundwater inflow collected across all connected cells. |
| `wet_in_d(hru_id)%flo` | When `gw_wet_flag == 1` and at least one connected cell has groundwater head above wetland stage. | The daily wetland inflow record is increased by the total groundwater inflow so wetland water balance and output accounting include the added water. |
| `wet_wat_d(hru_id)%seep` | When `gw_wet_flag == 1` and groundwater head is at or below wetland stage for a connected cell. | Wetland seepage is updated with the computed seepage loss to the soil, and the final wetland seepage record stores the minimum of wetland water volume and total seepage. |
| `wet_in_d(hru_id)%no3` | When `gw_wet_flag == 1`, `gw_solute_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | The daily wetland inflow nitrate record is increased by nitrate mass transferred from groundwater. |
| `wet_in_d(hru_id)%solp` | When `gw_wet_flag == 1`, `gw_solute_flag == 1`, and groundwater head exceeds wetland stage for a connected cell. | The daily wetland inflow soluble phosphorus record is increased by phosphorus mass transferred from groundwater. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved three commits affecting this file. The initial addition appeared in 9d9069f, which created `gwflow_wetland.f90` with water exchange only. Commit 05cc429 then expanded the routine with `gw_mass`, `heat_flux`, and `wet_depth`, added heat-transfer handling, and added solute transfer into groundwater and wetland summary arrays. Commit 2ee1889 resolved to no diff for this file, so it did not change `gwflow_wetland` behavior in the available evidence.

- 9d9069f added the wetland groundwater exchange routine and its core water-balance logic, including per-cell Darcy inflow, seepage fallback, and updates to wetland water volume and groundwater source-sink water summaries.
- 05cc429 extended the routine to track groundwater heat and solute exchange, adding `gw_mass`, `heat_flux`, and `wet_depth`, plus updates to `gw_heat_ss`, `gw_heat_ss_yr`, `gwsol_ss`, `gwsol_ss_sum`, `gwsol_ss_sum_mo`, `wet(hru_id)%no3`, `wet(hru_id)%solp`, `wet_in_d(hru_id)%no3`, and `wet_in_d(hru_id)%solp`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_wetland' has no extracted documentation comment.
