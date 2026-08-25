---
kind: procedure
symbol: pl_mortality
title: pl_mortality
status: filled
source_hash: d655c5fd25b6c8c9
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from ihru so the routine can access the current HRU's soil, residue,
    and plant mass records.
  idp: Plant database index for the current plant in pcom(j)%plcur(ipl)%idplt; used to read
    perennial mortality parameters from pldb.
  ly: Loop index over soil layers when distributing dead roots into layer-by-layer residue
    pools.
  bm_dieoff: Calculated above-ground biomass excess that should be removed and converted to
    residue, scaled by the plant-specific dieoff fraction.
  rto: Fraction of current biomass treated as dead material; used to add residue before the
    living pools are reduced.
  rto1: Fraction of biomass that remains alive after mortality; used to scale down the surviving
    plant mass pools.
uses:
  plant_data_module: plant_data_module supplies per-plant mortality controls. pldb(idp)%bm_dieoff
    sets the dieoff fraction applied to biomass above the perennial maximum, and pldb(idp)%bmx_peren
    provides that maximum biomass threshold.
  basin_module: basin_module matters because the routine's residue handling is gated by the
    basin configuration flag bsn_cc%cswat in the lineage history, which determines whether
    additional residue partitioning logic is active.
  hru_module: hru_module provides the current HRU and plant indices, ihru and ipl, that identify
    which HRU/plant masses and soil pools this mortality update should operate on.
  plant_module: plant_module supplies the current plant community state. pcom(j)%plcur(ipl)%idplt
    identifies the plant database record to use, and pcom(j)%plg(ipl)%rtfr(ly) gives the per-layer
    root fraction used to distribute dead root mass.
  carbon_module: carbon_module matters because mortality-derived residue updates are part
    of the plant-carbon and residue bookkeeping system, even though no direct symbol from
    the module appears in the extracted lines.
  organic_mineral_mass_module: 'organic_mineral_mass_module supplies the live plant mass pools
    and the soil residue pools that this routine updates: pl_mass(j)%ab_gr(ipl)%m is used
    to compute excess biomass, pl_mass(j)%rsd(ipl) and pl_mass(j)%rsd_tot receive surface
    residue, soil1(j)%pl(ipl)%rsd(ly) receives root residue, and the living mass components
    tot, ab_gr, leaf, stem, seed, and root are reduced.'
  soil_module: soil_module provides the soil layer count soil(j)%nly, which controls how many
    layers receive dead root residue.
---

<!-- facts:header -->

Limits perennial plant biomass at end of the year and routes the removed mass into residue pools. It reduces living plant components proportionally and distributes dead roots across soil layers.

## Bottom Line

pl_mortality runs at year end for the current HRU/plant combination. It checks whether the plant's above-ground biomass exceeds the perennial maximum allowed for that plant type, then computes how much biomass must die off and moves that amount into residue pools.

The routine matters because it preserves a biomass cap while conserving material by partitioning dead above-ground mass to plant surface residue and dead roots to layer-specific soil residue pools. It also scales the remaining live total, above-ground, leaf, stem, seed, and root masses by the surviving fraction.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside pl_grow at the end of the yearly plant-growth cycle, after growth and partitioning have already updated the plant state. pl_grow prepares the current HRU/plant context and then calls pl_mortality when time%end_yr is true; the results feed later residue and biomass bookkeeping for the next model steps and output summaries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set indices and plant type | Copies the current HRU index from ihru into j and looks up the current plant's database index idp from pcom(j)%plcur(ipl)%idplt. |
| 2. compute excess biomass | Calculates bm_dieoff as the plant-specific dieoff fraction times the amount by which above-ground biomass exceeds the perennial maximum biomass threshold. |
| 3. test whether mortality is needed | Only continues when the computed excess is meaningful and the current above-ground biomass is larger than the dieoff amount. |
| 4. compute dead and surviving fractions | Computes rto as the fraction of biomass that dies, limits it to at most 1, then computes rto1 as the surviving fraction and bounds it at zero or higher. |
| 5. add dead above-ground mass to residue | Moves the dead share of above-ground biomass into the plant surface residue pool and the plant-level total residue accumulator. |
| 6. distribute dead roots by soil layer | Loops over all soil layers and adds the dead share of root mass to each plant residue pool in proportion to the plant root-fraction profile for that layer. |
| 7. reduce living biomass pools | Scales the remaining total, above-ground, leaf, stem, seed, and root pools by the surviving fraction so the live biomass matches the mortality that occurred. |
| 8. return | Leaves the routine after the mortality update is complete, returning control to the caller with residue and live biomass state updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%bm_dieoff, pldb(idp)%bmx_peren` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%cswat` |
| [sym:hru_module] | `ihru, ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plg(ipl)%rtfr(ly)` |
| [sym:carbon_module] | `carbon-related state or types were imported through carbon_module, but no specific symbol from that module is referenced in the extracted source lines.` |  |
| [sym:organic_mineral_mass_module] | `pl_mass, soil1` | `pl_mass(j)%ab_gr(ipl)%m, pl_mass(j)%rsd(ipl), pl_mass(j)%ab_gr(ipl), pl_mass(j)%rsd_tot, soil1(j)%pl(ipl)%rsd(ly), pl_mass(j)%root(ipl), pl_mass(j)%tot(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%seed(ipl)` |
| [sym:soil_module] | `soil` | `soil(j)%nly` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pl_mass(j)%rsd(ipl)` | When bm_dieoff is positive and the plant's above-ground biomass exceeds the dieoff amount. | Dead above-ground biomass is added to the plant surface residue pool so removed biomass is retained in the residue system. |
| `pl_mass(j)%rsd_tot` | Same mortality trigger as above; updated in the same residue-routing block. | The plant-level total fresh residue accumulator is increased by the dead above-ground mass so downstream bookkeeping has the full residue total. |
| `soil1(j)%pl(ipl)%rsd(ly)` | For every soil layer from 1 to soil(j)%nly when mortality is triggered. | Layer-specific plant residue is increased by the dead root share, using the layer root-fraction profile to place root residue in the correct soil layers. |
| `pl_mass(j)%tot(ipl)` | When mortality is triggered. | The plant's total live biomass is reduced to the surviving fraction so the remaining live mass is consistent with the biomass moved to residue. |
| `pl_mass(j)%ab_gr(ipl)` | When mortality is triggered. | Above-ground live biomass is reduced to the surviving fraction after excess biomass has been routed to residue. |
| `pl_mass(j)%leaf(ipl)` | When mortality is triggered. | Leaf mass is scaled down with the surviving fraction, reflecting proportional mortality across live plant components. |
| `pl_mass(j)%stem(ipl)` | When mortality is triggered. | Stem mass is scaled down with the surviving fraction, reflecting proportional mortality across live plant components. |
| `pl_mass(j)%seed(ipl)` | When mortality is triggered. | Seed mass is scaled down with the surviving fraction, reflecting proportional mortality across live plant components. |
| `pl_mass(j)%root(ipl)` | When mortality is triggered. | Root mass is scaled down with the surviving fraction after the dead portion has been routed into soil residue pools. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage evidence shows five behavior-changing revisions to pl_mortality: it first switched from rsd1(j)%tot(ipl) to soil1(j)%rsd(1), then added soil-module layering and new ly indexing, then changed the mortality fraction formula and switched surface residue handling to use pl_mass(j)%rsd(ipl) and pl_mass(j)%rsd_tot, then replaced soil-layer root residue placement with plant-specific soil1(j)%pl(ipl)%rsd(ly) using pcom(j)%plg(ipl)%rtfr(ly), and finally corrected the root-residue line to use the plant root-fraction profile instead of soil layer fractions.

- eb22103 changed the residue target from rsd1(j)%tot(ipl) to soil1(j)%rsd(1), moving the procedure onto the new soil1 residue structure.
- b3b930a added use of soil_module, introduced ly, and expanded mortality to place dead above-ground biomass into soil1(j)%rsd(1) and additional C/N/P residue pools, while also adding root residue handling by soil layer.
- 452a041 changed bm_dieoff and rto calculation, and redirected above-ground residue bookkeeping through pl_mass(j)%rsd(ipl) and soil1(j)%rsd(1).
- 72206bc moved above-ground residue into pl_mass(j)%rsd(ipl) and pl_mass(j)%rsd_tot, and updated root residue placement to soil1(j)%pl(ipl)%rsd(ly).
- 3e18acf corrected the root-residue distribution to use pcom(j)%plg(ipl)%rtfr(ly) instead of soil layer root fractions.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_mortality' has no extracted documentation comment.
