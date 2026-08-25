---
kind: procedure
symbol: salt_aqu_read
title: salt_aqu_read
status: filled
source_hash: 0886991a3c3ccbbc
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the title line, and later the
    per-record first field while counting and loading `salt_aqu.ini`.
  header: Scratch character buffer used to read and discard the three header lines in `salt_aqu.ini`
    before the data records are counted or loaded.
  isalt: Loop index over aquifer salt records in `salt_aqu_ini`, used both when allocating
    per-entry arrays and when reading each record into storage.
  eof: I/O status flag returned by each `read` on unit 107; it controls end-of-file detection
    and exits from the counting and loading loops.
  imax: Holds the number of aquifer salt data records found in `salt_aqu.ini`; later used
    to allocate `salt_aqu_ini` and to loop over each entry.
  i_exist: Logical flag set by `inquire` to indicate whether `salt_aqu.ini` exists before
    the routine attempts to process it.
uses:
  constituent_mass_module: This module provides the shared salt initialization database and
    salt-count metadata that `salt_aqu_read` fills. The routine allocates and populates `salt_aqu_ini`,
    using `cs_db%num_salts` to size each entry's `conc` array and storing salt names, concentrations,
    and fractions in `salt_aqu_ini(isalt)%name`, `%conc`, and `%frac`; these values become
    the aquifer salt initial conditions used by the rest of the model.
  input_file_module: This module matters because the routine uses its file-existence state
    in the `inquire`/`if` guard that decides whether `salt_aqu.ini` should be processed at
    all. The imported logical `i_exist` is the only referenced symbol from this module in
    the extracted source.
  maximum_data_module: This module matters because `db_mx%salt_gw_ini` records how many aquifer
    salt initialization records were found in `salt_aqu.ini`. That count is set before allocation
    and can be used later by code that needs the maximum or actual number of groundwater salt
    initialization entries.
---

<!-- facts:header -->

Reads the aquifer salt-initialization file `salt_aqu.ini` and loads initial salt names, concentrations, and mineral fractions into shared model storage. It also counts how many aquifer salt records are present so later code can size related arrays.

## Bottom Line

salt_aqu_read is a file-driven initialization routine for aquifer salt ions. It opens `salt_aqu.ini`, skips the title and header lines, counts the data records to determine how many aquifer salt entries are present, then allocates `salt_aqu_ini` and its per-entry concentration and fraction arrays.

After sizing storage, it rewinds the file and reads each record into `salt_aqu_ini(isalt)%name`, `%conc`, and `%frac`. It also stores the record count in `db_mx%salt_gw_ini`, which lets other parts of the model know how many groundwater salt initialization records were loaded.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the input-reading phase, called by `proc_read` after other constituent and hydrology readers have set up shared database state such as salt counts. Its result is the aquifer salt initialization database and record count, which later model code uses when simulating salt conditions in groundwater and when referencing the number of loaded salt entries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Test whether the salt aquifer file should be processed | The routine uses `inquire(file="salt_aqu.ini", exist=i_exist)` and a file-name check to decide whether to enter the reading logic. |
| 2. Open the aquifer salt input file and skip its non-data lines | It opens unit 107 on `salt_aqu.ini` and reads a title line plus three header lines, stopping early if end-of-file is encountered. |
| 3. Count the number of data records | It resets `imax` to zero, then repeatedly reads one record at a time until `eof` changes, incrementing `imax` for each data line encountered. |
| 4. Save the record count in shared state | The routine copies the counted record total into `db_mx%salt_gw_ini` so the rest of the model knows how many aquifer salt entries were loaded. |
| 5. Allocate the aquifer salt database | It allocates `salt_aqu_ini(imax)` and then allocates each entry's `conc` and `frac` arrays, using `cs_db%num_salts` for concentration length and five slots for mineral fractions. |
| 6. Rewind the file and skip the headers again | After rewinding unit 107, it rereads the title and header lines so the file pointer is positioned at the first data record for the actual load pass. |
| 7. Load each aquifer salt record into shared arrays | The routine reads each record into `salt_aqu_ini(isalt)%name`, `%conc`, and `%frac`, filling the allocated aquifer salt initialization database. |
| 8. Close the input file and leave the routine | It closes unit 107, exits the surrounding file-processing block, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `salt_aqu_ini, cs_db` | `salt_aqu_ini(isalt)%conc, cs_db%num_salts, salt_aqu_ini(isalt)%frac(5), salt_aqu_ini(isalt)%name, salt_aqu_ini(isalt)%frac` |
| [sym:input_file_module] | `input_file_module` | `i_exist` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%salt_gw_ini` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%salt_gw_ini` | When `salt_aqu.ini` is present and the routine successfully counts the data records. | `db_mx%salt_gw_ini` is updated to the number of aquifer salt initialization records found in `salt_aqu.ini`, so downstream code can know how many groundwater salt entries were read. |

## File I/O

<!-- facts:io -->


## Lineage

This procedure was introduced in df07e3f as a new reader for aquifer salt initial data. In 39fabde, the allocation of each entry's `conc` and `frac` arrays changed to allocate with zero initialization (`source = 0.`), and the local scalars `titldum`, `header`, `isalt`, `eof`, and `imax` were initialized at declaration; 35b029c and 94b6dec show earlier formatting and file-addition history but no additional behavioral changes in the resolved diff for this routine.

- 39fabde initialized local variables and changed the per-entry array allocations to zero-fill `salt_aqu_ini(isalt)%conc` and `salt_aqu_ini(isalt)%frac`, preventing uninitialized values in the loaded aquifer salt state.
- df07e3f added the full `salt_aqu_read` routine to read `salt_aqu.ini`, count records, allocate storage, and populate aquifer salt initialization data.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- input_file_module is referenced in the source only through the file-existence guard; no additional imported symbols were resolved from the provided context.
- The source uses `if (i_exist .or. "salt_aqu.ini" /= "null") then`, which appears to make the guard always true because the filename literal is not equal to "null"; this behavior is preserved in the source-backed summary rather than interpreted.
