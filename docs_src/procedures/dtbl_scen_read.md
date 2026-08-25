---
kind: procedure
symbol: dtbl_scen_read
title: dtbl_scen_read
status: filled
source_hash: e757653cfc9edf1c
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to consume the file title/header line at the start of `scen_lu.dtl`.
  header: Scratch string used to skip section header lines before reading each block of decision-table
    content.
  eof: I/O status flag from each `read`; negative values indicate end-of-file or failed input
    and trigger exit from the scan/read loops.
  i: Outer loop counter over decision tables in the file, from 1 to `mdtbl`.
  mdtbl: Holds the number of decision tables reported in the file and is used to allocate
    `dtbl_scen(0:mdtbl)` and bound the outer loop.
  ic: Loop counter over condition rows within one decision table.
  ial: Loop counter over condition alternatives and action outcomes when reading row values.
  iac: Loop counter over action records within one decision table and over actions in the
    cross-walk pass.
  i_exist: Logical existence check from `inquire`; tells the routine whether the configured
    decision-table file is present before opening it.
  ilum: Loop counter used to search landuse or snow lookup tables when translating action
    file pointers to numeric indices.
uses:
  maximum_data_module: This module supplies `db_mx`, which is the shared capacity/count bookkeeping
    structure for database-style inputs. `dtbl_scen_read` updates `db_mx%dtbl_scen` with the
    number of decision tables loaded, and it also uses `db_mx%landuse` and `db_mx%sno` as
    loop bounds when cross-walking action pointers to landuse and snow parameter indices.
  reservoir_data_module: This module provides the snow-parameter database that the routine
    needs when an action has `typ = 'snow_change'`. The code compares each action's `file_pointer`
    to `snodb(ilum)%name` so it can turn the text pointer into the integer lookup stored in
    `dtbl_scen(i)%act_typ(iac)`.
  landuse_data_module: This module provides the land-use management database `lum`. The routine
    uses `lum(ilum)%name` to translate `lu_change` action pointers into numeric indices, so
    later decision-table processing can refer to the correct landuse record without string
    matching.
  mgt_operations_module: This module provides the land-use management database `lum`. The
    routine uses `lum(ilum)%name` to translate `lu_change` action pointers into numeric indices,
    so later decision-table processing can refer to the correct landuse record without string
    matching.
  tillage_data_module: No candidate reference from `tillage_data_module` is used in the extracted
    source for `dtbl_scen_read`; the module is imported but not referenced by any visible
    symbol in this routine.
  fertilizer_data_module: No candidate reference from `fertilizer_data_module` is used in
    the extracted source for `dtbl_scen_read`; the module is imported but not referenced by
    any visible symbol in this routine.
  input_file_module: This module provides `in_cond%dtbl_scen`, the configured filename for
    the decision-table input. The routine uses it both to test whether the file exists and
    to open the correct file unit for reading.
  conditional_module: This module defines the `decision_table` type and its nested fields.
    `dtbl_scen_read` allocates and fills those fields from `scen_lu.dtl`, including names,
    counts, condition arrays, action arrays, outcomes, and the `act_typ` lookup results that
    power later decision-table execution.
  hru_module: This module provides the snow-parameter lookup table `snodb`. Although the routine
    does not load snow data itself, it uses the names in `snodb(ilum)%name` to resolve `snow_change`
    action pointers to numeric snow-table indices.
---

<!-- facts:header -->

Reads the landuse/scenario decision-table file `scen_lu.dtl` and loads decision tables into `dtbl_scen`.
It also cross-walks action pointers to numeric indices for land-use and snow-change actions, then stores the table count in `db_mx%dtbl_scen`.

## Bottom Line

This subroutine is the file reader for SWAT+ decision tables used by landuse/scenario logic. It opens the configured `scen_lu.dtl` file, scans the table count, allocates `dtbl_scen`, and then reads each decision table's conditions, alternatives, actions, and action outcomes into the shared `conditional_module` data structure.

After the raw table records are loaded, it converts certain action pointers from text to numeric indices. For `lu_change` actions it matches `dtbl_scen(i)%act(iac)%file_pointer` against `lum(ilum)%name`; for `snow_change` actions it matches the same pointer against `snodb(ilum)%name`. The routine then records how many decision tables were loaded in `db_mx%dtbl_scen` so later model code can size and use this database.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model/input initialization, after the configured file name has been set in `in_cond%dtbl_scen` and before decision-table logic is used elsewhere. Its results are needed by later conditional processing that evaluates `dtbl_scen`, checks condition alternatives, and resolves action pointer indices for landuse and snow changes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the decision-table file should be read | The routine tests `in_cond%dtbl_scen` with `inquire` and treats a missing file or the literal string `null` as a disabled input. In that case it allocates an empty `dtbl_scen(0:0)` array and skips file parsing. |
| 2. Open the configured file and scan the table count | It opens unit 107 on `in_cond%dtbl_scen`, reads and discards the title line, reads `mdtbl`, skips one more record, and then allocates `dtbl_scen(0:mdtbl)`. The outer loop repeats on EOF-like status handling until a read succeeds without early exit. |
| 3. Read each decision-table header and allocate per-table arrays | For each table, the routine reads a section header, then the table name and counts for conditions, alternatives, and actions. Using those counts, it allocates the condition, alternative, action, outcome, and tracking arrays needed to hold the table content. |
| 4. Load condition rows | It reads another header and then loops through each condition row, loading one `cond(ic)` record plus all alternative values for that condition from `alt(ic,ial)`. This populates the rule tests that will later be evaluated against state. |
| 5. Load action rows and outcomes | After reading the action-section header, it loops through each action record and reads the action metadata plus all outcome flags for the alternatives. A trailing blank/separator record is then consumed before cross-walking begins. |
| 6. Translate action pointers to numeric lookup indices | For each action, the routine inspects `act(iac)%typ`. If it is `lu_change`, it searches `lum` by name and stores the matching index in `act_typ(iac)`; if it is `snow_change`, it searches `snodb` by name and stores that index instead. |
| 7. Record the number of loaded decision tables and close the file | Once one successful pass through the file completes, the routine stores `mdtbl` in `db_mx%dtbl_scen`, exits the open/read loop, and closes unit 107. That shared count becomes the model-wide maximum table count for later use. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%landuse, db_mx%sno, db_mx%dtbl_scen` |
| [sym:reservoir_data_module] | `snodb` | `snodb(ilum)%name` |
| [sym:landuse_data_module] | `lum` | `lum(ilum)%name` |
| [sym:mgt_operations_module] | `lum` | `lum(ilum)%name` |
| [sym:input_file_module] | `in_cond` | `in_cond%dtbl_scen` |
| [sym:conditional_module] | `dtbl_scen` | `dtbl_scen(i)%name, dtbl_scen(i)%conds, dtbl_scen(i)%alts, dtbl_scen(i)%acts, dtbl_scen(i)%cond(ic), dtbl_scen(i)%alt(ic,ial), dtbl_scen(i)%act(iac), dtbl_scen(i)%act_outcomes(iac,ial), dtbl_scen(i)%act(iac)%typ, dtbl_scen(i)%act(iac)%file_pointer, dtbl_scen(i)%act_typ(iac)` |
| [sym:hru_module] | `snodb` | `snodb(ilum)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `dtbl_scen(i)%act_typ(iac)` | When an action record has `typ = 'lu_change'` and `act(iac)%file_pointer` matches a `lum(ilum)%name` entry. | The routine stores the matched landuse index in `dtbl_scen(i)%act_typ(iac)`, converting a text pointer into a numeric reference that later decision-table code can use without string matching. |
| `db_mx%dtbl_scen` | After one complete successful pass through the input file, just before leaving the open/read loop. | The routine sets `db_mx%dtbl_scen = mdtbl` so the shared maximum-data bookkeeping reflects how many decision tables were loaded from `scen_lu.dtl`. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `dtbl_scen_read.f90`. The original addition in `df07e3f` created the reader, file scan, allocations, and cross-walk logic; `39fabde` initialized local counters and read buffers and changed `act_typ`/`act_app` allocations to zero-fill them; `e18817a` added zero-filled allocation for `lu_chg_mx`; and `57f3eea` imported `snodb`, added zero-filled `snow_chg_mx`, and extended the cross-walk to resolve `snow_change` actions against the snow database.

- df07e3f introduced the decision-table reader and its file-driven allocation/read workflow for `scen_lu.dtl`.
- 39fabde made the routine safer by initializing scalar locals and zero-filling `act_typ` and `act_app` on allocation.
- e18817a expanded per-action bookkeeping by allocating `lu_chg_mx` with zeros.
- 57f3eea added snow-change support by importing `snodb`, allocating `snow_chg_mx`, and mapping `snow_change` action pointers to snow database indices.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dtbl_scen_read' has no extracted documentation comment.
