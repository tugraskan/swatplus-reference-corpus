---
kind: output_family
source_symbols:
- ch_salt_output
- header_salt
title: channel_salt_*
status: filled
source_hash: 8e56f5f7926e74dd
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_salt`](../procedures/header_salt.md)  
**Written by:** [`ch_salt_output`](../procedures/ch_salt_output.md)  
**Primary data type:** `ch_salt_module::ch_salt_balance`  
**Files covered:** `channel_salt_day`, `channel_salt_mon`, `channel_salt_yr`, `channel_salt_aa` text/CSV pairs

## Bottom Line

`channel_salt_*` is the `channel_salt` salt ion time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. `ch_salt_output` writes each value field **once per simulated salt ion**: the row is time and object identity, then each field (`tot_in`, `gw_in`, `tot_out`, `seep`, `irr`, `div`, `water`, `conc`) repeated across all salt ions (an implied-do loop, `N = number of simulated salt ions`).

Only the file name, unit number, print condition, and source state object differ between frequencies; the field set is identical.

> **What each row means:** the `channel_salt` values for one object over one reporting period (daily, monthly, yearly, average annual). Each value field appears once per simulated salt ion, so the file is grouped by field and, within a field, ordered by salt ion. If a run simulates N salt ions there are N columns per field.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `channel_salt_day.txt` | `channel_salt_day.csv` | 5030 | 5031 | `header_salt.f90:467` |
| Monthly | `channel_salt_mon.txt` | `channel_salt_mon.csv` | 5032 | 5033 | `header_salt.f90:496` |
| Yearly | `channel_salt_yr.txt` | `channel_salt_yr.csv` | 5034 | 5035 | `header_salt.f90:525` |
| Average annual | `channel_salt_aa.txt` | `channel_salt_aa.csv` | 5036 | 5037 | `header_salt.f90:554` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do isalt = 1, cs_db%num_salts  →  if (pco%salt_chn%d == "y") then` | `header_salt.f90:467` |
| Monthly | `do isalt = 1, cs_db%num_salts  →  if (pco%salt_chn%d == "y") then  →  if (pco%cs` | `header_salt.f90:496` |
| Yearly | `do isalt = 1, cs_db%num_salts  →  if (pco%salt_chn%d == "y") then  →  if (pco%cs` | `header_salt.f90:525` |
| Average annual | `do isalt = 1, cs_db%num_salts  →  if (pco%salt_chn%d == "y") then  →  if (pco%cs` | `header_salt.f90:554` |

The header and units rows for every file are written by `header_salt`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `do isalt = 1, cs_db%num_salts` | All files | Open/print guard. |
| `do isalt=1,cs_db%num_salts` | aa, mon, yr | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%salt_chn%d == "y"` | All files | Enables output for this frequency. |
| `pco%salt_chn%m == "y"` | aa, mon, yr | Enables output for this frequency. |
| `pco%salt_chn%y == "y"` | aa, yr | Enables output for this frequency. |
| `time%end_mo == 1` | aa, mon, yr | Writes rows at month end. |
| `time%end_sim == 1 .and. pco%salt_chn%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | aa, yr | Writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_salt` | Basin name and program string. |
| Header row | `header_salt` | Column names; each value field is repeated per salt ion. |
| Units row | `header_salt` | Units for the value columns. |
| Data row | `ch_salt_output` | For one object: each field written once per salt ion via an implied-do loop. |

## Columns Written

Each value field below is written **once per simulated salt ion** (N columns per field, grouped by field):

| Column Group | Unit | Source Field | Source-Backed Meaning |
|---|---|---|---|
| `jday` | | `time%day` | Julian day / simulation day. |
| `mon` | | `time%mo` | Simulation month. |
| `day` | | `time%day_mo` | Day of month. |
| `yr` | | `time%yrc` | Simulation year. |
| `unit` | | `object index` | Index / id of the reported object. |
| `gis_id` | | `ob(iob)%gis_id` | GIS / object id. |
| `tot_in` (x N salt ions) | kg | `chsalt_d%salt(i)%tot_in` | total salt ion entering the channel |
| `gw_in` (x N salt ions) | kg | `chsalt_d%salt(i)%gw_in` | total salt ion entering the channel from groundwater |
| `tot_out` (x N salt ions) | kg | `chsalt_d%salt(i)%tot_out` | total salt ion leaving the channel |
| `seep` (x N salt ions) | kg | `chsalt_d%salt(i)%seep` | total salt ion leaving the channel via seepage |
| `irr` (x N salt ions) | kg | `chsalt_d%salt(i)%irr` | salt ion mass leaving the channel via irrigation |
| `div` (x N salt ions) | kg | `chsalt_d%salt(i)%div` | salt ion mass added to or removed from the channel via diversion |
| `water` (x N salt ions) | kg | `chsalt_d%salt(i)%water` | total salt ion in water at end of day |
| `conc` (x N salt ions) | mg/L | `chsalt_d%salt(i)%conc` | salt ion concentration in channel water at end of day |

## Frequency-Specific Behavior

The value fields are identical for every frequency (daily, monthly, yearly, average annual); only the file name, unit number, print flag, and source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency detail.

## Data Sources And Calculations

Each value comes from the matching field of the `ch_salt_balance` record for one salt ion (`chsalt_d%salt(i)`). `ch_salt_output` loops over the simulated salt ions with an implied-do; daily rows are per-timestep and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For the reported object, write the time and identity fields.
2. For each value field (`tot_in`, `gw_in`, `tot_out`, `seep`, `irr`, `div`, `water`, `conc`), write that field for salt ion 1..N via an implied-do loop.
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `ch_salt_output.f90:42` | `5030` | time, identity, then each field x N salt ions |
| `ch_salt_output.f90:52` | `5031` | time, identity, then each field x N salt ions |
| `ch_salt_output.f90:84` | `5032` | time, identity, then each field x N salt ions |
| `ch_salt_output.f90:94` | `5033` | time, identity, then each field x N salt ions |
| `ch_salt_output.f90:137` | `5034` | time, identity, then each field x N salt ions |
| `ch_salt_output.f90:147` | `5035` | time, identity, then each field x N salt ions |
| `ch_salt_output.f90:184` | `5036` | time, identity, then each field x N salt ions |
| `ch_salt_output.f90:194` | `5037` | time, identity, then each field x N salt ions |

Header and file-open statements are in `header_salt`.

## Review Notes

- Columns are grouped by field, and each field is written once per simulated salt ion (N columns per field).
- The value fields and their order are taken from the `ch_salt_output` write statement; units and meanings come from the `ch_salt_balance` type in `ch_salt_module`.
- N depends on the run (`cs_db%num_salts`); the header row names the concrete columns.
- Auto-derived from source; prose sections may benefit from human review.

## Source Links

- Writer: [`ch_salt_output`](../procedures/ch_salt_output.md)
- Header / opener: [`header_salt`](../procedures/header_salt.md)
- Data type: `ch_salt_module::ch_salt_balance`

## Evidence Used

- `ch_salt_output.f90`
- `header_salt.f90`
- `ch_salt_module.f90` (`type ch_salt_balance`)
