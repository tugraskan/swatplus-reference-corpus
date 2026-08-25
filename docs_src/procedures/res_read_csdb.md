---
kind: procedure
symbol: res_read_csdb
title: res_read_csdb
status: filled
source_hash: 0c400a19ab994028
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard title or label lines from `cs_res`,
    and also to probe the start of each data record while counting or loading entries.
  header: Holds the section header line read from `cs_res` so the routine can skip to and
    validate the database body before counting or loading records.
  i: Loop counter used to skip the 12 non-data lines in the file header on both passes through
    `cs_res`.
  eof: IOSTAT status flag used after each read to detect end-of-file or read failure while
    scanning and loading `cs_res`.
  imax: Counts how many reservoir constituent records are found in `cs_res`; this becomes
    the upper bound for allocating `res_cs_data` and is copied to `db_mx%res_cs`.
  i_exist: Logical flag from `inquire` that says whether the `cs_res` file is present before
    any attempt is made to open it.
  ires: Loop counter for the second pass through `cs_res` that indexes each constituent record
    as it is read into `res_cs_data`.
uses:
  input_file_module: The routine uses `in_res%nut_res` as a switch to decide whether reservoir
    nutrient-related input is enabled. If it is `"null"`, the routine skips loading the constituent
    database and creates only the minimal placeholder array.
  maximum_data_module: The routine writes the number of constituent records it found into
    `db_mx%res_cs`. That shared maximum-data value is how later reservoir routines know the
    size of the loaded constituent database.
  reservoir_data_module: This module provides the allocatable reservoir constituent database
    array that the routine sizes and fills from `cs_res`; without it there would be no shared
    storage for the parsed records.
  res_cs_module: This module defines the `reservoir_cs_data` derived type and the shared `res_cs_data`
    allocatable array. The routine allocates that array and reads each file record directly
    into one `reservoir_cs_data` element per entry.
---

<!-- facts:header -->

Reads the reservoir constituent database file `cs_res` into `res_cs_data`, after first counting how many records it contains. It also stores that record count in `db_mx%res_cs` so the reservoir constituent database can be sized and used later in the reservoir setup.

## Bottom Line

This subroutine loads reservoir water-quality constituent data from the `cs_res` text file. It first checks whether the file exists and whether reservoir nutrient input is enabled, then scans the file to count how many constituent records are present, allocates `res_cs_data` to match, and reads each record into the array.

The count is saved in `db_mx%res_cs`, which lets the rest of the reservoir-processing workflow know how many constituent database entries were found. If the file is missing or `in_res%nut_res` is set to `"null"`, it allocates a minimal `res_cs_data(0:0)` array instead of loading records.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir initialization, inside `proc_res`, after the other reservoir database readers have been called. Its results populate the shared constituent database and its size count, which later reservoir logic depends on when building and using reservoir water-quality state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and inspect file availability | The routine resets `eof` and `imax`, then checks whether `cs_res` exists and whether reservoir nutrient input is enabled through `in_res%nut_res`. If the file is missing or the feature is disabled, it allocates a minimal `res_cs_data(0:0)` placeholder and skips loading. |
| 2. Open `cs_res` and skip the file preamble | The routine opens unit 105 on `cs_res`, reads and discards the title lines, and skips the 12-line header block before attempting to reach the database section. |
| 3. Count constituent records | After reading the section header, the routine loops through the remaining lines until end-of-file, incrementing `imax` for each record-like line it encounters. It then stores that count in `db_mx%res_cs`. |
| 4. Allocate storage for the database records | Using the record count just determined, the routine allocates `res_cs_data(0:imax)` so there is one slot for each constituent record plus the zero index used by the array convention. |
| 5. Rewind and return to the start of the file | The routine rewinds unit 105 and repeats the same title and header skipping sequence so the file pointer is positioned at the database section again, this time for the actual read pass. |
| 6. Load each record into shared state | For each record index from 1 to `imax`, the routine reads a line to advance to the record, backs up one record, and then reads the full derived-type record into `res_cs_data(ires)`. The loop stops early if a read error or end-of-file occurs. |
| 7. Close the file and return | After finishing the load pass, the routine closes unit 105 and returns to its caller with the database array and record count updated in shared module state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_res` | `in_res%nut_res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_cs` |
| [sym:reservoir_data_module] | `res_cs_data` |  |
| [sym:res_cs_module] | `res_cs_data` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%res_cs` | When `cs_res` exists and `in_res%nut_res` is not `"null"`, after the scan pass determines `imax`. | `db_mx%res_cs` is set to the number of reservoir constituent database records found in `cs_res`, so downstream reservoir routines know how many entries were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f with the two-pass `cs_res` reader, placeholder allocation when input is absent, and the `db_mx%res_cs` count. Commit 35b029c only removed trailing blank lines at the end of the file. Commit 94b6dec added the same routine from upstream with the same logic. Commit 39fabde initialized the local variables (`titldum`, `header`, `i`, `eof`, `imax`, `ires`) to safe default values but did not change the file-reading algorithm.

- df07e3f added `res_read_csdb` as a two-pass reservoir constituent database reader that counts records, allocates `res_cs_data`, and loads the file contents into shared state.
- 39fabde changed only local variable initialization in `res_read_csdb`, reducing uninitialized-state risk without changing the parsing flow.
- 35b029c made a non-functional formatting change by removing extra blank lines at the end of the procedure.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_csdb' has no extracted documentation comment.
- The routine uses `in_res%nut_res == 'null'` as a feature gate; the exact reservoir workflow semantics are inferred from surrounding code, not from a dedicated comment.
- algorithm_steps revised: expanded the scan/load phases into separate steps and aligned source_lines with the visible numbered source block.
