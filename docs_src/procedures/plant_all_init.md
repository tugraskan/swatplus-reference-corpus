---
kind: procedure
symbol: plant_all_init
title: plant_all_init
status: filled
source_hash: f6286477d756bbad
version_label: SWAT+ 62.0.0
locals:
  iihru: 'Loop index over HRUs; used first to initialize each HRU and later to scan each HRU''s
    plant community. Initial value: `0`.'
  ipl: 'Loop index over plants within an HRU community. Initial value: `0`.'
  iplt: 'Temporary loop index over the current basin plant list while checking whether a plant
    name is already present. Initial value: `0`.'
  ipl_bsn: 'Loop index over basin-wide unique plants and their basin yield records. Initial
    value: `0`.'
  num_plts_cur: 'Snapshot of the current basin plant count used to bound the duplicate-check
    loop while the list may grow. Initial value: `0`.'
uses:
  plant_module: Provides the plant community definitions, basin plant counter, basin crop-yield
    arrays, and per-plant basin numbering that this routine initializes and fills.
  plant_data_module: Holds the basin-wide list of unique plant names that this routine builds
    from the HRU communities.
  hru_module: Supplies the HRU database pointers that are copied into the module-level land-use
    and soil selectors before plant initialization.
  hydrograph_module: Provides the number of HRUs to loop over during initialization and basin
    plant collection.
  maximum_data_module: Supplies the maximum plant count used to allocate the basin plant and
    yield arrays.
---

<!-- facts:header -->

Initializes plant-related basin arrays and HRU plant pointers for the current run.

## Bottom Line

plant_all_init allocates the basin-level plant yield arrays, initializes each HRU's plant runtime state by setting the land-use and soil database pointers, and calls plant_init for each HRU to finish plant setup.

It then scans all HRU plant communities to build the unique basin plant list, zeroes the basin crop-yield accumulators, and assigns each HRU plant a basin plant number so later output and accounting can refer to a consistent basin-wide plant index.

## Arguments

<!-- facts:arguments -->

## Where It Fits

proc_hru calls plant_all_init after soils_init and structure_init, before cn2_init_all and hydro_init. This is the basin/HRU plant setup step that prepares plant community pointers, basin plant lists, and basin crop-yield storage for later initialization and output.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Allocate basin plant arrays | Allocate the basin plant-name and basin crop-yield arrays using the maximum plant count from db_mx%plantparm. |
| 2. Initialize each HRU | Loop over all HRUs, copy the HRU land-use and soil database pointers into ilu and isol, and call plant_init with a zero flag to initialize plant state for that HRU. |
| 3. Build basin plant list | Scan every HRU plant community, add each new plant name to plts_bsn, and increment basin_plants only when a plant name has not already been recorded. |
| 4. Zero basin yield records | Initialize each basin crop-yield record and harvested-area record to the zero template bsn_crop_yld_z for every basin plant. |
| 5. Assign basin plant numbers | Loop over all HRU plants again and match each plant name against the basin plant list so the corresponding plant status record gets its basin plant number in pcom(iihru)%plcur(ipl)%bsn_num. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_module] | `pcom, bsn_crop_yld, bsn_crop_yld_aa, basin_plants, bsn_crop_yld_z` | `pcom(iihru)%npl, pcom(iihru)%pl(ipl), pcom(iihru)%plcur(ipl)%bsn_num` |
| [sym:plant_data_module] | `plts_bsn` |  |
| [sym:hru_module] | `hru, isol, ilu` | `hru(iihru)%dbs%land_use_mgt, hru(iihru)%dbs%soil` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantparm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ilu` | On entry | Set to the current HRU's land_use_mgt database index before calling plant_init. |
| `isol` | On entry | Set to the current HRU's soil database index before calling plant_init. |
| `plts_bsn(1)` | When basin_plants is 0 | Stores the first plant name encountered in the basin-wide unique plant list. |
| `basin_plants` | When a new plant name is found | Incremented after adding a previously unseen plant name to plts_bsn. |
| `plts_bsn(iplt+1)` | When a new plant name is found | Stores the next unique plant name after the current basin plant list has been scanned without a match. |
| `bsn_crop_yld(ipl_bsn)` | For each basin plant | Reset to the zero basin crop-yield template before basin yield accounting begins. |
| `bsn_crop_yld_aa(ipl_bsn)` | For each basin plant | Reset to the zero basin crop-yield template for annual-average harvested-area accounting. |
| `pcom(iihru)%plcur(ipl)%bsn_num` | When an HRU plant matches a basin plant name | Assigned the basin plant index corresponding to the matching plant name. |

## File I/O

<!-- facts:io -->


## Lineage

`plant_all_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `plant_all_init.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'plant_all_init' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
