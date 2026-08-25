---
kind: procedure
symbol: nut_nitvol
title: nut_nitvol
status: filled
source_hash: 0739dfd9d614c9d1
version_label: SWAT+ 62.0.0
locals:
  j: HRU index for the currently processed hydrologic response unit. It is reset, then assigned
    from `ihru` so the routine can access the matching soil and mineral-nitrogen profiles
    for that HRU.
  k: Soil-layer counter used to loop from the surface layer through `soil(j)%nly`. Each iteration
    computes layer-specific nitrification and volatilization losses.
  sw25: Per-layer soil-water threshold set to wilting-point water plus 25% of field-capacity
    water. It is used as the breakpoint that switches the soil-water factor from a linear
    drying response to full activity.
  swwp: Per-layer current soil water above wilting point, built from wilting-point water plus
    stored water. It represents the layer's current moisture status used in the soil-water
    response.
  swf: Soil-water factor for nitrification, ranging from 0 to 1. It scales nitrification activity
    based on how wet the layer is relative to wilting point and the `sw25` threshold.
  xx: Previous layer bottom depth used to determine the current layer midpoint depth. It is
    set to zero for the first layer and to `soil(j)%phys(k-1)%d` for deeper layers.
  dmidl: Midpoint depth of the current soil layer. It is used to reduce volatilization with
    depth through the depth-response factor `dpf`.
  dpf: Depth factor for volatilization, computed from `dmidl`. It reduces volatilization potential
    as the layer midpoint gets deeper.
  akn: Nitrification rate factor formed from temperature and soil-water responses. It is used
    to compute the nitrifiable ammonium fraction and the nitrification split of the combined
    loss.
  akv: Volatilization rate factor formed from temperature, depth, and CEC responses. It is
    used to compute the volatilizable ammonium fraction and the volatilization split of the
    combined loss.
  rnv: Combined ammonium loss pool before splitting into nitrate formation and volatilization.
    It is the total NH4 subject to the two pathways in the layer.
  rnit: Nitrified nitrogen amount for the current layer. After the split, it is the portion
    of `rnv` that is moved from ammonium to nitrate.
  rvol: Volatilized nitrogen amount for the current layer. After the split, it is the portion
    of `rnv` removed from ammonium to the atmosphere.
  tf: Temperature response factor for nitrification and volatilization. It is computed from
    soil temperature and gates the process so very cold layers do not react.
  cecf: Constant cation-exchange-capacity factor for volatilization. It is fixed at 0.15 and
    scales the volatilization rate in every layer.
uses:
  septic_data_module: '`sep(isep)` holds the septic-system option flag used to decide whether
    the biozone layer should be exempt from the standard nitrification/volatilization update.
    Without this module state, the routine could not honor the septic-system-specific routing
    of nitrogen losses.'
  basin_module: '`ihru` selects the current HRU, while `i_sep(j)` and `isep` identify whether
    that HRU is tied to an active septic system and which septic-system record to inspect.
    They determine both which soil profile is processed and whether the septic biozone layer
    is skipped.'
  organic_mineral_mass_module: '`soil1(j)%mn(k)%nh4` and `soil1(j)%mn(k)%no3` are the ammonium
    and nitrate pools this routine transforms. The procedure computes how much ammonium is
    nitrified or volatilized and writes the resulting changes back to these layer reservoirs.'
  hru_module: '`ihru`, `i_sep`, and `isep` come from `hru_module` and provide the current
    HRU index plus septic linkage state. They are needed to choose the active HRU and to apply
    the septic-system exception to the biozone layer.'
  soil_module: '`soil` provides the per-HRU layer count and layer physical properties that
    drive the response functions. The routine uses layer temperature, water status, wilting
    point, field capacity, and layer depth to compute the process factors for each soil layer.'
---

<!-- facts:header -->

Computes daily ammonium nitrification and ammonia volatilization by soil layer for the current HRU. It updates the layer mineral nitrogen pools after applying temperature, soil-water, depth, and septic-system restrictions.

## Bottom Line

`nut_nitvol` walks the active HRU's soil layers and, for each layer with ammonium present and warm enough soil, computes the temperature factor, soil-water factor, depth factor, and CEC factor that control ammonium nitrification and volatilization. It then splits the available ammonium loss between nitrate production and gaseous loss, with a septic-system guard that skips the active septic biozone layer.

The routine matters because it directly changes the layer mineral nitrogen state in `soil1(j)%mn(k)%nh4` and `soil1(j)%mn(k)%no3`, which later nutrient routines and the rest of the daily HRU water-quality sequence use after `hru_control` calls it.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the daily HRU control sequence after residue and carbon transformations have been computed and before phosphorus mineralization and septic biozone processing. `hru_control` prepares the current HRU context by setting `ihru` and other HRU-state pointers, and later nutrient routines depend on the updated `soil1(j)%mn(k)%nh4` and `soil1(j)%mn(k)%no3` values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop over soil layers | Iterates through every soil layer in the current HRU and computes the temperature response factor from layer temperature. |
| 2. require ammonium and warmth | Processes only layers with positive ammonium and a temperature factor of at least 0.001, then derives the water threshold and current water status for that layer. |
| 3. compute soil-water factor | Uses a linear moisture response below the `sw25` threshold and a full factor of 1 above it. |
| 4. get layer midpoint depth | Uses the previous layer depth, or zero for the first layer, to determine the current layer midpoint depth. |
| 5. compute depth and rate factors | Builds the depth factor and combines temperature, soil-water, depth, and CEC terms to compute the combined loss pool plus the nitrification and volatilization fractions. |
| 6. skip inactive septic biozone | Applies the nitrogen transformation only when the layer is not the active septic biozone or the septic system is not flagged as active. |
| 7. split combined loss pool | Allocates the combined ammonium loss between volatilization and nitrification in proportion to their relative fractions, then prevents negative nitrification. |
| 8. move nitrate and cap ammonium | Removes nitrified ammonium from the NH4 pool with a minimum floor, repairs any negative value, and adds the nitrified amount to the NO3 pool. |
| 9. remove volatilized ammonium | Subtracts volatilized ammonium from the NH4 pool, again enforcing a floor and correcting any negative residue. |
| 10. return | Ends the subroutine after all soil layers have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:septic_data_module] | `sep` |  |
| [sym:basin_module] | `ihru, i_sep, isep` |  |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(k)%nh4, soil1(j)%mn(k)%no3` |
| [sym:hru_module] | `ihru, i_sep, isep` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(k)%tmp, soil(j)%phys(k)%wpmm, soil(j)%phys(k)%fc, soil(j)%phys(k)%st, soil(j)%phys(k-1)%d, soil(j)%phys(k)%d` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil1(j)%mn(k)%nh4` | When a layer has positive NH4, sufficient temperature, and is not excluded by the septic-system gate, the routine subtracts the nitrified amount from `soil1(j)%mn(k)%nh4`. | Ammonium is consumed by nitrification and reduced toward a small positive floor so the pool does not go negative. |
| `soil1(j)%mn(k)%no3` | In the same processing branch, after nitrification is accounted for, the routine adds `rnit` to `soil1(j)%mn(k)%no3`. | Nitrate increases by the ammonium that was nitrified in the layer, preserving the transformed nitrogen in the mineral pool. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:1.3.1 | Nitrification temperature factor eta_tmp | $\eta_{tmp,ly}=0.41*\frac{(T_{soil,ly}-5)}{10}$ | tf=0.41*(T-5)/10; exact match when T>5 (tf checked >=0.001). |
| 3:1.3.2 | Soil water factor eta_sw (low SW case) | $\eta_{sw,ly}=\frac{SW_{ly}-WP_{ly}}{0.25*(FC_{ly}-WP_{ly})}$ | swf=(swwp-wpmm)/(sw25-wpmm) when swwp<sw25; sw25=WP+0.25*FC. Matches (SW-WP)/(0.25*(FC-WP)). |
| 3:1.3.3 | Soil water factor eta_sw=1 (saturated case) | $\eta_{sw,ly}=1.0$ | swf=1 when swwp>=sw25; exact match for eta_sw=1 when SW>=threshold. |
| 3:1.3.4 | Depth factor for volatilization eta_midz | $\eta_{midz,ly}=1-\frac{z_{mid,ly}}{z_{mid,ly}+exp[4.706-0.0305*z_{mid,ly}]}$ | dpf=1-dmidl/(dmidl+exp(4.706-0.0305*dmidl)); exact match. |
| 3:1.3.5 | CEC volatilization factor eta_cec=0.15 | $\eta_{cec,ly}=0.15$ | cecf=0.15 (parameter constant); exact match. |
| 3:1.3.6 | Nitrification rate akn = eta_tmp * eta_sw | $\eta_{nit,ly}=\eta_{tmp,ly}*\eta_{sw,ly}$ | akn=tf*swf; exact match for eta_nit=eta_tmp*eta_sw. |
| 3:1.3.7 | Volatilization rate akv = eta_tmp * eta_midz * eta_cec | $\eta_{vol,ly}=\eta_{tmp,ly}*\eta_{midz,ly}*\eta_{cec,ly}$ | akv=tf*dpf*cecf; exact match for eta_vol=eta_tmp*eta_midz*eta_cec. |
| 3:1.3.8 | Combined N nitrification+volatilization pool | $N_{nit\|vol,ly}=NH4_{ly}*(1-exp\lfloor-\eta_{nit,ly}-\eta_{vol,ly}\rfloor)$ | rnv=NH4*(1-exp(-akn-akv)); exact match for N_nit\|vol=NH4*(1-exp(-eta_nit-eta_vol)). |
| 3:1.3.9 | Nitrification fraction fr_nit | $fr_{nit,ly}=1-exp\lfloor-\eta_{nit,ly}\rfloor$ | rnit=1-exp(-akn); exact match for fr_nit=1-exp(-eta_nit). |
| 3:1.3.10 | Volatilization fraction fr_vol | $fr_{vol,ly}=1-exp\lfloor-\eta_{vol,ly}\rfloor$ | rvol=1-exp(-akv); exact match for fr_vol=1-exp(-eta_vol). |
| 3:1.3.11 | N nitrified (NH4 to NO3) | $N_{nit,ly}=\frac{fr_{nit,ly}}{(fr_{nit,ly}+fr_{vol,ly})}*N_{nit\|vol,ly}$ | rvol=rnv*rvol/(rvol+rnit); rnit=rnv-rvol; proportional split of rnv by fraction. |
| 3:1.3.12 | N volatilized (NH4 lost to atmosphere) | $N_{vol,ly}=\frac{fr_{vol,ly}}{(fr_{nit,ly}+fr_{vol,ly})}*N_{nit\|vol,ly}$ | rvol=rnv*fr_vol/(fr_nit+fr_vol); exact proportional allocation. |

## Lineage

Resolved lineage shows the routine was introduced in df07e3f with the full nitrification/volatilization algorithm. 39fabde initialized the local scalars and slightly adjusted comments and formatting, 9c706fd added a temporary debug print after the nitrate update and before volatilization, 1807dbb removed that debug print, and bd18ad4 added an unused `external :: ee` declaration.

- df07e3f added `nut_nitvol.f90` with the full layer loop, temperature/moisture/depth response calculations, septic-system gate, and NH4-to-NO3 / volatilization updates.
- 39fabde changed the local scalar declarations to explicit zero-initialized values and kept the same process logic.
- 9c706fd inserted a debug print after the nitrate update; 1807dbb later removed it, leaving the algorithm unchanged except for transient logging.
- bd18ad4 added an `external :: ee` declaration without any extracted use in the routine body.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_nitvol' has no extracted documentation comment.
