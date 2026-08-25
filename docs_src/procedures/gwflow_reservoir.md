---
kind: procedure
symbol: gwflow_reservoir
title: gwflow_reservoir
status: filled
source_hash: 52204635e4942730
version_label: SWAT+ 62.0.0
args:
  res_id: '`res_id` selects which reservoir object, reservoir-water state, and connected-reservoir-cell
    list this call operates on.'
locals:
  k: Loop counter over the reservoir-connected grid cells listed in `gw_resv_info(res_id)%cells`.
  jj: Loop counter over the grid cells connected to one reservoir cell through `cell_con(res_cell_id)%cell_id`.
  s: Loop counter over the solute slots being transferred between groundwater and the reservoir.
  res_cell_id: Holds the ID of the reservoir-side grid cell currently being processed.
  cell_id: Holds the ID of the groundwater cell paired with the current reservoir cell connection.
  isalt: Loop counter over salt ions when salt transport is enabled.
  ics: Loop counter over non-salt constituents when constituent transport is enabled.
  sol_index: Tracks the position in the combined solute array while mapping NO3, soluble P,
    salts, and other constituents.
  area_res_cell: Surface area of the current reservoir-connected cell, used to size the connection.
  area_cell: Surface area of the paired groundwater cell, used with the reservoir-cell area
    to estimate connection length.
  min_area: Smaller of the two cell areas, used to approximate the exchange connection width.
  head_diff: Hydraulic head difference between the reservoir water level and the groundwater
    head in the paired cell.
  q: Calculated water exchange volume for the current reservoir-cell pair before limits are
    applied.
  conn_length: Approximate connection length between cells, computed as the square root of
    the smaller cell area.
  res_volume: Reservoir water volume at the start of the exchange calculation, used to limit
    outflow and compute concentrations.
  resv_csol: Reservoir-water solute concentrations converted to g/m3 for each transported
    solute slot.
  solmass: Mass exchanged for each solute slot during the current cell-pair calculation.
  heat_flux: Heat transferred with groundwater inflow to the reservoir when heat tracking
    is active.
  seep_total: Running total of all seepage/exchange volumes for the reservoir during this
    call.
uses:
  gwflow_module: '`gwflow_module` provides the groundwater cell states, reservoir-connection
    metadata, and daily/monthly/yearly summary arrays that this routine reads and updates.
    The cell heads, areas, storages, and connection lists determine the exchange calculation,
    while `gw_hyd_ss`, `gw_hyd_ss_yr`, `gw_hyd_ss_mo`, `gw_heat_ss`, and `gw_heat_ss_yr` store
    the resulting water and heat fluxes for later gwflow accounting.'
  hydrograph_module: '`hydrograph_module` holds the reservoir hydrologic output record `res`,
    which carries the reservoir water volume and the reservoir NO3 and soluble P stores that
    are adjusted by exchange with groundwater.'
  water_body_module: '`water_body_module` holds `res_wat_d`, the reservoir water-body balance
    record. Its `seep` field is overwritten with the total exchange volume computed here so
    reservoir water-balance calculations use the same seepage total.'
  constituent_mass_module: '`constituent_mass_module` supplies the counts of simulated salts
    and other constituents and the reservoir mass arrays that are incremented or decremented
    when groundwater exchange moves solutes between the aquifer and the reservoir.'
---

<!-- facts:header -->

Moves water, heat, and dissolved constituents between a reservoir and the groundwater cells connected to it. It also records the exchange totals used later in groundwater and reservoir balance accounting.

## Bottom Line

`gwflow_reservoir` is the reservoir-groundwater exchange routine used by SWAT+ gwflow. For each reservoir-connected grid cell pair, it computes Darcy-based seepage or inflow, limits that exchange by available reservoir water or groundwater storage, and stores the resulting fluxes in the daily/monthly/yearly groundwater summary arrays.

When heat and solute tracking are enabled, the routine also moves heat and constituent mass with the water exchange. It updates reservoir NO3, soluble P, salts, and other constituents, then writes the total seepage back to `res_wat_d(res_id)%seep` so reservoir water-balance code can use the same exchange total.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`res_control` calls this routine after it has computed the reservoir's daily precip and evaporation terms and decided that gwflow is active (`bsn_cc%gwflow /= 0`). `gwflow_reservoir` then replaces the old seepage shortcut with gwflow-based exchange totals, and later reservoir and groundwater balance code depends on `res_wat_d(res_id)%seep`, the `gw_hyd_ss*` flux summaries, and the reservoir constituent updates it leaves behind.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether reservoir-groundwater exchange is enabled and capture the starting reservoir volume. | If `gw_res_flag` is active, the routine begins by reading the reservoir's current water volume from `res(res_id)%flo`; otherwise it exits without changing state. |
| 2. Loop over each reservoir-connected grid cell and each groundwater neighbor of that cell. | The routine walks the reservoir connection list in `gw_resv_info(res_id)%cells`, then uses `gw_state(res_cell_id)%ncon` and `cell_con(res_cell_id)%cell_id(jj)` to identify each paired groundwater cell. |
| 3. Skip inactive groundwater cells and set up the geometry for exchange. | For active cells only, it reads the reservoir-cell and groundwater-cell areas, derives the smaller area, and uses its square root as an approximate connection length. |
| 4. Compute Darcy-based water exchange between the reservoir and the groundwater cell. | The head difference comes from reservoir elevation minus groundwater head, and `Q` is computed from reservoir hydraulic conductivity, head gradient, and the estimated connection size. |
| 5. Limit outflow by available reservoir water or inflow by available groundwater storage. | Positive `Q` cannot remove more water than the reservoir currently contains, while negative `Q` cannot exceed the groundwater cell's available storage; the latter case also reduces `gw_state(cell_id)%stor` by the accepted inflow amount. |
| 6. Record the water exchange in groundwater summary arrays and reservoir seepage totals. | The accepted `Q` is added to daily, monthly, and yearly groundwater reservoir-exchange summaries, and it is accumulated into `seep_total` for the reservoir. |
| 7. Transfer heat with groundwater inflow when heat tracking is active. | If heat simulation is on and flow is from aquifer to reservoir, the routine computes heat flux from groundwater temperature, density, heat capacity, and `Q`, caps it by available groundwater heat storage, and stores it in the daily and yearly heat summaries. |
| 8. Transfer solute mass with groundwater-to-reservoir exchange. | When solute tracking is active and water moves from aquifer to reservoir, the routine multiplies groundwater concentrations by `Q`, caps mass removal at available groundwater mass, and records the mass in the daily and cumulative groundwater solute summaries. |
| 9. Add the transferred groundwater solutes to reservoir water-quality stores. | The accepted solute mass increases reservoir NO3, soluble P, salt, and other constituent inventories through `res` and `res_water` using the current simulated counts in `cs_db`. |
| 10. Compute reservoir-water concentrations when flow goes from reservoir to aquifer. | For reservoir outflow, the routine derives reservoir concentrations from the current reservoir stores and `res_volume` so it can convert a water flux into solute mass. |
| 11. Remove reservoir solute mass by the outgoing exchange and keep it within available stores. | It converts `Q` and reservoir concentrations to solute mass, caps each solute by the reservoir's available mass, and subtracts the accepted amounts from `res`, `res_water`, and the reservoir constituent arrays. |
| 12. Store outgoing reservoir solute mass in groundwater solute summaries and finish the reservoir seepage total. | The solute mass leaving the reservoir is recorded in the daily and cumulative groundwater solute summaries, then `res_wat_d(res_id)%seep` is set to the total exchange volume for use by reservoir water-balance accounting. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr` | `gw_state(res_cell_id)%ncon, gw_state(res_cell_id)%area, gw_state(cell_id)%area, gw_state(cell_id)%head, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%resv, gw_hyd_ss_yr(cell_id)%resv, gw_hyd_ss_mo(cell_id)%resv, gw_heat_ss(cell_id)%resv, gw_heat_ss_yr(cell_id)%resv` |
| [sym:hydrograph_module] | `res` | `res(res_id)%flo, res(res_id)%no3, res(res_id)%solp` |
| [sym:water_body_module] | `res_wat_d` | `res_wat_d(res_id)%seep` |
| [sym:constituent_mass_module] | `cs_db, res_water` | `cs_db%num_salts, res_water(res_id)%salt(isalt), cs_db%num_cs, res_water(res_id)%cs(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `res_K` | When `gw_res_flag == 1` and a reservoir-connected cell pair produces positive `Q`, after limiting by reservoir volume. | `res_K` is loaded from `gw_resv_info(res_id)%hydc(k)` so the computed exchange uses the reservoir-connection hydraulic conductivity for that connection. |
| `res_thick` | When `gw_res_flag == 1` and a reservoir-connected cell pair is processed. | `res_thick` is loaded from `gw_resv_info(res_id)%thck(k)` so the Darcy calculation uses the specified connection thickness for that reservoir cell. |
| `gw_state(cell_id)%stor` | When `gw_res_flag == 1`, the paired groundwater cell is active, and the computed exchange is positive or negative after storage checks. | `gw_state(cell_id)%stor` is reduced only in the aquifer-to-reservoir case when the requested inflow would otherwise exceed the cell's available groundwater storage. |
| `gw_hyd_ss(cell_id)%resv` | When a valid reservoir-cell exchange has been computed for an active groundwater cell. | `gw_hyd_ss(cell_id)%resv` is incremented by the accepted `Q` so the day's groundwater reservoir exchange is available to gwflow water-balance reporting. |
| `gw_hyd_ss_yr(cell_id)%resv` | When a valid reservoir-cell exchange has been computed for an active groundwater cell. | `gw_hyd_ss_yr(cell_id)%resv` is incremented by the accepted `Q` so yearly groundwater reservoir exchange totals accumulate alongside the daily value. |
| `gw_hyd_ss_mo(cell_id)%resv` | When a valid reservoir-cell exchange has been computed for an active groundwater cell. | `gw_hyd_ss_mo(cell_id)%resv` is incremented by the accepted `Q` so monthly groundwater reservoir exchange totals accumulate alongside the daily value. |
| `gw_heat_ss(cell_id)%resv` | When heat tracking is enabled and `Q < 0` so water moves from groundwater to the reservoir. | `gw_heat_ss(cell_id)%resv` is incremented by the capped heat flux removed from the groundwater cell. |
| `gw_heat_ss_yr(cell_id)%resv` | When heat tracking is enabled and `Q < 0` so water moves from groundwater to the reservoir. | `gw_heat_ss_yr(cell_id)%resv` is incremented by the same capped heat flux for yearly heat accounting. |
| `gwsol_ss(cell_id)%solute(s)%resv` | When solute tracking is enabled and `Q < 0` so mass leaves groundwater for the reservoir. | `gwsol_ss(cell_id)%solute(s)%resv` is set to the accepted mass removed from the groundwater cell for solute `s`. |
| `gwsol_ss_sum(cell_id)%solute(s)%resv` | When solute tracking is enabled and `Q < 0` so mass leaves groundwater for the reservoir. | `gwsol_ss_sum(cell_id)%solute(s)%resv` accumulates the accepted groundwater solute mass across the simulation period. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%resv` | When solute tracking is enabled and `Q < 0` so mass leaves groundwater for the reservoir. | `gwsol_ss_sum_mo(cell_id)%solute(s)%resv` accumulates the accepted groundwater solute mass into the monthly summary. |
| `res(res_id)%no3` | When solute tracking is enabled and `Q < 0` so mass enters the reservoir from groundwater. | `res(res_id)%no3` increases by the accepted nitrate mass converted from grams to kilograms. |
| `res(res_id)%solp` | When solute tracking is enabled and `Q < 0` so mass enters the reservoir from groundwater. | `res(res_id)%solp` increases by the accepted soluble phosphorus mass converted from grams to kilograms. |
| `res_water(res_id)%salt(isalt)` | When solute tracking is enabled and `Q < 0` so mass enters the reservoir from groundwater. | `res_water(res_id)%salt(isalt)` increases by the accepted salt mass for each salt ion that is simulated. |
| `res_water(res_id)%cs(ics)` | When solute tracking is enabled and `Q < 0` so mass enters the reservoir from groundwater. | `res_water(res_id)%cs(ics)` increases by the accepted non-salt constituent mass for each simulated constituent. |
| `res_wat_d(res_id)%seep` | When reservoir-water exchange has been accumulated across all connected cells, at the end of the routine. | `res_wat_d(res_id)%seep` is set to the total accepted seepage/exchange volume for the reservoir so the reservoir water balance can use the same gwflow result. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior-changing source revisions for this procedure. The initial 9d9069f addition introduced `gwflow_reservoir` as a new gwflow reservoir exchange routine with water, heat, and solute handling. The 05cc429 re-merge expanded that logic by adding `heat_flux` and `seep_total`, accumulating reservoir seepage across connections, limiting positive `Q` against total reservoir water, capping negative `Q` against groundwater storage, and storing the total in `res_wat_d(res_id)%seep`. Later source-only lineage entries `f1e61a3`, `39fabde`, and `94b6dec` were resolved but have no available diffs here, so no additional behavioral changes can be confirmed from the provided evidence.

- 9d9069f: added the reservoir-groundwater exchange subroutine with Darcy flow, heat transfer, and solute mass transfer between reservoir water and groundwater cells.
- 05cc429: added cumulative seepage tracking and heat-seepage bookkeeping, plus explicit reservoir and groundwater storage caps on exchange volume; the routine now writes the final seepage total back to `res_wat_d(res_id)%seep`.
- 05cc429: extended reservoir exchange bookkeeping so daily/monthly/yearly groundwater summaries capture reservoir water, heat, and solute fluxes during each call.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_reservoir' has no extracted documentation comment.
