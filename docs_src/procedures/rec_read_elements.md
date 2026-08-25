---
kind: procedure
symbol: rec_read_elements
title: rec_read_elements
status: filled
source_hash: 8a3ecae6f9187f00
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to consume the first title line from each input file
    before the routine reads the file header and data records.
  header: Scratch character buffer used to consume the file header line after the title line;
    it advances the file so the routine can scan the numeric records that follow.
  eof: I/O status flag used after each read to detect end-of-file or read failure and terminate
    the current scan loop safely.
  i_exist: Logical flag from INQUIRE that tells the routine whether the configured input file
    exists before attempting to open and read it.
  imax: Tracks the largest element index found while scanning the recall element file so the
    routine can allocate pcu_elem to the needed size.
  isp: Loop counter used both for element-count arrays and for iterating through HRU/element
    lists when copying or reading records.
  mcal: Unused local integer initialized to zero; no code in this routine changes or relies
    on it.
  mreg: Number of recall regions read from the definition files; drives allocation and looping
    over pcu_out, pcu_reg, and pcu_cal structures.
  i: General loop and record counter used when reading region and element records and indexing
    pcu_* arrays.
  k: Record-leading integer read from each data line; it appears to be a sequence or record
    identifier that is consumed but not otherwise used here.
  nspu: Number of defining-unit entries on a region record; determines whether the routine
    must expand an explicit membership list or fall back to all HRUs in the object.
  ielem1: Receives the total number of expanded element IDs returned by define_unit_elements
    so the routine can size num arrays correctly.
  ireg: Region loop counter used when copying membership and later when filling calibration
    arrays for each recall region.
  irec: Element-position counter inside a region used to populate per-region membership arrays
    and later compute HRU assignments and areas.
uses:
  input_file_module: The configured file names live in in_regs, and this routine uses those
    paths to decide which recall definition, region, and element files to open. Those filenames
    control all later file reads, so the module is the source of the external inputs that
    drive the routine.
  maximum_data_module: db_mx stores the maximum record counts for recall outputs and recall
    regions. This routine updates db_mx%rec_out and db_mx%rec_reg after reading the files
    so other setup code can size downstream arrays consistently.
  calibration_data_module: pcu_out, pcu_reg, pcu_cal, and pcu_elem hold the recall-unit memberships
    and derived per-element metadata that this routine builds. They are the persistent calibration
    structures later routines use to map region memberships to HRU numbers, areas, and recall
    output bookkeeping.
  hydrograph_module: 'sp_ob supplies fallback counts when a region record has no explicit
    element list: the routine uses sp_ob%hru and sp_ob%recall to size and fill the membership
    arrays so the recall unit covers all HRUs or recall objects. Those counts control the
    default expansion path when nspu is zero.'
---

<!-- facts:header -->

Reads recall-point-source definition files and expands each cataloging unit into its element membership list. It also prepares recall output structures and maps element IDs to HRU/recall metadata used by later calibration setup.

## Bottom Line

rec_read_elements reads up to three optional recall-related input files: the basin-level catalog unit file, the recall region file, and the element file. For each file it scans the listed regions, allocates the corresponding membership arrays, and fills module state that describes which element numbers belong to each recall unit or calibration region.

The routine matters because later calibration and hydrologic setup need these region-to-element mappings, plus per-region recall output arrays, to size and populate recall point-source structures. It also derives per-element HRU numbers and HRU areas for each recall region from the element definitions.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration-data preparation, after proc_cal has already invoked the other element-reading routines for aquifer, channel, reservoir, and soft-calibration data. Its results feed later calibration and routing setup by defining recall-unit memberships, recall output counts, and element-to-HRU mappings.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the recall catalog-unit definition file is available | The routine inquires on in_regs%def_psc and only enters the reader logic if the file exists or the configured name is not the literal "null". |
| 2. Read the recall catalog-unit file header and region count | It opens unit 107 on rec_catunit.def, reads the title, region count, and header, and stops early on end-of-file conditions. |
| 3. Allocate recall-output arrays by region | It allocates the srec_d, srec_m, srec_y, and srec_a arrays from 0 through mreg so later recall output can be stored by region. |
| 4. Scan each catalog-unit region record and expand memberships | For each region it reads the region summary, detects whether explicit subunits are listed, and either expands the list with define_unit_elements or defaults to all HRUs in sp_ob. |
| 5. Store the catalog-unit region count | After the scan completes, it records the number of recall output regions in db_mx%rec_out. |
| 6. Check and read the recall-region definition file | It repeats the same open-read-scan pattern for rec_reg.def, building pcu_reg memberships and saving the region count in db_mx%rec_reg. |
| 7. Zero recall calibration totals when regions exist | If any recall regions were read, it initializes the per-region accumulated area and count totals in pcu_cal to zero before later population. |
| 8. Read the recall element file and determine its size | It opens rec_catunit.ele, scans element indices to find the maximum one, and allocates pcu_elem to that size. |
| 9. Rewind and populate each recall element record | After rewinding the file, it rereads the header and loops through the element records, backspacing each line so it can read the full field set into pcu_elem(i). |
| 10. Derive HRU numbers and HRU areas for each recall region | For every region membership entry, it converts the stored element number to the element's obtypno and computes the HRU area as ru_frac times the region area. |
| 11. Close the shared file unit | It closes unit 107 after all input files have been processed and the calibration state has been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_regs` | `in_regs%def_psc, in_regs%def_psc_reg, in_regs%ele_psc` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%rec_out, db_mx%rec_reg` |
| [sym:calibration_data_module] | `pcu_out, pcu_reg, pcu_cal, pcu_elem` | `pcu_out(i)%name, pcu_out(i)%area_ha, pcu_out(i)%num(ielem1), pcu_out(i)%num, pcu_out(i)%num_tot, pcu_out(i)%num(irec), pcu_reg(i)%name, pcu_reg(i)%area_ha, pcu_reg(i)%num(ielem1), pcu_reg(i)%num, pcu_reg(i)%num_tot, pcu_reg(i)%num(irec), pcu_cal(ireg)%lum_ha_tot, pcu_cal(ireg)%lum_num_tot, pcu_elem(i)%name, pcu_elem(i)%obtyp, pcu_elem(i)%obtypno, pcu_elem(i)%bsn_frac, pcu_elem(i)%ru_frac, pcu_elem(i)%reg_frac, pcu_reg(ireg)%num_tot, pcu_reg(ireg)%num(irec), pcu_cal(ireg)%num(irec), pcu_elem(ielem1)%obtypno, pcu_cal(ireg)%hru_ha(irec), pcu_elem(ielem1)%ru_frac, pcu_cal(ireg)%area_ha` |
| [sym:hydrograph_module] | `sp_ob, srec_d, srec_m, srec_y, srec_a, elem_cnt, defunit_num, ielem_ru` | `sp_ob%hru, sp_ob%recall` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcu_out(i)%num` | When a recall catalog-unit region has been read and expanded from rec_catunit.def. | pcu_out(i)%num becomes the explicit list of element IDs assigned to recall output region i, either copied from defunit_num or filled with the default sequential HRU numbers. |
| `pcu_out(i)%num_tot` | When a recall catalog-unit region record is processed successfully. | pcu_out(i)%num_tot is set to the number of explicit members in that output region so later code knows the membership length. |
| `pcu_out(i)%num(irec)` | When the region has nspu > 0 and define_unit_elements has expanded the explicit member list. | pcu_out(i)%num(irec) receives each expanded member element number one by one, establishing the region's explicit membership vector. |
| `db_mx%rec_out` | After the rec_catunit.def scan finishes. | db_mx%rec_out is updated to the number of recall output regions so downstream allocation can size recall-output storage. |
| `pcu_reg(i)%num` | When a recall calibration region has been read and expanded from rec_reg.def. | pcu_reg(i)%num holds the explicit element IDs for that calibration region, or the default sequential HRU list when the record has no subunits. |
| `pcu_reg(i)%num_tot` | When a region record in rec_reg.def is processed successfully. | pcu_reg(i)%num_tot is set to the number of element memberships in the region. |
| `pcu_reg(i)%num(irec)` | When nspu > 0 for a region and define_unit_elements returns its explicit element list. | pcu_reg(i)%num(irec) is filled with each explicit member element number so the calibration region membership is preserved. |
| `db_mx%rec_reg` | After the rec_reg.def scan finishes. | db_mx%rec_reg is updated to the number of recall calibration regions so later setup can size region arrays correctly. |
| `pcu_cal(ireg)%lum_ha_tot` | If at least one recall region exists, before reading the recall element file. | pcu_cal(ireg)%lum_ha_tot is reset to zero so later routines can accumulate land-use area totals from a clean starting state. |
| `pcu_cal(ireg)%lum_num_tot` | If at least one recall region exists, before reading the recall element file. | pcu_cal(ireg)%lum_num_tot is reset to zero so later routines can accumulate land-use membership counts from a clean starting state. |
| `ielem_ru` | When the routine processes the recall element file and later maps each region membership entry to a specific element. | ielem_ru is reset to zero before the element pass begins, indicating that recall-to-HRU sequential linkage will be rebuilt from scratch. |
| `pcu_cal(ireg)%num(irec)` | During the final region-and-element mapping loop, once pcu_reg(ireg)%num(irec) has identified the element. | pcu_cal(ireg)%num(irec) is set to the element's obtypno value, converting the stored element reference into the HRU/object number used later. |
| `pcu_cal(ireg)%hru_ha(irec)` | During the final region-and-element mapping loop, once the element has been identified for a region member. | pcu_cal(ireg)%hru_ha(irec) is computed as pcu_elem(ielem1)%ru_frac multiplied by the region area, giving the HRU area contribution for that member. |

## File I/O

<!-- facts:io -->


## Lineage

`rec_read_elements.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `rec_read_elements.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'rec_read_elements' has no extracted documentation comment.
- No Git lineage commits were resolved for rec_read_elements, so lineage impacts are empty.
- The source reads and rewinds unit 107 multiple times across three different files; the file name bound to unit 107 changes by open statement.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
