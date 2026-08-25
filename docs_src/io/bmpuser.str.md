---
kind: io
source_symbols:
- scen_read_bmpuser
title: '`bmpuser.str`'
status: filled
source_hash: 0debca8782c6e1f7
version_label: SWAT+ 62.0.0
---

**Primary target:** `bmpuser_db(:)` (array of `type bmpuser_operation`)  
**Read by:** [sym:scen_read_bmpuser]

## Bottom Line

The file `bmpuser.str` defines user-specified Best Management Practice (BMP) operations for upland chemical and sediment removal.

It is optional; if absent or set to "null", an empty BMP user database is allocated.

The reader `scen_read_bmpuser` loads this file into the array `bmpuser_db`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file name string `in_str%bmpuser_str` used to locate the `bmpuser.str` file. |
| [sym:maximum_data_module] | Provides the global data structure `db_mx` where the count of BMP user operations `bmpuserop_db` is stored. |
| [sym:mgt_operations_module] | Defines the derived type `bmpuser_operation` and the array `bmpuser_db` where each BMP user operation record is stored. |

## File Variables

The file consists of multiple records each describing a BMP operation with fields mapped to the components of the derived type `bmpuser_operation`. Each record is read into an element of the array `bmpuser_db`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `bmpuser_db%name` | character (len=40) |  | Name identifier of the BMP operation |
| 3 |  | `bmpuser_db%bmp_flag` | integer |  | Flag indicating BMP operation status or type |
| 4 |  | `bmpuser_db%bmp_sed` | real | % | Sediment removal efficiency by BMP |
| 5 |  | `bmpuser_db%bmp_pp` | real | % | Particulate phosphorus removal efficiency by BMP |
| 6 |  | `bmpuser_db%bmp_sp` | real | % | Soluble phosphorus removal efficiency by BMP |
| 7 |  | `bmpuser_db%bmp_pn` | real | % | Particulate nitrogen removal efficiency by BMP |
| 8 |  | `bmpuser_db%bmp_sn` | real | % | Soluble nitrogen removal efficiency by BMP |
| 9 |  | `bmpuser_db%bmp_bac` | real | % | Bacteria removal efficiency by BMP |

## Sample

```text
Example record format (fields separated by spaces or commas):
"BMP_Name" 1 25.0 30.0 15.0 20.0 10.0 5.0 40.0
Where fields correspond to: name, bmp_flag, bmp_sed, bmp_pp, bmp_sp, bmp_pn, bmp_sn, bmp_bac
```

## Read Pattern

```fortran
open (107,file=in_str%bmpuser_str)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do while (not eof)
  read (107,*,iostat=eof) titldum
  imax = imax + 1
end do
allocate (bmpuser_db(0:imax))
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do ibmpop = 1, imax
  read (107,*,iostat=eof) bmpuser_db(ibmpop)
end do
close(107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_str%bmpuser_str)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) bmpuser_db(ibmpop)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:scen_read_bmpuser] | open, read, rewind, close | Reads the optional BMP user operations file `bmpuser.str` and populates the array `bmpuser_db` with BMP operation records. If the file does not exist or is set to "null", allocates an empty BMP user database. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and may be omitted or set to "null" to disable user BMP operations.
- The reader counts records by reading through the file once, then allocates and rereads to populate the array.
- No explicit sample data was found in the source; the sample format is inferred from the type declaration.
