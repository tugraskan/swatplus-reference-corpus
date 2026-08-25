---
kind: procedure
symbol: ch_read_elements
title: ch_read_elements
status: filled
source_hash: cbe877d02f56a46c
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from each input definition file header. It is not used
    for calculations; it is just consumed so the routine can advance past the title record.
  header: Temporary header line read from each input definition file. The code reads and discards
    it before processing the data records that follow.
  eof: I/O status flag for `read` statements. A negative value ends the scan when the file
    is exhausted or a read fails at end-of-file.
  imax: Tracks the largest element index found in `element.ccu` during the first pass so the
    routine can allocate `ccu_elem(imax)` before rereading the file.
  mcal: Initialized but not used in the shown routine body. It appears to be a leftover counter
    or placeholder for calibration-related counts.
  i_exist: Receives the result of `inquire(file=..., exist=...)` so the routine can tell whether
    each configured definition file is available before trying to read it.
  mreg: Holds the number of channel regions read from the definition file. The routine uses
    it to size loops, allocate output arrays, and store `db_mx%cha_reg`.
  i: General loop and record index, reused while scanning region records and while reading
    `element.ccu` entries.
  k: Record identifier read from the data files. The routine reads it with each row but does
    not use it in later calculations.
  nspu: Number of defining-unit entries listed for a region on a given record. It controls
    whether the routine expands a membership list and how many values are read into `elem_cnt`.
  isp: Loop counter used both for iterating over the `elem_cnt` list and for scanning the
    `element.ccu` file by record.
  ielem1: Receives the total number of explicit element IDs produced by `define_unit_elements`,
    and then serves as the allocation length for the region membership arrays.
  icha: Loop counter over the elements or HRUs within a region when copying memberships and
    later when computing calibration summaries.
  ireg: Loop counter over channel regions. It drives allocation, initialization, and final
    per-region mapping of calibration data.
  ires: Index used when storing a channel assignment into `ccu_out(i)%num(ires)` for the special
    case where a region contains all channel objects.
uses:
  input_file_module: This module provides the configured file names `in_regs%def_cha` and
    `in_regs%def_cha_reg`. `ch_read_elements` uses them to decide which channel-definition
    files to open and read.
  maximum_data_module: The routine stores the number of channel regions it finds in `db_mx%cha_reg`.
    That maximum-data field is the shared count other setup and allocation code uses to size
    channel-region structures.
  calibration_data_module: These arrays and derived quantities are the calibration-region
    state that `ch_read_elements` fills. It reads channel memberships into `ccu_out` and `ccu_reg`,
    uses `ccu_elem` for per-element metadata from `element.ccu`, and writes derived counts
    and areas into `ccu_cal` for later soft-calibration and output processing.
  hydrograph_module: The spatial object counts determine how many HRU, reservoir, and channel
    IDs exist when a region record does not list explicit elements. The routine uses `sp_ob%hru`,
    `sp_ob%res`, and `sp_ob%chan` to size fallback arrays and to map a region to all channel
    objects.
  sd_channel_module: This module owns the channel-output arrays `schsd_d`, `schsd_m`, `schsd_y`,
    and `schsd_a`. `ch_read_elements` allocates them with bounds `0:mreg` so channel soft-calibration
    output structures exist for every region index it reads.
---

<!-- facts:header -->

Reads channel cataloging-unit definitions and channel-region definitions, then expands the listed element memberships into calibration arrays. It also loads element metadata from `element.ccu` and derives per-region HRU area and object-number mappings used by channel calibration.

## Bottom Line

`ch_read_elements` is a setup routine for channel soft calibration. It checks whether the channel cataloging-unit definition file and channel region definition file are present, scans them to determine how many regions and elements exist, allocates the corresponding shared arrays, and fills `ccu_out`, `ccu_reg`, and `ccu_elem` with membership and element metadata.

After the membership lists are read, the routine converts element numbers into object numbers and computes HRU areas for each calibration region. Those results feed later channel calibration and output logic through `ccu_cal`, `ccu_out`, `ccu_reg`, and `db_mx%cha_reg`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration setup inside `proc_cal`, after soft-calibration codes and several other object-definition readers have prepared shared state. Its outputs are used later when channel calibration and region-based output need region membership lists, per-element object numbers, and HRU area totals.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test the configured channel definition file. | The routine resets local counters, checks whether `in_regs%def_cha` exists, and only enters the channel-definition reader if the file is present or the configured name is not the sentinel string `null`. |
| 2. Read the channel cataloging-unit header and region count. | It opens `in_regs%def_cha` on unit 107, reads the title line, reads `mreg`, and reads the header line before processing region records. |
| 3. Allocate channel-output arrays for all region slots. | Using the just-read region count, it allocates `schsd_d`, `schsd_m`, `schsd_y`, and `schsd_a` with bounds `0:mreg` so channel output structures exist for every region index. |
| 4. Scan each channel region record and load explicit memberships when present. | For each region, the routine reads the summary line, allocates `elem_cnt` if the region has explicit members, backspaces to reread the line with the full list, and calls `define_unit_elements` to expand the compact membership list into explicit element numbers. |
| 5. Store expanded channel memberships or fallback full-channel membership. | When explicit elements exist, it allocates `ccu_out(i)%num`, copies `defunit_num` into it, records `num_tot`, and deallocates `defunit_num`; otherwise it allocates the array from `sp_ob%hru`, sets `num_tot` from `sp_ob%res`, and fills the region with channel IDs from `sp_ob%chan`. |
| 6. Record the number of channel regions found. | After the scan completes, the routine exits the read loop and stores `mreg` in `db_mx%cha_reg` so the rest of the model knows how many channel regions were defined. |
| 7. Read the channel region soft-calibration definition file. | It repeats the open/read/backspace/expand pattern for `in_regs%def_cha_reg`, allocates `ccu_reg(i)%num` from the explicit membership list, and fills fallback membership from `sp_ob%hru` and `sp_ob%chan` when no explicit list is provided. |
| 8. Initialize calibration accumulators for all channel regions. | If any regions were defined, it loops over them and clears `ccu_cal(ireg)%lum_ha_tot` and `ccu_cal(ireg)%lum_num_tot` so later calibration accumulation starts from zero. |
| 9. Detect and open the channel element metadata file. | The routine checks whether `element.ccu` exists, opens it on unit 107, and reads past the title and header lines before scanning for the largest element index. |
| 10. Find the largest element index and allocate `ccu_elem`. | It scans the file for the maximum element number in `imax` and then allocates `ccu_elem(imax)` so each element record can be stored by index. |
| 11. Rewind and reread every element record into `ccu_elem`. | After rewinding unit 107, the routine rereads the title and header, loops through element indices, backspaces each record, and loads the element name, object type, object number, and fraction fields into `ccu_elem(i)`. |
| 12. Convert element numbers to object numbers and compute HRU areas. | For each region and each explicit member, it maps the stored element number to `ccu_elem(ielem1)%obtypno` and computes `ccu_cal(ireg)%hru_ha(icha)` as the element's `ru_frac` times the region area. |
| 13. Close the input unit and return. | The routine closes unit 107 and returns to the caller after all channel-region and element state has been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_regs` | `in_regs%def_cha, in_regs%def_cha_reg` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cha_reg` |
| [sym:calibration_data_module] | `ccu_out, ccu_reg, ccu_cal, ccu_elem` | `ccu_out(i)%name, ccu_out(i)%area_ha, ccu_out(i)%num(ielem1), ccu_out(i)%num, ccu_out(i)%num_tot, ccu_out(i)%num(ires), ccu_reg(i)%name, ccu_reg(i)%area_ha, ccu_reg(i)%num(ielem1), ccu_reg(i)%num, ccu_reg(i)%num_tot, ccu_reg(i)%num(icha), ccu_cal(ireg)%lum_ha_tot, ccu_cal(ireg)%lum_num_tot, ccu_elem(i)%name, ccu_elem(i)%obtyp, ccu_elem(i)%obtypno, ccu_elem(i)%bsn_frac, ccu_elem(i)%ru_frac, ccu_elem(i)%reg_frac, ccu_reg(ireg)%num_tot, ccu_reg(ireg)%num(icha), ccu_cal(ireg)%num(icha), ccu_elem(ielem1)%obtypno, ccu_cal(ireg)%hru_ha(icha), ccu_elem(ielem1)%ru_frac, ccu_cal(ireg)%area_ha` |
| [sym:hydrograph_module] | `sp_ob, elem_cnt, defunit_num` | `sp_ob%hru, sp_ob%res, sp_ob%chan` |
| [sym:sd_channel_module] | `schsd_d, schsd_m, schsd_y, schsd_a` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ccu_out(i)%num` | When a channel region record has `nspu > 0` in `ch_catunit.def`. | `ccu_out(i)%num` is allocated to the expanded membership length and filled from `defunit_num`, so the region stores explicit element IDs instead of a default all-channel listing. |
| `ccu_out(i)%num_tot` | When a channel region record has `nspu > 0` in `ch_catunit.def`. | `ccu_out(i)%num_tot` is set to the expanded element count returned by `define_unit_elements`, giving the total number of explicit members in that region. |
| `ccu_out(i)%num(ires)` | When the region has no explicit members, i.e. `nspu <= 0` while reading `ch_catunit.def`. | `ccu_out(i)%num(ires)` is assigned channel indices in the fallback case where the region is treated as covering all channels. |
| `db_mx%cha_reg` | After the channel cataloging-unit file has been scanned successfully and the region count `mreg` is known. | `db_mx%cha_reg` is updated to record the number of channel regions available for later allocation and calibration logic. |
| `ccu_reg(i)%num` | When a channel region record has `nspu > 0` in `ch_reg.def`. | `ccu_reg(i)%num` is allocated and filled with the explicit member element numbers returned by `define_unit_elements`. |
| `ccu_reg(i)%num_tot` | When a channel region record has `nspu > 0` in `ch_reg.def`. | `ccu_reg(i)%num_tot` is set to the expanded membership length so the calibration-region list knows how many element IDs it contains. |
| `ccu_reg(i)%num(icha)` | When the region has no explicit members in `ch_reg.def`. | `ccu_reg(i)%num(icha)` is filled with a simple 1-to-`sp_ob%chan` channel listing for the fallback case. |
| `ccu_cal(ireg)%lum_ha_tot` | When `mreg > 0`, before later channel calibration accumulation begins. | `ccu_cal(ireg)%lum_ha_tot` is cleared to zero so later routines can accumulate land-use areas for each region from a known baseline. |
| `ccu_cal(ireg)%lum_num_tot` | When `mreg > 0`, before later channel calibration accumulation begins. | `ccu_cal(ireg)%lum_num_tot` is cleared to zero so later routines can accumulate land-use counts for each region from a known baseline. |
| `ccu_cal(ireg)%num(icha)` | When `ccu_elem(ielem1)` has been loaded and the final per-region mapping loop runs. | `ccu_cal(ireg)%num(icha)` is set to the object number for each member element, converting element IDs into the HRU/object numbering used by calibration logic. |
| `ccu_cal(ireg)%hru_ha(icha)` | When `ccu_elem(ielem1)` has been loaded and the final per-region mapping loop runs. | `ccu_cal(ireg)%hru_ha(icha)` is computed as the element's `ru_frac` times the region area, giving each member's area contribution inside the calibration region. |

## File I/O

<!-- facts:io -->


## Lineage

`ch_read_elements.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ch_read_elements.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_elements' has no extracted documentation comment.
- No resolved lineage commits were available for this procedure span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
