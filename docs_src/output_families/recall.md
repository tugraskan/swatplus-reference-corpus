---
kind: output_family
source_symbols:
- header_write
- recall_output
title: recall_*
status: filled
source_hash: d89546a7951dc09c
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`recall_output`](../procedures/recall_output.md)  
**Primary data type:** `hydrograph_module::hyd_output`  
**Files covered:** `recall_day`, `recall_mon`, `recall_yr`, `recall_aa` text/CSV pairs

## Bottom Line

`recall_*` is the `recall` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `hyd_output` state object written by `recall_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `recall` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `recall_day.txt` | `recall_day.csv` | 4600 | 4604 | `header_write.f90:184` |
| Monthly | `recall_mon.txt` | `recall_mon.csv` | 4601 | 4605 | `header_write.f90:199` |
| Yearly | `recall_yr.txt` | `recall_yr.csv` | 4602 | 4606 | `header_write.f90:214` |
| Average annual | `recall_aa.txt` | `recall_aa.csv` | 4603 | 4607 | `header_write.f90:229` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%aqu_bsn%d == "y") then  →  if (pco%res_bsn%d == "y") then  →  if (pco%re` | `header_write.f90:184` |
| Monthly | `if (pco%aqu_bsn%d == "y") then  →  if (pco%res_bsn%d == "y") then  →  if (pco%re` | `header_write.f90:199` |
| Yearly | `if (pco%aqu_bsn%d == "y") then  →  if (pco%res_bsn%d == "y") then  →  if (pco%re` | `header_write.f90:214` |
| Average annual | `if (pco%aqu_bsn%d == "y") then  →  if (pco%res_bsn%d == "y") then  →  if (pco%re` | `header_write.f90:229` |

The header and units rows for every file are written by `header_write`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%aqu_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%recall%a == "y"` | aa | Enables output for this frequency. |
| `pco%recall%d == "y"` | All files | Enables output for this frequency. |
| `pco%recall%m == "y"` | mon | Enables output for this frequency. |
| `pco%recall%y == "y"` | aa, yr | Enables output for this frequency. |
| `pco%res_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%res_bsn%y == "y"` | All files | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_write` | Basin name and program string. |
| Header row | `header_write` | Column names for the time, identity, and `hyd_output` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `recall_output` | One `hyd_output` record for the active frequency. |

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
| `flo` | m^3 | `rec_d%flo` | volume of water |
| `sed` | metric tons | `rec_d%sed` | sediment |
| `orgn` | kg N | `rec_d%orgn` | organic N |
| `sedp` | kg P | `rec_d%sedp` | organic P |
| `no3` | kg N | `rec_d%no3` | NO3-N |
| `solp` | kg P | `rec_d%solp` | mineral (soluble P) |
| `chla` | kg | `rec_d%chla` | chlorophyll-a |
| `nh3` | kg N | `rec_d%nh3` | NH3 |
| `no2` | kg N | `rec_d%no2` | NO2 |
| `cbod` | kg | `rec_d%cbod` | carbonaceous biological oxygen demand |
| `dox` | kg | `rec_d%dox` | dissolved oxygen |
| `san` | tons | `rec_d%san` | detached sand |
| `sil` | tons | `rec_d%sil` | detached silt |
| `cla` | tons | `rec_d%cla` | detached clay |
| `sag` | tons | `rec_d%sag` | detached small ag |
| `lag` | tons | `rec_d%lag` | detached large ag |
| `grv` | tons | `rec_d%grv` | gravel |
| `temp` | deg c | `rec_d%temp` | temperature |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`rec_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `hyd_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `recall_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`recall_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `hyd_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `recall_output.f90:23` | `4600` | time, identity, `rec_d(idx)` record |
| `recall_output.f90:25` | `4604` | time, identity, `rec_d(idx)` record |
| `recall_output.f90:34` | `4601` | time, identity, `rec_m(idx)` record |
| `recall_output.f90:36` | `4605` | time, identity, `rec_m(idx)` record |
| `recall_output.f90:46` | `4602` | time, identity, `rec_y(idx)` record |
| `recall_output.f90:48` | `4606` | time, identity, `rec_y(idx)` record |
| `recall_output.f90:58` | `4603` | time, identity, `rec_a(idx)` record |
| `recall_output.f90:60` | `4607` | time, identity, `rec_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `hyd_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `hyd_output` type definition in `hydrograph_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`recall_output`](../procedures/recall_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `hydrograph_module::hyd_output`

## Evidence Used

- `recall_output.f90`
- `header_write.f90`
- `hydrograph_module.f90` (`type hyd_output`)
