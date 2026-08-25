---
kind: procedure
symbol: calsoft_plant
title: calsoft_plant
status: filled
source_hash: 1b4c19522c425fb7
version_label: SWAT+ 62.0.0
locals:
  iter_all: Outer calibration-iteration count.
  iterall: Outer calibration-iteration counter.
  isim: 'Flag: 1 if any parameter was adjusted (so a re-run is needed).'
  ireg: Calibration-region counter.
  ilum: Land-use counter within a region.
  iihru: HRU index within a region.
  ihru_s: HRU sequence counter within a region.
  iter_ind: Inner iteration limit.
  ist: Local counter/scalar used in the calibration loop (`ist`).
  ipl: Plant counter.
  nvar: Local counter/scalar used in the calibration loop (`nvar`).
  rmeas: Measured target value.
  denom: Denominator for a ratio/difference.
  soft: Measured (soft) target, scaled to a depth.
  diff: Relative difference between measured and simulated.
  chg_val: Computed parameter increment.
  perc_ln_func: Intermediate for the percolation-limit transform.
uses:
  hru_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
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
  soil_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
  plant_module: Provides the calibration data structures and HRU/region parameters that this
    routine reads and adjusts.
  output_landscape_module: Provides the calibration data structures and HRU/region parameters
    that this routine reads and adjusts.
---

<!-- facts:header -->

Soft-calibrates plant yield by adjusting plant parameters (epco, pesticide stress, potential LAI) per region/land-use to match measured yields.

## Bottom Line

`calsoft_plant` adjusts plant-growth parameters (plant-uptake compensation `epco`, pesticide-stress, and potential LAI) for each calibration region/land use so simulated crop yields match measured values.

Each adjustment is applied to the plant community of every HRU in the region, then the model is re-initialized and re-run via `time_control`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Part of the soft/hard calibration sequence (driven by `calsoft_control`/`calsoft_hyd_bfr`). It adjusts parameters to calibrate plant yield, re-initializes objects, and re-runs the model via `time_control`. It runs only when calibration is enabled, before the production simulation.

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
| [sym:hru_module] | `hru, hru_init` | `hru(iihru)%tiledrain, hru(iihru)%strsa, hru(iihru)%hyd%perco, hru(iihru)%hyd%perco_lim, hru_init(iihru)%hyd%perco, hru_init(iihru)%hyd%perco_lim` |
| [sym:hydrograph_module] | `no resolved imported state` |  |
| [sym:ru_module] | `no resolved imported state` |  |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:hru_lte_module] | `no resolved imported state` |  |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:basin_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plcal_reg` |
| [sym:calibration_data_module] | `plcal, pl_prms` | `plcal(ireg)%lum_num, plcal(ireg)%lum(ilum)%meas%yield, plcal(ireg)%lum(ilum)%aa%yield, plcal(ireg)%num_tot, plcal(ireg)%num(ihru_s), plcal(ireg)%lum(ilum)%meas%name, plcal(ireg)%lum(ilum)%prm%epco, pl_prms(ireg)%prm(ilum)%init_val, plcal(ireg)%lum(ilum)%ha, plcal(ireg)%lum(ilum)%prm_prev, plcal(ireg)%lum(ilum)%prm, plcal(ireg)%lum(ilum)%prev, plcal(ireg)%lum(ilum)%aa, plcal(ireg)%lum(ilum)%prm_lim%epco, plcal(ireg)%lum(ilum)%prm_lowlim%epco, plcal(ireg)%lum(ilum)%prm_uplim%epco, plcal(ireg)%lum(ilum)%prm_prev%epco, plcal(ireg)%lum(ilum)%prev%yield, pl_prms(ireg)%prm(ilum+nvar)%pos, pl_prms(ireg)%prm(ilum+nvar)%neg, pl_prms(ireg)%prm(ilum+nvar)%up, pl_prms(ireg)%prm(ilum+nvar)%lo, plcal(ireg)%lum(ilum)%prm_prev%pest_stress, plcal(ireg)%lum(ilum)%prm%pest_stress, pl_prms(ireg)%prm(ilum)%pos, plcal(ireg)%lum(ilum)%prm_lim%pest_stress, pl_prms(ireg)%prm(ilum)%neg, pl_prms(ireg)%prm(ilum)%up, pl_prms(ireg)%prm(ilum)%lo, plcal(ireg)%lum(ilum)%prm_prev%lai_pot, plcal(ireg)%lum(ilum)%prm%lai_pot, plcal(ireg)%lum(ilum)%prm_lim%lai_pot, plcal(ireg)%lum(ilum)%prm_prev%harv_idx, plcal(ireg)%lum(ilum)%prm%harv_idx, plcal(ireg)%lum(ilum)%prm_lim%harv_idx` |
| [sym:conditional_module] | `no resolved imported state` |  |
| [sym:reservoir_module] | `no resolved imported state` |  |
| [sym:soil_module] | `no resolved imported state` |  |
| [sym:plant_module] | `pcom, pcom_init` | `pcom(iihru)%npl, pcom(iihru)%pl(ipl), pcom(iihru)%plcur(ipl)%epco, pcom_init(iihru)%plcur(ipl)%epco, pcom(iihru)%plcur(ipl)%pest_stress, pcom_init(iihru)%plcur(ipl)%pest_stress, pcom(iihru)%plcur(ipl)%lai_pot, pcom_init(iihru)%plcur(ipl)%lai_pot, pcom(iihru)%plcur(ipl)%harv_idx, pcom_init(iihru)%plcur(ipl)%harv_idx` |
| [sym:output_landscape_module] | `no resolved imported state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(iihru)%hyd%perco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the percolation coefficient (baseflow) on the HRU to the calibrated value (clamped to bounds). |
| `hru(iihru)%hyd%perco_lim` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the percolation limit on the HRU to the calibrated value (clamped to bounds). |
| `hru_init(iihru)%hyd%perco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy percolation coefficient (baseflow) on the HRU to the calibrated value (clamped to bounds). |
| `hru_init(iihru)%hyd%perco_lim` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy percolation limit on the HRU to the calibrated value (clamped to bounds). |
| `hru(iihru)%strsa` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the aeration-stress factor on the HRU to the calibrated value (clamped to bounds). |
| `cal_sim` | Before each re-run of the model. | Sets the label identifying the current calibration stage for the re-run. |
| `plcal(ireg)%lum(ilum)%prm%epco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the plant-uptake (transpiration) compensation factor for the calibration unit by the computed increment (clamped to its limits). |
| `plcal(ireg)%lum(ilum)%prm_prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous parameter set before this adjustment so it can be restored or compared. |
| `plcal(ireg)%lum(ilum)%prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous statistics before this adjustment so it can be restored or compared. |
| `plcal(ireg)%lum(ilum)%prm_lim%epco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the plant-uptake (transpiration) compensation factor has hit its calibration limit, so it is no longer adjusted. |
| `plcal(ireg)%lum(ilum)%prm_lowlim%epco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the plant-uptake (transpiration) compensation factor for the calibration unit by the computed increment (clamped to its limits). |
| `plcal(ireg)%lum(ilum)%prm_uplim%epco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the plant-uptake (transpiration) compensation factor for the calibration unit by the computed increment (clamped to its limits). |
| `plcal(ireg)%lum(ilum)%prm_prev%epco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the plant-uptake (transpiration) compensation factor before adjustment. |
| `plcal(ireg)%lum(ilum)%prev%yield` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous simulated crop yield for the calibration unit. |
| `pcom(iihru)%plcur(ipl)%epco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the plant-uptake (transpiration) compensation factor on the HRU to the calibrated value (clamped to bounds). |
| `pcom_init(iihru)%plcur(ipl)%epco` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy plant-uptake (transpiration) compensation factor on the HRU to the calibrated value (clamped to bounds). |
| `plcal(ireg)%lum(ilum)%prm_prev%pest_stress` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the pesticide-stress factor before adjustment. |
| `plcal(ireg)%lum(ilum)%prm%pest_stress` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the pesticide-stress factor for the calibration unit by the computed increment (clamped to its limits). |
| `plcal(ireg)%lum(ilum)%prm_lim%pest_stress` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the pesticide-stress factor has hit its calibration limit, so it is no longer adjusted. |
| `pcom(iihru)%plcur(ipl)%pest_stress` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the pesticide-stress factor on the HRU to the calibrated value (clamped to bounds). |
| `pcom_init(iihru)%plcur(ipl)%pest_stress` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy pesticide-stress factor on the HRU to the calibrated value (clamped to bounds). |
| `plcal(ireg)%lum(ilum)%prm_prev%lai_pot` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the potential leaf area index before adjustment. |
| `plcal(ireg)%lum(ilum)%prm%lai_pot` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the potential leaf area index for the calibration unit by the computed increment (clamped to its limits). |
| `plcal(ireg)%lum(ilum)%prm_lim%lai_pot` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the potential leaf area index has hit its calibration limit, so it is no longer adjusted. |

## File I/O

<!-- facts:io -->


## Lineage

`calsoft_plant.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `calsoft_plant.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `16e54aa` (2024-07-05) — BB 61.0.1
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calsoft_plant' has no extracted documentation comment.
- Soft-calibration routine for plant yield: compares simulated vs measured statistics, adjusts parameters, and re-runs via time_control. 10 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
