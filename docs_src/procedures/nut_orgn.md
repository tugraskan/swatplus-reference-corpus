---
kind: procedure
symbol: nut_orgn
title: nut_orgn
status: filled
source_hash: 2e8cebf16eb10b64
version_label: SWAT+ 62.0.0
uses:
  hru_module: Provides the erosion-event controls and receives the computed organic N load
    in surface runoff.
  organic_mineral_mass_module: Provides the first-layer organic N pools and is updated to
    remove the exported organic N mass.
  soil_module: Supplies the first-layer bulk density and depth needed to compute soil mass
    wt1.
---

<!-- facts:header -->

nut_orgn computes organic nitrogen removed with sediment in surface runoff and deducts it from the first soil-layer organic N pools.

## Bottom Line

nut_orgn is the direct implementation target for the Chapter 4 Organic N in Surface Runoff page because it computes sedorgn(j) from first-layer organic N, enrichment ratio, and sediment yield.

The routine also updates the active and stable first-layer organic N pools to reflect the exported load.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls nut_orgn inside the runoff-event nutrient block after sediment and pesticide enrichment have already been computed and before nut_psed handles sediment-bound phosphorus.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Assemble first-layer organic N mass and soil mass | Builds orgn_kgha from the first-layer stable and active organic N pools and computes wt1 from first-layer bulk density and depth. |
| Choose the enrichment ratio | Uses hru(j)%hyd%erorgn when present, otherwise falls back to the event enrichment ratio enratio. |
| Compute exported organic N | Computes frac = orgn_kgha * er / wt1 and then sets sedorgn(j) = 1000. * frac * sedyld(j) / hru(j)%area_ha. |
| Remove exported mass from soil pools | Subtracts the exported organic N from the first-layer active and stable organic N pools in proportion to their contribution and clips negative pool values back to zero. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru; sedorgn; sedyld; ihru; enratio` | `HRU hydrologic controls, event enrichment ratio, sediment yield, and organic N export output` |
| [sym:organic_mineral_mass_module] | `soil1` | `hsta(1)%n, hact(1)%n` |
| [sym:soil_module] | `soil` | `phys(1)%bd, phys(1)%d` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sedorgn(j)` | Every eligible runoff event | Stores the organic N load exported with surface-runoff sediment. |
| `soil1(j)%hact(1)%n; soil1(j)%hsta(1)%n` | When first-layer organic N is available | Reduces the first-layer active and stable organic N pools to reflect the exported organic N mass. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
| 3:2.1.5 | Unit conversion conc_P to kg/ha | $\frac{conc_P*\rho_b*depth_{ly}}{100}=\frac{kgP}{ha}$ | Verified against SWAT+ 62.0.0 (nut_orgn.f90:36). |
| 4:2.2.1 |  | $orgN_{surf}=0.001*conc_{orgN}*\frac{sed}{area_{hru}}*\varepsilon_{N:sed}$ | Verified against SWAT+ 62.0.0 (nut_orgn.f90). (org-N w/ sediment) |
| 4:2.2.2 |  | $conc_{orgN}=100*\frac{(orgN_{frsh,surf}+orgN_{sta,surf}+orgN_{act,surf})}{\rho_b*depth_{surf}}$ | Verified against SWAT+ 62.0.0 (nut_orgn.f90:44). frac = orgn_kgha*er/wt1`; `sedorgn = 1000*frac*sedyld/area` (:48) |

## Lineage

`nut_orgn.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `nut_orgn.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The routine is bypassed when the CSWAT pathway is active; hru_control instead calls nut_orgnc2 in that branch.
- The exported organic N load is tied directly to sediment yield, not dissolved runoff volume.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up.
