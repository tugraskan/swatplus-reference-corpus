---
kind: procedure
symbol: swr_percmicro
title: swr_percmicro
status: filled
source_hash: 90f7755677b047e3
version_label: SWAT+ 62.0.0
args:
  ly1: Layer index within the current HRU. `ly1` selects which soil layer `swr_percmicro`
    evaluates, and it determines whether the routine computes normal layer drainage, septic-layer
    adjustments, or bottom-layer percolation limits.
locals:
  j: '`j` stores the current HRU index copied from `ihru` so the routine can read and update
    the correct `hru` and `soil` entries.'
  ho: '`ho` holds the intermediate water-table height / storage term derived from `sw_excess`
    and the layer’s drainable porosity before lateral flow is computed.'
  ratio: '`ratio` stores the split between seepage and lateral flow when the routine has to
    scale both fluxes down to fit within available excess water.'
  sol_k_sep: '`sol_k_sep` stores a septic-layer conductivity cap derived from the layer’s
    hydraulic properties; it is used to limit seepage from the biozone when an active septic
    system is present.'
uses:
  septic_data_module: '`septic_data_module` supplies septic-system operation flags through
    `sep(isep)%opt`, which this routine uses to decide whether to cap seepage for an active
    system or force a failed-system layer to a very large resistance.'
  hru_module: '`hru_module` provides the current HRU context and the shared flux/state variables
    that this routine reads and updates. The HRU topology and hydrology fields set the lateral-flow
    calculation, while `sepday`, `latlyr`, `lyrtile`, `bz_perc`, `i_sep`, `isep`, and `sw_excess`
    carry the drainage results back to the daily water balance.'
  soil_module: '`soil_module` holds the soil-layer properties that control whether water can
    move and how fast it moves. Temperature, saturation, field capacity, thickness, saturated
    conductivity, and stored water are all needed to compute lateral flow, seepage travel
    time, and septic-layer limits for the selected layer.'
---

<!-- facts:header -->

Computes daily micro-scale percolation, lateral subsurface flow, and septic-related seepage limits for a single soil layer in the current HRU.

## Bottom Line

swr_percmicro evaluates one soil layer for the active HRU after `swr_percmain` has identified excess water. It skips frozen layers, computes a hillslope lateral-flow term and a percolation travel time, then limits seepage so the layer does not drain more water than is available.

The routine also applies septic-system rules when the layer is the septic layer: it caps seepage for an active septic system or suppresses it for a failing one, and it writes the resulting `sepday`, `latlyr`, `lyrtile`, and `bz_perc` values back to shared HRU state for later storage updates and summary accounting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the per-layer loop in `swr_percmain`, after that driver has initialized `sepday`, `latlyr`, and `lyrtile` and confirmed that `sw_excess` is large enough to justify a call. Its outputs feed the subsequent update `soil(j)%phys(j1)%st = soil(j)%phys(j1)%st - sepday - latlyr - lyrtile`, so downstream soil-water storage, HRU water balance, and summary seepage totals depend on its results.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the active HRU and stop for frozen soil | Copies `ihru` into local `j`, then exits immediately with `sepday = 0.` if the selected layer temperature is at or below freezing, because no water movement is allowed in frozen soil. |
| 2. Compute the hillslope storage term for lateral flow | Builds `ho` from `sw_excess` and the layer’s drainable porosity. If saturated water content is not above field capacity, `ho` is set to zero; otherwise it is computed as `2. * sw_excess / ((ul - fc) / thick)`. |
| 3. Compute layer lateral flow | Sets `latlyr` to zero for the top layer and otherwise computes lateral subsurface flow from `latq_co`, `ho`, soil conductivity, slope, and slope length. The result is clipped to the range `[0, sw_excess]`. |
| 4. Compute the base seepage travel time | Calculates `soil(j)%phys(ly1)%hk` as `(ul - fc) / k`, which becomes the layer’s hydraulic time constant for the seepage equation. |
| 5. Apply septic-layer adjustments when the current layer is the septic layer | If `ly1` matches the septic-layer index, the routine checks `sep(isep)%opt`. For an active system it derives `sol_k_sep`, bounds it between `1.e-6` and the layer’s conductivity, and uses it to adjust `hk`; for a failing system it assigns a very large `hk` so seepage is effectively suppressed. |
| 6. Enforce a minimum hydraulic time constant | Raises `soil(j)%phys(ly1)%hk` to at least `2.` so the seepage equation cannot use an unrealistically small travel time. |
| 7. Compute daily seepage and keep it nonnegative | Computes `sepday` from the layer’s storage above field capacity and the daily exponential drainage term `1. - Exp(-24. / hk)`, then forces the result to be at least zero. |
| 8. Limit septic biozone seepage | When the current layer is the septic layer and the septic system is active, caps `sepday` by `sol_k_sep * 24.` and copies the final value to `bz_perc(j)` for biozone accounting. |
| 9. Reduce seepage in the bottom layer by the percolation limit | If the selected layer is the soil profile bottom, scales `sepday` by `hru(j)%hyd%perco_lim` to limit downward percolation. |
| 10. Enforce the daily mass balance between seepage and lateral flow | If seepage plus lateral flow exceeds `sw_excess`, the routine computes a split ratio and rescales `sepday` and `latlyr` so their sum fits within available excess water. It also prevents `sepday + lyrtile` from exceeding `sw_excess`. |
| 11. Return updated fluxes to the caller | Returns after leaving the updated shared state variables in place for the caller to subtract from soil storage. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:septic_data_module] | `sep` | `sep(isep)%opt` |
| [sym:hru_module] | `hru, i_sep, bz_perc, ihru, isep, latlyr, lyrtile, sepday, sw_excess` | `hru(j)%hyd%latq_co, hru(j)%topo%slope, hru(j)%topo%lat_len, hru(j)%hyd%perco_lim` |
| [sym:soil_module] | `soil` | `soil(j)%phys(ly1)%tmp, soil(j)%phys(ly1)%ul, soil(j)%phys(ly1)%fc, soil(j)%phys(ly1)%thick, soil(j)%phys(ly1)%k, soil(j)%phys(ly1)%hk, soil(j)%phys(ly1)%st, soil(j)%nly` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sepday` | When `sepday + latlyr > sw_excess` after seepage and lateral flow have been computed. | `sepday` is rescaled so the combined seepage and lateral flow do not exceed the layer’s available excess water. This keeps the daily water balance consistent before the caller removes water from soil storage. |
| `latlyr` | When `ly1 == 1` the routine sets `latlyr = 0.`; otherwise it computes lateral flow from the hillslope formula and later may rescale it if total flux exceeds `sw_excess`. | `latlyr` represents the day’s lateral subsurface flow from the current layer. It is only nonzero below the surface layer and may be reduced to keep the total drainage within available water. |
| `soil(j)%phys(ly1)%hk` | Always, after the base travel-time calculation; and again within septic-layer logic if `ly1 == i_sep(j)`. | `soil(j)%phys(ly1)%hk` is overwritten with the layer’s hydraulic time constant for seepage. The routine first derives it from `(ul - fc) / k`, then modifies it for active or failing septic-system behavior, and finally enforces a minimum value. |
| `bz_perc(j)` | When `ly1 == i_sep(j)` and `sep(isep)%opt == 1`. | `bz_perc(j)` stores the final capped seepage from the septic biozone layer so later HRU-level septic accounting can use the same limited flux. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:3.2.3 | Percolation from excess water | $w_{perc,ly}=SW_{ly,excess}*(1-exp[\frac{-\Delta t}{TT_{perc}}])$ | Verified against SWAT+ 62.0.0 (swr_percmicro.f90:95). sepday = (st-fc)*(1.-Exp(-24./hk))` — storage percolation |
| 2:3.5.1 | Lateral-flow storage relation | $SW_{ly,excess}=\frac{1000*H_o*\phi_d*L_{hill}}{2}$ | Verified against SWAT+ 62.0.0 (swr_percmicro.f90:64). SW_excess↔H_o algebraic inverse of the Ho line |
| 2:3.5.2 | Water-table height above impermeable layer | $H_o=\frac{2*SW_{ly,excess}}{1000*\phi_d*L_{hill}}$ | Verified against SWAT+ 62.0.0 (swr_percmicro.f90:64). ho = 2.*sw_excess/((ul-fc)/thick)` — hillslope storage H_o |
| 2:3.5.3 | Drainable porosity | $\phi_d=\phi_{soil}-\phi_{fc}$ | (ul - fc)/thick is the drainable-porosity term used in the lateral-flow calculation. |
| 2:3.5.6 | Lateral flow from Ho and velocity | $Q_{lat}=24*H_o*v_{lat}$ | Verified against SWAT+ 62.0.0 (swr_percmicro.f90:69). latlyr = latq_co*ho*k*slope/lat_len*.024` — Q_lat=24·H_o·v_lat |
| 2:3.5.7 | Lateral-flow velocity from Ksat and slope angle | $v_{lat}=K_{sat}*sin(\alpha_{hill})$ | Verified against SWAT+ 62.0.0 (swr_percmicro.f90:69). theory's `v_lat=K_sat·sin(α)`; code uses tan/slope, not sin |
| 2:3.5.8 | Lateral-flow velocity from Ksat and slope | $v_{lat}=K_{sat}*tan(\alpha_{hill})=K_{sat}*slp$ | Verified against SWAT+ 62.0.0 (swr_percmicro.f90:69). v_lat = K_sat·slope` (tan form) inside latlyr |
| 2:3.5.9 | Collapsed lateral-flow equation | $Q_{lat}=0.024*(\frac{2*SW_{ly,excess}*K_{sat}*slp}{\phi_d*L_{hill}})$ | Verified against SWAT+ 62.0.0 (swr_percmicro.f90:69). same line, fully combined kinematic-storage lateral flow |

## Lineage

Four resolved commits changed `swr_percmicro`: df07e3f created the routine with its frozen-layer check, lateral-flow computation, septic handling, seepage equation, and mass-balance logic; 94b6dec imported the same routine into the source tree without changing behavior; 39fabde initialized the local variables `j`, `ho`, `ratio`, and `sol_k_sep` to zero; and f1e61a3 only fixed indentation on the septic-layer `if` block.

- df07e3f introduced the full micro-percolation and lateral-flow procedure, including septic-system limits, bottom-layer perco limiting, and the mass-balance adjustment.
- 39fabde changed only local initialization of `j`, `ho`, `ratio`, and `sol_k_sep`; it did not alter the routine’s flow equations.
- f1e61a3 made whitespace-only tab fixes around the septic-layer block and did not change behavior.
- 94b6dec added the routine from the Bitbucket source snapshot; the diff shown does not indicate a functional change beyond importing the file.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'swr_percmicro' has no extracted documentation comment.
