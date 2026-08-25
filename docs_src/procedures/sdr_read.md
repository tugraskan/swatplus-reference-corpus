---
kind: procedure
symbol: sdr_read
title: sdr_read
status: filled
source_hash: fdcb0e17bb1b0f77
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary text buffer used to read and discard the title line and then the per-record
    leading identifier field while scanning and loading `tiledrain.str`.
  header: Temporary text buffer used to read and discard the file header line before the data
    records are counted and loaded.
  eof: I/O status flag for each read; it is tested for end-of-file or read failure while scanning
    and loading records from `tiledrain.str`.
  imax: Counts how many subsurface drainage records were found in the file so the routine
    can allocate `sdr(0:imax)` and store the total in `db_mx%sdr`.
  i_exist: Logical flag returned by `inquire` to decide whether the configured drainage file
    exists before attempting to open it.
  isdr: Loop counter used when reading each drainage record from the file into `sdr(isdr)`.
uses:
  input_file_module: This module supplies `in_str%tiledrain_str`, the configured filename
    that tells `sdr_read` which structural drainage database to open. Without that shared
    input-file setting, the routine would not know where to read the drainage definitions
    from.
  maximum_data_module: This module provides `db_mx%sdr`, the shared count of subsurface drainage
    records. `sdr_read` updates it so other database readers and later model logic can know
    how many drainage types were loaded.
  hru_module: This module owns the allocatable `sdr` array that stores the loaded `subsurface_drainage_parameters`
    records. `sdr_read` allocates and fills that shared state so HRU-related code can access
    the drainage definitions later.
---

<!-- facts:header -->

Reads the subsurface drainage database from `tiledrain.str` into the HRU `sdr` array. It first counts records to size storage, then rewinds and loads each drainage definition.

## Bottom Line

sdr_read is a database reader for subsurface drainage settings. It checks the configured `tiledrain.str` input, counts how many drainage records are present, allocates `hru_module::sdr` to match, and then reads each record into that shared array.

If the file is missing or the configured name is `null`, the routine still creates a one-element placeholder `sdr(0:0)` and records zero available drainage types in `db_mx%sdr`. That lets later code rely on the shared array and on the stored count even when no drainage definitions are supplied.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization in `proc_db`, after the management-operation readers and before the other structural/scenario readers. Its results establish the shared subsurface drainage definitions and record count that later HRU and structural processing depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check whether the drainage file is available. | Reset the EOF and record counter state, then inquire whether `in_str%tiledrain_str` exists. If the file is missing or the configured name is `null`, allocate a minimal `sdr(0:0)` placeholder instead of reading data. |
| 2. Open the drainage database and begin a counting pass. | Enter the file-processing block and open unit 107 on the configured drainage file so the routine can inspect its contents. |
| 3. Skip the title and header lines. | Read the first two records into temporary text buffers and stop if an end-of-file condition is encountered before the expected data section. |
| 4. Count the number of drainage records. | Loop through the remaining records, reading each line into `titldum` and incrementing `imax` until end-of-file is reached. |
| 5. Allocate shared storage for all records. | Allocate the allocatable HRU drainage array from index 0 through the counted maximum so it can hold every drainage definition. |
| 6. Rewind the file and return to the start. | Rewind unit 107 so the file can be reread from the beginning for actual data loading. |
| 7. Skip the title and header again after rewinding. | Read and discard the title and header lines a second time, again stopping early if the file ends unexpectedly. |
| 8. Load each drainage record into the shared array. | Loop from 1 to `imax`, reading each subsurface drainage record into `sdr(isdr)` and stopping early if a read error or end-of-file occurs. |
| 9. Exit the file-processing block and save the record count. | Leave the open-file block, store the final record count in `db_mx%sdr`, and close unit 107. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_str` | `in_str%tiledrain_str` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%sdr` |
| [sym:hru_module] | `sdr` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%sdr` | When `tiledrain.str` is missing, named `null`, or after counting/loading completes for a present file. | `db_mx%sdr` is set to the final number of subsurface drainage records found in the input file, or left as zero when no file is available. This gives the rest of the model a shared count of how many drainage systems were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

`sdr_read` was added in df07e3f with the initial file-reading logic for subsurface drainage definitions. In 94b6dec, the routine was carried forward unchanged in behavior while the source file was imported into the newer codebase. In 39fabde, only local variables were initialized at declaration (`titldum`, `header`, `eof`, `imax`, `isdr`), with matching reset assignments retained below; the file I/O and record-loading logic were not changed.

- df07e3f introduced the full `sdr_read` routine: file existence check, counting pass, allocation of `sdr(0:imax)`, rewind, record loading, and `db_mx%sdr` update.
- 39fabde only initialized local variables at declaration and did not change the file-reading algorithm or shared-state updates.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'sdr_read' has no extracted documentation comment.
