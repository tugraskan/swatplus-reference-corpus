---
kind: output_family
source_symbols:
- flow_dur_curve
title: flow_duration_curve.out
status: filled
source_hash: 912cfe9d5af12a54
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`flow_dur_curve`](../procedures/flow_dur_curve.md)
**File(s):** `flow_duration_curve.out` (unit 6000)

## Bottom Line

`flow_duration_curve.out` summarizes each routing object's flow behavior, including its flashiness index and flow-duration-curve statistics computed over the run.

## What It Writes

One row per command/object: object type, properties, drainage area, flashiness index, and flow-duration-curve summary values (`write (6000, …)`).

## Source Links

- Writer: [`flow_dur_curve`](../procedures/flow_dur_curve.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `flow_dur_curve.f90:16` (opens unit 6000)
- `flow_dur_curve.f90:145` (writes per-object FDC rows)
