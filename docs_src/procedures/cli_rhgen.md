---
kind: procedure
symbol: cli_rhgen
title: cli_rhgen
status: filled
source_hash: 569b70eaa719702f
version_label: SWAT+ 62.0.0
args:
  iwgn: '`iwgn` selects which weather-generator parameter set and monthly climate series to
    use. It indexes `wgn_pms(iwgn)` for dewpoint/relative-humidity handling and wet-day frequency,
    and `wgn(iwgn)` for the monthly temperature and dewpoint inputs used in the humidity calculation.'
locals:
  vv: Temporary offset from 1.0 used to build the upper humidity limit with the exponential
    expression.
  rhm: Monthly relative humidity after adjustment for wet/dry conditions; this becomes the
    center point for the daily triangular draw.
  yy: Intermediate wet-day weighting term, equal to 0.9 times the monthly wet-day proportion.
  uplm: Upper bound on the generated daily relative humidity for the month.
  blm: Lower bound on the generated daily relative humidity for the month.
  rhmo: Monthly mean relative humidity before wet/dry adjustment, derived either from dew
    point or taken directly from the weather-generator humidity input.
  tmpmean: Monthly mean air temperature used with `Ee` when dew point must be converted to
    relative humidity.
  atri: External triangular-distribution sampler used to generate the final bounded daily
    humidity value.
  ee: External saturation-vapor-pressure function used to convert temperature and dew point
    into a relative-humidity ratio.
uses:
  climate_module: This module holds the weather-generator parameters and station weather state
    that drive and receive the humidity calculation. `wgn_pms(iwgn)%idewpt` decides whether
    monthly input is dew point or relative humidity, `wgn(iwgn)%tmpmx`, `wgn(iwgn)%tmpmn`,
    and `wgn(iwgn)%dewpt` provide the monthly climate inputs, `wgn_pms(iwgn)%pr_wdays` supplies
    the wet-day fraction used in the adjustment, and `wst(iwst)%weat%precip`/`wst(iwst)%weat%rhum`
    determine whether to bias the day toward wet conditions and where the result is stored.
  hydrograph_module: This module provides the current station index `iwst`, which tells the
    routine which weather station entry in `wst` to update. Without it, the computed humidity
    could not be written to the correct station weather state.
  time_module: This module provides the current simulation month through `time%mo`. The routine
    uses that month to pick the correct monthly generator values from `wgn` and `wgn_pms`.
---

<!-- facts:header -->

Generates daily relative humidity for a weather station from monthly weather-generator inputs. It converts monthly dew point or relative humidity to a monthly mean, adjusts it for wet/dry and wet-day conditions, then draws a bounded daily humidity value.

## Bottom Line

cli_rhgen computes the daily relative humidity assigned to the current weather station (`wst(iwst)%weat%rhum`). It starts from the month for `time%mo`, uses weather-generator parameters from `wgn` and `wgn_pms`, and then bounds the daily value by a triangular draw between lower and upper humidity limits.

The routine matters because later climate forcing uses the updated station humidity. `climate_control` calls it when station humidity is simulated rather than read from observations, so this routine fills the weather state needed for downstream daily climate calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during climate forcing setup, inside `climate_control` when station humidity is being simulated (`wst(iwst)%wco_c%hgage == "sim"`). `climate_control` sets the station-to-weather-generator mapping and current station context before calling it, and the resulting `wst(iwst)%weat%rhum` is then available to later weather-driven calculations for the current day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. choose monthly humidity source | If `wgn_pms(iwgn)%idewpt == 0`, compute monthly mean humidity from dew point by first averaging monthly maximum and minimum temperature into `tmpmean` and then forming `rhmo = Ee(dewpt) / Ee(tmpmean)`. Otherwise, use the stored monthly humidity value directly from `wgn(iwgn)%dewpt(time%mo)`. |
| 2. apply wet-day weighting | Compute the wet-day adjustment factor `yy = 0.9 * wgn_pms(iwgn)%pr_wdays(time%mo)` and shift the monthly mean to a dry-day mean with `rhm = (rhmo - yy) / (1.0 - yy)`. |
| 3. protect against very low mean humidity | If the adjusted monthly humidity is below 0.05, replace it with half of the unadjusted monthly value to avoid an unrealistically small center value. |
| 4. bias wet days toward saturation | If the current station has precipitation on this day, move the monthly humidity toward saturation with `rhm = rhm * 0.1 + 0.9`. |
| 5. compute the upper draw limit | Set `vv = rhm - 1.` and use it to compute `uplm = rhm - vv * Exp(vv)`, which gives the upper bound for the daily triangular distribution. |
| 6. compute the lower draw limit | Compute `blm = rhm * (1.0 - Exp(-rhm))` as the lower bound for the daily triangular distribution. |
| 7. draw daily station humidity | Call `Atri(blm, rhm, uplm, rndseed(idg(7),iwgn))` to sample a bounded daily relative humidity and store it in `wst(iwst)%weat%rhum`. |
| 8. finish | Return to the caller after the station humidity state has been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `wgn_pms, wgn, wst` | `wgn_pms(iwgn)%idewpt, wgn(iwgn)%tmpmx, wgn(iwgn)%tmpmn, wgn(iwgn)%dewpt, wgn_pms(iwgn)%pr_wdays, wst(iwst)%weat%precip, wst(iwst)%weat%rhum` |
| [sym:hydrograph_module] | `iwst` |  |
| [sym:time_module] | `time` | `time%mo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%weat%rhum` | When the station humidity is being simulated and the routine reaches the final assignment at line 66. | `wst(iwst)%weat%rhum` is overwritten with the generated daily relative humidity for the current station and month, so later climate and weather routines use this simulated humidity instead of an observed or placeholder value. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:2.3.2 | Saturation vapor pressure | $e^o=exp[\frac{16.78*\overline T_{av}-116.9}{\overline T_{av}+237.3}]$ | e^o = exp[(16.78*T-116.9)/(T+237.3)] inside Ee, called at line 54. |
| 1:3.5.1 | Mean monthly relative humidity | $R_{hmon}=\frac{e_{mon}}{e^o_{mon}}$ | Verified against SWAT+ 62.0.0 (cli_rhgen.f90:54). (RH = Ee(dewpt)/Ee(tmean)) |
| 1:3.5.2 | Monthly saturation vapor pressure | $e^o_{mon}=exp[\frac{16.78*\mu tmp_{mon}-116.9}{\mu tmp_{mon}+237.3}]$ | tmpmean is passed to Ee() as the denominator in rhmo = Ee(dewpt)/Ee(tmpmean). |
| 1:3.5.3 | Monthly actual vapor pressure from dew point | $e_{mon}=exp[\frac{16.78*\mu dew_{mon}-116.9}{\mu dew_{mon}+273.3}]$ | Monthly dew point is passed to Ee() as the numerator in rhmo = Ee(dewpt)/Ee(tmpmean). |
| 1:3.5.4 | Upper RH limit | $R_{hUmon}=R_{hmon}+(1-R_{hmon})*exp(R_{hmon}-1)$ | Verified against SWAT+ 62.0.0 (cli_rhgen.f90). (RH upper limit) |
| 1:3.5.5 | Lower RH limit | $R_{hLmon}=R_{hmon}*(1-exp(-R_{hmon}))$ | Verified against SWAT+ 62.0.0 (cli_rhgen.f90). (RH lower limit) |
| 1:3.5.6 | Generated daily RH (ascending) | $R_h=R_{hmon}*\frac{R_{hLmon}+[rnd_1*(R_{hUmon}-R_{hLmon})*(R_{hmon}-R_{hLmon})]^{0.5}}{R_{hmon,mean}}$ | Verified against SWAT+ 62.0.0 (cli_rhgen.f90). (RH triangular gen) |
| 1:3.5.7 | Generated daily RH (descending) | $R_h=R_{hmon}*\frac{R_{hUmon}-(R_{hUmon}-R_{hmon})*[\frac{R_{hUmon}(1-rnd_1)-R_{hLmon}(1-rnd_1)}{R_{hUmon}-R_{hmon}}]^{0.5}}{R_{hmon,mean}}$ | Verified against SWAT+ 62.0.0 (cli_rhgen.f90). |
| 1:3.5.8 | Monthly RH weighting (wet/dry) | $R_{hmon}*days_{tot}=R_{hWmon}*days_{wet}+R_{hDmon}*days_{dry}$ | Dry-day adjustment built so the wet/dry-weighted mean returns monthly RH. |
| 1:3.5.9 | Wet-day mean RH | $R_{hWmon}=R_{hDmon}+b_H*(1-R_{hDmon})$ | Verified against SWAT+ 62.0.0 (cli_rhgen.f90:62). if (precip>0) rhm = rhm*0.1+0.9` — wet-day RH raise |
| 1:3.5.10 | Dry-day mean RH | $R_{hDmon}=(R_{hmon}-b_H*\frac{days_{wet}}{days_{tot}})*(1.0-b_H*\frac{days_{wet}}{days_{tot}})^{-1}$ | Verified against SWAT+ 62.0.0 (cli_rhgen.f90:60). rhm = (rhmo-yy)/(1.-yy)`, yy=0.9·pr_wdays → b_H hardcoded 0.9 |

## Lineage

`cli_rhgen` was introduced in df07e3f as a new routine to generate weather relative humidity. Later commits did not change the algorithm itself: 39fabde only initialized the local real variables, 889136d only fixed a comment typo, and bd18ad4 only added explicit external declarations for `atri`, `aunif`, and `ee`.

- df07e3f created the routine and its humidity-generation logic, including the dewpoint-to-humidity conversion, wet-day adjustment, humidity bounds, and triangular sampling.
- 39fabde did not alter behavior; it only initialized `vv`, `rhm`, `yy`, `uplm`, `blm`, `rhmo`, and `tmpmean` to zero.
- 889136d did not alter behavior; it only corrected the comment from "Paramenters" to "Parameters".
- bd18ad4 did not alter behavior; it only added `external :: atri, aunif, ee`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_rhgen' has no extracted documentation comment.
