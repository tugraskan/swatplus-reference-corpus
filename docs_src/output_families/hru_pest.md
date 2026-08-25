---
kind: output_family
source_symbols:
- header_pest
- hru_pesticide_output
title: hru_pest_*
status: filled
source_hash: 865f340607d7ac88
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_pest`](../procedures/header_pest.md)  
**Written by:** [`hru_pesticide_output`](../procedures/hru_pesticide_output.md)  
**Primary data type:** `output_ls_pesticide_module::pesticide_balance`  
**Files covered:** `hru_pest_day`, `hru_pest_mon`, `hru_pest_yr`, `hru_pest_aa` text/CSV pairs

## Bottom Line

`hru_pest_*` is the `hru_pest` pesticide time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `hru_pesticide_output` loops over every simulated pesticide and writes **one row per (object x pesticide)** for each period: the row carries the time and object-identity fields, the pesticide name, and a `pesticide_balance` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `hru_pest` balance of one pesticide for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several pesticides, each object appears once per pesticide per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hru_pest_day.txt` | `hru_pest_day.csv` | 2800 | 2804 | `header_pest.f90:18` |
| Monthly | `hru_pest_mon.txt` | `hru_pest_mon.csv` | 2801 | 2805 | `header_pest.f90:33` |
| Yearly | `hru_pest_yr.txt` | `hru_pest_yr.csv` | 2802 | 2806 | `header_pest.f90:48` |
| Average annual | `hru_pest_aa.txt` | `hru_pest_aa.csv` | 2803 | 2807 | `header_pest.f90:63` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (sp_ob%hru  →  0) then  →  if (pco%pest%d == "y" .and. cs_db%num_tot  →  0) t` | `header_pest.f90:18` |
| Monthly | `if (sp_ob%hru  →  0) then  →  if (pco%pest%m == "y" .and. cs_db%num_tot  →  0 ) ` | `header_pest.f90:33` |
| Yearly | `if (sp_ob%hru  →  0) then  →  if (pco%pest%y == "y" .and. cs_db%num_tot  →  0) t` | `header_pest.f90:48` |
| Average annual | `if (sp_ob%hru  →  0) then  →  if (pco%pest%a == "y" .and. cs_db%num_tot  →  0) t` | `header_pest.f90:63` |

The header and units rows for every file are written by `header_pest`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%pest%a == "y" .and. cs_db%num_tot` | aa | Enables output for this frequency. |
| `pco%pest%d == "y" .and. cs_db%num_tot` | day | Enables output for this frequency. |
| `pco%pest%m == "y" .and. cs_db%num_tot` | mon | Enables output for this frequency. |
| `pco%pest%y == "y" .and. cs_db%num_tot` | yr | Enables output for this frequency. |
| `sp_ob%hru` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_pest` | Basin name and program string. |
| Header row | `header_pest` | Column names for time, identity, the pesticide name, and the `pesticide_balance` values. |
| Units row | `header_pest` | Units for the value columns. |
| Data row | `hru_pesticide_output` | One `pesticide_balance` record for one pesticide at the active frequency. |

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
| `pesticide_name` | | `cs_db%pests(ipest)` | Name of the pesticide this row reports (one row per pesticide). |
| `plant` |  | `hpestb_d%pest(i)%plant` | character(len=10) :: name integer :: num_db pesticide on plant foliage |
| `soil` | kg/ha | `hpestb_d%pest(i)%soil` | pesticide in soil |
| `sed` | kg/ha | `hpestb_d%pest(i)%sed` | pesticide loading from HRU sorbed onto sediment |
| `surq` | kg/ha | `hpestb_d%pest(i)%surq` | amount of pesticide type lost in surface runoff in HRU |
| `latq` | kg/ha | `hpestb_d%pest(i)%latq` | amount of pesticide in lateral flow in HRU |
| `tileq` | kg/ha | `hpestb_d%pest(i)%tileq` | amount of pesticide in tile flow in HRU |
| `perc` | kg/ha | `hpestb_d%pest(i)%perc` | amount of pesticide leached past bottom of soil |
| `apply_s` | kg/ha | `hpestb_d%pest(i)%apply_s` | amount of pesticide applied on soil |
| `apply_f` | kg/ha | `hpestb_d%pest(i)%apply_f` | amount of pesticide applied on foliage |
| `decay_s` | kg/ha | `hpestb_d%pest(i)%decay_s` | amount of pesticide decayed on soil |
| `decay_f` | kg/ha | `hpestb_d%pest(i)%decay_f` | amount of pesticide decayed on foliage |
| `wash` | kg/ha | `hpestb_d%pest(i)%wash` | amount of pesticide washed off from plant to soil |
| `metab_s` | kg/ha | `hpestb_d%pest(i)%metab_s` | amount of pesticide metabolized from parent in soil |
| `metab_f` | kg/ha | `hpestb_d%pest(i)%metab_f` | amount of pesticide metabolized from parent on foilage |
| `pl_uptake` | kg/ha | `hpestb_d%pest(i)%pl_uptake` | amount of pesticide taken up by plants |
| `in_plant` | kg/ha | `hpestb_d%pest(i)%in_plant` | pesticide in plant foliage |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `pesticide_balance` record for one pesticide. `hru_pesticide_output` loops over the simulated pesticides (`cs_db%pests(ipest)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated pesticide.
2. If the frequency's print flag is on, write that pesticide's current `pesticide_balance` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hru_pesticide_output.f90:35` | `2800` | time, identity, pesticide name, one `pesticide_balance` record |
| `hru_pesticide_output.f90:38` | `2804` | time, identity, pesticide name, one `pesticide_balance` record |
| `hru_pesticide_output.f90:54` | `2801` | time, identity, pesticide name, one `pesticide_balance` record |
| `hru_pesticide_output.f90:57` | `2805` | time, identity, pesticide name, one `pesticide_balance` record |
| `hru_pesticide_output.f90:73` | `2802` | time, identity, pesticide name, one `pesticide_balance` record |
| `hru_pesticide_output.f90:76` | `2806` | time, identity, pesticide name, one `pesticide_balance` record |
| `hru_pesticide_output.f90:87` | `2803` | time, identity, pesticide name, one `pesticide_balance` record |
| `hru_pesticide_output.f90:90` | `2807` | time, identity, pesticide name, one `pesticide_balance` record |

Header and file-open statements are in `header_pest`.

## Review Notes

- Every frequency shares the `pesticide_balance` layout; the Columns Written table applies to all files in the family.
- Rows repeat per pesticide: an object with N simulated pesticides produces N rows per period.
- Column names, units, and meanings are taken from the `pesticide_balance` type definition in `output_ls_pesticide_module`.
- Auto-derived from the writer's per-pesticide output type; prose sections may benefit from human review.

## Source Links

- Writer: [`hru_pesticide_output`](../procedures/hru_pesticide_output.md)
- Header / opener: [`header_pest`](../procedures/header_pest.md)
- Data type: `output_ls_pesticide_module::pesticide_balance`

## Evidence Used

- `hru_pesticide_output.f90`
- `header_pest.f90`
- `output_ls_pesticide_module.f90` (`type pesticide_balance`)
