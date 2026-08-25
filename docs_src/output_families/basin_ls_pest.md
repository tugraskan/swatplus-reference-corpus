---
kind: output_family
source_symbols:
- basin_ls_pest_output
- header_pest
title: basin_ls_pest_*
status: filled
source_hash: b1854415f7dffcdb
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_pest`](../procedures/header_pest.md)  
**Written by:** [`basin_ls_pest_output`](../procedures/basin_ls_pest_output.md)  
**Primary data type:** `output_ls_pesticide_module::pesticide_balance`  
**Files covered:** `basin_ls_pest_day`, `basin_ls_pest_mon`, `basin_ls_pest_yr`, `basin_ls_pest_aa` text/CSV pairs

## Bottom Line

`basin_ls_pest_*` is the `basin_ls_pest` pesticide time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `basin_ls_pest_output` loops over every simulated pesticide and writes **one row per (object x pesticide)** for each period: the row carries the time and object-identity fields, the pesticide name, and a `pesticide_balance` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `basin_ls_pest` balance of one pesticide for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several pesticides, each object appears once per pesticide per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_ls_pest_day.txt` | `basin_ls_pest_day.csv` | 2864 | 2868 | `header_pest.f90:466` |
| Monthly | `basin_ls_pest_mon.txt` | `basin_ls_pest_mon.csv` | 2865 | 2869 | `header_pest.f90:481` |
| Yearly | `basin_ls_pest_yr.txt` | `basin_ls_pest_yr.csv` | 2866 | 2870 | `header_pest.f90:496` |
| Average annual | `basin_ls_pest_aa.txt` | `basin_ls_pest_aa.csv` | 2867 | 2871 | `header_pest.f90:511` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do ipest = 1, cs_db%num_pests  →  if (pco%day_print == "y" .and. pco%int_day_cur` | `header_pest.f90:466` |
| Monthly | `do ipest = 1, cs_db%num_pests  →  if (time%end_mo == 1) then  →  if (pco%pest%m ` | `header_pest.f90:481` |
| Yearly | `do ipest = 1, cs_db%num_pests  →  if (time%end_yr == 1) then  →  if (time%end_yr` | `header_pest.f90:496` |
| Average annual | `do ipest = 1, cs_db%num_pests  →  if (time%end_sim == 1 .and. pco%pest%a == "y")` | `header_pest.f90:511` |

The header and units rows for every file are written by `header_pest`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `do ipest = 1, cs_db%num_pests` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the print interval. |
| `pco%pest%d == "y"` | day | Enables output for this frequency. |
| `pco%pest%m == "y"` | mon | Enables output for this frequency. |
| `time%end_mo == 1` | mon | Writes rows at month end. |
| `time%end_sim == 1 .and. pco%pest%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Writes rows at year end. |
| `time%end_yr == 1 .and. pco%pest%y == "y"` | yr | Writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_pest` | Basin name and program string. |
| Header row | `header_pest` | Column names for time, identity, the pesticide name, and the `pesticide_balance` values. |
| Units row | `header_pest` | Units for the value columns. |
| Data row | `basin_ls_pest_output` | One `pesticide_balance` record for one pesticide at the active frequency. |

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
| `pesticide_name` | | `cs_db%pests(ipest)` | Name of the pesticide this row reports (one row per pesticide). |
| `plant` |  | `bpestb_d%pest(i)%plant` | character(len=10) :: name integer :: num_db pesticide on plant foliage |
| `soil` | kg/ha | `bpestb_d%pest(i)%soil` | pesticide in soil |
| `sed` | kg/ha | `bpestb_d%pest(i)%sed` | pesticide loading from HRU sorbed onto sediment |
| `surq` | kg/ha | `bpestb_d%pest(i)%surq` | amount of pesticide type lost in surface runoff in HRU |
| `latq` | kg/ha | `bpestb_d%pest(i)%latq` | amount of pesticide in lateral flow in HRU |
| `tileq` | kg/ha | `bpestb_d%pest(i)%tileq` | amount of pesticide in tile flow in HRU |
| `perc` | kg/ha | `bpestb_d%pest(i)%perc` | amount of pesticide leached past bottom of soil |
| `apply_s` | kg/ha | `bpestb_d%pest(i)%apply_s` | amount of pesticide applied on soil |
| `apply_f` | kg/ha | `bpestb_d%pest(i)%apply_f` | amount of pesticide applied on foliage |
| `decay_s` | kg/ha | `bpestb_d%pest(i)%decay_s` | amount of pesticide decayed on soil |
| `decay_f` | kg/ha | `bpestb_d%pest(i)%decay_f` | amount of pesticide decayed on foliage |
| `wash` | kg/ha | `bpestb_d%pest(i)%wash` | amount of pesticide washed off from plant to soil |
| `metab_s` | kg/ha | `bpestb_d%pest(i)%metab_s` | amount of pesticide metabolized from parent in soil |
| `metab_f` | kg/ha | `bpestb_d%pest(i)%metab_f` | amount of pesticide metabolized from parent on foilage |
| `pl_uptake` | kg/ha | `bpestb_d%pest(i)%pl_uptake` | amount of pesticide taken up by plants |
| `in_plant` | kg/ha | `bpestb_d%pest(i)%in_plant` | pesticide in plant foliage |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `pesticide_balance` record for one pesticide. `basin_ls_pest_output` loops over the simulated pesticides (`cs_db%pests(ipest)`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated pesticide.
2. If the frequency's print flag is on, write that pesticide's current `pesticide_balance` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_ls_pest_output.f90:41` | `2864` | time, identity, pesticide name, one `pesticide_balance` record |
| `basin_ls_pest_output.f90:44` | `2868` | time, identity, pesticide name, one `pesticide_balance` record |
| `basin_ls_pest_output.f90:60` | `2865` | time, identity, pesticide name, one `pesticide_balance` record |
| `basin_ls_pest_output.f90:63` | `2869` | time, identity, pesticide name, one `pesticide_balance` record |
| `basin_ls_pest_output.f90:79` | `2866` | time, identity, pesticide name, one `pesticide_balance` record |
| `basin_ls_pest_output.f90:82` | `2870` | time, identity, pesticide name, one `pesticide_balance` record |
| `basin_ls_pest_output.f90:93` | `2867` | time, identity, pesticide name, one `pesticide_balance` record |
| `basin_ls_pest_output.f90:96` | `2871` | time, identity, pesticide name, one `pesticide_balance` record |

Header and file-open statements are in `header_pest`.

## Review Notes

- Every frequency shares the `pesticide_balance` layout; the Columns Written table applies to all files in the family.
- Rows repeat per pesticide: an object with N simulated pesticides produces N rows per period.
- Column names, units, and meanings are taken from the `pesticide_balance` type definition in `output_ls_pesticide_module`.
- Auto-derived from the writer's per-pesticide output type; prose sections may benefit from human review.

## Source Links

- Writer: [`basin_ls_pest_output`](../procedures/basin_ls_pest_output.md)
- Header / opener: [`header_pest`](../procedures/header_pest.md)
- Data type: `output_ls_pesticide_module::pesticide_balance`

## Evidence Used

- `basin_ls_pest_output.f90`
- `header_pest.f90`
- `output_ls_pesticide_module.f90` (`type pesticide_balance`)
