---
kind: procedure
symbol: wq_semianalyt
title: wq_semianalyt
status: filled
source_hash: a0f53936dc504b4b
version_label: SWAT+ 62.0.0
args:
  tres: '`tres` is the reach residence time; it sets the decay/accumulation timescale in the
    exponential update and appears in the denominators of the source and equilibrium terms.'
  tdel: '`tdel` is the calculation timestep; it scales the exponential factor so the routine
    computes the change over that interval.'
  term_m: '`term_m` is the constant source/sink term in the semi-analytic equation; it shifts
    the equilibrium concentration contributed by processes other than the incoming concentration.'
  prock: '`prock` is the kinetic rate term; it is subtracted from `1./tres` to form the effective
    exponent coefficient that controls how quickly concentration relaxes.'
  cprev: '`cprev` is the concentration from the previous timestep; it is multiplied by the
    exponential carryover factor to preserve the remaining mass from the last step.'
  cint: '`cint` is the incoming concentration; together with `tres` it contributes to the
    steady-state/source term that is blended into the new concentration.'
locals:
  help1: '`help1` stores the effective rate coefficient `1./tres - prock` used in the exponential
    and equilibrium calculations.'
  help2: '`help2` stores the safe exponential decay factor `exp_w(-tdel * help1)` that carries
    the previous concentration forward.'
  help3: '`help3` stores the numerator of the source/equilibrium term, `cint / tres + term_m`.'
  help4: '`help4` stores the equilibrium concentration contribution `help3 / help1` used in
    the closed-form solution.'
  term1: '`term1` stores the carried-forward part of the solution, `cprev * help2`.'
  term2: '`term2` stores the new forcing contribution, `help4 * (1. - help2)`.'
  yy: '`yy` holds the assembled concentration result before it is assigned to the function
    name; it duplicates the final expression for readability.'
  wq_semianalyt: '`wq_semianalyt` is the function return value; it receives the final semi-analytic
    concentration update.'
uses:
  utils: The procedure uses `exp_w` from `utils` to evaluate the exponential safely, avoiding
    underflow when the timestep-rate product is very negative.
---

<!-- facts:header -->

Computes a semi-analytic QUAL2E concentration update for a reach over a timestep. It returns the end-of-step value from the previous concentration, incoming concentration, reaction term, residence time, and timestep.

## Bottom Line

wq_semianalyt evaluates the closed-form QUAL2E-style update used to advance a water-quality concentration through one timestep. It combines the previous concentration with the incoming concentration, a constant source/sink term, residence time, and reaction rate to produce the next value.

This matters because other water-quality routines use the result as the concentration after a day or substep, including algal biomass calculations and the k-to-m conversion logic.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside water-quality calculations whenever a semi-analytic QUAL2E concentration update is needed. `ch_watqual4` calls it when computing end-of-day algal biomass, and `wq_k2m` calls it when solving for a kinetic-to-source term conversion; both callers prepare the residence time, timestep, rate term, previous concentration, and incoming concentration before invoking it, and later model behavior depends on the returned concentration update.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Form the effective rate coefficient. | Computes `help1 = 1./tres - prock`, combining residence time and kinetic rate into the net exponent coefficient for the update. |
| 2. Compute the safe decay factor. | Calls `exp_w` on `-tdel * help1` to get the exponential carryover factor for the timestep. |
| 3. Build the forcing numerator. | Computes `help3 = cint / tres + term_m`, combining incoming concentration and the constant term. |
| 4. Convert forcing to equilibrium form. | Divides the forcing numerator by the net rate coefficient to get the equilibrium contribution `help4`. |
| 5. Carry the previous concentration forward. | Computes `term1 = cprev * help2`, the fraction of the old concentration that survives through the timestep. |
| 6. Add the new forcing contribution. | Computes `term2 = help4 * (1. - help2)`, the amount added by the source/equilibrium term over the timestep. |
| 7. Assemble the final concentration. | Adds the carryover and forcing pieces, stores the sum in `yy`, and assigns the same value to the function result. |
| 8. Return to caller. | Exits the function after the result has been written to the function name. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:utils] | `utils::exp_w` | `exp_w` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The function was introduced in bd18ad4, which added the full semi-analytic QUAL2E solver and the `exp_w` call for safe exponent handling. Later lineage entries available in the packet do not provide diffs for this file, so no further behavior change can be confirmed from the evidence.

- bd18ad4 introduced `wq_semianalyt` as a new function, added the semi-analytic concentration formula, and routed the exponential through `exp_w` for underflow-safe evaluation.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wq_semianalyt' has no extracted documentation comment.
