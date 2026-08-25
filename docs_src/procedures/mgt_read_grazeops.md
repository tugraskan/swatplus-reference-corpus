---
kind: procedure
symbol: mgt_read_grazeops
title: mgt_read_grazeops
status: filled
source_hash: f83e9a32f636f239
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary text buffer for the title or first non-data line read from `graze.ops`;
    used twice, once during the scan and again after rewind before reading records.
  header: Temporary text buffer for the second header line in `graze.ops`; it is read after
    `titldum` both during the scan and after rewind to skip file headers before the data records.
  eof: I/O status flag from each `read` on unit 107. Zero means the file is still being read,
    and a negative value is used to detect end-of-file and stop the scan or record load.
  imax: Counts how many grazing-operation data records are present in `graze.ops`. The routine
    increments it during the first pass and then uses it to allocate and loop over `grazeop_db`.
  i_exist: Logical result of the `inquire` check on `in_ops%graze_ops`. It tells the routine
    whether the configured grazing-operations file exists before any file I/O is attempted.
  igrazop: Loop index for the grazing-operation database records being read into `grazeop_db`
    and cross-walked to fertilizer data.
  mgrazops: Initialization counter set to zero at entry, but not otherwise used in the visible
    routine body.
  ifert: Loop index used to search `fertdb` for a fertilizer name that matches the grazing
    operation's `fertnm` value.
uses:
  input_file_module: This module supplies `in_ops%graze_ops`, the configured path to the grazing-operations
    input file. Without that shared file-name setting, the routine would not know which file
    to open.
  maximum_data_module: 'This module provides the maximum-count metadata used by the routine:
    `db_mx%fertparm` bounds the fertilizer lookup loop, and `db_mx%grazeop_db` stores the
    final grazing-operation count after the file is read.'
  mgt_operations_module: This allocatable database receives every grazing operation record
    read from `graze.ops`. Its fields hold the operation name, fertilizer name, grazing/trampling/manure
    rates, biomass threshold, and the fertilizer cross-reference assigned during the lookup.
  fertilizer_data_module: This module holds the fertilizer database that `mgt_read_grazeops`
    searches by name. Matching `fertdb(ifert)%fertnm` against each grazing operation's fertilizer
    name is how `manure_id` is assigned.
---

<!-- facts:header -->

Reads the grazing operations database from `graze.ops` into `grazeop_db` and links each grazing operation to a fertilizer entry. It also records how many grazing operations were found so later management code can use the loaded database.

## Bottom Line

mgt_read_grazeops opens the configured grazing-operations file, counts the usable data records, allocates `grazeop_db` to match, then reads each grazing operation record into module state. For every record it also cross-references the fertilizer name against `fertdb` and stores the matching fertilizer index in `manure_id`.

This routine matters because it turns the static `graze.ops` input file into the in-memory grazing-operation database used by the rest of the management setup. It also updates `db_mx%grazeop_db` so other routines know how many grazing operations are available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database setup in `proc_db`, after the management-file infrastructure is ready and before later management routines rely on loaded operation tables. Its results feed the grazing-management database used by later scheduling and management behavior, including fertilizer-name cross-referencing through `manure_id`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local counters and status flags | The routine starts with empty title/header buffers, zeroed status and counter variables, and resets `mgrazops`, `eof`, and `imax` before any file access. |
| 2. Check whether the grazing-operations file is available | It queries `in_ops%graze_ops` with `inquire` and, if the file is missing or set to the literal string `null`, allocates a one-element placeholder `grazeop_db(0:0)` and skips file loading. |
| 3. Open the grazing-operations file and scan its records | If the file is usable, the routine opens unit 107 on `in_ops%graze_ops`, reads and skips the title and header lines, then loops through the remaining records to count how many grazing-operation entries are present in `imax`. |
| 4. Allocate grazing-operation storage from the counted size | After counting the data rows, it allocates `grazeop_db(0:imax)` so the database has one slot per grazing-operation record. |
| 5. Rewind the file and skip the headers again | The routine rewinds unit 107 to the start of `graze.ops`, rereads the title and header lines, and positions the file at the first data record for the load pass. |
| 6. Read each grazing-operation record into module storage | It loops over each allocated database slot and reads the record fields into `grazeop_db(igrazop)%name`, `%fertnm`, `%eat`, `%tramp`, `%manure`, and `%biomin` until end-of-file is reached. |
| 7. Cross-walk fertilizer names to fertilizer IDs | For each loaded grazing operation, the routine searches `fertdb` from 1 to `db_mx%fertparm` and, when `fertnm` matches `fertdb(ifert)%fertnm`, stores the matching index in `grazeop_db(igrazop)%manure_id`. |
| 8. Close the input file and publish the record count | After loading finishes, it closes unit 107 and stores the final count in `db_mx%grazeop_db` so other routines can use the number of grazing operations that were read. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_ops` | `in_ops%graze_ops` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%fertparm, db_mx%grazeop_db` |
| [sym:mgt_operations_module] | `grazeop_db` | `grazeop_db(igrazop)%name, grazeop_db(igrazop)%fertnm, grazeop_db(igrazop)%eat, grazeop_db(igrazop)%tramp, grazeop_db(igrazop)%manure, grazeop_db(igrazop)%biomin, grazeop_db(igrazop)%manure_id` |
| [sym:fertilizer_data_module] | `fertdb` | `fertdb(ifert)%fertnm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `grazeop_db(igrazop)%manure_id` | When a grazing operation's `fertnm` matches `fertdb(ifert)%fertnm` during the fertilizer lookup loop. | `grazeop_db(igrazop)%manure_id` is set to the matching fertilizer index so the grazing operation can reference the fertilizer database by number instead of by name. |
| `db_mx%grazeop_db` | After the file has been scanned and the number of grazing-operation records has been determined. | `db_mx%grazeop_db` is updated to the final record count so other parts of the model know how many grazing-operation entries were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three source versions. The original addition in `df07e3f` introduced `mgt_read_grazeops` with file existence checking, two-pass counting/loading, fertilizer-name cross-walking, and final `db_mx%grazeop_db` storage. Commit `94b6dec` kept the same logic while bringing in the source from bitbucket. Commit `39fabde` only initialized local variables (`titldum`, `header`, `eof`, `imax`, `igrazop`, `mgrazops`, `ifert`) and removed a trailing space in the allocation line; it did not change the algorithm.

- df07e3f: added the grazing-operations reader, including file existence handling, two-pass record counting, allocation of `grazeop_db`, fertilizer cross-reference lookup, and final storage of `db_mx%grazeop_db`.
- 39fabde: initialized local variables at declaration time and made a cosmetic whitespace change; behavior stayed the same.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'mgt_read_grazeops' has no extracted documentation comment.
