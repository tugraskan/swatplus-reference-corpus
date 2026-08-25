---
kind: procedure
symbol: cn2_init
title: cn2_init
status: filled
source_hash: 761e4e2b0142b833
version_label: SWAT+ 62.0.0
args:
  j: '`j` is the HRU index. It selects which `hru(j)` record to read for the land-use management
    pointer and soil pointer, and it is also the index whose `cn2(j)` value is updated.'
locals:
  icn: '`icn` is the curve-number table index selected from `lum_str(ilum)%cn_lu`. It starts
    at 0 and is set to the land-use-specific curve-number group used to choose one of the
    four hydrologic-group values in `cn(icn)%cn`.'
  isol: '`isol` is the soil-table index for the current HRU. It starts at 0 and is set from
    `hru(j)%dbs%soil`, then used to read `sol(isol)%s%hydgrp` so the routine can choose the
    correct hydrologic soil group case.'
  ilum: '`ilum` is the land-use-management index for the current HRU. It starts at 0 and is
    set from `hru(j)%land_use_mgt`, then used to fetch the land-use curve-number group from
    `lum_str(ilum)%cn_lu`.'
uses:
  hru_module: The HRU module supplies the per-HRU pointers that determine both lookup keys
    and the destination state. `hru(j)%land_use_mgt` identifies which land-use group to use,
    `hru(j)%dbs%soil` identifies which soil record to inspect, and `cn2` is the shared HRU
    curve-number array updated by this routine.
  soil_module: The soil module matters because the hydrologic soil group controls which of
    the four curve-number values is selected. `sol(isol)%s%hydgrp` is the soil-group label
    that drives the A/B/C/D branch selection.
  maximum_data_module: The maximum-data module is the source of the curve-number lookup table
    used by this procedure. Its `cn` table holds the four hydrologic-group curve numbers for
    each land-use curve-number class, and `cn2_init` reads from that table after choosing
    `icn`.
  landuse_data_module: The land-use data module supplies the mapping from land-use management
    to curve-number class. `lum_str(ilum)%cn_lu` selects which row of the curve-number table
    applies to the current HRU.
---

<!-- facts:header -->

Initializes an HRU’s curve number state from its land-use and soil-group lookups.

## Bottom Line

cn2_init assigns each HRU's base SCS curve number from the HRU's land-use management group and the soil hydrologic group. It picks the appropriate curve-number table entry for hydrologic groups A through D, stores that value in cn2(j), and then passes it to curno to finish deriving the runoff-related curve-number state.

This routine matters because later runoff and hydrologic calculations depend on cn2 being set consistently for every HRU. It is used during HRU setup and after land-use changes so the model can refresh curve-number behavior for the current land-use/soil combination.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU initialization and also after land-use changes. `actions` prepares the HRU's land-use and soil pointers before calling it, and `cn2_init_all` calls it once for every HRU during bulk initialization. Its result, `cn2(j)`, is then used by later runoff and curve-number calculations through `curno` and the downstream hydrologic routines that rely on the HRU curve-number state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read the HRU's land-use and soil pointers. | The routine copies `hru(j)%land_use_mgt` into `ilum` and `hru(j)%dbs%soil` into `isol`, so the current HRU's land-use management and soil database entries can be used for the lookup. |
| 2. Map land-use management to a curve-number class. | The routine sets `icn = lum_str(ilum)%cn_lu`, selecting the curve-number table row associated with the current land-use management group. |
| 3. Branch on the soil hydrologic group. | The routine examines `sol(isol)%s%hydgrp` to determine whether the soil group is A, B, C, or D. |
| 4. Use the A-group curve number when hydgrp is A. | For hydrologic soil group A, the routine assigns `cn2(j) = cn(icn)%cn(1)`. |
| 5. Use the B-group curve number when hydgrp is B. | For hydrologic soil group B, the routine assigns `cn2(j) = cn(icn)%cn(2)`. |
| 6. Use the C-group curve number when hydgrp is C. | For hydrologic soil group C, the routine assigns `cn2(j) = cn(icn)%cn(3)`. |
| 7. Use the D-group curve number when hydgrp is D. | For hydrologic soil group D, the routine assigns `cn2(j) = cn(icn)%cn(4)`. |
| 8. Derive the rest of the curve-number state. | The routine calls `curno(cn2(j), j)` so the newly selected base curve number can be converted into the derived runoff-related curve-number state for this HRU. |
| 9. Exit the subroutine. | The routine returns after the HRU curve-number state has been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, cn2` | `hru(j)%land_use_mgt, hru(j)%dbs%soil` |
| [sym:soil_module] | `sol` | `sol(isol)%s%hydgrp` |
| [sym:maximum_data_module] | `cn` | `cn(icn)%cn(1), cn(icn)%cn(2), cn(icn)%cn(3), cn(icn)%cn(4)` |
| [sym:landuse_data_module] | `lum_str, cn` | `lum_str(ilum)%cn_lu` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cn2(j)` | When the current HRU's soil hydrologic group is A, B, C, or D after the land-use-to-table mapping is resolved. | The routine updates `cn2(j)` to the base curve number for the current HRU's land-use class and soil hydrologic group. That value is then refined by `curno` so later runoff calculations use the correct HRU curve-number state. |

## File I/O

<!-- facts:io -->


## Lineage

`cn2_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cn2_init.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cn2_init' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
