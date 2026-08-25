---
kind: procedure
symbol: cli_weatgn
title: cli_weatgn
status: filled
source_hash: 38075346e49aed42
version_label: SWAT+ 62.0.0
args:
  iwgn: '`iwgn` selects which weather-gage column in `climate_module` is being updated. The
    routine uses it to pick the correct `rndseed`, `rnd2`, `rnd8`, `rnd9`, `wgncur`, and `wgnold`
    entries for that gage.'
locals:
  zshape: Holds the fixed 3x3 shape descriptor used by `reshape` when loading the hard-coded
    A and B matrices.
  n: 'Loop index over the three weather-generator channels: max temperature, min temperature,
    and radiation.'
  l: Inner-loop index used to accumulate each row of the matrix products for the current weather-generator
    channel.
  a: Stores the hard-coded 3x3 A matrix used to carry forward the previous residual state
    from `wgnold` into the new `wgncur` values.
  b: Stores the hard-coded 3x3 B matrix used to mix the new random normal deviates into the
    current weather-generator residuals.
  xx: Temporary 3-element accumulator for the A * wgnold contribution before it is added into
    `wgncur`.
  e: Holds the three independent normal deviates generated from the uniform random stream
    for max temperature, min temperature, and radiation.
  v2: Temporary uniform random variate returned by `aunif`; it is passed into `cli_dstn1`
    and also written back to the corresponding `rnd*` state.
  aunif: External uniform-random-number generator used to advance the seed and produce each
    new uniform input for the normal transform.
  cli_dstn1: External transform that converts the uniform pair into a normal deviate; this
    routine uses it to form the residual inputs for the weather-generator channels.
uses:
  climate_module: '`climate_module` matters because it owns the shared per-gage random-number
    seeds and weather-generator state that this routine reads and updates. Without those module
    arrays, `cli_weatgn` would not be able to advance the correct gage-specific random stream
    or preserve the previous residuals needed for the recursion.'
---

<!-- facts:header -->

Generates the three weather-generator residuals for a given weather-gage index and updates the stored current/previous residual state. It is part of the climate random-number stream used to drive later temperature and precipitation-related weather generation.

## Bottom Line

`cli_weatgn` draws three new random inputs for the weather generator, converts them into residual terms for maximum temperature, minimum temperature, and radiation, and then combines those residuals with the previous residual state to form the next `wgncur` values. The routine clamps each result to the range -1 to 1 and copies it into `wgnold` so the next call starts from the updated history.

This matters because `climate_control` calls it once per weather gage before temperature generation, so the climate module's per-gage random state is refreshed in the correct sequence and later weather calculations see consistent residual correlations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cli_weatgn` runs during climate setup and weather generation, after `climate_control` has selected each weather-gage index and before temperature generation for that gage. Its results feed the later climate routines that depend on the updated weather-generator residual state, especially the temperature-generation path invoked immediately after this call.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize matrices and scratch arrays | Set the 3x3 array shape, load the fixed A and B coefficient matrices, and clear the temporary residual accumulator arrays before generating new values. |
| 2. generate max-temperature residual input | Draw a new uniform random number from the max-temperature seed, convert it to a standard-normal deviate, and store the updated uniform value back into `rnd8(iwgn)`. |
| 3. generate min-temperature residual input | Draw the next uniform number from the min-temperature seed, convert it to a standard-normal deviate, and write the updated uniform value back into `rnd9(iwgn)`. |
| 4. generate radiation residual input | Draw the next uniform number from the radiation seed, convert it to a standard-normal deviate, and write the updated uniform value back into `rnd2(iwgn)`. |
| 5. compute the new correlated residuals | For each of the three weather-generator channels, sum the B-matrix contribution from the new normal deviates and the A-matrix contribution from the previous residual state. |
| 6. finalize and store the updated state | Add the stored A-matrix contribution into each current residual, clamp the result to the valid interval [-1, 1], and copy the finished value into `wgnold` for the next call. |
| 7. return to caller | Exit after the weather-generator residuals and history arrays have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `rnd8, rnd9, rnd2, wgncur, wgnold` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rnd8(iwgn)` | After the max-temperature uniform draw at lines 75-77. | `rnd8(iwgn)` is replaced with the newest uniform random variate from the max-temperature seed so the stream advances for the next call. |
| `rnd9(iwgn)` | After the min-temperature uniform draw at lines 79-81. | `rnd9(iwgn)` is replaced with the newest uniform random variate from the min-temperature seed so the stream advances for the next call. |
| `rnd2(iwgn)` | After the radiation uniform draw at lines 83-85. | `rnd2(iwgn)` is replaced with the newest uniform random variate from the radiation seed so the stream advances for the next call. |
| `wgncur(n,iwgn)` | During the two nested loops that accumulate the B-matrix term and then add the A-matrix term, followed by the clamp at lines 87-98. | `wgncur(n,iwgn)` is recomputed as the current correlated residual for each of the three weather-generator channels, then limited to the range -1 to 1 so the stored residual stays bounded. |
| `wgnold(n,iwgn)` | After `wgncur(n,iwgn)` is finalized in the second loop at line 99. | `wgnold(n,iwgn)` is overwritten with the current residual so the next invocation can use it as the previous-state input to the recursion. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:3.4.1 | Daily residual recursion | $\chi_i(j)=A{\chi_{i-1}}(j)+B{\varepsilon_i}(j)$ | wgncur(n)=sum_l B(n,l)e(l)+sum_l A(n,l)wgnold(l), then residuals are clamped to [-1,1] at lines 97-98. |
| 1:3.4.2 | Definition A = M1*M0^-1 | $A=M_1*M_0^{-1}$ | A is the solved matrix, stored as the constant array. |
| 1:3.4.3 | Definition of B | $B*B^T=M_0-M_1*M_0^{-1}*M_1^T$ | B is the solved lower-triangular matrix, stored as the constant array. |
| 1:3.4.4 | Lag-0 matrix M0 (generic) | $M_0=\left[\begin{array}{ccc} 1 & \rho_0(1,2) & \rho_0(1,3) \\ \rho_0(1,2) & 1 & \rho_0(2,3) \\ \rho_0(1,3) & \rho_0(2,3) & 1 \end {array} \right ]$ | Generic M0; only its solved product enters the code. |
| 1:3.4.5 | Lag-1 matrix M1 (generic) | $M_1=\left[\begin{array}{ccc} \rho_1(1,1) & \rho_1(1,2) & \rho_0(1,3) \\ \rho_1(2,1) & \rho_1(2,2) & \rho_1(2,3) \\ \rho_1(3,1) & \rho_1(3,2) & \rho_1(3,3) \end {array} \right ]$ | Generic M1; only its solved product enters the code. |
| 1:3.4.6 | Numeric M0 | $M_0=\left[\begin{array}{ccc} 1.000 & 0.633 & 0.186 \\ 0.633 & 1.000 & -0.193 \\ 0.186 & -0.193 & 1.000 \end {array} \right ]$ | Verified against SWAT+ 62.0.0 (cli_weatgn.f90:66). theory's M₀ correlation matrix (0.633/0.186/-0.193) pre-solved offline into hardcoded A/B matrices; M₀ itself not in code |
| 1:3.4.7 | Numeric M1 | $M_1=\left[\begin{array}{ccc} 0.621 & 0.445 & 0.087 \\ 0.563 & 0.674 & -0.100 \\ 0.015 & -0.091 & 0.251 \end {array} \right ]$ | WGEN numeric M1; basis for hard-coded A and B. |
| 1:3.4.8 | Numeric A matrix | $A=\left[\begin{array}{ccc} 0.567 & 0.086 & -0.002 \\ 0.253 & 0.504 & -0.050 \\ -0.006 & -0.039 & 0.244 \end {array} \right ]$ | a = Reshape((/.567,.253,-.006,.086,.504,-.039,-.002,-.050,.244/)) matches published A. |
| 1:3.4.9 | Numeric B matrix | $B=\left[\begin{array}{ccc} 0.781 & 0 & 0 \\ 0.328 & 0.637 & 0 \\ 0.238 & -0.341 & 0.873 \end {array} \right ]$ | b = Reshape((/.781,.328,.238,0.,.637,-.341,0.,0.,.873/)) matches published B. |

## Lineage

Three resolved commits changed `cli_weatgn`. `df07e3f` added the routine with its purpose text, input/output comments, hard-coded A and B matrices, random draws, residual recursion, and the `wgncur`/`wgnold` update loop. `c7c8e22` brought in the same source as later upstream code and preserved that algorithm. `39fabde` only initialized local scalars and arrays (`zshape`, `n`, `l`, `a`, `b`, `xx`, `e`, `v2`) to zero and did not change the procedure logic.

- df07e3f introduced the full weather-generator residual update: three uniform draws, Box-Muller-style normal generation via `cli_dstn1`, matrix-based recursion, and clamping/history storage.
- 39fabde changed only local initialization defaults, which affects startup safety but not the weather-generator algorithm.
- c7c8e22 preserved the imported upstream implementation of `cli_weatgn` with the same control flow and residual update behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_weatgn' has no extracted documentation comment.
