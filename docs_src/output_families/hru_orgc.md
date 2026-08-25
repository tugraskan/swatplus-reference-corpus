---
kind: output_family
source_symbols:
- header_snutc
title: hru_orgc.txt
status: filled
source_hash: e406539048bba151
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`header_snutc`](../procedures/header_snutc.md)
**File(s):** `hru_orgc.txt` (unit 2610)

## Bottom Line

`hru_orgc.txt` is opened by `header_snutc`, which writes the title, an `orgc_hdr` column header, and an `orgc_units` units row. No data-writing statement targeting unit 2610 was found in the scanned source, so as built the file contains only the header — an inactive/legacy HRU organic-carbon output.

## What It Writes

Title row, `orgc_hdr` header, and `orgc_units` units row only; no data records are written to unit 2610 in the current source.

## Source Links

- Writer: [`header_snutc`](../procedures/header_snutc.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `header_snutc.f90:11-15` (opens unit 2610, writes header/units)
