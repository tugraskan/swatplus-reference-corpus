---
kind: output_family
source_symbols:
- soil_carbvar_write_legacy
title: hru_org_trans_vars
status: filled
source_hash: 644bbb94b1dcb7db
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md)
**File(s):** `hru_org_trans_vars.txt` (unit 8380), `hru_org_trans_vars.csv` (unit 8381)

## Bottom Line

`hru_org_trans_vars` is a legacy per-layer organic-carbon transformation-variable file, reporting `soil1%org_tran_lr` by layer. (Legacy carbon output — removed in rev 63.)

## What It Writes

Per HRU per output period, per layer: `freq_label`, layer, depth, time, unit, gis_id, name, then the organic transformation variable `soil1(j)%org_tran_lr(k)`.

## Source Links

- Writer: [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_carbvar_write_legacy.f90:84-92` (writes `hru_org_trans_vars` units 8380/8381)
