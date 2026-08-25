---
kind: output_family
source_symbols:
- header_sd_channel
- sd_chanbud_output
title: sd_chanbud_*
status: filled
source_hash: c927b3c44ebf15f5
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_sd_channel`](../procedures/header_sd_channel.md)  
**Written by:** [`sd_chanbud_output`](../procedures/sd_chanbud_output.md)  
**Primary data type:** `sd_channel_module::channel_sediment_budget_output`  
**Files covered:** `sd_chanbud_day`, `sd_chanbud_mon`, `sd_chanbud_yr`, `sd_chanbud_aa` text/CSV pairs

## Bottom Line

`sd_chanbud_*` is the `sd_chanbud` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `channel_sediment_budget_output` state object written by `sd_chanbud_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `sd_chanbud` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `sd_chanbud_day.txt` | `sd_chanbud_day.csv` | 4808 | 4812 | `header_sd_channel.f90:219` |
| Monthly | `sd_chanbud_mon.txt` | `sd_chanbud_mon.csv` | 4809 | 4813 | `header_sd_channel.f90:234` |
| Yearly | `sd_chanbud_yr.txt` | `sd_chanbud_yr.csv` | 4810 | 4814 | `header_sd_channel.f90:249` |
| Average annual | `sd_chanbud_aa.txt` | `sd_chanbud_aa.csv` | 4811 | 4815 | `header_sd_channel.f90:264` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:219` |
| Monthly | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:234` |
| Yearly | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:249` |
| Average annual | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:264` |

The header and units rows for every file are written by `header_sd_channel`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `1` | yr | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%sd_chan%a == "y"` | aa | Enables output for this frequency. |
| `pco%sd_chan%d == "y"` | All files | Enables output for this frequency. |
| `pco%sd_chan%m == "y"` | mon | Enables output for this frequency. |
| `pco%sd_chan%y == "y"` | All files | Enables output for this frequency. |
| `sp_ob%chandeg` | All files | Open/print guard. |
| `time%step` | yr | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_sd_channel` | Basin name and program string. |
| Header row | `header_sd_channel` | Column names for the time, identity, and `channel_sediment_budget_output` values. |
| Units row | `header_sd_channel` | Units for the value columns. |
| Data row | `sd_chanbud_output` | One `channel_sediment_budget_output` record for the active frequency. |

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
| `in_sed` | t | `ch_sed_bud%in_sed` | incoming sediment to channel |
| `out_sed` | t | `ch_sed_bud%out_sed` | outgoing sediment from channel |
| `fp_dep` | t | `ch_sed_bud%fp_dep` | flood plain deposition |
| `ch_dep` | t | `ch_sed_bud%ch_dep` | channel deposition |
| `bank_ero` | t | `ch_sed_bud%bank_ero` | channel bank erosion |
| `bed_ero` | t | `ch_sed_bud%bed_ero` | channel bed erosion |
| `in_no3` | t | `ch_sed_bud%in_no3` | incoming no3 to channel |
| `in_orgn` | t | `ch_sed_bud%in_orgn` | incoming organic n to channel |
| `out_no3` | t | `ch_sed_bud%out_no3` | outgoing no3 from channel |
| `out_orgn` | t | `ch_sed_bud%out_orgn` | outgoing organic n from channel |
| `fp_no3` | t | `ch_sed_bud%fp_no3` | flood plain no3 lost |
| `bank_no3` | t | `ch_sed_bud%bank_no3` | bank no3 gain |
| `bed_no3` | t | `ch_sed_bud%bed_no3` | bed no3 gain |
| `fp_orgn` | t | `ch_sed_bud%fp_orgn` | flood plain organic n deposited |
| `ch_orgn` | t | `ch_sed_bud%ch_orgn` | channel organic n deposited |
| `bank_orgn` | t | `ch_sed_bud%bank_orgn` | bank organic n gain from erosion |
| `bed_orgn` | t | `ch_sed_bud%bed_orgn` | bed organic n gain from erosion |
| `in_solp` | t | `ch_sed_bud%in_solp` | incoming soluble p to channel |
| `in_orgp` | t | `ch_sed_bud%in_orgp` | incoming organic p to channel |
| `out_solp` | t | `ch_sed_bud%out_solp` | outgoing soluble p from channel |
| `out_orgp` | t | `ch_sed_bud%out_orgp` | outgoing organic p from channel |
| `fp_solp` | t | `ch_sed_bud%fp_solp` | flood plain soluble p lost |
| `bank_solp` | t | `ch_sed_bud%bank_solp` | bank no3 gain |
| `bed_solp` | t | `ch_sed_bud%bed_solp` | bed no3 gain |
| `fp_orgp` | t | `ch_sed_bud%fp_orgp` | flood plain organic p deposited |
| `ch_orgp` | t | `ch_sed_bud%ch_orgp` | channel organic p deposited |
| `bank_orgp` | t | `ch_sed_bud%bank_orgp` | bank organic p gain from erosion |
| `bed_orgp` | t | `ch_sed_bud%bed_orgp` | bed organic n gain from erosion |
| `no3_orgn` | t | `ch_sed_bud%no3_orgn` | in channel transformation from no3 to organic n |
| `solp_orgp` | t | `ch_sed_bud%solp_orgp` | in channel transformation from no3 to organic n |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`ch_sed_bud` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `channel_sediment_budget_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `sd_chanbud_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`sd_chanbud_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `channel_sediment_budget_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `sd_chanbud_output.f90:19` | `4808` | time, identity, `ch_sed_bud(idx)` record |
| `sd_chanbud_output.f90:21` | `4812` | time, identity, `ch_sed_bud(idx)` record |
| `sd_chanbud_output.f90:34` | `4809` | time, identity, `ch_sed_bud_m(idx)` record |
| `sd_chanbud_output.f90:36` | `4813` | time, identity, `ch_sed_bud_m(idx)` record |
| `sd_chanbud_output.f90:50` | `4810` | time, identity, `ch_sed_bud_y(idx)` record |
| `sd_chanbud_output.f90:52` | `4814` | time, identity, `ch_sed_bud_y(idx)` record |
| `sd_chanbud_output.f90:65` | `4811` | time, identity, `ch_sed_bud_a(idx)` record |
| `sd_chanbud_output.f90:67` | `4815` | time, identity, `ch_sed_bud_a(idx)` record |

Header and file-open statements are in `header_sd_channel`.

## Review Notes

- Every frequency shares the `channel_sediment_budget_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `channel_sediment_budget_output` type definition in `sd_channel_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`sd_chanbud_output`](../procedures/sd_chanbud_output.md)
- Header / opener: [`header_sd_channel`](../procedures/header_sd_channel.md)
- Data type: `sd_channel_module::channel_sediment_budget_output`

## Evidence Used

- `sd_chanbud_output.f90`
- `header_sd_channel.f90`
- `sd_channel_module.f90` (`type channel_sediment_budget_output`)
