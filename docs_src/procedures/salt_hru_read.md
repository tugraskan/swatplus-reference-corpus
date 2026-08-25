---
kind: procedure
symbol: salt_hru_read
title: salt_hru_read
status: filled
source_hash: b642759784338f53
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary 80-character string used to read and discard title or record-label lines
    while scanning and rereading `salt_hru.ini`.
  header: Temporary 80-character string used to skip header lines in `salt_hru.ini` during
    both the counting pass and the data-loading pass.
  isalt: Loop index used while allocating per-HRU salt initialization records.
  isalti: Loop index used while rereading `salt_hru.ini` and loading each HRU record into
    `salt_soil_ini`.
  eof: I/O status flag from each `read`; a negative value indicates end-of-file and stops
    the scan or load loop.
  imax: Counts how many salt HRU records are present in `salt_hru.ini`, then drives allocation
    and the load loop.
  i_exist: Logical flag set by `inquire` to report whether `salt_hru.ini` exists before the
    routine tries to open it.
uses:
  constituent_mass_module: This module provides the shared salt initialization database and
    the constituent count needed to size and populate `salt_soil_ini`. `cs_db%num_salts` determines
    the length of each soil and plant array, and `salt_soil_ini` is the target storage filled
    by this routine.
  input_file_module: The routine uses file-input support from this module as part of the input-file
    handling context for SWAT+ readers, even though no specific imported symbol was isolated
    in the extracted references.
  maximum_data_module: This module holds `db_mx`, the shared maximum-data tracker that records
    how many salt initialization entries were found. `salt_hru_read` updates `db_mx%salt_ini`
    so later routines know the allocated size of the salt initialization database.
---

<!-- facts:header -->

Reads the salt HRU initialization file and loads initial salt concentrations for each HRU entry.
It first counts the records to size storage, then rewinds and fills the shared salt soil/plant initialization arrays.

## Bottom Line

salt_hru_read opens `salt_hru.ini`, scans it to count how many salt initialization records are present, stores that count in `db_mx%salt_ini`, allocates `salt_soil_ini`, and then rereads the file to load each salt name plus its soil and plant concentration arrays.

This routine matters because it turns the HRU salt input file into shared model state used later when salt constituent initialization is needed. It depends on the number of simulated salts already defined in `cs_db%num_salts` so it can size each record's soil and plant arrays correctly.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the input-reading phase, when `proc_read` is loading constituent and HRU setup data. `proc_read` calls it after earlier database initialization routines, and later salt-related model readers rely on `db_mx%salt_ini` and `salt_soil_ini` being populated.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the salt HRU input file should be read | The routine inquires whether `salt_hru.ini` exists and uses that result to decide whether to proceed with file reading. |
| 2. Open the input file and skip the fixed header block | It opens unit 107 on `salt_hru.ini`, reads the title line and four header lines, and exits early if end-of-file is encountered. |
| 3. Count the number of salt HRU records | The routine sets `imax` to zero and then loops through the remaining file contents, reading three fields per record and incrementing `imax` once for each salt initialization entry found. |
| 4. Store the record count in shared maximum-data state | It copies the counted record total into `db_mx%salt_ini` so other routines know how many salt HRU initialization entries are available. |
| 5. Allocate the salt initialization array | The routine allocates `salt_soil_ini(imax)` and, for each entry, allocates the soil and plant concentration arrays using `cs_db%num_salts+5` elements. |
| 6. Rewind the file to reread from the beginning | It rewinds unit 107 so the file can be reread from the start for the actual data load. |
| 7. Skip the header block again | The routine rereads and discards the title and header lines, positioning the file at the first data record. |
| 8. Load each salt HRU record | For each record, it reads the HRU name, the soil concentration array, and the plant concentration array into the corresponding `salt_soil_ini(isalti)` entry. |
| 9. Close the input file and return | After populating all records, the routine closes unit 107, exits the read block, and returns to its caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `salt_soil_ini, cs_db` | `salt_soil_ini(isalt)%soil, cs_db%num_salts, salt_soil_ini(isalt)%plt, salt_soil_ini(isalti)%name, salt_soil_ini(isalti)%soil, salt_soil_ini(isalti)%plt` |
| [sym:input_file_module] | `input_file_module` | `No candidate outside references were resolved to this module.` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%salt_ini` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%salt_ini` | When `salt_hru.ini` is present and the routine successfully scans the file | `db_mx%salt_ini` is updated to the number of salt HRU initialization records found in `salt_hru.ini`, which tells later readers how many `salt_soil_ini` entries were allocated and loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows the routine was introduced in `df07e3f`, later had allocation initialization changed in `f8bb6ec` and `39fabde`, and was then retained with the same file-reading flow in the later snapshots shown. The diffs specifically show initialization defaults for local scalars and zero-filled allocation of the salt plant array, not changes to the file parsing logic.

- df07e3f introduced `salt_hru_read` with the full scan/allocate/reread/load workflow for `salt_hru.ini`.
- f8bb6ec changed the `salt_soil_ini(isalt)%soil` allocation to use `source = 0.` so soil arrays start zeroed.
- 39fabde initialized local scalars (`titldum`, `header`, `isalt`, `isalti`, `eof`, `imax`) and also changed `salt_soil_ini(isalt)%plt` allocation to use `source = 0.`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_hru_read' has no extracted documentation comment.
- The extracted source uses `if (i_exist .or. 'salt_hru.ini' /= "null") then`; this is preserved as-is in the evidence and should be treated as source behavior rather than interpreted as a normal existence guard.
