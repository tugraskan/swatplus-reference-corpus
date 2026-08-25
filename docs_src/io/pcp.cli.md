---
kind: io
source_symbols:
- cli_pmeas
title: '`pcp.cli`'
status: filled
source_hash: 99febd94a360240b
version_label: SWAT+ 62.0.0
---

**Primary target:** `pcp(:)` (array of `type climate_measured_data`)  
**Read by:** [sym:cli_pmeas]

## Bottom Line

The file `pcp.cli` contains metadata and filenames for measured daily precipitation data used by the model.

It is optional and only read if the file exists and is not set to "null" in the configuration.

The reader subroutine `cli_pmeas` loads this file, allocating and filling the `pcp` array with precipitation station metadata and then reads each referenced precipitation data file.

| Module | Role for this file |
| --- | --- |
| [sym:climate_module] | Provides the derived type `climate_measured_data` used for the `pcp` array to store precipitation station data and time series. |
| [sym:maximum_data_module] | Provides the variable `pcp_n` which stores the number of precipitation stations read from the file. |
| [sym:basin_module] | Provides the variable `db_mx` where the number of precipitation files (`pcpfiles`) is stored after reading. |
| [sym:input_file_module] | Provides the input configuration variable `in_cli` which contains the filename for `pcp.cli`. |
| [sym:time_module] | Provides the `time` module variables such as `time%step`, `time%yrc`, and `time%day_start` used for time indexing and allocation of precipitation time series arrays. |

## File Variables

The `pcp.cli` file contains a list of precipitation station records. Each record includes a station identifier number followed by the filename of the precipitation data file for that station. The reader loads these filenames and then reads each referenced precipitation data file to populate the precipitation data arrays.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pcp%filename` | character (len=50) |  | Name of the precipitation data file for the station |
| 3 |  | `pcp%lat` | real |  | Latitude of the raingage station |
| 4 |  | `pcp%long` | real |  | Longitude of the raingage station |
| 5 |  | `pcp%elev` | real |  | Elevation of the raingage station |
| 6 |  | `pcp%nbyr` | integer |  | Number of years of daily rainfall data available |
| 7 |  | `pcp%tstep` | integer |  | Time step of precipitation data (e.g., daily or sub-daily) |
| 8 |  | `pcp%days_gen` | integer |  | Number of missing days for which data were generated |
| 9 |  | `pcp%yrs_start` | integer |  | Number of years of simulation before the precipitation record starts |
| 10 |  | `pcp%start_day` | integer |  | Julian day when daily precipitation data starts |
| 11 |  | `pcp%start_yr` | integer |  | Year when daily precipitation data starts |
| 12 |  | `pcp%end_day` | integer |  | Julian day when daily precipitation data ends |
| 13 |  | `pcp%end_yr` | integer |  | Year when daily precipitation data ends |
| 14 |  | `pcp%mean_mon` | real | same as variable unit | Mean monthly measured precipitation value |
| 15 |  | `pcp%max_mon` | real | same as variable unit | Maximum monthly measured precipitation value |
| 16 |  | `pcp%min_mon` | real | same as variable unit | Minimum monthly measured precipitation value |
| 17 |  | `pcp%ts` | real |  | Array storing daily precipitation time series if no sub-daily time step |
| 18 |  | `pcp%ts2` | real |  | Additional time series array (purpose not detailed in source) |
| 19 |  | `pcp%tss` | real |  | Array storing sub-daily precipitation time series if time step > 0 |

## Sample

```text
1
station1.dat
2
station2.dat
3
station3.dat
```

## Read Pattern

```fortran
open (107,file=in_cli%pcp_cli)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat = eof) titldum
rewind (107)
read (107,*,iostat = eof) pcp_n(i)
read (107,*,iostat = eof) pcp(i)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cli%pcp_cli)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) pcp_n(i)` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) pcp(i)%filename` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_pmeas] | open, read, rewind, close | Reads the `pcp.cli` file to determine the number of precipitation stations and their data filenames, allocates arrays accordingly, and then reads each referenced precipitation data file to load station metadata and precipitation time series into the `pcp` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The meaning of `pcp%ts2` is not clear from the source and requires further investigation.
- The sample read format is inferred as pairs of station number and filename lines, but no explicit example data block was found in the source.
