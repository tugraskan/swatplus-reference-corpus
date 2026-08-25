---
kind: procedure
symbol: salt_fert_read
title: salt_fert_read
status: filled
source_hash: 42ec0ad291895d8a
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the first line of `salt_fertilizer.frt`,
    which serves as a title string.
  header: Scratch character buffer used to read and discard the second line of `salt_fertilizer.frt`,
    which likely contains column or file header text.
  isalti: Loop index that steps through each fertilizer entry while reading the fertilizer
    salt database into `fert_salt`.
  eof: I/O status code for the header reads; it captures end-of-file or read failure when
    the file is first opened and skimmed.
  i_exist: Logical file-existence test from `inquire`; it gates all further work so the routine
    only opens and reads `salt_fertilizer.frt` when the file is present.
uses:
  constituent_mass_module: This module is imported by the routine, so it is part of the shared
    constituent-mass infrastructure that the salt fertilizer reader runs within; even though
    no specific symbol from it is referenced in the extracted source, it establishes the bookkeeping
    context for salt constituents.
  input_file_module: This module is imported so the routine can participate in the model's
    shared file-input workflow; it matters here because `salt_fert_read` is one of the procedures
    that loads initialization data from disk during the read phase.
  maximum_data_module: '`db_mx%fertparm` provides the fertilizer-record count used to size
    the allocation and to bound the read loop, so this maximum-data setting determines how
    many fertilizer entries are loaded from `salt_fertilizer.frt`.'
  salt_module: '`fert_salt` receives the per-fertilizer salt loading records from the file,
    and `fert_salt_flag` is set to indicate that this database has been successfully populated
    for later salt-related routines.'
---

<!-- facts:header -->

Reads the salt fertilizer input file and loads fertilizer salt-ion amounts into memory.

## Bottom Line

salt_fert_read checks for the presence of `salt_fertilizer.frt`, opens it, skips the title and header lines, then allocates the `fert_salt` array to the number of fertilizer types defined in `db_mx%fertparm`.

If the file exists, it reads one fertilizer record at a time into `fert_salt(isalti)` and sets `fert_salt_flag = 1` so later salt-loading code can use the fertilizer database.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model input-read phase, after `proc_read` has already been driving the salt-related input routines and before later constituent setup continues. Its result is the populated fertilizer salt database and flag that downstream salt loading and fertilizer-related process logic can rely on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Checks whether `salt_fertilizer.frt` exists before attempting any file I/O, so the routine only loads fertilizer salt data when the input file is present. |
| 2. io | Opens `salt_fertilizer.frt` on unit 107 to begin reading the fertilizer salt database. |
| 3. io | Reads and discards the file title line into `titldum`, using `iostat=eof` to detect read problems while skipping metadata. |
| 4. io | Reads and discards the file header line into `header`, again using `iostat=eof` while moving past non-data text. |
| 5. allocation | Allocates `fert_salt` to the number of fertilizer types defined by `db_mx%fertparm`, creating storage for all fertilizer salt records. |
| 6. assignment | Sets `fert_salt_flag` to 1 to mark that the fertilizer salt database has been loaded and is available for later use. |
| 7. loop | Loops from 1 through `db_mx%fertparm` and reads one fertilizer salt record into `fert_salt(isalti)` per iteration. |
| 8. io | Closes unit 107 after all fertilizer data have been read from `salt_fertilizer.frt`. |
| 9. return | Returns to the caller after either loading the fertilizer salt data or skipping work when the file is absent. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `constituent_mass_module` |  |
| [sym:input_file_module] | `input_file_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%fertparm` |
| [sym:salt_module] | `fert_salt, fert_salt_flag` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `fert_salt_flag` | When `salt_fertilizer.frt` exists and the routine reaches the read block, `fert_salt_flag` is set to 1 immediately after allocating `fert_salt`. | `fert_salt_flag` records that the fertilizer salt lookup table has been successfully initialized from file input, which lets later code know the array contents are available. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved for `salt_fert_read`. The file was introduced in df07e3f with the full reader logic, 35b029c made only whitespace/no-newline cleanup, 2ee1889 initialized local scalars and removed unused locals (`fert_name`, `imax`), and 39fabde further initialized `titldum`, `header`, `isalti`, and `eof` plus a comment-format cleanup.

- df07e3f added the `salt_fert_read` subroutine and its file-read workflow for `salt_fertilizer.frt`.
- 35b029c did not change behavior; it only adjusted formatting/newline handling in the new file.
- 2ee1889 changed local declarations by removing unused variables and leaving the file-reading logic intact.
- 39fabde changed local initialization to explicit default values and preserved the same read/allocate/flag behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_fert_read' has no extracted documentation comment.
