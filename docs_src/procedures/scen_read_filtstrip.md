---
kind: procedure
symbol: scen_read_filtstrip
title: scen_read_filtstrip
status: filled
source_hash: 521f67c52a2c5a07
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the file title line before the
    header and data records are processed.
  header: Scratch character buffer used to read and discard the file header line; it is read
    twice, once during the counting pass and again after rewind before loading records.
  eof: I/O status flag for each READ; zero means reading can continue, and a negative value
    is used to detect end-of-file and stop the scan.
  imax: Counts how many filter strip operation records are present in the input file, and
    is then used as the upper bound when allocating `filtstrip_db`.
  i_exist: Logical result of the file existence inquiry for `in_str%fstrip_str`; it controls
    whether the routine reads the file or falls back to allocating a zero-length database.
  ifiltop: Loop counter used to read each filter strip operation record into `filtstrip_db(1:imax)`
    after the file is rewound.
uses:
  input_file_module: This module supplies `in_str%fstrip_str`, the configured path to the
    filter strip input file. The routine cannot locate or open the database without that file-name
    setting.
  maximum_data_module: This module holds `db_mx%filtop_db`, the shared count of loaded filter
    strip operations. The routine updates it so later code can know how many entries were
    read.
  mgt_operations_module: This module defines the allocatable `filtstrip_db` array that receives
    the parsed filter strip operation records. The routine sizes and fills that shared database.
---

<!-- facts:header -->

Reads the filter strip operations database from `filterstrip.str` and loads it into `filtstrip_db`.

## Bottom Line

`scen_read_filtstrip` is a file-reader routine for the filter strip management database. It checks whether the configured structural input file exists, counts the number of operation records it contains, allocates `filtstrip_db` to hold them, and then reads each record into module state.

The routine also records the final record count in `db_mx%filtop_db`. That count tells the rest of the model how many filter strip operation entries were loaded and available for later management-processing steps.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the database-loading phase, when `proc_db` is assembling management and structural input files. It depends on `input_file_module` for the configured filename, and its results feed later management behavior that uses the populated `filtstrip_db` array and `db_mx%filtop_db` count.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and scan prerequisites | Initializes the EOF and record-count variables, then checks whether the configured filter strip file exists using `inquire` on `in_str%fstrip_str`. |
| 2. Allocate an empty database when no file is available | If the file is missing or set to the sentinel name `"null"`, allocates `filtstrip_db(0:0)` so the shared database exists but contains no operations. |
| 3. Open the file and count data records | Opens `filterstrip.str`, reads past the title and header lines, then loops through the remaining records to count how many filter strip operations are present in the file. |
| 4. Size the shared operation array | Allocates `filtstrip_db(0:imax)` using the counted record total so the array can hold every loaded operation plus the zero element used by the code's indexing convention. |
| 5. Rewind and reload the records | Rewinds the file, skips the title and header again, then reads each filter strip operation into `filtstrip_db(ifiltop)` for `ifiltop = 1..imax`. |
| 6. Publish the loaded count and close the file | Stores the final record count in `db_mx%filtop_db` and closes unit 107 for `filterstrip.str`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_str` | `in_str%fstrip_str` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%filtop_db` |
| [sym:mgt_operations_module] | `filtstrip_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%filtop_db` | After the file scan completes, whether the file existed or was set to "null". | `db_mx%filtop_db` is set to the number of filter strip operation records found in `filterstrip.str`; this publishes the loaded database size for later routines. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed this routine. The initial addition in 94b6dec created `scen_read_filtstrip` with the two-pass count-and-load pattern, file existence check, allocation of `filtstrip_db`, and storage of the record count in `db_mx%filtop_db`. Commit 39fabde did not change the algorithm, but initialized the local variables `titldum`, `header`, `eof`, `imax`, and `ifiltop` to default values.

- 94b6dec introduced the routine and its full filter-strip file loading logic, including the `inquire`/`open`/`rewind` workflow and `db_mx%filtop_db` assignment.
- 39fabde only changed local variable initialization and did not alter the file-reading behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'scen_read_filtstrip' has no extracted documentation comment.
