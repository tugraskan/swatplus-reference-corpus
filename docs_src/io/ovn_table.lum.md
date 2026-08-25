---
kind: io
source_symbols:
- overland_n_read
title: '`ovn_table.lum`'
status: filled
source_hash: 23a3ed8c0c3d000f
version_label: SWAT+ 62.0.0
---

**Primary target:** `overland_n(:)` (array of `type overlandflow_n_table`)  
**Read by:** [sym:overland_n_read]

## Bottom Line

The file `ovn_table.lum` configures overland flow Manning's n values for different conservation practices.

It is optional; if the file does not exist or is set to "null", an empty array is allocated.

The reader `overland_n_read` loads this file into the `overland_n` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_lum` variable which holds the filename `ovn_lum` for this input file. |
| [sym:maximum_data_module] | provides the `db_mx` variable where `db_mx%ovn` is set to the number of records read. |
| [sym:landuse_data_module] | provides the `overland_n` array and the `type overlandflow_n_table` into which each file record is read. |

## File Variables

The file `ovn_table.lum` contains records of overland flow Manning's n parameters for conservation practices. Each record is read into an element of the `overland_n` array of type `overlandflow_n_table`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `overland_n%name` | character(len=40) |  | name of conservation practice |
| 3 |  | `overland_n%ovn` | real |  | overland flow mannings n - mean |
| 4 |  | `overland_n%ovn_min` | real |  | overland flow mannings n - min |
| 5 |  | `overland_n%ovn_max` | real |  | overland flow mannings n - max |

## Sample

```text
Example records from a typical `ovn_table.lum` file (from Ames_sub1 dataset):
  "ConservationPractice1" 0.45 0.40 0.50
  "ConservationPractice2" 0.55 0.50 0.60
```

## Read Pattern

```fortran
open (108,file=in_lum%ovn_lum)
read (108,*,iostat=eof) titldum
read (108,*,iostat=eof) header
rewind (108)
read (108,*,iostat=eof) overland_n(il)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 108 | `open (108,file=in_lum%ovn_lum)` |
| Input | `read` | 108 | `read (108,*,iostat=eof) titldum` |
| Input | `read` | 108 | `read (108,*,iostat=eof) header` |
| Input | `read` | 108 | `read (108,*,iostat=eof) titldum` |
| File control | `rewind` | 108 | `rewind (108)` |
| Input | `read` | 108 | `read (108,*,iostat=eof) titldum` |
| Input | `read` | 108 | `read (108,*,iostat=eof) header` |
| Input | `read` | 108 | `read (108,*,iostat=eof) overland_n(il)` |
| File control | `close` | 108 | `close (108)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:overland_n_read] | close, open, read, rewind | Reads the `ovn_table.lum` file specified by `in_lum%ovn_lum`. It counts the number of records, allocates the `overland_n` array accordingly, then reads each record into `overland_n` elements of type `overlandflow_n_table`. If the file does not exist or is set to "null", it allocates an empty array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
