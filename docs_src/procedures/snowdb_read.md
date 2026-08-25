---
kind: procedure
symbol: snowdb_read
title: snowdb_read
status: filled
source_hash: c6b03866d35c7b0b
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer for the title and data-line skips. It is read from the
    first line and then reused while counting and rereading the file so the header line structure
    can be bypassed.
  header: Scratch character buffer for the database header line. The routine reads it to move
    past the file header before counting and loading snow records.
  eof: I/O status flag from each `read` on unit 107. A value below zero means end-of-file
    was reached, and the routine uses that to stop counting or reading.
  imax: Counter for the number of snow property records found in the file. It is incremented
    during the scan pass and then used to size `snodb` and to set `db_mx%sno`.
  i_exist: Logical flag returned by `inquire` to tell whether the configured snow database
    file exists. It gates whether the routine scans the file or falls back to an empty allocation.
  msno: Reset-to-zero working integer that is not used in the visible body of the routine.
    The source initializes it, but no later statement in this subroutine references it.
  isno: Loop index used when loading the snow records from `snodb(1)` through `snodb(imax)`.
    It advances through the allocated array while reading each record.
uses:
  input_file_module: This module supplies `in_parmdb%snow`, the configured path to the snow
    database file. Without that shared input-file setting, the routine would not know which
    `.sno` file to open.
  maximum_data_module: This module holds `db_mx%sno`, the shared count of snow property records.
    `snowdb_read` writes that count so other parts of the model can know how many snow database
    entries are available.
  hru_module: This module owns the allocatable `snodb` array that receives the snow parameter
    records. The routine allocates and fills that shared database so later HRU and snow-process
    code can access the parsed properties.
---

<!-- facts:header -->

Reads the snow property database from `snow.sno` into the shared `snodb` array and records how many snow parameter records were found.

## Bottom Line

This routine loads the snow database file named in `in_parmdb%snow`. It first checks whether the file exists and is not set to the literal string `null`; if the file is missing or disabled, it allocates a minimal `snodb(0:0)` array and stops after recording zero snow records.

When the file is present, it opens unit 107 on `snow.sno`, skips the title and header lines, counts the remaining data records to determine `imax`, rewinds the file, allocates `snodb(0:imax)`, then reads each snow parameter record into `snodb(isno)`. Finally it stores the count in `db_mx%sno` for later model use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model input-reading phase, called by `proc_read` after other database readers have prepared their own shared state. Its result is the in-memory snow database and record count, which later snow-related HRU processing depends on when using `snodb` and `db_mx%sno`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize working state | Initialize the scratch strings, EOF flag, and counters to known values before any file access begins. |
| 2. Check whether the snow database file is available | Use `inquire` on `in_parmdb%snow` to see whether the configured snow file exists, and if it is missing or set to `null`, allocate a minimal `snodb(0:0)` array instead of reading records. |
| 3. Open the snow file and skip the file title and header | Open unit 107 on `in_parmdb%snow`, read the first two lines into scratch variables, and stop early if end-of-file is encountered. |
| 4. Count snow records in the file | Loop through the remaining lines, reading each line into `titldum` and incrementing `imax` until end-of-file is reached. |
| 5. Rewind and prepare for data loading | Rewind unit 107, skip the title and header again, and allocate `snodb(0:imax)` using the record count found in the scan pass. |
| 6. Read snow parameter records into shared storage | Loop over record indices from 1 through `imax`, reading each snow database record into `snodb(isno)` and stopping early if an I/O error or end-of-file occurs. |
| 7. Close the file and publish the count | Exit the file-processing loop, close unit 107, and store the final record count in `db_mx%sno` for later routines. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_parmdb` | `in_parmdb%snow` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%sno` |
| [sym:hru_module] | `snodb` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%sno` | After the file scan and load logic finishes, including the missing-file branch that leaves `imax` at zero. | `db_mx%sno` is assigned the final number of snow database records found in `snow.sno`, so downstream code can know how many snow property entries were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in commit `df07e3f` with the initial snow-database reader logic. Commit `94b6dec` preserved that logic while bringing in the same source from Bitbucket, and `39fabde` only initialized the local scalars (`titldum`, `header`, `eof`, `imax`, `msno`, `isno`) and set their starting values explicitly; the file-reading control flow and `db_mx%sno = imax` behavior remained the same.

- df07e3f introduced the `snowdb_read` subroutine to scan `snow.sno`, allocate `snodb`, and publish the record count.
- 94b6dec carried the same reader logic forward unchanged in the imported source snapshot.
- 39fabde changed only local variable initialization, reducing reliance on implicit defaults without changing the reading algorithm.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'snowdb_read' has no extracted documentation comment.
