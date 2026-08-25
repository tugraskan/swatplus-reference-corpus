---
kind: io
source_symbols:
- ch_read
title: '`channel.cha`'
status: filled
source_hash: fc46825757492bcf
version_label: SWAT+ 62.0.0
---

**Primary target:** `ch_dat_c(:)` (array of `type channel_data_char_input`)  
**Read by:** [sym:ch_read]

## Bottom Line

The file `channel.cha` configures channel characteristics for the SWAT+ model, specifying channel names and linking to initial conditions, hydrology, sediment, and nutrient input files.

It is optional; if the file does not exist or is set to "null", empty channel data arrays are allocated.

The primary reader for this file is the `ch_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `db_mx` variable which stores maximum counts for channel data arrays used to allocate and index channel data. |
| [sym:input_file_module] | Provides the `in_cha` variable which contains the file path for `channel.cha` used to open and read the file. |
| [sym:channel_data_module] | Defines the `ch_dat_c` array of `type channel_data_char_input` where the raw character data from the file is stored, and the `ch_dat` array where resolved integer indices are stored. |
| [sym:maximum_data_module] | No direct evidence of usage in `ch_read` for reading or storing this file. |
| [sym:hydrograph_module] | No direct evidence of usage in `ch_read` for reading or storing this file. |
| [sym:pesticide_data_module] | No direct evidence of usage in `ch_read` for reading or storing this file. |

## File Variables

The `channel.cha` file consists of records describing channel characteristics, each record containing a channel name and references to initial conditions, hydrology, sediment, and nutrient input datasets. Each record is read into an element of the `ch_dat_c` array of type `channel_data_char_input`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ch_dat_c%name` | character(len=16) |  | Channel name identifier |
| 3 |  | `ch_dat_c%init` | character(len=16) |  | Points to initial_cha |
| 4 |  | `ch_dat_c%hyd` | character(len=16) |  | Points to hydrology.res for hydrology inputs |
| 5 |  | `ch_dat_c%sed` | character(len=16) |  | Sediment inputs - points to sediment.res |
| 6 |  | `ch_dat_c%nut` | character(len=16) |  | Nutrient inputs - points to nutrient.res |

## Sample

```text
1  default  initial_cha  hydrology.res  sediment.res  nutrient.res
```

## Read Pattern

```fortran
open (105,file=in_cha%dat)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
read (105,*,iostat=eof) i
rewind (105)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
read (105,*,iostat=eof) i
backspace (105)
read (105,*,iostat=eof) k, ch_dat_c(ichi)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_cha%dat)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) i` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) i` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) k, ch_dat_c(ichi)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read] | backspace, close, open, read, rewind | Reads the `channel.cha` file, loading channel characteristic records into the `ch_dat_c` array. It first checks if the file exists and is not set to "null". If present, it reads the maximum channel index, allocates arrays accordingly, then reads each record, storing character data and resolving references to initial conditions, hydrology, sediment, and nutrient input datasets by matching names to indices in corresponding arrays. It logs warnings if referenced names are not found. |

## Review Notes

- The `channel.cha` file is optional; if missing or set to "null", empty channel data arrays are allocated.
- The reader `ch_read` resolves character references in `channel.cha` to indices in initial, hydrology, sediment, and nutrient input arrays, linking channel data to these inputs.
- No sample data block was found in the source; the sample read format is inferred from the read pattern and type definition.
- No direct usage of `maximum_data_module`, `hydrograph_module`, or `pesticide_data_module` variables was found in the reader despite being used modules.
