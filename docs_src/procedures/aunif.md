---
kind: procedure
symbol: aunif
title: aunif
status: filled
source_hash: 9174084b692b4e05
version_label: SWAT+ 62.0.0
locals:
  x2: Temporary quotient used to split the seed update into safe integer pieces so the multiplication
    and subtraction do not overflow the generator logic.
args:
  x1: Holds the evolving random-number seed; it is both the input state and the updated output
    state returned to the caller.
---

<!-- facts:header -->

Generates a uniform pseudo-random number in the range 0.0 to 1.0 and advances the integer seed used by the SWAT+ random-number stream.

## Bottom Line

Aunif is the core uniform random-number generator used by several climate and conditions routines. It takes an integer seed by intent(in out), updates that seed with a Park-Miller style prime-modulus recurrence, and returns the new seed scaled to a real number between 0 and 1.

That matters because callers use the returned variate to drive stochastic weather generation, precipitation occurrence, wind speed, temperature perturbations, and probability-based condition logic. The routine is also responsible for keeping the seed in range by correcting negative intermediate results before scaling.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs wherever SWAT+ needs a reproducible uniform random draw. Upstream callers such as cli_initwgn, cli_pgen, cli_weatgn, cli_wndgen, conditions, atri, and gcycl prepare a seed from their own random-seed arrays or seed variables, then call aunif to get the next random variate. Later behavior depends on the returned number to decide event probabilities, draw weather-related randomness, and advance each caller's seed stream for the next stochastic draw.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. derive quotient from seed | Compute x2 = x1 / 127773 so the current seed can be updated using the generator's split multiply-and-subtract form. |
| 2. update seed with prime-modulus recurrence | Replace x1 with 16807 * (x1 - x2*127773) - x2 * 2836, which is the Park-Miller prime-modulus step expressed to avoid large intermediate values. |
| 3. correct negative seed | If the recurrence produced a negative seed, add 2147483647 so the seed stays in the valid positive generator range. |
| 4. scale to unit interval | Compute unif = x1 * 4.656612875d-10, converting the integer seed into a real number between 0.0 and 1.0. |
| 5. return value and updated seed | Return the uniform random variate while leaving x1 updated for the caller's next random draw. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `unif` | When the current seed update produces x1 < 0. | The routine adds 2147483647 to the seed so the generator remains in the valid positive range before the real-valued uniform variate is formed. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed aunif. df07e3f introduced the function as a new file with the uniform generator implementation and documentation block. 39fabde changed the local seed helper x2 from an uninitialized integer declaration to integer :: x2 = 0. 2ee1889 changed the ending from plain end to end function aunif.

- df07e3f added aunif.f90 with the full uniform random-number generator and its seed-updating recurrence.
- 39fabde initialized local variable x2 to 0, making the seed-quotient helper explicitly initialized.
- 2ee1889 made the function end statement explicit as end function aunif.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'aunif' has no extracted documentation comment.
