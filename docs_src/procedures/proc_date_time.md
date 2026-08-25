---
kind: procedure
symbol: proc_date_time
title: proc_date_time
status: filled
source_hash: b45ccfb208708e9e
version_label: SWAT+ 62.0.0
locals:
  date_time: Eight-element integer array filled by `DATE_AND_TIME`; the routine uses elements
    1, 2, 3, 5, 6, and 7 to format the simulation date and clock time for status output.
  b: Three-character buffer array passed to `DATE_AND_TIME` to receive date/time text components;
    it is not otherwise used in this routine.
uses:
  time_module: The routine `use`s `time_module`, and the resolved outside reference shows
    the module-owned `time` object is available here even though this subroutine does not
    assign to it directly.
---

<!-- facts:header -->

Prints the simulation date/time and announces the climate files being read.

## Bottom Line

proc_date_time captures the current date and time, writes a formatted timestamp to the screen and log unit 9003, then prints a sequence of status messages before each climate-file reader is called.

It does not load data itself; instead, it acts as a startup/status routine that brackets the measured PET, precipitation, temperature, solar radiation, relative humidity, wind, weather-generator, and weather-station reads with human-readable progress messages.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs at the start of the climate-input loading sequence. It prints the current simulation date/time, then announces each climate file just before the corresponding reader routine is called, so the startup log shows progress through PET, precipitation, temperature, solar radiation, humidity, wind, WGN, and weather-station inputs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Capture current date/time | Call `DATE_AND_TIME`, then write the formatted simulation date and time to standard output and unit 9003. |
| 2. Announce PET input | Print the PET-file status message to both outputs, refresh the timestamp, and call `cli_petmeas` to read measured PET data. |
| 3. Announce precipitation input | Print the precipitation-file status message to both outputs and call `cli_pmeas` to read measured precipitation data. |
| 4. Announce temperature input | Print the temperature-file status message, refresh the timestamp, and call `cli_tmeas` to read measured temperature data. |
| 5. Announce solar radiation input | Print the solar-radiation status message, refresh the timestamp, and call `cli_smeas` to read measured solar-radiation data. |
| 6. Announce humidity input | Print the relative-humidity status message, refresh the timestamp, and call `cli_hmeas` to read measured humidity data. |
| 7. Announce wind input | Print the wind-file status message, refresh the timestamp, and call `cli_wmeas` to read measured wind data. |
| 8. Announce WGN input | Print the weather-generator and weather-station status messages, refresh the timestamp, and call `cli_wgnread` to read WGN data. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `date_time` | each `DATE_AND_TIME` call | Refreshes the local timestamp array before printing the next status line. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_date_time.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_date_time.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No resolved caller was found in the scanned source tree.
- The routine is a status/logging wrapper around climate-file readers; it does not itself parse climate data.
- The final `write` pair at lines 47-49 announces the wx station file but does not call another routine afterward.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
