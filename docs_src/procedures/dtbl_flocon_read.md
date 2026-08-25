---
kind: procedure
symbol: dtbl_flocon_read
title: dtbl_flocon_read
status: filled
source_hash: 8c6c32817cacd0d9
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from the top of `flo_con.dtl`; it is only used to advance
    past the file header.
  header: Reusable scratch string for section header lines inside `flo_con.dtl` while the
    routine skips labeled blocks and reads grouped records.
  eof: I/O status flag from each `read` on unit 107; negative values signal end-of-file and
    terminate the scan/read loop.
  i: Loop counter over the decision tables being loaded from `flo_con.dtl`.
  mdtbl: Holds the number of flow-control decision tables declared in the file, and sets the
    allocation size for `dtbl_flo(0:mdtbl)`.
  ic: Loop counter over the condition rows within one decision table.
  ial: Loop counter over the alternative columns read for each condition row.
  iac: Loop counter over the action rows within one decision table.
  i_exist: Logical existence check for the configured flow-control input file; it guards the
    file read and triggers a null-table fallback when the file is missing.
  idb: Loop counter used during the cross-walk from object `ruleset` names to decision-table
    indices.
  iob: Loop counter over spatial objects in `sp_ob%objs` while assigning `ob(iob)%flo_dtbl`.
uses:
  maximum_data_module: This module owns `db_mx`, and `db_mx%dtbl_flo` stores the number of
    flow-control decision tables discovered in the file. The routine writes that count so
    other code can know how many entries in `dtbl_flo` are valid.
  hydrograph_module: This module owns the spatial object inventory and each object's flow-control
    linkage. `sp_ob%objs` sets the loop bound over objects, `ob(iob)%ruleset` provides the
    name to match, and `ob(iob)%flo_dtbl` is the index written here for later use by hydrograph/flow-control
    behavior.
  input_file_module: This module supplies the configured filename `in_cond%dtbl_flo`. The
    routine uses that path to decide which file to open, so the input configuration controls
    whether flow-control tables are loaded at all.
  conditional_module: This module defines the `dtbl_flo` decision-table array and its component
    fields. The routine allocates and fills those fields directly, so the table type is the
    storage target for everything read from `flo_con.dtl`.
---

<!-- facts:header -->

Reads the flow-control decision table file `flo_con.dtl` and loads its tables into `dtbl_flo`. It also cross-walks each spatial object's `ruleset` name to the matching decision-table index.

## Bottom Line

`dtbl_flocon_read` is the file reader for flow-control decision tables. It opens the configured `flo_con.dtl`, scans the file to count how many decision tables are present, allocates `dtbl_flo`, and then reads each table's name, condition definitions, alternatives, actions, and action outcomes.

After loading the tables, it sets `db_mx%dtbl_flo` to the number of tables found and assigns each object's `ob(iob)%flo_dtbl` pointer by matching `ob(iob)%ruleset` against `dtbl_flo(idb)%name`. That makes the flow-control table lookup available to later hydrograph and routing logic.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input initialization after the flow-control file name has been set in `in_cond%dtbl_flo`. It prepares the `dtbl_flo` table data and object-to-table links that later flow-control and hydrograph routines rely on when evaluating object rulesets.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and status flags | Set the scratch strings and loop/status variables to known initial values before any file access begins. |
| 2. Check whether the configured flow-control file exists | Test the configured path in `in_cond%dtbl_flo`; if the file is missing or set to `null`, allocate an empty `dtbl_flo(0:0)` and skip the read path. |
| 3. Open and probe the file header | Open unit 107 on `flo_con.dtl`, read the title line, read the table count into `mdtbl`, skip the next record, and allocate `dtbl_flo(0:mdtbl)` for the tables to be loaded. |
| 4. Read each decision table summary and allocate per-table storage | For each table index, read the table name and counts, then allocate arrays for conditions, alternatives, actions, hit flags, action type/app flags, and action outcomes. |
| 5. Load the table's condition section | Read the section header, then loop over each condition row and read the condition record plus all alternative values for that condition. |
| 6. Load the table's action section | Read the action-section header, then loop over each action and read the action record plus its outcome flags, followed by a record skip at the end of the table block. |
| 7. Record the number of loaded tables | Store the file-derived table count in `db_mx%dtbl_flo` and leave the file-reading loop. |
| 8. Cross-walk object rulesets to decision-table indices | Loop over all spatial objects; for each object with a non-`null` ruleset, search the loaded tables for a matching name and write the matching index to `ob(iob)%flo_dtbl`. |
| 9. Close the flow-control file | Close unit 107 and return to the caller after the decision-table data and object links are established. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dtbl_flo` |
| [sym:hydrograph_module] | `sp_ob, ob` | `sp_ob%objs, ob(iob)%ruleset, ob(iob)%flo_dtbl` |
| [sym:input_file_module] | `in_cond` | `in_cond%dtbl_flo` |
| [sym:conditional_module] | `dtbl_flo` | `dtbl_flo(i)%name, dtbl_flo(i)%conds, dtbl_flo(i)%alts, dtbl_flo(i)%acts, dtbl_flo(i)%cond(ic), dtbl_flo(i)%alt(ic,ial), dtbl_flo(i)%act(iac), dtbl_flo(i)%act_outcomes(iac,ial), dtbl_flo(idb)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%dtbl_flo` | When `flo_con.dtl` exists, is not `null`, and the scan succeeds through the table-count read. | `db_mx%dtbl_flo` is set to the number of flow-control decision tables declared in the file so later loops know the valid upper bound for `dtbl_flo`. |
| `ob(iob)%flo_dtbl` | For each `iob` where `ob(iob)%ruleset` is not `null` and matches `dtbl_flo(idb)%name` during the cross-walk loop. | `ob(iob)%flo_dtbl` is updated to the index of the matching flow-control decision table so the object can refer to its loaded ruleset by position. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `dtbl_flocon_read`. `df07e3f` added the routine and its full read/allocate/cross-walk logic. `94b6dec` updated the source to the imported version but did not change the routine's behavior in the visible diff. `39fabde` initialized the local scratch and counter variables and changed `act_typ` and `act_app` allocations to use `source = 0`. `080211e` removed the special-case block that mapped divert recall actions to `dtbl_flo(i)%act_typ`.

- df07e3f introduced the file reader, array allocation, section parsing, `db_mx%dtbl_flo` assignment, and `ob(iob)%flo_dtbl` cross-walk.
- 39fabde made local variables default-initialized and ensured `act_typ` and `act_app` start at zero for each table.
- 080211e removed the divert/recall action cross-walk into `dtbl_flo(i)%act_typ`, so the routine no longer rewrites action types from recall filenames.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dtbl_flocon_read' has no extracted documentation comment.
