---
kind: procedure
symbol: chrc_interp
title: chrc_interp
status: filled
source_hash: 3bfddddb230a81d7
version_label: SWAT+ 62.0.0
args:
  rc1: '`in` argument of type `type(channel_rating_curve_parameters)`.'
  rc2: '`in` argument of type `type(channel_rating_curve_parameters)`.'
  rci: '`out` argument of type `type(channel_rating_curve_parameters)`.'
  const: '`in` argument of type `real`.'
---

<!-- facts:header -->

Linearly interpolates between two channel rating-curve parameter sets by fraction `const`: rci = rc1 + const·(rc2 − rc1).

## Bottom Line

`chrc_interp` produces an interpolated `channel_rating_curve_parameters` record `rci` by linearly blending the two bracketing curves `rc1` and `rc2` at fraction `const`, for cross-sectional area, surface area, flow rate, depth, top width, channel and floodplain volumes, total volume, wetted perimeter, and travel time.

It lets the channel routing look up hydraulic geometry at an arbitrary point between tabulated rating-curve entries.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by the sd_channel routing when evaluating rating-curve geometry at a flow/stage between two stored curve points.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Review source manually | No major control-flow steps were extracted automatically. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `sd_channel_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sd_channel_module::chrc_interp' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
