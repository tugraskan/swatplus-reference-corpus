---
kind: output_family
source_symbols:
- header_hyd
- hydout_output
title: hydout_*
status: filled
source_hash: 2674b99e605b3d84
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_hyd`](../procedures/header_hyd.md)  
**Written by:** [`hydout_output`](../procedures/hydout_output.md)  
**Primary data type:** `hydrograph_module::hyd_output`  
**Files covered:** `hydout_day`, `hydout_mon`, `hydout_yr`, `hydout_aa` text/CSV pairs

## Bottom Line

`hydout_*` is the `hydout` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `hyd_output` state object written by `hydout_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `hydout` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hydout_day.txt` | `hydout_day.csv` | 2580 | 2584 | `header_hyd.f90:20` |
| Monthly | `hydout_mon.txt` | `hydout_mon.csv` | 2581 | 2585 | `header_hyd.f90:35` |
| Yearly | `hydout_yr.txt` | `hydout_yr.csv` | 2582 | 2586 | `header_hyd.f90:50` |
| Average annual | `hydout_aa.txt` | `hydout_aa.csv` | 2583 | 2587 | `header_hyd.f90:65` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%hyd%d == "y") then` | `header_hyd.f90:20` |
| Monthly | `if (pco%hyd%m == "y") then` | `header_hyd.f90:35` |
| Yearly | `if (pco%hyd%y == "y") then` | `header_hyd.f90:50` |
| Average annual | `if (pco%hyd%a == "y") then` | `header_hyd.f90:65` |

The header and units rows for every file are written by `header_hyd`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%hyd%a == "y"` | aa | Enables output for this frequency. |
| `pco%hyd%d == "y"` | day | Enables output for this frequency. |
| `pco%hyd%m == "y"` | mon | Enables output for this frequency. |
| `pco%hyd%y == "y"` | yr | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_hyd` | Basin name and program string. |
| Header row | `header_hyd` | Column names for the time, identity, and `hyd_output` values. |
| Units row | `header_hyd` | Units for the value columns. |
| Data row | `hydout_output` | One `hyd_output` record for the active frequency. |

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

Each value column is the matching field of the `hyd_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `hydout_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`hydout_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `hyd_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hydout_output.f90:22` | `2580` | time, identity, `ht1(idx)` record |
| `hydout_output.f90:27` | `2584` | time, identity, `ht1(idx)` record |
| `hydout_output.f90:39` | `2581` | time, identity, time/identity fields |
| `hydout_output.f90:44` | `2585` | time, identity, time/identity fields |
| `hydout_output.f90:58` | `2582` | time, identity, time/identity fields |
| `hydout_output.f90:63` | `2586` | time, identity, time/identity fields |
| `hydout_output.f90:76` | `2583` | time, identity, time/identity fields |
| `hydout_output.f90:81` | `2587` | time, identity, time/identity fields |

Header and file-open statements are in `header_hyd`.

## Review Notes

- Every frequency shares the `hyd_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `hyd_output` type definition in `hydrograph_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`hydout_output`](../procedures/hydout_output.md)
- Header / opener: [`header_hyd`](../procedures/header_hyd.md)
- Data type: `hydrograph_module::hyd_output`

## Evidence Used

- `hydout_output.f90`
- `header_hyd.f90`
- `hydrograph_module.f90` (`type hyd_output`)
