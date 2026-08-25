---
kind: output_family
source_symbols:
- output_landscape_init
title: crop_yld_*
status: filled
source_hash: 5c7017612f9d07e5
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`output_landscape_init`](../procedures/output_landscape_init.md)  
**Written by:** [`output_landscape_init`](../procedures/output_landscape_init.md)  
**Primary data type:** `output_landscape_module::output_waterbal_header`  
**Files covered:** `crop_yld_yr`, `crop_yld_aa` text/CSV pairs

## Bottom Line

`crop_yld_*` is the `crop_yld` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `output_waterbal_header` state object written by `output_landscape_init`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `crop_yld` values for a single reporting period (yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Yearly | `crop_yld_yr.txt` | `crop_yld_yr.csv` | 4010 | 4011 | `output_landscape_init.f90:1256` |
| Average annual | `crop_yld_aa.txt` | `crop_yld_aa.csv` | 4008 | 4009 | `output_landscape_init.f90:1270` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Yearly | `if (sp_ob%hru  →  0) then  →  if (pco%wb_hru%d == "y") then  →  if (pco%wb_hru%y` | `output_landscape_init.f90:1256` |
| Average annual | `if (time%end_sim == 1) then  →  if (pco%cb_snap_hru%a == "y" .and. j == 1) then ` | `output_landscape_init.f90:1270` |

The header and units rows for every file are written by `output_landscape_init`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | aa, yr | Open/print guard. |
| `db_mx%lsu_out` | yr | Open/print guard. |
| `do ipl = 1, pcom(j)%npl` | aa | Open/print guard. |
| `j == 1 .and. (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n")` | aa | Open/print guard. |
| `pco%cb_gl_hru%a == "y"` | yr | Enables output for this frequency. |
| `pco%cb_gl_hru%d == "y"` | yr | Enables output for this frequency. |
| `pco%cb_gl_hru%m == "y"` | yr | Enables output for this frequency. |
| `pco%cb_gl_hru%y == "y"` | yr | Enables output for this frequency. |
| `pco%cb_snap_hru%a == "y" .and. j == 1` | aa | Enables output for this frequency. |
| `pco%cb_trf_hru%a == "y"` | yr | Enables output for this frequency. |
| `pco%cb_trf_hru%d == "y"` | yr | Enables output for this frequency. |
| `pco%cb_trf_hru%m == "y"` | yr | Enables output for this frequency. |
| `pco%cb_trf_hru%y == "y"` | yr | Enables output for this frequency. |
| `pco%crop_yld == "a" .or. pco%crop_yld == "b"` | aa | Enables output for this frequency. |
| `pco%crop_yld == "y" .or. pco%crop_yld == "b"` | yr | Enables output for this frequency. |
| `pco%csvout == "y"` | aa, yr | Enables the CSV companion files. |
| `pco%ls_bsn%d == "y"` | yr | Enables output for this frequency. |
| `pco%ls_bsn%y == "y"` | yr | Enables output for this frequency. |
| `pco%ls_hru%d == "y"` | yr | Enables output for this frequency. |
| `pco%ls_hru%m == "y"` | yr | Enables output for this frequency. |
| `pco%ls_hru%y == "y"` | yr | Enables output for this frequency. |
| `pco%ls_lsu%d == "y"` | yr | Enables output for this frequency. |
| `pco%ls_sd%d == "y"` | yr | Enables output for this frequency. |
| `pco%ls_sd%y == "y"` | yr | Enables output for this frequency. |
| `pco%nb_bsn%d == "y"` | yr | Enables output for this frequency. |
| `pco%nb_bsn%y == "y"` | yr | Enables output for this frequency. |
| `pco%nb_hru%a == "y"` | yr | Enables output for this frequency. |
| `pco%nb_hru%d == "y"` | yr | Enables output for this frequency. |
| `pco%nb_hru%m == "y"` | yr | Enables output for this frequency. |
| `pco%nb_hru%y == "y"` | yr | Enables output for this frequency. |
| `pco%nb_lsu%d == "y"` | yr | Enables output for this frequency. |
| `pco%nb_lsu%y == "y"` | yr | Enables output for this frequency. |
| `pco%pw_bsn%d == "y"` | yr | Enables output for this frequency. |
| `pco%pw_bsn%y == "y"` | yr | Enables output for this frequency. |
| `pco%pw_hru%d == "y"` | yr | Enables output for this frequency. |
| `pco%pw_hru%m == "y"` | yr | Enables output for this frequency. |
| `pco%pw_hru%y == "y"` | yr | Enables output for this frequency. |
| `pco%pw_sd%d == "y"` | yr | Enables output for this frequency. |
| `pco%pw_sd%y == "y"` | yr | Enables output for this frequency. |
| `pco%wb_bsn%d == "y"` | yr | Enables output for this frequency. |
| `pco%wb_bsn%y == "y"` | yr | Enables output for this frequency. |
| `pco%wb_hru%d == "y"` | yr | Enables output for this frequency. |
| `pco%wb_hru%y == "y"` | yr | Enables output for this frequency. |
| `pco%wb_lsu%d == "y"` | yr | Enables output for this frequency. |
| `pco%wb_sd%d == "y"` | yr | Enables output for this frequency. |
| `pcom(j)%plcur(ipl)%harv_num` | aa | Open/print guard. |
| `sp_ob%hru` | yr | Open/print guard. |
| `sp_ob%hru_lte` | yr | Open/print guard. |
| `sp_ob%ru` | yr | Open/print guard. |
| `time%end_sim == 1` | aa | Builds and writes rows at simulation end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `output_landscape_init` | Basin name and program string. |
| Header row | `output_landscape_init` | Column names for the time, identity, and `output_waterbal_header` values. |
| Units row | `output_landscape_init` | Units for the value columns. |
| Data row | `output_landscape_init` | One `output_waterbal_header` record for the active frequency. |

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
| `day` |  | `wb_hdr%day` |  |
| `mo` |  | `wb_hdr%mo` |  |
| `day_mo` |  | `wb_hdr%day_mo` |  |
| `yrc` |  | `wb_hdr%yrc` |  |
| `isd` |  | `wb_hdr%isd` |  |
| `id` |  | `wb_hdr%id` |  |
| `name` |  | `wb_hdr%name` |  |
| `precip` |  | `wb_hdr%precip` |  |
| `snofall` |  | `wb_hdr%snofall` |  |
| `snomlt` |  | `wb_hdr%snomlt` |  |
| `surq_gen` |  | `wb_hdr%surq_gen` |  |
| `latq` |  | `wb_hdr%latq` |  |
| `wateryld` |  | `wb_hdr%wateryld` |  |
| `perc` |  | `wb_hdr%perc` |  |
| `et` |  | `wb_hdr%et` |  |
| `ecanopy` |  | `wb_hdr%ecanopy` |  |
| `eplant` |  | `wb_hdr%eplant` |  |
| `esoil` |  | `wb_hdr%esoil` |  |
| `surq_cont` |  | `wb_hdr%surq_cont` |  |
| `cn` |  | `wb_hdr%cn` |  |
| `sw_init` |  | `wb_hdr%sw_init` |  |
| `sw_final` |  | `wb_hdr%sw_final` |  |
| `sw_ave` |  | `wb_hdr%sw_ave` |  |
| `sw_300` |  | `wb_hdr%sw_300` |  |
| `sno_init` |  | `wb_hdr%sno_init` |  |
| `sno_final` |  | `wb_hdr%sno_final` |  |
| `snopack` |  | `wb_hdr%snopack` |  |
| `pet` |  | `wb_hdr%pet` |  |
| `qtile` |  | `wb_hdr%qtile` |  |
| `irr` |  | `wb_hdr%irr` |  |
| `surq_runon` |  | `wb_hdr%surq_runon` |  |
| `latq_runon` |  | `wb_hdr%latq_runon` |  |
| `overbank` |  | `wb_hdr%overbank` |  |
| `surq_cha` |  | `wb_hdr%surq_cha` |  |
| `surq_res` |  | `wb_hdr%surq_res` |  |
| `surq_ls` |  | `wb_hdr%surq_ls` |  |
| `latq_cha` |  | `wb_hdr%latq_cha` |  |
| `latq_res` |  | `wb_hdr%latq_res` |  |
| `latq_ls` |  | `wb_hdr%latq_ls` |  |
| `gwsoilq` |  | `wb_hdr%gwsoilq` |  |
| `satex` |  | `wb_hdr%satex` |  |
| `satex_chan` |  | `wb_hdr%satex_chan` |  |
| `sw_change` |  | `wb_hdr%sw_change` |  |
| `lagsurf` |  | `wb_hdr%lagsurf` |  |
| `laglatq` |  | `wb_hdr%laglatq` |  |
| `lagsatex` |  | `wb_hdr%lagsatex` |  |
| `wet_evap` |  | `wb_hdr%wet_evap` |  |
| `wet_oflo` |  | `wb_hdr%wet_oflo` |  |
| `wet_stor` |  | `wb_hdr%wet_stor` |  |
| `plt_cov` |  | `wb_hdr%plt_cov` |  |
| `mgt_ops` |  | `wb_hdr%mgt_ops` |  |

## Frequency-Specific Behavior

The columns are identical for every frequency (yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`wb_hdr` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `output_waterbal_header` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `output_landscape_init` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`output_landscape_init` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `output_waterbal_header` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `output_landscape_init.f90:38` | `2000` | time, identity, time/identity fields |
| `output_landscape_init.f90:41` | `9000` | time, identity, time/identity fields |
| `output_landscape_init.f90:45` | `2004` | time, identity, time/identity fields |
| `output_landscape_init.f90:55` | `2001` | time, identity, time/identity fields |
| `output_landscape_init.f90:62` | `2005` | time, identity, time/identity fields |
| `output_landscape_init.f90:72` | `2002` | time, identity, time/identity fields |
| `output_landscape_init.f90:78` | `2006` | time, identity, time/identity fields |
| `output_landscape_init.f90:88` | `2003` | time, identity, time/identity fields |
| `output_landscape_init.f90:94` | `2007` | time, identity, time/identity fields |
| `output_landscape_init.f90:104` | `2020` | time, identity, time/identity fields |
| `output_landscape_init.f90:110` | `2024` | time, identity, time/identity fields |
| `output_landscape_init.f90:120` | `3333` | time, identity, time/identity fields |
| `output_landscape_init.f90:126` | `3334` | time, identity, time/identity fields |
| `output_landscape_init.f90:135` | `3335` | time, identity, time/identity fields |
| `output_landscape_init.f90:141` | `3336` | time, identity, time/identity fields |
| `output_landscape_init.f90:150` | `3337` | time, identity, time/identity fields |
| `output_landscape_init.f90:156` | `3338` | time, identity, time/identity fields |
| `output_landscape_init.f90:165` | `3339` | time, identity, time/identity fields |
| `output_landscape_init.f90:171` | `3340` | time, identity, time/identity fields |
| `output_landscape_init.f90:181` | `2021` | time, identity, time/identity fields |
| `output_landscape_init.f90:187` | `2025` | time, identity, time/identity fields |
| `output_landscape_init.f90:196` | `2022` | time, identity, time/identity fields |
| `output_landscape_init.f90:202` | `2026` | time, identity, time/identity fields |
| `output_landscape_init.f90:211` | `2023` | time, identity, time/identity fields |
| `output_landscape_init.f90:217` | `2027` | time, identity, time/identity fields |
| `output_landscape_init.f90:227` | `4520` | time, identity, time/identity fields |
| `output_landscape_init.f90:233` | `4524` | time, identity, time/identity fields |
| `output_landscape_init.f90:242` | `4521` | time, identity, time/identity fields |
| `output_landscape_init.f90:248` | `4525` | time, identity, time/identity fields |
| `output_landscape_init.f90:257` | `4522` | time, identity, time/identity fields |
| `output_landscape_init.f90:263` | `4526` | time, identity, time/identity fields |
| `output_landscape_init.f90:272` | `4523` | time, identity, time/identity fields |
| `output_landscape_init.f90:278` | `4527` | time, identity, time/identity fields |
| `output_landscape_init.f90:290` | `4550` | time, identity, time/identity fields |
| `output_landscape_init.f90:296` | `4554` | time, identity, time/identity fields |
| `output_landscape_init.f90:305` | `4551` | time, identity, time/identity fields |
| `output_landscape_init.f90:311` | `4555` | time, identity, time/identity fields |
| `output_landscape_init.f90:320` | `4552` | time, identity, time/identity fields |
| `output_landscape_init.f90:326` | `4556` | time, identity, time/identity fields |
| `output_landscape_init.f90:335` | `4553` | time, identity, time/identity fields |
| `output_landscape_init.f90:341` | `4557` | time, identity, time/identity fields |
| `output_landscape_init.f90:432` | `2030` | time, identity, time/identity fields |
| `output_landscape_init.f90:438` | `2034` | time, identity, time/identity fields |
| `output_landscape_init.f90:450` | `2031` | time, identity, time/identity fields |
| `output_landscape_init.f90:456` | `2035` | time, identity, time/identity fields |
| `output_landscape_init.f90:465` | `2032` | time, identity, time/identity fields |
| `output_landscape_init.f90:471` | `2036` | time, identity, time/identity fields |
| `output_landscape_init.f90:480` | `2033` | time, identity, time/identity fields |
| `output_landscape_init.f90:486` | `2037` | time, identity, time/identity fields |
| `output_landscape_init.f90:496` | `2040` | time, identity, time/identity fields |
| `output_landscape_init.f90:502` | `2044` | time, identity, time/identity fields |
| `output_landscape_init.f90:511` | `2041` | time, identity, time/identity fields |
| `output_landscape_init.f90:517` | `2045` | time, identity, time/identity fields |
| `output_landscape_init.f90:526` | `2042` | time, identity, time/identity fields |
| `output_landscape_init.f90:532` | `2046` | time, identity, time/identity fields |
| `output_landscape_init.f90:541` | `2043` | time, identity, time/identity fields |
| `output_landscape_init.f90:547` | `2047` | time, identity, time/identity fields |
| `output_landscape_init.f90:560` | `2300` | time, identity, time/identity fields |
| `output_landscape_init.f90:566` | `2304` | time, identity, time/identity fields |
| `output_landscape_init.f90:576` | `2301` | time, identity, time/identity fields |
| `output_landscape_init.f90:582` | `2305` | time, identity, time/identity fields |
| `output_landscape_init.f90:593` | `2302` | time, identity, time/identity fields |
| `output_landscape_init.f90:599` | `2306` | time, identity, time/identity fields |
| `output_landscape_init.f90:610` | `2303` | time, identity, time/identity fields |
| `output_landscape_init.f90:616` | `2307` | time, identity, time/identity fields |
| `output_landscape_init.f90:638` | `2440` | time, identity, time/identity fields |
| `output_landscape_init.f90:644` | `2444` | time, identity, time/identity fields |
| `output_landscape_init.f90:653` | `2441` | time, identity, time/identity fields |
| `output_landscape_init.f90:659` | `2445` | time, identity, time/identity fields |
| `output_landscape_init.f90:668` | `2442` | time, identity, time/identity fields |
| `output_landscape_init.f90:674` | `2446` | time, identity, time/identity fields |
| `output_landscape_init.f90:683` | `2443` | time, identity, time/identity fields |
| `output_landscape_init.f90:689` | `2447` | time, identity, time/identity fields |
| `output_landscape_init.f90:700` | `2460` | time, identity, time/identity fields |
| `output_landscape_init.f90:706` | `2464` | time, identity, time/identity fields |
| `output_landscape_init.f90:715` | `2461` | time, identity, time/identity fields |
| `output_landscape_init.f90:721` | `2465` | time, identity, time/identity fields |
| `output_landscape_init.f90:730` | `2462` | time, identity, time/identity fields |
| `output_landscape_init.f90:736` | `2466` | time, identity, time/identity fields |
| `output_landscape_init.f90:745` | `2463` | time, identity, time/identity fields |
| `output_landscape_init.f90:751` | `2467` | time, identity, time/identity fields |
| `output_landscape_init.f90:763` | `2140` | time, identity, time/identity fields |
| `output_landscape_init.f90:769` | `2144` | time, identity, time/identity fields |
| `output_landscape_init.f90:779` | `2141` | time, identity, time/identity fields |
| `output_landscape_init.f90:785` | `2145` | time, identity, time/identity fields |
| `output_landscape_init.f90:795` | `2142` | time, identity, time/identity fields |
| `output_landscape_init.f90:801` | `2146` | time, identity, time/identity fields |
| `output_landscape_init.f90:811` | `2143` | time, identity, time/identity fields |
| `output_landscape_init.f90:817` | `2147` | time, identity, time/identity fields |
| `output_landscape_init.f90:827` | `2150` | time, identity, time/identity fields |
| `output_landscape_init.f90:833` | `2154` | time, identity, time/identity fields |
| `output_landscape_init.f90:842` | `2151` | time, identity, time/identity fields |
| `output_landscape_init.f90:848` | `2155` | time, identity, time/identity fields |
| `output_landscape_init.f90:857` | `2152` | time, identity, time/identity fields |
| `output_landscape_init.f90:863` | `2156` | time, identity, time/identity fields |
| `output_landscape_init.f90:872` | `2153` | time, identity, time/identity fields |
| `output_landscape_init.f90:878` | `2157` | time, identity, time/identity fields |
| `output_landscape_init.f90:888` | `2160` | time, identity, time/identity fields |
| `output_landscape_init.f90:894` | `2164` | time, identity, time/identity fields |
| `output_landscape_init.f90:903` | `2161` | time, identity, time/identity fields |
| `output_landscape_init.f90:909` | `2165` | time, identity, time/identity fields |
| `output_landscape_init.f90:918` | `2162` | time, identity, time/identity fields |
| `output_landscape_init.f90:924` | `2166` | time, identity, time/identity fields |
| `output_landscape_init.f90:933` | `2163` | time, identity, time/identity fields |
| `output_landscape_init.f90:939` | `2167` | time, identity, time/identity fields |
| `output_landscape_init.f90:949` | `2170` | time, identity, time/identity fields |
| `output_landscape_init.f90:955` | `2174` | time, identity, time/identity fields |
| `output_landscape_init.f90:965` | `2171` | time, identity, time/identity fields |
| `output_landscape_init.f90:971` | `2175` | time, identity, time/identity fields |
| `output_landscape_init.f90:980` | `2172` | time, identity, time/identity fields |
| `output_landscape_init.f90:986` | `2176` | time, identity, time/identity fields |
| `output_landscape_init.f90:995` | `2173` | time, identity, time/identity fields |
| `output_landscape_init.f90:1001` | `2177` | time, identity, time/identity fields |
| `output_landscape_init.f90:1012` | `2050` | time, identity, time/identity fields |
| `output_landscape_init.f90:1018` | `2054` | time, identity, time/identity fields |
| `output_landscape_init.f90:1027` | `2051` | time, identity, time/identity fields |
| `output_landscape_init.f90:1033` | `2055` | time, identity, time/identity fields |
| `output_landscape_init.f90:1042` | `2052` | time, identity, time/identity fields |
| `output_landscape_init.f90:1048` | `2056` | time, identity, time/identity fields |
| `output_landscape_init.f90:1057` | `2053` | time, identity, time/identity fields |
| `output_landscape_init.f90:1063` | `2057` | time, identity, time/identity fields |
| `output_landscape_init.f90:1073` | `2060` | time, identity, time/identity fields |
| `output_landscape_init.f90:1079` | `2064` | time, identity, time/identity fields |
| `output_landscape_init.f90:1088` | `2061` | time, identity, time/identity fields |
| `output_landscape_init.f90:1094` | `2065` | time, identity, time/identity fields |
| `output_landscape_init.f90:1103` | `2062` | time, identity, time/identity fields |
| `output_landscape_init.f90:1109` | `2066` | time, identity, time/identity fields |
| `output_landscape_init.f90:1118` | `2063` | time, identity, time/identity fields |
| `output_landscape_init.f90:1124` | `2067` | time, identity, time/identity fields |
| `output_landscape_init.f90:1134` | `2070` | time, identity, time/identity fields |
| `output_landscape_init.f90:1140` | `2074` | time, identity, time/identity fields |
| `output_landscape_init.f90:1149` | `2071` | time, identity, time/identity fields |
| `output_landscape_init.f90:1155` | `2075` | time, identity, time/identity fields |
| `output_landscape_init.f90:1164` | `2072` | time, identity, time/identity fields |
| `output_landscape_init.f90:1170` | `2076` | time, identity, time/identity fields |
| `output_landscape_init.f90:1179` | `2073` | time, identity, time/identity fields |
| `output_landscape_init.f90:1185` | `2077` | time, identity, time/identity fields |
| `output_landscape_init.f90:1195` | `2080` | time, identity, time/identity fields |
| `output_landscape_init.f90:1201` | `2084` | time, identity, time/identity fields |
| `output_landscape_init.f90:1210` | `2081` | time, identity, time/identity fields |
| `output_landscape_init.f90:1216` | `2085` | time, identity, time/identity fields |
| `output_landscape_init.f90:1225` | `2082` | time, identity, time/identity fields |
| `output_landscape_init.f90:1231` | `2086` | time, identity, time/identity fields |
| `output_landscape_init.f90:1240` | `2083` | time, identity, time/identity fields |
| `output_landscape_init.f90:1246` | `2087` | time, identity, time/identity fields |
| `output_landscape_init.f90:1257` | `4010` | time, identity, time/identity fields |
| `output_landscape_init.f90:1262` | `4011` | time, identity, time/identity fields |
| `output_landscape_init.f90:1271` | `4008` | time, identity, time/identity fields |
| `output_landscape_init.f90:1276` | `4009` | time, identity, time/identity fields |
| `output_landscape_init.f90:1294` | `4750` | time, identity, time/identity fields |
| `output_landscape_init.f90:1300` | `4754` | time, identity, time/identity fields |
| `output_landscape_init.f90:1308` | `4751` | time, identity, time/identity fields |
| `output_landscape_init.f90:1314` | `4755` | time, identity, time/identity fields |
| `output_landscape_init.f90:1322` | `4752` | time, identity, time/identity fields |
| `output_landscape_init.f90:1328` | `4756` | time, identity, time/identity fields |
| `output_landscape_init.f90:1336` | `4753` | time, identity, time/identity fields |
| `output_landscape_init.f90:1342` | `4757` | time, identity, time/identity fields |
| `output_landscape_init.f90:1352` | `4758` | time, identity, time/identity fields |
| `output_landscape_init.f90:1358` | `4762` | time, identity, time/identity fields |
| `output_landscape_init.f90:1366` | `4759` | time, identity, time/identity fields |
| `output_landscape_init.f90:1372` | `4763` | time, identity, time/identity fields |
| `output_landscape_init.f90:1380` | `4760` | time, identity, time/identity fields |
| `output_landscape_init.f90:1386` | `4764` | time, identity, time/identity fields |
| `output_landscape_init.f90:1394` | `4761` | time, identity, time/identity fields |
| `output_landscape_init.f90:1400` | `4765` | time, identity, time/identity fields |
| `output_landscape_init.f90:1410` | `4766` | time, identity, time/identity fields |
| `output_landscape_init.f90:1415` | `4770` | time, identity, time/identity fields |
| `output_landscape_init.f90:1422` | `4767` | time, identity, time/identity fields |
| `output_landscape_init.f90:1427` | `4771` | time, identity, time/identity fields |
| `output_landscape_init.f90:1434` | `4768` | time, identity, time/identity fields |
| `output_landscape_init.f90:1439` | `4772` | time, identity, time/identity fields |
| `output_landscape_init.f90:1446` | `4769` | time, identity, time/identity fields |
| `output_landscape_init.f90:1451` | `4773` | time, identity, time/identity fields |

Header and file-open statements are in `output_landscape_init`.

## Review Notes

- Every frequency shares the `output_waterbal_header` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `output_waterbal_header` type definition in `output_landscape_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Header / opener: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Data type: `output_landscape_module::output_waterbal_header`

## Evidence Used

- `output_landscape_init.f90`
- `output_landscape_init.f90`
- `output_landscape_module.f90` (`type output_waterbal_header`)
