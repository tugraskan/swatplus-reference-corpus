---
kind: procedure
symbol: cntbl_read
title: cntbl_read
status: filled
source_hash: 49b0c8ded7d64539
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for the title line and later header-skipping reads from
    `cntable.lum`. The routine uses it both during the counting pass and again after `rewind(107)`
    to skip the first file line before reading data records.
  header: Temporary character buffer for the second line of `cntable.lum`, treated as a header
    line and skipped before table data are counted and loaded.
  eof: I/O status flag for reads from unit 107. The routine checks `eof < 0` to stop on end-of-file
    and uses `eof == 0` to continue scanning data lines.
  imax: Counts how many curve-number records are found in `cntable.lum`. The routine increments
    it during the scan and uses it to allocate `cn(0:imax)` and to set `db_mx%cn_lu`.
  icno: Loop counter for the second pass that loads data records into `cn(icno)` after the
    file has been rewound.
  i_exist: Logical flag set by `inquire` to indicate whether the configured curve-number file
    exists. It controls whether the routine reads the file or falls back to allocating an
    empty table.
uses:
  input_file_module: This module supplies `in_lum%cntable_lum`, the configured file name for
    the curve-number table. `cntbl_read` uses that path to decide which file to inquire about,
    open, and read.
  maximum_data_module: This module holds `db_mx%cn_lu`, the shared record count for the curve-number
    table. `cntbl_read` updates it so later database and landuse logic know how many curve-number
    entries were loaded.
  landuse_data_module: This module owns the allocatable `cn` table that stores curve-number
    records. `cntbl_read` allocates and fills that array, so the rest of the landuse database
    can use the loaded table values.
---

<!-- facts:header -->

Reads the curve-number lookup table from `cntable.lum` into the landuse database. It sizes the `cn` array from the file contents and records the number of table entries in `db_mx%cn_lu`.

## Bottom Line

`cntbl_read` is a file-reader for the curve-number table used by land use data. It checks whether `in_lum%cntable_lum` exists and is not set to the literal string `null`, counts the table records, allocates `cn` to match, then reads each record into `landuse_data_module::cn`.

When the file is missing or disabled, it still allocates a minimal `cn(0:0)` array and leaves the record count at zero. In all cases it closes unit 107 and stores the final table size in `db_mx%cn_lu` for later model code.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cntbl_read` runs during database initialization, inside `proc_db`, after earlier database readers have prepared other landuse-related tables. Its results feed the shared landuse curve-number array and `db_mx%cn_lu`, which later landuse and management routines depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check file presence | The routine resets `eof` and `imax`, then uses `inquire` on `in_lum%cntable_lum` to determine whether the curve-number file exists and whether the configured path is the literal string `null`. |
| 2. Allocate an empty table when the file is unavailable | If the file does not exist or is disabled, the routine allocates `cn(0:0)` so the landuse curve-number table remains defined even though no records were read. |
| 3. Open the curve-number table for scanning | When the file is available, the routine opens unit 107 on `in_lum%cntable_lum` and reads the first title line into `titldum`. |
| 4. Skip the header and count data records | The routine reads the header line into `header`, then loops reading additional lines into `titldum` while `eof == 0`, incrementing `imax` for each data record encountered. |
| 5. Allocate the curve-number array to the discovered size | After counting finishes, the routine allocates `cn(0:imax)` so the array can hold the full set of curve-number records plus the zero index used by the module type. |
| 6. Rewind the file for a second pass | The routine rewinds unit 107 so it can reread the file from the beginning and load the actual curve-number values. |
| 7. Skip title and header again | After rewinding, the routine rereads the title line into `titldum` and the header line into `header`, again discarding both before loading data. |
| 8. Load each curve-number record | The routine loops `icno` from 1 to `imax` and reads each record into `cn(icno)`, stopping early if an end-of-file condition is detected. |
| 9. Exit the scan loop and store table size | After the data load completes, the routine exits the enclosing loop and writes the final record count `imax` to `db_mx%cn_lu`. |
| 10. Close the file and return | The routine closes unit 107 and returns to its caller after finishing the curve-number table load. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_lum` | `in_lum%cntable_lum` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cn_lu` |
| [sym:landuse_data_module] | `cn` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%cn_lu` | When `cntbl_read` finishes scanning `cntable.lum`, including the no-file path where `imax` remains 0. | `db_mx%cn_lu` is set to the number of curve-number records found in `cntable.lum`, or to zero when the file is missing or disabled, so later routines know the loaded table length. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows two behavior-relevant revisions for `cntbl_read`. The initial addition in `df07e3f` introduced the subroutine, its file scan/load logic, allocation of `cn`, and assignment to `db_mx%cn_lu`. Commit `39fabde` did not change the algorithm; it only initialized local variables `titldum`, `header`, `eof`, `imax`, and `icno` at declaration and retained the existing `eof = 0` reset.

- df07e3f introduced `cntbl_read` as a new database reader for `cntable.lum`, adding the two-pass count-then-load workflow, dynamic allocation of `cn`, and the `db_mx%cn_lu` summary value.
- 39fabde changed only local-variable initialization style by giving `titldum`, `header`, `eof`, `imax`, and `icno` default values; it did not alter file handling or record-loading behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cntbl_read' has no extracted documentation comment.
