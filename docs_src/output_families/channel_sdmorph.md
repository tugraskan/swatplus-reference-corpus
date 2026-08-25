---
kind: output_family
source_symbols:
- header_sd_channel
- sd_chanmorph_output
title: channel_sdmorph_*
status: filled
source_hash: 0c534b55f0364535
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_sd_channel`](../procedures/header_sd_channel.md)  
**Written by:** [`sd_chanmorph_output`](../procedures/sd_chanmorph_output.md)  
**Primary data type:** `sd_channel_module::sd_ch_output`  
**Files covered:** `channel_sdmorph_day`, `channel_sdmorph_mon`, `channel_sdmorph_yr`, `channel_sdmorph_aa` text/CSV pairs

## Bottom Line

`channel_sdmorph_*` is the `channel_sdmorph` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `sd_ch_output` state object written by `sd_chanmorph_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `channel_sdmorph` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `channel_sdmorph_day.txt` | `channel_sdmorph_day.csv` | 4800 | 4804 | `header_sd_channel.f90:150` |
| Monthly | `channel_sdmorph_mon.txt` | `channel_sdmorph_mon.csv` | 4801 | 4805 | `header_sd_channel.f90:167` |
| Yearly | `channel_sdmorph_yr.txt` | `channel_sdmorph_yr.csv` | 4802 | 4806 | `header_sd_channel.f90:184` |
| Average annual | `channel_sdmorph_aa.txt` | `channel_sdmorph_aa.csv` | 4803 | 4807 | `header_sd_channel.f90:201` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:150` |
| Monthly | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:167` |
| Yearly | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:184` |
| Average annual | `if (sp_ob%chandeg  →  0) then  →  if (pco%sd_chan%d == "y") then  →  if (sp_ob%c` | `header_sd_channel.f90:201` |

The header and units rows for every file are written by `header_sd_channel`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%sd_chan%a == "y"` | aa | Enables output for this frequency. |
| `pco%sd_chan%d == "y"` | All files | Enables output for this frequency. |
| `pco%sd_chan%m == "y"` | mon | Enables output for this frequency. |
| `pco%sd_chan%y == "y"` | All files | Enables output for this frequency. |
| `sp_ob%chandeg` | All files | Open/print guard. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_sd_channel` | Basin name and program string. |
| Header row | `header_sd_channel` | Column names for the time, identity, and `sd_ch_output` values. |
| Units row | `header_sd_channel` | Units for the value columns. |
| Data row | `sd_chanmorph_output` | One `sd_ch_output` record for the active frequency. |

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
| `flo_in` | (m^3/s) | `chsd_d%flo_in` | average daily inflow rate during time step |
| `aqu_in` | (m^3/s) | `chsd_d%aqu_in` | geomorphic aquifer flow into channel/aquifer inflow using geomorphic baseflow method |
| `flo` | (m^3/s) | `chsd_d%flo` | average daily outflow rate during timestep |
| `peakr` | (m^3/s) | `chsd_d%peakr` | average peak runoff rate during timestep |
| `sed_in` | (tons) | `chsd_d%sed_in` | sediment in |
| `sed_out` | (tons) | `chsd_d%sed_out` | sediment out |
| `washld` | (tons) | `chsd_d%washld` | wash load (suspended) out |
| `bedld` | (tons) | `chsd_d%bedld` | bed load out |
| `dep` | (tons) | `chsd_d%dep` | deposition in channel and flood plain |
| `deg_btm` | (tons) | `chsd_d%deg_btm` | erosion of channel bottom |
| `deg_bank` | (tons) | `chsd_d%deg_bank` | erosion of channel bank |
| `hc_sed` | (tons) | `chsd_d%hc_sed` | erosion from gully head cut |
| `width` | m | `chsd_d%width` | channel bank full top width at end of time step |
| `depth` | m | `chsd_d%depth` | channel bank full depth at end of time step |
| `slope` | m/m | `chsd_d%slope` | channel slope |
| `deg_btm_m` |  | `chsd_d%deg_btm_m` | (m) !downcutting of channel bottom |
| `deg_bank_m` | (m) | `chsd_d%deg_bank_m` | widening of channel banks |
| `hc_m` | (m) | `chsd_d%hc_m` | headcut retreat |
| `flo_in_mm` | (mm) | `chsd_d%flo_in_mm` | inflow rate total sum for each time step |
| `aqu_in_mm` | (mm) | `chsd_d%aqu_in_mm` | aquifer inflow rate total sum for each time step |
| `flo_mm` | (mm) | `chsd_d%flo_mm` | outflow rate total sum for each time step |
| `sed_stor` | (tons) | `chsd_d%sed_stor` | sed storage at end of timestep |
| `n_tot` | (kg N) | `chsd_d%n_tot` | total nitrogen leaving the reach |
| `p_tot` | (kg N) | `chsd_d%p_tot` | total phosphorus leaving the reach |
| `dep_bf` | m | `chsd_d%dep_bf` | depth of water when reach is at bankfull depth |
| `velav_bf` | m/s | `chsd_d%velav_bf` | average velocity when reach is at bankfull depth |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`chsd_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `sd_ch_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `sd_chanmorph_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`sd_chanmorph_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `sd_ch_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `sd_chanmorph_output.f90:20` | `4800` | time, identity, `chsd_d(idx)` record |
| `sd_chanmorph_output.f90:22` | `4804` | time, identity, `chsd_d(idx)` record |
| `sd_chanmorph_output.f90:35` | `4801` | time, identity, `chsd_m(idx)` record |
| `sd_chanmorph_output.f90:37` | `4805` | time, identity, `chsd_m(idx)` record |
| `sd_chanmorph_output.f90:51` | `4802` | time, identity, `chsd_y(idx)` record |
| `sd_chanmorph_output.f90:53` | `4806` | time, identity, `chsd_y(idx)` record |
| `sd_chanmorph_output.f90:65` | `4803` | time, identity, `chsd_a(idx)` record |
| `sd_chanmorph_output.f90:67` | `4807` | time, identity, `chsd_a(idx)` record |

Header and file-open statements are in `header_sd_channel`.

## Review Notes

- Every frequency shares the `sd_ch_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `sd_ch_output` type definition in `sd_channel_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`sd_chanmorph_output`](../procedures/sd_chanmorph_output.md)
- Header / opener: [`header_sd_channel`](../procedures/header_sd_channel.md)
- Data type: `sd_channel_module::sd_ch_output`

## Evidence Used

- `sd_chanmorph_output.f90`
- `header_sd_channel.f90`
- `sd_channel_module.f90` (`type sd_ch_output`)
