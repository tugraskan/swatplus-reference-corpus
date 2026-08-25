---
kind: procedure
symbol: plant_transplant_read
title: plant_transplant_read
status: filled
source_hash: f0e04fc1746d09b5
version_label: SWAT+ 62.0.0
locals:
  ic: '`ic` is the loop counter used to read each transplant record from `transplant.plt`
    into `transpl(ic)` after the array size has been determined.'
  titldum: '`titldum` is a scratch character variable used to read and discard the file title
    or other non-data lines while counting and re-reading the transplant file.'
  header: '`header` is a scratch character variable used to read and discard the file header
    line before the routine counts or loads the actual transplant records.'
  eof: '`eof` receives the `iostat` status from each read. The routine uses it to detect normal
    end-of-file or read failure while scanning and loading `transplant.plt`.'
  imax: '`imax` counts how many transplant data records are present in `transplant.plt`; it
    becomes the upper bound used when allocating `transpl(0:imax)` and the value copied into
    `db_mx%transplant`.'
  i_exist: '`i_exist` is the `inquire` result that tells the routine whether `transplant.plt`
    exists before it tries to open and read it.'
uses:
  input_file_module: '`input_file_module` is used for file-input conventions in this codebase
    and is part of the routine''s database-reading environment, even though no specific symbol
    from it is referenced in the extracted lines.'
  maximum_data_module: '`maximum_data_module` provides `db_mx`, which stores the final transplant
    database size. This matters because the loader updates `db_mx%transplant` after counting
    records so later routines can see how many transplant entries were loaded.'
  plant_data_module: '`plant_data_module` provides the allocatable transplant database array
    `transpl`. The routine allocates that array and fills it with records from `transplant.plt`,
    so this module holds the loaded data that other plant routines will use.'
---

<!-- facts:header -->

Reads the plant transplant database from `transplant.plt` into the allocatable `transpl` array and records how many transplant records were loaded.

## Bottom Line

This routine is the database loader for plant transplant definitions. It checks whether `transplant.plt` exists, counts the number of data records in the file, allocates `transpl` to fit, then rewinds and reads each record into `plant_data_module::transpl`.

When the file is missing or disabled, it still allocates a minimal `transpl(0:0)` array and leaves the database count at zero. The final record count is stored in `maximum_data_module::db_mx%transplant` so later code can know how many transplant entries are available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization in `proc_db`, immediately after plant parameter initialization and before the remaining database readers. Its result is the in-memory transplant database and the count `db_mx%transplant`, which later plant-management code depends on when it needs transplant definitions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check whether the transplant file exists | The routine clears `eof` and `imax`, then uses `inquire(file="transplant.plt", exist=i_exist)` to see whether the database file is present. If the file is missing or treated as disabled, it allocates a minimal `transpl(0:0)` array and skips file loading. |
| 2. Open the file and begin the first pass | If the file exists, the routine opens unit 104 on `transplant.plt`, reads a title line into `titldum`, and reads a header line into `header`. Either read can terminate the pass early if `iostat` reports end-of-file or an error. |
| 3. Count transplant records | The routine loops while `eof == 0`, reading and discarding one line at a time into `titldum` and incrementing `imax` for each record encountered. This pass determines how many transplant entries the file contains. |
| 4. Allocate the transplant database array | After counting, the routine allocates `transpl(0:imax)` so the in-memory database has enough slots for every transplant record plus the zero index used by this codebase. |
| 5. Rewind and prepare for the data-loading pass | The file is rewound to the beginning, then the title and header lines are read again and skipped so the routine can position itself at the first data record for the second pass. |
| 6. Load each transplant record into shared state | A loop over `ic = 1, imax` reads each transplant record from unit 104 into `transpl(ic)`. This populates the shared plant transplant database used by later routines. |
| 7. Publish the record count and close the file | The routine stores the final record count in `db_mx%transplant`, closes unit 104, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module state` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%transplant` |
| [sym:plant_data_module] | `transpl` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%transplant` | After the file exists check and first counting pass, `imax` holds the number of transplant records found in `transplant.plt`. | `db_mx%transplant` is updated to that count so the shared maximum-data state reflects how many transplant database records were loaded for the current run. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage shows three resolved commits. `df07e3f` added `plant_transplant_read` with the current file-scan, allocate, rewind, read, and close logic. `94b6dec` preserved the routine when importing the latest source snapshot without changing the algorithm in the extracted diff. `39fabde` only initialized local variables (`ic`, `titldum`, `header`, `eof`, `imax`) to default values and left the file I/O and database-loading behavior unchanged.

- df07e3f introduced the procedure and its two-pass read of `transplant.plt`, including allocation of `transpl` and assignment of `db_mx%transplant`.
- 39fabde changed local variable initialization by setting `ic`, `titldum`, `header`, `eof`, and `imax` to explicit defaults before the file is processed.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'plant_transplant_read' has no extracted documentation comment.
