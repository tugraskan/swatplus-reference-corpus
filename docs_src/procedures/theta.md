---
kind: procedure
symbol: theta
title: theta
status: filled
source_hash: 834441d357dfca04
version_label: SWAT+ 62.0.0
args:
  r20: '`r20` is the baseline reaction-rate coefficient at 20°C. The function raises or lowers
    this starting rate according to temperature, so larger `r20` values produce proportionally
    larger corrected rates.'
  thk: '`thk` is the empirical temperature adjustment factor for the reaction. It controls
    how strongly the rate changes for each degree above or below 20°C when the function evaluates
    `thk ** (tmp - 20.)`.'
  tmp: '`tmp` is the current temperature used for the correction. It sets the exponent offset
    from 20°C, so warmer or cooler conditions directly change the returned rate constant.'
locals:
  theta: '`theta` is the function result: the temperature-corrected reaction rate coefficient.
    It is assigned the computed value and returned to the caller for use in downstream decay
    or reaction calculations.'
---

<!-- facts:header -->

`theta` scales a 20°C reaction rate to the current water or air temperature. It returns a temperature-corrected first-order rate constant.

## Bottom Line

This function applies the QUAL2E temperature adjustment formula, computing a local reaction rate from a standard 20°C rate (`r20`), an empirical temperature factor (`thk`), and the current temperature (`tmp`). The result is used anywhere SWAT+ needs temperature-dependent decay or reaction rates.

In the calling code, `theta` feeds pathogen die-off, nutrient settling/reaction, and constituent reaction calculations so those processes respond to the day’s temperature instead of using a fixed rate.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs whenever a process needs a temperature-adjusted first-order rate constant. Upstream callers prepare a base rate plus a temperature factor and the current water, reach, or wetland temperature, and later model steps use the returned value to compute pathogen die-off, constituent reaction loss, or nutrient adjustment in channels, reservoirs, wetlands, and landscape processes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. compute temperature-corrected rate | Calculates the returned reaction coefficient as `r20 * thk ** (tmp - 20.)`, which converts a 20°C base rate into a local rate at the current temperature. |
| 2. return to caller | Ends the function and returns the computed `theta` value to the process that requested the temperature adjustment. |

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

`theta` was added in commit df07e3f with the QUAL2E temperature-correction formula and the accompanying argument comments. Commit 94b6dec preserved the same computation and documentation while carrying the file forward from the Bitbucket source import. Commit 2ee1889 changed only the function ending from a bare `end` to `end function theta`.

- df07e3f introduced the `theta(r20,thk,tmp)` function and its `r20 * thk ** (tmp - 20.)` calculation for temperature-corrected reaction rates.
- 2ee1889 updated the closing statement to `end function theta` without changing the rate calculation.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'theta' has no extracted documentation comment.
