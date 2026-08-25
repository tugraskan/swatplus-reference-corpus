---
kind: procedure
symbol: nuts
title: nuts
status: filled
source_hash: 038507220f80fde4
version_label: SWAT+ 62.0.0
args:
  u1: Actual amount of the element present in the plant. In the calling routines, this is
    the measured plant nitrogen or above-ground plant phosphorus mass that drives the stress
    calculation.
  u2: Optimal amount of the same element for the plant. This sets the reference level for
    the ratio and also disables stress when it is effectively zero.
  uu: Output stress factor returned by the helper. The caller uses this as the plant nutrient-stress
    response, with values bounded between 0 and 1.
---

<!-- facts:header -->

Computes a plant nitrogen-or-phosphorus stress factor from actual versus optimal element content.

## Bottom Line

`nuts` turns an actual-to-optimal element ratio into a bounded growth-stress response. It is used for both nitrogen and phosphorus stress, so the same helper serves two plant nutrient limitation pathways.

The routine first forms a scaled state variable from `u1` and `u2`, then maps that value through a logistic-style expression. It forces the result to zero when the computed stress is nonpositive, to one when the stress is very large, and to one whenever the optimal requirement `u2` is essentially zero.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the plant nutrient uptake workflow after the caller has updated plant nitrogen or phosphorus pools. `pl_nup` prepares total plant N and the crop-specific optimum N, then combines the result with an additional nitrate-stress limit; `pl_pup` prepares above-ground plant P and optimum P and stores the returned value as phosphorus stress. Later growth logic depends on this output because the caller writes it into `pcom(j)%plstr(ipl)%strsn` or `strsp` for use in subsequent growth constraint calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize output to zero | Sets `uu` to 0 before any calculation, providing a default stress response if later logic does not raise it. |
| 2. compute scaled nutrient ratio | Forms a scaled state variable from the actual-versus-optimal nutrient ratio: `uu = 200. * (u1 / (u2 + .0001) - .5)`. The small offset prevents division by zero. |
| 3. reject nonpositive stress | If the scaled value is `<= 0`, the routine keeps the response at zero, meaning no growth benefit is credited from the nutrient state. |
| 4. map moderate stress through response curve | For intermediate values below 99, the routine converts the scaled state into a bounded factor using `uu / (uu + Exp(3.535 - .02597 * uu))`. This is the main nonlinear nutrient-stress response. |
| 5. cap very large stress at unity | If the scaled value reaches 99 or more, the routine assigns `uu = 1.`, representing the maximum response allowed by the helper. |
| 6. override when optimum is negligible | If the optimal nutrient amount `u2` is essentially zero, the routine forces `uu = 1.` regardless of the earlier calculation. |
| 7. return to caller | Exits the subroutine after writing the final stress factor to the output argument. |

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


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:3.1.6 | Nitrogen stress factor | $nstrs=1-\frac{\phi _n}{\phi_n +exp[3.535-0.02597*\phi _n]}$ | The helper routine computes the growth factor uu = phi_n/(phi_n + exp(3.535 - 0.02597*phi_n)); the theory page prints stress as 1 - that term, so SWAT+ uses the opposite convention and combines it through reg = min(...). |
| 5:3.1.7 | Nitrogen stress state variable | $\phi_n=200*(\frac{bio_N}{bio_{N,opt}}-0.5)$ | The helper variable is formed as 200*(u1/(u2+1e-4) - 0.5). In the nitrogen call site, u1 is total plant N and u2 is optimal plant N. |
| 5:3.1.8 | Phosphorus stress factor | $pstrs=1-\frac{\phi_p}{\phi_p +exp[3.535-0.02597*\phi_p]}$ | The same nuts helper computes a growth factor rather than the printed stress complement. SWAT+ therefore uses the opposite convention from the theory page and combines the result through reg = min(...). |
| 5:3.1.9 | Phosphorus stress state variable | $\phi_p=200*(\frac{bio_P}{bio_{P,opt}}-0.5)$ | The helper variable is formed as 200*(u1/(u2+1e-4) - 0.5). For phosphorus, the call site passes above-ground plant P and optimal P, so the state variable is not formed from a separately named phi_p variable in pl_pup itself. |

## Lineage

Two source-backed commits were resolved for `nuts`. The routine was introduced in `df07e3f` as a new file with the current nutrient-stress calculation, and `94b6dec` kept the implementation unchanged in the diff shown while re-adding the same source after the file was imported from Bitbucket.

- df07e3f introduced `nuts.f90` and its nutrient-stress helper logic, including the scaled ratio, nonlinear response curve, and the `u2 <= 1.e-6` override.
- 94b6dec re-imported the same `nuts.f90` content into the repository snapshot shown; the diff excerpt does not show a behavioral change to the routine itself.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nuts' has no extracted documentation comment.
