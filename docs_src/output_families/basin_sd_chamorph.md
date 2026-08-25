---
kind: output_family
source_symbols:
- basin_chanmorph_output
- header_write
title: basin_sd_chamorph_*
status: filled
source_hash: dcb12c167e008f81
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`basin_chanmorph_output`](../procedures/basin_chanmorph_output.md)  
**Primary data type:** `sd_channel_module::sd_ch_output`  
**Files covered:** `basin_sd_chamorph_day`, `basin_sd_chamorph_mon`, `basin_sd_chamorph_yr`, `basin_sd_chamorph_aa` text/CSV pairs

## Bottom Line

`basin_sd_chamorph_*` is the `basin_sd_chamorph` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `sd_ch_output` state object written by `basin_chanmorph_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `basin_sd_chamorph` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_sd_chamorph_day.txt` | `basin_sd_chamorph_day.csv` | 2120 | 2124 | `header_write.f90:372` |
| Monthly | `basin_sd_chamorph_mon.txt` | `basin_sd_chamorph_mon.csv` | 2121 | 2125 | `header_write.f90:387` |
| Yearly | `basin_sd_chamorph_yr.txt` | `basin_sd_chamorph_yr.csv` | 2122 | 2126 | `header_write.f90:402` |
| Average annual | `basin_sd_chamorph_aa.txt` | `basin_sd_chamorph_aa.csv` | 2123 | 2127 | `header_write.f90:417` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `header_write.f90:372` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%sd_chan_bsn%m == "y") then` | `header_write.f90:387` |
| Yearly | `if (time%end_yr == 1) then  →  if (pco%sd_chan_bsn%y == "y") then` | `header_write.f90:402` |
| Average annual | `if (time%end_sim == 1 .and. pco%sd_chan_bsn%a == "y") then` | `header_write.f90:417` |

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
| Header row | `header_write` | Column names for the time, identity, and `sd_ch_output` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `basin_chanmorph_output` | One `sd_ch_output` record for the active frequency. |

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
| `flo_in` | (m^3/s) | `bchsd_d%flo_in` | average daily inflow rate during time step |
| `aqu_in` | (m^3/s) | `bchsd_d%aqu_in` | geomorphic aquifer flow into channel/aquifer inflow using geomorphic baseflow method |
| `flo` | (m^3/s) | `bchsd_d%flo` | average daily outflow rate during timestep |
| `peakr` | (m^3/s) | `bchsd_d%peakr` | average peak runoff rate during timestep |
| `sed_in` | (tons) | `bchsd_d%sed_in` | sediment in |
| `sed_out` | (tons) | `bchsd_d%sed_out` | sediment out |
| `washld` | (tons) | `bchsd_d%washld` | wash load (suspended) out |
| `bedld` | (tons) | `bchsd_d%bedld` | bed load out |
| `dep` | (tons) | `bchsd_d%dep` | deposition in channel and flood plain |
| `deg_btm` | (tons) | `bchsd_d%deg_btm` | erosion of channel bottom |
| `deg_bank` | (tons) | `bchsd_d%deg_bank` | erosion of channel bank |
| `hc_sed` | (tons) | `bchsd_d%hc_sed` | erosion from gully head cut |
| `width` | m | `bchsd_d%width` | channel bank full top width at end of time step |
| `depth` | m | `bchsd_d%depth` | channel bank full depth at end of time step |
| `slope` | m/m | `bchsd_d%slope` | channel slope |
| `deg_btm_m` |  | `bchsd_d%deg_btm_m` | (m) !downcutting of channel bottom |
| `deg_bank_m` | (m) | `bchsd_d%deg_bank_m` | widening of channel banks |
| `hc_m` | (m) | `bchsd_d%hc_m` | headcut retreat |
| `flo_in_mm` | (mm) | `bchsd_d%flo_in_mm` | inflow rate total sum for each time step |
| `aqu_in_mm` | (mm) | `bchsd_d%aqu_in_mm` | aquifer inflow rate total sum for each time step |
| `flo_mm` | (mm) | `bchsd_d%flo_mm` | outflow rate total sum for each time step |
| `sed_stor` | (tons) | `bchsd_d%sed_stor` | sed storage at end of timestep |
| `n_tot` | (kg N) | `bchsd_d%n_tot` | total nitrogen leaving the reach |
| `p_tot` | (kg N) | `bchsd_d%p_tot` | total phosphorus leaving the reach |
| `dep_bf` | m | `bchsd_d%dep_bf` | depth of water when reach is at bankfull depth |
| `velav_bf` | m/s | `bchsd_d%velav_bf` | average velocity when reach is at bankfull depth |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`bchsd_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `sd_ch_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `basin_chanmorph_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`basin_chanmorph_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `sd_ch_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_chanmorph_output.f90:25` | `2120` | time, identity, `bchsd_d(idx)` record |
| `basin_chanmorph_output.f90:27` | `2124` | time, identity, `bchsd_d(idx)` record |
| `basin_chanmorph_output.f90:39` | `2121` | time, identity, `bchsd_m(idx)` record |
| `basin_chanmorph_output.f90:41` | `2125` | time, identity, `bchsd_m(idx)` record |
| `basin_chanmorph_output.f90:54` | `2122` | time, identity, `bchsd_y(idx)` record |
| `basin_chanmorph_output.f90:56` | `2126` | time, identity, `bchsd_y(idx)` record |
| `basin_chanmorph_output.f90:68` | `2123` | time, identity, `bchsd_a(idx)` record |
| `basin_chanmorph_output.f90:70` | `2127` | time, identity, `bchsd_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `sd_ch_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `sd_ch_output` type definition in `sd_channel_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`basin_chanmorph_output`](../procedures/basin_chanmorph_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `sd_channel_module::sd_ch_output`

## Evidence Used

- `basin_chanmorph_output.f90`
- `header_write.f90`
- `sd_channel_module.f90` (`type sd_ch_output`)
