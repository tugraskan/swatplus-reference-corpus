---
kind: procedure
symbol: reg_read_elements
title: reg_read_elements
status: filled
source_hash: 3b9d98dcc84f2b48
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from each input file header section and discarded after
    skipping the file's descriptive first record.
  header: Temporary header line read from each input file; used to advance past the file's
    second descriptive line before reading data records.
  eof: I/O status flag for `read` statements; negative values signal end-of-file or read failure
    and stop the current scan loop.
  i_exist: Result of the file-existence inquiry; tells the routine whether the configured
    region definition file is present before attempting to open it.
  imax: Highest record index found while scanning `ls_reg.ele`; used to size `reg_elem` before
    the file is reread.
  mcal: Unused local counter initialized to zero; no source lines later in the routine update
    or reference it.
  mreg: Number of landscape regions read from `ls_reg.def`; drives allocation and per-region
    loops.
  mlug: Number of land-use management groups read from `ls_reg.def`; controls land-use group
    allocation and reads.
  ireg: Loop index for regions; used when allocating and filling per-region arrays and when
    deriving region HRU membership.
  i: General record index used while scanning and rereading region and element lists.
  k: Record key or sequence value read from the input files alongside names, areas, and type
    codes.
  ilum: Loop index over land-use management group names when reading grouped land-use labels
    from `ls_reg.def`.
  nspu: Number of spatial units listed for a region entry in `ls_reg.def`; determines whether
    grouped-unit expansion is needed.
  isp: Loop index over spatial-unit counts and over element records when iterating through
    grouped entries.
  ielem1: Loop index over expanded defining-unit elements and later over region element slots
    when building HRU membership arrays.
  iihru: Inner loop index over HRUs inside a landscape unit during region HRU expansion.
  ihru_tot: Running total of HRUs implied by the current region's element definitions; used
    to size region-level arrays.
  ilsu: Landscape-unit index extracted from `reg_elem%obtypno` when a region element refers
    to an LSU rather than a direct HRU.
uses:
  input_file_module: The file names in `input_file_module` provide the configured paths that
    this routine opens. `in_regs%def_reg` and `in_regs%ele_reg` are the control points that
    decide which two region-definition files are read.
  maximum_data_module: The maxima in `maximum_data_module` are updated here so other code
    knows how many landscape regions, region elements, and land-use groups were loaded. Those
    counts are used to size downstream arrays and to guard later access.
  calibration_data_module: The calibration module holds the shared region, LSU, and element
    structures that this routine populates. Those arrays carry the memberships, areas, and
    object-type codes that later calibration and output routines need to map regions onto
    HRUs and LSU fragments.
  landuse_data_module: The land-use management group container supplies the group-name list
    read from the definition file. `lum_grp%num` and `lum_grp%name` are populated here so
    the region file's land-use group header can be represented in shared state.
  hydrograph_module: The hydrograph module provides the spatial-object count for HRUs and
    the reusable `elem_cnt`/`defunit_num` bookkeeping used when expanding grouped region entries.
    That expansion is what turns a compact region definition into explicit HRU membership
    IDs.
  hru_module: The HRU table supplies the per-HRU area used when a region element is a direct
    HRU entry. `hru(ihru)%area_ha` is copied into `region(ireg)%hru_ha` so region summaries
    reflect the actual HRU areas.
  output_landscape_module: The landscape output arrays are dimensioned by region and land-use
    group here so later accumulated water-balance, nutrient, loss, and plant-weather reporting
    has storage for each regional land-use bin.
---

<!-- facts:header -->

Reads region and landscape-region element definitions from `ls_reg.def` and `ls_reg.ele`, then builds the in-memory arrays needed for landscape calibration and regional output. It also expands grouped element lists into HRU/LSU memberships and stores region-wide HRU areas.

## Bottom Line

`reg_read_elements` is a setup routine for landscape-region bookkeeping. It opens the configured region definition files, scans them to determine how many regions, land-use groups, and region elements exist, allocates the corresponding arrays, and fills shared calibration/output state such as `lsu_reg`, `region`, and `reg_elem`.

The routine matters because later landscape calibration and output code needs these memberships and counts to map region definitions onto actual HRUs and LSU elements. It uses `define_unit_elements` to expand grouped element counts into explicit element numbers, then derives the per-region HRU numbering and area summaries from the loaded definitions.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model setup after the region-definition files have been configured in `in_regs`. Its results feed landscape calibration, region bookkeeping, and regional output initialization, because later code depends on `lsu_reg`, `region`, and `reg_elem` being populated with explicit memberships and areas.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether region input files should be read | The routine inquires about `in_regs%def_reg` and only enters the read logic if the file exists or the configured name is not the sentinel `null` value. |
| 2. Open `ls_reg.def` and read the file-level counts | It opens the region-definition file, skips the title line, and reads `mreg` and `mlug`, which control later allocations and loops. |
| 3. Allocate region-level output and bookkeeping arrays | It allocates the LSU/region containers and the regional output arrays for water balance, nutrient balance, losses, and plant-weather summaries, then stores `mlug` in `db_mx%landuse`. |
| 4. Read land-use group names and region header data | For nonzero land-use groups, it backs up and rereads the file to populate `lum_grp`, then skips the next header line before processing region records. |
| 5. Allocate per-region land-use summary arrays | When regions are present, it allocates per-region land-use totals and the land-use output arrays for each region index. |
| 6. Read each LSU region record and expand memberships | It stores the region count in `db_mx%lsu_reg`, reads each LSU record, and either expands grouped spatial units through `define_unit_elements` or assigns all HRUs directly when `nspu` is zero. |
| 7. Open `ls_reg.ele` and find the maximum element index | It opens the element-definition file, skips its header lines, scans the element indices to find `imax`, and allocates `reg_elem(imax)`. |
| 8. Rewind and load the detailed element records | It rewinds the element file, rereads the header, stores `imax` in `db_mx%reg_elem`, and fills each `reg_elem(i)` record with the element metadata. |
| 9. Count HRUs implied by the region elements | For each region, it traverses the loaded element definitions and sums the HRUs contributed by direct HRU elements and by LSU elements. |
| 10. Allocate region HRU arrays and map elements to HRUs | It allocates `region(ireg)%num` and `region(ireg)%hru_ha`, then fills them by walking the region elements and copying HRU numbers and areas from the HRU and LSU state. |
| 11. Close the element file and return | It closes unit 107 for `ls_reg.ele` and exits the subroutine after the region and element state has been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_regs` | `in_regs%def_reg, in_regs%ele_reg` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%landuse, db_mx%lsu_reg, db_mx%reg_elem` |
| [sym:calibration_data_module] | `region, lsu_reg, reg_elem, lsu_out, lsu_elem` | `region(ireg)%lumc(mlug), region(ireg)%lum_ha_tot(mlug), region(ireg)%lum_num_tot(mlug), region(ireg)%lum_ha_tot, region(ireg)%lum_num_tot, lsu_reg(i)%name, lsu_reg(i)%area_ha, lsu_reg(i)%num(ielem1), lsu_reg(i)%num, lsu_reg(i)%num_tot, lsu_reg(i)%num(ihru), reg_elem(i)%name, reg_elem(i)%ha, reg_elem(i)%obtyp, reg_elem(i)%obtypno, reg_elem(ielem1)%obtyp, reg_elem(ielem1)%obtypno, lsu_out(ilsu)%num_tot, region(ireg)%num_tot, region(ireg)%num(ihru_tot), region(ireg)%hru_ha(ihru_tot), reg_elem(ireg)%obtyp, region(ireg)%num(ihru), region(ireg)%hru_ha(ihru), lsu_elem(iihru)%obtypno, lsu_elem(iihru)%ru_frac, lsu_out(ilsu)%area_ha` |
| [sym:landuse_data_module] | `lum_grp, lum` | `lum_grp%name(mlug), lum_grp%num, lum_grp%name(ilum)` |
| [sym:hydrograph_module] | `sp_ob, elem_cnt` | `sp_ob%hru` |
| [sym:hru_module] | `hru` | `hru(ihru)%area_ha` |
| [sym:output_landscape_module] | `rwb_a, rnb_a, rls_a, rpw_a, rwb_d, rwb_m, rwb_y, rnb_d, rnb_m, rnb_y, rls_d, rls_m, rls_y, rpw_d, rpw_m, rpw_y` | `rwb_a(ireg)%lum(mlug), rnb_a(ireg)%lum(mlug), rls_a(ireg)%lum(mlug), rpw_a(ireg)%lum(mlug)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%landuse` | When `ls_reg.def` is successfully read and the file's `mlug` value is available. | `db_mx%landuse` is set to the number of land-use management groups so later code can size land-use related regional output arrays and loops. |
| `region(ireg)%lum_ha_tot` | When `mreg > 0` and the routine allocates per-region land-use totals. | `region(ireg)%lum_ha_tot` is created and initialized to zero to hold accumulated land-use area totals for each region. |
| `region(ireg)%lum_num_tot` | When `mreg > 0` and the routine allocates per-region land-use counts. | `region(ireg)%lum_num_tot` is created and initialized to zero to hold the number of HRUs or elements contributing to each land-use group in the region. |
| `db_mx%lsu_reg` | After the region-count line is read from `ls_reg.def`. | `db_mx%lsu_reg` is set to the number of landscape-region entries so downstream arrays know how many LSU-region records exist. |
| `lsu_reg(i)%num` | When a region record has `nspu > 0` and `define_unit_elements` returns a populated `defunit_num` list. | `lsu_reg(i)%num` receives the expanded defining-unit element numbers for that region's grouped spatial-unit definition. |
| `lsu_reg(i)%num_tot` | When a region record has `nspu > 0` or when all HRUs are assigned directly. | `lsu_reg(i)%num_tot` is set to the number of explicit element numbers that belong to the region. |
| `lsu_reg(i)%num(ihru)` | When a region record has `nspu > 0` and `lsu_reg(i)%num` is allocated. | `lsu_reg(i)%num(ihru)` stores each explicit HRU or defining-unit element number copied from `defunit_num`. |
| `db_mx%reg_elem` | After `ls_reg.ele` has been scanned and `imax` is known. | `db_mx%reg_elem` is set to the maximum region-element index so the `reg_elem` array size is recorded for later use. |
| `ihru` | When a region element refers to an LSU in the first pass over the region definition. | `ihru_tot` accumulates the total number of HRUs implied by all elements in the current region and is later used to dimension region HRU arrays. |
| `region(ireg)%num_tot` | After the first pass over region elements for a given region completes. | `region(ireg)%num_tot` is set to the total number of HRUs implied by that region's element list. |
| `region(ireg)%num(ihru)` | During the second pass through region elements for a given region. | `region(ireg)%num(ihru)` stores each explicit HRU number that belongs to the region, whether copied directly from `reg_elem` or expanded from an LSU. |
| `region(ireg)%hru_ha(ihru)` | During the second pass when an HRU entry or LSU-expanded HRU is assigned to the region. | `region(ireg)%hru_ha(ihru)` stores the HRU area, either directly from `hru(ihru)%area_ha` or as an LSU fraction times `lsu_out(ilsu)%area_ha`. |

## File I/O

<!-- facts:io -->


## Lineage

`reg_read_elements.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `reg_read_elements.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'reg_read_elements' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
