---
kind: procedure
symbol: qman
title: qman
status: filled
source_hash: 1bc6f4a45fa96b7f
version_label: SWAT+ 62.0.0
args:
  x1: 'Controls the scale factor in the Manning calculation: callers pass cross-sectional
    area when they want discharge, or `1.0` when they want velocity only.'
  x2: Supplies the hydraulic radius term, which combines the flow area and wetted perimeter
    into the effective depth/shape used by Manning's equation.
  x3: Supplies the Manning roughness coefficient `n`; larger values reduce the returned flow
    rate or velocity.
  x4: Supplies channel or waterway slope; the function uses its square root, so steeper slopes
    produce larger returned flow or velocity.
locals:
  qman: '`qman` is both the function name and the single local result variable; it holds the
    computed Manning flow rate or velocity that the function returns to the caller.'
---

<!-- facts:header -->

Computes flow velocity or flow rate with Manning's equation from area, hydraulic radius, roughness, and slope.

## Bottom Line

`qman` is a small helper function that evaluates Manning's equation. When callers pass an area in `x1`, it returns discharge; when callers pass `1.0` in `x1`, it returns flow velocity for the same cross section.

It matters because several channel, sediment, and grass waterway routines use it to turn geometric properties and roughness into velocity, discharge, and travel-time inputs for routing and storage calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs wherever SWAT+ needs Manning-based hydraulic speed or discharge from a shaped cross section. The caller must already have computed flow area, hydraulic radius, roughness, and slope, and later channel, sediment, and waterway calculations depend on the returned velocity or flow rate for capacity checks, travel time, and storage-discharge coefficients.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read Manning inputs and return the computed hydraulic value. | The function receives scale factor `x1`, hydraulic radius `x2`, roughness `x3`, and slope `x4`, then evaluates `x1 * x2 ** .6666 * Sqrt(x4) / (x3 + .001)` as the function result. |
| 2. Exit immediately. | The routine returns the computed result to the caller and ends without changing any shared state or calling other routines. |

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

Source-backed lineage resolved for three commits. `df07e3f` introduced `qman.f90` with the Manning-equation implementation and its interface/documentation comments. `94b6dec` preserved the same logic and content while importing the source into the repository. `2ee1889` made a textual cleanup only by changing the closing statement from `end` to `end function qman` without altering the calculation.

- `df07e3f` added the `qman` function and its Manning-equation formula for flow rate or velocity.
- `2ee1889` changed only the function terminator to `end function qman`; the numerical behavior stayed the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'qman' has no extracted documentation comment.
