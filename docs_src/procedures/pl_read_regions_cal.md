---
kind: procedure
symbol: pl_read_regions_cal
title: pl_read_regions_cal
status: filled
source_hash: 3dc6f223bd6c3ae6
version_label: SWAT+ 62.0.0
locals:
  titldum: Header/title line read from `plant_gro.sft` before the region count and data records.
  header: Section header line(s) read from `plant_gro.sft` before the land-use measurement
    block for a region.
  eof: I/O status flag used on each read from unit 107 to detect end-of-file or read failure
    and stop the scan loop.
  i_exist: Logical flag set by `inquire` to show whether the configured `plant_gro.sft` file
    exists.
  imax: Scratch counter initialized to zero here but not used later in the shown routine.
  nspu: Number of spatial units listed for the current plant calibration region; it controls
    whether the routine reads an explicit HRU list or assigns all HRUs to the region.
  mcal: Scratch counter initialized to zero here but not used later in the shown routine.
  mreg: Number of plant calibration regions found in the file; it sizes `plcal` and is stored
    in `db_mx%plcal_reg`.
  i: Loop index over plant calibration regions in `plcal`.
  isp: Loop index used while reading the explicit HRU count list into `elem_cnt`.
  ielem1: Returned total count of defining HRU elements from `define_unit_elements`; it sets
    the allocation size for `plcal(i)%num`.
  ihru: Loop index over the HRU numbers belonging to one calibration region.
  iihru: Actual HRU index retrieved from the region membership list and used to mark the HRU's
    crop calibration region.
  ilum_mx: Temporary copy of the current region's land-use count used to allocate and loop
    over `plcal(i)%lum`.
  ilum: Loop index over the land-use measurement entries within a region.
uses:
  input_file_module: This module provides `in_chg%plant_gro_sft`, the configured file name
    that tells the routine which plant calibration soft-data file to open and read.
  maximum_data_module: This module holds `db_mx%plcal_reg`, the shared maximum-data counter
    updated here so the model records how many plant calibration regions were loaded.
  calibration_data_module: This module defines the `plcal` array that stores each calibration
    region's name, land-use count, HRU membership, total HRU count, and per-land-use measurement
    data populated by this routine.
  hydrograph_module: This module supplies `sp_ob%hru`, the total HRU count used when a region
    has no explicit HRU list and the routine must assign every HRU to that region.
  hru_module: This module provides the `hru` array whose `crop_reg` field is updated so each
    HRU knows which plant calibration region it belongs to during later calibration processing.
---

<!-- facts:header -->

Reads the plant-region soft calibration file and loads plant calibration regions plus their HRU membership and land-use measurements into shared model arrays. The routine also tags matching HRUs with their crop calibration region for later calibration workflows.

## Bottom Line

pl_read_regions_cal opens the configured `plant_gro.sft` file, checks whether it exists, and then scans its region records. For each plant calibration region, it allocates the region structure, records the HRU membership list, and reads any associated land-use measurement data.

Its main job is to populate `plcal` and `db_mx%plcal_reg` so later plant calibration and parameter-processing routines know how many plant calibration regions exist, which HRUs belong to each region, and what soft-calibration measurements are attached to each land-use entry. It also writes the region index back into each matching HRU through `hru%crop_reg`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration-data setup, after `proc_cal` has already started reading calibration inputs and before later plant-parameter and calibration-condition routines need the region definitions. Its results feed the rest of the plant soft-calibration workflow by supplying region membership, land-use measurement structures, and `crop_reg` tags on the HRU records.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Reset local counters. | Initializes the region-count scratch variables to zero before any file processing begins. |
| 2. Check whether the configured input file exists. | Uses `inquire` to test the configured `plant_gro.sft` file and, if it is missing or set to the literal string `null`, allocates a minimal empty `plcal` array instead of reading data. |
| 3. Open the plant calibration file and skip the title, region count, and header lines. | Opens unit 107 on `plant_gro.sft`, reads the title line into `titldum`, the number of regions into `mreg`, and a header line into `header`; then allocates `plcal(mreg)` for the region records. |
| 4. Read each plant calibration region record. | Loops over the declared number of regions and reads each region's name, land-use count, and spatial-unit count. |
| 5. Expand explicit HRU memberships when a region lists spatial units. | If `nspu` is positive, allocates `elem_cnt`, backs up one record, rereads the region line with explicit HRU IDs, calls `define_unit_elements` to build the full HRU membership list, copies `defunit_num` into `plcal(i)%num`, stores the total in `plcal(i)%num_tot`, and tags each referenced HRU's `crop_reg` with the region index. |
| 6. Assign all HRUs to the region when no explicit membership list is provided. | If `nspu` is zero, allocates `plcal(i)%num` to the total HRU count in `sp_ob%hru`, fills it with every HRU number, sets `plcal(i)%num_tot`, and writes the region index to each `hru(ihru)%crop_reg`. |
| 7. Read optional land-use measurement data for the region. | When `plcal(i)%lum_num` is positive, reads a header line, allocates the `lum` array, and reads each land-use measurement entry into `plcal(i)%lum(ilum)%meas`. |
| 8. Save the region count and close the file. | After all regions are processed, stores `mreg` in `db_mx%plcal_reg`, closes unit 107, and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_chg` | `in_chg%plant_gro_sft` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plcal_reg` |
| [sym:calibration_data_module] | `plcal` | `plcal(i)%name, plcal(i)%lum_num, plcal(i)%num(ielem1), plcal(i)%num, plcal(i)%num_tot, plcal(i)%num(ihru), plcal(i)%lum(ilum_mx), plcal(i)%lum(ilum)%meas` |
| [sym:hydrograph_module] | `sp_ob, elem_cnt, defunit_num` | `sp_ob%hru` |
| [sym:hru_module] | `hru` | `hru(iihru)%crop_reg, hru(ihru)%crop_reg` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `plcal(i)%num` | When a region record lists explicit spatial units (`nspu > 0`). | `plcal(i)%num` is allocated to the expanded HRU list returned by `define_unit_elements`, so the region stores the explicit HRU membership numbers that define the plant calibration region. |
| `plcal(i)%num_tot` | When the file has been read enough to know the number of regions, or when the file is absent and `mreg` remains zero. | `plcal(i)%num_tot` is set to the number of HRUs assigned to the current region, either the expanded defining-unit count from `define_unit_elements` or `sp_ob%hru` when all HRUs belong to the region. |
| `hru(iihru)%crop_reg` | When an HRU is included in a region membership list and its index is assigned during the membership loop. | `hru(iihru)%crop_reg` is set to the current region index so each referenced HRU is marked as belonging to that plant calibration region. |
| `plcal(i)%num(ihru)` | When explicit spatial units are provided for the region and `define_unit_elements` returns a membership list. | `plcal(i)%num(ihru)` receives the HRU number from `defunit_num`, giving the region a stored list of the exact HRUs included in the calibration region. |
| `hru(ihru)%crop_reg` | When no explicit spatial-unit list is provided (`nspu == 0`). | `hru(ihru)%crop_reg` is set for every HRU in the model because the region is defined as containing all HRUs. |
| `db_mx%plcal_reg` | After the region-reading loop finishes, including the empty-file path. | `db_mx%plcal_reg` records the total number of plant calibration regions discovered in `plant_gro.sft` so other setup code can size or iterate over plant calibration regions later. |

## File I/O

<!-- facts:io -->


## Lineage

`pl_read_regions_cal.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_read_regions_cal.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'pl_read_regions_cal' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
