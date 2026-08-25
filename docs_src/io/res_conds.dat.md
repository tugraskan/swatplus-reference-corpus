---
kind: io
source_symbols:
- res_read_conds
title: '`res_conds.dat`'
status: filled
source_hash: c138d643285a6a65
version_label: SWAT+ 62.0.0
---

**Primary target:** `ctbl(:)` (array of `type reservoir_condition_tables`)  
**Read by:** [sym:res_read_conds]

## Bottom Line

The file `res_conds.dat` defines reservoir condition tables used to configure reservoir behavior in the model.

It is optional; if the file does not exist, the reader `res_read_conds` simply returns without error.

The reader `res_read_conds` loads this file and populates the array `ctbl` of type `reservoir_condition_tables`.

| Module | Role for this file |
| --- | --- |
| [sym:reservoir_conditions_module] | Provides the derived type `reservoir_condition_tables` and its components such as `conds` and `mods` where the file data is stored. |
| [sym:maximum_data_module] | Provides the global variable `db_mx` whose member `ctbl_res` is set to the number of condition tables read from the file. |

## File Variables

The file `res_conds.dat` contains multiple reservoir condition tables, each with a name, counts of conditions and modules, and nested condition and module data structures. The reader maps each table into an element of the `ctbl` array of `type reservoir_condition_tables`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ctbl%name` | character(25) |  | The name identifier of the reservoir condition table. |
| 3 |  | `ctbl%num_tbl` | integer |  | Number of tables (not directly used per record; overall count stored separately). |
| 4 |  | `ctbl%num_conds` | integer |  | Number of conditions in this reservoir condition table. |
| 5 |  | `ctbl%num_modules` | integer |  | Number of modules in this reservoir condition table. |
| 6 |  | `ctbl%conds` | type (conditions) |  | Array of condition structures, each containing subconditions and actions. |
| 7 |  | `ctbl%mods` | type (modules) |  | Array of module structures, each containing conditions with subconditions and actions. |

## Sample

```text
Example snippet from `res_conds.dat` (from source reading pattern):
Title line (string)
Number of tables (integer)
For each table:
  Name (string), Number of conditions (integer), Number of modules (integer)
  For each condition:
    Number of subconditions (integer)
    Condition details: Number of conditions, list of subcondition IDs, action code
  For each module:
    Number of conditions (integer)
    For each condition:
      Number of subconditions (integer)
      Condition details: Number of conditions, list of subcondition IDs, action code
```

## Read Pattern

```fortran
open (100,file="res_conds.dat")
read (100,*,iostat=eof) title
read (100,*,iostat=eof) max_table
read (100,*) ctbl(ictbl)%name, ctbl(ictbl)%num_conds, ctbl(ictbl)%num_modules
read (100,*) isub_con
backspace (100)
read (100,*) ctbl(ictbl)%conds(ii)%num_conds, (ctbl(ictbl)%conds(ii)%scon(icc), icc = 1, isub_con), ctbl(ictbl)%conds(ii)%action
read (100,*) tnum_conds
read (100,*) ctbl(ictbl)%mods(imod)%con(ii)%num_conds, (ctbl(ictbl)%mods(imod)%con(ii)%scon(icc), icc = 1, isub_con), ctbl(ictbl)%mods(imod)%con(ii)%action
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 100 | `open (100,file="res_conds.dat")` |
| Input | `read` | 100 | `read (100,*,iostat=eof) title` |
| Input | `read` | 100 | `read (100,*,iostat=eof) max_table` |
| Input | `read` | 100 | `read (100,*) ctbl(ictbl)%name, ctbl(ictbl)%num_conds, ctbl(ictbl)%num_modules` |
| Input | `read` | 100 | `read (100,*) isub_con` |
| File control | `backspace` | 100 | `backspace (100)` |
| Input | `read` | 100 | `read (100,*) ctbl(ictbl)%conds(ii)%num_conds, (ctbl(ictbl)%conds(ii)%scon(icc), icc = 1, isub_con), ctbl(ictbl)%conds(ii)%action` |
| Input | `read` | 100 | `read (100,*) tnum_conds` |
| Input | `read` | 100 | `read (100,*) isub_con` |
| File control | `backspace` | 100 | `backspace (100)` |
| Input | `read` | 100 | `read (100,*) ctbl(ictbl)%mods(imod)%con(ii)%num_conds, (ctbl(ictbl)%mods(imod)%con(ii)%scon(icc), icc = 1, isub_con), ctbl(ictbl)%mods(imod)%con(ii)%action` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_conds] | backspace, open, read | Reads the file `res_conds.dat` if it exists, allocates and populates the array `ctbl` of reservoir condition tables, including nested conditions and modules with their subconditions and actions. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
