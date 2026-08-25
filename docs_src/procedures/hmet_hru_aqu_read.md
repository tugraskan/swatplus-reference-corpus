---
kind: procedure
symbol: hmet_hru_aqu_read
title: hmet_hru_aqu_read
status: filled
source_hash: 0501a835f2fccbe8
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to consume title lines, blank markers, and the label
    fields that accompany each numeric record in `hmet_hru.ini`.
  header: Scratch character buffer used to read each section header while scanning and then
    again while loading each heavy-metals record.
  ihmet: Loop index over heavy-metals species within a record; also used while allocating
    and reading species-sized concentration arrays.
  ihmeti: Loop index over heavy-metals initial-condition entries in `hmet_soil_ini`.
  eof: I/O status flag from `read` statements; controls when the scan or load loop exits on
    end-of-file or read failure.
  imax: Counter for how many heavy-metals initial-condition entries were found during the
    first scan of the file.
  i_exist: Logical flag set by `inquire` to indicate whether the configured heavy-metals input
    file is present.
  ipest: Loop index over the metals/species slots when reading each entry's soil and plant
    concentration values.
uses:
  constituent_mass_module: This module supplies the heavy-metals database count `cs_db%num_metals`
    that determines how many concentration values to read and allocate per record, and it
    owns `hmet_soil_ini`, the shared array this routine populates with each entry's name plus
    soil and plant initial concentrations.
  input_file_module: This module provides `in_init%hmet_soil`, the configured filename that
    tells the routine which initial-condition file to open and parse.
  maximum_data_module: This module holds `db_mx%hmet_ini`, the shared counter updated here
    after the file is scanned so later code knows how many heavy-metals initial-condition
    records were loaded.
---

<!-- facts:header -->

Reads the heavy-metals initial-condition file `hmet_hru.ini` and loads soil and plant concentrations into shared SWAT+ state. It first counts the records to size storage, then rewinds and fills `hmet_soil_ini` for later model use.

## Bottom Line

This routine is the heavy-metals initial-condition reader for HRU/Aquatic setup. It opens the file named by `in_init%hmet_soil`, scans through the file once to count how many heavy-metals entries it contains, stores that count in `db_mx%hmet_ini`, and allocates `hmet_soil_ini` plus the per-entry soil/plant concentration arrays sized by `cs_db%num_metals`.

It then rewinds the file and reads each entry's name and the soil/plant concentration values into `hmet_soil_ini(ihmeti)%name`, `%soil(ihmet)`, and `%plt(ihmet)`. These shared arrays provide the initialized heavy-metals concentrations used later by the model after `proc_read` has finished loading all initial-condition databases.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `proc_read`, after the core constituent and other initial-condition readers have been called and before later setup routines such as the salt readers. Its results matter wherever the model needs the heavy-metals initial concentrations and the record count in `db_mx%hmet_ini` to drive later allocation and initialization logic.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check file presence and configuration | The routine inquires whether the configured heavy-metals input file exists and also allows processing when the file name is not the literal string "null". If neither condition is satisfied, it skips the read logic. |
| 2. Open the heavy-metals initial-condition file | It opens unit 107 on `in_init%hmet_soil` and reads the first record into a scratch title buffer to position the file for scanning. |
| 3. Count available records | The routine initializes `imax` to zero and scans through the file record by record, reading headers, names, and `cs_db%num_metals` species records until end-of-file, incrementing `imax` once per heavy-metals entry found. |
| 4. Publish count and allocate storage | It stores the record count in `db_mx%hmet_ini`, allocates `hmet_soil_ini(imax)`, allocates the shared `cs_hmet_solsor` array sized by `cs_db%num_metals`, and allocates each entry's `soil` and `plt` arrays with zero initialization. |
| 5. Rewind for data loading | The file is rewound and the first line is read again so the second pass starts from the beginning of `hmet_hru.ini`. |
| 6. Read each entry's name and concentrations | For each initial-condition entry, the routine reads the header, loads the constituent name, then loops over `cs_db%num_metals` to read soil and plant concentration values into `hmet_soil_ini(ihmeti)%soil(ihmet)` and `%plt(ihmet)`. |
| 7. Close file and finish | After all records are loaded, it closes unit 107, exits the wrapping loop, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_db, hmet_soil_ini` | `cs_db%num_metals, hmet_soil_ini(ihmet)%soil, hmet_soil_ini(ihmet)%plt, hmet_soil_ini(ihmeti)%name, hmet_soil_ini(ihmeti)%soil(ihmet), hmet_soil_ini(ihmeti)%plt(ihmet)` |
| [sym:input_file_module] | `in_init` | `in_init%hmet_soil` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%hmet_ini` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%hmet_ini` | When the configured file exists or `in_init%hmet_soil` is not "null", after the first full scan completes. | `db_mx%hmet_ini` is updated to the number of heavy-metals initial-condition entries found in `hmet_hru.ini`, so later code knows how many entries were loaded and how much storage was allocated. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows the procedure was added in df07e3f with the initial file-scan, allocation, rewind, and record-loading logic already present. f8bb6ec changed allocation of `hmet_soil_ini(ihmet)%soil` to use zero initialization, and 39fabde also zero-initialized `titldum`, `header`, `ihmet`, `ihmeti`, `eof`, `imax`, `ipest`, and `hmet_soil_ini(ihmet)%plt`.

- f8bb6ec changed the soil-array allocation to `allocate (..., source = 0.)`, ensuring the per-entry soil concentrations start at zero instead of undefined values.
- 39fabde initialized the local scratch variables and also changed the plant-array allocation to `allocate (..., source = 0.)`, reducing the risk of stale values during file scanning and load.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hmet_hru_aqu_read' has no extracted documentation comment.
