---
kind: procedure
symbol: sep_read
title: sep_read
status: filled
source_hash: e026a68df93146e1
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard title or non-data lines from
    `septic.str` during the file scan and the second pass.
  header: Scratch character buffer used to read the file header line from `septic.str` before
    the data records are counted or loaded.
  eof: I/O status flag for reads from unit 172. It is used to detect end-of-file or read failure
    and control when the scan loop stops.
  imax: Counter for how many septic-system records were found in `septic.str`. It becomes
    the upper bound for allocating `sep` and is copied to `db_mx%septic`.
  i_exist: Logical flag set by `inquire` to tell whether the configured septic input file
    is present. It controls whether the routine skips loading and allocates only a minimal
    `sep` array.
  isep: Loop index used on the second pass to read each septic-system record into `sep(isep)`.
uses:
  input_file_module: This module supplies `in_str%septic_str`, the configured path name for
    the septic database file. `sep_read` uses that path both to test file presence and to
    open the file for reading.
  maximum_data_module: This module holds `db_mx%septic`, the shared count of septic-system
    records. `sep_read` updates it so the rest of the model can know how many septic entries
    were loaded.
  septic_data_module: This module owns the allocatable `sep` array of `septic_system` records.
    `sep_read` allocates and fills that array, making the parsed septic database available
    to later routines.
---

<!-- facts:header -->

Reads the septic-system database file `septic.str` into the shared `sep` array. It first counts usable records to size the array, then rewinds and loads each septic definition for later model use.

## Bottom Line

`sep_read` is a database loader for septic system definitions. It checks whether the configured septic input file exists, counts the number of records in it, allocates `sep` to match, then rereads the file and fills `sep(1:imax)` with the septic-system data.

The routine matters because it establishes both the in-memory septic database and the record count `db_mx%septic`. Later model code can rely on those results to know how many septic-system types are available and to access each parsed `septic_system` entry.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization in `proc_db`, after other structural-operation readers and before later database-driven processing such as other scenario and BMP readers. `proc_db` prepares the shared input-file configuration, and downstream model code depends on `sep_read` having populated `sep` and `db_mx%septic` before septic-system information is referenced.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check file presence and initialize counters | The routine resets `eof` and `imax`, then tests whether `in_str%septic_str` exists and is not the sentinel string `"null"`. That decides whether the septic database can be read or whether only a minimal array will be allocated. |
| 2. Allocate a minimal array when no file is available | If the file is missing or disabled, the routine allocates `sep(0:0)` and skips the rest of the loading logic. This keeps the septic array defined even when no septic database is supplied. |
| 3. Open the septic database for scanning | When the file is available, the routine opens `septic.str` on unit 172 and begins a scan pass. The scan uses the file contents themselves to determine how many records are present. |
| 4. Skip title and header records | The first two records are read into `titldum` and `header` and discarded from the count. These reads position the file at the start of the actual septic-system records. |
| 5. Count septic-system records | The routine loops while reads succeed, consuming one record into `titldum` at a time and incrementing `imax` for each record seen. This determines the number of septic-system entries in the file. |
| 6. Allocate the septic database array | After counting, the routine allocates `sep(0:imax)`, sizing the shared septic-system array to hold all records it found. The lower bound remains zero, matching the module's array convention. |
| 7. Rewind the file for data loading | The routine rewinds unit 172 so the file can be read again from the beginning. This resets the record pointer for the actual load pass. |
| 8. Skip title and header again | After rewinding, the routine rereads the title and header records and discards them. This positions the input stream at the first septic-system data record for the load loop. |
| 9. Load each septic-system record | The routine reads records one by one into `sep(isep)` for `isep = 1` through `imax`, stopping early if a read fails. This populates the shared septic-system database with parsed file data. |
| 10. Close the file and publish the count | The routine closes unit 172 and stores `imax` in `db_mx%septic`. That makes the loaded septic record count available to other model code. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_str` | `in_str%septic_str` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%septic` |
| [sym:septic_data_module] | `sep` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%septic` | When `in_str%septic_str` exists and is not `"null"`, after counting the data records in `septic.str`. | `db_mx%septic` is updated to the number of septic-system records found in the file. This gives the model a shared maximum/count value for the septic database. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows two behavioral snapshots for `sep_read`: the file was introduced in df07e3f with the current logic for checking `in_str%septic_str`, counting records, allocating `sep`, rewinding, reading entries, and setting `db_mx%septic`. Commit 39fabde kept that logic and only changed local variable initialization and formatting, leaving the procedure's behavior intact.

- df07e3f introduced `sep_read.f90` with the full septic file-counting and load workflow, including the `inquire` check, two-pass read, `sep` allocation, and `db_mx%septic = imax`.
- 39fabde did not change the procedure logic; it initialized `titldum`, `header`, `eof`, `imax`, and `isep` at declaration and made minor formatting adjustments.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'sep_read' has no extracted documentation comment.
