---
kind: procedure
symbol: atri
title: atri
status: filled
source_hash: ef65641aab97c742
version_label: SWAT+ 62.0.0
args:
  at1: Lower bound of the triangular distribution; it anchors the left end of the possible
    draw range.
  at2: Target mean / peak-control value for the distribution; it shifts the triangle and also
    sets the final rescaling target.
  at3: Upper bound of the triangular distribution; it anchors the right end of the possible
    draw range and shapes the right-hand tail.
  at4i: Random-number seed passed into `Aunif`; it is updated in place so the next stochastic
    draw continues the same SWAT+ random stream.
locals:
  u3: Stores the width of the left segment of the triangle, computed as `at2 - at1`, for use
    in the inverse-transform branches.
  rn: Holds the uniform random variate returned by `Aunif(at4i)` and determines which side
    of the triangle is sampled.
  y: Stores the triangle height factor `2.0 / (at3 - at1)`, used to convert the uniform draw
    into the triangular CDF threshold and inverse formula.
  b1: Intermediate scaled random quantity `rn / y` used in both branches of the inverse transform.
  b2: Stores the right-side width `at3 - at2`, used to compute the right-hand inverse-transform
    expression.
  x1: Holds the threshold `y * u3 / 2.0` that decides whether the uniform draw falls on the
    left or right half of the triangle.
  xx: Temporary squared quantity under the square root in each branch; it is checked for nonpositive
    values before taking `Sqrt`.
  yy: Stores the square-root result, or zero when the radicand is nonpositive, before converting
    it into the final draw.
  amn: Holds the triangular distribution mean `(at3 + at2 + at1) / 3.0`, which is used to
    rescale the draw so the output matches the requested mean.
  atri: Local function result variable; it receives the sampled triangular value, is rescaled
    by the mean ratio, and is finally clipped to the interval `[0.001, 0.99]`.
  aunif: External random-number function used to obtain the initial uniform variate that drives
    the triangular sampling.
---

<!-- facts:header -->

Samples a value from a triangular distribution using a seedable uniform random variate. The result is scaled and clipped for use as a bounded stochastic fraction.

## Bottom Line

`atri` turns three triangular-distribution control points into one random draw. It first samples a uniform random number from `Aunif`, maps that number onto the left or right side of the triangle with square-root inversion, then rescales the draw so its mean matches `at2`.

The routine matters anywhere SWAT+ needs a bounded random fraction or timing factor. Callers use its output to vary storm timing, humidity, and half-hour rainfall fractions while advancing the shared random-number seed through `at4i`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs whenever SWAT+ needs a random value with triangular variability rather than a fixed constant. Upstream callers such as `cli_pgenhr`, `cli_rhgen`, and `climate_control` prepare the lower bound, central value, upper bound, and seed before calling it, and downstream weather generation uses the returned draw to compute storm duration, humidity, or half-hour rainfall fractions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize working scalars | Zeroes the local temporaries so the routine starts from a known state before computing distribution parameters and the random draw. |
| 2. Build distribution parameters | Computes the left width `u3`, draws a uniform random number with `Aunif(at4i)`, forms the height factor `y`, computes the right width `b2`, scales the random variate into `b1`, and determines the left-side threshold `x1` that separates the two inverse-transform branches. |
| 3. Sample left half of triangle | If the uniform variate falls in the left half of the triangle, computes the left-side inverse-transform radicand, guards against a nonpositive value, takes the square root when valid, and shifts the result up by `at1` to get the sample. |
| 4. Sample right half of triangle | If the uniform variate falls in the right half, computes the right-side inverse-transform radicand, guards against a nonpositive value, takes the square root when valid, and subtracts it from `at3` to get the sample. |
| 5. Rescale to requested mean | Computes the triangular mean `amn` and scales the sampled value by `at2 / amn` so the output is adjusted to the requested central tendency. |
| 6. Clamp to valid output range | Forces the final result away from the endpoints by clipping values at or above 1.0 to 0.99 and values at or below 0.0 to 0.001. |
| 7. Return the sample | Returns the bounded triangular random value to the caller. |

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

Resolved commits show the procedure was introduced in df07e3f as a new triangular random-number function, then adjusted in c7c8e22 when the latest source was imported, and later refined in 39fabde and bd18ad4. The diffs show the local variables were initialized to zero in 39fabde, the external declaration for `aunif` was modernized in bd18ad4, and the function end statement was made explicit as `end function atri` in bd18ad4.

- df07e3f added `atri` as a triangular-distribution sampler that uses `Aunif`, square roots, and a mean-based rescaling step.
- 39fabde initialized the working locals (`u3`, `rn`, `y`, `b1`, `b2`, `x1`, `xx`, `yy`, `amn`) to zero before use.
- bd18ad4 changed `aunif` to `real, external :: aunif` and made the closing statement `end function atri`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'atri' has no extracted documentation comment.
