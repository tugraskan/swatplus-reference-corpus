---
kind: procedure
symbol: manure_db_read
title: manure_db_read
status: filled
source_hash: 37aaf993d6aba014
version_label: SWAT+ 62.0.0
locals:
  it: Loop counter for traversing manure database records while reading them into `manure_db`.
  titldum: Temporary title/header-line buffer used to read and skip the first line(s) of `manure_db.frt`.
  header: Temporary header-line buffer used to read and skip the second line of `manure_db.frt`
    before counting data records.
  eof: I/O status flag from each `read`; it signals end-of-file or other read status and controls
    record counting and loop exit.
  imax: Counts how many manure parameter records are present in `manure_db.frt` and is used
    as the upper bound for allocating `manure_db`.
  mfrt: Inner-loop index used to search `manure_om` for a matching organic-matter name so
    `iorg_min` can be assigned.
  i_exist: Logical file-existence flag returned by `inquire`; it decides whether the routine
    reads `manure_db.frt` or allocates an empty database.
uses:
  input_file_module: The routine needs `input_file_module` because its first decision is whether
    the manure database file exists; that flag controls whether the file is read or the database
    is left as an empty one-element allocation.
  maximum_data_module: The routine uses `maximum_data_module` to store the number of manure
    parameter records it found in `db_mx%manureparm`, and it also uses `db_mx%manure_om` as
    the loop limit when crosswalking `org_min` names to `manure_om` entries.
  fertilizer_data_module: The routine uses `fertilizer_data_module` because it fills `manure_db`
    records from `manure_db.frt` and then resolves each record's `org_min` string against
    `manure_om(mfrt)%name` to set the `iorg_min` pointer.
---

<!-- facts:header -->

Reads the manure database file and loads manure type metadata into shared model storage. It also crosswalks each manure entry to the manure organic-matter database and records the number of manure parameter records found.

## Bottom Line

`manure_db_read` opens `manure_db.frt`, counts the manure records in the file, allocates `manure_db` to hold them, then rereads the file to populate each manure database entry. While loading each record, it crosswalks the `org_min` name to `manure_om` so the manure entry gets a numeric `iorg_min` pointer.

The routine matters because later manure-application and database routines rely on the loaded `manure_db` entries and on `db_mx%manureparm` to know how many manure parameter records are available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization inside `proc_db`, after other parameter files such as manure organic matter are read and before management and spatial modules use the manure database. Its results feed later manure and nutrient-application behavior that depends on `manure_db` contents, especially the crosswalked `iorg_min` pointers and the total manure record count in `db_mx%manureparm`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check whether the file exists. | The routine resets `eof`, `imax`, and `mfrt`, then uses `inquire` to see whether `manure_db.frt` exists. If the file is missing or disabled by the literal name check, it allocates a minimal `manure_db(0:0)` and skips file loading. |
| 2. Count manure records in the file. | The routine opens unit 107 on `manure_db.frt`, reads and skips the title and header lines, then repeatedly reads remaining lines into `titldum` until end-of-file. Each successful read increments `imax`, which becomes the number of manure parameter records. |
| 3. Allocate manure database storage. | After counting the data rows, the routine allocates `manure_db(0:imax)` so there is storage for every manure record it will load. |
| 4. Rewind and skip the file headers again. | The routine rewinds unit 107 to the start of `manure_db.frt`, rereads the title line, and rereads the header line so the actual data load starts at the first manure record. |
| 5. Load each manure record into shared state. | For each record index from 1 through `imax`, the routine reads the manure name, the `org_min` crosswalk name, and the other manure database fields into `manure_db(it)`. |
| 6. Crosswalk `org_min` to the manure organic-matter table. | For each manure record, the routine searches `manure_om` from 1 to `db_mx%manure_om`. When `manure_db(it)%org_min` matches `manure_om(mfrt)%name`, it stores that index in `manure_db(it)%iorg_min` and exits the search loop. |
| 7. Save the final record count and close the file. | After loading completes, the routine stores `imax` in `db_mx%manureparm` so the rest of the model knows how many manure database entries exist, then closes unit 107. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module provides the file-existence state queried by `inquire` for `manure_db.frt`.` | `i_exist` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%manure_om, db_mx%manureparm` |
| [sym:fertilizer_data_module] | `manure_db, manure_om` | `manure_db(it)%name, manure_db(it)%org_min, manure_db(it)%pests, manure_db(it)%paths, manure_db(it)%hmets, manure_db(it)%salts, manure_db(it)%constit, manure_db(it)%descrip, manure_om(mfrt)%name, manure_db(it)%iorg_min` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `manure_db(it)%iorg_min` | For each manure record when `manure_db(it)%org_min == manure_om(mfrt)%name` during the crosswalk loop. | `manure_db(it)%iorg_min` is set to the matching `manure_om` index so the manure record has a numeric pointer to its organic-matter definition instead of only a text name. |
| `db_mx%manureparm` | After the file scan and load finish, unconditionally at the end of the routine. | `db_mx%manureparm` is updated to the number of manure parameter records found in `manure_db.frt`, which lets other code size loops and know how many manure entries are available. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was introduced in 561bc28 as a new source file for manure application management. The diff shows it opens `manure_db.frt`, counts records, allocates `manure_db`, reloads the file, crosswalks `org_min` to `manure_om`, and records the count in `db_mx%manureparm`.

- 561bc28 added the entire `manure_db_read` subroutine, including file existence checking, record counting, allocation, record loading, and the `org_min` to `manure_om` crosswalk.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'manure_db_read' has no extracted documentation comment.
