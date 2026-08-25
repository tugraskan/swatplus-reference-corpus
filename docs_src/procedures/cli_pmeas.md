---
kind: procedure
symbol: cli_pmeas
title: cli_pmeas
status: filled
source_hash: 103e872de74a1950
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary text buffer for reading and skipping title lines in pcp.cli and the station
    files.
  header: Temporary text buffer for reading and skipping the header line in pcp.cli and the
    station files.
  eof: I/O status flag used to detect normal reads, end-of-file, and to stop the scan/parse
    loops.
  imax: Counts how many precipitation station entries are listed in pcp.cli so the routine
    can allocate pcp and pcp_n to the right size.
  iyr: Holds the calendar year read from a station file while locating the simulation start
    and while loading time-series records.
  i_exist: Set by INQUIRE to indicate whether the configured pcp.cli file exists before the
    routine tries to read it.
  mpcp: Scratch counter initialized to zero; it is not used later in the shown routine.
  i: Loop index for iterating over station entries in pcp.cli and then over station-file records.
  istep: Holds the Julian day or time-step index read from station files and becomes the saved
    start/end day values.
  iyr_prev: Tracks the previous year while reading station records so the routine can detect
    when the record stream advances into a new year.
  iyrs: Counts which simulation year slot is being filled in the allocated precipitation arrays.
  iss: Subdaily sample counter used when loading time-step precipitation into pcp(i)%tss.
  mo: Receives the month value from subdaily precipitation records; it is read to preserve
    the record structure.
  day_mo: Receives the day-of-month value from subdaily precipitation records; it is read
    to preserve the record structure.
  ihr: Receives the hour value from subdaily precipitation records; it is read to preserve
    the record structure.
uses:
  climate_module: The climate_module provides the pcp and pcp_n allocatable arrays that this
    routine fills. It also defines each station's metadata fields and time-series storage,
    so the loader can store filenames, station attributes, start/end dates, and precipitation
    values in the expected shared types.
  maximum_data_module: db_mx%pcpfiles is the shared count of precipitation files discovered
    in pcp.cli. Setting it here lets the rest of the model know how many precipitation stations
    were loaded and how large the precipitation station list is.
  basin_module: This module owns the precipitation station data structures that cli_pmeas
    populates. Those fields are the persistent state used later by climate and simulation
    routines to access station metadata and measured precipitation series.
  input_file_module: in_cli%pcp_cli identifies the station-list file to open, and in_path_pcp%pcp
    optionally supplies a directory prefix for each station file name. Without these input-file
    settings, the routine would not know where to find the precipitation configuration and
    data files.
  time_module: time%step, time%yrc, and time%day_start define the simulation time grid and
    starting point. cli_pmeas uses them to size subdaily arrays and to skip forward in each
    station file until the record reaches the simulation start.
---

<!-- facts:header -->

Reads measured precipitation station metadata and time-series records from pcp.cli and the referenced station files. It loads them into the shared climate database and records the number of precipitation files available.

## Bottom Line

This routine is the precipitation-file loader. It first checks whether the configured pcp.cli list file exists; if it does not, it creates empty placeholder arrays. Otherwise, it scans pcp.cli to count stations, allocates storage, reads each station filename, and then opens each station file to load station metadata and precipitation records into the shared pcp array.

The results matter because later climate and simulation code depends on pcp(:) and db_mx%pcpfiles being populated. For each station, the routine stores file name, number of years, time-step flag, location metadata, start/end dates, and either daily totals or subdaily time-series values, using the current simulation time window from time_module to align the records.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during startup in proc_date_time, after the precipitation input file names have been set up in the input-file modules and before the temperature and solar loaders run. Its output populates the shared precipitation station database that later climate initialization and weather-driving routines depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check for the list file | Resets local counters, probes for the configured pcp.cli file, and branches to an empty-data path if the file is missing or explicitly set to 'null'. |
| 2. Count station entries in pcp.cli | Opens pcp.cli and scans past the title and header lines, then counts remaining non-empty records to determine how many precipitation station files are listed. |
| 3. Allocate precipitation metadata arrays | Allocates pcp and pcp_n to match the counted number of precipitation files so the station list and station metadata can be stored. |
| 4. Read station filenames from pcp.cli | Rewinds pcp.cli, skips the title/header text again, and reads each precipitation station filename into the pcp_n list and pcp(i)%filename. |
| 5. Open each station file and read its metadata | Opens each referenced station file, skips its title/header lines, reads nbyr, tstep, lat, long, and elev, and allocates either the subdaily tss array or the daily ts array with zeros. |
| 6. Record the first available date in each station file | Reads the first year/day pair, stores it as the station start date, and computes yrs_start from the simulation year so later loading begins in the correct year slot. |
| 7. Skip ahead to the simulation start | Advances through the station file until the record reaches the current simulation year and start day, then backs up so the first in-range record can be read again. |
| 8. Load precipitation records into shared arrays | Reads daily or subdaily precipitation records into pcp(i)%ts or pcp(i)%tss, advances the year-slot counter when a year boundary is detected, and keeps the file positioned so no records are skipped. |
| 9. Store station end date and close the file | Closes the station file after loading and saves the final day and year as the station end date in pcp(i). |
| 10. Publish the number of precipitation files and exit | Closes pcp.cli, stores the number of loaded precipitation files in db_mx%pcpfiles, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `pcp, pcp_n` | `pcp(i)%filename, pcp(i)%nbyr, pcp(i)%tstep, pcp(i)%lat, pcp(i)%long, pcp(i)%elev, pcp(i)%tss, pcp(i)%start_day, pcp(i)%start_yr, pcp(i)%yrs_start, pcp(i)%tss(iss,istep,iyrs), pcp(i)%ts(istep,iyrs), pcp(i)%end_day, pcp(i)%end_yr` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pcpfiles` |
| [sym:basin_module] | `pcp, pcp_n` | `pcp(i)%filename, pcp(i)%nbyr, pcp(i)%tstep, pcp(i)%lat, pcp(i)%long, pcp(i)%elev, pcp(i)%tss, pcp(i)%start_day, pcp(i)%start_yr, pcp(i)%yrs_start, pcp(i)%tss(iss,istep,iyrs), pcp(i)%ts(istep,iyrs), pcp(i)%end_day, pcp(i)%end_yr` |
| [sym:input_file_module] | `in_cli, in_path_pcp` | `in_cli%pcp_cli, in_path_pcp%pcp` |
| [sym:time_module] | `time` | `time%step, time%yrc, time%day_start` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcp(i)%start_day` | After the first year/day pair is read from each station file. | Captures the Julian day of the first precipitation record in pcp(i)%start_day so downstream code knows when the station record begins. |
| `pcp(i)%start_yr` | After the first year/day pair is read from each station file. | Captures the calendar year of the first precipitation record in pcp(i)%start_yr so downstream code knows the record's starting year. |
| `pcp(i)%yrs_start` | When the station start year is later than the current simulation year. | Stores how many years of simulation occur before the precipitation record starts; otherwise leaves the offset at zero for files that already cover the simulation start. |
| `pcp(i)%end_day` | After the final precipitation record has been read from each station file. | Stores the Julian day of the last loaded precipitation record in pcp(i)%end_day. |
| `pcp(i)%end_yr` | After the final precipitation record has been read from each station file. | Stores the calendar year of the last loaded precipitation record in pcp(i)%end_yr. |
| `db_mx%pcpfiles` | After the station list has been counted and all files have been processed. | Publishes the number of precipitation station files discovered in pcp.cli so other model components can size and reference the precipitation database. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f as part of the initial source import, with the full pcp.cli-to-station-file loading flow already present. In f8bb6ec, the allocates for pcp(i)%tss and pcp(i)%ts were changed to initialize the arrays with source = 0. In 39fabde, only local variable initializations were added or corrected (for example titldum, header, eof, imax, iyr, mpcp, i, istep, iyr_prev, iyrs, iss, mo, day_mo, ihr); the file-loading behavior itself was not changed.

- df07e3f established the precipitation loader: it counts entries in pcp.cli, opens each station file, reads metadata and time-series records, and stores the station count in db_mx%pcpfiles.
- f8bb6ec changed the precipitation array allocations so newly allocated daily or subdaily storage is zero-initialized instead of left uninitialized.
- 39fabde standardized initialization of the routine's local scalars and buffers, reducing reliance on separate assignment statements before the file-reading loops.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_pmeas' has no extracted documentation comment.
