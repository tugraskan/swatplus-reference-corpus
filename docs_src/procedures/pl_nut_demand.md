---
kind: procedure
symbol: pl_nut_demand
title: pl_nut_demand
status: filled
source_hash: 7909980d179f41d6
version_label: SWAT+ 62.0.0
locals:
  j: HRU index used to select the current plant community and soil profile; it is set from
    `ihru` before any plant or soil sums are computed.
  nly: Loop index over soil layers when summing the profile nitrate and labile phosphorus
    pools.
  idp: Plant database index copied from the active plant’s `idplt`; it is used to look up
    species parameters such as `t_base` in `pldb`.
  delg: Daily fractional increment to the plant’s accumulated heat-unit progress for annual
    growth (`phuacc`), computed from temperature above base and normalized by `phumat`.
  delg_p: Daily fractional increment to the perennial heat-unit progress (`phuacc_p`), computed
    the same way as `delg` but normalized by `phumat_p`.
uses:
  hru_module: The HRU module supplies the current HRU/plant indices and the arrays that store
    per-plant and HRU-total nutrient demand. `pl_nut_demand` reads and updates `uno3d`, `uapd`,
    `uno3d_tot`, `uapd_tot`, `sum_no3`, and `sum_solp`, so these HRU-level state variables
    are the main outputs of the routine.
  soil_module: The soil module provides the HRU soil-layer count used to iterate through the
    profile. Without `soil(j)%nly`, the routine could not total nitrate and labile phosphorus
    across all layers.
  plant_module: The plant module provides the current plant community and plant-status fields
    that determine which plants are processed and how their heat-unit progress is updated.
    `npl`, `idorm`, `gro`, `phumat`, `phumat_p`, `phuacc`, and `phuacc_p` control both eligibility
    for demand updates and the growth-stage tracking that feeds those updates.
  plant_data_module: The plant data module supplies species-level parameters for the selected
    crop, especially `t_base`. That base temperature is required to convert the day’s mean
    temperature into a normalized heat-unit increment.
  organic_mineral_mass_module: The organic/mineral mass module provides the soil-layer mineral
    pools that are summed at the end of the routine. `soil1(j)%mn(nly)%no3` and `soil1(j)%mp(nly)%lab`
    are the nitrate and labile phosphorus amounts the model uses to describe available soil
    nutrients.
  climate_module: The climate module supplies the day’s mean air temperature `w%tave`, which
    drives the heat-unit increment used to advance plant development and therefore plant nutrient
    demand.
---

<!-- facts:header -->

Updates each active plant’s daily nitrogen and phosphorus demand and accumulates HRU-level nutrient demand totals. It also refreshes plant heat-unit progress and sums soil mineral N and P in the profile.

## Bottom Line

pl_nut_demand walks the plants in the current HRU and updates nutrient-demand state for each plant that is both growing and not dormant. For those plants it advances accumulated heat units using daily temperature and the crop’s base temperature, then calls the plant nitrogen and phosphorus update routines to refresh per-plant demand values.

After the plant loop, it sums the plant-level nitrogen and phosphorus demands into HRU totals, and it also scans all soil layers to total the profile’s nitrate and labile phosphorus pools. Those totals provide the nutrient-demand and available-nutrient context used by later plant/soil uptake logic in the growth workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called by `pl_grow` near the start of daily plant-growth processing, after the current HRU has been selected and before biomass and partitioning updates proceed. Its results feed the rest of the growth-day workflow by establishing plant-level N and P demand totals and current heat-unit progress, which later uptake and growth routines rely on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU context and reset plant demand totals | Copy the current HRU index from `ihru` into `j`, then zero the per-plant and total nitrogen/phosphorus demand accumulators before scanning the plant community. |
| 2. loop over plants in the current community | Iterate through every plant slot in the current HRU plant community and fetch that plant’s database index from `idplt`. |
| 3. process only growing, non-dormant plants | Skip nutrient-demand updates unless the plant is active: it must not be dormant and must be marked as growing. |
| 4. compute daily heat-unit increments | Start the daily increment at zero, then if the plant has valid maturity heat units compute annual and perennial progress increments from mean temperature minus base temperature, normalized by `phumat` and `phumat_p`. |
| 5. clip negative heat-unit increments | Force both heat-unit increments to zero when temperature is below base so development does not move backward. |
| 6. advance plant heat-unit progress | Add the daily increments to the plant’s accumulated annual and perennial heat-unit fractions. |
| 7. update nitrogen demand state | Call `pl_nupd` to refresh the active plant’s nitrogen demand and deficit based on the new growth stage. |
| 8. update phosphorus demand state | Call `pl_pupd` to refresh the active plant’s phosphorus demand and deficit based on the new growth stage. |
| 9. accumulate HRU nutrient-demand totals | Add the current plant’s nitrogen and phosphorus demand values into the HRU totals. |
| 10. finish plant loop | End the per-plant processing loop after all plants in the community have been checked. |
| 11. reset soil nutrient sums | Clear the soil-profile nitrate and labile phosphorus totals before summing across layers. |
| 12. sum soil-layer nitrate and labile phosphorus | Loop over every soil layer in the current HRU and accumulate nitrate from `mn(nly)%no3` and labile phosphorus from `mp(nly)%lab`. |
| 13. return to caller | Return after the plant-demand totals and soil nutrient sums have been updated for the day. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `uno3d, uapd, ihru, ipl, uapd_tot, uno3d_tot, sum_no3, sum_solp` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%idorm, pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%phumat, pcom(j)%plcur(ipl)%phumat_p, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plcur(ipl)%phuacc_p` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%t_base` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(nly)%no3, soil1(j)%mp(nly)%lab` |
| [sym:climate_module] | `w` | `w%tave` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `uno3d(ipl)` | When a plant in the current HRU is growing and not dormant, after its daily heat-unit progress is updated and `pl_nupd` has run. | `uno3d(ipl)` is refreshed to the current plant’s nitrogen demand/deficit, so the HRU has a per-plant N demand value for downstream nutrient allocation. |
| `uno3d_tot` | After each active plant’s `uno3d(ipl)` has been updated in the plant loop. | `uno3d_tot` is the sum of all active plants’ nitrogen demand in the current HRU, which later routines use as the HRU-level nitrogen demand total. |
| `uapd(ipl)` | When a plant in the current HRU is growing and not dormant, after `pl_pupd` has run. | `uapd(ipl)` is refreshed to the current plant’s phosphorus demand/deficit, giving a per-plant P demand value for later allocation. |
| `uapd_tot` | After each active plant’s `uapd(ipl)` has been updated in the plant loop. | `uapd_tot` is the sum of all active plants’ phosphorus demand in the current HRU, which later routines use as the HRU-level phosphorus demand total. |
| `pcom(j)%plcur(ipl)%phuacc` | When the plant is active and daily temperature is used to compute a nonnegative heat-unit increment. | `pcom(j)%plcur(ipl)%phuacc` advances by the day’s normalized annual heat-unit increment, representing the plant’s accumulated fraction of maturity for annual growth. |
| `pcom(j)%plcur(ipl)%phuacc_p` | When the plant is active and daily temperature is used to compute a nonnegative perennial heat-unit increment. | `pcom(j)%plcur(ipl)%phuacc_p` advances by the day’s normalized perennial heat-unit increment, representing the perennial maturity-progress fraction. |
| `sum_no3` | After the soil-profile sum loop begins for the current HRU. | `sum_no3` becomes the total nitrate mass across all soil layers in the HRU, which characterizes available mineral nitrogen in the profile. |
| `sum_solp` | After the soil-profile sum loop begins for the current HRU. | `sum_solp` becomes the total labile phosphorus mass across all soil layers in the HRU, which characterizes available mineral phosphorus in the profile. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:1.1.1 | Daily heat units | $HU=\overline T_{av}-T_{base}$ | Daily PHU increment uses delg = (tave - t_base)/phumat with negative values clipped to zero, which is the normalized form of HU = max(tave - t_base, 0). |
| 5:1.1.2 | Accumulated potential heat units fraction | $PHU=\sum_{d=1}^m HU$ | The code accumulates normalized fractions phuacc and phuacc_p rather than storing PHU directly; phumat/phumat_p provide the denominator. |
| 5:2.1.11 | Fraction of potential heat units accumulated | $fr_{PHU}=\frac{\sum_{i=1}^d HU_i}{PHU}$ | Verified against SWAT+ 62.0.0 (pl_nut_demand.f90:71). phuacc = phuacc + delg` — fr_PHU accumulation |
| 5:1.1.4 | Base-zero annual heat-unit total | $PHU_0=\sum_{d=1}^{365} HU_0$ | Verified against SWAT+ 62.0.0 (pl_nut_demand.f90). (PHU accumulation) |

## Lineage

`pl_nut_demand.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_nut_demand.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_nut_demand' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 13 source-backed steps to separate initialization, per-plant gating, heat-unit updates, nutrient-demand calls, accumulation, and soil-profile summation.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
