---
kind: procedure
symbol: soil_db_read
title: soil_db_read
status: filled
source_hash: df7ab7a185d1ae78
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch text buffer used to read and skip title/record-label lines from `soils.sol`
    during both the counting pass and the data load pass.
  header: Scratch text buffer used to read the file header line from `soils.sol` before scanning
    or loading profile records.
  eof: IO status flag from each `read`; it controls loop exit on end-of-file or read failure
    and is also reused to detect when the scan/load should stop.
  imax: Counts how many soil profiles were found during the initial scan so the routine can
    size `soildb` and publish `db_mx%soil`.
  i_exist: Logical flag set by `inquire` to decide whether `in_sol%soils_sol` can be opened
    or whether the routine must fall back to a minimal empty database.
  j: Loop counter for reading individual soil layers within one soil profile.
  nlyr: Holds the layer count read during the scan pass for the current profile so the routine
    can skip that many layer lines and increment `imax`.
  lyr: Temporary loop counter used only while scanning through layer records in the first
    pass.
  mlyr: Copies the current profile's layer count from `soildb(isol)%s%nly` so the routine
    can allocate and read the correct number of layer entries.
  isol: Loop counter for the soil-profile records loaded into `soildb`; each iteration fills
    one profile and its layers.
uses:
  input_file_module: '`input_file_module` supplies `in_sol%soils_sol`, the configured path
    to the soils database file. That path determines which file is checked, opened, rewound,
    and read here.'
  maximum_data_module: '`maximum_data_module` supplies `db_mx%soil`, the shared count of loaded
    soil profiles. `soil_db_read` sets it after the counting pass so other routines can use
    the database size.'
  soil_data_module: '`soil_data_module` defines the `soildb` allocatable database and the
    profile/layer components that this routine fills from file records. Those structures are
    the actual in-memory result of the load.'
---

<!-- facts:header -->

Reads the soil database file `soils.sol` into the shared `soildb` array and records the number of soil profiles in `db_mx%soil`. It also enforces a minimum first-layer depth rule for each soil profile.

## Bottom Line

`soil_db_read` is the SWAT+ soil database loader. It checks whether the configured soils file exists, scans it once to count soil profiles, allocates `soildb`, then rewinds and reads each soil profile header and layer records into `soil_data_module` state.

The routine matters because later model code uses the loaded soil profile metadata and layer properties for hydrology, erosion, and soil-process calculations. It also updates `db_mx%soil` so other code knows how many soil database entries were loaded.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`soil_db_read` runs during the general read phase, called by `proc_read` after other database readers such as `snowdb_read`. It depends on `proc_read` having already entered the model's input-loading workflow, and its results feed later soil-based model calculations that use `soildb` and `db_mx%soil`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize scratch variables and counters | Set up local string buffers, counters, and the I/O status flag, with `eof` and `imax` starting at zero. |
| 2. Test whether the configured soil file can be used | Check whether `in_sol%soils_sol` exists and is not the literal string `null`; if not, allocate a minimal one-entry soil database with a zero-sized layer array. |
| 3. Open the soil file and skip the title/header records | Open unit 107 on `soils.sol`, then read and discard the title and header lines before scanning records. |
| 4. Count soil profiles and their layer lines | Loop through the file to count how many soil profiles exist, using each profile's `nlyr` value to skip the correct number of layer records and increment `imax` once per profile. |
| 5. Publish the profile count and allocate the database | Store the counted profile total in `db_mx%soil` and allocate `soildb(0:imax)` to hold the soil database entries. |
| 6. Rewind the file and restart from the beginning | Rewind unit 107 and reread the file title and header so the load pass starts from the first record again. |
| 7. Read each soil profile header and allocate its layers | For each soil entry, read the profile name and layer count, allocate that profile's layer array, backspace one record, then reread the full profile metadata fields. |
| 8. Read each layer record for the current profile | Loop through all layers in the profile and read the depth and soil-property fields for each layer into `soildb(isol)%ly(j)`. |
| 9. Enforce the first-layer depth rule | If the first layer depth is less than 20 cm, adjust it upward to 20 cm when the profile has one layer or when the second layer is deeper than 20 cm. |
| 10. Close the file and return | Exit the outer loops, close unit 107, and return to the caller with the soil database loaded. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_sol` | `in_sol%soils_sol` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%soil` |
| [sym:soil_data_module] | `soildb` | `soildb(0)%ly(0:0), soildb(isol)%s%snam, soildb(isol)%s%nly, soildb(isol)%ly(mlyr), soildb(isol)%s%hydgrp, soildb(isol)%s%zmx, soildb(isol)%s%anion_excl, soildb(isol)%s%crk, soildb(isol)%s%texture, soildb(isol)%ly(j)%z, soildb(isol)%ly(j)%bd, soildb(isol)%ly(j)%awc, soildb(isol)%ly(j)%k, soildb(isol)%ly(j)%cbn, soildb(isol)%ly(j)%clay, soildb(isol)%ly(j)%silt, soildb(isol)%ly(j)%sand, soildb(isol)%ly(j)%rock, soildb(isol)%ly(j)%alb, soildb(isol)%ly(j)%usle_k, soildb(isol)%ly(j)%ec, soildb(isol)%ly(j)%cal, soildb(isol)%ly(j)%ph, soildb(isol)%ly(1)%z, soildb(isol)%ly(2)%z` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%soil` | After the initial scan pass completes and before allocation of the soil database array. | `db_mx%soil` is set to the number of soil profiles found in `soils.sol`, so later routines can know how many soil database entries were loaded and iterate over them safely. |
| `soildb(isol)%ly(1)%z` | If a loaded profile's first layer depth is below 20 cm, and the profile has only one layer or the second layer is deeper than 20 cm. | `soildb(isol)%ly(1)%z` is raised to 20 cm to enforce the routine's minimum first-layer depth rule for the loaded soil profile. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four commits affecting `soil_db_read`: df07e3f created the routine with file scanning, allocation, and layered reads; 39fabde initialized the local variables and kept the allocation/read flow intact; 56aa528 changed the layer-reading loop to use the file's custom layer depths; 72206bc added a post-read adjustment that raises the first layer depth to at least 20 cm. 84ef959 later refined that adjustment so it only applies when the profile has one layer or the second layer is deeper than 20 cm.

- df07e3f introduced the initial soil file ingestion workflow: existence check, profile counting, allocation of `soildb`, full reread, and layer population.
- 39fabde initialized the local scratch variables and counters (`titldum`, `header`, `eof`, `imax`, `j`, `nlyr`, `lyr`, `mlyr`, `isol`) without changing the read algorithm.
- 56aa528 preserved the same database structure but changed the layer-loading loop to honor custom layer depths specified in the file.
- 72206bc added a minimum-depth correction for the first soil layer after reading the layer records.
- 84ef959 narrowed the first-layer depth correction so it only applies for single-layer profiles or when a second layer exists deeper than 20 cm.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'soil_db_read' has no extracted documentation comment.
