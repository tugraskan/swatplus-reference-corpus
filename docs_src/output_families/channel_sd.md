---
kind: output_family
source_symbols:
- header_sd_channel
- sd_channel_output
title: channel_sd_*
status: filled
source_hash: 00588ad447d48b95
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_sd_channel`](../procedures/header_sd_channel.md)  
**Written by:** [`sd_channel_output`](../procedures/sd_channel_output.md)  
**Primary data type:** `hydrograph_module::hyd_output`  
**Files covered:** `channel_sd_day`, `channel_sd_mon`, `channel_sd_yr`, `channel_sd_aa` text/CSV pairs

## Bottom Line

`channel_sd_*` is the `channel_sd` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `hyd_output` state object written by `sd_channel_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `channel_sd` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `channel_sd_day.txt` | `channel_sd_day.csv` | 2500 | 2504 | `header_sd_channel.f90:29` |
| Monthly | `channel_sd_mon.txt` | `channel_sd_mon.csv` | 2501 | 2505 | `header_sd_channel.f90:58` |
| Yearly | `channel_sd_yr.txt` | `channel_sd_yr.csv` | 2502 | 2506 | `header_sd_channel.f90:88` |
| Average annual | `channel_sd_aa.txt` | `channel_sd_aa.csv` | 2503 | 2507 | `header_sd_channel.f90:118` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then` | `header_sd_channel.f90:29` |
| Monthly | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:58` |
| Yearly | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:88` |
| Average annual | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:118` |

The header and units rows for every file are written by `header_sd_channel`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%sd_chan%a == "y"` | aa | Enables output for this frequency. |
| `pco%sd_chan%d == "y"` | All files | Enables output for this frequency. |
| `pco%sd_chan%m == "y"` | mon | Enables output for this frequency. |
| `pco%sd_chan%y == "y"` | aa, yr | Enables output for this frequency. |
| `sp_ob%chandeg` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_sd_channel` | Basin name and program string. |
| Header row | `header_sd_channel` | Column names for the time, identity, and `hyd_output` values. |
| Units row | `header_sd_channel` | Units for the value columns. |
| Data row | `sd_channel_output` | One `hyd_output` record for the active frequency. |

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
| `flo` | m^3 | `ch_stor%flo` | volume of water |
| `sed` | metric tons | `ch_stor%sed` | sediment |
| `orgn` | kg N | `ch_stor%orgn` | organic N |
| `sedp` | kg P | `ch_stor%sedp` | organic P |
| `no3` | kg N | `ch_stor%no3` | NO3-N |
| `solp` | kg P | `ch_stor%solp` | mineral (soluble P) |
| `chla` | kg | `ch_stor%chla` | chlorophyll-a |
| `nh3` | kg N | `ch_stor%nh3` | NH3 |
| `no2` | kg N | `ch_stor%no2` | NO2 |
| `cbod` | kg | `ch_stor%cbod` | carbonaceous biological oxygen demand |
| `dox` | kg | `ch_stor%dox` | dissolved oxygen |
| `san` | tons | `ch_stor%san` | detached sand |
| `sil` | tons | `ch_stor%sil` | detached silt |
| `cla` | tons | `ch_stor%cla` | detached clay |
| `sag` | tons | `ch_stor%sag` | detached small ag |
| `lag` | tons | `ch_stor%lag` | detached large ag |
| `grv` | tons | `ch_stor%grv` | gravel |
| `temp` | deg c | `ch_stor%temp` | temperature |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`ch_stor` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `hyd_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `sd_channel_output` from the finer state. Storage/level fields reported as period averages (divided by the number of steps): `flo`. Remaining fields are period sums.

## Writer Flow

`sd_channel_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `hyd_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `sd_channel_output.f90:25` | `2508` | time, identity, time/identity fields |
| `sd_channel_output.f90:33` | `2500` | time, identity, `ch_stor(idx)` record |
| `sd_channel_output.f90:37` | `2504` | time, identity, `ch_stor(idx)` record |
| `sd_channel_output.f90:58` | `2501` | time, identity, `ch_stor(idx)` record |
| `sd_channel_output.f90:63` | `2505` | time, identity, `ch_stor(idx)` record |
| `sd_channel_output.f90:88` | `2502` | time, identity, `ch_stor(idx)` record |
| `sd_channel_output.f90:92` | `2506` | time, identity, `ch_stor(idx)` record |
| `sd_channel_output.f90:108` | `2503` | time, identity, `ch_stor(idx)` record |
| `sd_channel_output.f90:112` | `2507` | time, identity, `ch_stor(idx)` record |

Header and file-open statements are in `header_sd_channel`.

## Review Notes

- Every frequency shares the `hyd_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `hyd_output` type definition in `hydrograph_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`sd_channel_output`](../procedures/sd_channel_output.md)
- Header / opener: [`header_sd_channel`](../procedures/header_sd_channel.md)
- Data type: `hydrograph_module::hyd_output`

## Evidence Used

- `sd_channel_output.f90`
- `header_sd_channel.f90`
- `hydrograph_module.f90` (`type hyd_output`)
