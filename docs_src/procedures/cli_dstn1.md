---
kind: procedure
symbol: cli_dstn1
title: cli_dstn1
status: filled
source_hash: 8ca809279de9f814
version_label: SWAT+ 62.0.0
args:
  rn1: First uniform random number; it is the radial term inside `log(rn1)`, so its value
    controls the magnitude of the generated normal deviate.
  rn2: Second uniform random number; it controls the angular term in `cos(6.283185 * rn2)`,
    so it sets the sign and phase of the generated normal deviate.
locals:
  cli_dstn1: '`cli_dstn1` is the function result variable. It temporarily holds the generated
    standard-normal deviate before the function returns it to the caller.'
---

<!-- facts:header -->

Generates a standard-normal deviate from two uniform random numbers using the Box-Muller transform.

## Bottom Line

`cli_dstn1` turns two input random numbers into one value on the mean-zero, unit-standard-deviation normal distribution. SWAT+ uses that value as a reusable Gaussian noise source in climate generation and precipitation routines.

The routine is pure arithmetic: it computes `sqrt(-2*log(rn1)) * cos(6.283185*rn2)` and returns the result. The calling code uses that deviate to skew daily precipitation and weather perturbations through other climate generators.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the climate/weather generation path whenever a caller needs a Gaussian random value derived from two uniform draws. `cli_initwgn`, `cli_pgen`, and `cli_weatgn` each prepare their own uniform random inputs and previous-seed state, then call `cli_dstn1` to get the normal deviate used to perturb precipitation or weather variables downstream.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute the Box-Muller radius term. | Evaluates `Sqrt(-2. * Log(rn1))` to convert the first uniform random number into a nonnegative magnitude for the Gaussian deviate. |
| 2. Compute the angular term and return the deviate. | Multiplies the radius by `Cos(6.283185 * rn2)` to form one standard-normal sample, stores it in the function return variable `cli_dstn1`, and exits. |

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

Three resolved commits affect `cli_dstn1`. `df07e3f` introduced the file with the Box-Muller standard-normal calculation and inline documentation. `c7c8e22` preserved the same computation while formatting the source in a newer import. `bd18ad4` changed only the return-variable declaration and the function-end statement formatting; the numerical algorithm was unchanged.

- df07e3f added `cli_dstn1` as a new function implementing `Sqrt(-2. * Log(rn1)) * Cos(6.283185 * rn2)` for standard-normal sampling.
- c7c8e22 imported the file into the later source tree without changing the algorithm or interface.
- bd18ad4 updated the return-variable comment and named the closing statement `end function cli_dstn1`; behavior stayed the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_dstn1' has no extracted documentation comment.
