---
kind: output_family
source_symbols:
- hru_lte_control
title: yield
status: filled
source_hash: cb9f77dfc3af1066
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`hru_lte_control`](../procedures/hru_lte_control.md)
**File(s):** `yield.out` (unit 4700), `yield.csv` (unit 4701)

## Bottom Line

`yield` reports crop yield at harvest for the HRU-LTE (lite) spatial units. One record is written each time an HRU-LTE crop is harvested.

## What It Writes

Per-harvest record: HRU-LTE unit (`isd`), day, year, plant name, leaf area index (`alai`), biomass (`dm`), and yield (`write (4700/4701, …)`).

## Source Links

- Writer: [`hru_lte_control`](../procedures/hru_lte_control.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `hru_lte_control.f90:208-210` (writes `yield.out`/`yield.csv`)
