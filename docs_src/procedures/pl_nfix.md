---
kind: procedure
symbol: pl_nfix
title: pl_nfix
status: filled
source_hash: b89835e3bbbcf53f
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; it selects the active HRU-specific soil, plant, and nutrient
    state used in the fixation calculation.
  l: Soil-layer loop counter used to sum nitrate across all layers in the active soil profile.
  idp: Plant database index taken from the current plant community's `idplt`; it selects the
    plant parameter record that provides `nfix_co`.
  uno3l: The unmet plant nitrogen demand used as the base amount for fixation; it is computed
    as `uno3d(ipl) - nplnt(j)` when demand exceeds uptake.
  fxw: Soil-water reduction factor for fixation, computed from current soil water relative
    to field capacity (`soil(j)%sw / (.85 * soil(j)%sumfc)`).
  sumn: Total nitrate in the soil profile, accumulated by summing `soil1(j)%mn(l)%no3` across
    all layers.
  fxn: Nitrate availability factor; it is reduced to 0, interpolated between 100 and 300 kg
    N/ha, or set to 1 when profile nitrate is low.
  fxg: Growth-stage factor derived from `pcom(j)%plcur(ipl)%phuacc`; it is 0 before fixation
    starts, rises through mid-season, peaks, and declines late in the season.
  fxr: Intermediate raw fixation scaling factor formed from `Min(1., fxw, fxn) * fxg` and
    then floored at 0 before converting unmet demand into `fixn`.
uses:
  basin_module: '`bsn_prm%nfixmx` provides the basin-wide upper bound on daily nitrogen fixation,
    so this routine must read it to cap `fixn` after all plant- and soil-based scaling is
    applied.'
  organic_mineral_mass_module: '`soil1` holds the layer-by-layer mineral nitrogen pools. `pl_nfix`
    sums `soil1(j)%mn(l)%no3` to determine total profile nitrate and build the nitrate-limitation
    factor `fxn`.'
  hru_module: '`ihru` selects the current HRU, `ipl` selects the active plant slot, `uno3d(ipl)`
    provides daily plant nitrogen demand, `nplnt(j)` provides current plant N uptake, and
    `fixn` is the output state written by this routine for later use.'
  soil_module: '`soil(j)%sw` and `soil(j)%sumfc` define the soil-water condition used to compute
    `fxw`, while `soil(j)%nly` determines how many layers must be scanned when totaling nitrate
    for fixation control.'
  plant_module: '`pcom` supplies the active plant identity and growth progression. `idplt`
    selects the plant parameter record, and `phuacc` drives the growth-stage factor `fxg`.'
  plant_data_module: '`pldb(idp)%nfix_co` controls how strongly the computed fixation replaces
    unmet demand versus leaving the result closer to the original nitrogen deficit.'
---

<!-- facts:header -->

Estimates daily plant nitrogen fixation for legumes based on crop demand, soil nitrate, soil water, and growth stage. It writes the result to `fixn` for the current HRU/plant and caps it by plant and basin limits.

## Bottom Line

`pl_nfix` calculates how much nitrogen a legume can fix on the current day when plant demand exceeds available soil nitrate. It first checks whether the plant is N-limited, then builds reduction factors from soil water, summed profile nitrate, and accumulated heat units before combining them into a fixation amount.

The routine stores the final daily fixation in `fixn`, blending the computed fixation with the plant-specific coefficient `nfix_co` and limiting it by both the unmet demand and the basin maximum `bsn_prm%nfixmx`. `pl_nup` calls this routine after soil uptake so the added fixed N can be included in plant N balance updates.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during plant nitrogen uptake processing after `pl_nup` has already computed the day's N uptake and determined that the crop is a legume (`pldb(idp)%nfix_co > 1.e-6`). Its result, `fixn`, is then added back into `nplnt(j)` by the caller and propagated into plant biomass and nutrient balance accounting, so downstream plant mass and HRU nitrogen bookkeeping depends on it.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and plant record. | Copies `ihru` into `j` and reads the current plant species index from `pcom(j)%plcur(ipl)%idplt` so the routine can use the correct HRU, soil, and plant parameter state. |
| 2. Stop if plant demand is already met. | If `uno3d(ipl)` is not greater than `nplnt(j)`, there is no unmet nitrogen demand to fix, so the routine sets `fixn = 0.` and returns immediately. |
| 3. Compute soil-water limitation. | Calculates `fxw` as current soil water divided by 85% of field capacity, giving a moisture stress factor for fixation. |
| 4. Sum nitrate across the soil profile. | Initializes `sumn` and `fxn`, then loops over all soil layers to accumulate `soil1(j)%mn(l)%no3` into a whole-profile nitrate total. |
| 5. Convert nitrate total to a fixation factor. | Sets `fxn` to 0 when profile nitrate exceeds 300, linearly decreases it between 100 and 300, and leaves it at 1 when nitrate is 100 or less. |
| 6. Build the growth-stage factor. | Initializes `fxg` to 0, then raises it during the middle of the season based on `pcom(j)%plcur(ipl)%phuacc`, with a rise, plateau, and decline across the documented PHU ranges. |
| 7. Combine limiting factors into a raw fixation scaler. | Computes `fxr = Min(1., fxw, fxn) * fxg` and clips it at zero so negative values cannot reduce fixation below none. |
| 8. Convert unmet demand to daily fixation. | Starts from `Min(6., fxr * uno3l)`, blends that with the plant coefficient `pldb(idp)%nfix_co`, then caps the result by the unmet demand `uno3l` and the basin maximum `bsn_prm%nfixmx`. |
| 9. Return to the caller. | Exits after writing the final daily fixation to `fixn` for use by `pl_nup`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%nfixmx` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(l)%no3` |
| [sym:hru_module] | `uno3d, nplnt, ihru, fixn, ipl` |  |
| [sym:soil_module] | `soil` | `soil(j)%sw, soil(j)%sumfc, soil(j)%nly` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%phuacc` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%nfix_co` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `fixn` | When `uno3d(ipl) > nplnt(j)` and the plant is a fixer, after soil and growth factors are applied. | `fixn` is set to the day’s computed nitrogen fixation amount for the active HRU/plant. It remains 0 when plant demand is already satisfied, and otherwise reflects the capped legume fixation contribution that `pl_nup` adds back into plant nitrogen totals. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.3.9 | Nitrogen fixation | $N_{fix}=N_{demand}*f_{gr}*min(f_{sw},f_{no3},1)$ | Verified against SWAT+ 62.0.0 (pl_nfix.f90:81). N_fix = demand*fxg*Min(fxw,fxn,1.) |
| 5:2.3.10 | Zero fixation before 15% PHU | $f_{gr}=0$ | Verified against SWAT+ 62.0.0 (pl_nfix.f90:73). fr_PHU≤0.15 growth-stage branch (fxg=0 below :73) |
| 5:2.3.11 | Rising growth-stage fixation factor | $f_{gr}=6.67*fr_{PHU}-1$ | For 0.15 < phuacc <= 0.30, fxg = 6.67*phuacc - 1. |
| 5:2.3.12 | Full fixation growth-stage factor | $f_{gr}=1$ | For 0.30 < phuacc <= 0.55, fxg = 1. |
| 5:2.3.13 | Declining growth-stage fixation factor | $f_{gr}=3.75 -5*fr_{PHU}$ | For 0.55 < phuacc <= 0.75, fxg = 3.75 - 5*phuacc. |
| 5:2.3.14 | Zero fixation after 75% PHU | $f_{gr}=0$ | Verified against SWAT+ 62.0.0 (pl_nfix.f90:77). fr_PHU>0.75 growth-stage upper bound (fxg=0 above :78) |
| 5:2.3.15 | Nitrate factor below 100 kg N/ha | $f_{no3}=1$ | Verified against SWAT+ 62.0.0 (pl_nfix.f90:69). if (sumn <= 100.) fxn = 1. |
| 5:2.3.16 | Nitrate factor between 100 and 300 kg N/ha | $f_{no3}=1.5-0.0005*NO3$ | Verified against SWAT+ 62.0.0 (pl_nfix.f90:68). if (sumn>100 .and. sumn<=300) fxn = 1.5-.005*sumn |
| 5:2.3.17 | Nitrate factor above 300 kg N/ha | $f_{no3}=0$ | Verified against SWAT+ 62.0.0 (pl_nfix.f90:67). if (sumn>300.) fxn = 0. |
| 5:2.3.18 | Soil-water factor for fixation | $f_{SW}=\frac{SW}{.85*FC}$ | Verified against SWAT+ 62.0.0 (pl_nfix.f90:59). fxw = sw/(.85*sumfc)` — soil-water fixation factor |

## Lineage

Three source-backed commits were resolved for `pl_nfix`. The initial addition in `df07e3f` introduced the subroutine, its documentation header, module uses, the demand check, soil nitrate and growth-stage factors, and the final fixation cap logic. Commit `94b6dec` brought in the same routine from Bitbucket without changing the algorithm shown in the resolved diff. Commit `39fabde` only initialized local variables (`j`, `l`, `idp`, `uno3l`, `fxw`, `sumn`, `fxn`, `fxg`, `fxr`) to zero and left the fixation logic unchanged.

- df07e3f added the full `pl_nfix` routine for legume nitrogen fixation, including the unmet-demand check, soil nitrate and water stress factors, growth-stage factor, and final capping by plant and basin limits.
- 39fabde changed only local variable initialization in `pl_nfix`, setting `j`, `l`, `idp`, `uno3l`, `fxw`, `sumn`, `fxn`, `fxg`, and `fxr` to zero before use without altering the fixation equations or control flow.
- 94b6dec imported the routine from upstream Bitbucket into the repository, preserving the same fixation behavior shown in the resolved diff.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_nfix' has no extracted documentation comment.
