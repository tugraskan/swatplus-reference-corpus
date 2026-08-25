---
kind: output_family
source_symbols:
- soil_nutcarb_write_legacy
title: hru_n_p_pool_stat
status: filled
source_hash: a54e37e3bdd3f701
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
**File(s):** `hru_n_p_pool_stat.txt` (unit 8382), `hru_n_p_pool_stat.csv` (unit 8383)

## Bottom Line

`hru_n_p_pool_stat` is a legacy per-layer file reporting the nitrogen and phosphorus content of the soil carbon pools. (Legacy carbon output — removed in rev 63.)

## What It Writes

Per HRU per output period, per layer (a `-1, -1` row denotes the whole-profile total): `freq_label`, layer, depth, time, unit, gis_id, name, then the N and P pool contents. Frequency from the writer's `out_freq`.

## Source Links

- Writer: [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_nutcarb_write_legacy.f90:284-315` (writes `hru_n_p_pool_stat` units 8382/8383)
