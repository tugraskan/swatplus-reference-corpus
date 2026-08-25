---
kind: procedure
symbol: cli_clgen
title: cli_clgen
status: filled
source_hash: 1c057af7c8d729a7
version_label: SWAT+ 62.0.0
args:
  iwgn: Selects which weather generator parameter set and station latitude values to use;
    `iwgn` indexes `wgn_pms(iwgn)` and the matching station-dependent radiation fractions
    `frad(iwgn, :)`.
locals:
  ii: Loop counter over subdaily time steps when building the hourly radiation distribution,
    and reused to store each fraction.
  sd: Solar declination angle for the current simulation day, used in daylength and radiation
    geometry.
  sdlat: Intermediate value for `-tan(sd) * tan(latitude)`, used to decide whether sunrise/sunset
    exists and to compute the half-day hour angle.
  h: Half-day hour angle in radians; controls computed daylength and the clear-sky radiation
    integral.
  ys: Precomputed `sin(sd) * sin(latitude)` term used in the radiation formulas.
  yc: Precomputed `cos(sd) * cos(latitude)` term used in the radiation formulas.
  dd: Earth-Sun दूरी factor for the current day, used to scale maximum potential radiation.
  cosrho: Temporary array holding the cosine-of-zenith-angle term for each subdaily time step
    before it is normalized into `frad`.
  totrho: Accumulator for the sum of positive `cosrho` values across the day; used to normalize
    each subdaily fraction.
  hr_angle: Hour-angle at the midpoint of each subdaily interval, used to compute instantaneous
    solar geometry for that interval.
uses:
  basin_module: '`basin_module` matters because it provides the basin-level station index
    `iwst`, which links the selected weather generator index to the active weather station
    record that this routine updates.'
  climate_module: '`climate_module` matters because it holds the weather-station state and
    weather-generator latitude parameters that determine precipitation status, daylength,
    clear-sky radiation, and the per-step radiation fractions written by this routine.'
  time_module: '`time_module` matters because the current simulation day, the number of subdaily
    steps, and the step length control the solar declination calculation, the daylength scaling,
    and the hourly distribution loop.'
  hydrograph_module: '`hydrograph_module` matters because it supplies the current weather-station
    index `iwst`, which this routine uses to store results back into the active station’s
    weather state.'
---

<!-- facts:header -->

Generates daily solar-radiation timing factors for one weather generator station. It also updates the station’s daylength, maximum clear-sky radiation, and whether the previous day was wet or dry.

## Bottom Line

`cli_clgen` is a climate helper routine called once per weather station to derive solar geometry for the current day. Using the simulation day, the station’s latitude parameters, and the current subdaily time-step setting, it computes daylength, an upper bound on clear-sky radiation, and the fraction of daily radiation assigned to each time step.

It also tags the current station’s prior-day precipitation state as `wet` or `dry` based on today’s precipitation amount. Those outputs feed later climate/radiation generation and any downstream routines that need subdaily radiation weights.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the climate-control daily update, after `climate_control` has assigned the active weather-generator index for each weather station and before subdaily solar radiation is generated or used elsewhere in the climate workflow. Its results are later consumed when hourly radiation is distributed for the station and when the model needs the station’s updated daylength, maximum radiation, or prior-day precipitation category.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. classify prior day precipitation | Uses the current station’s precipitation amount to set `wst(iwst)%weat%precip_prior_day` to `wet` when precipitation is at least 0.1, otherwise `dry`. |
| 2. compute solar declination | Computes the day’s solar declination from the simulation day number. |
| 3. compute Earth-Sun distance factor | Calculates the relative Earth-Sun distance scaling factor used to adjust clear-sky radiation. |
| 4. form sunrise geometry term | Builds `sdlat` from latitude sine/cosine terms and declination so the code can decide whether the location has normal daylength, polar night, or polar day behavior. |
| 5. resolve half-day hour angle | Sets `h` to zero for polar night, to `Acos(sdlat)` for normal conditions, or to pi for polar day, then uses `h` to derive station daylength. |
| 6. store daylength | Writes the computed daylength into the station’s daily weather record. |
| 7. precompute latitude declination terms | Computes `ys` and `yc` from latitude and declination, then uses them with `dd` and `h` to calculate the station’s maximum clear-sky solar radiation. |
| 8. clear hourly arrays | Initializes the hourly cosine-radiation array and the daily sum accumulator before distributing radiation across the day. |
| 9. loop over subdaily steps | For each subdaily step, computes the midpoint hour angle, evaluates the cosine-of-zenith term, clips negative values to zero, and accumulates the daily total. |
| 10. normalize to fractions | When the daily total is large enough, divides each positive hourly cosine term by the total and stores the normalized fraction in `frad(iwgn,ii)`. |
| 11. return | Exits after updating the station weather fields and radiation fractions for the current day. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `wst, wgn_pms, frad` | `wst(iwst)%weat%precip, wst(iwst)%weat%precip_prior_day, wgn_pms(iwgn)%latsin, wst(iwst)%weat%daylength, wgn_pms(iwgn)%latcos, wst(iwst)%weat%solradmx, wst(iwst), wgn_pms(iwgn), frad(iwgn,ii)` |
| [sym:climate_module] | `wst, wgn_pms, frad` | `wst(iwst)%weat%precip, wst(iwst)%weat%precip_prior_day, wgn_pms(iwgn)%latsin, wst(iwst)%weat%daylength, wgn_pms(iwgn)%latcos, wst(iwst)%weat%solradmx` |
| [sym:time_module] | `time` | `time%day, time%step, time%dtm` |
| [sym:hydrograph_module] | `iwst, wet` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%weat%precip_prior_day` | When `wst(iwst)%weat%precip >= 0.1` the routine marks the prior day as wet; otherwise it marks it dry. | `wst(iwst)%weat%precip_prior_day` is refreshed at the start of the daily climate update so later weather logic can distinguish whether the immediately preceding day was wet or dry. |
| `wst(iwst)%weat%daylength` | Always, after computing the solar declination and resolving `h` for the current latitude/day combination. | `wst(iwst)%weat%daylength` is updated to the calculated daylight duration for the current day at the station latitude. |
| `wst(iwst)%weat%solradmx` | Always, after computing `dd`, `h`, `ys`, and `yc` for the current day and station latitude. | `wst(iwst)%weat%solradmx` is set to the station’s estimated maximum clear-sky daily solar radiation for the current day. |
| `frad(iwgn,ii)` | Only when `totrho > 0.001` after summing positive cosine-of-zenith values over all subdaily steps. | `frad(iwgn,ii)` is filled with normalized hourly radiation fractions so later routines can distribute daily solar radiation across the day. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:1.1.1 | Earth-Sun distance factor E0 | $E_0 = (r_0/r)^2 = 1+ 0.033 cos [(2\pi d_n /365)]$ | dd = 1 + 0.033*Cos(day/58.09); 58.09 = 365/2pi. |
| 1:1.1.2 | Solar declination | $\delta = sin^{-1} \{0.4sin [ 2 \pi /365] (d_n - 82)\}$ | sd = Asin(0.4*Sin((day-82)/58.09)); 0.4 ~ sin(23.5deg). |
| 1:1.1.3 | Cosine of solar zenith angle | $\cos\theta_z = \sin\delta\sin\phi + \cos\delta \cos\phi\cos\omega t$ | Verified against SWAT+ 62.0.0 (cli_clgen.f90:110). |
| 1:1.1.4 | Sunrise (hour angle) | $T_{SR} = +(\cos^{-1}[-\tan\delta \tan\phi]/\omega)$ | Verified against SWAT+ 62.0.0 (cli_clgen.f90). |
| 1:1.1.5 | Sunset (hour angle) | $T_{SS} = - (\cos^{-1}[-tan \delta \tan\phi]/\omega)$ | Verified against SWAT+ 62.0.0 (cli_clgen.f90). |
| 1:1.1.6 | Daylength | $T_{DL} = (2 \cos^ {-1}[-1\tan \delta \tan \phi]/\omega)$ | Verified against SWAT+ 62.0.0 (cli_clgen.f90:88). |
| 1:1.2.1 | Extraterrestrial normal irradiance | $I_{0n} = I_{SC}E_0$ | I0n = Isc*E0; folded into solradmx (E0 = dd). |
| 1:1.2.2 | Irradiance on horizontal | $I_0 = I_{0n} \cos\theta_z = I_{SC}E_0\cos\theta_z$ | Verified against SWAT+ 62.0.0 (cli_clgen.f90:94). solradmx = 30.*dd*(h*ys+yc*Sin(h))` — I_0=I_SC·E_0·cosθz integrated to daily (dd=E_0) |
| 1:1.2.3 | Daily integral of irradiance | $H_0 = \int_{SR}^{SS} I_0dt = 2 \int_0^{SS} I_0dt$ | H0 = integral sunrise->sunset; step toward line 94. |
| 1:1.2.4 | Integrated daily radiation | $H_0 = \frac{24}{\pi} I_{SC}E_0\int_0^{\omega T_{SR} }(\sin\delta \sin\phi+\cos\delta\cos\phi\cos\omega t)d\omega t$ | Integration over hour angle; step toward line 94. |
| 1:1.2.5 | Evaluated daily radiation | $H_0 = \frac{24}{\pi} I_{SC}E_0[{\omega T_{SR} }(\sin\delta \sin\phi+\cos\delta\cos\phi\sin(\omega T_{SR}))]$ | Closed form (24/pi)Isc*E0[...]; step toward line 94. |
| 1:1.2.7 | Solar radiation under cloudless skies | $H_{MX} = 30.0E_0[{\omega T_{SR} }\sin\delta \sin\phi+\cos\delta\cos\phi\sin(\omega T_{SR})]$ | solradmx = 30*dd*(h*ys + yc*Sin(h)); 30.0 bundles the solar constant with cloudless-sky transmittance. |
| 1:1.2.8 | Instantaneous radiation over the day | $I_0=I_{SC}E_0(\sin\delta\sin\phi+\cos\delta\cos\phi\cos\omega t)$ | cosrho = ys + yc*Cos(hr_angle) is proportional to instantaneous I0. |
| 1:1.2.9 | Hourly radiation from daily total | $I_{hr}=I_{frac} H_{day}$ | I_hr = I_frac*H_day; cli_clgen computes I_frac=frad, product formed downstream. |
| 1:1.2.10 | Hourly radiation fraction | $I_{frac}=\frac {\displaystyle(\sin\delta\sin\phi + \cos\delta\cos\phi\cos\omega t_i)} {\displaystyle\sum_{t=SR}^{SS}(\sin\delta\sin\phi+\cos\delta\cos\omega t)}$ | frad = cosrho/totrho, normalized cosine-of-zenith distribution. |

## Lineage

Resolved lineage shows three commits affecting `cli_clgen`: `df07e3f` added the routine with its documentation comments and full implementation; `39fabde` initialized the local scalars and counter at declaration; `889136d` corrected comment typos only, without changing computational behavior.

- df07e3f introduced `cli_clgen` and implemented the full daylength, maximum radiation, and hourly radiation-fraction calculations.
- 39fabde changed local variable declarations to initialize `ii`, `sd`, `sdlat`, `h`, `ys`, `yc`, `dd`, `totrho`, and `hr_angle` to zero at declaration.
- 889136d updated documentation comments only, including spelling fixes for the `frad` description and the hourly radiation comment.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_clgen' has no extracted documentation comment.
