---
kind: output_family
source_symbols:
- soil_nutcarb_write_legacy
title: hru_seq_lyr
status: filled
source_hash: a54e37e3bdd3f701
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
**File(s):** `hru_seq_lyr.txt` (unit 8358), `hru_seq_lyr.csv` (unit 8359)

## Bottom Line

`hru_seq_lyr` is a legacy per-layer sequestered-soil-carbon file, with the 300 mm sequestered sum. The header (with layer depths) is written once at file open. (Legacy carbon output — removed in rev 63.)

## What It Writes

Per HRU per output period: `freq_label`, time, unit, object type, name, then sequestered carbon by layer and the `Seq_300_sum`. Frequency from the writer's `out_freq`.

## Source Links

- Writer: [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_nutcarb_write_legacy.f90:240-278` (writes `hru_seq_lyr` units 8358/8359)
