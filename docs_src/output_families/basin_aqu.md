---
kind: output_family
source_symbols:
- basin_aquifer_output
- header_write
title: basin_aqu_*
status: filled
source_hash: 5a136bb7f8b9b587
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`basin_aquifer_output`](../procedures/basin_aquifer_output.md)  
**Primary data type:** `aquifer_module::aquifer_dynamic`  
**Files covered:** `basin_aqu_day`, `basin_aqu_mon`, `basin_aqu_yr`, `basin_aqu_aa` text/CSV pairs

## Bottom Line

`basin_aqu_*` is the `basin_aqu` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `aquifer_dynamic` state object written by `basin_aquifer_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `basin_aqu` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_aqu_day.txt` | `basin_aqu_day.csv` | 2090 | 2094 | `header_write.f90:60` |
| Monthly | `basin_aqu_mon.txt` | `basin_aqu_mon.csv` | 2091 | 2095 | `header_write.f90:75` |
| Yearly | `basin_aqu_yr.txt` | `basin_aqu_yr.csv` | 2092 | 2096 | `header_write.f90:90` |
| Average annual | `basin_aqu_aa.txt` | `basin_aqu_aa.csv` | 2093 | 2097 | `header_write.f90:105` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `header_write.f90:60` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%aqu_bsn%m == "y") then` | `header_write.f90:75` |
| Yearly | `if (time%end_mo == 1) then  →  if (time%end_yr == 1) then  →  if (pco%aqu_bsn%y ` | `header_write.f90:90` |
| Average annual | `if (time%end_mo == 1) then  →  if (time%end_sim == 1 .and. pco%aqu_bsn%a == "y")` | `header_write.f90:105` |

The header and units rows for every file are written by `header_write`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%aqu_bsn%d == "y"` | day | Enables output for this frequency. |
| `pco%aqu_bsn%m == "y"` | mon | Enables output for this frequency. |
| `pco%aqu_bsn%y == "y"` | yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the configured print interval. |
| `time%end_mo == 1` | aa, mon, yr | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%aqu_bsn%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_write` | Basin name and program string. |
| Header row | `header_write` | Column names for the time, identity, and `aquifer_dynamic` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `basin_aquifer_output` | One `aquifer_dynamic` record for the active frequency. |

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
| `flo` | mm | `baqu_d%flo` | lateral flow from aquifer |
| `dep_wt` | m | `baqu_d%dep_wt` | average depth from average surface elevation to water table |
| `stor` | mm | `baqu_d%stor` | average water storage in aquifer in timestep |
| `rchrg` | mm | `baqu_d%rchrg` | recharge entering aquifer from other objects |
| `seep` | mm | `baqu_d%seep` | seepage from bottom of aquifer |
| `revap` | mm | `baqu_d%revap` | plant water uptake and evaporation |
| `no3_st` | kg/ha N | `baqu_d%no3_st` | current total NO3-N mass in aquifer |
| `minp` | kg/ha P | `baqu_d%minp` | mineral phosphorus transported in return (lateral) flow |
| `cbn` | percent | `baqu_d%cbn` | organic carbon in aquifer - currently static |
| `orgn` | kg/ha P | `baqu_d%orgn` | organic nitrogen in aquifer - currently static |
| `no3_rchg` | kg/ha N | `baqu_d%no3_rchg` | nitrate NO3-N flowing into aquifer from another object |
| `no3_loss` | kg/ha | `baqu_d%no3_loss` | nitrate NO3-N loss |
| `no3_lat` | kg/ha N | `baqu_d%no3_lat` | nitrate loading to reach in groundwater |
| `no3_seep` | kg/ha N | `baqu_d%no3_seep` | seepage of no3 to next object |
| `flo_cha` | mm H2O | `baqu_d%flo_cha` | surface runoff flowing into channels |
| `flo_res` | mm H2O | `baqu_d%flo_res` | surface runoff flowing into reservoirs |
| `flo_ls` | mm H2O | `baqu_d%flo_ls` | surface runoff flowing into a landscape element (hru or ru) |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`baqu_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `aquifer_dynamic` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `basin_aquifer_output` from the finer state. Storage/level fields reported as period averages (divided by the number of steps): `dep_wt`, `no3_st`, `stor`. Remaining fields are period sums.

## Writer Flow

`basin_aquifer_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `aquifer_dynamic` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_aquifer_output.f90:29` | `2090` | time, identity, `baqu_d(idx)` record |
| `basin_aquifer_output.f90:31` | `2094` | time, identity, `baqu_d(idx)` record |
| `basin_aquifer_output.f90:44` | `2091` | time, identity, `baqu_m(idx)` record |
| `basin_aquifer_output.f90:46` | `2095` | time, identity, `baqu_m(idx)` record |
| `basin_aquifer_output.f90:59` | `2092` | time, identity, `baqu_y(idx)` record |
| `basin_aquifer_output.f90:61` | `2096` | time, identity, `baqu_y(idx)` record |
| `basin_aquifer_output.f90:71` | `2093` | time, identity, `baqu_a(idx)` record |
| `basin_aquifer_output.f90:73` | `2097` | time, identity, `baqu_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `aquifer_dynamic` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `aquifer_dynamic` type definition in `aquifer_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`basin_aquifer_output`](../procedures/basin_aquifer_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `aquifer_module::aquifer_dynamic`

## Evidence Used

- `basin_aquifer_output.f90`
- `header_write.f90`
- `aquifer_module.f90` (`type aquifer_dynamic`)
