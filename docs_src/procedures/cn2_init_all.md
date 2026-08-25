---
kind: procedure
symbol: cn2_init_all
title: cn2_init_all
status: filled
source_hash: 1365ae9a33fc6dcb
version_label: SWAT+ 62.0.0
locals:
  j: Loop counter for HRU indices; initialized to 0 and then used to visit each HRU from 1
    through sp_ob%hru.
uses:
  soil_module: This routine imports soil_module as part of the curve-number initialization
    context, so cn2_init can use soil-related state while initializing each HRU.
  maximum_data_module: This routine imports maximum_data_module as part of the curve-number
    initialization context, so cn2_init can use model-wide maximum data needed during HRU
    setup.
  landuse_data_module: This routine imports landuse_data_module as part of the curve-number
    initialization context, so cn2_init can use land-use state while initializing each HRU.
  hydrograph_module: cn2_init_all uses the total HRU count from sp_ob%hru to determine how
    many HRUs to initialize.
---

<!-- facts:header -->

Initializes curve-number state for every HRU.

## Bottom Line

cn2_init_all loops over every HRU and calls cn2_init for each one. Its job is to make sure each HRU's curve-number state is initialized before later hydrologic processing runs.

It depends on the total HRU count in sp_ob%hru and is invoked from proc_hru after soils, structures, and plants have already been initialized. That placement ensures the curve-number setup sees the HRU inventory that the rest of the HRU workflow will use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

proc_hru calls cn2_init_all after soils_init, structure_init, and plant_all_init. That means the HRU inventory and related lookup state are already in place before curve-number initialization, and later hydrologic routines such as hydro_init depend on the initialized HRU state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop | Iterate over every HRU index from 1 to the total HRU count in sp_ob%hru. |
| 2. call | Call cn2_init for the current HRU index so that HRU's curve-number state is initialized. |
| 3. return | Return after all HRUs have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `module state imported by use soil_module` | `[]` |
| [sym:maximum_data_module] | `module state imported by use maximum_data_module` | `[]` |
| [sym:landuse_data_module] | `module state imported by use landuse_data_module` | `[]` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cn2(j)` | for each HRU j | cn2_init_all triggers cn2_init for every HRU, which initializes that HRU's curve-number state. |

## File I/O

<!-- facts:io -->


## Lineage

`cn2_init_all.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cn2_init_all.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cn2_init_all' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
