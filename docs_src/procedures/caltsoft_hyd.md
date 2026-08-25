---
kind: procedure
symbol: caltsoft_hyd
title: caltsoft_hyd
status: filled
source_hash: b82a68730d113a3e
version_label: SWAT+ 62.0.0
locals:
  iter_all: Outer calibration-iteration count.
  iterall: Outer calibration-iteration counter.
  isim: 'Flag: 1 if any parameter was adjusted (so a re-run is needed).'
  ireg: Calibration-region counter.
  ilum: Land-use counter within a region.
  iihru: HRU index within a region.
  icn: Curve-number iteration counter.
  ihru_s: HRU sequence counter within a region.
  iter_ind: Inner iteration limit.
  ietco: ET-adjustment iteration counter.
  ik: Iteration counter.
  iperco: Percolation-adjustment iteration counter.
  rmeas: Measured target value.
  denom: Denominator for a ratio/difference.
  soft: Measured (soft) target, scaled to a depth.
  diff: Relative difference between measured and simulated.
  chg_val: Computed parameter increment.
  qn1: Local counter/scalar used in the calibration loop (`qn1`).
  qn3: Local counter/scalar used in the calibration loop (`qn3`).
  s3: Local counter/scalar used in the calibration loop (`s3`).
  rto3: Local counter/scalar used in the calibration loop (`rto3`).
  rtos: Local counter/scalar used in the calibration loop (`rtos`).
  sumul: Local counter/scalar used in the calibration loop (`sumul`).
  sumfc: Local counter/scalar used in the calibration loop (`sumfc`).
uses:
  hydrograph_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
  ru_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
  aquifer_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
  hru_lte_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
  sd_channel_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
  basin_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
  maximum_data_module: Provides the calibration data structures and HRU/region parameters
    that this routine reads and adjusts.
  calibration_data_module: Provides the calibration data structures and HRU/region parameters
    that this routine reads and adjusts.
  conditional_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
  reservoir_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
---

<!-- facts:header -->

Temporally soft-calibrates the water balance for low-resolution (LTE) HRUs by adjusting curve number, ET, and percolation parameters to match measured ratios.

## Bottom Line

`caltsoft_hyd` is the temporal hydrology soft-calibration for low-resolution (LTE) HRUs. It compares simulated vs measured surface-runoff, ET, and percolation statistics per region/land use and adjusts the LTE HRU curve number (`cn`), ET (`etco`), and percolation (`perco`) parameters.

Adjusted parameters are applied to the LTE HRUs (`hlt`), and the model is re-run via `time_control` until convergence.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Part of the soft/hard calibration sequence (driven by `calsoft_control`/`calsoft_hyd_bfr`). It adjusts parameters to calibrate temporal water balance (LTE HRUs), re-initializes objects, and re-runs the model via `time_control`. It runs only when calibration is enabled, before the production simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select output conditions | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |
| 2. Loop over output items | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |
| 3. Write output records | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |
| 4. Update output state | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `no resolved imported state` |  |
| [sym:ru_module] | `no resolved imported state` |  |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:hru_lte_module] | `hlt, hlt_init` | `hlt(iihru)%cn2, hlt(iihru)%smx, hlt(iihru)%por, hlt(iihru)%awc, hlt(iihru)%cn3_swf, hlt(iihru)%wrt2, hlt(iihru)%etco, hlt(iihru)%perco, hlt(iihru)%revapc, hlt_init(iihru)%revapc` |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:basin_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_reg, db_mx%plcal_reg` |
| [sym:calibration_data_module] | `lscalt, ls_prms, region, plcal, cal_codes` | `lscalt(ireg)%lum_num, lscalt(ireg)%lum(ilum)%meas%srr, lscalt(ireg)%lum(ilum)%precip_aa, lscalt(ireg)%lum(ilum)%ha, lscalt(ireg)%lum(ilum)%prm_lim%cn, lscalt(ireg)%lum(ilum)%prm_prev, lscalt(ireg)%lum(ilum)%prm, lscalt(ireg)%lum(ilum)%prev, lscalt(ireg)%lum(ilum)%aa, lscalt(ireg)%lum(ilum)%aa%srr, lscalt(ireg)%lum(ilum)%prm_prev%cn, lscalt(ireg)%lum(ilum)%prm%cn, lscalt(ireg)%lum(ilum)%prev%srr, ls_prms(1)%pos, ls_prms(1)%neg, region(ireg)%num_tot, region(ireg)%num(ihru_s), ls_prms(1)%up, ls_prms(1)%lo, lscalt(ireg)%lum(ilum)%nbyr, plcal(ireg)%lum_num, plcal(ireg)%lum(ilum)%nbyr, plcal(ireg)%lum(ilum)%precip_aa, plcal(ireg)%lum(ilum)%aa, lscalt(ireg)%lum(ilum)%meas%etr, lscalt(ireg)%lum(ilum)%prm_lim%etco, lscalt(ireg)%lum(ilum)%aa%etr, lscalt(ireg)%lum(ilum)%prm_prev%etco, lscalt(ireg)%lum(ilum)%prm%etco, lscalt(ireg)%lum(ilum)%prev%etr, ls_prms(7)%pos, ls_prms(7)%neg, ls_prms(7)%up, ls_prms(7)%lo, lscalt(ireg)%lum(ilum)%meas%pcr, lscalt(ireg)%lum(ilum)%prm_lim%perco, lscalt(ireg)%lum(ilum)%aa%pcr, lscalt(ireg)%lum(ilum)%prm_prev%perco, lscalt(ireg)%lum(ilum)%prm%perco, lscalt(ireg)%lum(ilum)%prev%pcr, ls_prms(8)%pos, ls_prms(8)%neg, ls_prms(8)%up, ls_prms(8)%lo, lscalt(ireg)%lum(ilum)%meas%lfr, lscalt(ireg)%lum(ilum)%prm_lim%revapc, lscalt(ireg)%lum(ilum)%aa%lfr, lscalt(ireg)%lum(ilum)%prm_prev%revapc, lscalt(ireg)%lum(ilum)%prm%revapc, lscalt(ireg)%lum(ilum)%prev%lfr, ls_prms(9)%pos, ls_prms(9)%neg, ls_prms(9)%up, ls_prms(9)%lo, lscalt(ireg)%lum(ilum)%prm_lim%cn3_swf, lscalt(ireg)%lum(ilum)%prm_prev%cn3_swf, lscalt(ireg)%lum(ilum)%prm%cn3_swf, ls_prms(10)%pos, ls_prms(10)%neg, ls_prms(10)%up, ls_prms(10)%lo, cal_codes%hyd_hru` |
| [sym:conditional_module] | `no resolved imported state` |  |
| [sym:reservoir_module] | `no resolved imported state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lscalt(ireg)%lum(ilum)%prm_prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous parameter set before this adjustment so it can be restored or compared. |
| `lscalt(ireg)%lum(ilum)%prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous statistics before this adjustment so it can be restored or compared. |
| `lscalt(ireg)%lum(ilum)%prm_prev%cn` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the curve number before adjustment. |
| `lscalt(ireg)%lum(ilum)%prm%cn` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the curve number for the calibration unit by the computed increment (clamped to its limits). |
| `lscalt(ireg)%lum(ilum)%prev%srr` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous simulated surface-runoff ratio for the calibration unit. |
| `lscalt(ireg)%lum(ilum)%prm_lim%cn` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the curve number has hit its calibration limit, so it is no longer adjusted. |
| `hlt(iihru)` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the hlt(iihru) on the HRU to the calibrated value (clamped to bounds). |
| `hlt(iihru)%cn2` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the curve number (CN2) on the HRU to the calibrated value (clamped to bounds). |
| `hlt(iihru)%smx` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the retention parameter on the HRU to the calibrated value (clamped to bounds). |
| `hlt_init(iihru)` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy hlt_init(iihru) on the HRU to the calibrated value (clamped to bounds). |
| `lscalt(ireg)%lum(ilum)%nbyr` | After applying an adjustment, before re-running. | Resets the calibration unit's simulated-year counter so fresh averages accumulate on the re-run. |
| `lscalt(ireg)%lum(ilum)%precip_aa` | After applying an adjustment, before re-running. | Resets the accumulated average-annual precipitation for the calibration unit. |
| `lscalt(ireg)%lum(ilum)%aa` | After applying an adjustment, before re-running. | Resets the calibration unit's average-annual simulated statistics to zero. |
| `plcal(ireg)%lum(ilum)%nbyr` | After applying an adjustment, before re-running. | Resets the calibration unit's simulated-year counter so fresh averages accumulate on the re-run. |
| `plcal(ireg)%lum(ilum)%precip_aa` | After applying an adjustment, before re-running. | Resets the accumulated average-annual precipitation for the calibration unit. |
| `plcal(ireg)%lum(ilum)%aa` | After applying an adjustment, before re-running. | Resets the calibration unit's average-annual simulated statistics to zero. |
| `lscalt(ireg)%lum(ilum)%prm_prev%etco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the ET soil-evaporation compensation factor (esco) before adjustment. |
| `lscalt(ireg)%lum(ilum)%prm%etco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the ET soil-evaporation compensation factor (esco) for the calibration unit by the computed increment (clamped to its limits). |
| `lscalt(ireg)%lum(ilum)%prev%etr` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous simulated ET ratio for the calibration unit. |
| `lscalt(ireg)%lum(ilum)%prm_lim%etco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the ET soil-evaporation compensation factor (esco) has hit its calibration limit, so it is no longer adjusted. |
| `hlt(iihru)%etco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the ET soil-evaporation compensation factor (esco) on the HRU to the calibrated value (clamped to bounds). |
| `lscalt(ireg)%lum(ilum)%prm_prev%perco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the percolation coefficient (baseflow) before adjustment. |
| `lscalt(ireg)%lum(ilum)%prm%perco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the percolation coefficient (baseflow) for the calibration unit by the computed increment (clamped to its limits). |
| `lscalt(ireg)%lum(ilum)%prev%pcr` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous simulated percolation ratio for the calibration unit. |

## File I/O

<!-- facts:io -->


## Lineage

`caltsoft_hyd.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `caltsoft_hyd.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'caltsoft_hyd' has no extracted documentation comment.
- Soft-calibration routine for temporal water balance (LTE HRUs): compares simulated vs measured statistics, adjusts parameters, and re-runs via time_control. 7 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
