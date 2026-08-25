---
kind: procedure
symbol: pl_pup
title: pl_pup
status: filled
source_hash: 90cf3140f623626a
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru` so the routine can index the current watershed/landscape
    and its plant/soil state.
  l: Loop counter for soil layers while scanning root depth and distributing phosphorus uptake
    through the rooted profile.
  root_depth: Effective root penetration depth used to decide which soil layers can contribute
    phosphorus uptake and to scale the depth-shaped uptake curve.
  soil_depth: Bottom depth of the current soil layer, used to compare against root depth and
    compute the layer's uptake potential.
  uapl: Actual phosphorus removed from the current soil layer during the uptake pass, limited
    by both unmet plant demand and labile soil P.
  upmx: Maximum phosphorus the current layer can supply under the depth-based uptake distribution
    before the plant's remaining demand is applied.
uses:
  basin_module: This module provides `bsn_prm%p_updis`, the basin-level phosphorus uptake
    distribution parameter used in the exponential depth weighting at line 70.
  organic_mineral_mass_module: This module holds the soil labile phosphorus pool and the plant
    phosphorus pools that are decremented and incremented by uptake, so it supplies both the
    source reservoir and the biomass accounting states touched by this routine.
  hru_module: This module provides the current HRU/plant phosphorus demand and normalization
    inputs (`uapd`, `up2`, `rto_solp`, `pplnt`, `ipl`, `ihru`) that control how much P can
    be taken up and how the stress response is evaluated.
  soil_module: This module provides the soil-layer geometry (`soil(j)%nly`, `soil(j)%phys(l)%d`)
    needed to determine which layers lie within the current root zone and to compute uptake
    by depth.
  plant_module: This module provides the plant root-depth and root-fraction state used to
    decide which layers are rooted and how the absorbed phosphorus is split between above-ground
    and root biomass pools.
  output_landscape_module: This module stores the daily HRU nutrient-balance summary, and
    `pl_pup` adds the computed plant phosphorus uptake to `hnb_d(j)%puptake` for later reporting
    and accounting.
  utils: The `utils` module matters because it supplies `Exp_w`, the safe exponential wrapper
    used in the depth-distribution formula for phosphorus uptake.
---

<!-- facts:header -->

Calculates daily plant phosphorus uptake for the current HRU and plant, distributing demand through rooted soil layers and updating plant and soil phosphorus pools.

## Bottom Line

pl_pup is the plant phosphorus uptake routine. It starts from the plant phosphorus demand for the current HRU/plant, walks downward through the soil layers that the roots occupy, and removes labile soil phosphorus layer by layer until the plant demand is satisfied or the rooted soil zone is exhausted.

As it does that, it accumulates actual plant P uptake in `pplnt`, reduces `soil1(j)%mp(l)%lab`, updates plant biomass P pools and the HRU phosphorus uptake summary, and then computes the phosphorus stress factor with `nuts` from above-ground P versus the optimal P content.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside daily plant biomass growth, after `pl_biomass_gro` has prepared the plant's phosphorus demand (`uapd`) and related uptake controls for the active HRU/plant. Its results feed plant phosphorus stress, biomass phosphorus accounting, and HRU nutrient-balance output used by later plant growth and reporting code.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU bookkeeping and early exit on zero demand | Copies the current HRU index from `ihru` into `j`, resets plant phosphorus stress to neutral (`pcom(j)%plstr(ipl)%strsp = 1.`) and the HRU phosphorus uptake accumulator to zero, then returns immediately if the current plant phosphorus demand `uapd(ipl)` is negligible. |
| 2. find the rooted soil depth boundary | Starts from the plant root depth, enforces a minimum effective depth of 10.1 mm, then scans soil layers until the layer bottom depth exceeds the root depth. When that happens, it snaps `root_depth` to that layer bottom and exits the loop. |
| 3. walk rooted layers and compute uptake potential | Loops again through the soil layers, stopping once the current layer lies below the effective root depth. For each rooted layer, it computes `upmx` from plant demand, the soil-depth exponential curve, the basin phosphorus distribution parameter, and the phosphorus normalization factor. |
| 4. take actual phosphorus from each rooted layer | Limits actual layer uptake to the smaller of unmet plant demand and the layer's labile phosphorus pool, adds that amount to cumulative plant uptake `pplnt(j)`, and subtracts it from `soil1(j)%mp(l)%lab`. |
| 5. prevent negative accumulated plant uptake | Clamps the cumulative plant phosphorus uptake to zero if rounding or prior bookkeeping would make `pplnt(j)` negative. |
| 6. update plant phosphorus biomass pools | Adds the day's plant phosphorus uptake to total plant P, splits that uptake between above-ground and root biomass using `pcom(j)%plg(ipl)%root_frac`, and stores the daily uptake in `pl_mass_up%p`. |
| 7. record HRU phosphorus uptake and compute stress | Adds the accumulated plant P uptake to the HRU nutrient-balance output and calls `nuts` to recalculate the phosphorus stress factor from above-ground plant P versus optimal P. |
| 8. return | Exits the subroutine after all plant and soil phosphorus accounting is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%p_updis` |
| [sym:organic_mineral_mass_module] | `soil1, pl_mass, pl_mass_up` | `soil1(j)%mp(l)%lab, pl_mass(j)%tot(ipl)%p, pl_mass(j)%ab_gr(ipl)%p, pl_mass(j)%root(ipl)%p, pl_mass_up%p` |
| [sym:hru_module] | `uptake, pplnt, up2, uapd, ihru, ipl, rto_solp` | `uptake%p_norm` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(l)%d` |
| [sym:plant_module] | `pcom` | `pcom(j)%plstr(ipl)%strsp, pcom(j)%plg(ipl)%root_dep` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%puptake` |
| [sym:utils] | `utils` | `Exp_w` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plstr(ipl)%strsp` | After nonzero phosphorus uptake has been accumulated in `pplnt(j)`. | `pcom(j)%plstr(ipl)%strsp` is recomputed by `nuts` to represent the current plant phosphorus stress, based on updated above-ground P and optimal P content. |
| `hnb_d(j)%puptake` | After `pplnt(j)` is added to the HRU balance near the end of the routine. | `hnb_d(j)%puptake` records the day's plant phosphorus uptake for the HRU so the model can report and aggregate nutrient-balance outputs. |
| `pplnt(j)` | Whenever the routine reaches the uptake loop, with `uapd(ipl)` above the early-return threshold. | `pplnt(j)` accumulates the plant's actual phosphorus uptake from all rooted soil layers during this call. |
| `soil1(j)%mp(l)%lab` | For each rooted soil layer where uptake occurs. | `soil1(j)%mp(l)%lab` is reduced by the phosphorus removed from that layer, representing depletion of the labile mineral phosphorus pool. |
| `pl_mass(j)%tot(ipl)%p` | After all rooted layers have been processed and `pplnt(j)` is finalized. | `pl_mass(j)%tot(ipl)%p` increases by the plant's daily phosphorus uptake so total plant phosphorus mass reflects today's acquisition. |
| `pl_mass(j)%ab_gr(ipl)%p` | After total plant P is updated and the routine splits the uptake into biomass fractions. | `pl_mass(j)%ab_gr(ipl)%p` is increased by the above-ground share of the day's uptake, using `1. - pcom(j)%plg(ipl)%root_frac`. |
| `pl_mass(j)%root(ipl)%p` | After total plant P is updated and the routine splits the uptake into biomass fractions. | `pl_mass(j)%root(ipl)%p` is increased by the root share of the day's uptake, using `pcom(j)%plg(ipl)%root_frac`. |
| `pl_mass_up%p` | After the uptake total has been finalized for the day. | `pl_mass_up%p` stores the day's plant phosphorus uptake for use as a daily biomass-and-nutrient increment summary. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.3.24 | Cumulative phosphorus uptake by depth | $P_{up,z}=\frac{P_{up}}{[1-exp(-\beta_p)]}*[1-exp(-\beta_p*\frac{z}{z_{root}})]$ | Verified against SWAT+ 62.0.0 (pl_pup.f90:70). upmx = uapd*rto_solp*(1.-Exp_w(-p_updis*z/root_dep))/p_norm` — P uptake depth dist |
| 5:2.3.25 | Layer phosphorus uptake potential | $P_{up,ly}=P_{up,zl}-P_{up,zu}$ | Layer uptake is recovered from the cumulative depth curve through the running plant total pplnt rather than by an explicit Pup,zl - Pup,zu difference variable. |
| 5:2.3.26 | Actual layer phosphorus uptake | $P_{actualup,ly}=min\lfloor P_{up,ly}+P_{demand},P_{solution,ly}\rfloor$ | Actual layer uptake is min(upmx - pplnt, labile soil P). The separate Pdemand addition is folded into the cumulative-demand formulation. |

## Lineage

`pl_pup.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_pup.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f52e9d8` (2025-10-14) — Removed a debug print statement in sq_greenampt and added use utils to a pl_pup and basin_prm_default to catch exp(x) underflows.
- `09d23f0` (2025-06-26) — Comment and formatting changes
- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_pup' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
