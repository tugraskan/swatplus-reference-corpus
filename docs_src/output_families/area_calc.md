---
kind: output_family
source_symbols:
- hyd_connect
title: area_calc.out
status: filled
source_hash: 2b184a6ef0e85826
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`hyd_connect`](../procedures/hyd_connect.md)
**File(s):** `area_calc.out` (unit 9004, record length 80000)

## Bottom Line

`area_calc.out` is a per-object area-calculation diagnostic produced while the hydrograph connectivity is built. It lets you compare each object's configured drainage area with the area SWAT+ computes from the connectivity.

## What It Writes

One row per spatial object: `iob`, object type, object number, `area_ha` (configured) and `area_ha_calc` (computed), plus related connectivity fields (`write (9004, …)`).

## Source Links

- Writer: [`hyd_connect`](../procedures/hyd_connect.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `hyd_connect.f90:21` (opens unit 9004)
- `hyd_connect.f90:537` (writes per-object area rows)
