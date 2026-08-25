---
kind: output_family
source_symbols:
- header_const
- ru_cs_output
title: rout_unit_cs_*
status: filled
source_hash: c0b025271dc94012
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_const`](../procedures/header_const.md)  
**Written by:** [`ru_cs_output`](../procedures/ru_cs_output.md)  
**Primary data type:** `cs_module::cs_balance`  
**Files covered:** `rout_unit_cs_day`, `rout_unit_cs_mon`, `rout_unit_cs_yr`, `rout_unit_cs_aa` text/CSV pairs

## Bottom Line

`rout_unit_cs_*` is the `rout_unit_cs` constituent time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. `ru_cs_output` writes each value field **once per simulated constituent**: the row is time and object identity, then each field (`sedm`, `wtsp`, `irsw`, `irgw`, `irwo`, `rain`, `dryd`, `fert`, `uptk`, `rctn`, `sorb`) repeated across all constituents (an implied-do loop, `N = number of simulated constituents`).

Only the file name, unit number, print condition, and source state object differ between frequencies; the field set is identical.

> **What each row means:** the `rout_unit_cs` values for one object over one reporting period (daily, monthly, yearly, average annual). Each value field appears once per simulated constituent, so the file is grouped by field and, within a field, ordered by constituent. If a run simulates N constituents there are N columns per field.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `rout_unit_cs_day.txt` | `rout_unit_cs_day.csv` | 6070 | 6071 | `header_const.f90:731` |
| Monthly | `rout_unit_cs_mon.txt` | `rout_unit_cs_mon.csv` | 6072 | 6073 | `header_const.f90:769` |
| Yearly | `rout_unit_cs_yr.txt` | `rout_unit_cs_yr.csv` | 6074 | 6075 | `header_const.f90:807` |
| Average annual | `rout_unit_cs_aa.txt` | `rout_unit_cs_aa.csv` | 6076 | 6077 | `header_const.f90:845` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:731` |
| Monthly | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:769` |
| Yearly | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:807` |
| Average annual | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:845` |

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
| `pco%cs_res%a == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_res%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_res%m == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_res%y == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_ru%a == "y" .and. cs_db%num_cs` | aa | Enables output for this frequency. |
| `pco%cs_ru%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_ru%m == "y" .and. cs_db%num_cs` | aa, mon, yr | Enables output for this frequency. |
| `pco%cs_ru%y == "y" .and. cs_db%num_cs` | aa, yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `sp_ob%aqu` | All files | Open/print guard. |
| `sp_ob%chandeg` | All files | Open/print guard. |
| `sp_ob%res` | All files | Open/print guard. |
| `sp_ob%ru` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_const` | Basin name and program string. |
| Header row | `header_const` | Column names; each value field is repeated per constituent. |
| Units row | `header_const` | Units for the value columns. |
| Data row | `ru_cs_output` | For one object: each field written once per constituent via an implied-do loop. |

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
| `sedm` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%sedm` | mass lost in sediment runoff in HRU |
| `wtsp` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%wtsp` | mass in wetland seepage (to soil profile) |
| `irsw` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%irsw` | mass applied on soil via surface water irrigation |
| `irgw` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%irgw` | mass applied on soil via groundwater irrigation |
| `irwo` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%irwo` | mass applied on soil via irrigation from without (wo) the watershed |
| `rain` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%rain` | mass added to soil via rainfall |
| `dryd` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%dryd` | mass added to soil via dry atmospheric deposition |
| `fert` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%fert` | mass added to soil via fertilizer |
| `uptk` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%uptk` | mass taken up by crop roots |
| `rctn` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%rctn` | mass transferred by chemical reaction |
| `sorb` (x N constituents) | kg/ha | `ru_hru_csb_d%cs(i)%sorb` | mass transferred by sorption |

## Frequency-Specific Behavior

The value fields are identical for every frequency (daily, monthly, yearly, average annual); only the file name, unit number, print flag, and source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency detail.

## Data Sources And Calculations

Each value comes from the matching field of the `cs_balance` record for one constituent (`ru_hru_csb_d%cs(i)`). `ru_cs_output` loops over the simulated constituents with an implied-do; daily rows are per-timestep and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For the reported object, write the time and identity fields.
2. For each value field (`sedm`, `wtsp`, `irsw`, `irgw`, `irwo`, `rain`, `dryd`, `fert`, `uptk`, `rctn`, `sorb`), write that field for constituent 1..N via an implied-do loop.
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `ru_cs_output.f90:48` | `6070` | time, identity, then each field x N constituents |
| `ru_cs_output.f90:66` | `6071` | time, identity, then each field x N constituents |
| `ru_cs_output.f90:124` | `6072` | time, identity, then each field x N constituents |
| `ru_cs_output.f90:142` | `6073` | time, identity, then each field x N constituents |
| `ru_cs_output.f90:200` | `6074` | time, identity, then each field x N constituents |
| `ru_cs_output.f90:218` | `6075` | time, identity, then each field x N constituents |
| `ru_cs_output.f90:275` | `6076` | time, identity, then each field x N constituents |
| `ru_cs_output.f90:293` | `6077` | time, identity, then each field x N constituents |

Header and file-open statements are in `header_const`.

## Review Notes

- Columns are grouped by field, and each field is written once per simulated constituent (N columns per field).
- The value fields and their order are taken from the `ru_cs_output` write statement; units and meanings come from the `cs_balance` type in `cs_module`.
- N depends on the run (`cs_db%num_cs`); the header row names the concrete columns.
- Auto-derived from source; prose sections may benefit from human review.

## Source Links

- Writer: [`ru_cs_output`](../procedures/ru_cs_output.md)
- Header / opener: [`header_const`](../procedures/header_const.md)
- Data type: `cs_module::cs_balance`

## Evidence Used

- `ru_cs_output.f90`
- `header_const.f90`
- `cs_module.f90` (`type cs_balance`)
