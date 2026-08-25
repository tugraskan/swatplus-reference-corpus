---
kind: procedure
symbol: gwflow_phreatophyte
title: gwflow_phreatophyte
status: filled
source_hash: 2e404c09508c6dee
version_label: SWAT+ 62.0.0
locals:
  k: Loop counter over the phreatophyte-enabled groundwater cells in gw_phyt_ids; each pass
    selects one cell to process.
  i: Loop counter over adjacent points in the depth-to-ET lookup curve; it finds which segment
    brackets the current water-table depth.
  cell_id: The current groundwater cell index taken from gw_phyt_ids(k), used to read state
    and update summary totals.
  wt_depth: Computed depth to the water table below the ground surface for the current cell,
    from gw_state(cell_id)%elev minus gw_state(cell_id)%head.
  ratio: Interpolation fraction within the active depth-rate segment, based on where wt_depth
    falls between gw_phyt_dep(i) and gw_phyt_dep(i+1).
  et_rate: Interpolated phreatophyte transpiration rate for the current water-table depth,
    in depth-per-time units.
  et_q: Volumetric phreatophyte withdrawal for the current cell; first computed as rate times
    area, then capped by storage and negated before being added to groundwater sinks.
uses:
  gwflow_module: This module provides the groundwater cell state needed to compute phreatophyte
    demand and the summary arrays that receive the resulting sink term. `gw_state(cell_id)%elev`
    and `%head` define water-table depth, `%stor` limits the withdrawal to available groundwater,
    and `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_mo` collect the daily, yearly, and monthly
    phreatophyte flux totals that later groundwater balance reporting uses.
---

<!-- facts:header -->

Computes phreatophyte groundwater extraction for cells where the option is enabled. It turns a water-table-depth curve into a volumetric groundwater removal and records that removal in the groundwater summaries.

## Bottom Line

This routine loops over groundwater cells that have phreatophytes, estimates transpiration from the current water-table depth using a piecewise linear depth-rate curve, converts that rate to a cell volume, and limits the withdrawal to the water currently stored in the aquifer. The resulting volume is stored as a negative groundwater sink.

Its main job is to supply the phreatophyte loss term used by the groundwater simulation water balance. The daily, monthly, and yearly summary fields are incremented here so later groundwater accounting can report how much water was removed by phreatophytes.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the groundwater simulation after recharge and groundwater evapotranspiration have been handled and before channel exchange and other groundwater interactions. `gwflow_simulate` prepares the groundwater state and active phreatophyte cell lists before calling it, and its negative sink totals feed later groundwater balance calculations and summary reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check phreatophyte flag | Only execute the routine body when the phreatophyte option is enabled with gw_phyt_flag == 1; otherwise skip all calculations and return. |
| 2. visit active cells | Loop over each phreatophyte-enabled groundwater cell, map the loop index to the actual cell_id, and prepare to compute that cell's withdrawal. |
| 3. compute depth and reset flux | Initialize the cell's ET volume to zero and calculate water-table depth from ground elevation minus simulated head. |
| 4. find the depth segment | Scan the phreatophyte depth curve to find the segment that brackets wt_depth, then linearly interpolate the transpiration rate between the two surrounding points and convert it to a volumetric withdrawal using the cell area. |
| 5. limit to available storage | If the computed withdrawal exceeds the groundwater storage in the cell, reduce it to the available storage so the sink cannot remove more water than exists. |
| 6. store as negative sink | Negate the volumetric withdrawal so it represents groundwater removal from the aquifer rather than an inflow. |
| 7. accumulate summaries | Add the negative phreatophyte flux to the daily, monthly, and yearly groundwater summary fields for the current cell so downstream water-balance accounting can report it. |
| 8. finish | Advance to the next cell until all active cells are processed, then return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo` | `gw_state(cell_id)%elev, gw_state(cell_id)%head, gw_state(cell_id)%stor, gw_hyd_ss(cell_id)%phyt, gw_hyd_ss_yr(cell_id)%phyt, gw_hyd_ss_mo(cell_id)%phyt` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_hyd_ss(cell_id)%phyt` | When gw_phyt_flag == 1 and the current cell's water-table depth falls within one of the phreatophyte depth segments, the computed negative withdrawal is added to gw_hyd_ss(cell_id)%phyt. | This daily groundwater sink records how much water phreatophytes removed from the aquifer in the current step, and it is used in the groundwater balance calculations after this routine returns. |
| `gw_hyd_ss_yr(cell_id)%phyt` | When gw_phyt_flag == 1 and the current cell is processed, the same negative withdrawal is added to gw_hyd_ss_yr(cell_id)%phyt. | This yearly accumulator tracks the phreatophyte groundwater loss over the current water year for reporting and annual water-balance summaries. |
| `gw_hyd_ss_mo(cell_id)%phyt` | When gw_phyt_flag == 1 and the current cell is processed, the same negative withdrawal is added to gw_hyd_ss_mo(cell_id)%phyt. | This monthly accumulator tracks the phreatophyte groundwater loss over the current month for monthly reporting and summary calculations. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed lineage commits were resolved. The earliest resolved commit, 9d9069f, created gwflow_phreatophyte as a stub with only a purpose comment, implicit none, and an immediate return. The later commit, 05cc429, replaced the stub with the full implementation: it added the gwflow_module use association, local counters and flux variables, the phreatophyte flag check, the per-cell loop, depth-based interpolation, storage capping, sign reversal, and updates to the daily, monthly, and yearly groundwater summary arrays.

- 9d9069f introduced the new subroutine skeleton but no behavior beyond return.
- 05cc429 added the complete phreatophyte extraction algorithm and summary accumulation into gw_hyd_ss, gw_hyd_ss_yr, and gw_hyd_ss_mo.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_phreatophyte' has no extracted documentation comment.
- algorithm_steps revised: merged the final loop/return into a concise completion step and expanded the computation steps to reflect the full source behavior.
- Source shows a typo in the inline comment near line 40 ('groundawter'); documentation preserves the intended groundwater meaning.
