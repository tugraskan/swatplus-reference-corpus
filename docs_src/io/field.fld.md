---
kind: io
source_symbols:
- field_read
title: '`field.fld`'
status: filled
source_hash: 7bc48cfdb18b50b9
version_label: SWAT+ 62.0.0
---

**Primary target:** `field_db(:)` (array of `type fields_db`)  
**Read by:** [sym:field_read]

## Bottom Line

The file `field.fld` configures wind erosion field parameters such as field name, length, width, and angle.

It is optional; if the file does not exist or is set to "null", an empty `field_db` array is allocated.

The primary reader that loads this file is the `field_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_hyd` variable which contains the filename `field_fld` for this input file |
| [sym:maximum_data_module] | provides the `db_mx` variable which stores the maximum number of fields read (`db_mx%field`) |
| [sym:topography_data_module] | provides the derived type `fields_db` and the array `field_db` where each record from the file is stored |

## File Variables

The file `field.fld` consists of records matching the derived type `fields_db`. Each record contains a field name and parameters describing the field's dimensions and orientation relevant for wind erosion modeling.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `field_db%name` | character(len=16) |  | field name identifier |
| 3 |  | `field_db%length` | real | m | field length for wind erosion |
| 4 |  | `field_db%wid` | real | m | field width for wind erosion |
| 5 |  | `field_db%ang` | real | deg | field angle for wind erosion |

## Sample

```text
Example record block from a typical `field.fld` file:
  Field1
  500.0 100.0 30.0
  Field2
  600.0 120.0 45.0
```

## Read Pattern

```fortran
open (107,file=in_hyd%field_fld)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) field_db(ith)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_hyd%field_fld)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) field_db(ith)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:field_read] | backspace, close, open, read, rewind | Reads the `field.fld` file, counts the number of field records, allocates the `field_db` array accordingly, and loads each record into `field_db` for wind erosion field configuration. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or set to "null", an empty `field_db` array is allocated.
- The sample read format is inferred from the type fields and typical usage; no explicit example record was found in the source.
