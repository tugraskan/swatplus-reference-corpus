---
kind: procedure
symbol: salt_irr_read
title: salt_irr_read
status: filled
source_hash: 18193baaa5339922
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the file title line during the
    initial scan, then read it again after rewind before the data records are loaded.
  header: Scratch character buffer used to read and discard the file header line during the
    initial scan, then read it again after rewind before the data records are loaded.
  isalti: Loop index for each irrigation-source record in `salt_water_irr`; it is used both
    when allocating each source's `water` array and when reading the source name and values
    into the allocated array.
  eof: I/O status flag from `read(...,iostat=eof)` that controls scanning and early exit when
    the file ends or a read fails.
  imax: Record count for the number of irrigation-source entries found in `salt_irrigation`;
    it determines how many `salt_water_irr` elements are allocated and read.
  i_exist: Logical flag set by `inquire` to indicate whether `salt_irrigation` is present
    before attempting to read it.
uses:
  constituent_mass_module: '`constituent_mass_module` provides the shared salt database and
    irrigation-salt storage that this routine populates. `cs_db%num_salts` sets the length
    of each concentration vector, while `salt_water_irr(isalti)%name` and `salt_water_irr(isalti)%water`
    are the allocatable targets that receive the irrigation-source name and its per-salt concentrations.'
  input_file_module: '`input_file_module` is part of the model''s input-handling infrastructure
    and matters here because this routine is one of the file readers invoked during the global
    read phase. Even though no specific symbol from the module was resolved in the extracted
    snippet, the module is part of the routine''s declared dependencies and indicates this
    reader participates in the centralized input workflow.'
  maximum_data_module: '`maximum_data_module` matters because this reader sizes and allocates
    shared storage based on the contents of `salt_irrigation`. The module is declared as a
    dependency, so it is part of the broader sizing context used by model readers even though
    no concrete symbol from it was resolved in the extracted snippet.'
---

<!-- facts:header -->

Reads the `salt_irrigation` input file that defines salt concentrations in outside irrigation water. It counts the records, allocates `salt_water_irr`, then loads each irrigation source name and its salt-water concentration vector into shared model state.

## Bottom Line

`salt_irr_read` is a file reader for the `salt_irrigation` database used by SWAT+ salt routines. It first checks that the file exists, then scans past the title/header to count how many irrigation sources are defined, allocates `salt_water_irr(imax)`, and allocates each source's `water` array to match `cs_db%num_salts`.

It then rewinds the file and reads each irrigation source name plus its salt concentration values into `salt_water_irr(isalti)%name` and `salt_water_irr(isalti)%water`. The result is shared state that later salt-transport or irrigation routines can use when outside irrigation water contributes salts to the simulation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model's input-reading phase, after `proc_read` has started loading salt-related databases and before later simulation routines use irrigation-salt concentrations. `proc_read` calls it after other salt readers, so its output becomes part of the shared constituent database available to downstream irrigation and salt-transport calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the salt irrigation file exists | The routine announces that it is reading outside irrigation salt data, then uses `inquire(file="salt_irrigation", exist=i_exist)` to avoid attempting file reads when the input file is missing. |
| 2. Open the file and skip title/header lines | Inside the read loop, unit 107 is opened on `salt_irrigation`, then the routine reads and discards the title and header lines into `titldum` and `header`. Each read uses `iostat=eof` so the routine can stop cleanly on end-of-file or error. |
| 3. Count irrigation-source records | The routine resets `imax` to zero and reads one record at a time into `titldum` until `eof` changes. Each successful read increments `imax`, producing the number of irrigation-source entries to allocate. |
| 4. Allocate storage for all irrigation sources | Using the counted record total, the routine allocates `salt_water_irr(imax)` and then allocates each `salt_water_irr(isalti)%water` array to length `cs_db%num_salts`, initializing each water array to zero with `source = 0.`. |
| 5. Rewind and reread the file from the top | The routine rewinds unit 107 to the start of `salt_irrigation`, rereads the title and header lines, and prepares for the final data pass now that storage has been allocated. |
| 6. Load each irrigation-source name and salt vector | For each allocated irrigation-source slot, the routine reads the source name and its salt concentration vector into `salt_water_irr(isalti)%name` and `salt_water_irr(isalti)%water`. If a read fails, it exits early. |
| 7. Close the input file and return | After the records are loaded, the routine closes unit 107, leaves the loop, and returns control to the caller with `salt_water_irr` populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `salt_water_irr, cs_db` | `salt_water_irr(isalti)%water, cs_db%num_salts, salt_water_irr(isalti)%name` |
| [sym:input_file_module] | `input_file_module` | `input file state used by the model's reader workflow` |
| [sym:maximum_data_module] | `maximum_data_module` | `maximum data limits and related shared sizing state` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show that `salt_irr_read` was introduced in df07e3f as a new routine to read `salt_irrigation`, count records, allocate `salt_water_irr`, rewind, and load irrigation-source salt concentrations. f8bb6ec then changed the allocation of each `water` array to initialize it to zero with `source = 0.`. 39fabde initialized local variables (`titldum`, `header`, `isalt`, `isalti`, `eof`, `imax`) to default values and preserved the zero-initialized water allocation. 2ee1889 removed the unused `isalt` local; 35b029c and 94b6dec reflect earlier formatting/history updates without changing the routine's behavior shown in the diffs.

- df07e3f added the routine and its two-pass file-reading workflow for `salt_irrigation`, including allocation of `salt_water_irr` based on the number of data records.
- f8bb6ec changed the per-source `water` allocation to initialize values to zero on allocation.
- 39fabde initialized the local buffers and counters (`titldum`, `header`, `isalt`, `isalti`, `eof`, `imax`) to default values, reducing uninitialized-state risk.
- 2ee1889 removed the unused local variable `isalt`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_irr_read' has no extracted documentation comment.
- algorithm_steps revised: merged the initial title/header skip into the first read pass, split the rewind-and-reread pass from the final data load, and added the explicit close/return step to match the source flow.
- input_file_module and maximum_data_module are declared uses but no specific resolved symbols were extracted from them in the provided context; descriptions reflect that uncertainty rather than inventing symbols.
