---
kind: procedure
symbol: pl_read_parms_cal
title: pl_read_parms_cal
status: filled
source_hash: b82832c88fef7ff2
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from plant_parms.sft and discarded after the file header
    is skipped.
  header: Temporary header text read from plant_parms.sft before the region or parameter blocks
    are processed.
  eof: I/O status flag for reads from unit 107; negative values are used to stop processing
    at end-of-file or failed input.
  i_exist: Logical flag set by inquire to decide whether the configured plant calibration
    file exists before attempting to read it.
  mreg: Holds the number of plant calibration regions read from the file and drives the outer
    loop and pl_prms allocation.
  i: Loop counter for the current plant calibration region being read and processed.
  ilum: Loop counter for iterating over each land-use/parameter calibration entry inside a
    region.
  ilum_mx: Computed total number of calibration entries for a region, equal to lum_num * parms.
  isp: Loop counter used while reading the temporary elem_cnt list of HRU counts or element
    counts from the soft file.
  ielem1: Returned total size of the expanded unit list from define_unit_elements, used to
    size pl_prms(i)%num.
  iihru: Intermediate HRU index taken from pl_prms(i)%num(ihru) before updating the matching
    HRU record.
  ihru: Loop counter over the HRUs assigned to a calibration region or over all HRUs when
    no subgroups are listed.
  nspu: Number of spatial units listed for the current region; if positive, the routine reads
    an explicit unit list.
  ipl: Loop counter over plants in the current HRU's plant community when matching plant names
    to calibration entries.
uses:
  maximum_data_module: db_mx%plcal_reg stores the maximum/active count of plant calibration
    regions, so this routine can publish how many regions were read and downstream calibration
    code can size or validate region-based plant calibration data.
  calibration_data_module: pl_prms is the persistent container for each plant calibration
    region, its HRU membership list, and its per-plant soft-calibration entries; this routine
    allocates and fills that shared data so later code can use it when applying calibration
    values.
  hydrograph_module: sp_ob%hru provides the total HRU count used when a region does not list
    explicit subunits; it defines how many HRUs belong to the region in the all-HRU case.
  hru_module: hru(iihru)%crop_reg and hru(ihru)%crop_reg are the per-HRU region labels that
    this routine assigns so later plant and HRU processing can tell which calibration region
    each HRU belongs to.
  input_file_module: in_chg%plant_parms_sft supplies the file name to open, so it controls
    whether this routine reads plant calibration data at all and which file it reads.
  plant_module: pcom holds each HRU's plant community and current plant status, which is where
    the read calibration values are applied after matching plant names and parameter names.
---

<!-- facts:header -->

Reads the plant calibration soft file and applies region-based plant parameter settings to HRUs and plant status variables.

## Bottom Line

pl_read_parms_cal loads the plant parameter soft-calibration file named by in_chg%plant_parms_sft, builds the list of calibration regions in pl_prms, and maps each region to the HRUs it contains. It also records the region count in db_mx%plcal_reg.

For each calibration region and each matched plant name, it applies the file's init_val to the corresponding plant status field: epco, pest_stress, lai_pot, or harv_idx. That makes the soft-calibration file an input to later plant-growth and calibration behavior.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration setup in proc_cal, after cal_parm_read and cal_parmchg_read and after pl_read_regions_cal has prepared related plant-region data. Its outputs feed later plant calibration and plant-status initialization because it assigns HRU membership and writes plant status calibration values into pcom.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check whether the configured file exists. | The routine resets mreg and eof, then uses inquire on in_chg%plant_parms_sft to decide whether the plant calibration file is available or named 'null'. |
| 2. Handle the no-file case with an empty region array. | If the file is missing or disabled, it allocates pl_prms with bounds 0:0 and skips the rest of the reading logic. |
| 3. Open the plant calibration file and read its top-of-file metadata. | The file is opened on unit 107, the title line is skipped, the number of regions mreg is read, the next header line is skipped, and pl_prms is allocated to size mreg. |
| 4. Read each calibration region record. | For each region, the routine reads the region name, land-use count, parameter count, and spatial-unit count; if the read fails or reaches end-of-file, the loop stops. |
| 5. Expand explicit region memberships when nspu is positive. | When the record lists one or more spatial units, the routine allocates elem_cnt, backs up one record, rereads the unit list, calls define_unit_elements to expand it, copies defunit_num into pl_prms(i)%num, stores the total in num_tot, marks each matching hru(iihru)%crop_reg, and then deallocates defunit_num. |
| 6. Assign all HRUs to the region when no explicit list is provided. | If nspu is not positive, the routine allocates pl_prms(i)%num for all HRUs in sp_ob%hru, fills the membership list with the full HRU index range, and sets each hru(ihru)%crop_reg to the current region. |
| 7. Read optional landscape soft-calibration entries for the region. | If the region has land-use entries, the routine computes ilum_mx from lum_num and parms, reads a section header, allocates pl_prms(i)%prm, and reads each calibration record into that array. |
| 8. Apply matching plant calibration values to plant status. | For each region calibration entry, each member HRU, and each plant in the HRU's community, the routine matches plant names and writes the init_val into the corresponding plant status field selected by var. |
| 9. Finish the region loop and publish the region count. | After the outer loop ends, the routine stores mreg in db_mx%plcal_reg, closes unit 107, and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plcal_reg` |
| [sym:calibration_data_module] | `pl_prms` | `pl_prms(i)%name, pl_prms(i)%lum_num, pl_prms(i)%parms, pl_prms(i)%num(ielem1), pl_prms(i)%num, pl_prms(i)%num_tot, pl_prms(i)%num(ihru), pl_prms(i)%prm(ilum_mx), pl_prms(i)%prm(ilum), pl_prms(i)%prm(ilum)%name, pl_prms(i)%prm(ilum)%var, pl_prms(i)%prm(ilum)%init_val` |
| [sym:hydrograph_module] | `sp_ob, elem_cnt, defunit_num` | `sp_ob%hru` |
| [sym:hru_module] | `hru` | `hru(iihru)%crop_reg, hru(ihru)%crop_reg` |
| [sym:input_file_module] | `in_chg` | `in_chg%plant_parms_sft` |
| [sym:plant_module] | `pcom` | `pcom(iihru)%npl, pcom(iihru)%pl(ipl), pcom(iihru)%plcur(ipl)%epco, pcom(iihru)%plcur(ipl)%pest_stress, pcom(iihru)%plcur(ipl)%lai_pot, pcom(iihru)%plcur(ipl)%harv_idx` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pl_prms(i)%num` | When a region record is read and nspu > 0, pl_prms(i)%num is allocated to ielem1 and filled from defunit_num; when nspu <= 0, it is allocated to sp_ob%hru and filled with the full HRU index range. | pl_prms(i)%num becomes the membership list for calibration region i, identifying which HRUs belong to that region. |
| `pl_prms(i)%num_tot` | After the region membership list is built, pl_prms(i)%num_tot is set to ielem1 for explicit memberships or to sp_ob%hru for the all-HRU case. | pl_prms(i)%num_tot records how many HRUs are in the current calibration region and sets the loop bound for later plant updates. |
| `hru(iihru)%crop_reg` | In the explicit-membership branch, each HRU index returned by pl_prms(i)%num(ihru) is used to set hru(iihru)%crop_reg = i. | The crop region field on each referenced HRU is tagged with the current calibration region so later code can tell which region the HRU belongs to. |
| `pl_prms(i)%num(ihru)` | Whenever an explicit membership list is expanded, pl_prms(i)%num(ihru) holds the HRU index copied from defunit_num for each position in the region list. | These entries are the explicit HRU identifiers used to locate each HRU when applying calibration data. |
| `hru(ihru)%crop_reg` | In the all-HRU branch, each hru(ihru)%crop_reg is set while the loop assigns every HRU to the current region. | The crop region field is filled for every HRU when the calibration region applies to the entire spatial domain. |
| `pcom(iihru)%plcur(ipl)%epco` | During the plant-application loop, when pl_prms(i)%prm(ilum)%var equals 'epco', the corresponding plant status field is assigned init_val. | epco becomes the calibrated plant water-uptake compensation factor for the matched plant in the matched HRU. |
| `pcom(iihru)%plcur(ipl)%pest_stress` | During the plant-application loop, when pl_prms(i)%prm(ilum)%var equals 'pest_stress', the corresponding plant status field is assigned init_val. | pest_stress becomes the calibrated pest-stress factor for the matched plant in the matched HRU. |
| `pcom(iihru)%plcur(ipl)%lai_pot` | During the plant-application loop, when pl_prms(i)%prm(ilum)%var equals 'lai_pot', the corresponding plant status field is assigned init_val. | lai_pot becomes the calibrated potential leaf-area index for the matched plant in the matched HRU. |
| `pcom(iihru)%plcur(ipl)%harv_idx` | During the plant-application loop, when pl_prms(i)%prm(ilum)%var equals 'harv_idx', the corresponding plant status field is assigned init_val. | harv_idx becomes the calibrated harvest index for the matched plant in the matched HRU. |
| `db_mx%plcal_reg` | After all region records are processed, db_mx%plcal_reg is assigned the final mreg value. | db_mx%plcal_reg records the number of plant calibration regions read from the file for use by later calibration setup. |

## File I/O

<!-- facts:io -->


## Lineage

`pl_read_parms_cal.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_read_parms_cal.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'pl_read_parms_cal' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
