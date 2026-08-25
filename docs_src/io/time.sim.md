---
kind: io
source_symbols:
- time_read
title: '`time.sim`'
status: filled
source_hash: 671a9a11f5cba7e9
version_label: SWAT+ 62.0.0
---

**Primary target:** `time(:)` (array of `type time_current`)  
**Read by:** [sym:time_read]

## Bottom Line

The `time.sim` input file configures the simulation time control parameters for the SWAT+ model, including start and end dates, time step resolution, and printing intervals.

This file is optional and is read by the `time_read` subroutine.

It initializes the `time` variable of derived type `time_current` from the `time_module`.

| Module | Role for this file |
| --- | --- |
| [sym:time_module] | Provides the derived type `time_current` and the variable `time` where the simulation time parameters are stored. |
| [sym:input_file_module] | Provides the `in_sim` variable which contains the file path for `time.sim`. |

## File Variables

The `time.sim` file contains simulation time control parameters that map directly into the components of the `time_current` derived type. Each record corresponds to a set of time parameters such as start and end days, years, and time step size.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `time%day_print` | character (len=1) |  | Not explicitly documented in source; likely a flag for daily printing |
| 3 |  | `time%day` | integer |  | current day of simulation |
| 4 |  | `time%mo` | integer |  | current month of simulation |
| 5 |  | `time%mo_start` | integer |  | starting month |
| 6 |  | `time%yrc` | integer |  | current calendar year |
| 7 |  | `time%yrc_start` | integer |  | starting calendar year |
| 8 |  | `time%yrc_end` | integer |  | ending calendar year |
| 9 |  | `time%yrs` | integer |  | current sequential year |
| 10 |  | `time%day_mo` | integer |  | day of month (1-31) |
| 11 |  | `time%end_mo` | integer |  | set to 1 if end of month |
| 12 |  | `time%end_yr` | integer |  | set to 1 if end of year |
| 13 |  | `time%end_sim` | integer |  | set to 1 if end of simulation |
| 14 |  | `time%end_aa_prt` | integer |  | set to 1 if end of simulation |
| 15 |  | `time%day_start` | integer |  | beginning julian day of simulation |
| 16 |  | `time%day_end_yr` | integer |  | ending julian day of each year |
| 17 |  | `time%day_end` | integer |  | input ending julian day of simulation |
| 18 |  | `time%nbyr` | integer |  | number of years of simulation run |
| 19 |  | `time%step` | integer |  | number of time steps in a day for rainfall, runoff and routing |
| 20 |  | `time%dtm` | real |  | 0 = daily; 1=increment(12 hrs); 24=hourly; 96=15 mins; 1440=minute; time step in minutes for rainfall, runoff and routing |
| 21 |  | `time%days_prt` | real |  | number of days for average annual printing for entire time period |
| 22 |  | `time%yrs_prt` | real |  | number of years for average annual printing for entire time period |
| 23 |  | `time%yrs_prt_int` | real |  | number of years for average annual printing for printing interval- pco%aa_yrs() |
| 24 |  | `time%num_leap` | integer |  | number of leap years in simulation for average annual printing |
| 25 |  | `time%prt_int_cur` | integer |  | current average annual print interval |
| 26 |  | `time%yrc_tot` | integer |  | Not explicitly documented in source |

## Sample

```text
Example time.sim file snippet:
Title of simulation time control file
Header describing the time parameters
1 2020 365 2022 1
```

## Read Pattern

```fortran
open (107,file=in_sim%time)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) time%day_start, time%yrc_start, time%day_end, time%yrc_end, time%step
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_sim%time)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) time%day_start, time%yrc_start, time%day_end, time%yrc_end, time%step` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:time_read] | open, read, close | Reads the `time.sim` file to initialize the simulation time parameters stored in the `time` variable of type `time_current`. It sets start and end days and years, the number of time steps per day, and derives additional fields such as month and day of month using the external `xmon` subroutine. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The `day_print` and `yrc_tot` fields lack explicit source documentation; their meanings are inferred or unknown.
- The sample read format is a minimal example constructed from typical file content; no full example dataset was available in the source.
