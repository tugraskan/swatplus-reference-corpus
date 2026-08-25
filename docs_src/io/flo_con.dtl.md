---
kind: io
source_symbols:
- dtbl_flocon_read
title: '`flo_con.dtl`'
status: filled
source_hash: bbc8ddafa2ec1aa4
version_label: SWAT+ 62.0.0
---

**Primary target:** `dtbl_flo(:)` (array of `type decision_table`)  
**Read by:** [sym:dtbl_flocon_read]

## Bottom Line

The file `flo_con.dtl` is a required input file that configures decision tables used for conditional management operations within the SWAT+ model.

It is read by the `dtbl_flocon_read` subroutine, which parses the file into an array of `decision_table` derived types (`dtbl_flo`).

These decision tables define conditions, alternatives, and actions that control land use changes, management operations, and other conditional behaviors in the model.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | Provides the `db_mx` variable, which stores the count of decision tables read (`db_mx%dtbl_flo`). |
| [sym:hydrograph_module] | Provides the `ob` array and `sp_ob` structure, used to cross-reference decision tables with objects' rulesets. |
| [sym:input_file_module] | Provides the `in_cond` structure, which contains the filename for the `flo_con.dtl` input file (`in_cond%dtbl_flo`). |
| [sym:conditional_module] | Defines the `decision_table` derived type and related types (`conditions_var`, `actions_var`) used to store the parsed data. |

## File Variables

The `flo_con.dtl` file contains multiple decision tables, each with a name, counts of conditions, alternatives, and actions, followed by detailed condition and action records. The file is read sequentially and mapped into an array of `decision_table` derived types (`dtbl_flo`).

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `dtbl_flo%name` | character (len=40) |  | name of the decision table |
| 3 |  | `dtbl_flo%conds` | integer |  | number of conditions |
| 4 |  | `dtbl_flo%alts` | integer |  | number of alternatives |
| 5 |  | `dtbl_flo%acts` | integer |  | number of actions |
| 6 |  | `dtbl_flo%cond` | type (conditions_var) |  | conditions |
| 7 |  | `dtbl_flo%alt` | character(len=25) |  | condition alternatives |
| 8 |  | `dtbl_flo%act` | type (actions_var) |  | actions |
| 9 |  | `dtbl_flo%lu_chg_mx` | integer |  | max times lu change can occur |
| 10 |  | `dtbl_flo%snow_chg_mx` | integer |  | max times snow change can occur |
| 11 |  | `dtbl_flo%act_outcomes` | character(len=1) |  | action outcomes ("y" to perform action; "n" to not perform) |
| 12 |  | `dtbl_flo%act_hit` | character(len=1) |  | "y" if all condition alternatives (rules) are met; "n" if not |
| 13 |  | `dtbl_flo%act_typ` | integer |  | pointer to action type (ie plant, fert type, tillage implement, release type, etc) |
| 14 |  | `dtbl_flo%act_app` | integer |  | pointer to operation or application type (ie harvest.ops, chem_app.ops, wier shape, etc) |
| 15 |  | `dtbl_flo%con_act` | integer |  | pointer for days since last action condition to point to appropriate action |
| 16 |  | `dtbl_flo%hru_lu` | integer |  | number of hru's in the land_use condition(s) - used for probabilistic mgt operations or lu change |
| 17 |  | `dtbl_flo%ha_lu` | real |  | area of land_use in ha |
| 18 |  | `dtbl_flo%hru_lu_cur` | integer |  | number of hru's in the land_use condition(s) that have currently been applied |
| 19 |  | `dtbl_flo%hru_ha_cur` | real |  | area of land_use in ha that has currently been applied |
| 20 |  | `dtbl_flo%days_prob` | integer |  | days since start of application window |
| 21 |  | `dtbl_flo%day_prev` | integer |  | to check if same day - don't increment day in application window |
| 22 |  | `dtbl_flo%prob_cum` | real |  | cumulative probability of application on current day of window |
| 23 |  | `dtbl_flo%frac_app` | real |  | fraction of time (during each window) the application occurs |

## Sample

```text
Example snippet from a typical `flo_con.dtl` file:
Title line (ignored): "Decision Table File for Management"
Number of tables: 2

Header line (ignored)
Table 1: "Planting", 3 conditions, 2 alternatives, 2 actions
Header line (ignored)
Condition 1 record, alternatives...
Condition 2 record, alternatives...
Condition 3 record, alternatives...
Header line (ignored)
Action 1 record, outcomes...
Action 2 record, outcomes...

Header line (ignored)
Table 2: "Fertilizer", 2 conditions, 3 alternatives, 1 action
Header line (ignored)
Condition 1 record, alternatives...
Condition 2 record, alternatives...
Header line (ignored)
Action 1 record, outcomes...
```

## Read Pattern

```fortran
open (107,file=in_cond%dtbl_flo)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mdtbl
read (107,*,iostat=eof)
read (107,*,iostat=eof) header
read (107,*,iostat=eof) dtbl_flo(i)%name, dtbl_flo(i)%conds, dtbl_flo(i)%alts, dtbl_flo(i)%acts
read (107,*,iostat=eof) dtbl_flo(i)%cond(ic), (dtbl_flo(i)%alt(ic,ial), ial = 1, dtbl_flo(i)%alts)
read (107,*,iostat=eof) dtbl_flo(i)%act(iac), (dtbl_flo(i)%act_outcomes(iac,ial), ial = 1, dtbl_flo(i)%alts)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cond%dtbl_flo)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mdtbl` |
| Input | `read` | 107 | `read (107,*,iostat=eof)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_flo(i)%name, dtbl_flo(i)%conds, dtbl_flo(i)%alts, dtbl_flo(i)%acts` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_flo(i)%cond(ic), (dtbl_flo(i)%alt(ic,ial), ial = 1, dtbl_flo(i)%alts)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_flo(i)%act(iac), (dtbl_flo(i)%act_outcomes(iac,ial), ial = 1, dtbl_flo(i)%alts)` |
| Input | `read` | 107 | `read (107,*,iostat=eof)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dtbl_flocon_read] | close, open, read | Reads the `flo_con.dtl` file, parsing multiple decision tables into the `dtbl_flo` array of `decision_table` derived types. It allocates memory dynamically based on the number of tables and their components, then cross-references the decision tables with objects' rulesets for later use in conditional management. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is required if `in_cond%dtbl_flo` is set and not "null"; otherwise, an empty allocation is made.
- The reader cross-links decision tables to objects by matching the `ruleset` string with the decision table `name`.
- No sample data lines are present in the source; the sample read format is inferred from the read pattern and typical file structure.
