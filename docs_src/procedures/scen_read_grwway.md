---
kind: procedure
symbol: scen_read_grwway
title: scen_read_grwway
status: filled
source_hash: 40841db07914b074
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the file title line on the first
    pass and again after rewinding on the second pass.
  header: Scratch character buffer used to read and discard the file header line before counting
    or loading data records.
  eof: I/O status flag from each read; it is tested for end-of-file and used to stop the counting
    and loading loops.
  imax: Counts how many grassed-waterway operation records are present in the file; that count
    is used to size `grwaterway_db` and is later copied to `db_mx%grassop_db`.
  i_exist: Logical flag set by `inquire` to indicate whether the configured grassed waterways
    file exists before the routine tries to open it.
  igrwwop: Loop counter that indexes the individual grassed-waterway records as they are read
    into `grwaterway_db`.
uses:
  input_file_module: This module provides `in_str%grassww_str`, the configured pathname for
    the grassed waterways input file. The routine uses that string to decide which file to
    open and to test whether the file is effectively disabled by the sentinel value `"null"`.
  maximum_data_module: This module holds `db_mx%grassop_db`, the shared counter for how many
    grassed-waterway operation records were loaded. Setting it here makes the loaded database
    size available to later routines that need to know how many entries exist.
  mgt_operations_module: This module owns `grwaterway_db`, the allocatable array that receives
    the parsed grassed-waterway operation records. The routine allocates and fills that array
    so other management code can use the loaded database.
---

<!-- facts:header -->

Reads the grassed waterways structural scenario file and loads its records into the shared grass waterway operation database. It also records how many operations were found for later model use.

## Bottom Line

`scen_read_grwway` is a file-loader for the grassed waterways structure database. It checks whether the configured `grassedww.str` file exists, counts the data records, allocates `grwaterway_db`, then rereads the file and stores each record into the shared `mgt_operations_module` database.

The routine matters because later management processing uses `grwaterway_db` as the in-memory source of grassed-waterway definitions, and `db_mx%grassop_db` captures how many records were loaded.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization in `proc_db`, after other management/structural readers and before later model components use the structural operation databases. Its results feed the shared grassed-waterway management database and the record count used by downstream management logic.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and detect the configured file | The routine resets `eof` and `imax`, then checks whether `in_str%grassww_str` exists. If the file is missing or the configured name is the sentinel string `"null"`, it bypasses file scanning and prepares to allocate a one-element placeholder database. |
| 2. Allocate a placeholder when the file is absent | If no usable grassed waterways file is available, the routine allocates `grwaterway_db(0:0)` so the shared database exists even though no records were loaded. |
| 3. Open and scan the file to count records | When a usable file exists, the routine opens unit 107 on `in_str%grassww_str`, reads and discards the title and header lines, and then loops through the remaining lines, incrementing `imax` once per data record until end-of-file is reached. |
| 4. Allocate the management database at the counted size | After counting the records, the routine allocates `grwaterway_db(0:imax)` so the shared grassed-waterway database has enough slots for every record read from the file. |
| 5. Rewind and skip the file prologue again | The routine rewinds unit 107 to the start of `grassedww.str`, rereads the title and header lines, and positions the file so the actual data records can be loaded from the beginning. |
| 6. Load each grassed-waterway record into shared state | Using `igrwwop` as the record index, the routine reads each data line into `grwaterway_db(igrwwop)` until all counted records have been transferred or an end-of-file condition stops the loop. |
| 7. Publish the record count and close the file | The routine stores the final record count in `db_mx%grassop_db`, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_str` | `in_str%grassww_str` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%grassop_db` |
| [sym:mgt_operations_module] | `grwaterway_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%grassop_db` | After the file scan completes, with `imax` holding the number of grassed-waterway records found in `grassedww.str`. | `db_mx%grassop_db` is updated to the number of grassed-waterway operation records loaded by this routine, making the count available to later management and database code. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed this procedure. The initial addition in 94b6dec introduced `scen_read_grwway` with the existing two-pass file scan, allocation, reload, and count export logic. Commit 39fabde then initialized the local scratch variables (`titldum`, `header`, `eof`, `imax`, and `igrwwop`) at declaration time; the procedure logic itself did not change.

- 94b6dec added the full reader: file existence check, two-pass counting and loading of `grassedww.str`, allocation of `grwaterway_db`, and assignment of `db_mx%grassop_db`.
- 39fabde only changed local variable initialization style by assigning default values at declaration for `titldum`, `header`, `eof`, `imax`, and `igrwwop`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'scen_read_grwway' has no extracted documentation comment.
