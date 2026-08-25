---
kind: io
source_symbols:
- cli_tmeas
title: '`tmp.cli`'
status: filled
source_hash: fdc23af71db4b9b3
version_label: SWAT+ 62.0.0
---

**Primary target:** `tmp(:)` (array of `type climate_measured_data`)  
**Read by:** [sym:cli_tmeas]

## Bottom Line

The file `tmp.cli` contains measured daily temperature data for multiple raingages, including metadata and time series of temperature values.

It is optional and only read if the filename is not "null" and the file exists.

The reader subroutine `cli_tmeas` loads this file, allocating and populating an array `tmp` of `type climate_measured_data` with the data.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_cli%tmp_cli` used to locate the `tmp.cli` file. |
| [sym:climate_module] | provides the derived type `climate_measured_data` and the array `tmp` where the file data is stored. |
| [sym:maximum_data_module] | provides the variable `db_mx%tmpfiles` which is set to the number of records read from `tmp.cli`. |
| [sym:time_module] | provides the current simulation year `time%yrc` and start day `time%day_start` used to filter and align the temperature time series data. |

## File Variables

The `tmp.cli` file contains measured daily temperature data for multiple raingages, with each record describing metadata and daily temperature time series for one raingage. The file is read into an array of `type climate_measured_data` where each element corresponds to one raingage's data.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `tmp%filename` | character (len=50) |  | Name of the file containing the detailed temperature time series for this raingage |
| 3 |  | `tmp%lat` | real |  | Latitude of the raingage location |
| 4 |  | `tmp%long` | real |  | Longitude of the raingage location |
| 5 |  | `tmp%elev` | real |  | Elevation of the raingage location |
| 6 |  | `tmp%nbyr` | integer |  | Number of years of daily rainfall data available |
| 7 |  | `tmp%tstep` | integer |  | Timestep of precipitation data (e.g., daily) |
| 8 |  | `tmp%days_gen` | integer |  | Number of missing days for which data was generated |
| 9 |  | `tmp%yrs_start` | integer |  | Number of years of simulation before the record starts |
| 10 |  | `tmp%start_day` | integer |  | Julian day when daily precipitation data starts |
| 11 |  | `tmp%start_yr` | integer |  | Year when daily precipitation data starts |
| 12 |  | `tmp%end_day` | integer |  | Julian day when daily precipitation data ends |
| 13 |  | `tmp%end_yr` | integer |  | Year when daily precipitation data ends |
| 14 |  | `tmp%mean_mon` | real | same as variable unit | Mean monthly measured temperature value |
| 15 |  | `tmp%max_mon` | real | same as variable unit | Maximum monthly measured temperature value |
| 16 |  | `tmp%min_mon` | real | same as variable unit | Minimum monthly measured temperature value |
| 17 |  | `tmp%ts` | real |  | Array of daily temperature values (first type) indexed by day and year |
| 18 |  | `tmp%ts2` | real |  | Array of daily temperature values (second type) indexed by day and year |
| 19 |  | `tmp%tss` | real |  | Unused or undefined in source; no evidence for meaning |

## Sample

```text
Example record block (from `tmp.cli`):
Line 1: Title line (ignored)
Line 2: Header line (ignored)
Line 3+: For each raingage:
  - One line with an integer (tmp_n) count
  - One line with the raingage filename (tmp(i)%filename)
  - File named by tmp(i)%filename contains:
    * Title line
    * Header line
    * One line with nbyr, tstep, lat, long, elev
    * One line with start year and start julian day
    * Multiple lines with year, day, ts, ts2 daily values
```

## Read Pattern

```fortran
open (107,file=in_cli%tmp_cli)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat = eof) tmp_n(i)
read (107,*,iostat = eof) tmp(i)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cli%tmp_cli)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) tmp_n(i)` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) tmp(i)%filename` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_tmeas] | close, open, read, rewind | Reads the `tmp.cli` file if it exists and is not "null", allocating and populating the array `tmp` of `climate_measured_data` with metadata and daily temperature time series for each raingage. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The fields `ts`, `ts2`, and `tss` are arrays of daily temperature values; `tss` is declared but not assigned in the reader, so its meaning is uncertain.
- The reader filters temperature data to start from the current simulation year and day, using `time%yrc` and `time%day_start`.
- The file `tmp.cli` is a master index listing raingage filenames, each of which contains detailed temperature time series data.
