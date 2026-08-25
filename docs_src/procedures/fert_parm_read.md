---
kind: procedure
symbol: fert_parm_read
title: fert_parm_read
status: filled
source_hash: 77caacf535a3c4b9
version_label: SWAT+ 62.0.0
locals:
  it: '`it` is the loop counter used when rereading fertilizer records into `fertdb(it)` after
    the file has been counted and the array has been allocated.'
  titldum: '`titldum` is a throwaway character buffer used to read and skip the file''s title
    line and later to advance through records during the counting pass.'
  header: '`header` holds the header line from `fertilizer.frt` so the routine can skip the
    non-data header section before counting and loading records.'
  eof: '`eof` captures the `iostat` status from each `read` and is used as the end-of-file
    / error signal that controls the scan loops and exits.'
  imax: '`imax` counts how many fertilizer data records were found in the file and is then
    used as the upper bound for allocating `fertdb` and for the reread loop.'
  mfrt: '`mfrt` is initialized but not used in the extracted source; it appears to be a leftover
    counter placeholder for fertilizer records.'
  i_exist: '`i_exist` receives the result of `inquire(file=..., exist=...)` and tells the
    routine whether the configured fertilizer database file is physically present before it
    attempts to open it.'
uses:
  input_file_module: The routine gets the fertilizer database path from `input_file_module`
    through `in_parmdb%fert_frt`, so this module controls which file is opened and whether
    the default `fertilizer.frt` name or another configured path is used.
  maximum_data_module: '`maximum_data_module` provides `db_mx%fertparm`, the shared count
    of loaded fertilizer records. This value is how the rest of the model learns the size
    of the fertilizer database after loading completes.'
  fertilizer_data_module: '`fertilizer_data_module` owns the allocatable `fertdb` array that
    stores the fertilizer parameter records. This routine allocates that array and fills it
    with the file contents.'
---

<!-- facts:header -->

Reads the fertilizer parameter database from `fertilizer.frt` into the shared `fertdb` array and records how many fertilizer entries were loaded. It is part of the database initialization sequence used before management and nutrient routines run.

## Bottom Line

`fert_parm_read` loads the fertilizer database used by SWAT+ from the file named in `in_parmdb%fert_frt`, which defaults to `fertilizer.frt`. It first checks whether that file exists; if not, or if the name is the sentinel string `null`, it creates a minimal `fertdb(0:0)` allocation instead of reading records.

When a real file is present, the routine counts data records, allocates `fertdb(0:imax)`, rewinds the file, and rereads the fertilizer records into `fertdb(1:imax)`. It then stores the final count in `db_mx%fertparm`, so later code knows how many fertilizer parameter records are available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization, as part of `proc_db`, before management, nutrient, and other spatial routines need fertilizer properties. `proc_db` prepares the shared database-loading sequence, and later model behavior depends on `fertdb` being allocated and `db_mx%fertparm` being set to the number of available fertilizer entries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and status flags | The routine starts with local counters and buffers initialized, setting `eof`, `imax`, and `mfrt` to zero and preparing the variables used to scan and load the file. |
| 2. Check whether the fertilizer file exists or is disabled | It uses `inquire` on `in_parmdb%fert_frt` to detect whether the configured fertilizer file exists, and if the file is missing or the path is the literal string `null`, it allocates a minimal `fertdb(0:0)` array and skips loading. |
| 3. Open the fertilizer file and read past title/header lines | If a real file is present, the routine opens unit 107 on `in_parmdb%fert_frt`, reads the title line into `titldum`, and reads the header line into `header`, stopping early if either read hits end-of-file. |
| 4. Count fertilizer data records | It loops through the remaining lines with `read` into `titldum`, incrementing `imax` for each successful record until the read status indicates end-of-file. |
| 5. Allocate the fertilizer database array | After the scan, it allocates `fertdb(0:imax)` so the shared fertilizer database has enough space for the record count that was just discovered. |
| 6. Rewind the file and reread the title and header | The routine rewinds unit 107 and repeats the title/header reads so it can start a clean second pass from the top of the file. |
| 7. Load fertilizer records into shared state | It loops from `it = 1` to `imax` and reads each fertilizer record directly into `fertdb(it)`, filling the allocated database array with file contents. |
| 8. Publish the database size and close the file | Finally, the routine stores the discovered record count in `db_mx%fertparm` and closes unit 107 for `fertilizer.frt`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_parmdb` | `in_parmdb%fert_frt` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%fertparm` |
| [sym:fertilizer_data_module] | `fertdb` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%fertparm` | After the fertilizer file scan completes, whether the file existed or not. | `db_mx%fertparm` is set to the number of fertilizer records found in `fertilizer.frt`, or left at zero when the file is missing or disabled. This publishes the database size for later routines that need to know how many fertilizer parameter records were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit df07e3f with the full fertilizer-file reader, including the existence check, counting pass, allocation of `fertdb`, reread after `rewind`, and publication of `db_mx%fertparm`. Commit 94b6dec then copied that same implementation into the next source snapshot without changing the visible logic in the resolved diff. Commit 39fabde only initialized local variables (`it`, `titldum`, `header`, `eof`, `imax`, and `mfrt`) and did not alter the algorithm beyond those default values.

- df07e3f added the fertilizer database reader and its two-pass file-loading logic, including the `fertdb` allocation and `db_mx%fertparm` update.
- 39fabde initialized the local counters and buffers at declaration time, changing only startup defaults and not the file-reading flow.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'fert_parm_read' has no extracted documentation comment.
