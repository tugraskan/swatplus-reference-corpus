---
kind: procedure
symbol: ero_ysed
title: ero_ysed
status: filled
source_hash: adcb38445717b483
version_label: SWAT+ 62.0.0
locals:
  j: Local copy of the active HRU index ihru.
  rock: Local coarse-fragment attenuation factor computed from surface-soil rock percentage
    but unused by the active sediment-yield path.
uses:
  hru_module: Supplies the hydrologic and HRU state needed by the erosion equations and receives
    the updated sediment-yield and USLE outputs.
  soil_module: Supplies the coarse-fragment percentage used to form the inactive rock attenuation
    term.
  erosion_module: Receives the daily erosion diagnostics accumulated by the routine.
  climate_module: Supplies precipitation for the daily erosion diagnostics written to ero_output.
---

<!-- facts:header -->

ero_ysed computes HRU sediment yield with the active MUSLE form, applies snow-cover protection, and computes a USLE comparison value for erosion diagnostics.

## Bottom Line

ero_ysed is the direct implementation target for the Chapter 4 USLE and Snow Cover Effects pages because it computes daily sediment yield, applies the snow-cover attenuation branch, and stores the comparison USLE value in module state.

The coarse-fragment factor appears only as a local variable rock in the active source and is not used by the live sediment-yield equation; the only uses are in commented-out alternative lines.

## Arguments

<!-- facts:arguments -->

## Where It Fits

surface calls ero_ysed immediately after ero_cfactor when runoff and peak runoff are both nontrivial. A wetland flush uses the same ero_cfactor and cklsp ingredients, but computes wetland sediment directly in wetland_control instead of calling ero_ysed.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Build the combined support-practice multiplier | Forms cklsp(j) = usle_cfac(j) * hru(j)%lumv%usle_mult and computes the local coarse-fragment factor rock. |
| Compute active MUSLE sediment yield | Uses (10. * surfq(j) * qp_cms * hru(j)%area_ha) ** .56 * cklsp(j) for sedyld(j) and clips negative results to zero. |
| Apply snow-cover protection | Leaves near-zero yields at zero, otherwise zeroes yield for deep snow and attenuates yield by Exp(hru(j)%sno_mm * 3. / 25.4) for partial snow cover. |
| Compute USLE comparison value | Stores a comparison USLE value with usle = 1.292 * usle_ei * cklsp(j) / 11.8. |
| Write erosion diagnostics | Publishes sediment yield, precipitation, surface runoff, and peak runoff into ero_output(j)%ero_d and accumulates ero_ave. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru; usle_cfac; cklsp; surfq; sedyld; usle; ihru; qp_cms; usle_ei` | `HRU area, runoff, snow depth, cover factor, routing factors, and erosion outputs` |
| [sym:soil_module] | `soil` | `phys(1)%rock` |
| [sym:erosion_module] | `ero_output` | `ero_d%sedyld, ero_d%precip, ero_d%surfq, ero_d%peak, ero_ave, n_events` |
| [sym:climate_module] | `w` | `precip` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cklsp(j)` | Every call | Stores the product of the current cover-management factor and usle_mult for downstream erosion calculations. |
| `sedyld(j)` | Every call | Stores the active HRU's daily sediment yield after MUSLE and any snow-cover adjustment. |
| `usle` | Every call | Stores the comparison USLE soil-loss estimate (usle = 1.292 * usle_ei * cklsp(j) / 11.8) written to output for comparison with the active MUSLE sediment yield. |
| `ero_output(j)%ero_d%sedyld; ero_output(j)%ero_d%precip; ero_output(j)%ero_d%surfq; ero_output(j)%ero_d%peak; ero_output(j)%ero_ave` | Every call | Updates the daily erosion diagnostics and cumulative erosion-average accumulator. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
| 4:1.2.1 |  | $sed=1.292*EI_{USLE}*K_{USLE}*C_{USLE}*P_{USLE}*LS_{USLE}*CFRG$ | Verified against SWAT+ 62.0.0 (ero_ysed.f90:81). (1.292 MUSLE, cklsp=K*C*P*LS) |

## Lineage

`ero_ysed.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ero_ysed.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `530b045` (2026-02-18) — Refactor usle import and variable initialization
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- rock = Exp(-.053 * soil(j)%phys(1)%rock) is computed at ero_ysed.f90:52, but the only uses of rock are inside commented-out alternative lines 58-60; the active sedyld(j) expression at line 55 does not include it.
- The active caller chain for the HRU path is surface.f90:77-79: ero_cfactor runs first, then ero_ysed consumes usle_cfac(j).
- Wetland flushing uses the same usle_cfac and cklsp ingredients in wetland_control.f90:227-235, but it does not call ero_ysed.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up; entry 1 carries no theory equation id, so there is nothing to look up.
