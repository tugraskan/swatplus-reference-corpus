---
kind: procedure
symbol: rcurv_interp_flo
title: rcurv_interp_flo
status: filled
source_hash: 43a009b91228428e
version_label: SWAT+ 62.0.0
args:
  icha: '`icha` selects which channel rating curve in `ch_rcurv` is used. The routine reads
    `ch_rcurv(icha)` to get the set of elevation/flow points for that specific channel.'
  flo_rate: '`flo_rate` is the flow rate to match against the rating-curve points. It determines
    whether the routine uses the first point, interpolates between two points, or extrapolates
    above the highest point.'
locals:
  ielev: '`ielev` is the loop index over the rating-curve points for the selected channel.
    It advances until the routine finds the first stored point whose `flo_rate` exceeds the
    requested flow.'
  rto: '`rto` is the interpolation ratio used to blend between two rating-curve points. It
    is computed from the requested flow relative to the bracketing flow values and then passed
    to the interpolation logic.'
uses:
  sd_channel_module: '`sd_channel_module` provides the shared rating-curve storage that this
    routine reads from and writes to. The routine needs `ch_rcurv(icha)%npts` and the stored
    `elev` points to locate the bracket for interpolation, and it writes the resulting curve
    into the module variable `rcurv` so later channel-process routines can reuse the same
    interpolated state.'
---

<!-- facts:header -->

Interpolates a channel rating curve for a given flow rate. It returns a blended curve in `rcurv` that downstream channel routing, water-quality, and sediment routines use.

## Bottom Line

`rcurv_interp_flo` looks up the channel rating-curve points for channel `icha` and interpolates between the two bracketing flow-rate points for the supplied `flo_rate`. The interpolated rating curve is stored in the module variable `rcurv`.

If the requested flow is below the first rating-curve point, it scales that first point directly. If the flow is above the highest point, it extrapolates from the top point and adjusts travel time so it does not keep shrinking unrealistically. The result is used by routing, water-quality, and sediment calculations that need the current channel depth, area, and travel time.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs whenever a channel process needs the current rating curve for a specific flow rate. Its callers set up the channel index and a flow-rate value derived from the current routing or peak-flow calculation, then call `rcurv_interp_flo` before using `rcurv` in routing, water-quality, or sediment computations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop through rating-curve points | Iterate over the stored rating-curve points for channel `icha` from the first point through `npts` to find the first point with a flow rate above the requested `flo_rate`. |
| 2. test for bracketing point | Compare the requested flow rate to the current stored point. When `flo_rate` is less than the point's flow rate, the routine has found the upper bracket for interpolation or the first point for low-flow scaling. |
| 3. handle below-first-point case | If the first stored point already exceeds the requested flow, scale that first rating-curve point by `flo_rate / point_flow` and copy its travel time directly into `rcurv%ttime`, then stop searching. |
| 4. interpolate between two points | If the bracket is not the first point, compute the interpolation fraction from the previous and current flow-rate points, then call `chrc_interp` to blend the two rating-curve states into `rcurv`. |
| 5. handle above-highest-point case | When the loop reaches the last stored point without finding a larger flow rate, extrapolate from the top point using a ratio greater than one, scale the top rating-curve point into `rcurv`, and reduce `rcurv%ttime` so travel time does not decrease without bound at very high flow. |
| 6. exit after producing the curve | Return to the caller after `rcurv` has been filled with the interpolated or extrapolated channel rating curve. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `ch_rcurv, rcurv` | `ch_rcurv(icha)%npts, ch_rcurv(icha)%elev(ielev)%flo_rate, ch_rcurv(icha)%elev(ielev), rcurv%ttime, ch_rcurv(icha)%elev(ielev)%ttime, ch_rcurv(icha)%elev(ielev-1)%flo_rate, ch_rcurv(icha)%elev(ielev-1)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rcurv` | When `flo_rate` falls below a stored rating-curve point or exceeds the highest point after the loop reaches `ielev == 4`. | `rcurv` is overwritten with the channel rating curve corresponding to the requested flow rate, either by scaling a single point, interpolating between two stored points, or extrapolating from the top point. This makes the module-level curve consistent with the current hydraulic condition for later calculations. |
| `rcurv%ttime` | When the routine fills `rcurv` from the first point, from `chrc_interp`, or from the top-point extrapolation branch. | `rcurv%ttime` is set to the interpolated travel time from the bracketed points, copied from the first point at low flow, or adjusted at high flow so the travel time does not keep shrinking unrealistically above the largest stored rating-curve point. |

## File I/O

<!-- facts:io -->


## Lineage

`rcurv_interp_flo.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `rcurv_interp_flo.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'rcurv_interp_flo' has no extracted documentation comment.
- Git lineage evidence reported no resolved commits for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
