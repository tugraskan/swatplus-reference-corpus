---
kind: procedure
symbol: res_read_saltdb
title: res_read_saltdb
status: filled
source_hash: 276e2f86894dd22b
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer for title or record lines while skipping file headers
    and probing records during both the counting pass and the data load pass.
  header: Scratch character buffer for the database header line read after the skipped title
    lines; it marks the start of the actual table section before record counting and loading.
  i: Loop counter used to skip the fixed block of eight non-data lines in the file header.
  eof: I/O status flag from list-directed reads; the routine uses it to detect end-of-file
    or read failure and stop scanning/loading.
  imax: Counts how many reservoir salt records are found in `salt_res`, and then becomes the
    allocation size for `res_salt_data(0:imax)`.
  i_exist: Logical file-existence flag returned by `inquire`; it controls whether the routine
    reads `salt_res` or falls back to a minimal allocation.
  ires: Loop index for filling `res_salt_data(1:imax)` with reservoir names and initial concentration
    arrays.
  isalti: Loop index for allocating the `c_init` array for each reservoir record before the
    file is reread and populated.
uses:
  input_file_module: This module supplies the configured reservoir nutrient input filename
    state. `res_read_saltdb` uses `in_res%nut_res` as an enable/disable check, so if it is
    set to `"null"` the routine skips normal loading even when the file exists.
  maximum_data_module: This module holds the shared database-size counter that records how
    many reservoir salt entries were found. `res_read_saltdb` writes `db_mx%res_salt` so other
    routines can know the array extent.
  reservoir_data_module: The routine uses this module as part of the reservoir initialization
    context even though no specific resolved component was extracted. It matters because the
    salt database is read during reservoir setup and must be consistent with the reservoir
    data structures that will later consume it.
  res_salt_module: This module defines the allocatable reservoir salt database that the routine
    sizes and fills. The routine allocates each record's `c_init` array and then stores the
    reservoir name plus salt-ion initial concentrations into `res_salt_data`.
  constituent_mass_module: This module provides the number of salt constituents simulated.
    `res_read_saltdb` uses `cs_db%num_salts` to allocate each reservoir's `c_init` array with
    the correct number of salt-ion slots.
---

<!-- facts:header -->

Reads the reservoir salt database file and loads per-reservoir initial salt concentrations into shared model state.

## Bottom Line

`res_read_saltdb` opens the reservoir salt input file `salt_res`, checks that it exists and that reservoir nutrient input is enabled, then scans the file to count how many reservoir salt records are present. It uses that count to size `res_salt_data` and stores the total in `db_mx%res_salt`.

It then rewinds the file and reads each reservoir name and its initial salt concentrations into `res_salt_data(ires)%name` and `res_salt_data(ires)%c_init`. Those values become the reservoir salt database used later when reservoir objects are allocated and initialized.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir initialization inside `proc_res`, after the other reservoir database readers and before reservoir objects are allocated and used. Its results provide the salt-specific reservoir database that later reservoir setup and simulation logic rely on for initial concentrations and database sizing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether reservoir salt input should be read | The routine tests whether `salt_res` exists and whether `in_res%nut_res` is not `"null"`; otherwise it skips normal loading and allocates a minimal `res_salt_data(0:0)` array. |
| 2. Open the reservoir salt file and skip the title/header block | When loading is enabled, the routine opens unit 105 on `salt_res`, reads two title lines, skips eight fixed header lines, and reads the table header while checking for end-of-file conditions. |
| 3. Count reservoir salt records | The routine reads each remaining line into `titldum` until end-of-file and increments `imax` for every reservoir salt record found. |
| 4. Publish the record count and allocate storage | The count is copied to `db_mx%res_salt`, then `res_salt_data(0:imax)` is allocated and each record's `c_init` array is allocated to length `cs_db%num_salts` with zeros. |
| 5. Rewind and re-skip the file header | The file is rewound so the data pass starts at the beginning again, and the same title/header block is skipped to align with the record section. |
| 6. Read each reservoir salt record into shared state | For each reservoir entry, the routine reads a label probe, backs up one record, then reads the reservoir name and initial salt concentrations into `res_salt_data(ires)`. |
| 7. Finish and close the file | After loading all records, the loop exits, the file is closed, and the subroutine returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_res` | `in_res%nut_res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_salt` |
| [sym:reservoir_data_module] | `reservoir_data_module state/types` | `reservoir-data types and reservoir-related shared state imported by the routine` |
| [sym:res_salt_module] | `res_salt_data` | `res_salt_data(isalti)%c_init, res_salt_data(ires)%name, res_salt_data(ires)%c_init` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%res_salt` | When `salt_res` exists and `in_res%nut_res` is not `"null"`, after the counting pass completes | Stores the number of reservoir salt database records found in `salt_res`, so downstream code can size and interpret the reservoir salt array. |

## File I/O

<!-- facts:io -->


## Lineage

`res_read_saltdb` was introduced in df07e3f with the initial reservoir-salt reader implementation. 94b6dec added the source file into the tree with the same file-scan/count/load structure, and 39fabde initialized the local scalars and changed the per-reservoir `c_init` allocation to zero-fill the array. 35b029c made only a formatting cleanup at the end of the subroutine.

- df07e3f introduced the full `salt_res` scan/count/allocate/load workflow and the `db_mx%res_salt` assignment.
- 39fabde changed local variable initialization and zero-initialized each `res_salt_data(isalti)%c_init` allocation.
- 35b029c only adjusted trailing source formatting and did not change behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_saltdb' has no extracted documentation comment.
