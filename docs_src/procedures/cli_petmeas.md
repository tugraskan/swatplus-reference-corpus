---
kind: procedure
symbol: cli_petmeas
title: cli_petmeas
status: filled
source_hash: 68541855b8d43fcd
version_label: SWAT+ 62.0.0
locals:
  i: Loop index over PET files, file records, and daily time steps.
  titldum: Scratch string used to read and discard title or data rows while scanning the control
    and PET files.
  header: Scratch string used to read and discard header rows in `pet.cli` and each PET data
    file.
  eof: I/O status flag from each read; negative values trigger early exit when a file ends
    or a read fails.
  imax: Counts how many PET file entries are listed in `pet.cli`, and is used to size `petm`
    and `petm_n`.
  iyr: Calendar year read from the measured PET file while locating the simulation start and
    loading values.
  i_exist: Holds the `inquire` result for whether the configured PET control file exists on
    disk.
  istep: Julian day / timestep read from the measured PET file and used as the daily record
    index.
  iyr_prev: Tracks the previous year while loading PET records so the code can increment the
    year counter when the file rolls into a new year.
  iyrs: Index into the second dimension of `petm(i)%ts`, representing which year block is
    currently being filled.
  pet_read: Temporary holder for one PET value used while skipping forward to the simulation
    start point before storing values into `petm(i)%ts`.
uses:
  climate_module: This module owns the `petm` array and `petm_n` names that `cli_petmeas`
    allocates and fills. The routine stores filename, geometry, timing metadata, and daily
    PET series into those shared climate records for later use by the simulation.
  input_file_module: This module provides the configured control-file name `in_cli%pet_cli`
    and optional directory prefix `in_path_pet%peti`. `cli_petmeas` uses them to locate `pet.cli`
    and the referenced measured PET files.
  time_module: The current simulation year and starting day determine where measured PET loading
    should begin. `cli_petmeas` compares file dates against `time%yrc` and `time%day_start`
    to skip records before the model start.
  maximum_data_module: '`db_mx%petfiles` records how many measured PET files were found. Other
    parts of the model can use that count to know how many PET datasets are available after
    this loader runs.'
---

<!-- facts:header -->

Reads the measured PET control file and each referenced PET data file, then stores their metadata and time-series values in shared climate state.

## Bottom Line

cli_petmeas is the measured-potential-evapotranspiration file loader. It first checks whether the configured `pet.cli` exists; if it does not, or if the path is set to `null`, it creates empty PET containers. Otherwise it scans `pet.cli` to count PET-file entries, allocates `petm` and `petm_n`, then reads each referenced measured PET file and loads its file name, metadata, start/end timing, and daily values into `climate_module` state.

This routine matters because later model code can only use measured PET after `petm` has been populated and `db_mx%petfiles` has been set. It also aligns each dataset to the simulation calendar using `time%yrc` and `time%day_start`, so downstream water-balance calculations can access the correct daily PET records.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the input-reading phase, when `proc_date_time` has just reported that it is reading PET data and then calls `cli_petmeas`. Its results populate shared climate storage before later model calculations need measured PET time series and file metadata.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check for control-file availability | The routine clears the working counters, checks whether `in_cli%pet_cli` exists, and if the file is missing or set to `null` it allocates empty PET containers instead of attempting to read data. |
| 2. Count PET file entries in the control file | It opens `pet.cli`, skips the title and header rows, and counts each remaining record to determine how many measured PET files are listed. |
| 3. Allocate PET file-name storage | Using the counted maximum, it allocates `petm(0:imax)` for the measured PET objects and `petm_n(imax)` for the file-name list. |
| 4. Read the PET file-name list from the control file | The routine rewinds `pet.cli`, rereads the title and header, and loads each PET file name into `petm(i)%filename`. |
| 5. Open each measured PET file | For each listed file, it opens the measured PET data file either directly or through `in_path_pet%peti`, then skips that file's title and header rows. |
| 6. Read dataset metadata and allocate the daily series | It reads `nbyr`, `tstep`, `lat`, `long`, and `elev`, then allocates `petm(i)%ts(366,petm(i)%nbyr)` to hold the daily PET values for each year. |
| 7. Identify the dataset start year and day | The routine reads the first date record, stores `start_day` and `start_yr`, and sets `yrs_start` from the difference between the file year and `time%yrc` when the file starts after the simulation year. |
| 8. Advance to the simulation start point | It reads and discards PET records until it reaches the first record on or after `time%yrc` and `time%day_start`, then backs up one record so the main load loop can reread it. |
| 9. Load daily PET values by year block | The routine reads year, day, and PET value triplets into `petm(i)%ts(istep,iyrs)`, and when it reaches day 365 or 366 it peeks ahead to detect a year change and increments `iyrs` as needed. |
| 10. Close each file and save the end date | After the series is loaded, it closes the PET data file and records the last read day and year in `end_day` and `end_yr`. |
| 11. Finish control-file processing | Once all PET files are handled, it closes `pet.cli`, stores the total count in `db_mx%petfiles`, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `petm, petm_n` | `petm(i)%filename, petm(i)%nbyr, petm(i)%tstep, petm(i)%lat, petm(i)%long, petm(i)%elev, petm(i)%start_day, petm(i)%start_yr, petm(i)%yrs_start, petm(i)%ts(istep,iyrs), petm(i)%end_day, petm(i)%end_yr` |
| [sym:input_file_module] | `in_cli, in_path_pet` | `in_cli%pet_cli, in_path_pet%peti` |
| [sym:time_module] | `time` | `time%yrc, time%day_start` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%petfiles` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `petm(i)%start_day` | After reading the first date record from each measured PET file. | `petm(i)%start_day` is set to the first Julian day found in the file so the dataset's beginning can be recorded in shared climate state. |
| `petm(i)%start_yr` | After reading the first date record from each measured PET file. | `petm(i)%start_yr` is set to the first calendar year found in the file so the dataset's starting year is preserved. |
| `petm(i)%yrs_start` | When the file starts after the current simulation year; otherwise it is set to zero. | `petm(i)%yrs_start` records how many whole years of simulation occur before the file begins, which is used to align the loaded PET series with the model calendar. |
| `petm(i)%end_day` | After the daily load loop finishes for each measured PET file. | `petm(i)%end_day` captures the last Julian day read from the file so the dataset's end position is known. |
| `petm(i)%end_yr` | After the daily load loop finishes for each measured PET file. | `petm(i)%end_yr` captures the last calendar year read from the file so the dataset's end year is known. |
| `db_mx%petfiles` | After all PET file entries have been counted and processed. | `db_mx%petfiles` is updated with the number of measured PET files found in `pet.cli`, providing a global count for later model logic. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four behavior-relevant revisions: the subroutine was added in df07e3f; f8bb6ec changed the PET-series allocation to initialize `petm(i)%ts` with zeros; 39fabde initialized local scalars such as `i`, `titldum`, `header`, `eof`, `imax`, `iyr`, `istep`, `iyr_prev`, `iyrs`, and `pet_read`; and 2ee1889 made only a formatting cleanup to the final `return` line.

- df07e3f introduced the full `cli_petmeas` implementation for loading measured PET control and data files.
- f8bb6ec changed `allocate (petm(i)%ts(366,petm(i)%nbyr))` to `allocate (petm(i)%ts(366,petm(i)%nbyr), source = 0.)`, ensuring PET storage starts zero-filled.
- 39fabde initialized the routine's local variables at declaration time, reducing dependence on prior values before reads and loops.
- 2ee1889 only removed trailing whitespace from `return` and did not change runtime behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_petmeas' has no extracted documentation comment.
