---
kind: output_family
source_symbols:
- hru_output
- output_landscape_init
title: hru_ls_*
status: filled
source_hash: 9757d21fc5959b0f
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`output_landscape_init`](../procedures/output_landscape_init.md)  
**Written by:** [`hru_output`](../procedures/hru_output.md)  
**Primary data type:** `output_landscape_module::output_waterbal`  
**Files covered:** `hru_ls_day`, `hru_ls_mon`, `hru_ls_yr`, `hru_ls_aa` text/CSV pairs

## Bottom Line

`hru_ls_*` is the `hru_ls` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `output_waterbal` state object written by `hru_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `hru_ls` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hru_ls_day.txt` | `hru_ls_day.csv` | 2030 | 2034 | `output_landscape_init.f90:431` |
| Monthly | `hru_ls_mon.txt` | `hru_ls_mon.csv` | 2031 | 2035 | `output_landscape_init.f90:449` |
| Yearly | `hru_ls_yr.txt` | `hru_ls_yr.csv` | 2032 | 2036 | `output_landscape_init.f90:464` |
| Average annual | `hru_ls_aa.txt` | `hru_ls_aa.csv` | 2033 | 2037 | `output_landscape_init.f90:479` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `output_landscape_init.f90:431` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%ls_hru%m == "y") then` | `output_landscape_init.f90:449` |
| Yearly | `if (time%end_yr == 1) then  →  if (pco%ls_hru%y == "y") then` | `output_landscape_init.f90:464` |
| Average annual | `if (time%end_sim == 1 .and. pco%ls_hru%a == "y") then` | `output_landscape_init.f90:479` |

The header and units rows for every file are written by `output_landscape_init`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the configured print interval. |
| `pco%ls_hru%d == "y"` | day | Enables output for this frequency. |
| `pco%ls_hru%m == "y"` | mon | Enables output for this frequency. |
| `pco%ls_hru%y == "y"` | yr | Enables output for this frequency. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%ls_hru%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `output_landscape_init` | Basin name and program string. |
| Header row | `output_landscape_init` | Column names for the time, identity, and `output_waterbal` values. |
| Units row | `output_landscape_init` | Units for the value columns. |
| Data row | `hru_output` | One `output_waterbal` record for the active frequency. |

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
| `precip` | mm H2O | `hwb_d%precip` | precipitation falling as rain and snow |
| `snofall` | mm H2O | `hwb_d%snofall` | precipitation falling as snow, sleet or freezing rain |
| `snomlt` | mm H2O | `hwb_d%snomlt` | snow or melting ice |
| `surq_gen` | mm H2O | `hwb_d%surq_gen` | surface runoff generated from the landscape |
| `latq` | mm H2O | `hwb_d%latq` | lateral soil flow |
| `wateryld` | mm H2O | `hwb_d%wateryld` | water yield - sum of surface runoff, lateral soil flow and tile flow |
| `perc` | mm H2O | `hwb_d%perc` | amt of water perc out of the soil profile & into the vadose zone |
| `et` | mm H2O | `hwb_d%et` | actual evapotranspiration from the soil |
| `ecanopy` | mm H2O | `hwb_d%ecanopy` | not reported |
| `eplant` | mm H2O | `hwb_d%eplant` | plant transpiration |
| `esoil` | mm H2O | `hwb_d%esoil` | soil evaporation |
| `surq_cont` | mm H2O | `hwb_d%surq_cont` | surface runoff leaving the landscape |
| `cn` | none | `hwb_d%cn` | average curve number value for timestep |
| `sw_init` | mm H2O | `hwb_d%sw_init` | initial soil water content of soil profile at start of time step |
| `sw_final` | mm H2O | `hwb_d%sw_final` | final soil water content of soil profile at end of time step |
| `sw` | mm H2O | `hwb_d%sw` | average soil water content of soil profile |
| `sw_300` | mm H2O | `hwb_d%sw_300` | final soil water content of upper 300 mm at end of time step |
| `sno_init` | mm H2O | `hwb_d%sno_init` | initial soil water content of snow pack |
| `sno_final` | mm H2O | `hwb_d%sno_final` | final soil water content of snow pack |
| `snopack` | mm | `hwb_d%snopack` | water equivalent in snow pack |
| `pet` | mm H2O | `hwb_d%pet` | potential evapotranspiration |
| `qtile` | mm H2O | `hwb_d%qtile` | subsurface tile flow leaving the landscape |
| `irr` | mm H2O | `hwb_d%irr` | irrigation water applied |
| `surq_runon` | mm H2O | `hwb_d%surq_runon` | surface runoff from upland landscape |
| `latq_runon` | mm H2O | `hwb_d%latq_runon` | lateral soil flow from upland landscape |
| `overbank` | mm H2O | `hwb_d%overbank` | overbank flooding from channels |
| `surq_cha` | mm H2O | `hwb_d%surq_cha` | surface runoff flowing into channels |
| `surq_res` | mm H2O | `hwb_d%surq_res` | surface runoff flowing into reservoirs |
| `surq_ls` | mm H2O | `hwb_d%surq_ls` | surface runoff flowing onto the landscape |
| `latq_cha` | mm H2O | `hwb_d%latq_cha` | lateral soil flow into channels |
| `latq_res` | mm H2O | `hwb_d%latq_res` | lateral soil flow into reservoirs |
| `latq_ls` | mm H2O | `hwb_d%latq_ls` | lateral soil flow into a landscape element |
| `gwsoil` | mm H2O | `hwb_d%gwsoil` | groundwater transferred to soil profile (when water table is in soil profile) !rtb gwflow |
| `satex` | mm H2O | `hwb_d%satex` | saturation excess flow developed from high water table !rtb gwflow |
| `satex_chan` | mm H2O | `hwb_d%satex_chan` | saturation excess flow reaching main channel !rtb gwflow |
| `delsw` | mm H2O | `hwb_d%delsw` | change in soil water volume !rtb gwflow |
| `lagsurf` | mm H2O | `hwb_d%lagsurf` | surface runoff in transit to channel |
| `laglatq` | mm H2O | `hwb_d%laglatq` | lateral flow in transit to channel |
| `lagsatex` | mm H2O | `hwb_d%lagsatex` | saturation excess flow in transit to channel |
| `wet_evap` | mm H2O | `hwb_d%wet_evap` | evaporation from wetland surface |
| `wet_out` | mm H2O | `hwb_d%wet_out` | outflow (spill) from wetland |
| `wet_stor` | mm H2O | `hwb_d%wet_stor` | volume stored in wetland at end of time period |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`hwb_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `output_waterbal` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `hru_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`hru_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `output_waterbal` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hru_output.f90:63` | `2000` | time, identity, `hwb_d(idx)` record |
| `hru_output.f90:67` | `2004` | time, identity, `hwb_d(idx)` record |
| `hru_output.f90:75` | `2020` | time, identity, `hnb_d(idx)` record |
| `hru_output.f90:78` | `2024` | time, identity, `hnb_d(idx)` record |
| `hru_output.f90:83` | `2030` | time, identity, `hls_d(idx)` record |
| `hru_output.f90:86` | `2034` | time, identity, `hls_d(idx)` record |
| `hru_output.f90:92` | `2040` | time, identity, `hpw_d(idx)` record |
| `hru_output.f90:95` | `2044` | time, identity, `hpw_d(idx)` record |
| `hru_output.f90:122` | `2001` | time, identity, `hwb_m(idx)` record |
| `hru_output.f90:125` | `2005` | time, identity, `hwb_m(idx)` record |
| `hru_output.f90:131` | `2021` | time, identity, `hnb_m(idx)` record |
| `hru_output.f90:134` | `2025` | time, identity, `hnb_m(idx)` record |
| `hru_output.f90:140` | `2031` | time, identity, `hls_m(idx)` record |
| `hru_output.f90:143` | `2035` | time, identity, `hls_m(idx)` record |
| `hru_output.f90:151` | `2041` | time, identity, `hpw_m(idx)` record |
| `hru_output.f90:154` | `2045` | time, identity, `hpw_m(idx)` record |
| `hru_output.f90:193` | `2002` | time, identity, `hwb_y(idx)` record |
| `hru_output.f90:196` | `2006` | time, identity, `hwb_y(idx)` record |
| `hru_output.f90:202` | `2022` | time, identity, `hnb_y(idx)` record |
| `hru_output.f90:205` | `2026` | time, identity, `hnb_y(idx)` record |
| `hru_output.f90:211` | `2032` | time, identity, `hls_y(idx)` record |
| `hru_output.f90:214` | `2036` | time, identity, `hls_y(idx)` record |
| `hru_output.f90:222` | `2042` | time, identity, `hpw_y(idx)` record |
| `hru_output.f90:225` | `2046` | time, identity, `hpw_y(idx)` record |
| `hru_output.f90:245` | `2003` | time, identity, `hwb_a(idx)` record |
| `hru_output.f90:248` | `2007` | time, identity, `hwb_a(idx)` record |
| `hru_output.f90:267` | `2023` | time, identity, `hnb_a(idx)` record |
| `hru_output.f90:270` | `2027` | time, identity, `hnb_a(idx)` record |
| `hru_output.f90:279` | `2033` | time, identity, `hls_a(idx)` record |
| `hru_output.f90:282` | `2037` | time, identity, `hls_a(idx)` record |
| `hru_output.f90:294` | `2043` | time, identity, `hpw_a(idx)` record |
| `hru_output.f90:297` | `2047` | time, identity, `hpw_a(idx)` record |
| `hru_output.f90:329` | `4008` | time, identity, time/identity fields |
| `hru_output.f90:331` | `4009` | time, identity, time/identity fields |

Header and file-open statements are in `output_landscape_init`.

## Review Notes

- Every frequency shares the `output_waterbal` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `output_waterbal` type definition in `output_landscape_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`hru_output`](../procedures/hru_output.md)
- Header / opener: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Data type: `output_landscape_module::output_waterbal`

## Evidence Used

- `hru_output.f90`
- `output_landscape_init.f90`
- `output_landscape_module.f90` (`type output_waterbal`)
