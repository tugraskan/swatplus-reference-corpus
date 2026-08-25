---
kind: io
source_symbols:
- ch_read_init_cs
title: '`initial.cha_cs`'
status: filled
source_hash: 26d55f633dfe92d2
version_label: SWAT+ 62.0.0
---

**Primary target:** `ch_init_cs(:)` (array of `type channel_init_datafiles_cs`)  
**Read by:** [sym:ch_read_init_cs]

## Bottom Line

The file `initial.cha_cs` is an optional input file that configures initial conditions for channel pesticide, pathogen, heavy metals, salt, and constituent data in the SWAT+ model.

It is read by the `ch_read_init_cs` subroutine, which loads the data into the array `ch_init_cs` of derived type `channel_init_datafiles_cs`.

If the file does not exist or is named "null", the array is allocated with zero length, meaning no initial channel constituent data is loaded.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the global variable `db_mx` which stores the count of channel initial data records (`db_mx%ch_init_cs`). |
| [sym:input_file_module] | Used for input file handling utilities and possibly file existence checks. |
| [sym:maximum_data_module] | Likely used for maximum array sizes or constants, though not explicitly referenced in this routine. |
| [sym:channel_data_module] | Defines the derived type `channel_init_datafiles_cs` and the array `ch_init_cs` where the file data is stored. |
| [sym:sd_channel_module] | Imported but no explicit variables or types from this module are directly referenced in the reader. |

## File Variables

The file `initial.cha_cs` consists of records matching the derived type `channel_init_datafiles_cs`. Each record contains character fields pointing to initial input files for various channel constituents such as pesticides, pathogens, heavy metals, salts, and other constituents. The file is read sequentially, skipping header lines, and each record is stored into the corresponding element of the `ch_init_cs` array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ch_init_cs%name` | character(len=16) |  | Name identifier for the channel initial data record. |
| 3 |  | `ch_init_cs%pest` | character(len=16) |  | Points to initial pesticide input file. |
| 4 |  | `ch_init_cs%path` | character(len=16) |  | Points to initial pathogen input file. |
| 5 |  | `ch_init_cs%hmet` | character(len=16) |  | Points to initial heavy metals input file. |
| 6 |  | `ch_init_cs%salt` | character(len=16) |  | Points to initial salt input file. |
| 7 |  | `ch_init_cs%cs` | character(len=16) |  | Points to initial constituent input file. |

## Sample

```text
Example record block from `initial.cha_cs` (fields separated by spaces or fixed width):
Name           Pest           Path           Hmet           Salt           Cs
Channel1       pestfile1      pathfile1      hmetfile1      saltfile1      csfile1
Channel2       pestfile2      pathfile2      hmetfile2      saltfile2      csfile2
```

## Read Pattern

```fortran
open (105,file="initial.cha_cs")
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
read (105,*,iostat=eof) ch_init_cs(ich)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file="initial.cha_cs")` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) ch_init_cs(ich)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_init_cs] | open, read, rewind, close | Reads the optional file `initial.cha_cs` to load initial channel constituent data into the array `ch_init_cs`. It first checks if the file exists; if not, it allocates an empty array. If the file exists, it reads and counts the data records after skipping header lines, allocates the array accordingly, rewinds the file, skips the headers again, and reads each record into `ch_init_cs`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `initial.cha_cs` is optional; if missing or named "null", no initial channel constituent data is loaded.
- The reader uses `db_mx%ch_init_cs` from `basin_module` to store the count of records read.
- No explicit sample record was found in the source; the sample format is inferred from the type fields.
- No additional modules besides those imported are referenced explicitly in the reader.
