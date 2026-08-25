---
kind: output_family
source_symbols:
- aqu_salt_output
- header_salt
title: aquifer_salt_*
status: filled
source_hash: c9367b5ed6f21580
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_salt`](../procedures/header_salt.md)  
**Written by:** [`aqu_salt_output`](../procedures/aqu_salt_output.md)  
**Primary data type:** `salt_aquifer::salt_balance_aqu`  
**Files covered:** `aquifer_salt_day`, `aquifer_salt_mon`, `aquifer_salt_yr`, `aquifer_salt_aa` text/CSV pairs

## Bottom Line

`aquifer_salt_*` is the `aquifer_salt` num_salt time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `aqu_salt_output` loops over every simulated num_salt and writes **one row per (object x num_salt)** for each period: the row carries the time and object-identity fields, the num_salt name, and a `salt_balance_aqu` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `aquifer_salt` balance of one num_salt for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several num_salts, each object appears once per num_salt per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `aquifer_salt_day.txt` | `aquifer_salt_day.csv` | 5060 | 5061 | `header_salt.f90:347` |
| Monthly | `aquifer_salt_mon.txt` | `aquifer_salt_mon.csv` | 5062 | 5063 | `header_salt.f90:377` |
| Yearly | `aquifer_salt_yr.txt` | `aquifer_salt_yr.csv` | 5064 | 5065 | `header_salt.f90:407` |
| Average annual | `aquifer_salt_aa.txt` | `aquifer_salt_aa.csv` | 5066 | 5067 | `header_salt.f90:437` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do isalt=1,cs_db%num_salts  →  if (pco%salt_aqu%d == "y") then` | `header_salt.f90:347` |
| Monthly | `do isalt=1,cs_db%num_salts  →  if (pco%salt_aqu%d == "y") then  →  if (pco%csvou` | `header_salt.f90:377` |
| Yearly | `do isalt=1,cs_db%num_salts  →  if (pco%salt_aqu%d == "y") then  →  if (pco%csvou` | `header_salt.f90:407` |
| Average annual | `do isalt=1,cs_db%num_salts  →  if (pco%salt_aqu%d == "y") then  →  if (pco%csvou` | `header_salt.f90:437` |

The header and units rows for every file are written by `header_salt`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `do isalt = 1, cs_db%num_salts` | aa, mon, yr | Open/print guard. |
| `do isalt=1,cs_db%num_salts` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%salt_aqu%d == "y"` | All files | Enables output for this frequency. |
| `pco%salt_aqu%m == "y"` | aa, mon, yr | Enables output for this frequency. |
| `pco%salt_aqu%y == "y"` | aa, yr | Enables output for this frequency. |
| `time%end_mo == 1` | aa, mon, yr | Writes rows at month end. |
| `time%end_sim == 1 .and. pco%salt_aqu%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | aa, yr | Writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_salt` | Basin name and program string. |
| Header row | `header_salt` | Column names for time, identity, the num_salt name, and the `salt_balance_aqu` values. |
| Units row | `header_salt` | Units for the value columns. |
| Data row | `aqu_salt_output` | One `salt_balance_aqu` record for one num_salt at the active frequency. |

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
| `num_salt_name` | | `(asaltb_d(iaq)%salt(isalt)%conc,isalt=1,cs_db%num_salts)` | Name of the num_salt this row reports (one row per num_salt). |
| `diss` | kg | `asaltb_d%salt(i)%diss` | salt ion mass transferred from sorbed phase to dissolved phase |
| `rchrg` | kg | `asaltb_d%salt(i)%rchrg` | salt ion mass reaching the water table (recharge) |
| `seep` | kg | `asaltb_d%salt(i)%seep` | salt ion mass seepage out of aquifer |
| `saltgw` | kg | `asaltb_d%salt(i)%saltgw` | salt ion mass loaded to streams from the aquifer |
| `irr` | kg | `asaltb_d%salt(i)%irr` | salt ion mass removed via irrigation (groundwater pumping) |
| `div` | kg | `asaltb_d%salt(i)%div` | salt ion mass removed via diversion |
| `mass` |  | `asaltb_d%salt(i)%mass` | kg !salt ion mass in aquifer |
| `conc` | g/m3 | `asaltb_d%salt(i)%conc` | salt ion mass concentration in groundwater |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `salt_balance_aqu` record for one num_salt. `aqu_salt_output` loops over the simulated num_salts (`(asaltb_d(iaq)%salt(isalt)%conc,isalt=1,cs_db%num_salts)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated num_salt.
2. If the frequency's print flag is on, write that num_salt's current `salt_balance_aqu` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `aqu_salt_output.f90:36` | `5060` | time, identity, num_salt name, one `salt_balance_aqu` record |
| `aqu_salt_output.f90:46` | `5061` | time, identity, num_salt name, one `salt_balance_aqu` record |
| `aqu_salt_output.f90:78` | `5062` | time, identity, num_salt name, one `salt_balance_aqu` record |
| `aqu_salt_output.f90:88` | `5063` | time, identity, num_salt name, one `salt_balance_aqu` record |
| `aqu_salt_output.f90:131` | `5064` | time, identity, num_salt name, one `salt_balance_aqu` record |
| `aqu_salt_output.f90:141` | `5065` | time, identity, num_salt name, one `salt_balance_aqu` record |
| `aqu_salt_output.f90:177` | `5066` | time, identity, num_salt name, one `salt_balance_aqu` record |
| `aqu_salt_output.f90:187` | `5067` | time, identity, num_salt name, one `salt_balance_aqu` record |

Header and file-open statements are in `header_salt`.

## Review Notes

- Every frequency shares the `salt_balance_aqu` layout; the Columns Written table applies to all files in the family.
- Rows repeat per num_salt: an object with N simulated num_salts produces N rows per period.
- Column names, units, and meanings are taken from the `salt_balance_aqu` type definition in `salt_aquifer`.
- Auto-derived from the writer's per-num_salt output type; prose sections may benefit from human review.

## Source Links

- Writer: [`aqu_salt_output`](../procedures/aqu_salt_output.md)
- Header / opener: [`header_salt`](../procedures/header_salt.md)
- Data type: `salt_aquifer::salt_balance_aqu`

## Evidence Used

- `aqu_salt_output.f90`
- `header_salt.f90`
- `salt_aquifer.f90` (`type salt_balance_aqu`)
