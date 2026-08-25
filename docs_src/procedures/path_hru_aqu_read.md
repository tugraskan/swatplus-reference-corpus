---
kind: procedure
symbol: path_hru_aqu_read
title: path_hru_aqu_read
status: filled
source_hash: ca79ad60a7d6c280
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to consume title, label, and data tokens from `path_hru.ini`;
    it is read repeatedly when the file format has a leading text field that is not stored.
  header: Scratch string used to read each record header line during the scan and load passes;
    the routine uses it to step through the file format without keeping the header text.
  ipath: Loop index used while scanning records and while allocating per-record arrays; it
    counts through pathogen-path entries or component counts within a record.
  ipathi: Loop index for the second pass that fills `path_soil_ini`; it selects which record
    in the allocated array is being populated.
  eof: I/O status flag from each `read`; negative values terminate on end-of-file, zero keeps
    the loops scanning or loading, and positive errors are not handled specially here.
  imax: Counter for the number of pathogen-path records found in the input file; it becomes
    the size used for `path_soil_ini` and is copied to `db_mx%path_ini`.
  i_exist: Logical flag from `inquire` that tells the routine whether the configured file
    exists; it gates whether the routine attempts to open and parse the input file.
uses:
  constituent_mass_module: '`constituent_mass_module` provides both the record count source
    `cs_db%num_paths` and the target database `path_soil_ini`. The count controls how many
    per-record values are read from each file entry, and the target arrays hold the pathogen
    names plus their soil and plant initial concentrations for later model use.'
  input_file_module: '`input_file_module` supplies `in_init%path_soil`, the configured file
    name for this initializer. Without that setting, the routine would not know which input
    file to scan and load.'
  maximum_data_module: '`maximum_data_module` owns `db_mx%path_ini`, the shared counter for
    how many pathogen initial-condition records were found. Other setup code can use that
    count to size loops and validate whether pathogen-path data were loaded.'
---

<!-- facts:header -->

Reads the pathogen HRU/AQU initial-path file, counts how many pathogen path records it contains, allocates storage, and loads the soil/plant initial-condition arrays into shared module state.

## Bottom Line

`path_hru_aqu_read` loads the pathogen initial-condition database from `in_init%path_soil` (the `path_hru.ini` input file). It first scans the file to count records, stores that count in `db_mx%path_ini`, allocates `path_soil_ini` and its `soil`/`plt` arrays, then rewinds and reads each pathogen entry into memory.

The data it reads are not local-only: the routine populates shared module state in `constituent_mass_module` so later simulation setup can look up pathogen names and their initial soil and plant concentrations by record index.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during global read/setup, after `proc_read` has already initialized the core database and before later initial-condition readers continue. Its results matter because it defines how many pathogen-path initial-condition records exist and fills the shared arrays that later initialization and simulation logic use when pathogens are mapped to soil and plant starting concentrations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the configured pathogen-path file is available | The routine inquires on `in_init%path_soil` and only enters the read logic if the file exists or the configured name is not the sentinel string `null`. |
| 2. Open the input file and scan the first title field | Unit 107 is opened on `in_init%path_soil`, the first token is read into `titldum`, and the record counter `imax` is reset before counting begins. |
| 3. Count complete record groups in the file | The loop reads each record header, a record name token, and `cs_db%num_paths` additional tokens per entry; each successful pass increments `imax` until end-of-file is reached. |
| 4. Save the record count and allocate storage | The routine stores the discovered count in `db_mx%path_ini`, allocates `path_soil_ini(imax)`, allocates `cs_path_solsor(cs_db%num_paths)`, and sizes each record's `soil` and `plt` arrays to the number of pathogen paths. |
| 5. Rewind the file for a second pass | `rewind(107)` resets `path_hru.ini` to the beginning and the title token is read again so the file can be parsed from the top into the newly allocated arrays. |
| 6. Load each pathogen-path record into shared arrays | For each record, the routine reads the header, the path name, and the soil and plant concentration values into `path_soil_ini(ipathi)%name`, `%soil`, and `%plt`. |
| 7. Close the file and return | After all records are loaded, unit 107 is closed, the file-processing loop exits, and the subroutine returns to its caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_db, path_soil_ini` | `cs_db%num_paths, path_soil_ini(ipath)%soil, path_soil_ini(ipath)%plt, path_soil_ini(ipathi)%name, path_soil_ini(ipathi)%soil, path_soil_ini(ipathi)%plt` |
| [sym:input_file_module] | `in_init` | `in_init%path_soil` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%path_ini` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%path_ini` | When `path_hru.ini` is available and the scan pass counts at least one complete record group, `db_mx%path_ini` is assigned `imax`. | This stores the number of pathogen initial-condition records discovered in the file so later setup code can size and traverse the loaded `path_soil_ini` array consistently. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved for `path_hru_aqu_read`. The initial addition in `df07e3f` introduced the subroutine and its two-pass file scan/load logic. `16e54aa` changed the load pass to read `soil` and `plt` together from one record line instead of two separate reads. `39fabde` initialized the local variables and changed the `plt` allocation to zero-fill the array on allocation.

- `df07e3f` added the routine with file inquiry, scan, allocation, rewind, load, and close behavior for `path_hru.ini`.
- `16e54aa` reduced the number of reads during the load pass by combining `soil` and `plt` into one `read` statement, changing the input record format handling.
- `39fabde` made the local counters and scratch strings start from defined values and zero-initialized each `plt` array when allocating it.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'path_hru_aqu_read' has no extracted documentation comment.
