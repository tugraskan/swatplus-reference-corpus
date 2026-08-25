---
kind: procedure
symbol: field_read
title: field_read
status: filled
source_hash: d73b5845b262a7e4
version_label: SWAT+ 62.0.0
locals:
  ith: '`ith` is the loop counter for the second pass through the field records. It indexes
    `field_db(ith)` while each data row is reread from `field.fld`.'
  titldum: '`titldum` is a scratch character buffer used to read and discard title or intermediate
    lines while scanning `field.fld`. It also advances the file position before the routine
    backspaces and reads the actual record into `field_db(ith)`.'
  header: '`header` holds the header line read from `field.fld` after the title line. The
    routine reads it during both passes to skip over non-data content before processing the
    field records.'
  eof: '`eof` captures the `iostat` status from each `read` statement. The routine uses negative
    values to detect end-of-file and zero to continue looping while counting or loading records.'
  imax: '`imax` accumulates the number of field data records found in `field.fld`. After the
    scan pass, it becomes the upper bound used to allocate `field_db(0:imax)` and to set `db_mx%field`.'
  i_exist: '`i_exist` stores the result of the `inquire` check on `in_hyd%field_fld`. It tells
    the routine whether the configured input file is present before trying to open it.'
uses:
  input_file_module: '`input_file_module` provides `in_hyd%field_fld`, the configured filename
    that tells this routine which field database file to load. Without that module state,
    `field_read` would not know which file to inquire, open, or read.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%field`, the shared count of
    field database entries. `field_read` sets it after counting records so other routines
    can know how many field entries were loaded.'
  topography_data_module: '`topography_data_module` provides the allocatable `field_db` array
    that receives the parsed field records. This module is the storage location for the field
    database used after reading completes.'
---

<!-- facts:header -->

Reads the field database from `field.fld` into `field_db` and records how many field entries were found. It first counts records to size the array, then rereads the file to populate each field entry.

## Bottom Line

`field_read` is a file loader for the field properties database. It checks whether the configured `field.fld` file exists and is not set to the literal string `"null"`; if the file is missing or disabled, it creates a one-element placeholder allocation. Otherwise it opens the file, scans past the title and header, counts the data records to determine the database size, and stores that count in `db_mx%field`.

After sizing `field_db`, the routine rewinds `field.fld` and rereads each field record into `field_db(ith)`. This matters because later model code uses the populated field database and the `db_mx%field` count to access field properties consistently.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the input-reading phase, after `proc_read` has already prepared the broader model state and invoked related database loaders such as `topo_read`. Its results feed later model behavior that depends on the loaded field database and on `db_mx%field` for looping over field entries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the configured field file is usable | The routine inquiries about `in_hyd%field_fld` and tests whether it exists and is not the literal string `"null"`. If the file is unavailable or disabled, it allocates a minimal `field_db(0:0)` placeholder instead of reading records. |
| 2. Open the field file and start a counting pass | The routine opens unit 107 on `in_hyd%field_fld`, reads the title line into `titldum`, and reads the header into `header`. These reads advance past non-data lines before counting the file contents. |
| 3. Count data records to determine database size | The routine loops while `eof == 0`, reading successive lines into `titldum` and incrementing `imax` for each record. This first pass determines how many field entries are present in the file. |
| 4. Save the record count and allocate the database array | After counting, the routine stores the total in `db_mx%field` and allocates `field_db(0:imax)` to hold the field records. The shared count and the array size are matched to the number of records found. |
| 5. Rewind the file and skip the title and header again | The routine rewinds unit 107 and rereads the title and header lines so the second pass starts at the first data record. This resets the file position after the counting scan. |
| 6. Read each field record into the allocatable array | For each index from 1 to `db_mx%field`, the routine probes a record with `titldum`, backs up one record, and then reads the actual structured record into `field_db(ith)`. This fills the in-memory field database from the file. |
| 7. Stop the loop and close the file | The routine exits the open-file loop after loading the records and then closes unit 107. This ends file access for `field.fld` and leaves the database available in memory. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_hyd` | `in_hyd%field_fld` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%field` |
| [sym:topography_data_module] | `field_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%field` | When `field.fld` exists and is not the string `"null"`, the routine counts records successfully and stores the total before loading data. | `db_mx%field` is updated to the number of field records discovered in `field.fld`. This shared count tells the rest of the model how many field database elements were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows the procedure was introduced in df07e3f with the current file-based loading logic, and 39fabde only initialized local variables without changing the algorithm.

- df07e3f added the `field_read` routine to read `field.fld`, count records into `imax`, allocate `field_db`, and load each record into memory.
- 39fabde changed only the local variable declarations to initialize `ith`, `titldum`, `header`, `eof`, and `imax`; the file-reading behavior remained the same.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'field_read' has no extracted documentation comment.
