---
kind: output_family
source_symbols:
- basin_output
- output_landscape_init
title: basin_nb_*
status: filled
source_hash: 19044e4eb883746f
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`output_landscape_init`](../procedures/output_landscape_init.md)  
**Written by:** [`basin_output`](../procedures/basin_output.md)  
**Primary data type:** `output_landscape_module::output_waterbal`  
**Files covered:** `basin_nb_day`, `basin_nb_mon`, `basin_nb_yr`, `basin_nb_aa` text/CSV pairs

## Bottom Line

`basin_nb_*` is the `basin_nb` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `output_waterbal` state object written by `basin_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `basin_nb` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `basin_nb_day.txt` | `basin_nb_day.csv` | 2060 | 2064 | `output_landscape_init.f90:1072` |
| Monthly | `basin_nb_mon.txt` | `basin_nb_mon.csv` | 2061 | 2065 | `output_landscape_init.f90:1087` |
| Yearly | `basin_nb_yr.txt` | `basin_nb_yr.csv` | 2062 | 2066 | `output_landscape_init.f90:1102` |
| Average annual | `basin_nb_aa.txt` | `basin_nb_aa.csv` | 2063 | 2067 | `output_landscape_init.f90:1117` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%day_print == "y" .and. pco%int_day_cur == pco%int_day) then  →  if (pco%` | `output_landscape_init.f90:1072` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%nb_bsn%m == "y") then` | `output_landscape_init.f90:1087` |
| Yearly | `if (time%end_yr == 1) then  →  if (pco%nb_bsn%y == "y") then` | `output_landscape_init.f90:1102` |
| Average annual | `if (time%end_sim == 1) then  →  if (pco%nb_bsn%a == "y") then` | `output_landscape_init.f90:1117` |

The header and units rows for every file are written by `output_landscape_init`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%day_print == "y" .and. pco%int_day_cur == pco%int_day` | day | Restricts daily rows to the configured print interval. |
| `pco%nb_bsn%a == "y"` | aa | Enables output for this frequency. |
| `pco%nb_bsn%d == "y"` | day | Enables output for this frequency. |
| `pco%nb_bsn%m == "y"` | mon | Enables output for this frequency. |
| `pco%nb_bsn%y == "y"` | yr | Enables output for this frequency. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1` | aa | Builds and writes rows at simulation end. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `output_landscape_init` | Basin name and program string. |
| Header row | `output_landscape_init` | Column names for the time, identity, and `output_waterbal` values. |
| Units row | `output_landscape_init` | Units for the value columns. |
| Data row | `basin_output` | One `output_waterbal` record for the active frequency. |

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
| `precip` | mm H2O | `bwb_d%precip` | precipitation falling as rain and snow |
| `snofall` | mm H2O | `bwb_d%snofall` | precipitation falling as snow, sleet or freezing rain |
| `snomlt` | mm H2O | `bwb_d%snomlt` | snow or melting ice |
| `surq_gen` | mm H2O | `bwb_d%surq_gen` | surface runoff generated from the landscape |
| `latq` | mm H2O | `bwb_d%latq` | lateral soil flow |
| `wateryld` | mm H2O | `bwb_d%wateryld` | water yield - sum of surface runoff, lateral soil flow and tile flow |
| `perc` | mm H2O | `bwb_d%perc` | amt of water perc out of the soil profile & into the vadose zone |
| `et` | mm H2O | `bwb_d%et` | actual evapotranspiration from the soil |
| `ecanopy` | mm H2O | `bwb_d%ecanopy` | not reported |
| `eplant` | mm H2O | `bwb_d%eplant` | plant transpiration |
| `esoil` | mm H2O | `bwb_d%esoil` | soil evaporation |
| `surq_cont` | mm H2O | `bwb_d%surq_cont` | surface runoff leaving the landscape |
| `cn` | none | `bwb_d%cn` | average curve number value for timestep |
| `sw_init` | mm H2O | `bwb_d%sw_init` | initial soil water content of soil profile at start of time step |
| `sw_final` | mm H2O | `bwb_d%sw_final` | final soil water content of soil profile at end of time step |
| `sw` | mm H2O | `bwb_d%sw` | average soil water content of soil profile |
| `sw_300` | mm H2O | `bwb_d%sw_300` | final soil water content of upper 300 mm at end of time step |
| `sno_init` | mm H2O | `bwb_d%sno_init` | initial soil water content of snow pack |
| `sno_final` | mm H2O | `bwb_d%sno_final` | final soil water content of snow pack |
| `snopack` | mm | `bwb_d%snopack` | water equivalent in snow pack |
| `pet` | mm H2O | `bwb_d%pet` | potential evapotranspiration |
| `qtile` | mm H2O | `bwb_d%qtile` | subsurface tile flow leaving the landscape |
| `irr` | mm H2O | `bwb_d%irr` | irrigation water applied |
| `surq_runon` | mm H2O | `bwb_d%surq_runon` | surface runoff from upland landscape |
| `latq_runon` | mm H2O | `bwb_d%latq_runon` | lateral soil flow from upland landscape |
| `overbank` | mm H2O | `bwb_d%overbank` | overbank flooding from channels |
| `surq_cha` | mm H2O | `bwb_d%surq_cha` | surface runoff flowing into channels |
| `surq_res` | mm H2O | `bwb_d%surq_res` | surface runoff flowing into reservoirs |
| `surq_ls` | mm H2O | `bwb_d%surq_ls` | surface runoff flowing onto the landscape |
| `latq_cha` | mm H2O | `bwb_d%latq_cha` | lateral soil flow into channels |
| `latq_res` | mm H2O | `bwb_d%latq_res` | lateral soil flow into reservoirs |
| `latq_ls` | mm H2O | `bwb_d%latq_ls` | lateral soil flow into a landscape element |
| `gwsoil` | mm H2O | `bwb_d%gwsoil` | groundwater transferred to soil profile (when water table is in soil profile) !rtb gwflow |
| `satex` | mm H2O | `bwb_d%satex` | saturation excess flow developed from high water table !rtb gwflow |
| `satex_chan` | mm H2O | `bwb_d%satex_chan` | saturation excess flow reaching main channel !rtb gwflow |
| `delsw` | mm H2O | `bwb_d%delsw` | change in soil water volume !rtb gwflow |
| `lagsurf` | mm H2O | `bwb_d%lagsurf` | surface runoff in transit to channel |
| `laglatq` | mm H2O | `bwb_d%laglatq` | lateral flow in transit to channel |
| `lagsatex` | mm H2O | `bwb_d%lagsatex` | saturation excess flow in transit to channel |
| `wet_evap` | mm H2O | `bwb_d%wet_evap` | evaporation from wetland surface |
| `wet_out` | mm H2O | `bwb_d%wet_out` | outflow (spill) from wetland |
| `wet_stor` | mm H2O | `bwb_d%wet_stor` | volume stored in wetland at end of time period |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`bwb_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `output_waterbal` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `basin_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`basin_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `output_waterbal` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `basin_output.f90:72` | `2050` | time, identity, `bwb_d(idx)` record |
| `basin_output.f90:74` | `2054` | time, identity, `bwb_d(idx)` record |
| `basin_output.f90:80` | `2060` | time, identity, `bnb_d(idx)` record |
| `basin_output.f90:82` | `2064` | time, identity, `bnb_d(idx)` record |
| `basin_output.f90:86` | `2070` | time, identity, `bls_d(idx)` record |
| `basin_output.f90:88` | `2074` | time, identity, `bls_d(idx)` record |
| `basin_output.f90:92` | `2080` | time, identity, `bpw_d(idx)` record |
| `basin_output.f90:94` | `2084` | time, identity, `bpw_d(idx)` record |
| `basin_output.f90:112` | `2051` | time, identity, `bwb_m(idx)` record |
| `basin_output.f90:114` | `2055` | time, identity, `bwb_m(idx)` record |
| `basin_output.f90:120` | `2061` | time, identity, `bnb_m(idx)` record |
| `basin_output.f90:122` | `2065` | time, identity, `bnb_m(idx)` record |
| `basin_output.f90:126` | `2071` | time, identity, `bls_m(idx)` record |
| `basin_output.f90:128` | `2075` | time, identity, `bls_m(idx)` record |
| `basin_output.f90:134` | `2081` | time, identity, `bpw_m(idx)` record |
| `basin_output.f90:136` | `2085` | time, identity, `bpw_m(idx)` record |
| `basin_output.f90:164` | `2052` | time, identity, `bwb_y(idx)` record |
| `basin_output.f90:166` | `2056` | time, identity, `bwb_y(idx)` record |
| `basin_output.f90:172` | `2062` | time, identity, `bnb_y(idx)` record |
| `basin_output.f90:174` | `2066` | time, identity, `bnb_y(idx)` record |
| `basin_output.f90:178` | `2072` | time, identity, `bls_y(idx)` record |
| `basin_output.f90:180` | `2076` | time, identity, `bls_y(idx)` record |
| `basin_output.f90:186` | `2082` | time, identity, `bpw_y(idx)` record |
| `basin_output.f90:188` | `2086` | time, identity, `bpw_y(idx)` record |
| `basin_output.f90:215` | `2053` | time, identity, `bwb_a(idx)` record |
| `basin_output.f90:217` | `2057` | time, identity, `bwb_a(idx)` record |
| `basin_output.f90:227` | `2063` | time, identity, `bnb_a(idx)` record |
| `basin_output.f90:229` | `2067` | time, identity, `bnb_a(idx)` record |
| `basin_output.f90:236` | `2073` | time, identity, `bls_a(idx)` record |
| `basin_output.f90:238` | `2077` | time, identity, `bls_a(idx)` record |
| `basin_output.f90:246` | `2083` | time, identity, `bpw_a(idx)` record |
| `basin_output.f90:248` | `2087` | time, identity, `bpw_a(idx)` record |

Header and file-open statements are in `output_landscape_init`.

## Review Notes

- Every frequency shares the `output_waterbal` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `output_waterbal` type definition in `output_landscape_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`basin_output`](../procedures/basin_output.md)
- Header / opener: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Data type: `output_landscape_module::output_waterbal`

## Evidence Used

- `basin_output.f90`
- `output_landscape_init.f90`
- `output_landscape_module.f90` (`type output_waterbal`)
