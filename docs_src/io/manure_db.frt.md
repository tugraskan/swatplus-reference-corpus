---
kind: io
source_symbols:
- manure_db_read
title: '`manure_db.frt`'
status: filled
source_hash: 787b62ec5c2302ca
version_label: SWAT+ 62.0.0
---

**Primary target:** `manure_db(:)` (array of `type manure_database`)  
**Read by:** [sym:manure_db_read]

## Bottom Line

The file `manure_db.frt` configures manure type definitions used in the SWAT+ model, specifying manure characteristics such as organic matter, pesticides, pathogens, heavy metals, salts, and other constituents.

This file is optional; if it does not exist or is set to "null", an empty manure database is allocated.

The reader subroutine `manure_db_read` loads this file and populates the `manure_db` array with manure type records.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides file input utilities and possibly global input file handling used by `manure_db_read`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable which stores maximum counts such as `manure_om` and `manureparm` used for array sizing and cross-referencing manure organic matter types. |
| [sym:fertilizer_data_module] | Defines the `manure_db` array and the `type manure_database` which holds manure type data fields read from the file. |

## File Variables

The file `manure_db.frt` contains records defining manure types with fields for manure name, associated organic matter, pesticides, pathogens, heavy metals, salts, other constituents, and descriptive text. Each record maps directly to an element of the `manure_db` array of derived type `manure_database`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `manure_db%name` | character (len=25) |  | name of manure type |
| 3 |  | `manure_db%org_min` | character (len=25) |  | sediment, carbon, and nutrients |
| 4 |  | `manure_db%pests` | character (len=25) |  | pesticides - ppm |
| 5 |  | `manure_db%paths` | character (len=25) |  | pathogens - cfu |
| 6 |  | `manure_db%hmets` | character (len=25) |  | heavy metals - ppm |
| 7 |  | `manure_db%salts` | character (len=25) |  | salt ions - ppm |
| 8 |  | `manure_db%constit` | character (len=25) |  | other constituents - ppm |
| 9 |  | `manure_db%descrip` | character (len=80) |  | description |
| 10 |  | `manure_db%iorg_min` | integer |  | sediment, carbon, and nutrients - pointer to |
| 11 |  | `manure_db%ipests` | integer |  | pesticides - pointer to |
| 12 |  | `manure_db%ipaths` | integer |  | pathogens - pointer to |
| 13 |  | `manure_db%imets` | integer |  | heavy metals - pointer to |
| 14 |  | `manure_db%isalts` | integer |  | salt ions - pointer to |
| 15 |  | `manure_db%iconstit` | integer |  | other constituents - pointer to |

## Sample

```text
Example record lines from manure_db.frt:
ManureType1 OrganicMatter1 Pesticide1 Pathogen1 HeavyMetal1 SaltIon1 Constituent1 Description of manure type 1
ManureType2 OrganicMatter2 Pesticide2 Pathogen2 HeavyMetal2 SaltIon2 Constituent2 Description of manure type 2
```

## Read Pattern

```fortran
open (107,file="manure_db.frt")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) manure_db(it)%name, manure_db(it)%org_min, manure_db(it)%pests, manure_db(it)%paths, manure_db(it)%hmets, manure_db(it)%salts, manure_db(it)%constit, manure_db(it)%descrip
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="manure_db.frt")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) manure_db(it)%name, manure_db(it)%org_min, manure_db(it)%pests, manure_db(it)%paths, manure_db(it)%hmets, manure_db(it)%salts, manure_db(it)%constit, manure_db(it)%descrip` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:manure_db_read] | close, open, read, rewind | Reads the manure_db.frt file, counts the number of manure records, allocates the manure_db array accordingly, and reads each manure record into the array. It also cross-references the organic matter name to the manure_om database to set the iorg_min pointer. The reader handles the case where the file does not exist or is set to "null" by allocating an empty manure_db array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The reader crosswalk for pests to fertdb is commented out and thus ipests is not set by manure_db_read.
- The sample_read_format is a placeholder example constructed from field names; no actual example records were found in the source.
