---
kind: procedure
symbol: mgt_read_puddle
title: mgt_read_puddle
status: filled
source_hash: ccf535b6958c2d9f
version_label: SWAT+ 62.0.0
locals:
  ic: Loop counter used to step through `pudl_db` records while reading the file into memory.
  titldum: Temporary string buffer used to read and discard the first title line, then the
    first line again after rewinding.
  header: Temporary string buffer used to read and discard the file header line before counting
    or loading data records.
  eof: I/O status flag for `read` statements; it is tested for end-of-file or read failure
    while scanning and loading `puddle.ops`.
  imax: Counts how many puddle-operation data records are present in `puddle.ops`; that count
    is then used to allocate `pudl_db(0:imax)` and stored in `db_mx%pudl_db`.
  i_exist: Logical flag from `inquire` that tells the routine whether `puddle.ops` exists
    before trying to open and read it.
uses:
  maximum_data_module: '`db_mx` is the shared maximum-size bookkeeping structure from `maximum_data_module`.
    This routine writes `db_mx%pudl_db` so the rest of the model can see how many puddle-operation
    records were loaded.'
  mgt_operations_module: '`pudl_db` is the allocatable puddle-operation database in `mgt_operations_module`.
    This routine allocates it and fills its elements because the loaded puddling operations
    must be available to management code after initialization.'
---

<!-- facts:header -->

Reads the puddling management operations file `puddle.ops` into the `pudl_db` database and records how many entries were loaded. It is part of the database initialization sequence run by `proc_db` before later management simulation uses the puddle operation data.

## Bottom Line

`mgt_read_puddle` is a file reader for the puddling operations database. It checks whether `puddle.ops` exists, scans the file to count how many puddle operation records are present, allocates `pudl_db` to fit that count, then rewinds and loads each record into the `mgt_operations_module` state.

After loading, it stores the record count in `db_mx%pudl_db`. That maximum-data value lets the model know how many puddle-operation entries were available for downstream management processing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `proc_db` while the model is reading management scheduling and data files. `proc_db` prepares the shared management modules, and later management behavior depends on the populated `pudl_db` array and the recorded maximum count in `db_mx%pudl_db`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and status flags | The routine starts with zeroed loop and end-of-file controls (`ic`, `eof`, `imax`) and a logical existence flag for the input file. |
| 2. Check whether `puddle.ops` is available | It inquires whether `puddle.ops` exists and, if the file is missing or treated as null, allocates a one-element placeholder `pudl_db(0:0)`. |
| 3. Open the puddle operations file | If the file is present, the routine opens `puddle.ops` on unit 104 for sequential reading. |
| 4. Read and skip the file title and header | It reads the title and header lines into temporary buffers, exiting early if an end-of-file condition appears. |
| 5. Count data records in a scan loop | The routine loops through the remaining lines, reading each into `titldum` and incrementing `imax` for every record encountered. |
| 6. Allocate the puddle database to match the count | After counting, it allocates `pudl_db(0:imax)` so the storage matches the number of records discovered in the file. |
| 7. Rewind and reread the file header | The file is rewound and the title/header are read again so the data section can be loaded from the start. |
| 8. Load each puddle-operation record | A loop reads each record from `puddle.ops` into `pudl_db(ic)` for `ic = 1` through `imax`. |
| 9. Store the loaded record count | The routine writes the count `imax` into `db_mx%pudl_db` so other code can know how many puddle operations were loaded. |
| 10. Close the file and return | It closes unit 104 and returns to the caller after loading the puddle-operation database. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pudl_db` |
| [sym:mgt_operations_module] | `pudl_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%pudl_db` | When `puddle.ops` exists and is read successfully, after counting the data rows | `db_mx%pudl_db` is updated to the number of puddle-operation records found in `puddle.ops`, making that count available to later database and management logic. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The procedure was introduced in `df07e3f` with the full file-reading workflow: existence check, open/read/rewind/load, and storing the count in `db_mx%pudl_db`. In `39fabde`, only local initialization changed: `ic`, `titldum`, `header`, `eof`, and `imax` were given explicit default values, while the file-reading logic and outputs remained the same.

- `df07e3f` added `mgt_read_puddle` and its complete `puddle.ops` loading workflow, including allocation of `pudl_db` and assignment to `db_mx%pudl_db`.
- `39fabde` initialized the local counters and string buffers (`ic`, `titldum`, `header`, `eof`, `imax`) but did not change the read/allocate algorithm or the stored result.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'mgt_read_puddle' has no extracted documentation comment.
