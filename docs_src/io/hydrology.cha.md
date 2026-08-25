---
kind: io
source_symbols:
- ch_read_hyd
title: '`hydrology.cha`'
status: filled
source_hash: e81d69cbcff5edb9
version_label: SWAT+ 62.0.0
---

**Primary target:** `ch_hyd(:)` (array of `type channel_hyd_data`)  
**Read by:** [sym:ch_read_hyd]

## Bottom Line

The file `hydrology.cha` configures hydraulic and geometric properties of main channels and reservoirs within subbasins, such as channel width, depth, slope, length, and hydraulic conductivity.

This file is optional; if it does not exist or is set to "null", the model allocates an empty channel hydraulics array.

The reader `ch_read_hyd` is responsible for loading this file and populating the `ch_hyd` array.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the global dimension variable `db_mx%ch_hyd` used to store the number of channel hydraulics records read from the file. |
| [sym:input_file_module] | Supplies the input file path variable `in_cha%hyd` which specifies the location of the `hydrology.cha` file to be read. |
| [sym:maximum_data_module] | Defines the global maximum dimension container `db_mx` whose `ch_hyd` component is set to the number of records read. |
| [sym:channel_data_module] | Defines the derived type `channel_hyd_data` and the array `ch_hyd` into which each record from the file is read and stored. |

## File Variables

The file consists of multiple records each describing hydraulic and geometric properties of a main channel or reservoir within a subbasin. Each record is read into an element of the `ch_hyd` array of type `channel_hyd_data`. The file format includes header lines that are skipped before reading the data records.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ch_hyd%name` | character(len=16) |  | Variables are conditional on res_dat()%hyd = 0 for reservoirs and 1 for HRU; impounding surface areas are hectares for 0 and fraction of HRU for 1; volumes are ha-m for 0 and mm for 1; br1 and br2 are used for 0 and acoef for 0 -- for surface area - volume relationship |
| 3 |  | `ch_hyd%w` | real | m | Average width of main channel |
| 4 |  | `ch_hyd%d` | real | m | Average depth of main channel |
| 5 |  | `ch_hyd%s` | real | m/m | Average slope of main channel |
| 6 |  | `ch_hyd%l` | real | km | Main channel length in subbasin |
| 7 |  | `ch_hyd%n` | real | none | Manning's "n" value for the main channel |
| 8 |  | `ch_hyd%k` | real | mm/hr | Effective hydraulic conductivity of main channel alluvium |
| 9 |  | `ch_hyd%wdr` | real | m/m | Channel width to depth ratio |
| 10 |  | `ch_hyd%alpha_bnk` | real | days | Alpha factor for bank storage recession curve |
| 11 |  | `ch_hyd%side` | real |  | Change in horizontal distance per unit |

## Sample

```text
Example records from a typical hydrology.cha file (e.g. Ames_sub1) would include header lines followed by records with fields matching the `channel_hyd_data` type, such as:
RecordID Name             W     D     S     L     N     K     WDR   Alpha_Bnk Side
1        MainChannel1     2.0   0.5   0.01  0.1   0.05  0.01  6.0   0.03      0.0
```

## Read Pattern

```fortran
open (105,file=in_cha%hyd)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
do loop reading titldum lines to count records
rewind (105)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
loop over ich = 1 to db_mx%ch_hyd:
  read (105,*,iostat=eof) titldum
  backspace (105)
  read (105,*,iostat=eof) ch_hyd(ich)
close (105)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_cha%hyd)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) ch_hyd(ich)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_hyd] | backspace, close, open, read, rewind | Reads the `hydrology.cha` file if it exists and is not set to "null". It counts the number of records, allocates the `ch_hyd` array accordingly, then reads each record into `ch_hyd`. It applies validation and default corrections to certain fields such as `alpha_bnk`, `s`, `n`, `l`, `wdr`, and `side` after reading each record. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as the reader allocates an empty array if the file does not exist or is set to "null".
- The reader performs post-read validation and correction on some fields to ensure physical plausibility.
- Sample record format is inferred from type declaration and typical usage; no explicit example records are present in the source.
