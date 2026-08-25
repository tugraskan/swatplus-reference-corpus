---
kind: io
source_symbols:
- mgt_read_fireops
title: '`fire.ops`'
status: filled
source_hash: 9d9844bf9069de2e
version_label: SWAT+ 62.0.0
---

**Primary target:** `fire_db(:)` (array of `type fire_operation`)  
**Read by:** [sym:mgt_read_fireops]

## Bottom Line

The `fire.ops` input file configures fire operation parameters used in the model, specifically detailing fire operation names, changes in curve number II values, and fraction burned.

This file is optional; if it does not exist or is set to "null", an empty fire operation database is allocated.

The file is read by the `mgt_read_fireops` subroutine, which loads the data into the `fire_db` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_ops` variable which contains the filename for the fire operations input file (`fire_ops`), used to locate and open the file. |
| [sym:maximum_data_module] | provides the `db_mx` variable, specifically `db_mx%fireop_db`, which stores the count of fire operations read from the file. |
| [sym:mgt_operations_module] | provides the `fire_db` array of `type fire_operation` where each record from the file is stored. |

## File Variables

The `fire.ops` file consists of records describing fire operations, each mapped to an element of the `fire_db` array of `type fire_operation`. Each record includes a name, a change in SCS curve number II value, and a fraction burned. The file is read sequentially after skipping header lines.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `fire_db%name` | character (len=40) |  | fire operation name |
| 3 |  | `fire_db%cn2_upd` | real |  | change in SCS curve number II value |
| 4 |  | `fire_db%fr_burn` | real |  | fraction burned |

## Sample

```text
Example records are not present in the source; typical records would start after two header lines and include fields matching the `fire_operation` type: a character string (name), followed by two real numbers (cn2_upd and fr_burn).
```

## Read Pattern

```fortran
open (107,file=in_ops%fire_ops)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do while (eof == 0)
  read (107,*,iostat=eof) titldum
end do
allocate (fire_db(0:imax))
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do ifireop = 1, imax
  read (107,*,iostat=eof) fire_db(ifireop)
end do
close(107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ops%fire_ops)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) fire_db(ifireop)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:mgt_read_fireops] | close, open, read, rewind | Reads the `fire.ops` file if it exists and is not set to "null", counts the number of fire operation records, allocates the `fire_db` array accordingly, and loads each fire operation record into `fire_db`. If the file does not exist or is "null", it allocates an empty `fire_db` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The source code does not provide example data records; sample record format is inferred from the `fire_operation` type definition.
- The file is optional and the reader handles non-existence or "null" filename by allocating an empty fire operation array.
