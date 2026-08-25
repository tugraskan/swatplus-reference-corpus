---
kind: output_family
source_symbols:
- basin_recall_output
- header_write
title: basin_psc_*
status: filled
source_hash: 64fe7ce6edd6842b
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`basin_recall_output`](../procedures/basin_recall_output.md)  
**Primary data type:** `hydrograph_module::hyd_output`  
**Files covered:** `basin_psc_day`, `basin_psc_mon`, `basin_psc_yr`, `basin_psc_aa` text/CSV pairs

## Bottom Line

`basin_psc_*` is the `basin_psc` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `hyd_output` state object written by `basin_recall_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `basin_psc` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_psc_day.txt` | `basin_psc_day.csv` | 4500 | 4504 | `header_write.f90:497` |
| Monthly | `basin_psc_mon.txt` | `basin_psc_mon.csv` | 4501 | 4505 | `header_write.f90:512` |
| Yearly | `basin_psc_yr.txt` | `basin_psc_yr.csv` | 4502 | 4506 | `header_write.f90:527` |
| Average annual | `basin_psc_aa.txt` | `basin_psc_aa.csv` | 4503 | 4507 | `header_write.f90:542` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `header_write.f90:497` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%recall_bsn%m == "y") then` | `header_write.f90:512` |
| Yearly | `if (time%end_mo == 1) then  →  if (time%end_yr == 1) then  →  if (pco%recall_bsn` | `header_write.f90:527` |
| Average annual | `if (time%end_mo == 1) then  →  if (time%end_sim == 1 .and. pco%recall_bsn%a == "` | `header_write.f90:542` |

The header and units rows for every file are written by `header_write`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the configured print interval. |
| `pco%recall_bsn%d == "y"` | day | Enables output for this frequency. |
| `pco%recall_bsn%m == "y"` | mon | Enables output for this frequency. |
| `pco%recall_bsn%y == "y"` | yr | Enables output for this frequency. |
| `time%end_mo == 1` | aa, mon, yr | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%recall_bsn%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_write` | Basin name and program string. |
| Header row | `header_write` | Column names for the time, identity, and `hyd_output` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `basin_recall_output` | One `hyd_output` record for the active frequency. |

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
| `flo` | m^3 | `brec_d%flo` | volume of water |
| `sed` | metric tons | `brec_d%sed` | sediment |
| `orgn` | kg N | `brec_d%orgn` | organic N |
| `sedp` | kg P | `brec_d%sedp` | organic P |
| `no3` | kg N | `brec_d%no3` | NO3-N |
| `solp` | kg P | `brec_d%solp` | mineral (soluble P) |
| `chla` | kg | `brec_d%chla` | chlorophyll-a |
| `nh3` | kg N | `brec_d%nh3` | NH3 |
| `no2` | kg N | `brec_d%no2` | NO2 |
| `cbod` | kg | `brec_d%cbod` | carbonaceous biological oxygen demand |
| `dox` | kg | `brec_d%dox` | dissolved oxygen |
| `san` | tons | `brec_d%san` | detached sand |
| `sil` | tons | `brec_d%sil` | detached silt |
| `cla` | tons | `brec_d%cla` | detached clay |
| `sag` | tons | `brec_d%sag` | detached small ag |
| `lag` | tons | `brec_d%lag` | detached large ag |
| `grv` | tons | `brec_d%grv` | gravel |
| `temp` | deg c | `brec_d%temp` | temperature |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`brec_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `hyd_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `basin_recall_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`basin_recall_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `hyd_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_recall_output.f90:23` | `4500` | time, identity, `brec_d(idx)` record |
| `basin_recall_output.f90:25` | `4504` | time, identity, `brec_d(idx)` record |
| `basin_recall_output.f90:34` | `4501` | time, identity, `brec_m(idx)` record |
| `basin_recall_output.f90:36` | `4505` | time, identity, `brec_m(idx)` record |
| `basin_recall_output.f90:46` | `4502` | time, identity, `brec_y(idx)` record |
| `basin_recall_output.f90:48` | `4506` | time, identity, `brec_y(idx)` record |
| `basin_recall_output.f90:59` | `4503` | time, identity, `brec_a(idx)` record |
| `basin_recall_output.f90:61` | `4507` | time, identity, `brec_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `hyd_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `hyd_output` type definition in `hydrograph_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`basin_recall_output`](../procedures/basin_recall_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `hydrograph_module::hyd_output`

## Evidence Used

- `basin_recall_output.f90`
- `header_write.f90`
- `hydrograph_module.f90` (`type hyd_output`)
