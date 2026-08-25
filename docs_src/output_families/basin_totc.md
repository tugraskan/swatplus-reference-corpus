---
kind: output_family
source_symbols:
- header_snutc
title: basin_totc.txt
status: filled
source_hash: e406539048bba151
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`header_snutc`](../procedures/header_snutc.md)
**File(s):** `basin_totc.txt` (unit 2613)

## Bottom Line

`basin_totc.txt` is opened by `header_snutc`. No data-writing statement targeting unit 2613 was found in the scanned source, so as built the file contains only its opening header rows — an inactive/legacy basin total-carbon output.

## What It Writes

Opening header rows only; no data records are written to unit 2613 in the current source.

## Source Links

- Writer: [`header_snutc`](../procedures/header_snutc.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `header_snutc.f90:27` (opens unit 2613)
