---
kind: procedure
symbol: cs_irr_read
title: cs_irr_read
status: filled
source_hash: d863aeec354ea27f
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and skip the first title line and then
    to count remaining data records during the file scan and reread passes.
  header: Temporary character buffer used to read and skip the file header line before the
    data records are counted or loaded.
  icsi: Loop index for the second pass that reads each irrigation-source constituent record
    into `cs_water_irr`.
  ics: Loop index used when allocating the per-record `water` array for each irrigation-source
    constituent entry.
  eof: I/O status flag from `read` statements; zero means continue, negative values stop the
    scan or reread at end-of-file or error.
  imax: Count of irrigation-source constituent records found in `cs_irrigation`; used to size
    `cs_water_irr` and to store `db_mx%cs_ini`.
  i_exist: Logical file-existence flag set by `inquire`; controls whether the routine attempts
    to open and read `cs_irrigation`.
uses:
  constituent_mass_module: 'The constituent mass module provides the shared irrigation-source
    storage being populated here: `cs_water_irr` holds each outside irrigation entry''s name
    and water concentrations, and `cs_db%num_cs` supplies the number of constituent concentration
    slots to allocate for each entry. Without this module, the routine could not size or fill
    the irrigation-source constituent database.'
  input_file_module: This module matters because the routine is part of SWAT+'s centralized
    input-reading workflow and is compiled alongside the file/input infrastructure used by
    the model; however, no specific imported symbol from `input_file_module` is resolved in
    the provided evidence beyond the `use` statement.
  maximum_data_module: The maximum-data module holds `db_mx%cs_ini`, which this routine updates
    after counting the records in `cs_irrigation`. That count is a model-wide size indicator
    used later to know how many outside irrigation-source constituent entries were loaded.
---

<!-- facts:header -->

Reads the `cs_irrigation` input file and loads outside-source irrigation constituent concentrations into shared SWAT+ state.

## Bottom Line

`cs_irr_read` checks whether the `cs_irrigation` file exists, scans it to count how many irrigation-source constituent records are present, allocates storage for that many entries, and then rereads the file to populate each entry's name and water-concentration values.

The routine also records the discovered record count in `db_mx%cs_ini`, so later code knows how many outside irrigation-source constituent entries were loaded for the constituent system.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cs_irr_read` runs during the `proc_read` input phase, after other constituent-related readers have been called and before later constituent setup routines such as `cs_plant_read`, `cs_uptake_read`, `cs_reactions_read`, `cs_urban_read`, and `cs_fert_read`. Its results populate the outside-irrigation constituent database used by later constituent-mass behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the irrigation constituent file exists | The routine tests for the presence of `cs_irrigation` with `inquire`. If the file is absent, it skips the rest of the reader. |
| 2. Open and inspect the file header | When the file exists, the routine opens unit 107 on `cs_irrigation` and reads the title and header lines into temporary buffers, stopping early if an end/error condition is returned. |
| 3. Count irrigation-source records | The routine resets `imax` to zero and loops through the remaining lines, incrementing the count for each record it can read until end-of-file or error is reached. The final count is stored in `db_mx%cs_ini`. |
| 4. Allocate shared storage for the records | Using the discovered record count, the routine allocates `cs_water_irr(imax)` and then allocates each entry's `water` array to match `cs_db%num_cs`, initializing the water values to zero. |
| 5. Rewind and reread the file | The routine rewinds unit 107, skips the title and header again, and then reads each record's constituent name and water-concentration vector into `cs_water_irr(icsi)`. |
| 6. Close the input file and return | After all records are loaded, the routine closes unit 107 and exits, leaving the populated irrigation-source constituent array and record count in shared module state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_water_irr, cs_db` | `cs_water_irr(ics)%water, cs_db%num_cs, cs_water_irr(icsi)%name, cs_water_irr(icsi)%water` |
| [sym:input_file_module] | `input_file_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cs_ini` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%cs_ini` | After `cs_irrigation` exists and the file scan completes, `imax` is assigned to `db_mx%cs_ini`. | `db_mx%cs_ini` becomes the number of irrigation-source constituent records found in `cs_irrigation`, which gives the rest of the model a size for this input database. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows the routine was added in df07e3f with the full file-read workflow, then f8bb6ec changed the `water` allocation to initialize with `source = 0.`, and 39fabde initialized the local buffers and counters plus applied formatting changes to the allocation statements.

- df07e3f introduced the entire `cs_irr_read` subroutine, including file existence checking, record counting, allocation, rereading, and storage of `db_mx%cs_ini`.
- f8bb6ec changed the per-entry `water` allocation to initialize the array contents to zero at allocation time.
- 39fabde initialized `titldum`, `header`, `icsi`, `ics`, `eof`, and `imax` and made minor allocation-format changes without altering the file-reading logic.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- No specific imported symbols from `input_file_module` were resolved in the provided evidence, so its role is documented at module level only.
