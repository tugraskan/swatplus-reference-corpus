---
kind: procedure
symbol: nut_orgnc
title: nut_orgnc
status: filled
source_hash: c0f0ea9a90fd661d
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; selects which HRU entry in `hru`, `soil1`, `pl_mass`, `soil`,
    and `pcom` is being updated.
  xx: Temporary sum of organic nitrogen available for export from the first soil layer and
    surface organic pools in the current HRU; used to compute concentration and to decide
    whether pool reductions are applied.
  wt1: Conversion factor derived from bulk density and layer depth for the top soil layer;
    used to convert the organic-N amount into a concentration basis before sediment export
    is computed.
  er: Enrichment ratio used in the sediment organic-N concentration calculation; taken from
    `hru(j)%hyd%erorgn` when defined, otherwise from the daily HRU enrichment ratio `enratio`.
  conc: Computed organic nitrogen concentration in soil material; multiplied by sediment yield
    to estimate organic N lost in runoff.
  xx1: Retained fraction of the original organic N pools after sediment loss is removed; applied
    as a multiplicative reduction to the affected pools when `xx` is large enough.
uses:
  organic_mineral_mass_module: '`organic_mineral_mass_module` owns the organic-mass pools
    that `nut_orgnc` reads and scales. The routine depends on `soil1(j)%hact(1)%n`, `soil1(j)%hsta(1)%n`,
    `soil1(j)%tot(1)%n`, `soil1(j)%man(1)%n`, and `pl_mass(j)%rsd_tot%n` to compute the available
    organic N and then updates `soil1(j)%tot(1)%n`, `soil1(j)%hact(1)%n`, `soil1(j)%hsta(1)%n`,
    `soil1(j)%man(1)%n`, and `pl_mass(j)%rsd(ipl)%n` after runoff removal.'
  hru_module: '`hru_module` supplies the current HRU index and hydrologic drivers needed to
    calculate runoff-associated organic N loss. `hru(j)%hyd%erorgn` controls the enrichment
    ratio choice, while `sedorgn(j)` is the HRU-level output written by this routine from
    sediment yield and area-based scaling.'
  soil_module: '`soil_module` provides the top-layer bulk density and depth used to build
    `wt1`, the conversion factor that turns the organic-N mass sum into a concentration before
    sediment export is computed.'
  plant_module: '`plant_module` provides `pcom(j)%npl`, the number of plants in the community,
    which determines how many residue pools in `pl_mass(j)%rsd(ipl)%n` must be reduced to
    reflect the exported organic N.'
---

<!-- facts:header -->

Calculates organic nitrogen lost from the HRU in surface runoff and applies a matching reduction to first-layer organic N pools.

## Bottom Line

`nut_orgnc` estimates the organic nitrogen concentration associated with eroded sediment for the current HRU, using the HRU-specific organic N enrichment ratio when present and otherwise the daily HRU enrichment ratio. It converts that concentration into an organic N sediment load, `sedorgn(j)`, scaled by sediment yield and HRU area.

If there is enough organic N in the first soil layer to matter, the routine then reduces the first-layer total organic pool and the active humus, stable humus, residue, and manure nitrogen pools by the same proportional loss. This keeps the sediment export and the remaining soil/plant organic pools consistent after a runoff event.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the HRU runoff/sediment calculation after the current HRU index `ihru` and sediment yield fields such as `sedyld(j)` have been set up in `hru_module`. It uses the current HRU enrichment ratio and soil/plant organic pools to compute `sedorgn(j)`, and later HRU sediment-nitrogen accounting depends on that value together with the reduced soil and residue pools.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set current HRU | Copy `ihru` into `j` so the routine works on the active HRU's state arrays. |
| 2. sum available organic N | Add active humus, stable humus, total fresh residue across the plant community, and manure nitrogen from the top soil layer to form `xx`, then compute `wt1` from bulk density and layer depth. |
| 3. choose enrichment ratio | Use the HRU's organic-N enrichment ratio when it exceeds 0.001; otherwise fall back to the daily HRU enrichment ratio `enratio`. |
| 4. compute runoff organic N | Convert the organic-N sum to concentration with `conc = xx * er / wt1`, then calculate sediment organic nitrogen as `sedorgn(j) = .001 * conc * sedyld(j) / hru(j)%area_ha`. |
| 5. reduce pools if meaningful | If `xx` is greater than `1.e-6`, compute the retained fraction `xx1 = 1. - sedorgn(j) / xx` and scale the top-layer total organic pool, active humus, stable humus, each plant residue pool, and manure pool by `xx1`. |
| 6. return | Exit after the HRU sediment nitrogen and pool adjustments are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:organic_mineral_mass_module] | `soil1, pl_mass` | `soil1(j)%hact(1)%n, soil1(j)%hsta(1)%n, pl_mass(j)%rsd_tot%n, soil1(j)%man(1)%n, soil1(j)%tot(1)%n, pl_mass(j)%rsd(ipl)%n` |
| [sym:hru_module] | `hru, sedorgn, sedyld, ihru, enratio, ipl` | `hru(j)%hyd%erorgn` |
| [sym:soil_module] | `soil` | `soil(j)%phys(1)%bd, soil(j)%phys(1)%d` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sedorgn(j)` | When `xx > 1.e-6`, `sedorgn(j)` is computed from `conc`, `sedyld(j)`, and `hru(j)%area_ha` after the enrichment ratio is chosen. | `sedorgn(j)` stores the organic nitrogen load exported with sediment from the current HRU for this event. |
| `soil1(j)%tot(1)%n` | When `xx > 1.e-6`, `soil1(j)%tot(1)%n` is multiplied by `xx1 = 1. - sedorgn(j) / xx`. | The top-layer total organic nitrogen pool is reduced to remove the portion exported in runoff. |
| `soil1(j)%hact(1)%n` | When `xx > 1.e-6`, `soil1(j)%hact(1)%n` is multiplied by `xx1`. | Active humus nitrogen in the top layer is reduced in proportion to the organic N lost with sediment. |
| `soil1(j)%hsta(1)%n` | When `xx > 1.e-6`, `soil1(j)%hsta(1)%n` is multiplied by `xx1`. | Stable humus nitrogen in the top layer is reduced in proportion to the organic N lost with sediment. |
| `pl_mass(j)%rsd(ipl)%n` | When `xx > 1.e-6`, each `pl_mass(j)%rsd(ipl)%n` is multiplied by `xx1` inside the `do ipl = 1, pcom(j)%npl` loop. | Every plant residue nitrogen pool in the community is reduced to match the fraction of organic N removed from the HRU by runoff. |
| `soil1(j)%man(1)%n` | When `xx > 1.e-6`, `soil1(j)%man(1)%n` is multiplied by `xx1`. | Manure nitrogen in the top layer is reduced in proportion to the organic N exported with sediment. |

## File I/O

<!-- facts:io -->


## Lineage

Five resolved commits changed `nut_orgnc`: df07e3f introduced the routine with runoff-based organic nitrogen loss from the first soil layer and residue/manure pools; 39fabde only initialized local variables; f1e61a3 corrected indentation without changing logic; eb22103 switched the routine from `rsd1` pools to the refactored `soil1` structure and expanded the pool update to `soil1(j)%hact(1)%n`, `soil1(j)%hsta(1)%n`, `soil1(j)%rsd(1)%n`, and `soil1(j)%man(1)%n`; 72206bc replaced the single residue pool with `pl_mass(j)%rsd_tot%n` in the available-N sum, added `plant_module` and `ipl`, and changed the pool reduction loop to scale each plant residue in `pl_mass(j)%rsd(ipl)%n`.

- df07e3f added the core sediment organic-nitrogen calculation and the first-pass reduction of top-layer soil and residue/manure nitrogen pools.
- 39fabde made no behavioral change; it only initialized local variables to zero.
- f1e61a3 made no behavioral change; it only fixed tabs/formatting.
- eb22103 updated the routine for the new `soil1` layout, moving the depletion from `rsd1` pools to `soil1` humus, residue, and manure pools.
- 72206bc expanded the routine to work with plant-community residue mass via `pl_mass` and `pcom(j)%npl`, replacing the single residue pool update with a loop over all plant residues.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_orgnc' has no extracted documentation comment.
