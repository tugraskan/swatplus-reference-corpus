---
kind: output_family
source_symbols:
- ch_cs_output
- header_const
title: channel_cs_*
status: filled
source_hash: 346777bd9285f6c2
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_const`](../procedures/header_const.md)  
**Written by:** [`ch_cs_output`](../procedures/ch_cs_output.md)  
**Primary data type:** `ch_cs_module::ch_cs_balance`  
**Files covered:** `channel_cs_day`, `channel_cs_mon`, `channel_cs_yr`, `channel_cs_aa` text/CSV pairs

## Bottom Line

`channel_cs_*` is the `channel_cs` constituent time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. `ch_cs_output` writes each value field **once per simulated constituent**: the row is time and object identity, then each field (`tot_in`, `gw_in`, `tot_out`, `seep`, `irr`, `div`, `water`, `conc`) repeated across all constituents (an implied-do loop, `N = number of simulated constituents`).

Only the file name, unit number, print condition, and source state object differ between frequencies; the field set is identical.

> **What each row means:** the `channel_cs` values for one object over one reporting period (daily, monthly, yearly, average annual). Each value field appears once per simulated constituent, so the file is grouped by field and, within a field, ordered by constituent. If a run simulates N constituents there are N columns per field.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `channel_cs_day.txt` | `channel_cs_day.csv` | 6030 | 6031 | `header_const.f90:483` |
| Monthly | `channel_cs_mon.txt` | `channel_cs_mon.csv` | 6032 | 6033 | `header_const.f90:512` |
| Yearly | `channel_cs_yr.txt` | `channel_cs_yr.csv` | 6034 | 6035 | `header_const.f90:541` |
| Average annual | `channel_cs_aa.txt` | `channel_cs_aa.csv` | 6036 | 6037 | `header_const.f90:570` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do ics = 1, cs_db%num_cs  →  if (pco%cs_chn%d == "y") then` | `header_const.f90:483` |
| Monthly | `do ics = 1, cs_db%num_cs  →  if (pco%cs_chn%d == "y") then  →  if (pco%csvout ==` | `header_const.f90:512` |
| Yearly | `do ics = 1, cs_db%num_cs  →  if (pco%cs_chn%d == "y") then  →  if (pco%csvout ==` | `header_const.f90:541` |
| Average annual | `do ics = 1, cs_db%num_cs  →  if (pco%cs_chn%d == "y") then  →  if (pco%csvout ==` | `header_const.f90:570` |

The header and units rows for every file are written by `header_const`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `do ics = 1, cs_db%num_cs` | All files | Open/print guard. |
| `do ics=1,cs_db%num_cs` | aa, mon, yr | Open/print guard. |
| `pco%cs_chn%d == "y"` | All files | Enables output for this frequency. |
| `pco%cs_chn%m == "y"` | aa, mon, yr | Enables output for this frequency. |
| `pco%cs_chn%y == "y"` | aa, yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `time%end_mo == 1` | aa, mon, yr | Writes rows at month end. |
| `time%end_sim == 1 .and. pco%cs_chn%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | aa, yr | Writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_const` | Basin name and program string. |
| Header row | `header_const` | Column names; each value field is repeated per constituent. |
| Units row | `header_const` | Units for the value columns. |
| Data row | `ch_cs_output` | For one object: each field written once per constituent via an implied-do loop. |

## Columns Written

Each value field below is written **once per simulated constituent** (N columns per field, grouped by field):

| Column Group | Unit | Source Field | Source-Backed Meaning |
|---|---|---|---|
| `jday` | | `time%day` | Julian day / simulation day. |
| `mon` | | `time%mo` | Simulation month. |
| `day` | | `time%day_mo` | Day of month. |
| `yr` | | `time%yrc` | Simulation year. |
| `unit` | | `object index` | Index / id of the reported object. |
| `gis_id` | | `ob(iob)%gis_id` | GIS / object id. |
| `tot_in` (x N constituents) | kg | `chcs_d%cs(i)%tot_in` | total constituent entering the channel |
| `gw_in` (x N constituents) | kg | `chcs_d%cs(i)%gw_in` | total constituent entering the channel from groundwater |
| `tot_out` (x N constituents) | kg | `chcs_d%cs(i)%tot_out` | total constituent leaving the channel |
| `seep` (x N constituents) | kg | `chcs_d%cs(i)%seep` | constituent mass leaving the channel via seepage |
| `irr` (x N constituents) | kg | `chcs_d%cs(i)%irr` | constituent mass leaving the channel via irrigation |
| `div` (x N constituents) | kg | `chcs_d%cs(i)%div` | constituent mass added to or removed from the channel via diversion |
| `water` (x N constituents) | kg | `chcs_d%cs(i)%water` | total constituent in water at end of day |
| `conc` (x N constituents) | mg/L | `chcs_d%cs(i)%conc` | constituent concentration in channel water at end of day |

## Frequency-Specific Behavior

The value fields are identical for every frequency (daily, monthly, yearly, average annual); only the file name, unit number, print flag, and source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency detail.

## Data Sources And Calculations

Each value comes from the matching field of the `ch_cs_balance` record for one constituent (`chcs_d%cs(i)`). `ch_cs_output` loops over the simulated constituents with an implied-do; daily rows are per-timestep and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For the reported object, write the time and identity fields.
2. For each value field (`tot_in`, `gw_in`, `tot_out`, `seep`, `irr`, `div`, `water`, `conc`), write that field for constituent 1..N via an implied-do loop.
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `ch_cs_output.f90:43` | `6030` | time, identity, then each field x N constituents |
| `ch_cs_output.f90:53` | `6031` | time, identity, then each field x N constituents |
| `ch_cs_output.f90:85` | `6032` | time, identity, then each field x N constituents |
| `ch_cs_output.f90:95` | `6033` | time, identity, then each field x N constituents |
| `ch_cs_output.f90:138` | `6034` | time, identity, then each field x N constituents |
| `ch_cs_output.f90:148` | `6035` | time, identity, then each field x N constituents |
| `ch_cs_output.f90:185` | `6036` | time, identity, then each field x N constituents |
| `ch_cs_output.f90:195` | `6037` | time, identity, then each field x N constituents |

Header and file-open statements are in `header_const`.

## Review Notes

- Columns are grouped by field, and each field is written once per simulated constituent (N columns per field).
- The value fields and their order are taken from the `ch_cs_output` write statement; units and meanings come from the `ch_cs_balance` type in `ch_cs_module`.
- N depends on the run (`cs_db%num_cs`); the header row names the concrete columns.
- Auto-derived from source; prose sections may benefit from human review.

## Source Links

- Writer: [`ch_cs_output`](../procedures/ch_cs_output.md)
- Header / opener: [`header_const`](../procedures/header_const.md)
- Data type: `ch_cs_module::ch_cs_balance`

## Evidence Used

- `ch_cs_output.f90`
- `header_const.f90`
- `ch_cs_module.f90` (`type ch_cs_balance`)
