---
kind: output_family
source_symbols:
- lsu_output
- output_landscape_init
title: lsunit_pw_*
status: filled
source_hash: e12fdb8e365a2b82
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`output_landscape_init`](../procedures/output_landscape_init.md)  
**Written by:** [`lsu_output`](../procedures/lsu_output.md)  
**Primary data type:** `output_landscape_module::output_waterbal`  
**Files covered:** `lsunit_pw_day`, `lsunit_pw_mon`, `lsunit_pw_yr`, `lsunit_pw_aa` text/CSV pairs

## Bottom Line

`lsunit_pw_*` is the `lsunit_pw` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `output_waterbal` state object written by `lsu_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `lsunit_pw` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `lsunit_pw_day.txt` | `lsunit_pw_day.csv` | 2170 | 2174 | `output_landscape_init.f90:948` |
| Monthly | `lsunit_pw_mon.txt` | `lsunit_pw_mon.csv` | 2171 | 2175 | `output_landscape_init.f90:964` |
| Yearly | `lsunit_pw_yr.txt` | `lsunit_pw_yr.csv` | 2172 | 2176 | `output_landscape_init.f90:979` |
| Average annual | `lsunit_pw_aa.txt` | `lsunit_pw_aa.csv` | 2173 | 2177 | `output_landscape_init.f90:994` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do ilsu = 1, db_mx%lsu_out  →  if (pco%day_print == "y" .and. pco%int_day_cur ==` | `output_landscape_init.f90:948` |
| Monthly | `do ilsu = 1, db_mx%lsu_out  →  if (time%end_mo == 1) then  →  if (pco%pw_lsu%m =` | `output_landscape_init.f90:964` |
| Yearly | `do ilsu = 1, db_mx%lsu_out  →  if (time%end_yr == 1) then  →  if (pco%pw_lsu%y =` | `output_landscape_init.f90:979` |
| Average annual | `do ilsu = 1, db_mx%lsu_out  →  if (time%end_sim == 1 .and. pco%pw_lsu%a == "y") ` | `output_landscape_init.f90:994` |

The header and units rows for every file are written by `output_landscape_init`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | day | Open/print guard. |
| `db_mx%lsu_out` | day | Open/print guard. |
| `do ilsu = 1, db_mx%lsu_out` | All files | Open/print guard. |
| `pco%cb_gl_hru%a == "y"` | day | Enables output for this frequency. |
| `pco%cb_gl_hru%d == "y"` | day | Enables output for this frequency. |
| `pco%cb_gl_hru%m == "y"` | day | Enables output for this frequency. |
| `pco%cb_gl_hru%y == "y"` | day | Enables output for this frequency. |
| `pco%cb_trf_hru%a == "y"` | day | Enables output for this frequency. |
| `pco%cb_trf_hru%d == "y"` | day | Enables output for this frequency. |
| `pco%cb_trf_hru%m == "y"` | day | Enables output for this frequency. |
| `pco%cb_trf_hru%y == "y"` | day | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day, mon | Restricts daily rows to the configured print interval. |
| `pco%ls_hru%d == "y"` | day | Enables output for this frequency. |
| `pco%ls_hru%m == "y"` | day | Enables output for this frequency. |
| `pco%ls_hru%y == "y"` | day | Enables output for this frequency. |
| `pco%ls_lsu%d == "y"` | day | Enables output for this frequency. |
| `pco%ls_lsu%y == "y"` | day | Enables output for this frequency. |
| `pco%ls_sd%d == "y"` | day | Enables output for this frequency. |
| `pco%ls_sd%y == "y"` | day | Enables output for this frequency. |
| `pco%nb_hru%a == "y"` | day | Enables output for this frequency. |
| `pco%nb_hru%d == "y"` | day | Enables output for this frequency. |
| `pco%nb_hru%m == "y"` | day | Enables output for this frequency. |
| `pco%nb_hru%y == "y"` | day | Enables output for this frequency. |
| `pco%nb_lsu%d == "y"` | day | Enables output for this frequency. |
| `pco%nb_lsu%y == "y"` | day | Enables output for this frequency. |
| `pco%pw_hru%d == "y"` | day | Enables output for this frequency. |
| `pco%pw_hru%m == "y"` | day | Enables output for this frequency. |
| `pco%pw_hru%y == "y"` | day | Enables output for this frequency. |
| `pco%pw_lsu%d == "y"` | day, mon | Enables output for this frequency. |
| `pco%pw_lsu%m == "y"` | mon | Enables output for this frequency. |
| `pco%pw_lsu%y == "y"` | yr | Enables output for this frequency. |
| `pco%pw_sd%d == "y"` | day | Enables output for this frequency. |
| `pco%pw_sd%y == "y"` | day | Enables output for this frequency. |
| `pco%wb_hru%d == "y"` | day | Enables output for this frequency. |
| `pco%wb_hru%y == "y"` | day | Enables output for this frequency. |
| `pco%wb_lsu%d == "y"` | day | Enables output for this frequency. |
| `pco%wb_sd%d == "y"` | day | Enables output for this frequency. |
| `sp_ob%hru` | day | Open/print guard. |
| `sp_ob%hru_lte` | day | Open/print guard. |
| `sp_ob%ru` | day | Open/print guard. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1 .and. pco%pw_lsu%a == "y"` | aa | Open/print guard. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `output_landscape_init` | Basin name and program string. |
| Header row | `output_landscape_init` | Column names for the time, identity, and `output_waterbal` values. |
| Units row | `output_landscape_init` | Units for the value columns. |
| Data row | `lsu_output` | One `output_waterbal` record for the active frequency. |

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
| `precip` | mm H2O | `ruwb_d%precip` | precipitation falling as rain and snow |
| `snofall` | mm H2O | `ruwb_d%snofall` | precipitation falling as snow, sleet or freezing rain |
| `snomlt` | mm H2O | `ruwb_d%snomlt` | snow or melting ice |
| `surq_gen` | mm H2O | `ruwb_d%surq_gen` | surface runoff generated from the landscape |
| `latq` | mm H2O | `ruwb_d%latq` | lateral soil flow |
| `wateryld` | mm H2O | `ruwb_d%wateryld` | water yield - sum of surface runoff, lateral soil flow and tile flow |
| `perc` | mm H2O | `ruwb_d%perc` | amt of water perc out of the soil profile & into the vadose zone |
| `et` | mm H2O | `ruwb_d%et` | actual evapotranspiration from the soil |
| `ecanopy` | mm H2O | `ruwb_d%ecanopy` | not reported |
| `eplant` | mm H2O | `ruwb_d%eplant` | plant transpiration |
| `esoil` | mm H2O | `ruwb_d%esoil` | soil evaporation |
| `surq_cont` | mm H2O | `ruwb_d%surq_cont` | surface runoff leaving the landscape |
| `cn` | none | `ruwb_d%cn` | average curve number value for timestep |
| `sw_init` | mm H2O | `ruwb_d%sw_init` | initial soil water content of soil profile at start of time step |
| `sw_final` | mm H2O | `ruwb_d%sw_final` | final soil water content of soil profile at end of time step |
| `sw` | mm H2O | `ruwb_d%sw` | average soil water content of soil profile |
| `sw_300` | mm H2O | `ruwb_d%sw_300` | final soil water content of upper 300 mm at end of time step |
| `sno_init` | mm H2O | `ruwb_d%sno_init` | initial soil water content of snow pack |
| `sno_final` | mm H2O | `ruwb_d%sno_final` | final soil water content of snow pack |
| `snopack` | mm | `ruwb_d%snopack` | water equivalent in snow pack |
| `pet` | mm H2O | `ruwb_d%pet` | potential evapotranspiration |
| `qtile` | mm H2O | `ruwb_d%qtile` | subsurface tile flow leaving the landscape |
| `irr` | mm H2O | `ruwb_d%irr` | irrigation water applied |
| `surq_runon` | mm H2O | `ruwb_d%surq_runon` | surface runoff from upland landscape |
| `latq_runon` | mm H2O | `ruwb_d%latq_runon` | lateral soil flow from upland landscape |
| `overbank` | mm H2O | `ruwb_d%overbank` | overbank flooding from channels |
| `surq_cha` | mm H2O | `ruwb_d%surq_cha` | surface runoff flowing into channels |
| `surq_res` | mm H2O | `ruwb_d%surq_res` | surface runoff flowing into reservoirs |
| `surq_ls` | mm H2O | `ruwb_d%surq_ls` | surface runoff flowing onto the landscape |
| `latq_cha` | mm H2O | `ruwb_d%latq_cha` | lateral soil flow into channels |
| `latq_res` | mm H2O | `ruwb_d%latq_res` | lateral soil flow into reservoirs |
| `latq_ls` | mm H2O | `ruwb_d%latq_ls` | lateral soil flow into a landscape element |
| `gwsoil` | mm H2O | `ruwb_d%gwsoil` | groundwater transferred to soil profile (when water table is in soil profile) !rtb gwflow |
| `satex` | mm H2O | `ruwb_d%satex` | saturation excess flow developed from high water table !rtb gwflow |
| `satex_chan` | mm H2O | `ruwb_d%satex_chan` | saturation excess flow reaching main channel !rtb gwflow |
| `delsw` | mm H2O | `ruwb_d%delsw` | change in soil water volume !rtb gwflow |
| `lagsurf` | mm H2O | `ruwb_d%lagsurf` | surface runoff in transit to channel |
| `laglatq` | mm H2O | `ruwb_d%laglatq` | lateral flow in transit to channel |
| `lagsatex` | mm H2O | `ruwb_d%lagsatex` | saturation excess flow in transit to channel |
| `wet_evap` | mm H2O | `ruwb_d%wet_evap` | evaporation from wetland surface |
| `wet_out` | mm H2O | `ruwb_d%wet_out` | outflow (spill) from wetland |
| `wet_stor` | mm H2O | `ruwb_d%wet_stor` | volume stored in wetland at end of time period |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`ruwb_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `output_waterbal` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `lsu_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`lsu_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `output_waterbal` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `lsu_output.f90:72` | `2140` | time, identity, `ruwb_d(idx)` record |
| `lsu_output.f90:74` | `2144` | time, identity, `ruwb_d(idx)` record |
| `lsu_output.f90:81` | `2150` | time, identity, `runb_d(idx)` record |
| `lsu_output.f90:83` | `2154` | time, identity, `runb_d(idx)` record |
| `lsu_output.f90:88` | `2160` | time, identity, `ruls_d(idx)` record |
| `lsu_output.f90:90` | `2164` | time, identity, `ruls_d(idx)` record |
| `lsu_output.f90:95` | `2170` | time, identity, `rupw_d(idx)` record |
| `lsu_output.f90:97` | `2175` | time, identity, `rupw_d(idx)` record |
| `lsu_output.f90:117` | `2141` | time, identity, `ruwb_m(idx)` record |
| `lsu_output.f90:119` | `2145` | time, identity, `ruwb_m(idx)` record |
| `lsu_output.f90:126` | `2151` | time, identity, `runb_m(idx)` record |
| `lsu_output.f90:128` | `2155` | time, identity, `runb_m(idx)` record |
| `lsu_output.f90:133` | `2161` | time, identity, `ruls_m(idx)` record |
| `lsu_output.f90:135` | `2165` | time, identity, `ruls_m(idx)` record |
| `lsu_output.f90:142` | `2171` | time, identity, `rupw_m(idx)` record |
| `lsu_output.f90:172` | `2142` | time, identity, `ruwb_y(idx)` record |
| `lsu_output.f90:174` | `2146` | time, identity, `ruwb_y(idx)` record |
| `lsu_output.f90:181` | `2152` | time, identity, `runb_y(idx)` record |
| `lsu_output.f90:183` | `2156` | time, identity, `runb_y(idx)` record |
| `lsu_output.f90:188` | `2162` | time, identity, `ruls_y(idx)` record |
| `lsu_output.f90:190` | `2166` | time, identity, `ruls_y(idx)` record |
| `lsu_output.f90:197` | `2172` | time, identity, `rupw_y(idx)` record |
| `lsu_output.f90:199` | `2176` | time, identity, `rupw_y(idx)` record |
| `lsu_output.f90:226` | `2143` | time, identity, `ruwb_a(idx)` record |
| `lsu_output.f90:228` | `2147` | time, identity, `ruwb_a(idx)` record |
| `lsu_output.f90:233` | `2153` | time, identity, `runb_a(idx)` record |
| `lsu_output.f90:235` | `2157` | time, identity, `runb_a(idx)` record |
| `lsu_output.f90:240` | `2163` | time, identity, `ruls_a(idx)` record |
| `lsu_output.f90:242` | `2167` | time, identity, `ruls_a(idx)` record |
| `lsu_output.f90:250` | `2173` | time, identity, `rupw_a(idx)` record |
| `lsu_output.f90:252` | `2177` | time, identity, `rupw_a(idx)` record |

Header and file-open statements are in `output_landscape_init`.

## Review Notes

- Every frequency shares the `output_waterbal` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `output_waterbal` type definition in `output_landscape_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`lsu_output`](../procedures/lsu_output.md)
- Header / opener: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Data type: `output_landscape_module::output_waterbal`

## Evidence Used

- `lsu_output.f90`
- `output_landscape_init.f90`
- `output_landscape_module.f90` (`type output_waterbal`)
