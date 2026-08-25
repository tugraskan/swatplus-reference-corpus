---
kind: io
source_symbols:
- water_allocation_read
title: '`water_allocation.wro`'
status: filled
source_hash: c201ac9202a13508
version_label: SWAT+ 62.0.0
---

**Primary target:** `wallo(:)` (array of `type water_allocation`)  
**Read by:** [sym:water_allocation_read]

## Bottom Line

The `water_allocation.wro` input file configures water allocation objects and their associated transfer objects used in the SWAT+ model to manage water distribution rules and sources.

This file is optional and is read by the `water_allocation_read` subroutine.

It defines water allocation rules, transfer object counts, and detailed transfer object parameters including source and receiving information.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file path variable `in_watrts%transfer_wro` used to locate the water allocation input file. |
| [sym:water_allocation_module] | Defines the `type water_allocation` and related types such as `water_transfer_objects` used to store the water allocation data read from the file. |
| [sym:mgt_operations_module] | Used for management operation data structures that are allocated alongside water allocation objects (e.g., `wal_omd`, `wal_omm`, `wal_omy`, `wal_oma`). |
| [sym:maximum_data_module] | Provides maximum database sizes and counters such as `db_mx%wallo_db`, `db_mx%dtbl_lum`, `db_mx%irrop_db`, and `db_mx%dtbl_flo` used for cross-referencing decision tables. |
| [sym:hydrograph_module] | Used for hydrological graph data structures related to water allocation outputs (e.g., `wallod_out`, `wallom_out`, `walloy_out`, `walloa_out`). |
| [sym:sd_channel_module] | Used for channel-related data referenced in water allocation transfer sources (e.g., checking if a source is a channel). |
| [sym:conditional_module] | Used for conditional logic and decision tables referenced during reading and crosswalks with transfer objects. |
| [sym:constituent_mass_module] | Used for constituent mass data structures allocated per transfer object source. |
| [sym:recall_module] | Provides the `recall_db` used to crosswalk and assign sequential numbers for outside sources (`osrc`). |
| [sym:exco_module] | Provides the `exco_db` and `exco_om_name` used to crosswalk and assign sequential numbers for outside sources with attribute `osrc_a`. |
| [sym:hru_module] | Provides the `hru` type used to identify HRU numbers for irrigation demand decision table crosswalks. |

## File Variables

The `water_allocation.wro` file contains records defining water allocation objects, each with a name, allocation rule type, and a number of transfer objects. Each transfer object includes detailed parameters such as type, amount, rights, source counts, and source/receiver information. The file is parsed into an array of `type water_allocation` instances (`wallo`).

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wallo%name` | character (len=25) |  | name of the water allocation object |
| 3 |  | `wallo%rule_typ` | character (len=25) |  | rule type to allocate water |
| 4 |  | `wallo%trn_cur` | integer |  | current transfer object |
| 5 |  | `wallo%trn_obs` | integer |  | number of transfer objects |
| 6 |  | `wallo%tot` | type (source_output) |  | total demand, withdrawal and unmet for entire allocation object |
| 7 |  | `wallo%trn` | type (water_transfer_objects) |  | dimension by transfer objects |

## Sample

```text
Example snippet from `water_allocation.wro` (format inferred from reader):
Title line (ignored): "Water Allocation Transfer Objects"
Number of water allocation objects: 2

Header line (ignored)
Object 1: "Irrigation", "rule1", 3
Header line (ignored)
Transfer object 1: 1, "dtbl_lum", "IrrigationDemand", 100.0, 1, 2
Transfer object 2: 2, "dtbl_con", "FlowControl", 50.0, 0, 1
Transfer object 3: 3, "other", "OtherType", 75.0, 1, 1

Header line (ignored)
Object 2: "Urban", "rule2", 1
Header line (ignored)
Transfer object 1: 1, "dtbl_con", "UrbanFlow", 200.0, 1, 1
```

## Read Pattern

```fortran
open (107,file=in_watrts%transfer_wro)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) wallo(iwro)%name, wallo(iwro)%rule_typ, wallo(iwro)%trn_obs
read (107,*,iostat=eof) i
backspace (107)
read (107,*,iostat=eof) k, wallo(iwro)%trn(i)%trn_typ, wallo(iwro)%trn(i)%trn_typ_name, wallo(iwro)%trn(i)%amount, wallo(iwro)%trn(i)%right, wallo(iwro)%trn(i)%src_num
read (107,*,iostat=eof) k, wallo(iwro)%trn(i)%trn_typ, wallo(iwro)%trn(i)%trn_typ_name, wallo(iwro)%trn(i)%amount, wallo(iwro)%trn(i)%right, wallo(iwro)%trn(i)%src_num, wallo(iwro)%trn(i)%dtbl_src, (wallo(iwro)%trn(i)%src(isrc), isrc = 1, num_src), wallo(iwro)%trn(i)%rcv
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_watrts%transfer_wro)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) wallo(iwro)%name, wallo(iwro)%rule_typ, wallo(iwro)%trn_obs` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, wallo(iwro)%trn(i)%trn_typ, wallo(iwro)%trn(i)%trn_typ_name, wallo(iwro)%trn(i)%amount, wallo(iwro)%trn(i)%right, wallo(iwro)%trn(i)%src_num` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, wallo(iwro)%trn(i)%trn_typ, wallo(iwro)%trn(i)%trn_typ_name, wallo(iwro)%trn(i)%amount, wallo(iwro)%trn(i)%right, wallo(iwro)%trn(i)%src_num, wallo(iwro)%trn(i)%dtbl_src, (wallo(iwro)%trn(i)%src(isrc), isrc = 1, num_src), wallo(iwro)%trn(i)%rcv` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:water_allocation_read] | backspace, close, open, read | Reads the `water_allocation.wro` file to populate the array `wallo` of water allocation objects. It opens the file, reads the number of water allocation objects, allocates arrays accordingly, and then reads each object's name, rule type, and number of transfer objects. For each transfer object, it reads detailed parameters including type, amount, rights, source counts, and source and receiver information. It also crosswalks transfer objects with decision tables and external databases such as recall and exco to assign additional metadata. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
