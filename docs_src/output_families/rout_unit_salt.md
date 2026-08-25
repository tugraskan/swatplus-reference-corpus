---
kind: output_family
source_symbols:
- header_salt
- ru_salt_output
title: rout_unit_salt_*
status: filled
source_hash: 57979841a4e889e8
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_salt`](../procedures/header_salt.md)  
**Written by:** [`ru_salt_output`](../procedures/ru_salt_output.md)  
**Primary data type:** `salt_module::salt_balance`  
**Files covered:** `rout_unit_salt_day`, `rout_unit_salt_mon`, `rout_unit_salt_yr`, `rout_unit_salt_aa` text/CSV pairs

## Bottom Line

`rout_unit_salt_*` is the `rout_unit_salt` num_salt time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `ru_salt_output` loops over every simulated num_salt and writes **one row per (object x num_salt)** for each period: the row carries the time and object-identity fields, the num_salt name, and a `salt_balance` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `rout_unit_salt` balance of one num_salt for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several num_salts, each object appears once per num_salt per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `rout_unit_salt_day.txt` | `rout_unit_salt_day.csv` | 5070 | 5071 | `header_salt.f90:703` |
| Monthly | `rout_unit_salt_mon.txt` | `rout_unit_salt_mon.csv` | 5072 | 5073 | `header_salt.f90:741` |
| Yearly | `rout_unit_salt_yr.txt` | `rout_unit_salt_yr.csv` | 5074 | 5075 | `header_salt.f90:779` |
| Average annual | `rout_unit_salt_aa.txt` | `rout_unit_salt_aa.csv` | 5076 | 5077 | `header_salt.f90:817` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:703` |
| Monthly | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:741` |
| Yearly | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:779` |
| Average annual | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:817` |

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
| `pco%salt_ru%a == "y" .and. cs_db%num_salts` | aa | Enables output for this frequency. |
| `pco%salt_ru%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_ru%m == "y" .and. cs_db%num_salts` | aa, mon, yr | Enables output for this frequency. |
| `pco%salt_ru%y == "y" .and. cs_db%num_salts` | aa, yr | Enables output for this frequency. |
| `sp_ob%aqu` | All files | Open/print guard. |
| `sp_ob%chandeg` | All files | Open/print guard. |
| `sp_ob%res` | All files | Open/print guard. |
| `sp_ob%ru` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_salt` | Basin name and program string. |
| Header row | `header_salt` | Column names for time, identity, the num_salt name, and the `salt_balance` values. |
| Units row | `header_salt` | Units for the value columns. |
| Data row | `ru_salt_output` | One `salt_balance` record for one num_salt at the active frequency. |

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
| `num_salt_name` | | `(ru_hru_saltb_d(iru)%salt(isalt)%uptk,isalt=1,cs_db%num_salts)` | Name of the num_salt this row reports (one row per num_salt). |
| `soil` |  | `ru_hru_saltb_d%salt(i)%soil` | salt ions = so4,ca,mg,na,k,cl,co3,hco3 total salt ion mass in the soil profile |
| `diss` | kg/ha | `ru_hru_saltb_d%salt(i)%diss` | salt ion mass transferred from sorbed phase to dissolved phase |
| `surq` | kg/ha | `ru_hru_saltb_d%salt(i)%surq` | salt ion mass lost in surface runoff in HRU |
| `latq` | kg/ha | `ru_hru_saltb_d%salt(i)%latq` | salt ion mass in lateral flow in HRU |
| `urbq` | kg/ha | `ru_hru_saltb_d%salt(i)%urbq` | salt ion mass in urban runoff |
| `wetq` | kg/ha | `ru_hru_saltb_d%salt(i)%wetq` | salt ion mass in wetland runoff |
| `tile` | kg/ha | `ru_hru_saltb_d%salt(i)%tile` | salt ion mass in tile flow in HRU |
| `perc` | kg/ha | `ru_hru_saltb_d%salt(i)%perc` | salt ion mass leached past bottom of soil |
| `gwup` | kg/ha | `ru_hru_saltb_d%salt(i)%gwup` | salt ion mass from groundwater (to soil profile) |
| `wtsp` | kg/ha | `ru_hru_saltb_d%salt(i)%wtsp` | salt ion mass in wetland seepage (to soil profile) |
| `irsw` | kg/ha | `ru_hru_saltb_d%salt(i)%irsw` | salt ion mass applied on soil via surface water irrigation |
| `irgw` | kg/ha | `ru_hru_saltb_d%salt(i)%irgw` | salt ion mass applied on soil via groundwater irrigation |
| `irwo` | kg/ha | `ru_hru_saltb_d%salt(i)%irwo` | salt ion mass applied on soil via girrigation from without (wo) the watershed |
| `rain` | kg/ha | `ru_hru_saltb_d%salt(i)%rain` | salt ion mass added to soil via rainfall |
| `dryd` | kg/ha | `ru_hru_saltb_d%salt(i)%dryd` | salt ion mass added to soil via dry atmospheric deposition |
| `road` | kg/ha | `ru_hru_saltb_d%salt(i)%road` | salt ion mass added to soil via applied road salt |
| `fert` | kg/ha | `ru_hru_saltb_d%salt(i)%fert` | salt ion mass added to soil via fertilizer |
| `amnd` | kg/ha | `ru_hru_saltb_d%salt(i)%amnd` | salt ion mass added to soil via salt amendments |
| `uptk` | kg/ha | `ru_hru_saltb_d%salt(i)%uptk` | salt ion mass taken up by crop roots |
| `conc` | mg/L | `ru_hru_saltb_d%salt(i)%conc` | salt ion concentration in soil water (averaged over all soil layers) |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `salt_balance` record for one num_salt. `ru_salt_output` loops over the simulated num_salts (`(ru_hru_saltb_d(iru)%salt(isalt)%uptk,isalt=1,cs_db%num_salts)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated num_salt.
2. If the frequency's print flag is on, write that num_salt's current `salt_balance` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `ru_salt_output.f90:48` | `5070` | time, identity, num_salt name, one `salt_balance` record |
| `ru_salt_output.f90:66` | `5071` | time, identity, num_salt name, one `salt_balance` record |
| `ru_salt_output.f90:123` | `5072` | time, identity, num_salt name, one `salt_balance` record |
| `ru_salt_output.f90:141` | `5073` | time, identity, num_salt name, one `salt_balance` record |
| `ru_salt_output.f90:198` | `5074` | time, identity, num_salt name, one `salt_balance` record |
| `ru_salt_output.f90:216` | `5075` | time, identity, num_salt name, one `salt_balance` record |
| `ru_salt_output.f90:271` | `5076` | time, identity, num_salt name, one `salt_balance` record |
| `ru_salt_output.f90:289` | `5077` | time, identity, num_salt name, one `salt_balance` record |

Header and file-open statements are in `header_salt`.

## Review Notes

- Every frequency shares the `salt_balance` layout; the Columns Written table applies to all files in the family.
- Rows repeat per num_salt: an object with N simulated num_salts produces N rows per period.
- Column names, units, and meanings are taken from the `salt_balance` type definition in `salt_module`.
- Auto-derived from the writer's per-num_salt output type; prose sections may benefit from human review.

## Source Links

- Writer: [`ru_salt_output`](../procedures/ru_salt_output.md)
- Header / opener: [`header_salt`](../procedures/header_salt.md)
- Data type: `salt_module::salt_balance`

## Evidence Used

- `ru_salt_output.f90`
- `header_salt.f90`
- `salt_module.f90` (`type salt_balance`)
