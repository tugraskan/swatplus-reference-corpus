---
kind: procedure
symbol: wet_all_initial
title: wet_all_initial
status: filled
source_hash: c8bbea2d4d183985
version_label: SWAT+ 62.0.0
locals:
  iihru: Loop index for the HRU currently being examined and initialized.
  iprop: Holds the numeric surface-storage database pointer from `hru(iihru)%dbs%surf_stor`;
    in this routine it is assigned but not used in the active test.
uses:
  hru_module: The routine decides whether an HRU has surface storage by inspecting each HRU's
    numeric and character database pointers in `hru`; those values control whether wetland
    initialization runs for that HRU.
  hydrograph_module: The routine needs `sp_ob%hru` to know how many HRUs to scan, and it writes
    to `wet_om_init` while reading `wet` so the hydrograph module carries the initialized
    wetland output state forward for later model use.
---

<!-- facts:header -->

Initializes wetland surface-storage outputs for every HRU that is linked to a wetland surface-storage database entry. It copies each initialized wetland output into the `wet_om_init` archive state.

## Bottom Line

`wet_all_initial` is a driver routine that walks through every HRU in the spatial object list and, for HRUs whose character database field `surf_stor` is not the string `"null"`, invokes `wet_initial` to build the wetland's starting state. After that initialization call, it saves the resulting wetland output state from `wet(iihru)` into `wet_om_init(iihru)`.

This matters because it establishes the baseline wetland/organic-matter initialization for all active surface-storage HRUs before later wetland routing and bookkeeping use those states.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during initial setup of wetland surface-storage states, after `sp_ob%hru` and the HRU database pointers in `hru` have been populated. It relies on those prepared inputs to decide which HRUs need wetland initialization, then calls `wet_initial` to build the wetland state and copies that result into `wet_om_init`; later wetland/hydrology behavior depends on those initialized output states being available.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. scan HRUs | Iterate over every HRU index from 1 through `sp_ob%hru`, so each spatial HRU can be checked for wetland surface-storage initialization. |
| 2. read surface-storage pointer | Load the numeric surface-storage database pointer from `hru(iihru)%dbs%surf_stor` into `iprop`. The commented test shows this was intended as a pointer-based check, but the active code uses the character field instead. |
| 3. test for wetland linkage | Proceed only when `hru(iihru)%dbsc%surf_stor` is not the string `"null"`, meaning the HRU has a defined surface-storage/wetland database association. |
| 4. initialize wetland state | Call `wet_initial` for this HRU so the wetland output state is built from the HRU's wetland database references and starting conditions. |
| 5. archive initialized output | Copy the freshly initialized wetland output from `wet(iihru)` into `wet_om_init(iihru)` so the initial wetland state is preserved for later use. |
| 6. finish loop | Advance to the next HRU until all spatial HRUs have been checked. |
| 7. return | Return to the caller after all eligible HRUs have been initialized and archived. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` | `hru(iihru)%dbs%surf_stor, hru(iihru)%dbsc%surf_stor` |
| [sym:hydrograph_module] | `sp_ob, wet_om_init, wet` | `sp_ob%hru` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet_om_init(iihru)` | When `hru(iihru)%dbsc%surf_stor /= "null"` inside the HRU loop. | `wet_om_init(iihru)` changes only for HRUs that are linked to a surface-storage/wetland database entry. For those HRUs, the routine first calls `wet_initial` to populate `wet(iihru)`, then copies that initialized wetland output into `wet_om_init(iihru)` so the model retains the starting wetland state. |

## File I/O

<!-- facts:io -->


## Lineage

`wet_all_initial.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `wet_all_initial.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `ded9d38` (2025-10-29) — minor change: wetland storage check
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wet_all_initial' has no extracted documentation comment.
- algorithm_steps revised: expanded the loop into explicit read/test/call/copy/return steps to match the visible source lines.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
