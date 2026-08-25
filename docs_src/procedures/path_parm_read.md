---
kind: procedure
symbol: path_parm_read
title: path_parm_read
status: filled
source_hash: 4dc09d70ca22653c
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary text buffer used to read and skip the file title line and per-record
    leading tokens while counting and loading pathogen records.
  header: Temporary text buffer used to read the header line after the title line on the pathogen
    parameter file.
  ibac: Loop counter for walking through each pathogen record while loading the allocated
    database array.
  eof: I/O status flag from `read` statements; it detects end-of-file or read failure so the
    routine can stop scanning or loading.
  imax: Counter that accumulates the number of pathogen data records found during the first
    pass through the file; it becomes the allocation size and the stored maximum count.
  i_exist: Logical flag set by `inquire` to tell whether the configured pathogen parameter
    file exists before attempting to open it.
uses:
  input_file_module: This module provides `in_parmdb%pathcom_db`, the configured filename
    for the pathogen parameter database. The routine depends on that value to decide which
    file to open and whether the input is disabled by the sentinel name `null`.
  pathogen_data_module: '`path_db` is the allocatable pathogen database array that this routine
    creates and fills. Its contents become the in-memory pathogen parameter records used by
    later pathogen handling.'
  maximum_data_module: '`db_mx%path` stores the number of pathogen records discovered in the
    file. The routine writes that count so other code can know how many `path_db` entries
    were loaded.'
---

<!-- facts:header -->

Reads the pathogen parameter database file and loads all pathogen records into `path_db`.

## Bottom Line

`path_parm_read` checks whether the configured pathogen database file exists, counts the data records in it, and allocates `path_db` to match. It uses the path stored in `in_parmdb%pathcom_db`, which defaults to `pathogens.pth`.

If the file is present, the routine rewinds and rereads it record by record, storing each pathogen entry into `path_db(1:db_mx%path)` and updating `db_mx%path` to the number of records found. That count and array are then available to later database setup and pathogen-related model code.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization in `proc_db`, after other parameter readers and before later management and simulation setup. Its output, `path_db` plus `db_mx%path`, is needed for downstream pathogen database access and any model behavior that uses pathogen parameters.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Verify the configured pathogen file | The routine checks whether `in_parmdb%pathcom_db` exists and whether it is the sentinel value `"null"`. If the file is unavailable or disabled, it allocates a one-element placeholder `path_db(0:0)` and skips loading real records. |
| 2. Open and count data records | When the file is present, the routine opens unit 107 on the pathogen database file, reads past the title and header lines, then loops through the remaining records to count how many pathogen entries are present. The count is accumulated in `imax`. |
| 3. Store the database size | The routine copies the discovered record count into `db_mx%path` and allocates `path_db(0:imax)` so the pathogen database array matches the file size. |
| 4. Rewind and skip file headers again | The file is rewound to the beginning, and the title and header lines are read again so the routine can start a second pass from the first data record. |
| 5. Load each pathogen record | The routine loops from 1 to `db_mx%path`, reads and backs up one record to position on the current data line, and then reads that line into `path_db(ibac)`. This fills the allocatable pathogen database with structured records. |
| 6. Close the input file | After loading completes, the routine closes unit 107 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_parmdb` | `in_parmdb%pathcom_db` |
| [sym:pathogen_data_module] | `path_db` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%path` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%path` | When `in_parmdb%pathcom_db` exists and is not `"null"`, the routine counts the file records and assigns `db_mx%path = imax`. | `db_mx%path` becomes the number of pathogen parameter records found in the input file, which is then used to size the `path_db` allocation and bound the load loop. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `path_parm_read`. The initial addition in `df07e3f` introduced the subroutine, its file existence check, the two-pass read of the pathogen parameter file, allocation of `path_db`, and the assignment to `db_mx%path`. Commit `39fabde` only initialized the local variables (`titldum`, `header`, `ibac`, `eof`, and `imax`) to default values; the file-reading algorithm itself was unchanged.

- df07e3f added the full pathogen database reader: file existence check, two-pass counting/loading logic, allocation of `path_db`, and storage of the record count in `db_mx%path`.
- 39fabde changed local variable initialization by setting `titldum` and `header` to empty strings and `ibac`, `eof`, and `imax` to zero before use.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'path_parm_read' has no extracted documentation comment.
