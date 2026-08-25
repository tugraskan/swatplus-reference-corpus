---
kind: procedure
symbol: pest_pesty
title: pest_pesty
status: filled
source_hash: 11405f0b165c7a6a
version_label: SWAT+ 62.0.0
uses:
  hru_module: Provides the sediment transport driver and enrichment control used to scale
    sorbed pesticide export.
  constituent_mass_module: Stores first-layer pesticide mass and is reduced by the exported
    sorbed pesticide load.
  output_ls_pesticide_module: Receives the pesticide mass exported with suspended sediment
    for each pesticide.
---

<!-- facts:header -->

pest_pesty computes pesticide transported with suspended sediment from the first soil layer during runoff events.

## Bottom Line

pest_pesty is the direct implementation target for the Chapter 4 Transport of Sorbed Pesticide page because it computes sediment-bound pesticide export from first-layer soil pesticide mass, sorption, enrichment ratio, and sediment yield.

The routine then subtracts the exported sorbed pesticide mass from the first-layer soil pesticide store.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls pest_pesty inside the runoff-event block after pest_enrsb has established enrichment support and only when sediment yield is positive, so this routine represents the sediment-bound pesticide export phase of the event.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Select first-layer pesticide mass and sorption terms | For each pesticide, loads first-layer soil pesticide mass, computes kd and zdb1, and converts the soil store into a sorbed pesticide concentration conc. |
| Choose the enrichment ratio | Uses hru(j)%hyd%erorgn when present, otherwise falls back to the event enrichment ratio enratio. |
| Compute sorbed pesticide export and update soil storage | Computes hpestb_d(j)%pest(k)%sed from sediment yield, sorbed concentration, enrichment ratio, and HRU area, then clamps it to available pesticide mass and subtracts it from the first-layer soil store. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru; sedyld; ihru; enratio` | `HRU hydrologic controls, sediment yield, and event enrichment ratio` |
| [sym:constituent_mass_module] | `cs_soil` | `ly(1)%pest(:)` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `sed` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpestb_d(j)%pest(k)%sed` | When first-layer pesticide mass is at least 0.0001 | Stores the pesticide mass exported with suspended sediment during the event. |
| `cs_soil(j)%ly(1)%pest(k)` | When sorbed export occurs | Reduces the first-layer soil pesticide store by the amount exported with suspended sediment. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
| 4:3.3.1 |  | $pst_{sed}=0.001*C_{solidphase}*\frac{sed}{area_{hru}}*\varepsilon_{pst:sed}$ | Verified against SWAT+ 62.0.0 (pest_pesty.f90). (sorbed pesticide w/ sediment) |
| 4:3.3.2 |  | $pst_{s,ly}=0.01*(C_{solution}*SAT_{ly}+C_{solidphase}*\rho_b*depth_{ly})$ | Verified against SWAT+ 62.0.0 (pest_pesty.f90:36). sorbed-phase partition zdb1; `conc=100·kd·pest/zdb1` (:38) |
| 4:3.3.3 |  | $pst_{s,ly}=0.01*(\frac{C_{solidphase}}{K_p}*SAT_{ly}+C_{solidphase}*\rho_b*depth_{ly})$ | Verified against SWAT+ 62.0.0 (pest_pesty.f90:36). same partition, C_solid/Kp form |
| 4:3.3.4 |  | $C_{solidphase}=\frac{100*K_p*pst_{s,ly}}{(SAT_{ly}+K_p*\rho_b*depth_{ly})}$ | Verified against SWAT+ 62.0.0 (pest_pesty.f90:38). conc = 100.*kd*pest_init/zdb1 |

## Lineage

`pest_pesty.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `4d173cc` (2025-04-17, "merge"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pest_pesty.f90` are listed.

- `4d173cc` (2025-04-17) — merge
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The routine reuses hru(j)%hyd%erorgn as the enrichment override for pesticides; otherwise it falls back to the shared event enrichment ratio enratio.
- Only the first soil layer participates in the sorbed-pesticide export calculation in this routine.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up.
