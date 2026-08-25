---
kind: procedure
symbol: cli_slrgen
title: cli_slrgen
status: filled
source_hash: 07b4637943db070d
version_label: SWAT+ 62.0.0
args:
  iwgn: Selects which weather generator record to use for the current station; iwgn indexes
    wgn, wgn_pms, and wgncur entries that supply the monthly solar average, wet-day proportion,
    and radiation variability term.
locals:
  rx: Intermediate spread term for solar radiation. It stores the difference between the station's
    daily maximum solar radiation and the adjusted monthly mean so the routine can scale the
    daily perturbation by wgncur(3,iwgn)/4.
  rav: Adjusted monthly-average radiation baseline for the current month. It is computed from
    the generator monthly mean and wet-day proportion, then halved on wet days before the
    daily variability term is added.
uses:
  hydrograph_module: hydrograph_module provides iwst, the current weather-station index. cli_slrgen
    uses iwst to read and write the active station's daily weather state in wst(iwst)%weat.
  climate_module: climate_module holds the weather-generator databases and station weather
    state that determine and receive the radiation calculation. cli_slrgen reads the generator
    monthly mean and wet-day fraction, uses the generator perturbation term, and stores the
    computed daily solar radiation back into the active station record.
---

<!-- facts:header -->

Generates daily solar radiation for the current weather station and weather generator pair. It adjusts a monthly mean using wet-day/dry-day weighting and a weather-generator radiation perturbation, then applies a floor if the result is nonpositive.

## Bottom Line

cli_slrgen computes the station-day solar radiation value used by the climate simulation. It starts from the monthly generator mean for the selected weather generator, adjusts that mean based on whether the day is wet, and combines it with the generator's radiation variability term and the station's daily maximum radiation.

The routine matters because climate_control calls it during daily solar-radiation setup for each weather station when the station is configured to simulate radiation. Its result is written into wst(iwst)%weat%solrad for later weather and hydrologic calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the daily climate workflow after climate_control has selected the active weather generator for each weather station and after cli_clgen has prepared the other daily climate variables. If the station's solar-radiation source is simulated, cli_slrgen supplies wst(iwst)%weat%solrad for later model processes that depend on daily radiation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. compute adjusted monthly baseline | Use the current month to compute a baseline solar-radiation mean from wgn(iwgn)%solarav and divide by 1 - 0.5*wgn_pms(iwgn)%pr_wdays, which converts the monthly mean into the dry-day equivalent for the generator. |
| 2. damp wet-day baseline | If the active day has precipitation, reduce the adjusted monthly baseline by half so the routine uses the wet-day radiation mean rather than the dry-day mean. |
| 3. form spread to maximum | Compute the gap between the station's daily maximum solar radiation and the adjusted baseline; this gap becomes the amplitude used for the random radiation perturbation. |
| 4. generate daily solar radiation | Add the weather-generator radiation factor wgncur(3,iwgn) scaled by rx/4 to the adjusted baseline and store the resulting daily solar radiation in wst(iwst)%weat%solrad. |
| 5. enforce nonnegative floor | If the computed solar radiation is zero or negative, replace it with 5 percent of the station's daily maximum solar radiation to keep the climate state physically plausible. |
| 6. overwrite with monthly mean | Overwrite the computed daily solar radiation with the monthly average solar radiation from wgn(iwgn)%solarav(time%mo), so the final stored value is the generator monthly mean. |
| 7. return | Exit the routine after updating the active station's solar-radiation state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `iwst` |  |
| [sym:climate_module] | `wgn, wgn_pms, wst, wgncur` | `wgn(iwgn)%solarav, wgn_pms(iwgn)%pr_wdays, wst(iwst)%weat%precip, wst(iwst)%weat%solradmx, wst(iwst)%weat%solrad` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%weat%solrad` | After the routine computes a value for wst(iwst)%weat%solrad, it always assigns wgn(iwgn)%solarav(time%mo) to that field before returning. | The station's daily solar-radiation state is replaced by the generator's monthly average for the current month. The earlier wet-day/dry-day and perturbation calculation still informs the documented algorithm, but the final stored value is the monthly mean. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:3.4.12 | Generated solar radiation | $H_{day}=\mu rad_{mon} + \chi_i(3)*\sigma rad_{mon}$ | Verified against SWAT+ 62.0.0 (cli_slrgen.f90:33). solrad = rav + wgncur(3)*rx/4. |
| 1:3.4.13 | Radiation standard deviation | $\sigma rad_{mon}=\frac{H_{mx}-\mu rad_{mon}}{4}$ | Verified against SWAT+ 62.0.0 (cli_slrgen.f90:33). rx/4.` with rx = solradmx − rav → σrad=(H_mx−μrad)/4 |
| 1:3.4.19 | Monthly mean weighting (wet/dry) | $\mu rad_{mon}*days_{tot}=\mu Wrad_{mon}*days_{wet}+\mu Drad_{mon}*days_{dry}$ | Verified against SWAT+ 62.0.0 (cli_slrgen.f90:30). wet/dry radiation weighting implied by the rav normalization |
| 1:3.4.20 | Wet-day mean radiation | $\mu Wrad_{mon}=b_R*\mu Drad_{mon}$ | Verified against SWAT+ 62.0.0 (cli_slrgen.f90:31). if (precip>0) rav = 0.5*rav` → b_R hardcoded 0.5 |
| 1:3.4.21 | Dry-day mean radiation | $\mu Drad_{mon}=\frac{\mu rad_{mon}*days_{tot}}{b_R*days_{wet}+days_{dry}}$ | Verified against SWAT+ 62.0.0 (cli_slrgen.f90:30). rav = solarav/(1.-0.5*pr_wdays)` — dry-day mean radiation |
| 1:3.4.22 | Radiation on wet days | $H_{day}=\mu Wrad_{mon}+\chi_i(3)*\sigma rad_{mon}$ | Verified against SWAT+ 62.0.0 (cli_slrgen.f90:31). wet-day H_day (same generator, halved rav) |
| 1:3.4.23 | Radiation on dry days | $H_{day}=\mu Drad_{mon}+\chi_i(3)*\sigma rad_{mon}$ | Verified against SWAT+ 62.0.0 (cli_slrgen.f90:33). dry-day H_day; SAME dead-code overwrite at :36 (see chunk T) |

## Lineage

Resolved lineage shows the routine was added in df07e3f with the current solar-radiation logic. c7c8e22 carried the same code into the imported source version, 39fabde only initialized rx and rav to zero without changing the algorithm, and 2ee1889 made a blank-line cleanup after the final assignment; no resolved commit changed the computed behavior beyond the routine's original implementation.

- df07e3f introduced cli_slrgen with the wet-day adjustment, radiation perturbation, floor check, and final monthly-mean assignment.
- 39fabde initialized rx and rav to 0. but did not alter the calculation sequence.
- 2ee1889 only added whitespace after the final assignment and did not change behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_slrgen' has no extracted documentation comment.
