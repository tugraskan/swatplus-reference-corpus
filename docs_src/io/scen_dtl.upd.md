---
kind: io
source_symbols:
- cal_cond_read
title: '`scen_dtl.upd`'
status: filled
source_hash: d4f3daac7d440b56
version_label: SWAT+ 62.0.0
---

**Primary target:** `upd_cond(:)` (array of `type update_conditional`)  
**Read by:** [sym:cal_cond_read]

## Bottom Line

The file `scen_dtl.upd` configures scenario update tables that define conditional parameter changes during a simulation.

It is optional; if missing or named "null", an empty update list is allocated.

The reader `cal_cond_read` loads this file, storing data into the `upd_cond` array of `type update_conditional`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides general input file utilities and possibly global input variables used by `cal_cond_read`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable which stores maximum data counts, including `cond_up` and `dtbl_scen` used for indexing and crosswalk. |
| [sym:calibration_data_module] | Defines the `type update_conditional` and the `upd_cond` array where the file data is stored. |
| [sym:conditional_module] | Provides the `dtbl_scen` array of decision tables used to cross-reference the `dtbl` string read from the file and assign `cond_num`. |

## File Variables

The file consists of a header title line, a count of update tables, a header line, and then multiple records each describing an update conditional table with fields for maximum executions, type, and decision table name. These map to the `upd_cond` array of `type update_conditional`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `upd_cond%max_hits` | integer |  | maximum number of times the table will be executed |
| 3 |  | `upd_cond%num_hits` | integer |  | current number of times the table will be executed |
| 4 |  | `upd_cond%typ` | character(len=25) |  | type of table- "lu_change" checks all hru; "hru_fr_change" sets all hru fractions |
| 5 |  | `upd_cond%dtbl` | character(len=25) |  | points to ruleset in conditional.ctl for scheduling the update |
| 6 |  | `upd_cond%cond_num` | integer |  | integer pointer to d_table in conditional.ctl |

## Sample

```text
Example contents of scen_dtl.upd:
Title of update scenario file
3
Header line describing columns
5 lu_change scenario1
10 hru_fr_change scenario2
7 lu_change scenario3
```

## Read Pattern

```fortran
open (107,file="scen_dtl.upd")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) num_dtls
read (107,*,iostat=eof) header
read (107,*,iostat=eof) upd_cond(i)%max_hits, upd_cond(i)%typ, upd_cond(i)%dtbl
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="scen_dtl.upd")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) num_dtls` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) upd_cond(i)%max_hits, upd_cond(i)%typ, upd_cond(i)%dtbl` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cal_cond_read] | open, read | Reads the scenario update file `scen_dtl.upd` if it exists, parsing the number of update tables and their parameters into the `upd_cond` array. It cross-references each update's decision table name with the `dtbl_scen` array from `conditional_module` to assign an integer pointer `cond_num` for scheduling updates. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or named "null", an empty update list is allocated.
- The `num_hits` field of `upd_cond` is not read from the file but presumably managed elsewhere.
- The crosswalk loop matches the `dtbl` string to `dtbl_scen` names to assign `cond_num` for internal indexing.
