---
kind: procedure
symbol: calsoft_hyd_bfr_latq
title: calsoft_hyd_bfr_latq
status: filled
source_hash: 561b42b19fceb82e
version_label: SWAT+ 62.0.0
locals:
  isim: 'Flag: 1 if any parameter was adjusted (so a re-run is needed).'
  ireg: Calibration-region counter.
  ilum: Land-use counter within a region.
  iihru: HRU index within a region.
  ihru_s: HRU sequence counter within a region.
  iter_ind: Inner iteration limit.
  ik: Iteration counter.
  rmeas: Measured target value.
  denom: Denominator for a ratio/difference.
  soft: Measured (soft) target, scaled to a depth.
  diff: Relative difference between measured and simulated.
  chg_val: Computed parameter increment.
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

Soft-calibrates lateral flow (before flow-regime partitioning) by adjusting lat_len/latq_co (lateral flow) per region/land-use to match the measured ratio.

## Bottom Line

`calsoft_hyd_bfr_latq` is the before-flow-regime soft-calibration for lateral flow. For each region/land use it compares the simulated vs measured lateral flow statistic and adjusts lat_len/latq_co (lateral flow), clamping to limits.

The adjusted parameter is applied to each HRU in the region, then the model is re-initialized and re-run via `time_control`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Part of the soft/hard calibration sequence (driven by `calsoft_control`/`calsoft_hyd_bfr`). It adjusts parameters to calibrate lateral flow (before-flow-regime), re-initializes objects, and re-runs the model via `time_control`. It runs only when calibration is enabled, before the production simulation.

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
| [sym:hru_module] | `hru, hru_init` | `hru(iihru)%lum_group_c, hru(iihru)%hyd%latq_co, hru_init(iihru)%hyd%latq_co` |
| [sym:soil_module] | `no resolved imported state` |  |
| [sym:plant_module] | `no resolved imported state` |  |
| [sym:hydrograph_module] | `no resolved imported state` |  |
| [sym:ru_module] | `no resolved imported state` |  |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:hru_lte_module] | `no resolved imported state` |  |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:basin_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_reg` |
| [sym:calibration_data_module] | `region, lscal, ls_prms, lscal_z` | `region(ireg)%nlum, lscal(ireg)%lum(ilum)%meas%lfr, lscal(ireg)%lum(ilum)%precip_aa, lscal(ireg)%lum(ilum)%ha, lscal(ireg)%lum(ilum)%prm_prev, lscal(ireg)%lum(ilum)%prm, lscal(ireg)%lum(ilum)%prev, lscal(ireg)%lum(ilum)%aa, lscal(ireg)%lum(ilum)%aa%lfr, lscal(ireg)%lum(ilum)%prm_prev%lat_len, lscal(ireg)%lum(ilum)%prm%lat_len, lscal(ireg)%lum(ilum)%prev%lfr, ls_prms(3)%pos, lscal(ireg)%lum(ilum)%prm_lim%lat_len, ls_prms(3)%neg, region(ireg)%num_tot, region(ireg)%num(ihru_s), lscal(ireg)%lum(ilum)%meas%name, ls_prms(3)%up, ls_prms(3)%lo, lscal(ireg)%lum(ilum)%nbyr` |
| [sym:conditional_module] | `no resolved imported state` |  |
| [sym:reservoir_module] | `no resolved imported state` |  |
| [sym:organic_mineral_mass_module] | `no resolved imported state` |  |
| [sym:time_module] | `cal_sim, cal_adj` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lscal(ireg)%lum(ilum)%prm_prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous parameter set before this adjustment so it can be restored or compared. |
| `lscal(ireg)%lum(ilum)%prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous statistics before this adjustment so it can be restored or compared. |
| `lscal(ireg)%lum(ilum)%prm_prev%lat_len` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the lateral-flow hillslope length before adjustment. |
| `lscal(ireg)%lum(ilum)%prm%lat_len` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the lateral-flow hillslope length for the calibration unit by the computed increment (clamped to its limits). |
| `lscal(ireg)%lum(ilum)%prev%lfr` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous simulated lateral-flow ratio for the calibration unit. |
| `lscal(ireg)%lum(ilum)%prm_lim%lat_len` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the lateral-flow hillslope length has hit its calibration limit, so it is no longer adjusted. |
| `hru(iihru)%hyd%latq_co` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the lateral-flow coefficient on the HRU to the calibrated value (clamped to bounds). |
| `hru_init(iihru)%hyd%latq_co` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the init copy lateral-flow coefficient on the HRU to the calibrated value (clamped to bounds). |
| `lscal(ireg)%lum(ilum)%nbyr` | After applying an adjustment, before re-running. | Resets the calibration unit's simulated-year counter so fresh averages accumulate on the re-run. |
| `lscal(ireg)%lum(ilum)%precip_aa` | After applying an adjustment, before re-running. | Resets the accumulated average-annual precipitation for the calibration unit. |
| `lscal(ireg)%lum(ilum)%aa` | After applying an adjustment, before re-running. | Resets the calibration unit's average-annual simulated statistics to zero. |
| `cal_sim` | Before each re-run of the model. | Sets the label identifying the current calibration stage for the re-run. |
| `cal_adj` | After computing a parameter increment. | Records the applied parameter adjustment for the stage. |

## File I/O

<!-- facts:io -->


## Lineage

`calsoft_hyd_bfr_latq.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `calsoft_hyd_bfr_latq.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calsoft_hyd_bfr_latq' has no extracted documentation comment.
- Soft-calibration routine for lateral flow (before-flow-regime): compares simulated vs measured statistics, adjusts parameters, and re-runs via time_control. 11 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
