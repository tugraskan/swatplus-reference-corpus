---
kind: output_family
source_symbols:
- basin_channel_output
- header_write
title: basin_cha_*
status: filled
source_hash: 2c19e2b1dd90132e
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`header_write`](../procedures/header_write.md)  
**Written by:** [`basin_channel_output`](../procedures/basin_channel_output.md)  
**Primary data type:** `channel_module::ch_output`  
**Files covered:** `basin_cha_day`, `basin_cha_mon`, `basin_cha_yr`, `basin_cha_aa` text/CSV pairs

## Bottom Line

`basin_cha_*` is the `basin_cha` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `ch_output` state object written by `basin_channel_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `basin_cha` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_cha_day.txt` | `basin_cha_day.csv` | 2110 | 2114 | `header_write.f90:247` |
| Monthly | `basin_cha_mon.txt` | `basin_cha_mon.csv` | 2111 | 2115 | `header_write.f90:262` |
| Yearly | `basin_cha_yr.txt` | `basin_cha_yr.csv` | 2112 | 2116 | `header_write.f90:277` |
| Average annual | `basin_cha_aa.txt` | `basin_cha_aa.csv` | 2113 | 2117 | `header_write.f90:292` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `header_write.f90:247` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%chan_bsn%m == "y") then` | `header_write.f90:262` |
| Yearly | `if (time%end_yr == 1) then  →  if (pco%chan_bsn%y == "y") then` | `header_write.f90:277` |
| Average annual | `if (time%end_sim == 1 .and. pco%chan_bsn%a == "y") then` | `header_write.f90:292` |

The header and units rows for every file are written by `header_write`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%chan_bsn%d == "y"` | day | Enables output for this frequency. |
| `pco%chan_bsn%m == "y"` | mon | Enables output for this frequency. |
| `pco%chan_bsn%y == "y"` | yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the configured print interval. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%chan_bsn%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `header_write` | Basin name and program string. |
| Header row | `header_write` | Column names for the time, identity, and `ch_output` values. |
| Units row | `header_write` | Units for the value columns. |
| Data row | `basin_channel_output` | One `ch_output` record for the active frequency. |

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
| `flo_in` | (ha-m) | `bch_d%flo_in` | streamflow into reach during time step |
| `flo_out` | (ha-m) | `bch_d%flo_out` | streamflow out of reach during time step |
| `evap` | (m^3/s) | `bch_d%evap` | daily rate of water loss from reach by evaporation |
| `tloss` | (m^3/s) | `bch_d%tloss` | rate of water loss from reach by transmission through the streambed |
| `sed_in` | (tons) | `bch_d%sed_in` | sediment transported with water into reach |
| `sed_out` | (tons) | `bch_d%sed_out` | sediment transported with water out of reach |
| `sed_conc` | (mg/L) | `bch_d%sed_conc` | concentration of sediment in reach |
| `orgn_in` | (kg N) | `bch_d%orgn_in` | organic nitrogen transported with water into reach |
| `orgn_out` | (kg N) | `bch_d%orgn_out` | organic nitrogen transported with water out of reach |
| `orgp_in` | (kg P) | `bch_d%orgp_in` | organic phosphorus transported with water into reach |
| `orgp_out` | (kg P) | `bch_d%orgp_out` | organic phosphorus transported with water out of reach |
| `no3_in` | (kg N) | `bch_d%no3_in` | nitrate transported with water into reach |
| `no3_out` | (kg N) | `bch_d%no3_out` | nitrate transported with water out of reach |
| `nh4_in` | (kg) | `bch_d%nh4_in` | ammonium transported with water into reach |
| `nh4_out` | (kg) | `bch_d%nh4_out` | ammonium transported with water out of reach |
| `no2_in` | (kg) | `bch_d%no2_in` | nitrite transported with water into reach |
| `no2_out` | (kg) | `bch_d%no2_out` | nitrite transported with water out of reach |
| `solp_in` | (kg P) | `bch_d%solp_in` | soluble pesticide transported with water into reach |
| `solp_out` | (kg P) | `bch_d%solp_out` | soluble pesticide transported with water out of reach |
| `chla_in` | (kg) | `bch_d%chla_in` | amount of chlorophyll a transported into reach |
| `chla_out` | (kg) | `bch_d%chla_out` | amount of chlorophyll a transported out of reach |
| `cbod_in` | (kg) | `bch_d%cbod_in` | carbonaceous biochemical oxygen demand of material transported into reach |
| `cbod_out` | (kg) | `bch_d%cbod_out` | carbonaceous biochemical oxygen demand of material transported out of reach |
| `dis_in` | (kg) | `bch_d%dis_in` | amount of dissolved oxygen transported into reach |
| `dis_out` | (kg) | `bch_d%dis_out` | amount of dissolved oxygen transported out of reach |
| `solpst_in` | (mg pst) | `bch_d%solpst_in` | soluble pesticide transported with water into reach |
| `solpst_out` | (mg pst) | `bch_d%solpst_out` | soluble pesticide transported with water out of reach |
| `sorbpst_in` | (mg pst) | `bch_d%sorbpst_in` | pesticide sorbed to sediment transported with water into reach |
| `sorbpst_out` | (mg pst) | `bch_d%sorbpst_out` | pesticide sorbed to sediment transported with water out of reach |
| `react` | (mg pst) | `bch_d%react` | loss of pesticide from water from reaction |
| `volat` | (mg) | `bch_d%volat` | loss of pesticide from water by volatilization |
| `setlpst` | (mg pst) | `bch_d%setlpst` | transfer of pesticide from water to river bed sediment by settling |
| `resuspst` | (mg) | `bch_d%resuspst` | transfer of pesticide from river bed sediment to water by resuspension |
| `difus` | mg | `bch_d%difus` | transfer of pesticide from water to river bed sediment by diffusion |
| `reactb` | (mg) | `bch_d%reactb` | loss of pesticide from river bed sediment by reaction |
| `bury` | (mg) | `bch_d%bury` | loss of pesticide from river bed sediment by burial |
| `sedpest` | mg | `bch_d%sedpest` | pesticide in river bed sediment |
| `bacp` | # cfu/100mL | `bch_d%bacp` | number of persistent bacteria transported out of reach |
| `baclp` | # cfu/100mL | `bch_d%baclp` | number of less persistent bacteria transported out of reach |
| `met1` | kg | `bch_d%met1` | conservative metal #1 transported out of reach |
| `met2` | kg | `bch_d%met2` | conservative metal #2 transported out of reach |
| `met3` | kg | `bch_d%met3` | conservative metal #3 transported out of reach |
| `sand_in` | tons | `bch_d%sand_in` | sand in |
| `sand_out` | tons | `bch_d%sand_out` | sand out |
| `silt_in` | tons | `bch_d%silt_in` | silt_in |
| `silt_out` | tons | `bch_d%silt_out` | silt_out |
| `clay_in` | tons | `bch_d%clay_in` | clay_in |
| `clay_out` | tons | `bch_d%clay_out` | clay_out |
| `smag_in` | tons | `bch_d%smag_in` | small aggregates transported into reach |
| `smag_out` | tons | `bch_d%smag_out` | small aggregates transported out of reach |
| `lag_in` | tons | `bch_d%lag_in` | large aggregates transported into reachlg ag in |
| `lag_out` | tons | `bch_d%lag_out` | large aggregates transported out of reach |
| `grvl_in` | tons | `bch_d%grvl_in` | gravel in |
| `grvl_out` | tons | `bch_d%grvl_out` | gravel out |
| `bnk_ero` | tons | `bch_d%bnk_ero` | bank erosion |
| `ch_deg` | tons | `bch_d%ch_deg` | channel degradation |
| `ch_dep` | tons | `bch_d%ch_dep` | channel deposition |
| `fp_dep` | tons | `bch_d%fp_dep` | flood deposition |
| `tot_ssed` | mg/L | `bch_d%tot_ssed` | total suspended sediments |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`bch_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `ch_output` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `basin_channel_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`basin_channel_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `ch_output` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_channel_output.f90:25` | `2110` | time, identity, `bch_d(idx)` record |
| `basin_channel_output.f90:27` | `2114` | time, identity, `bch_d(idx)` record |
| `basin_channel_output.f90:36` | `2111` | time, identity, `bch_m(idx)` record |
| `basin_channel_output.f90:38` | `2115` | time, identity, `bch_m(idx)` record |
| `basin_channel_output.f90:48` | `2112` | time, identity, `bch_y(idx)` record |
| `basin_channel_output.f90:50` | `2116` | time, identity, `bch_y(idx)` record |
| `basin_channel_output.f90:60` | `2113` | time, identity, `bch_a(idx)` record |
| `basin_channel_output.f90:62` | `2117` | time, identity, `bch_a(idx)` record |

Header and file-open statements are in `header_write`.

## Review Notes

- Every frequency shares the `ch_output` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `ch_output` type definition in `channel_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`basin_channel_output`](../procedures/basin_channel_output.md)
- Header / opener: [`header_write`](../procedures/header_write.md)
- Data type: `channel_module::ch_output`

## Evidence Used

- `basin_channel_output.f90`
- `header_write.f90`
- `channel_module.f90` (`type ch_output`)
