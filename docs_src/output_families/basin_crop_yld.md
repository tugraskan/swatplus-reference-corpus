---
kind: output_family
source_symbols:
- header_yield
title: basin_crop_yld
status: filled
source_hash: cf95a415d1fd0ca7
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`header_yield`](../procedures/header_yield.md)  
**Also:** [`time_control`](../procedures/time_control.md)
**File(s):** `basin_crop_yld_yr.txt` (unit 5100), `basin_crop_yld_aa.txt` (unit 5101)

## Bottom Line

`basin_crop_yld` reports basin-aggregated crop yields at the yearly and average-annual frequencies. The files are opened by `header_yield` and the rows are written from `time_control` at year end and simulation end.

## What It Writes

Basin crop-yield summary rows written yearly (`_yr`, unit 5100) and average-annual (`_aa`, unit 5101). See `time_control` for the per-crop field set.

## Source Links

- Writer: [`header_yield`](../procedures/header_yield.md)
- Writer: [`time_control`](../procedures/time_control.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `header_yield.f90:22,26` (opens the `_yr`/`_aa` files)
- `time_control.f90` (writes the yearly/aa rows)
