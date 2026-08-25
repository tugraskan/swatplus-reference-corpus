---
kind: output_family
source_symbols:
- co2_read
title: co2.out
status: filled
source_hash: 5c3047cbac6a83b3
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`co2_read`](../procedures/co2_read.md)
**File(s):** `co2.out` (unit 2222)

## Bottom Line

`co2.out` logs the atmospheric CO2 concentration used by the simulation. It is written by the CO2 reader as it resolves the annual CO2 series (from `co2_yr.dat` or the basin default).

## What It Writes

A two-column table with the header `YR  CO2(ppm)`: one row per year with the CO2 concentration in ppm applied that year.

## Source Links

- Writer: [`co2_read`](../procedures/co2_read.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `co2_read.f90:35-36` (opens `co2.out`, writes the `YR  CO2(ppm)` header)
