---
kind: procedure
symbol: sq_snom
title: sq_snom
status: filled
source_hash: e8be46d6bcf59925
version_label: SWAT+ 62.0.0
locals:
  j: Loop/index selector for the active HRU. `j` is set from `ihru` so the routine can read
    and update the snow state for the currently processed HRU.
  smfac: Seasonal snowmelt factor computed from the HRU’s summer and winter melt rates and
    the current day of year. It scales the temperature-driven melt equation before snow-cover
    adjustment.
  rto_sno: Ratio of the current HRU snow water storage to the full-cover threshold (`covmx`).
    It is the normalized snow amount used to compute fractional snow cover.
  snocov: Fraction of the HRU surface covered by snow. It is computed from `rto_sno` and used
    to reduce melt when snowpack is incomplete.
  snotmp: Current snowpack temperature estimate for the active HRU. The routine resets it
    at entry and then uses daily average air temperature and the HRU lag factor to update
    it before melt is computed.
uses:
  time_module: This routine branches on the simulation time step count and uses the current
    day of simulation. `time%step` controls whether subdaily precipitation arrays are zeroed
    or incremented, and `time%day` sets the seasonal position for the melt-factor sinusoid.
  hydrograph_module: The hydrograph timestep array is where subdaily precipitation is accumulated.
    `ts` must be updated when melt occurs so later hydrologic routing and time-step output
    see the added water.
  hru_module: The active HRU record stores the snow parameters and snow state that this routine
    reads and updates. `hru(j)%sno%...` controls snowfall and melt thresholds, `hru(j)%sno_mm`
    is the snow water storage being changed, and `hru(j)%snocov2` shapes the snow-cover fraction.
  climate_module: Daily weather supplies the temperature drivers that determine whether precipitation
    falls as snow and whether melt can occur. `w%tave`, `w%tmax`, and `w%ts` are the climate
    inputs and subdaily precipitation state this routine reads and modifies.
  output_landscape_module: This module is part of the routine’s imported landscape-output
    context, but the extracted code does not show a direct reference to a named state or type
    from it. The import may exist for broader snow/hydrology bookkeeping elsewhere in the
    build, but no specific use is visible here.
---

<!-- facts:header -->

Updates snowpack state for the current HRU and day. It partitions precipitation into snowfall versus rain, computes snowmelt and snow cover, and adjusts effective precipitation for routing.

## Bottom Line

sq_snom runs once per HRU inside the HRU control workflow to update the day’s snow state. It uses daily weather, HRU snow parameters, and the current time step count to decide whether precipitation adds to snowpack or whether melt removes water from snowpack.

The routine matters because it changes `hru(j)%sno_mm`, `snofall`, `snomlt`, `precip_eff`, and subdaily precipitation arrays used by later runoff and routing calculations. It also applies the seasonal melt-factor and snow-cover equations that drive SWAT+ snow behavior.

## Arguments

<!-- facts:arguments -->

## Where It Fits

sq_snom is called from `hru_control` after canopy interception and before overland-flow routing, so it runs during the per-HRU daily water-balance sequence. `hru_control` has already selected the active HRU via `ihru` and prepared the day’s climate and precipitation state; the results from sq_snom feed later runoff, routing, and water-balance calculations through `hru(j)%sno_mm`, `snofall`, `snomlt`, `precip_eff`, and `w%ts`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set HRU index | Initialize the local HRU index and copy `ihru` into `j` so the routine works on the currently active HRU record. |
| 2. update snowpack temperature | Blend the prior snowpack temperature with the current daily average air temperature using the HRU temperature-lag factor. |
| 3. test snowfall condition | If average air temperature is at or below the HRU snowfall threshold, treat current effective precipitation as snowfall, add it to snow storage, clear `precip_eff`, and zero subdaily precipitation when the simulation uses more than one step per day. |
| 4. test melt condition | If maximum temperature exceeds the melt threshold and snowpack exists, compute a seasonal melt factor from day of year, then calculate potential melt from snow temperature, maximum temperature, and the melt threshold. |
| 5. compute snow cover | Convert snow storage into fractional snow cover: use the exponential shape equation when snowpack is below the full-cover amount, otherwise set cover to 1. |
| 6. limit and apply melt | Scale melt by snow cover, prevent negative or excessive melt, subtract it from snow storage, and add the melted water back into effective precipitation. |
| 7. update subdaily precipitation | When the run uses multiple time steps per day, distribute melt into the subdaily precipitation array and enforce nonnegative effective precipitation. |
| 8. no melt branch | If melt is not allowed by temperature or snow storage, set daily snowmelt to zero. |
| 9. return | Exit after the HRU snow state, effective precipitation, and subdaily precipitation have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%step, time%day` |
| [sym:hydrograph_module] | `ts` |  |
| [sym:hru_module] | `hru, ihru, precip_eff, snofall, snomlt` | `hru(j)%sno%timp, hru(j)%sno%falltmp, hru(j)%sno_mm, hru(j)%sno%melttmp, hru(j)%sno%meltmx, hru(j)%sno%meltmn, hru(j)%sno%covmx, hru(j)%snocov2` |
| [sym:climate_module] | `w` | `w%tave, w%ts, w%tmax, w%ts(:)` |
| [sym:output_landscape_module] | `output_landscape_module state is imported but no specific symbol from it is referenced in the extracted source lines.` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(j)%sno_mm` | When `w%tave > hru(j)%sno%falltmp` no snow is added; otherwise snowfall is added at line 56 and then melt may later reduce it. | `hru(j)%sno_mm` is the active HRU’s snow water storage. It increases by effective precipitation when temperatures are cold enough for snowfall, and later decreases by any melt that occurs in the same routine. |
| `snofall` | When `w%tave <= hru(j)%sno%falltmp`. | `snofall` captures the day’s precipitation that fell as snow or freezing rain. It is set equal to the current effective precipitation when snowfall conditions are met. |
| `precip_eff` | When snowfall is assigned, `precip_eff` is set to zero; when melt occurs, it is increased by `snomlt` and then clipped to nonnegative values. | `precip_eff` is the effective precipitation remaining for runoff accounting after snow partitioning and melt. The routine removes precipitation that becomes snowpack, then adds melt water back for later hydrologic routing. |
| `snomlt` | When `w%tmax > hru(j)%sno%melttmp .and. hru(j)%sno_mm > 0.`. | `snomlt` is the daily snowmelt amount. It is computed only when temperatures are warm enough and snowpack exists, then bounded so it cannot be negative or exceed the available snow water. |
| `w%ts(:)` | When `time%step > 1` and melt has occurred. | `w%ts(:)` receives the melt water distributed across the subdaily precipitation time steps. This keeps the time-step precipitation series consistent with meltwater added during the day. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:2.4.1 | Snow water balance | $SNO=SNO+R_{day}-E_{sub}-SNO_{mlt}$ | Verified against SWAT+ 62.0.0 (sq_snom.f90:79). SNO balance: −snomlt (:79), +precip_eff (:80), −sublimation (et_act) |
| 1:2.4.2 | Snow cover fraction | $sno_{cov}=\frac{SNO}{SNO_{100}}*[\frac{SNO}{SNO_{100}}+exp[cov_1-cov_2*\frac{SNO}{SNO_{100}}]]^{-1}$ | Verified against SWAT+ 62.0.0 (sq_snom.f90:72). |
| 1:2.5.1 | Snow-pack temperature | $T_{snow(d_n)}=T_{snow(d_n-1)}*(1-\ell_{sno})+\overline T_{av}*\ell_{sno}$ | Verified against SWAT+ 62.0.0 (sq_snom.f90:52). snotmp = snotmp*(1.-timp) + tave*timp` — exact |
| 1:2.5.2 | Snow melt | $SNO_{mlt}=b_{mlt}*sno_{cov}*[\frac{T_{snow}+T_{mx}}{2}-T_{mlt}]$ | Verified against SWAT+ 62.0.0 (sq_snom.f90:67). snomlt = smfac*((snotmp+tmax)/2 - melttmp)`, ×snocov (:76) |
| 1:2.5.3 | Seasonal melt factor | $b_{mlt}=\frac{(b_{mlt6}+b_{mlt12})}{2}+\frac{(b_{mlt6}-b_{mlt12})}{2}*sin(\frac{2\pi}{365}*(d_n-81))$ | smfac = (meltmx+meltmn)/2 + Sin((day-81)/58.09)*(meltmx-meltmn)/2. |

## Lineage

Resolved lineage shows four source-backed changes to sq_snom. The initial commit `df07e3f` added the routine with its snow partitioning, seasonal melt, and snow-cover logic. `39fabde` initialized local variables such as `j` and `smfac` to zero. `fd90e36` added an explicit `snotmp = 0.` reset near the top of the routine. `889136d` only corrected the documentation typo from “Celcius” to “Celsius`.

- df07e3f introduced sq_snom as a new routine for snowfall, snowmelt, snow-cover scaling, and updates to `snofall`, `snomlt`, `precip_eff`, and `w%ts`.
- 39fabde changed local initialization by setting `j` and `smfac` to zero at declaration, reducing reliance on implicit initial values.
- fd90e36 added an explicit `snotmp = 0.` assignment before `j = ihru`, forcing the snowpack temperature local to start at zero each call.
- 889136d did not change behavior; it only fixed the spelling in the documentation comment.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_snom' has no extracted documentation comment.
