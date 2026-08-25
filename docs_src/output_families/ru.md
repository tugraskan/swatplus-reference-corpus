---
kind: output_family
source_symbols:
- header_write
- ru_output
title: ru_*
status: filled
source_hash: dd85896ecd9af018
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`ru_output`](../procedures/ru_output.md)  
**Primary data type:** `hydrograph_module::hyd_output`  
**Files covered:** `ru_day`, `ru_mon`, `ru_yr`, `ru_aa` text/CSV pairs

## Bottom Line

`ru_*` is the `ru` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `hyd_output` state object written by `ru_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `ru` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `ru_day.txt` | `ru_day.csv` | 2600 | 2604 | `header_write.f90:560` |
| Monthly | `ru_mon.txt` | `ru_mon.csv` | 2601 | 2605 | `header_write.f90:575` |
| Yearly | `ru_yr.txt` | `ru_yr.csv` | 2602 | 2606 | `header_write.f90:590` |
| Average annual | `ru_aa.txt` | `ru_aa.csv` | 2603 | 2607 | `header_write.f90:605` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%aqu_bsn%d == "y") then  →  if (pco%res_bsn%d == "y") then  →  if (pco%re` | `header_write.f90:560` |
| Monthly | `if (pco%aqu_bsn%d == "y") then  →  if (pco%res_bsn%d == "y") then  →  if (pco%re` | `header_write.f90:575` |
| Yearly | `if (pco%aqu_bsn%d == "y") then  →  if (pco%res_bsn%d == "y") then  →  if (pco%re` | `header_write.f90:590` |
| Average annual | `if (pco%aqu_bsn%d == "y") then  →  if (pco%res_bsn%d == "y") then  →  if (pco%re` | `header_write.f90:605` |

The header and units rows for every file are written by `header_write`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%aqu_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%chan_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%chan_bsn%y == "y"` | All files | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%recall%d == "y"` | All files | Enables output for this frequency. |
| `pco%recall%y == "y"` | All files | Enables output for this frequency. |
| `pco%recall_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%recall_bsn%y == "y"` | All files | Enables output for this frequency. |
| `pco%res_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%res_bsn%y == "y"` | All files | Enables output for this frequency. |
| `pco%ru%a == "y"` | aa | Enables output for this frequency. |
| `pco%ru%d == "y"` | All files | Enables output for this frequency. |
| `pco%ru%m == "y"` | mon | Enables output for this frequency. |
| `pco%ru%y == "y"` | aa, yr | Enables output for this frequency. |
| `pco%sd_chan_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%sd_chan_bsn%y == "y"` | All files | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_write` | Basin name and program string. |
| Header row | `header_write` | Column names for the time, identity, and `hyd_output` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `ru_output` | One `hyd_output` record for the active frequency. |

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
| `flo` | m^3 | `ru_d%flo` | volume of water |
| `sed` | metric tons | `ru_d%sed` | sediment |
| `orgn` | kg N | `ru_d%orgn` | organic N |
| `sedp` | kg P | `ru_d%sedp` | organic P |
| `no3` | kg N | `ru_d%no3` | NO3-N |
| `solp` | kg P | `ru_d%solp` | mineral (soluble P) |
| `chla` | kg | `ru_d%chla` | chlorophyll-a |
| `nh3` | kg N | `ru_d%nh3` | NH3 |
| `no2` | kg N | `ru_d%no2` | NO2 |
| `cbod` | kg | `ru_d%cbod` | carbonaceous biological oxygen demand |
| `dox` | kg | `ru_d%dox` | dissolved oxygen |
| `san` | tons | `ru_d%san` | detached sand |
| `sil` | tons | `ru_d%sil` | detached silt |
| `cla` | tons | `ru_d%cla` | detached clay |
| `sag` | tons | `ru_d%sag` | detached small ag |
| `lag` | tons | `ru_d%lag` | detached large ag |
| `grv` | tons | `ru_d%grv` | gravel |
| `temp` | deg c | `ru_d%temp` | temperature |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`ru_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `hyd_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `ru_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`ru_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `hyd_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `ru_output.f90:24` | `2600` | time, identity, `ru_d(idx)` record |
| `ru_output.f90:26` | `2604` | time, identity, `ru_d(idx)` record |
| `ru_output.f90:35` | `2601` | time, identity, `ru_m(idx)` record |
| `ru_output.f90:37` | `2605` | time, identity, `ru_m(idx)` record |
| `ru_output.f90:47` | `2602` | time, identity, `ru_y(idx)` record |
| `ru_output.f90:49` | `2606` | time, identity, `ru_y(idx)` record |
| `ru_output.f90:59` | `2603` | time, identity, `ru_a(idx)` record |
| `ru_output.f90:61` | `2607` | time, identity, `ru_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `hyd_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `hyd_output` type definition in `hydrograph_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`ru_output`](../procedures/ru_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `hydrograph_module::hyd_output`

## Evidence Used

- `ru_output.f90`
- `header_write.f90`
- `hydrograph_module.f90` (`type hyd_output`)
