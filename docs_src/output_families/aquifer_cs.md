---
kind: output_family
source_symbols:
- aqu_cs_output
- header_const
title: aquifer_cs_*
status: filled
source_hash: beb217580e81af02
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_const`](../procedures/header_const.md)  
**Written by:** [`aqu_cs_output`](../procedures/aqu_cs_output.md)  
**Primary data type:** `cs_aquifer::cs_balance_aqu`  
**Files covered:** `aquifer_cs_day`, `aquifer_cs_mon`, `aquifer_cs_yr`, `aquifer_cs_aa` text/CSV pairs

## Bottom Line

`aquifer_cs_*` is the `aquifer_cs` constituent time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. `aqu_cs_output` writes each value field **once per simulated constituent**: the row is time and object identity, then each field (`csgw`, `rchrg`, `seep`, `irr`, `div`, `sorb`, `rctn`, `mass`, `conc`, `srbd`) repeated across all constituents (an implied-do loop, `N = number of simulated constituents`).

Only the file name, unit number, print condition, and source state object differ between frequencies; the field set is identical.

> **What each row means:** the `aquifer_cs` values for one object over one reporting period (daily, monthly, yearly, average annual). Each value field appears once per simulated constituent, so the file is grouped by field and, within a field, ordered by constituent. If a run simulates N constituents there are N columns per field.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `aquifer_cs_day.txt` | `aquifer_cs_day.csv` | 6060 | 6061 | `header_const.f90:355` |
| Monthly | `aquifer_cs_mon.txt` | `aquifer_cs_mon.csv` | 6062 | 6063 | `header_const.f90:387` |
| Yearly | `aquifer_cs_yr.txt` | `aquifer_cs_yr.csv` | 6064 | 6065 | `header_const.f90:419` |
| Average annual | `aquifer_cs_aa.txt` | `aquifer_cs_aa.csv` | 6066 | 6067 | `header_const.f90:451` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do ics=1,cs_db%num_cs  →  if (pco%cs_aqu%d == "y") then` | `header_const.f90:355` |
| Monthly | `do ics=1,cs_db%num_cs  →  if (pco%cs_aqu%d == "y") then  →  if (pco%csvout == "y` | `header_const.f90:387` |
| Yearly | `do ics=1,cs_db%num_cs  →  if (pco%cs_aqu%d == "y") then  →  if (pco%csvout == "y` | `header_const.f90:419` |
| Average annual | `do ics=1,cs_db%num_cs  →  if (pco%cs_aqu%d == "y") then  →  if (pco%csvout == "y` | `header_const.f90:451` |

The header and units rows for every file are written by `header_const`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `do ics=1,cs_db%num_cs` | All files | Open/print guard. |
| `pco%cs_aqu%d == "y"` | All files | Enables output for this frequency. |
| `pco%cs_aqu%m == "y"` | aa, mon, yr | Enables output for this frequency. |
| `pco%cs_aqu%y == "y"` | aa, yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `time%end_mo == 1` | aa, mon, yr | Writes rows at month end. |
| `time%end_sim == 1 .and. pco%cs_aqu%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | aa, yr | Writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_const` | Basin name and program string. |
| Header row | `header_const` | Column names; each value field is repeated per constituent. |
| Units row | `header_const` | Units for the value columns. |
| Data row | `aqu_cs_output` | For one object: each field written once per constituent via an implied-do loop. |

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
| `csgw` (x N constituents) | kg | `acsb_d%cs(i)%csgw` | mass loaded to streams from the aquifer |
| `rchrg` (x N constituents) | kg | `acsb_d%cs(i)%rchrg` | mass reaching the water table (recharge) |
| `seep` (x N constituents) | kg | `acsb_d%cs(i)%seep` | mass seepage out of aquifer |
| `irr` (x N constituents) | kg | `acsb_d%cs(i)%irr` | mass removed via irrigation (groundwater pumping) |
| `div` (x N constituents) | kg | `acsb_d%cs(i)%div` | mass removed or added via diversion |
| `sorb` (x N constituents) | kg | `acsb_d%cs(i)%sorb` | mass transferred from sorbed phase to dissolved phase |
| `rctn` (x N constituents) | kg | `acsb_d%cs(i)%rctn` | mass transferred by chemical reaction |
| `mass` (x N constituents) |  | `acsb_d%cs(i)%mass` | kg !mass stored in aquifer |
| `conc` (x N constituents) | g/m3 | `acsb_d%cs(i)%conc` | concentration in groundwater |
| `srbd` (x N constituents) | kg | `acsb_d%cs(i)%srbd` | mass sorbed to aquifer material |

## Frequency-Specific Behavior

The value fields are identical for every frequency (daily, monthly, yearly, average annual); only the file name, unit number, print flag, and source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency detail.

## Data Sources And Calculations

Each value comes from the matching field of the `cs_balance_aqu` record for one constituent (`acsb_d%cs(i)`). `aqu_cs_output` loops over the simulated constituents with an implied-do; daily rows are per-timestep and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For the reported object, write the time and identity fields.
2. For each value field (`csgw`, `rchrg`, `seep`, `irr`, `div`, `sorb`, `rctn`, `mass`, `conc`, `srbd`), write that field for constituent 1..N via an implied-do loop.
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `aqu_cs_output.f90:39` | `6060` | time, identity, then each field x N constituents |
| `aqu_cs_output.f90:51` | `6061` | time, identity, then each field x N constituents |
| `aqu_cs_output.f90:88` | `6062` | time, identity, then each field x N constituents |
| `aqu_cs_output.f90:100` | `6063` | time, identity, then each field x N constituents |
| `aqu_cs_output.f90:150` | `6064` | time, identity, then each field x N constituents |
| `aqu_cs_output.f90:162` | `6065` | time, identity, then each field x N constituents |
| `aqu_cs_output.f90:205` | `6066` | time, identity, then each field x N constituents |
| `aqu_cs_output.f90:217` | `6067` | time, identity, then each field x N constituents |

Header and file-open statements are in `header_const`.

## Review Notes

- Columns are grouped by field, and each field is written once per simulated constituent (N columns per field).
- The value fields and their order are taken from the `aqu_cs_output` write statement; units and meanings come from the `cs_balance_aqu` type in `cs_aquifer`.
- N depends on the run (`cs_db%num_cs`); the header row names the concrete columns.
- Auto-derived from source; prose sections may benefit from human review.

## Source Links

- Writer: [`aqu_cs_output`](../procedures/aqu_cs_output.md)
- Header / opener: [`header_const`](../procedures/header_const.md)
- Data type: `cs_aquifer::cs_balance_aqu`

## Evidence Used

- `aqu_cs_output.f90`
- `header_const.f90`
- `cs_aquifer.f90` (`type cs_balance_aqu`)
