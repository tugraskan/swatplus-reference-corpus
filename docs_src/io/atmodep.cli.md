---
kind: io
source_symbols:
- cli_read_atmodep
title: '`atmodep.cli`'
status: filled
source_hash: 141d5b1093f8fa09
version_label: SWAT+ 62.0.0
---

**Primary target:** `atmodep_cont(:)` (array of `type atmospheric_deposition_control`)  
**Read by:** [sym:cli_read_atmodep]

## Bottom Line

The `atmodep.cli` input file configures atmospheric deposition parameters for the SWAT+ model, specifying ammonia and nitrate deposition rates in rainfall and dry deposition.

It is optional; if the file is missing or set to "null", no atmospheric deposition data is loaded.

The file is read by the `cli_read_atmodep` subroutine, which populates the `atmodep_cont` control structure and the `atmodep` array of atmospheric deposition records.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `db_mx` variable used to store the count of atmospheric deposition stations read from the file. |
| [sym:input_file_module] | Supplies the `in_cli` variable that holds the filename for the atmospheric deposition input file (`atmo_cli`). |
| [sym:climate_module] | Defines the derived types `atmospheric_deposition_control` and `atmospheric_deposition` used to store the file data, and the arrays `atmodep_cont` and `atmodep` where data is stored. |
| [sym:time_module] | Provides the `time` variable with simulation start year and month (`yrc_start`, `mo_start`) used to align the time series data read from the file. |
| [sym:maximum_data_module] | No specific types or variables from this module are directly referenced in the reader. |

## File Variables

The file contains a header section followed by a control record of type `atmospheric_deposition_control` that specifies metadata such as number of stations, timestep, and time range. Then, for each station, records of type `atmospheric_deposition` are read, containing ammonia and nitrate deposition values either as annual averages, monthly time series, or yearly time series depending on the timestep.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `atmodep_cont%num_sta` | integer |  | Number of atmospheric deposition stations or records in the file. |
| 3 |  | `atmodep_cont%timestep` | character(len=2) |  | Time step for the deposition data: "aa" for annual average, "mo" for monthly, or "yr" for yearly. |
| 4 |  | `atmodep_cont%ts` | integer |  | Index or counter for the current timestep in the time series data. |
| 5 |  | `atmodep_cont%mo_init` | integer |  | Starting month of the deposition data time series. |
| 6 |  | `atmodep_cont%yr_init` | integer |  | Starting year of the deposition data time series. |
| 7 |  | `atmodep_cont%num` | integer |  | Number of time steps (months or years) in the deposition time series. |
| 8 |  | `atmodep_cont%first` | integer |  | Flag indicating if this is the first timestep (0 = no, 1 = yes). |
| 2 |  | `atmodep%nh4_rf` | real |  | Average annual ammonia concentration in rainfall (mg/l). |
| 3 |  | `atmodep%no3_rf` | real |  | Average annual nitrate concentration in rainfall (mg/l). |
| 4 |  | `atmodep%nh4_dry` | real |  | Average annual ammonia dry deposition (kg/ha/yr). |
| 5 |  | `atmodep%no3_dry` | real |  | Average annual nitrate dry deposition (kg/ha/yr). |
| 6 |  | `atmodep%name` | character(len=50) |  | Name or identifier of the atmospheric deposition station or record. |
| 7 |  | `atmodep%nh4_rfmo` | real |  | Monthly ammonia concentration in rainfall time series (mg/l). |
| 8 |  | `atmodep%no3_rfmo` | real |  | Monthly nitrate concentration in rainfall time series (mg/l). |
| 9 |  | `atmodep%nh4_drymo` | real |  | Monthly ammonia dry deposition time series (kg/ha/yr). |
| 10 |  | `atmodep%no3_drymo` | real |  | Monthly nitrate dry deposition time series (kg/ha/yr). |
| 11 |  | `atmodep%nh4_rfyr` | real |  | Yearly ammonia concentration in rainfall time series (mg/l). |
| 12 |  | `atmodep%no3_rfyr` | real |  | Yearly nitrate concentration in rainfall time series (mg/l). |
| 13 |  | `atmodep%nh4_dryyr` | real |  | Yearly ammonia dry deposition time series (kg/ha/yr). |
| 14 |  | `atmodep%no3_dryyr` | real |  | Yearly nitrate dry deposition time series (kg/ha/yr). |

## Sample

```text
Example header lines:
Title of file line
Header line
3  mo 0 2000 12
StationName1
0.8
0.15
0.05
0.1
0.7 0.75 0.8 0.85 0.9 0.95 1.0 1.05 1.1 1.15 1.2 1.25
0.1 0.12 0.14 0.16 0.18 0.2 0.22 0.24 0.26 0.28 0.3 0.32
0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05
0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1
StationName2
... (similar blocks for other stations)
```

## Read Pattern

```fortran
open (127,file = in_cli%atmo_cli)
read (127,*,iostat=eof) titldum
read (127,*,iostat=eof) header
read (127,*,iostat=eof) atmodep_cont%num_sta, atmodep_cont%timestep, atmodep_cont%mo_init, atmodep_cont%yr_init, atmodep_cont%num
read (127,*,iostat=eof) atmodep(iadep)%name
read (127,*,iostat=eof)   atmodep(iadep)%nh4_rf
read (127,*,iostat=eof)   atmodep(iadep)%no3_rf
read (127,*,iostat=eof)   atmodep(iadep)%nh4_dry
read (127,*,iostat=eof)   atmodep(iadep)%no3_dry
read (127,*,iostat=eof) (atmodep(iadep)%nh4_rfmo(imo), imo = 1,atmodep_cont%num)
read (127,*,iostat=eof) (atmodep(iadep)%no3_rfmo(imo), imo = 1,atmodep_cont%num)
read (127,*,iostat=eof) (atmodep(iadep)%nh4_drymo(imo),imo = 1,atmodep_cont%num)
read (127,*,iostat=eof) (atmodep(iadep)%no3_drymo(imo),imo = 1,atmodep_cont%num)
read (127,*,iostat=eof) (atmodep(iadep)%nh4_rfyr(iyr), iyr = 1,atmodep_cont%num)
read (127,*,iostat=eof) (atmodep(iadep)%no3_rfyr(iyr), iyr = 1,atmodep_cont%num)
read (127,*,iostat=eof) (atmodep(iadep)%nh4_dryyr(iyr),iyr = 1,atmodep_cont%num)
read (127,*,iostat=eof) (atmodep(iadep)%no3_dryyr(iyr),iyr = 1,atmodep_cont%num)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 127 | `open (127,file = in_cli%atmo_cli)` |
| Input | `read` | 127 | `read (127,*,iostat=eof) titldum` |
| Input | `read` | 127 | `read (127,*,iostat=eof) header` |
| Input | `read` | 127 | `read (127,*,iostat=eof) atmodep_cont%num_sta, atmodep_cont%timestep, atmodep_cont%mo_init, atmodep_cont%yr_init, atmodep_cont%num` |
| Input | `read` | 127 | `read (127,*,iostat=eof) atmodep(iadep)%name` |
| Input | `read` | 127 | `read (127,*,iostat=eof)   atmodep(iadep)%nh4_rf` |
| Input | `read` | 127 | `read (127,*,iostat=eof)   atmodep(iadep)%no3_rf` |
| Input | `read` | 127 | `read (127,*,iostat=eof)   atmodep(iadep)%nh4_dry` |
| Input | `read` | 127 | `read (127,*,iostat=eof)   atmodep(iadep)%no3_dry` |
| Input | `read` | 127 | `read (127,*,iostat=eof) atmodep(iadep)%name` |
| Input | `read` | 127 | `read (127,*,iostat=eof) (atmodep(iadep)%nh4_rfmo(imo), imo = 1,atmodep_cont%num)` |
| Input | `read` | 127 | `read (127,*,iostat=eof) (atmodep(iadep)%no3_rfmo(imo), imo = 1,atmodep_cont%num)` |
| Input | `read` | 127 | `read (127,*,iostat=eof) (atmodep(iadep)%nh4_drymo(imo),imo = 1,atmodep_cont%num)` |
| Input | `read` | 127 | `read (127,*,iostat=eof) (atmodep(iadep)%no3_drymo(imo),imo = 1,atmodep_cont%num)` |
| Input | `read` | 127 | `read (127,*,iostat=eof) atmodep(iadep)%name` |
| Input | `read` | 127 | `read (127,*,iostat=eof) (atmodep(iadep)%nh4_rfyr(iyr), iyr = 1,atmodep_cont%num)` |
| Input | `read` | 127 | `read (127,*,iostat=eof) (atmodep(iadep)%no3_rfyr(iyr), iyr = 1,atmodep_cont%num)` |
| Input | `read` | 127 | `read (127,*,iostat=eof) (atmodep(iadep)%nh4_dryyr(iyr),iyr = 1,atmodep_cont%num)` |
| Input | `read` | 127 | `read (127,*,iostat=eof) (atmodep(iadep)%no3_dryyr(iyr),iyr = 1,atmodep_cont%num)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_read_atmodep] | open, read | Reads the atmospheric deposition input file `atmodep.cli` if it exists and is not set to "null". It reads header lines, then reads the control record into `atmodep_cont` to determine the number of stations, timestep type, and time range. It then allocates arrays accordingly and reads each station's atmospheric deposition data into the `atmodep` array, supporting annual average, monthly, or yearly time series data depending on the timestep. The subroutine also aligns the time series with the simulation start time from the `time` module. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or set to "null", no atmospheric deposition data is loaded and arrays are allocated with zero size.
- The reader aligns the deposition time series with the simulation start year and month from the `time` module.
- The meaning of some fields like `ts` and `first` is inferred from code usage but not explicitly documented in source comments.
