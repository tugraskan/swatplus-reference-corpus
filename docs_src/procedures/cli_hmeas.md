---
kind: procedure
symbol: cli_hmeas
title: cli_hmeas
status: filled
source_hash: 3a77bec0d44fb925
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to skip or probe header/title lines in `hmd.cli`
    and each humidity data file while counting and loading records.
  header: Temporary character buffer for the second header line in `hmd.cli` and the humidity
    data files; it is read and discarded as part of file parsing.
  eof: I/O status flag used on each read to detect end-of-file or read failure and stop scanning/loading
    when a file is exhausted.
  i: Loop counter over humidity file entries in `hmd.cli` and over the allocated `hmd` array.
  imax: Count of humidity file entries discovered in `hmd.cli`; used to size `hmd` and `hmd_n`
    before loading data.
  iyr: Year value read from each humidity time series file; used to track the current record
    year and final year for the series.
  i_exist: Logical flag from `inquire` indicating whether the configured `hmd.cli` file exists
    before attempting to read it.
  istep: Julian day value read from the humidity data files; used to mark the start/end day
    and to index daily values in `hmd(i)%ts`.
  iyr_prev: Tracks the previous year while reading a humidity file so the routine can detect
    when the year changes and advance the `iyrs` index.
  iyrs: Year index into `hmd(i)%ts`; starts at 1 and increments when the input file advances
    to a new year.
uses:
  input_file_module: '`input_file_module` provides the configured control-file name `in_cli%hmd_cli`
    and optional base path `in_path_hmd%hmd`, which determine whether the routine can find
    the humidity file list and how it constructs each humidity data file path.'
  climate_module: '`climate_module` owns the `hmd` array and the `hmd_n` name list that this
    routine allocates and fills; their components store the metadata and daily values read
    from the humidity files.'
  maximum_data_module: '`maximum_data_module` supplies `db_mx%rhfiles`, the shared count of
    humidity files loaded, which is set here so other code knows how many measured humidity
    datasets are available.'
  time_module: '`time_module` provides the simulation calendar start values `time%yrc` and
    `time%day_start`, which the routine uses to decide where the loaded humidity series begins
    relative to the simulation window.'
---

<!-- facts:header -->

Reads the measured daily relative humidity file list and each referenced humidity time series, then stores the file metadata and series into the climate module.

## Bottom Line

`cli_hmeas` is a file-ingestion routine for measured relative humidity inputs. It first checks the configured `hmd.cli` control file, counts how many humidity records are listed, allocates the `hmd` and `hmd_n` arrays, then reads each referenced humidity data file.

For each humidity file, it records the file name, number of years, timestep, location metadata, and the daily values into `climate_module` state. It also computes start/end year-day markers and stores the total file count in `db_mx%rhfiles` so later climate processing can use the loaded humidity datasets.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cli_hmeas` runs in the climate-input setup sequence, called by `proc_date_time` after other measured-climate loaders such as `cli_tmeas` and `cli_smeas`. It prepares the measured relative humidity datasets that later climate and weather routines consume through `climate_module`, along with the file-count summary in `db_mx%rhfiles`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and scan control file availability | Reset counters, check whether `in_cli%hmd_cli` exists, and branch either to a null/empty allocation path or to the file-scanning path for measured humidity inputs. |
| 2. Count humidity file entries in hmd.cli | Open `hmd.cli`, skip the leading title and header lines, then loop through the remaining records to count how many humidity file names are listed in `imax`. |
| 3. Allocate module arrays for the listed files | Allocate `hmd(0:imax)` and `hmd_n(imax)` so the routine can store one climate record and one name entry for each measured humidity file discovered in the control file. |
| 4. Read humidity file names from hmd.cli | Rewind `hmd.cli`, skip the title and header again, and load each file name into `hmd_n(i)` and then `hmd(i)%filename` for the actual humidity file processing pass. |
| 5. Open each humidity data file with optional path prefix | Construct the data-file path from `in_path_hmd%hmd` when present, otherwise use the raw file name, and open unit 108 for the current measured humidity file. |
| 6. Read file metadata and allocate the time-series storage | Skip title/header lines, read the file metadata (`nbyr`, `tstep`, `lat`, `long`, `elev`), and allocate the daily storage array `hmd(i)%ts(366,hmd(i)%nbyr)` initialized to zero. |
| 7. Find the first record at or after the simulation start | Read the first year/day record, store it as the file start date, backspace, and compute `hmd(i)%yrs_start` by comparing the file start year with `time%yrc`. |
| 8. Advance to the simulation start position | Read forward through the humidity file until the year/day meets or exceeds `time%yrc` and `time%day_start`, then backspace so the next pass begins at that starting record. |
| 9. Load daily humidity values into the year/day array | Loop through the file, storing each daily humidity value into `hmd(i)%ts(istep,iyrs)`, and increment `iyrs` when the input year changes after day 365 or 366. |
| 10. Close the file and save end markers | Close unit 108 and record the last day and year read in `hmd(i)%end_day` and `hmd(i)%end_yr` for later use. |
| 11. Finish control-file processing | After all humidity files are processed, close `hmd.cli` and store the total count in `db_mx%rhfiles`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_cli, in_path_hmd` | `in_cli%hmd_cli, in_path_hmd%hmd` |
| [sym:climate_module] | `hmd, hmd_n` | `hmd(i)%filename, hmd(i)%nbyr, hmd(i)%tstep, hmd(i)%lat, hmd(i)%long, hmd(i)%elev, hmd(i)%start_day, hmd(i)%start_yr, hmd(i)%yrs_start, hmd(i)%ts(istep,iyrs), hmd(i)%end_day, hmd(i)%end_yr` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%rhfiles` |
| [sym:time_module] | `time` | `time%yrc, time%day_start` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hmd(i)%start_day` | When the first record in a humidity file is read and before the loop advances to the simulation start position. | Stores the starting Julian day of the humidity file so later code knows the first day represented in the loaded series. |
| `hmd(i)%start_yr` | When the first record in a humidity file is read and before the loop advances to the simulation start position. | Stores the calendar year of the first loaded humidity record. |
| `hmd(i)%yrs_start` | If the file starts after `time%yrc`, set to `iyr - time%yrc`; otherwise set to 0 when the file already covers the simulation year. | Records how many years of simulation elapse before the humidity series begins, which is later useful for aligning the series to the model calendar. |
| `hmd(i)%end_day` | After the load loop finishes reading the final valid humidity record from the file. | Stores the last Julian day represented in the humidity series. |
| `hmd(i)%end_yr` | After the load loop finishes reading the final valid humidity record from the file. | Stores the last calendar year represented in the humidity series. |
| `db_mx%rhfiles` | After all humidity file names have been processed from `hmd.cli`. | Stores the total number of measured humidity files found in the control file so other code can size or iterate over the available humidity datasets. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved lineage commits changed `cli_hmeas`. The initial addition in `df07e3f` introduced the routine and its file-reading logic. `f8bb6ec` changed the `hmd(i)%ts` allocation to initialize the array with `source = 0.`. `39fabde` initialized the local scalars (`titldum`, `header`, `eof`, `i`, `imax`, `iyr`, `istep`, `iyr_prev`, `iyrs`) to default values. `2ee1889` only made a trailing whitespace cleanup at the final `return` line.

- `df07e3f` added the full `cli_hmeas` routine, including control-file scanning, humidity-file loading, time alignment, and population of `hmd`/`hmd_n` plus `db_mx%rhfiles`.
- `f8bb6ec` changed the humidity time-series allocation to `allocate (hmd(i)%ts(366,hmd(i)%nbyr), source = 0.)`, ensuring the series array starts zeroed instead of uninitialized.
- `39fabde` initialized the local working variables at declaration, reducing reliance on later assignments and making the routine's read/error handling deterministic.
- `2ee1889` made no behavioral change; it only adjusted whitespace on the final `return` line.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_hmeas' has no extracted documentation comment.
