---
kind: procedure
symbol: urban_parm_read
title: urban_parm_read
status: filled
source_hash: 1b020b0ac0f89795
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to consume title/label lines while scanning and rereading
    `urban.urb`; it is not stored as output state.
  header: Temporary string used to consume the file header line in `urban.urb` before counting
    or reading the data records.
  eof: I/O status flag from each `read`; values below zero signal end-of-file and stop the
    scan or data load.
  imax: Counter for the number of urban database records discovered in the first pass; it
    is later used to allocate `urbdb(0:imax)` and copied to `db_mx%urban`.
  i_exist: Logical flag set by `inquire` to tell whether the configured urban database file
    exists before attempting to open it.
  iu: Loop counter used on the second pass to read each urban record into `urbdb(iu)`.
uses:
  input_file_module: This module supplies the configured path for the urban parameter database.
    `urban_parm_read` uses `in_parmdb%urban_urb` to decide which file to inquire about, open,
    and read; without it, the routine would not know where the urban database lives.
  maximum_data_module: This module holds the shared maximum-record counts for database files.
    `urban_parm_read` stores the number of urban land-use types it found into `db_mx%urban`
    so later routines can size loops and know how many urban records are available.
  urban_data_module: This module owns the allocatable array that receives the parsed urban
    database records. `urban_parm_read` allocates and fills `urbdb`, so this module is the
    shared in-memory destination for the urban parameter data.
---

<!-- facts:header -->

Reads the urban land-use parameter database from `urban.urb` into the shared `urbdb` array and records how many urban types were found.

## Bottom Line

`urban_parm_read` is the database loader for urban land-use parameters. It checks whether the configured `urban.urb` file exists, scans it to count the number of records, allocates `urbdb` to match, then rereads the file and fills each `urban_db` entry.

This matters because later urban-land simulations depend on `urbdb` being populated and on `db_mx%urban` holding the number of urban types available in the database.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`urban_parm_read` runs inside `proc_db` during the database-loading phase, after the input-file module has been initialized with the path to `urban.urb`. Its results feed later urban parameter use by populating `urbdb` and setting `db_mx%urban`, which downstream urban-related routines rely on for record access and loop bounds.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Test the configured urban file path | The routine checks whether `in_parmdb%urban_urb` points to an existing file and is not the literal string `"null"`. If the file is missing or disabled, it allocates a minimal `urbdb(0:0)` array instead of reading records. |
| 2. Open the urban database file | When the file is available, the routine opens `urban.urb` on unit 108 so it can scan the file sequentially. |
| 3. Skip title and header records | It reads the title and header lines into `titldum` and `header`, using the I/O status flag to stop immediately if the file ends unexpectedly. |
| 4. Count the data records | The routine resets `imax` to zero and loops through the remaining lines, reading each one into `titldum` and incrementing `imax` for every record found until end-of-file is reached. |
| 5. Allocate the urban database array | After the count is known, it allocates `urbdb(0:imax)` so the shared urban database has enough slots for all records plus the zero index. |
| 6. Rewind the file for a second pass | The file is rewound to the beginning so the routine can reread the title, header, and actual data records from the start. |
| 7. Skip title and header again | It rereads the title and header lines after rewinding, again using the status code to guard against unexpected end-of-file before data loading begins. |
| 8. Load each urban record | A loop over `iu = 1, imax` reads each urban record from `urban.urb` directly into `urbdb(iu)`. This populates the shared urban parameter table used by later model code. |
| 9. Finish and publish record count | After the file is loaded, the routine exits the loop, stores `imax` in `db_mx%urban`, closes unit 108, and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_parmdb` | `in_parmdb%urban_urb` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%urban` |
| [sym:urban_data_module] | `urbdb` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%urban` | After counting records from `urban.urb`, including the missing-file case where `imax` remains 0 | The routine copies the number of urban database records found into the shared maximum-count state so later code knows how many urban land-use types are available. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `urban_parm_read`. The initial addition in `df07e3f` introduced the subroutine with file scanning, allocation, rewind, record loading, and `db_mx%urban` assignment. Commit `94b6dec` kept the same logic while bringing in the upstream source snapshot. Commit `39fabde` only initialized local variables (`titldum`, `header`, `eof`, and `iu`) and removed trailing whitespace on the `allocate` line; it did not change the routine's algorithm.

- `df07e3f` introduced the urban database reader workflow: existence check, two-pass scan of `urban.urb`, allocation of `urbdb`, loading of records, and publication of `db_mx%urban`.
- `39fabde` made local-state initialization explicit by setting `titldum`, `header`, `eof`, and `iu` to default values before file I/O, reducing dependence on uninitialized locals.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'urban_parm_read' has no extracted documentation comment.
