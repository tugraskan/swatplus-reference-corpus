---
kind: io
source_symbols:
- recalldb_read
title: '`recall_db.rec`'
status: filled
source_hash: 21a43a5fb9010deb
version_label: SWAT+ 62.0.0
---

**Primary target:** `recall_db(:)` (array of `type recall_databases`)  
**Read by:** [sym:recalldb_read]

## Bottom Line

The file `recall_db.rec` configures recall database entries used by the SWAT+ model for constituent recall data management.

It is optional and only read if the file exists.

The reader subroutine `recalldb_read` loads this file and populates the `recall_db` array of type `recall_databases`.

| Module | Role for this file |
| --- | --- |
| [sym:water_allocation_module] | Provides variables or types related to water allocation that may be referenced or updated during recall database reading, as imported by `recalldb_read`. |
| [sym:maximum_data_module] | Supplies the `db_mx` variable whose `recalldb_max` member is set to the maximum recall database index found in the file. |
| [sym:recall_module] | Defines the `type recall_databases` and the `recall_db` array that stores each record read from `recall_db.rec`. |
| [sym:hydrograph_module] | Imported but no direct variables or types are explicitly assigned in `recalldb_read`; likely used for related hydrograph data management. |

## File Variables

The file `recall_db.rec` contains records describing recall databases, each with a name and several constituent file data fields. Each record is read into an element of the `recall_db` array of type `recall_databases`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `recall_db%name` | character(len=13) |  | The name identifier for the recall database entry. |
| 3 |  | `recall_db%org_min` | type (constituent_file_data) |  | Data related to organic mineral constituents associated with this recall database entry. |
| 4 |  | `recall_db%pest` | type (constituent_file_data) |  | Data related to pesticide constituents associated with this recall database entry. |
| 5 |  | `recall_db%path` | type (constituent_file_data) |  | Data related to pathogen constituents associated with this recall database entry. |
| 6 |  | `recall_db%hmet` | type (constituent_file_data) |  | Data related to heavy metal constituents associated with this recall database entry. |
| 7 |  | `recall_db%salt` | type (constituent_file_data) |  | Data related to salt constituents associated with this recall database entry. |
| 8 |  | `recall_db%constit` | type (constituent_file_data) |  | Data related to other constituents associated with this recall database entry. |
| 9 |  | `recall_db%iorg_min` | integer |  | Integer index or flag related to organic mineral constituents. |
| 10 |  | `recall_db%ipest` | integer |  | Integer index or flag related to pesticide constituents. |
| 11 |  | `recall_db%ipath` | integer |  | Integer index or flag related to pathogen constituents. |
| 12 |  | `recall_db%ihmet` | integer |  | Integer index or flag related to heavy metal constituents. |
| 13 |  | `recall_db%isalt` | integer |  | Integer index or flag related to salt constituents. |
| 14 |  | `recall_db%iconstit` | integer |  | Integer index or flag related to other constituents. |

## Sample

```text
1 'RecallDB1' org_min_data pest_data path_data hmet_data salt_data constit_data
```

## Read Pattern

```fortran
open (107,file="recall_db.rec")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat = eof) k, recall_db(i)%name, recall_db(i)%org_min, recall_db(i)%pest, recall_db(i)%path, recall_db(i)%hmet, recall_db(i)%salt, recall_db(i)%constit
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="recall_db.rec")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat = eof) k, recall_db(i)%name, recall_db(i)%org_min, recall_db(i)%pest, recall_db(i)%path, recall_db(i)%hmet, recall_db(i)%salt, recall_db(i)%constit` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:recalldb_read] | backspace, close, open, read, rewind | Reads the recall database file `recall_db.rec` if it exists, determines the maximum record index, allocates arrays accordingly, then reads each recall database record into the `recall_db` array. Calls `recall_read(i)` to process each individual recall record. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists, as checked by `inquire`.
- The reader `recalldb_read` reads the file header lines, determines the maximum record index, allocates arrays, then reads each record into the `recall_db` array.
- The integer fields `iorg_min` through `iconstit` are declared in the type but not explicitly read in this routine; their values may be set elsewhere or defaulted.
- The sample read format is inferred since no example record is present in the source; actual constituent file data types are complex and not shown here.
