---
kind: procedure
symbol: aqu_read_elements
title: aqu_read_elements
status: filled
source_hash: 1eab0c9ffb18fa6e
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title-line string read from the input files and discarded after the file
    header is validated.
  header: Temporary header string read from the input files; it is used to skip the second
    header line before data records are scanned.
  eof: I/O status flag for reads; negative values are used to stop when end-of-file is reached.
  imax: Tracks the maximum aquifer element index seen in aqu_catunit.ele so the aquifer element
    array can be allocated to the right size.
  mcal: Declared and reset but not used in the visible source; it appears to be a leftover
    counter placeholder.
  i_exist: Logical flag from INQUIRE that tells whether the configured input file exists before
    the routine tries to read it.
  mreg: Holds the number of aquifer regions read from aqu_catunit.def and drives allocation
    plus later region loops.
  i: General loop and record index used while reading region and element records.
  k: Record number or leading index field read from the catalog-unit data lines before the
    named fields.
  nspu: Number of defining-unit entries listed on a region record; it controls whether the
    record must be expanded with define_unit_elements.
  isp: Loop index used when scanning the per-record element count list elem_cnt and when iterating
    over element counts.
  ielem1: Receives the total expanded element count returned by define_unit_elements so the
    target num array can be allocated.
  ihru: Loop index used when filling the default full-HRU membership list for a region with
    no explicit element list.
  iaqu: Loop index used when converting aquifer-region memberships to element numbers and
    later to aquifer calibration entries.
  ireg: Region index for the calibration and per-region aquifer loops after all input has
    been read.
uses:
  input_file_module: 'input_file_module provides the configured filenames aqu_read_elements
    opens: in_regs%def_aqu for aquifer region/output definitions, in_regs%def_aqu_reg for
    aquifer-type soft-calibration regions, and in_regs%ele_aqu for aquifer element definitions.
    Those file names control whether the routine can read anything at all.'
  calibration_data_module: calibration_data_module holds the shared aquifer region, output,
    calibration, and element arrays that this routine allocates and fills. The routine writes
    membership numbers, names, area totals, and aquifer-element properties into these structures
    so later calibration and output code can use them.
  hydrograph_module: hydrograph_module supplies sp_ob%hru and sp_ob%aqu, which the routine
    uses when no explicit element list is provided for a region. Those counts define the full
    default membership size for a region and distinguish HRU-based versus aquifer-based looping.
  aquifer_module: aquifer_module contains the aquifer state arrays saqu_d, saqu_m, saqu_y,
    and saqu_a that are allocated alongside the region tables. They matter because aquifer
    output/state records must exist for each region before the aquifer simulation and reporting
    code can populate them.
  maximum_data_module: maximum_data_module holds db_mx, which this routine updates with the
    number of aquifer output regions, aquifer soft-calibration regions, and aquifer elements
    that were actually read. Those maxima are used later to size and iterate over aquifer-related
    arrays consistently.
---

<!-- facts:header -->

Reads aquifer catalog-unit definitions and aquifer element listings, then expands them into module state for aquifer output, soft calibration, and per-region element mapping.

## Bottom Line

aqu_read_elements is a setup routine for aquifer-related calibration and output. It reads aquifer definition files, allocates the aquifer region/output arrays, expands any grouped element lists into explicit element numbers with define_unit_elements, and stores those memberships in shared calibration data.

It then reads the aquifer element file, builds the aquifer element table, and converts each region's stored element numbers into HRU/object numbers and HRU areas. The resulting shared state is used later by aquifer output and aquifer soft-calibration workflows, which are initialized from the arrays this routine fills.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the calibration/setup phase in proc_cal, after cal_conditions, calsoft_read_codes, lcu_read_softcal, and ls_read_lsparms_cal have prepared the broader calibration context. Its outputs define aquifer-region memberships and aquifer element metadata that later aquifer output and soft-calibration code depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Reset counters and check whether the aquifer definition file should be used. | Sets mreg, imax, and mcal to zero, then uses INQUIRE on in_regs%def_aqu. The routine proceeds when the file exists or the configured name is not 'null'. |
| 2. Open the aquifer definition file and read its title, region count, and header. | Opens the file on unit 107, reads the title line into titldum, the region count into mreg, and the header line into header, exiting the loop if end-of-file is encountered. |
| 3. Allocate aquifer output, region, and dynamic state arrays for the declared region count. | Allocates acu_reg, acu_out, acu_cal, and the aquifer dynamic arrays saqu_d, saqu_m, saqu_y, and saqu_a using bounds 0:mreg so region-indexed state exists before membership lists are filled. |
| 4. Scan each aquifer output region record and expand explicit membership lists when present. | For each region record, reads the name, area, and member count. If nspu is greater than zero, it allocates elem_cnt, backs up one record, rereads the explicit member list, calls define_unit_elements to expand it, copies defunit_num into acu_out(i)%num, stores the total in acu_out(i)%num_tot, and then deallocates defunit_num. |
| 5. Default aquifer output regions to all HRUs when no explicit list is supplied. | When nspu is zero, the routine allocates acu_out(i)%num to the size of sp_ob%hru, sets num_tot to sp_ob%hru, and fills the membership numbers sequentially from 1 to sp_ob%hru. |
| 6. Record the number of aquifer output regions that were read. | After the region loop, the routine exits the read loop and stores mreg in db_mx%aqu_out so later code knows how many aquifer output regions were configured. |
| 7. Open the aquifer soft-calibration region definition file and read its header. | Checks in_regs%def_aqu_reg, opens unit 107, and reads the title, region count, and header lines for the aquifer-region pass. |
| 8. Read each aquifer calibration region and expand explicit memberships when present. | For each region record, reads the name, area, and member count. If nspu is greater than zero, it allocates elem_cnt, backs up, rereads the explicit list, calls define_unit_elements, copies defunit_num into acu_reg(i)%num, sets num_tot, and deallocates defunit_num. |
| 9. Default aquifer calibration regions to all aquifer objects when no explicit list is supplied. | When nspu is zero, the routine allocates acu_reg(i)%num to sp_ob%hru, sets num_tot to sp_ob%hru, and fills the membership numbers in the fallback loop. |
| 10. Record the number of aquifer calibration regions that were read. | After the region loop, the routine exits the read loop and stores mreg in db_mx%aqu_reg so later code can size aquifer calibration/output structures. |
| 11. Initialize aquifer calibration totals when region data exist. | If mreg is greater than zero, the routine loops over each aquifer calibration region and resets lum_ha_tot and lum_num_tot to zero before later calibration bookkeeping uses them. |
| 12. Scan the aquifer element file to determine how many element records exist. | Checks in_regs%ele_aqu, opens unit 107, reads the title and header, then loops through the file reading the element index i and tracking the maximum value in imax. |
| 13. Rewind the aquifer element file and load each element record into acu_elem. | Rewinds unit 107, rereads the title and header, stores imax in db_mx%aqu_elem, then reads each indexed record into acu_elem(i)%name, obtyp, obtypno, bsn_frac, ru_frac, and reg_frac. |
| 14. Map region membership element numbers to aquifer object numbers and HRU areas, then close the file. | For each aquifer calibration region and each stored member, the routine looks up the element number in acu_elem, copies obtypno into acu_cal(ireg)%num(iaqu), computes hru_ha from ru_frac times the region area, closes unit 107, and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_regs` | `in_regs%def_aqu, in_regs%def_aqu_reg, in_regs%ele_aqu` |
| [sym:calibration_data_module] | `acu_out, acu_reg, acu_cal, acu_elem` | `acu_out(i)%name, acu_out(i)%area_ha, acu_out(i)%num(ielem1), acu_out(i)%num, acu_out(i)%num_tot, acu_out(i)%num(ihru), acu_reg(i)%name, acu_reg(i)%area_ha, acu_reg(i)%num(ielem1), acu_reg(i)%num, acu_reg(i)%num_tot, acu_reg(i)%num(ihru), acu_cal(ireg)%lum_ha_tot, acu_cal(ireg)%lum_num_tot, acu_elem(i)%name, acu_elem(i)%obtyp, acu_elem(i)%obtypno, acu_elem(i)%bsn_frac, acu_elem(i)%ru_frac, acu_elem(i)%reg_frac, acu_reg(ireg)%num_tot, acu_reg(ireg)%num(iaqu), acu_cal(ireg)%num(iaqu), acu_elem(ielem1)%obtypno, acu_cal(ireg)%hru_ha(iaqu), acu_elem(ielem1)%ru_frac, acu_cal(ireg)%area_ha` |
| [sym:hydrograph_module] | `sp_ob, elem_cnt, defunit_num` | `sp_ob%hru, sp_ob%aqu` |
| [sym:aquifer_module] | `saqu_d, saqu_m, saqu_y, saqu_a` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%aqu_out, db_mx%aqu_reg, db_mx%aqu_elem` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `acu_out(i)%num` | When nspu > 0 for an aquifer output region record read from in_regs%def_aqu, after define_unit_elements expands the explicit member list. | acu_out(i)%num is allocated to the expanded member count and filled with the explicit defining-unit numbers copied from defunit_num, replacing any default membership. |
| `acu_out(i)%num_tot` | When each aquifer output region record is processed; after either explicit expansion or the all-HRU fallback. | acu_out(i)%num_tot is set to the number of member HRUs/elements stored for that region so later routines know the region size. |
| `acu_out(i)%num(ihru)` | When nspu = 0 for an aquifer output region record read from in_regs%def_aqu. | acu_out(i)%num(ihru) is filled sequentially with every HRU number from 1 to sp_ob%hru so the region represents all HRUs. |
| `db_mx%aqu_out` | After the aquifer output region pass completes successfully. | db_mx%aqu_out is set to mreg to record the maximum number of aquifer output regions configured in the input file. |
| `acu_reg(i)%num` | When nspu > 0 for an aquifer calibration region record read from in_regs%def_aqu_reg, after define_unit_elements expands the list. | acu_reg(i)%num is allocated and filled with the explicit defining-unit numbers copied from defunit_num for that region. |
| `acu_reg(i)%num_tot` | When each aquifer calibration region record is processed; after either explicit expansion or the fallback assignment. | acu_reg(i)%num_tot is set to the number of member HRUs/elements stored for that region. |
| `acu_reg(i)%num(ihru)` | When nspu = 0 for an aquifer calibration region record read from in_regs%def_aqu_reg. | acu_reg(i)%num(ihru) is filled in the fallback loop so the region includes the full available set referenced by the routine. |
| `db_mx%aqu_reg` | After the aquifer calibration region pass completes successfully. | db_mx%aqu_reg is set to mreg to record the maximum number of aquifer calibration regions configured in the input file. |
| `acu_cal(ireg)%lum_ha_tot` | When mreg > 0 before element mapping begins. | acu_cal(ireg)%lum_ha_tot is reset to zero for each aquifer calibration region so later land-use accounting starts from a clean total. |
| `acu_cal(ireg)%lum_num_tot` | When mreg > 0 before element mapping begins. | acu_cal(ireg)%lum_num_tot is reset to zero for each aquifer calibration region so later land-use accounting starts from a clean total. |
| `db_mx%aqu_elem` | When the aquifer element file in_regs%ele_aqu is scanned and the largest element index has been found. | db_mx%aqu_elem is set to imax so later code can size and access the aquifer element table correctly. |
| `acu_cal(ireg)%num(iaqu)` | When each stored aquifer region member number iaqu is mapped to an element record during the final region loop. | acu_cal(ireg)%num(iaqu) is assigned the element's obtypno, converting stored element membership into the object number used by later model code. |
| `acu_cal(ireg)%hru_ha(iaqu)` | When each stored aquifer region member number iaqu is mapped to an element record during the final region loop. | acu_cal(ireg)%hru_ha(iaqu) is computed from acu_elem(ielem1)%ru_frac multiplied by acu_cal(ireg)%area_ha, giving the member area in hectares. |

## File I/O

<!-- facts:io -->


## Lineage

`aqu_read_elements.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `aqu_read_elements.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'aqu_read_elements' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft into 14 source-backed steps and separated the two file passes plus final mapping/close actions.
- Source shows a likely bug in the fallback aquifer calibration loop: line 117 assigns acu_reg(i)%num(ihru) inside a loop over iaqu.
- Source shows another potential issue in the aquifer region pass: line 89 opens in_regs%def_aqu instead of in_regs%def_aqu_reg despite the surrounding logic for the region-definition file.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
