---
kind: io
source_symbols:
- snowdb_read
title: '`snow.sno`'
status: filled
source_hash: 4fd12fa587158fa3
version_label: SWAT+ 62.0.0
---

**Primary target:** `snodb(:)` (array of `type snow_parameters`)  
**Read by:** [sym:snowdb_read]

## Bottom Line

The file `snow.sno` configures snow parameter data for the model, specifying snow temperature thresholds, melt rates, snow water content, and related snowpack properties.

It is optional: if the file does not exist or is set to "null", an empty snow parameter array is allocated.

The reader `snowdb_read` loads this file into the `snodb` array of `type snow_parameters`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_parmdb` variable which contains the filename for the snow parameter database (`in_parmdb%snow`), used to locate the `snow.sno` file. |
| [sym:maximum_data_module] | provides the `db_mx` variable, whose `sno` member is set to the number of snow parameter records read from the file. |
| [sym:hru_module] | provides the `snodb` array of `type snow_parameters` into which the snow parameter records from the file are read and stored. |

## File Variables

The file `snow.sno` contains multiple records of snow parameter data, each record corresponding to one snow parameter set stored as an element of the `snodb` array of derived type `snow_parameters`. Each record includes fields such as snow temperature thresholds, melt rates, snow water content, and snow cover fractions.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `snodb%name` | character (len=40) |  | Snow parameter set name or identifier |
| 3 |  | `snodb%falltmp` | real | deg C | Snowfall temperature threshold |
| 4 |  | `snodb%melttmp` | real | deg C | Snow melt base temperature |
| 5 |  | `snodb%meltmx` | real | mm/deg C/day | Maximum snow melt rate during the year (around June 21) |
| 6 |  | `snodb%meltmn` | real | mm/deg C/day | Minimum snow melt rate during the year (around Dec 21) |
| 7 |  | `snodb%timp` | real | none | Snow pack temperature lag factor (range 0-1) |
| 8 |  | `snodb%covmx` | real | mm H20 | Snow water content at full ground cover |
| 9 |  | `snodb%cov50` | real | none | Fraction of `covmx` at 50% snow cover |
| 10 |  | `snodb%init_mm` | real | mm H20 | Initial snow water content at simulation start |

## Sample

```text
Example record format (fields in order):
name (character*40), falltmp (real), melttmp (real), meltmx (real), meltmn (real), timp (real), covmx (real), cov50 (real), init_mm (real)
Example record (from Ames_sub1 or similar dataset):
  "DefaultSnowParam" 0.0 0.5 4.5 0.5 0.8 25.0 0.5 0.0
```

## Read Pattern

```fortran
open (107,file=in_parmdb%snow)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) snodb(isno)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_parmdb%snow)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) snodb(isno)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:snowdb_read] | open, read, rewind, close | Reads the snow parameter database file `snow.sno` specified by `in_parmdb%snow`. It first checks if the file exists; if not, it allocates an empty snow parameter array. If the file exists, it counts the number of records by reading through the file, rewinds, allocates the `snodb` array accordingly, and reads all snow parameter records into `snodb`. It sets `db_mx%sno` to the number of records read. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `snow.sno` is optional; if missing or set to "null", an empty snow parameter array is allocated.
- The reader `snowdb_read` uses `in_parmdb%snow` as the filename and stores data into `snodb` from `hru_module`.
- No sample data record was found in the source; the sample record is a plausible example based on the type definition.
- No ambiguous or uncertain source facts detected.
