---
kind: procedure
symbol: gwflow_lateral
title: gwflow_lateral
status: filled
source_hash: 829cde4679afe97d
version_label: SWAT+ 62.0.0
locals:
  i: Loop index over cells, transit records, and output rows.
  j: Secondary loop index used when searching all cells for the current transit location.
  k: Index over the connected neighbors of a groundwater cell.
  n: Flow sub-step counter within the daily groundwater solution.
  cell_id: Identifier of the connected cell, current transit cell, or selected output cell.
  num_ts: Number of flow sub-steps computed from the groundwater time step.
  area1: Surface area of the connected neighbor cell.
  area2: Surface area of the current cell.
  area: Smaller of the two cell areas, used to estimate the shared interface size.
  conn_length: Estimated connection length across the shared face.
  dist_x: X-distance between cell centroids.
  dist_y: Y-distance between cell centroids.
  grad_distance: Centroid-to-centroid distance used in the hydraulic gradient.
  q_cell: Lateral flow rate between the current cell and one neighbor.
  q: Running sum of all lateral flows into or out of the current cell.
  face_k: Harmonic-mean hydraulic conductivity at the cell interface.
  sat_thick1: Saturated thickness of the connected cell.
  sat_thick2: Saturated thickness of the current cell.
  face_sat: Average saturated thickness at the interface.
  stor_change: Storage change over the current flow sub-step.
  sat_change: Change in saturated thickness implied by storage change.
  flow_area: Cross-sectional groundwater flow area at the interface.
  gradient: Hydraulic gradient between the two cell heads.
  qs: Specific discharge used for transit-time calculations.
  vs: Linear groundwater velocity used for transit-time calculations.
  ds: Distance traveled during one flow time step.
  dist_frac: Fraction of centroid-to-centroid distance traveled in one step.
  q_dir_x: Sign of x-direction movement for transit tracking.
  q_dir_y: Sign of y-direction movement for transit tracking.
  cell_length: Square-cell side length derived from cell area.
  x_min: Minimum x-boundary of the current cell.
  x_max: Maximum x-boundary of the current cell.
  y_min: Minimum y-boundary of the current cell.
  y_max: Maximum y-boundary of the current cell.
  cell_transit: Temporary cell identifier used for transit output bookkeeping.
  line_num: Count of populated values to write to the transit output record.
  line_vals: Packed output buffer holding transit time, coordinates, and cell id values.
uses:
  gwflow_module: Provides the groundwater cell geometry, hydraulic properties, connectivity,
    boundary classification, transit tracking arrays, and summary accumulators that this routine
    reads and updates while computing lateral flow and travel time.
  time_module: Imported for the broader GWFLOW time-step context; no specific resolved outside
    references from this module were provided in the context packet.
---

<!-- facts:header -->

Computes lateral groundwater exchange between connected cells using Darcy's law. It also updates groundwater head, storage, travel-time tracking, and optional heat/solute transport hooks.

## Bottom Line

gwflow_lateral is the groundwater lateral-flow step for the GWFLOW subsystem. For each flow sub-step, it loops over active cells, computes exchange with connected neighbors using Darcy's law, accumulates lateral and boundary water-budget terms, and updates each cell's storage and head.

When travel-time tracking is enabled, it also advances groundwater particle locations, records first-arrival times to channels or tiles, and writes selected transit records to the groundwater transit output unit. If heat or solute transport is enabled, it calls the corresponding routines inside the same flow loop so those processes stay synchronized with the updated heads and fluxes.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from gwflow_simulate after the model has prepared the groundwater flow state for the current step. It performs the lateral-flow update before the later save/write-out section in gwflow_simulate, and its results feed head, storage, transit-time, heat, and solute outputs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize flow accumulators | Compute the number of flow sub-steps from gw_time_step, then clear the per-cell head-change accumulators before the flow loop begins. |
| 2. Loop over flow sub-steps | Repeat the groundwater update for each sub-step in the daily solution. |
| 3. Process each active cell | Visit each cell and skip inactive ones; treat interior and boundary cells differently. |
| 4. Sum neighbor exchanges | For each connected neighbor, compute interface geometry, hydraulic conductivity, saturated thickness, gradient, and Darcy flow; store lateral flux and saturated thickness for transport accounting; optionally accumulate transit-direction offsets; then add the flow to the cell's lateral or boundary budget. |
| 5. Update storage and head | Convert the net flow balance into storage change and new head for active interior cells, or reset constant-head cells to their initial head and storage. |
| 6. Copy new heads forward | Move the newly computed head into the live head state and preserve the previous head in hold for the next sub-step. |
| 7. Call heat and solute transport | If enabled, call the groundwater heat and solute transport routines inside the same flow sub-step so they use the updated flow field. |
| 8. Advance transit locations | When travel-time tracking is enabled, locate each groundwater particle in its current or another cell, shift its coordinates by the cell's flow-induced offsets, advance its cumulative travel time, and record first arrival times to channels or tiles. |
| 9. Write transit output | Pack selected transit records into a line buffer and write them to the groundwater transit output unit. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_transit, gw_cell_chan_time, gw_cell_tile_time, bc_type_array, gw_transit_cells, gw_time_step, ncell, gw_ttime, gw_transit_num` | `gw_state(i)%hnew, gw_state(i)%hold, gw_state(i)%delx, gw_state(i)%dely, gw_state(i)%ncon, gw_state(cell_id)%area, gw_state(i)%area, gw_state(cell_id)%hydc, gw_state(i)%hydc, gw_state(cell_id)%botm, gw_state(cell_id)%head, gw_state(i)%botm, gw_state(i)%head, gw_state(i)%xcrd, gw_state(cell_id)%xcrd, gw_state(i)%ycrd, gw_state(cell_id)%ycrd, gw_state(cell_id)%spyd, gw_hyd_ss(i)%bndr, gw_hyd_ss(i)%latl, gw_hyd_ss_yr(i)%latl, gw_hyd_ss(i)%totl, gw_state(i)%stor, gw_state(i)%spyd, gw_state(i)%init, gw_transit(i)%cell, gw_state(cell_id)%delx, gw_state(cell_id)%dely, gw_state(j)%xcrd, gw_state(j)%ycrd, gw_state(j)%delx, gw_state(j)%dely, gw_transit(i)%t` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_state(i)%hnew` | During each flow sub-step for active interior cells | Set to the current head plus the storage-derived head change, or to the initial head for constant-head cells. |
| `gw_state(i)%hold` | At the start of the routine and before each head copy | Cleared to zero initially, then updated to preserve the previous head before head is overwritten with hnew. |
| `gw_state(i)%delx` | When travel-time tracking is enabled and a cell has nonzero lateral flow | Accumulated x-direction groundwater displacement for the current flow sub-step. |
| `gw_state(i)%dely` | When travel-time tracking is enabled and a cell has nonzero lateral flow | Accumulated y-direction groundwater displacement for the current flow sub-step. |
| `cell_con(i)%latl(k)` | For each connected neighbor during Darcy-flow calculation | Stores the lateral flow rate for the k-th connection so later transport and mass-balance calculations can use it. |
| `cell_con(i)%sat(k)` | For each connected neighbor during Darcy-flow calculation | Stores the interface saturated thickness used in transport and flow accounting. |
| `gw_hyd_ss(i)%bndr` | For each neighbor classified as a boundary cell | Accumulates boundary exchange volume for the current cell. |
| `gw_hyd_ss(i)%latl` | For each non-boundary neighbor | Accumulates lateral exchange volume for the current cell. |
| `gw_hyd_ss_yr(i)%latl` | For each non-boundary neighbor | Accumulates year-to-date lateral exchange volume for the current cell. |
| `gw_state(i)%stor` | After summing all neighbor flows in a sub-step | Updated by the net storage change implied by lateral and boundary flows. |
| `gw_state(i)%head` | After summing all neighbor flows in a sub-step | Overwritten with the new groundwater head for the next sub-step. |
| `gw_transit(i)%x` | When a transit particle remains in or moves through a cell | Shifted by the cell's x-direction displacement to track groundwater movement. |
| `gw_transit(i)%y` | When a transit particle remains in or moves through a cell | Shifted by the cell's y-direction displacement to track groundwater movement. |
| `gw_transit(i)%cell` | When a transit particle is found in a new cell | Updated to the cell index containing the particle's current coordinates. |
| `gw_transit(i)%t` | Each time transit tracking advances | Incremented by the groundwater flow time step. |
| `gw_cell_chan_time(i)` | When a transit particle first enters a channel cell | Stores the first travel time to a channel cell for that transit record. |
| `gw_cell_tile_time(i)` | When tile drainage is enabled and a transit particle first enters a tile cell | Stores the first travel time to a tile-drained cell for that transit record. |

## File I/O

<!-- facts:io -->


## Lineage

`gwflow_lateral.f90` was introduced in `9d9069f` (2026-03-31, "gwflow re-merge: module foundation - unified sources/sinks (ss) type, file renam…") and has been changed in 5 non-merge commit(s) since, most recently `c38f3b8` (2026-04-05, "clean up and bugfixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `gwflow_lateral.f90` are listed.

- `c38f3b8` (2026-04-05) — clean up and bugfixes
- `b78c4ea` (2026-04-04) — gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portability, dynamic array sizes
- `92db11b` (2026-04-01) — gwflow re-merge: transport solvers, chemistry, wallo div_conc integration
- `72aa70a` (2026-03-31) — gwflow re-merge: core flow solver - simulate driver, lateral flow, output system
- `9d9069f` (2026-03-31) — gwflow re-merge: module foundation - unified sources/sinks (ss) type, file renames, heat/pond/phreatophyte types, stubs

## Review Notes

- Direct file I/O writes selected groundwater transit records to out_gw_transit; the unit name is parser-supplied and no open/close context was provided.
- time_module is imported, but no resolved outside references from that module were provided in the context packet.
- warning: missing_doc: Procedure 'gwflow_lateral' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
