---
kind: procedure
symbol: structure_init
title: structure_init
status: filled
source_hash: 56220ccc110102d2
version_label: SWAT+ 62.0.0
locals:
  j: 'Loop counter over HRUs; used as the HRU index passed to structure_set_parms. Initial
    value: 0.'
  ilum: 'Holds the land-use-management index for the current HRU, taken from hru(j)%land_use_mgt.
    Initial value: 0.'
uses:
  hydrograph_module: Provides the number of HRUs to iterate over in the initialization loop.
  hru_module: Maps each HRU to the land-use-management record that controls which structural
    practices are initialized.
  landuse_data_module: Supplies the structural practice pointers that determine which parameter
    sets are applied for the current HRU.
---

<!-- facts:header -->

Initializes structural land-management settings for each HRU.

## Bottom Line

structure_init loops over every HRU, finds its land-use-management record, and dispatches any configured structural practices to structure_set_parms. It only acts when the land-use record points to a real tiledrain, filter strip, grassed waterway, or user-defined BMP entry rather than the sentinel value "null".

This routine matters because it wires land-use management definitions into the HRU-specific structural parameter state before later HRU initialization and process routines run.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from proc_hru after soils_init and before plant_all_init, cn2_init_all, and hydro_init. It prepares HRU structural-management parameters so later HRU process routines can use the configured tile drainage, filter strip, grassed waterway, and user-defined BMP settings.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop | Iterate over every HRU and fetch its land-use-management index. |
| 2. if | If the current land-use record defines a tiledrain entry, pass that structure index to structure_set_parms for this HRU. |
| 3. if | If the current land-use record defines a filter-strip entry, apply its parameters to this HRU. |
| 4. if | If the current land-use record defines a grassed-waterway entry, apply its parameters to this HRU. |
| 5. if | If the current land-use record defines a user BMP entry, apply its parameters to this HRU. |
| 6. return | Exit the subroutine after all HRUs have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:hru_module] | `hru` | `hru(j)%land_use_mgt` |
| [sym:landuse_data_module] | `lum` | `lum(ilum)%tiledrain, lum(ilum)%fstrip, lum(ilum)%grassww, lum(ilum)%bmpuser` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `HRU structural-management parameter state via structure_set_parms` | For each HRU whose land-use-management record points to a non-null structural practice | Initializes the HRU's structural land-management settings for tiledrain, filter strip, grassed waterway, and user-defined BMP practices. |

## File I/O

<!-- facts:io -->


## Lineage

`structure_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `structure_init.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'structure_init' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
