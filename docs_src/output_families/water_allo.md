---
kind: output_family
source_symbols:
- header_water_allocation
- wallo_allo_output
title: water_allo_*
status: filled
source_hash: 231e6b737951eb80
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_water_allocation`](../procedures/header_water_allocation.md)  
**Written by:** [`wallo_allo_output`](../procedures/wallo_allo_output.md)  
**Primary data type:** `water_allocation_module::water_transfer_objects`  
**Files covered:** `water_allo_day`, `water_allo_mon`, `water_allo_yr`, `water_allo_aa` text/CSV pairs

## Bottom Line

`water_allo_*` is the `water_allo` constituent time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `wallo_allo_output` loops over every simulated constituent and writes **one row per (object x constituent)** for each period: the row carries the time and object-identity fields, the constituent name, and a `water_transfer_objects` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `water_allo` balance of one constituent for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several constituents, each object appears once per constituent per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `water_allo_day.txt` | `water_allo_day.csv` | 3110 | 3114 | `header_water_allocation.f90:13` |
| Monthly | `water_allo_mon.txt` | `water_allo_mon.csv` | 3111 | 3115 | `header_water_allocation.f90:30` |
| Yearly | `water_allo_yr.txt` | `water_allo_yr.csv` | 3112 | 3116 | `header_water_allocation.f90:47` |
| Average annual | `water_allo_aa.txt` | `water_allo_aa.csv` | 3113 | 3117 | `header_water_allocation.f90:64` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (db_mx%wallo_db  →  0) then  →  if (pco%water_allo%d == "y") then` | `header_water_allocation.f90:13` |
| Monthly | `if (db_mx%wallo_db  →  0) then  →  if (pco%water_allo%d == "y") then  →  if (db_` | `header_water_allocation.f90:30` |
| Yearly | `if (db_mx%wallo_db  →  0) then  →  if (pco%water_allo%d == "y") then  →  if (db_` | `header_water_allocation.f90:47` |
| Average annual | `if (db_mx%wallo_db  →  0) then  →  if (pco%water_allo%d == "y") then  →  if (db_` | `header_water_allocation.f90:64` |

The header and units rows for every file are written by `header_water_allocation`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `db_mx%wallo_db` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%water_allo%a == "y"` | aa | Enables output for this frequency. |
| `pco%water_allo%d == "y"` | All files | Enables output for this frequency. |
| `pco%water_allo%m == "y"` | mon | Enables output for this frequency. |
| `pco%water_allo%y == "y"` | aa, yr | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_water_allocation` | Basin name and program string. |
| Header row | `header_water_allocation` | Column names for time, identity, the constituent name, and the `water_transfer_objects` values. |
| Units row | `header_water_allocation` | Units for the value columns. |
| Data row | `wallo_allo_output` | One `water_transfer_objects` record for one constituent at the active frequency. |

## Columns Written

| Column | Unit | Source Field | Source-Backed Meaning |
|---|---|---|---|
| `jday` |  | `time%day` | Julian day / simulation day of the reporting period. |
| `mon` |  | `time%mo` | Simulation month. |
| `day` |  | `time%day_mo` | Day of month. |
| `yr` |  | `time%yrc` | Simulation year. |
| `unit` |  | `object index` | Index / id of the reported object. |
| `gis_id` |  | `ob(iob)%gis_id` | GIS / object id of the reported object. |
| `name` |  | `ob(iob)%name` | Object name. |
| `constituent_name` | | `cs_db constituent name` | Name of the constituent this row reports (one row per constituent). |
| `num` |  | `wallo%trn(i)%num` | transfer object number |
| `ch_src` |  | `wallo%trn(i)%ch_src` | channel number in transfer object (0 if no channel) |
| `trn_typ` |  | `wallo%trn(i)%trn_typ` | transfer type - decision table, recall, ave daily |
| `trn_typ_name` |  | `wallo%trn(i)%trn_typ_name` | transfer type name of table or recall |
| `dtbl_num` |  | `wallo%trn(i)%dtbl_num` | number of decision table for demand amount (if used) |
| `dtbl_lum` |  | `wallo%trn(i)%dtbl_lum` | number of decision table for demand amount for irrigation (if used) |
| `rec_num` |  | `wallo%trn(i)%rec_num` | number of recall file for demand amount (if used) |
| `amount` |  | `wallo%trn(i)%amount` | m3 per day for urban objects and mm for hru |
| `right` |  | `wallo%trn(i)%right` | water right (sr -senior or jr - junior right) |
| `src_num` |  | `wallo%trn(i)%src_num` | number of source objects |
| `dtbl_src` |  | `wallo%trn(i)%dtbl_src` | decision table name to allocate sources |
| `dtbl_src_num` |  | `wallo%trn(i)%dtbl_src_num` | number of source allocation decision table |
| `src` |  | `wallo%trn(i)%src` | sequential source objects as listed in wallo object |
| `osrc` |  | `wallo%trn(i)%osrc` | number of outside basin source object - recall_db.rec file |
| `rcv_num` |  | `wallo%trn(i)%rcv_num` | number of receiving objects |
| `rcv` |  | `wallo%trn(i)%rcv` | character (len=25) :: dtbl_rcv = "" decision table name to allocate receiving objects receiving object |
| `unmet_m3` | m3 | `wallo%trn(i)%unmet_m3` | unmet demand for the object |
| `withdr_tot` | m3 | `wallo%trn(i)%withdr_tot` | total withdrawal of demand object from all sources |
| `irr_eff` |  | `wallo%trn(i)%irr_eff` | irrigation in-field efficiency |
| `surq` |  | `wallo%trn(i)%surq` | surface runoff ratio |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `water_transfer_objects` record for one constituent. `wallo_allo_output` loops over the simulated constituents (`cs_db constituent list`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated constituent.
2. If the frequency's print flag is on, write that constituent's current `water_transfer_objects` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `wallo_allo_output.f90:24` | `3110` | time, identity, constituent name, one `water_transfer_objects` record |
| `wallo_allo_output.f90:30` | `3114` | time, identity, constituent name, one `water_transfer_objects` record |
| `wallo_allo_output.f90:50` | `3111` | time, identity, constituent name, one `water_transfer_objects` record |
| `wallo_allo_output.f90:56` | `3115` | time, identity, constituent name, one `water_transfer_objects` record |
| `wallo_allo_output.f90:78` | `3112` | time, identity, constituent name, one `water_transfer_objects` record |
| `wallo_allo_output.f90:84` | `3116` | time, identity, constituent name, one `water_transfer_objects` record |
| `wallo_allo_output.f90:105` | `3113` | time, identity, constituent name, one `water_transfer_objects` record |
| `wallo_allo_output.f90:111` | `3117` | time, identity, constituent name, one `water_transfer_objects` record |

Header and file-open statements are in `header_water_allocation`.

## Review Notes

- Every frequency shares the `water_transfer_objects` layout; the Columns Written table applies to all files in the family.
- Rows repeat per constituent: an object with N simulated constituents produces N rows per period.
- Column names, units, and meanings are taken from the `water_transfer_objects` type definition in `water_allocation_module`.
- Auto-derived from the writer's per-constituent output type; prose sections may benefit from human review.

## Source Links

- Writer: [`wallo_allo_output`](../procedures/wallo_allo_output.md)
- Header / opener: [`header_water_allocation`](../procedures/header_water_allocation.md)
- Data type: `water_allocation_module::water_transfer_objects`

## Evidence Used

- `wallo_allo_output.f90`
- `header_water_allocation.f90`
- `water_allocation_module.f90` (`type water_transfer_objects`)
