---
kind: procedure
symbol: climate_control
title: climate_control
status: filled
source_hash: 722667239fea44de
version_label: SWAT+ 62.0.0
locals:
  ii: 'Loop counter for subdaily temperature steps during climate-change precipitation scaling.
    Initial value: 0.'
  half_hr_mn: 'Lower bound used when sampling the daily half-hour rainfall fraction. Initial
    value: 0.'
  half_hr_mx: 'Upper bound used when sampling the daily half-hour rainfall fraction. Initial
    value: 0.'
  iwgn: 'Weather-generator index for the current station. Initial value: 0.'
  ig: 'Measured climate record index selected from station codes. Initial value: 0.'
  yrs_to_start: 'Offset from the measured record start year to the current simulation year.
    Initial value: 0.'
  cur_day: 'Current simulation day copied from time%day before bounds checking. Initial value:
    0.'
  ramm: 'Extraterrestrial radiation term used in the Hargreaves PET calculation. Initial value:
    0.'
  xl: 'Latent heat of vaporization term used in the Hargreaves PET calculation. Initial value:
    0.'
  atri: Triangular-distribution draw used to compute the half-hour rainfall fraction.
  xx: 'Intermediate exponent argument used to derive the half-hour rainfall fraction. Initial
    value: 0.'
  out_bounds: 'One-character flag set by cli_bounds_check to indicate whether a measured climate
    record is outside the current simulation date. Initial value: ''n''.'
uses:
  climate_module: Provides the station weather records, measured climate series, weather-generator
    parameters, and climate-change increments that this routine reads and updates each day.
---

<!-- facts:header -->

Controls daily climate inputs for all weather stations. It reads or generates precipitation, temperature, solar radiation, humidity, wind, PET, and several derived climate indices, then applies monthly climate-change adjustments.

## Bottom Line

`climate_control` is the central daily weather driver for SWAT+. For each weather station it selects measured data when available, falls back to weather-generator routines when records are missing or simulated, and then computes derived fields such as dew point, climatic moisture index, half-hour rainfall fraction, and base-zero heat units.

It matters because later hydrology, plant growth, and routing calculations consume the populated station weather state. The routine also applies monthly climate-change increments to precipitation, temperature, solar radiation, and humidity before returning.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from time_control after the simulation time state has been advanced for the day. It populates the station weather state that later climate, hydrology, and plant-growth routines consume.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Generate precipitation | Call the precipitation control routine to prepare daily precipitation inputs before other climate fields are processed. |
| 2. Loop stations for temperature | For each weather station, select the weather-generator index, generate temperature if configured, otherwise read measured temperature with bounds checking and fallback generation, then compute daily mean temperature. |
| 3. Loop stations for solar radiation | For each station, prepare radiation generator state, generate solar radiation when configured, otherwise read measured radiation with bounds checking and fallback generation. |
| 4. Loop stations for humidity | For each station, generate or read relative humidity, then compute dew point from temperature and humidity. |
| 5. Loop stations for wind speed | For each station, generate or read wind speed with bounds checking and fallback generation. |
| 6. Read or estimate PET | For each station, read measured PET when available; otherwise estimate PET with the Hargreaves method when the measured value is missing. |
| 7. Update moisture and lag state | Update the 30-day precip/PET moving sums, climatic moisture index, and the station air-temperature lag array used later for stream temperature. |
| 8. Sample half-hour rainfall fraction | Compute the maximum half-hour rainfall fraction for each station using a triangular draw and store it in the station weather state. |
| 9. Update base-zero heat units | Accumulate base-zero heat units from daily mean temperature and reset them at year end. |
| 10. Apply climate adjustments | Apply monthly climate-change increments to precipitation, subdaily temperature series, solar radiation, and humidity, with lower and upper bounds where needed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `wst, tmp, slr, hmd, wnd, petm, wgn_pms` | `wst(iwst)%wco%wgn, wst(iwst)%wco_c%tgage, wst(iwst)%wco%tgage, tmp(ig)%start_day, tmp(ig)%start_yr, tmp(ig)%end_day, tmp(ig)%end_yr, wst(iwst)%weat%tmax, wst(iwst)%weat%tmin, tmp(ig)%yrs_start, tmp(ig)%ts, tmp(ig)%ts2, tmp(ig)%days_gen, wst(iwst)%weat%tave, wst(iwst)%wco_c%sgage, wst(iwst)%wco%sgage, slr(ig)%start_day, slr(ig)%start_yr, slr(ig)%end_day, slr(ig)%end_yr, wst(iwst)%weat%solrad, slr(ig)%yrs_start, slr(ig)%ts, slr(ig)%days_gen, wst(iwst)%wco_c%hgage, wst(iwst)%wco%hgage, hmd(ig)%start_day, hmd(ig)%start_yr, hmd(ig)%end_day, hmd(ig)%end_yr, wst(iwst)%weat%rhum, hmd(ig)%yrs_start, hmd(ig)%ts, hmd(ig)%days_gen, wst(iwst)%weat%dewpt, wst(iwst)%wco_c%wgage, wst(iwst)%wco%wgage, wnd(ig)%start_day, wnd(ig)%start_yr, wnd(ig)%end_day, wnd(ig)%end_yr, wst(iwst)%weat%windsp, wnd(ig)%yrs_start, wnd(ig)%ts, wnd(ig)%days_gen, wst(iwst)%wco%petgage, petm(ig)%start_day, petm(ig)%start_yr, petm(ig)%end_day, petm(ig)%end_yr, wst(iwst)%weat%pet, petm(ig)%yrs_start, petm(ig)%ts, wst(iwst)%weat%solradmx, wst(iwst)%weat%ppet, wst(iwst)%weat%precip, wgn_pms(iwgn)%precip_sum, wgn_pms(iwgn)%precip_mce(ppet_mce), wgn_pms(iwgn)%pet_sum, wgn_pms(iwgn)%pet_mce(ppet_mce), wgn_pms(iwgn)%p_pet_rto, wst(iwst)%tlag_mne, wst(iwst)%airlag_temp, wst(iwst)%weat%precip_half_hr, wgn_pms(iwgn)%phutot, wst(iwst)%weat%phubase0, wst(iwst)%rfinc, wst(iwst)%weat%ts(ii), wst(iwst)%tmpinc, wst(iwst)%radinc, wst(iwst)%huminc` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%weat%tmax` | When a station is configured to simulate temperature or when measured temperature is missing | Set from the temperature generator or from measured data; missing values are replaced by generated temperatures and later adjusted by climate-change increments. |
| `wst(iwst)%weat%tmin` | When a station is configured to simulate temperature or when measured temperature is missing | Set from the temperature generator or from measured data; missing values are replaced by generated temperatures and later adjusted by climate-change increments. |
| `tmp(ig)%days_gen` | When measured temperature is missing and generation is needed | Incremented to count how many measured temperature days had to be generated for the record. |
| `wst(iwst)%weat%tave` | After temperature is finalized for the station | Computed as the daily mean of maximum and minimum temperature. |
| `wst(iwst)%weat%solrad` | When a station is configured to simulate solar radiation or when measured radiation is missing | Set from the solar-radiation generator or measured record, then later adjusted by climate-change increments and bounded at zero. |
| `slr(ig)%days_gen` | When measured solar radiation is missing and generation is needed | Incremented to count how many measured solar-radiation days had to be generated for the record. |
| `wst(iwst)%weat%rhum` | When a station is configured to simulate humidity or when measured humidity is missing | Set from the humidity generator or measured record, then later adjusted by climate-change increments and bounded to the valid range. |
| `hmd(ig)%days_gen` | When measured humidity is missing and generation is needed | Incremented to count how many measured humidity days had to be generated for the record. |
| `wst(iwst)%weat%dewpt` | After humidity and temperature are available | Computed from daily mean temperature and relative humidity using the simple Lawrence (2005) dewpoint relation. |
| `wst(iwst)%weat%windsp` | When a station is configured to simulate wind or when measured wind speed is missing | Set from the wind generator or measured record, then used by later climate and evapotranspiration calculations. |
| `wnd(ig)%days_gen` | When measured wind speed is missing and generation is needed | Incremented to count how many measured wind-speed days had to be generated for the record. |
| `wst(iwst)%weat%pet` | When measured PET is available or when Hargreaves PET is needed | Set from the measured PET record when present; otherwise estimated with the Hargreaves method when the measured value is missing. |
| `ppet_mce` | Each day after PET and precipitation are available | Advanced as a circular index into the 30-day precip/PET moving-sum arrays. |
| `wst(iwst)%weat%ppet` | Each day after PET and precipitation are available | Accumulated climatic moisture index based on the station's daily precipitation divided by PET when PET is sufficiently large. |
| `wgn_pms(iwgn)%precip_sum` | Each day after PET and precipitation are available | Updated as a 30-day moving sum of precipitation for the weather-generator group. |
| `wgn_pms(iwgn)%pet_sum` | Each day after PET and precipitation are available | Updated as a 30-day moving sum of PET for the weather-generator group. |
| `wgn_pms(iwgn)%p_pet_rto` | Each day after PET and precipitation are available | Updated as the 30-day precipitation-to-PET ratio, with a small denominator safeguard. |
| `wgn_pms(iwgn)%precip_mce(ppet_mce)` | Each day after PET and precipitation are available | Stores the current day's precipitation in the circular moving-sum buffer. |
| `wgn_pms(iwgn)%pet_mce(ppet_mce)` | Each day after PET and precipitation are available | Stores the current day's PET in the circular moving-sum buffer. |
| `wst(iwst)%tlag(wst(iwst)%tlag_mne)` | Each day after temperature is available | Stores the current daily mean temperature in the station's lag array for later stream-temperature use. |
| `wst(iwst)%tlag_mne` | Each day after temperature is available | Advances the lag-array pointer and wraps it after six days. |
| `wst(iwst)%airlag_temp` | Each day after temperature is available | Set to the lagged temperature value selected by the updated lag pointer. |
| `wst(iwst)%weat%precip_half_hr` | Each day after precipitation is available | Set to a triangularly sampled fraction representing the maximum half-hour rainfall share for the day. |
| `wst(iwst)%weat%phubase0` | When base-zero heat units are positive and the day is not year-end reset | Accumulated from daily mean temperature divided by the weather-generator annual heat-unit total; reset to zero at year end or when the annual total is nonpositive. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:1.2.6 | Daily radiation (37.59 coefficient) | $H_0 = 37.59E_0[{\omega T_{SR} }\sin\delta \sin\phi+\cos\delta\cos\phi\sin(\omega T_{SR})]$ | Verified against SWAT+ 62.0.0 (climate_control.f90:183). |
| 1:3.2.4 |  | $\alpha_{0.5}=\alpha_{0.5mon}*\frac{\alpha_{0.5L}+[rnd_1*(\alpha_{0.5U}-\alpha_{0.5L})*(\alpha_{0.5mon}-\alpha_{0.5L})]^{0.5}}{\alpha_{0.5mean}}$ | Verified against SWAT+ 62.0.0 (climate_control.f90:243). max half-hr rain via `Atri` triangular sampler (rnd₁ lower branch) |
| 1:3.2.5 |  | $\alpha_{0.5}=\alpha_{0.5mon}*(\frac{\alpha_{0.5U}-(\alpha_{0.5U}-\alpha_{0.5mon})*[\frac{\alpha_{0.5U}(1-rnd_1)-\alpha_{0.5L}(1-rnd_1)}{\alpha_{0.5U}-\alpha_{0.5mon}}]^{0.5}}{\alpha_{0.5mean}})$ | Verified against SWAT+ 62.0.0 (climate_control.f90:243). same Atri call (rnd₁ upper branch) |
| 1:4.2.1 |  | $R_{day}=R_{day}*(1+\frac{adj_{pcp}}{100})$ | Verified against SWAT+ 62.0.0 (climate_control.f90:260). precip = precip*(1.+rfinc/100.) |
| 1:4.2.2 |  | $T_{mx}=T_{mx}+adj_{tmp}$ | Verified against SWAT+ 62.0.0 (climate_control.f90:268). tmax = tmax + tmpinc(mo)` — climate-change temp adj |
| 1:4.2.3 |  | $T_{mn}=T_{mn}+adj_{tmp}$ | Verified against SWAT+ 62.0.0 (climate_control.f90:269). tmin = tmin + tmpinc(mo) |
| 1:4.2.4 |  | $\overline T_{av} =\overline T_{av} +adj_{tmp}$ | Verified against SWAT+ 62.0.0 (climate_control.f90:87). tave = (tmax+tmin)/2.` (recomputed post-adjust) |
| 1:4.2.5 |  | $H_{day}= H_{day}+ adj_{rad}$ | Verified against SWAT+ 62.0.0 (climate_control.f90:270). solrad = solrad + radinc |
| 1:4.2.6 |  | $R_h=R_h +adj_{hmd}$ | Verified against SWAT+ 62.0.0 (climate_control.f90:272). rhum = rhum + huminc(mo)`, clamped 0.01–0.99 (:273-274) |

## Lineage

`climate_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 11 non-merge commit(s) since, most recently `e0f6e77` (2026-04-03, "updated !! comments"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `climate_control.f90` are listed.

- `e0f6e77` (2026-04-03) — updated !! comments
- `90892a7` (2026-04-01) — Fix divide-by-zero bug
- `cfa8824` (2026-04-01) — Update climate_control.f90
- `18b3209` (2026-04-01) — Update climate_control.f90
- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'climate_control' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
