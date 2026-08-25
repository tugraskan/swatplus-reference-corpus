---
kind: procedure
symbol: cli_tmeas
title: cli_tmeas
status: filled
source_hash: 6555f4e5420f1ad2
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to read and discard title or data lines while scanning `tmp.cli`
    and each temperature file.
  header: Scratch string used to read and discard the header line in `tmp.cli` and in each
    referenced temperature file before the numeric records are processed.
  eof: I/O status flag returned by `read(..., iostat=eof)`; negative values stop scanning
    or signal end-of-file while building counts and loading data.
  imax: Counts how many measured-temperature files are listed in `tmp.cli`, then becomes the
    allocation size for `tmp` and `tmp_n`.
  i: Loop counter over the temperature-file list and over the allocated `tmp` records.
  iyr: Current year read from a temperature record; used to detect the start year, end year,
    and year boundaries while loading data.
  i_exist: Logical flag from `inquire` that tells whether the configured `tmp.cli` file exists
    before any reading starts.
  istep: Current Julian day-of-year read from a temperature record; used to capture start/end
    day and to index daily temperatures.
  mtmp: Initialized to zero but not used by the shown source logic.
  tempx: Temporary real used when peeking ahead in the file to find the first record at or
    after the simulation start date.
  tempn: Temporary real used with `tempx` during the same peek-ahead read; it is not stored,
    only used to advance to the correct record.
  iyr_prev: Remembers the prior year so the routine can detect when the file advances into
    a new calendar year and increment `iyrs`.
  iyrs: Counts the current year index within the temperature file while filling the 2-D daily
    arrays `ts` and `ts2`.
  num_tot: Per-month counter of how many daily records contributed to each monthly max/min
    average.
  day_mo: Receives the day-of-month from `xmon`; used only as an output scratch value from
    the Julian-day conversion.
  mo: Receives the month number from `xmon` so the routine can accumulate monthly max/min
    sums into the correct month bucket.
uses:
  input_file_module: This module provides the configured `tmp.cli` file name and optional
    temperature-file path prefix, so `cli_tmeas` can locate the file list and each referenced
    measured-temperature file.
  climate_module: 'This module holds the shared temperature-file database that `cli_tmeas`
    fills: file names, station metadata, daily series arrays, and start/end coverage fields
    used by later climate routines.'
  maximum_data_module: This module stores the global count of temperature files; `cli_tmeas`
    updates `db_mx%tmpfiles` so the rest of the model knows how many measured-temperature
    datasets were loaded.
  time_module: The current simulation year and starting Julian day determine where reading
    begins inside each measured-temperature file, so this module controls which records are
    accepted and how start-year offsets are computed.
---

<!-- facts:header -->

`cli_tmeas` reads the measured-temperature climate list file `tmp.cli`, then opens each referenced temperature file and loads daily maximum/minimum temperature series plus record timing metadata. It also computes per-file start/end dates, yearly coverage, and monthly temperature averages for later model use.

## Bottom Line

`cli_tmeas` is the temperature-file reader for SWAT+ climate inputs. It first checks whether `tmp.cli` exists and is enabled, counts how many measured-temperature files are listed, and allocates the `climate_module::tmp` and `tmp_n` arrays to hold those files and their names.

For each listed temperature file, it opens the file, reads the station metadata and daily records, stores the daily max/min series into `tmp(i)%ts` and `tmp(i)%ts2`, tracks start and end day/year, and accumulates monthly max/min means. The resulting counts and arrays are published through `tmp` and `db_mx%tmpfiles` for downstream date/time and climate processing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_date_time` calls `cli_tmeas` after the other climate list readers and after `DATE_AND_TIME` has updated the shared time state. `cli_tmeas` must run before later climate initialization uses `tmp`, `tmp_n`, and `db_mx%tmpfiles` to know which temperature stations exist and how their daily series are bounded.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check for the file list | The routine zeros its counters, checks whether `in_cli%tmp_cli` exists, and handles the disabled/missing case by allocating empty `tmp` and `tmp_n` arrays. |
| 2. Count entries in tmp.cli | It opens `tmp.cli`, skips the title and header lines, then counts one file-name record per loop iteration to determine `imax` before allocating the climate arrays. |
| 3. Reload tmp.cli and read file names | After rewinding, it rereads the title and header, then loads each temperature-file name into `tmp(i)%filename`. |
| 4. Open each temperature file and read station metadata | For each file, it applies the optional temp-path prefix, opens the measured-temperature file, discards its title/header, and reads the file metadata into `tmp(i)` before allocating the daily temperature arrays. |
| 5. Capture the file start date | It reads the first date record, stores the starting Julian day and year into `tmp(i)%start_day` and `tmp(i)%start_yr`, and backspaces so that record can be reread in the main loop. |
| 6. Find the first record at or after the simulation start | Using `time%yrc` and `time%day_start`, it determines whether the file starts after the simulation begins and advances until the first usable record is found, then backspaces to preserve it. |
| 7. Set year indexing and leap-year day tables | It initializes the year counter and selects `ndays_leap` or `ndays_noleap` based on the current year so later processing can use the correct annual day boundaries. |
| 8. Load daily max/min temperatures | The main read loop stores each day's maximum and minimum temperature into `tmp(i)%ts` and `tmp(i)%ts2`, while also accumulating monthly sums and record counts. |
| 9. Detect year boundaries while reading | When the end of a year is reached, it peeks at the next record, backspaces, and increments `iyrs` when the year changes so the next daily data land in the correct year slice. |
| 10. Close file and compute summaries | After each temperature file is finished, it closes the file, stores the ending date, and converts monthly max/min sums into averages by dividing by the month counts. |
| 11. Finish list processing | Once all files are processed, it closes `tmp.cli`, stores the total file count in `db_mx%tmpfiles`, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_cli, in_path_tmp` | `in_cli%tmp_cli, in_path_tmp%tmp` |
| [sym:climate_module] | `tmp, tmp_n` | `tmp(i)%filename, tmp(i)%nbyr, tmp(i)%tstep, tmp(i)%lat, tmp(i)%long, tmp(i)%elev, tmp(i)%start_day, tmp(i)%start_yr, tmp(i)%yrs_start, tmp(i)%ts(istep,iyrs), tmp(i)%ts2(istep,iyrs), tmp(i)%max_mon(mo), tmp(i)%min_mon(mo), tmp(i)%end_day, tmp(i)%end_yr, tmp(i)%max_mon, tmp(i)%min_mon` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%tmpfiles` |
| [sym:time_module] | `time, ndays, ndays_leap, ndays_noleap` | `time%yrc, time%day_start` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `tmp(i)%start_day` | After the first daily record is read from each temperature file, before the file is backspaced. | Stores the first Julian day of the temperature series so downstream code knows when observations begin within the file. |
| `tmp(i)%start_yr` | After the first daily record is read from each temperature file, before the file is backspaced. | Stores the calendar year containing the file's first daily observation. |
| `tmp(i)%yrs_start` | If the file starts after the simulation year, `iyrs` is set from the gap to `time%yrc`; otherwise it is reset to zero. | Records how many simulation years precede the file start so the daily arrays can be indexed from the first usable year. |
| `ndays` | Each time the routine checks the current year, including the initial year and any later year transitions. | Selects the correct cumulative-day lookup table for leap or non-leap years. |
| `tmp(i)%max_mon(mo)` | For every loaded daily record, after `xmon` identifies the month number. | Accumulates the sum of daily maximum temperatures for that month before averaging. |
| `tmp(i)%min_mon(mo)` | For every loaded daily record, after `xmon` identifies the month number. | Accumulates the sum of daily minimum temperatures for that month before averaging. |
| `tmp(i)%end_day` | After the main daily read loop finishes for a file. | Stores the last Julian day loaded from the file so the file's ending date is preserved. |
| `tmp(i)%end_yr` | After the main daily read loop finishes for a file. | Stores the last year loaded from the file so the file's ending year is preserved. |
| `tmp(i)%max_mon` | After all daily records are read and month counts are available. | Holds the monthly average maximum temperatures computed from the accumulated sums. |
| `tmp(i)%min_mon` | After all daily records are read and month counts are available. | Holds the monthly average minimum temperatures computed from the accumulated sums. |
| `db_mx%tmpfiles` | After all temperature files from `tmp.cli` have been processed. | Publishes how many measured-temperature files were loaded so other climate routines can iterate over them. |

## File I/O

<!-- facts:io -->


## Lineage

`cli_tmeas.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cli_tmeas.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `f8bb6ec` (2024-07-25) — Manually coded init changes
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_tmeas' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft into 11 source-backed steps that follow the file-list scan, per-file load, year-boundary handling, and final summary flow.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
