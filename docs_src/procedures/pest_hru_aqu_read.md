---
kind: procedure
symbol: pest_hru_aqu_read
title: pest_hru_aqu_read
status: filled
source_hash: 365b7109efb7acd5
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard title or label lines, and to
    hold the text token before each soil/plant concentration row.
  header: Scratch character buffer used to read and discard the section header line during
    the file scan and again after rewinding.
  eof: I/O status flag for the reads; it controls loop exit when end-of-file or an input error
    is reached.
  imax: Counter for how many pesticide initial-condition blocks were found in `pest_hru.ini`;
    it becomes the allocation size and the value stored in `db_mx%pest_ini`.
  ipest: Inner loop index over pesticide species when scanning or filling each block's soil
    and plant arrays.
  ipesti: Outer loop index over initial-condition blocks in `pest_soil_ini` when the file
    is reread into memory.
  i_exist: Logical flag set by `inquire` to indicate whether the configured `pest_soil` file
    is present before attempting to read it.
uses:
  constituent_mass_module: This module owns the pesticide database count and the `pest_soil_ini`
    derived-type array that this routine sizes and fills. `cs_db%num_pests` tells the routine
    how many pesticide columns to read per block, and the `pest_soil_ini` components receive
    the name, soil, and plant starting concentrations from the file.
  input_file_module: This module provides the configured filename `in_init%pest_soil`, which
    determines which input file the routine opens and reads. Without it, the routine would
    not know where to find the pesticide initial-condition data.
  maximum_data_module: This module holds `db_mx%pest_ini`, the shared count of pesticide initial-condition
    records. The routine sets it after scanning the file so later code can know how many `pest_soil_ini`
    entries were loaded.
---

<!-- facts:header -->

Reads the pesticide HRU/aquatic initial-condition file and loads pesticide soil and plant concentrations into shared database arrays.

## Bottom Line

pest_hru_aqu_read opens the configured `pest_hru.ini` initial-condition file, counts how many HRU/aquatic pesticide entries it contains, allocates storage for those entries, and then reads each pesticide name plus its soil and plant starting concentrations into `pest_soil_ini`.

This routine matters because later pesticide initialization and transport logic needs the loaded `pest_soil_ini` values and the record count stored in `db_mx%pest_ini` to know how many initial-condition blocks exist.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the main initialization read sequence, immediately after other constituent and soil/plant setup in `proc_read`. It depends on `proc_read` having already prepared the shared input-file settings and pesticide database sizes, and its results feed later pesticide HRU/aquatic initialization by populating `pest_soil_ini` and `db_mx%pest_ini`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether a pesticide initial-condition file should be read | The routine uses `inquire` on `in_init%pest_soil` and only enters the read logic when the file exists or the configured name is not the literal string `null`. |
| 2. Open the configured file and skip the leading title line | Unit 107 is opened on `in_init%pest_soil`, then the first record is read into `titldum`; if that read reaches end-of-file, the routine exits the wrapper loop. |
| 3. Scan blocks to count how many pesticide initial-condition records are present | The routine loops through the file structure, reading `header`, a block name token, and `cs_db%num_pests` data rows per block until end-of-file, incrementing `imax` for each complete block found. |
| 4. Save the block count in shared maximum-data state | The counted number of blocks is copied into `db_mx%pest_ini` so other routines can know how many pesticide initial-condition entries were loaded. |
| 5. Allocate the pesticide initial-condition array and its per-block concentration vectors | The routine allocates `pest_soil_ini(imax)` and, for each block, allocates zero-initialized `soil` and `plt` arrays sized to `cs_db%num_pests`. |
| 6. Rewind the file to reread it from the beginning | After allocation, the routine rewinds unit 107 and rereads the title and header lines so the actual data pass starts from the top of the file. |
| 7. Load each pesticide block into shared state | For each block, the routine reads the pesticide name and then reads `cs_db%num_pests` soil and plant values into the corresponding `pest_soil_ini(ipesti)` arrays. |
| 8. Close the file and finish | The file is closed, the wrapper loop is exited, and the subroutine returns to its caller with the shared pesticide initial-condition state populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_db, pest_soil_ini` | `cs_db%num_pests, pest_soil_ini(ipest)%soil, pest_soil_ini(ipest)%plt, pest_soil_ini(ipesti)%name, pest_soil_ini(ipesti)%soil(ipest), pest_soil_ini(ipesti)%plt(ipest)` |
| [sym:input_file_module] | `in_init` | `in_init%pest_soil` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pest_ini` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%pest_ini` | After the scan loop completes a full pass through `pest_hru.ini` and before allocation begins. | `db_mx%pest_ini` is set to the number of pesticide initial-condition blocks found in the file. That count becomes the shared size indicator for later code that allocates or iterates through pesticide initial-condition records. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was added in commit df07e3f as a new reader for pesticide HRU initial-condition data. Commit 94b6dec later initialized the local scratch variables (`titldum`, `header`, `eof`, `imax`, `ipest`, and `ipesti`) and zero-initialized `pest_soil_ini(ipest)%plt` allocations. Commit f8bb6ec had already changed the `pest_soil_ini(ipest)%soil` allocation to use `source = 0.`, and commit 39fabde preserved that soil initialization while adding the same zero-initialization for `plt` allocations and the local variable initial values.

- df07e3f introduced the new `pest_hru_aqu_read` subroutine, including the scan-allocate-reread pattern and the assignment to `db_mx%pest_ini`.
- f8bb6ec changed the soil allocation to initialize `pest_soil_ini(ipest)%soil` with zeros.
- 39fabde initialized the local scratch variables and changed `pest_soil_ini(ipest)%plt` allocation to zero-initialize the plant array.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'pest_hru_aqu_read' has no extracted documentation comment.
