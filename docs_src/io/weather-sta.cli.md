---
kind: io
source_symbols:
- cli_staread
title: '`weather-sta.cli`'
status: filled
source_hash: 64446c53d6c138e5
version_label: SWAT+ 62.0.0
---

**Primary target:** `wst(:)` (array of `type weather_station`)  
**Read by:** [sym:cli_staread]

## Bottom Line

The `weather-sta.cli` file configures weather station metadata and associated weather code mappings for the model.

It is optional; if the file does not exist or is set to "null", empty arrays are allocated.

The reader `cli_staread` loads this file and populates the `wst` array of `type weather_station` with station names, weather codes, and related climate adjustments.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file path variable `in_cli%weat_sta` used to locate the weather station file. |
| [sym:maximum_data_module] | Supplies global counters and arrays such as `db_mx%wst`, `db_mx%wgnsta`, `db_mx%pcpfiles`, and others used for indexing and searching station codes. |
| [sym:climate_module] | Defines the `type weather_station` and related types (`weather_codes_station_char`, `weather_codes_station`, `weather_daily`) used to store the weather station data read from the file. |
| [sym:time_module] | Provides the `time%step` variable used to allocate time series arrays within each weather station record. |
| [sym:hydrograph_module] | Used indirectly for weather station related hydrologic data structures, though specific variables used are not detailed in the source. |

## File Variables

The file consists of records representing weather stations, each mapped to a `type weather_station` instance in Fortran. Each record includes station name, latitude, weather code character and numeric mappings, daily weather data arrays, and monthly climate adjustment parameters.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wst%name` | character(len=50) |  | Station name identifier |
| 3 |  | `wst%lat` | real | degrees | Latitude coordinate of the station |
| 4 |  | `wst%wco_c` | type (weather_codes_station_char) |  | Character-based weather codes for the station |
| 5 |  | `wst%wco` | type (weather_codes_station) |  | Numeric weather codes resolved from character codes |
| 6 |  | `wst%weat` | type (weather_daily) |  | Daily weather data time series for the station |
| 7 |  | `wst%precip_aa` | real | mm | Average annual precipitation at the station |
| 8 |  | `wst%pet_aa` | real | mm | Average annual potential evapotranspiration |
| 9 |  | `wst%pcp_ts` | integer | 1/day | Precipitation time steps per day (0 or 1 means daily) |
| 10 |  | `wst%rfinc` | real | deg C | Monthly precipitation adjustment factor |
| 11 |  | `wst%tmpinc` | real | deg C | Monthly temperature adjustment factor |
| 12 |  | `wst%radinc` | real | MJ/m^2 | Monthly solar radiation adjustment |
| 13 |  | `wst%huminc` | real | none | Monthly humidity adjustment |
| 14 |  | `wst%tlag` | real | deg C | Daily average temperature used for channel temperature lag |
| 15 |  | `wst%airlag_temp` | real | deg C | Average temperature from air lag days ago |
| 16 |  | `wst%tlag_mne` | integer |  | Next element (day) index for air temperature linked list |

## Sample

```text
Example record lines are not present in the source; typical lines read station name and weather code characters, e.g.:
"Farmer Branch IL" "wco_c data"
```

## Read Pattern

```fortran
open (107,file=in_cli%weat_sta)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) wst(i)%name, wst(i)%wco_c
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cli%weat_sta)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) wst(i)%name, wst(i)%wco_c` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_staread] | backspace, close, open, read, rewind | Reads the `weather-sta.cli` file to load weather station metadata into the `wst` array. It checks for file existence, counts records, allocates arrays, initializes daily weather time series, and resolves weather code indices by searching global code name arrays. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The source code does not provide example record lines; the sample read format is inferred from read statements.
- The file is optional; if missing or set to "null", empty arrays are allocated.
- The reader performs multiple reads of header lines and rewinds before reading station records.
- Weather code character fields are read from the file and then resolved to numeric codes by searching global name arrays.
