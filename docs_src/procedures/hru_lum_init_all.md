---
kind: procedure
symbol: hru_lum_init_all
title: hru_lum_init_all
status: filled
source_hash: e10b57a75e9567ee
version_label: SWAT+ 62.0.0
locals:
  iihru: '`iihru` is the loop index for HRU number during initialization. It starts at 0,
    then counts from 1 through `sp_ob%hru` to process each HRU in turn.'
uses:
  hru_module: '`hru_module` provides the shared HRU array that this routine updates. `hru(iihru)%land_use_mgt`
    is the active land-use-management selection for each HRU, and `hru(iihru)%dbs%land_use_mgt`
    supplies the database default that gets copied into that active field before detailed
    initialization.'
  hydrograph_module: '`hydrograph_module` supplies `sp_ob%hru`, the number of HRUs to initialize.
    Without that count, this routine would not know how many entries in `hru` to process.'
---

<!-- facts:header -->

Initializes land-use management settings for every HRU. It copies each HRU's default land-use management pointer from the database and then delegates per-HRU setup to `hru_lum_init`.

## Bottom Line

`hru_lum_init_all` is a simple driver routine for HRU land-use initialization. It loops over every HRU currently defined in `sp_ob%hru`, sets each HRU's active land-use-management index from its database default, and calls `hru_lum_init` to finish the detailed setup for that HRU.

This matters because later HRU processing expects each HRU to have a valid `land_use_mgt` selection before land-use-dependent initialization and management logic runs.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU setup inside `proc_hru`, after `hru_allo`, `hru_read`, and `hrudb_init` have allocated and populated HRU data and database pointers. Its results feed later HRU initialization and setup steps such as `topohyd_init`, `hru_output_allo`, and subsequent management-related processing that relies on each HRU's land-use assignment.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop over HRUs | Iterate through every HRU index from 1 to `sp_ob%hru`, so each spatial HRU gets land-use initialization. |
| 2. set active land-use management | Copy the default land-use-management pointer from the HRU database record into the HRU's active `land_use_mgt` field. |
| 3. initialize one HRU | Call `hru_lum_init` for the current HRU to complete land-use-specific initialization using the selected management code. |
| 4. finish | End the loop, return to the caller, and complete the all-HRU land-use initialization pass. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` | `hru(iihru)%land_use_mgt, hru(iihru)%dbs%land_use_mgt` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(iihru)%land_use_mgt` | For each HRU index `iihru` from 1 to `sp_ob%hru`. | `hru(iihru)%land_use_mgt` is assigned the database default land-use-management index before per-HRU initialization runs, ensuring each HRU starts from its configured land-use selection. |

## File I/O

<!-- facts:io -->


## Lineage

`hru_lum_init_all.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_lum_init_all.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_lum_init_all' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
