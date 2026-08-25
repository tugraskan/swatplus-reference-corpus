---
kind: output_family
source_symbols:
- header_salt
- wet_salt_output
title: wetland_salt_*
status: filled
source_hash: 4d4c50c25f3c9419
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_salt`](../procedures/header_salt.md)  
**Written by:** [`wet_salt_output`](../procedures/wet_salt_output.md)  
**Primary data type:** `res_salt_module::res_salt_balance`  
**Files covered:** `wetland_salt_day`, `wetland_salt_mon`, `wetland_salt_yr`, `wetland_salt_aa` text/CSV pairs

## Bottom Line

`wetland_salt_*` is the `wetland_salt` num_salt time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `wet_salt_output` loops over every simulated num_salt and writes **one row per (object x num_salt)** for each period: the row carries the time and object-identity fields, the num_salt name, and a `res_salt_balance` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `wetland_salt` balance of one num_salt for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several num_salts, each object appears once per num_salt per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `wetland_salt_day.txt` | `wetland_salt_day.csv` | 5090 | 5091 | `header_salt.f90:855` |
| Monthly | `wetland_salt_mon.txt` | `wetland_salt_mon.csv` | 5092 | 5093 | `header_salt.f90:885` |
| Yearly | `wetland_salt_yr.txt` | `wetland_salt_yr.csv` | 5094 | 5095 | `header_salt.f90:915` |
| Average annual | `wetland_salt_aa.txt` | `wetland_salt_aa.csv` | 5096 | 5097 | `header_salt.f90:945` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:855` |
| Monthly | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:885` |
| Yearly | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:915` |
| Average annual | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:945` |

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
| `pco%salt_res%a == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_res%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_res%m == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_res%y == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_ru%a == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_ru%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_ru%m == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_ru%y == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_wet%a == "y" .and. cs_db%num_salts` | aa | Enables output for this frequency. |
| `pco%salt_wet%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_wet%m == "y" .and. cs_db%num_salts` | aa, mon, yr | Enables output for this frequency. |
| `pco%salt_wet%y == "y" .and. cs_db%num_salts` | aa, yr | Enables output for this frequency. |
| `sp_ob%aqu` | All files | Open/print guard. |
| `sp_ob%chandeg` | All files | Open/print guard. |
| `sp_ob%res` | All files | Open/print guard. |
| `sp_ob%ru` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_salt` | Basin name and program string. |
| Header row | `header_salt` | Column names for time, identity, the num_salt name, and the `res_salt_balance` values. |
| Units row | `header_salt` | Units for the value columns. |
| Data row | `wet_salt_output` | One `res_salt_balance` record for one num_salt at the active frequency. |

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
| `num_salt_name` | | `(wetsalt_d(j)%salt(isalt)%conc,isalt=1,cs_db%num_salts)` | Name of the num_salt this row reports (one row per num_salt). |
| `inflow` | kg | `wetsalt_d%salt(i)%inflow` | salt entering the reservoir via streamflow |
| `outflow` | kg | `wetsalt_d%salt(i)%outflow` | salt leaving the reservoir via streamflow |
| `seep` | kg | `wetsalt_d%salt(i)%seep` | salt leaving the reservoir via seepage to aquifer |
| `fert` | kg | `wetsalt_d%salt(i)%fert` | salt added to reservoir (wetland) via fertilizer |
| `irrig` | kg | `wetsalt_d%salt(i)%irrig` | salt removed from the reservoir via irrigation diversion |
| `div` | kg | `wetsalt_d%salt(i)%div` | salt mass removed or added via diversion |
| `mass` | kg | `wetsalt_d%salt(i)%mass` | salt in reservoir water at end of day |
| `conc` | g/m3 | `wetsalt_d%salt(i)%conc` | salt concentration in reservoir at end of day |
| `volm` | m3 | `wetsalt_d%salt(i)%volm` | volume of water in the reservoir |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `res_salt_balance` record for one num_salt. `wet_salt_output` loops over the simulated num_salts (`(wetsalt_d(j)%salt(isalt)%conc,isalt=1,cs_db%num_salts)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated num_salt.
2. If the frequency's print flag is on, write that num_salt's current `res_salt_balance` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `wet_salt_output.f90:42` | `5090` | time, identity, num_salt name, one `res_salt_balance` record |
| `wet_salt_output.f90:53` | `5091` | time, identity, num_salt name, one `res_salt_balance` record |
| `wet_salt_output.f90:87` | `5092` | time, identity, num_salt name, one `res_salt_balance` record |
| `wet_salt_output.f90:98` | `5093` | time, identity, num_salt name, one `res_salt_balance` record |
| `wet_salt_output.f90:145` | `5094` | time, identity, num_salt name, one `res_salt_balance` record |
| `wet_salt_output.f90:156` | `5095` | time, identity, num_salt name, one `res_salt_balance` record |
| `wet_salt_output.f90:196` | `5096` | time, identity, num_salt name, one `res_salt_balance` record |
| `wet_salt_output.f90:207` | `5097` | time, identity, num_salt name, one `res_salt_balance` record |

Header and file-open statements are in `header_salt`.

## Review Notes

- Every frequency shares the `res_salt_balance` layout; the Columns Written table applies to all files in the family.
- Rows repeat per num_salt: an object with N simulated num_salts produces N rows per period.
- Column names, units, and meanings are taken from the `res_salt_balance` type definition in `res_salt_module`.
- Auto-derived from the writer's per-num_salt output type; prose sections may benefit from human review.

## Source Links

- Writer: [`wet_salt_output`](../procedures/wet_salt_output.md)
- Header / opener: [`header_salt`](../procedures/header_salt.md)
- Data type: `res_salt_module::res_salt_balance`

## Evidence Used

- `wet_salt_output.f90`
- `header_salt.f90`
- `res_salt_module.f90` (`type res_salt_balance`)
