---
kind: procedure
symbol: res_read_init
title: res_read_init
status: filled
source_hash: 5e80c879583f5b1f
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character variable used to read and discard title or blank/header lines
    while counting and then loading records from `initial.res`.
  header: Scratch character variable used to capture the file header line after the title
    line so the routine can skip non-data text before reading initialization records.
  eof: I/O status flag for each read from `initial.res`; negative values signal end-of-file
    and stop the scan or load loop.
  imax: Running count of how many reservoir initialization data records were found in `initial.res`;
    this becomes the array bound and the stored record count.
  i_exist: Logical flag set by `inquire` to indicate whether the configured initial-reservoir
    file exists on disk.
  ires: Loop counter for the second pass through `initial.res` when the routine reads each
    parsed record into `res_init_dat_c(ires)`.
uses:
  basin_module: This module supplies the configured path for the reservoir initial-condition
    file. The routine uses `in_res%init_res` both to test whether the file should be read
    and to open `initial.res` for the scan and load passes.
  input_file_module: This module defines the reservoir input-file name string that controls
    which file `res_read_init` reads. Without `in_res%init_res`, the routine would not know
    which initial reservoir file to scan or load.
  maximum_data_module: This module holds `db_mx%res_init`, the shared count of reservoir initialization
    records. `res_read_init` computes that count and stores it here so later reservoir code
    can size loops and arrays consistently.
  reservoir_data_module: This module provides the shared reservoir initialization arrays and
    the character-based record type. `res_read_init` allocates `res_init`, `wet_init`, and
    `res_init_dat_c`, then fills `res_init_dat_c` from the file.
---

<!-- facts:header -->

Reads the reservoir initial-conditions file `initial.res`, counts how many reservoir records it contains, and loads those records into shared reservoir initialization arrays. It also records the number of entries in `db_mx%res_init` so later reservoir processing can size and iterate over the data.

## Bottom Line

res_read_init is the reservoir initial-file loader. It checks whether `in_res%init_res` points to a usable file, scans the file once to count data records, stores that count in `db_mx%res_init`, and allocates the reservoir initialization arrays to match.

If the file exists, it rewinds and reads each initialization record into `res_init_dat_c(ires)` for later use by reservoir initialization logic. If the file is missing or set to `null`, it still allocates minimal `res_init` and `wet_init` storage so downstream code has defined arrays to work with.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir setup in `proc_res`, after the other reservoir readers have been called and before later reservoir initialization and chemistry processing. Its result is the populated reservoir initial-condition storage and the record count in `db_mx%res_init`, which later reservoir logic uses to size and traverse initialization data.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize scan state and check file availability | Reset `eof` and `imax`, then inquire whether `in_res%init_res` exists and is not the literal string `null`. |
| 2. Allocate minimal arrays when no input file is usable | If the file is missing or disabled, allocate `res_init(0:0)` and `wet_init(0:0)` so downstream code still sees defined reservoir arrays. |
| 3. Open the reservoir initial file | Begin the read pass by opening unit 105 on `in_res%init_res`. |
| 4. Skip title and header lines | Read and discard the title and header lines, stopping early if end-of-file is hit. |
| 5. Count reservoir initialization records | Loop through the remaining file lines, reading one line at a time into `titldum` and incrementing `imax` for each successful data line. |
| 6. Store the record count in shared maximum-data state | Copy the counted record total into `db_mx%res_init` for later use by reservoir routines. |
| 7. Allocate storage sized to the counted records | Allocate `res_init`, `wet_init`, and `res_init_dat_c` over `0:imax` so each reservoir entry has storage. |
| 8. Rewind the file for a second pass | Rewind unit 105 so the file can be read again from the beginning. |
| 9. Skip title and header again | Read and discard the title and header lines again before loading the actual records. |
| 10. Read each initialization record into character storage | Loop from 1 to `db_mx%res_init`, reading each record into `res_init_dat_c(ires)` and stopping early if end-of-file occurs. |
| 11. Close the file and finish | Close unit 105, exit the outer loop, and return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `in_res` | `in_res%init_res` |
| [sym:input_file_module] | `in_res` | `in_res%init_res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_init` |
| [sym:reservoir_data_module] | `res_init, wet_init, res_init_dat_c` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%res_init` | When `initial.res` exists and is not `null`, after the first pass through the data lines completes. | `db_mx%res_init` is set to the number of reservoir initialization records found in `initial.res`, and that count drives array allocation and the second read pass. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f with the full reservoir initial-file scan, allocation, rewind, and load logic. Commit 94b6dec preserved the same behavior while importing the source into the current tree, and 39fabde only initialized the local counters and scratch strings (`titldum`, `header`, `eof`, `imax`, `ires`) without changing the file-reading algorithm.

- df07e3f added `res_read_init` as a new routine that scans `initial.res`, allocates reservoir initialization arrays, stores the record count in `db_mx%res_init`, and loads records into `res_init_dat_c`.
- 94b6dec carried the same reservoir initial-file logic into the later source snapshot without changing the routine's behavior.
- 39fabde initialized the local scratch variables used by the file scan and load passes, but did not alter the read/allocate workflow.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_init' has no extracted documentation comment.
