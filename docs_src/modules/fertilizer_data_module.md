---
kind: module
symbol: fertilizer_data_module
title: fertilizer_data_module
status: filled
source_hash: 765e80ec9fe5acb4
version_label: SWAT+ 62.0.0
variables:
  fertdb: Loaded by `fert_parm_read` from `in_parmdb%fert_frt`; run-wide fertilizer composition
    table.
  manure_db: Loaded by `manure_parm_read` from `manure.frt`; visible type currently stores
    only `manurenm`.
type_components:
  fertilizer_db:
    fertnm: Fertilizer name used for name-to-id crosswalks.
    fminn: kg minN/kg frt; fraction of fertilizer that is mineral N (NO3 + NH3).
    fminp: kg minP/kg frt; fraction of fertilizer that is mineral phosphorus.
    forgn: kg orgN/kg frt; fraction of fertilizer that is organic nitrogen.
    forgp: kg orgP/kg frt; fraction of fertilizer that is organic phosphorus.
    fnh3n: kg NH3-N/kg N; fraction of mineral N content that is NH3/NH4.
type_summaries:
  fertilizer_db: Record layout for one row of `fertilizer.frt`.
---

<!-- facts:header -->

Central storage for fertilizer composition records. This module declares the public derived types and allocatable database arrays. Separate reader routines populate those arrays during startup, and later routines use the resulting ids and fractions.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module owns data declarations, not read logic. Startup order still matters because later management and decision-table readers assume `fertdb` has already been loaded.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:fert_parm_read] | `in_parmdb%fert_frt` | `fertdb(0:imax)` | Counts records, allocates index-zero placeholder, reads records directly into the derived type, sets `db_mx%fertparm`. |
| [sym:manure_parm_read] | `manure.frt` | `manure_db(0:imax)` | Same count/allocate/read pattern, but path is hard-coded. |

## Key Consumers

Module pages should keep the FORD-style used-by reference, with SWAT+ grouping added only as context.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:read_mgtops] | fertdb(idb)%fertnm | Maps scheduled `fert` and `manu` names to `op1` fertilizer ids. |
| [sym:dtbl_lum_read] | fertdb(idb)%fertnm | Maps decision-table `fertilize` and `fert_future` actions to `act_typ` ids. |
| [sym:hru_dtbl_actions_init] | fertdb(idb)%fertnm | Builds future fertilizer records and stores `fertnum`. |
| [sym:mgt_read_grazeops] | fertdb(ifert)%fertnm | Maps grazing manure name to `grazeop_db%manure_id`. |
| [sym:manure_allocation_read] | fertdb(idb)%fertnm | Maps manure source type to `mallo%src%fertdb`. |
| [sym:actions] | mapped `d_tbl%act_typ` id | Calls `pl_fert` or `pl_fert_wet`, which read `fertdb(ifrt)`. |
| [sym:pl_fert] | nutrient composition fields | Updates soil nutrient/carbon pools and fertilizer reporting variables. |
| [sym:pl_fert_wet] | same fields | Updates wetland/paddy water nutrient pools and reporting variables. |
| [sym:pl_manure] | same fields | Applies manure-like material into mineral, humus, manure, and SWAT-C pools. |
| [sym:pl_graze] | fertdb(graze%manure_id) | Applies manure returned during grazing. |
| [sym:salt_fert] | fertdb(ifrt)%fertnm | Uses fertilizer name prefix to classify salt mass as amendment or regular fertilizer. |

## Lineage

`fertilizer_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `452f563` (2026-05-01, "Update to comments to correct units and definitions. Updates to pl_manure equati…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `fertilizer_data_module.f90` are listed.

- `452f563` (2026-05-01) — Update to comments to correct units and definitions. Updates to pl_manure equations to utilize input carbon in manure_om.frt file.
- `561bc28` (2026-04-10) — Add manure application (manu) management operation
- `f8feed6` (2025-10-30) — Minor bug fixes and sinching Jeffs code back up to swatplus/main
- `16e54aa` (2024-07-05) — BB 61.0.1
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The module has no module-level purpose comment.
- `fertdb` is public mutable global state; required startup order should be explicit.
- Sample `fertilizer.frt` includes `pathogens` and `description` columns not represented in `fertilizer_db`.
- `manure_data` stores only `manurenm`; commented fields suggest incomplete or future metadata.
- `cs_fert` imports this module, but the visible path does not directly read `fertdb`.
- `mfrt` is declared in both `fert_parm_read` and `manure_parm_read` but not used in visible source.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
