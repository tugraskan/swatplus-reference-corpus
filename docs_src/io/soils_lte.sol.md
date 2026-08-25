---
kind: io
source_symbols:
- soil_lte_db_read
title: '`soils_lte.sol`'
status: filled
source_hash: 63806f533434b655
version_label: SWAT+ 62.0.0
---

**Primary target:** `soil_lte(:)` (array of `type soil_lte_database`)  
**Read by:** [sym:soil_lte_db_read]

## Bottom Line

The file `soils_lte.sol` provides lookup table entries for soil texture properties used in the SWAT+ model.

It is optional; if the file does not exist or is set to "null", the soil_lte array is allocated with zero length.

The reader `soil_lte_db_read` loads this file, reading 12 fixed records into the `soil_lte` array of type `soil_lte_database`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_sol` variable which contains the filename `lte_sol` for this input file. |
| [sym:maximum_data_module] | No direct evidence of specific types or variables used from this module in the reader. |
| [sym:hru_lte_module] | No direct evidence of specific types or variables used from this module in the reader. |
| [sym:soil_data_module] | Provides the derived type `soil_lte_database` and the `soil_lte` array variable where records are stored. |

## File Variables

The file consists of 12 fixed records, each representing soil texture lookup table entries with properties mapped to the `soil_lte` array of derived type `soil_lte_database`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `soil_lte%texture` | character(len=16) |  | Soil texture name or identifier for the lookup entry. |
| 3 |  | `soil_lte%awc` | real |  | Available water capacity associated with the soil texture. |
| 4 |  | `soil_lte%por` | real |  | Porosity value for the soil texture. |
| 5 |  | `soil_lte%scon` | real |  | Soil conductivity parameter for the soil texture. |

## Sample

```text
Example record lines are not present in the source; typical records contain fields matching the `soil_lte_database` type, e.g.:
"SandyLoam       0.15 0.45 0.25"
```

## Read Pattern

```fortran
open (107,file=in_sol%lte_sol)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) soil_lte(k)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_sol%lte_sol)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) soil_lte(k)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:soil_lte_db_read] | open, read, close | Reads the optional `soils_lte.sol` file if it exists and is not set to "null". It reads two header lines and then reads 12 fixed records into the `soil_lte` array of type `soil_lte_database`. If the file does not exist or is "null", it allocates an empty `soil_lte` array. |

## Review Notes

- The file `soils_lte.sol` is optional and fixed to 12 records if present.
- The reader allocates `soil_lte` with 12 entries or zero length if the file is missing or set to "null".
- No sample record lines were found in the source; example format is inferred from the type fields.
- No direct usage of `maximum_data_module` or `hru_lte_module` variables is evident in the reader.
