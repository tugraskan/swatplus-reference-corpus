---
kind: procedure
symbol: soil_plant_init
title: soil_plant_init
status: filled
source_hash: f84bedfaab620d3a
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch title/data-line buffer used to skip the first line and to count remaining
    records while scanning `soil_plant.ini`; it is not stored after reading.
  header: Scratch header buffer used to skip the second line of `soil_plant.ini` during both
    the counting pass and the data-loading pass.
  eof: I/O status flag for `read` operations. It is initialized to 0, set by `iostat`, and
    used to detect end-of-file or other read failures.
  imax: Counter for the number of soil-plant records found in the file. It becomes the allocation
    size for `sol_plt_ini` and is copied to `db_mx%sol_plt_ini`.
  i_exist: Logical file-existence flag returned by `inquire`; it controls whether the routine
    proceeds with opening and reading the configured input file.
  ii: Loop index over soil-plant records in the second pass that loads the allocated array.
uses:
  hru_module: The `sol_plt_ini` array in `hru_module` is the target being filled. Its components
    hold the soil-plant initialization values read from each record, so this module is the
    in-memory destination for the file contents.
  basin_module: The basin control code `bsn_cc%nam1` selects which file layout to expect.
    When it is zero the routine reads a shorter record without `csc`; otherwise it reads the
    extra `csc` field, so this flag directly governs parsing.
  input_file_module: The configured path `in_init%soil_plant_ini` tells the routine which
    file to open. Without this input-file state, the subroutine would not know where to read
    the soil-plant initialization data from.
  maximum_data_module: The maximum-data tracker `db_mx%sol_plt_ini` records how many soil-plant
    initialization entries were found. Other code can use that count to size or iterate over
    the loaded database entries consistently.
  constituent_mass_module: This module is imported by the routine, but no resolved symbols
    from it are referenced in the extracted source span. It likely matters because this initialization
    is part of the broader constituent-mass setup, but the visible code here does not show
    a direct use.
---

<!-- facts:header -->

Initializes soil-plant coefficient data from `soil_plant.ini` into the shared `sol_plt_ini` array. It counts records, allocates storage, and loads each initialization row for later HRU setup.

## Bottom Line

This routine reads the soil-plant initialization file named by `in_init%soil_plant_ini` (normally `soil_plant.ini`). It first scans the file to count how many data rows are present, stores that count in `db_mx%sol_plt_ini`, allocates `sol_plt_ini(imax)`, then rereads the file to populate each `sol_plt_ini(ii)` record.

The loaded records provide plant-related initial constituent identifiers and fractions used by later SWAT+ initialization and database logic. A basin control flag, `bsn_cc%nam1`, changes whether the routine reads the `csc` field, so the file format can support both older and newer input layouts.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the reading phase of model setup, immediately after `pest_metabolite_read` and before other database readers such as `solt_db_read`. `proc_read` calls it after the shared input-file and database state has been established, and its results feed later HRU and constituent initialization that depends on the populated `sol_plt_ini` array and its count.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | The routine asks whether the configured soil-plant initialization file exists. It only proceeds when the file is present or the configured name is not the literal string "null". |
| 2. Open the configured file and start a read loop | The routine opens unit 107 on `in_init%soil_plant_ini` and reads the first line into `titldum` to begin scanning the file. |
| 3. Skip the header line | It reads the second line into `header`, then checks for end-of-file before continuing. |
| 4. Count data records | The routine resets `imax` to zero and then repeatedly reads one line into `titldum`, incrementing `imax` for each record until a read signals end-of-file. |
| 5. Store the record count | It copies the counted record total into `db_mx%sol_plt_ini` so the rest of the model knows how many soil-plant initialization entries were found. |
| 6. Allocate the target array | The routine allocates `sol_plt_ini(imax)` so each soil-plant initialization row has a storage slot. |
| 7. Rewind and rescan the file | It rewinds unit 107 and rereads the title and header lines so the file position returns to the first data row. |
| 8. Load each soil-plant record | The routine loops from 1 to `imax` and reads each record into `sol_plt_ini(ii)`. If `bsn_cc%nam1` is zero, it reads the shorter format without `csc`; otherwise it reads the longer format including `csc`. |
| 9. Close the input file | After loading all records, the routine closes unit 107 to finish with `soil_plant.ini`. |
| 10. Return to caller | The subroutine exits after the shared array and count have been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `sol_plt_ini` | `sol_plt_ini(ii)%name, sol_plt_ini(ii)%sw_frac, sol_plt_ini(ii)%nutc, sol_plt_ini(ii)%pestc, sol_plt_ini(ii)%pathc, sol_plt_ini(ii)%saltc, sol_plt_ini(ii)%hmetc, sol_plt_ini(ii)%csc` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%nam1` |
| [sym:input_file_module] | `in_init` | `in_init%soil_plant_ini` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%sol_plt_ini` |
| [sym:constituent_mass_module] | `constituent_mass_module` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%sol_plt_ini` | When `in_init%soil_plant_ini` exists or is not the string "null", the routine counts the records and assigns the result to `db_mx%sol_plt_ini`. | `db_mx%sol_plt_ini` changes from its initial value to the number of soil-plant initialization rows found in the input file. That count is then available for later allocation and iteration over the `sol_plt_ini` database. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f as a new soil-plant initialization reader that scans `soil_plant.ini`, counts records, allocates `sol_plt_ini`, and loads the data. 39fabde changed only local variable initialization by giving `titldum`, `header`, `eof`, `imax`, and `ii` explicit default values. 1c812c1 added `basin_module` and changed the record read so that `bsn_cc%nam1` selects between a shorter format and a newer format that includes `csc`.

- df07e3f: added the full `soil_plant_init` file-reading and allocation workflow for soil-plant initialization data.
- 39fabde: initialized the scratch variables and counters, but did not alter the file-reading logic.
- 1c812c1: introduced `bsn_cc%nam1`-controlled parsing and support for the optional `csc` field.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'soil_plant_init' has no extracted documentation comment.
- algorithm_steps revised: split the original combined scan/read phase into distinct open, count, rewind, load, and close steps to match the visible source lines.
- constituent_mass_module is imported but no resolved symbol from it appears in the extracted source span; its exact role is not visible here.
