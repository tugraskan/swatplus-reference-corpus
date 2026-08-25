---
kind: procedure
symbol: gwflow_solute
title: gwflow_solute
status: filled
source_hash: f45ade4a271577cb
version_label: SWAT+ 62.0.0
locals:
  i: Loop index for groundwater cells; used to process each cell and later copy updated concentrations
    back into the main state array.
  j: Declared general counter, but it is not used in the extracted source.
  k: Loop index for connected cells in the current cell's connection list.
  s: Loop index for solutes; used to compute transport, reaction, sorption, and concentration
    updates for each constituent.
  t: Loop index for the transport sub-timesteps inside one groundwater flow time step.
  cell_id: Holds the ID of the neighboring or current cell being referenced during transport
    calculations, including the cell passed to chemistry.
  gw_trans_time_step: Length of one groundwater transport sub-timestep, computed by dividing
    the flow time step by the number of transport steps.
  time_fraction: Fraction of the full flow step completed at the current transport sub-step;
    used to interpolate groundwater volume.
  gw_volume_old: Groundwater volume at the start of the flow step for the current cell.
  gw_volume_new: Groundwater volume at the end of the flow step for the current cell.
  gw_volume_inter: Interpolated groundwater volume at the current transport sub-step; used
    in chemistry and concentration calculations.
  mass_adv: Per-solute advective mass flux accumulated from all connected cells for the current
    transport sub-step.
  mass_dsp: Per-solute dispersive mass flux accumulated from all connected cells for the current
    transport sub-step.
  m_change: Per-solute net mass change over the transport sub-step after advection, dispersion,
    reactions, minerals, and sorption scaling are combined.
  del_no_sorp: Per-solute mass change computed before sorption adjustment, used to derive
    sorbed mass removal.
  mass_sorb: Per-solute mass removed by sorption during the transport sub-step.
  mass_rct_local: Declared local reaction mass buffer, but the source comment says it is unused
    because the module-level mass_rct is used instead.
  q_cell: Lateral flow rate between the current cell and one connected cell; its sign controls
    whether advective mass enters or leaves the current cell.
  face_sat: Saturated thickness at the interface between two connected cells, used in dispersion
    calculations.
  area1: Surface area of the connected cell, used to determine the smaller interface area
    for dispersion geometry.
  area2: Surface area of the current cell, used to determine the smaller interface area for
    dispersion geometry.
  area: The smaller of the two cell areas; used to estimate connection length as sqrt(area).
  conn_length: Connection length between cells, approximated from the smaller cell area and
    used in the concentration-gradient term for dispersion.
uses:
  gwflow_module: The groundwater module provides the cell geometry, connectivity, flow-step
    timing, and the solute state arrays that this routine reads and updates. In particular,
    `gw_state` supplies active/boundary status, head/volume geometry, and connection counts,
    while `gw_time_step` and `ncell` control how long and how many cells are processed.
  time_module: The time module matters because this routine divides the groundwater flow time
    step into transport sub-steps, and that time-step value is needed to compute `gw_trans_time_step`
    and scale mass updates.
---

<!-- facts:header -->

Computes groundwater solute transport for each flow time step, including advection, dispersion, reactions, and sorption. It updates cell concentrations over transport sub-steps and accumulates mass-budget terms for reporting.

## Bottom Line

This subroutine advances solute concentrations in groundwater cells during a flow time step. For each transport sub-step, it computes advective and dispersive exchange from connected cells, calls the chemistry routine to fill reaction and mineral mass terms, applies sorption adjustment, and then updates each cell's solute mass and concentration.

It matters because it is the point where groundwater flow results are converted into solute transport and budget outputs. The routine also accumulates per-cell and summary bookkeeping for advection, dispersion, reactions, minerals, and sorption so later mass-balance writeout can report what happened during the step.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `gwflow_lateral` during a flow time step, after the lateral groundwater flow solution has populated the cell connection flows, saturation thicknesses, and updated head/hold information used here. Its results feed the groundwater solute state (`gwsol_state`) and the mass-balance accumulators that later reporting depends on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute transport sub-step size. | Divides the full groundwater flow step by `num_ts_transport` to get the length of one transport sub-timestep. |
| 2. Loop over transport sub-steps and cells. | Iterates through each transport sub-timestep and then through each groundwater cell. |
| 3. Skip non-interior cells and compute cell volumes. | Processes only interior cells, computes old and new groundwater volume from head, bottom, area, and specific yield, and interpolates volume for the current sub-step. |
| 4. Accumulate advective mass exchange from connected cells. | Loops over each connection, uses lateral flow direction to choose donor concentration, and sums advective mass flux for each solute. |
| 5. Accumulate dispersive mass exchange. | Uses interface saturation thickness, the smaller of the two cell areas, and a length scale from sqrt(area) to compute concentration-gradient-driven dispersive mass exchange. |
| 6. Call chemistry and initialize reaction buffers. | Sets the current cell ID, clears reaction and mineral mass arrays, and calls `gwflow_chem` with the interpolated groundwater volume so chemistry can populate reaction terms. |
| 7. Compute net mass change and sorption loss. | Combines advection, dispersion, reaction, mineral, and background total terms into a net mass change, then computes the amount removed by sorption from the unsorbed and sorbed formulations. |
| 8. Update cell mass and concentration. | Adds the net mass change to each solute mass, clips negative mass to zero, and converts mass back to concentration using the interpolated groundwater volume; if volume is zero, both mass and concentration are reset to zero. |
| 9. Accumulate per-step budget terms. | Stores advective, dispersive, reaction, mineral, and sorption contributions in the cell-level solute summary arrays for later budget reporting. |
| 10. Accumulate annual and monthly summary terms. | Adds the same reaction, mineral, and sorption contributions to the cumulative annual and monthly summary arrays. |
| 11. Zero concentrations for constant-concentration cells. | For boundary cells marked as constant concentration, resets `cnew` to zero instead of computing transport updates. |
| 12. Copy new concentrations into the main state array. | After each transport sub-step, copies the computed `cnew` values into `gwsol_state(i)%solute(s)%conc` so the next sub-step uses the updated concentrations. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_time_step, ncell` | `gw_state(i)%botm, gw_state(i)%area, gw_state(i)%hold, gw_state(i)%spyd, gw_state(i)%head, gw_state(i)%ncon, gw_state(cell_id)%area` |
| [sym:time_module] | `gw_time_step` | `gw_time_step` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mass_rct` | Inside interior cells (`gw_state(i)%stat == 1`), after calling `gwflow_chem` and before mass-budget storage. | The module-level reaction mass array is reset to zero and then filled by `gwflow_chem`; its values represent the chemical reaction source or sink used in the transport mass-change calculation and later budget terms. |
| `mass_min` | Inside interior cells (`gw_state(i)%stat == 1`), after calling `gwflow_chem` and before mass-budget storage. | The module-level mineral mass array is reset to zero and then filled by `gwflow_chem`; its values represent mineral-related mass change used in the transport update and cumulative budget terms. |
| `gwsol_state(i)%solute(s)%mass` | For active interior cells during each transport sub-step when the routine computes `m_change` and applies it to the cell. | The solute mass in the current groundwater cell is incremented by the net mass change for each solute, then clipped to zero if negative; this is the transported mass that carries into the next sub-step. |
| `gwsol_state(i)%solute(s)%cnew` | For active interior cells after mass is updated; if `gw_volume_inter > 0`, concentration is recomputed from mass, otherwise it is cleared. | The new concentration is derived from updated solute mass divided by interpolated groundwater volume, or set to zero when no groundwater volume is present. |
| `gwsol_ss(i)%solute(s)%advn` | For active interior cells when storing per-step mass-budget terms, using the advective mass flux computed from connected-cell flows. | The advection budget accumulator records how much solute mass moved by advective transport during the sub-step. |
| `gwsol_ss(i)%solute(s)%disp` | For active interior cells when storing per-step mass-budget terms, using the dispersive mass flux computed from concentration gradients. | The dispersion budget accumulator records how much solute mass moved by dispersive exchange during the sub-step. |
| `gwsol_ss(i)%solute(s)%rcti` | For active interior cells after chemistry, when `mass_rct(s) > 0`. | The incoming reaction budget accumulator stores positive reaction production for the solute during the sub-step. |
| `gwsol_ss(i)%solute(s)%rcto` | For active interior cells after chemistry, when `mass_rct(s) <= 0`. | The outgoing reaction budget accumulator stores reaction consumption for the solute during the sub-step. |
| `gwsol_ss(i)%solute(s)%minl` | For active interior cells during per-step budget storage, using the mineral mass returned by chemistry. | The mineral budget accumulator records mineral-related mass change for the solute during the sub-step. |
| `gwsol_ss(i)%solute(s)%sorb` | For active interior cells during per-step budget storage, after sorption loss is computed. | The sorption budget accumulator records the mass removed by sorption during the sub-step. |
| `gwsol_ss_sum(i)%solute(s)%rcti` | For active interior cells when annual/monthly summaries are updated and `mass_rct(s) > 0`. | The annual summary reaction-production accumulator stores positive reaction mass for later writeout. |
| `gwsol_ss_sum_mo(i)%solute(s)%rcti` | For active interior cells when annual/monthly summaries are updated and `mass_rct(s) > 0`. | The monthly summary reaction-production accumulator stores positive reaction mass for later writeout. |
| `gwsol_ss_sum(i)%solute(s)%rcto` | For active interior cells when annual/monthly summaries are updated and `mass_rct(s) <= 0`. | The annual summary reaction-consumption accumulator stores negative reaction mass for later writeout. |
| `gwsol_ss_sum_mo(i)%solute(s)%rcto` | For active interior cells when annual/monthly summaries are updated and `mass_rct(s) <= 0`. | The monthly summary reaction-consumption accumulator stores negative reaction mass for later writeout. |
| `gwsol_ss_sum(i)%solute(s)%minl` | For active interior cells during annual/monthly summary storage. | The annual mineral summary accumulator records mineral mass change for later reporting. |
| `gwsol_ss_sum_mo(i)%solute(s)%minl` | For active interior cells during annual/monthly summary storage. | The monthly mineral summary accumulator records mineral mass change for later reporting. |
| `gwsol_ss_sum(i)%solute(s)%sorb` | For active interior cells during annual/monthly summary storage. | The annual sorption summary accumulator records sorbed mass removed during the sub-step. |
| `gwsol_ss_sum_mo(i)%solute(s)%sorb` | For active interior cells during annual/monthly summary storage. | The monthly sorption summary accumulator records sorbed mass removed during the sub-step. |
| `gwsol_state(i)%solute(s)%conc` | After each transport sub-step for all cells when the routine copies `cnew` into the main concentration array. | The current groundwater solute concentration is replaced with the newly computed concentration so the next sub-step starts from the updated state. |

## File I/O

<!-- facts:io -->


## Lineage

`gwflow_solute.f90` was introduced in `9d9069f` (2026-03-31, "gwflow re-merge: module foundation - unified sources/sinks (ss) type, file renam…") and has been changed in 2 non-merge commit(s) since, most recently `92db11b` (2026-04-01, "gwflow re-merge: transport solvers, chemistry, wallo div_conc integration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `gwflow_solute.f90` are listed.

- `92db11b` (2026-04-01) — gwflow re-merge: transport solvers, chemistry, wallo div_conc integration
- `9d9069f` (2026-03-31) — gwflow re-merge: module foundation - unified sources/sinks (ss) type, file renames, heat/pond/phreatophyte types, stubs

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_solute' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
