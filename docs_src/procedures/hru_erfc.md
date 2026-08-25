---
kind: procedure
symbol: hru_erfc
title: hru_erfc
status: filled
source_hash: a81e07b7cbe2867e
version_label: SWAT+ 62.0.0
args:
  xx: Input value whose sign and magnitude determine the complementary error-function approximation;
    the routine scales it, uses its absolute value in the polynomial, and restores the sign
    for negative xx.
locals:
  c1: Coefficient in the polynomial approximation used to estimate erf from the scaled input
    x.
  c2: Second coefficient in the erf approximation polynomial; contributes to the x^2 term.
  c3: Third coefficient in the erf approximation polynomial; contributes to the x^3 term.
  c4: Fourth coefficient in the erf approximation polynomial; contributes to the x^4 term.
  x: Intermediate scaled magnitude of xx, computed as Abs(1.4142 * xx), used as the argument
    to the approximation polynomial.
  erf: Holds the approximate error-function value derived from x, then is sign-adjusted for
    negative xx before erfc is formed.
  hru_erfc: Function result variable; receives 1 - erf and is returned to the caller as the
    complementary error-function approximation.
---

<!-- facts:header -->

Computes a complementary error-function approximation for a real input xx.

## Bottom Line

`hru_erfc` returns an approximation of the complementary error function, erfc(xx), using a fixed polynomial expression. It is a small math utility routine: it converts the input to a scaled absolute value, evaluates an erf approximation, flips the sign for negative inputs, and then returns 1 - erf.

The result matters anywhere SWAT+ needs a smooth Gaussian/probability-style transform of a real variable. The routine is self-contained and does not read files, call other project routines, or depend on model state beyond its argument.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs whenever SWAT+ needs the complementary error function and an internal approximation is sufficient. The source comments show it only depends on the intrinsic Abs and on the incoming xx value; no upstream SWAT+ routine is identified here, and no downstream model state is directly updated beyond the returned value.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. scale input to a nonnegative magnitude | Compute x as Abs(1.4142 * xx), so the approximation works from the magnitude of the input after a fixed sqrt(2)-style scale factor is applied. |
| 2. evaluate erf approximation | Compute erf from a polynomial in x, then transform it with the power term so the result approximates the error function. |
| 3. restore sign for negative input | If xx is negative, negate erf so the approximation follows the odd symmetry of the error function. |
| 4. convert erf to complementary error function | Set the function result to 1. - erf, which is the complementary error function value returned to the caller. |
| 5. return result | Return control to the caller with hru_erfc holding the computed complementary error-function approximation. |

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

Source-backed lineage commits were resolved. The routine was introduced in df07e3f with the full hru_erfc implementation and inline initialization of x and erf; 39fabde changed those declarations to initialize x and erf directly, while 2ee1889 only renamed the closing statement to `end function hru_erfc` without changing behavior.

- df07e3f added the hru_erfc function body, including the approximation formula, sign handling, and 1 - erf return value.
- 39fabde initialized local variables x and erf at declaration time; the body still resets them before use, so the computational behavior is unchanged.
- 2ee1889 changed only the function terminator text to `end function hru_erfc`, with no effect on results.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_erfc' has no extracted documentation comment.
