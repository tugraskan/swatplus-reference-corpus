---
kind: io
source_symbols:
- cons_prac_read
title: '`cons_practice.lum`'
status: filled
source_hash: 305ceffbb4347084
version_label: SWAT+ 62.0.0
---

**Primary target:** `cons_prac(:)` (array of `type conservation_practice_table`)  
**Read by:** [sym:cons_prac_read]

## Bottom Line

The file `cons_practice.lum` configures conservation practice parameters such as name, USLE P factor, and maximum slope length used in land use modeling.

This file is optional; if it does not exist or is set to "null", the conservation practice array is allocated with zero length.

The reader `cons_prac_read` loads this file into the `cons_prac` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_lum%cons_prac_lum` used to locate the file |
| [sym:maximum_data_module] | provides the global counter variable `db_mx%cons_prac` to store the number of conservation practices read |
| [sym:landuse_data_module] | provides the derived type `conservation_practice_table` and the array `cons_prac` where the file records are stored |

## File Variables

The file consists of multiple records each corresponding to a conservation practice. Each record is read into an element of the `cons_prac` array of type `conservation_practice_table`. The file includes a title line and header lines which are read and discarded before reading the data records.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `cons_prac%name` | character(len=40) |  | name of conservation practice |
| 3 |  | `cons_prac%pfac` | real |  | usle p factor |
| 4 |  | `cons_prac%sl_len_mx` | real | m | m !maximum slope length |

## Sample

```text
Example record format (fields separated by spaces or tabs):
ConservationPracticeName 0.8 150.0
Where the fields correspond to:
1. name (character, max 40 chars)
2. pfac (real, USLE P factor)
3. sl_len_mx (real, maximum slope length in meters)
```

## Read Pattern

```fortran
open (107,file=in_lum%cons_prac_lum)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) cons_prac(icp)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_lum%cons_prac_lum)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cons_prac(icp)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cons_prac_read] | close, open, read, rewind | Reads the file `cons_practice.lum` if it exists and is not set to "null". It counts the number of conservation practice records by reading through the file once, allocates the `cons_prac` array accordingly, rewinds the file, and then reads all conservation practice records into the `cons_prac` array. If the file does not exist or is "null", it allocates `cons_prac` with zero length. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the check for existence and "null" string in the reader.
- The reader uses a two-pass approach: first to count records, then to read them after allocation.
- No sample data records were found in the source; the sample format is inferred from the type definition fields.
