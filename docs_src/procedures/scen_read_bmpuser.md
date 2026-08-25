---
kind: procedure
symbol: scen_read_bmpuser
title: scen_read_bmpuser
status: filled
source_hash: 149f7ffbc3988db1
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the title line and the per-record
    first field during the file scan and reload passes.
  header: Scratch character buffer used to read and discard the file header line after the
    title line.
  eof: IOSTAT status flag for each read; negative values signal end-of-file or read failure,
    and zero means the read succeeded.
  imax: Counts how many BMP user operation records are present in the file, then becomes the
    upper bound used to allocate `bmpuser_db(0:imax)`.
  i_exist: Logical flag set by `inquire` to tell the routine whether the configured BMP user
    file is present on disk.
  ibmpop: Loop counter used to fill `bmpuser_db` entries one by one after the file has been
    rewound.
uses:
  input_file_module: This module provides `in_str%bmpuser_str`, the configured pathname for
    the BMP user operations file. The routine uses that string both to test file presence
    and to open the file for reading.
  maximum_data_module: This module owns `db_mx%bmpuserop_db`, the shared maximum/count field
    that records how many BMP user operation records were loaded. Other database readers and
    later initialization code can use that count to know the available size of `bmpuser_db`.
  mgt_operations_module: This module defines the allocatable `bmpuser_db` array that receives
    the parsed user BMP operation records. The routine allocates and fills that shared database
    so the management-operations code can use the loaded entries later.
---

<!-- facts:header -->

Reads the user BMP operation database from `bmpuser.str` into `bmpuser_db` and records how many entries were found. It is a small file-loader used during database initialization.

## Bottom Line

`scen_read_bmpuser` is a database reader for the user-defined upland BMP/CP removal operations file. It checks whether `in_str%bmpuser_str` exists, counts the number of data records in `bmpuser.str`, allocates `bmpuser_db` to fit, then rereads the file and loads each record into `mgt_operations_module` storage.

The routine also stores the final record count in `db_mx%bmpuserop_db`, which lets later code know how many user BMP operation entries are available. If the configured file is missing or set to the literal string `"null"`, it allocates a minimal `bmpuser_db(0:0)` and leaves the count at zero.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database setup inside `proc_db`, after earlier management database readers and before later database readers such as `readpcom`. Its result is needed by the management-operations database because it loads the shared `bmpuser_db` array and publishes the record count in `db_mx%bmpuserop_db`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and status buffers | Sets the scratch strings, EOF status, file-count variable, existence flag, and loop counter up front, and resets `imax` to zero before any file work begins. |
| 2. Test whether the configured BMP user file exists | Uses `inquire` on `in_str%bmpuser_str` to determine whether the file is available; if it is missing or explicitly set to `null`, it allocates a minimal `bmpuser_db(0:0)` and skips loading records. |
| 3. Open the file and scan the title and header | Opens `bmpuser.str` on unit 107, reads the title line into `titldum`, then reads the header line into `header`, exiting early if either read reaches end-of-file. |
| 4. Count data records in a first pass | Loops through the remaining lines of the file, reading each record into `titldum` and incrementing `imax` for every successful data line until EOF is reached. |
| 5. Allocate the database array to the counted size | Allocates `bmpuser_db(0:imax)` so the management-operation database has room for the title/header slot plus all counted records. |
| 6. Rewind the file for a second read pass | Repositions unit 107 back to the beginning of `bmpuser.str` so the file can be reread from the top after allocation. |
| 7. Reread and discard title and header | Reads the title and header again into the scratch buffers, stopping if EOF is encountered before the data section begins. |
| 8. Load each operation record into shared state | Iterates from 1 to `imax` and reads each BMP user operation record directly into `bmpuser_db(ibmpop)`, stopping early if a read fails. |
| 9. Publish the final record count and close the file | Exits the file-processing loop, stores `imax` in `db_mx%bmpuserop_db`, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_str` | `in_str%bmpuser_str` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%bmpuserop_db` |
| [sym:mgt_operations_module] | `bmpuser_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%bmpuserop_db` | After the file existence test succeeds and the file has been scanned or, if missing, after the minimal array is allocated. | `db_mx%bmpuserop_db` is set to the number of BMP user operation records found in `bmpuser.str` so other code can know how many entries were loaded into `bmpuser_db`. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in commit df07e3f with the full file-reading logic for `bmpuser.str`. Commit 94b6dec carried that same implementation forward into the next source snapshot, and commit 39fabde only initialized local variables (`titldum`, `header`, `eof`, `imax`, and `ibmpop`) without changing the file-processing flow.

- df07e3f introduced `scen_read_bmpuser` as a new subroutine that opens `bmpuser.str`, counts records, allocates `bmpuser_db`, rereads the file, loads the records, stores `db_mx%bmpuserop_db`, and closes unit 107.
- 39fabde changed local variable initialization by assigning default values to `titldum`, `header`, `eof`, `imax`, and `ibmpop`; the reader logic and stored results remained the same.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'scen_read_bmpuser' has no extracted documentation comment.
