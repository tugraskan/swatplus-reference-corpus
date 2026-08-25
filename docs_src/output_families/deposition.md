---
kind: output_family
source_symbols:
- header_hyd
- hyddep_output
title: deposition_*
status: filled
source_hash: 23f8c94a52055b00
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_hyd`](../procedures/header_hyd.md)  
**Written by:** [`hyddep_output`](../procedures/hyddep_output.md)  
**Primary data type:** `hydrograph_module::hyd_output`  
**Files covered:** `deposition_day`, `deposition_mon`, `deposition_yr`, `deposition_aa` text/CSV pairs

## Bottom Line

`deposition_*` is the `deposition` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `hyd_output` state object written by `hyddep_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `deposition` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `deposition_day.txt` | `deposition_day.csv` | 2700 | 2704 | `header_hyd.f90:144` |
| Monthly | `deposition_mon.txt` | `deposition_mon.csv` | 2701 | 2705 | `header_hyd.f90:160` |
| Yearly | `deposition_yr.txt` | `deposition_yr.csv` | 2702 | 2706 | `header_hyd.f90:176` |
| Average annual | `deposition_aa.txt` | `deposition_aa.csv` | 2703 | 2707 | `header_hyd.f90:192` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%hyd%d == "y") then  →  if (pco%hyd%m == "y") then  →  if (pco%hyd%y == "` | `header_hyd.f90:144` |
| Monthly | `if (pco%hyd%d == "y") then  →  if (pco%hyd%m == "y") then  →  if (pco%hyd%y == "` | `header_hyd.f90:160` |
| Yearly | `if (pco%hyd%d == "y") then  →  if (pco%hyd%m == "y") then  →  if (pco%hyd%y == "` | `header_hyd.f90:176` |
| Average annual | `if (pco%hyd%d == "y") then  →  if (pco%hyd%m == "y") then  →  if (pco%hyd%y == "` | `header_hyd.f90:192` |

The header and units rows for every file are written by `header_hyd`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%hyd%a == "y"` | All files | Enables output for this frequency. |
| `pco%hyd%d == "y"` | All files | Enables output for this frequency. |
| `pco%hyd%m == "y"` | All files | Enables output for this frequency. |
| `pco%hyd%y == "y"` | All files | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_hyd` | Basin name and program string. |
| Header row | `header_hyd` | Column names for the time, identity, and `hyd_output` values. |
| Units row | `header_hyd` | Units for the value columns. |
| Data row | `hyddep_output` | One `hyd_output` record for the active frequency. |

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
| `flo` | m^3 | `ht1%flo` | volume of water |
| `sed` | metric tons | `ht1%sed` | sediment |
| `orgn` | kg N | `ht1%orgn` | organic N |
| `sedp` | kg P | `ht1%sedp` | organic P |
| `no3` | kg N | `ht1%no3` | NO3-N |
| `solp` | kg P | `ht1%solp` | mineral (soluble P) |
| `chla` | kg | `ht1%chla` | chlorophyll-a |
| `nh3` | kg N | `ht1%nh3` | NH3 |
| `no2` | kg N | `ht1%no2` | NO2 |
| `cbod` | kg | `ht1%cbod` | carbonaceous biological oxygen demand |
| `dox` | kg | `ht1%dox` | dissolved oxygen |
| `san` | tons | `ht1%san` | detached sand |
| `sil` | tons | `ht1%sil` | detached silt |
| `cla` | tons | `ht1%cla` | detached clay |
| `sag` | tons | `ht1%sag` | detached small ag |
| `lag` | tons | `ht1%lag` | detached large ag |
| `grv` | tons | `ht1%grv` | gravel |
| `temp` | deg c | `ht1%temp` | temperature |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`ht1` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `hyd_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `hyddep_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`hyddep_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `hyd_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hyddep_output.f90:21` | `2700` | time, identity, `ht1(idx)` record |
| `hyddep_output.f90:23` | `2704` | time, identity, `ht1(idx)` record |
| `hyddep_output.f90:33` | `2701` | time, identity, time/identity fields |
| `hyddep_output.f90:36` | `2705` | time, identity, time/identity fields |
| `hyddep_output.f90:47` | `2702` | time, identity, time/identity fields |
| `hyddep_output.f90:51` | `2706` | time, identity, time/identity fields |
| `hyddep_output.f90:63` | `2703` | time, identity, time/identity fields |
| `hyddep_output.f90:66` | `2707` | time, identity, time/identity fields |

Header and file-open statements are in `header_hyd`.

## Review Notes

- Every frequency shares the `hyd_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `hyd_output` type definition in `hydrograph_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`hyddep_output`](../procedures/hyddep_output.md)
- Header / opener: [`header_hyd`](../procedures/header_hyd.md)
- Data type: `hydrograph_module::hyd_output`

## Evidence Used

- `hyddep_output.f90`
- `header_hyd.f90`
- `hydrograph_module.f90` (`type hyd_output`)
