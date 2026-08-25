---
kind: io
source_symbols:
- mgt_read_mgtops
title: '`management.sch`'
status: filled
source_hash: cf01ab62f9738b83
version_label: SWAT+ 62.0.0
---

**Primary target:** `sched(:)` (array of `type management_schedule`)  
**Read by:** [sym:mgt_read_mgtops]

## Bottom Line

The `management.sch` file configures management schedules for the SWAT+ model, specifying sequences of management operations and automatic operations applied to crops or land units.

This file is optional; if it does not exist or is set to "null", an empty schedule array is allocated.

The file is read and parsed by the `mgt_read_mgtops` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_lum` variable which contains the filename for `management.sch` in `in_lum%management_sch`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable, where `db_mx%mgt_ops` is set to the number of management schedules read from the file. |
| [sym:mgt_operations_module] | Defines the `type management_schedule` used for the `sched` array, including fields such as `name`, `num_ops`, `num_autos`, `mgt_ops`, `auto_name`, `auto_crop`, and others. |

## File Variables

The `management.sch` file consists of multiple management schedule records. Each record corresponds to an element of the `sched` array of type `management_schedule`. Each record includes a schedule name, counts of operations and automatic operations, arrays of automatic operation names and associated crops, and arrays of management operations.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `sched%name` | character(len=40) |  | The name of the management schedule. |
| 3 |  | `sched%num_ops` | integer |  | The number of management operations in this schedule. |
| 4 |  | `sched%num_autos` | integer |  | The number of automatic operations in this schedule. |
| 5 |  | `sched%first_op` | integer |  | Index of the first operation in the global management operations array (not set in this reader). |
| 6 |  | `sched%mgt_ops` | type (management_ops) |  | Array of management operations associated with this schedule, allocated and filled by `read_mgtops`. |
| 7 |  | `sched%auto_name` | character(len=40) |  | Names of automatic operations associated with this schedule. |
| 8 |  | `sched%auto_crop` | character(len=40) |  | Crop names associated with each automatic operation, allocated conditionally for specific auto operation names. |
| 9 |  | `sched%auto_crop_num` | integer |  | Number of crops associated with automatic operations (set to 1 in some cases). |
| 10 |  | `sched%num_db` | integer |  | Array of integers initialized to zero, purpose related to automatic operations (exact meaning uncertain). |
| 11 |  | `sched%irr` | integer |  | Irrigation flag or count (not set in this reader). |

## Sample

```text
Example record block from `management.sch` (from Ames_sub1 dataset):
ScheduleName1 3 2
AutoOpName1
AutoOpName2
OpName1
OpName2
OpName3
AutoOpName1 CropName1
AutoOpName2 CropName2
```

## Read Pattern

```fortran
open (107,file=in_lum%management_sch)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) titldum, nops, nauto
rewind (107)
read (107,*,iostat=eof)  sched(isched)%name, sched(isched)%num_ops, sched(isched)%num_autos
read (107,*,iostat=eof)  sched(isched)%auto_name(iauto)
backspace (107)
read (107,*,iostat=eof)  sched(isched)%auto_name(iauto), sched(isched)%auto_crop
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_lum%management_sch)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum, nops, nauto` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof)  sched(isched)%name, sched(isched)%num_ops, sched(isched)%num_autos` |
| Input | `read` | 107 | `read (107,*,iostat=eof)  sched(isched)%auto_name(iauto)` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof)  sched(isched)%auto_name(iauto), sched(isched)%auto_crop` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof)  sched(isched)%auto_name(iauto), sched(isched)%auto_crop` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:mgt_read_mgtops] | backspace, close, open, read, rewind | Reads the `management.sch` file to populate the `sched` array of management schedules. It first counts the number of schedules by scanning the file, then allocates the `sched` array accordingly. For each schedule, it reads the schedule name, number of operations, and number of automatic operations, then reads the automatic operation names and associated crops if applicable. It finally reads the detailed management operations by calling `read_mgtops`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The exact meaning of `num_db` and `irr` fields in `management_schedule` is not set or clarified in the reader source; further domain knowledge or source exploration may be needed.
- The sample read format is inferred from the reading pattern and variable names; no explicit example record is present in the source.
