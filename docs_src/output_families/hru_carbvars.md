---
kind: output_family
source_symbols:
- soil_carbvar_write_legacy
title: hru_carbvars
status: filled
source_hash: 644bbb94b1dcb7db
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md)
**File(s):** `hru_carbvars.txt` (unit 8374), `hru_carbvars.csv` (unit 8375)

## Bottom Line

`hru_carbvars` is a legacy per-layer soil-carbon variables file. (Legacy carbon output — the source notes it will be removed in revision 63.)

## What It Writes

Per HRU per output period, per layer: `freq_label`, layer, depth, time, unit, gis_id, name, then the per-layer soil carbon variables. Frequency from the writer's `out_freq`.

## Source Links

- Writer: [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_carbvar_write_legacy.f90:51-56` (writes `hru_carbvars` units 8374/8375)
