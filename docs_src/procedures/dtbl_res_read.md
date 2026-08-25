---
kind: procedure
symbol: dtbl_res_read
title: dtbl_res_read
status: filled
source_hash: fa2c6356d093ad58
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to read and discard the file title line at the start of `res_rel.dtl`.
  header: Scratch string used to read and discard section headers before each block of condition
    or action records.
  eof: I/O status flag from `read(..., iostat=eof)` calls; negative values end the scan or
    abort the current pass.
  i: Outer loop counter over decision tables from 1 to `mdtbl`.
  mdtbl: Number of reservoir decision tables reported by the input file and used to size `dtbl_res`.
  ic: Counter for condition rows within one decision table.
  ial: Counter over the alternative columns when reading condition alternatives or action
    outcomes.
  iac: Counter for action rows within one decision table and for the later action cross-walk
    loop.
  i_exist: Logical result of `inquire(file=...)` that tells the routine whether the configured
    decision-table file exists before opening it.
  idb: Loop counter used to search database lists (`res_weir` and `recall_db`) for a matching
    `file_pointer` name.
uses:
  maximum_data_module: The routine writes `db_mx%dtbl_res` after loading the file and uses
    `db_mx%res_weir` and `db_mx%recalldb_max` as the bounds for matching action pointers to
    model database entries.
  reservoir_data_module: Reservoir weir names are the lookup keys for `typ='release'` and
    `option='weir'` actions, so this module provides the target names that `file_pointer`
    must match.
  landuse_data_module: This module defines the `decision_table` type that `dtbl_res_read`
    populates; every field read from `res_rel.dtl` lands in this shared table array.
  mgt_operations_module: The action records read here use the `actions_var` structure from
    this module, including `typ`, `option`, and `file_pointer`, which drive the later cross-walk
    logic.
  tillage_data_module: It is imported even though no specific symbol is referenced in the
    extracted lines; the routine still relies on the shared decision-table definitions and
    loader context established by the model's data modules.
  fertilizer_data_module: It is imported even though no specific symbol is referenced in the
    extracted lines; the routine still relies on the shared decision-table definitions and
    loader context established by the model's data modules.
  input_file_module: The file name comes from `in_cond%dtbl_res`, so `input_file_module` controls
    which decision-table file this routine opens or whether the loader should skip reading
    entirely.
  conditional_module: The whole routine populates the `conditional_module::dtbl_res` array,
    then uses its nested condition, alternative, action, and pointer fields to build the reservoir
    decision-table database.
  recall_module: Measured-release actions can point to recall database names, so this module
    supplies the `recall_db` list that `file_pointer` is matched against.
  hydrograph_module: 'The procedure uses `use hydrograph_module, only : recall`, so that module
    is part of the imported state set even though the resolved code path now prefers `recall_db`
    for the measured-release lookup.'
---

<!-- facts:header -->

Reads the reservoir decision-table file `res_rel.dtl` and builds the in-memory `dtbl_res` database. It also cross-walks action pointer strings to numeric indices for reservoir weirs and recall databases.

## Bottom Line

`dtbl_res_read` is the loader for reservoir release decision tables. It checks the configured file name in `in_cond%dtbl_res`, opens `res_rel.dtl`, reads the table count and each table's header, conditions, alternatives, actions, and action outcomes, then allocates and fills `conditional_module::dtbl_res` entries.

After reading the text data, it resolves action metadata into model indices. For actions with `typ = 'release'` and `option = 'weir'`, it matches `file_pointer` against `res_weir(idb)%name`; for `option = 'meas'`, it matches against `recall_db(idb)%name`, storing the found index in `dtbl_res(i)%act_typ(iac)` and updating `db_mx%dtbl_res` with the number of loaded tables.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization when the reservoir decision-table file must be loaded into memory. The upstream input-file setup must supply `in_cond%dtbl_res`, and later reservoir release decision logic depends on the populated `dtbl_res` tables and the resolved `act_typ` indices.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the configured decision-table file is available | The routine queries `in_cond%dtbl_res` with `inquire` and, if the file is missing or set to `null`, allocates an empty `dtbl_res(0:0)` array instead of reading any data. |
| 2. Open the decision-table file and read the file-level header | Inside the load loop, unit 107 is opened on `in_cond%dtbl_res`, the title line and table count are read, and an extra record is skipped before allocation proceeds. |
| 3. Allocate the decision-table array using the table count | The routine allocates `dtbl_res(0:mdtbl)` so each table from the file can be stored in a dedicated array element. |
| 4. Read each table's metadata and allocate its child arrays | For each table, the routine reads the section header and table metadata, then allocates arrays for conditions, alternatives, actions, hit flags, action type pointers, action application pointers, and action outcomes. |
| 5. Load the condition and alternative rows | The routine reads the condition section header and then loads each condition plus its list of alternative labels into `dtbl_res(i)%cond` and `dtbl_res(i)%alt`. |
| 6. Load the action rows and action outcomes | The routine reads the action section header, then loads each action record and its alternative-specific outcome flags into `dtbl_res(i)%act` and `dtbl_res(i)%act_outcomes`. |
| 7. Cross-walk release actions to reservoir weir indices | For each action whose type is `release` and option is `weir`, the routine scans `res_weir` by name and stores the matching index in `dtbl_res(i)%act_typ(iac)`. |
| 8. Cross-walk measured-release actions to recall database indices | For each action whose type is `release` and option is `meas`, the routine scans `recall_db` by name and stores the matching index in `dtbl_res(i)%act_typ(iac)`. |
| 9. Save the number of loaded tables and exit the file-scan loop | After all tables are processed, the routine writes the table count into `db_mx%dtbl_res` and exits the open-ended load loop. |
| 10. Close the input file and return | The routine closes unit 107 and returns to the caller after the decision-table database is loaded or skipped. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_weir, db_mx%recalldb_max, db_mx%dtbl_res` |
| [sym:reservoir_data_module] | `res_weir` | `res_weir(idb)%name` |
| [sym:landuse_data_module] | `dtbl_res` | `dtbl_res(i)%name, dtbl_res(i)%conds, dtbl_res(i)%alts, dtbl_res(i)%acts, dtbl_res(i)%cond(ic), dtbl_res(i)%alt(ic,ial), dtbl_res(i)%act(iac), dtbl_res(i)%act_outcomes(iac,ial), dtbl_res(i)%act(iac)%typ, dtbl_res(i)%act(iac)%option, dtbl_res(i)%act(iac)%file_pointer, dtbl_res(i)%act_typ(iac)` |
| [sym:mgt_operations_module] | `dtbl_res` | `dtbl_res(i)%name, dtbl_res(i)%conds, dtbl_res(i)%alts, dtbl_res(i)%acts, dtbl_res(i)%cond(ic), dtbl_res(i)%alt(ic,ial), dtbl_res(i)%act(iac), dtbl_res(i)%act_outcomes(iac,ial), dtbl_res(i)%act(iac)%typ, dtbl_res(i)%act(iac)%option, dtbl_res(i)%act(iac)%file_pointer, dtbl_res(i)%act_typ(iac)` |
| [sym:tillage_data_module] | `dtbl_res` | `dtbl_res(i)%name, dtbl_res(i)%conds, dtbl_res(i)%alts, dtbl_res(i)%acts, dtbl_res(i)%cond(ic), dtbl_res(i)%alt(ic,ial), dtbl_res(i)%act(iac), dtbl_res(i)%act_outcomes(iac,ial), dtbl_res(i)%act(iac)%typ, dtbl_res(i)%act(iac)%option, dtbl_res(i)%act(iac)%file_pointer, dtbl_res(i)%act_typ(iac)` |
| [sym:fertilizer_data_module] | `dtbl_res` | `dtbl_res(i)%name, dtbl_res(i)%conds, dtbl_res(i)%alts, dtbl_res(i)%acts, dtbl_res(i)%cond(ic), dtbl_res(i)%alt(ic,ial), dtbl_res(i)%act(iac), dtbl_res(i)%act_outcomes(iac,ial), dtbl_res(i)%act(iac)%typ, dtbl_res(i)%act(iac)%option, dtbl_res(i)%act(iac)%file_pointer, dtbl_res(i)%act_typ(iac)` |
| [sym:input_file_module] | `in_cond` | `in_cond%dtbl_res` |
| [sym:conditional_module] | `dtbl_res` | `dtbl_res(i)%name, dtbl_res(i)%conds, dtbl_res(i)%alts, dtbl_res(i)%acts, dtbl_res(i)%cond(ic), dtbl_res(i)%alt(ic,ial), dtbl_res(i)%act(iac), dtbl_res(i)%act_outcomes(iac,ial), dtbl_res(i)%act(iac)%typ, dtbl_res(i)%act(iac)%option, dtbl_res(i)%act(iac)%file_pointer, dtbl_res(i)%act_typ(iac)` |
| [sym:recall_module] | `recall_db` | `recall_db(idb)%name` |
| [sym:hydrograph_module] | `recall` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `dtbl_res(i)%act_typ(iac)` | When `dtbl_res(i)%act(iac)%typ` is `release` and `dtbl_res(i)%act(iac)%option` is `weir` or `meas` during the cross-walk loop. | `dtbl_res(i)%act_typ(iac)` is overwritten with the numeric index of the matching reservoir weir or recall database entry so later release logic can refer to a model object by number instead of by name. |
| `db_mx%dtbl_res` | After the routine finishes reading all decision tables from the configured file. | `db_mx%dtbl_res` is set to the number of loaded reservoir decision tables, which records the size of the database for later indexing and validation. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior-changing commits. `df07e3f` added the routine with the full file-reading and cross-walk logic. `94b6dec` left the procedure body unchanged in the excerpted diff, so it did not alter behavior here. `39fabde` changed only local variable initialization and allocated `act_typ` and `act_app` with `source = 0`, ensuring those arrays start at zero. `080211e` switched the measured-release lookup from `db_mx%recall_max`/`recall(idb)%name` to `db_mx%recalldb_max`/`recall_db(idb)%name` and added `use recall_module`.

- df07e3f introduced `dtbl_res_read` as a new loader for `res_rel.dtl`, including allocation of decision-table arrays and cross-walking release actions to database indices.
- 39fabde tightened initialization by zeroing `titldum`, `header`, `eof`, counters, and the `act_typ`/`act_app` arrays so unfilled pointer slots start from known values.
- 080211e changed measured-release resolution to use `recall_module::recall_db` and `db_mx%recalldb_max`, affecting which database list is searched for `file_pointer` matches.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dtbl_res_read' has no extracted documentation comment.
- The extracted source shows `use hydrograph_module, only : recall` but the resolved lookup for measured-release actions now uses `recall_db` from `recall_module`; the hydrograph import is retained in source but not used in the shown lines.
