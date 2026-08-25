---
kind: io
source_symbols:
- mgt_read_sweepops
title: '`sweep.ops`'
status: filled
source_hash: 0261da41708fd5bb
version_label: SWAT+ 62.0.0
---

**Primary target:** `sweepop_db(:)` (array of `type streetsweep_operation`)  
**Read by:** [sym:mgt_read_sweepops]

## Bottom Line

The `sweep.ops` input file configures street sweeping operations used in the model to represent removal of pollutants by street sweeping.

This file is optional; if it does not exist or is set to "null", no sweeping operations are loaded and the corresponding data array is allocated empty.

The file is read by the `mgt_read_sweepops` subroutine, which loads the data into the `sweepop_db` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_ops` variable which contains the file path for `sweep.ops` |
| [sym:maximum_data_module] | provides the `db_mx` variable which stores the maximum count of sweeping operations read |
| [sym:mgt_operations_module] | provides the `sweepop_db` array and the `type streetsweep_operation` definition used to store each record |

## File Variables

The `sweep.ops` file contains records of street sweeping operations, each mapped to an element of the `sweepop_db` array of type `streetsweep_operation`. Each record includes a name, removal efficiency, and availability factor.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `sweepop_db%name` | character (len=40) |  | name of the street sweeping operation |
| 3 |  | `sweepop_db%eff` | real | none | removal efficiency of sweeping operation |
| 4 |  | `sweepop_db%fr_curb` | real | none | availability factor, the fraction of the curbside swept |

## Sample

```text
Example records from a typical `sweep.ops` file are not present in the source code or context packet; users should refer to reference datasets such as Ames_sub1 for format examples.
```

## Read Pattern

```fortran
open (107,file=in_ops%sweep_ops)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) sweepop_db(isweepop)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ops%sweep_ops)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) sweepop_db(isweepop)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:mgt_read_sweepops] | close, open, read, rewind | Reads the `sweep.ops` file if it exists and is not set to "null". It counts the number of street sweeping operation records, allocates the `sweepop_db` array accordingly, then reads each record into this array. If the file does not exist or is "null", it allocates an empty array. It also updates `db_mx%sweepop_db` with the number of records read. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample record format is not present in the source or context; users should consult reference datasets for examples.
