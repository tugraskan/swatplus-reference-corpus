---
kind: procedure
symbol: proc_hru
title: proc_hru
status: filled
source_hash: 01ecee2482311f70
version_label: SWAT+ 62.0.0
locals:
  j: Loop counter over HRUs; also used to index soil and HRU arrays during initialization
    and checker output.
  ilum: Land-use-management index for the current HRU, taken from `hru(j)%land_use_mgt` and
    used to look up septic structure settings.
uses:
  hydrograph_module: Provides the HRU count that gates the whole routine and the checker output
    header/unit records written to `checker.out`.
  maximum_data_module: Imported by the procedure, but no candidate outside references were
    resolved to this module in the context packet.
  hru_module: Holds the HRU array being allocated, initialized, and written to the checker
    output; the routine reads HRU management and hydrology fields from each HRU record.
  soil_module: Provides the soil profile fields written to the checker output for each HRU.
  constituent_mass_module: Controls whether optional pesticide, pathogen, salt, and generic
    constituent initialization routines are called.
  landuse_data_module: Provides the septic structure pointer checked before soil initialization
    so septic layers can be inserted in the correct soil profile.
  erosion_module: Provides the erosion output header records written to `erosion.out`.
  output_path_module: Imported because the routine calls `open_output_file`, which uses output-path
    resolution from this module.
---

<!-- facts:header -->

Initializes HRU-related databases and output structures for a run. It also writes checker and erosion output headers and per-HRU diagnostic lines.

## Bottom Line

`proc_hru` is the HRU setup routine. When HRUs exist, it allocates and reads HRU data, initializes HRU databases and land-use/topography/hydrology state, applies septic structure parameters before soil initialization, and then initializes soils, structures, plants, curve numbers, hydrology, and optional constituent modules.

It also allocates erosion output storage, opens `erosion.out` and `checker.out`, writes their headers, emits a per-HRU checker line with soil and hydrology parameters, and finally reads routing nutrient input. This routine matters because it prepares the HRU state used by later simulation and output routines.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Runs during HRU setup after spatial HRU counts are known and before the simulation proceeds into routines that need initialized HRU, soil, hydrology, and constituent state. It prepares the HRU database and output files that later model behavior depends on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize HRU setup | If HRUs exist, allocate and read HRU data, initialize HRU databases, land-use management, topography/hydrology, and HRU output storage. |
| 2. Apply septic parameters | Loop over HRUs, look up each HRU's land-use management record, and apply septic structure parameters before soils are initialized. |
| 3. Initialize soils and management | Initialize soils, structural settings, plants, curve numbers, hydrology, and optional pesticide, pathogen, salt, and constituent state. |
| 4. Allocate erosion output | Allocate erosion output storage, open `erosion.out`, and write the basin and erosion header records. |
| 5. Open checker output | Open `checker.out` and write the basin header, checker header, checker units, and the file-name marker on unit 9000. |
| 6. Write checker rows | Loop over HRUs and write one checker line per HRU with soil and hydrology parameters. |
| 7. Read routing nutrients | Read routing nutrient input after HRU setup is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, chk_hdr, chk_unit` | `sp_ob%hru` |
| [sym:hru_module] | `hru` | `hru(j)%land_use_mgt, hru(j)%lumv%usle_p, hru(j)%lumv%usle_ls, hru(j)%hyd%esco, hru(j)%hyd%epco, hru(j)%hyd%cn3_swf, hru(j)%hyd%perco, hru(j)%hyd%latq_co, hru(j)%tiledrain` |
| [sym:soil_module] | `soil` | `soil(j)%snam, soil(j)%hydgrp, soil(j)%zmx, soil(j)%usle_k, soil(j)%sumfc, soil(j)%sumul` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%num_paths, cs_db%num_salts, cs_db%num_cs` |
| [sym:landuse_data_module] | `lum` | `lum(ilum)%septic` |
| [sym:erosion_module] | `ero_hdr, ero_hdr_units` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `HRU arrays and output structures` | sp_ob%hru > 0 | Allocates and initializes HRU-related state, including HRU databases, output arrays, and optional constituent pools. |
| `HRU septic structure parameters` | lum(ilum)%septic /= 'null' | Applies septic structure settings to the current HRU before soil initialization so the septic zone can be represented in the soil profile. |
| `pesticide state` | cs_db%num_pests > 0 | Initializes pesticide pools for HRUs. |
| `pathogen state` | cs_db%num_paths > 0 | Initializes pathogen pools for HRUs. |
| `salt state` | cs_db%num_salts > 0 | Initializes salt pools for HRUs. |
| `generic constituent state` | cs_db%num_cs > 0 | Initializes generic constituent pools for HRUs. |
| `ero_output(sp_ob%hru)` | always after allocation | Allocates erosion output storage for all HRUs. |
| `erosion.out` | always after opening unit 4001 | Writes basin and erosion header records to the erosion output file. |
| `checker.out` | always after opening unit 4000 | Writes basin and checker header records to the checker output file. |
| `checker.out rows` | per HRU loop | Writes one diagnostic line per HRU with soil and hydrology parameters. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_hru.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 10 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_hru.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `29e2d36` (2025-10-29) — Bug fixes and changes related to water allocation
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No resolved lineage commits for this source span.
- `maximum_data_module` and `output_path_module` are imported, but the context packet did not resolve concrete outside references for them.
- The routine writes directly to units 4000, 4001, and 9000; the file names for 4000 and 4001 are established through `open_output_file`, while unit 9000 is written as a marker line.
- `proc_hru` has no extracted documentation comment in the source packet.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
