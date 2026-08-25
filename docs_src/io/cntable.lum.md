---
kind: io
source_symbols:
- cntbl_read
title: '`cntable.lum`'
status: filled
source_hash: dee5295ccad9938a
version_label: SWAT+ 62.0.0
---

**Primary target:** `cn(:)` (array of `type curvenumber_table`)  
**Read by:** [sym:cntbl_read]

## Bottom Line

The file `cntable.lum` configures curve number lookup tables used in hydrologic modeling.

It is optional: if the file does not exist or is set to "null", an empty curve number array is allocated.

The reader `cntbl_read` loads this file into the array `cn` of type `curvenumber_table`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_lum%cntable_lum` used to locate the file |
| [sym:maximum_data_module] | provides the global variable `db_mx%cn_lu` which is set to the number of curve number records read |
| [sym:landuse_data_module] | provides the derived type `curvenumber_table` and the array `cn` where each record is stored |

## File Variables

The file consists of multiple records each representing a curve number entry with a name and a curve number value. Each record is read into an element of the array `cn` of type `curvenumber_table`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `cn%name` | character(len=40) |  | name includes abbrev for lu/treatment/condition |
| 3 |  | `cn%cn` | real |  | curve number |

## Sample

```text
Example record block from a typical `cntable.lum` file (e.g. Ames_sub1):
  "Curve Number Table Title"
  "Header describing the curve number data"
  "Name1" 30.0
  "Name2" 55.0
  "Name3" 70.0
  "Name4" 77.0
```

## Read Pattern

```fortran
open (107,file=in_lum%cntable_lum)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) cn(icno)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_lum%cntable_lum)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cn(icno)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cntbl_read] | close, open, read, rewind | Reads the curve number lookup table file `cntable.lum` into the array `cn` of type `curvenumber_table`. If the file does not exist or is set to "null", it allocates an empty array. It counts the number of records by reading through the file once, then rewinds and reads the data into the array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
