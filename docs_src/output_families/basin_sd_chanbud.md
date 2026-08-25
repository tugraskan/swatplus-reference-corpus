---
kind: output_family
source_symbols:
- basin_chanbud_output
- header_write
title: basin_sd_chanbud_*
status: filled
source_hash: ab6d67a1c4715277
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`basin_chanbud_output`](../procedures/basin_chanbud_output.md)  
**Primary data type:** `sd_channel_module::channel_sediment_budget_output`  
**Files covered:** `basin_sd_chanbud_day`, `basin_sd_chanbud_mon`, `basin_sd_chanbud_yr`, `basin_sd_chanbud_aa` text/CSV pairs

## Bottom Line

`basin_sd_chanbud_*` is the `basin_sd_chanbud` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `channel_sediment_budget_output` state object written by `basin_chanbud_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `basin_sd_chanbud` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_sd_chanbud_day.txt` | `basin_sd_chanbud_day.csv` | 2128 | 2132 | `header_write.f90:434` |
| Monthly | `basin_sd_chanbud_mon.txt` | `basin_sd_chanbud_mon.csv` | 2129 | 2133 | `header_write.f90:449` |
| Yearly | `basin_sd_chanbud_yr.txt` | `basin_sd_chanbud_yr.csv` | 2130 | 2134 | `header_write.f90:464` |
| Average annual | `basin_sd_chanbud_aa.txt` | `basin_sd_chanbud_aa.csv` | 2131 | 2135 | `header_write.f90:479` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `header_write.f90:434` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%sd_chan_bsn%m == "y") then` | `header_write.f90:449` |
| Yearly | `if (time%end_yr == 1) then  →  if (pco%sd_chan_bsn%y == "y") then` | `header_write.f90:464` |
| Average annual | `if (time%end_sim == 1 .and. pco%sd_chan_bsn%a == "y") then` | `header_write.f90:479` |

The header and units rows for every file are written by `header_write`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the configured print interval. |
| `pco%sd_chan_bsn%d == "y"` | day | Enables output for this frequency. |
| `pco%sd_chan_bsn%m == "y"` | mon | Enables output for this frequency. |
| `pco%sd_chan_bsn%y == "y"` | yr | Enables output for this frequency. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%sd_chan_bsn%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_write` | Basin name and program string. |
| Header row | `header_write` | Column names for the time, identity, and `channel_sediment_budget_output` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `basin_chanbud_output` | One `channel_sediment_budget_output` record for the active frequency. |

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
| `in_sed` | t | `bch_sed_bud_d%in_sed` | incoming sediment to channel |
| `out_sed` | t | `bch_sed_bud_d%out_sed` | outgoing sediment from channel |
| `fp_dep` | t | `bch_sed_bud_d%fp_dep` | flood plain deposition |
| `ch_dep` | t | `bch_sed_bud_d%ch_dep` | channel deposition |
| `bank_ero` | t | `bch_sed_bud_d%bank_ero` | channel bank erosion |
| `bed_ero` | t | `bch_sed_bud_d%bed_ero` | channel bed erosion |
| `in_no3` | t | `bch_sed_bud_d%in_no3` | incoming no3 to channel |
| `in_orgn` | t | `bch_sed_bud_d%in_orgn` | incoming organic n to channel |
| `out_no3` | t | `bch_sed_bud_d%out_no3` | outgoing no3 from channel |
| `out_orgn` | t | `bch_sed_bud_d%out_orgn` | outgoing organic n from channel |
| `fp_no3` | t | `bch_sed_bud_d%fp_no3` | flood plain no3 lost |
| `bank_no3` | t | `bch_sed_bud_d%bank_no3` | bank no3 gain |
| `bed_no3` | t | `bch_sed_bud_d%bed_no3` | bed no3 gain |
| `fp_orgn` | t | `bch_sed_bud_d%fp_orgn` | flood plain organic n deposited |
| `ch_orgn` | t | `bch_sed_bud_d%ch_orgn` | channel organic n deposited |
| `bank_orgn` | t | `bch_sed_bud_d%bank_orgn` | bank organic n gain from erosion |
| `bed_orgn` | t | `bch_sed_bud_d%bed_orgn` | bed organic n gain from erosion |
| `in_solp` | t | `bch_sed_bud_d%in_solp` | incoming soluble p to channel |
| `in_orgp` | t | `bch_sed_bud_d%in_orgp` | incoming organic p to channel |
| `out_solp` | t | `bch_sed_bud_d%out_solp` | outgoing soluble p from channel |
| `out_orgp` | t | `bch_sed_bud_d%out_orgp` | outgoing organic p from channel |
| `fp_solp` | t | `bch_sed_bud_d%fp_solp` | flood plain soluble p lost |
| `bank_solp` | t | `bch_sed_bud_d%bank_solp` | bank no3 gain |
| `bed_solp` | t | `bch_sed_bud_d%bed_solp` | bed no3 gain |
| `fp_orgp` | t | `bch_sed_bud_d%fp_orgp` | flood plain organic p deposited |
| `ch_orgp` | t | `bch_sed_bud_d%ch_orgp` | channel organic p deposited |
| `bank_orgp` | t | `bch_sed_bud_d%bank_orgp` | bank organic p gain from erosion |
| `bed_orgp` | t | `bch_sed_bud_d%bed_orgp` | bed organic n gain from erosion |
| `no3_orgn` | t | `bch_sed_bud_d%no3_orgn` | in channel transformation from no3 to organic n |
| `solp_orgp` | t | `bch_sed_bud_d%solp_orgp` | in channel transformation from no3 to organic n |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`bch_sed_bud_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `channel_sediment_budget_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `basin_chanbud_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`basin_chanbud_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `channel_sediment_budget_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_chanbud_output.f90:23` | `2128` | time, identity, `bch_sed_bud_d(idx)` record |
| `basin_chanbud_output.f90:25` | `2132` | time, identity, `bch_sed_bud_d(idx)` record |
| `basin_chanbud_output.f90:37` | `2129` | time, identity, `bch_sed_bud_m(idx)` record |
| `basin_chanbud_output.f90:39` | `2133` | time, identity, `bch_sed_bud_m(idx)` record |
| `basin_chanbud_output.f90:52` | `2130` | time, identity, `bch_sed_bud_y(idx)` record |
| `basin_chanbud_output.f90:54` | `2134` | time, identity, `bch_sed_bud_y(idx)` record |
| `basin_chanbud_output.f90:65` | `2131` | time, identity, `bch_sed_bud_a(idx)` record |
| `basin_chanbud_output.f90:67` | `2135` | time, identity, `bch_sed_bud_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `channel_sediment_budget_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `channel_sediment_budget_output` type definition in `sd_channel_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`basin_chanbud_output`](../procedures/basin_chanbud_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `sd_channel_module::channel_sediment_budget_output`

## Evidence Used

- `basin_chanbud_output.f90`
- `header_write.f90`
- `sd_channel_module.f90` (`type channel_sediment_budget_output`)
