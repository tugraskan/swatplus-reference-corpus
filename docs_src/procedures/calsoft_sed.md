---
kind: procedure
symbol: calsoft_sed
title: calsoft_sed
status: filled
source_hash: ce19a6ebeb11c5bb
version_label: SWAT+ 62.0.0
locals:
  isim: 'Flag: 1 if any parameter was adjusted (so a re-run is needed).'
  ireg: Calibration-region counter.
  ilum: Land-use counter within a region.
  iihru: HRU index within a region.
  ihru_s: HRU sequence counter within a region.
  iter: Iteration counter.
  isl: Local counter/scalar used in the calibration loop (`isl`).
  rmeas: Measured target value.
  denom: Denominator for a ratio/difference.
  soft: Measured (soft) target, scaled to a depth.
  diff: Relative difference between measured and simulated.
  chg_val: Computed parameter increment.
  xm: Local counter/scalar used in the calibration loop (`xm`).
  sin_sl: Local counter/scalar used in the calibration loop (`sin_sl`).
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
---

<!-- facts:header -->

Soft-calibrates sediment yield by adjusting overland time of concentration and slope/USLE factors per region/land-use to match measured sediment.

## Bottom Line

`calsoft_sed` adjusts the overland time of concentration (`tconc`) and slope/USLE topographic factors for each calibration region/land use so simulated sediment yield matches the measured target.

Adjusted values are applied to each HRU (updating `usle_ls`/`usle_mult`), then the model is re-initialized and re-run.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Part of the soft/hard calibration sequence (driven by `calsoft_control`/`calsoft_hyd_bfr`). It adjusts parameters to calibrate sediment yield, re-initializes objects, and re-runs the model via `time_control`. It runs only when calibration is enabled, before the production simulation.

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
| [sym:hru_module] | `hru, tconc, ihru` | `hru(ihru)%lum_group_c, hru(iihru)%topo%slope, hru(iihru)%lumv%usle_ls, hru(iihru)%lumv%usle_mult, hru(iihru)%lumv%usle_p` |
| [sym:soil_module] | `soil` | `soil(iihru)%phys(1)%rock, soil(iihru)%usle_k` |
| [sym:plant_module] | `no resolved imported state` |  |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:ru_module] | `no resolved imported state` |  |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:hru_lte_module] | `no resolved imported state` |  |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:basin_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cha_reg` |
| [sym:calibration_data_module] | `region, lscal, ls_prms, lscal_z` | `region(ireg)%nlum, lscal(ireg)%lum(ilum)%meas%sed, lscal(ireg)%lum(ilum)%ha, lscal(ireg)%lum(ilum)%prm_lim%tconc, region(ireg)%num_tot, region(ireg)%num(ihru_s), lscal(ireg)%lum(ilum)%meas%name, lscal(ireg)%lum(ilum)%prm_prev, lscal(ireg)%lum(ilum)%prm, lscal(ireg)%lum(ilum)%prev, lscal(ireg)%lum(ilum)%aa, lscal(ireg)%lum(ilum)%aa%sed, lscal(ireg)%lum(ilum)%prm_prev%tconc, lscal(ireg)%lum(ilum)%prev%sed, ls_prms(1)%pos, ls_prms(6)%pos, ls_prms(6)%neg, lscal(ireg)%lum(ilum)%nbyr, lscal(ireg)%lum(ilum)%precip_aa, lscal(ireg)%lum(ilum)%prm%tconc, lscal(ireg)%lum(ilum)%prev%srr, lscal(ireg)%lum(ilum)%aa%srr, ls_prms(5)%pos, ls_prms(5)%neg, lscal(ireg)%lum(ilum)%prm%slope, lscal(ireg)%lum(ilum)%prm_prev%slope` |
| [sym:conditional_module] | `no resolved imported state` |  |
| [sym:reservoir_module] | `no resolved imported state` |  |
| [sym:organic_mineral_mass_module] | `no resolved imported state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lscal(ireg)%lum(ilum)%prm_prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous parameter set before this adjustment so it can be restored or compared. |
| `lscal(ireg)%lum(ilum)%prev` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the region/land-use's previous statistics before this adjustment so it can be restored or compared. |
| `lscal(ireg)%lum(ilum)%prm_prev%tconc` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous value of the overland time of concentration before adjustment. |
| `lscal(ireg)%lum(ilum)%prev%sed` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Saves the previous simulated sediment yield for the calibration unit. |
| `lscal(ireg)%lum(ilum)%prm_lim%tconc` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Specifically when the adjusted value reaches its allowed bound. | Flags that the overland time of concentration has hit its calibration limit, so it is no longer adjusted. |
| `tconc(iihru)` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the tconc(iihru) on the HRU to the calibrated value (clamped to bounds). |
| `lscal(ireg)%lum(ilum)%nbyr` | After applying an adjustment, before re-running. | Resets the calibration unit's simulated-year counter so fresh averages accumulate on the re-run. |
| `lscal(ireg)%lum(ilum)%precip_aa` | After applying an adjustment, before re-running. | Resets the accumulated average-annual precipitation for the calibration unit. |
| `lscal(ireg)%lum(ilum)%aa` | After applying an adjustment, before re-running. | Resets the calibration unit's average-annual simulated statistics to zero. |
| `lscal(ireg)%lum(ilum)%prm%tconc` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the overland time of concentration for the calibration unit by the computed increment (clamped to its limits). |
| `lscal(ireg)%lum(ilum)%prm%slope` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. | Adjusts the HRU slope for the calibration unit by the computed increment (clamped to its limits). |
| `hru(iihru)%topo%slope` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the HRU slope on the HRU to the calibrated value (clamped to bounds). |
| `hru(iihru)%lumv%usle_ls` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the USLE topographic (LS) factor on the HRU to the calibrated value (clamped to bounds). |
| `hru(iihru)%lumv%usle_mult` | When the simulated statistic differs from the measured target beyond the tolerance for a region/land-use. Applied to each HRU in the region. | Sets the composite USLE erosion multiplier on the HRU to the calibrated value (clamped to bounds). |

## File I/O

<!-- facts:io -->


## Lineage

`calsoft_sed.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `calsoft_sed.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calsoft_sed' has no extracted documentation comment.
- Soft-calibration routine for sediment yield: compares simulated vs measured statistics, adjusts parameters, and re-runs via time_control. 9 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
