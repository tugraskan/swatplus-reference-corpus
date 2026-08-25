---
kind: procedure
symbol: swr_substor
title: swr_substor
status: filled
source_hash: 50c93a155dfc6d90
version_label: SWAT+ 62.0.0
uses:
  hru_module: Provides both the stored subsurface lag pools and the current-day loads that
    are accumulated and routed.
---

<!-- facts:header -->

swr_substor stores lagged lateral flow, tile flow, and their nitrate loads, then releases the routed fraction each step.

## Bottom Line

swr_substor is the subsurface half of the Chapter 4 nutrient-lag implementation because it stores lateral water, lateral nitrate, tile water, and tile nitrate in bss and releases them using travel-time fractions.

Although the source comments mention lat_pst, the active executable body does not store or release pesticide lag state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls swr_substor immediately after stor_surfstor, so subsurface water and nitrate lag are applied after the surface lag routing step.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Accumulate current-day subsurface loads | Adds lateral water, lateral nitrate, tile water, and tile nitrate into bss(1:4,j) and clips near-zero storage to zero. |
| Release the routed fraction | Recomputes latq(j), latno3(j), qtile, and tileno3(j) as travel-time fractions of the stored pools using lat_ttime and tile_ttime. |
| Retain the unreleased remainder | Subtracts the released lateral and tile loads from bss(1:4,j) so the remainder carries into the next step. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru; ihru; latq; latno3; qtile; bss; tileno3` | `active HRU state, lateral and tile water and nitrate loads, and subsurface lag buckets` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bss(1:4,j)` | Every call | Updates the subsurface lag pools to include new loads and retain the unreleased remainder. |
| `latq(j); latno3(j); qtile; tileno3(j)` | Every call | Overwrites the current-day lateral and tile water and nitrate loads with the routed fraction released from storage. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |

## Lineage

`swr_substor.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `swr_substor.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The executable body only lags water and nitrate in lateral and tile pathways. The lat_pst comment block is not matched by active pesticide storage code in this routine.
- This routine supports a distributed mapping for nutrient lag but does not provide source-backed support for pesticide lag on its own.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up.
