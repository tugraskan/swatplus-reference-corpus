---
kind: procedure
symbol: till_parm_read
title: till_parm_read
status: filled
source_hash: 930c2e9d49eb5b61
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and skip the file title or blank/data lines
    while counting and re-reading `tillage.til`.
  header: Scratch character buffer used to read the header line from `tillage.til` during
    both the counting pass and the data-loading pass.
  eof: I/O status flag for the `read` statements; it controls loop exit and tells the routine
    when the file has ended or a read failed.
  imax: Counter for the number of tillage records found in the file; it is later used to size
    `tilldb` and to report the total number of tillage parameters loaded.
  i_exist: Logical file-existence flag returned by `inquire`; it decides whether the routine
    reads `tillage.til` or allocates an empty `tilldb`.
  itl: Loop index for populating each tillage database entry in `tilldb` during the second
    pass through the file.
  mtl: Initialized but not used in the visible routine body; it appears to be a leftover counter
    placeholder.
uses:
  input_file_module: This module supplies `in_parmdb%till_til`, the configured path to the
    tillage database file. The routine cannot locate or open the file without that shared
    input setting.
  maximum_data_module: This module holds `db_mx%tillparm`, the shared count of tillage records
    loaded from `tillage.til`. Other database and setup code relies on that count to know
    how many tillage entries are available.
  tillage_data_module: This module defines the `tilldb` array that receives the parsed tillage
    records, plus the biomix globals `bmix_idtill`, `bmix_eff`, and `bmix_depth` that this
    routine initializes from the `biomix` record or default values.
---

<!-- facts:header -->

Reads the tillage parameter database from `tillage.til` into the shared tillage array. It also records how many tillage entries were loaded and captures the biomix tillage defaults used by later mixing logic.

## Bottom Line

`till_parm_read` is a database loader for SWAT+ tillage definitions. It checks whether the configured tillage input file exists, counts the records, allocates `tilldb`, then reads each tillage record into shared module state.

While loading the file, it looks for the tillage entry named `biomix` and copies that record's efficiency and depth into the global biomix settings. If no biomix record is found, it falls back to the hard-coded defaults `bmix_eff = 0.2` and `bmix_depth = 50.`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization in `proc_db`, after the input-file module has provided the configured database filename and before later management and operation routines use tillage parameters. Its results feed the shared tillage database and biomix settings used by tillage-related model behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and biomix state | Resets the local file-status counters and clears the biomix tillage index before any file I/O begins. |
| 2. Check whether the tillage input file is usable | Uses `inquire` on `in_parmdb%till_til`; if the file is missing or set to `null`, it allocates a one-element empty `tilldb` array and skips loading. |
| 3. Open the tillage file and start a counting pass | Opens unit 105 on `tillage.til`, reads past the title and header, then counts data records by reading lines until end-of-file updates `eof`. |
| 4. Allocate the tillage database array | Allocates `tilldb(0:imax)` after the record count has been determined so the shared database has room for all tillage entries. |
| 5. Rewind and reload the file from the top | Rewinds unit 105 and rereads the title and header lines so the routine can make a second pass through the data section. |
| 6. Read each tillage record into shared state | Loops from 1 to `imax`, reading each record into `tilldb(itl)`; when a record name equals `biomix`, it saves that index and copies the record's efficiency and depth into the global biomix variables. |
| 7. Apply default biomix values when needed | If no `biomix` tillage record was found, assigns the fallback biomix efficiency and depth values. |
| 8. Publish the record count and close the file | Stores the final tillage record count in `db_mx%tillparm`, closes unit 105, and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_parmdb` | `in_parmdb%till_til` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%tillparm` |
| [sym:tillage_data_module] | `tilldb, bmix_idtill, bmix_eff, bmix_depth` | `tilldb(itl)%tillnm, tilldb(itl)%effmix, tilldb(itl)%deptil` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bmix_idtill` | When a loaded tillage record has `tilldb(itl)%tillnm == "biomix"`. | `bmix_idtill` is set to the matching array index so later routines can identify which tillage entry represents biological mixing. |
| `bmix_eff` | When the `biomix` tillage record is found, or when no such record is found and defaults are applied. | `bmix_eff` receives the biomix efficiency from the `biomix` tillage record, or the fallback value `0.2` if no biomix record exists. |
| `bmix_depth` | When the `biomix` tillage record is found, or when no such record is found and defaults are applied. | `bmix_depth` receives the biological mixing depth from the `biomix` tillage record, or the fallback value `50.` if no biomix record exists. |
| `db_mx%tillparm` | After the counting and loading pass completes, regardless of whether the file existed; in the missing-file case `imax` remains 0. | `db_mx%tillparm` is updated with the number of tillage records available so the rest of the model knows how many tillage database entries were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved for `till_parm_read`. The routine was introduced in df07e3f with the initial file-scan, allocate, rewind, read, and close logic. 94b6dec preserved that logic when the source was imported, and 39fabde initialized the local variables. 62cc4fc changed biomix handling so `bmix_idtill` is reset before reading, the `biomix` record is searched for while loading `tillage.til`, and fallback biomix defaults are assigned only if no matching record is found.

- df07e3f introduced the first implementation of `till_parm_read`, including the two-pass read of `tillage.til`, allocation of `tilldb`, and setting `db_mx%tillparm`.
- 39fabde initialized `titldum`, `header`, `eof`, `imax`, `itl`, and `mtl`, which reduced dependence on uninitialized local state.
- 62cc4fc added biomix extraction from `tillage.til`: it resets `bmix_idtill`, captures `bmix_eff` and `bmix_depth` from the `biomix` record, and applies fallback defaults when that record is absent.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'till_parm_read' has no extracted documentation comment.
