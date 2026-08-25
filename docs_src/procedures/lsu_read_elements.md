---
kind: procedure
symbol: lsu_read_elements
title: lsu_read_elements
status: filled
source_hash: ca311f515cc94224
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title string read from the first line of each input file and discarded
    after header parsing.
  header: Temporary header string read from each file to skip or capture the file's descriptive
    header line before record scanning.
  eof: IO status flag used to detect end-of-file or read failure while scanning the two LSU
    input files.
  imax: Tracks the maximum element index found in ls_unit.ele so lsu_elem can be allocated
    to the correct size.
  nspu: Holds the number of elements listed for the current LSU record in ls_unit.def.
  i_exist: Logical flag from INQUIRE that tells whether the configured input file exists before
    attempting to read it.
  mcal: Unused local counter initialized to zero; it is set but not used in the shown routine
    body.
  mlsu: Number of LSU output units read from ls_unit.def and the bound used to allocate lsu_out
    and related output arrays.
  i: General loop/index variable used to scan LSU output records and LSU element IDs.
  k: Record identifier read from both files before the associated LSU output or element fields
    are loaded.
  isp: Loop index used when reading the list of element counts for one LSU record and when
    expanding them into defunit_num.
  ielem1: Returned count of expanded element IDs from define_unit_elements; used to size lsu_out(i)%num.
uses:
  input_file_module: input_file_module provides the configured file names in_regs%def_lsu
    and in_regs%ele_lsu, so this routine knows which LSU definition files to open.
  maximum_data_module: maximum_data_module stores db_mx, which records the maximum LSU output
    and LSU element counts found here for later allocation checks.
  calibration_data_module: calibration_data_module defines the shared lsu_out and lsu_elem
    arrays that this routine allocates and fills with LSU membership and element metadata
    used by later model setup and calibration/output routines.
  hydrograph_module: hydrograph_module supplies elem_cnt and defunit_num; the LSU definition
    file's element counts are expanded into defunit_num before copying into lsu_out(i)%num.
  output_landscape_module: output_landscape_module provides the LSU-level output arrays that
    are allocated here using the LSU count so later landscape output can store water, nutrient,
    loss, and plant-weather balances per LSU.
---

<!-- facts:header -->

Reads landscape unit definition and element files, then populates LSU output and element arrays used throughout SWAT+ initialization.

## Bottom Line

lsu_read_elements loads the landscape cataloging unit setup from the configured definition files. It first reads ls_unit.def to determine how many LSU groups exist and how many element IDs belong to each group, then uses define_unit_elements to expand those memberships into lsu_out(i)%num and lsu_out(i)%num_tot.

It then reads ls_unit.ele to size and fill lsu_elem with the element name, object type, object number, and basin/region fractions for each LSU element. The routine also records maximum counts in db_mx%lsu_out and db_mx%lsu_elem and allocates the landscape output arrays that depend on the LSU count.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during LSU input initialization after the input file names are available in in_regs. It prepares LSU membership and element metadata that downstream landscape setup and output modules rely on for grouping HRUs and tracking LSU-level balance arrays.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether LSU definition input is available | The routine inquires about the configured LSU definition file and proceeds only if the file exists or the file name is not the null sentinel. |
| 2. Open ls_unit.def and read its header records | It opens ls_unit.def, reads the title, LSU count, and header, and stops the pass if an end-of-file condition is encountered. |
| 3. Allocate LSU output and balance arrays | Using mlsu, it allocates lsu_out and all LSU-level output arrays for water balance, nutrient balance, losses, and plant-weather output. |
| 4. Scan each LSU definition record | For each LSU, it reads the summary record, and if the LSU has subelements, it allocates elem_cnt, backspaces, and rereads the record with the full element-count list. |
| 5. Expand element counts into explicit LSU membership | It calls define_unit_elements to build defunit_num and length ielem1, allocates lsu_out(i)%num to that size, copies the expanded membership, stores the total count, and frees the temporary array. |
| 6. Handle LSUs with no listed elements | If an LSU record has no subelements, it allocates a one-element placeholder array for lsu_out(i)%num instead of an expanded membership list. |
| 7. Record the LSU output maximum | After the LSU loop finishes, it stores the LSU count in db_mx%lsu_out for later allocation and sizing checks. |
| 8. Check whether LSU element input is available | It separately inquires about the LSU element file and proceeds only if that file exists or is not the null sentinel. |
| 9. Open ls_unit.ele and find the maximum element ID | The routine opens ls_unit.ele, reads the title and header, scans element IDs to determine imax, and allocates lsu_elem to that size. |
| 10. Rewind and reread ls_unit.ele data records | It rewinds the file, skips the title and header again, stores the maximum in db_mx%lsu_elem, then reads each element record into lsu_elem(i) after backspacing to reread the full line. |
| 11. Close the LSU element file and return | The file unit is closed and the subroutine returns to its caller after the LSU structures have been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_regs` | `in_regs%def_lsu, in_regs%ele_lsu` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out, db_mx%lsu_elem` |
| [sym:calibration_data_module] | `lsu_out, lsu_elem` | `lsu_out(i)%name, lsu_out(i)%area_ha, lsu_out(i)%num(ielem1), lsu_out(i)%num, lsu_out(i)%num_tot, lsu_out(i)%num(0:0), lsu_elem(i)%name, lsu_elem(i)%obtyp, lsu_elem(i)%obtypno, lsu_elem(i)%bsn_frac, lsu_elem(i)%ru_frac` |
| [sym:hydrograph_module] | `elem_cnt, defunit_num` |  |
| [sym:output_landscape_module] | `ruwb_d, ruwb_m, ruwb_y, ruwb_a, lsu_wb_d, runb_d, runb_m, runb_y, runb_a, ruls_d, ruls_m, ruls_y, ruls_a, rupw_d, rupw_m, rupw_y, rupw_a` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lsu_out(i)%num` | When an LSU definition record lists one or more element counts and define_unit_elements expands them. | lsu_out(i)%num is allocated and filled with the explicit element IDs for LSU i, replacing the temporary counted representation from ls_unit.def. |
| `lsu_out(i)%num_tot` | After define_unit_elements returns the expanded element count for LSU i. | lsu_out(i)%num_tot is set to the total number of explicit element IDs stored in lsu_out(i)%num. |
| `db_mx%lsu_out` | After the routine finishes scanning all LSU definition records in ls_unit.def. | db_mx%lsu_out is updated to the number of LSU output units so later code can allocate and size LSU-level output arrays consistently. |
| `db_mx%lsu_elem` | After the routine finishes scanning all LSU element records in ls_unit.ele. | db_mx%lsu_elem is updated to the maximum LSU element index found in the file so later code knows how large lsu_elem must be. |

## File I/O

<!-- facts:io -->


## Lineage

`lsu_read_elements.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `lsu_read_elements.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'lsu_read_elements' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
