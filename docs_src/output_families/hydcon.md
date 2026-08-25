---
kind: output_family
source_symbols:
- hyd_connect_out
title: hydcon
status: filled
source_hash: c83d3639e9718a4a
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`hyd_connect_out`](../procedures/hyd_connect_out.md)
**File(s):** `hydcon.out` (unit 7000), `hydcon.csv` (unit 7001)

## Bottom Line

`hydcon` is the hydrograph-connectivity dump: it reports how the spatial objects are wired together (which object sends which hydrograph to which receiver). It is a topology listing, not a time series.

## What It Writes

Object connection records describing the routing network, written by `hyd_connect_out` to the text file and, when CSV output is enabled, the CSV companion.

## Source Links

- Writer: [`hyd_connect_out`](../procedures/hyd_connect_out.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `hyd_connect_out.f90:10-13` (opens `hydcon.out`/`hydcon.csv`)
