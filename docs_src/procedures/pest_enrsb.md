---
kind: procedure
symbol: pest_enrsb
title: pest_enrsb
status: filled
source_hash: 0b4133536224d130
version_label: SWAT+ 62.0.0
uses:
  hru_module: Receives the computed enrichment ratio and also has small sediment events zeroed
    before the ratio calculation proceeds.
---

<!-- facts:header -->

pest_enrsb computes the event enrichment ratio used by nutrient, pesticide, and pathogen sediment-transport routines.

## Bottom Line

pest_enrsb is the direct implementation target for the Chapter 4 Enrichment Ratio page because it computes enratio from event sediment yield, HRU area, and runoff using the documented CREAMS-style formula.

The resulting enratio is then consumed downstream by nutrient, pesticide, and pathogen transport routines rather than applied further inside pest_enrsb itself.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls pest_enrsb inside the runoff-event block before pest_pesty, nut_orgn, nut_psed, and the pathogen runoff routine later consumes enratio in the same HRU day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Zero negligible sediment events | If sedyld(j) is below 1.e-4, zeroes sediment yield and the particle-size yield partitions before enrichment is computed. |
| Compute the CREAMS enrichment ratio | Computes cy = 0.1 * sedyld(j) / (hru(j)%area_ha * surfq(j) + 1.e-6), derives enratio = 0.78 * cy ** (-0.2468) when cy is positive, and caps enratio at 3.0. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `enratio; sedyld; sanyld; silyld; clayld; sagyld; lagyld` | `event enrichment ratio and sediment/yield partitions` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `enratio` | Every runoff-event call | Stores the event enrichment ratio used later by nutrient, pesticide, and pathogen sediment-transport routines. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |

## Lineage

`pest_enrsb.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `4d173cc` (2025-04-17, "merge"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pest_enrsb.f90` are listed.

- `4d173cc` (2025-04-17) — merge
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The exported equation-id range crosses topic boundaries, but the actual enrichment-ratio calculation itself is direct and localized in this routine.
- Downstream consumers include nut_orgn, nut_psed, pest_pesty, and path_ls_runoff.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up.
