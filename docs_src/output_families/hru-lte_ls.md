---
kind: output_family
source_symbols:
- hru_lte_output
- output_landscape_init
title: hru-lte_ls_*
status: filled
source_hash: da5f4470494e1f43
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`output_landscape_init`](../procedures/output_landscape_init.md)  
**Written by:** [`hru_lte_output`](../procedures/hru_lte_output.md)  
**Primary data type:** `output_landscape_module::output_waterbal`  
**Files covered:** `hru-lte_ls_day`, `hru-lte_ls_mon`, `hru-lte_ls_yr`, `hru-lte_ls_aa` text/CSV pairs

## Bottom Line

`hru-lte_ls_*` is the `hru-lte_ls` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `output_waterbal` state object written by `hru_lte_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `hru-lte_ls` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hru-lte_ls_day.txt` | `hru-lte_ls_day.csv` | 2440 | 2444 | `output_landscape_init.f90:637` |
| Monthly | `hru-lte_ls_mon.txt` | `hru-lte_ls_mon.csv` | 2441 | 2445 | `output_landscape_init.f90:652` |
| Yearly | `hru-lte_ls_yr.txt` | `hru-lte_ls_yr.csv` | 2442 | 2446 | `output_landscape_init.f90:667` |
| Average annual | `hru-lte_ls_aa.txt` | `hru-lte_ls_aa.csv` | 2443 | 2447 | `output_landscape_init.f90:682` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `output_landscape_init.f90:637` |
| Monthly | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (time` | `output_landscape_init.f90:652` |
| Yearly | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (time` | `output_landscape_init.f90:667` |
| Average annual | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (time` | `output_landscape_init.f90:682` |

The header and units rows for every file are written by `output_landscape_init`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | All files | Restricts daily rows to the configured print interval. |
| `pco%ls_sd%d == "y"` | day | Enables output for this frequency. |
| `pco%ls_sd%m == "y"` | mon | Enables output for this frequency. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%ls_sd%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |
| `time%end_yr == 1 .and. pco%ls_sd%y == "y"` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `output_landscape_init` | Basin name and program string. |
| Header row | `output_landscape_init` | Column names for the time, identity, and `output_waterbal` values. |
| Units row | `output_landscape_init` | Units for the value columns. |
| Data row | `hru_lte_output` | One `output_waterbal` record for the active frequency. |

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
| `precip` | mm H2O | `hltwb_d%precip` | precipitation falling as rain and snow |
| `snofall` | mm H2O | `hltwb_d%snofall` | precipitation falling as snow, sleet or freezing rain |
| `snomlt` | mm H2O | `hltwb_d%snomlt` | snow or melting ice |
| `surq_gen` | mm H2O | `hltwb_d%surq_gen` | surface runoff generated from the landscape |
| `latq` | mm H2O | `hltwb_d%latq` | lateral soil flow |
| `wateryld` | mm H2O | `hltwb_d%wateryld` | water yield - sum of surface runoff, lateral soil flow and tile flow |
| `perc` | mm H2O | `hltwb_d%perc` | amt of water perc out of the soil profile & into the vadose zone |
| `et` | mm H2O | `hltwb_d%et` | actual evapotranspiration from the soil |
| `ecanopy` | mm H2O | `hltwb_d%ecanopy` | not reported |
| `eplant` | mm H2O | `hltwb_d%eplant` | plant transpiration |
| `esoil` | mm H2O | `hltwb_d%esoil` | soil evaporation |
| `surq_cont` | mm H2O | `hltwb_d%surq_cont` | surface runoff leaving the landscape |
| `cn` | none | `hltwb_d%cn` | average curve number value for timestep |
| `sw_init` | mm H2O | `hltwb_d%sw_init` | initial soil water content of soil profile at start of time step |
| `sw_final` | mm H2O | `hltwb_d%sw_final` | final soil water content of soil profile at end of time step |
| `sw` | mm H2O | `hltwb_d%sw` | average soil water content of soil profile |
| `sw_300` | mm H2O | `hltwb_d%sw_300` | final soil water content of upper 300 mm at end of time step |
| `sno_init` | mm H2O | `hltwb_d%sno_init` | initial soil water content of snow pack |
| `sno_final` | mm H2O | `hltwb_d%sno_final` | final soil water content of snow pack |
| `snopack` | mm | `hltwb_d%snopack` | water equivalent in snow pack |
| `pet` | mm H2O | `hltwb_d%pet` | potential evapotranspiration |
| `qtile` | mm H2O | `hltwb_d%qtile` | subsurface tile flow leaving the landscape |
| `irr` | mm H2O | `hltwb_d%irr` | irrigation water applied |
| `surq_runon` | mm H2O | `hltwb_d%surq_runon` | surface runoff from upland landscape |
| `latq_runon` | mm H2O | `hltwb_d%latq_runon` | lateral soil flow from upland landscape |
| `overbank` | mm H2O | `hltwb_d%overbank` | overbank flooding from channels |
| `surq_cha` | mm H2O | `hltwb_d%surq_cha` | surface runoff flowing into channels |
| `surq_res` | mm H2O | `hltwb_d%surq_res` | surface runoff flowing into reservoirs |
| `surq_ls` | mm H2O | `hltwb_d%surq_ls` | surface runoff flowing onto the landscape |
| `latq_cha` | mm H2O | `hltwb_d%latq_cha` | lateral soil flow into channels |
| `latq_res` | mm H2O | `hltwb_d%latq_res` | lateral soil flow into reservoirs |
| `latq_ls` | mm H2O | `hltwb_d%latq_ls` | lateral soil flow into a landscape element |
| `gwsoil` | mm H2O | `hltwb_d%gwsoil` | groundwater transferred to soil profile (when water table is in soil profile) !rtb gwflow |
| `satex` | mm H2O | `hltwb_d%satex` | saturation excess flow developed from high water table !rtb gwflow |
| `satex_chan` | mm H2O | `hltwb_d%satex_chan` | saturation excess flow reaching main channel !rtb gwflow |
| `delsw` | mm H2O | `hltwb_d%delsw` | change in soil water volume !rtb gwflow |
| `lagsurf` | mm H2O | `hltwb_d%lagsurf` | surface runoff in transit to channel |
| `laglatq` | mm H2O | `hltwb_d%laglatq` | lateral flow in transit to channel |
| `lagsatex` | mm H2O | `hltwb_d%lagsatex` | saturation excess flow in transit to channel |
| `wet_evap` | mm H2O | `hltwb_d%wet_evap` | evaporation from wetland surface |
| `wet_out` | mm H2O | `hltwb_d%wet_out` | outflow (spill) from wetland |
| `wet_stor` | mm H2O | `hltwb_d%wet_stor` | volume stored in wetland at end of time period |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`hltwb_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `output_waterbal` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `hru_lte_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`hru_lte_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `output_waterbal` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hru_lte_output.f90:24` | `2300` | time, identity, `hltwb_d(idx)` record |
| `hru_lte_output.f90:26` | `2304` | time, identity, `hltwb_d(idx)` record |
| `hru_lte_output.f90:37` | `2440` | time, identity, `hltls_d(idx)` record |
| `hru_lte_output.f90:39` | `2444` | time, identity, `hltls_d(idx)` record |
| `hru_lte_output.f90:44` | `2460` | time, identity, `hltpw_d(idx)` record |
| `hru_lte_output.f90:46` | `2464` | time, identity, `hltpw_d(idx)` record |
| `hru_lte_output.f90:65` | `2301` | time, identity, `hltwb_m(idx)` record |
| `hru_lte_output.f90:67` | `2305` | time, identity, `hltwb_m(idx)` record |
| `hru_lte_output.f90:78` | `2441` | time, identity, `hltls_m(idx)` record |
| `hru_lte_output.f90:80` | `2445` | time, identity, `hltls_m(idx)` record |
| `hru_lte_output.f90:85` | `2461` | time, identity, `hltpw_m(idx)` record |
| `hru_lte_output.f90:87` | `2465` | time, identity, `hltpw_m(idx)` record |
| `hru_lte_output.f90:111` | `2302` | time, identity, `hltwb_y(idx)` record |
| `hru_lte_output.f90:113` | `2306` | time, identity, `hltwb_y(idx)` record |
| `hru_lte_output.f90:124` | `2442` | time, identity, `hltls_y(idx)` record |
| `hru_lte_output.f90:126` | `2446` | time, identity, `hltls_y(idx)` record |
| `hru_lte_output.f90:131` | `2462` | time, identity, `hltpw_y(idx)` record |
| `hru_lte_output.f90:133` | `2466` | time, identity, `hltpw_y(idx)` record |
| `hru_lte_output.f90:144` | `2303` | time, identity, `hltwb_a(idx)` record |
| `hru_lte_output.f90:146` | `2307` | time, identity, `hltwb_a(idx)` record |
| `hru_lte_output.f90:163` | `2443` | time, identity, `hltls_a(idx)` record |
| `hru_lte_output.f90:165` | `2447` | time, identity, `hltls_a(idx)` record |
| `hru_lte_output.f90:174` | `2463` | time, identity, `hltpw_a(idx)` record |
| `hru_lte_output.f90:176` | `2467` | time, identity, `hltpw_a(idx)` record |

Header and file-open statements are in `output_landscape_init`.

## Review Notes

- Every frequency shares the `output_waterbal` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `output_waterbal` type definition in `output_landscape_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`hru_lte_output`](../procedures/hru_lte_output.md)
- Header / opener: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Data type: `output_landscape_module::output_waterbal`

## Evidence Used

- `hru_lte_output.f90`
- `output_landscape_init.f90`
- `output_landscape_module.f90` (`type output_waterbal`)
