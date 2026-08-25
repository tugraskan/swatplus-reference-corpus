---
kind: procedure
symbol: ascrv
title: ascrv
status: filled
source_hash: a8628ff24072d684
version_label: SWAT+ 62.0.0
args:
  x1: x1 is the first x-coordinate used in the S-curve fit, and it should be near the midpoint
    of the curve (about 0.5) so the routine can solve the midpoint-related shape term.
  x2: x2 is the second x-coordinate used in the S-curve fit, and it should be near an endpoint
    of the curve (close to 0.0 or 1.0) so the routine can solve the endpoint-related shape
    term.
  x3: x3 is the y-value paired with x1; it supplies the midpoint-side response value used
    to compute the intermediate log term and the final shape parameters.
  x4: x4 is the y-value paired with x2; it supplies the endpoint-side response value used
    together with x2 to solve x6.
  x5: x5 is the first output shape parameter. The routine writes the midpoint-controlled parameter
    here after combining the two point constraints.
  x6: x6 is the second output shape parameter. The routine writes the endpoint-controlled
    parameter here after comparing the two point constraints.
locals:
  xx: xx holds the intermediate logarithmic value computed from the first point, Log(x3/x1
    - x3), so that the second equation can reuse it when solving x6 and x5.
---

<!-- facts:header -->

Computes two S-curve shape parameters from two (x, y) points.

## Bottom Line

ascrv solves for the two parameters x5 and x6 in the SWAT+ S-curve form x = y / (y + exp(x5 + x6*y)). It uses one point near the curve midpoint and one point near an endpoint to derive the curve shape from the provided x/y pairs.

The routine matters because other initialization and setup code uses its results to parameterize plant growth, snow cover, and hydrologic response curves. Those callers prepare application-specific x/y points, then store the solved parameters back into database or HRU state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during parameter initialization and database reading, after each caller has prepared two curve points that bracket the intended S-curve behavior. Its outputs are then stored into plant, snow, or hydrologic parameter fields that later model calculations use to evaluate those curves.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. compute the intermediate log term from the first point | Calculates xx = Log(x3/x1 - x3), which encodes the first x/y point in a form that can be reused to solve the S-curve parameters. |
| 2. solve the second shape parameter from both points | Computes x6 as the difference between the two logarithmic terms divided by the y-value separation (x4 - x3), giving the slope-like parameter that controls the curve near the endpoints. |
| 3. solve the first shape parameter from x6 | Computes x5 by adding x3 * x6 to the intermediate log term, producing the midpoint-related shape parameter for the S-curve. |
| 4. return to caller | Returns the solved x5 and x6 values to the caller; the routine has no additional side effects beyond writing its output arguments. |

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

Four source-backed lineage commits were resolved. df07e3f added the new ascrv subroutine with the S-curve formulas and documentation. c7c8e22 carried the same implementation forward from the imported source snapshot. 39fabde changed xx from an uninitialized local to xx = 0. for safety. 2ee1889 kept the code logic unchanged except for formatting the terminator as end subroutine ascrv and removing a blank line.

- df07e3f introduced ascrv with the two-logarithm solution for x5 and x6 and the original purpose text.
- 39fabde initialized xx to 0.0, removing an uninitialized local variable risk without changing the algorithm.
- 2ee1889 did not change the computation; it only updated the subroutine terminator style and spacing.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ascrv' has no extracted documentation comment.
