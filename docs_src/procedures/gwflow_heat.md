---
kind: procedure
symbol: gwflow_heat
title: gwflow_heat
status: filled
source_hash: cb6d5083fdf2c1e5
version_label: SWAT+ 62.0.0
grounding_allow:
- i
- k
- cell_id
- heat_adv
- cell_adv
- heat_dsp
- q_heat
- heat_change
- face_thmc
- q_cell
- dist_x
- dist_y
- grad_distance
- gradient
- area1
- area2
- area
- conn_length
- face_sat
- flow_area
locals:
  i: Loop index over groundwater cells; also used in the final pass that copies new temperatures
    into the live state.
  k: Loop index over the connected cells for a given groundwater cell.
  cell_id: Holds the id of the current connected cell being processed inside the connection
    loops.
  heat_adv: Accumulates the net advective heat flux for the current cell from all connected-cell
    flows.
  cell_adv: Stores the heat flux contribution from one connection before it is added to the
    cell total.
  heat_dsp: Accumulates the net dispersive heat flux for the current cell from all connected
    cells.
  q_heat: Stores the dispersive heat flux contribution from one connection before it is added
    to the cell total.
  heat_change: Stores the net heat-storage change applied to the cell after advection, dispersion,
    and total source/sink terms are combined.
  face_thmc: Holds the harmonic-mean thermal conductivity at the interface between the current
    cell and a connected cell.
  q_cell: Stores the lateral groundwater flow rate between the current cell and a connected
    cell; its sign controls advective heat direction.
  dist_x: X-coordinate separation between the current cell centroid and the connected cell
    centroid.
  dist_y: Y-coordinate separation between the current cell centroid and the connected cell
    centroid.
  grad_distance: Distance between cell centroids used as the denominator for the temperature
    gradient.
  gradient: Temperature gradient between the connected cell and the current cell along the
    centroid-to-centroid line.
  area1: Surface area of the connected cell, used when estimating interface geometry.
  area2: Surface area of the current cell, used when estimating interface geometry.
  area: The smaller of the two cell areas, used as the basis for the shared connection length.
  conn_length: Estimated connection length at the cell face, computed as the square root of
    the smaller cell area.
  face_sat: Saturated thickness at the interface, taken from the connection geometry data
    for this cell and neighbor.
  flow_area: Cross-sectional area available for dispersive heat transport at the interface,
    computed from face saturation and connection length.
uses:
  gwflow_module: '`gwflow_module` supplies the groundwater cell state and heat-summary arrays
    that this routine reads and updates. It needs `gw_state(i)%ncon` to know which neighbors
    to loop over, `gw_state(i)%xcrd`/`ycrd` and `gw_state(cell_id)%xcrd`/`ycrd` to compute
    distance and gradient, `gw_state(i)%area` and `gw_state(cell_id)%area` to estimate the
    interface geometry, `gw_state(i)%stor` to convert heat change back into temperature, and
    `gw_heat_ss` / `gw_heat_ss_yr` to accumulate daily and yearly heat-flow summaries for
    lateral, boundary, and dispersion terms.'
  time_module: '`gw_time_step` converts the instantaneous heat fluxes accumulated in each
    cell into per-step heat totals and summary values. Without the groundwater flow time step,
    the routine could not scale `heat_adv`, `heat_dsp`, and `gw_heat_ss(i)%totl` into the
    heat-content update used for storage and temperature.'
---

<!-- facts:header -->

Calculates groundwater heat advection and dispersion for each active cell, then updates the stored and current groundwater temperature state.

## Bottom Line

`gwflow_heat` runs inside the groundwater flow time step to move heat with lateral groundwater exchange and dispersive mixing between connected cells. It also keeps per-cell heat storage balanced so the model can convert the updated heat content back into a new temperature.

The routine accumulates heat gains and losses from connection flows, boundary exchanges, and dispersion into `gwheat_state(i)%stor`, updates `gwheat_state(i)%tnew`, and finally rolls the new temperature into `gwheat_state(i)%temp` / `told`. Those updates feed the next groundwater transport step because the routine is called from `gwflow_lateral` after the Darcy head update.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the groundwater lateral-flow solution, after `gwflow_lateral` has updated heads and while heat transport is enabled by `gw_heat_flag`. `gwflow_lateral` sets up the flow state and connection fluxes that this routine uses, and the updated `gwheat_state(i)%temp` values carry forward into later groundwater transport behavior in the same simulation step.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize per-cell heat bookkeeping from the current stored heat. | Copies `gwheat_state(i)%stor` into `heat_cell(i)` for every cell so the routine can track how much heat remains available while it moves heat between cells. |
| 2. Process each active groundwater cell. | Loops over all cells and limits the transport work to interior cells (`gw_state(i)%stat == 1`), starting each one from its current stored heat. |
| 3. Compute advective heat exchange across each connected flow link. | For every connected cell, uses the sign of `cell_con(i)%latl(k)` to determine whether heat enters or leaves the current cell, limits the flux by available heat in the donor cell, adds the result to `heat_adv`, updates `heat_cell(i)`, and records the daily and yearly lateral/boundary summaries in `gw_heat_ss` and `gw_heat_ss_yr`. |
| 4. Compute dispersive heat exchange across each connected face. | For every connection, computes centroid distance, temperature gradient, interface area, face saturation, and harmonic-mean thermal conductivity, then uses them to estimate dispersive heat flux. The flux is limited so it cannot remove more heat than is available in the donor cell, summed into `heat_dsp`, and applied to `heat_cell(i)`. |
| 5. Convert flux totals into daily and yearly dispersion summaries. | Stores the current step's dispersive heat into `gw_heat_ss(i)%disp` and accumulates it into the yearly dispersion total `gw_heat_ss_yr(i)%disp`. |
| 6. Update stored heat and derive the new temperature. | Combines advection, dispersion, and `gw_heat_ss(i)%totl`, scales by `gw_time_step`, adds the resulting heat change to `gwheat_state(i)%stor`, and converts the updated storage to `gwheat_state(i)%tnew` when groundwater storage is positive; otherwise it sets the new temperature to zero. |
| 7. Roll the new temperature into the live state for the next step. | Copies the previous temperature to `gwheat_state(i)%told` and promotes `gwheat_state(i)%tnew` to `gwheat_state(i)%temp` for all cells. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_heat_ss, gw_heat_ss_yr, ncell, gw_time_step` | `gw_state(i)%ncon, gw_heat_ss(i)%bndr, gw_heat_ss(i)%latl, gw_heat_ss_yr(i)%latl, gw_state(i)%xcrd, gw_state(cell_id)%xcrd, gw_state(i)%ycrd, gw_state(cell_id)%ycrd, gw_state(cell_id)%area, gw_state(i)%area, gw_heat_ss(i)%disp, gw_heat_ss_yr(i)%disp, gw_heat_ss(i)%totl, gw_state(i)%stor` |
| [sym:time_module] | `time_module` | `gw_time_step` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `heat_cell(i)` | When `gw_state(i)%stat == 1` and the routine starts processing cell `i`. | `heat_cell(i)` is seeded with the cell's current stored heat so the routine can subtract outgoing heat and add incoming heat while preserving a per-cell availability check. |
| `heat_cell(cell_id)` | When a connected cell supplies heat or when the current cell receives a limiting adjustment during the advection loop. | `heat_cell(cell_id)` is reduced when that neighbor donates more advective heat than it has available, and `heat_cell(i)` is increased or decreased by the final per-connection advective transfer. |
| `gw_heat_ss(i)%bndr` | When `Q_cell > 0` and the connected cell is a boundary cell (`gw_state(cell_id)%stat == 2`). | `gw_heat_ss(i)%bndr` accumulates the advective heat exchange associated with boundary inflow into the cell, scaled by the groundwater time step. |
| `gw_heat_ss(i)%latl` | When `Q_cell > 0` or `Q_cell <= 0` and the connected cell is not a boundary cell. | `gw_heat_ss(i)%latl` records the cell-to-cell advective heat exchange for the current step, capturing lateral transport between interior groundwater cells. |
| `gw_heat_ss_yr(i)%latl` | When the connected cell is not a boundary cell during the same advective loop. | `gw_heat_ss_yr(i)%latl` accumulates the yearly running total of lateral advective heat exchange. |
| `gw_heat_ss(i)%disp` | When a connection produces positive dispersive heat flux and the donor cell lacks enough heat to satisfy it. | `gw_heat_ss(i)%disp` is not changed directly here, but the flux is limited before it contributes to the cell's dispersion total; the limiting prevents the summary from implying more heat moved than existed in the donor cell. |
| `gw_heat_ss_yr(i)%disp` | When yearly dispersion is accumulated in the dispersion section. | `gw_heat_ss_yr(i)%disp` grows by the current step's dispersive heat contribution so the yearly heat budget remains consistent with the per-step value in `gw_heat_ss(i)%disp`. |
| `gwheat_state(i)%stor` | After advection, dispersion, and total source/sink terms are combined for an interior cell. | `gwheat_state(i)%stor` is increased by the net heat change for the step, representing the updated stored heat content of the cell. |
| `gwheat_state(i)%tnew` | When the cell has positive groundwater storage after the heat update. | `gwheat_state(i)%tnew` is computed from stored heat divided by `gw_rho * gw_cp * gw_state(i)%stor`, converting heat content back into temperature for the next state. |
| `gwheat_state(i)%told` | When the cell has no positive groundwater storage after the heat update. | `gwheat_state(i)%told` is not changed in this routine; it is assigned during the final state roll-forward pass as the prior temperature before `tnew` replaces `temp`. |
| `gwheat_state(i)%temp` | When the cell has no positive groundwater storage after the heat update. | `gwheat_state(i)%temp` is set to the new temperature value at the end of the routine, and cells with zero storage are forced to zero temperature instead of being divided by zero. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved for `gwflow_heat`. The initial commit `9d9069f` created the subroutine as an empty stub with only a purpose comment and an immediate return. The later commit `92db11b` replaced that stub with the full groundwater heat-transport implementation, added `use gwflow_module` and `use time_module`, declared local working variables, computed advective and dispersive heat exchange, updated heat summary arrays, and rolled updated heat storage into new and current temperatures.

- `9d9069f` introduced `gwflow_heat` as a placeholder routine with no transport logic, so no state changes occurred at that stage.
- `92db11b` implemented the actual heat-transport algorithm: advection across `cell_con(i)%latl(k)`, dispersion using centroid distance and harmonic-mean conductivity, heat-summary accumulation in `gw_heat_ss` / `gw_heat_ss_yr`, and storage-to-temperature updates in `gwheat_state(i)`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_heat' has no extracted documentation comment.
