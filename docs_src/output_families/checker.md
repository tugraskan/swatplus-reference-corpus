---
kind: output_family
source_symbols:
- proc_hru
title: checker.out
status: filled
source_hash: 7f522d5f677bc93e
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`proc_hru`](../procedures/proc_hru.md)
**File(s):** `checker.out` (unit 4000, record length 1200)

## Bottom Line

`checker.out` is an HRU setup/consistency check file. It is opened during HRU processing and, per the source comment, always prints (it is not gated by a print flag).

## What It Writes

Diagnostic check output written during HRU initialization/processing. See the writer for the exact fields; it is a setup log rather than a time-series family.

## Source Links

- Writer: [`proc_hru`](../procedures/proc_hru.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `proc_hru.f90:56-57` (opens `checker.out`, unit 4000)
