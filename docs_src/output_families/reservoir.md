---
kind: output_family
source_symbols:
- header_reservoir
- reservoir_output
title: reservoir_*
status: filled
source_hash: 1e4093c1b8b91a6e
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_reservoir`](../procedures/header_reservoir.md)  
**Written by:** [`reservoir_output`](../procedures/reservoir_output.md)  
**Primary data type:** `water_body_module::water_body`  
**Files covered:** `reservoir_day`, `reservoir_mon`, `reservoir_yr`, `reservoir_aa` text/CSV pairs

## Bottom Line

`reservoir_*` is the `reservoir` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `water_body` state object written by `reservoir_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `reservoir` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `reservoir_day.txt` | `reservoir_day.csv` | 2540 | 2544 | `header_reservoir.f90:15` |
| Monthly | `reservoir_mon.txt` | `reservoir_mon.csv` | 2541 | 2545 | `header_reservoir.f90:30` |
| Yearly | `reservoir_yr.txt` | `reservoir_yr.csv` | 2542 | 2546 | `header_reservoir.f90:45` |
| Average annual | `reservoir_aa.txt` | `reservoir_aa.csv` | 2543 | 2547 | `header_reservoir.f90:60` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%res%d == "y" .and. sp_ob%res  →  0 ) then` | `header_reservoir.f90:15` |
| Monthly | `if (pco%res%m == "y" .and. sp_ob%res  →  0 ) then` | `header_reservoir.f90:30` |
| Yearly | `if (pco%res%y == "y" .and. sp_ob%res  →  0 ) then` | `header_reservoir.f90:45` |
| Average annual | `if (pco%res%a == "y" .and. sp_ob%res  →  0) then` | `header_reservoir.f90:60` |

The header and units rows for every file are written by `header_reservoir`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%res%a == "y" .and. sp_ob%res` | aa | Enables output for this frequency. |
| `pco%res%d == "y" .and. sp_ob%res` | day | Enables output for this frequency. |
| `pco%res%m == "y" .and. sp_ob%res` | mon | Enables output for this frequency. |
| `pco%res%y == "y" .and. sp_ob%res` | yr | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_reservoir` | Basin name and program string. |
| Header row | `header_reservoir` | Column names for the time, identity, and `water_body` values. |
| Units row | `header_reservoir` | Units for the value columns. |
| Data row | `reservoir_output` | One `water_body` record for the active frequency. |

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
| `area_ha` | ha | `res_wat_d%area_ha` | water body surface area |
| `precip` | m3 | `res_wat_d%precip` | precip on the water body |
| `evap` | m3 | `res_wat_d%evap` | evaporation from the water surface |
| `seep` | m3 | `res_wat_d%seep` | seepage from bottom of water body |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`res_wat_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `water_body` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `reservoir_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`reservoir_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `water_body` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `reservoir_output.f90:20` | `2540` | time, identity, `res_wat_d(idx)` record |
| `reservoir_output.f90:23` | `2544` | time, identity, `res_wat_d(idx)` record |
| `reservoir_output.f90:43` | `2541` | time, identity, `res_wat_m(idx)` record |
| `reservoir_output.f90:46` | `2545` | time, identity, `res_wat_m(idx)` record |
| `reservoir_output.f90:63` | `2542` | time, identity, `res_wat_y(idx)` record |
| `reservoir_output.f90:66` | `2546` | time, identity, `res_wat_y(idx)` record |
| `reservoir_output.f90:80` | `2543` | time, identity, `res_wat_a(idx)` record |
| `reservoir_output.f90:83` | `2547` | time, identity, `res_wat_a(idx)` record |

Header and file-open statements are in `header_reservoir`.

## Review Notes

- Every frequency shares the `water_body` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `water_body` type definition in `water_body_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`reservoir_output`](../procedures/reservoir_output.md)
- Header / opener: [`header_reservoir`](../procedures/header_reservoir.md)
- Data type: `water_body_module::water_body`

## Evidence Used

- `reservoir_output.f90`
- `header_reservoir.f90`
- `water_body_module.f90` (`type water_body`)
