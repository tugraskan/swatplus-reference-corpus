---
kind: procedure
symbol: cli_pgenhr
title: cli_pgenhr
status: filled
source_hash: 0851de0e51971924
version_label: SWAT+ 62.0.0
locals:
  itime: Current subdaily index used to place each generated rainfall increment into `wst(iwst)%weat%ts_next`
    as the routine marches through the storm period.
  pt: Current elapsed time in minutes within the storm window; it is advanced by `time%dtm`
    and compared with the peak time and storm duration to decide which exponential branch
    to use.
  k: Seed/counter passed into `atri` to draw the triangular random fraction that sets the
    storm’s time-to-peak position.
  vv: The stochastic fraction returned by `atri`; it represents the generated time-to-peak
    position as a value between the lower and upper bounds used by the triangular draw.
  blm: Lower bound for the triangular random draw passed to `atri`.
  qmn: Central/mean control value for the triangular random draw passed to `atri`.
  uplm: Upper bound for the triangular random draw passed to `atri`.
  dur: Computed storm duration in hours, derived from daily precipitation and peak intensity;
    it is capped at 24 hours if needed.
  pkrain: Rainfall accumulated by the time of the peak, computed as the fraction `vv` of the
    daily precipitation.
  rtp: Time of peak rainfall rate in minutes from the storm start, computed from `vv` and
    `dur`.
  xk1: Dimensionless rising-branch constant controlling the pre-peak exponential shape.
  xk2: Dimensionless falling-branch constant controlling the post-peak exponential shape.
  xkp1: Scaled rising-branch exponential constant in hours, used in the pre-peak rainfall
    integral.
  xkp2: Scaled falling-branch exponential constant in hours, used in the post-peak rainfall
    integral.
  rx: Running cumulative rainfall total at the current subdaily time, used to compute each
    increment as `rx - sumrain`.
  pkrr: Peak rainfall rate, computed from daily precipitation and half-hour precipitation
    fraction, and recomputed if the duration is capped.
  sumrain: Cumulative rainfall already assigned before the current subdaily step; it is subtracted
    from `rx` to get the incremental amount and updated after each step.
  atri: External triangular-distribution random variate function used to generate the storm’s
    time-to-peak fraction.
uses:
  climate_module: '`climate_module` provides the active weather-station record `wst(iwst)%weat`,
    which is where the routine reads the day’s precipitation inputs and stores the generated
    subdaily rainfall totals. Its `ts` and `ts_next` arrays are the actual outputs of this
    procedure.'
  time_module: '`time_module` supplies the simulation time resolution (`time%dtm` and `time%step`)
    that controls how many subdaily increments are generated and how far the loops advance
    through the day.'
  hydrograph_module: '`hydrograph_module` supplies `iwst`, the current weather-station index,
    so the routine updates the correct station’s precipitation state rather than a generic
    or local copy.'
---

<!-- facts:header -->

Distributes a day’s precipitation into subdaily rainfall amounts using a stochastic time-to-peak and a two-sided exponential storm shape. It fills the current weather station’s subdaily precipitation arrays for the active simulation day.

## Bottom Line

`cli_pgenhr` takes the daily precipitation already loaded for the current weather station and turns it into subdaily rainfall increments. It first chooses a random time-to-peak fraction with `atri`, then computes storm duration, peak timing, and the exponential rise/decay constants that define the within-day rainfall curve.

It writes the resulting rainfall amounts into `wst(iwst)%weat%ts_next`, stepping through the current time resolution from `time_module`. Those subdaily values are then available to the precipitation-control workflow, which copies them into the current-day array and sums them into `precip_next` when the simulation is using generated precipitation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the precipitation-control workflow after `cli_precip_control` has selected simulated precipitation and before the day’s subdaily precipitation is used downstream. `cli_precip_control` sets up the current station/day state and then calls `cli_pgenhr` when `time%step > 1`; later model behavior depends on the filled `wst(iwst)%weat%ts_next` values, which are copied into `ts` and summed into `precip_next` for subsequent climate and hydrologic calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. zero subdaily precip array | Clears the current station’s subdaily precipitation array `wst(iwst)%weat%ts` before generating a new storm profile. |
| 2. guard on no rain | Returns immediately when daily precipitation is effectively zero, because there is no storm to distribute within the day. |
| 3. compute peak rate | Derives the peak rainfall rate from daily precipitation and the half-hour intensity fraction stored in the weather record. |
| 4. draw peak fraction | Sets fixed triangular-distribution bounds and calls `atri` to generate the stochastic fraction `vv` that locates the storm peak. |
| 5. derive shape constants | Computes the dimensionless exponential constants `xk1` and `xk2` from the generated peak fraction. |
| 6. compute duration and cap | Calculates storm duration from precipitation and peak rate; if duration exceeds 24 hours, it is capped and the peak rate is recomputed. |
| 7. compute peak totals | Computes rainfall accumulated by the peak and the peak time in minutes from storm start. |
| 8. scale exponential constants | Converts the dimensionless constants into hour-based exponential constants used by the integrated rainfall equations. |
| 9. initialize stepping state | Initializes the current time counter, subdaily index, and cumulative rainfall before stepping through the storm. |
| 10. fill pre-peak steps | Advances through time before the peak, computes cumulative rainfall with the rising exponential form, stores each increment in `ts_next`, and updates the cumulative total until the peak or time-step limit is reached. |
| 11. fill post-peak steps | Continues stepping through the storm after the peak, computes cumulative rainfall with the falling exponential form, stores each increment in `ts_next`, and stops at the end of the storm or time-step limit. |
| 12. assign leftover rainfall | Adds any remaining unassigned rainfall to the last populated subdaily increment so the generated subdaily totals match the daily precipitation. |
| 13. return | Exits after the subdaily rainfall profile has been written back into the station state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%ts, wst(iwst)%weat%precip, wst(iwst)%weat%precip_half_hr, wst(iwst)%weat%ts_next(itime), wst(iwst)%weat%ts_next(itime-1)` |
| [sym:time_module] | `time` | `time%dtm, time%step` |
| [sym:hydrograph_module] | `iwst` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%weat%ts` | When daily precipitation is nonzero and the routine starts generating the storm profile. | `wst(iwst)%weat%ts` is reset to zero so the current-day subdaily rainfall array can be rebuilt from scratch for this station. |
| `wst(iwst)%weat%ts_next(itime)` | During the pre-peak and post-peak loops whenever a new subdaily increment is computed and `itime <= time%step`. | `wst(iwst)%weat%ts_next(itime)` receives the rainfall increment for that subdaily interval, built as the change in cumulative rainfall from the previous step. |
| `wst(iwst)%weat%ts_next(itime-1)` | After each successful subdaily increment is written and the loop advances to the next time point. | `wst(iwst)%weat%ts_next(itime-1)` becomes the previous interval’s rainfall amount; if the storm ends with leftover daily rainfall, the last populated increment is adjusted to absorb the remainder. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:3.3.1 | Rainfall intensity i(T) | $i(T)={i_{mx}*exp[\frac{T-T_{peak}}{\delta_{1}}], i_{mx}*exp[\frac{T_{peak}-T}{\delta_2}}]$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:114). double-exponential within-day intensity (rise :114 / fall :125), δ=xkp1/xkp2 |
| 1:3.3.2 | Normalized intensity i-hat | $\hat i =\frac{i}{i_{ave}}$ | Dimensionless i/i_ave; implicit in the integrated forms. |
| 1:3.3.3 | Normalized time t-hat | $\hat t=\frac{T}{T_{dur}}$ | Dimensionless T/T_dur; implicit in exponent arguments. |
| 1:3.3.4 | Normalized intensity distribution | $\hat i(\hat t)={\hat i_{mx}*exp[\frac{\hat t - \hat t_{peak}}{d_1}] , \hat i_{mx}*exp[\frac{\hat t_{peak}-\hat t}{d_2}]}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:114). normalized form of same distribution |
| 1:3.3.5 | Exponential constant delta_1 | $\delta_1=d_1*T_{dur}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:103). xkp1 = dur*xk1` — δ₁ |
| 1:3.3.6 | Exponential constant delta_2 | $\delta_2=d_2*T_{dur}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:104). xkp2 = dur*xk2` — δ₂ |
| 1:3.3.7 | Dimensionless constant d_1 | $d_1=\frac{\hat t-\hat t_{peak}}{ln(\frac{\hat i}{\hat i_{mx}})}=\frac{0-\hat t_{peak}}{ln(0.01)}=\frac{\hat t_{peak}}{4.605}$ | xk1 = vv/4.605 = t_peak/ln(100). |
| 1:3.3.8 | Dimensionless constant d_2 | $d_2=\frac{\hat t_{peak}-\hat t}{ln(\frac{\hat i}{\hat i_{mx}})}=\frac{\hat t_{peak}-1}{ln(0.01)}=\frac{1.0-\hat t_{peak}}{4.605}$ | xk2 = (1-vv)/4.605 = (1 - t_peak)/ln(100). |
| 1:3.3.9 | Generated time to peak (ascending) | $\hat t_{peak}=\hat t_{peakM} * \frac{\displaystyle \hat t_{peakL}+[rnd_1*(\hat t_{peakU}-\hat t_{peakL})*(\hat t_{peakM}-\hat t_{peakL})]^{0.5}}{\displaystyle\hat t_{peak,mean}}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90). (subdaily peak rain time) |
| 1:3.3.10 | Generated time to peak (descending) | $\hat t_{peak}=\hat t_{peakM}*\frac{\displaystyle\hat t_{peakU}-(\hat t_{peakU}-\hat t_{peakM})*[\frac{\hat t_{peakU}(1-rnd_1)-\hat t_{peakL}(1-rnd_1)}{\hat t_{peakU}-\hat t_{peakM}}]^{0.5}}{\displaystyle\hat t_{peak,mean}}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:85). time-to-peak `vv = Atri(blm,qmn,uplm)`; code uses fixed 0.05/0.25/0.95, not monthly |
| 1:3.3.11 | Cumulative rainfall integral R_T | $R_T=\int_0^T i dT$ | R_T = integral of i dT; code uses the closed forms (1:3.3.12). |
| 1:3.3.12 | Cumulative rainfall (integrated) | $R_T ={R_{Tpeak}-i_{mx}*\delta_1*(1-exp[(\frac{(T-T_{peak})}{\delta_1})] , {R_{Tpeak}+i_{mx}*\delta_2*(1-exp[\frac{(T_{peak}-T)}{\delta_2}])}}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:114). |
| 1:3.3.13 | Time of peak rainfall | $T_{peak}=\hat t_{peak}*T_{dur}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:99). rtp = vv*dur*60` — time to peak |
| 1:3.3.14 | Rainfall at time of peak | $R_{Tpeak}=\hat t_{peak} *R_{day}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:98). pkrain = vv*precip` — rain at peak |
| 1:3.3.15 | Daily rainfall from intensity and duration | $R_{day}=i_{mx}*(\delta_1+\delta_2)=i_{mx}*T_{dur}*(d_1+d_2)$ | R_day = i_mx*T_dur*(d1+d2); rearranged for duration. |
| 1:3.3.16 | Storm duration | $T_{dur}=\frac{R_{day}}{i_{mx}*(d_1+d_2)}$ | Verified against SWAT+ 62.0.0 (cli_pgenhr.f90:90). dur = precip/(pkrr*(xk1+xk2))` — storm duration |

## Lineage

Three source-backed commits were resolved for `cli_pgenhr`. `df07e3f` introduced the routine with its documentation and full storm-distribution logic. `c7c8e22` updated the imported source but did not change the algorithmic behavior visible in this file. `39fabde` initialized the local scalar variables to zero, affecting only default values, and `bd18ad4` added an `external :: atri, aunif` declaration without changing the rainfall calculation flow.

- `df07e3f` added the complete `cli_pgenhr` subroutine that distributes daily rainfall into subdaily values using a stochastic time-to-peak, exponential rise/decay, and the `ts_next` array writes.
- `39fabde` changed local variable initialization so the working scalars start at zero, which reduces dependence on undefined initial values but does not alter the storm-shape equations.
- `bd18ad4` added an explicit external declaration for `atri` and `aunif`; this affects symbol binding only and does not change the generated rainfall algorithm.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_pgenhr' has no extracted documentation comment.
