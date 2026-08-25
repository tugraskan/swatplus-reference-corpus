---
kind: output_family
source_symbols:
- sd_channel_output
title: channel_sd_subday
status: filled
source_hash: c2ac29014fbb4e0c
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`sd_channel_output`](../procedures/sd_channel_output.md)
**File(s):** `channel_sd_subday.txt` (unit 2508), `channel_sd_subday.csv` (unit 4814)

## Bottom Line

`channel_sd_subday` is the sub-daily routed-channel output. Unlike the standard channel families it reports within-day (sub-daily) time steps, so it is emitted only when sub-daily routing is active.

## What It Writes

Sub-daily channel routing records written by `sd_channel_output` to the text file and, when CSV output is enabled, the CSV companion.

## Source Links

- Writer: [`sd_channel_output`](../procedures/sd_channel_output.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `sd_channel_output.f90:15,21` (opens `channel_sd_subday.txt`/`.csv`)
