---
kind: procedure
symbol: septic_parm_read
title: septic_parm_read
status: filled
source_hash: ae433e5de981287f
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and skip the title or record-key line from
    `septic.sep` during the count pass and again before reading each septic record.
  header: Scratch character buffer used to read the file header line after the title line
    in both passes through `septic.sep`.
  eof: I/O status flag for the `read` statements; it is initialized to 0 and used to detect
    end-of-file or read failure while counting and loading records.
  imax: Running count of how many septic data records were found in `septic.sep`; this becomes
    the array upper bound and the value stored in `db_mx%sep`.
  i_exist: Logical flag from `inquire` that tells the routine whether the configured septic
    database file actually exists before trying to read it.
  is: Loop counter used for the second pass to step through each septic record and load it
    into `sepdb(is)`.
uses:
  input_file_module: This module supplies `in_parmdb%septic_sep`, the configured path for
    the septic parameter file. The routine cannot choose or open the input file without that
    shared configuration.
  maximum_data_module: This module provides `db_mx%sep`, the shared record-count slot for
    septic database entries. The routine sets it after counting the file so other code can
    know how many septic records were loaded.
  septic_data_module: This module owns the allocatable septic database array `sepdb`. The
    routine allocates and fills that shared array so septic-system lookups later in the model
    have the parsed parameters available.
---

<!-- facts:header -->

Reads the septic parameter database from `septic.sep` into the shared septic database array. It first counts records to size the array, then rereads the file and loads each septic definition for later model use.

## Bottom Line

`septic_parm_read` is the septic-database loader. It opens the file named in `in_parmdb%septic_sep`, counts how many septic records are present, stores that count in `db_mx%sep`, allocates `sepdb`, and then rereads the file to populate each `septic_db` entry.

This matters because later septic-system processing depends on the populated `sepdb` array and the record count in `db_mx%sep`. If the configured file is missing or set to `null`, it falls back to allocating a one-element placeholder array instead of loading data.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization, after `proc_db` has started reading the model’s parameter databases and before later management and process routines depend on septic-system parameters. Its output, `sepdb` and `db_mx%sep`, becomes available for any later septic-related model behavior that needs the parsed septic definitions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test the configured file | The routine resets `eof` and `imax`, then uses `inquire` on `in_parmdb%septic_sep` to see whether the septic parameter file exists and is not set to the literal string `null`. |
| 2. Allocate a placeholder if no usable file is available | If the file is missing or disabled, the routine allocates `sepdb(0:0)` instead of attempting to read septic records. |
| 3. Open the septic database file | For a usable file, the routine opens unit 171 on `in_parmdb%septic_sep` so it can scan the file contents. |
| 4. Skip title and header lines | It reads the title line into `titldum` and the header line into `header`, stopping early if either read hits end-of-file. |
| 5. Count septic data records | The routine loops through the remaining lines, reading each into `titldum` and incrementing `imax` once per record until end-of-file is reached. |
| 6. Store the record count and allocate the septic array | It copies the count into `db_mx%sep` and allocates `sepdb(0:imax)` so the shared septic database has one slot per record. |
| 7. Rewind and restart the file | The routine rewinds unit 171 and rereads the title and header lines to position the file at the first data record for the load pass. |
| 8. Load each septic record into shared state | For each index from 1 to `db_mx%sep`, it reads a line into `titldum`, backs up one record, and then reads the structured record directly into `sepdb(is)`. |
| 9. Close the file and return | After all records are loaded, the routine closes unit 171 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_parmdb` | `in_parmdb%septic_sep` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%sep` |
| [sym:septic_data_module] | `sepdb` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%sep` | When `septic.sep` exists and `in_parmdb%septic_sep` is not `null`, the routine counts the file records and assigns that count to `db_mx%sep` before allocating and filling `sepdb`. | `db_mx%sep` becomes the number of septic database records discovered in the input file. That value controls the size of the shared septic array and the number of iterations used to load its entries. |

## File I/O

<!-- facts:io -->


## Lineage

`septic_parm_read` was introduced in commit `df07e3f`. Commit `94b6dec` brought the same routine forward from the earlier source snapshot without changing the logic shown here. Commit `35b029c` made only an end-statement formatting change. Commit `39fabde` initialized the local scalars `titldum`, `header`, `eof`, `imax`, and `is` and removed a trailing whitespace-only difference on the `allocate (sepdb(0:imax))` line.

- 39fabde: initialized local scratch variables (`titldum`, `header`, `eof`, `imax`, `is`) and preserved the same septic file scan/load flow.
- 35b029c: changed only the subroutine end-statement formatting; no algorithm change.
- 94b6dec: imported the routine into the current source history with the same septic database counting, allocation, rewind, backspace, and load sequence.
- df07e3f: added the septic parameter reader with the current two-pass file read and shared-state population behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'septic_parm_read' has no extracted documentation comment.
