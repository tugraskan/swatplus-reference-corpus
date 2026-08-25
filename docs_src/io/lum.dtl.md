---
kind: io
source_symbols:
- dtbl_lum_read
title: '`lum.dtl`'
status: filled
source_hash: d56117712a4eaae0
version_label: SWAT+ 62.0.0
---

**Primary target:** `dtbl_lum(:)` (array of `type decision_table`)  
**Read by:** [sym:dtbl_lum_read]

## Bottom Line

The file `lum.dtl` is an optional input file that configures decision tables for land use management and conditional actions within SWAT+. It is read by the `dtbl_lum_read` subroutine, which parses and stores the data into the `dtbl_lum` array of `type decision_table`.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | Provides `db_mx` which contains database size limits and counters used for cross-walking action types and pointers. |
| [sym:reservoir_data_module] | No direct variables or types used from this module in the reader. |
| [sym:landuse_data_module] | Provides `lum` array used for cross-walking land use change actions by name. |
| [sym:mgt_operations_module] | Provides `harvop_db` and `fire_db` used for cross-walking harvest and burn operation types. |
| [sym:tillage_data_module] | Provides `tillop_db` used for cross-walking tillage operation types. |
| [sym:fertilizer_data_module] | Provides `fertdb` used for cross-walking fertilizer names. |
| [sym:input_file_module] | Provides `in_cond%dtbl_lum` which is the filename string for `lum.dtl`. |
| [sym:conditional_module] | Defines the `type decision_table` and related types `conditions_var` and `actions_var` used to store the file data. |
| [sym:pesticide_data_module] | Provides `cs_db` which contains pest names used for cross-walking pest application actions. |
| [sym:plant_data_module] | Provides `transpl` array used for cross-walking planting/transplanting actions. |
| [sym:constituent_mass_module] | No direct variables or types used from this module in the reader. |
| [sym:hydrograph_module] | Provides `sp_ob` which contains the number of HRUs used to count land use HRUs in conditions. |
| [sym:hru_module] | Provides `hru` array used to determine HRUs and areas matching land use conditions, and `snodb` used for snow change actions. |

## File Variables

The `lum.dtl` file contains decision tables that define conditional management actions and land use changes. Each record corresponds to a decision table stored as an element of the `dtbl_lum` array of `type decision_table` in Fortran. The file is parsed sequentially, reading metadata, conditions, alternatives, and actions with their associated attributes.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `dtbl_lum%name` | character (len=40) |  | name of the decision table |
| 3 |  | `dtbl_lum%conds` | integer |  | number of conditions |
| 4 |  | `dtbl_lum%alts` | integer |  | number of alternatives |
| 5 |  | `dtbl_lum%acts` | integer |  | number of actions |
| 6 |  | `dtbl_lum%cond` | type (conditions_var) |  | conditions |
| 7 |  | `dtbl_lum%alt` | character(len=25) |  | condition alternatives |
| 8 |  | `dtbl_lum%act` | type (actions_var) |  | actions |
| 9 |  | `dtbl_lum%lu_chg_mx` | integer |  | max times lu change can occur |
| 10 |  | `dtbl_lum%snow_chg_mx` | integer |  | max times snow change can occur |
| 11 |  | `dtbl_lum%act_outcomes` | character(len=1) |  | action outcomes ("y" to perform action; "n" to not perform) |
| 12 |  | `dtbl_lum%act_hit` | character(len=1) |  | "y" if all condition alternatives (rules) are met; "n" if not |
| 13 |  | `dtbl_lum%act_typ` | integer |  | pointer to action type (ie plant, fert type, tillage implement, release type, etc) |
| 14 |  | `dtbl_lum%act_app` | integer |  | pointer to operation or application type (ie harvest.ops, chem_app.ops, wier shape, etc) |
| 15 |  | `dtbl_lum%con_act` | integer |  | pointer for days since last action condition to point to appropriate action |
| 16 |  | `dtbl_lum%hru_lu` | integer |  | number of hru's in the land_use condition(s) - used for probabilistic mgt operations or lu change |
| 17 |  | `dtbl_lum%ha_lu` | real |  | area of land_use in ha |
| 18 |  | `dtbl_lum%hru_lu_cur` | integer |  | number of hru's in the land_use condition(s) that have currently been applied |
| 19 |  | `dtbl_lum%hru_ha_cur` | real |  | area of land_use in ha that has currently been applied |
| 20 |  | `dtbl_lum%days_prob` | integer |  | days since start of application window |
| 21 |  | `dtbl_lum%day_prev` | integer |  | to check if same day - don't increment day in application window |
| 22 |  | `dtbl_lum%prob_cum` | real |  | cumulative probability of application on current day of window |
| 23 |  | `dtbl_lum%frac_app` | real |  | fraction of time (during each window) the application occurs |

## Sample

```text
Example record block from lum.dtl (format inferred from reader):
Title line (ignored)
Number of decision tables (mdtbl)
Blank line
Header line (ignored)
For each decision table i = 1 to mdtbl:
  Header line (ignored)
  dtbl_lum(i)%name, dtbl_lum(i)%conds, dtbl_lum(i)%alts, dtbl_lum(i)%acts
  Header line (ignored)
  For each condition ic = 1 to dtbl_lum(i)%conds:
    dtbl_lum(i)%cond(ic), dtbl_lum(i)%alt(ic,1), ..., dtbl_lum(i)%alt(ic, dtbl_lum(i)%alts)
    (If dtbl_lum(i)%cond(ic)%var == "prob_unif", then next line reads dtbl_lum(i)%cond(ic)%var and dtbl_lum(i)%frac_app)
  Header line (ignored)
  For each action iac = 1 to dtbl_lum(i)%acts:
    dtbl_lum(i)%act(iac), dtbl_lum(i)%act_outcomes(iac,1), ..., dtbl_lum(i)%act_outcomes(iac, dtbl_lum(i)%alts)
```

## Read Pattern

```fortran
open (107,file=in_cond%dtbl_lum)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mdtbl
read (107,*,iostat=eof)
read (107,*,iostat=eof) header
read (107,*,iostat=eof) dtbl_lum(i)%name, dtbl_lum(i)%conds, dtbl_lum(i)%alts, dtbl_lum(i)%acts
read (107,*,iostat=eof) dtbl_lum(i)%cond(ic), (dtbl_lum(i)%alt(ic,ial), ial = 1, dtbl_lum(i)%alts)
backspace (107)
read (107,*,iostat=eof) dtbl_lum(i)%cond(ic)%var, dtbl_lum(i)%frac_app
read (107,*,iostat=eof) dtbl_lum(i)%act(iac), (dtbl_lum(i)%act_outcomes(iac,ial), ial = 1, dtbl_lum(i)%alts)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_cond%dtbl_lum)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mdtbl` |
| Input | `read` | 107 | `read (107,*,iostat=eof)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_lum(i)%name, dtbl_lum(i)%conds, dtbl_lum(i)%alts, dtbl_lum(i)%acts` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_lum(i)%cond(ic), (dtbl_lum(i)%alt(ic,ial), ial = 1, dtbl_lum(i)%alts)` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_lum(i)%cond(ic)%var, dtbl_lum(i)%frac_app` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dtbl_lum(i)%act(iac), (dtbl_lum(i)%act_outcomes(iac,ial), ial = 1, dtbl_lum(i)%alts)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dtbl_lum_read] | backspace, close, open, read | Reads the `lum.dtl` file containing decision tables for land use and management actions. It allocates and populates the `dtbl_lum` array of `type decision_table` by reading metadata, conditions, alternatives, and actions, and performs cross-walking of action names to internal database indices for planting, harvesting, tillage, fertilization, pest application, grazing, burning, land use change, and snow change operations. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `lum.dtl` is optional as indicated by the existence check and allocation of zero-length array if missing or set to 'null'.
- Cross-walking of action types to internal database indices is extensive and covers many management operation types.
- No sample data block was found in the source; the sample read format is inferred from the reading sequence and loop structure.
