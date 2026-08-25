---
kind: output_family
source_symbols:
- lsu_carbon_output
- output_landscape_init
title: lsu_scf_*
status: filled
source_hash: d907d73d00a39590
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`output_landscape_init`](../procedures/output_landscape_init.md)  
**Written by:** [`lsu_carbon_output`](../procedures/lsu_carbon_output.md)  
**Primary data type:** `carbon_module::carbon_soil_gain_losses`  
**Files covered:** `lsu_scf_day`, `lsu_scf_mon`, `lsu_scf_yr`, `lsu_scf_aa` text/CSV pairs

## Bottom Line

`lsu_scf_*` is the `lsu_scf` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `carbon_soil_gain_losses` state object written by `lsu_carbon_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `lsu_scf` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `lsu_scf_day.txt` | `lsu_scf_day.csv` | 4758 | 4762 | `output_landscape_init.f90:1351` |
| Monthly | `lsu_scf_mon.txt` | `lsu_scf_mon.csv` | 4759 | 4763 | `output_landscape_init.f90:1365` |
| Yearly | `lsu_scf_yr.txt` | `lsu_scf_yr.csv` | 4760 | 4764 | `output_landscape_init.f90:1379` |
| Average annual | `lsu_scf_aa.txt` | `lsu_scf_aa.csv` | 4761 | 4765 | `output_landscape_init.f90:1393` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `do ilsu = 1, db_mx%lsu_out  →  if (pco%cb_trf_lsu%d == "y") then` | `output_landscape_init.f90:1351` |
| Monthly | `do ilsu = 1, db_mx%lsu_out  →  if (time%end_mo == 1) then  →  if (pco%cb_trf_lsu` | `output_landscape_init.f90:1365` |
| Yearly | `do ilsu = 1, db_mx%lsu_out  →  if (time%end_yr == 1) then  →  if (pco%cb_trf_lsu` | `output_landscape_init.f90:1379` |
| Average annual | `do ilsu = 1, db_mx%lsu_out  →  if (time%end_sim == 1) then  →  if (pco%cb_gl_lsu` | `output_landscape_init.f90:1393` |

The header and units rows for every file are written by `output_landscape_init`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `db_mx%lsu_out` | All files | Open/print guard. |
| `do ilsu = 1, db_mx%lsu_out` | All files | Open/print guard. |
| `pco%cb_gl_hru%a == "y"` | All files | Enables output for this frequency. |
| `pco%cb_gl_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%cb_gl_hru%m == "y"` | All files | Enables output for this frequency. |
| `pco%cb_gl_hru%y == "y"` | All files | Enables output for this frequency. |
| `pco%cb_gl_lsu%a == "y" .or. pco%cb_trf_lsu%a == "y" .or. pco%cb_plt_lsu%a == "y"` | aa | Enables output for this frequency. |
| `pco%cb_trf_hru%a == "y"` | All files | Enables output for this frequency. |
| `pco%cb_trf_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%cb_trf_hru%m == "y"` | All files | Enables output for this frequency. |
| `pco%cb_trf_hru%y == "y"` | All files | Enables output for this frequency. |
| `pco%cb_trf_lsu%a == "y"` | aa | Enables output for this frequency. |
| `pco%cb_trf_lsu%d == "y"` | day | Enables output for this frequency. |
| `pco%cb_trf_lsu%m == "y"` | mon | Enables output for this frequency. |
| `pco%cb_trf_lsu%y == "y"` | yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%ls_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%ls_bsn%y == "y"` | All files | Enables output for this frequency. |
| `pco%ls_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%ls_hru%m == "y"` | All files | Enables output for this frequency. |
| `pco%ls_hru%y == "y"` | All files | Enables output for this frequency. |
| `pco%ls_lsu%d == "y"` | All files | Enables output for this frequency. |
| `pco%ls_sd%d == "y"` | All files | Enables output for this frequency. |
| `pco%ls_sd%y == "y"` | All files | Enables output for this frequency. |
| `pco%nb_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%nb_bsn%y == "y"` | All files | Enables output for this frequency. |
| `pco%nb_hru%a == "y"` | All files | Enables output for this frequency. |
| `pco%nb_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%nb_hru%m == "y"` | All files | Enables output for this frequency. |
| `pco%nb_hru%y == "y"` | All files | Enables output for this frequency. |
| `pco%nb_lsu%d == "y"` | All files | Enables output for this frequency. |
| `pco%nb_lsu%y == "y"` | All files | Enables output for this frequency. |
| `pco%pw_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%pw_bsn%y == "y"` | All files | Enables output for this frequency. |
| `pco%pw_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%pw_hru%m == "y"` | All files | Enables output for this frequency. |
| `pco%pw_hru%y == "y"` | All files | Enables output for this frequency. |
| `pco%pw_sd%d == "y"` | All files | Enables output for this frequency. |
| `pco%pw_sd%y == "y"` | All files | Enables output for this frequency. |
| `pco%wb_bsn%d == "y"` | All files | Enables output for this frequency. |
| `pco%wb_bsn%y == "y"` | All files | Enables output for this frequency. |
| `pco%wb_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%wb_hru%y == "y"` | All files | Enables output for this frequency. |
| `pco%wb_lsu%d == "y"` | All files | Enables output for this frequency. |
| `pco%wb_sd%d == "y"` | All files | Enables output for this frequency. |
| `sp_ob%hru` | All files | Open/print guard. |
| `sp_ob%hru_lte` | All files | Open/print guard. |
| `sp_ob%ru` | All files | Open/print guard. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1` | aa | Builds and writes rows at simulation end. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `output_landscape_init` | Basin name and program string. |
| Header row | `output_landscape_init` | Column names for the time, identity, and `carbon_soil_gain_losses` values. |
| Units row | `output_landscape_init` | Units for the value columns. |
| Data row | `lsu_carbon_output` | One `carbon_soil_gain_losses` record for the active frequency. |

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
| `sed_c` | kg C/ha | `lsc_d%sed_c` | C transported with sediment yield |
| `surq_c` | kg C/ha | `lsc_d%surq_c` | total dissolved C transported with surface runoff |
| `latq_c` | kg C/ha | `lsc_d%latq_c` | dissolved organic C transported with lateral flow (all layers) |
| `perc_c` | kg C/ha | `lsc_d%perc_c` | total dissolved C transported with percolate |
| `rsd_decay_c` | kg C/ha | `lsc_d%rsd_decay_c` | carbon added to soil from residue decay |
| `man_app_c` | kg C/ha | `lsc_d%man_app_c` | amount of carbon applied to soil from manure |
| `man_graz_c` | kg C/ha | `lsc_d%man_graz_c` | amount of carbon manure from grazing animals |
| `rsp_c` | kg C/ha | `lsc_d%rsp_c` | CO2 production from soil respiration summarized for the profile |
| `emit_c` | kg C/ha | `lsc_d%emit_c` | CO2 production from burning soil carbon |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`lsc_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `carbon_soil_gain_losses` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `lsu_carbon_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`lsu_carbon_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `carbon_soil_gain_losses` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `lsu_carbon_output.f90:66` | `4750` | time, identity, `lsc_d(idx)` record |
| `lsu_carbon_output.f90:67` | `4754` | time, identity, `lsc_d(idx)` record |
| `lsu_carbon_output.f90:70` | `4758` | time, identity, `lscf_d(idx)` record |
| `lsu_carbon_output.f90:71` | `4762` | time, identity, `lscf_d(idx)` record |
| `lsu_carbon_output.f90:74` | `4766` | time, identity, time/identity fields |
| `lsu_carbon_output.f90:75` | `4770` | time, identity, time/identity fields |
| `lsu_carbon_output.f90:86` | `4751` | time, identity, `lsc_m(idx)` record |
| `lsu_carbon_output.f90:87` | `4755` | time, identity, `lsc_m(idx)` record |
| `lsu_carbon_output.f90:90` | `4759` | time, identity, `lscf_m(idx)` record |
| `lsu_carbon_output.f90:91` | `4763` | time, identity, `lscf_m(idx)` record |
| `lsu_carbon_output.f90:94` | `4767` | time, identity, time/identity fields |
| `lsu_carbon_output.f90:95` | `4771` | time, identity, time/identity fields |
| `lsu_carbon_output.f90:112` | `4752` | time, identity, `lsc_y(idx)` record |
| `lsu_carbon_output.f90:113` | `4756` | time, identity, `lsc_y(idx)` record |
| `lsu_carbon_output.f90:116` | `4760` | time, identity, `lscf_y(idx)` record |
| `lsu_carbon_output.f90:117` | `4764` | time, identity, `lscf_y(idx)` record |
| `lsu_carbon_output.f90:120` | `4768` | time, identity, time/identity fields |
| `lsu_carbon_output.f90:121` | `4772` | time, identity, time/identity fields |
| `lsu_carbon_output.f90:138` | `4753` | time, identity, `lsc_a(idx)` record |
| `lsu_carbon_output.f90:139` | `4757` | time, identity, `lsc_a(idx)` record |
| `lsu_carbon_output.f90:142` | `4761` | time, identity, `lscf_a(idx)` record |
| `lsu_carbon_output.f90:143` | `4765` | time, identity, `lscf_a(idx)` record |
| `lsu_carbon_output.f90:146` | `4769` | time, identity, time/identity fields |
| `lsu_carbon_output.f90:147` | `4773` | time, identity, time/identity fields |

Header and file-open statements are in `output_landscape_init`.

## Review Notes

- Every frequency shares the `carbon_soil_gain_losses` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `carbon_soil_gain_losses` type definition in `carbon_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`lsu_carbon_output`](../procedures/lsu_carbon_output.md)
- Header / opener: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Data type: `carbon_module::carbon_soil_gain_losses`

## Evidence Used

- `lsu_carbon_output.f90`
- `output_landscape_init.f90`
- `carbon_module.f90` (`type carbon_soil_gain_losses`)
