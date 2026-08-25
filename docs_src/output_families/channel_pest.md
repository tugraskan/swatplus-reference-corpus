---
kind: output_family
source_symbols:
- cha_pesticide_output
- header_pest
title: channel_pest_*
status: filled
source_hash: 8a4d3930b24337a6
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_pest`](../procedures/header_pest.md)  
**Written by:** [`cha_pesticide_output`](../procedures/cha_pesticide_output.md)  
**Primary data type:** `ch_pesticide_module::ch_pesticide_processes`  
**Files covered:** `channel_pest_day`, `channel_pest_mon`, `channel_pest_yr`, `channel_pest_aa` text/CSV pairs

## Bottom Line

`channel_pest_*` is the `channel_pest` pesticide time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `cha_pesticide_output` loops over every simulated pesticide and writes **one row per (object x pesticide)** for each period: the row carries the time and object-identity fields, the pesticide name, and a `ch_pesticide_processes` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `channel_pest` balance of one pesticide for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several pesticides, each object appears once per pesticide per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `channel_pest_day.txt` | `channel_pest_day.csv` | 2808 | 2812 | `header_pest.f90:82` |
| Monthly | `channel_pest_mon.txt` | `channel_pest_mon.csv` | 2809 | 2813 | `header_pest.f90:97` |
| Yearly | `channel_pest_yr.txt` | `channel_pest_yr.csv` | 2810 | 2814 | `header_pest.f90:112` |
| Average annual | `channel_pest_aa.txt` | `channel_pest_aa.csv` | 2811 | 2815 | `header_pest.f90:127` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do ipest = 1, cs_db%num_pests  →  if (pco%day_print == "y" .and. pco%int_day_cur` | `header_pest.f90:82` |
| Monthly | `do ipest = 1, cs_db%num_pests  →  if (time%end_mo == 1) then  →  if (pco%pest%m ` | `header_pest.f90:97` |
| Yearly | `do ipest = 1, cs_db%num_pests  →  if (time%end_yr == 1) then  →  if (time%end_yr` | `header_pest.f90:112` |
| Average annual | `do ipest = 1, cs_db%num_pests  →  if (time%end_sim == 1 .and. pco%pest%a == "y")` | `header_pest.f90:127` |

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
| Header row | `header_pest` | Column names for time, identity, the pesticide name, and the `ch_pesticide_processes` values. |
| Units row | `header_pest` | Units for the value columns. |
| Data row | `cha_pesticide_output` | One `ch_pesticide_processes` record for one pesticide at the active frequency. |

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
| `tot_in` | kg | `chpst_d%pest(i)%tot_in` | total pesticide into reservoir |
| `sol_out` | kg | `chpst_d%pest(i)%sol_out` | soluble pesticide out of reservoir |
| `sor_out` | kg | `chpst_d%pest(i)%sor_out` | sorbed pesticide out of reservoir |
| `react` | kg | `chpst_d%pest(i)%react` | pesticide lost through reactions in water layer |
| `metab` | kg | `chpst_d%pest(i)%metab` | pesticide metabolized from parent in water layer |
| `volat` | kg | `chpst_d%pest(i)%volat` | pesticide lost through volatilization |
| `settle` | kg | `chpst_d%pest(i)%settle` | pesticide settling to sediment layer |
| `resus` | kg | `chpst_d%pest(i)%resus` | pesticide resuspended into lake water |
| `difus` | kg | `chpst_d%pest(i)%difus` | pesticide diffusing from sediment to water |
| `react_bot` | kg | `chpst_d%pest(i)%react_bot` | pesticide lost from benthic sediment by reactions |
| `metab_bot` | kg | `chpst_d%pest(i)%metab_bot` | pesticide metabolized from parent in water layer |
| `bury` | kg | `chpst_d%pest(i)%bury` | pesticide lost from benthic sediment by burial |
| `water` | kg | `chpst_d%pest(i)%water` | pesticide in water at end of day |
| `benthic` | kg | `chpst_d%pest(i)%benthic` | pesticide in benthic sediment at tend of day |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `ch_pesticide_processes` record for one pesticide. `cha_pesticide_output` loops over the simulated pesticides (`cs_db%pests(ipest)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated pesticide.
2. If the frequency's print flag is on, write that pesticide's current `ch_pesticide_processes` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `cha_pesticide_output.f90:36` | `2808` | time, identity, pesticide name, one `ch_pesticide_processes` record |
| `cha_pesticide_output.f90:39` | `2812` | time, identity, pesticide name, one `ch_pesticide_processes` record |
| `cha_pesticide_output.f90:55` | `2809` | time, identity, pesticide name, one `ch_pesticide_processes` record |
| `cha_pesticide_output.f90:58` | `2813` | time, identity, pesticide name, one `ch_pesticide_processes` record |
| `cha_pesticide_output.f90:74` | `2810` | time, identity, pesticide name, one `ch_pesticide_processes` record |
| `cha_pesticide_output.f90:77` | `2814` | time, identity, pesticide name, one `ch_pesticide_processes` record |
| `cha_pesticide_output.f90:88` | `2811` | time, identity, pesticide name, one `ch_pesticide_processes` record |
| `cha_pesticide_output.f90:91` | `2815` | time, identity, pesticide name, one `ch_pesticide_processes` record |

Header and file-open statements are in `header_pest`.

## Review Notes

- Every frequency shares the `ch_pesticide_processes` layout; the Columns Written table applies to all files in the family.
- Rows repeat per pesticide: an object with N simulated pesticides produces N rows per period.
- Column names, units, and meanings are taken from the `ch_pesticide_processes` type definition in `ch_pesticide_module`.
- Auto-derived from the writer's per-pesticide output type; prose sections may benefit from human review.

## Source Links

- Writer: [`cha_pesticide_output`](../procedures/cha_pesticide_output.md)
- Header / opener: [`header_pest`](../procedures/header_pest.md)
- Data type: `ch_pesticide_module::ch_pesticide_processes`

## Evidence Used

- `cha_pesticide_output.f90`
- `header_pest.f90`
- `ch_pesticide_module.f90` (`type ch_pesticide_processes`)
