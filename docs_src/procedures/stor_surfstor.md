---
kind: procedure
symbol: stor_surfstor
title: stor_surfstor
status: filled
source_hash: 051faa0209a7e118
version_label: SWAT+ 62.0.0
uses:
  hru_module: Provides the stored and routed sediment state that defines the surface-runoff
    lag implementation.
  time_module: Selects the daily versus subdaily routing branch.
---

<!-- facts:header -->

stor_surfstor stores one-day surface-runoff lag pools and releases the routed fraction for sediment and other surface constituents.

## Bottom Line

stor_surfstor is the direct implementation target for Chapter 4 sediment lag in surface runoff because it explicitly accumulates sedyld(j) into surf_bs(2,j), releases the routed fraction with rt(j), and carries the remainder forward.

The same routine also lags surface-runoff nutrient constituent pools, so it forms the surface half of the distributed Chapter 4 nutrient-lag mapping alongside swr_substor.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls stor_surfstor after swr_latsed and before swr_substor, so surface sediment lag is applied before subsurface lag routing and before edge-of-field filtering.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Daily sediment lag routing | For daily steps, adds sedyld(j) into surf_bs(2,j), routes surf_bs(2,j) * brt(j) to sedyld(j), and retains the remainder in surf_bs(2,j). |
| Subdaily sediment lag routing | For subdaily steps, iterates through hhsurf_bs(2,j,k) and hhsedy(j,k), routing each step's sediment fraction with rt(j) and summing the routed sediment back into daily sedyld(j). |
| Release stored surface constituents | Applies the same rt(j) fraction to lagged nutrient and constituent pools stored in surf_bs. |
| Remove delivered loads from storage | Subtracts the routed sediment and constituent deliveries from the corresponding surf_bs storage buckets so the remainder carries forward. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `sedyld; surf_bs; hhsurf_bs; hhsedy; brt` | `surface sediment yield, lag buckets, subdaily lag buckets, subdaily routed sediment, and routing fraction` |
| [sym:time_module] | `time` | `step` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `surf_bs(2,j); sedyld(j)` | Daily timestep | Updates the surface sediment lag bucket and replaces sedyld(j) with the routed fraction delivered this step. |
| `hhsurf_bs(2,j,k); hhsedy(j,k); sedyld(j)` | Subdaily timestep | Routes subdaily sediment through the lag buckets and recomputes the daily total as the sum of routed subdaily deliveries. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
| 4:1.4.1 |  | $sed=(sed'+sed_{stor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (stor_surfstor.f90:98). sediment lag `sedyld = surf_bs(2,j)·brt(j)`; brt=1−exp(−surlag/tconc) |
| 4:2.5.3 |  | $orgN_{surf}=(orgN'_{surf}+orgN_{stor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (stor_surfstor.f90:98). orgN surface lag (same brt factor) |
| 4:2.5.4 |  | $P_{surf}=(P'_{surf}+P_{stor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (stor_surfstor.f90:98). solP surface lag (same brt factor) |
| 4:3.4.1 |  | $pst_{surf}=(pst'_{surf}+pst_{surstor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (stor_surfstor.f90:98). pesticide surface lag (same brt factor) |
| 4:3.4.3 |  | $pst_{sed}=(pst'_{sed}+pst_{sedstor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (stor_surfstor.f90:98). pesticide sediment lag (shared `brt` factor) |

## Lineage

`stor_surfstor.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `20c879b` (2025-10-14, "Added checks to sq_surfs.f90 and stor_surfstor.f90 to prevent gfortran underflow…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `stor_surfstor.f90` are listed.

- `20c879b` (2025-10-14) — Added checks to sq_surfs.f90 and stor_surfstor.f90 to prevent gfortran underflow errors.
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The sediment lag state is explicit in surf_bs(2,j), with rt(j) acting as the same-step delivery fraction and the remainder left in storage for the next call.
- This routine handles the surface-runoff side of the distributed nutrient-lag mapping, while swr_substor handles the lateral and tile nitrate side.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up; entry 1 carries no theory equation id, so there is nothing to look up.
