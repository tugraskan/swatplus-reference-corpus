---
kind: procedure
symbol: soil_lte_db_read
title: soil_lte_db_read
status: filled
source_hash: a12f1c3410b598db
version_label: SWAT+ 62.0.0
locals:
  titldum: Holds the first header/title line read from `soils_lte.sol`; the routine reads
    it and discards it before reading the next header line.
  header: Holds the second header line from `soils_lte.sol`; it is read and discarded before
    the 12 soil records are loaded.
  eof: Captures the `iostat` status from each read so the routine can detect end-of-file or
    read failure and stop the loop.
  k: Loop counter for the 12 LTE soil database records read from the file.
  i_exist: Logical flag set by `inquire` to tell the routine whether the configured LTE soil
    file actually exists on disk.
uses:
  input_file_module: '`input_file_module` supplies `in_sol%lte_sol`, the configured path for
    the LTE soil input file. That path controls which file is opened and also whether the
    routine treats the input as disabled when the name is `null`.'
  maximum_data_module: '`maximum_data_module` is imported by this routine, but the extracted
    context does not resolve any direct symbols from it. The module matters because the procedure
    is compiled in the same input-loading context as the model''s maximum-size definitions,
    which may govern database sizing or related shared limits even though no specific reference
    was extracted here.'
  hru_lte_module: '`hru_lte_module` is imported by this routine, but the extracted context
    does not resolve any direct symbols from it. The module matters because this loader runs
    in the LTE-HRU input setup phase, so any LTE-specific shared state in that module can
    depend on the soil database being populated first.'
  soil_data_module: '`soil_data_module` provides the allocatable shared array `soil_lte`,
    which is the data structure this routine creates and fills from the input file. Without
    that module, the read loop would have nowhere to store the LTE soil database records.'
---

<!-- facts:header -->

Reads the LTE soils database file and loads its 12 records into the shared `soil_lte` array. If the file is missing or disabled, it creates a one-element placeholder array instead.

## Bottom Line

This routine initializes the shared LTE soil database from the file named in `in_sol%lte_sol`, which defaults to `soils_lte.sol`. It first checks whether the file exists and is not set to `null`, then either allocates a dummy `soil_lte(0:0)` array or opens the file and reads the database records into `soil_lte`.

The result matters because later code expects the `soil_lte` allocatable array from `soil_data_module` to exist before LTE soil properties are used elsewhere in the model. `proc_read` calls this routine as part of the broader input-file loading sequence.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the centralized read phase, after `proc_read` has already started loading other model input tables and just before the remaining initialization work can rely on the LTE soil database. Its output is the shared `soil_lte` array, which later LTE-related model code uses to access soil database properties.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check the configured LTE soil file | The routine tests whether `in_sol%lte_sol` exists on disk and whether the configured name is not the literal string `null`. If either condition fails, it allocates a one-element placeholder array `soil_lte(0:0)` instead of trying to read file data. |
| 2. Open the LTE soil database file | When the file is valid, the routine enters a read loop and opens unit 107 on `in_sol%lte_sol`, which is the LTE soils database file. |
| 3. Skip the title line | It reads the first line into `titldum` and exits if the read fails or reaches end-of-file, effectively skipping the file title line. |
| 4. Skip the header line | It reads the next line into `header` and exits on read failure or end-of-file, skipping the header row before data records. |
| 5. Allocate LTE soil storage | The routine allocates the shared `soil_lte` array with 12 elements so it can hold the fixed set of LTE soil database records. |
| 6. Read the 12 soil records | A loop runs `k` from 1 to 12 and reads each record from unit 107 into `soil_lte(k)`, stopping early if a read error or end-of-file is encountered. |
| 7. Close the file | After the read loop finishes, the routine closes unit 107 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_sol` | `in_sol%lte_sol` |
| [sym:maximum_data_module] | `soil_lte` | `soil_lte(0:0), soil_lte(12), soil_lte(k)` |
| [sym:hru_lte_module] | `soil_lte` | `soil_lte(0:0), soil_lte(12), soil_lte(k)` |
| [sym:soil_data_module] | `soil_lte` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved history shows three commits touching this routine. The initial addition in df07e3f introduced `soil_lte_db_read` with file existence checking, header skipping, allocation of `soil_lte(12)`, and the 12-record read loop. The later 94b6dec change kept the same logic but adjusted the file to the newer source snapshot. The 39fabde commit only initialized the local variables `titldum`, `header`, `eof`, and `k` to default values.

- df07e3f established the routine and its current read pattern: check `in_sol%lte_sol`, allocate `soil_lte`, read 12 records, and close the file.
- 39fabde changed only local initialization for `titldum`, `header`, `eof`, and `k`; no file-processing logic changed in the diff shown.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'soil_lte_db_read' has no extracted documentation comment.
