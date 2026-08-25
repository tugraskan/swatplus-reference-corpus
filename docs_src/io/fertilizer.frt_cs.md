---
kind: io
source_symbols:
- cs_fert_read
title: '`fertilizer.frt_cs`'
status: filled
source_hash: 35cfdac9a842c8be
version_label: SWAT+ 62.0.0
---

**Primary target:** `fert_cs(:)` (array of `type fert_db_cs`)  
**Read by:** [sym:cs_fert_read]

## Bottom Line

The file `fertilizer.frt_cs` contains constituent fertilizer loading rates (kg/ha) for various fertilizer types used in the model.

It is optional and only read if the file exists.

The reader subroutine `cs_fert_read` loads this file into the array `fert_cs` of derived type `fert_db_cs`.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the `fert_cs_flag` logical flag indicating if constituent fertilizer data has been read. |
| [sym:input_file_module] | Used for input file handling and possibly for file existence checking. |
| [sym:maximum_data_module] | Provides `db_mx%fertparm` which determines the number of fertilizer parameter records to read and allocate. |
| [sym:cs_module] | Defines the derived type `fert_db_cs` and the array `fert_cs` where the fertilizer constituent data is stored. |

## File Variables

The file consists of multiple records each representing a fertilizer constituent loading entry. Each record is mapped to an element of the array `fert_cs` of type `fert_db_cs`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `fert_cs%fertnm` | character(len=16) |  | Name of the fertilizer constituent |
| 3 |  | `fert_cs%seo4` | real | kg seo4/ha | fertilizer load of seo4 (kg/ha) |
| 4 |  | `fert_cs%seo3` | real | kg seo3/ha | fertilizer load of seo3 (kg/ha) |
| 5 |  | `fert_cs%boron` | real | kg boron/ha | fertilizer load of boron (kg/ha) |

## Sample

```text
Example record format (fields separated by spaces or tabs):
FERTNAME 0.0 0.0 0.0
Where FERTNAME is a string up to 16 characters, followed by real values for seo4, seo3, and boron fertilizer loads in kg/ha.
```

## Read Pattern

```fortran
open (107,file="fertilizer.frt_cs")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*) fert_cs(icsi)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="fertilizer.frt_cs")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*) fert_cs(icsi)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cs_fert_read] | open, read, close | Reads the file `fertilizer.frt_cs` if it exists, allocates the `fert_cs` array to the number of fertilizer parameters, sets the `fert_cs_flag` to indicate data presence, and loads constituent fertilizer loading rates (kg/ha) into the `fert_cs` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists, as indicated by the inquire statement.
- The reader sets a flag `fert_cs_flag` in `constituent_mass_module` to indicate the fertilizer constituent data has been loaded.
- No sample data records were found in the source; the sample format is inferred from the type definition and read statements.
