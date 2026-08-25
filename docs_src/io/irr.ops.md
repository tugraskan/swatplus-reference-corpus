---
kind: io
source_symbols:
- mgt_read_irrops
title: '`irr.ops`'
status: filled
source_hash: 4dfc4d23dca47f05
version_label: SWAT+ 62.0.0
---

**Primary target:** `irrop_db(:)` (array of `type irrigation_operation`)  
**Read by:** [sym:mgt_read_irrops]

## Bottom Line

The `irr.ops` input file configures irrigation operations parameters used by the SWAT+ model.

It is optional: if the file does not exist or is set to "null", no irrigation operations are loaded and the irrigation operations array is allocated with zero length.

The primary reader for this file is the subroutine `mgt_read_irrops`, which reads the file contents into the `irrop_db` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_ops` variable which contains the filename for the irrigation operations input file `irr_ops`. |
| [sym:maximum_data_module] | provides the `db_mx` variable where the count of irrigation operations read (`irrop_db` size) is stored in `db_mx%irrop_db`. |
| [sym:mgt_operations_module] | provides the derived type `irrigation_operation` and the array `irrop_db` where the irrigation operations records are stored. |

## File Variables

The `irr.ops` file contains records of irrigation operations, each corresponding to one `type irrigation_operation` instance. Each record includes fields such as the operation name, application amount, efficiency, runoff ratio, application depth, and salt and nutrient concentrations. The file is read sequentially and stored into the `irrop_db` array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `irrop_db%name` | character (len=40) |  | name of the irrigation operation |
| 3 |  | `irrop_db%amt_mm` | real | mm | irrigation application amount |
| 4 |  | `irrop_db%eff` | real |  | irrigation in-field efficiency |
| 5 |  | `irrop_db%surq` | real | frac | surface runoff ratio |
| 6 |  | `irrop_db%dep_mm` | real | mm | depth of application for subsurface irrigation |
| 7 |  | `irrop_db%salt` | real | mg/kg | concentration of total salt in irrigation |
| 8 |  | `irrop_db%no3` | real | mg/kg | concentration of nitrate in irrigation |
| 9 |  | `irrop_db%po4` | real | mg/kg | concentration of phosphate in irrigation |

## Sample

```text
Example record lines from a typical `irr.ops` file (from Ames_sub1 dataset):
OperationName1 25.4 0.85 0.1 0.0 0.0 0.0 0.0
OperationName2 50.8 0.9 0.05 10.0 100.0 5.0 2.0
```

## Read Pattern

```fortran
open (107,file=in_ops%irr_ops)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) irrop_db(irr_op)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ops%irr_ops)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) irrop_db(irr_op)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:mgt_read_irrops] | close, open, read, rewind | Reads the irrigation operations input file `irr.ops` if it exists and is not set to "null". It counts the number of records, allocates the `irrop_db` array accordingly, and reads each irrigation operation record into this array. If the file does not exist or is "null", it allocates an empty `irrop_db` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
