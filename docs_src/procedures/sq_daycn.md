---
kind: procedure
symbol: sq_daycn
title: sq_daycn
status: filled
source_hash: 8e2c01cc81d2d63e
version_label: SWAT+ 62.0.0
locals:
  bb: Temporary threshold depth equal to 0.2 times the curve-number retention parameter `r2`;
    it is subtracted from `precip_eff` to form `pb` before runoff is computed.
  cnimp: Temporary impervious-area curve number, fixed to 98 for the urban runoff calculation
    branch.
  j: Current HRU index copied from `ihru` so the routine can read and write the matching entries
    in `cnday` and `surfq`.
  pb: Effective precipitation remaining after initial abstraction (`precip_eff - bb`); if
    it is positive, runoff is computed.
  r2: Curve-number retention parameter `S` derived from `cnday(j)` for the pervious branch,
    then recomputed from `cnimp` for the impervious branch.
  surfqimp: Temporary runoff depth calculated for the impervious portion of an urban HRU before
    it is blended into `surfq(j)`.
  ulu: Urban-land-use database index taken from `hru(j)%luse%urb_lu` so the routine can fetch
    the connected impervious fraction from `urbdb`.
uses:
  urban_data_module: '`urbdb(ulu)%fcimp` provides the directly connected impervious fraction
    for the HRU''s urban land-use class. That fraction is what lets the routine blend normal
    HRU runoff with impervious runoff instead of treating the whole HRU as pervious.'
  hru_module: '`hru(j)%luse%urb_lu` tells the routine whether the current HRU is urban and,
    if so, which urban database record to use. Without `hru_module`, the routine would not
    know whether to execute the impervious blending branch or which `urbdb` entry to consult.'
---

<!-- facts:header -->

Computes daily surface runoff for the current HRU using an SCS curve number method. If the HRU is urban, it blends the normal HRU runoff with impervious-area runoff using the connected impervious fraction.

## Bottom Line

sq_daycn calculates daily runoff depth for the active HRU from effective precipitation and the current curve number. It first computes runoff for the HRU's normal curve number, then, if the HRU is urban, recomputes runoff for an impervious curve number of 98 and mixes the two results by the directly connected impervious fraction from `urbdb`.

The routine does not take arguments; it relies on `ihru`, `precip_eff`, `cnday`, `hru(j)%luse%urb_lu`, and `urbdb(ulu)%fcimp` from module state. Its output is the updated `surfq(j)`, which is the daily surface runoff used later in the HRU water balance and channel routing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `sq_volq`, which chooses `sq_daycn` when the basin is not using the Green-Ampt option (`bsn_cc%gampt == 0`). `sq_volq` has already set up the daily runoff calculation context, including the current HRU index and effective precipitation, and the `surfq(j)` value produced here is later used as the day's HRU surface runoff in downstream water-balance and routing calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set HRU index | Copy the active HRU number from `ihru` into local index `j` so all reads and writes target the current HRU. |
| 2. compute pervious retention | Derive the SCS retention parameter from `cnday(j)`, compute the initial abstraction threshold `bb = 0.2*r2`, and form `pb = precip_eff - bb`. |
| 3. compute pervious runoff | Initialize `surfq(j)` to zero, then compute SCS runoff only when `pb > 0`, using the daily effective precipitation and retention parameter. |
| 4. check urban land use | Test whether the HRU has an urban land-use class (`hru(j)%luse%urb_lu > 0`) and, only then, apply the impervious-area adjustment. |
| 5. compute impervious runoff | Set impervious runoff to zero, assign `cnimp = 98`, recompute `r2`, `bb`, and `pb`, and calculate runoff for the impervious portion when `pb > 0`. |
| 6. blend urban runoff | Fetch the urban database index `ulu` and replace `surfq(j)` with a weighted mix of pervious and impervious runoff using `urbdb(ulu)%fcimp`. |
| 7. return | Exit after leaving the final runoff depth in `surfq(j)` for later HRU water-balance and routing use. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:urban_data_module] | `urbdb` | `urbdb(ulu)%fcimp` |
| [sym:hru_module] | `hru, cnday, surfq, ihru, precip_eff` | `hru(j)%luse%urb_lu` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `surfq(j)` | Always sets `surfq(j)`, with an additional urban blending update when `hru(j)%luse%urb_lu > 0`. | `surfq(j)` is overwritten with the day’s computed surface runoff depth for the active HRU. For urban HRUs, the stored value changes again to include the impervious-area contribution weighted by `urbdb(ulu)%fcimp`. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:1.1.1 | SCS runoff equation | $Q_{surf}=\frac{(R_{day}-I_a)^2}{(R_{day}-I_a+S)}$ | Computes runoff only when precipitation exceeds initial abstraction threshold. |
| 2:1.1.2 | Retention parameter from curve number | $S=25.4(\frac{1000}{CN}-10)$ | r2 = 25400/cnday - 254 is the standard S = 25.4*(1000/CN - 10) form in mm. |
| 2:1.1.3 | SCS runoff with Ia = 0.2S | $Q_{surf}=\frac{(R_{day}-0.2S)^2}{(R_{day}+0.8S)}$ | surfq = (Rday - 0.2*S)^2 / (Rday + 0.8*S) with the branch guarded by precip > 0.2*S. |

## Lineage

Three resolved commits changed `sq_daycn`. `df07e3f` introduced the subroutine with the SCS runoff calculation and urban impervious blending. `94b6dec` brought in the same source from Bitbucket without changing the algorithm. `39fabde` only initialized local variables (`bb`, `cnimp`, `j`, `pb`, `r2`, `surfqimp`, `ulu`) at declaration time.

- df07e3f added the complete `sq_daycn` routine: per-HRU SCS runoff from `cnday(j)` and `precip_eff`, plus urban blending with `urbdb(ulu)%fcimp` when `hru(j)%luse%urb_lu > 0`.
- 39fabde changed only initialization style for local variables, assigning default zero values at declaration; the runoff logic and branching remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_daycn' has no extracted documentation comment.
