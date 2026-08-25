---
kind: output_family
source_symbols:
- basin_sdchannel_output
- header_write
title: basin_sd_cha_*
status: filled
source_hash: a3b8ea335b087f37
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`basin_sdchannel_output`](../procedures/basin_sdchannel_output.md)  
**Primary data type:** `water_body_module::water_body`  
**Files covered:** `basin_sd_cha_day`, `basin_sd_cha_mon`, `basin_sd_cha_yr`, `basin_sd_cha_aa` text/CSV pairs

## Bottom Line

`basin_sd_cha_*` is the `basin_sd_cha` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `water_body` state object written by `basin_sdchannel_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `basin_sd_cha` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_sd_cha_day.txt` | `basin_sd_cha_day.csv` | 4900 | 4904 | `header_write.f90:309` |
| Monthly | `basin_sd_cha_mon.txt` | `basin_sd_cha_mon.csv` | 4901 | 4905 | `header_write.f90:324` |
| Yearly | `basin_sd_cha_yr.txt` | `basin_sd_cha_yr.csv` | 4902 | 4906 | `header_write.f90:339` |
| Average annual | `basin_sd_cha_aa.txt` | `basin_sd_cha_aa.csv` | 4903 | 4907 | `header_write.f90:354` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `header_write.f90:309` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%sd_chan_bsn%m == "y") then` | `header_write.f90:324` |
| Yearly | `if (time%end_yr == 1) then  →  if (pco%sd_chan_bsn%y == "y") then` | `header_write.f90:339` |
| Average annual | `if (time%end_sim == 1 .and. pco%sd_chan_bsn%a == "y") then` | `header_write.f90:354` |

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
| Header row | `header_write` | Column names for the time, identity, and `water_body` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `basin_sdchannel_output` | One `water_body` record for the active frequency. |

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
| `area_ha` | ha | `bch_wat_d%area_ha` | water body surface area |
| `precip` | m3 | `bch_wat_d%precip` | precip on the water body |
| `evap` | m3 | `bch_wat_d%evap` | evaporation from the water surface |
| `seep` | m3 | `bch_wat_d%seep` | seepage from bottom of water body |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`bch_wat_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `water_body` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `basin_sdchannel_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`basin_sdchannel_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `water_body` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_sdchannel_output.f90:34` | `4900` | time, identity, `bch_wat_d(idx)` record |
| `basin_sdchannel_output.f90:37` | `4904` | time, identity, `bch_wat_d(idx)` record |
| `basin_sdchannel_output.f90:52` | `4901` | time, identity, `bch_wat_m(idx)` record |
| `basin_sdchannel_output.f90:55` | `4905` | time, identity, `bch_wat_m(idx)` record |
| `basin_sdchannel_output.f90:73` | `4902` | time, identity, `bch_wat_y(idx)` record |
| `basin_sdchannel_output.f90:76` | `4906` | time, identity, `bch_wat_y(idx)` record |
| `basin_sdchannel_output.f90:91` | `4903` | time, identity, `bch_wat_a(idx)` record |
| `basin_sdchannel_output.f90:94` | `4907` | time, identity, `bch_wat_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `water_body` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `water_body` type definition in `water_body_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`basin_sdchannel_output`](../procedures/basin_sdchannel_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `water_body_module::water_body`

## Evidence Used

- `basin_sdchannel_output.f90`
- `header_write.f90`
- `water_body_module.f90` (`type water_body`)
