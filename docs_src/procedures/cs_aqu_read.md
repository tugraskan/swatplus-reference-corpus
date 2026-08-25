---
kind: procedure
symbol: cs_aqu_read
title: cs_aqu_read
status: filled
source_hash: f71a43039c642d65
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch text buffer for title or separator lines read from `cs_aqu.ini`; it is
    used to skip non-data rows both during the counting pass and the data-loading pass.
  header: Scratch text buffer for header lines in `cs_aqu.ini`; the routine reads two header
    records into it and discards them before reaching the data rows.
  ics: Loop index for walking through each aquifer constituent record in the file and through
    each allocated `cs_aqu_ini` entry.
  eof: I/O status flag from each `read` on unit 107; the routine uses negative values to detect
    end-of-file and nonnegative values to keep counting or loading records.
  imax: Counter for the number of aquifer constituent data rows found in `cs_aqu.ini`; it
    becomes the allocation size and is copied into `db_mx%cs_ini`.
  i_exist: Logical result from `inquire` that reports whether `cs_aqu.ini` exists before the
    routine attempts to read it.
uses:
  constituent_mass_module: The `constituent_mass_module` provides the shared aquifer constituent
    database and storage that this routine fills. `cs_db%num_cs` determines how large each
    aquifer concentration array must be, and `cs_aqu_ini(ics)%name` plus `cs_aqu_ini(ics)%aqu`
    receive the parsed name and values for every record.
  input_file_module: This module is part of the reader framework that supplies file-handling
    conventions for input-data routines; `cs_aqu_read` follows the same model of reading a
    fixed named `.ini` file used by the other `proc_read` loaders.
  maximum_data_module: The `maximum_data_module` holds the shared maximum-record counters.
    `db_mx%cs_ini` is updated here so the rest of the model can know how many aquifer constituent
    initialization rows were read.
---

<!-- facts:header -->

Reads the aquifer initial constituent concentration file `cs_aqu.ini` and loads the data into shared aquifer constituent state. It also counts the records first so it can size the `cs_aqu_ini` storage and record the number of aquifer constituent entries.

## Bottom Line

`cs_aqu_read` is the aquifer-side companion to the other constituent readers in `proc_read`. It opens `cs_aqu.ini`, skips the title and header rows, counts the data records, stores that count in `db_mx%cs_ini`, allocates `cs_aqu_ini`, and then reads each aquifer constituent name plus its initial concentration/sorbed-mass array into module state.

That matters because later groundwater constituent initialization and transport routines need the loaded `cs_aqu_ini` records and the `db_mx%cs_ini` count to know how many aquifer constituent entries exist and what starting values to use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the input-reading phase of the model, when `proc_read` is assembling all constituent-related initialization data. `proc_read` calls it after `cs_hru_read` and before other constituent readers, and the resulting `cs_aqu_ini` array plus `db_mx%cs_ini` value are used later when aquifer constituent state is initialized and simulated.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the aquifer constituent file should be read | The routine calls `inquire` on `cs_aqu.ini` to set `i_exist`, then proceeds only if the file exists or the filename test is not the sentinel value `null`. |
| 2. Open the aquifer constituent file | It enters a read loop and opens unit 107 on `cs_aqu.ini` so the file can be scanned. |
| 3. Skip title and header records | It reads and discards one title line and two header lines, exiting early if end-of-file is encountered during the scan. |
| 4. Count data records | It initializes `imax` to zero and then reads through the remaining records, incrementing `imax` once per aquifer constituent record until end-of-file is reached. |
| 5. Save the record count for the model | It copies the number of records found into `db_mx%cs_ini` so the shared maximum-data state reflects the size of the aquifer constituent input. |
| 6. Allocate the aquifer constituent container | It allocates `cs_aqu_ini(imax)` so there is one storage element for each aquifer constituent record. |
| 7. Allocate each aquifer constituent concentration array | It loops over all records and allocates `cs_aqu_ini(ics)%aqu` to hold `cs_db%num_cs + cs_db%num_cs` values, initializing the array to zero with `source = 0.`. |
| 8. Rewind the file for the data pass | It rewinds unit 107 so the file can be read again from the start, this time to load values into memory. |
| 9. Skip title and headers again | It rereads and discards the title line and two header lines after the rewind, positioning the file at the first data record. |
| 10. Read each aquifer constituent record into module state | It loops over the expected record count and reads each line into `cs_aqu_ini(ics)%name` and `cs_aqu_ini(ics)%aqu`, exiting if an end-of-file condition occurs. |
| 11. Close the input file and finish | It closes unit 107, leaves the file-reading loop, and returns to the caller with the loaded aquifer constituent state in shared module storage. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_aqu_ini, cs_db, cs_aqu` | `cs_aqu_ini(ics)%aqu, cs_db%num_cs, cs_aqu_ini(ics)%name` |
| [sym:input_file_module] | `input_file_module` | `input-file control state and file-path conventions used by the SWAT+ reader workflow` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cs_ini` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%cs_ini` | When `cs_aqu.ini` is available and the routine completes the counting pass, `db_mx%cs_ini` is set to the number of aquifer constituent data rows found. | This records the size of the aquifer constituent initialization database so downstream code can use the correct record count and allocate or iterate over the loaded entries safely. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior changes to `cs_aqu_read`: the file was introduced in df07e3f as a reader for aquifer constituent initialization data; f8bb6ec changed the aquifer concentration allocation to initialize the array contents to zero with `source = 0.`; and 39fabde initialized the local scratch variables `titldum`, `header`, `ics`, `eof`, and `imax` at declaration.

- df07e3f introduced the full `cs_aqu_read` subroutine, including the `cs_aqu.ini` double-pass read, record counting, allocation of `cs_aqu_ini`, and assignment to `db_mx%cs_ini`.
- f8bb6ec changed the `cs_aqu_ini(ics)%aqu` allocation so each aquifer concentration array is zero-initialized with `source = 0.`.
- 39fabde initialized the local working variables `titldum`, `header`, `ics`, `eof`, and `imax` to default values at declaration.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- algorithm_steps revised: split the original broad scan/read phases into eleven source-backed steps to match the visible control flow and line numbers.
- The `input_file_module` snippet did not resolve a concrete symbol used by this routine; its role is inferred from the SWAT+ reader context.
