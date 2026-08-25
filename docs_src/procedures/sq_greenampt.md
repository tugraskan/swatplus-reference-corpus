---
kind: procedure
symbol: sq_greenampt
title: sq_greenampt
status: filled
source_hash: bb545a08825bdee9
version_label: SWAT+ 62.0.0
locals:
  j: HRU index selected from the current model HRU pointer (`ihru`); it identifies which `hru(j)`,
    `soil(j)`, and related per-HRU arrays this call updates.
  k: Loop counter over the subdaily time steps in the current day (`1..time%step`).
  adj_hc: Effective hydraulic conductivity for the current time step, computed from soil conductivity
    and curve number and then floored at a small positive value.
  dthet: Initial volumetric moisture deficit at the wetting front; used to form the suction
    term for Green-Ampt infiltration.
  soilw: Current soil profile water used to derive the moisture deficit; it is limited to
    just below field capacity when the profile is at or above it.
  psidt: Wetting-front suction term multiplied by moisture deficit; it drives the Green-Ampt
    infiltration equation.
  tst: Trial cumulative infiltration value used in the successive-substitution loop that solves
    the implicit Green-Ampt equation.
  f1: Next successive-substitution estimate of cumulative infiltration; compared against `tst`
    until convergence.
  ulu: Urban landuse code for the current HRU; if it is positive, the routine applies the
    urban impervious runoff branch.
  cuminf: Running cumulative infiltration for the day, indexed by subdaily step, with element
    0 used as the previous-step carryover.
  cumr: Running cumulative rainfall for the day, accumulated from `w%ts(k)` at each subdaily
    step.
  excum: Running cumulative runoff for the day, used to track excess rainfall across subdaily
    steps.
  exinc: Incremental runoff generated during the current subdaily step.
  rateinf: Infiltration capacity for each subdaily step; it is used to decide whether all
    rain infiltrates or an implicit Green-Ampt solve is needed.
  rintns: Subdaily rainfall intensity in mm/hr, computed from precipitation depth and `time%dtm`.
  swdt: Intermediate soil-water-plus-infiltration total used to update the daily curve number
    estimate.
  sw_fac: Exponent argument used in the daily curve-number update formula; it is clamped to
    avoid extreme values.
  r2: Intermediate curve-number-related value used to compute `cnday(j)` and adjusted for
    frozen soil conditions.
uses:
  urban_data_module: The urban database provides the impervious fraction for the current urban
    landuse (`urbdb(ulu)%fcimp`), which controls how much of the runoff is routed through
    the urban impervious branch and reduced on the pervious portion.
  climate_module: The weather daily and station state supply the current subdaily precipitation
    series (`w%ts(k)`) and the station-linked daily series used for impervious runoff (`wst(iwst)`),
    so they determine rainfall intensity and urban runoff generation.
  basin_module: The basin parameters provide global controls for urban initial abstraction
    (`bsn_prm%urb_init_abst`) and frozen-soil runoff adjustment (`bsn_prm%cn_froz`), both
    of which change how infiltration and curve number respond in this routine.
  hydrograph_module: The hydrograph timestep storage provides the subdaily step structure
    (`ts`) and the current weather-station index (`iwst`), which are needed to align runoff
    calculations with routing time steps and station rainfall data.
  hru_module: The HRU state contains the current HRU identity and all runoff/infiltration
    outputs and carryover fields for this calculation, including urban landuse, prior infiltration
    trigger, runoff accumulators, and the daily curve-number and runoff totals.
  soil_module: The soil profile supplies the hydraulic conductivity, porosity, current soil
    water, field-capacity sum, and temperature needed to compute the Green-Ampt deficit, infiltration
    capacity, and frozen-soil curve-number adjustment.
  time_module: The time state determines the number of subdaily iterations and the rainfall/routing
    timestep length, which control the size of the daily arrays and the conversion from precipitation
    depth to rainfall intensity.
---

<!-- facts:header -->

Computes subdaily surface runoff and infiltration for one HRU using the Green-Ampt method, including urban impervious runoff handling.

## Bottom Line

sq_greenampt runs the Green-Ampt runoff/infiltration calculation for the current HRU and day. It steps through each subdaily precipitation interval, updates cumulative rainfall and infiltration, and computes subdaily runoff, daily runoff, and the next infiltration capacity.

It also applies urban-area adjustments when the HRU has an urban landuse, including impervious-area runoff, initial abstraction, and carryover of the infiltration trigger between days. The routine finishes by updating the day’s curve number estimate from current soil water, with a frozen-soil adjustment when needed.

## Arguments

<!-- facts:arguments -->

## Where It Fits

sq_volq calls this routine when Green-Ampt runoff is enabled (`bsn_cc%gampt /= 0`). It runs after upstream weather, soil, HRU, and time state have been prepared for the current day, and its results feed the HRU’s subdaily runoff totals, urban runoff terms, the next-day infiltration trigger, and the updated daily curve number used by later hydrologic calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize HRU and daily arrays. | Select the current HRU (`j = ihru`), read its urban landuse code, and clear the day’s cumulative rainfall, infiltration, runoff, incremental runoff, infiltration-rate, and rainfall-intensity arrays. |
| 2. Set the starting moisture deficit and carryover infiltration state. | If the HRU is flagged as carrying a rainfall event across midnight, restore the previous infiltration rate and force a tiny moisture deficit; otherwise derive soil water, moisture deficit, and initial infiltration capacity from current soil water and field capacity. |
| 3. Loop over the subdaily precipitation steps. | Process each rainfall/routing interval for the current day. |
| 4. Compute soil and rainfall forcing for the step. | Update effective hydraulic conductivity from soil K and curve number, accumulate rainfall depth, and convert rainfall depth to intensity using the model timestep. |
| 5. Route all rainfall through infiltration when capacity exceeds intensity. | When infiltration capacity is at least rainfall intensity, add the full step rainfall to cumulative infiltration and carry forward any previous excess runoff without creating new excess runoff. |
| 6. Solve the implicit Green-Ampt equation when rainfall exceeds capacity. | Use successive substitution to solve cumulative infiltration, then compute cumulative excess rainfall, incremental runoff, and subdaily HRU runoff for the step. |
| 7. Apply the urban impervious-area adjustment when the HRU is urban. | Reduce or restore urban initial abstraction depending on rainfall intensity, split pervious runoff by impervious fraction, compute impervious runoff from the weather-station rainfall, and clip negative impervious runoff to zero. |
| 8. Accumulate daily runoff and update the next infiltration rate. | Add the step runoff components into the daily runoff total and compute the next-step infiltration rate from the current cumulative infiltration. |
| 9. Update the day’s curve number estimate. | Combine current soil water and cumulative infiltration into a curve-number state, clamp the exponent term, adjust for frozen soil temperature if needed, enforce a minimum curve-number-derived bound, and convert the result to `cnday(j)`. |
| 10. Set the next-day carryover flag when rainfall occurred. | If the day’s precipitation sum exceeds the event threshold, mark the HRU as carrying a rainfall event over midnight and save the final infiltration rate for reuse on the next day. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:urban_data_module] | `urbdb` |  |
| [sym:climate_module] | `w, wst` | `w%ts(k), w%ts` |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%urb_init_abst, bsn_prm%cn_froz` |
| [sym:hydrograph_module] | `ts, iwst` |  |
| [sym:hru_module] | `hru, swtrg, rateinf_prev, wfsh, hhqday, urb_abstinit, ubnrunoff, hhsurfq, surfq, wrt, smx, cnday, ihru, pet_day` | `hru(j)%luse%urb_lu` |
| [sym:soil_module] | `soil` | `soil(j)%phys(1)%por, soil(j)%sw, soil(j)%sumfc, soil(j)%phys(1)%k, soil(j)%phys(2)%tmp` |
| [sym:time_module] | `time` | `time%step, time%dtm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `swtrg(j)` | When `Sum(w%ts) > 12.` at the end of the day. | `swtrg(j)` is set to 1 to remember that rainfall is still considered active over midnight, so the next call starts from carryover-event logic instead of a fresh-day reset. |
| `rateinf_prev(j)` | When `Sum(w%ts) > 12.` at the end of the day. | `rateinf_prev(j)` stores the final infiltration rate from the current day so the next day can resume a continuing rainfall event with the prior infiltration capacity. |
| `hhqday(j,k)` | Whenever the successive-substitution solve converges in the excess-rainfall branch for a subdaily step (`rateinf(k) < rintns(k)` and the `Abs(f1 - tst) <= 0.001` test passes). | `hhqday(j,k)` is assigned the incremental runoff generated in that subdaily interval, so the HRU keeps a per-step runoff record for later routing and aggregation. |
| `urb_abstinit(j)` | When `ulu > 0` and `rintns(k) > 0.017` or otherwise during the urban branch for a step. | `urb_abstinit(j)` is decreased by rainfall during higher-intensity rain or increased by a PET-based increment during low-intensity periods, so the urban initial abstraction tracks storm progression. |
| `ubnrunoff(k)` | When `ulu > 0` and the routine computes impervious runoff for the current step. | `ubnrunoff(k)` stores runoff from the impervious urban fraction after subtracting initial abstraction, and is clipped to zero if abstraction exceeds rainfall. |
| `hhsurfq(j,k)` | For every subdaily step after the pervious and impervious runoff pieces are combined. | `hhsurfq(j,k)` becomes the total subdaily surface runoff for the HRU, combining pervious runoff and urban impervious runoff before daily accumulation. |
| `surfq(j)` | For every subdaily step after `hhsurfq(j,k)` is computed. | `surfq(j)` accumulates the day’s total surface runoff across all subdaily steps. |
| `cnday(j)` | For every subdaily step, after soil water, cumulative infiltration, and frozen-soil checks are applied. | `cnday(j)` is recalculated as the day’s adjusted curve number, so later hydrologic work uses the updated runoff potential. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:1.2.1 | Green-Ampt infiltration rate | $f_{inf,t}=K_e*(1+\frac{\Psi_{wf}*\Delta\theta_v}{F_{inf,t}})$ | rateinf(k+1) = adj_hc*(psidt/(cuminf(k)+1e-6) + 1). |
| 2:1.2.2 | Cumulative infiltration when all rain infiltrates | $F_{inf,t}=F_{inf,t-1}+R_{\Delta t}$ | When rainfall intensity is below infiltration capacity, cumulative infiltration is incremented by the full time-step rainfall. |
| 2:1.2.3 | Implicit Green-Ampt cumulative infiltration update | $F_{inf,t}=F_{inf,t-1}+K_e*\Delta t+ \Psi_{wf}*\Delta\theta_v*ln[\frac{F_{inf,t}+\Psi_{wf}*\Delta\theta_v}{F_{inf,t-1}+\Psi_{wf}*\Delta\theta_v}]$ | Successive substitution solves the implicit cumulative infiltration equation. |
| 2:1.2.4 | Effective hydraulic conductivity | $K_e=\frac{56.82*K_{sat}^{0.286}}{1+0.051*exp(0.062*CN)}-2$ | adj_hc = 56.82*Ksat^0.286/(1 + 0.051*exp(0.062*CN)) - 2, floored at 0.001. |
| 2:1.2.6 | Initial moisture deficit | $\Delta\theta_v=(1-\frac{SW}{FC})*(0.95*\phi_{soil})$ | dthet = (1 - soilw/sumfc)*por*0.95 matches theory (1 - SW/FC)*0.95*phi term-for-term; theory SW and FC are both whole-profile quantities, so soil%sw and soil%sumfc ARE the theory variables (not a single-layer substitution as previously noted). Only deviation is a numerical guard capping soilw at 0.999*sumfc so dthet stays positive. Reclassified from 'implemented (modified)'; see section_2_1_surface_runoff.md. |
| 2:1.2.7 | Carryover-event minimum moisture deficit | $\Delta\theta_v=0.001*(0.95*\phi_{soil})$ | When rainfall continues across midnight, dthet is reset to 0.001*por*0.95. |

## Lineage

Four resolved commits changed `sq_greenampt`. The initial addition in df07e3f created the procedure with Green-Ampt runoff logic, urban handling, and daily curve-number updates. 39fabde initialized the local scalar variables and kept the original logic intact. 889136d only corrected a comment typo in the runoff label. eb76cac updated the hru_module import list, expanded the local arrays to `0:time%step+1`, removed an inline conductivity initialization, and added the new subdaily curve-number update variables and formulas.

- df07e3f introduced the routine and its Green-Ampt runoff, urban impervious runoff, and daily curve-number calculations.
- 39fabde changed local scalar declarations to initialize `j`, `k`, `adj_hc`, `dthet`, `soilw`, `psidt`, `tst`, `f1`, and `ulu` at zero.
- 889136d only corrected a comment from 'pervious area' to 'previous area' and did not change behavior.
- eb76cac expanded the working arrays to include indices `0:time%step+1`, added `wrt` and `smx` to the imported HRU state, removed the inline conductivity precompute, and added the soil-water/curve-number update block that recalculates `cnday(j)` each step.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_greenampt' has no extracted documentation comment.
