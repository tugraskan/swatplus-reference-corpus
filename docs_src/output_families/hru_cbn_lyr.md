---
kind: output_family
source_symbols:
- soil_nutcarb_write_legacy
title: hru_cbn_lyr
status: filled
source_hash: a54e37e3bdd3f701
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
**File(s):** `hru_cbn_lyr.txt` (unit 8348), `hru_cbn_lyr.csv` (unit 8349)

## Bottom Line

`hru_cbn_lyr` is a legacy per-layer soil-carbon file: total soil organic carbon (Mg/ha) by soil layer, plus the 300 mm sequestered-carbon sum. The header (with each layer's depth) is written once at file open. (Legacy carbon output — removed in rev 63.)

## What It Writes

Per HRU per output period: `freq_label`, time (jday/mon/day/yr), unit, object type, name, then total soil carbon by layer and the 300 mm sum. Frequency is chosen by the writer's `out_freq` argument (d/m/y/a).

## Source Links

- Writer: [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_nutcarb_write_legacy.f90:198-236` (writes `hru_cbn_lyr` units 8348/8349)
