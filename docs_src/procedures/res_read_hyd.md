---
kind: procedure
symbol: res_read_hyd
title: res_read_hyd
status: filled
source_hash: 94e69069d6c0b456
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and discard title/label lines from hydrology.res
    before the data records are counted or loaded.
  header: Temporary string used to read and discard the file header line from hydrology.res
    before the data records are processed.
  eof: I/O status flag for reads on unit 105; zero means reads continue, negative values indicate
    end-of-file or read termination.
  imax: Counter for the number of reservoir hydrology data records found in hydrology.res;
    it becomes the allocation size and the value stored in `db_mx%res_hyd`.
  i_exist: Logical flag set by `inquire` to show whether the configured hydrology file exists
    before the routine tries to open it.
  ires: Loop counter for loading each reservoir hydrology record into `res_hyddb`.
uses:
  basin_module: This module is imported by the routine and is part of the shared model state
    context available while reservoir hydrology records are read and stored.
  input_file_module: '`in_res%hyd_res` supplies the configured filename to open and read,
    so this module determines which hydrology file the routine processes.'
  maximum_data_module: '`db_mx%res_hyd` stores the count of reservoir hydrology records discovered
    in the file, which matters for downstream sizing and validation of reservoir database
    usage.'
  reservoir_data_module: '`res_hyddb` is the shared reservoir hydrology array that receives
    each parsed record and the defaulted parameter values used later by reservoir process
    calculations.'
---

<!-- facts:header -->

Reads reservoir hydrology definitions from hydrology.res into the shared reservoir hydrology database, setting missing geometry defaults as needed.

## Bottom Line

`res_read_hyd` loads the reservoir hydrology file named by `in_res%hyd_res`, counts the data rows, allocates `res_hyddb`, and reads each reservoir record into the shared database. It also updates `db_mx%res_hyd` with the number of records found.

After reading each record, it fills in default values for missing principal spillway volume, emergent spillway volume, surface areas, and evaporation coefficient so later reservoir calculations have usable hydrologic parameters.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir setup in `proc_res`, immediately after the reservoir process initialization sequence begins. `proc_res` calls `res_read_hyd` before other reservoir readers such as sediment, nutrients, and initial conditions, and the populated `res_hyddb` plus `db_mx%res_hyd` are then used by later reservoir calculations and related readers.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check for the configured file | Reset `eof` and `imax`, inquire whether `in_res%hyd_res` exists, and if the file is missing or set to the literal string `null`, allocate a one-element placeholder `res_hyddb(0:0)` and stop file processing. |
| 2. Open the hydrology file and skip title/header lines | Open hydrology.res on unit 105, read the title line into `titldum`, then read the header line into `header`. Abort the scan early if either read reaches end-of-file. |
| 3. Count reservoir records | Loop through the remaining lines, reading each record into `titldum` only to advance the file pointer, and increment `imax` for every data line encountered until the read status signals end-of-file. |
| 4. Store the discovered record count and allocate storage | Copy the record count into `db_mx%res_hyd` and allocate `res_hyddb(0:imax)` so the reservoir hydrology database can hold every file record. |
| 5. Rewind and reread title/header for the load pass | Rewind unit 105 to the beginning of hydrology.res and reread the title and header lines so the file is positioned at the first data record for loading. |
| 6. Read each reservoir hydrology record | Loop from `ires = 1` to `imax`, reading each file record into `res_hyddb(ires)` and stopping early if a read error or end-of-file occurs. |
| 7. Fill in missing reservoir parameter defaults | For each loaded record, derive reasonable defaults when key hydrology values are missing: use 0.9 times `evol` or 60000.0 for `pvol`, compute `evol` from `pvol`, set `psa` from `pvol`, set `esa` from `psa`, and default `evrsv` to 0.6. |
| 8. Close the file and return | Close unit 105, exit the enclosing block, and return to the caller with `res_hyddb` and `db_mx%res_hyd` populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` | `basin_module` |
| [sym:input_file_module] | `in_res` | `in_res%hyd_res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_hyd` |
| [sym:reservoir_data_module] | `res_hyddb` | `res_hyddb(ires)%pvol, res_hyddb(ires)%evol, res_hyddb(ires)%psa, res_hyddb(ires)%esa, res_hyddb(ires)%evrsv` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%res_hyd` | When hydrology.res exists and contains readable reservoir data lines | Set to the number of reservoir hydrology records counted in the file so the model knows how many reservoir entries were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved for `res_read_hyd`. The initial addition in `df07e3f` created the routine to read `hydrology.res`, count records, allocate `res_hyd`, and populate default reservoir hydrology values. Commit `96c2bfb` changed the target array name from `res_hyd` to `res_hyddb` throughout the routine, including the allocation and read assignments, but did not change the algorithm. Commit `39fabde` initialized the local variables `titldum`, `header`, `eof`, `imax`, and `ires` with default values, without changing the file-reading logic.

- df07e3f introduced the full reservoir hydrology file-reading workflow: file existence check, record counting, allocation, second-pass record loading, default value filling, and file close.
- 96c2bfb renamed the in-memory reservoir hydrology target from `res_hyd` to `res_hyddb` in this routine so the reader writes to the database array used by the rest of the model.
- 39fabde initialized the local scratch variables and counters to safe defaults, reducing reliance on later assignment before file reads begin.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_hyd' has no extracted documentation comment.
