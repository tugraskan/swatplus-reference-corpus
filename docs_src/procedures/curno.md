---
kind: procedure
symbol: curno
title: curno
status: filled
source_hash: 9217085e38157d8f
version_label: SWAT+ 62.0.0
args:
  cnn: '`cnn` is the new SCS curve number for moisture condition II. The routine uses it as
    the starting point for updating `cn2(h)` and for computing the derived CN1, CN3, and retention/shape
    parameters.'
  h: '`h` selects the HRU whose curve-number, soil-water, and shape-parameter state will be
    updated. All state changes are written to the `h`-th entries of `cn2`, `smx`, and `wrt`
    and read from `soil(h)` and `hru(h)`.'
locals:
  c2: Temporary complement of the CN2 value (`100 - cnn`), used in the CN1 and CN3 transformations.
  cn1: Calculated curve number for moisture condition I, used to derive the maximum retention
    parameter `smx(h)` and the retention ratio inputs for `ascrv`.
  cn3: Calculated curve number for moisture condition III, used to derive the CN3 retention
    parameter and the upper-end retention ratio.
  s3: Retention parameter corresponding to CN3; used with `smx(h)` to compute the fraction
    difference `rto3` passed to `ascrv`.
  rto3: Fractional difference between the CN3 retention parameter and the maximum retention
    parameter; one of the two S-curve fit inputs passed to `ascrv`.
  rtos: Fractional difference between the CN=99 retention parameter and the maximum retention
    parameter; the second S-curve fit input passed to `ascrv`.
  smxold: Local copy of the maximum retention expression based on CN1; it is computed but
    not used after assignment in this routine.
  sumul: Copies the soil-profile saturation storage for HRU `h`; it provides the upper bound
    for the retention-parameter fit.
  sumfc: Represents the HRU’s field-capacity storage adjusted by `hru(h)%hyd%cn3_swf`; it
    is clipped into a valid range before being passed to `ascrv`.
  max: Intrinsic `MAX` function, used to enforce the lower bound `cn1 >= 0.4*cnn` and `sumfc
    >= 0.05`.
  amin1: Intrinsic `AMIN1` function, used to cap `sumfc` so it does not exceed `sumul - 0.05`.
uses:
  time_module: '`time_module` is imported by `curno`, but this source span does not reference
    any `time_module` components directly; it is present only as a module dependency and may
    be required by linked compile context elsewhere.'
  hru_module: '`hru_module` provides the per-HRU curve-number arrays and the `hru(h)%hyd%cn3_swf`
    calibration factor. `curno` writes `cn2(h)` and `smx(h)` and uses `wrt(:,h)`, so this
    module holds the state that the routine updates for the selected HRU.'
  soil_module: '`soil_module` provides the soil-profile water-storage limits `soil(h)%sumul`
    and `soil(h)%sumfc`. Those values define the retention-parameter bounds used to compute
    `sumfc` and therefore the S-curve shape parameters.'
---

<!-- facts:header -->

Updates an HRU’s SCS curve-number state and derives the water-retention shape parameters used by the runoff curve routines.

## Bottom Line

`curno` takes an HRU-level curve number for moisture condition II, stores it as `cn2(h)`, and derives the corresponding moisture-condition I and III curve numbers. From those values it computes the retention parameters and shape coefficients used by the SWAT+ water-retention / runoff curve formulation.

The procedure also folds in the HRU’s soil-water limits and the HRU hydrology calibration factor `cn3_swf` to set `smx(h)`, then calls `ascrv` to solve the two shape parameters written to `wrt(1,h)` and `wrt(2,h)`. These outputs are then available to later runoff and management routines that rely on updated curve-number behavior.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`curno` runs whenever another routine changes an HRU curve number or a related hydrology calibration factor and needs the dependent retention parameters refreshed. The callers shown here prepare `cn2(h)` or `cnn` first — for example, `actions`, `cal_parm_select`, `mgt_sched`, `pl_burnop`, `cn2_init`, and the calibration routines — then call `curno` so later runoff and water-retention calculations can use updated `cn2(h)`, `smx(h)`, and `wrt(:,h)` values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. assign new CN2 | Store the caller-supplied curve number for moisture condition II into `cn2(h)` so the HRU’s baseline CN state matches the requested value. |
| 2. derive CN1 and CN3 | Compute `c2 = 100 - cnn`, then calculate `cn1` with the exponential CN1 transformation and floor it at `0.4*cnn`; also compute `cn3` from the CN3 exponential relation. |
| 3. compute max retention | Calculate the maximum retention parameter `smx(h)` from `cn1`, then compute the CN3 retention parameter `s3` from `cn3`. |
| 4. form retention ratios | Convert the retention parameters into the normalized ratios `rto3` and `rtos` that define the S-curve shape fit. |
| 5. load soil-water bounds | Read `soil(h)%sumul` and a `cn3_swf`-adjusted `sumfc`, then constrain `sumfc` to stay positive and below `sumul - 0.05` before fitting the curve. |
| 6. solve shape parameters | Call `ascrv` with the normalized retention ratios and soil-water bounds so it can write the two water-retention shape parameters to `wrt(1,h)` and `wrt(2,h)`. |
| 7. return | Exit after updating the HRU’s curve-number state and water-retention coefficients. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time_module` | `none resolved from this source span` |
| [sym:hru_module] | `hru, cn2, smx, wrt` | `hru(h)%hyd%cn3_swf` |
| [sym:soil_module] | `soil` | `soil(h)%sumul, soil(h)%sumfc` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cn2(h)` | Always after `cnn` is assigned to `cn2(h)`; the computed value is independent of the `sumfc < 0.` branch except for the downstream shape fit. | `cn2(h)` is refreshed to the current moisture-condition-II curve number for the selected HRU, so later runoff calculations and logs see the updated baseline CN value. |
| `smx(h)` | After `cn1` is computed and `smx(h)` is assigned from it; `smx(h)` reflects the current HRU curve number, not the local `sumfc` correction branch. | `smx(h)` becomes the HRU’s maximum retention parameter, derived from the updated CN1 value and used as the scaling reference for the S-curve shape fit. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:1.1.4 | CN1 from CN2 | $CN_1=CN_2-\frac{20*(100-CN_2)}{(100-CN_2+exp[2.533-0.0636*(100-CN_2)])}$ | Direct CN1 transformation from CN2. |
| 2:1.1.5 | CN3 from CN2 | $CN_3=CN_2*exp[0.00673*(100-CN_2)]$ | Direct CN3 exponential relation. |
| 2:1.1.12 | Slope-adjusted CN2 | $CN_{2s}=\frac{(CN_3-CN_2)}{3}*[1-2*exp(-13.86*slp)]+CN_2$ | The printed CN2 slope-adjustment formula was not found as a direct implementation in this checkout; CN setup is handled through CN1/CN3 and S-curve parameterization instead. |

## Lineage

`curno.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `curno.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `09d23f0` (2025-06-26) — Comment and formatting changes
- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'curno' has no extracted documentation comment.
- time_module is imported but not referenced in the visible source span.
- algorithm_steps revised: expanded the draft from 3 generic steps to 7 source-backed steps to reflect the actual CN update, retention derivation, bound clamping, and S-curve solve sequence.
- Lineage evidence reported no resolved commits for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
