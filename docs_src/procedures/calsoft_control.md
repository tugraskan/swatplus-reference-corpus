---
kind: procedure
symbol: calsoft_control
title: calsoft_control
status: filled
source_hash: 6e616ccaa350400e
version_label: SWAT+ 62.0.0
locals:
  ireg: Calibration-region counter.
  ilum: Land-use counter within a region.
  icvmax: Local counter/scalar used in the calibration dispatch (`icvmax`).
  nyskip: Saved value of `pco%nyskip` (years to skip) restored after enabling output.
  ihru: Local counter/scalar used in the calibration dispatch (`ihru`).
  isdh: Local counter/scalar used in the calibration dispatch (`isdh`).
  idb: Local counter/scalar used in the calibration dispatch (`idb`).
  iord: Local counter/scalar used in the calibration dispatch (`iord`).
uses:
  sd_channel_module: Provides the calibration data structures, print control (`pco`), and
    the measured targets this dispatcher sets up.
  hru_lte_module: Provides the calibration data structures, print control (`pco`), and the
    measured targets this dispatcher sets up.
  maximum_data_module: Provides the calibration data structures, print control (`pco`), and
    the measured targets this dispatcher sets up.
  calibration_data_module: Provides the calibration data structures, print control (`pco`),
    and the measured targets this dispatcher sets up.
  time_module: Provides the calibration data structures, print control (`pco`), and the measured
    targets this dispatcher sets up.
  basin_module: Provides the calibration data structures, print control (`pco`), and the measured
    targets this dispatcher sets up.
  hru_module: Provides the calibration data structures, print control (`pco`), and the measured
    targets this dispatcher sets up.
  hydrograph_module: Provides the calibration data structures, print control (`pco`), and
    the measured targets this dispatcher sets up.
  soil_module: Provides the calibration data structures, print control (`pco`), and the measured
    targets this dispatcher sets up.
---

<!-- facts:header -->

Top-level soft-calibration dispatcher. It enables basin water-balance averaging, scales the measured calibration targets from ratios to depths, and calls each calibration stage (water balance, before-flow-regime, temporal, plant, sediment) that is turned on.

## Bottom Line

`calsoft_control` drives the soft-calibration sequence. It turns on the basin average water-balance output, preserves `pco%nyskip`, and for each enabled calibration type scales the measured targets (`%meas%srr/lfr/pcr/etr/tfr`) by average-annual precipitation to convert input ratios to depths.

It then calls the matching calibration routine (`calsoft_hyd`, `calsoft_hyd_bfr`, `caltsoft_hyd`, `calsoft_plant`, `calsoft_sed`) and finally writes the calibrated parameters via `pl_write_parms_cal`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Runs once before the production simulation when soft calibration is enabled. It is the entry point for the calsoft family: it sets up calibration output/targets and invokes each calibration stage, which in turn re-run the model via `time_control`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select output conditions | Enables calibration output, scales measured targets to depths, and calls each enabled calibration stage; finally writes calibrated parameters. |
| 2. Loop over output items | Enables calibration output, scales measured targets to depths, and calls each enabled calibration stage; finally writes calibrated parameters. |
| 3. Write output records | Enables calibration output, scales measured targets to depths, and calls each enabled calibration stage; finally writes calibrated parameters. |
| 4. Update output state | Enables calibration output, scales measured targets to depths, and calls each enabled calibration stage; finally writes calibrated parameters. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:hru_lte_module] | `hlt, hlt_db` | `hlt(isdh)%props, hlt(isdh)%name, hlt_db(idb)%dakm2, hlt(isdh)%cn2, hlt(isdh)%cn3_swf, hlt_db(idb)%tc, hlt_db(idb)%soildep, hlt(isdh)%perco, hlt_db(isdh)%slope, hlt_db(idb)%slopelen, hlt(isdh)%etco, hlt_db(idb)%sy, hlt_db(idb)%abf, hlt(idb)%revapc, hlt_db(idb)%percc, hlt_db(idb)%sw, hlt_db(idb)%gw, hlt_db(idb)%gwflow, hlt_db(idb)%gwdeep, hlt_db(idb)%snow, hlt_db(idb)%xlat, hlt_db(idb)%text, hlt_db(idb)%tropical, hlt_db(idb)%igrow1, hlt_db(idb)%igrow2, hlt_db(idb)%plant, hlt(isdh)%stress, hlt_db(idb)%ipet, hlt_db(idb)%irr, hlt_db(idb)%irrsrc, hlt_db(idb)%tdrain, hlt_db(idb)%uslek, hlt_db(idb)%uslec, hlt_db(idb)%uslep, hlt_db(idb)%uslels` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_reg, db_mx%ch_reg` |
| [sym:calibration_data_module] | `cal_codes, region, lscal, lscalt, chcal, ch_prms` | `cal_codes%hyd_hru, region(ireg)%nlum, lscal(ireg)%lum(ilum)%meas%srr, lscal(ireg)%lum(ilum)%precip_aa_sav, lscal(ireg)%lum(ilum)%meas%lfr, lscal(ireg)%lum(ilum)%meas%pcr, lscal(ireg)%lum(ilum)%meas%etr, lscal(ireg)%lum(ilum)%meas%tfr, cal_codes%hyd_hrul, lscalt(ireg)%lum_num, lscalt(ireg)%lum(ilum)%meas%srr, lscalt(ireg)%lum(ilum)%precip_aa_sav, lscalt(ireg)%lum(ilum)%meas%lfr, lscalt(ireg)%lum(ilum)%meas%pcr, lscalt(ireg)%lum(ilum)%meas%etr, lscalt(ireg)%lum(ilum)%meas%tfr, cal_codes%plt, cal_codes%sed, cal_codes%chsed, chcal(ireg)%ord_num, chcal(ireg)%ord(iord)%aa%chw, ch_prms(1)%name, ch_prms(1)%chg_typ, chcal(ireg)%ord(iord)%prm%erod` |
| [sym:time_module] | `no resolved imported state` |  |
| [sym:basin_module] | `pco` | `pco%nyskip, pco%wb_bsn%a` |
| [sym:hru_module] | `hru` | `hru(ihru)%hyd` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru_lte, sp_ob%hru` |
| [sym:soil_module] | `no resolved imported state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pco` | At entry. | The print-control structure is updated to enable the basin water-balance average output needed for calibration. |
| `pco%wb_bsn%a` | At entry. | Enables basin water-balance average-annual output (`pco%wb_bsn%a = "y"`) so calibration statistics are produced. |
| `pco%nyskip` | At entry (saved and restored). | The skip-years setting is saved and restored around enabling calibration output. |
| `lscal(ireg)%lum(ilum)%meas%srr` | When the calibration type is enabled, before running it. | Converts the measured surface-runoff target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscal(ireg)%lum(ilum)%meas%lfr` | When the calibration type is enabled, before running it. | Converts the measured lateral-flow target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscal(ireg)%lum(ilum)%meas%pcr` | When the calibration type is enabled, before running it. | Converts the measured percolation target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscal(ireg)%lum(ilum)%meas%etr` | When the calibration type is enabled, before running it. | Converts the measured ET target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscal(ireg)%lum(ilum)%meas%tfr` | When the calibration type is enabled, before running it. | Converts the measured total-flow target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscalt(ireg)%lum(ilum)%meas%srr` | When the calibration type is enabled, before running it. | Converts the measured LTE surface-runoff target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscalt(ireg)%lum(ilum)%meas%lfr` | When the calibration type is enabled, before running it. | Converts the measured LTE lateral-flow target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscalt(ireg)%lum(ilum)%meas%pcr` | When the calibration type is enabled, before running it. | Converts the measured LTE percolation target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscalt(ireg)%lum(ilum)%meas%etr` | When the calibration type is enabled, before running it. | Converts the measured LTE ET target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |
| `lscalt(ireg)%lum(ilum)%meas%tfr` | When the calibration type is enabled, before running it. | Converts the measured LTE total-flow target from a ratio to a depth by scaling with average-annual precipitation (`* precip_aa_sav`). |

## File I/O

<!-- facts:io -->


## Lineage

`calsoft_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `calsoft_control.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `fd90e36` (2025-02-06) — variable initialization changes
- `dab22e1` (2024-10-08) — Remove unused format labels in Fortran source files
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'calsoft_control' has no extracted documentation comment.
- Top-level soft-calibration dispatcher; state changes are print-control setup and measured-target scaling. 3 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
