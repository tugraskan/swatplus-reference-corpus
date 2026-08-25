---
kind: procedure
symbol: ero_eiusle
title: ero_eiusle
status: filled
source_hash: 95c14a0823af8bcd
version_label: SWAT+ 62.0.0
locals:
  j: '`j` is the current HRU index. The routine sets `j = ihru` so it can read the active
    HRU object number and write the resulting erosivity factor back to `usle_eifac(j)`.'
  xb: '`xb` is the intermediate rainfall-intensity multiplier derived from the station half-hour
    rainfall fraction: `-2 * Log(1. - wst(iwst)%weat%precip_half_hr)`. It is used to scale
    daily precipitation into the peak-intensity proxy `pkrf`.'
  pkrf: '`pkrf` is the peak-intensity proxy built as `xb * w%precip`. The routine uses it
    inside `Log10(pkrf)` when computing the USLE EI value.'
  pkrf30: '`pkrf30` is the 30-minute storm intensity proxy computed as `2. * w%precip * wst(iwst)%weat%precip_half_hr`.
    It supplies the `I_30` factor in the EI calculation.'
  iob: '`iob` is the object-connectivity index for the current HRU. It is used to reach `ob(iob)%wst`,
    which identifies the weather station supplying the half-hour precipitation fraction.'
uses:
  climate_module: '`climate_module` provides the daily precipitation `w%precip` and the weather-station
    field `wst(iwst)%weat%precip_half_hr`. Those two climate values determine whether the
    routine runs its erosion calculation and what EI value it computes.'
  hydrograph_module: '`hydrograph_module` links the current object to its assigned weather
    station through `ob(iob)%wst`. That mapping is needed so the routine can pick the correct
    station index `iwst` before reading station rainfall characteristics.'
  hru_module: '`hru_module` supplies the active HRU context `ihru`, the HRU-to-object link
    `hru(j)%obj_no`, and the output array `usle_eifac(j)`. This module is where the computed
    erosivity factor must be stored for later HRU-based erosion work.'
---

<!-- facts:header -->

Computes the USLE rainfall erosivity index EI for the current HRU. It uses daily precipitation and station half-hour rainfall fraction to derive the storm energy and intensity factor.

## Bottom Line

This routine calculates the USLE rainfall erosion index for the active HRU when there is enough precipitation to matter. It combines the day's rainfall depth with the weather-station half-hour intensity fraction to build the EI value used by later erosion calculations.

The result is stored in the HRU-level erosivity field `usle_eifac(j)` and in `usle_ei`. Those values are then available to downstream rainfall-driven sediment routines called from `surface`, such as the overland sediment erosion calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the surface erosion workflow after `surface` has already established that the day has enough runoff and peak flow to justify erosion processing. `surface` prepares the call by selecting the active HRU/day context, and the EI result then feeds later sediment calculations in the same surface pass, especially `ero_ovrsed` and related rainfall-driven erosion behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select current HRU and weather station | The routine maps the active HRU index `ihru` into local `j`, then follows `hru(j)%obj_no` to the object connectivity record and `ob(iob)%wst` to the weather-station index `iwst` that supplies rainfall characteristics. |
| 2. Skip dry days | If daily precipitation is not greater than `1.e-4`, the routine does not compute an erosivity index and falls through to the return. |
| 3. Build intensity multiplier from half-hour fraction | For wet days, it computes `xb = -2. * Log(1. - wst(iwst)%weat%precip_half_hr)`, which converts the station's half-hour rainfall fraction into a storm-intensity scaling term. |
| 4. Compute 30-minute intensity proxy | It calculates `pkrf30 = 2. * w%precip * wst(iwst)%weat%precip_half_hr`, the proxy used for the USLE 30-minute intensity component. |
| 5. Compute peak-rainfall proxy | It sets `pkrf = xb * w%precip`, combining daily precipitation with the intensity multiplier to obtain the peak-intensity proxy used in the logarithmic term. |
| 6. Calculate USLE EI | The routine computes `usle_ei` from daily precipitation, the log of `pkrf`, and `pkrf30`, yielding the storm erosivity index for the day. |
| 7. Zero tiny erosion values | If the computed index is below `1.e-4`, it is forced to zero so negligible numerical noise does not propagate into later sediment calculations. |
| 8. Store HRU erosivity factor | The final `usle_ei` value is copied into `usle_eifac(j)`, preserving the result in the HRU-specific erosivity-factor array for later use. |
| 9. Return to caller | The subroutine ends after updating the HRU erosivity state; no values are returned through arguments because the routine works through module variables. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `w, wst` | `w%precip, wst(iwst)%weat%precip_half_hr` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:hru_module] | `hru, usle_eifac, usle_ei, ihru` | `hru(j)%obj_no` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | After `j = ihru` and before exit, `iwst` is set from `ob(iob)%wst` using the current HRU's object connectivity. | `iwst` changes to the weather-station index associated with the active HRU so the routine can read that station's rainfall-fraction data for the current day. |
| `usle_ei` | If `w%precip > 1.e-4`, then `usle_ei` is computed; if the result is smaller than `1.e-4`, it is reset to zero. | `usle_ei` is updated from the day's rainfall depth and intensity proxy only on wet days, and tiny values are suppressed so trivial erosion does not carry forward. |
| `usle_eifac(j)` | When `w%precip > 1.e-4`, after `usle_ei` is finalized. | `usle_eifac(j)` receives the HRU's current erosivity index so later HRU-based erosion routines can reuse the computed rainfall factor without recomputing it. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 4:1.2.2 | EI_USLE = E_storm * I_30 | $EI_{USLE}=E_{storm}*I_{30}$ | Verified against SWAT+ 62.0.0 (ero_eiusle.f90:57). (usle_ei = E*I30) |
| 4:1.2.3 | Exponential intensity i_t = i_mx*exp(-t/k_i) | $i_t=i_{mx}*exp(-\frac{t}{k_i})$ | Verified against SWAT+ 62.0.0 (ero_eiusle.f90:57). exponential intensity subsumed into the EI regression `(12.1+8.9·(log10(pkrf)−.4343)) |
| 4:1.2.4 | E_storm incremental form | $E_{storm}=\Delta R_{day}*(12.1+8.9*log_{10}[\frac{\Delta R_{day}}{\Delta t}])$ | Incremental form E=DeltaR*(12.1+8.9*log10(DeltaR/Dt)); integrated into the closed-form expression at line 57. |
| 4:1.2.5 | E_storm integral form | $E_{storm}=12.1\int_0^{\infty}i_t dt+8.9\int_0^{\infty} i_t log_{10} i_tdt$ | Integral form of storm energy; analytical result folded into line 57. |
| 4:1.2.6 | E_storm = R_day/1000*(12.1+8.9*(log10(i_mx)-0.434)) | $E_{storm}=\frac{R_{day}}{1000}*(12.1+8.9*(log_{10}[i_{mx}]-0.434))$ | The factor w%precip*(12.1+8.9*(log10(pkrf)-0.4343))/1000 at line 57 implements E_storm with pkrf=i_mx*k_i (peak intensity proxy). Combined with pkrf30 (I_30) to give EI. |
| 4:1.2.7 | R_day = i_mx * k_i | $R_{day}=i_{mx}*k_i$ | pkrf = xb * w%precip where xb=-2*ln(1-alpha_0.5); this gives pkrf = i_mx (peak intensity), the product i_mx*k_i = R_day/xb * xb = R_day is recovered via pkrf. |
| 4:1.2.8 | Cumulative rainfall R_t = R_day*(1-exp(-t/k_i)) | $R_t=R_{day}*(1-exp[-\frac{t}{k_i}])$ | Verified against SWAT+ 62.0.0 (ero_eiusle.f90:57). cumulative-rain form; same EI regression |
| 4:1.2.9 | R_0.5 = alpha_0.5 * R_day | $R_{0.5}=\alpha_{0.5}*R_{day}$ | Verified against SWAT+ 62.0.0 (ero_eiusle.f90:55). pkrf30 = 2·precip·α₀.₅` = 2·R₀.₅ |
| 4:1.2.10 | i_mx = -2*R_day*ln(1-alpha_0.5) | $i_{mx}=-2*R_{day}*1n(1-\alpha_{0.5})$ | Verified against SWAT+ 62.0.0 (ero_eiusle.f90:56). pkrf = xb*precip`, xb=−2·Log(1−α₀.₅) — i_mx |
| 4:1.2.11 | I_30 = 2*alpha_0.5*R_day | $I_{30}=2*\alpha_{0.5}*R_{day}$ | pkrf30=2*w%precip*wst%precip_half_hr = 2*alpha_0.5*R_day; exact match for I_30. |

## Lineage

Three source-backed commits were resolved for `ero_eiusle`. The original file was introduced in `df07e3f` with the procedure body and documentation skeleton. Commit `39fabde` changed only local variable initialization, setting `j`, `xb`, `pkrf`, `pkrf30`, and `iob` to zero at declaration. Commit `889136d` made a documentation typo fix in the local-definition comment, changing "occuring" to "occurring".

- df07e3f added the subroutine, its module dependencies, the wet-day EI computation, and the `usle_eifac(j)` assignment.
- 39fabde changed the local declarations to initialize `j`, `xb`, `pkrf`, `pkrf30`, and `iob`, reducing uninitialized-state risk without changing the algorithm.
- 889136d corrected only a comment spelling error in the local variable description; it did not alter runtime behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ero_eiusle' has no extracted documentation comment.
