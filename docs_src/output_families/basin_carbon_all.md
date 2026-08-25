---
kind: output_family
source_symbols:
- soil_nutcarb_write_legacy
title: basin_carbon_all.txt
status: filled
source_hash: a54e37e3bdd3f701
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
**File(s):** `basin_carbon_all.txt` (unit 8366)

## Bottom Line

`basin_carbon_all.txt` is a legacy basin-level carbon summary. It reports the basin totals of soil, plant, and residue organic carbon. (Legacy carbon output — the source notes it will be removed in revision 63.)

## What It Writes

One row: `time%day`, `time%yrc`, a `basin` label, then basin organic carbon totals for soil (`bsn_org_soil%c`), plants (`bsn_org_pl%c`), and residue (`bsn_org_rsd%c`).

## Source Links

- Writer: [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `soil_nutcarb_write_legacy.f90:413` (writes unit 8366)
