---
kind: procedure
symbol: pest_lch
title: pest_lch
status: filled
source_hash: fb60d86a48b10f41
version_label: SWAT+ 62.0.0
uses:
  hru_module: Provides the pathway flows and drain-layer control used by soluble pesticide
    routing.
  constituent_mass_module: Stores per-layer pesticide mass and is updated as pesticide is
    removed or transferred downward.
  output_ls_pesticide_module: Receives the daily soluble pesticide loads for each transport
    pathway.
---

<!-- facts:header -->

pest_lch computes soluble pesticide transport in surface runoff, lateral flow, tile flow, and percolation through the soil profile.

## Bottom Line

pest_lch is the direct implementation target for the Chapter 4 Movement of Soluble Pesticide page because it computes soluble pesticide losses to surface runoff, lateral flow, tile flow, and percolation for each soil layer and each pesticide.

The routine also updates each soil-layer pesticide store as mass is removed or transferred to the next layer.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls pest_lch immediately after pesticide degradation and before the total-soil-pesticide summary, so dissolved pesticide movement is resolved before sediment-bound pesticide export is considered later in the runoff-event block.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Initialize daily pathway outputs | Zeros daily percolation, surface-runoff, and lateral-flow outputs for each pesticide before layer routing begins. |
| Build sorption and flow terms per layer | For each layer and pesticide, computes kd, zdb1, pathway flow volume vf, dissolved mass xx, dissolved concentration co, and the surface-runoff-adjusted concentration csurf. |
| Route surface runoff, tile flow, and lateral flow losses | Computes pesticide removed to surface runoff from layer 1, to tile flow from the drain layer, and to lateral flow from every layer, subtracting each mass from the soil-layer store. |
| Route percolation to the next layer or out of profile | Computes percolation loss xx from each layer, subtracts it from the source layer, and either adds it to the next layer or records it as hpestb_d(j)%pest(k)%perc at the bottom layer. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru; surfq; qtile; ihru` | `surface runoff, tile flow, active HRU id, and drain-layer metadata` |
| [sym:constituent_mass_module] | `cs_soil` | `ly(:)%pest(:)` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `surq, latq, tileq, perc` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpestb_d(j)%pest(k)%surq; hpestb_d(j)%pest(k)%latq; hpestb_d(j)%pest(k)%tileq; hpestb_d(j)%pest(k)%perc` | Every call | Stores soluble pesticide loads leaving the HRU via surface runoff, lateral flow, tile flow, and bottom-of-profile percolation. |
| `cs_soil(j)%ly(:)%pest(:)` | Every call | Updates soil-layer pesticide stores after dissolved losses and downward transfers between layers. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
| 4:3.2.1 |  | $\frac{dpst_{s,ly}}{dt}=0.01*C_{solution}*w_{mobile}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:55). soluble-pest flux = co·w_mobile |
| 4:3.2.10 |  | $conc_{pst,flow}=min{[pst_{flow}/[w_{perc,surf}+\beta_{pst}(Q_{surf}+Q_{lat,surf})]], pst_{sol}/100}.$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:58). csurf = percop * co` — β_pst applied to surface conc |
| 4:3.2.11 |  | $conc_{pst,flow}=min[{[pst_{flow}/w_{mobile}],}pst_{sol}/100.]$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:56). co = xx/vf`, capped `Min(solub/100., co)` (:57) |
| 4:3.2.12 |  | $pst_{perc,ly}=conc_{pst,flow}*w_{perc,ly}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:87). xx = co*prk` — percolation |
| 4:3.2.13 |  | $pst_{lat,surf}=\beta_{pst}*conc_{pst,flow}*Q_{lat,surf}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:78). yy = csurf*flat` (layer 1 uses surface conc) |
| 4:3.2.14 |  | $pst_{lat,ly}=conc_{pst,flow}*Q_{lat,ly}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:80). yy = co*flat` (deeper layers) |
| 4:3.2.15 |  | $pst_{surf}=\beta_{pst}*conc_{pst,flow}*Q_{surf}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:62). yy = csurf*surfq(j) |
| 4:3.2.2 |  | $w_{mobile}=Q_{surf}+Q_{lat,surf}+w_{perc,surf}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:49). vf = prk + flat`, `+surfq` if ly==1 (:50) |
| 4:3.2.3 |  | $w_{mobile}=Q_{lat,ly}+w_{perc,ly}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:49). same line, deeper-layer form |
| 4:3.2.4 |  | $pst_{s,ly}=0.01*(C_{solution}*SAT_{ly}+C_{solidphase}*\rho_b*depth_{ly})$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:45). mass partition (zdb1) |
| 4:3.2.5 |  | $pst_{s,ly}=0.01*(C_{solution}*SAT_{ly}+C_{solution}*K_p*\rho_b*depth_{ly})$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:45). partition with C_solid=Kp·C_sol |
| 4:3.2.6 |  | $C_{solution}=\frac{pst_{s,ly}}{0.01*(SAT_{ly}+K_p*\rho_b*depth_{ly})}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:45). zdb1 = ul + kd·bd·thick` = 0.01·(SAT+Kp·ρb·depth) partition; C_sol=pest/zdb1 |
| 4:3.2.7 |  | $\frac{dpst_{s,ly}}{dt}=\frac{pst_{s,ly}*w_{mobile}}{(SAT_{ly}+K_p*\rho_b*depth_{ly})}$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:55). rate form of the zdb1 exponential |
| 4:3.2.8 |  | $pst_{s,ly,t}=pst_{s,ly,o}*exp[\frac{-w_{mobile}}{(SAT_{ly}+K_p*\rho_b*depth_{ly})}]$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:55). remaining pest `= pest·Exp(-vf/zdb1)`; leached `(1-Exp)` at :55 |
| 4:3.2.9 |  | $pst_{flow}=pst_{s,ly,o}*(1-exp[\frac{-w_{mobile}}{(SAT_{ly}+K_p*\rho_b*depth_{ly})}])$ | Verified against SWAT+ 62.0.0 (pest_lch.f90:55). (pesticide leach 1-exp) |

## Lineage

`pest_lch.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `4d173cc` (2025-04-17, "merge"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pest_lch.f90` are listed.

- `4d173cc` (2025-04-17) — merge
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `2405a68` (2024-07-16) — Fixing for Compiling
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The routine writes tile-flow pesticide to hpestb_d(j)%pest(k)%tileq even though only surq, latq, and perc are explicitly zeroed at initialization in this body.
- The first layer uses csurf for lateral transport, while deeper layers use the dissolved concentration co directly.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up.
