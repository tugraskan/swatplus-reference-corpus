---
kind: io
source_symbols:
- shade_factor_read
title: '`shade_factor.shf`'
status: filled
source_hash: 589d25e253b603ad
version_label: SWAT+ 62.0.0
---

**Primary target:** `shf_db(:)` (array of `type shade_factor_data`)  
**Read by:** [sym:shade_factor_read]

## Bottom Line

shade_factor.shf is an input file that provides shade factor values by day of year and landscape unit.

It is optional; if the file does not exist or is set to "null", an empty shade factor database is allocated.

The file is read by the `shade_factor_read` subroutine, which loads the data into the `shf_db` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_shf` variable which contains the filename `ssff_shf` for shade_factor.shf |
| [sym:maximum_data_module] | provides the `db_mx` variable whose `shf` field is set to the number of shade factor records read |
| [sym:sd_channel_module] | not directly used for types or variables in this reader |
| [sym:hydrograph_module] | provides the `shf_db` array of `type shade_factor_data` where the file records are stored |

## File Variables

shade_factor.shf consists of multiple records each containing a day of year, a landscape unit, and a shade factor value. These map to the fields of the `shade_factor_data` derived type stored in the `shf_db` array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `shf_db%jday` | integer | none | day of the year |
| 3 |  | `shf_db%lsu` | integer | none | landscape unit |
| 4 |  | `shf_db%value` | real | none | shade factor value |

## Sample

```text
Example record lines from shade_factor.shf might look like:
  150  1  0.75
  151  1  0.80
  152  2  0.65
where columns correspond to jday, lsu, and value respectively.
```

## Read Pattern

```fortran
open (107,file=in_shf%ssff_shf)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) shf_db(idlsu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_shf%ssff_shf)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) shf_db(idlsu)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:shade_factor_read] | close, open, read, rewind | Reads the shade_factor.shf file if it exists, counts the number of records, allocates the shade factor database array `shf_db`, and loads each record into it. If the file is missing or set to "null", allocates an empty database. Updates `db_mx%shf` with the number of records read. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The reader uses a double read pattern: first to count records, then to read data after rewind.
- The file is optional; if missing or set to "null", an empty shade factor database is allocated.
- No explicit sample data lines are present in the source; the sample format is inferred from the `shade_factor_data` type fields.
