---
kind: io
source_symbols:
- dtbl_res_read
title: '`res_rel.dtl`'
status: filled
source_hash: f38d9c98af36a7d2
version_label: SWAT+ 62.0.0
---

**Primary target:** `dtbl_res(:)` (array of `type decision_table`)  
**Read by:** [sym:dtbl_res_read]

## Bottom Line

The file `res_rel.dtl` configures decision tables used for conditional management actions in the model.

It is optional; if the file does not exist or is set to "null", no decision tables are allocated.

The reader `dtbl_res_read` loads this file and populates the `dtbl_res` array of decision tables.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | provides `db_mx` which contains maximum counts such as `res_weir` and `recalldb_max` used to map action types. |
| [sym:reservoir_data_module] | provides `res_weir` array used to identify weir release types for actions. |
| [sym:landuse_data_module] | not directly referenced in the reader but likely related to land use conditions in decision tables. |
| [sym:mgt_operations_module] | not directly referenced in the reader but likely related to management operations referenced by actions. |
| [sym:tillage_data_module] | not directly referenced in the reader but possibly related to tillage actions. |
| [sym:fertilizer_data_module] | not directly referenced in the reader but possibly related to fertilizer actions. |
| [sym:input_file_module] | provides `in_cond%dtbl_res` which is the filename string for the `res_rel.dtl` input file. |
| [sym:conditional_module] | provides the `decision_table` type and related types `conditions_var` and `actions_var` used to store the decision table data. |
| [sym:recall_module] | provides `recall_db` array used to identify measured release types for actions. |
| [sym:hydrograph_module] | provides `recall` (only) but not directly used in this reader. |

## File Variables

The file `res_rel.dtl` contains one or more decision tables that define conditional logic for management actions. Each decision table record is read into an element of the `dtbl_res` array of type `decision_table`. The file includes metadata lines, followed by blocks of conditions, alternatives, and actions with associated outcomes.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `dtbl_res%name` | character (len=40) |  | name of the decision table |
| 3 |  | `dtbl_res%conds` | integer |  | number of conditions |
| 4 |  | `dtbl_res%alts` | integer |  | number of alternatives |
| 5 |  | `dtbl_res%acts` | integer |  | number of actions |
| 6 |  | `dtbl_res%cond` | type (conditions_var) |  | conditions |
| 7 |  | `dtbl_res%alt` | character(len=25) |  | condition alternatives |
| 8 |  | `dtbl_res%act` | type (actions_var) |  | actions |
| 9 |  | `dtbl_res%lu_chg_mx` | integer |  | max times lu change can occur |
| 10 |  | `dtbl_res%snow_chg_mx` | integer |  | max times snow change can occur |
| 11 |  | `dtbl_res%act_outcomes` | character(len=1) |  | action outcomes ("y" to perform action; "n" to not perform) |
| 12 |  | `dtbl_res%act_hit` | character(len=1) |  | "y" if all condition alternatives (rules) are met; "n" if not |
| 13 |  | `dtbl_res%act_typ` | integer |  | pointer to action type (ie plant, fert type, tillage implement, release type, etc) |
| 14 |  | `dtbl_res%act_app` | integer |  | pointer to operation or application type (ie harvest.ops, chem_app.ops, wier shape, etc) |
| 15 |  | `dtbl_res%con_act` | integer |  | pointer for days since last action condition to point to appropriate action |
| 16 |  | `dtbl_res%hru_lu` | integer |  | number of hru's in the land_use condition(s) - used for probabilistic mgt operations or lu change |
| 17 |  | `dtbl_res%ha_lu` | real |  | area of land_use in ha |
| 18 |  | `dtbl_res%hru_lu_cur` | integer |  | number of hru's in the land_use condition(s) that have currently been applied |
| 19 |  | `dtbl_res%hru_ha_cur` | real |  | area of land_use in ha that has currently been applied |
| 20 |  | `dtbl_res%days_prob` | integer |  | days since start of application window |
| 21 |  | `dtbl_res%day_prev` | integer |  | to check if same day - don't increment day in application window |
| 22 |  | `dtbl_res%prob_cum` | real |  | cumulative probability of application on current day of window |
| 23 |  | `dtbl_res%frac_app` | real |  | fraction of time (during each window) the application occurs |

## Sample

```text
Example snippet from a typical `res_rel.dtl` file (format inferred from reader):
Title line (80 chars)
Number of decision tables (integer)
(blank line)
Header line (80 chars)
Decision table name (char40), number of conditions (int), number of alternatives (int), number of actions (int)
Header line (80 chars)
For each condition: condition record, followed by alternatives (char25) repeated for number of alternatives
Header line (80 chars)
For each action: action record, followed by action outcomes (char1) repeated for number of alternatives
(blank line)
```

## Read Pattern

```fortran
open (107,file=in_cond%dtbl_res)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mdtbl
read (107,*,iostat=eof)
read (107,*,iostat=eof) header
read (107,*,iostat=eof) dtbl_res(i)%name, dtbl_res(i)%conds, dtbl_res(i)%alts, dtbl_res(i)%acts
read (107,*,iostat=eof) dtbl_res(i)%cond(ic), (dtbl_res(i)%alt(ic,ial), ial = 1, dtbl_res(i)%alts)
read (107,*,iostat=eof) dtbl_res(i)%act(iac), (dtbl_res(i)%act_outcomes(iac,ial), ial = 1, dtbl_res(i)%alts)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cond%dtbl_res)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mdtbl` |
| Input | `read` | 107 | `read (107,*,iostat=eof)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_res(i)%name, dtbl_res(i)%conds, dtbl_res(i)%alts, dtbl_res(i)%acts` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_res(i)%cond(ic), (dtbl_res(i)%alt(ic,ial), ial = 1, dtbl_res(i)%alts)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_res(i)%act(iac), (dtbl_res(i)%act_outcomes(iac,ial), ial = 1, dtbl_res(i)%alts)` |
| Input | `read` | 107 | `read (107,*,iostat=eof)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dtbl_res_read] | close, open, read | Reads the `res_rel.dtl` file containing decision tables for conditional management actions. It opens the file specified by `in_cond%dtbl_res`, reads header and metadata lines, allocates the `dtbl_res` array, and reads each decision table's name, conditions, alternatives, and actions. It also maps action types to indices in reservoir weir or recall databases for later use. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as the reader allocates zero-length array if the file does not exist or is set to "null".
- The reader maps action types to reservoir weir and recall database indices to link actions to model components.
- No sample data records were found in the source; the sample read format is inferred from the read statements.
