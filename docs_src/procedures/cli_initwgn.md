---
kind: procedure
symbol: cli_initwgn
title: cli_initwgn
status: filled
source_hash: 36db463d9bba77b3
version_label: SWAT+ 62.0.0
args:
  iwgn: '`iwgn` selects which weather-generator station record in `wgn`/`wgn_pms` is initialized;
    all derived values are written for that one index.'
locals:
  xx: Temporary radian latitude value used to compute sine, cosine, and tangent-based daylength
    geometry.
  lattan: Tangent of latitude in radians; used to compute the minimum daylength threshold.
  x1: Intermediate value in the daylength and rainfall calculations; first holds `0.4348 *
    Abs(tan(lat))`, later holds the `0.5 / rain_yrs` term for the rainfall factor.
  x2: Intermediate daylength/rainfall helper; used as the acos input for minimum daylength
    and later as the monthly wet-day denominator `x1 / pcpd(mon)`.
  x3: Intermediate rainfall-intensity term derived from smoothed half-hour rainfall and the
    logarithmic wet-day ratio; used in the `amp_r` calculation.
  tav: Monthly average temperature computed from monthly max and min temperatures; used to
    track annual temperature extrema and to accumulate heat units and PET inputs.
  tmin: Tracks the lowest monthly average temperature seen across the year.
  tmax: Tracks the highest monthly average temperature seen across the year.
  tk: Monthly average temperature converted to Kelvin for the Priestley-Taylor PET calculation.
  alb: Albedo constant used in the Priestley-Taylor net radiation estimate.
  d: Slope of the saturation vapor pressure curve term used in the PET calculation.
  gma: Priestley-Taylor weighting factor derived from `d`; used to scale PET.
  ho: Net radiation / daylight energy term used in the PET calculation.
  aph: Priestley-Taylor alpha coefficient used to compute monthly PET.
  inext: Loop index for initializing and filling the 30-element precipitation/PET linked-list
    arrays.
  sum: Accumulator for 1000 random precipitation samples used to normalize the precipitation
    correction factor.
  summm_p: Annual sum of monthly precipitation, used for annual precipitation totals and climate-region
    classification.
  summm_pet: Annual sum of monthly PET, used to compute the annual precipitation/PET ratio.
  summn_t: Annual sum of monthly minimum temperatures, used in the annual average air-temperature
    summary.
  summx_t: Annual sum of monthly maximum temperatures, used in the annual average air-temperature
    summary.
  rnm2: Second uniform random number used with `rndm1` to generate a normal deviate for the
    precipitation correction sampling.
  r6: Skew-related scaling factor derived from the monthly precipitation skew coefficient
    and used in the precipitation sampling transform.
  xlv: Intermediate transformed variate used to generate sample precipitation values for the
    correction factor.
  rain_hhsm: Smoothed monthly maximum half-hour rainfall, computed as a 3-month moving average
    of `rainhmx` with wraparound at year boundaries.
  rndm1: First uniform random number stream value used as the seed/input for the random sampling
    loop.
  dl: Dormancy daylength threshold stored into `wgn_pms(iwgn)%daylth`; either a basin-specified
    value or a latitude-derived default.
  mon: Monthly loop counter reused in several loops over the 12 months.
  mdays: Number of days in the current month, taken from the leap-year `ndays` array.
  j: Inner-loop counter for the 1000-sample precipitation correction-factor calculation.
  m1: Temporary month index used to find the month following the current one when locating
    the current simulation day within the year.
  nda: Julian day of the last day in a month, used to determine the month containing `time%day_start`.
  cli_dstn1: External normal-deviate generator called to transform two uniform random numbers
    into a standard-normal sample for precipitation normalization.
  pcp_gen: Synthetic daily precipitation value generated during the 1000-sample loop, before
    averaging to form the correction factor.
  aunif: External uniform-random-number generator used to seed and advance the stochastic
    precipitation-sampling stream.
  xrnd: Integer random-number seed copied from `rndseed(idg(3),iwgn)` and advanced by `aunif`.
  mo_ppet: Reference month for initializing the 30-day precip/PET arrays; set to the previous
    month, or December when `time%mo` is January.
uses:
  basin_module: '`basin_module` matters because the basin parameter `bsn_prm%dorm_hr` overrides
    the default latitude-based dormancy threshold when it is set, and `bsn_prm%adj_pkr` scales
    the monthly rainfall intensity factor `amp_r` computed here.'
  climate_module: '`climate_module` matters because this routine reads the station weather-generator
    inputs from `wgn(iwgn)` and writes all derived monthly and annual generator parameters
    into `wgn_pms(iwgn)`, which later weather generation and climate-dependent processes consume.'
  time_module: '`time_module` matters because `time%mo` determines which month is used to
    seed the 30-day precipitation/PET moving-window arrays, and `time%day_start` determines
    the month index used when initializing soil-layer temperature conditions.'
---

<!-- facts:header -->

Initializes one weather-generator record by deriving latitude, dormancy, rainfall, precipitation, PET, and climate classification parameters from the already-read .wgn data.

## Bottom Line

`cli_initwgn` takes the monthly weather-generator inputs for a single station/index `iwgn` and converts them into the derived climate parameters SWAT+ uses later in simulation. It computes latitude geometry, minimum daylength, dormancy threshold, smoothed half-hour rainfall, monthly wet-day and precipitation statistics, monthly PET, and annual climate summaries.

It also allocates and seeds the 30-day precipitation/PET moving-window arrays, detects whether dew point or relative humidity is being supplied, derives monthly precipitation correction and rainfall-intensity factors, and assigns the annual precipitation category. These results feed later climate generation and time-step weather behavior.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after `cli_wgnread` has read a station’s monthly weather-generator record from the .wgn file and before the climate state is used by the rest of the model. Its outputs are used later by weather generation, precipitation/PET ratio tracking, dormancy logic, and precipitation-region classification during simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute latitude geometry and daylength bounds | Convert latitude to radians, store sine and cosine in `wgn_pms(iwgn)`, compute tangent-based minimum daylength, and set the dormancy threshold `daylth` from basin settings or latitude rules. |
| 2. Smooth monthly half-hour rainfall maxima | Build `rain_hhsm` as a 3-month moving average of `wgn(iwgn)%rainhmx`, wrapping December and January at the ends of the year. |
| 3. Reset annual accumulators and scan months | Loop through all 12 months to derive monthly and annual climate summaries, including heat units, wet-day statistics, precipitation means, and PET. |
| 4. Derive monthly precipitation statistics | Check and repair wet-day probabilities when needed, compute wet-day fraction, monthly mean precipitation per wet day, clamp skew minimums, and accumulate annual precipitation totals and wet-day counts. |
| 5. Compute monthly PET with Priestley-Taylor | Use monthly average temperature, solar radiation, and the Priestley-Taylor formulation to populate `wgn_pms(iwgn)%pet(mon)` and accumulate annual PET. |
| 6. Detect dew point input type | Set `idewpt` to indicate dew-point input by default, then flip it to relative-humidity input if any monthly dew point values fall outside 0..1. |
| 7. Allocate and seed 30-day moving arrays | Allocate `mne_ppet`, `precip_mce`, and `pet_mce`, then initialize the linked-list next-element array for the 30-day moving window. |
| 8. Seed precipitation/PET moving-window values | Choose the prior month based on `time%mo`, clear the running sums, and fill all 30 slots with per-day precipitation and PET rates from that month. |
| 9. Finalize annual climate summaries | Store annual precipitation, precipitation/PET ratio, and mean air temperature summaries into `wgn_pms(iwgn)`. |
| 10. Find the month containing simulation start day | Use `time%day_start` and `ndays` to determine the month index used when initializing soil-layer temperatures. |
| 11. Initialize the random-number stream | Copy the station seed from `rndseed(idg(3),iwgn)` and draw the first uniform variate used by the precipitation sampling loop. |
| 12. Compute monthly precipitation correction factors | For each month, generate 1000 synthetic daily precipitation samples with `aunif` and `cli_dstn1`, average them, and store the normalization factor `pcf(mon)`. |
| 13. Derive monthly rainfall intensity factor | Build the monthly `amp_r` factor from smoothed half-hour rainfall, annual rain record length, monthly wet-day frequency, and basin adjustment, then clamp it to [0.1, 0.95]. |
| 14. Classify annual precipitation region and return | Assign `ireg` from annual precipitation totals and exit the routine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%dorm_hr, bsn_prm%adj_pkr` |
| [sym:climate_module] | `wgn, wgn_pms` | `wgn(iwgn)%lat, wgn_pms(iwgn)%latsin, wgn_pms(iwgn)%latcos, wgn_pms(iwgn)%daylmn, wgn_pms(iwgn)%daylth, wgn(iwgn)%rainhmx(1), wgn(iwgn)%rainhmx(2), wgn(iwgn)%rainhmx(mon), wgn(iwgn)%rainhmx(mon+1), wgn(iwgn)%rainhmx(12), wgn(iwgn)%tmpmx(mon), wgn(iwgn)%tmpmn(mon), wgn_pms(iwgn)%phutot, wgn(iwgn)%pr_ww(mon), wgn(iwgn)%pr_wd(mon), wgn(iwgn)%pcpd(mon), wgn_pms(iwgn)%pr_wdays(mon), wgn_pms(iwgn)%pcpmean(mon), wgn(iwgn)%pcpmm(mon), wgn(iwgn)%pcpskw(mon), wgn_pms(iwgn)%pcpdays, wgn(iwgn)%solarav(mon), wgn_pms(iwgn)%pet(mon), wgn_pms(iwgn)%idewpt, wgn(iwgn)%dewpt(mon), wgn_pms(iwgn)%mne_ppet(ppet_ndays), wgn_pms(iwgn)%precip_mce(ppet_ndays), wgn_pms(iwgn)%pet_mce(ppet_ndays), wgn_pms(iwgn)%mne_ppet(inext), wgn_pms(iwgn)%precip_sum, wgn_pms(iwgn)%pet_sum, wgn_pms(iwgn)%precip_mce(inext), wgn(iwgn)%pcpmm(mo_ppet), wgn_pms(iwgn)%pet_mce(inext), wgn_pms(iwgn)%pet(mo_ppet), wgn_pms(iwgn)%pcp_an, wgn_pms(iwgn)%ppet_an, wgn_pms(iwgn)%tmp_an, wgn(iwgn)%pcpstd(mon), wgn_pms(iwgn)%pcf(mon), wgn(iwgn)%rain_yrs, wgn_pms(iwgn)%amp_r(mon), wgn_pms(iwgn)%ireg` |
| [sym:time_module] | `time, ndays` | `time%mo, time%day_start` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wgn_pms(iwgn)%latsin` | When `bsn_prm%dorm_hr` is below `1.e-6`, or when the basin dormancy override is absent and the latitude rule is applied at lines 138-146. | `wgn_pms(iwgn)%latsin` is set to `Sin(xx)` where `xx` is latitude in radians, so later climate logic can use the station’s latitude geometry without recomputing it. |
| `wgn_pms(iwgn)%latcos` | When `bsn_prm%dorm_hr` is below `1.e-6`, or when the basin dormancy override is absent and the latitude rule is applied at lines 138-146. | `wgn_pms(iwgn)%latcos` is set to `Cos(xx)` so later model code can use the station’s latitude cosine directly. |
| `wgn_pms(iwgn)%daylmn` | When the latitude-derived minimum-daylength calculation runs at lines 127-133. | `wgn_pms(iwgn)%daylmn` stores the shortest daylength for this station, which later supports dormancy-related climate behavior. |
| `wgn_pms(iwgn)%daylth` | When the dormancy-threshold logic completes at lines 135-148. | `wgn_pms(iwgn)%daylth` stores the active dormancy threshold hours, either basin-defined or derived from latitude, for later plant-dormancy decisions. |
| `wgn(iwgn)%pr_wd(mon)` | On each monthly loop iteration when `pr_ww(mon) <= pr_wd(mon)` or `pr_wd(mon) <= 0.`; otherwise the existing wet-day probabilities are used to infer `pcpd(mon)`. | `wgn(iwgn)%pr_wd(mon)` is repaired or recalculated so the monthly wet-day probability is consistent with precipitation-day counts. |
| `wgn(iwgn)%pr_ww(mon)` | On each monthly loop iteration when `pr_ww(mon) <= pr_wd(mon)` or `pr_wd(mon) <= 0.`; otherwise the existing wet-day probabilities are used to infer `pcpd(mon)`. | `wgn(iwgn)%pr_ww(mon)` is repaired or recalculated so the wet-after-wet probability is compatible with the wet-day probability and monthly precipitation-day count. |
| `wgn(iwgn)%pcpd(mon)` | On each monthly loop iteration when wet-day probabilities are bad or when `pcpd(mon)` is inferred from them. | `wgn(iwgn)%pcpd(mon)` becomes the monthly number of precipitation days, either repaired to a minimum or derived from the Markov-chain wet-day probabilities. |
| `wgn_pms(iwgn)%pr_wdays(mon)` | On each monthly loop iteration after `pcpd(mon)` is established. | `wgn_pms(iwgn)%pr_wdays(mon)` is updated to the proportion of wet days in the month by dividing precipitation days by days in month. |
| `wgn_pms(iwgn)%pcpmean(mon)` | On each monthly loop iteration after `pcpd(mon)` is established. | `wgn_pms(iwgn)%pcpmean(mon)` stores the average precipitation per wet day for the month. |
| `wgn_pms(iwgn)%pcpdays` | On each monthly loop iteration after `pcpd(mon)` is established. | `wgn_pms(iwgn)%pcpdays` accumulates the annual total number of precipitation days across all months. |
| `wgn_pms(iwgn)%pet(mon)` | On each monthly loop iteration when monthly PET is computed with Priestley-Taylor. | `wgn_pms(iwgn)%pet(mon)` stores the monthly potential evapotranspiration for the station. |
| `wgn_pms(iwgn)%idewpt` | After scanning all 12 monthly dew point values. | `wgn_pms(iwgn)%idewpt` is set to 1 for dew point input or 0 if the monthly values look like relative humidity, so later code knows how to interpret the weather file. |
| `ppet_ndays` | Right before the 30-day precipitation/PET window is allocated. | `ppet_ndays` is fixed to 30 so the moving-window arrays have a consistent length for later daily updates. |
| `wgn_pms(iwgn)%mne_ppet(inext)` | During the 30-day window initialization loop. | `wgn_pms(iwgn)%mne_ppet(inext)` is initialized as a simple next-element link from 1 to 30, establishing the circular-style storage order for the moving window. |
| `wgn_pms(iwgn)%precip_sum` | After selecting the reference month from `time%mo` and clearing the running totals. | `wgn_pms(iwgn)%precip_sum` is filled with the 30-day sum of daily precipitation rates for the reference month and becomes the baseline moving precipitation sum. |
| `wgn_pms(iwgn)%pet_sum` | After selecting the reference month from `time%mo` and clearing the running totals. | `wgn_pms(iwgn)%pet_sum` is filled with the 30-day sum of daily PET rates for the reference month and becomes the baseline moving PET sum. |
| `wgn_pms(iwgn)%precip_mce(inext)` | During the 30-day initialization loop for the reference month. | `wgn_pms(iwgn)%precip_mce(inext)` stores a per-day precipitation rate copied from the reference month so the moving window has initial content. |
| `wgn_pms(iwgn)%pet_mce(inext)` | During the 30-day initialization loop for the reference month. | `wgn_pms(iwgn)%pet_mce(inext)` stores a per-day PET rate copied from the reference month so the moving window has initial content. |
| `wgn_pms(iwgn)%pcp_an` | After the annual monthly precipitation totals are accumulated. | `wgn_pms(iwgn)%pcp_an` becomes the annual precipitation total for this station. |
| `wgn_pms(iwgn)%ppet_an` | After the annual monthly precipitation totals and PET totals are accumulated. | `wgn_pms(iwgn)%ppet_an` becomes the annual precipitation-to-PET ratio, with a small-denominator guard if annual PET is nearly zero. |
| `wgn_pms(iwgn)%tmp_an` | After the annual monthly temperature sums are accumulated. | `wgn_pms(iwgn)%tmp_an` becomes the annual mean air temperature summary derived from the total monthly max and min sums. |
| `wgn_pms(iwgn)%pcf(mon)` | During the monthly precipitation correction-factor loop. | `wgn_pms(iwgn)%pcf(mon)` is normalized from the Monte Carlo precipitation samples, or set to 1. when the sampled sum is not positive. |
| `wgn_pms(iwgn)%amp_r(mon)` | During the monthly rainfall-factor loop after `rain_hhsm`, `rain_yrs`, and `pcpmean(mon)` are known. | `wgn_pms(iwgn)%amp_r(mon)` is derived from the smoothed half-hour rainfall and basin adjustment, then clamped to a valid range. |
| `wgn_pms(iwgn)%ireg` | At the end of the routine after annual precipitation has been summed. | `wgn_pms(iwgn)%ireg` is assigned to precipitation region 1, 2, or 3 based on annual precipitation thresholds. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:3.2.1 | Smoothed monthly max half-hour rain | $R_{0.5sm(mon)}=\frac{R_{0.5x(mon-1)}+R_{0.5x(mon)}+R_{0.5x(mon+1)}}{3}$ | Verified against SWAT+ 62.0.0 (cli_initwgn.f90:154). |
| 1:3.2.2 | Monthly half-hour rainfall factor | $\alpha_{0.5mon}=adj_{0.5\alpha}*[1-exp(\frac{R_{0.5sm(mon)}}{{\mu_{mon}}*ln*(\frac{0.5}{yrs*days_{wet}})})]$ | amp_r(mon) = adj_pkr*(1 - exp(x3/...)) from smoothed half-hour rainfall, with fallback at line 297 and clamped to [0.1,0.95] at lines 299-300. |

## Lineage

Resolved lineage shows four behavior changes to `cli_initwgn`: the original implementation was added in `df07e3f`; `c7c8e22` imported the routine from upstream bitbucket; `39fabde` initialized local variables and arrays to zero; `889136d` fixed the `summn_t` comment typo; and `c641594` guarded `ppet_an` against division by very small annual PET.

- `39fabde` made the local working variables and `rain_hhsm` explicitly initialize to zero, reducing dependence on implicit or uninitialized values during climate setup.
- `889136d` only corrected the `summn_t` comment from “mimimum” to “minimum”; it did not change runtime behavior.
- `c641594` changed the annual precipitation/PET ratio calculation so `ppet_an` uses a 1.e-3 floor on annual PET instead of dividing unconditionally, avoiding a small-denominator blow-up.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_initwgn' has no extracted documentation comment.
- algorithm_steps revised: split the original coarse steps into 14 source-backed steps to match the routine's actual control flow and state updates.
- Source uncertainty: `cli_wgnread` snippet shows the initialization call, but the broader caller setup outside the snippet is not visible in the packet.
- `ci_initwgn` is a weather-generator initialization routine, not an I/O routine; file reading happens in `cli_wgnread` before this call.
