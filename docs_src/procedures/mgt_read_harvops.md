---
kind: procedure
symbol: mgt_read_harvops
title: mgt_read_harvops
status: filled
source_hash: b7c903735b0d99dd
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer for reading and discarding the file title line during
    the initial scan and the second pass through `harv.ops`.
  header: Scratch character buffer for reading and discarding the header line in `harv.ops`;
    it marks the non-data header row before the routine starts counting or loading records.
  eof: I/O status flag from each `read`; values below zero indicate end-of-file, and the loop
    logic uses it to stop scanning or loading.
  imax: Counts how many harvest operation data records were found in `harv.ops`; it is then
    used as the upper bound when allocating and filling `harvop_db`.
  i_exist: Logical flag set by `inquire` to tell whether the configured harvest-operations
    file exists before the routine tries to open it.
  iharvop: Loop counter used on the second pass to load each harvested operation record into
    `harvop_db(iharvop)`.
uses:
  input_file_module: This module provides `in_ops%harv_ops`, the configured path to the harvest-operations
    file. The routine depends on that setting to decide which file to open and whether the
    file is effectively disabled by a `null` name.
  maximum_data_module: This module holds `db_mx%harvop_db`, the shared counter for how many
    harvest-operation records were loaded. Updating it here publishes the file size to the
    rest of the database setup process.
  mgt_operations_module: This module defines the allocatable `harvop_db` array and the `harvest_operation`
    type that stores each parsed record. The routine allocates and fills that shared database,
    so later management code can use the loaded operations.
---

<!-- facts:header -->

Reads the harvest-only management operations database from `harv.ops` into `harvop_db` and records how many entries were loaded. It is part of the database initialization sequence used before management scheduling runs.

## Bottom Line

mgt_read_harvops opens the harvest-operations input file named in `in_ops%harv_ops`, counts the data records after skipping the title and header lines, allocates `harvop_db` to hold those records, then rereads the file and loads each harvest operation into the shared database array.

If the file is missing or set to the literal `null`, the routine still allocates a one-element placeholder array and leaves the harvest-operation count at zero. It always updates `db_mx%harvop_db` so later code knows how many harvest operation records were available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization inside `proc_db`, after the schedule/database file paths have been set up in `input_file_module`. Its output is used later by management operations code that needs the harvest-only operation table and by any routines that rely on `db_mx%harvop_db` to know how many records were loaded.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and buffers | Set the title/header scratch buffers to empty strings, reset `eof` and `imax` to zero, and declare the loop counter and file-existence flag used by the read logic. |
| 2. Check whether the harvest file should be read | Use `inquire` on `in_ops%harv_ops` to test whether the file exists, and if it does not exist or is named `null`, allocate a minimal `harvop_db(0:0)` placeholder instead of reading records. |
| 3. Open and count data rows | Open unit 107 on the configured file, read and skip the title and header lines, then read through the remaining records until end-of-file while incrementing `imax` once per data row. |
| 4. Allocate storage for the loaded records | Allocate the shared harvest-operation database array from index 0 through `imax`, creating enough slots for all records found during the count pass. |
| 5. Rewind and skip the file prologue again | Rewind unit 107 to the start of `harv.ops` and reread the title and header lines so the load pass starts at the first data record. |
| 6. Load each harvest operation record | Loop from 1 to `imax` and read each harvest-operation record directly into `harvop_db(iharvop)`, stopping early only if an end-of-file condition occurs. |
| 7. Close the file and publish the count | Close unit 107 and store the final loaded-record count in `db_mx%harvop_db` so other routines can see how many harvest operations were available. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_ops` | `in_ops%harv_ops` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%harvop_db` |
| [sym:mgt_operations_module] | `harvop_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%harvop_db` | When `harv.ops` exists and is not named `null`, the routine counts its data rows, allocates `harvop_db(0:imax)`, and then fills that array from the file. | `db_mx%harvop_db` is updated to the number of harvest-operation records found in the input file, publishing the loaded database size for downstream management and database routines. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit df07e3f with logic to read harvest-only operations from `harv.ops`, count records, allocate `harvop_db`, rewind, and load the records; the later 39fabde commit only initialized the local variables (`titldum`, `header`, `eof`, and `iharvop`) without changing the file-reading algorithm. The 94b6dec import preserved the same procedure structure and behavior.

- df07e3f added the full `mgt_read_harvops` procedure to read `harv.ops`, count records, allocate `harvop_db`, and store the count in `db_mx%harvop_db`.
- 39fabde changed only local variable initialization, setting default values for `titldum`, `header`, `eof`, and `iharvop` while leaving the read/allocate logic unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'mgt_read_harvops' has no extracted documentation comment.
