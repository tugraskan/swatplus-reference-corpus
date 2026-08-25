---
kind: procedure
symbol: cli_wndgen
title: cli_wndgen
status: filled
source_hash: ed78c1c9f364cd70
version_label: SWAT+ 62.0.0
args:
  iwgn: '`iwgn` selects which weather-generator record to use for the current station. It
    controls the monthly mean wind-speed lookup in `wgn(iwgn)%windav(time%mo)` and also indexes
    the random-seed stream passed to `aunif`.'
locals:
  v6: Holds the first uniform random variate drawn for wind-speed generation. The routine
    uses it inside `-Log(v6)` to convert a uniform seed draw into a skewed daily wind-speed
    multiplier.
  v7: Holds the second uniform random variate, intended for wind-direction selection if that
    branch were enabled. It is compared against cumulative direction probabilities in `wnd_dir(iwndir)%dir(mo,idir)`.
  rdir2: Stores the prior direction-bin index as a real value so the final direction angle
    can be reconstructed from the selected bin and interpolation factor.
  pi2: Holds `2*pi` as a conversion factor from a normalized direction index to radians.
  idir: Loop counter over the 16 wind-direction classes when searching for the first cumulative
    probability that exceeds `v7`.
  idir1: Tracks the upper direction-bin index that brackets the random draw `v7`; it starts
    at 16 and is reset to the first bin whose cumulative probability exceeds `v7`.
  idir2: Tracks the lower bracketing direction-bin index used together with `idir1` to interpolate
    the final wind direction.
  mo: Copies the current simulation month from `time%mo` so the routine can index month-dependent
    wind-direction probabilities.
  iwndir: Selects the wind-direction table to use. In this version it is forced to zero, which
    disables the direction-generation branch.
  aunif: Declared as the uniform-random function interface used to produce the stochastic
    draws consumed by this routine.
  g: Stores the interpolation fraction within the selected wind-direction bin before converting
    it to an angle. It is only used if the disabled direction branch runs.
uses:
  hydrograph_module: '`hydrograph_module` provides `iwst`, the current weather-station index.
    That index tells the routine which `wst` entry to update for the active hydrograph/station
    context.'
  climate_module: '`climate_module` supplies the station, generator, and wind-direction data
    structures that this routine reads from and writes to. `wgn` provides the monthly mean
    wind speed, `wnd_dir` provides cumulative direction probabilities, and `wst` holds the
    weather values being updated.'
  time_module: '`time_module` provides the current simulation month through `time%mo`. That
    month chooses the correct monthly wind-speed average and, if enabled, the matching wind-direction
    distribution.'
---

<!-- facts:header -->

Generates a daily wind speed for the current weather station from the monthly generator value and a random variate. It also contains a disabled wind-direction routine that can map a random draw into a direction class.

## Bottom Line

`cli_wndgen` fills the current station weather state with a simulated wind speed for the active month. It draws a uniform random number, transforms the generator month-average wind speed with a `(-log(r))^0.3` shape, and stores the result in `wst(iwst)%weat%windsp`.

The subroutine also includes wind-direction code, but that branch is disabled by setting `iwndir = 0` before the test. As written, the direction state is not updated during normal execution, so only wind speed affects later climate handling.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `climate_control` during the daily weather update for each weather station, after that driver has selected the station's generator index (`iwgn = wst(iwst)%wco%wgn`). Its results feed the station weather state that later climate calculations and downstream model routines use for the current day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize month and constant | Set `pi2` to `2*pi` and copy the current simulation month from `time%mo` into `mo` for later month-based lookups. |
| 2. draw wind-speed random number | Call `Aunif` with the wind-speed random-seed stream to get `v6`, then compute daily wind speed as the month-average wind speed from `wgn(iwgn)%windav(time%mo)` multiplied by `(-Log(v6))**0.3` and store it in `wst(iwst)%weat%windsp`. |
| 3. disable direction generation | Set `iwndir` to zero and test `if (iwndir > 0) then`; because `iwndir` is forced to zero, the wind-direction block is skipped in normal execution. |
| 4. bracket random direction | If the direction block were active, initialize the bracketing direction indices, draw `v7`, and scan the 16 direction classes until the cumulative probability in `wnd_dir(iwndir)%dir(mo,idir)` exceeds `v7`, then stop at that class. |
| 5. interpolate within bin | If the first bin is selected, compute `g` directly from `v7`; otherwise interpolate between the lower and upper cumulative probabilities to get the within-bin fraction `g`. |
| 6. convert bin to radians | Convert the selected bin and interpolation fraction into a radian wind direction, store it in `wst(iwst)%weat%wndir`, and add `pi2` to shift the angle into the model's expected range. |
| 7. return | Exit the subroutine after updating the weather state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `iwst` |  |
| [sym:climate_module] | `wst, wgn, wnd_dir` | `wst(iwst)%weat%windsp, wgn(iwgn)%windav, wnd_dir(iwndir)%dir(mo,idir), wnd_dir(iwndir)%dir(mo,idir1), wnd_dir(iwndir)%dir(mo,idir2), wst(iwst)%weat%wndir` |
| [sym:time_module] | `time` | `time%mo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%weat%windsp` | Always when the subroutine runs; the value is assigned before the disabled direction branch. | `wst(iwst)%weat%windsp` is replaced with a stochastic daily wind speed derived from the current month's generator mean and a uniform random draw. |
| `wst(iwst)%weat%wndir` | Only if `iwndir > 0`; in this source it never changes because `iwndir` is set to zero before the test. | `wst(iwst)%weat%wndir` would hold the generated wind direction angle for the current day, but the present code leaves it unchanged because the direction branch is disabled. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:3.6.1 | Daily wind-speed generation (modified exponential) | $\mu _{10m}=\mu wnd_{mon}*(-ln(rnd_1))^{0.3}$ | windsp = windav(mo)*(-Log(v6))**0.3 implements mu_10m = mu_wnd_mon*(-ln(rnd))^0.3 from GitBook 1:3.6. The 1:1.4 wind-profile equations are handled in et_pot, not here. |

## Lineage

The procedure was introduced in `df07e3f` as a new source file that generated wind speed and included a direction-generation branch. `bd18ad4` added an explicit external declaration for `aunif` without changing the algorithm. `39fabde` initialized the local scalars and counters to zero, but left the computation intact.

- df07e3f: created `cli_wndgen` with monthly wind-speed generation from `wgn(iwgn)%windav(time%mo)` and the optional wind-direction lookup/interpolation logic.
- bd18ad4: added `external :: aunif`, making the random-number function declaration explicit while preserving behavior.
- 39fabde: initialized local working variables (`v6`, `v7`, `rdir2`, `pi2`, `idir`, `idir1`, `idir2`, `mo`, `iwndir`, `g`) to zero to avoid undefined values before use.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_wndgen' has no extracted documentation comment.
