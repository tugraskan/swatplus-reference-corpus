---
kind: io
source_symbols:
- scen_read_filtstrip
title: '`filterstrip.str`'
status: filled
source_hash: df87b621c66140a5
version_label: SWAT+ 62.0.0
---

**Primary target:** `filtstrip_db(:)` (array of `type filtstrip_operation`)  
**Read by:** [sym:scen_read_filtstrip]

## Bottom Line

The `filterstrip.str` file configures vegetative filter strip operations for the SWAT+ model.

It is optional; if the file does not exist or is set to "null", no filter strip operations are loaded.

The file is read by the `scen_read_filtstrip` subroutine, which populates the `filtstrip_db` array with filter strip operation records.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_str` structure containing the filename `fstrip_str` for the filter strip input file. |
| [sym:maximum_data_module] | Provides the `db_mx` structure where the total number of filter strip operations `filtop_db` is stored. |
| [sym:mgt_operations_module] | Defines the `type filtstrip_operation` and the `filtstrip_db` array where each filter strip record is stored. |

## File Variables

The file consists of a header block followed by multiple records of filter strip operations. Each record maps to one element of the `filtstrip_db` array of type `filtstrip_operation`. The file is read sequentially, counting records first to allocate the array, then reading the data into the array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `filtstrip_db%name` | character (len=40) |  | Name identifier of the filter strip operation |
| 3 |  | `filtstrip_db%vfsi` | integer |  | On/off flag indicating whether the vegetative filter strip is active |
| 4 |  | `filtstrip_db%vfsratio` | real |  | Contouring USLE P factor representing the effect of filter strip on erosion |
| 5 |  | `filtstrip_db%vfscon` | real |  | Fraction of the total runoff from the entire field that passes through the filter strip |
| 6 |  | `filtstrip_db%vfsch` | real |  | Fraction of flow entering the most concentrated 10% of the vegetative filter strip |

## Sample

```text
Example record format from `filterstrip.str` (fields after leading record id):
NAME                           VFSi  VFSRATIO  VFSCON  VFSCH
Example:
FilterStrip1                   1     0.5       0.3     0.1
```

## Read Pattern

```fortran
open (107,file=in_str%fstrip_str)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do while (eof == 0)
  read (107,*,iostat=eof) titldum
  imax = imax + 1
end do
allocate (filtstrip_db(0:imax))
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do ifiltop = 1, imax
  read (107,*,iostat=eof) filtstrip_db(ifiltop)
end do
close(107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_str%fstrip_str)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) filtstrip_db(ifiltop)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:scen_read_filtstrip] | open, read, rewind, close | Reads the `filterstrip.str` file if it exists and is not set to "null". It first counts the number of filter strip records to allocate the `filtstrip_db` array, then rewinds and reads the actual filter strip operation records into this array. If the file does not exist or is "null", it allocates an empty array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and controls vegetative filter strip operations in the model.
- The reader uses a two-pass approach: first counting records to allocate storage, then reading data.
- No sample data records were found in the source; the sample read format is inferred from the type declaration.
