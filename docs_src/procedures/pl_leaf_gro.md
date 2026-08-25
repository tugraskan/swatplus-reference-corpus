---
kind: procedure
symbol: pl_leaf_gro
title: pl_leaf_gro
status: filled
source_hash: 4106644c59149979
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru` so the routine can address the current basin plant community
    entry in `pcom(j)`.
  idp: Plant database index taken from `pcom(j)%plcur(ipl)%idplt`; it selects the species/parameter
    record in `plcp` and `pldb` for the active plant.
  f: Annual fraction of maximum LAI reached from the current heat-unit accumulation. It is
    also reused as the canopy-height fraction for annual plants.
  f_p: Perennial fraction of maximum LAI reached from perennial heat-unit accumulation. It
    is used to size canopy height for perennial plants.
  ff: The incremental change in the LAI fraction relative to the previous stored transfer
    fraction (`f - laimxfr`); it becomes the driver for leaf-area increase after growth gating.
  deltalai: Daily change applied to LAI after water-stress reduction, canopy-growth limiting,
    and competition adjustment.
  laimax: The maximum LAI allowed for the current plant on this day. It is set from potential
    LAI and reduced for perennial trees using years-to-maturity scaling.
  lai_exp: Intermediate exponent used to scale perennial maximum LAI from the current years-to-maturity
    ratio through `pldb(idp)%laixco_tree`.
  rto_lin: 'Linear years-to-maturity ratio for perennial plants: current year of maturation
    divided by `mat_yrs`.'
  rto: 'Log-scaled growth ratio used twice: first to build the perennial LAI exponent, then
    later as the plant-competition weighting factor for LAI increment.'
  sumlaiht: Competition denominator built by summing LAI multiplied by canopy height across
    all plants in the community, used to apportion the LAI increment.
  exponent: Guarded exponent argument for the perennial `Exp(...)` term; it is clamped to
    avoid underflow before evaluating the heat-unit sigmoid.
  jpl: Loop counter over plants in the community when summing the LAI-height competition term.
uses:
  plant_data_module: The plant database module supplies the species-specific parameters that
    control leaf development and canopy scaling. `plcp(idp)%leaf1` and `%leaf2` shape the
    LAI fraction curves, while `pldb(idp)%dlai`, `%typ`, `%laixco_tree`, and `%chtmx` determine
    when growth is active, whether the plant is perennial, how perennial LAI is scaled, and
    the maximum canopy height.
  basin_module: The basin module is included because this routine runs in the basin-wide growth
    sequence and relies on basin-level model state to participate in the active simulation
    context, even though no specific basin variable was extracted into the line-by-line logic
    here.
  hru_module: The HRU module provides the current HRU index and active plant slot. `ihru`
    chooses the plant community to update, and `ipl` selects the current plant within that
    community.
  plant_module: The plant module holds the mutable plant status, growth, and stress records
    that this routine updates. `pcom(j)` provides the current plant's accumulated heat units,
    growth history, canopy state, community size, and water-stress factor needed to compute
    and store leaf-area and height changes.
  carbon_module: The carbon module matters because leaf growth is part of the broader biomass
    and carbon allocation workflow, even though no direct carbon state symbol was extracted
    in this routine's visible equations.
  organic_mineral_mass_module: The organic/mineral mass module matters because plant leaf
    growth is coupled to nutrient and residue-related plant-process bookkeeping elsewhere
    in the growth sequence, although no direct symbol from that module appears in the extracted
    line-by-line calculations.
---

<!-- facts:header -->

Updates plant leaf area growth and canopy height for the active plant in the current HRU. It computes LAI development from accumulated heat units, applies water-stress-limited leaf growth, and stores the updated leaf-growth state back into the plant community.

## Bottom Line

pl_leaf_gro advances the current plant's leaf development on a daily growth step. It uses the plant's accumulated heat units, plant database shape parameters, and plant-community growth state to update the fraction of maximum LAI reached, canopy height, current LAI, and the values that mark when leaf decline begins.

The routine only acts when the current plant is still in its growth window (`phuacc < dlai`). For perennial plants it also adjusts maximum LAI using years-to-maturity scaling and uses perennial heat-unit accumulation to shape growth and canopy height.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the daily plant-growth workflow after `pl_biomass_gro` and `pl_root_gro` and before leaf senescence, seed growth, and partitioning in `pl_grow`. Its results feed later growth and partition routines by updating the plant's LAI, canopy height, and leaf-growth bookkeeping for the current day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. compute annual LAI fraction | Compute the annual fraction of maximum LAI from the current heat-unit fraction, store the previous transfer fraction in `ff`, and update `pcom(j)%plg(ipl)%laimxfr` to the new annual fraction. |
| 2. guard perennial exponent and compute perennial fraction | Build the perennial heat-unit exponent from `leaf1` and `leaf2`, clamp it to avoid underflow, and evaluate the perennial LAI fraction `f_p` from the guarded exponent. |
| 3. enter leaf-growth window | Only proceed with LAI and canopy updates when the plant's accumulated heat units are still below the decline threshold `dlai`. |
| 4. initialize growth limits | Reset the day-specific maximum LAI and increment to zero before calculating the plant's allowed leaf-area growth. |
| 5. compute perennial LAI cap | For perennial plants, force the current year-of-maturity counter to at least 1, compute the years-to-maturity ratio, transform it with `alog10`, and scale potential LAI by `laixco_tree`, capped at the potential LAI itself. |
| 6. use potential LAI for nonperennials | For annual or nonperennial plants, set the maximum allowed LAI directly to the potential LAI from the current plant status. |
| 7. compute canopy height | Set canopy height from the appropriate LAI fraction: use `f_p` for perennial plants and `f` for other plants, both scaled by the species maximum canopy height. |
| 8. set perennial leaf fraction | For perennial plants, set the above-ground leaf fraction to a fixed tree value of 0.03. |
| 9. clamp current LAI to cap | If current LAI already exceeds the calculated maximum, clip it down to `laimax` before applying any increment. |
| 10. compute stressed LAI increment | Calculate the day’s LAI increment from the growth fraction, maximum LAI, current LAI deficit, and square root of water stress. |
| 11. compute competition weighting | Sum LAI-height products over all plants in the community and convert that total into a relative weighting factor for the current plant; default to 1.0 when the total is effectively zero. |
| 12. apply competition and update LAI | Scale the increment by the competition weight and add it to the current plant LAI. |
| 13. enforce post-update LAI cap and save state | Clip LAI back to `laimax` if needed, copy the final LAI to `olai`, and save the current heat-unit fraction in `dphu`. |
| 14. return | Exit the routine after updating the current plant's leaf-growth state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `plcp, pldb` | `plcp(idp)%leaf2, plcp(idp)%leaf1, pldb(idp)%dlai, pldb(idp)%typ, pldb(idp)%laixco_tree, pldb(idp)%chtmx` |
| [sym:basin_module] | `ihru, ipl` |  |
| [sym:hru_module] | `ihru, ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plg(ipl)%laimxfr, pcom(j)%plcur(ipl)%phuacc_p, pcom(j)%plcur(ipl)%curyr_mat, pcom(j)%plcur(ipl)%lai_pot, pcom(j)%plg(ipl)%cht, pcom(j)%plg(ipl)%leaf_frac, pcom(j)%plg(ipl)%lai, pcom(j)%npl, pcom(j)%plg(jpl)%cht, pcom(j)%plg(ipl)%olai, pcom(j)%plg(ipl)%dphu` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plg(ipl)%laimxfr` | When the current plant's accumulated heat units are below `pldb(idp)%dlai` and the new annual fraction `f` is computed. | `pcom(j)%plg(ipl)%laimxfr` is updated to the current annual LAI fraction so later calls can measure how much the plant has advanced since the previous step. |
| `pcom(j)%plg(ipl)%cht` | When the current plant is inside the growth window and canopy height is recalculated. | `pcom(j)%plg(ipl)%cht` is assigned a species maximum height scaled by the appropriate LAI fraction, so downstream growth logic uses the current canopy height. |
| `pcom(j)%plg(ipl)%leaf_frac` | When the plant is perennial and the routine enters the growth window. | `pcom(j)%plg(ipl)%leaf_frac` is forced to 0.03 for perennial plants, representing the fixed tree leaf share used by later biomass partitioning. |
| `pcom(j)%plg(ipl)%lai` | When the current plant remains below the leaf-decline threshold `dlai`. | `pcom(j)%plg(ipl)%lai` is limited, incremented, and re-limited so it reflects the current day's water-stressed leaf-area growth. |
| `pcom(j)%plg(ipl)%olai` | When the growth-window logic runs after LAI is updated. | `pcom(j)%plg(ipl)%olai` is copied from the final LAI so the routine preserves the leaf area value used to mark the onset of decline. |
| `pcom(j)%plg(ipl)%dphu` | When the growth-window logic runs after LAI is updated. | `pcom(j)%plg(ipl)%dphu` is set to the current accumulated heat units so the plant stores the heat-unit level associated with the current leaf state. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.1.10 | Fraction of maximum LAI from PHU fraction | $fr_{LAImx}=\frac{fr_{PHU}}{fr_{PHU}+exp(\Box_1 - \Box_2 * fr_{PHU})}$ | Verified against SWAT+ 62.0.0 (pl_leaf_gro.f90:86). f = phuacc/(phuacc+Exp(leaf1-leaf2*phuacc))` — fr_LAImx |
| 5:2.1.14 | Canopy height from LAI fraction | $h_c=h_{c,mx}*\sqrt{fr_{LAImx}}$ | Verified against SWAT+ 62.0.0 (pl_leaf_gro.f90:123). (cht = chtmx*Sqrt(f_p)) |
| 5:2.1.15 | Tree canopy height from years to full development | $h_c=h_{c,mx}*(\frac{yr_{cur}}{yr_{fulldev}})$ | Verified against SWAT+ 62.0.0 (pl_leaf_gro.f90:112). tree height via maturity ratio `curyr_mat/mat_yrs |
| 5:2.1.18 | LAI update | $LAI_i=LAI_{i-1}+\Delta LAI_{i}$ | Verified against SWAT+ 62.0.0 (pl_leaf_gro.f90:147). lai = lai + deltalai |
| 5:3.2.2 | Actual LAI increment | $\Delta LAI _{act,i}=\Delta LAI_i*\sqrt{\gamma _{reg}}$ | Verified against SWAT+ 62.0.0 (pl_leaf_gro.f90:135). deltalai = ff*laimax*(1-Exp(5*(lai-laimax)))*Sqrt(strsw)` — ΔLAI·√γ_reg |
| 5:2.1.9 | Tree biomass scaling by years to full development | $bio_{annual}=1000*(\frac{yr_{cur}}{yr_{fulldev}})*bio_{fulldev}$ | Verified against SWAT+ 62.0.0 (pl_leaf_gro.f90:112). tree development scaled by maturity ratio `curyr_mat/mat_yrs |

## Lineage

Resolved lineage shows the routine was added in df07e3f with the original purpose and growth logic already present. In 39fabde, the local variables were initialized and a temporary underflow guard was introduced for the perennial `Exp(...)` calculation. In e18817a, that guard was briefly implemented with `tmp_calc` and then removed so the direct expression was restored. In fd90e36, the perennial exponential argument was reworked again by adding `exponent`, clamping it at -16.0, and evaluating `f_p` from the guarded value.

- df07e3f introduced `pl_leaf_gro` with the leaf-growth, canopy-height, LAI-update, and state-bookkeeping workflow that still anchors the routine.
- 39fabde initialized locals and added an underflow check around the perennial `Exp(...)` term so the heat-unit fraction calculation would be numerically safer.
- e18817a temporarily reverted the `tmp_calc` guard back to the direct exponential expression after the earlier underflow workaround.
- fd90e36 added the current `exponent` variable, clamped it to -16.0, and used that guarded value for the perennial LAI-fraction computation.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_leaf_gro' has no extracted documentation comment.
- algorithm_steps revised: reordered and rephrased the source-line steps to match the visible control flow and to keep each step tied to real line spans.
- The `basin_module`, `carbon_module`, and `organic_mineral_mass_module` imports are not resolved to specific symbols in the extracted line-by-line usage, so their descriptions are intentionally high level.
- Source line 135 applies `sqrt(pcom(j)%plstr(ipl)%strsw)`; the GitBook note in the packet summarizes this as water-stress limitation, not the broader combined stress term.
