---
kind: procedure
symbol: gwflow_rech
title: gwflow_rech
status: filled
source_hash: 616f39ab0c021c09
version_label: SWAT+ 62.0.0
locals:
  i: Loop index over cells within an LSU or HRU when distributing recharge fractions to individual
    grid cells.
  j: Loop index over HRUs listed inside one LSU in the LSU-to-cell mapping branch.
  k: Loop index over HRUs or LSUs, depending on which mapping branch is active.
  n: Loop index over subbasin or outlet groupings in the national-model branch that is present
    in the lineage history but removed in the current source.
  s: Solute index used to update recharge mass for each tracked solute.
  hru_id: The HRU number pulled from `lsu_out(k)%num(j)` or used directly in the HRU-to-cell
    branch.
  ob_num: Index of the hydrologic object in `ob`; used to get the HRU area for converting
    depth-based recharge to volume and mass.
  cell_id: Grid-cell index receiving recharge after any boundary-cell redirection.
  cell_count: Counts LSU cells that have not already received recharge from an HRU in the
    removed national-model path; not used in the current active branches.
  recharge: Stores the prior recharge value for an HRU before it is overwritten by delayed
    recharge.
  recharge_sol: Stores the prior solute recharge value for one HRU and solute before the delayed
    update.
  hru_recharge: Recharge volume for one HRU after converting depth to cubic meters.
  rech_volume: Accumulated recharge volume for the current LSU or HRU group before cell fractions
    are applied.
  cell_rech_volume: Recharge volume assigned to one grid cell after multiplying by the cell
    fraction.
  rech_solmass: Accumulated solute mass for the current LSU or HRU group before cell fractions
    are applied.
  cell_rech_solmass: Solute mass assigned to one grid cell after multiplying by the cell fraction.
  cell_rech_heat: Heat assigned to one grid cell after multiplying the recharge heat by the
    cell fraction.
  hru_total: Running total of recharge volume from all HRUs in a subbasin in the removed national-model
    branch.
  hru_cell_total: Running total of the recharge volume actually distributed to cells from
    HRUs in the removed national-model branch.
  sub_recharge: Subbasin-level recharge volume accumulator in the removed national-model branch.
  sub_heat: Subbasin-level recharge heat accumulator in the removed heat-enabled logic added
    by lineage.
  sub_solmass: Subbasin-level solute mass accumulator in the removed national-model branch.
  perc_volm: Volume of deep percolation from the current HRU, used to compute recharge heat.
  perc_temp: Temperature of the soil water at the bottom soil layer, used as the temperature
    of the percolating water.
  perc_heat: Heat content of the deep percolation water before delay is applied.
  recharge_heat: Stores the prior delayed recharge heat before the new delayed value is written.
uses:
  gwflow_module: '`gwflow_module` owns the recharge inputs and per-cell summary arrays that
    this routine reads and updates, including the delay factor, per-HRU recharge, optional
    solute recharge, cell-link tables, and the `groundwater_ss` summary fields where recharge
    is accumulated for daily, monthly, and yearly groundwater accounting.'
  hydrograph_module: '`hydrograph_module` supplies the HRU object list and object areas that
    identify which spatial object each HRU belongs to and provide the area needed to convert
    recharge depth into volume and mass.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%lsu_out`, the upper bound for
    looping through the LSU output regions that define the LSU-to-cell mapping branch.'
  calibration_data_module: '`calibration_data_module` provides `lsu_out(k)%num_tot` and `lsu_out(k)%num(j)`,
    which list the HRUs belonging to each LSU so the routine can aggregate HRU recharge before
    distributing it to grid cells.'
  soil_module: '`soil_module` provides the bottom-layer soil temperature used to compute the
    heat content of deep percolation when heat tracking is enabled.'
---

<!-- facts:header -->

Calculates groundwater recharge reaching each aquifer cell from HRU or LSU sources, then updates daily, monthly, and yearly groundwater water, heat, and solute recharge summaries.

## Bottom Line

`gwflow_rech` takes the per-HRU recharge already prepared in `gw_rech`, applies the groundwater delay factor, and rewrites recharge so it reflects the current day’s mix of new deep percolation and lagged recharge. If heat or solute tracking is enabled, it applies the same delay logic to `gw_rechheat` and `gw_rechsol` as well.

It then maps the recharge from HRUs or LSUs onto grid cells. Depending on whether LSU-cell linking is enabled, it distributes volume, heat, and solute mass into the per-cell summary arrays such as `gw_hyd_ss`, `gw_hyd_ss_yr`, `gw_hyd_ss_mo`, `gw_heat_ss`, `gw_heat_ss_yr`, `gwsol_ss`, `gwsol_ss_sum`, and `gwsol_ss_sum_mo`. Those summaries feed the groundwater balance accounting used later in `gwflow_simulate`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `gwflow_simulate` during the groundwater source/sink phase, immediately after the model has prepared per-HRU recharge and the spatial connection tables. Its results are then used by the later groundwater balance calculations because the routine populates the per-cell recharge summaries for water, heat, and solutes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Apply delayed recharge to each HRU. | For every HRU, save the previous recharge value, replace `gw_rech(k)` with a weighted mix of current deep percolation (`gwflow_perc(k)`) and the prior recharge, and zero out very small results. When heat tracking is enabled, compute deep-percolation heat from the bottom soil temperature and rewrite `gw_rechheat(k)` with the same delay logic. When solute tracking is enabled, do the same delayed update for each `gw_rechsol(k,s)` using `gwflow_percsol(k,s)`. |
| 2. Choose the LSU-to-cell mapping branch. | If `lsu_cells_link` is set, the routine uses LSU aggregation and LSU cell fractions; otherwise it maps recharge directly from HRUs to cells. |
| 3. Aggregate HRU recharge within each LSU. | Loop over LSU output regions, sum the recharge volume from each HRU listed in `lsu_out(k)%num`, and, if enabled, accumulate solute mass for each tracked solute. The HRU area from `ob(ob_num)%area_ha` converts depth-based recharge to volume and mass. |
| 4. Distribute LSU recharge to linked grid cells. | For each LSU cell, redirect boundary cells to the nearest active cell, apply the LSU cell fraction, and add recharge volume to `gw_hyd_ss(cell_id)%rech` and `gw_hyd_ss_yr(cell_id)%rech`. If heat tracking is enabled, add fractional recharge heat to `gw_heat_ss(cell_id)%rech` and `gw_heat_ss_yr(cell_id)%rech`. If solute tracking is enabled, add fractional solute mass to `gwsol_ss`, `gwsol_ss_sum`, and `gwsol_ss_sum_mo`. |
| 5. Aggregate and distribute direct HRU-to-cell recharge. | If LSU linking is off, the routine loops directly over HRUs, converts each HRU’s recharge to volume and optional solute mass, and distributes those totals across the HRU’s linked cells using `hru_cells_fract`. Boundary cells are redirected before the recharge is added to the per-cell groundwater water, heat, and solute summary arrays. |
| 6. Finish without further calls. | Return to the caller after all recharge summaries have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gwflow_perc, gw_rech, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, gw_delay, lsu_num_cells, lsu_cells, gw_bound_near, lsu_cells_fract, hru_num_cells, hru_cells, hru_cells_fract, lsu_cells_link` | `gw_hyd_ss(cell_id)%rech, gw_hyd_ss_yr(cell_id)%rech, gw_hyd_ss_mo(cell_id)%rech, gw_heat_ss(cell_id)%rech, gw_heat_ss_yr(cell_id)%rech` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out` |
| [sym:calibration_data_module] | `lsu_out` | `lsu_out(k)%num_tot, lsu_out(k)%num(j)` |
| [sym:soil_module] | `soil` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_rech(k)` | After the initial HRU loop for every `k=1,sp_ob%hru`. | `gw_rech(k)` is replaced with the delayed recharge that combines current deep percolation and the previous recharge signal, so later routines use the updated recharge value rather than the pre-delay input. |
| `gw_rechheat(k)` | When `gw_heat_flag == 1` for each HRU in the initial HRU loop. | `gw_rechheat(k)` is updated to the delayed recharge heat, using heat derived from the current deep percolation and the previous heat value. |
| `gw_rechsol(k,s)` | When `gw_solute_flag == 1` for each HRU and each solute `s`. | `gw_rechsol(k,s)` is rewritten as delayed solute recharge so downstream mass accounting uses the lagged solute flux. |
| `gw_hyd_ss(cell_id)%rech` | When `lsu_cells_link == 1` and an LSU cell receives recharge in the LSU branch. | `gw_hyd_ss(cell_id)%rech` accumulates the LSU recharge volume assigned to that cell for the current timestep. |
| `gw_hyd_ss_yr(cell_id)%rech` | When `lsu_cells_link == 1` and an LSU cell receives recharge in the LSU branch. | `gw_hyd_ss_yr(cell_id)%rech` accumulates the same LSU recharge volume into the yearly groundwater-water summary. |
| `gw_hyd_ss_mo(cell_id)%rech` | When `lsu_cells_link == 1` and an LSU cell receives recharge in the LSU branch. | `gw_hyd_ss_mo(cell_id)%rech` accumulates the same LSU recharge volume into the monthly groundwater-water summary. |
| `gw_heat_ss(cell_id)%rech` | When `gw_heat_flag == 1` and the LSU branch assigns recharge to a cell. | `gw_heat_ss(cell_id)%rech` accumulates the cell’s share of recharge heat for daily heat accounting. |
| `gw_heat_ss_yr(cell_id)%rech` | When `gw_heat_flag == 1` and the LSU branch assigns recharge to a cell. | `gw_heat_ss_yr(cell_id)%rech` accumulates the cell’s share of recharge heat for yearly heat accounting. |
| `gwsol_ss(cell_id)%solute(s)%rech` | When `gw_solute_flag == 1` and the LSU branch assigns recharge to a cell. | `gwsol_ss(cell_id)%solute(s)%rech` accumulates the cell’s share of solute mass in recharge for the current timestep. |
| `gwsol_ss_sum(cell_id)%solute(s)%rech` | When `gw_solute_flag == 1` and the LSU branch assigns recharge to a cell. | `gwsol_ss_sum(cell_id)%solute(s)%rech` accumulates the same solute recharge mass into the cell-level summary total. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%rech` | When `gw_solute_flag == 1` and the LSU branch assigns recharge to a cell. | `gwsol_ss_sum_mo(cell_id)%solute(s)%rech` accumulates the same solute recharge mass into the monthly summary total. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:4.2.2 | Recharge delay to shallow aquifer | $w_{rchrg,i}=(1-exp\lfloor-1/\delta_{gw}\rfloor)*w_{seep}+exp\lfloor-1/\delta_{gw}\rfloor*w_{rchrg,i-1}$ | Verified against SWAT+ 62.0.0 (gwflow_rech.f90:48). gw_rech=(1.-gw_delay)*perc+gw_delay*recharge` — delay-weighted recharge (aqu_1d_control:87 has it commented) |
| 3:1.9.1 | Lagged NO3 recharge into shallow aquifer | $NO3_{rchrg,i}=(1-exp\lfloor-1/\delta_{gw}\rfloor)*NO3_{perc}+exp\lfloor-1/\delta_{gw}\rfloor*NO3_{rchrg,i-1}$ | Verified against SWAT+ 62.0.0 (gwflow_rech.f90:60). gw_rechsol=(1.-gw_delay)*percsol+gw_delay*recharge_sol` — nitrate recharge delay |

## Lineage

Four resolved commits changed `gwflow_rech`. The oldest resolved source import added the routine with direct HRU recharge delays and LSU/HRU-to-cell mapping. A later re-merge switched the water summaries from `gw_ss`/`gw_ss_sum` to `gw_hyd_ss`/`gw_hyd_ss_yr` and updated the yearly recharge accumulation. Another re-merge added `soil_module`, heat-tracking variables, and heat recharge calculations. The most recent resolved change removed the unused HUC12 catchment accumulator and the corresponding national-model mapping comment.

- `94b6dec` introduced the initial `gwflow_rech` logic for delaying HRU recharge and distributing recharge to LSU or HRU-connected cells.
- `9d9069f` renamed the water summary targets to `gw_hyd_ss` and `gw_hyd_ss_yr`, changing which groundwater summary arrays receive recharge.
- `e6ca4de` added heat-tracking support, `soil_module` usage, and the `gw_rechheat` / `gw_heat_ss` updates.
- `2a5e8de` removed the unused `huc12_cell_total` variable and the stale national-model recharge mapping comment.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_rech' has no extracted documentation comment.
