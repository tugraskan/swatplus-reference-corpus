---
kind: procedure
symbol: time_read
title: time_read
status: filled
source_hash: 3f2c391b22d0c816
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from `time.sim`; it consumes the first record before
    the header and numeric timing values.
  header: Temporary header line read from `time.sim`; it consumes the second record before
    the simulation timing values.
  eof: I/O status flag for the reads. It is initialized to zero and set by `read(..., iostat=eof)`
    to detect end-of-file or read failure.
  mo: Scratch month output from `xmon`; the routine uses it to transfer the converted starting
    month into `time%mo` and `time%mo_start`.
  day_mo: Scratch day-of-month output from `xmon`; the routine copies it into `time%day_mo`.
  i_exist: Logical existence test for `in_sim%time`; it determines whether the configured
    file is present before the routine attempts to read it.
uses:
  time_module: The `time_module` shared `time` object is the destination for every simulation
    timing value this routine reads or derives. Without that module state, `time_read` could
    not publish the start/end bounds, step size, year count, or converted month/day values
    for later model initialization and time stepping.
  input_file_module: The `input_file_module` shared `in_sim` object supplies the configured
    path name for the simulation time file through `in_sim%time`. `time_read` uses that path
    both to test whether the file exists and to open the correct file for record reads.
---

<!-- facts:header -->

Reads the simulation time settings from `time.sim` into the shared `time` state. It also derives the simulation year count and starting month/day fields used by the rest of the model.

## Bottom Line

This routine opens the configured `time.sim` file, reads its title, header, and the simulation start/end/time-step values, then stores those values in `time_module`'s shared `time` structure. It also normalizes invalid step/day values and derives the simulation length in years plus the start month/day-of-month via `xmon`.

The results matter because `proc_bsn` calls `time_read` before basin parameter setup continues, and later model code depends on `time%day_start`, `time%yrc_start`, `time%day_end`, `time%yrc_end`, `time%step`, `time%nbyr`, `time%mo`, `time%day_mo`, `time%mo_start`, and `time%yrc`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during basin-level setup, after `proc_bsn` has opened diagnostics and read basin connectivity/object data, and before later basin parameter work continues. Its outputs establish the simulation calendar and time-step controls that downstream model execution uses for time stepping and date-related logic.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the simulation time file should be read | The routine queries whether `in_sim%time` exists and also checks whether the configured name is not the literal string `null`. If neither condition is true, it skips the file-reading block. |
| 2. Open the configured simulation time file | If the file is enabled, the routine enters a loop and opens unit 107 on `in_sim%time` so it can read the file contents. |
| 3. Read and discard the title record | It reads the first record into `titldum` and exits if the read reports end-of-file or an error through `eof`. |
| 4. Read and discard the header record | It reads the second record into `header` and again exits if the input status indicates end-of-file or failure. |
| 5. Read the simulation timing values | It reads the start day/year, end day/year, and time-step values into the shared `time` structure, stopping if the record cannot be read. |
| 6. Normalize invalid step and start-day values | If `time%step` is nonpositive, it is forced to 1. If `time%day_start` is nonpositive, it is forced to 1. |
| 7. Derive simulation length in years | The routine computes `time%nbyr` as `time%yrc_end - time%yrc_start + 1` so the shared time state reflects the number of simulation years covered by the file. |
| 8. Convert the starting Julian day to month and day-of-month | It calls `xmon` with `time%day_start` to obtain `mo` and `day_mo`, then stores those values in `time%mo`, `time%day_mo`, and `time%mo_start`. |
| 9. Leave the read loop and close the file | After the successful read path, the loop is exited and the routine closes unit 107. |
| 10. Set the current year and return | The routine copies the start year into `time%yrc` and then returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day_start, time%yrc_start, time%day_end, time%yrc_end, time%step, time%nbyr, time%mo, time%day_mo, time%mo_start, time%yrc` |
| [sym:input_file_module] | `in_sim` | `in_sim%time` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `time%nbyr` | After a valid `time.sim` read, `time%yrc_end` and `time%yrc_start` are available. | The routine sets `time%nbyr` to the inclusive year span of the simulation, using end year minus start year plus one. |
| `time%mo` | After `xmon` returns the month for `time%day_start`. | The routine stores the converted start month in `time%mo` so the shared time state knows the calendar month at simulation start. |
| `time%day_mo` | After `xmon` returns the day-of-month for `time%day_start`. | The routine stores the converted day-of-month in `time%day_mo` so later logic can use the calendar day within the start month. |
| `time%mo_start` | After `xmon` returns the start month. | The routine copies the start month into `time%mo_start` as a dedicated record of the simulation's starting month. |
| `time%yrc` | After the file read and month conversion complete. | The routine sets `time%yrc` to `time%yrc_start`, establishing the current calendar year at the beginning of the simulation. |

## File I/O

<!-- facts:io -->


## Lineage

`time_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `time_read.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'time_read' has no extracted documentation comment.
- The source shows `open (107,file=in_sim%time)` inside a `do` loop with an unconditional `exit` after the first successful read path; the loop structure is unusual but preserved in the description.
- No lineage commits were resolved for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
