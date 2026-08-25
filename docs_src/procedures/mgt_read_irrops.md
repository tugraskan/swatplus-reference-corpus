---
kind: procedure
symbol: mgt_read_irrops
title: mgt_read_irrops
status: filled
source_hash: 87d5d6cfaeda21fe
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and discard the file title or to consume
    each data line while counting records; it is also reused when the file is rewound before
    the actual data load.
  header: Temporary character buffer for the file header line; the routine reads it after
    the title both during the counting pass and again after rewinding before loading records.
  eof: I/O status flag used by each `read` to detect end-of-file or read failure; a negative
    value exits the scan, and zero keeps the record-counting loop going.
  imax: Counts how many irrigation operation data records were found in `irr.ops`; that count
    is used to size `irrop_db(0:imax)` and stored in `db_mx%irrop_db`.
  i_exist: Logical existence flag set by `inquire`; it tells the routine whether the configured
    irrigation operations file is available before attempting to open and read it.
  mirrops: A local counter initialized to zero but not otherwise used in the visible routine
    body; it appears to be a leftover or placeholder variable.
  irr_op: Loop counter used when reading the actual irrigation operation records into `irrop_db(irr_op)`
    after the array has been allocated.
uses:
  input_file_module: This module supplies `in_ops%irr_ops`, the configured path/name for the
    irrigation operations file. The routine uses that setting to check file existence and
    to open the correct file.
  maximum_data_module: This module holds `db_mx%irrop_db`, the shared maximum/element-count
    field for irrigation operations. The routine updates it with the number of records found
    so downstream code knows the database size.
  mgt_operations_module: This module owns the allocatable `irrop_db` array that stores the
    parsed irrigation operation records. The routine allocates and fills that shared database
    so later management logic can use the loaded operations.
---

<!-- facts:header -->

Reads the irrigation operations database from `irr.ops` into `irrop_db` and records how many entries were loaded. It also handles the empty-or-missing-file case by creating a zero-length database entry.

## Bottom Line

mgt_read_irrops is the irrigation-operations database loader. It checks whether the configured irrigation operations file exists, counts the data records in that file, allocates `irrop_db` to the needed size, then rewinds and reads each irrigation operation record into the global database array.

This routine matters because later management code depends on `mgt_operations_module%irrop_db` being populated and on `maximum_data_module%db_mx%irrop_db` reflecting how many irrigation operation records were found. If the file is missing or set to `null`, it creates a minimal `irrop_db(0:0)` allocation instead of loading records.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization inside `proc_db`, after earlier parameter and database readers have already prepared shared input settings. Its result is the populated irrigation operations database and record count that later management scheduling and irrigation behavior depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local counters and buffers | The routine starts with blank title/header buffers, zeroed I/O status and counters, and a local irrigation-operation counter. This establishes a clean state before any file access occurs. |
| 2. Check whether the irrigation operations file exists | It uses `inquire` on `in_ops%irr_ops` to see whether the configured irrigation file is present. If the file is missing or the name is literally `null`, it allocates `irrop_db(0:0)` as a minimal placeholder. |
| 3. Open the file and begin a counting pass | If the file exists, the routine opens unit 107 on `irr.ops`, reads past the title and header, then loops through the remaining records to count them. Each successful read increments `imax` until end-of-file is reached. |
| 4. Allocate the irrigation database to the discovered size | After counting, it allocates the shared `irrop_db` array from index 0 through `imax`, so the database has room for every irrigation operation record found in the file. |
| 5. Rewind the file and reread the fixed header records | The file is rewound to the beginning, then the title and header lines are read again so the file pointer is positioned correctly for the data section. |
| 6. Load each irrigation operation record into shared state | A loop from 1 to `imax` reads each irrigation operation record into `irrop_db(irr_op)`, populating the shared management database with the file contents. |
| 7. Record the final database size and close the file | The routine exits the one-time open/read block, stores the final record count in `db_mx%irrop_db`, closes unit 107, and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_ops` | `in_ops%irr_ops` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%irrop_db` |
| [sym:mgt_operations_module] | `irrop_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%irrop_db` | After the file scan completes, or immediately when the file is missing or set to `null`. | `db_mx%irrop_db` is set to the number of irrigation operation records found in `irr.ops` so the rest of the model knows how many elements were loaded into `irrop_db`. In the missing-file case, the count remains zero. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The original addition, `df07e3f`, introduced `mgt_read_irrops` with the current open-scan-rewind-load pattern. Later `94b6dec` kept the same logic but updated the imported source snapshot, and `39fabde` initialized the local scalars (`titldum`, `header`, `eof`, `imax`, `mirrops`, `irr_op`) while preserving the read/allocate workflow.

- df07e3f established the full irrigation-operations file reader: existence check, record counting, allocation of `irrop_db`, rewind, record loading, and update of `db_mx%irrop_db`.
- 39fabde changed only local variable initialization by giving `titldum`, `header`, `eof`, `imax`, `mirrops`, and `irr_op` default values; the file-reading algorithm itself remained the same.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'mgt_read_irrops' has no extracted documentation comment.
