---
kind: procedure
symbol: cli_wmeas
title: cli_wmeas
status: filled
source_hash: 5e0931ff9b528a7d
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and skip title or date-like records from
    `wnd.cli` and each wind file before the routine reaches actual data lines.
  header: Temporary character buffer used to read and skip the header line in `wnd.cli` and
    each wind file.
  eof: I/O status flag for every read; the routine uses it to detect normal end-of-file or
    read failure while scanning and loading records.
  i: Loop counter over the wind-file list and over records within each file.
  imax: Count of wind files found in `wnd.cli`; it becomes the size used when allocating `wnd`
    and `wnd_n`.
  iyr: Calendar year read from each wind data record; also used to detect when the loader
    crosses into a new year.
  i_exist: Logical flag from `inquire` that tells the routine whether `wnd.cli` exists before
    attempting to read it.
  istep: Julian day / timestep read from the wind file; it is saved as the start and end day
    markers and used as the first index into `wnd(i)%ts`.
  iyr_prev: Tracks the previous year while reading the daily series so the routine can increment
    `iyrs` when the file advances to a new calendar year.
  iyrs: Current year index into `wnd(i)%ts`; it starts at 1 and is advanced when the reader
    detects a new year in the wind file.
uses:
  input_file_module: '`input_file_module` provides the configured control-file path `in_cli%wnd_cli`
    and optional base directory `in_path_wnd%wnd`; those values decide whether the wind inputs
    exist and how the per-station files are opened.'
  climate_module: '`climate_module` owns the `wnd` array and the `wnd_n` name list that this
    routine allocates and fills, so its derived-type components are the destination for all
    metadata and time-series data read from the wind files.'
  maximum_data_module: '`maximum_data_module` supplies `db_mx%wndfiles`, the shared counter
    used elsewhere to know how many wind-file entries were loaded from `wnd.cli`.'
  time_module: '`time_module` supplies the current simulation year and start day, which the
    loader uses to locate the first record that should be retained and to compute `yrs_start`.'
---

<!-- facts:header -->

Reads the wind-measurement control file `wnd.cli`, then opens each listed wind data file and loads its metadata and daily time series into `climate_module` state.

## Bottom Line

`cli_wmeas` is the wind-data loader for SWAT+ climate inputs. It first checks the `wnd.cli` control file, counts how many wind files are listed, allocates the wind-file registry, and then reads each referenced wind file in turn.

For each wind file, it records the source filename, station metadata, start and end date markers, and the daily values array `wnd(i)%ts`. It also stores the total number of wind files in `db_mx%wndfiles` so later climate-processing code knows how many measured wind stations were loaded.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cli_wmeas` runs during climate-input setup, after `proc_date_time` has already called the other measured-climate loaders and before `cli_wgnread` is invoked. Its results populate the wind-station registry and time-series arrays that later climate routines use for measured wind forcing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check whether the wind control file exists. | The routine resets `eof` and `imax`, then uses `inquire(file=in_cli%wnd_cli, exist=i_exist)` to see whether the configured `wnd.cli` file is present. If the file is missing or the filename is the literal `null`, it skips loading and prepares empty wind storage. |
| 2. Allocate empty wind structures when no wind list is available. | When the control file is absent or disabled, the routine allocates `wnd(0:0)` and `wnd_n(0)` so downstream code still has defined containers even though no measured wind files were loaded. |
| 3. Scan the control file to count wind file entries. | The routine opens `wnd.cli`, skips the leading title and header lines, then reads forward until end-of-file while incrementing `imax` once per remaining record. That pass determines how many wind files must be loaded. |
| 4. Allocate storage for the wind-file registry. | After counting entries, the routine allocates `wnd(0:imax)` for the measured-wind data objects and `wnd_n(imax)` for the filename list. |
| 5. Rewind and read the wind filenames from `wnd.cli`. | The control file is rewound, its title and header are skipped again, and each filename is read into `wnd_n(i)` for the `imax` listed wind files. |
| 6. Rewind again and load each wind file name into the climate records. | The routine rewinds `wnd.cli` a second time, skips the title and header again, and stores each filename into `wnd(i)%filename` so the corresponding station record knows which data file it came from. |
| 7. Open each wind file and read its station metadata. | For each entry, the routine opens the file named in `wnd(i)%filename` using either the raw name or the configured wind path prefix. It skips the file’s title and header, then reads `nbyr`, `tstep`, `lat`, `long`, and `elev` into the `wnd(i)` record. |
| 8. Allocate the daily time-series array for that station. | The routine allocates `wnd(i)%ts(366,wnd(i)%nbyr)` so there is room for up to 366 Julian days across the number of years reported in the file. |
| 9. Read the first record date and store the start markers. | The first year/day pair is read into `iyr` and `istep`, then copied to `wnd(i)%start_yr` and `wnd(i)%start_day`. A `backspace` repositions the file so that record can be read again as part of the stored series. |
| 10. Determine how many years precede the simulation start. | The routine compares the first file year with `time%yrc`. If the file begins after the current simulation year, `wnd(i)%yrs_start` is set to the year offset; otherwise it is set to zero so the loader starts within the current year. |
| 11. Advance to the first record at or after the simulation start day. | The routine reads year/day pairs until it finds a record whose year is at least `time%yrc` and whose day is at least `time%day_start`, then backspaces so that record can be consumed again in the data-loading loop. |
| 12. Load the daily wind values into `wnd(i)%ts` across years. | With `iyr_prev` and `iyrs` initialized, the routine reads year/day/value triplets into `wnd(i)%ts(istep,iyrs)`. When it encounters day 365 or 366, it peeks ahead to the next year/day, backspaces, and increments `iyrs` whenever the calendar year changes. |
| 13. Close each wind file and capture its ending date. | After the series is loaded, unit 108 is closed and the last-read `istep` and `iyr` are stored in `wnd(i)%end_day` and `wnd(i)%end_yr`. |
| 14. Store the total number of wind files and finish. | When all entries have been processed, the control file is closed, `db_mx%wndfiles` is set to `imax`, and the subroutine returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_cli, in_path_wnd` | `in_cli%wnd_cli, in_path_wnd%wnd` |
| [sym:climate_module] | `wnd, wnd_n` | `wnd(i)%filename, wnd(i)%nbyr, wnd(i)%tstep, wnd(i)%lat, wnd(i)%long, wnd(i)%elev, wnd(i)%start_day, wnd(i)%start_yr, wnd(i)%yrs_start, wnd(i)%ts(istep,iyrs), wnd(i)%end_day, wnd(i)%end_yr` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wndfiles` |
| [sym:time_module] | `time` | `time%yrc, time%day_start` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wnd(i)%start_day` | After reading the first year/day record from each wind file, before rewinding to store the series. | `wnd(i)%start_day` records the first Julian day present in that wind file so later code can see where the measured series begins. |
| `wnd(i)%start_yr` | After reading the first year/day record from each wind file, before rewinding to store the series. | `wnd(i)%start_yr` records the first calendar year present in that wind file and identifies the starting year of the measured station record. |
| `wnd(i)%yrs_start` | After comparing the file start year to `time%yrc`. | `wnd(i)%yrs_start` is set to the number of years between the file start year and the current simulation year, or to zero if the file already begins in or before the current simulation year. |
| `wnd(i)%end_day` | After the daily-value loading loop finishes for each wind file. | `wnd(i)%end_day` captures the last Julian day read from the file so the station record has an ending day marker. |
| `wnd(i)%end_yr` | After the daily-value loading loop finishes for each wind file. | `wnd(i)%end_yr` captures the last calendar year read from the file so the station record has an ending year marker. |
| `db_mx%wndfiles` | After all wind-file entries from `wnd.cli` have been processed. | `db_mx%wndfiles` stores the total number of wind files loaded from the control file for use by later climate-data management code. |

## File I/O

<!-- facts:io -->


## Lineage

`cli_wmeas` was introduced in commit df07e3f with the full wind-file loading implementation. Commit 39fabde did not change the algorithm, but it initialized the local scalars `titldum`, `header`, `eof`, `i`, `imax`, `iyr`, `istep`, `iyr_prev`, and `iyrs` at declaration time and added explicit resets for `eof` and `imax` at the top of the routine.

- df07e3f added the new subroutine and its wind-control/wind-data loading workflow, including allocation, file scanning, record loading, and the final `db_mx%wndfiles` assignment.
- 39fabde tightened local-variable initialization by giving the string and integer temporaries default values and preserving the explicit `eof` and `imax` resets used by the routine.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_wmeas' has no extracted documentation comment.
