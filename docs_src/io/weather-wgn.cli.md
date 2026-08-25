---
kind: io
source_symbols:
- cli_wgnread
title: '`weather-wgn.cli`'
status: filled
source_hash: ebe472ec4e37440d
version_label: SWAT+ 62.0.0
---

**Primary target:** `wgn(:)` (array of `type weather_generator_db`)  
**Read by:** [sym:cli_wgnread]

## Bottom Line

The file `weather-wgn.cli` contains weather generator parameters for multiple weather stations, including monthly temperature, precipitation, and related statistics.

It is optional; if missing or set to "null", default allocations and initializations occur without reading data.

The reader subroutine `cli_wgnread` loads this file and populates the `wgn` array of `type weather_generator_db` with its contents.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file path variable `in_cli%weat_wgn` used to locate the `weather-wgn.cli` file. |
| [sym:time_module] | Provides the `time%step` variable used to dimension the `frad` array allocated during reading. |
| [sym:maximum_data_module] | Provides the `db_mx%wgnsta` variable used to store the count of weather generator stations read from the file. |
| [sym:climate_module] | Defines the `type weather_generator_db` used for the `wgn` array and related weather generator data structures. |

## File Variables

The file `weather-wgn.cli` contains records for weather generator stations. Each record starts with an integer station ID followed by metadata and monthly weather statistics stored in the `wgn` array of `type weather_generator_db`. The file is read sequentially with header lines and monthly data blocks for 12 months per station.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wgn%lat` | real | degrees | latitude of weather station used to compile data |
| 3 |  | `wgn%long` | real | degrees | longitude of weather station |
| 4 |  | `wgn%elev` | real |  | elevation of weather station used to compile weather generator data |
| 5 |  | `wgn%rain_yrs` | real | none | number of years of recorded maximum 0.5h rainfall used to calculate values for rainhhmx(:) |
| 6 |  | `wgn%tmpmx` | real | deg C | avg monthly maximum air temperature |
| 7 |  | `wgn%tmpmn` | real | deg C | avg monthly minimum air temperature |
| 8 |  | `wgn%tmpstdmx` | real | deg C | standard deviation for avg monthly maximum air temperature |
| 9 |  | `wgn%tmpstdmn` | real | deg C | standard deviation for avg monthly minimum air temperature |
| 10 |  | `wgn%pcpmm` | real | mm | amount of precipitation in month |
| 11 |  | `wgn%pcpstd` | real | mm/day | standard deviation for the average daily |
| 12 |  | `wgn%pcpskw` | real | none | skew coefficient for the average daily precipitation |
| 13 |  | `wgn%pr_wd` | real | none | probability of wet day after dry day in month |
| 14 |  | `wgn%pr_ww` | real | none | probability of wet day after wet day in month |
| 15 |  | `wgn%pcpd` | real | days | average number of days of precipitation in the month |
| 16 |  | `wgn%rainhmx` | real | mm | maximum 0.5 hour rainfall in month |
| 17 |  | `wgn%solarav` | real | MJ/m^2/day | average daily solar radiation for the month |
| 18 |  | `wgn%dewpt` | real | deg C | average dew point temperature for the month |
| 19 |  | `wgn%windav` | real | m/s | average wind speed for the month |

## Sample

```text
1 34.05 -118.25 89.0 10.0
Header line for station 1
15.0 5.0 2.0 1.0 50.0 10.0 0.5 0.3 0.4 12.0 5.0 20.0 10.0 3.0
16.0 6.0 2.1 1.1 55.0 11.0 0.6 0.4 0.5 13.0 5.5 21.0 11.0 3.5
... (10 more monthly lines) ...
```

## Read Pattern

```fortran
open (114,file=in_cli%weat_wgn)
read (114,*,iostat=eof) titldum
read (114,*,iostat=eof) titldum
read (114,*,iostat=eof) header
rewind (114)
read (114,*,iostat=eof) wgn_n(iwgn), wgn(iwgn)%lat, wgn(iwgn)%long, wgn(iwgn)%elev, wgn(iwgn)%rain_yrs
read (114,*,iostat=eof) wgn(iwgn)%tmpmx(mo), wgn(iwgn)%tmpmn(mo), wgn(iwgn)%tmpstdmx(mo), wgn(iwgn)%tmpstdmn(mo), wgn(iwgn)%pcpmm(mo), wgn(iwgn)%pcpstd(mo), wgn(iwgn)%pcpskw(mo), wgn(iwgn)%pr_wd(mo), wgn(iwgn)%pr_ww(mo), wgn(iwgn)%pcpd(mo), wgn(iwgn)%rainhmx(mo), wgn(iwgn)%solarav(mo), wgn(iwgn)%dewpt(mo), wgn(iwgn)%windav(mo)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 114 | `open (114,file=in_cli%weat_wgn)` |
| Input | `read` | 114 | `read (114,*,iostat=eof) titldum` |
| Input | `read` | 114 | `read (114,*,iostat=eof) titldum` |
| Input | `read` | 114 | `read (114,*,iostat=eof) header` |
| Input | `read` | 114 | `read (114,*,iostat=eof) titldum` |
| File control | `rewind` | 114 | `rewind (114)` |
| Input | `read` | 114 | `read (114,*,iostat=eof) titldum` |
| Input | `read` | 114 | `read (114,*,iostat=eof) wgn_n(iwgn), wgn(iwgn)%lat, wgn(iwgn)%long, wgn(iwgn)%elev, wgn(iwgn)%rain_yrs` |
| Input | `read` | 114 | `read (114,*,iostat=eof) header` |
| Input | `read` | 114 | `read (114,*,iostat=eof) wgn(iwgn)%tmpmx(mo), wgn(iwgn)%tmpmn(mo), wgn(iwgn)%tmpstdmx(mo), wgn(iwgn)%tmpstdmn(mo), wgn(iwgn)%pcpmm(mo), wgn(iwgn)%pcpstd(mo), wgn(iwgn)%pcpskw(mo), wgn(iwgn)%pr_wd(mo), wgn(iwgn)%pr_ww(mo), wgn(iwgn)%pcpd(mo), wgn(iwgn)%rainhmx(mo), wgn(iwgn)%solarav(mo), wgn(iwgn)%dewpt(mo), wgn(iwgn)%windav(mo)` |
| File control | `close` | 114 | `close (114)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_wgnread] | close, open, read, rewind | Reads the weather generator parameter file `weather-wgn.cli` specified by `in_cli%weat_wgn`. It first checks if the file exists and is not set to "null". If the file is missing or null, it allocates default empty arrays and calls `gcycl` to initialize default weather cycles. Otherwise, it opens the file, counts the number of weather stations by reading header and monthly data blocks, allocates arrays accordingly, rewinds the file, and reads each station's metadata and monthly weather statistics into the `wgn` array. After reading each station, it calls `cli_initwgn` to initialize weather generator parameters for that station. Finally, it closes the file. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample read format is a constructed example based on the read pattern and variable types; no explicit example record was found in the source.
- The reader subroutine `cli_wgnread` conditionally reads the file if it exists and is not "null"; otherwise, it allocates default empty arrays and initializes default weather cycles.
- The file format includes repeated blocks per station: a station ID and metadata line, a header line, then 12 lines of monthly weather statistics.
