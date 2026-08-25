---
kind: output_family
source_symbols:
- header_salt
- hru_salt_output
title: hru_salt_*
status: filled
source_hash: 7f3c799e155f24b7
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_salt`](../procedures/header_salt.md)  
**Written by:** [`hru_salt_output`](../procedures/hru_salt_output.md)  
**Primary data type:** `salt_module::salt_balance`  
**Files covered:** `hru_salt_day`, `hru_salt_mon`, `hru_salt_yr`, `hru_salt_aa` text/CSV pairs

## Bottom Line

`hru_salt_*` is the `hru_salt` num_salt time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `hru_salt_output` loops over every simulated num_salt and writes **one row per (object x num_salt)** for each period: the row carries the time and object-identity fields, the num_salt name, and a `salt_balance` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `hru_salt` balance of one num_salt for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several num_salts, each object appears once per num_salt per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hru_salt_day.txt` | `hru_salt_day.csv` | 5021 | 5022 | `header_salt.f90:186` |
| Monthly | `hru_salt_mon.txt` | `hru_salt_mon.csv` | 5023 | 5024 | `header_salt.f90:226` |
| Yearly | `hru_salt_yr.txt` | `hru_salt_yr.csv` | 5025 | 5026 | `header_salt.f90:266` |
| Average annual | `hru_salt_aa.txt` | `hru_salt_aa.csv` | 5027 | 5028 | `header_salt.f90:306` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:186` |
| Monthly | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:226` |
| Yearly | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:266` |
| Average annual | `if (pco%salt_basin%d == "y" .and. cs_db%num_salts  →  0) then  →  if (pco%salt_b` | `header_salt.f90:306` |

The header and units rows for every file are written by `header_salt`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%salt_basin%a == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_basin%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_basin%m == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_basin%y == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_hru%a == "y" .and. cs_db%num_salts` | aa | Enables output for this frequency. |
| `pco%salt_hru%d == "y" .and. cs_db%num_salts` | All files | Enables output for this frequency. |
| `pco%salt_hru%m == "y" .and. cs_db%num_salts` | aa, mon, yr | Enables output for this frequency. |
| `pco%salt_hru%y == "y" .and. cs_db%num_salts` | aa, yr | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_salt` | Basin name and program string. |
| Header row | `header_salt` | Column names for time, identity, the num_salt name, and the `salt_balance` values. |
| Units row | `header_salt` | Units for the value columns. |
| Data row | `hru_salt_output` | One `salt_balance` record for one num_salt at the active frequency. |

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
| `num_salt_name` | | `(hsaltb_d(j)%salt(isalt)%conc,isalt=1,cs_db%num_salts)` | Name of the num_salt this row reports (one row per num_salt). |
| `soil` |  | `hsaltb_d%salt(i)%soil` | salt ions = so4,ca,mg,na,k,cl,co3,hco3 total salt ion mass in the soil profile |
| `diss` | kg/ha | `hsaltb_d%salt(i)%diss` | salt ion mass transferred from sorbed phase to dissolved phase |
| `surq` | kg/ha | `hsaltb_d%salt(i)%surq` | salt ion mass lost in surface runoff in HRU |
| `latq` | kg/ha | `hsaltb_d%salt(i)%latq` | salt ion mass in lateral flow in HRU |
| `urbq` | kg/ha | `hsaltb_d%salt(i)%urbq` | salt ion mass in urban runoff |
| `wetq` | kg/ha | `hsaltb_d%salt(i)%wetq` | salt ion mass in wetland runoff |
| `tile` | kg/ha | `hsaltb_d%salt(i)%tile` | salt ion mass in tile flow in HRU |
| `perc` | kg/ha | `hsaltb_d%salt(i)%perc` | salt ion mass leached past bottom of soil |
| `gwup` | kg/ha | `hsaltb_d%salt(i)%gwup` | salt ion mass from groundwater (to soil profile) |
| `wtsp` | kg/ha | `hsaltb_d%salt(i)%wtsp` | salt ion mass in wetland seepage (to soil profile) |
| `irsw` | kg/ha | `hsaltb_d%salt(i)%irsw` | salt ion mass applied on soil via surface water irrigation |
| `irgw` | kg/ha | `hsaltb_d%salt(i)%irgw` | salt ion mass applied on soil via groundwater irrigation |
| `irwo` | kg/ha | `hsaltb_d%salt(i)%irwo` | salt ion mass applied on soil via girrigation from without (wo) the watershed |
| `rain` | kg/ha | `hsaltb_d%salt(i)%rain` | salt ion mass added to soil via rainfall |
| `dryd` | kg/ha | `hsaltb_d%salt(i)%dryd` | salt ion mass added to soil via dry atmospheric deposition |
| `road` | kg/ha | `hsaltb_d%salt(i)%road` | salt ion mass added to soil via applied road salt |
| `fert` | kg/ha | `hsaltb_d%salt(i)%fert` | salt ion mass added to soil via fertilizer |
| `amnd` | kg/ha | `hsaltb_d%salt(i)%amnd` | salt ion mass added to soil via salt amendments |
| `uptk` | kg/ha | `hsaltb_d%salt(i)%uptk` | salt ion mass taken up by crop roots |
| `conc` | mg/L | `hsaltb_d%salt(i)%conc` | salt ion concentration in soil water (averaged over all soil layers) |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `salt_balance` record for one num_salt. `hru_salt_output` loops over the simulated num_salts (`(hsaltb_d(j)%salt(isalt)%conc,isalt=1,cs_db%num_salts)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated num_salt.
2. If the frequency's print flag is on, write that num_salt's current `salt_balance` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hru_salt_output.f90:48` | `5021` | time, identity, num_salt name, one `salt_balance` record |
| `hru_salt_output.f90:69` | `5022` | time, identity, num_salt name, one `salt_balance` record |
| `hru_salt_output.f90:123` | `5023` | time, identity, num_salt name, one `salt_balance` record |
| `hru_salt_output.f90:144` | `5024` | time, identity, num_salt name, one `salt_balance` record |
| `hru_salt_output.f90:220` | `5025` | time, identity, num_salt name, one `salt_balance` record |
| `hru_salt_output.f90:241` | `5026` | time, identity, num_salt name, one `salt_balance` record |
| `hru_salt_output.f90:310` | `5027` | time, identity, num_salt name, one `salt_balance` record |
| `hru_salt_output.f90:331` | `5028` | time, identity, num_salt name, one `salt_balance` record |

Header and file-open statements are in `header_salt`.

## Review Notes

- Every frequency shares the `salt_balance` layout; the Columns Written table applies to all files in the family.
- Rows repeat per num_salt: an object with N simulated num_salts produces N rows per period.
- Column names, units, and meanings are taken from the `salt_balance` type definition in `salt_module`.
- Auto-derived from the writer's per-num_salt output type; prose sections may benefit from human review.

## Source Links

- Writer: [`hru_salt_output`](../procedures/hru_salt_output.md)
- Header / opener: [`header_salt`](../procedures/header_salt.md)
- Data type: `salt_module::salt_balance`

## Evidence Used

- `hru_salt_output.f90`
- `header_salt.f90`
- `salt_module.f90` (`type salt_balance`)
