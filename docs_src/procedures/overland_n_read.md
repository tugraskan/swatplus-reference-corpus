---
kind: procedure
symbol: overland_n_read
title: overland_n_read
status: filled
source_hash: 9909dc8f4106c475
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and skip the file title line and then the
    same title again during the second pass through `ovn_table.lum`.
  header: Scratch character buffer used to read and skip the file header line on both the
    counting pass and the data-loading pass.
  eof: I/O status flag for `read` statements; it is tested for end-of-file or other read termination
    while scanning and loading `ovn_table.lum`.
  imax: Counts how many overland-n table records are present in the file so the routine can
    size `overland_n` and later store the total in `db_mx%ovn`.
  i_exist: Logical flag set by `inquire` to tell the routine whether the configured overland-n
    file actually exists before attempting to open it.
  il: Loop counter used to read each overland-n table record into `overland_n(il)` after the
    array has been allocated.
uses:
  input_file_module: This module provides `in_lum%ovn_lum`, the configured path to the overland-n
    lookup file that the routine must check, open, and read.
  maximum_data_module: This module provides `db_mx%ovn`, the shared maximum-element counter
    that the routine updates after counting the file records so other database readers and
    later logic can know how many overland-n entries were loaded.
  landuse_data_module: This module owns the allocatable `overland_n` table that receives the
    parsed records; the routine allocates and fills that shared landuse database array.
---

<!-- facts:header -->

Reads the overland-flow Manning's n lookup table from `ovn_table.lum` into `landuse_data_module` and records how many entries it found. It is a small database loader called during `proc_db` before landuse-related setup continues.

## Bottom Line

`overland_n_read` opens the configured overland-flow n table file, counts the data rows, allocates the `overland_n` array to match, then rewinds and reads each table record into `landuse_data_module`. If the file is missing or the configured name is `"null"`, it still creates a one-element placeholder array and leaves the count at zero.

The routine also stores the number of loaded overland-n records in `db_mx%ovn`, which gives later model code a quick maximum-count summary for this database table.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in `proc_db` during database initialization, after other lookup tables such as `cntbl_read` and `cons_prac_read` have been handled and before `landuse_read`. Its result is the populated `overland_n` table and `db_mx%ovn`, which later landuse-related model code can rely on when referencing overland-flow Manning's n values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check for a usable file name | The routine starts with blank title/header buffers and zeroed counters, then uses `inquire` on `in_lum%ovn_lum` to see whether the configured file exists. If the file is missing or the name is `"null"`, it takes the no-file path instead of attempting normal reads. |
| 2. Create a placeholder array when no file is available | If the overland-n file is unavailable, the routine allocates `overland_n(0:0)` so the shared array exists even though no table records were loaded. |
| 3. Open the overland-n table and skip title/header records | When the file is usable, the routine opens unit 108 on `in_lum%ovn_lum`, reads the title line into `titldum`, and reads the header line into `header`. Those records are skipped so the following loop can count data lines. |
| 4. Count the data rows in the file | The routine loops through the remaining records, reading each line into `titldum` and incrementing `imax` until end-of-file is reached. This produces the number of overland-n entries in the file. |
| 5. Allocate the overland-n table to the counted size | After counting, the routine allocates `overland_n(0:imax)` so the shared landuse table has room for the indexed records plus the zero element used by the module convention. |
| 6. Rewind the file and reread the title/header | The routine rewinds unit 108 back to the start of `ovn_table.lum`, then rereads and skips the title and header so it can make a clean second pass over the data records. |
| 7. Load each overland-n record into shared state | A loop over `il = 1, imax` reads each table entry from `ovn_table.lum` into `overland_n(il)`, filling the allocated landuse database array. |
| 8. Stop the outer loop after one successful pass | The surrounding `do` block exits after the file is counted, allocated, and loaded once; it is not intended to repeat the open/read sequence multiple times. |
| 9. Publish the record count and close the file | The routine stores the final count in `db_mx%ovn`, closes unit 108 for `ovn_table.lum`, and returns to the caller with the table and summary count set. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_lum` | `in_lum%ovn_lum` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ovn` |
| [sym:landuse_data_module] | `overland_n` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ovn` | After the file scan completes, whether the file was missing or successfully read. | `db_mx%ovn` is assigned the final `imax` count so the shared maximum-data state records how many overland-flow n rows were present in `ovn_table.lum`; if the file was missing or disabled, this remains zero. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `overland_n_read`. The initial addition in df07e3f introduced the full reader: file existence check, opening `ovn_table.lum`, counting rows, allocating `overland_n`, rewinding, loading records, and storing `db_mx%ovn`. Commit 39fabde made only initialization/formatting changes in this file, setting `titldum`, `header`, `eof`, `imax`, and `il` to explicit initial values and leaving the read logic unchanged.

- df07e3f added the overland-n table reader and its `db_mx%ovn` summary count.
- 39fabde initialized the local scratch variables and counters without changing the file-reading algorithm.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'overland_n_read' has no extracted documentation comment.
