---
kind: procedure
symbol: rcurv_interp_dep
title: rcurv_interp_dep
status: filled
source_hash: afba91104839226f
version_label: SWAT+ 62.0.0
args:
  icha: '`icha` selects which channel''s rating-curve table in `ch_rcurv` will be inspected
    and interpolated. The routine uses it as the index into the channel-specific curve data.'
  flow_dep: '`flow_dep` is the target flow depth used to choose the two rating-curve points
    to blend. It controls whether the routine uses the first point, interpolates between two
    points, or extrapolates above the highest point.'
locals:
  ielev: '`ielev` is the loop counter over the stored rating-curve points for channel `icha`.
    It advances until the routine finds the first point whose depth exceeds `flow_dep`, or
    reaches the last point.'
  rto: '`rto` is the interpolation ratio used to blend two rating-curve states. It is computed
    from `flow_dep` relative to the surrounding point depths, or from the first/last point
    when the depth is outside the interior range.'
uses:
  sd_channel_module: '`sd_channel_module` supplies the channel rating-curve types and shared
    state that this routine reads and writes. `ch_rcurv` holds the per-channel stored depth
    points and their associated curve parameters, while `rcurv` is the module-level output
    container that receives the interpolated parameter set.'
---

<!-- facts:header -->

Interpolates a channel rating curve for a specified flow depth. It selects or blends the stored curve points for channel `icha` and returns the matching curve state in `rcurv`.

## Bottom Line

This subroutine uses the channel rating-curve table for channel `icha` to estimate a full rating-curve state at the requested flow depth `flow_dep`. If the depth falls below the first stored point, it scales that first point directly; if it falls between stored points, it linearly interpolates between the two surrounding points; and if it is above the last stored point, it extrapolates from the last point and adjusts travel time to keep the maximum-bankfull behavior consistent.

The interpolated result is written to the module state `rcurv`, which `sd_hydsed_init` copies into the channel's initial inflow and outflow rating-curve states. That makes this routine part of the channel initialization path that sets the starting storage, volume, and travel-time conditions used by later hydrology and sediment calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during hydrology/sediment initialization when a channel's starting flow depth has been computed. `sd_hydsed_init` prepares `icha` and `flow_dep` from the initial organic-water flow and channel geometry, then calls `rcurv_interp_dep` to build the starting rating-curve state. The result is used immediately to populate `ch_rcurv(ich)%in1`, `ch_rcurv(ich)%out1`, and the initial storage volume, which downstream routing and sediment calculations depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. scan points | Loop over the stored rating-curve depth points for channel `icha` from the first point through `ch_rcurv(icha)%npts` to find where the requested depth fits. |
| 2. compare depth | Check whether `flow_dep` is below the current stored depth `ch_rcurv(icha)%elev(ielev)%dep`; if so, the routine has found the bracket or the first point that is above the target. |
| 3. first-point case | When the target depth is below the first stored point, compute a simple scaling ratio from `flow_dep` to the first point depth, scale the full first rating-curve record into `rcurv`, copy its travel time, and stop. |
| 4. interior case | When the target depth lies between two stored points, compute the interpolation fraction from the lower and upper point depths, interpolate the full parameter set with `chrc_interp`, and stop. |
| 5. upper-bound case | If the loop reaches the last stored point, treat the target depth as above the available table, extrapolate from the last point with a depth-based scaling factor, and reduce `rcurv%ttime` so travel time stays consistent with the maximum-bankfull adjustment. |
| 6. exit subroutine | Return to the caller after `rcurv` has been filled with the interpolated or extrapolated rating-curve state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `ch_rcurv, rcurv` | `ch_rcurv(icha)%npts, ch_rcurv(icha)%elev(ielev)%dep, ch_rcurv(icha)%elev(ielev), rcurv%ttime, ch_rcurv(icha)%elev(ielev)%ttime, ch_rcurv(icha)%elev(ielev-1)%dep, ch_rcurv(icha)%elev(ielev-1)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rcurv` | When `flow_dep` is below the first stored depth, between two stored depths, or above the last stored depth for channel `icha`. | `rcurv` is overwritten with the rating-curve parameters corresponding to the requested flow depth, either by scaling the nearest endpoint, interpolating between two stored points, or extrapolating from the last point. |
| `rcurv%ttime` | Only in the first-point and upper-bound branches, and through `chrc_interp` in the interior branch. | `rcurv%ttime` is set or adjusted so the interpolated rating curve carries the correct travel time for the chosen depth; the upper-bound branch divides by the extrapolation ratio to keep maximum-bankfull travel time from increasing with the extrapolated scaling. |

## File I/O

<!-- facts:io -->


## Lineage

`rcurv_interp_dep.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `rcurv_interp_dep.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'rcurv_interp_dep' has no extracted documentation comment.
- algorithm_steps revised: consolidated the loop and branch behavior into six source-backed steps, using only visible source lines.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
