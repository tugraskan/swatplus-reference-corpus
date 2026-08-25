---
kind: output_family
source_symbols:
- header_mgt
title: mgt_out.txt
status: filled
source_hash: 7d2f7f509307594d
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`header_mgt`](../procedures/header_mgt.md)  
**Also:** [`actions`](../procedures/actions.md)
**File(s):** `mgt_out.txt` (unit 2612)

## Bottom Line

`mgt_out.txt` is the management-operations log. It records scheduled and conditional management operations (planting, tillage, fertilizer, harvest, etc.) as they are applied during the run. The file is opened by `header_mgt` and rows are written by `actions`.

## What It Writes

One line per management operation applied, with the operation context. It is an event log rather than a fixed-frequency family.

## Source Links

- Writer: [`header_mgt`](../procedures/header_mgt.md)
- Writer: [`actions`](../procedures/actions.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `header_mgt.f90:9` (opens `mgt_out.txt`, unit 2612)
- `actions.f90` (writes management-operation rows)
