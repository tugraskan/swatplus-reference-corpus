---
kind: io
source_symbols:
- cli_hmeas
title: '`hmd.cli`'
status: filled
source_hash: 1def5651e09d37b2
version_label: SWAT+ 62.0.0
---

**Primary target:** `hmd(:)` (array of `type climate_measured_data`)  
**Read by:** [sym:cli_hmeas]

## Bottom Line

The file `hmd.cli` contains measured daily precipitation data for multiple raingages, including metadata and time series values.

It is optional; if the file does not exist or is set to "null", no precipitation data is loaded.

The reader subroutine `cli_hmeas` loads this file and populates the array `hmd` of type `climate_measured_data`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_cli%hmd_cli` used to locate the `hmd.cli` file. |
| [sym:climate_module] | provides the derived type `climate_measured_data` and the array `hmd` where the precipitation data and metadata are stored. |
| [sym:maximum_data_module] | provides the variable `db_mx%rhfiles` which is set to the number of precipitation files read. |
| [sym:time_module] | provides the current simulation year `time%yrc` and day start `time%day_start` used to align precipitation data with the simulation time. |

## File Variables

The `hmd.cli` file contains multiple precipitation measurement records, each with metadata and daily precipitation time series. Each record corresponds to one raingage and is read into an element of the `hmd` array of type `climate_measured_data`. The file includes header lines, counts, filenames, and then detailed precipitation data per raingage.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `hmd%filename` | character (len=50) |  | filename of the precipitation data file for this raingage |
| 3 |  | `hmd%lat` | real |  | latitude of raingage |
| 4 |  | `hmd%long` | real |  | longitude of raingage |
| 5 |  | `hmd%elev` | real |  | elevation of raingage |
| 6 |  | `hmd%nbyr` | integer |  | number of years of daily rainfall data available |
| 7 |  | `hmd%tstep` | integer |  | time step of precipitation data (e.g., daily) |
| 8 |  | `hmd%days_gen` | integer |  | number of missing days generated (not read from file) |
| 9 |  | `hmd%yrs_start` | integer |  | number of years of simulation before the precipitation record starts |
| 10 |  | `hmd%start_day` | integer |  | starting Julian day of the precipitation record |
| 11 |  | `hmd%start_yr` | integer |  | starting year of the precipitation record |
| 12 |  | `hmd%end_day` | integer |  | ending Julian day of the precipitation record |
| 13 |  | `hmd%end_yr` | integer |  | ending year of the precipitation record |
| 14 |  | `hmd%mean_mon` | real | same as variable unit | mean monthly measured precipitation value |
| 15 |  | `hmd%max_mon` | real | same as variable unit | maximum monthly measured precipitation value |
| 16 |  | `hmd%min_mon` | real | same as variable unit | minimum monthly measured precipitation value |
| 17 |  | `hmd%ts` | real |  | time series array of daily precipitation values indexed by day and year |
| 18 |  | `hmd%ts2` | real |  | additional time series data (meaning not specified in source) |
| 19 |  | `hmd%tss` | real |  | additional time series data (meaning not specified in source) |

## Sample

```text
Example snippet from `hmd.cli` (not in source, inferred structure):
Line 1: Title line (string)
Line 2: Header line (string)
Line 3+: For each raingage:
  - One line with an integer count (hmd_n(i))
  - One line with the raingage filename (hmd(i)%filename)
  - Contents of the raingage file (opened separately):
    - Title line
    - Header line
    - One line with nbyr, tstep, lat, long, elev
    - Lines with year, day, precipitation values
```

## Read Pattern

```fortran
open (107,file=in_cli%hmd_cli)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat = eof) hmd_n(i)
read (107,*,iostat = eof) hmd(i)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cli%hmd_cli)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) hmd_n(i)` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat = eof) hmd(i)%filename` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_hmeas] | open, read, rewind, close | Reads the `hmd.cli` file to load measured daily precipitation data for multiple raingages. It allocates and fills the array `hmd` of type `climate_measured_data` with metadata and daily precipitation time series. It also opens each raingage's precipitation file to read detailed time series data aligned with the simulation time. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The meaning of fields `ts2` and `tss` in `climate_measured_data` is not explained in the source and remains unclear.
- The sample read format is inferred from source code structure; no explicit example data block is present in source.
