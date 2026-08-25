---
kind: output_family
source_symbols:
- proc_hru
title: erosion.out
status: filled
source_hash: 7f522d5f677bc93e
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`proc_hru`](../procedures/proc_hru.md)
**File(s):** `erosion.out` (unit 4001, record length 1200)

## Bottom Line

`erosion.out` is the erosion diagnostic output. It is opened during HRU processing with a header (`ero_hdr`) and units row (`ero_hdr_units`) from the erosion module.

## What It Writes

A header row (`ero_hdr`), a units row (`ero_hdr_units`), then erosion output records. See `erosion_module` for the field set.

## Source Links

- Writer: [`proc_hru`](../procedures/proc_hru.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `proc_hru.f90:49-54` (opens `erosion.out`, writes `ero_hdr`/`ero_hdr_units`)
- `erosion_module.f90`
