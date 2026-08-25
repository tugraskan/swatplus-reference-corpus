---
kind: output_family
source_symbols:
- header_wetland
- wetland_output
title: wetland_*
status: filled
source_hash: 8b4933433b420ac7
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_wetland`](../procedures/header_wetland.md)  
**Written by:** [`wetland_output`](../procedures/wetland_output.md)  
**Primary data type:** `water_body_module::water_body`  
**Files covered:** `wetland_day`, `wetland_mon`, `wetland_yr`, `wetland_aa` text/CSV pairs

## Bottom Line

`wetland_*` is the `wetland` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `water_body` state object written by `wetland_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `wetland` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `wetland_day.txt` | `wetland_day.csv` | 2548 | 2552 | `header_wetland.f90:12` |
| Monthly | `wetland_mon.txt` | `wetland_mon.csv` | 2549 | 2553 | `header_wetland.f90:28` |
| Yearly | `wetland_yr.txt` | `wetland_yr.csv` | 2550 | 2554 | `header_wetland.f90:44` |
| Average annual | `wetland_aa.txt` | `wetland_aa.csv` | 2551 | 2555 | `header_wetland.f90:61` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%res%d == "y") then` | `header_wetland.f90:12` |
| Monthly | `if (pco%res%m == "y") then` | `header_wetland.f90:28` |
| Yearly | `if (pco%res%y == "y") then` | `header_wetland.f90:44` |
| Average annual | `if (pco%res%a == "y") then` | `header_wetland.f90:61` |

The header and units rows for every file are written by `header_wetland`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%res%a == "y"` | aa | Enables output for this frequency. |
| `pco%res%d == "y"` | day | Enables output for this frequency. |
| `pco%res%m == "y"` | mon | Enables output for this frequency. |
| `pco%res%y == "y"` | yr | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_wetland` | Basin name and program string. |
| Header row | `header_wetland` | Column names for the time, identity, and `water_body` values. |
| Units row | `header_wetland` | Units for the value columns. |
| Data row | `wetland_output` | One `water_body` record for the active frequency. |

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
| `area_ha` | ha | `wet_wat_d%area_ha` | water body surface area |
| `precip` | m3 | `wet_wat_d%precip` | precip on the water body |
| `evap` | m3 | `wet_wat_d%evap` | evaporation from the water surface |
| `seep` | m3 | `wet_wat_d%seep` | seepage from bottom of water body |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`wet_wat_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `water_body` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `wetland_output` from the finer state. Storage/level fields reported as period averages (divided by the number of steps): `flo`. Remaining fields are period sums.

## Writer Flow

`wetland_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `water_body` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `wetland_output.f90:20` | `2548` | time, identity, `wet_wat_d(idx)` record |
| `wetland_output.f90:23` | `2552` | time, identity, `wet_wat_d(idx)` record |
| `wetland_output.f90:46` | `2549` | time, identity, `wet_wat_m(idx)` record |
| `wetland_output.f90:49` | `2553` | time, identity, `wet_wat_m(idx)` record |
| `wetland_output.f90:66` | `2550` | time, identity, `wet_wat_y(idx)` record |
| `wetland_output.f90:69` | `2554` | time, identity, `wet_wat_y(idx)` record |
| `wetland_output.f90:83` | `2551` | time, identity, `wet_wat_a(idx)` record |
| `wetland_output.f90:86` | `2555` | time, identity, `wet_wat_a(idx)` record |

Header and file-open statements are in `header_wetland`.

## Review Notes

- Every frequency shares the `water_body` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `water_body` type definition in `water_body_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`wetland_output`](../procedures/wetland_output.md)
- Header / opener: [`header_wetland`](../procedures/header_wetland.md)
- Data type: `water_body_module::water_body`

## Evidence Used

- `wetland_output.f90`
- `header_wetland.f90`
- `water_body_module.f90` (`type water_body`)
