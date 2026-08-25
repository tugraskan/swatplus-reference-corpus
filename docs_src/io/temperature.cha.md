---
kind: io
source_symbols:
- ch_read_temp
title: '`temperature.cha`'
status: filled
source_hash: 2ef5400548d16bfc
version_label: SWAT+ 62.0.0
---

**Primary target:** `w_temp(:)` (array of `type water_temperature_data`)  
**Read by:** [sym:ch_read_temp]

## Bottom Line

The file `temperature.cha` configures channel water temperature parameters for the SWAT+ model.

It is optional and loaded by the `ch_read_temp` reader.

The file defines coefficients and lag times that influence temperature contributions from snowmelt, groundwater, surface runoff, and lateral flow to the channel water temperature state.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `in_cha` variable which contains the file path for `temperature.cha`. |
| [sym:time_module] | Used for time-related constants or types, though no direct variables are referenced in this reader. |
| [sym:input_file_module] | Likely provides input file handling utilities or types; no direct variables referenced in this reader. |
| [sym:maximum_data_module] | Provides `db_mx%w_temp` which stores the count of temperature records read from the file. |
| [sym:channel_data_module] | Defines the `w_temp` array of `type water_temperature_data` where each record from the file is stored. |
| [sym:hydrograph_module] | No direct variables used in this reader but included for hydrograph-related context. |

## File Variables

The `temperature.cha` file consists of multiple records each describing channel water temperature parameters. Each record is read into an element of the `w_temp` array of derived type `water_temperature_data`. The file includes a header and title lines that are skipped during reading.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `w_temp%name` | character(len=13) |  | Name identifier for the channel temperature record |
| 3 |  | `w_temp%sno_mlt` | real | none | Coefficient influencing snowmelt temperature contributions |
| 4 |  | `w_temp%gw` | real | none | Coefficient influencing groundwater temperature contributions |
| 5 |  | `w_temp%sur_lat` | real | none | Coefficient influencing surface and lateral flow temperature contributions |
| 6 |  | `w_temp%sno_lag` | real | days | Average air temperature lag to snowmelt (1-3 days) |
| 7 |  | `w_temp%gw_lag` | real | days | Average air temperature lag to groundwater flow (200-365 days) |
| 8 |  | `w_temp%surf_lag` | real | days | Average air temperature lag to surface runoff (2-5 days) |
| 9 |  | `w_temp%lat_lag` | real | days | Average air temperature lag to lateral flow (5-10 days) |
| 10 |  | `w_temp%lat_lag_coef` | real | none | Lateral flow air lag coefficient |
| 11 |  | `w_temp%surf_lag_coef` | real | none | Surface air lag coefficient (also used for snow) |
| 12 |  | `w_temp%gw_lag_coef` | real | none | Groundwater air lag coefficient |
| 13 |  | `w_temp%hex_coef1` | real | none | Coefficient to calibrate dew point |
| 14 |  | `w_temp%hex_coef2` | real | none | Coefficient to calibrate channel geometry |
| 15 |  | `w_temp%sf_on` | integer | none | Shade factor file activation flag (1 = use file, 0 = use calibration file value) |
| 16 |  | `w_temp%ssff` | real | none | Shade factor file fraction (default 0.5, range 0-1) |

## Sample

```text
Example record format (fields separated by spaces or tabs):
RecordID Name SnoMlt Gw SurLat SnoLag GwLag SurfLag LatLag LatLagCoef SurfLagCoef GwLagCoef HexCoef1 HexCoef2 SfOn Ssff
e.g.
1 ChannelA 1.0 1.0 1.0 2.0 250.0 5.0 10.0 0.75 0.75 0.75 0.75 1.5 0 0.5
```

## Read Pattern

```fortran
open (105,file=in_cha%temp)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) w_temp(ich_temp)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_cha%temp)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) w_temp(ich_temp)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_temp] | backspace, close, open, read, rewind | Reads the `temperature.cha` file, counts the number of records, allocates the `w_temp` array accordingly, and reads each record into `w_temp`. Handles file existence checking and skips header lines. |

## Review Notes

- The file `temperature.cha` is optional and may be set to "null" to skip reading.
- The reader `ch_read_temp` uses `in_cha%temp` from `basin_module` as the file path.
- The reader counts records by reading lines after the header, then allocates `w_temp` accordingly.
- The file format includes title and header lines which are read and skipped before reading data records.
- No sample data records were found in the source; the sample format is inferred from the type declaration.
- No ambiguous or uncertain source references were found.
