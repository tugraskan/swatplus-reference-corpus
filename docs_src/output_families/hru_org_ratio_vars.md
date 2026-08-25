---
kind: output_family
source_symbols:
- soil_carbvar_write_legacy
title: hru_org_ratio_vars
status: filled
source_hash: 644bbb94b1dcb7db
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md)
**File(s):** `hru_org_ratio_vars.txt` (unit 8378), `hru_org_ratio_vars.csv` (unit 8379)

## Bottom Line

`hru_org_ratio_vars` is a legacy per-layer organic-carbon ratio-variable file, reporting `soil1%org_ratio_lr` by layer. (Legacy carbon output — removed in rev 63.)

## What It Writes

Per HRU per output period, per layer: `freq_label`, layer, depth, time, unit, gis_id, name, then the organic ratio variable `soil1(j)%org_ratio_lr(k)`.

## Source Links

- Writer: [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_carbvar_write_legacy.f90:75-81` (writes `hru_org_ratio_vars` units 8378/8379)
