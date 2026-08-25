---
kind: procedure
symbol: nut_solp
title: nut_solp
status: filled
source_hash: fd4b76d702e33bae
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index copied from ihru so the routine can address all HRU-scoped arrays and
    derived state for the active unit.
  jj: Layer counter used only in the groundwater-to-soil transfer loop over all soil layers.
  xx: 'Intermediate denominator for the surface runoff soluble P calculation: soil bulk density
    times layer depth times the HRU phosphorus partition coefficient.'
  vap: Exponential coefficient used in the leaching and tile-drain formulas; it converts percolation
    or tile flow and soil properties into the decay term passed to exp_w.
  plch: Temporary amount of soluble phosphorus removed from a layer by percolation or tile
    drainage before the amount is bounded and stored.
  ly: Layer counter used in the percolation, bottom-leaching, and tile-drain loops over the
    soil profile.
uses:
  basin_module: bsn_cc%gwflow is the basin-level switch that enables or disables the groundwater-flow
    pathway. nut_solp only writes gwflow_percsol when that pathway is active, so the basin
    control code determines whether the leaching loss is exported for groundwater solute routing.
  organic_mineral_mass_module: soil1 holds the HRU soil profile mass pools, including the
    labile phosphorus pool in each layer. nut_solp reads and updates those layer pools directly
    to remove phosphorus to runoff, leaching, tile flow, and groundwater-to-soil transfer.
  gwflow_module: gw_soil_flag and gw_solute_flag gate the groundwater-to-soil phosphorus mass
    transfer, hru_soil provides the transferred mass by HRU and layer, and gwflow_percsol
    stores the leaching export for later groundwater routing. These states determine whether
    the routine adds groundwater P to the soil profile and whether it hands leached P off
    to gwflow.
  hru_module: hru supplies the HRU-specific phosphorus partition coefficient and percolation
    coefficient used in the runoff and leaching equations, and the land-management drainage
    layer. Those values control how much soluble P leaves the profile by runoff, percolation,
    and tile drainage for the active HRU.
  soil_module: soil provides the layer geometry and water/percolation state that drive the
    phosphorus transport formulas. Layer count, depth, bulk density, stored water, and percolation
    all enter the runoff, leaching, and tile-drain calculations.
  output_landscape_module: hls_d is the daily landscape-loss output record. nut_solp writes
    the computed soluble P losses there so downstream reporting can access the HRU's runoff,
    bottom-leaching, and tile-drain phosphorus losses for the day.
  hydrograph_module: ht1 carries the soluble phosphorus mass routed into the HRU from surface
    runon. nut_solp adds ht1%solp into the top soil layer before computing current-day soluble
    P losses.
  utils: utils matters because nut_solp calls exp_w for the exponential attenuation term in
    the leaching and tile-drain calculations. The wrapper provides safe exponential evaluation
    for large negative arguments.
---

<!-- facts:header -->

Updates soluble phosphorus in an HRU soil profile. It adds groundwater and runon P where enabled, then computes daily soluble P losses to runoff, leaching, and tile drainage.

## Bottom Line

nut_solp is the daily phosphorus-movement step for a single HRU. It starts from the current HRU index, updates labile soil P when groundwater-to-soil transfers are active, adds soluble P from runon, then partitions soluble P out of the top soil layer to surface runoff, percolation to lower layers, tile drainage, and bottom-layer leaching.

The routine also records the resulting losses in the landscape output array and, when gwflow is active, copies the bottom-layer leaching loss into gwflow_percsol for groundwater solute routing. Its results therefore feed both nutrient accounting in the HRU and downstream water-quality routing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

nut_solp runs during HRU daily phosphorus bookkeeping after hru_control has finished the day's water and HRU setup and just before later nutrient/salt routing steps continue. hru_control prepares the active HRU index, runoff, percolation-related state, and management context, and the outputs from nut_solp are then used by landscape reporting and groundwater solute routing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | If groundwater-to-soil solute transfer is enabled, loop through every soil layer and add the layer-specific groundwater phosphorus mass from hru_soil into soil1(j)%mp(jj)%lab, while also accumulating that mass in gwsoilp(j) for the HRU total. |
| 2. reset outputs | Clear the daily landscape loss accumulators for soluble runoff P, bottom-layer leaching P, and tile-flow P before computing today's values. |
| 3. add runon | Add soluble phosphorus routed in from surface runon, ht1%solp, into the top soil layer so the subsequent loss calculations use the updated surface-layer pool. |
| 4. compute runoff loss | Compute soluble P loss from the surface layer with a runoff equation using soil bulk density, surface-layer depth, the HRU phosphorus partition coefficient, and surfq; bound the loss between zero and the available surface pool, store it in hls_d(j)%surqsolp, and subtract it from the top-layer labile P pool. |
| 5. loop | Loop through each soil layer to compute percolation-based phosphorus movement and, separately, tile-drain phosphorus loss where the layer matches the HRU drainage layer. |
| 6. skip septic layer | For layers that are not the septic-system layer, compute a leaching coefficient from layer percolation, water stored in the layer, bulk density, and pperco; use exp_w to convert that coefficient into a phosphorus loss, cap the loss at the available labile P, and subtract it from the current layer. |
| 7. route bottom or down | If the current layer is the bottom layer, record the computed leaching amount as the daily bottom-leached soluble P loss; otherwise add the leached phosphorus to the next deeper layer's labile P pool. |
| 8. compute tile loss | If the current layer is the HRU tile-drain layer, compute an additional phosphorus loss using qtile instead of percolation, bound it to the available layer pool, subtract it from the layer, and store it as the daily tile-labile P loss. |
| 9. store gwflow export | When groundwater flow and groundwater solute routing are both active, copy the bottom-layer leaching amount into gwflow_percsol(j,2) so the groundwater module can use the soluble phosphorus percolation loss. |
| 10. return | Return to the caller after updating the HRU soil phosphorus pools and daily loss outputs. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mp(jj)%lab, soil1(j)%mp(1)%lab, soil1(j)%mp(ly)%lab, soil1(j)%mp(ly+1)%lab` |
| [sym:gwflow_module] | `gw_soil_flag, gw_solute_flag, hru_soil, gwflow_percsol` | `gw_soil_flag, gw_solute_flag, hru_soil, gwflow_percsol` |
| [sym:hru_module] | `hru, surqsolp, gwsoilp, surfq, i_sep, ihru, qtile` | `hru(j)%nut%phoskd, hru(j)%nut%pperco, hru(j)%lumv%ldrain` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(1)%bd, soil(j)%phys(1)%d, soil(j)%ly(ly)%prk, soil(j)%phys(ly)%st, soil(j)%phys(ly)%bd` |
| [sym:output_landscape_module] | `hls_d` | `hls_d(j)%surqsolp, hls_d(j)%lchlabp, hls_d(j)%tilelabp` |
| [sym:hydrograph_module] | `ht1` | `ht1%solp` |
| [sym:utils] | `exp_w` | `exp_w` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil1(j)%mp(jj)%lab` | When gw_soil_flag.eq.1 and gw_solute_flag == 1, for every soil layer jj in 1..soil(j)%nly. | The routine adds groundwater-delivered phosphorus mass to each layer's labile pool so the HRU soil profile reflects groundwater-to-soil solute exchange before runoff and leaching are computed. |
| `gwsoilp(j)` | When gw_soil_flag.eq.1 and gw_solute_flag == 1, inside the loop over soil layers. | The routine accumulates the groundwater-to-soil phosphorus input as an HRU total so later accounting can report how much phosphorus entered the soil profile from groundwater. |
| `hls_d(j)%surqsolp` | Always after the groundwater transfer and before soluble P calculations. | The routine stores the computed daily soluble phosphorus loss to surface runoff for the HRU in the landscape output record. |
| `hls_d(j)%lchlabp` | When the percolation loop reaches the bottom soil layer and the layer is not excluded by i_sep(j). | The routine records the soluble phosphorus amount leaving the bottom of the soil profile by leaching so downstream reporting and groundwater routing can use it. |
| `hls_d(j)%tilelabp` | When the current layer equals hru(j)%lumv%ldrain and the layer is not excluded by i_sep(j). | The routine records the soluble phosphorus amount leaving through tile drainage for the HRU's drainage layer. |
| `soil1(j)%mp(1)%lab` | At the start of the runoff calculation, after adding ht1%solp to the surface layer. | The top-layer labile phosphorus pool is increased by incoming runon phosphorus so the surface runoff loss is computed from the updated pool. |
| `surqsolp(j)` | Always, after the surface runoff formula is evaluated. | The routine writes the computed soluble phosphorus export in surface runoff to the HRU output array. |
| `soil1(j)%mp(ly)%lab` | When ly is not the septic layer i_sep(j), for each layer in the percolation loop. | The current layer's labile phosphorus pool is reduced by the amount leached downward from that layer. |
| `soil1(j)%mp(ly+1)%lab` | When ly is not the bottom layer and leaching occurs. | The leached phosphorus is added to the next deeper soil layer so phosphorus is conserved within the profile as it moves downward. |
| `gwflow_percsol(j,2)` | When bsn_cc%gwflow == 1 and gw_solute_flag == 1 after the bottom-layer leaching calculation. | The routine copies the profile leaching loss into the groundwater-routing array so the gwflow module can transport soluble phosphorus through the groundwater system. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:2.4.1 | Soluble P leaching from soil layer | $P_{perc}=\frac{P_{solution,surf}*w_{perc,surf}}{10*\rho_b*depth_{surf}*k_{d,perc}}$ | Verified against SWAT+ 62.0.0 (nut_solp.f90:75). P percolation (same phoskd structure) |
| 4:2.3.1 | P_surf = P_sol*Q_surf/(rho_b*depth*k_d) | $P_{surf}=\frac{P_{solution,surf}*Q_{surf}}{\rho_b*depth_{surf}*k_{d,surf}}$ | Verified against SWAT+ 62.0.0 (nut_solp.f90:58). surqsolp = lab*surfq/(bd*d*phoskd + 1.)` — exact |

## Lineage

`nut_solp.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `1e02118` (2026-01-05, "Add instructions on compiling with dynamic lib + fix floating error"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `nut_solp.f90` are listed.

- `1e02118` (2026-01-05) — Add instructions on compiling with dynamic lib + fix floating error
- `f797125` (2025-02-06) — Replaced bsn_prm%phoskd and bsn_prm%pperco with hru(j)%nut%phoskd and hru(j)%nut%pperco in three sections: 1. Soluble P lost in surface runo…
- `f1e61a3` (2024-10-08) — fixed tabs
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_solp' has no extracted documentation comment.
- utils reference was not resolved to a specific imported helper beyond exp_w in the provided context.
- algorithm_steps revised: expanded the core flow into 10 steps to reflect the distinct reset, runoff, leaching, tile, and gwflow export operations visible in the source.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
