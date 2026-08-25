---
kind: procedure
symbol: gwflow_canal_ext
title: gwflow_canal_ext
status: filled
source_hash: 4eea62783fef62f2
version_label: SWAT+ 62.0.0
locals:
  i: Loop index over canal connections in `gw_canl_out_info`; selects each canal-cell linkage
    to process.
  s: Loop index over groundwater solutes when transferring mass between the cell and the canal.
  cell_id: Groundwater grid cell connected to the current canal link; used to read and update
    the cell state and summaries.
  sol_index: Running index into `canal_out_conc` when building the canal inflow mass vector
    for salts and other constituents.
  ics: Loop index over other constituents (`cs_db%num_cs`) when channel water is entering
    the cell.
  isalt: Loop index over salts (`cs_db%num_salts`) when channel water is entering the cell.
  width: Canal width for the current link, read from `gw_canl_out_info(i)%wdth` and used to
    define seepage area.
  depth: Canal water depth for the current link, read from `gw_canl_out_info(i)%dpth` and
    used to compute canal-bed elevation.
  thick: Canal bed thickness for the current link, read from `gw_canl_out_info(i)%thck` and
    used in the Darcy-style seepage rate.
  length: Length of canal within the cell, read from `gw_canl_out_info(i)%leng` and used with
    width to form seepage area.
  stage: Canal water surface elevation for the current link, read from `gw_canl_out_info(i)%elev`.
  bed_k: Hydraulic conductivity of the canal bed for the current link, read from `gw_canl_out_info(i)%hydc`
    and used in the seepage calculation.
  reduc: Declared in this routine but not used in the extracted source block; likely a leftover
    placeholder from canal-flow logic.
  daycount_real: Declared in this routine but not used in the extracted source block; likely
    intended for day-based scaling or timing logic that is not present here.
  flow_area: Seepage exchange area computed as canal length times width; used to scale the
    flux.
  canal_bed: Derived canal-bed elevation (`stage - depth`), used to decide whether groundwater
    is below the bed or between bed and stage.
  head_diff: Head difference driving seepage in the current branch; used with `bed_K`, thickness,
    and area to compute `Q`.
  q: Net water exchange volume for the current canal-cell link in m3/day; positive means canal
    water enters groundwater, negative means groundwater drains to the canal.
  solmass: Per-solute transferred mass for the current link; populated for groundwater-to-canal
    loss or canal-to-groundwater gain and then accumulated into solute summary arrays.
  heat_flux: Transferred heat for the current link when heat exchange is enabled and flow
    is from groundwater to canal; accumulated into heat summary arrays.
uses:
  gwflow_module: These groundwater state and summary arrays are the main outputs and constraints
    of the routine. `gw_state(cell_id)%stat` decides whether the cell can participate, `gw_state(cell_id)%head`
    controls seepage direction, `gw_state(cell_id)%stor` limits how much groundwater can be
    removed, and the `gw_hyd_ss`/`gw_heat_ss` arrays record the canal-exchange contribution
    for daily, monthly, and yearly groundwater budgets.
  hydrograph_module: '`ch_stor` is the channel-storage data structure imported from the hydrograph
    module, and canal diversion/external canal logic is tied to channel water availability
    elsewhere in the groundwater workflow. Even though this subroutine does not reference
    `ch_stor` in the extracted lines, the import shows the procedure is part of the canal-exchange
    subsystem that shares canal state with channel storage accounting.'
  time_module: '`time%day` gates exchange so the routine only acts when the canal is active
    for the current simulation day. That makes the daily time state essential for turning
    canal seepage on and off according to each link''s start and end days.'
  constituent_mass_module: '`cs_db%num_salts` and `cs_db%num_cs` determine how many salt and
    other constituent masses are appended to the canal inflow mass vector. Without these counts,
    the routine would not know how far to extend the `solmass` loop when water enters the
    groundwater cell from the canal source.'
---

<!-- facts:header -->

Routes seepage between outside-source irrigation canals and connected groundwater cells. It updates groundwater storage plus daily, monthly, and yearly hydro, heat, and solute canal-exchange summaries.

## Bottom Line

`gwflow_canal_ext` walks the list of canal-connected cells that are flagged as active for canal exchange and, when the canal is on for the current day, computes seepage using canal geometry, bed conductivity, and the groundwater head in the target cell. Positive flux represents canal water entering the aquifer; negative flux represents groundwater leaving the cell toward the canal, capped so it cannot remove more water or heat than the cell stores.

The routine then records the exchange in groundwater state and summary arrays. Water flux goes into `gw_state(cell_id)%stor` and the hydrology summaries, heat is accumulated only when heat routing is enabled and flow is outward from the cell, and solute masses are transferred either from groundwater concentrations or from canal inflow concentrations depending on flow direction.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the groundwater simulation step after `gwflow_simulate` has established the current day and canal-link lists. `gwflow_simulate` calls it before the canal diversion bookkeeping that follows, so its results feed the same-day groundwater storage, heat, and solute balances used by later groundwater and water-quality calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether outside-canal exchange is enabled. | The routine exits immediately unless the canal-exchange flag is on, so none of the per-cell seepage accounting runs when the feature is disabled. |
| 2. Loop over every outside-canal connection. | Each connection in `gw_canl_out_info` is visited in turn and mapped to its target groundwater `cell_id`. |
| 3. Process only active groundwater cells during the canal's on-period. | The routine skips inactive cells and skips dates outside the canal's start/end day window, so exchange only occurs for active, water-bearing canal links on the current day. |
| 4. Load canal geometry and bed properties for the current link. | The canal width, depth, bed thickness, length, stage, and bed hydraulic conductivity are copied from the link record into local scalars for the seepage calculation. |
| 5. Compute the seepage area and choose the Darcy-flow branch from head relation. | The code forms a seepage area from length and width, derives the canal-bed elevation, and then computes `Q` based on whether groundwater head lies below the bed, above the canal stage, or between them. |
| 6. Prevent groundwater-to-canal loss from exceeding available storage and update groundwater water budgets. | If the flux is negative, it is capped so the routine cannot remove more water than the cell stores. The resulting `Q` is then added to groundwater storage and to the daily, monthly, and yearly hydrology canal-exchange summaries. |
| 7. Accumulate heat transfer when heat routing is active and flow is leaving groundwater. | With heat exchange enabled, outward flow carries heat out of the cell using groundwater temperature, density, and heat capacity; that heat flux is limited by available heat storage and added to daily and yearly heat summaries. |
| 8. Compute and record solute mass transfer for groundwater loss or canal inflow. | When solute routing is enabled, outward flow removes mass from groundwater using cell concentrations, while inward flow uses canal inflow concentrations for nitrate, phosphorus, salts, and other constituents. The per-solute masses are accumulated into daily and summary canal-exchange arrays. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr` | `gw_state(cell_id)%stat, gw_state(cell_id)%head, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%canl, gw_hyd_ss_yr(cell_id)%canl, gw_hyd_ss_mo(cell_id)%canl, gw_heat_ss(cell_id)%canl, gw_heat_ss_yr(cell_id)%canl` |
| [sym:hydrograph_module] | `ch_stor` |  |
| [sym:time_module] | `time` | `time%day` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts, cs_db%num_cs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_state(cell_id)%stor` | When `gw_canal_flag == 1`, the cell is active, the canal is on for `time%day`, and the computed flux `Q` is applied. | `gw_state(cell_id)%stor` is incremented by `Q`, so available groundwater storage is reduced for outward flow or increased for canal seepage into the aquifer. |
| `gw_hyd_ss(cell_id)%canl` | When canal exchange is active and the cell/day filters pass. | `gw_hyd_ss(cell_id)%canl` records the day's canal water exchange for the cell, preserving the signed water budget contribution. |
| `gw_hyd_ss_yr(cell_id)%canl` | When canal exchange is active and the cell/day filters pass. | `gw_hyd_ss_yr(cell_id)%canl` accumulates the same canal water flux into the yearly hydrology summary for later reporting. |
| `gw_hyd_ss_mo(cell_id)%canl` | When canal exchange is active and the cell/day filters pass. | `gw_hyd_ss_mo(cell_id)%canl` accumulates the same canal water flux into the monthly hydrology summary for later reporting. |
| `gw_heat_ss(cell_id)%canl` | When `gw_heat_flag == 1`, `Q < 0`, and the cell/day filters pass. | `gw_heat_ss(cell_id)%canl` stores the heat carried from groundwater to the canal by outward seepage. |
| `gw_heat_ss_yr(cell_id)%canl` | When `gw_heat_flag == 1`, `Q < 0`, and the cell/day filters pass. | `gw_heat_ss_yr(cell_id)%canl` accumulates the same heat transfer into the yearly heat summary. |
| `gwsol_ss(cell_id)%solute(s)%canl` | When `gw_solute_flag == 1` and the cell/day filters pass. | `gwsol_ss(cell_id)%solute(s)%canl` records per-solute canal exchange mass for the current day, either removed from groundwater or added from canal inflow. |
| `gwsol_ss_sum(cell_id)%solute(s)%canl` | When `gw_solute_flag == 1` and the cell/day filters pass. | `gwsol_ss_sum(cell_id)%solute(s)%canl` accumulates the same solute canal exchange mass into the overall summary total. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%canl` | When `gw_solute_flag == 1` and the cell/day filters pass. | `gwsol_ss_sum_mo(cell_id)%solute(s)%canl` accumulates the same solute canal exchange mass into the monthly summary total. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows two behavior-changing revisions to `gwflow_canal_ext`. Commit `9d9069f` introduced the subroutine as a new outside-boundary canal seepage routine with water-only exchange logic. Commit `0ece228` expanded it to include `hydrograph_module`'s `ch_stor`, added `sol_index`, `ics`, `isalt`, `reduc`, `daycount_real`, and `heat_flux`, and extended the body to update heat and solute canal-exchange summaries in addition to water storage.

- 9d9069f created the routine and implemented canal-to-groundwater or groundwater-to-canal water exchange with storage capping and hydrology summaries.
- 0ece228 broadened the routine to import `ch_stor`, add extra local indices and tracking scalars, and compute/accumulate heat and solute exchange in addition to water flux.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_canal_ext' has no extracted documentation comment.
