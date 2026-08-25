---
kind: io
source_symbols:
- cli_smeas
title: '`slr.cli`'
status: filled
source_hash: 2b0756a69d8f3955
version_label: SWAT+ 62.0.0
---

**Primary target:** `slr(:)` (array of `type climate_measured_data`)  
**Read by:** [sym:cli_smeas]

## Bottom Line

The file `slr.cli` contains measured daily solar radiation data for multiple stations or locations.

It is optional; if the file does not exist or is set to "null", the model allocates empty arrays and proceeds without measured solar radiation data.

The reader subroutine `cli_smeas` loads this file and populates the `slr` array of `climate_measured_data` records with metadata and time series of solar radiation.

| Module | Role for this file |
| --- | --- |
| [sym:climate_module] | Provides the derived type `climate_measured_data` which defines the structure of each solar radiation record stored in `slr`. |
| [sym:input_file_module] | Supplies the `in_cli` variable which contains the filename path for `slr.cli` and possibly `in_path_slr` for relative paths. |
| [sym:time_module] | Provides the `time` variable used to compare and align the solar radiation data years and days with the simulation time step and start day. |
| [sym:maximum_data_module] | Provides the `db_mx` variable where the number of solar radiation files read (`slrfiles`) is stored. |

## File Variables

The `slr.cli` file contains multiple records of measured daily solar radiation data, each identified by a filename and associated metadata such as location coordinates, elevation, number of years, and time step. Each record includes a time series array of solar radiation values indexed by day and year. The file is read in multiple passes to first count records, then read metadata counts, and finally read detailed data for each record into the `slr` array of `climate_measured_data` type.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `slr%filename` | character (len=50) |  | Name of the file containing the measured solar radiation data for this record. |
| 3 |  | `slr%lat` | real |  | Latitude coordinate of the solar radiation measurement station. |
| 4 |  | `slr%long` | real |  | Longitude coordinate of the solar radiation measurement station. |
| 5 |  | `slr%elev` | real |  | Elevation of the solar radiation measurement station. |
| 6 |  | `slr%nbyr` | integer |  | Number of years of daily solar radiation data available in the file. |
| 7 |  | `slr%tstep` | integer |  | Time step of the solar radiation data, must match the simulation time step. |
| 8 |  | `slr%days_gen` | integer |  | Number of missing days for which data were generated (not read from file). |
| 9 |  | `slr%yrs_start` | integer |  | Number of years of simulation before the solar radiation record starts, used for alignment. |
| 10 |  | `slr%start_day` | integer |  | Julian day when the daily solar radiation data starts. |
| 11 |  | `slr%start_yr` | integer |  | Year when the daily solar radiation data starts. |
| 12 |  | `slr%end_day` | integer |  | Julian day when the daily solar radiation data ends. |
| 13 |  | `slr%end_yr` | integer |  | Year when the daily solar radiation data ends. |
| 14 |  | `slr%mean_mon` | real | same as variable unit | Mean monthly measured solar radiation value. |
| 15 |  | `slr%max_mon` | real | same as variable unit | Maximum monthly measured solar radiation value. |
| 16 |  | `slr%min_mon` | real | same as variable unit | Minimum monthly measured solar radiation value. |
| 17 |  | `slr%ts` | real |  | Time series array of daily solar radiation values indexed by day and year. |
| 18 |  | `slr%ts2` | real |  | Additional time series data related to solar radiation (usage unclear from source). |
| 19 |  | `slr%tss` | real |  | Additional time series data related to solar radiation (usage unclear from source). |

## Sample

```text
Example snippet of slr.cli file format (not from source, illustrative only):
Title line
Header line
Record count line (integer)
Filename1
Filename2
...
Each filename file contains:
Title line
Header line
nbyr tstep lat long elev
start_year start_day
Year Day SolarRadiationValue
...
```

## Read Pattern

```fortran
open (107,file=in_cli%slr_cli)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*, iostat=eof) slr_n(i)
read (107,*,iostat = eof) slr(i)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cli%slr_cli)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*, iostat=eof) slr_n(i)` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) slr(i)%filename` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_smeas] | close, open, read, rewind | Reads the `slr.cli` file and loads measured daily solar radiation data into the `slr` array of `climate_measured_data`. It first checks if the file exists and is not set to "null". If present, it counts the number of records, allocates arrays, then reads metadata and filenames. For each filename, it opens the corresponding solar radiation data file, reads metadata (years, timestep, location), allocates the time series array, and reads daily solar radiation values aligned with the simulation time. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The meaning of `ts2` and `tss` fields in `climate_measured_data` is not clear from the source code and may require further investigation.
- The sample read format is illustrative only; no actual example data lines were found in the source.
