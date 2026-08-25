---
kind: procedure
symbol: calsoft_hyd
title: calsoft_hyd
status: filled
source_hash: cf48a1cf6f5cee7c
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
  perc_ln_func: Intermediate for the percolation-limit transform.
uses:
  hru_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
  soil_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
  plant_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
  hydrograph_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
  ru_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
  aquifer_module: Provides the calibration data structures and HRU/region parameters that
    this routine reads and adjusts.
  channel_module: Provides the calibration data structures and HRU/region parameters that
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
  organic_mineral_mass_module: Provides the calibration data structures and HRU/region parameters
    that this routine reads and adjusts.
  time_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
---

<!-- facts:header -->

Soft-calibrates the water balance by iteratively adjusting ET (esco), PET (pet_co), and surface-runoff (cn3_swf) parameters per region/land-use to match measured ratios.

## Bottom Line

`calsoft_hyd` is the hydrology soft-calibration driver. For each calibration region and land use it compares the simulated average-annual ET, PET, and surface-runoff statistics against the measured targets, and when the difference exceeds tolerance it nudges the matching parameter (esco, pet_co, cn3_swf), clamping to limits.

After each adjustment stage it pushes the new parameter onto every HRU in the region, re-initializes objects, and re-runs the model via `time_control`, iterating until the statistics converge or parameters hit their limits.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Part of the soft/hard calibration sequence (driven by `calsoft_control`/`calsoft_hyd_bfr`). It adjusts parameters to calibrate water balance (ET, PET, surface runoff), re-initializes objects, and re-runs the model via `time_control`. It runs only when calibration is enabled, before the production simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Iterate configured work | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |
| 2. Evaluate branch conditions | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |
| 3. Call model routines | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |
| 4. Update shared state | Iterates calibration regions/land uses, compares simulated vs measured statistics, adjusts the relevant parameter (clamped to limits), applies it to the region's HRUs, and re-runs the model. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, hru_init` | `hru(iihru)%lum_group_c, hru(iihru)%hyd%esco, hru_init(iihru)%hyd%esco, hru(iihru)%hyd%pet_co, hru_init(iihru)%hyd%pet_co, hru(iihru)%tiledrain, hru(iihru)%hyd%cn3_swf, hru_init(iihru)%hyd%cn3_swf, hru(iihru)%hyd%latq_co, hru_init(iihru)%hyd%latq_co, hru(iihru)%hyd%perco, hru_init(iihru)%hyd%perco, hru(iihru)%hyd%perco_lim, hru_init(iihru)%hyd%perco_lim` |
| [sym:soil_module] | `no resolved imported state` |  |
| [sym:plant_module] | `no resolved imported state` |  |
| [sym:hydrograph_module] | `no resolved imported state` |  |
| [sym:ru_module] | `no resolved imported state` |  |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:channel_module] | `no resolved imported state` |  |
| [sym:hru_lte_module] | `no resolved imported state` |  |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:basin_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_reg` |
| [sym:calibration_data_module] | `region, lscal, ls_prms` | `region(ireg)%nlum, lscal(ireg)%lum(ilum)%meas%etr, lscal(ireg)%lum(ilum)%precip_aa, lscal(ireg)%lum(ilum)%ha, lscal(ireg)%lum(ilum)%prm_lim%etco, lscal(ireg)%lum(ilum)%prm_prev, lscal(ireg)%lum(ilum)%prm, lscal(ireg)%lum(ilum)%prev, lscal(ireg)%lum(ilum)%aa, lscal(ireg)%lum(ilum)%aa%etr, lscal(ireg)%lum(ilum)%prm_prev%etco, lscal(ireg)%lum(ilum)%prm%etco, lscal(ireg)%lum(ilum)%prev%etr, ls_prms(2)%pos, ls_prms(2)%neg, region(ireg)%num_tot, region(ireg)%num(ihru_s), lscal(ireg)%lum(ilum)%meas%name, ls_prms(2)%up, ls_prms(2)%lo, lscal(ireg)%lum(ilum)%nbyr, lscal(ireg)%lum(ilum)%prm_prev%petco, lscal(ireg)%lum(ilum)%prm%petco, ls_prms(4)%pos, lscal(ireg)%lum(ilum)%prm_lim%petco, ls_prms(4)%neg, ls_prms(4)%up, ls_prms(4)%lo, lscal(ireg)%lum(ilum)%meas%srr, lscal(ireg)%lum(ilum)%prm_lim%cn3_swf, lscal(ireg)%lum(ilum)%aa%srr, lscal(ireg)%lum(ilum)%prm_prev%cn3_swf, lscal(ireg)%lum(ilum)%prm%cn3_swf, lscal(ireg)%lum(ilum)%prev%srr, ls_prms(10)%pos, ls_prms(10)%neg, ls_prms(10)%up, ls_prms(10)%lo, lscal(ireg)%lum(ilum)%meas%lfr, lscal(ireg)%lum(ilum)%prm_lim%lat_len, lscal(ireg)%lum(ilum)%aa%lfr, lscal(ireg)%lum(ilum)%prm_prev%lat_len, lscal(ireg)%lum(ilum)%prm%lat_len, lscal(ireg)%lum(ilum)%prev%lfr, ls_prms(3)%pos, ls_prms(3)%neg, ls_prms(3)%up, ls_prms(3)%lo, lscal(ireg)%lum(ilum)%meas%pcr, lscal(ireg)%lum(ilum)%prm_lim%perco, lscal(ireg)%lum(ilum)%aa%pcr, lscal(ireg)%lum(ilum)%prm_prev%perco, lscal(ireg)%lum(ilum)%prm%perco, lscal(ireg)%lum(ilum)%prev%pcr, ls_prms(8)%pos, ls_prms(8)%neg, ls_prms(8)%up, ls_prms(8)%lo` |
| [sym:conditional_module] | `no resolved imported state` |  |
| [sym:reservoir_module] | `no resolved imported state` |  |
| [sym:organic_mineral_mass_module] | `no resolved imported state` |  |
| [sym:time_module] | `no resolved imported state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lscal(ireg)%lum(ilum)%prm_prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous parameter set before this adjustment so it can be restored or compared. |
| `lscal(ireg)%lum(ilum)%prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous statistics before this adjustment so it can be restored or compared. |
| `lscal(ireg)%lum(ilum)%prm_prev%etco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the ET soil-evaporation compensation factor (esco) before adjustment. |
| `lscal(ireg)%lum(ilum)%prm%etco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the ET soil-evaporation compensation factor (esco) for the calibration unit by the computed increment (clamped to its limits). |
| `lscal(ireg)%lum(ilum)%prev%etr` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous simulated ET ratio for the calibration unit. |
| `lscal(ireg)%lum(ilum)%prm_lim%etco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the ET soil-evaporation compensation factor (esco) has hit its calibration limit, so it is no longer adjusted. |
| `hru(iihru)%hyd%esco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the soil-evaporation compensation factor on the HRU to the calibrated value (clamped to bounds). |
| `hru_init(iihru)%hyd%esco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy soil-evaporation compensation factor on the HRU to the calibrated value (clamped to bounds). |
| `lscal(ireg)%lum(ilum)%nbyr` | After applying an adjustment, before re-running. | Resets the calibration unit's simulated-year counter so fresh averages accumulate on the re-run. |
| `lscal(ireg)%lum(ilum)%precip_aa` | After applying an adjustment, before re-running. | Resets the accumulated average-annual precipitation for the calibration unit. |
| `lscal(ireg)%lum(ilum)%aa` | After applying an adjustment, before re-running. | Resets the calibration unit's average-annual simulated statistics to zero. |
| `cal_sim` | Before each re-run of the model. | Sets the label identifying the current calibration stage for the re-run. |
| `cal_adj` | After computing a parameter increment. | Records the applied parameter adjustment for the stage. |
| `lscal(ireg)%lum(ilum)%prm_prev%petco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the PET adjustment coefficient before adjustment. |
| `lscal(ireg)%lum(ilum)%prm%petco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the PET adjustment coefficient for the calibration unit by the computed increment (clamped to its limits). |
| `lscal(ireg)%lum(ilum)%prm_lim%petco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the PET adjustment coefficient has hit its calibration limit, so it is no longer adjusted. |
| `hru(iihru)%hyd%pet_co` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the PET adjustment coefficient on the HRU to the calibrated value (clamped to bounds). |
| `hru_init(iihru)%hyd%pet_co` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy PET adjustment coefficient on the HRU to the calibrated value (clamped to bounds). |
| `lscal(ireg)%lum(ilum)%prm_prev%cn3_swf` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the CN3 soil-water adjustment factor (surface runoff) before adjustment. |
| `lscal(ireg)%lum(ilum)%prm%cn3_swf` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the CN3 soil-water adjustment factor (surface runoff) for the calibration unit by the computed increment (clamped to its limits). |
| `lscal(ireg)%lum(ilum)%prev%srr` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous simulated surface-runoff ratio for the calibration unit. |
| `lscal(ireg)%lum(ilum)%prm_lim%cn3_swf` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the CN3 soil-water adjustment factor (surface runoff) has hit its calibration limit, so it is no longer adjusted. |
| `hru(iihru)%hyd%cn3_swf` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the CN3 soil-water adjustment factor (surface runoff) on the HRU to the calibrated value (clamped to bounds). |
| `hru_init(iihru)%hyd%cn3_swf` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy CN3 soil-water adjustment factor (surface runoff) on the HRU to the calibrated value (clamped to bounds). |

## File I/O

<!-- facts:io -->


## Lineage

`calsoft_hyd.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `calsoft_hyd.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calsoft_hyd' has no extracted documentation comment.
- Soft-calibration routine for water balance (ET, PET, surface runoff): compares simulated vs measured statistics, adjusts parameters, and re-runs via time_control. 13 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
