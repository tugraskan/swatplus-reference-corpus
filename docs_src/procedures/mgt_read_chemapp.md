---
kind: procedure
symbol: mgt_read_chemapp
title: mgt_read_chemapp
status: filled
source_hash: fa6c6f3e98fd59c7
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch title/header token read from `chem_app.ops` while skipping the file's title
    line and again when rewinding to reload the data.
  header: Scratch header token read from `chem_app.ops` after the title line; it advances
    the file past the header before counting or loading records.
  eof: I/O status flag for reads from unit 107; it starts at 0, is set by each `read(...,iostat=eof)`,
    and controls loop termination and error/EOF exit.
  imax: Record counter used to determine how many chemical application operation entries are
    in `chem_app.ops`; it becomes the allocation upper bound and later the stored database
    size.
  i_exist: Logical existence check from `inquire` that tells the routine whether the configured
    operations file is present before attempting to open it.
  ichemapp: Loop index used to fill `chemapp_db(1:imax)` one record at a time after the file
    is rewound.
uses:
  input_file_module: The routine uses `in_ops%chem_ops` to get the configured filename for
    the chemical application operations file, so this module controls which database file
    is read.
  maximum_data_module: The routine writes the discovered record count into `db_mx%chemapp_db`,
    which records the size of the chemical application operations database for the rest of
    the model.
  mgt_operations_module: This module owns the allocatable `chemapp_db` array that receives
    the parsed chemical application operation records, so it is the target storage for the
    file contents.
---

<!-- facts:header -->

Reads the chemical application operations database from `chem_app.ops` into the management operations module. It counts records first so the `chemapp_db` array can be allocated to the right size, then loads each operation record and stores the total count in `db_mx%chemapp_db`.

## Bottom Line

mgt_read_chemapp loads the chemical application operations table used by SWAT+ management scheduling. It checks the configured operations filename, counts the data records in `chem_app.ops`, allocates `chemapp_db` to match, then rereads the file to populate each `chemical_application_operation` entry.

This routine matters because later management logic needs both the in-memory database (`chemapp_db`) and the maximum count (`db_mx%chemapp_db`) to resolve chemical application operations during simulation setup.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization inside `proc_db`, after other management input readers and before later management-processing routines need the chemical application database. Its output feeds any model behavior that selects or counts chemical application operations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the chemical-operations file is available | The routine calls `inquire` on `in_ops%chem_ops` to see whether the configured file exists. If the file is missing or the name is the literal string "null", it bypasses file reading and allocates a minimal `chemapp_db(0:0)` array. |
| 2. Open and scan the file to count data records | When the file is present, the routine opens unit 107 on `in_ops%chem_ops`, reads and skips the title and header lines, then loops through the remaining records to increment `imax` for each chemical application operation entry. |
| 3. Allocate the operations database to the counted size | After the scan, the routine allocates `chemapp_db(0:imax)` so the module array has one slot per counted record, with index 0 reserved as the lower bound. |
| 4. Rewind the file and skip the non-data lines again | The routine rewinds unit 107 to the start of `chem_app.ops`, rereads the title line and header line, and prepares to load the actual operation records into the array. |
| 5. Load each chemical application operation record | A loop from 1 to `imax` reads each file record into `chemapp_db(ichemapp)`, filling the allocatable array with the parsed chemical application operation data. |
| 6. Close the file and publish the record count | After the load loop, the routine exits the file-processing block, closes unit 107, and stores `imax` in `db_mx%chemapp_db` so other model code knows how many chemical application operations were read. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_ops` | `in_ops%chem_ops` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%chemapp_db` |
| [sym:mgt_operations_module] | `chemapp_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%chemapp_db` | When `in_ops%chem_ops` exists and is not 'null', the routine allocates `chemapp_db(0:imax)` and then fills it; otherwise it only allocates `chemapp_db(0:0)`. | The chemical application operations database is sized and populated from `chem_app.ops`, and the discovered count is published for later model setup. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows two behavior-relevant revisions. The initial addition in df07e3f introduced `mgt_read_chemapp` with the file-existence check, two-pass record counting/loading, allocation of `chemapp_db`, and assignment to `db_mx%chemapp_db`. Commit 39fabde kept the same logic but initialized the local scalars (`titldum`, `header`, `eof`, `imax`, `ichemapp`) and made a whitespace-only allocation formatting change.

- df07e3f added the full reader: it checks `in_ops%chem_ops`, counts records, allocates `chemapp_db`, reloads the file, and stores the count in `db_mx%chemapp_db`.
- 39fabde did not change the algorithm; it initialized local variables to default values and made a formatting-only change to the allocation statement.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'mgt_read_chemapp' has no extracted documentation comment.
