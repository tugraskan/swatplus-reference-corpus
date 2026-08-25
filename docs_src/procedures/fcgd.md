---
kind: procedure
symbol: fcgd
title: fcgd
status: filled
source_hash: dfc4422ef42038c6
version_label: SWAT+ 62.0.0
args:
  xx: Current soil temperature to evaluate against the temperature-response curve; values
    at or below `tn` or at or above `tx` force the function to return zero.
locals:
  fcgd: 'Function result: the temperature multiplier returned to the caller after the curve
    is evaluated and clipped to nonnegative values.'
  tn: Lower temperature bound for the response curve, copied from `org_con%tn`.
  top: Optimum temperature at which the response curve peaks, copied from `org_con%top`.
  tx: Upper temperature bound for the response curve, copied from `org_con%tx`.
  qq: Shape exponent used in the temperature-response formula, computed from `tn`, `top`,
    and `tx` as `(tn - top)/(top - tx)`; initial value is 0 before assignment.
uses:
  carbon_module: carbon_module supplies the shared organic-control settings that define the
    temperature curve shape. `fcgd` does not hard-code the bounds; it reads `org_con%tn`,
    `org_con%top`, and `org_con%tx` so the same thresholds are used consistently by carbon
    and biomass routines that depend on this factor.
---

<!-- facts:header -->

Computes the soil-temperature multiplier used for carbon and biomass processes.

## Bottom Line

fcgd returns a temperature response factor for biological activity based on the current soil temperature `xx`. It uses three control points from `carbon_module%org_con` — minimum `tn`, optimum `top`, and maximum `tx` — to shape the curve, then clips any negative result to zero.

The function is used wherever SWAT+ needs a temperature scaling term for organic carbon decomposition or biomass mixing. It also protects the model from invalid fractional powers by returning 0 outside the active temperature range.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when other organic-process code needs a temperature scaling factor, after `carbon_module%org_con` has been populated with the active control settings. `cbn_zhang2` uses it when `org_con%tmpf == 2` to set the soil-temperature factor for carbon calculations, and `mgt_biomix` uses it to scale biomass mixing. Those later processes depend on the returned multiplier to reduce biological activity outside the allowed temperature range and to shape activity near the optimum.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load temperature bounds | Copies the minimum, optimum, and maximum temperature control values from `org_con` into local variables so the calculation uses the shared carbon-module settings. |
| 2. reject out-of-range temperatures | Checks whether `xx` is at or outside the active range `[tn, tx]`; if so, it returns 0 immediately to avoid invalid fractional powers and because biological activity is treated as zero there. |
| 3. compute curve exponent | Calculates `qq` from the temperature bounds, setting the curvature of the response function. |
| 4. evaluate response | Computes the temperature multiplier from `xx`, `tn`, `top`, and `tx` using the SWAT+ curve formula. |
| 5. clip negative results | Forces any negative computed value to zero so the factor cannot reduce downstream biological rates below zero. |
| 6. return function result | Ends the function and returns the computed multiplier to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:carbon_module] | `org_con` | `org_con%tn, org_con%top, org_con%tx` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show three behavioral changes: 6e6757a switched the function from hard-coded temperature bounds to `carbon_module%org_con`; 45c961c kept that module-based input and added inline comments identifying the original hard-coded defaults; and bc7755a added an explicit out-of-range guard that returns 0 before evaluating the fractional-power formula, preventing NaN generation. 39fabde only initialized locals and preserved the same formula, and 2ee1889 changed the end statement formatting without altering behavior.

- 6e6757a: made `fcgd` read `tn`, `top`, and `tx` from `carbon_module%org_con` instead of using fixed literals, so model-wide organic controls now govern the temperature curve.
- 45c961c: documented the meaning and legacy default values of the three temperature bounds while keeping the module-driven calculation intact.
- bc7755a: added an early zero return for `xx <= tn` or `xx >= tx`, preventing invalid `(xx-tn)**qq` evaluation and explicitly treating those temperatures as biologically inactive.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'fcgd' has no extracted documentation comment.
