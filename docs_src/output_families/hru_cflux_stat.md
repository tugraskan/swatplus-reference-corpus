---
kind: output_family
source_symbols:
- soil_nutcarb_write_legacy
title: hru_cflux_stat
status: filled
source_hash: a54e37e3bdd3f701
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
**File(s):** `hru_cflux_stat.txt` (unit 8367), `hru_cflux_stat.csv` (unit 8368)

## Bottom Line

`hru_cflux_stat` is a legacy per-layer carbon/nitrogen flux file (the source describes it as the organic flux pools, made non-cumulative). It reports about 37 flux variables. (Legacy carbon output — removed in rev 63.)

## What It Writes

Per HRU per output period, per layer (a `-1, -1` row denotes the whole-profile total): `freq_label`, layer, depth, time, unit, gis_id, name, then the C and N flux variables. Frequency from the writer's `out_freq`.

## Source Links

- Writer: [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_nutcarb_write_legacy.f90:337-353` (writes `hru_cflux_stat` units 8367/8368)
