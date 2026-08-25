---
kind: procedure
symbol: cli_tgen
title: cli_tgen
status: filled
source_hash: 51939d7de487a25a
version_label: SWAT+ 62.0.0
args:
  iwgn: '`iwgn` selects which weather generator record to use. It indexes the monthly temperature
    means, standard deviations, and wet-day proportions in `wgn(iwgn)` and `wgn_pms(iwgn)`
    for the current month, so the generated temperatures are station-specific.'
locals:
  tmxg: Daily generated maximum temperature after the monthly wet/dry adjustment and the max-temperature
    random perturbation are applied. This becomes the final `wst(iwst)%weat%tmax` value.
  tmng: Daily generated minimum temperature after applying the monthly minimum-temperature
    mean and its random perturbation. It is compared against `tmxg` and lowered if needed
    to keep minimum temperature below maximum temperature.
  tamp: Half the monthly spread between mean maximum and mean minimum temperature. It is the
    wet/dry adjustment amount used to shift the max-temperature mean before daily generation.
  txxm: The adjusted monthly mean maximum temperature used as the base for generating daily
    maximum temperature. It starts from the monthly mean and is shifted by wet-day proportion,
    then reduced on rainy days.
uses:
  climate_module: '`climate_module` holds the weather-generator database and the current weather
    state that this routine reads and writes. `wgn`, `wgn_pms`, `wgncur`, and `wst` provide
    the monthly temperature means, wet-day proportion, random temperature deviates, and destination
    daily station temperatures that control the generated result.'
  hydrograph_module: '`hydrograph_module` provides `iwst`, the active weather-station index
    used to pick which `wst` entry receives the generated temperatures. Without that station
    index, the routine would not know which station’s weather record to update.'
  time_module: '`time_module` supplies `time%mo`, the current simulation month. That month
    index determines which monthly temperature statistics are used from the weather generator
    and which wet-day proportion applies.'
---

<!-- facts:header -->

Generates daily maximum and minimum air temperature for a weather station from monthly weather-generator statistics. It adjusts the daily temperatures for wet-day conditions and stores the results in the current station weather state.

## Bottom Line

`cli_tgen` turns the current month’s weather-generator parameters into one day of generated temperature for the active weather station. It computes a wet/dry adjusted maximum-temperature mean, adds random monthly variability for max and min temperature, and then writes the final daily `tmax` and `tmin` values into `wst(iwst)%weat`.

The routine matters because it supplies the station-level temperature values used by the rest of the climate sequence whenever temperature is being simulated rather than read from file. It uses the current month, the selected weather generator, the current station’s precipitation state, and the weather-generator random deviates to shape the day’s temperatures.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the climate-control temperature step, after `climate_control` has selected the active weather generator for each weather station and after `cli_weatgn` has prepared the generator random values. If `wst(iwst)%wco_c%tgage` is set to simulate temperatures, `cli_tgen` produces the day’s `tmax` and `tmin`; later model behavior uses those station weather values wherever daily climate inputs are needed.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. compute wet/dry adjustment | Computes `tamp` as half the difference between monthly mean max and min temperature, then builds `txxm` by shifting the monthly max mean by the wet-day proportion so the daily max base reflects the month’s wet/dry mix. |
| 2. lower max mean on wet days | If the current station’s precipitation is greater than zero, the routine subtracts `tamp` from `txxm`, applying the wet-day maximum-temperature reduction used for rainy days. |
| 3. generate daily maximum temperature | Adds the monthly max-temperature standard deviation times `wgncur(1,iwgn)` to `txxm` to produce `tmxg`, the generated daily maximum temperature. |
| 4. generate daily minimum temperature | Adds the monthly min-temperature standard deviation times `wgncur(2,iwgn)` to the monthly minimum mean to produce `tmng`, the generated daily minimum temperature. |
| 5. enforce temperature ordering | If the generated minimum temperature exceeds the generated maximum temperature, resets `tmng` to `tmxg - .2 * Abs(tmxg)` so minimum temperature stays below maximum temperature. |
| 6. store generated temperatures | Writes the generated daily temperatures into the current station weather record as `wst(iwst)%weat%tmax = tmxg` and `wst(iwst)%weat%tmin = tmng`. |
| 7. return | Ends the subroutine after the station weather state has been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `wgn, wgn_pms, wst, wgncur` | `wgn(iwgn)%tmpmx, wgn(iwgn)%tmpmn, wgn_pms(iwgn)%pr_wdays, wst(iwst)%weat%precip, wgn(iwgn)%tmpstdmx, wgn(iwgn)%tmpstdmn, wst(iwst)%weat%tmax, wst(iwst)%weat%tmin` |
| [sym:hydrograph_module] | `iwst` |  |
| [sym:time_module] | `time` | `time%mo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%weat%tmax` | After `tmxg` and `tmng` are computed, `wst(iwst)%weat%tmax` is always assigned `tmxg`. | `wst(iwst)%weat%tmax` is updated to the generated daily maximum temperature for the active station, including the monthly wet/dry adjustment and the random weather-generator perturbation. |
| `wst(iwst)%weat%tmin` | After `tmng` is computed, and after the optional correction when `tmng > tmxg`. | `wst(iwst)%weat%tmin` is updated to the generated daily minimum temperature for the active station; if the raw minimum would exceed the maximum, it is reduced to stay below `tmax`. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:3.4.10 | Generated maximum temperature | $T_{mx}=\mu mx_{mon} + \chi_i(1)*\sigma mx_{mon}$ | Verified against SWAT+ 62.0.0 (cli_tgen.f90:47). tmxg = txxm + tmpstdmx*wgncur(1) |
| 1:3.4.11 | Generated minimum temperature | $T_{mn}=\mu mn_{mon} + \chi_i(2)*\sigma mn_{mon}$ | Verified against SWAT+ 62.0.0 (cli_tgen.f90:48). tmng = tmpmn + tmpstdmn*wgncur(2) |
| 1:3.4.14 | Monthly mean weighting (wet/dry) | $\mu mx_{mon}*days_{tot}=\mu Wmx_{mon}*days_{wet}+\mu Dmx_{mon}*days_{dry}$ | Dry/wet conditional means are built so their wet/dry-weighted average returns the monthly mean. |
| 1:3.4.15 | Wet-day conditional max mean | $\mu Wmx_{mon}=\mu Dmx_{mon}-b_T*(\mu mx_{mon}-\mu mn_{mon})$ | On wet days txxm = (dry-day mean) - tamp, the downward shift. |
| 1:3.4.16 | Dry-day conditional max mean | $\mu Dmx_{mon}=\mu mx_{mon}+b_T*\frac{days_{wet}}{days_{tot}}*(\mu mx_{mon}-\mu mn_{mon})$ | Verified against SWAT+ 62.0.0 (cli_tgen.f90:43). txxm = tmpmx + tamp*pr_wdays`, tamp=.5*(tmpmx-tmpmn) → theory's b_T is hardcoded 0.5 |
| 1:3.4.17 | Max temperature on wet days | $T_{mx}=\mu Wmx_{mon}+\chi_i(1)*\sigma mx_{mon}$ | Verified against SWAT+ 62.0.0 (cli_tgen.f90:45). wet-day: `if (precip>0) txxm = txxm - tamp |
| 1:3.4.18 | Max temperature on dry days | $T_{mx}=\mu Dmx_{mon}+\chi_i(1)*\sigma mx_{mon}$ | Verified against SWAT+ 62.0.0 (cli_tgen.f90:47). dry-day T_mx (txxm carries the dry adjustment) |

## Lineage

Two source-backed commits were resolved for `cli_tgen`. In `df07e3f`, the file was introduced with the temperature-generation logic and documentation block. In `39fabde`, the procedure body was unchanged but local real variables `tmxg`, `tmng`, `tamp`, and `txxm` were initialized to `0.` in the declarations.

- df07e3f introduced `cli_tgen.f90` with the wet/dry-adjusted daily temperature generation logic, including the max/min calculation and the min-below-max safeguard.
- 39fabde changed only initialization of the local real variables (`tmxg`, `tmng`, `tamp`, `txxm`) to `0.`; the computed temperature algorithm itself did not change.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_tgen' has no extracted documentation comment.
