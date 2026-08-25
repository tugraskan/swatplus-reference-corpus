---
kind: output_family
source_symbols:
- header_const
- hru_cs_output
title: hru_cs_*
status: filled
source_hash: 9ab3084eddb9f7f7
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_const`](../procedures/header_const.md)  
**Written by:** [`hru_cs_output`](../procedures/hru_cs_output.md)  
**Primary data type:** `cs_module::cs_balance`  
**Files covered:** `hru_cs_day`, `hru_cs_mon`, `hru_cs_yr`, `hru_cs_aa` text/CSV pairs

## Bottom Line

`hru_cs_*` is the `hru_cs` constituent time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. `hru_cs_output` writes each value field **once per simulated constituent**: the row is time and object identity, then each field (`soil`, `surq`, `sedm`, `latq`, `urbq`, `wetq`, `tile`, `perc`, `wtsp`, `irsw`, `irgw`, `irwo`, `rain`, `dryd`, `fert`, `uptk`, `rctn`, `sorb`, `conc`, `srbd`) repeated across all constituents (an implied-do loop, `N = number of simulated constituents`).

Only the file name, unit number, print condition, and source state object differ between frequencies; the field set is identical.

> **What each row means:** the `hru_cs` values for one object over one reporting period (daily, monthly, yearly, average annual). Each value field appears once per simulated constituent, so the file is grouped by field and, within a field, ordered by constituent. If a run simulates N constituents there are N columns per field.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hru_cs_day.txt` | `hru_cs_day.csv` | 6021 | 6022 | `header_const.f90:190` |
| Monthly | `hru_cs_mon.txt` | `hru_cs_mon.csv` | 6023 | 6024 | `header_const.f90:231` |
| Yearly | `hru_cs_yr.txt` | `hru_cs_yr.csv` | 6025 | 6026 | `header_const.f90:272` |
| Average annual | `hru_cs_aa.txt` | `hru_cs_aa.csv` | 6027 | 6028 | `header_const.f90:313` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:190` |
| Monthly | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:231` |
| Yearly | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:272` |
| Average annual | `if (pco%cs_basin%d == "y" .and. cs_db%num_cs  →  0) then  →  if (pco%cs_basin%m ` | `header_const.f90:313` |

The header and units rows for every file are written by `header_const`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%cs_basin%a == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_basin%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_basin%m == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_basin%y == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_hru%a == "y" .and. cs_db%num_cs` | aa | Enables output for this frequency. |
| `pco%cs_hru%d == "y" .and. cs_db%num_cs` | All files | Enables output for this frequency. |
| `pco%cs_hru%m == "y" .and. cs_db%num_cs` | aa, mon, yr | Enables output for this frequency. |
| `pco%cs_hru%y == "y" .and. cs_db%num_cs` | aa, yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_const` | Basin name and program string. |
| Header row | `header_const` | Column names; each value field is repeated per constituent. |
| Units row | `header_const` | Units for the value columns. |
| Data row | `hru_cs_output` | For one object: each field written once per constituent via an implied-do loop. |

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
| `soil` (x N constituents) |  | `hcsb_d%cs(i)%soil` | constituents = seo4,seo3,boron total mass in the soil profile |
| `surq` (x N constituents) | kg/ha | `hcsb_d%cs(i)%surq` | mass lost in surface runoff in HRU |
| `sedm` (x N constituents) | kg/ha | `hcsb_d%cs(i)%sedm` | mass lost in sediment runoff in HRU |
| `latq` (x N constituents) | kg/ha | `hcsb_d%cs(i)%latq` | mass in lateral flow in HRU |
| `urbq` (x N constituents) | kg/ha | `hcsb_d%cs(i)%urbq` | mass in urban runoff |
| `wetq` (x N constituents) | kg/ha | `hcsb_d%cs(i)%wetq` | mass in wetland outflow |
| `tile` (x N constituents) | kg/ha | `hcsb_d%cs(i)%tile` | mass in tile flow in HRU |
| `perc` (x N constituents) | kg/ha | `hcsb_d%cs(i)%perc` | mass leached past bottom of soil |
| `wtsp` (x N constituents) | kg/ha | `hcsb_d%cs(i)%wtsp` | mass in wetland seepage (to soil profile) |
| `irsw` (x N constituents) | kg/ha | `hcsb_d%cs(i)%irsw` | mass applied on soil via surface water irrigation |
| `irgw` (x N constituents) | kg/ha | `hcsb_d%cs(i)%irgw` | mass applied on soil via groundwater irrigation |
| `irwo` (x N constituents) | kg/ha | `hcsb_d%cs(i)%irwo` | mass applied on soil via irrigation from without (wo) the watershed |
| `rain` (x N constituents) | kg/ha | `hcsb_d%cs(i)%rain` | mass added to soil via rainfall |
| `dryd` (x N constituents) | kg/ha | `hcsb_d%cs(i)%dryd` | mass added to soil via dry atmospheric deposition |
| `fert` (x N constituents) | kg/ha | `hcsb_d%cs(i)%fert` | mass added to soil via fertilizer |
| `uptk` (x N constituents) | kg/ha | `hcsb_d%cs(i)%uptk` | mass taken up by crop roots |
| `rctn` (x N constituents) | kg/ha | `hcsb_d%cs(i)%rctn` | mass transferred by chemical reaction |
| `sorb` (x N constituents) | kg/ha | `hcsb_d%cs(i)%sorb` | mass transferred by sorption |
| `conc` (x N constituents) | mg/L | `hcsb_d%cs(i)%conc` | concentration in soil water (averaged over all soil layers) |
| `srbd` (x N constituents) | kg/ha | `hcsb_d%cs(i)%srbd` | mass sorbed to soil |

## Frequency-Specific Behavior

The value fields are identical for every frequency (daily, monthly, yearly, average annual); only the file name, unit number, print flag, and source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency detail.

## Data Sources And Calculations

Each value comes from the matching field of the `cs_balance` record for one constituent (`hcsb_d%cs(i)`). `hru_cs_output` loops over the simulated constituents with an implied-do; daily rows are per-timestep and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For the reported object, write the time and identity fields.
2. For each value field (`soil`, `surq`, `sedm`, `latq`, `urbq`, `wetq`, `tile`, `perc`, `wtsp`, `irsw`, `irgw`, `irwo`, `rain`, `dryd`, `fert`, `uptk`, `rctn`, `sorb`, `conc`, `srbd`), write that field for constituent 1..N via an implied-do loop.
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hru_cs_output.f90:49` | `6021` | time, identity, then each field x N constituents |
| `hru_cs_output.f90:71` | `6022` | time, identity, then each field x N constituents |
| `hru_cs_output.f90:128` | `6023` | time, identity, then each field x N constituents |
| `hru_cs_output.f90:150` | `6024` | time, identity, then each field x N constituents |
| `hru_cs_output.f90:230` | `6025` | time, identity, then each field x N constituents |
| `hru_cs_output.f90:252` | `6026` | time, identity, then each field x N constituents |
| `hru_cs_output.f90:325` | `6027` | time, identity, then each field x N constituents |
| `hru_cs_output.f90:347` | `6028` | time, identity, then each field x N constituents |

Header and file-open statements are in `header_const`.

## Review Notes

- Columns are grouped by field, and each field is written once per simulated constituent (N columns per field).
- The value fields and their order are taken from the `hru_cs_output` write statement; units and meanings come from the `cs_balance` type in `cs_module`.
- N depends on the run (`cs_db%num_cs`); the header row names the concrete columns.
- Auto-derived from source; prose sections may benefit from human review.

## Source Links

- Writer: [`hru_cs_output`](../procedures/hru_cs_output.md)
- Header / opener: [`header_const`](../procedures/header_const.md)
- Data type: `cs_module::cs_balance`

## Evidence Used

- `hru_cs_output.f90`
- `header_const.f90`
- `cs_module.f90` (`type cs_balance`)
