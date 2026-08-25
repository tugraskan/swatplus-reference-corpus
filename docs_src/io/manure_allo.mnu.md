---
kind: io
source_symbols:
- manure_allocation_read
title: '`manure_allo.mnu`'
status: filled
source_hash: 9f8f8a7869a42e3e
version_label: SWAT+ 62.0.0
---

**Primary target:** `mallo(:)` (array of `type manure_allocation`)  
**Read by:** [sym:manure_allocation_read]

## Bottom Line

The `manure_allo.mnu` input file configures manure allocation objects, specifying sources and demand objects for manure management in the model.

It is optional; if the file does not exist or is named "null", the allocation array is allocated empty.

The file is read by the `manure_allocation_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides general input file utilities and possibly constants used during reading. |
| [sym:manure_allocation_module] | Defines the `manure_allocation` derived type and related types such as `source_manure_output`, `manure_source_objects`, and `manure_demand_objects` used to store the file data. |
| [sym:mgt_operations_module] | Used for management operation data structures or constants referenced during reading or crosswalks. |
| [sym:maximum_data_module] | Provides maximum database sizes and global counters such as `db_mx` used for indexing and allocation. |
| [sym:hydrograph_module] | Likely used for hydrologic or spatial referencing related to manure source or demand objects. |
| [sym:sd_channel_module] | Possibly used for channel or spatial data related to manure transport or allocation. |
| [sym:conditional_module] | Used for conditional logic or flags during reading or data validation. |
| [sym:hru_module] | Provides the `hru` type and variables; used to crosswalk manure allocation demand objects to HRU irrigation decision tables. |

## File Variables

The `manure_allo.mnu` file contains records defining manure allocation objects, each with a name, allocation rule type, and counts of source and demand objects. Each source and demand object has detailed attributes read into nested derived types within the main `manure_allocation` type.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `mallo%name` | character (len=25) |  | name of the water allocation object |
| 3 |  | `mallo%rule_typ` | character (len=25) |  | rule type to allocate water |
| 4 |  | `mallo%src_obs` | integer |  | number of source objects |
| 5 |  | `mallo%trn_obs` | integer |  | number of demand objects |
| 6 |  | `mallo%tot` | type (source_manure_output) |  | total demand, withdrawal and unmet for entire allocation object |
| 7 |  | `mallo%src` | type (manure_source_objects) |  | dimension by source objects |
| 8 |  | `mallo%trn` | type (manure_demand_objects) |  | dimension by demand objects |

## Sample

```text
Example record block from manure_allo.mnu:
Manure Allocation Title Line
2
Header line for allocation object 1
AllocationName1 RuleType1 3 2
Header line for source objects
1 1 ManureTypeA 35.0 -90.0 100.0 500.0 12
2 2 ManureTypeB 36.0 -91.0 50.0 300.0 10
3 1 ManureTypeC 35.5 -90.5 75.0 400.0 11
Header line for demand objects
1 hru 101 dtbl1 right
2 hru 102 dtbl2 right
```

## Read Pattern

```fortran
open (107,file="manure_allo.mnu")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) mallo(imro)%name, mallo(imro)%rule_typ, mallo(imro)%src_obs, mallo(imro)%trn_obs
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
backspace (107)
read (107,*,iostat=eof) k, mallo(imro)%src(i)%mois_typ, mallo(imro)%src(i)%manure_typ, mallo(imro)%src(i)%lat, mallo(imro)%src(i)%long, mallo(imro)%src(i)%stor_init, mallo(imro)%src(i)%stor_max, mallo(imro)%src(i)%prod_mon
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
backspace (107)
read (107,*,iostat=eof) k, mallo(imro)%trn(i)%ob_typ, mallo(imro)%trn(i)%ob_num, mallo(imro)%trn(i)%dtbl, mallo(imro)%trn(i)%right
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="manure_allo.mnu")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mallo(imro)%name, mallo(imro)%rule_typ, mallo(imro)%src_obs, mallo(imro)%trn_obs` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, mallo(imro)%src(i)%mois_typ, mallo(imro)%src(i)%manure_typ, mallo(imro)%src(i)%lat, mallo(imro)%src(i)%long, mallo(imro)%src(i)%stor_init, mallo(imro)%src(i)%stor_max, mallo(imro)%src(i)%prod_mon` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, mallo(imro)%trn(i)%ob_typ, mallo(imro)%trn(i)%ob_num, mallo(imro)%trn(i)%dtbl, mallo(imro)%trn(i)%right` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:manure_allocation_read] | backspace, close, open, read | Reads the `manure_allo.mnu` file to populate the array `mallo` of manure allocation objects, including their source and demand objects, crosswalking manure types to fertilizer database entries and linking demand objects to HRU irrigation decision tables. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or named "null", an empty allocation array is allocated.
- The reader crosswalks manure types to fertilizer database entries and links demand objects to HRU irrigation decision tables and chemical application methods.
- Sample record format is inferred from read statements and variable names; no official example provided in source.
