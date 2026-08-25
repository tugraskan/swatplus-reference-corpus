---
kind: procedure
symbol: hydro_init
title: hydro_init
status: filled
source_hash: f5dd094768f93d38
version_label: SWAT+ 62.0.0
uses:
  hru_module: Receives the composite factor later multiplied by usle_cfac in erosion calculations.
---

<!-- facts:header -->

hydro_init assembles the composite USLE multiplier from stored rock, K, P, and LS factors for each HRU.

## Bottom Line

hydro_init is a supporting implementation target for the Chapter 4 soil-erodibility and topographic-factor pages because it combines stored erosion factors into hru(j)%lumv%usle_mult before event sediment calculations run.

The routine does not derive the underlying equations itself; it composes already prepared factor state for downstream erosion use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hydro_init runs during HRU initialization after the component erosion factors exist, composing the usle_mult state later consumed by ero_ysed and wetland sediment-yield calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Build the composite USLE multiplier | Computes rock = Exp(-.053 * soil(j)%phys(1)%rock) and multiplies rock, usle_k, usle_p, and usle_ls by 11.8 to populate hru(j)%lumv%usle_mult. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru(:)%lumv%usle_mult` | `composite erosion-factor multiplier` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(j)%lumv%usle_mult` | During hydrologic initialization | Stores the composite erosion-factor multiplier consumed later when cklsp(j) is formed in erosion routines. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
| 2:3.5.10 |  | $Q_{lat}=(Q'_{lat}+Q_{latstor,i-1})*(1-exp[\frac{-1}{TT_{lag}}])$ | Verified against SWAT+ 62.0.0 (hydro_init.f90:142). lat_ttime = 1.-Exp(-1./xx)` — lateral lag factor |
| 2:3.5.11 |  | $TT_{lag}=\frac{tile_{lag}}{24}$ | Verified against SWAT+ 62.0.0 (hydro_init.f90:147). tile lag `tile_ttime = 1.-Exp(-24./sdr%lag) |
| 2:3.5.12 |  | $TT_{lag}=10.4*\frac{L_{hill}}{K_{sat,mx}}$ | Verified against SWAT+ 62.0.0 (hydro_init.f90:140). xx = 10.4*lat_len/scmx` — TT_lag=10.4·L_hill/K_sat,mx |
| 4:2.5.2 |  | $NO3_{lat}=(NO3'_{lat}+NO3_{latstor,i-1})*(1-exp[\frac{-1}{TT_{lat}}])$ | Verified against SWAT+ 62.0.0 (hydro_init.f90:142). NO3 lateral lag factor = lat_ttime (1−exp(−1/TT_lat)); NO3 rides lagged latq |
| 4:3.4.2 |  | $pst_{lat}=(pst'_{lat}+pst_{latstor,i-1})*(1-exp[\frac{-1}{TT_{lat}}])$ | Verified against SWAT+ 62.0.0 (hydro_init.f90:142). pesticide lateral lag (same lat_ttime factor) |

## Lineage

`hydro_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `e18817a` (2024-10-08, "Refactor and enhance various modules and subroutines"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hydro_init.f90` are listed.

- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- This overlay is supporting because the routine composes factors into usle_mult rather than computing the underlying K or LS equations themselves.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up; entry 1 carries no theory equation id, so there is nothing to look up.
