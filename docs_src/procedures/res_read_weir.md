---
kind: procedure
symbol: res_read_weir
title: res_read_weir
status: filled
source_hash: 37d5c9394f6c58fa
version_label: SWAT+ 62.0.0
locals:
  titldum: '`titldum` is a scratch character buffer used to read and discard title or placeholder
    lines while counting records and before loading data records.'
  header: '`header` holds the second line of the file, which is read and skipped as a header
    record before the routine counts or loads the actual reservoir weir data.'
  eof: '`eof` captures the `iostat` status from each read so the routine can detect end-of-file
    or input errors and stop scanning or loading safely.'
  imax: '`imax` counts how many reservoir weir data records are present in the file and is
    then used to size `res_weir(0:imax)`.'
  i_exist: '`i_exist` records whether the configured `in_res%weir_res` file exists so the
    routine can fall back to a minimal allocation when the file is missing.'
  ires: '`ires` is the loop counter for loading each reservoir weir record into `res_weir(ires)`
    after the file has been sized.'
uses:
  input_file_module: The routine gets the input-file path from `input_file_module` through
    `in_res%weir_res`, so this module determines which file is opened and whether the routine
    treats the file as configured input.
  maximum_data_module: '`maximum_data_module` provides `db_mx%res_weir`, the shared counter
    that records how many reservoir weir entries were found. That count is needed to size
    the allocation and exposes file size to the rest of the model.'
  reservoir_data_module: '`reservoir_data_module` defines the allocatable `res_weir` array
    that receives the parsed weir records. This is the actual reservoir state other routines
    will use after reading completes.'
---

<!-- facts:header -->

Reads weir-reservoir configuration data from the reservoir weir input file and stores it in shared reservoir state.

## Bottom Line

res_read_weir opens the configured `weir.res` file, checks whether it exists and is not set to `"null"`, counts the data records, and stores that count in `db_mx%res_weir`. It then allocates `res_weir` large enough to hold the records plus index 0.

After sizing storage, it rewinds the file and reads each reservoir-weir record into `res_weir(ires)`. That shared array becomes the in-memory source for later reservoir weir/outflow calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir input initialization, after `in_res%weir_res` has been set in `input_file_module`. Its results matter later when the reservoir module needs the parsed weir geometry/outflow data stored in `res_weir` and the record count in `db_mx%res_weir`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check file availability | The routine resets `eof` and `imax`, then checks whether the configured `in_res%weir_res` file exists. If the file is missing or set to `"null"`, it allocates a minimal `res_weir(0:0)` array instead of reading data. |
| 2. Open the configured reservoir weir file | If the file is available, the routine opens `weir.res` on unit 105 and reads the first record into `titldum` to skip the title line. |
| 3. Read the header and count data records | The routine reads a header line into `header`, then loops through the remaining records, reading each line into `titldum` and incrementing `imax` until end-of-file is reached. |
| 4. Save the record count and allocate storage | After counting the entries, the routine stores the total in `db_mx%res_weir` and allocates `res_weir(0:imax)` so the parsed reservoir weir records can be held in memory. |
| 5. Rewind the file for a second pass | The routine rewinds unit 105 so it can reread the file from the beginning and load the structured records into `res_weir`. |
| 6. Skip title and header again | It rereads the title line into `titldum` and the header line into `header`, using the same file layout as the first pass before it starts loading data records. |
| 7. Load each reservoir weir record | For each record index from 1 to `imax`, the routine reads and discards a line into `titldum`, backs up one record, then reads that record into `res_weir(ires)`. |
| 8. Close the input file and return | After the data load finishes, the routine exits the file-processing block, closes unit 105, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_res` | `in_res%weir_res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_weir` |
| [sym:reservoir_data_module] | `res_weir` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%res_weir` | When `in_res%weir_res` exists and is not `"null"`, after the first scan completes successfully. | `db_mx%res_weir` is updated to the number of reservoir weir data records found in `weir.res`, giving the model a shared count of how many `res_weir` entries were allocated and loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed this routine. The initial addition in `df07e3f` created `res_read_weir` with file existence checking, record counting, allocation, rewinding, and loading from `weir.res`. Commit `39fabde` initialized local variables `titldum`, `header`, `eof`, `imax`, and `ires` with default values. Commit `889136d` only corrected a documentation typo in the comment block from “occuring” to “occurring”; the executable logic was unchanged.

- df07e3f added the full file-driven weir input workflow, including the `in_res%weir_res` existence check, `db_mx%res_weir` sizing, and loading of `res_weir(ires)`.
- 39fabde changed local variable initialization so the scratch strings and counters start from known default values before the reads and loops execute.
- 889136d updated only the embedded comment text and did not change runtime behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_weir' has no extracted documentation comment.
