---
kind: procedure
symbol: res_read_salt_cs
title: res_read_salt_cs
status: filled
source_hash: 944494620bb96552
version_label: SWAT+ 62.0.0
locals:
  i: Loop counter over reservoir entries while scanning the `reservoir.res_cs` file.
  header: Holds the two header lines read from `reservoir.res_cs` before the data records
    are processed.
  eof: Receives I/O status from list-directed reads so the routine can stop cleanly at end-of-file
    or a read failure.
  imax: Initialized but not used in the shown source; it appears to be a leftover counter
    or size placeholder.
  i_exist: Logical flag set by `inquire` to indicate whether `reservoir.res_cs` is present
    before opening it.
  ires: Reservoir index read from the file and used to place the parsed salt/constituent names
    into the correct reservoir record.
  k: Leading integer field read from each data record and discarded; it is used only to consume
    the full record before the character fields are parsed.
  isalt: Loop index used to search all defined reservoir salt records for a name match.
  ics: Loop index used to search all defined reservoir constituent records for a name match.
uses:
  maximum_data_module: The counts in `db_mx%res_dat`, `db_mx%res_salt`, and `db_mx%res_cs`
    control how many reservoir rows and lookup-table entries this routine allocates and scans,
    so they determine the loop bounds and storage size.
  reservoir_data_module: The `res_dat_c_cs` and `res_dat` arrays hold the raw string inputs
    and the resolved integer indices for each reservoir, so this routine both fills and updates
    those shared reservoir records.
  constituent_mass_module: This lookup table provides the canonical salt names that are compared
    against `res_dat_c_cs(ires)%salt` so the routine can convert the file's text name into
    the correct salt index.
  reservoir_module: The reservoir module provides the shared reservoir records that store
    both the parsed names and the resolved salt/constituent references used by later reservoir
    setup.
  res_salt_module: This module supplies the `res_salt_data` table whose `name` field is used
    for matching the salt identifier read from the reservoir constituent file.
  res_cs_module: This module supplies the `res_cs_data` table whose `name` field is used for
    matching the constituent identifier read from the reservoir constituent file.
---

<!-- facts:header -->

Reads reservoir salt and constituent lookup names from `reservoir.res_cs` and maps them onto integer indices in reservoir data.

## Bottom Line

This routine opens `reservoir.res_cs`, skips its two header records, and scans each reservoir entry to load the salt and constituent source names into `res_dat_c_cs(ires)`. It then translates those names into numeric indices by matching against the master lookup tables in `res_salt_data` and `res_cs_data`.

Those indices are stored in `res_dat(ires)%salt` and `res_dat(ires)%cs`, which lets later reservoir processing refer to the correct salt and constituent definitions without comparing strings again. If the file does not exist, the routine does nothing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir preprocessing, immediately after `proc_res` has initialized reservoir objects and called `res_read`. Its output is needed before `res_initial` and later reservoir simulation steps can use numeric salt and constituent links instead of file names.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize status variables. | Sets the local counters and status variables to known values before any file work starts, including `eof` and `imax`. |
| 2. Check whether the input file exists. | Uses `inquire` on `reservoir.res_cs` and only continues if the file is present. |
| 3. Open the file and skip its header records. | Opens unit 105 on `reservoir.res_cs` and reads two header lines into `header`. |
| 4. Allocate character-input storage for reservoir constituent links. | Allocates `res_dat_c_cs` to the number of reservoir data records so the raw salt/constituent names can be stored by reservoir index. |
| 5. Loop through reservoir records. | Reads each reservoir index, backs up one record, then rereads the line into the integer field and character-input structure for that reservoir. |
| 6. Match the salt name to a salt index. | Searches all defined salt names and stores the matching index in `res_dat(ires)%salt`. |
| 7. Match the constituent name to a constituent index. | Searches all defined constituent names and stores the matching index in `res_dat(ires)%cs`. |
| 8. Close the file and return. | Closes unit 105 if the file was opened and then exits the routine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_dat, db_mx%res_salt, db_mx%res_cs` |
| [sym:reservoir_data_module] | `res_dat_c_cs, res_dat` | `res_dat_c_cs(ires)%salt, res_dat(ires)%salt, res_dat_c_cs(ires)%cs, res_dat(ires)%cs` |
| [sym:constituent_mass_module] | `res_salt_data` | `res_salt_data(isalt)%name` |
| [sym:reservoir_module] | `res_dat, res_dat_c_cs` | `res_dat(ires)%salt, res_dat(ires)%cs, res_dat_c_cs(ires)%salt, res_dat_c_cs(ires)%cs` |
| [sym:res_salt_module] | `res_salt_data` | `res_salt_data(isalt)%name` |
| [sym:res_cs_module] | `res_cs_data` | `res_cs_data(ics)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `res_dat(ires)%salt` | When a reservoir entry's salt name in `res_dat_c_cs(ires)%salt` matches `res_salt_data(isalt)%name`. | Stores the resolved salt lookup index in `res_dat(ires)%salt` so later reservoir processing can refer to the configured salt definition by number. |
| `res_dat(ires)%cs` | When a reservoir entry's constituent name in `res_dat_c_cs(ires)%cs` matches `res_cs_data(ics)%name`. | Stores the resolved constituent lookup index in `res_dat(ires)%cs` so later reservoir processing can refer to the configured constituent definition by number. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f with the full reservoir salt/constituent file-reading logic. 35b029c only adjusted trailing whitespace and the end statement, while 39fabde initialized the local counters and header string to zero or empty values without changing the reading algorithm.

- df07e3f added the new `res_read_salt_cs` routine to open `reservoir.res_cs`, allocate `res_dat_c_cs`, read reservoir records, and map salt/constituent names to indices.
- 35b029c made no behavioral change; it only cleaned up the file ending and blank lines.
- 39fabde did not change the algorithm, but it initialized `i`, `header`, `eof`, `imax`, `ires`, `k`, `isalt`, and `ics` at declaration time.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_salt_cs' has no extracted documentation comment.
- algorithm_steps revised: condensed the core algorithm into eight source-backed steps that match the visible control flow and line numbers.
- No candidate references were resolved for `constituent_mass_module` or `reservoir_module`; their roles are inferred from the imported reservoir lookup and data state used by this routine.
- The source initializes `imax` but never uses it in the shown procedure.
