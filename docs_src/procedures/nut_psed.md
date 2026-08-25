---
kind: procedure
symbol: nut_psed
title: nut_psed
status: filled
source_hash: 636b42a5bb718ba4
version_label: SWAT+ 62.0.0
uses:
  hru_module: Provides the erosion controls and receives the computed organic and mineral
    phosphorus exports.
  organic_mineral_mass_module: Provides the attached-sediment phosphorus source pools and
    is updated to remove the exported mass.
  soil_module: Supplies the first-layer bulk density and depth needed to compute soil mass
    wt1.
---

<!-- facts:header -->

nut_psed computes organic and mineral phosphorus exported with sediment in surface runoff and removes that mass from first-layer soil pools.

## Bottom Line

nut_psed is the direct implementation target for the Chapter 4 Organic and Mineral P Attached to Sediment in Surface Runoff page because it partitions sediment-bound phosphorus into organic, active mineral, and stable mineral components and exports them as surface-runoff sediment loads.

The routine then deducts those exported masses from the first-layer mineral, humus, and manure phosphorus pools.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls nut_psed in the same runoff-event nutrient block as nut_orgn, after sediment and pesticide enrichment are available and before the general phosphorus-movement routine nut_solp runs later in the HRU day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Assemble attached phosphorus composition | Forms sedp_attach from first-layer organic and mineral P pools and computes the fractions fr_orgp, fr_actmin, and fr_stamin. |
| Compute total sediment-bound P export | Computes the first-layer soil mass wt1, chooses the enrichment ratio, builds frac = sedp_attach * er / wt1, and converts that to the total exported sediment-bound P mass sedp. |
| Partition export into organic and mineral components | Assigns sedorgp(j), sedminpa(j), and sedminps(j) from sedp using the attached-P fractions, limits mineral exports to the available pools, and subtracts them from the first-layer mineral P pools. |
| Remove organic P from humus and manure pools | Splits the organic sediment-bound P export across the humus and manure pools, limits each removal to the available pool mass, and subtracts the exported amounts. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru; sedyld; sedorgp; sedminpa; sedminps; ihru; enratio` | `HRU hydrologic controls, sediment yield, event enrichment ratio, and sediment-bound P outputs` |
| [sym:organic_mineral_mass_module] | `soil1` | `first-layer organic and mineral phosphorus pools` |
| [sym:soil_module] | `soil` | `phys(1)%bd, phys(1)%d` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sedorgp(j); sedminpa(j); sedminps(j)` | When sedp > 1.e-9 | Stores the organic, active mineral, and stable mineral phosphorus exported with sediment in surface runoff. |
| `soil1(j)%mp(1)%act; soil1(j)%mp(1)%sta; soil1(j)%hsta(1)%p; soil1(j)%man(1)%p` | When sedp > 1.e-9 | Reduces the first-layer mineral and organic phosphorus pools to reflect the exported sediment-bound phosphorus mass. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
| 4:2.4.1 |  | $sedP_{surf}=0.001*conc_{sedP}*\frac{sed}{area_{hru}}*\varepsilon_{P:sed}$ | Verified against SWAT+ 62.0.0 (nut_psed.f90). (sediment-P transport) |
| 4:2.4.2 |  | $conc_{sedP}=100*\frac{(minP_{act,surf}+minP_{sta,surf}+orgP_{hum,surf}+orgP_{frsh,surf})}{\rho_b*depth_{surf}}$ | Verified against SWAT+ 62.0.0 (nut_psed.f90). same structure for P |
| 4:2.5.5 |  | $sedP_{surf}=(sedP'_{surf}+sedP_{stor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (nut_psed.f90). |

## Lineage

`nut_psed.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `eb22103` (2024-12-05, "Refactor residue management to use new soil1 structure"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `nut_psed.f90` are listed.

- `eb22103` (2024-12-05) — Refactor residue management to use new soil1 structure
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The source duplicates soil1(j)%man(1)%p in the attached-P and organic-P sums at lines 56 and 58; the overlay records the active implementation rather than correcting it.
- The routine zeros the sediment-bound P outputs when sedp is negligible.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up.
