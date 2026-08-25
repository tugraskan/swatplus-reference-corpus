---
kind: output_family
source_symbols:
- soil_nutcarb_write_legacy
title: hru_plc_stat
status: filled
source_hash: a54e37e3bdd3f701
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
**File(s):** `hru_plc_stat.txt` (unit 8360), `hru_plc_stat.csv` (unit 8363)

## Bottom Line

`hru_plc_stat` is a legacy HRU-level plant-carbon file (plant/community organic carbon state), reported at the HRU level with no soil-layer breakdown. (Legacy carbon output — removed in rev 63.)

## What It Writes

Per HRU per output period: `freq_label`, time, unit, gis_id, name, then the plant-community organic carbon state values. Frequency from the writer's `out_freq`.

## Source Links

- Writer: [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_nutcarb_write_legacy.f90:323-329` (writes `hru_plc_stat` units 8360/8363)
