---
kind: procedure
symbol: cons_prac_read
title: cons_prac_read
status: filled
source_hash: cfaeca777441382a
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch title/string buffer used to read and discard the file title line during
    the file scan and again after rewinding before the data records are loaded.
  header: Scratch string buffer used to read and discard the file header line so the routine
    can position itself at the first data record.
  i_exist: Logical flag set by `inquire` to show whether the configured `cons_practice.lum`
    file is present before trying to read it.
  eof: I/O status code from each `read` call; values below zero indicate end-of-file or a
    failed read, and zero means reads can continue.
  imax: Counts how many conservation-practice data records are found in `cons_practice.lum`;
    that count is later used to allocate `cons_prac` and store `db_mx%cons_prac`.
  icp: Loop counter used to read each conservation-practice record into `cons_prac(icp)` after
    the table has been allocated.
uses:
  input_file_module: This module provides `in_lum%cons_prac_lum`, the configured file name
    for the conservation-practice table. The routine uses that path to decide which file to
    open and whether the table is effectively disabled by the sentinel value `"null"`.
  maximum_data_module: This module holds `db_mx%cons_prac`, the shared maximum/record-count
    field for the conservation-practice table. `cons_prac_read` updates it so later database
    and landuse setup can know how many records were loaded.
  landuse_data_module: This module owns the allocatable `cons_prac` table that receives the
    parsed conservation-practice records. The routine fills that shared array so other landuse
    code can look up loaded practice data by record index.
---

<!-- facts:header -->

Reads the conservation-practice lookup table from `cons_practice.lum` into the landuse database. It counts the records, allocates `cons_prac`, loads each table entry, and stores the record count for later model setup.

## Bottom Line

`cons_prac_read` is a database-reader subroutine for conservation practice data. It checks whether the configured file `cons_practice.lum` exists and is enabled, then loads the file into the allocatable `landuse_data_module::cons_prac` table.

The routine first scans the file to count data records, allocates `cons_prac(0:imax)`, rewinds the file, reads each record into `cons_prac(icp)`, and saves the final count in `db_mx%cons_prac`. That count tells later landuse/database routines how many conservation-practice records are available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization, when `proc_db` is loading landuse-related lookup tables. `proc_db` prepares the shared module state and then calls `cons_prac_read` before later routines such as `overland_n_read` and `landuse_read`, which depend on the conservation-practice table and its record count.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and probe the file path | The routine resets the record counter state and uses `inquire` on `in_lum%cons_prac_lum` to determine whether the conservation-practice file exists. If the file is missing or the configured name is the sentinel string `"null"`, the routine takes the empty-table path. |
| 2. Allocate an empty table when no file is available | If the file is unavailable or disabled, the routine allocates `cons_prac(0:0)` so the shared table exists even though it contains no usable records. |
| 3. Open the conservation-practice file | When the file is available, the routine enters a read loop and opens `cons_practice.lum` on unit 107 to begin scanning its contents. |
| 4. Skip title and header lines | The routine reads a title record into `titldum` and a header record into `header`, exiting early if either read reaches end-of-file. |
| 5. Count data records | The routine continues reading scratch text records until the file ends, incrementing `imax` once for each data line encountered during the counting pass. |
| 6. Allocate the shared table to the counted size | After the count is known, the routine allocates `cons_prac(0:imax)` so the shared conservation-practice table has enough storage for all records. |
| 7. Rewind and skip the file prologue again | The routine rewinds unit 107 back to the beginning, then rereads the title and header lines so the file is positioned at the first data record for the load pass. |
| 8. Load each record into shared state | The routine loops from 1 through `imax`, reading each conservation-practice record into `cons_prac(icp)` and stopping early if a read fails or reaches end-of-file. |
| 9. Save the record count and close the file | The routine exits the scan loop, stores the final count in `db_mx%cons_prac`, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_lum` | `in_lum%cons_prac_lum` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cons_prac` |
| [sym:landuse_data_module] | `cons_prac` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%cons_prac` | After the file scan completes, `db_mx%cons_prac` is assigned the final value of `imax`. | `db_mx%cons_prac` changes to record how many conservation-practice entries were found in `cons_practice.lum`. That shared count is needed so later database and landuse routines know the table size that was loaded. |

## File I/O

<!-- facts:io -->


## Lineage

`cons_prac_read` was introduced in df07e3f as a new subroutine that scans `cons_practice.lum`, allocates `cons_prac`, and stores the record count in `db_mx%cons_prac`. Commit c7c8e22 preserved that logic when the source was imported from Bitbucket. Commit 39fabde only initialized local variables (`titldum`, `header`, `eof`, `imax`, `icp`) and did not change the read algorithm.

- df07e3f added the full `cons_prac_read` implementation: file existence check, two-pass read of `cons_practice.lum`, allocation of `cons_prac`, and update of `db_mx%cons_prac`.
- 39fabde changed only local variable initialization in `cons_prac_read`, setting `titldum`, `header`, `eof`, `imax`, and `icp` to initial values without altering the file-reading flow.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cons_prac_read' has no extracted documentation comment.
