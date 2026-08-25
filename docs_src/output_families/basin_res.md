---
kind: output_family
source_symbols:
- basin_reservoir_output
- header_write
title: basin_res_*
status: filled
source_hash: c5fe9856c2ac15dc
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`basin_reservoir_output`](../procedures/basin_reservoir_output.md)  
**Primary data type:** `water_body_module::water_body`  
**Files covered:** `basin_res_day`, `basin_res_mon`, `basin_res_yr`, `basin_res_aa` text/CSV pairs

## Bottom Line

`basin_res_*` is the `basin_res` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `water_body` state object written by `basin_reservoir_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `basin_res` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_res_day.txt` | `basin_res_day.csv` | 2100 | 2104 | `header_write.f90:122` |
| Monthly | `basin_res_mon.txt` | `basin_res_mon.csv` | 2101 | 2105 | `header_write.f90:137` |
| Yearly | `basin_res_yr.txt` | `basin_res_yr.csv` | 2102 | 2106 | `header_write.f90:152` |
| Average annual | `basin_res_aa.txt` | `basin_res_aa.csv` | 2103 | 2107 | `header_write.f90:167` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `header_write.f90:122` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%res_bsn%m == "y") then` | `header_write.f90:137` |
| Yearly | `if (time%end_mo == 1) then  →  if (time%end_yr == 1) then  →  if (pco%res_bsn%y ` | `header_write.f90:152` |
| Average annual | `if (time%end_mo == 1) then  →  if (time%end_sim == 1 .and. pco%res_bsn%a == "y")` | `header_write.f90:167` |

The header and units rows for every file are written by `header_write`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the configured print interval. |
| `pco%res_bsn%d == "y"` | day | Enables output for this frequency. |
| `pco%res_bsn%m == "y"` | mon | Enables output for this frequency. |
| `pco%res_bsn%y == "y"` | yr | Enables output for this frequency. |
| `time%end_mo == 1` | aa, mon, yr | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%res_bsn%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_write` | Basin name and program string. |
| Header row | `header_write` | Column names for the time, identity, and `water_body` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `basin_reservoir_output` | One `water_body` record for the active frequency. |

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
| `area_ha` | ha | `bres_wat_d%area_ha` | water body surface area |
| `precip` | m3 | `bres_wat_d%precip` | precip on the water body |
| `evap` | m3 | `bres_wat_d%evap` | evaporation from the water surface |
| `seep` | m3 | `bres_wat_d%seep` | seepage from bottom of water body |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`bres_wat_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `water_body` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `basin_reservoir_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`basin_reservoir_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `water_body` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_reservoir_output.f90:39` | `2100` | time, identity, `bres_wat_d(idx)` record |
| `basin_reservoir_output.f90:42` | `2104` | time, identity, `bres_wat_d(idx)` record |
| `basin_reservoir_output.f90:56` | `2101` | time, identity, `bres_wat_m(idx)` record |
| `basin_reservoir_output.f90:59` | `2105` | time, identity, `bres_wat_m(idx)` record |
| `basin_reservoir_output.f90:75` | `2102` | time, identity, `bres_wat_y(idx)` record |
| `basin_reservoir_output.f90:78` | `2106` | time, identity, `bres_wat_y(idx)` record |
| `basin_reservoir_output.f90:93` | `2103` | time, identity, `bres_wat_a(idx)` record |
| `basin_reservoir_output.f90:96` | `2107` | time, identity, `bres_wat_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `water_body` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `water_body` type definition in `water_body_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`basin_reservoir_output`](../procedures/basin_reservoir_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `water_body_module::water_body`

## Evidence Used

- `basin_reservoir_output.f90`
- `header_write.f90`
- `water_body_module.f90` (`type water_body`)
