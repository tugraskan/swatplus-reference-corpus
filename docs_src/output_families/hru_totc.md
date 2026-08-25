---
kind: output_family
source_symbols:
- header_snutc
title: hru_totc.txt
status: filled
source_hash: e406539048bba151
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`header_snutc`](../procedures/header_snutc.md)
**File(s):** `hru_totc.txt` (unit 2611)

## Bottom Line

`hru_totc.txt` is opened by `header_snutc`, which writes the title, a `totc_hdr` column header, and a `totc_units` units row. No data-writing statement targeting unit 2611 was found in the scanned source, so as built the file contains only the header — an inactive/legacy HRU total-carbon output.

## What It Writes

Title row, `totc_hdr` header, and `totc_units` units row only; no data records are written to unit 2611 in the current source.

## Source Links

- Writer: [`header_snutc`](../procedures/header_snutc.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `header_snutc.f90:19-23` (opens unit 2611, writes header/units)
