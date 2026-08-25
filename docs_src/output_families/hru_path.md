---
kind: output_family
source_symbols:
- header_path
- hru_pathogen_output
title: hru_path_*
status: filled
source_hash: 8345f7c9c60a1055
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_path`](../procedures/header_path.md)  
**Written by:** [`hru_pathogen_output`](../procedures/hru_pathogen_output.md)  
**Primary data type:** `output_ls_pathogen_module::pathogen_balance`  
**Files covered:** `hru_path_day`, `hru_path_mon`, `hru_path_yr`, `hru_path_aa` text/CSV pairs

## Bottom Line

`hru_path_*` is the `hru_path` constituent time-series output family. Every file shares one record layout, so daily, monthly, yearly, and average-annual reporting live on one page. Unlike the single-value families, `hru_pathogen_output` loops over every simulated constituent and writes **one row per (object x constituent)** for each period: the row carries the time and object-identity fields, the constituent name, and a `pathogen_balance` balance record.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** the `hru_path` balance of one constituent for one object over one reporting period (daily, monthly, yearly, average annual). If a run simulates several constituents, each object appears once per constituent per period. The columns are the same in every file of the family.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hru_path_day.txt` | `hru_path_day.csv` | 2790 | 2794 | `header_path.f90:13` |
| Monthly | `hru_path_mon.txt` | `hru_path_mon.csv` | 2791 | 2795 | `header_path.f90:28` |
| Yearly | `hru_path_yr.txt` | `hru_path_yr.csv` | 2792 | 2796 | `header_path.f90:43` |
| Average annual | `hru_path_aa.txt` | `hru_path_aa.csv` | 2793 | 2797 | `header_path.f90:58` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%wb_hru%d == "y" .and. cs_db%num_tot  →  0) then` | `header_path.f90:13` |
| Monthly | `if (pco%wb_hru%m == "y" .and. cs_db%num_tot  →  0) then` | `header_path.f90:28` |
| Yearly | `if (pco%wb_hru%y == "y" .and. cs_db%num_tot  →  0) then` | `header_path.f90:43` |
| Average annual | `if (pco%wb_hru%a == "y" .and. cs_db%num_tot  →  0) then` | `header_path.f90:58` |

The header and units rows for every file are written by `header_path`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%wb_hru%a == "y" .and. cs_db%num_tot` | aa | Enables output for this frequency. |
| `pco%wb_hru%d == "y" .and. cs_db%num_tot` | day | Enables output for this frequency. |
| `pco%wb_hru%m == "y" .and. cs_db%num_tot` | mon | Enables output for this frequency. |
| `pco%wb_hru%y == "y" .and. cs_db%num_tot` | yr | Enables output for this frequency. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_path` | Basin name and program string. |
| Header row | `header_path` | Column names for time, identity, the constituent name, and the `pathogen_balance` values. |
| Units row | `header_path` | Units for the value columns. |
| Data row | `hru_pathogen_output` | One `pathogen_balance` record for one constituent at the active frequency. |

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
| `constituent_name` | | `cs_db constituent name` | Name of the constituent this row reports (one row per constituent). |
| `plant` |  | `hpath_bal%path(i)%plant` | character(len=10) :: name integer :: num_db pathogen on plant foliage |
| `soil` | kg/ha | `hpath_bal%path(i)%soil` | pathogen enrichment ratio |
| `sed` | kg/ha | `hpath_bal%path(i)%sed` | pathogen loading from HRU sorbed onto sediment |
| `surq` | kg/ha | `hpath_bal%path(i)%surq` | amount of pathogen type lost in surface runoff on current day in HRU |
| `latq` | kg/ha | `hpath_bal%path(i)%latq` | amount of pathogen in lateral flow in HRU for the day |
| `perc1` | kg/ha | `hpath_bal%path(i)%perc1` | amount of pathogen leached past first layer |
| `apply_sol` | kg/ha | `hpath_bal%path(i)%apply_sol` | amount of pathogen applied to soil |
| `apply_plt` | kg/ha | `hpath_bal%path(i)%apply_plt` | amount of pathogen applied to plant |
| `regro` | kg/ha | `hpath_bal%path(i)%regro` | amount of pathogen regrowth |
| `die_off` | kg/ha | `hpath_bal%path(i)%die_off` | amount of pathogen die-off |
| `wash` | kg/ha | `hpath_bal%path(i)%wash` | amount of pathogen washed off from plant to soil |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). Only the file name, unit number, print flag, and the source state object differ. See the Output Family and Writer And Print Controls tables for per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `pathogen_balance` record for one constituent. `hru_pathogen_output` loops over the simulated constituents (`cs_db constituent list`); daily rows are written from the per-timestep state and coarser frequencies are accumulated from the finer state. See the writer for whether each field is summed or averaged.

## Writer Flow

1. For each reported object, loop over every simulated constituent.
2. If the frequency's print flag is on, write that constituent's current `pathogen_balance` state to the text file (and CSV when `pco%csvout == "y"`).
3. Accumulate the finer-frequency state into the coarser one and write at each period boundary.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hru_pathogen_output.f90:35` | `2790` | time, identity, constituent name, one `pathogen_balance` record |
| `hru_pathogen_output.f90:37` | `2794` | time, identity, constituent name, one `pathogen_balance` record |
| `hru_pathogen_output.f90:56` | `2791` | time, identity, constituent name, one `pathogen_balance` record |
| `hru_pathogen_output.f90:58` | `2795` | time, identity, constituent name, one `pathogen_balance` record |
| `hru_pathogen_output.f90:78` | `2792` | time, identity, constituent name, one `pathogen_balance` record |
| `hru_pathogen_output.f90:80` | `2796` | time, identity, constituent name, one `pathogen_balance` record |
| `hru_pathogen_output.f90:90` | `2793` | time, identity, constituent name, one `pathogen_balance` record |
| `hru_pathogen_output.f90:92` | `2797` | time, identity, constituent name, one `pathogen_balance` record |

Header and file-open statements are in `header_path`.

## Review Notes

- Every frequency shares the `pathogen_balance` layout; the Columns Written table applies to all files in the family.
- Rows repeat per constituent: an object with N simulated constituents produces N rows per period.
- Column names, units, and meanings are taken from the `pathogen_balance` type definition in `output_ls_pathogen_module`.
- Auto-derived from the writer's per-constituent output type; prose sections may benefit from human review.

## Source Links

- Writer: [`hru_pathogen_output`](../procedures/hru_pathogen_output.md)
- Header / opener: [`header_path`](../procedures/header_path.md)
- Data type: `output_ls_pathogen_module::pathogen_balance`

## Evidence Used

- `hru_pathogen_output.f90`
- `header_path.f90`
- `output_ls_pathogen_module.f90` (`type pathogen_balance`)
