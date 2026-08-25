---
kind: procedure
symbol: gwflow_output_day
title: gwflow_output_day
status: filled
source_hash: e0b8b15c8c22e8fc
version_label: SWAT+ 62.0.0
locals:
  i: Loop index for active groundwater cells and for several output passes over all cells.
  j: Nested loop index used when walking the cell IDs that belong to a groundwater water-balance
    group.
  k: Loop index for groundwater observation wells.
  s: Loop index for solutes when solute transport output is enabled.
  iob: Index into the `ob` array for the HRU object that corresponds to a pumping record being
    written.
  cell_id: Temporary groundwater cell ID pulled from a group membership table before its fluxes
    and head depth are accumulated.
  gis_id: GIS-style cell identifier written to long-format cell output; assigned from `cell_gis_id(i)`
    for each active cell.
  sum: Accumulator used first for watershed-average depth to water table, then for average
    groundwater temperature, and also for group depth aggregation.
  obs_temp: Observation-well temperature value written to the daily observation file; set
    to a sentinel when heat output is disabled.
  obs_no3: Observation-well solute concentration used for the first solute column in the observation
    file; set to a sentinel when solute output is disabled.
  obs_p: Observation-well solute concentration used for the second solute column in the observation
    file; set to a sentinel when solute output is disabled.
  obs_name: Formatted observation-well label such as `obs_0001` written to the observation
    output record.
  frac_sat: Fraction of active cells that are saturated, computed from `satx_count` and `num_active`
    for the basin balance output.
  depth_wt_avg: Watershed-average depth to groundwater computed from active-cell elevation
    minus head before any output is written.
  depth_wt_avg_grp: Average depth to groundwater for the current groundwater balance group,
    computed from the group members that are active.
  mass_error: Percent mass-balance error for the current water, heat, or solute balance block
    before the balance is written.
  temp_avg: Watershed-average groundwater temperature across active cells; only computed when
    heat output is enabled.
  sol_grid_rech: Grid-total solute mass associated with recharge, accumulated across active
    cells for the current solute.
  sol_grid_gwsw: Grid-total solute mass associated with groundwater-to-surface-water exchange
    for the current solute.
  sol_grid_swgw: Grid-total solute mass associated with surface-water-to-groundwater exchange
    for the current solute.
  sol_grid_satx: Grid-total solute mass associated with saturation-excess flow for the current
    solute.
  sol_grid_advn: Grid-total solute mass associated with advective transport for the current
    solute.
  sol_grid_disp: Grid-total solute mass associated with dispersion for the current solute.
  sol_grid_rcti: Grid-total solute mass associated with internal reaction/removal for the
    current solute.
  sol_grid_rcto: Grid-total solute mass associated with external reaction/removal for the
    current solute.
  sol_grid_minl: Grid-total solute mass associated with mineralization losses for the current
    solute.
  sol_grid_sorb: Grid-total solute mass associated with sorption; negated before mass-error
    calculation to represent leaving groundwater.
  sol_grid_ppag: Grid-total solute mass associated with allocation-driven pumping for the
    current solute.
  sol_grid_ppex: Grid-total solute mass associated with external pumping for the current solute.
  sol_grid_tile: Grid-total solute mass associated with tile drainage for the current solute.
  sol_grid_soil: Grid-total solute mass associated with exchange to the soil profile for the
    current solute.
  sol_grid_resv: Grid-total solute mass associated with reservoir exchange for the current
    solute.
  sol_grid_wetl: Grid-total solute mass associated with wetland exchange for the current solute.
  sol_grid_canl: Grid-total solute mass associated with canal exchange for the current solute.
  sol_grid_fpln: Grid-total solute mass associated with floodplain exchange for the current
    solute.
  sol_grid_pond: Grid-total solute mass associated with recharge pond seepage for the current
    solute.
  count: Counter for active cells used when averaging depth to water table and temperature.
uses:
  gwflow_module: This module holds the simulated groundwater state and daily source/sink flux
    arrays that the routine reads to compute balances and write output. Without `gw_state`,
    `gw_hyd_ss`, and `gw_hyd_grid_mo`, there is nothing to summarize or accumulate.
  hydrograph_module: This module supplies the observation arrays that are populated here and
    written to the daily observation-well output. It matters because the routine records the
    current simulated head, temperature, and solute concentration at each observation location.
  sd_channel_module: This module provides the HRU pumping array and the object indexing used
    to map a pumping total back to the corresponding HRU record. It matters because the routine
    writes daily pumping output only for HRUs with positive pumping.
  time_module: The current simulation date is written into every daily output record so each
    balance and observation row is timestamped correctly.
  basin_module: The basin name labels all water, heat, and solute balance records, and the
    total basin area is required to normalize summed groundwater volumes to depth units for
    the basin-wide daily balance.
---

<!-- facts:header -->

Computes and writes daily groundwater output for observation wells, cell groups, basin/grid water balances, heat balance, solute mass balance, and per-cell / per-HRU daily reports.

## Bottom Line

`gwflow_output_day` is the daily reporting routine for the groundwater flow system. It gathers end-of-day heads, temperatures, solute masses, and source/sink fluxes from module state, then writes the requested observation, balance, cell, and pumping outputs.

It also updates the daily values that feed monthly, yearly, and average-annual groundwater, heat, and solute summaries. In other words, this routine is the daily checkpoint that turns simulated state into reportable files and cumulative balance trackers.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`gwflow_output_day` runs inside the daily groundwater simulation workflow after the solver has updated the per-cell groundwater, heat, and solute states for the day. `gwflow_simulate` calls it immediately after setting end-of-day masses such as `gwsol_state(i)%solute(s)%maft`, and its output feeds the later monthly and yearly summary routines by updating the shared grid accumulation variables and writing the daily report files.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute watershed-average diagnostics | The routine first loops over active groundwater cells to compute the average depth to water table, and—when heat output is enabled—the average groundwater temperature. Both averages are based only on cells with `gw_state(i)%stat == 1`. |
| 2. Cache observation-well state | For each observation well, the routine copies current simulated head into `gw_obs_head(k)`, and conditionally copies temperature and each solute concentration into `gw_obs_temp(k)` and `gw_obs_solute(k,s)`. |
| 3. Write observation-well records | If observation output is enabled, it formats an observation name, fills missing heat/solute values with sentinels, and writes one daily record per observation well containing date, cell ID, head, depth to water, temperature, and selected solute concentrations. |
| 4. Store end-of-day cell state | The routine updates end-of-day groundwater volume in `gw_state(i)%vaft`, groundwater heat storage in `gwheat_state(i)%haft`, and solute mass in `gwsol_state(i)%solute(s)%maft` for active cells. |
| 5. Build group balances when requested | When groundwater group output is enabled, the routine accumulates all active member-cell fluxes and volumes into the group totals, computes group depth-to-water and mass error, and writes one daily balance record per group. |
| 6. Build basin grid water balance | The routine sums active-cell groundwater fluxes across the whole grid, computes mass error, converts volumes to basin-depth units using `bsn%area_tot_ha`, computes the saturated-cell fraction, and writes the basin-wide daily groundwater balance if enabled. |
| 7. Accumulate basin water totals for later periods | After the daily water balance is computed, the routine adds the daily grid totals into the monthly, yearly, and average-annual groundwater balance accumulators stored in `gw_hyd_grid_mo`, `gw_hyd_grid_yr`, and `gw_hyd_grid_aa`. |
| 8. Build heat balance when enabled | If heat output is active, the routine sums active-cell heat fluxes, computes heat mass error, converts the totals to MJ, writes the daily heat-balance record, and accumulates the results into the yearly and average-annual heat balance stores. |
| 9. Build solute balances when enabled | For each simulated solute, the routine sums active-cell masses and fluxes, converts them to kilograms, computes mass error when end-of-day mass exists, writes the daily solute balance record, and accumulates the totals into monthly, yearly, and total solute summary arrays. |
| 10. Write per-cell daily output | When daily cell output is enabled, the routine writes one long-format record for each active groundwater cell with cell identity, cell name, head, depth to water, and the daily groundwater source/sink terms. |
| 11. Write per-HRU pumping output | If pumping output is enabled, the routine loops over HRUs, selects those with positive pumping, maps each HRU to its object index, and writes the daily pumping amount with GIS and name fields. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_grid_mo` | `gw_state(i)%elev, gw_state(i)%head, gw_state(gw_obs_cells(k))%elev, gw_state(i)%vaft, gw_state(i)%botm, gw_state(i)%area, gw_state(i)%spyd, gw_state(cell_id)%vbef, gw_state(cell_id)%vaft, gw_hyd_ss(cell_id)%rech, gw_hyd_ss(cell_id)%gwet, gw_hyd_ss(cell_id)%gwsw, gw_hyd_ss(cell_id)%swgw, gw_hyd_ss(cell_id)%satx, gw_hyd_ss(cell_id)%soil, gw_hyd_ss(cell_id)%latl, gw_hyd_ss(cell_id)%bndr, gw_hyd_ss(cell_id)%ppag, gw_hyd_ss(cell_id)%ppdf, gw_hyd_ss(cell_id)%ppex, gw_hyd_ss(cell_id)%tile, gw_hyd_ss(cell_id)%resv, gw_hyd_ss(cell_id)%wetl, gw_hyd_ss(cell_id)%canl, gw_hyd_ss(cell_id)%fpln, gw_hyd_ss(cell_id)%pond, gw_hyd_ss(cell_id)%phyt, gw_state(cell_id)%elev, gw_state(cell_id)%head, gw_state(i)%vbef, gw_hyd_ss(i)%rech, gw_hyd_ss(i)%gwet, gw_hyd_ss(i)%gwsw, gw_hyd_ss(i)%swgw, gw_hyd_ss(i)%satx, gw_hyd_ss(i)%soil, gw_hyd_ss(i)%latl, gw_hyd_ss(i)%bndr, gw_hyd_ss(i)%ppag, gw_hyd_ss(i)%ppdf, gw_hyd_ss(i)%ppex, gw_hyd_ss(i)%tile, gw_hyd_ss(i)%resv, gw_hyd_ss(i)%wetl, gw_hyd_ss(i)%canl, gw_hyd_ss(i)%fpln, gw_hyd_ss(i)%pond, gw_hyd_ss(i)%phyt, gw_hyd_grid_mo%chng, gw_hyd_grid_mo%rech, gw_hyd_grid_mo%gwet, gw_hyd_grid_mo%gwsw, gw_hyd_grid_mo%swgw, gw_hyd_grid_mo%satx, gw_hyd_grid_mo%soil, gw_hyd_grid_mo%latl, gw_hyd_grid_mo%bndr, gw_hyd_grid_mo%ppag, gw_hyd_grid_mo%ppdf, gw_hyd_grid_mo%ppex, gw_hyd_grid_mo%tile, gw_hyd_grid_mo%resv, gw_hyd_grid_mo%wetl, gw_hyd_grid_mo%canl, gw_hyd_grid_mo%fpln, gw_hyd_grid_mo%pond` |
| [sym:hydrograph_module] | `gw_obs_head, gw_obs_temp, gw_obs_solute` | `gw_obs_head(k), gw_obs_temp(k), gw_obs_solute(k,s)` |
| [sym:sd_channel_module] | `hru_pump, sp_ob, sp_ob1, ob` | `hru_pump(i), sp_ob%hru, sp_ob1%hru, ob(iob)%gis_id, ob(iob)%name` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc` |
| [sym:basin_module] | `bsn` | `bsn%name, bsn%area_tot_ha` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_obs_head(k)` | For each observation well during the daily observation pass. | Stores the current simulated groundwater head at the observation cell so it can be written to the observation file and reused by the daily output record. |
| `gw_obs_temp(k)` | Only when `gw_heat_flag == 1`, for each observation well. | Stores the current groundwater temperature at the observation cell so the observation output can report temperature alongside head. |
| `gw_obs_solute(k,s)` | Only when `gw_solute_flag == 1`, for each observation well and each solute index `s`. | Stores the current simulated solute concentration at the observation cell so the observation output can report solute concentrations. |
| `gw_state(i)%vaft` | For every active groundwater cell after the daily state update. | Recomputes the end-of-day groundwater volume from the current head, aquifer bottom, cell area, and specific yield. |
| `gwheat_state(i)%haft` | Only when `gw_heat_flag == 1`, for every active groundwater cell after the daily state update. | Copies the end-of-day heat storage from the current heat storage state so heat balances can compare beginning and ending storage. |
| `gwsol_state(i)%solute(s)%maft` | Only when `gw_solute_flag == 1`, for every active groundwater cell and solute. | Copies the end-of-day solute mass from the current solute mass state so solute balances can compare beginning and ending storage. |
| `vbef_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating beginning-of-day groundwater volumes for the group. |
| `vaft_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating end-of-day groundwater volumes for the group. |
| `rech_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group recharge fluxes. |
| `gwet_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group groundwater evapotranspiration fluxes. |
| `gwsw_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group groundwater-to-surface-water discharge. |
| `swgw_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group surface-water-to-groundwater exchange. |
| `satx_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group saturation-excess flow. |
| `soil_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group groundwater-to-soil exchange. |
| `latl_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group lateral flow. |
| `bndr_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group boundary exchange. |
| `ppag_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group allocation-driven pumping. |
| `ppdf_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group pumping deficit. |
| `ppex_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group external pumping. |
| `tile_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group tile drainage. |
| `resv_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group reservoir exchange. |
| `wetl_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group wetland exchange. |
| `canl_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group canal exchange. |
| `fpln_grp` | When group output is enabled and the routine starts a new groundwater water-balance group. | Reset to zero before accumulating group floodplain exchange. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `gwflow_output_day` in the lineage evidence. The 2026-03-31 commit 9d9069f introduced the subroutine as a stub. The 2026-04-02 commit 7ff5029 replaced the stub with the full daily groundwater output implementation, adding module use associations, daily balance calculations, observation output, heat and solute reporting, and daily cell / pumping writes. The 2026-06-02 commit 3cc92b5 then refactored the daily cell output to use `cell_gis_id(i)` and `cell_name(i)` and widened the cell-name format from `a4` plus numeric suffix to `a12`. The 2026-04-16 commit 2a5e8de added `gis_id` to the local declarations and made the daily cell output choose a structured-grid GIS ID or `i` before writing, but this was later superseded by the `cell_gis_id(i)` refactor.

- Added the full daily groundwater output workflow, including observation, group, basin, heat, solute, and per-cell/per-HRU reporting, replacing the initial stub.
- Changed daily cell output identity handling from ad hoc grid math to `cell_gis_id(i)` / `cell_name(i)` and updated the cell output format to accommodate the longer cell name field.
- Inserted a local `gis_id` variable and conditional GIS-ID selection for the daily cell output before later refactoring to `cell_gis_id(i)`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_output_day' has no extracted documentation comment.
- algorithm_steps revised: expanded the daily workflow into 11 steps to match the source blocks and keep each step aligned with visible line ranges.
- `hydrograph_module` and `sd_channel_module` are used indirectly by named arrays/objects in the source packet, but no standalone candidate refs were resolved to those modules; outside-state entries for them are therefore intentionally sparse.
- `obs_no3` and `obs_p` are written as the first two solute concentrations when solute output is enabled; the source packet does not label them by chemistry name, so that mapping is based only on their position in the write list and should be treated cautiously.
