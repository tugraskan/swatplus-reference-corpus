---
kind: output_family
source_symbols:
- hru_carbon_output
- output_landscape_init
title: hru_scf_*
status: filled
source_hash: 5fd463f409b997d5
version_label: SWAT+ 62.0.0
---

**Kind:** output family  
**Opened by:** [`output_landscape_init`](../procedures/output_landscape_init.md)  
**Written by:** [`hru_carbon_output`](../procedures/hru_carbon_output.md)  
**Primary data type:** `carbon_module::carbon_soil_gain_losses`  
**Files covered:** `hru_scf_day`, `hru_scf_mon`, `hru_scf_yr`, `hru_scf_aa` text/CSV pairs

## Bottom Line

`hru_scf_*` is the `hru_scf` time-series output family. Every file in it shares one record layout, so daily, monthly, yearly, and average-annual reporting are documented here on one page instead of on separate near-identical pages. Each row is one reported object for one period: it begins with time and object-identity fields, then expands a `carbon_soil_gain_losses` state object written by `hru_carbon_output`.

Only the file name, unit number, print condition, and source state object differ between frequencies; the columns are identical.

> **What each row means:** one object's `hru_scf` values for a single reporting period (daily, monthly, yearly, average annual). Every file in the family has the same columns — pick the one whose frequency matches the timestep you want.

## Output Family

| Frequency | Text File | CSV File | Text Unit | CSV Unit | Open Lines |
|---|---|---|---:|---:|---|
| Daily | `hru_scf_day.txt` | `hru_scf_day.csv` | 4550 | 4554 | `output_landscape_init.f90:289` |
| Monthly | `hru_scf_mon.txt` | `hru_scf_mon.csv` | 4551 | 4555 | `output_landscape_init.f90:304` |
| Yearly | `hru_scf_yr.txt` | `hru_scf_yr.csv` | 4552 | 4556 | `output_landscape_init.f90:319` |
| Average annual | `hru_scf_aa.txt` | `hru_scf_aa.csv` | 4553 | 4557 | `output_landscape_init.f90:334` |

## File Contracts

| Frequency | Open Condition | Open Lines |
|---|---|---|
| Daily | `if (pco%cb_trf_hru%d == "y") then` | `output_landscape_init.f90:289` |
| Monthly | `if (time%end_mo == 1) then  →  if (pco%cb_trf_hru%m == "y") then` | `output_landscape_init.f90:304` |
| Yearly | `if (time%end_yr == 1) then  →  if (pco%cb_trf_hru%y == "y") then` | `output_landscape_init.f90:319` |
| Average annual | `if (time%end_sim == 1) then  →  if (pco%cb_gl_hru%a == "y" .or. pco%cb_trf_hru%a` | `output_landscape_init.f90:334` |

The header and units rows for every file are written by `output_landscape_init`.

## Writer And Print Controls

| Control | Applies To | Meaning |
|---|---|---|
| `0` | All files | Open/print guard. |
| `pco%cb_gl_hru%a == "y"` | All files | Enables output for this frequency. |
| `pco%cb_gl_hru%a == "y" .or. pco%cb_trf_hru%a == "y"` | aa | Enables output for this frequency. |
| `pco%cb_gl_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%cb_gl_hru%m == "y"` | All files | Enables output for this frequency. |
| `pco%cb_gl_hru%y == "y"` | All files | Enables output for this frequency. |
| `pco%cb_trf_hru%a == "y"` | aa | Enables output for this frequency. |
| `pco%cb_trf_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%cb_trf_hru%m == "y"` | aa, mon, yr | Enables output for this frequency. |
| `pco%cb_trf_hru%y == "y"` | aa, yr | Enables output for this frequency. |
| `pco%csvout == "y"` | All files | Enables the CSV companion files. |
| `pco%nb_hru%a == "y"` | All files | Enables output for this frequency. |
| `pco%nb_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%nb_hru%m == "y"` | All files | Enables output for this frequency. |
| `pco%nb_hru%y == "y"` | All files | Enables output for this frequency. |
| `pco%wb_hru%d == "y"` | All files | Enables output for this frequency. |
| `pco%wb_hru%y == "y"` | All files | Enables output for this frequency. |
| `sp_ob%hru` | All files | Open/print guard. |
| `time%end_mo == 1` | mon | Builds and writes rows at month end. |
| `time%end_sim == 1` | aa | Builds and writes rows at simulation end. |
| `time%end_yr == 1` | yr | Builds and writes rows at year end. |

## Shared Record Layout

| Row Part | Written By | Contents |
|---|---|---|
| Title row | `output_landscape_init` | Basin name and program string. |
| Header row | `output_landscape_init` | Column names for the time, identity, and `carbon_soil_gain_losses` values. |
| Units row | `output_landscape_init` | Units for the value columns. |
| Data row | `hru_carbon_output` | One `carbon_soil_gain_losses` record for the active frequency. |

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
| `sed_c` | kg C/ha | `hsc_d%sed_c` | C transported with sediment yield |
| `surq_c` | kg C/ha | `hsc_d%surq_c` | total dissolved C transported with surface runoff |
| `latq_c` | kg C/ha | `hsc_d%latq_c` | dissolved organic C transported with lateral flow (all layers) |
| `perc_c` | kg C/ha | `hsc_d%perc_c` | total dissolved C transported with percolate |
| `rsd_decay_c` | kg C/ha | `hsc_d%rsd_decay_c` | carbon added to soil from residue decay |
| `man_app_c` | kg C/ha | `hsc_d%man_app_c` | amount of carbon applied to soil from manure |
| `man_graz_c` | kg C/ha | `hsc_d%man_graz_c` | amount of carbon manure from grazing animals |
| `rsp_c` | kg C/ha | `hsc_d%rsp_c` | CO2 production from soil respiration summarized for the profile |
| `emit_c` | kg C/ha | `hsc_d%emit_c` | CO2 production from burning soil carbon |

## Frequency-Specific Behavior

The columns are identical for every frequency (daily, monthly, yearly, average annual). What differs is only the file name, unit number, print flag, and the source state object (`hsc_d` for daily and its monthly/yearly/average-annual counterparts). See the Output Family and Writer And Print Controls tables above for the per-frequency file, unit, and trigger.

## Data Sources And Calculations

Each value column is the matching field of the `carbon_soil_gain_losses` state object. Daily rows are written from the per-timestep state; coarser frequencies are accumulated by `hru_carbon_output` from the finer state. Coarser frequencies accumulate the finer-frequency state; see the writer for whether each field is summed or averaged.

## Writer Flow

`hru_carbon_output` writes one record per reported object per active frequency:

1. Resolve the object's spatial index and, if the frequency's print flag is on, write the current `carbon_soil_gain_losses` state to the text file (and the CSV file when `pco%csvout == "y"`).
2. Accumulate the finer-frequency state into the coarser one.
3. At each period boundary (month/year/simulation end) write the accumulated record for that frequency.

## Line-Based I/O Trace

| Source Line | Unit | Writes |
|---|---|---|
| `hru_carbon_output.f90:34` | `4520` | time, identity, `hsc_d(idx)` record |
| `hru_carbon_output.f90:35` | `4524` | time, identity, `hsc_d(idx)` record |
| `hru_carbon_output.f90:38` | `4550` | time, identity, `hscf_d(idx)` record |
| `hru_carbon_output.f90:39` | `4554` | time, identity, `hscf_d(idx)` record |
| `hru_carbon_output.f90:50` | `4521` | time, identity, `hsc_m(idx)` record |
| `hru_carbon_output.f90:51` | `4525` | time, identity, `hsc_m(idx)` record |
| `hru_carbon_output.f90:54` | `4551` | time, identity, `hscf_m(idx)` record |
| `hru_carbon_output.f90:55` | `4555` | time, identity, `hscf_m(idx)` record |
| `hru_carbon_output.f90:71` | `4522` | time, identity, `hsc_y(idx)` record |
| `hru_carbon_output.f90:72` | `4526` | time, identity, `hsc_y(idx)` record |
| `hru_carbon_output.f90:75` | `4552` | time, identity, `hscf_y(idx)` record |
| `hru_carbon_output.f90:76` | `4556` | time, identity, `hscf_y(idx)` record |
| `hru_carbon_output.f90:93` | `4523` | time, identity, `hsc_a(idx)` record |
| `hru_carbon_output.f90:94` | `4527` | time, identity, `hsc_a(idx)` record |
| `hru_carbon_output.f90:97` | `4553` | time, identity, `hscf_a(idx)` record |
| `hru_carbon_output.f90:98` | `4557` | time, identity, `hscf_a(idx)` record |

Header and file-open statements are in `output_landscape_init`.

## Review Notes

- Every frequency shares the `carbon_soil_gain_losses` layout, so the Columns Written table applies to all files in the family.
- Column names, units, and meanings are taken verbatim from the `carbon_soil_gain_losses` type definition in `carbon_module`.
- The value columns and their order are auto-derived from the writer's output state type; the prose sections are generated from the writer/header source and may benefit from human review.

## Source Links

- Writer: [`hru_carbon_output`](../procedures/hru_carbon_output.md)
- Header / opener: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Data type: `carbon_module::carbon_soil_gain_losses`

## Evidence Used

- `hru_carbon_output.f90`
- `output_landscape_init.f90`
- `carbon_module.f90` (`type carbon_soil_gain_losses`)
