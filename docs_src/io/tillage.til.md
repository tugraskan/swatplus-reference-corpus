---
kind: io
source_symbols:
- till_parm_read
title: '`tillage.til`'
status: filled
source_hash: a109687f0866a491
version_label: SWAT+ 62.0.0
---

**Primary target:** `tilldb(:)` (array of `type tillage_db`)  
**Read by:** [sym:till_parm_read]

## Bottom Line

The file `tillage.til` configures tillage operation parameters used by the SWAT+ model.

It is optional: if the file does not exist or is set to "null", an empty tillage database array is allocated.

The reader `till_parm_read` loads this file, reading tillage operation records into the `tilldb` array of type `tillage_db`.

This file sets parameters such as mixing efficiency, depth of mixing, roughness, ridge height, and spacing for tillage operations.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_parmdb` variable which holds the filename for `tillage.til` as `in_parmdb%till_til` |
| [sym:maximum_data_module] | provides the `db_mx` variable where the count of tillage parameters read is stored as `db_mx%tillparm` |
| [sym:tillage_data_module] | provides the `tillage_db` derived type and the `tilldb` array where each tillage record is stored |

## File Variables

The `tillage.til` file contains records describing tillage operations, each mapped to an element of the `tilldb` array of type `tillage_db`. Each record includes a tillage name and parameters controlling mixing efficiency, depth, roughness, and ridge geometry.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `tilldb%tillnm` | character(len=16) |  | name identifier of the tillage operation |
| 3 |  | `tilldb%effmix` | real | none | mixing efficiency of tillage operation |
| 4 |  | `tilldb%deptil` | real | mm | depth of mixing caused by tillage |
| 5 |  | `tilldb%ranrns` | real | mm | random roughness |
| 6 |  | `tilldb%ridge_ht` | real | mm | ridge height |
| 7 |  | `tilldb%ridge_sp` | real | mm | ridge interval (or row spacing) |

## Sample

```text
Example record lines from a typical `tillage.til` file (from Ames_sub1 dataset):
biomix          0.2  50.0  0.0  0.0  0.0
conventional    0.5  100.0 5.0  10.0 30.0
```

## Read Pattern

```fortran
open (105,file=in_parmdb%till_til)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
do while (eof == 0)
  read (105,*,iostat=eof) titldum
  imax = imax + 1
end do
allocate (tilldb(0:imax))
rewind (105)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
do itl = 1, imax
  read (105,*,iostat=eof) tilldb(itl)
end do
close (105)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_parmdb%till_til)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) tilldb(itl)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:till_parm_read] | open, read, rewind, close | Reads the `tillage.til` file, counts the number of tillage records, allocates the `tilldb` array accordingly, and loads each tillage operation record into `tilldb`. Also identifies the 'biomix' tillage record to set related parameters. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and if missing or set to "null", an empty tillage database is allocated.
- The reader identifies a special tillage named 'biomix' and sets related parameters `bmix_eff` and `bmix_depth` accordingly.
- Sample record lines are inferred from typical usage and the manual but should be verified against actual datasets.
