---
kind: output_family
source_symbols:
- header_const
- res_cs_output
title: reservoir_cs_*
status: filled
source_hash: b0979a8ad8b724c3
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_const`](../procedures/header_const.md)  
**Written by:** [`res_cs_output`](../procedures/res_cs_output.md)  
**Primary data type:** `res_cs_module::res_cs_balance`  
**Files covered:** `reservoir_cs_day`, `reservoir_cs_mon`, `reservoir_cs_yr`, `reservoir_cs_aa` text/CSV pairs

## Bottom Line

`reservoir_cs_*` is the `reservoir_cs` num_c time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `res_cs_output` loops over every simulated num_c and writes **one row per (object x num_c)** for each period: the row carries the time and object-identity fields, the num_c name, and a `res_cs_balance` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `reservoir_cs` balance of one num_c for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several num_cs, each object appears once per num_c per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `reservoir_cs_day.txt` | `reservoir_cs_day.csv` | 6040 | 6041 | `header_const.f90:599` |
| Monthly | `reservoir_cs_mon.txt` | `reservoir_cs_mon.csv` | 6042 | 6043 | `header_const.f90:632` |
| Yearly | `reservoir_cs_yr.txt` | `reservoir_cs_yr.csv` | 6044 | 6045 | `header_const.f90:665` |
| Average annual | `reservoir_cs_aa.txt` | `reservoir_cs_aa.csv` | 6046 | 6047 | `header_const.f90:698` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:599` |
| Monthly | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:632` |
| Yearly | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:665` |
| Average annual | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:698` |

The header and units rows for every file are written by `header_const`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%cs_aqu%a == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_aqu%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_aqu%m == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_aqu%y == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_basin%a == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_basin%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_basin%m == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_basin%y == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_chn%a == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_chn%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_chn%m == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_chn%y == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_hru%a == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_hru%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_hru%m == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_hru%y == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_res%a == "y" .and. cs_db%num_cs` | aa | Enables output for this frequency. |
| `pco%cs_res%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_res%m == "y" .and. cs_db%num_cs` | aa, mon, yr | Enables output for this frequency. |
| `pco%cs_res%y == "y" .and. cs_db%num_cs` | aa, yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `sp_ob%aqu` | All files | Open/print guard. |
| `sp_ob%chandeg` | All files | Open/print guard. |
| `sp_ob%res` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_const` | Basin name and program string. |
| Header row | `header_const` | Column names for time, identity, the num_c name, and the `res_cs_balance` values. |
| Units row | `header_const` | Units for the value columns. |
| Data row | `res_cs_output` | One `res_cs_balance` record for one num_c at the active frequency. |

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
| `num_c_name` | | `(rescs_d(j)%cs(ics)%conc,ics=1,cs_db%num_cs)` | Name of the num_c this row reports (one row per num_c). |
| `inflow` | kg | `rescs_d%cs(i)%inflow` | constituent entering the reservoir |
| `outflow` | kg | `rescs_d%cs(i)%outflow` | constituent leaving the reservoir via streamflow |
| `seep` | kg | `rescs_d%cs(i)%seep` | constituent leaving the reservoir via seepage to aquifer |
| `settle` | kg | `rescs_d%cs(i)%settle` | constituent settling to bottom of reservoir |
| `rctn` | kg | `rescs_d%cs(i)%rctn` | constituent removal due to chemical reaction |
| `prod` | kg | `rescs_d%cs(i)%prod` | constituent produced due to chemical reaction |
| `fert` | kg | `rescs_d%cs(i)%fert` | constituent added in fertilizer (to wetland) |
| `irrig` | kg | `rescs_d%cs(i)%irrig` | constituent removed from the reservoir via irrigation diversion |
| `div` | kg | `rescs_d%cs(i)%div` | constituent removed or added via diversion |
| `mass` | kg | `rescs_d%cs(i)%mass` | constituent in reservoir water at end of day |
| `conc` | g/m3 | `rescs_d%cs(i)%conc` | constituent concentration in reservoir at end of day |
| `volm` | m3 | `rescs_d%cs(i)%volm` | volume of water in the reservoir |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `res_cs_balance` record for one num_c. `res_cs_output` loops over the simulated num_cs (`(rescs_d(j)%cs(ics)%conc,ics=1,cs_db%num_cs)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated num_c.
2. If the frequency's print flag is on, write that num_c's current `res_cs_balance` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `res_cs_output.f90:44` | `6040` | time, identity, num_c name, one `res_cs_balance` record |
| `res_cs_output.f90:58` | `6041` | time, identity, num_c name, one `res_cs_balance` record |
| `res_cs_output.f90:98` | `6042` | time, identity, num_c name, one `res_cs_balance` record |
| `res_cs_output.f90:112` | `6043` | time, identity, num_c name, one `res_cs_balance` record |
| `res_cs_output.f90:168` | `6044` | time, identity, num_c name, one `res_cs_balance` record |
| `res_cs_output.f90:182` | `6045` | time, identity, num_c name, one `res_cs_balance` record |
| `res_cs_output.f90:231` | `6046` | time, identity, num_c name, one `res_cs_balance` record |
| `res_cs_output.f90:245` | `6047` | time, identity, num_c name, one `res_cs_balance` record |

Header and file-open statements are in `header_const`.

## Review Notes

- Every frequency shares the `res_cs_balance` layout; the Columns Written table applies to all files in the family.
- Rows repeat per num_c: an object with N simulated num_cs produces N rows per period.
- Column names, units, and meanings are taken from the `res_cs_balance` type definition in `res_cs_module`.
- Auto-derived from the writer's per-num_c output type; prose sections may benefit from human review.

## Source Links

- Writer: [`res_cs_output`](../procedures/res_cs_output.md)
- Header / opener: [`header_const`](../procedures/header_const.md)
- Data type: `res_cs_module::res_cs_balance`

## Evidence Used

- `res_cs_output.f90`
- `header_const.f90`
- `res_cs_module.f90` (`type res_cs_balance`)
