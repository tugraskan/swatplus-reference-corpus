---
kind: output_family
source_symbols:
- channel_output
- header_channel
title: channel_*
status: filled
source_hash: 0286bdebf6ef74e4
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_channel`](../procedures/header_channel.md)  
**Written by:** [`channel_output`](../procedures/channel_output.md)  
**Primary data type:** `channel_module::ch_output`  
**Files covered:** `channel_day`, `channel_mon`, `channel_yr`, `channel_aa` text/CSV pairs

## Bottom Line

`channel_*` is the `channel` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `ch_output` state object written by `channel_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `channel` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `channel_day.txt` | `channel_day.csv` | 2480 | 2484 | `header_channel.f90:26` |
| Monthly | `channel_mon.txt` | `channel_mon.csv` | 2481 | 2485 | `header_channel.f90:43` |
| Yearly | `channel_yr.txt` | `channel_yr.csv` | 2482 | 2486 | `header_channel.f90:60` |
| Average annual | `channel_aa.txt` | `channel_aa.csv` | 2483 | 2487 | `header_channel.f90:77` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `header_channel.f90:26` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%chan%m == "y") then` | `header_channel.f90:43` |
| Yearly | `if (time%end_yr == 1) then  →  if (pco%chan%y == "y") then` | `header_channel.f90:60` |
| Average annual | `if (time%end_sim == 1 .and. pco%chan%a == "y") then` | `header_channel.f90:77` |

The header and units rows for every file are written by `header_channel`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%chan%d == "y"` | day | Enables output for this frequency. |
| `pco%chan%m == "y"` | mon | Enables output for this frequency. |
| `pco%chan%y == "y"` | yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the configured print interval. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%chan%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_channel` | Basin name and program string. |
| Header row | `header_channel` | Column names for the time, identity, and `ch_output` values. |
| Units row | `header_channel` | Units for the value columns. |
| Data row | `channel_output` | One `ch_output` record for the active frequency. |

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
| `flo_in` | (ha-m) | `ch_d%flo_in` | streamflow into reach during time step |
| `flo_out` | (ha-m) | `ch_d%flo_out` | streamflow out of reach during time step |
| `evap` | (m^3/s) | `ch_d%evap` | daily rate of water loss from reach by evaporation |
| `tloss` | (m^3/s) | `ch_d%tloss` | rate of water loss from reach by transmission through the streambed |
| `sed_in` | (tons) | `ch_d%sed_in` | sediment transported with water into reach |
| `sed_out` | (tons) | `ch_d%sed_out` | sediment transported with water out of reach |
| `sed_conc` | (mg/L) | `ch_d%sed_conc` | concentration of sediment in reach |
| `orgn_in` | (kg N) | `ch_d%orgn_in` | organic nitrogen transported with water into reach |
| `orgn_out` | (kg N) | `ch_d%orgn_out` | organic nitrogen transported with water out of reach |
| `orgp_in` | (kg P) | `ch_d%orgp_in` | organic phosphorus transported with water into reach |
| `orgp_out` | (kg P) | `ch_d%orgp_out` | organic phosphorus transported with water out of reach |
| `no3_in` | (kg N) | `ch_d%no3_in` | nitrate transported with water into reach |
| `no3_out` | (kg N) | `ch_d%no3_out` | nitrate transported with water out of reach |
| `nh4_in` | (kg) | `ch_d%nh4_in` | ammonium transported with water into reach |
| `nh4_out` | (kg) | `ch_d%nh4_out` | ammonium transported with water out of reach |
| `no2_in` | (kg) | `ch_d%no2_in` | nitrite transported with water into reach |
| `no2_out` | (kg) | `ch_d%no2_out` | nitrite transported with water out of reach |
| `solp_in` | (kg P) | `ch_d%solp_in` | soluble pesticide transported with water into reach |
| `solp_out` | (kg P) | `ch_d%solp_out` | soluble pesticide transported with water out of reach |
| `chla_in` | (kg) | `ch_d%chla_in` | amount of chlorophyll a transported into reach |
| `chla_out` | (kg) | `ch_d%chla_out` | amount of chlorophyll a transported out of reach |
| `cbod_in` | (kg) | `ch_d%cbod_in` | carbonaceous biochemical oxygen demand of material transported into reach |
| `cbod_out` | (kg) | `ch_d%cbod_out` | carbonaceous biochemical oxygen demand of material transported out of reach |
| `dis_in` | (kg) | `ch_d%dis_in` | amount of dissolved oxygen transported into reach |
| `dis_out` | (kg) | `ch_d%dis_out` | amount of dissolved oxygen transported out of reach |
| `solpst_in` | (mg pst) | `ch_d%solpst_in` | soluble pesticide transported with water into reach |
| `solpst_out` | (mg pst) | `ch_d%solpst_out` | soluble pesticide transported with water out of reach |
| `sorbpst_in` | (mg pst) | `ch_d%sorbpst_in` | pesticide sorbed to sediment transported with water into reach |
| `sorbpst_out` | (mg pst) | `ch_d%sorbpst_out` | pesticide sorbed to sediment transported with water out of reach |
| `react` | (mg pst) | `ch_d%react` | loss of pesticide from water from reaction |
| `volat` | (mg) | `ch_d%volat` | loss of pesticide from water by volatilization |
| `setlpst` | (mg pst) | `ch_d%setlpst` | transfer of pesticide from water to river bed sediment by settling |
| `resuspst` | (mg) | `ch_d%resuspst` | transfer of pesticide from river bed sediment to water by resuspension |
| `difus` | mg | `ch_d%difus` | transfer of pesticide from water to river bed sediment by diffusion |
| `reactb` | (mg) | `ch_d%reactb` | loss of pesticide from river bed sediment by reaction |
| `bury` | (mg) | `ch_d%bury` | loss of pesticide from river bed sediment by burial |
| `sedpest` | mg | `ch_d%sedpest` | pesticide in river bed sediment |
| `bacp` | # cfu/100mL | `ch_d%bacp` | number of persistent bacteria transported out of reach |
| `baclp` | # cfu/100mL | `ch_d%baclp` | number of less persistent bacteria transported out of reach |
| `met1` | kg | `ch_d%met1` | conservative metal #1 transported out of reach |
| `met2` | kg | `ch_d%met2` | conservative metal #2 transported out of reach |
| `met3` | kg | `ch_d%met3` | conservative metal #3 transported out of reach |
| `sand_in` | tons | `ch_d%sand_in` | sand in |
| `sand_out` | tons | `ch_d%sand_out` | sand out |
| `silt_in` | tons | `ch_d%silt_in` | silt_in |
| `silt_out` | tons | `ch_d%silt_out` | silt_out |
| `clay_in` | tons | `ch_d%clay_in` | clay_in |
| `clay_out` | tons | `ch_d%clay_out` | clay_out |
| `smag_in` | tons | `ch_d%smag_in` | small aggregates transported into reach |
| `smag_out` | tons | `ch_d%smag_out` | small aggregates transported out of reach |
| `lag_in` | tons | `ch_d%lag_in` | large aggregates transported into reachlg ag in |
| `lag_out` | tons | `ch_d%lag_out` | large aggregates transported out of reach |
| `grvl_in` | tons | `ch_d%grvl_in` | gravel in |
| `grvl_out` | tons | `ch_d%grvl_out` | gravel out |
| `bnk_ero` | tons | `ch_d%bnk_ero` | bank erosion |
| `ch_deg` | tons | `ch_d%ch_deg` | channel degradation |
| `ch_dep` | tons | `ch_d%ch_dep` | channel deposition |
| `fp_dep` | tons | `ch_d%fp_dep` | flood deposition |
| `tot_ssed` | mg/L | `ch_d%tot_ssed` | total suspended sediments |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`ch_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `ch_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `channel_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`channel_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `ch_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `channel_output.f90:29` | `2480` | time, identity, `ch_d(idx)` record |
| `channel_output.f90:31` | `2484` | time, identity, `ch_d(idx)` record |
| `channel_output.f90:40` | `2481` | time, identity, `ch_m(idx)` record |
| `channel_output.f90:42` | `2485` | time, identity, `ch_m(idx)` record |
| `channel_output.f90:52` | `2482` | time, identity, `ch_y(idx)` record |
| `channel_output.f90:54` | `2486` | time, identity, `ch_y(idx)` record |
| `channel_output.f90:64` | `2483` | time, identity, `ch_a(idx)` record |
| `channel_output.f90:66` | `2487` | time, identity, `ch_a(idx)` record |

Header and file-open statements are in `header_channel`.

## Review Notes

- Every frequency shares the `ch_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `ch_output` type definition in `channel_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`channel_output`](../procedures/channel_output.md)
- Header / opener: [`header_channel`](../procedures/header_channel.md)
- Data type: `channel_module::ch_output`

## Evidence Used

- `channel_output.f90`
- `header_channel.f90`
- `channel_module.f90` (`type ch_output`)
