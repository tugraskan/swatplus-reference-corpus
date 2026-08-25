---
kind: procedure
symbol: hydrol_read
title: hydrol_read
status: filled
source_hash: 11c7995ce06e84c0
version_label: SWAT+ 62.0.0
locals:
  mhydrol: Local counter initialized to 0 and not changed in the extracted source; it appears
    to be a leftover or placeholder variable rather than an active control variable in this
    routine.
  ithyd: Loop counter used when reading hydrology records into `hyd_db(ithyd)` after the file
    is rewound. It runs from 1 to `imax`.
  titldum: Temporary character buffer used to read and discard the file title line during
    the file scan and again after rewind before the data records are loaded.
  header: Temporary character buffer used to read and discard the hydrology file header line
    before counting or loading the record data.
  eof: I/O status flag used on each `read` to detect end-of-file or read failure. A negative
    value exits the scan or load loops; zero means reading can continue.
  imax: Record counter that is incremented while scanning the file to determine how many hydrology
    database entries need to be allocated and read.
  i_exist: Logical file-existence flag set by `inquire`; it controls whether the routine reads
    `hydrology.hyd` or falls back to allocating an empty placeholder database.
uses:
  input_file_module: '`input_file_module` provides `in_hyd%hydrol_hyd`, the configured path
    to the hydrology input file. Without it, this routine would not know which file to open.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%hyd`, the shared count of hydrology
    database records. This routine sets that value after counting the file so later code can
    size and validate hydrology-dependent data.'
  hydrology_data_module: '`hydrology_data_module` owns the allocatable `hyd_db` array that
    receives the parsed hydrology records. The routine allocates and fills that shared database
    for downstream model setup and calculations.'
---

<!-- facts:header -->

Reads the hydrology definition file into the shared hydrology database. It first counts records to size the array, then rewinds and loads each hydrology record for later use by the model.

## Bottom Line

`hydrol_read` loads the hydrology input table referenced by `in_hyd%hydrol_hyd`. If the file is missing or set to `"null"`, it allocates a one-element `hyd_db` placeholder; otherwise it scans the file to count records, allocates `hyd_db(0:imax)`, and reads each record into the shared hydrology database.

The routine also updates `db_mx%hyd` with the number of hydrology records found. That count and the populated `hyd_db` array are used by later hydrology-related routines that depend on the database being sized and filled before simulation setup continues.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hydrol_read` runs during the input-loading phase of model startup, called by `proc_read` after other core input tables have already been read. Its output prepares the hydrology database and record count that later hydrology model behavior depends on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local counters and status flags. | Set `mhydrol`, `eof`, and `imax` to zero before any file checks or reads. These values start the routine in a known state and provide a clean record counter and I/O status flag. |
| 2. Check whether the configured hydrology file is usable. | Use `inquire` on `in_hyd%hydrol_hyd` and test both file existence and the special `"null"` filename. If the file is missing or disabled, allocate a one-element `hyd_db(0:0)` placeholder instead of reading records. |
| 3. Open the hydrology file and begin a record-count scan. | Open unit 107 on the hydrology file, read and discard the title and header lines, and stop early if an end-of-file condition is encountered. This prepares the routine to count only data records. |
| 4. Count the number of hydrology records. | Loop while `eof == 0`, reading and discarding one record at a time and incrementing `imax` for each successful read. The resulting `imax` is the number of hydrology database entries to allocate. |
| 5. Allocate the hydrology database array. | Allocate `hyd_db(0:imax)` using the counted number of records. This creates storage for the full set of hydrology entries plus the zero index used by the module's storage convention. |
| 6. Rewind the file and reread the non-data lines. | Rewind unit 107 back to the start of `hydrology.hyd`, then reread and discard the title and header lines so the file is positioned at the first data record again. |
| 7. Load each hydrology record into shared state. | Iterate `ithyd` from 1 to `imax` and read each record into `hyd_db(ithyd)`, stopping early if a read error or end-of-file occurs. This populates the shared hydrology database used by later model code. |
| 8. Close the file and publish the record count. | Close unit 107 and store the final record count in `db_mx%hyd`. That shared count tells the rest of the model how many hydrology records were loaded. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_hyd` | `in_hyd%hydrol_hyd` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%hyd` |
| [sym:hydrology_data_module] | `hyd_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%hyd` | When the hydrology input file is missing or disabled, `db_mx%hyd` remains 0; otherwise it is set to the counted record total after loading. | `db_mx%hyd` becomes the number of hydrology database records present in `hydrology.hyd`. This value is published so other routines can size loops or validate hydrology-related input. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. Commit `df07e3f` introduced `hydrol_read` with file-existence checking, record counting, allocation, rewind, record loading, and `db_mx%hyd` assignment. Commit `39fabde` kept the same logic but initialized the local variables `mhydrol`, `ithyd`, `titldum`, `header`, `eof`, and `imax` at declaration time.

- df07e3f added the full `hydrol_read` implementation: it reads `in_hyd%hydrol_hyd`, allocates `hyd_db`, populates the hydrology records, and stores the count in `db_mx%hyd`.
- 39fabde changed only local variable initialization in `hydrol_read`, setting `mhydrol`, `ithyd`, `titldum`, `header`, `eof`, and `imax` to default values at declaration without changing the algorithm.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hydrol_read' has no extracted documentation comment.
