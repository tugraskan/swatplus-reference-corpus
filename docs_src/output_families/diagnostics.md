---
kind: output_family
source_symbols:
- carbon_bsn_read
title: diagnostics.out
status: filled
source_hash: 62ee54373bdf61f2
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`carbon_bsn_read`](../procedures/carbon_bsn_read.md)
**File(s):** `diagnostics.out` (unit 9001, record length 8000)

## Bottom Line

`diagnostics.out` is the model's global diagnostic and warning log. Unit 9001 is opened once early in the run and then written to from routines across the whole code base whenever a non-fatal problem is detected — a missing or `null` input file, a row with the wrong number of columns, an unrecognized column header, and similar input-quality issues.

## What It Writes

One free-form warning/diagnostic line per issue, written by many routines (e.g. the `table_reader` input helpers in `utils.f90`) with `write(9001, …)`. It is a log, not a per-record table; there is no shared column layout.

## Source Links

- Writer: [`carbon_bsn_read`](../procedures/carbon_bsn_read.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `carbon_bsn_read.f90` (opens unit 9001)
- `utils.f90` and many others (write warnings to 9001)
