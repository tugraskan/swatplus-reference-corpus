---
kind: procedure
symbol: res_read_elements
title: res_read_elements
status: filled
source_hash: a29b13c1507f0d53
version_label: SWAT+ 62.0.0
locals:
  header: Holds the second header line read from each input file before data records are scanned;
    it is discarded after the file format is confirmed.
  titldum: Holds the title line read from each input file; the routine reads it to skip past
    file metadata before the record counts and headers.
  eof: I/O status flag used by each READ to detect end-of-file or read failure and stop scanning
    the current file.
  i_exist: Logical flag from INQUIRE that tells the routine whether the configured file exists
    before attempting to open it.
  imax: Tracks the largest element index found in the reservoir element file so the routine
    can allocate `rcu_elem` large enough to hold every referenced element slot.
  mcal: Reserved counter variable initialized here but not used in the shown logic.
  mreg: Holds the number of reservoir output groups or reservoir calibration groups read from
    the current definition file.
  i: Loop and record index used while scanning group and element records.
  k: Leading integer field read from each data record; it is carried through the file format
    but not used in the later logic shown.
  nspu: Number of elements listed for the current reservoir group record; determines whether
    the routine reads an explicit membership list or falls back to default numbering.
  isp: Loop index used when reading the variable-length element-count list and when initializing
    `rcu_elem` records from 1 to `imax`.
  ielem1: Returned element-list length from `define_unit_elements`; used as the allocation
    size and total membership count for the current group.
  ireg: Iterates over reservoir regions when post-processing totals and when mapping region
    member numbers to element object numbers.
  ires: Iterates over member positions inside each region or reservoir group.
uses:
  input_file_module: The reservoir file names come from `input_file_module%in_regs`, so this
    module controls which definition files are opened and whether the routine treats the configured
    paths as real files or the default `null` placeholder values.
  maximum_data_module: The routine writes the discovered reservoir-group counts into `db_mx%res_out`
    and `db_mx%res_reg`, and those maxima are used elsewhere to size and validate reservoir-region
    data structures.
  calibration_data_module: 'These calibration-data arrays are the persistent targets that
    `res_read_elements` fills: it allocates group membership lists, stores reservoir names
    and areas, assigns member element numbers, and records reservoir type/object-number information
    that later calibration and reporting routines consume.'
  hydrograph_module: The routine uses `sp_ob%hru` and `sp_ob%res` as fallback sizes when a
    group record has no explicit element list, so hydrograph object counts determine how many
    member slots to allocate and initialize by default.
  reservoir_module: The module matters because the subroutine is part of reservoir setup and
    is called during the reservoir-reading stage from `proc_cal`; even though no named symbol
    is visible in the snippet, the imported module marks this routine as part of the reservoir
    subsystem.
---

<!-- facts:header -->

Reads reservoir cataloging-unit definition files and reservoir-element files, then builds the reservoir region membership arrays used by calibration and reporting.

## Bottom Line

res_read_elements loads reservoir cataloging-unit definitions from three input files: reservoir output groups (`res_catunit.def`), reservoir soft-calibration/type groups (`res_reg.def`), and reservoir element listings (`res_catunit.ele`). It sizes the shared arrays from the file contents, allocates membership lists, and copies each group’s element records into the `rcu_out`, `rcu_cal`, `rcu_reg`, and `rcu_elem` structures.

It matters because later reservoir calibration and output setup depend on the populated shared state, including `db_mx%res_out`, `db_mx%res_reg`, and the mapped reservoir type numbers stored in the group `num` arrays.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `proc_cal` after other landscape and channel setup routines and before calibration arrays are finalized. It prepares reservoir output, reservoir-region, and reservoir-element membership data so later calibration and reporting code can map reservoir objects by name, area, type, and member element number.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Reset counters and check for the reservoir output-definition file | Initialize the scan counters to zero, inquire whether `in_regs%def_res` exists, and only enter the reservoir output read loop if the file is present or the configured name is not the null placeholder. |
| 2. Read reservoir output-group headers and member lists | Open `res_catunit.def`, skip the title and header lines, read each output group, and either expand explicit member lists with `define_unit_elements` or assign the default reservoir object range when `nspu` is zero; then store the group count in `db_mx%res_out`. |
| 3. Check for the reservoir soft-calibration file | Inquire whether `in_regs%def_res_reg` exists and only enter the reservoir soft-calibration read loop if the file is present or the configured name is not the null placeholder. |
| 4. Read reservoir calibration-group headers and member lists | Open `res_reg.def`, skip the title and header lines, read each calibration group, and either expand explicit member lists with `define_unit_elements` or assign the default reservoir object range when `nspu` is zero; then store the group count in `db_mx%res_reg`. |
| 5. Initialize per-region land-use totals | If any calibration regions were read, zero the `lum_ha_tot` and `lum_num_tot` accumulators for each region before later calculations use them. |
| 6. Check for the reservoir element listing | Inquire whether `in_regs%ele_res` exists and only enter the reservoir element scan if the file is present or the configured name is not the null placeholder. |
| 7. Scan the element file to size the element array | Open `res_catunit.ele`, skip the title and header lines, read the element indices to find the largest index, and allocate `rcu_elem(imax)` so every referenced reservoir element can be stored. |
| 8. Rewind and load reservoir element records | Rewind the file, skip the title and header again, and read each element record into `rcu_elem(i)` with its name, object type, object number, and fractional weights. |
| 9. Map calibration-group member ids to reservoir object numbers | For each calibration region and each member slot, look up the referenced element in `rcu_elem` and replace the stored member id with that element's `obtypno` value. |
| 10. Close the shared input unit and return | Close unit 107 after all reservoir setup arrays have been populated, then return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_regs` | `in_regs%def_res, in_regs%def_res_reg, in_regs%ele_res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_out, db_mx%res_reg` |
| [sym:calibration_data_module] | `rcu_out, rcu_cal, rcu_reg, rcu_elem` | `rcu_out(i)%name, rcu_out(i)%area_ha, rcu_out(i)%num(ielem1), rcu_out(i)%num, rcu_out(i)%num_tot, rcu_out(i)%num(ires), rcu_cal(i)%name, rcu_cal(i)%area_ha, rcu_cal(i)%num(ielem1), rcu_cal(i)%num, rcu_cal(i)%num_tot, rcu_reg(i)%num, rcu_reg(i)%num_tot, rcu_reg(i)%num(ires), rcu_cal(ireg)%lum_ha_tot, rcu_cal(ireg)%lum_num_tot, rcu_elem(i)%name, rcu_elem(i)%obtyp, rcu_elem(i)%obtypno, rcu_elem(i)%bsn_frac, rcu_elem(i)%ru_frac, rcu_elem(i)%reg_frac, rcu_reg(ireg)%num_tot, rcu_reg(ireg)%num(ires), rcu_cal(ireg)%num(ires), rcu_elem(ielem1)%obtypno` |
| [sym:hydrograph_module] | `sp_ob, elem_cnt, defunit_num` | `sp_ob%hru, sp_ob%res` |
| [sym:reservoir_module] | `reservoir_module state/types are not directly referenced in the extracted lines, but the module is imported because this routine is reservoir-specific and its allocations feed reservoir-related processing.` | `No specific reservoir_module symbols are visible in the extracted source lines.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rcu_out(i)%num` | When a reservoir output group has explicit member entries in `res_catunit.def` (`nspu > 0`), after `define_unit_elements` fills `defunit_num`. | `rcu_out(i)%num` is replaced with the expanded reservoir object/member list copied from `defunit_num` so the group stores the actual selected members rather than the raw file tokens. |
| `rcu_out(i)%num_tot` | When a reservoir output group has explicit member entries in `res_catunit.def` (`nspu > 0`), immediately before `rcu_out(i)%num` is allocated and filled. | `rcu_out(i)%num_tot` records the number of expanded member ids returned by `define_unit_elements` for that output group. |
| `rcu_out(i)%num(ires)` | When a reservoir output group has no explicit member list in `res_catunit.def` (`nspu == 0`), during the default-fill branch. | `rcu_out(i)%num(ires)` is filled with the sequential reservoir ids `1..sp_ob%res` so the output group covers all reservoirs. |
| `db_mx%res_out` | After the `res_catunit.def` scan completes successfully for one or more groups. | `db_mx%res_out` is set to the number of reservoir output groups read from the file, making that maximum available to later setup code. |
| `rcu_cal(i)%num` | When a reservoir calibration group has explicit member entries in `res_reg.def` (`nspu > 0`), after `define_unit_elements` fills `defunit_num`. | `rcu_cal(i)%num` is replaced with the expanded reservoir object/member list copied from `defunit_num` so the calibration group stores the actual selected members. |
| `rcu_cal(i)%num_tot` | When a reservoir calibration group has explicit member entries in `res_reg.def` (`nspu > 0`), immediately before `rcu_cal(i)%num` is allocated and filled. | `rcu_cal(i)%num_tot` records the number of expanded member ids returned by `define_unit_elements` for that calibration group. |
| `rcu_reg(i)%num_tot` | When a reservoir calibration group has no explicit member list in `res_reg.def` (`nspu == 0`), during the default-fill branch. | `rcu_reg(i)%num_tot` is set to `sp_ob%res`, meaning the region spans the full reservoir object range used by default. |
| `rcu_reg(i)%num(ires)` | When a reservoir calibration group has no explicit member list in `res_reg.def` (`nspu == 0`), during the default-fill branch. | `rcu_reg(i)%num(ires)` is filled with the sequential reservoir ids `1..sp_ob%res` so the region covers all reservoirs. |
| `db_mx%res_reg` | After the `res_reg.def` scan completes successfully for one or more groups. | `db_mx%res_reg` is set to the number of reservoir calibration groups read from the file, making that maximum available to later setup code. |
| `rcu_cal(ireg)%lum_ha_tot` | If one or more reservoir calibration regions were read (`mreg > 0`), before later calibration calculations use the totals. | `rcu_cal(ireg)%lum_ha_tot` is reset to zero for each region so land-use area totals can be accumulated later from a clean baseline. |
| `rcu_cal(ireg)%lum_num_tot` | If one or more reservoir calibration regions were read (`mreg > 0`), before later calibration calculations use the totals. | `rcu_cal(ireg)%lum_num_tot` is reset to zero for each region so land-use count totals can be accumulated later from a clean baseline. |
| `rcu_cal(ireg)%num(ires)` | When the routine maps reservoir calibration-group members after reading `res_catunit.ele`. | `rcu_cal(ireg)%num(ires)` is overwritten with `rcu_elem(ielem1)%obtypno`, translating each stored element id into its reservoir object type number. |

## File I/O

<!-- facts:io -->


## Lineage

`res_read_elements.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `res_read_elements.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_elements' has no extracted documentation comment.
- No resolved lineage commits for this span; lineage fields are based on the absence of evidence.
- algorithm_steps revised: merged the source scan into a 10-step sequence and aligned each step to visible source lines in `res_read_elements.f90`.
- The source allocates `rcu_out(i)%num(sp_ob%hru)` and `rcu_reg(i)%num(sp_ob%hru)` in the default branches, but the loops fill `1..sp_ob%res`; that mismatch is preserved here because it appears in the source.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
