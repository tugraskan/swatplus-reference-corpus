---
kind: procedure
symbol: cb_soil_snap_emit
title: cb_soil_snap_emit
status: filled
source_hash: 7a392f1b8e74cde9
version_label: SWAT+ 62.0.0
args:
  u_txt: Text output unit number. It controls which already-open text snapshot file receives
    the wide per-layer row.
  u_csv: CSV output unit number. It controls which already-open CSV snapshot file receives
    the row when CSV output is enabled.
  stage: Snapshot stage label such as `begsim`, `endsim`, or `period`. The code documents
    the stage for the row, but the emitted layout is the same for all three values.
  hru_j: HRU index whose soil profile is being exported. It selects `soil(hru_j)` and `soil1(hru_j)`
    data for the row.
  hru_iob: Index into `ob` for the current HRU object metadata. It is passed to the row-id
    helpers so the emitted row is tagged with the correct GIS ID and name.
locals:
  k: Loop index over soil layers and fixed output columns. It is used to copy each HRU layer
    value into the temporary buffer up to `min(cb_n_layers, n_use)`.
  n_use: Actual number of soil layers in the current HRU profile, taken from `soil(hru_j)%nly`.
    It limits how many real layer values are copied and tells the write helpers how much of
    the fixed-width row is populated.
  buf: Temporary fixed-length layer buffer passed to the row-writing helpers. It holds one
    variable's per-layer values and is reset before each block so missing layers can be padded
    consistently.
---

<!-- facts:header -->

Emits one wide soil-snapshot row for an HRU to text and, optionally, CSV output. It writes the same per-layer layout for begsim, endsim, and period snapshots.

## Bottom Line

cb_soil_snap_emit is the shared formatter for soil snapshot exports. Given an HRU and open text/CSV units, it writes the HRU row prefix and then appends one column block per soil layer for depth, bulk density, available water content, saturated hydraulic conductivity, soil carbon, clay, silt, sand, rock, albedo, USLE K, electrical conductivity, calcium, and pH.

The routine always writes the text row, and only writes the CSV row when `pco%csvout == "y"`. It pads any unused layer slots to the fixed `cb_n_layers` width, so downstream snapshot files stay column-aligned across HRUs with different soil profile depths.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when the soil/carbon writer needs to emit snapshot rows for a specific HRU, both for period snapshots and for begsim/endsim snapshot output. `cb_soil_snap_period` prepares the correct text and CSV unit numbers and passes `stage='period'`, while `soil_nutcarb_write` calls it directly for begsim/endsim exports. Its output feeds the soil snapshot files that report layer-wise soil and carbon state for later inspection and comparison.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Determine how many soil layers to export | Sets `n_use` from `soil(hru_j)%nly`, so later writes know how many actual layers belong to this HRU profile. |
| 2. Write the text-row identifier | Calls the text row-id helper to emit the HRU/object prefix on the text snapshot unit before any numeric columns are written. |
| 3. Emit text depth columns | Loads layer depths into `buf`, padding unused positions with zero before the helper writes the depth block to the text row. |
| 4. Emit text soil-property blocks | Repeatedly fills `buf` with one soil property at a time from `soil(hru_j)%phys` or `soil(hru_j)%ly`, then writes each block to the text row in a fixed order: bulk density, available water capacity, hydraulic conductivity, total soil carbon, clay, silt, sand, rock, albedo, USLE K, electrical conductivity, calcium, and pH. |
| 5. Optionally write the CSV row | Checks `pco%csvout`; when CSV export is enabled, writes the CSV row-id prefix and then repeats the same depth and per-layer property blocks to the CSV unit using comma-separated formatting. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

One resolved commit changed this file: bc7755a updated snapshot-export behavior in `soil_nutcarb_write.f90`. The diff shows `cb_soil_snap_emit` was simplified to use the shared wide-row helper pattern, with `stage` documented as `begsim`, `endsim`, or `period`, and the row content standardized so total soil carbon comes from `soil1(hru_j)%tot(ly)%c` for all stages.

- bc7755a standardized the snapshot row layout and carbon source so begsim, endsim, and period exports all use the same per-layer formatting and `soil1(hru_j)%tot(ly)%c` values.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cb_soil_snap_emit' has no extracted documentation comment.
