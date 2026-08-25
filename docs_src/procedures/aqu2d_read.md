---
kind: procedure
symbol: aqu2d_read
title: aqu2d_read
status: filled
source_hash: 81c6b493c78052c2
version_label: SWAT+ 62.0.0
locals:
  titldum: Title line buffer read from `aqu_cha.lin` before the routine skips into the table
    data.
  header: Second header line buffer from `aqu_cha.lin`; used to advance past file metadata
    before the data records are scanned or loaded.
  namedum: Temporary name field read while probing each aquifer record's header line before
    the full record is reread.
  eof: IO status flag for reads from unit 107; negative means end-of-file or read failure,
    and the loop uses it to stop scanning and loading.
  imax: Tracks the largest aquifer record index seen in the file, which becomes the number
    of aquifer linkage records to allocate and process.
  nspu: Number of defining-unit entries listed for the current aquifer linkage record; also
    used as the loop bound when expanding element counts.
  i_exist: File-existence test result for `in_link%aqu_cha`, used to decide whether the routine
    should read the file or allocate an empty `aq_ch` array.
  i: Temporary integer read during the first file scan; each value is compared to update `imax`.
  isp: Loop counter for walking through `elem_cnt(1:nspu)` in the expanded aquifer linkage
    record.
  numb: Record number or leading integer field in the full aquifer linkage record; read to
    match the file layout before the aquifer name and element list.
  iaq: Aquifer linkage index read from the data file and used to address the corresponding
    `aq_ch(iaq)` entry.
  iaq_db: Loop counter over the scanned aquifer records from 1 to `imax` during the data-loading
    pass.
  ielem1: Returned by `define_unit_elements` as the total number of expanded element IDs that
    must be allocated into `aq_ch(iaq)%num`.
uses:
  hydrograph_module: This module supplies the shared aquifer linkage containers and counters
    that `aqu2d_read` fills. `sp_ob%aqu` sets the allocation size for `aq_ch`, and the `aq_ch`
    components plus `elem_cnt`/`defunit_num` hold the connection names and expanded element
    memberships that the routine reads and populates.
  input_file_module: This module provides the configured input filename. `in_link%aqu_cha`
    tells `aqu2d_read` which linkage file to open, and the routine treats the value `
  maximum_data_module: '`maximum_data_module` provides `db_mx`, the shared maximum-size bookkeeping
    used to record how many aquifer-link records were found in `aqu_cha.lin`. `aqu2d_read`
    writes `db_mx%aqu2d` so later routines can size or validate aquifer-related data structures
    against the file’s record count.'
---

<!-- facts:header -->

Reads the aquifer-channel linkage file `aqu_cha.lin` and builds the aquifer connection arrays used by the 2-D groundwater connectivity setup. It counts how many aquifer records are present, allocates `aq_ch`, and loads each aquifer's linked element numbers.

## Bottom Line

`aqu2d_read` loads the aquifer-to-element linkage table for the 2-D groundwater setup. It finds how many aquifer linkage records exist, stores that maximum in `db_mx%aqu2d`, and allocates `aq_ch` so each aquifer record can hold its linked element list.

The routine then rereads `aqu_cha.lin`, parses each aquifer entry, expands the defining-unit element groups with `define_unit_elements`, and copies the resulting element numbers into `aq_ch(iaq)%num`. Later hydrology code uses that populated `aq_ch` array to know which model elements belong to each aquifer linkage.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`aqu2d_read` runs inside `hyd_connect` after `hyd_read_connect` has prepared the aquifer connection context and after `sp_ob%aqu` confirms aquifer objects exist. Its output populates the shared aquifer linkage table that downstream groundwater and hydrology routines use to assign elements to aquifers.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the aquifer linkage file is available. | The routine inquires on `in_link%aqu_cha` and, if the file is missing or set to the literal string `"null"`, it skips file processing and allocates a one-element placeholder `aq_ch(0:0)` array. |
| 2. Scan the file to determine the largest aquifer index. | If the file is usable, the routine opens unit 107 on `in_link%aqu_cha`, reads and skips the title and header lines, then loops through the remaining records to find the maximum aquifer number in `imax`. |
| 3. Save the maximum record count and allocate the aquifer table. | The routine stores the discovered maximum in `db_mx%aqu2d` and allocates `aq_ch(sp_ob%aqu)` so there is one aquifer-link record slot for each aquifer object. |
| 4. Rewind the file and restore the header records. | It rewinds unit 107 back to the beginning of `aqu_cha.lin` and rereads the title and header lines so the file is positioned at the first aquifer data record. |
| 5. Read each aquifer entry header. | For each record position up to `imax`, the routine reads the aquifer index, a name placeholder, and the number of unit groups; end-of-file stops the loop early. |
| 6. Expand and store the linked element list when a record has members. | If `nspu` is positive, the routine backs up one record, allocates `elem_cnt`, rereads the full entry including the element counts, calls `define_unit_elements` to build `defunit_num`, allocates `aq_ch(iaq)%num`, copies the expanded element list into it, records the total count in `aq_ch(iaq)%num_tot`, and deallocates `defunit_num`. |
| 7. Close the aquifer linkage file and return. | After all records are processed, the routine closes unit 107 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, aq_ch, elem_cnt, defunit_num` | `sp_ob%aqu, aq_ch(iaq)%name, aq_ch(iaq)%num(ielem1), aq_ch(iaq)%num, aq_ch(iaq)%num_tot` |
| [sym:input_file_module] | `in_link` | `in_link%aqu_cha` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%aqu2d` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%aqu2d` | When `aqu_cha.lin` exists and is not `"null"`, after the initial scan of records completes. | `db_mx%aqu2d` is set to the maximum aquifer index found in the linkage file so the model knows how many aquifer-link records were declared. |
| `aq_ch(iaq)%num` | For each aquifer record with `nspu > 0` after `define_unit_elements` returns. | `aq_ch(iaq)%num` is allocated and filled with the expanded element numbers for that aquifer linkage. |
| `aq_ch(iaq)%num_tot` | For each aquifer record with `nspu > 0` after the expanded list is copied. | `aq_ch(iaq)%num_tot` is set to the total number of element IDs placed into `aq_ch(iaq)%num`. |

## File I/O

<!-- facts:io -->


## Lineage

`aqu2d_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `d70017a` (2025-11-24, "code cleanup of stacked routines, unused routines, added 'end subroutine/functio…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `aqu2d_read.f90` are listed.

- `d70017a` (2025-11-24) — code cleanup of stacked routines, unused routines, added 'end subroutine/function' to some codes to be consistent., remove warnings in code…
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'aqu2d_read' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
