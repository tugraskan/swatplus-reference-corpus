---
kind: procedure
symbol: mgt_read_fireops
title: mgt_read_fireops
status: filled
source_hash: 0528a939da3b51b3
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for the file title line and, later, for each counted
    data line while scanning or rereading `fire.ops`. It is not retained after the file is
    processed.
  header: Temporary character buffer used to read and skip the header line in `fire.ops` before
    counting or loading the actual fire-operation records.
  eof: IO status flag for reads from unit 107. A negative value signals end-of-file, and zero
    means the read succeeded, letting the routine stop scanning or loading at the right time.
  imax: Counter for the number of fire-operation data records found in `fire.ops`. It is used
    to size `fire_db` and then copied to `db_mx%fireop_db`.
  i_exist: Logical flag set by `inquire` to tell whether the configured fire-operations file
    exists on disk before the routine tries to open it.
  ifireop: Loop index for the second pass that reads each fire-operation record into `fire_db(ifireop)`.
uses:
  input_file_module: This module provides `in_ops%fire_ops`, the configured path to the fire-operations
    input file. Without that path, the routine would not know which file to open or whether
    the file has been disabled by setting it to `null`.
  maximum_data_module: This module owns `db_mx%fireop_db`, the shared counter used to publish
    how many fire-operation records were loaded. That value matters because later model setup
    can use it as the size or availability summary for fire-operation data.
  mgt_operations_module: This module defines the allocatable `fire_db` array of `fire_operation`
    records. `mgt_read_fireops` fills that shared array so the rest of the management system
    can access the parsed fire-operation definitions.
---

<!-- facts:header -->

Reads the fire operations definition file and loads its records into the shared `fire_db` array. It also stores the number of fire operation records found in `db_mx%fireop_db` for later use by management setup.

## Bottom Line

`mgt_read_fireops` is the fire-operations file reader used during management database setup. It looks up the configured `fire.ops` path, checks that the file exists and is not set to `null`, then reads the file into the allocatable `fire_db` array of `fire_operation` records.

The routine first scans past the title and header lines to count how many data records are present, allocates `fire_db(0:imax)`, rewinds the file, and reads each record into `fire_db(ifireop)`. When it finishes, it publishes the record count in `db_mx%fireop_db`, which downstream code can use to know how many fire-operation entries were loaded.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `proc_db`, after earlier management-file readers have been called and before later readers such as `mgt_read_mgtops`. Its output is the populated `fire_db` array and the record count in `db_mx%fireop_db`, which later management processing depends on to access fire-operation data.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and file-state buffers | The routine starts with empty title and header buffers, zeroed end-of-file and record counters, and a logical flag for file existence. It also resets `eof` and `imax` before any file access. |
| 2. Check whether the configured fire-operations file exists | It asks `inquire` about `in_ops%fire_ops` and, if the file is missing or the path is set to `null`, allocates a minimal `fire_db(0:0)` instead of trying to read records. |
| 3. Open the file and start a counting pass | When the file is usable, the routine opens unit 107 on `in_ops%fire_ops`, reads and skips the title and header records, then loops through the remaining lines to count each data record by incrementing `imax`. |
| 4. Allocate the fire-operation database array | After counting, it allocates `fire_db(0:imax)` so the shared fire-operation database has one slot per counted record, plus the zero index used by this code's allocation convention. |
| 5. Rewind the file and reread the non-data lines | The routine rewinds unit 107 to the start of `fire.ops`, then rereads the title and header lines so the second pass begins at the first data record. |
| 6. Load each fire-operation record into shared state | It loops from `ifireop = 1` through `imax` and reads each record directly into `fire_db(ifireop)`, stopping early if an input error or end-of-file occurs. |
| 7. Publish the record count and close the file | Finally, the routine stores the counted size in `db_mx%fireop_db`, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_ops` | `in_ops%fire_ops` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%fireop_db` |
| [sym:mgt_operations_module] | `fire_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%fireop_db` | When `fire.ops` is missing, disabled with `null`, or present and scanned to determine `imax`. | `db_mx%fireop_db` is updated to the number of fire-operation data records found in the input file. This publishes the loaded database size so later model code can know how many fire-operation entries are available. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved for `mgt_read_fireops`. The initial add in `df07e3f` introduced the routine with file existence checking, two-pass counting and loading of `fire.ops`, allocation of `fire_db`, and assignment to `db_mx%fireop_db`. Commit `94b6dec` brought in the same routine from the upstream source with no behavioral change visible in the diff. Commit `39fabde` changed only local variable initialization by setting `titldum`, `header`, `eof`, `imax`, and `ifireop` to explicit default values.

- df07e3f added the full fire-operations reader: it checks `in_ops%fire_ops`, scans the file to count records, allocates `fire_db`, rereads the file, and stores the count in `db_mx%fireop_db`.
- 39fabde made the local buffers and counters explicitly initialized at declaration, reducing reliance on later assignment before use.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'mgt_read_fireops' has no extracted documentation comment.
