---
kind: output_family
source_symbols:
- header_lu_change
title: lu_change_out.txt
status: filled
source_hash: 4289c98bc7fdfc09
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`header_lu_change`](../procedures/header_lu_change.md)  
**Also:** [`actions`](../procedures/actions.md)
**File(s):** `lu_change_out.txt` (unit 3612)

## Bottom Line

`lu_change_out.txt` logs land-use / land-management change events triggered by decision tables during the run. The file is opened by `header_lu_change` and rows are written by `actions` when a land-use change is applied.

## What It Writes

One line per land-use-change event. It is an event log rather than a fixed-frequency family.

## Source Links

- Writer: [`header_lu_change`](../procedures/header_lu_change.md)
- Writer: [`actions`](../procedures/actions.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `header_lu_change.f90:8` (opens `lu_change_out.txt`, unit 3612)
- `actions.f90` (writes land-use-change rows)
