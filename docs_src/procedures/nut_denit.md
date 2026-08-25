---
kind: procedure
symbol: nut_denit
title: nut_denit
status: filled
source_hash: 3f70b56a199e2451
version_label: SWAT+ 62.0.0
args:
  k: Layer index `k`; it selects which soil layer within HRU `j` is evaluated and updated.
  j: HRU index `j`; it selects the hydrologic response unit whose soil profile state is read
    and modified.
  cdg: '`cdg` is the soil temperature factor that scales denitrification potential; larger
    values increase the exponential loss term.'
  wdn: '`wdn` is the output nitrate loss from denitrification for the selected layer, in kg
    N/ha, and is assigned inside the routine.'
  void: '`void` is the layer void fraction input used to compute the water-filled void factor
    `vof`; it controls how strongly wetness promotes denitrification.'
locals:
  vof: '`vof` holds the water-filled void factor computed from `void` as `1. / (1. + (void/0.04)**5)`.
    It converts the layer void fraction into a moisture response multiplier for denitrification.'
uses:
  basin_module: '`bsn_prm%cdn` provides the basin-level denitrification exponential rate coefficient.
    That coefficient is the calibration/control parameter that sets the strength of nitrate
    loss in the rate equation.'
  organic_mineral_mass_module: '`soil1(j)%mn(k)%no3` is the nitrate pool being depleted, and
    `soil1(j)%tot(k)%c` supplies the layer organic carbon term that drives denitrification.
    Without these profile masses, the routine cannot compute or apply the nitrate loss.'
  soil_module: '`soil_module` is needed because it provides the soil-profile context that
    indexes the layer state for HRU `j`. Even though the resolved state objects are owned
    by `organic_mineral_mass_module`, this module is what makes the soil-layer mass structures
    available to the routine''s execution context.'
---

<!-- facts:header -->

Computes nitrate denitrification in a soil layer for one HRU. It reduces the layer nitrate pool using a moisture factor, a temperature factor, basin denitrification coefficient, and soil organic carbon.

## Bottom Line

nut_denit estimates how much nitrate is lost from a specific soil layer by denitrification. It computes a water-filled void factor from the layer void fraction, combines that with the basin denitrification coefficient, soil temperature factor, and soil carbon, and then subtracts the resulting loss from the layer nitrate pool.

The routine matters because it directly updates the layer mineral nitrogen state used by later nitrogen transport and accounting. It also returns the computed loss through `wdn`, so callers can track how much nitrate was removed from the soil layer.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the soil nitrogen denitrification calculation for a given HRU and layer. Its inputs are prepared by the calling nitrogen/soil process using the current HRU layer state, and its result feeds later nitrogen bookkeeping because it updates the layer nitrate pool and returns the amount removed as denitrification loss.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the reported loss to zero. | The routine starts by clearing `wdn`, so any returned loss begins from a known zero value before the denitrification calculation is applied. |
| 2. Convert void fraction to a wetness factor. | It computes `vof` from `void` using the nonlinear water-filled void relation `1. / (1. + (void/0.04)**5)`, so wetter layers receive a larger denitrification multiplier. |
| 3. Compute nitrate lost from the layer. | It calculates `wdn` as the current layer nitrate mass times `1 - Exp(-bsn_prm%cdn * cdg * vof * soil1(j)%tot(k)%c)`, combining basin coefficient, temperature factor, moisture factor, and soil carbon into the denitrification rate. |
| 4. Reduce the layer nitrate pool. | It subtracts the computed loss from `soil1(j)%mn(k)%no3` and floors the remaining nitrate at `0.0001` to avoid an unrealistically empty pool. |
| 5. Return to the caller. | The subroutine exits after updating the shared soil state and leaving the computed denitrification loss in `wdn` for the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%cdn` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(k)%no3, soil1(j)%tot(k)%c` |
| [sym:soil_module] | `soil1` | `soil1(j)%mn(k)%no3, soil1(j)%tot(k)%c, soil1(j)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil1(j)%mn(k)%no3` | Always, after `wdn` is computed from the layer nitrate pool. | `soil1(j)%mn(k)%no3` is reduced by the denitrification loss `wdn`, but it is never allowed to drop below `0.0001`. This preserves a small nitrate residual while recording the amount removed from the layer. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:1.4.1 | Denitrification water threshold condition | $\gamma_{sw,ly}\ge \gamma_{sw,thr}$ | vof=1/(1+(void/0.04)^5) is a water-filled void factor; theory uses gamma_sw>=gamma_sw_thr. nut_nminrl:185 has explicit sut>=sdnco check. |
| 3:1.4.2 | Denitrification rate formula | $N_{denit,ly}=0.0$ | wdn=NO3*(1-exp(-cdn*cdg*vof*C)); matches N_denit=NO3*(1-exp(-beta*gamma_sw*gamma_tmp*orgC)). |

## Lineage

`nut_denit` was introduced in df07e3f with the denitrification calculation already present. The initial source used `bsn_prm%cdn`, `soil1(j)%mn(k)%no3`, `soil1(j)%tot(k)%c`, and the `max(0.0001, ...)` nitrate floor. Commit 39fabde only normalized the declaration formatting and initialized `vof` to `0.`, and f1e61a3 only fixed indentation and spacing without changing the calculation.

- df07e3f introduced the subroutine and its denitrification update logic, including the nitrate depletion formula and minimum nitrate floor.
- 39fabde made a non-behavioral cleanup by initializing `vof` and adjusting declaration spacing.
- f1e61a3 made a non-behavioral cleanup by fixing tab/space indentation.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_denit' has no extracted documentation comment.
