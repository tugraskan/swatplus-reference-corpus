---
kind: io
source_symbols:
- dtbl_scen_read
title: '`scen_lu.dtl`'
status: filled
source_hash: d7e842e2f70e5d92
version_label: SWAT+ 62.0.0
---

**Primary target:** `dtbl_scen(:)` (array of `type decision_table`)  
**Read by:** [sym:dtbl_scen_read]

## Bottom Line

The file `scen_lu.dtl` contains decision tables that configure conditional management scenarios in the model.

It is optional; if the file does not exist or is set to "null", no decision tables are allocated.

The reader `dtbl_scen_read` loads this file and populates the `dtbl_scen` array of `type decision_table` accordingly.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | Provides `db_mx` which contains maximum counts such as `db_mx%landuse` and `db_mx%sno` used for indexing and allocation. |
| [sym:reservoir_data_module] | No specific types or variables from this module are directly referenced in the reader. |
| [sym:landuse_data_module] | Provides `lum` array used to match land use names to indices for action types. |
| [sym:mgt_operations_module] | No specific types or variables from this module are directly referenced in the reader. |
| [sym:tillage_data_module] | No specific types or variables from this module are directly referenced in the reader. |
| [sym:fertilizer_data_module] | No specific types or variables from this module are directly referenced in the reader. |
| [sym:input_file_module] | Provides `in_cond%dtbl_scen` which is the filename string for the decision table input file. |
| [sym:conditional_module] | Provides the `type decision_table` and related types `conditions_var` and `actions_var` used to store the decision table data read from the file. |
| [sym:hru_module] | Provides `snodb` array used to match snow change names to indices for action types. |

## File Variables

The file `scen_lu.dtl` is structured as a sequence of decision tables, each with a name, counts of conditions, alternatives, and actions, followed by detailed condition and action records. Each decision table is read into an element of the `dtbl_scen` array of `type decision_table`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `dtbl_scen%name` | character (len=40) |  | name of the decision table |
| 3 |  | `dtbl_scen%conds` | integer |  | number of conditions |
| 4 |  | `dtbl_scen%alts` | integer |  | number of alternatives |
| 5 |  | `dtbl_scen%acts` | integer |  | number of actions |
| 6 |  | `dtbl_scen%cond` | type (conditions_var) |  | conditions |
| 7 |  | `dtbl_scen%alt` | character(len=25) |  | condition alternatives |
| 8 |  | `dtbl_scen%act` | type (actions_var) |  | actions |
| 9 |  | `dtbl_scen%lu_chg_mx` | integer |  | max times lu change can occur |
| 10 |  | `dtbl_scen%snow_chg_mx` | integer |  | max times snow change can occur |
| 11 |  | `dtbl_scen%act_outcomes` | character(len=1) |  | action outcomes ("y" to perform action; "n" to not perform) |
| 12 |  | `dtbl_scen%act_hit` | character(len=1) |  | "y" if all condition alternatives (rules) are met; "n" if not |
| 13 |  | `dtbl_scen%act_typ` | integer |  | pointer to action type (ie plant, fert type, tillage implement, release type, etc) |
| 14 |  | `dtbl_scen%act_app` | integer |  | pointer to operation or application type (ie harvest.ops, chem_app.ops, wier shape, etc) |
| 15 |  | `dtbl_scen%con_act` | integer |  | pointer for days since last action condition to point to appropriate action |
| 16 |  | `dtbl_scen%hru_lu` | integer |  | number of hru's in the land_use condition(s) - used for probabilistic mgt operations or lu change |
| 17 |  | `dtbl_scen%ha_lu` | real |  | area of land_use in ha |
| 18 |  | `dtbl_scen%hru_lu_cur` | integer |  | number of hru's in the land_use condition(s) that have currently been applied |
| 19 |  | `dtbl_scen%hru_ha_cur` | real |  | area of land_use in ha that has currently been applied |
| 20 |  | `dtbl_scen%days_prob` | integer |  | days since start of application window |
| 21 |  | `dtbl_scen%day_prev` | integer |  | to check if same day - don't increment day in application window |
| 22 |  | `dtbl_scen%prob_cum` | real |  | cumulative probability of application on current day of window |
| 23 |  | `dtbl_scen%frac_app` | real |  | fraction of time (during each window) the application occurs |

## Sample

```text
Example record block from `scen_lu.dtl` (format inferred from reader):
Line 1: Title line (ignored by reader)
Line 2: Number of decision tables (mdtbl)
Line 3: Blank or separator line
For each decision table (i = 1 to mdtbl):
  Line: Header line (ignored)
  Line: dtbl_scen(i)%name, dtbl_scen(i)%conds, dtbl_scen(i)%alts, dtbl_scen(i)%acts
  Line: Header line (ignored)
  For each condition (ic = 1 to dtbl_scen(i)%conds):
    Line: dtbl_scen(i)%cond(ic), dtbl_scen(i)%alt(ic,1), ..., dtbl_scen(i)%alt(ic, dtbl_scen(i)%alts)
  Line: Header line (ignored)
  For each action (iac = 1 to dtbl_scen(i)%acts):
    Line: dtbl_scen(i)%act(iac), dtbl_scen(i)%act_outcomes(iac,1), ..., dtbl_scen(i)%act_outcomes(iac, dtbl_scen(i)%alts)
  Line: Blank or separator line
```

## Read Pattern

```fortran
open (107,file=in_cond%dtbl_scen)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mdtbl
read (107,*,iostat=eof)
read (107,*,iostat=eof) header
read (107,*,iostat=eof) dtbl_scen(i)%name, dtbl_scen(i)%conds, dtbl_scen(i)%alts, dtbl_scen(i)%acts
read (107,*,iostat=eof) dtbl_scen(i)%cond(ic), (dtbl_scen(i)%alt(ic,ial), ial = 1, dtbl_scen(i)%alts)
read (107,*,iostat=eof) dtbl_scen(i)%act(iac), (dtbl_scen(i)%act_outcomes(iac,ial), ial = 1, dtbl_scen(i)%alts)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cond%dtbl_scen)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mdtbl` |
| Input | `read` | 107 | `read (107,*,iostat=eof)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_scen(i)%name, dtbl_scen(i)%conds, dtbl_scen(i)%alts, dtbl_scen(i)%acts` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_scen(i)%cond(ic), (dtbl_scen(i)%alt(ic,ial), ial = 1, dtbl_scen(i)%alts)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_scen(i)%act(iac), (dtbl_scen(i)%act_outcomes(iac,ial), ial = 1, dtbl_scen(i)%alts)` |
| Input | `read` | 107 | `read (107,*,iostat=eof)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dtbl_scen_read] | close, open, read | Reads the `scen_lu.dtl` file containing decision tables for conditional management scenarios. It opens the file specified by `in_cond%dtbl_scen`, reads the number of decision tables, and for each table reads its name, counts of conditions, alternatives, and actions, then reads the detailed condition and action records into the `dtbl_scen` array of `type decision_table`. It also cross-references action types to land use and snow database indices. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `scen_lu.dtl` is optional and may be set to "null" to disable loading.
- The reader cross-references action types to land use and snow database entries to set internal pointers.
- No sample data records were found in the source; the sample read format is inferred from the read statements.
