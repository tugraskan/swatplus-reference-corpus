---
kind: output_family
source_symbols:
- header_salt
- res_salt_output
title: reservoir_salt_*
status: filled
source_hash: 75b078d17b315049
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_salt`](../procedures/header_salt.md)  
**Written by:** [`res_salt_output`](../procedures/res_salt_output.md)  
**Primary data type:** `res_salt_module::res_salt_balance`  
**Files covered:** `reservoir_salt_day`, `reservoir_salt_mon`, `reservoir_salt_yr`, `reservoir_salt_aa` text/CSV pairs

## Bottom Line

`reservoir_salt_*` is the `reservoir_salt` num_salt time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `res_salt_output` loops over every simulated num_salt and writes **one row per (object x num_salt)** for each period: the row carries the time and object-identity fields, the num_salt name, and a `res_salt_balance` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `reservoir_salt` balance of one num_salt for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several num_salts, each object appears once per num_salt per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `reservoir_salt_day.txt` | `reservoir_salt_day.csv` | 5040 | 5041 | `header_salt.f90:583` |
| Monthly | `reservoir_salt_mon.txt` | `reservoir_salt_mon.csv` | 5042 | 5043 | `header_salt.f90:613` |
| Yearly | `reservoir_salt_yr.txt` | `reservoir_salt_yr.csv` | 5044 | 5045 | `header_salt.f90:643` |
| Average annual | `reservoir_salt_aa.txt` | `reservoir_salt_aa.csv` | 5046 | 5047 | `header_salt.f90:673` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:583` |
| Monthly | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:613` |
| Yearly | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:643` |
| Average annual | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:673` |

The header and units rows for every file are written by `header_salt`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%salt_aqu%a == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_aqu%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_aqu%m == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_aqu%y == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_basin%a == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_basin%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_basin%m == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_basin%y == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_chn%a == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_chn%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_chn%m == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_chn%y == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_hru%a == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_hru%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_hru%m == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_hru%y == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_res%a == "y" .and. cs_db%num_salts` | aa | Enables output for this frequency. |
| `pco%salt_res%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_res%m == "y" .and. cs_db%num_salts` | aa, mon, yr | Enables output for this frequency. |
| `pco%salt_res%y == "y" .and. cs_db%num_salts` | aa, yr | Enables output for this frequency. |
| `sp_ob%aqu` | All files | Open/print guard. |
| `sp_ob%chandeg` | All files | Open/print guard. |
| `sp_ob%res` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_salt` | Basin name and program string. |
| Header row | `header_salt` | Column names for time, identity, the num_salt name, and the `res_salt_balance` values. |
| Units row | `header_salt` | Units for the value columns. |
| Data row | `res_salt_output` | One `res_salt_balance` record for one num_salt at the active frequency. |

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
| `num_salt_name` | | `(ressalt_d(j)%salt(isalt)%conc,isalt=1,cs_db%num_salts)` | Name of the num_salt this row reports (one row per num_salt). |
| `inflow` | kg | `ressalt_d%salt(i)%inflow` | salt entering the reservoir via streamflow |
| `outflow` | kg | `ressalt_d%salt(i)%outflow` | salt leaving the reservoir via streamflow |
| `seep` | kg | `ressalt_d%salt(i)%seep` | salt leaving the reservoir via seepage to aquifer |
| `fert` | kg | `ressalt_d%salt(i)%fert` | salt added to reservoir (wetland) via fertilizer |
| `irrig` | kg | `ressalt_d%salt(i)%irrig` | salt removed from the reservoir via irrigation diversion |
| `div` | kg | `ressalt_d%salt(i)%div` | salt mass removed or added via diversion |
| `mass` | kg | `ressalt_d%salt(i)%mass` | salt in reservoir water at end of day |
| `conc` | g/m3 | `ressalt_d%salt(i)%conc` | salt concentration in reservoir at end of day |
| `volm` | m3 | `ressalt_d%salt(i)%volm` | volume of water in the reservoir |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `res_salt_balance` record for one num_salt. `res_salt_output` loops over the simulated num_salts (`(ressalt_d(j)%salt(isalt)%conc,isalt=1,cs_db%num_salts)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated num_salt.
2. If the frequency's print flag is on, write that num_salt's current `res_salt_balance` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `res_salt_output.f90:41` | `5040` | time, identity, num_salt name, one `res_salt_balance` record |
| `res_salt_output.f90:52` | `5041` | time, identity, num_salt name, one `res_salt_balance` record |
| `res_salt_output.f90:86` | `5042` | time, identity, num_salt name, one `res_salt_balance` record |
| `res_salt_output.f90:97` | `5043` | time, identity, num_salt name, one `res_salt_balance` record |
| `res_salt_output.f90:144` | `5044` | time, identity, num_salt name, one `res_salt_balance` record |
| `res_salt_output.f90:155` | `5045` | time, identity, num_salt name, one `res_salt_balance` record |
| `res_salt_output.f90:195` | `5046` | time, identity, num_salt name, one `res_salt_balance` record |
| `res_salt_output.f90:206` | `5047` | time, identity, num_salt name, one `res_salt_balance` record |

Header and file-open statements are in `header_salt`.

## Review Notes

- Every frequency shares the `res_salt_balance` layout; the Columns Written table applies to all files in the family.
- Rows repeat per num_salt: an object with N simulated num_salts produces N rows per period.
- Column names, units, and meanings are taken from the `res_salt_balance` type definition in `res_salt_module`.
- Auto-derived from the writer's per-num_salt output type; prose sections may benefit from human review.

## Source Links

- Writer: [`res_salt_output`](../procedures/res_salt_output.md)
- Header / opener: [`header_salt`](../procedures/header_salt.md)
- Data type: `res_salt_module::res_salt_balance`

## Evidence Used

- `res_salt_output.f90`
- `header_salt.f90`
- `res_salt_module.f90` (`type res_salt_balance`)
