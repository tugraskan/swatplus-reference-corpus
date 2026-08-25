---
kind: output_family
source_symbols:
- header_pest
- res_pesticide_output
title: reservoir_pest_*
status: filled
source_hash: 41eb399f9201cd1f
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_pest`](../procedures/header_pest.md)  
**Written by:** [`res_pesticide_output`](../procedures/res_pesticide_output.md)  
**Primary data type:** `res_pesticide_module::res_pesticide_processes`  
**Files covered:** `reservoir_pest_day`, `reservoir_pest_mon`, `reservoir_pest_yr`, `reservoir_pest_aa` text/CSV pairs

## Bottom Line

`reservoir_pest_*` is the `reservoir_pest` pesticide time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `res_pesticide_output` loops over every simulated pesticide and writes **one row per (object x pesticide)** for each period: the row carries the time and object-identity fields, the pesticide name, and a `res_pesticide_processes` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `reservoir_pest` balance of one pesticide for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several pesticides, each object appears once per pesticide per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `reservoir_pest_day.txt` | `reservoir_pest_day.csv` | 2816 | 2820 | `header_pest.f90:146` |
| Monthly | `reservoir_pest_mon.txt` | `reservoir_pest_mon.csv` | 2817 | 2821 | `header_pest.f90:161` |
| Yearly | `reservoir_pest_yr.txt` | `reservoir_pest_yr.csv` | 2818 | 2822 | `header_pest.f90:176` |
| Average annual | `reservoir_pest_aa.txt` | `reservoir_pest_aa.csv` | 2819 | 2823 | `header_pest.f90:191` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (sp_ob%res  →  0) then  →  if (pco%pest%d == "y" .and. cs_db%num_tot  →  0) t` | `header_pest.f90:146` |
| Monthly | `if (sp_ob%res  →  0) then  →  if (pco%pest%m == "y" .and. cs_db%num_tot  →  0 ) ` | `header_pest.f90:161` |
| Yearly | `if (sp_ob%res  →  0) then  →  if (pco%pest%y == "y" .and. cs_db%num_tot  →  0) t` | `header_pest.f90:176` |
| Average annual | `if (sp_ob%res  →  0) then  →  if (pco%pest%a == "y" .and. cs_db%num_tot  →  0) t` | `header_pest.f90:191` |

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
| `sp_ob%res` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_pest` | Basin name and program string. |
| Header row | `header_pest` | Column names for time, identity, the pesticide name, and the `res_pesticide_processes` values. |
| Units row | `header_pest` | Units for the value columns. |
| Data row | `res_pesticide_output` | One `res_pesticide_processes` record for one pesticide at the active frequency. |

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
| `tot_in` | kg | `respst_d%pest(i)%tot_in` | total pesticide into reservoir |
| `sol_out` | kg | `respst_d%pest(i)%sol_out` | soluble pesticide out of reservoir |
| `sor_out` | kg | `respst_d%pest(i)%sor_out` | sorbed pesticide out of reservoir |
| `react` | kg | `respst_d%pest(i)%react` | pesticide lost through reactions in water layer |
| `metab` | kg | `respst_d%pest(i)%metab` | pesticide metabolized from parent in water layer |
| `volat` | kg | `respst_d%pest(i)%volat` | pesticide lost through volatilization |
| `settle` | kg | `respst_d%pest(i)%settle` | pesticide settling to sediment layer |
| `resus` | kg | `respst_d%pest(i)%resus` | pesticide resuspended into lake water |
| `difus` | kg | `respst_d%pest(i)%difus` | pesticide diffusing from sediment to water |
| `react_bot` | kg | `respst_d%pest(i)%react_bot` | pesticide lost from benthic sediment by reactions |
| `metab_bot` | kg | `respst_d%pest(i)%metab_bot` | pesticide metabolized from parent in water layer |
| `bury` | kg | `respst_d%pest(i)%bury` | pesticide lost from benthic sediment by burial |
| `water` | kg | `respst_d%pest(i)%water` | pesticide in water at end of day |
| `benthic` | kg | `respst_d%pest(i)%benthic` | pesticide in benthic sediment at end of day |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `res_pesticide_processes` record for one pesticide. `res_pesticide_output` loops over the simulated pesticides (`cs_db%pests(ipest)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated pesticide.
2. If the frequency's print flag is on, write that pesticide's current `res_pesticide_processes` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `res_pesticide_output.f90:33` | `2816` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `res_pesticide_output.f90:36` | `2820` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `res_pesticide_output.f90:52` | `2817` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `res_pesticide_output.f90:55` | `2821` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `res_pesticide_output.f90:71` | `2818` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `res_pesticide_output.f90:74` | `2822` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `res_pesticide_output.f90:85` | `2819` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `res_pesticide_output.f90:88` | `2823` | time, identity, pesticide name, one `res_pesticide_processes` record |

Header and file-open statements are in `header_pest`.

## Review Notes

- Every frequency shares the `res_pesticide_processes` layout; the Columns Written table applies to all files in the family.
- Rows repeat per pesticide: an object with N simulated pesticides produces N rows per period.
- Column names, units, and meanings are taken from the `res_pesticide_processes` type definition in `res_pesticide_module`.
- Auto-derived from the writer's per-pesticide output type; prose sections may benefit from human review.

## Source Links

- Writer: [`res_pesticide_output`](../procedures/res_pesticide_output.md)
- Header / opener: [`header_pest`](../procedures/header_pest.md)
- Data type: `res_pesticide_module::res_pesticide_processes`

## Evidence Used

- `res_pesticide_output.f90`
- `header_pest.f90`
- `res_pesticide_module.f90` (`type res_pesticide_processes`)
