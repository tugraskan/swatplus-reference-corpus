---
kind: procedure
symbol: cli_smeas
title: cli_smeas
status: filled
source_hash: 180bbe4a206caeed
version_label: SWAT+ 62.0.0
locals:
  i: '`i` is the file index used to iterate through the solar-radiation file list and then
    through records within each measured file.'
  titldum: '`titldum` is a throwaway text buffer used to skip title lines and other non-data
    records while scanning and reading the CLI and data files.'
  header: '`header` holds the second header line in each file so the routine can step past
    file metadata before reading file names or data rows.'
  eof: '`eof` captures I/O status from each read so the routine can detect end-of-file or
    read failure and stop scanning safely.'
  imax: '`imax` counts how many solar-radiation files are listed in `slr.cli`; it is then
    used to size `slr` and `slr_n`.'
  iyr: '`iyr` stores the calendar year read from each measured solar-radiation record and
    is used to detect simulation start/end positions and year transitions.'
  i_exist: '`i_exist` holds the file-existence result from `inquire` on `in_cli%slr_cli`,
    deciding whether the routine can load any solar-radiation files.'
  istep: '`istep` stores the Julian day read from each measured record and becomes the recorded
    start/end day for the file.'
  iyr_prev: '`iyr_prev` tracks the previous record''s year so the routine can increment the
    file-year counter when the data file moves into a new calendar year.'
  iyrs: '`iyrs` is the index into the per-file year dimension of `slr(i)%ts`, starting at
    1 and incrementing each time a new calendar year is encountered.'
  solrad: '`solrad` temporarily holds the solar-radiation value while the routine scans forward
    to the first record at or after the simulation start day.'
uses:
  climate_module: The `climate_module` provides the `slr` and `slr_n` shared arrays that this
    routine fills. It also defines the per-file fields being populated (`filename`, `nbyr`,
    `tstep`, `lat`, `long`, `elev`, `start_day`, `start_yr`, `yrs_start`, `ts`, `end_day`,
    `end_yr`), so the module is the destination state for all parsed solar-radiation data.
  input_file_module: The `input_file_module` supplies the configured control filename `in_cli%slr_cli`
    and optional path prefix `in_path_slr%slr`. `cli_smeas` uses those values to find the
    list file and to build the full path for each measured solar-radiation file.
  time_module: The `time_module` supplies the current simulation year and starting Julian
    day (`time%yrc`, `time%day_start`), which determine where each measured series begins
    storing data and whether the file starts before or after the model window.
  maximum_data_module: The `maximum_data_module` provides `db_mx%slrfiles`, the shared count
    of solar-radiation files discovered in `slr.cli`. Other code can use that count to know
    how many `slr` entries were loaded.
---

<!-- facts:header -->

Reads the solar-radiation climate control list and the referenced measured solar-radiation files into shared climate state. It records each file's metadata, simulation start/end positions, and daily radiation time series for later SWAT+ climate processing.

## Bottom Line

`cli_smeas` is the solar-radiation file loader. It first checks `slr.cli`, counts how many measured solar-radiation files are listed, then allocates the shared `slr` and `slr_n` arrays to hold those entries.

After that, it re-reads `slr.cli` to get each solar-radiation filename, opens each referenced file, captures its header metadata (`nbyr`, `tstep`, `lat`, `long`, `elev`), finds the start and end day/year for the simulation window, and stores the daily radiation values into `slr(i)%ts`. The routine finishes by publishing the total file count in `db_mx%slrfiles`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cli_smeas` runs during the climate-file initialization sequence, immediately after `cli_tmeas` and before `cli_hmeas` in `proc_date_time`. It depends on the upstream setup of input paths and simulation time, and its results are used later wherever SWAT+ needs measured solar-radiation file names, start/end dates, or the loaded daily radiation series.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test whether the control file exists | The routine resets `eof` and `imax`, then checks whether `in_cli%slr_cli` exists and is not set to the sentinel string `null`. |
| 2. Allocate empty state when no solar-radiation list is available | If the list file is missing or disabled, it allocates minimal placeholder arrays `slr(0:0)` and `slr_n(0)` and skips loading data. |
| 3. Count the number of listed solar-radiation files | The routine opens `slr.cli`, skips the title and header records, and counts remaining records to determine `imax`, the number of solar-radiation files listed. |
| 4. Allocate the shared storage arrays | Using the count from the scan, it allocates `slr(0:imax)` and `slr_n(imax)` to hold the file metadata and file-name list. |
| 5. Rewind the control file and load the file-name list | The control file is rewound, its title and header are skipped again, and each listed solar-radiation filename is read into `slr_n(i)`. |
| 6. Rewind again and load each file name into climate state | After a second rewind and header skip, the routine reads each file name from `slr.cli` into `slr(i)%filename` for subsequent opening. |
| 7. Open each measured file and read its header metadata | For each file, it opens the measured solar-radiation data file using either the bare name or the configured path prefix, skips its title and header lines, reads `nbyr`, `tstep`, `lat`, `long`, and `elev`, and allocates the per-file time-series array. |
| 8. Capture the first date and store the start position | The routine reads the first year/day pair, saves it as `start_yr` and `start_day`, and uses that position to anchor the loaded series. |
| 9. Determine how many years precede the simulation window | After backspacing one record, it compares the file year to `time%yrc` and sets `yrs_start` to the number of pre-simulation years or to zero when the file already covers the simulation year. |
| 10. Advance to the first usable radiation record | The routine scans year/day/solar-radiation rows until it reaches the first record at or after `time%yrc` and `time%day_start`, then backspaces so that record can be loaded into storage. |
| 11. Load the daily solar-radiation time series | It reads each record into `slr(i)%ts(istep,iyrs)`, watches for year boundaries at day 365 or 366, and advances `iyrs` when the file moves into a new calendar year. |
| 12. Close the data file and record its end position | Once the file is exhausted, it closes unit 108 and stores the last seen day and year in `end_day` and `end_yr`. |
| 13. Finish the control-file loop and publish the file count | After all files are processed, it closes `slr.cli`, writes the discovered file count to `db_mx%slrfiles`, and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `slr, slr_n` | `slr(i)%filename, slr(i)%nbyr, slr(i)%tstep, slr(i)%lat, slr(i)%long, slr(i)%elev, slr(i)%start_day, slr(i)%start_yr, slr(i)%yrs_start, slr(i)%ts(istep,iyrs), slr(i)%end_day, slr(i)%end_yr` |
| [sym:input_file_module] | `in_cli, in_path_slr` | `in_cli%slr_cli, in_path_slr%slr` |
| [sym:time_module] | `time` | `time%yrc, time%day_start` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%slrfiles` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `slr(i)%start_day` | When a measured solar-radiation file is opened and its first year/day pair is read. | `slr(i)%start_day` captures the Julian day of the first record in the file so later climate routines know where that series begins. |
| `slr(i)%start_yr` | When a measured solar-radiation file is opened and its first year/day pair is read. | `slr(i)%start_yr` stores the calendar year of the first record in the file as the file's start year. |
| `slr(i)%yrs_start` | After comparing the file's first year to `time%yrc`. | `slr(i)%yrs_start` becomes the number of years between the file start year and the simulation year, or zero if the file already begins in or before the simulation year. |
| `slr(i)%end_day` | When the end of the measured file is reached in the load loop. | `slr(i)%end_day` stores the last Julian day successfully read from the file, marking the file's end position. |
| `slr(i)%end_yr` | When the end of the measured file is reached in the load loop. | `slr(i)%end_yr` stores the last calendar year successfully read from the file, marking the file's end year. |
| `db_mx%slrfiles` | After all solar-radiation file names in `slr.cli` have been processed. | `db_mx%slrfiles` is set to `imax` so the rest of the model can know how many solar-radiation files were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

`cli_smeas` was introduced in commit df07e3f as a new routine that reads `slr.cli`, opens each referenced solar-radiation file, and loads the measured data. Commit f8bb6ec changed the allocation of `slr(i)%ts` to initialize it with `source = 0.`, commit 39fabde initialized local scalars such as `i`, `eof`, `imax`, `iyr`, `istep`, `iyr_prev`, `iyrs`, `titldum`, `header`, and `solrad`, and commit 2ee1889 only made a trailing whitespace cleanup at the `return` statement.

- df07e3f added the complete `cli_smeas` routine for reading the solar-radiation control list and measured files.
- f8bb6ec changed `slr(i)%ts` allocation to zero-initialize the time-series array with `source = 0.`.
- 39fabde initialized the routine's local variables at declaration instead of leaving them undefined.
- 2ee1889 made no behavioral change; it only adjusted trailing whitespace near `return`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_smeas' has no extracted documentation comment.
- algorithm_steps revised: merged the source into 13 model steps to reflect the actual count/read/load/finalize flow.
- The source uses unlabeled `do`/`exit` control flow around the control-file scan; descriptions follow the actual record-processing behavior rather than the loop syntax.
