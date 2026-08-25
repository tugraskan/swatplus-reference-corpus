---
kind: procedure
symbol: res_read_sed
title: res_read_sed
status: filled
source_hash: 537b034540f4674c
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary line buffer used to read and skip title or placeholder records from `sediment.res`
    during both the counting pass and the data-loading pass.
  header: Temporary line buffer used to read the file header line from `sediment.res` before
    the routine scans or loads the data records.
  eof: I/O status flag from each `read` call; `0` means a successful read, and a negative
    value ends the scan or load when the file is exhausted.
  imax: Counts how many reservoir sediment data records are present in `sediment.res`; this
    becomes the allocation size and is copied to `db_mx%res_sed`.
  i_exist: Logical flag from `inquire` indicating whether the configured sediment input file
    exists on disk, so the routine can fall back to an empty allocation when the file is missing.
  ires: Loop counter used on the second pass to read each reservoir sediment record into `res_sed(ires)`
    after the array has been allocated.
uses:
  input_file_module: '`input_file_module` supplies `in_res%sed_res`, the configured path to
    the reservoir sediment input file. This path decides which file is opened and whether
    the routine treats the input as present or disabled.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%res_sed`, the shared count of
    reservoir sediment records discovered in the file. That count is used by other model code
    to know how many reservoir sediment entries were loaded.'
  reservoir_data_module: '`reservoir_data_module` owns the allocatable `res_sed` array that
    receives the parsed sediment records. The routine must allocate and populate that shared
    state so later reservoir procedures can use the sediment parameters.'
---

<!-- facts:header -->

Reads the reservoir sediment input file and loads one sediment-data record per reservoir into shared model state. It first counts how many records are present, then allocates and fills `res_sed` for later reservoir initialization and routing use.

## Bottom Line

`res_read_sed` is a file-loading routine for reservoir sediment settings. It looks up the configured sediment input file, checks that the file exists and is not set to `null`, then scans it to count data records before allocating storage and reading the records into the `reservoir_data_module` array `res_sed`.

This matters because reservoir processing in `proc_res` depends on `res_sed` being sized and populated before later reservoir readers and initializers run. The routine also stores the record count in `db_mx%res_sed`, giving the model a shared count of how many reservoir sediment entries were found in the input file.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir setup in `proc_res`, immediately after `res_read_hyd` and before the other reservoir readers. It depends on `in_res%sed_res` having been set to the correct file name and on `reservoir_data_module` being available for allocation; its results feed later reservoir initialization and any model behavior that uses the loaded sediment properties and the `db_mx%res_sed` count.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the sediment file is available | The routine tests `in_res%sed_res` with `inquire` and checks for the special value `"null"`. If the file is missing or disabled, it allocates `res_sed(0:0)` and skips the file-reading path. |
| 2. Open the file and count usable records | When the file is present, the routine opens unit 105 on `in_res%sed_res`, reads past the title and header lines, and loops through the remaining records to count how many sediment entries are present by incrementing `imax`. |
| 3. Save the record count and allocate storage | After counting, the routine copies `imax` into `db_mx%res_sed` and allocates `res_sed(0:imax)` so there is shared storage for every reservoir sediment record found in the file. |
| 4. Rewind and reread the file from the top | The routine rewinds unit 105, rereads the title and header lines, and resets the file position so it can perform the actual data load in record order. |
| 5. Load each sediment record into shared state | For each record index from 1 to `imax`, the routine reads a line, backs up one record, and then reads the full derived-type record into `res_sed(ires)`. This fills the shared reservoir sediment array with the parsed data. |
| 6. Close the file | The routine closes unit 105 after the load is complete, ending access to `sediment.res`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_res` | `in_res%sed_res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_sed` |
| [sym:reservoir_data_module] | `res_sed` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%res_sed` | When `in_res%sed_res` exists and is not `"null"`, after the first scan of the file completes. | `db_mx%res_sed` is set to the number of reservoir sediment records found in `sediment.res`. This gives the rest of the reservoir workflow a shared count of how many records were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved history shows three changes to `res_read_sed`. The initial addition in `df07e3f` introduced the routine and its file-counting/reading logic. Commit `94b6dec` brought the file into the lineage snapshot without changing the shown algorithm. Commit `39fabde` initialized the local variables (`titldum`, `header`, `eof`, `imax`, `ires`) and `889136d` only corrected a comment typo in the purpose block.

- df07e3f added the complete `res_read_sed` subroutine, including the existence check, record counting, allocation of `res_sed`, reread with `rewind`, and record-by-record loading into shared state.
- 39fabde changed local variable initialization by assigning default values to `titldum`, `header`, `eof`, `imax`, and `ires`, reducing dependence on later explicit resets.
- 889136d changed only documentation text in the purpose comment; the executable behavior shown in the diff did not change.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_sed' has no extracted documentation comment.
