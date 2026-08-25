---
kind: procedure
symbol: wq_k2m
title: wq_k2m
status: filled
source_hash: 60935e598d152049
version_label: SWAT+ 62.0.0
args:
  t1: t1 is the residence-time or timescale parameter passed into the semi-analytic solution;
    it sets the denominator and exponential decay behavior used to infer the m-term.
  t2: t2 is the timestep/observation interval used in the semi-analytic update; it controls
    the exponential weighting applied when solving for the m-term.
  tk: tk is the known kinetic term supplied for the second semi-analytic evaluation; it lets
    the function compare the target response against the zero-rate case to solve for m.
  c1: c1 is the upstream/previous concentration input to the semi-analytic equation; it participates
    in both the helper evaluations and the algebra used to solve the m-term.
  c2: c2 is the incoming concentration input to the semi-analytic equation; it is carried
    through the helper evaluations and subtracted in the final m-term formula.
locals:
  h1: Holds the first semi-analytic evaluation with zero m-term and zero kinetic term, giving
    the baseline helper result for the same t1, t2, c1, and c2 inputs.
  h2: Holds the second semi-analytic evaluation with zero m-term and the supplied tk kinetic
    term, providing the comparison value used to back-calculate tm.
  help: Stores exp_w(-t2 / t1), the safe exponential decay factor used to avoid underflow
    when computing the m-term formula.
  tm: Stores the solved m-term value computed from h2, c1, c2, t1, and the exponential factor;
    this is the function's result.
  h3: Holds a final semi-analytic check using the solved tm and zero kinetic term; it is computed
    after tm is known, likely as a consistency evaluation.
  wq_k2m: Function return variable that receives the solved m-term before the function exits.
  wq_semianalyt: Local explicit interface declaration for the external semi-analytic helper
    used by this function to evaluate the QUAL2E expression.
uses:
  utils: The routine relies on exp_w from utils to compute exp(-t2 / t1) with underflow protection,
    which stabilizes the m-term calculation when the exponent is very negative.
---

<!-- facts:header -->

Computes the m-term parameter for a semi-analytic QUAL2E water-quality update.

## Bottom Line

wq_k2m solves for the constant m-term used in the semi-analytic QUAL2E concentration equation. It evaluates the semi-analytic helper twice, uses a safe exponential to form the correction factor, and returns the inferred m-term that matches the specified rate and concentration inputs.

In practice, ch_watqual4 uses this value to convert an rk1 kinetic rate into an m-term before updating CBOD with wq_semianalyt. That makes the function part of the carbonaceous oxygen-demand calculation path rather than a standalone mathematical utility.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the water-quality carbon/oxygen update path. ch_watqual4 prepares the time, timestep, rate, and concentration inputs, then calls wq_k2m to convert an rk1 kinetic coefficient into an m-term; that result is immediately reused to drive the subsequent wq_semianalyt update of ht3%cbod.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Evaluate the semi-analytic helper with zero m-term and zero kinetic term. | Computes h1 from wq_semianalyt using t1, t2, c1, and c2 with both reaction terms set to zero, establishing a baseline response. |
| 2. Evaluate the semi-analytic helper with zero m-term and the supplied kinetic term. | Computes h2 with tk included so the routine can compare the target kinetic response against the baseline and infer the missing m-term. |
| 3. Compute the safe exponential decay factor. | Uses exp_w(-t2 / t1) to form a numerically safe decay term for the m-term formula. |
| 4. Solve the m-term algebraically. | Derives tm from h2, c1, c2, t1, and the exponential factor, producing the constant term that matches the semi-analytic relation. |
| 5. Re-evaluate the semi-analytic helper using the solved m-term. | Computes h3 with tm and zero kinetic term, apparently as a consistency or verification evaluation after tm has been found. |
| 6. Return the solved m-term. | Assigns tm to the function result wq_k2m and exits the function. |

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

Two resolved commits created and then refined this function. Commit bd18ad4 added wq_k2m as a new helper for the QUAL2E semi-analytic solution and initially declared wq_semianalyt as external; commit 35d329f changed that declaration to a real statement to prevent a warning, while leaving the calculation logic unchanged.

- bd18ad4 introduced the new wq_k2m function, including the semi-analytic calls, exp_w-based decay factor, tm solve, and return value.
- 35d329f adjusted only the local declaration of wq_semianalyt from external to real to suppress a warning; the function's computation path stayed the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wq_k2m' has no extracted documentation comment.
