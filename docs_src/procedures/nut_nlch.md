---
kind: procedure
symbol: nut_nlch
title: nut_nlch
status: filled
source_hash: 6ad991cfb8f85fe1
version_label: SWAT+ 62.0.0
uses:
  hru_module: Provides the hydrologic and nutrient routing inputs and receives the computed
    nitrate losses for each pathway.
  organic_mineral_mass_module: Stores the per-layer nitrate pools that are updated as nitrate
    moves between layers and leaves the profile.
  gwflow_module: Adds groundwater-derived nitrate mass into the soil profile before pathway
    losses are computed.
---

<!-- facts:header -->

nut_nlch computes nitrate movement and loss in surface runoff, lateral flow, tile flow, and percolation through the soil profile.

## Bottom Line

nut_nlch is the direct implementation target for the Chapter 4 Nitrate Movement page because it computes surqno3, latno3, tileno3, and percn from the active soil nitrate pools and layer water fluxes.

The routine also updates each soil-layer nitrate pool as those pathway losses are removed and passed downward through the profile.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls nut_nlch after nut_nrain and before nut_solp, so nitrate routing through runoff, lateral flow, tile flow, and percolation is computed before the phosphorus-movement stage of the HRU day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Inject groundwater-derived nitrate when enabled | Adds aquifer-transferred nitrate mass into each soil layer and records the HRU total in gwsoiln(j). |
| Build the mobile-water nitrate concentration | Carries percolated nitrate into each layer, forms the mobile-water volume vv, computes ww, then derives mobile nitrate vno3 and concentration co. |
| Compute surface-runoff nitrate loss | In the first layer, computes surqno3(j) from surface runoff, nperco, and co, limits it to available nitrate, and subtracts it from the first-layer pool. |
| Compute tile-flow nitrate loss | At the drain layer, aggregates nitrate and mobile-water storage from the drain layer to the bottom of the profile, computes tileno3(j), and removes that mass from the contributing layers. |
| Compute lateral-flow and percolation losses | Computes lateral nitrate ssfnlyr and percolation nitrate percnlyr from co, subtracts them from the current layer, accumulates latno3(j), and records bottom-layer percolation in percn(j). |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru; latno3; percn; surqno3; tileno3; surfq; ihru; qtile; gwsoiln` | `HRU nutrient controls, hydrologic pathway flows, and nitrate-loss outputs` |
| [sym:organic_mineral_mass_module] | `soil1` | `mn(:)%no3` |
| [sym:gwflow_module] | `gw_soil_flag; gw_solute_flag; hru_soil` | `aquifer-to-soil nitrate transfer` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `surqno3(j); latno3(j); tileno3(j); percn(j)` | Every call | Stores nitrate losses to surface runoff, lateral flow, tile flow, and bottom-of-profile percolation. |
| `soil1(j)%mn(:)%no3` | Every call | Updates soil-layer nitrate pools after additions from above or groundwater and removals by each transport pathway. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
| 4:2.1.2 |  | $conc_{NO3,mobile}=\frac{NO3_{ly}*(1-exp[\frac{-w_{mobile}}{(1-\theta_e)*SAT_{ly}}])}{w_{mobile}}$ | Verified against SWAT+ 62.0.0 (nut_nlch.f90:88). vno3 = no3*(1.-Exp(ww))`, `co=vno3/vv`; ww=−vv/((1−anion_excl)·ul) — mobile NO3 conc |
| 4:2.5.1 |  | $NO3_{surf}=(NO3'_{surf}+NO3_{surstor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (nut_nlch.f90). (NO3 surf runoff, lag) |

## Lineage

`nut_nlch.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `95d4ff5` (2025-02-06, "Modified nitrate calculation in surface runoff and tile flow to use HRU-specific…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `nut_nlch.f90` are listed.

- `95d4ff5` (2025-02-06) — Modified nitrate calculation in surface runoff and tile flow to use HRU-specific parameters instead of basin parameters: `bsn_prm%nperco` to…
- `9c706fd` (2025-02-03) — Made a correction to case 3 in the cbn_zhang2.f90 to reset the till_eff to 1.0 after 30 days.
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The surface-runoff nitrate pathway is only evaluated in the first soil layer, while tile nitrate can draw from the drain layer through the bottom of the profile.
- The routine clamps ww to -80 to avoid exponential underflow issues in the concentration calculation.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up.
