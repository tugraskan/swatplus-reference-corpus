---
kind: io
source_symbols:
- cli_wmeas
title: '`wnd.cli`'
status: filled
source_hash: 069346832ed04f5f
version_label: SWAT+ 62.0.0
---

**Primary target:** `wnd(:)` (array of `type climate_measured_data`)  
**Read by:** [sym:cli_wmeas]

## Bottom Line

The file `wnd.cli` contains measured daily wind data records used to configure wind climate inputs in the model.

It is optional; if the file does not exist or is set to "null", no wind data are loaded and an empty array is allocated.

The reader subroutine `cli_wmeas` loads this file and populates the `wnd` array of `type climate_measured_data`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_cli%wnd_cli` used to locate the `wnd.cli` file. |
| [sym:climate_module] | provides the derived type `climate_measured_data` and the `wnd` array where the wind data records are stored. |
| [sym:maximum_data_module] | provides the global data structure `db_mx` where the number of wind files read (`wndfiles`) is stored. |
| [sym:time_module] | provides the global time variables `time%yrc` (current year) and `time%day_start` used to control reading of time series data. |

## File Variables

The `wnd.cli` file contains multiple records of measured daily wind data, each corresponding to a wind station. Each record is read into an element of the `wnd` array of type `climate_measured_data`. The file format includes header lines, counts of records, filenames for individual station data, and time series data for each station.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wnd%filename` | character (len=50) |  | filename of the wind data file for the station |
| 3 |  | `wnd%lat` | real |  | latitude of raingage |
| 4 |  | `wnd%long` | real |  | longitude of raingage |
| 5 |  | `wnd%elev` | real |  | elevation of raingage |
| 6 |  | `wnd%nbyr` | integer |  | number of years of daily rainfall data available |
| 7 |  | `wnd%tstep` | integer |  | time step of precipitation data (must match model time step) |
| 8 |  | `wnd%days_gen` | integer |  | number of missing days generated (filled in) |
| 9 |  | `wnd%yrs_start` | integer |  | number of years of simulation before the record starts |
| 10 |  | `wnd%start_day` | integer |  | starting Julian day of daily precipitation data |
| 11 |  | `wnd%start_yr` | integer |  | starting year of daily precipitation data |
| 12 |  | `wnd%end_day` | integer |  | ending Julian day of daily precipitation data |
| 13 |  | `wnd%end_yr` | integer |  | ending year of daily precipitation data |
| 14 |  | `wnd%mean_mon` | real | same as variable unit | mean monthly measured value |
| 15 |  | `wnd%max_mon` | real | same as variable unit | maximum monthly measured value |
| 16 |  | `wnd%min_mon` | real | same as variable unit | minimum monthly measured value |
| 17 |  | `wnd%ts` | real |  | time series array of measured wind data (daily values) |
| 18 |  | `wnd%ts2` | real |  | secondary time series data (meaning not specified in source) |
| 19 |  | `wnd%tss` | real |  | tertiary time series data (meaning not specified in source) |

## Sample

```text
Example record block from a typical wnd.cli file (not from source, illustrative only):
Line 1: Title line (ignored)
Line 2: Header line (ignored)
Line 3+: Repeated blocks:
  - Number of stations (wnd_n)
  - For each station:
    - filename (e.g. "station1.wnd")
    - station file contains:
      - title line
      - header line
      - nbyr, tstep, lat, long, elev
      - start year and start day
      - daily wind data time series lines
```

## Read Pattern

```fortran
open (107,file=in_cli%wnd_cli)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) wnd_n(i)
read (107,*,iostat = eof) wnd(i)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cli%wnd_cli)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) wnd_n(i)` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) wnd(i)%filename` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_wmeas] | close, open, read, rewind | Reads the `wnd.cli` file if it exists and is not set to "null". It counts the number of wind station records, allocates arrays accordingly, reads filenames for each station, then opens each station's wind data file to read metadata and daily wind time series data into the `wnd` array of `climate_measured_data`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The meaning of `ts2` and `tss` fields in `climate_measured_data` is not specified in the source code and remains unclear.
- The file is optional: if the path is "null" or the file does not exist, empty arrays are allocated and no data is read.
- The reader uses global time variables `time%yrc` and `time%day_start` to control which years and days of data to read from each station file.
