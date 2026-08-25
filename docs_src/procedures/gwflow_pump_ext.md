---
kind: procedure
symbol: gwflow_pump_ext
title: gwflow_pump_ext
status: filled
source_hash: 86607129f88b0eb8
version_label: SWAT+ 62.0.0
locals:
  i: Loop counter over configured external pumps in `gw_pumpex_cell`, `gw_pumpex_nperiods`,
    and `gw_pumpex_rates`.
  j: Loop counter over the pumping periods associated with the current pump.
  s: Loop counter over solutes when solute transport is enabled.
  cell_id: The groundwater cell ID for the current external pump being processed.
  pumpex_start_date: Start day of the current pumping period, loaded from `gw_pumpex_dates(i,1,j)`.
  pumpex_end_date: End day of the current pumping period, loaded from `gw_pumpex_dates(i,2,j)`.
  q: The requested pumping rate for the current pump period, then capped to available groundwater
    storage before being applied as the actual withdrawal volume.
  solmass: Per-solute mass removed by pumping from the current cell during this day, computed
    from pumped volume and solute concentration.
  heat_flux: Heat removed with pumped groundwater, computed from cell temperature, water density,
    specific heat, and pumped volume, then capped by available heat storage.
uses:
  gwflow_module: All of the live pumping state, storage limits, and summary accumulators live
    in `gwflow_module`, so this routine can determine whether a cell is active, how much water
    is available, and where to record the extracted water, heat, and solute mass. The module-backed
    fields `gw_state(cell_id)%stor`, `gw_hyd_ss*%ppex`, `gw_heat_ss*%ppex`, and `gwsol_ss*%ppex`
    are the outputs that downstream groundwater balance and reporting code consumes.
---

<!-- facts:header -->

Removes external pumping withdrawals from active groundwater cells and records the water, heat, and solute losses in daily, monthly, and yearly groundwater summary states.

## Bottom Line

This routine runs only when external pumping is enabled. It walks each configured pump and each pumping period, checks whether the current simulation day falls inside that period, limits the withdrawal to the water actually in storage, and subtracts the withdrawal from the cell's groundwater storage and from the daily, monthly, and yearly pumping summary accumulators.

If heat or solute transport is active, it also removes the associated heat and solute mass from the matching groundwater summary states using the pumped water volume and the cell concentration/temperature. Those summary fields are later used by the groundwater balance and reporting logic in `gwflow_simulate` and other groundwater bookkeeping.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the groundwater simulation step after `gwflow_simulate` has finished the earlier bookkeeping for that day and before later groundwater exchanges such as tile-drain discharge are handled. `gwflow_simulate` sets up the current day counter and calls this routine; its results then feed the groundwater balance, daily/monthly/yearly summary accumulation, and any later reporting that uses the `ppex` pumping totals.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Proceed only when external pumping is enabled through `gw_pumpex_flag`; otherwise leave groundwater state unchanged. |
| 2. loop | Iterate over each configured external pump so the routine can apply withdrawals cell by cell. |
| 3. if | Skip inactive groundwater cells and only process pumps located in cells whose groundwater state is active. |
| 4. loop | Iterate over each pumping period configured for the current pump. |
| 5. if | Load the start and end day for the current period and apply pumping only when the simulation day falls within that date window. |
| 6. if | Read the requested withdrawal rate, cap it to the cell's available storage if necessary, and subtract the actual withdrawal from groundwater storage. |
| 7. if | Record the withdrawn water as negative pumping flux in the daily, monthly, and yearly hydrology summaries. |
| 8. if | When heat transport is enabled, compute extracted heat from cell temperature and pumped volume, cap it by available heat storage, and subtract it from daily and yearly heat summaries. |
| 9. if | When solute transport is enabled, enter the solute accounting for the pumped groundwater. |
| 10. loop | For each solute, compute pumped mass from volume and concentration, then subtract that mass from the daily, summed, and monthly solute pumping summaries. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, gw_daycount` | `gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%ppex, gw_hyd_ss_yr(cell_id)%ppex, gw_hyd_ss_mo(cell_id)%ppex, gw_heat_ss(cell_id)%ppex, gw_heat_ss_yr(cell_id)%ppex` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_state(cell_id)%stor` | When external pumping is active, the cell is active, the current day falls inside a pumping period, and the requested withdrawal exceeds available groundwater storage, the routine caps `Q` to the stored volume before subtracting it. | `gw_state(cell_id)%stor` is reduced by the actual pumped volume so the cell cannot lose more water than it contains. |
| `gw_hyd_ss(cell_id)%ppex` | When `gw_pumpex_flag == 1`, the cell is active, and the current day is inside the pumping period. | `gw_hyd_ss(cell_id)%ppex` accumulates the day’s external pumping as a negative hydrologic flux for the cell. |
| `gw_hyd_ss_yr(cell_id)%ppex` | When `gw_pumpex_flag == 1`, the cell is active, and the current day is inside the pumping period. | `gw_hyd_ss_yr(cell_id)%ppex` accumulates the same external pumping in the yearly groundwater water summary. |
| `gw_hyd_ss_mo(cell_id)%ppex` | When `gw_pumpex_flag == 1`, the cell is active, and the current day is inside the pumping period. | `gw_hyd_ss_mo(cell_id)%ppex` accumulates the same external pumping in the monthly groundwater water summary. |
| `gw_heat_ss(cell_id)%ppex` | When `gw_heat_flag == 1` and the cell is pumping during the active date window. | `gw_heat_ss(cell_id)%ppex` stores the pumped heat as a negative flux leaving the aquifer. |
| `gw_heat_ss_yr(cell_id)%ppex` | When `gw_heat_flag == 1` and the cell is pumping during the active date window. | `gw_heat_ss_yr(cell_id)%ppex` stores the pumped heat in the yearly heat summary. |
| `gwsol_ss(cell_id)%solute(s)%ppex` | When `gw_solute_flag == 1` and the cell is pumping during the active date window. | `gwsol_ss(cell_id)%solute(s)%ppex` stores the solute mass removed with pumped water as a negative flux. |
| `gwsol_ss_sum(cell_id)%solute(s)%ppex` | When `gw_solute_flag == 1` and the cell is pumping during the active date window. | `gwsol_ss_sum(cell_id)%solute(s)%ppex` accumulates the pumped solute mass in the cell’s summed solute bookkeeping. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%ppex` | When `gw_solute_flag == 1` and the cell is pumping during the active date window. | `gwsol_ss_sum_mo(cell_id)%solute(s)%ppex` accumulates the pumped solute mass in the monthly summed solute bookkeeping. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was introduced in `df07e3f` as part of the initial gwflow source set. `9d9069f` added the new external-pumping subroutine with water-only withdrawal accounting, and `05cc429` extended it by adding heat accounting, the `heat_flux` local, and the monthly water and solute summary updates currently present in the source.

- 9d9069f introduced `gwflow_pump_ext` as a new routine that subtracts external pumping from groundwater storage and water summary fields for active cells during configured date windows.
- 05cc429 expanded the routine to include heat withdrawal accounting, capped heat removal, and monthly water/solute summary updates, and it added the `heat_flux` local variable.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_pump_ext' has no extracted documentation comment.
