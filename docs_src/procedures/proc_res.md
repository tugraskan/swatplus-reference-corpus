---
kind: procedure
symbol: proc_res
title: proc_res
status: filled
source_hash: 9894df006711a28c
version_label: SWAT+ 62.0.0
uses:
  hydrograph_module: The routine checks `sp_ob%res` from `hydrograph_module` to decide whether
    any reservoir objects exist at all. That count controls whether reservoir arrays are allocated
    and whether reservoir definitions and initial conditions are loaded.
---

<!-- facts:header -->

Initializes reservoir processing by reading reservoir-related input databases, allocating reservoir structures, and loading reservoir object definitions and starting conditions.

## Bottom Line

`proc_res` is the reservoir setup routine. It pulls in the reservoir hydrology, sediment, nutrient, initial-condition, salt, constituent, and condition-table databases, then uses the configured reservoir count to allocate reservoir objects and read the project’s reservoir definitions.

Its job is to prepare all reservoir state needed before simulation starts. After it runs, later reservoir routing and water-quality code can rely on `res_ob`, `res_dat`, `res_hyd`, `res_prm`, `res_init`, and related lookup data being populated.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_res` runs during reservoir initialization, after the reservoir input readers it calls have prepared the shared database state and before daily reservoir simulation begins. `res_read_hyd`, `res_read_sed`, `res_read_nut`, `res_read_init`, `res_read_saltdb`, `res_read_csdb`, and `res_read_conds` prepare the shared reservoir lookup tables; then, if `sp_ob%res > 0`, `res_allo`, `res_objects`, `res_read`, `res_read_salt_cs`, and `res_initial` build the reservoir object arrays and load the project’s actual reservoir definitions and starting state that later reservoir routing and quality calculations depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. call | Read the reservoir hydrology database into shared state so reservoir hydrologic properties are available for later setup. |
| 2. call | Read the reservoir sediment database so sediment parameters are available for reservoir initialization and later settling calculations. |
| 3. call | Read the reservoir nutrient database and prepare nutrient-process parameters for later reservoir water-quality simulation. |
| 4. call | Read the reservoir initial-condition file so startup reservoir state is available before object initialization. |
| 5. call | Read the reservoir salt database so salt concentration defaults can be linked into reservoir setup. |
| 6. call | Read the reservoir constituent database so constituent lookup data is available for reservoir initialization. |
| 7. call | Read reservoir condition-table definitions into shared state for later release-control or operating-rule evaluation. |
| 8. if | Check whether the project contains any reservoir objects before allocating and populating reservoir-specific arrays. |
| 9. call | Allocate reservoir arrays and storage now that the code knows reservoirs exist. |
| 10. call | Assign reservoir object numbers and property indices to the compact reservoir object list. |
| 11. call | Read the reservoir definition file and resolve each reservoir’s database references and operating settings. |
| 12. call | Resolve reservoir salt and constituent names to numeric lookup indices in the reservoir data. |
| 13. call | Compute reservoir initial geometry and starting operating state so later reservoir routing begins from initialized values. |
| 14. return | Finish reservoir setup and return to the caller with shared reservoir state prepared. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%res` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_res.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_res.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'proc_res' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
