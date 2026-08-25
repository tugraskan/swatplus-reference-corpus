---
kind: output_family
source_symbols:
- soil_nutcarb_write_legacy
title: hru_begsim_soil_prop
status: filled
source_hash: a54e37e3bdd3f701
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
**File(s):** `hru_begsim_soil_prop.txt` (unit 8386), `hru_begsim_soil_prop.csv` (unit 8387)

## Bottom Line

`hru_begsim_soil_prop` is a legacy one-time snapshot of soil physical properties by layer, taken at the start of the simulation (`freq_label = begsim`). (Legacy carbon output — removed in rev 63.)

## What It Writes

Per HRU, per layer: the `begsim` label, soil name, layer, depth, time, unit, gis_id, name, then the soil physical properties. Written once at simulation start.

## Source Links

- Writer: [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_nutcarb_write_legacy.f90:82-92` (writes `hru_begsim_soil_prop` units 8386/8387)
