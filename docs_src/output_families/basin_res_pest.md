---
kind: output_family
source_symbols:
- basin_res_pest_output
- header_pest
title: basin_res_pest_*
status: filled
source_hash: 1d8a0e0e7e1243b8
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_pest`](../procedures/header_pest.md)  
**Written by:** [`basin_res_pest_output`](../procedures/basin_res_pest_output.md)  
**Primary data type:** `res_pesticide_module::res_pesticide_processes`  
**Files covered:** `basin_res_pest_day`, `basin_res_pest_mon`, `basin_res_pest_yr`, `basin_res_pest_aa` text/CSV pairs

## Bottom Line

`basin_res_pest_*` is the `basin_res_pest` pesticide time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `basin_res_pest_output` loops over every simulated pesticide and writes **one row per (object x pesticide)** for each period: the row carries the time and object-identity fields, the pesticide name, and a `res_pesticide_processes` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `basin_res_pest` balance of one pesticide for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several pesticides, each object appears once per pesticide per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_res_pest_day.txt` | `basin_res_pest_day.csv` | 2848 | 2852 | `header_pest.f90:402` |
| Monthly | `basin_res_pest_mon.txt` | `basin_res_pest_mon.csv` | 2849 | 2853 | `header_pest.f90:417` |
| Yearly | `basin_res_pest_yr.txt` | `basin_res_pest_yr.csv` | 2850 | 2854 | `header_pest.f90:432` |
| Average annual | `basin_res_pest_aa.txt` | `basin_res_pest_aa.csv` | 2851 | 2855 | `header_pest.f90:447` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do ipest = 1, cs_db%num_pests  →  if (pco%day_print == "y" .and. pco%int_day_cur` | `header_pest.f90:402` |
| Monthly | `do ipest = 1, cs_db%num_pests  →  if (time%end_mo == 1) then  →  if (pco%pest%m ` | `header_pest.f90:417` |
| Yearly | `do ipest = 1, cs_db%num_pests  →  if (time%end_yr == 1) then  →  if (time%end_yr` | `header_pest.f90:432` |
| Average annual | `do ipest = 1, cs_db%num_pests  →  if (time%end_sim == 1 .and. pco%pest%a == "y")` | `header_pest.f90:447` |

The header and units rows for every file are written by `header_pest`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `do ipest = 1, cs_db%num_pests` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the print interval. |
| `pco%pest%d == "y"` | day | Enables output for this frequency. |
| `pco%pest%m == "y"` | mon | Enables output for this frequency. |
| `time%end_mo == 1` | mon | Writes rows at month end. |
| `time%end_sim == 1 .and. pco%pest%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Writes rows at year end. |
| `time%end_yr == 1 .and. pco%pest%y == "y"` | yr | Writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_pest` | Basin name and program string. |
| Header row | `header_pest` | Column names for time, identity, the pesticide name, and the `res_pesticide_processes` values. |
| Units row | `header_pest` | Units for the value columns. |
| Data row | `basin_res_pest_output` | One `res_pesticide_processes` record for one pesticide at the active frequency. |

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
| `tot_in` | kg | `brespst_d%pest(i)%tot_in` | total pesticide into reservoir |
| `sol_out` | kg | `brespst_d%pest(i)%sol_out` | soluble pesticide out of reservoir |
| `sor_out` | kg | `brespst_d%pest(i)%sor_out` | sorbed pesticide out of reservoir |
| `react` | kg | `brespst_d%pest(i)%react` | pesticide lost through reactions in water layer |
| `metab` | kg | `brespst_d%pest(i)%metab` | pesticide metabolized from parent in water layer |
| `volat` | kg | `brespst_d%pest(i)%volat` | pesticide lost through volatilization |
| `settle` | kg | `brespst_d%pest(i)%settle` | pesticide settling to sediment layer |
| `resus` | kg | `brespst_d%pest(i)%resus` | pesticide resuspended into lake water |
| `difus` | kg | `brespst_d%pest(i)%difus` | pesticide diffusing from sediment to water |
| `react_bot` | kg | `brespst_d%pest(i)%react_bot` | pesticide lost from benthic sediment by reactions |
| `metab_bot` | kg | `brespst_d%pest(i)%metab_bot` | pesticide metabolized from parent in water layer |
| `bury` | kg | `brespst_d%pest(i)%bury` | pesticide lost from benthic sediment by burial |
| `water` | kg | `brespst_d%pest(i)%water` | pesticide in water at end of day |
| `benthic` | kg | `brespst_d%pest(i)%benthic` | pesticide in benthic sediment at end of day |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `res_pesticide_processes` record for one pesticide. `basin_res_pest_output` loops over the simulated pesticides (`cs_db%pests(ipest)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated pesticide.
2. If the frequency's print flag is on, write that pesticide's current `res_pesticide_processes` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_res_pest_output.f90:38` | `2848` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `basin_res_pest_output.f90:41` | `2852` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `basin_res_pest_output.f90:57` | `2849` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `basin_res_pest_output.f90:60` | `2853` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `basin_res_pest_output.f90:76` | `2850` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `basin_res_pest_output.f90:79` | `2854` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `basin_res_pest_output.f90:90` | `2851` | time, identity, pesticide name, one `res_pesticide_processes` record |
| `basin_res_pest_output.f90:93` | `2855` | time, identity, pesticide name, one `res_pesticide_processes` record |

Header and file-open statements are in `header_pest`.

## Review Notes

- Every frequency shares the `res_pesticide_processes` layout; the Columns Written table applies to all files in the family.
- Rows repeat per pesticide: an object with N simulated pesticides produces N rows per period.
- Column names, units, and meanings are taken from the `res_pesticide_processes` type definition in `res_pesticide_module`.
- Auto-derived from the writer's per-pesticide output type; prose sections may benefit from human review.

## Source Links

- Writer: [`basin_res_pest_output`](../procedures/basin_res_pest_output.md)
- Header / opener: [`header_pest`](../procedures/header_pest.md)
- Data type: `res_pesticide_module::res_pesticide_processes`

## Evidence Used

- `basin_res_pest_output.f90`
- `header_pest.f90`
- `res_pesticide_module.f90` (`type res_pesticide_processes`)
