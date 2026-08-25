---
kind: io
source_symbols:
- scen_read_grwway
title: '`grassedww.str`'
status: filled
source_hash: aae430cafacf41f9
version_label: SWAT+ 62.0.0
---

**Primary target:** `grwaterway_db(:)` (array of `type grwaterway_operation`)  
**Read by:** [sym:scen_read_grwway]

## Bottom Line

The file `grassedww.str` configures grassed waterway operations for the SWAT+ model.

It is optional; if the file does not exist or is set to "null", an empty grassed waterway database is allocated.

The reader `scen_read_grwway` loads this file and populates the `grwaterway_db` array with grassed waterway operation records.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_str` variable which contains the filename `grassww_str` for the grassed waterway input file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable where the total number of grassed waterway operations read (`grassop_db`) is stored. |
| [sym:mgt_operations_module] | Defines the `type grwaterway_operation` and the `grwaterway_db` array where the file records are stored. |

## File Variables

The file consists of multiple records each describing a grassed waterway operation. Each record is read into an element of the `grwaterway_db` array of type `grwaterway_operation`. The file includes a title line and a header line before the data records.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `grwaterway_db%name` | character (len=40) |  | Name identifier for the grassed waterway operation |
| 3 |  | `grwaterway_db%grwat_i` | integer | none | On/off flag indicating whether the grassed waterway simulation is active |
| 4 |  | `grwaterway_db%grwat_n` | real | none | Manning's n roughness coefficient for the grassed waterway |
| 5 |  | `grwaterway_db%grwat_spcon` | real | none | User-defined sediment transport coefficient for the grassed waterway |
| 6 |  | `grwaterway_db%grwat_d` | real | m | Depth of the grassed waterway channel |
| 7 |  | `grwaterway_db%grwat_w` | real | none | Width of the grassed waterway channel |
| 8 |  | `grwaterway_db%grwat_l` | real | km | Length of the grassed waterway channel |
| 9 |  | `grwaterway_db%grwat_s` | real | m/m | Slope of the grassed waterway channel |

## Sample

```text
Example record format (fields separated by spaces or tabs):
Name (char40)  grwat_i (int)  grwat_n (real)  grwat_spcon (real)  grwat_d (real)  grwat_w (real)  grwat_l (real)  grwat_s (real)
e.g.
GRASS_WAY_01 1 0.035 0.5 0.3 5.0 0.2 0.01
```

## Read Pattern

```fortran
open (107,file=in_str%grassww_str)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do while (eof == 0)
  read (107,*,iostat=eof) titldum
  imax = imax + 1
end do
allocate (grwaterway_db(0:imax))
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do igrwwop = 1, imax
  read (107,*,iostat=eof) grwaterway_db(igrwwop)
end do
close(107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_str%grassww_str)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) grwaterway_db(igrwwop)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:scen_read_grwway] | open, read, rewind, close | Reads the grassed waterway operations file `grassedww.str` if it exists and is not set to "null". It counts the number of records, allocates the `grwaterway_db` array accordingly, then reads all grassed waterway operation records into this array. If the file does not exist or is "null", it allocates an empty array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and may be omitted or set to "null" to disable grassed waterway operations.
- The reader `scen_read_grwway` uses the `in_str%grassww_str` filename from `input_file_module` and stores the count in `db_mx%grassop_db` from `maximum_data_module`.
- No sample data block was found in the source; the sample format is inferred from the type definition.
