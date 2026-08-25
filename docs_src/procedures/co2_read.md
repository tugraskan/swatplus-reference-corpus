---
kind: procedure
symbol: co2_read
title: co2_read
status: filled
source_hash: aae5529349ffc644
version_label: SWAT+ 62.0.0
grounding_allow:
- co2
- yrs
- co2_yr
locals:
  titldum: A title or heading string read from `co2_yr.dat` and discarded after use; it appears
    to be the first non-data line in the file.
  header: A second header string read from `co2_yr.dat` and skipped before the annual CO2
    records are loaded.
  done: A one-character flag that tracks whether `co2y` has already been filled from the basin
    default or from a CO2 file range, so later branches can be skipped.
  eof: I/O status flag used on `read` calls from unit 107; negative values terminate the scan
    of `co2_yr.dat`.
  i_exist: Logical result from `inquire` that says whether `co2_yr.dat` exists before attempting
    to open it.
  iyr_start: Computes the starting index offset between the simulation start year and the
    first CO2 record year.
  iyrc: Working calendar-year counter used when writing `co2.out` so each `co2y` value is
    paired with the correct year.
  itot: Loop index used while reading and storing each annual CO2 record into `co2_inc%co2_yr`.
  iyr: Loop index over the model years in `time%nbyr` when filling or writing the `co2y` series.
  iyr_co2: Index into the annual CO2 input series while mapping file years onto simulation
    years.
  co2_end: Holds the last CO2 value read from the annual file so the routine can extend that
    value beyond the final record if needed.
  co2: A component of the local `co2` derived type that stores one annual CO2 concentration
    value from the file.
  yrs: A component of the local `co2_annual` derived type that stores how many annual CO2
    records were read.
  co2_yr: Allocatable array inside `co2_inc` that stores the sequence of annual year/CO2 records
    read from `co2_yr.dat`.
  co2_inc: Local container that holds the number of annual records and the allocatable year/CO2
    record array read from the input file.
uses:
  input_file_module: The module is used here only as an input-file support dependency; the
    visible code does not reference any specific imported symbol from it, so the routine relies
    on its file-handling context rather than a named state item.
  basin_module: '`bsn_prm%co2` supplies the fallback basin CO2 concentration when no annual
    CO2 file is available, so this module provides the default concentration that populates
    `co2y`.'
  time_module: '`time%nbyr`, `time%yrc`, and `time%yrc_start` define the simulation length
    and calendar-year window that `co2_read` maps the annual CO2 values onto.'
  climate_module: '`co2y` is the shared climate-series array that this routine allocates and
    fills; later climate and simulation code reads it as the active CO2 time series.'
  output_path_module: This module matters because `open_output_file` uses the output-path
    machinery to open `co2.out` in the model's configured output location.
---

<!-- facts:header -->

Reads annual atmospheric CO2 values from `co2_yr.dat` when present, expands them to the simulation years, and writes the resulting series to `co2.out`.

## Bottom Line

`co2_read` prepares the CO2 concentration time series used by the basin simulation. It first opens the CO2 output file, then tries to read a year-by-year CO2 input file. If no annual file is available, it falls back to the basin default CO2 concentration from `bsn_prm%co2`.

When annual CO2 data are available, the routine maps them onto the model run years in `co2y`, carrying the last known value forward when the input record ends before the simulation ends. It then writes the year/CO2 pairs to `co2.out` for inspection.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_bsn` calls `co2_read` after basin parameters and print codes are read and initialized. The routine must run before later basin/carbon setup so `co2y` is available as the CO2 forcing series for the rest of the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Open the CO2 output file and write its header. | The routine calls `open_output_file` for unit 2222 and writes the column heading `YR    CO2(ppm)` to `co2.out`. |
| 2. Check whether the annual CO2 input file exists. | It inquires on `co2_yr.dat` and branches away if the file is missing or disabled by the literal comparison against `" null"`. |
| 3. Open and scan the annual CO2 file. | Inside the read loop, unit 107 is opened on `co2_yr.dat`, the title and header lines are skipped, the record count is read, storage is allocated, and each annual CO2 record is read into `co2_inc%co2_yr` until done. |
| 4. Allocate the simulation-year output array. | The shared `co2y` array is allocated for `time%nbyr` simulation years and initialized to zero before any fallback or mapping logic runs. |
| 5. Fall back to the basin default when no annual CO2 records exist. | If `co2_inc%yrs` is zero, every model year is assigned `bsn_prm%co2` and the routine marks the work as done. |
| 6. Fill all years with the last file value when the file ends before the simulation starts. | If the simulation start year is at or after the last annual CO2 record year, the routine copies that final CO2 value into every year of `co2y` and stops further processing. |
| 7. Map annual CO2 records onto the simulation years. | When the annual series overlaps the simulation window, the routine computes the starting offset, walks through each simulation year, assigns the file value when a matching record exists, and carries the last read value forward after the file ends. |
| 8. Write the year-by-year CO2 series to the output file. | The routine starts from `time%yrc_start` and writes each simulation year with its corresponding `co2y` value to unit 2222. |
| 9. Return to the caller. | The subroutine exits after the shared CO2 series has been prepared and reported. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `No imported symbols from `input_file_module` are referenced in the visible source span.` |  |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%co2` |
| [sym:time_module] | `time` | `time%nbyr, time%yrc, time%yrc_start` |
| [sym:climate_module] | `co2y` |  |
| [sym:output_path_module] | `No imported symbols from `output_path_module` are referenced by name in the visible source span.` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `co2y(iyr)` | When an annual CO2 record exists for the current simulation year, or when the routine falls back to the basin default / last available value. | `co2y(iyr)` is assigned from `bsn_prm%co2`, from the last annual record, or from `co2_inc%co2_yr(iyr_co2)%co2` depending on which branch applies; these assignments establish the CO2 concentration used for each simulation year. |

## File I/O

<!-- facts:io -->


## Lineage

`co2_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `504d2b3` (2025-12-11, "Align Use statements and adjusting whitespace."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `co2_read.f90` are listed.

- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'co2_read' has no extracted documentation comment.
- algorithm_steps revised: split the original scan/allocate/store draft into explicit read, allocation, fallback, mapping, and write steps based on the visible source lines.
- No resolved lineage commits were available for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
