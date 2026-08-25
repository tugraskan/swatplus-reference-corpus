---
kind: procedure
symbol: sq_dailycn
title: sq_dailycn
status: filled
source_hash: f4e61a613a811138
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from ihru so the routine can read and update the current HRU's entries
    in wrt, smx, soil, and cnday.
  r2: Working retention parameter for the curve-number equation. It is computed from soil
    water, optionally adjusted for frozen soil, bounded to a minimum of 3., and then converted
    to cnday.
  sw_fac: Intermediate exponent argument built from the two wrt shape parameters and soil(j)%sw.
    It is clipped to keep Exp(sw_fac) numerically safe before the retention equation uses
    it.
uses:
  basin_module: basin_module provides bsn_prm%cn_froz, the frozen-soil adjustment coefficient.
    sq_dailycn uses it when soil(j)%phys(2)%tmp is at or below freezing to reduce infiltration
    capacity and raise the effective curve number.
  hru_module: 'hru_module holds the current-HRU state and outputs that drive this calculation:
    ihru selects the active HRU, wrt supplies the retention shape parameters, smx provides
    the maximum retention coefficient, and cnday is the daily result written back for later
    runoff use.'
  soil_module: soil_module provides the soil water state and temperature for the active HRU.
    soil(j)%sw controls the moisture-based retention calculation, and soil(j)%phys(2)%tmp
    determines whether the frozen-soil adjustment is applied.
---

<!-- facts:header -->

Computes the daily curve number for the current HRU from soil water, retention parameters, and frozen-soil adjustment.

## Bottom Line

sq_dailycn calculates the current-day curve number for the active HRU. It takes the HRU index from hru_module%ihru, uses the soil water state and retention coefficients to form a daily retention value, applies a frozen-soil adjustment when the second soil layer is at or below freezing, and stores the resulting curve number in cnday(j).

This routine sits just before runoff generation in surface. Its output is the daily curve number that later runoff calculations use, so it directly affects how much precipitation becomes surface flow for the HRU.

## Arguments

<!-- facts:arguments -->

## Where It Fits

surface calls sq_dailycn after setting j = ihru and before sq_volq computes runoff. That means sq_dailycn runs once per HRU, with the current HRU's soil and parameter state already prepared, and its cnday(j) result then feeds the runoff computation that follows in the same surface workflow.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. assign HRU index | Copy the current HRU number from ihru into local variable j so the routine can index HRU-specific soil, retention, and output arrays. |
| 2. compute soil-water factor | Form sw_fac from the two wrt shape parameters and the current HRU soil water, creating the exponent argument used in the retention equation. |
| 3. clamp low exponent | Limit sw_fac to -20. when it is too negative so Exp(sw_fac) does not underflow and destabilize the retention calculation. |
| 4. clamp high exponent | Limit sw_fac to 20. when it is too positive so Exp(sw_fac) stays numerically safe. |
| 5. compute retention from soil water | If soil water plus exp(sw_fac) is large enough, compute daily retention as smx(j) * (1. - soil(j)%sw / (soil(j)%sw + Exp(sw_fac))); otherwise fall back to the maximum retention smx(j). |
| 6. adjust for frozen soil | When the second soil-layer temperature is at or below freezing, convert the retention value with the basin frozen-soil coefficient using r2 = smx(j) * (1. - Exp(- bsn_prm%cn_froz * r2)). |
| 7. enforce minimum retention | Raise r2 to at least 3. so the curve-number conversion never uses an unrealistically small retention value. |
| 8. convert retention to curve number | Translate the final retention value into the daily curve number and store it in cnday(j) with the standard 25400. / (r2 + 254.) relationship. |
| 9. return to caller | Finish the HRU curve-number update and hand control back to surface, which uses cnday(j) in runoff generation. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%cn_froz` |
| [sym:hru_module] | `wrt, smx, cnday, ihru` |  |
| [sym:soil_module] | `soil` | `soil(j)%sw, soil(j)%phys(2)%tmp` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cnday(j)` | Whenever sq_dailycn runs for the current HRU, after r2 has been computed and bounded. | cnday(j) is updated to the current-day curve number for HRU j, derived from soil water retention and any frozen-soil adjustment. That value is the day-specific runoff control used by later surface runoff calculations. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:1.1.6 | Daily retention parameter from soil water | $S=S_{max}*(1-\frac{SW}{[SW+exp(w_1-w_2*SW)]})$ | Uses S = Smax*(1 - SW/(SW + exp(w1 - w2*SW))) after bounding the exponent argument. |
| 2:1.1.9 | Antecedent/PET retention update | $S=S_{prev}+E_o *exp(\frac{-cncoef*S_{prev}}{S_{max}})-R_{day}+Q_{surf}$ | Current code recomputes retention directly from soil water each day rather than updating S from the previous day with PET, rainfall, and runoff. |
| 2:1.1.10 | Frozen-soil retention adjustment | $S_{frz}=S_{max}*[1-exp(-0.000862*S)]$ | r2 = smx*(1 - exp(-cn_froz*r2)) with cn_froz default 0.000862. |
| 2:1.1.11 | Daily curve number from retention | $CN=\frac{25400}{(S+254)}$ | cnday = 25400/(r2 + 254). |

## Lineage

Three resolved commits changed sq_dailycn. df07e3f added the new subroutine with the daily curve-number calculation, soil-water retention equation, frozen-soil adjustment, and cnday output. 94b6dec updated the imported source but did not change the sq_dailycn logic itself in the shown diff. 39fabde initialized the local variables j, r2, and sw_fac with default values, leaving the algorithm unchanged.

- df07e3f introduced sq_dailycn and implemented the daily retention-to-curve-number workflow, including the soil-moisture equation, frozen-soil modification, and cnday assignment.
- 39fabde changed only local variable initialization for j, r2, and sw_fac; the computation of cnday(j) remained the same in the diff shown.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sq_dailycn' has no extracted documentation comment.
