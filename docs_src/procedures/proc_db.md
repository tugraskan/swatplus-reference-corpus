---
kind: procedure
symbol: proc_db
title: proc_db
status: filled
source_hash: 0320d7a696f09ec8
version_label: SWAT+ 62.0.0
---

<!-- facts:header -->

Initializes the shared SWAT+ database tables used by spatial modules. It reads plant, management, structural-operation, plant-community, and landuse lookup data in a fixed startup sequence.

## Bottom Line

proc_db is the database bootstrap routine for SWAT+. It has no arguments and simply calls a long, ordered set of reader/initializer routines to load the shared parameter tables used by spatial modules and later landuse/management processing.

The routine matters because it establishes the core lookup state before the model can attach plants, management schedules, drainage, septic, conservation practice, and BMP definitions to landuse records. Its work is mostly orchestration: it does not compute new model results itself, but it prepares the database state that downstream routines depend on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model/database startup, before spatial modules and landuse-driven HRU setup need their lookup tables. It is the upstream initializer for the shared plant, management, structural-operation, plant-community, and landuse databases that later routines consume.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load plant databases | Load the shared plant, transplant, tillage, pesticide, fertilizer, manure, urban, pathogen, and septic databases in the documented order. |
| 2. Load management operations | Read the management scheduling and operation tables for irrigation, chemical application, harvest, grazing, sweeping, fire, general management, and puddling. |
| 3. Load structural operation tables | Read the structural operation databases for subsurface drainage, septic systems, grassed waterways, filter strips, user BMPs, and saturated buffers. |
| 4. Load plant communities | Read the plant community database and link each community plant to the master plant database. |
| 5. Load landuse lookup tables | Read the curve-number, conservation-practice, overland roughness, and landuse databases that complete the landuse lookup state. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `shared plant, management, structural-operation, plant-community, and landuse lookup tables` | During startup database initialization | Populates the shared database state by invoking the ordered reader and initializer routines that load the model's core lookup data. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_db.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `561bc28` (2026-04-10, "Add manure application (manu) management operation"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_db.f90` are listed.

- `561bc28` (2026-04-10) — Add manure application (manu) management operation
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `1807dbb` (2025-03-26) — na
- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'proc_db' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
