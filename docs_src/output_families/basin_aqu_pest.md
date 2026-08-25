---
kind: output_family
source_symbols:
- basin_aqu_pest_output
- header_pest
title: basin_aqu_pest_*
status: filled
source_hash: ecc316f3063bfb38
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_pest`](../procedures/header_pest.md)  
**Written by:** [`basin_aqu_pest_output`](../procedures/basin_aqu_pest_output.md)  
**Primary data type:** `aqu_pesticide_module::aqu_pesticide_processes`  
**Files covered:** `basin_aqu_pest_day`, `basin_aqu_pest_mon`, `basin_aqu_pest_yr`, `basin_aqu_pest_aa` text/CSV pairs

## Bottom Line

`basin_aqu_pest_*` is the `basin_aqu_pest` pesticide time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `basin_aqu_pest_output` loops over every simulated pesticide and writes **one row per (object x pesticide)** for each period: the row carries the time and object-identity fields, the pesticide name, and a `aqu_pesticide_processes` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `basin_aqu_pest` balance of one pesticide for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several pesticides, each object appears once per pesticide per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_aqu_pest_day.txt` | `basin_aqu_pest_day.csv` | 3000 | 3004 | `header_pest.f90:210` |
| Monthly | `basin_aqu_pest_mon.txt` | `basin_aqu_pest_mon.csv` | 3001 | 3005 | `header_pest.f90:225` |
| Yearly | `basin_aqu_pest_yr.txt` | `basin_aqu_pest_yr.csv` | 3002 | 3006 | `header_pest.f90:240` |
| Average annual | `basin_aqu_pest_aa.txt` | `basin_aqu_pest_aa.csv` | 3003 | 3007 | `header_pest.f90:255` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do ipest = 1, cs_db%num_pests  →  if (pco%day_print == "y" .and. pco%int_day_cur` | `header_pest.f90:210` |
| Monthly | `do ipest = 1, cs_db%num_pests  →  if (time%end_mo == 1) then  →  if (pco%pest%m ` | `header_pest.f90:225` |
| Yearly | `do ipest = 1, cs_db%num_pests  →  if (time%end_yr == 1) then  →  if (time%end_yr` | `header_pest.f90:240` |
| Average annual | `do ipest = 1, cs_db%num_pests  →  if (time%end_sim == 1 .and. pco%pest%a == "y")` | `header_pest.f90:255` |

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
| Header row | `header_pest` | Column names for time, identity, the pesticide name, and the `aqu_pesticide_processes` values. |
| Units row | `header_pest` | Units for the value columns. |
| Data row | `basin_aqu_pest_output` | One `aqu_pesticide_processes` record for one pesticide at the active frequency. |

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
| `tot_in` | kg | `baqupst_d%pest(i)%tot_in` | total pesticide into aquifer |
| `sol_flo` | kg | `baqupst_d%pest(i)%sol_flo` | soluble pesticide out of aquifer |
| `sor_flo` | kg | `baqupst_d%pest(i)%sor_flo` | sorbed pesticide out of aquifer |
| `sol_perc` | kg | `baqupst_d%pest(i)%sol_perc` | sorbed pesticide out of aquifer |
| `react` | kg | `baqupst_d%pest(i)%react` | pesticide lost through reactions |
| `metab` | kg | `baqupst_d%pest(i)%metab` | amount of pesticide metabolized from parent |
| `stor_ave` | kg | `baqupst_d%pest(i)%stor_ave` | average end of day pesticide in aquifer during the time period |
| `stor_init` | kg | `baqupst_d%pest(i)%stor_init` | pesticide in aquifer at the start of the day |
| `stor_final` | kg | `baqupst_d%pest(i)%stor_final` | pesticide in aquifer at the end of the day |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `aqu_pesticide_processes` record for one pesticide. `basin_aqu_pest_output` loops over the simulated pesticides (`cs_db%pests(ipest)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated pesticide.
2. If the frequency's print flag is on, write that pesticide's current `aqu_pesticide_processes` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_aqu_pest_output.f90:41` | `3000` | time, identity, pesticide name, one `aqu_pesticide_processes` record |
| `basin_aqu_pest_output.f90:44` | `3004` | time, identity, pesticide name, one `aqu_pesticide_processes` record |
| `basin_aqu_pest_output.f90:61` | `3001` | time, identity, pesticide name, one `aqu_pesticide_processes` record |
| `basin_aqu_pest_output.f90:64` | `3005` | time, identity, pesticide name, one `aqu_pesticide_processes` record |
| `basin_aqu_pest_output.f90:83` | `3002` | time, identity, pesticide name, one `aqu_pesticide_processes` record |
| `basin_aqu_pest_output.f90:86` | `3006` | time, identity, pesticide name, one `aqu_pesticide_processes` record |
| `basin_aqu_pest_output.f90:101` | `3003` | time, identity, pesticide name, one `aqu_pesticide_processes` record |
| `basin_aqu_pest_output.f90:104` | `3007` | time, identity, pesticide name, one `aqu_pesticide_processes` record |

Header and file-open statements are in `header_pest`.

## Review Notes

- Every frequency shares the `aqu_pesticide_processes` layout; the Columns Written table applies to all files in the family.
- Rows repeat per pesticide: an object with N simulated pesticides produces N rows per period.
- Column names, units, and meanings are taken from the `aqu_pesticide_processes` type definition in `aqu_pesticide_module`.
- Auto-derived from the writer's per-pesticide output type; prose sections may benefit from human review.

## Source Links

- Writer: [`basin_aqu_pest_output`](../procedures/basin_aqu_pest_output.md)
- Header / opener: [`header_pest`](../procedures/header_pest.md)
- Data type: `aqu_pesticide_module::aqu_pesticide_processes`

## Evidence Used

- `basin_aqu_pest_output.f90`
- `header_pest.f90`
- `aqu_pesticide_module.f90` (`type aqu_pesticide_processes`)
