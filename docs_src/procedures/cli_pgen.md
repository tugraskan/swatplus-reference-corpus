---
kind: procedure
symbol: cli_pgen
title: cli_pgen
status: filled
source_hash: 1f09fdc6978edb24
version_label: SWAT+ 62.0.0
args:
  iwgn: Selects the weather-generator record and corresponding station context used to draw
    precipitation probabilities and monthly rainfall parameters.
locals:
  vv: First uniform random variate used to decide whether the current day is wet or dry.
  pcpgen: Holds the generated daily precipitation depth before it is stored for the next day.
  v8: Second uniform random variate used as the angular random input to the Box-Muller normal
    deviate calculation.
  r6: Convenience factor derived from the monthly skew coefficient; used to shape the skewed
    rainfall distribution.
  xlv: Intermediate rainfall-depth calculation that is transformed from a standard normal
    deviate into daily precipitation.
  aunif: Local declaration for the random-number function that returns a uniform 0 to 1 variate.
  xx: Threshold probability for a wet day, taken from the monthly wet-day probability for
    the prior-day condition.
  cli_dstn1: Function that converts two uniform random numbers into a standard normal deviate
    used in the rainfall amount calculation.
uses:
  basin_module: These climate-module states hold the monthly wet-day probabilities, rainfall-shape
    parameters, monthly mean and correction factor, and the stored random-number stream that
    together determine whether precipitation occurs and how much falls. `precip_next` is the
    output state this routine populates for the rest of the weather workflow.
  climate_module: The hydrograph module provides the current weather-station index `iwst`,
    which is the lookup key that ties this precipitation generator call to the active station
    being processed.
  hydrograph_module: The time module provides the current simulation month `time%mo`, which
    selects the monthly precipitation probabilities and rainfall parameters used in both the
    wet/dry test and the precipitation amount calculation.
  time_module: The current simulation month determines which of the 12 monthly probability
    and precipitation-parameter slots to use. `time%mo` makes the routine choose the correct
    wet-day probabilities, skew coefficient, daily precipitation standard deviation, monthly
    mean precipitation, and correction factor for the active month.
---

<!-- facts:header -->

Generates daily precipitation for a weather station from the SWAT+ weather generator. It decides whether the day is wet or dry, then computes and stores the next-day precipitation amount for use by the precipitation control flow.

## Bottom Line

cli_pgen generates one day of weather-generator precipitation for the selected weather generator station. It uses the station’s prior-day wet/dry state, the current month, and two uniform random draws to decide whether the day is wet; if it is wet, it computes a skewed-normal precipitation amount from the generator parameters and applies the monthly precipitation correction factor.

The routine does not read or write files. Its main effect is to update `wst(iwst)%weat%precip_next`, which the precipitation-control workflow later promotes into the active day and may use to build subdaily rainfall when the day length requires it.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the precipitation-control sequence after `cli_precip_control` has selected the active weather generator index from the station record and reset the station’s next-day precipitation storage. Its result feeds the later daily weather update, and if the simulation is using generated subdaily precipitation, the calling control flow also uses the generated day-total to build hourly rainfall distribution.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize precipitation output | Set the generated daily precipitation accumulator to zero before any wet/dry decision is made. |
| 2. draw wet/dry random number | Draw a uniform random variate from the SWAT+ random seed stream for this weather generator and store it in `vv`. |
| 3. choose prior-day transition probability | Use the station’s prior-day wet/dry flag to select the current month’s wet-day probability after a dry day or after a wet day. |
| 4. test for a wet day | Compare the random draw to the selected wet-day probability; if the draw exceeds the threshold, leave precipitation at zero for a dry day. |
| 5. draw second random value | If the day is wet, draw another uniform variate to supply the normal-deviate transformation. |
| 6. compute skew factor | Form the monthly skew scaling factor from the generator’s precipitation skew coefficient. |
| 7. convert to standard normal | Call `cli_Dstn1` with the stored random deviate and the new uniform draw to obtain a standard normal value for rainfall generation. |
| 8. shape rainfall amount | Transform the standard normal value with the skew factor into a skewed rainfall depth component and scale it back by the monthly skew coefficient. |
| 9. update random stream state | Store the second uniform draw back into `rnd3(iwgn)` so the next call continues the random sequence. |
| 10. apply monthly mean and correction | Convert the shaped value into millimeters using the monthly standard deviation and mean precipitation, then multiply by the monthly precipitation correction factor. |
| 11. enforce minimum precipitation | Floor any generated wet-day precipitation below 0.1 mm up to 0.1 mm to avoid zero or tiny wet-day amounts. |
| 12. store next-day precipitation | Copy the generated total into the station’s `precip_next` field so the caller can promote it to the current day later. |
| 13. return | Exit after the station state has been updated with the generated next-day precipitation. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `wst, wgn, wgn_pms, rnd3` | `wst(iwst)%weat%precip_prior_day, wgn(iwgn)%pr_wd, wgn(iwgn)%pr_ww, wgn(iwgn)%pcpskw, wgn(iwgn)%pcpstd, wgn_pms(iwgn)%pcpmean, wgn_pms(iwgn)%pcf, wst(iwst)%weat%precip_next, rnd3(iwgn)` |
| [sym:climate_module] | `wst, wgn, wgn_pms, rnd3` | `wst(iwst)%weat%precip_prior_day, wgn(iwgn)%pr_wd, wgn(iwgn)%pr_ww, wgn(iwgn)%pcpskw, wgn(iwgn)%pcpstd, wgn_pms(iwgn)%pcpmean, wgn_pms(iwgn)%pcf, wst(iwst)%weat%precip_next` |
| [sym:hydrograph_module] | `iwst` |  |
| [sym:time_module] | `time` | `time%mo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rnd3(iwgn)` | When the day is wet and the routine reaches the normal-deviate branch, `rnd3(iwgn)` is updated from the second uniform draw. | The stored random-number stream advances so the next precipitation generation call uses the fresh uniform variate instead of reusing the old one. |
| `wst(iwst)%weat%precip_next` | At the end of the routine, after dry-day or wet-day processing completes, `wst(iwst)%weat%precip_next` is assigned the generated precipitation total. | The next-day precipitation slot for the active weather station is filled so `cli_precip_control` can move it into the current-day precipitation state and, if needed, generate subdaily rainfall. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:3.1.1 | P(dry\|wet) complement | $P_i(D/W)=1-P_i(W/W)$ | Stores P(wet\|dry)=pr_wd and P(wet\|wet)=pr_ww; P(dry\|wet)=1-P(wet\|wet) is the implied complement in the wet/dry branch. |
| 1:3.1.2 | P(wet\|wet) | $P_i(W/W)=1-P_i(W/D)$ | xx = pr_ww when prior day wet (line 51); vv>xx test applies the Markov transition. |
| 1:3.1.3 | Rainfall amount (skewed-normal) | $R_{day}=\mu_{mon}+2*\sigma_{mon}*(\frac{[(SND_{day}-\frac{g_{mon}}{{6}})*\frac{g_{mon}}{{6}}+1]^3-1}{g_{mon}})$ | Skewed-normal rainfall is formed at lines 58-62, then multiplied by pcf at line 63 and floored at 0.1 at line 64. |
| 1:3.1.4 | Standard normal deviate SND_day | $SND_{day}=cos(6.283*rnd_2)*\sqrt{-2ln(rnd_1)}$ | Verified against SWAT+ 62.0.0 (cli_pgen.f90). |
| 1:3.1.5 |  | $R_{day}=\mu_{mon}*(-ln(rnd_1))^{rexp}$ | Verified against SWAT+ 62.0.0 (cli_pgen.f90:62). code uses skewed-normal precip gen `xlv*pcpstd+pcpmean`, not the exponential `μ·(−ln rnd)^rexp` form |

## Lineage

`cli_pgen.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cli_pgen.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_pgen' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
