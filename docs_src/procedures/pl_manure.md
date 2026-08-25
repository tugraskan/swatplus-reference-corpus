---
kind: procedure
symbol: pl_manure
title: pl_manure
status: filled
source_hash: 85eb4ff8d60e30c9
version_label: SWAT+ 62.0.0
args:
  ifrt: Selects the manure type record in `manure_om`; its fractions control how the applied
    mass is split into water, mineral N/P, organic N/P, and carbon pools.
  frt_kg: Specifies the manure application amount in kg/ha; the routine scales all manure-derived
    additions to soil pools and summary outputs from this amount.
  fertop: Selects the chemical application record in `chemapp_db`; its `surf_frac` determines
    what fraction of the manure is assigned to the surface layer versus the lower layer.
locals:
  rtof: Partitioning factor from `man_coef%rtof` that splits organic manure N and P between
    the faster/organic and slower/stable soil organic pools.
  j: Current HRU index copied from `ihru`, used to update the active soil and mass state for
    that HRU.
  l: Layer loop index; the routine processes two application zones, surface and subsurface.
  fr_ly: Fraction of the manure assigned to the current layer, based on `chemapp_db(fertop)%surf_frac`.
  org_c: Organic carbon mass applied to the current layer, derived from manure carbon content.
  meta_fr: Computed fraction of `org_c` routed to the metabolic litter pool, constrained to
    the 0.01 to 0.7 range.
  meta_c: Organic carbon added to the metabolic litter carbon pool.
  meta_m: Total metabolic litter mass added from the manure carbon allocation.
  meta_n: Organic nitrogen added to the metabolic litter nitrogen pool.
  str_c: Organic carbon remaining after metabolic allocation, routed to the structural litter
    carbon pool.
  str_m: Total structural litter mass added from the remaining carbon allocation.
  c_n_fac: Carbon-to-nitrogen factor used to compute `meta_fr` from manure C and combined
    mineral/organic N.
  liq_manure_kg: Calculated kg/ha of manure water associated with the applied manure mass.
  liq_manure_mm: Converted manure water depth in mm/ha, used to add water to `soil(j)%phys(l)%st`.
  frac_solids: Solid fraction of the manure, computed from `manure_om(ifrt)%frac_water` and
    used to derive the liquid portion.
  fr_mass: Mass of manure assigned to the current layer after multiplying the total application
    by `fr_ly`; this is the base mass used for all layer-specific soil additions.
uses:
  mgt_operations_module: '`chemapp_db(fertop)%surf_frac` tells the routine how to split the
    applied manure between the first layer and the remaining fraction, so the application
    depth pattern comes from the management operation database.'
  fertilizer_data_module: '`manure_om(ifrt)` supplies the manure composition fractions that
    determine how much of the applied mass becomes water, nitrate/ammonium, organic N/P, and
    carbon in the soil pools.'
  basin_module: '`bsn_cc%cswat` selects which carbon-cycling formulation is active, which
    changes whether manure updates go to the legacy humus pools or the CENTURY-style manure,
    humus, metabolic, structural, and lignin pools.'
  soil_module: '`soil(j)%phys(l)%st` holds soil-layer water storage; the routine adds manure
    liquid water there, so this module provides the physical layer state being modified.'
  organic_mineral_mass_module: '`soil1(j)` contains the organic and mineral mass pools that
    receive the manure additions, including mineral N/P, humus, litter, manure, metabolic,
    structural, and lignin reservoirs.'
  hru_module: '`ihru` selects the active HRU to update, and the `fert*` accumulators store
    manure-derived output totals that later management reporting and nutrient accounting use.'
---

<!-- facts:header -->

Applies manure to the current HRU and splits its water, mineral nutrients, and organic matter into soil pools. The exact pool routing depends on the SWAT carbon-cycling mode and the manure/application database entries.

## Bottom Line

`pl_manure` applies a manure fertilizer event to the current HRU by splitting the requested manure mass between the surface and subsurface portions defined by `chemapp_db(fertop)%surf_frac`, then updating soil water and nutrient pools for each affected layer. It converts the manure's water fraction from `manure_om(ifrt)%frac_water` into a liquid-water depth and uses the manure database fractions for mineral N, organic N/P, carbon, and ammonium/labile P to update the soil state.

The routine matters because it is the shared manure-application engine used by both scheduled management (`mgt_sched`) and action-triggered management (`actions`). After the soil pools are updated, it also accumulates the fertilizer summary variables `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `fertn`, and `fertp` for later reporting and downstream management output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a manure management operation is executed from the management scheduler or action handler. `actions` or `mgt_sched` set up the manure type, amount, and application fraction before calling it, and the resulting soil pool and `fert*` updates are then used by later nutrient accounting and management-output reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load HRU and manure controls | Copies the active HRU index from `ihru` into `j` and loads the manure-partition factor `rtof` from `man_coef%rtof` for later splitting of organic N and P. |
| 2. compute manure water content | Uses `manure_om(ifrt)%frac_water` to compute the manure's solid fraction, derives the liquid manure mass from the requested application rate, and converts that liquid mass to an equivalent water depth in mm/ha. |
| 3. loop over two application zones | Processes the manure twice: once for the surface fraction and once for the remaining fraction, with `chemapp_db(fertop)%surf_frac` controlling how the manure is split between the two layers. |
| 4. compute layer manure mass | Computes `fr_mass` as the manure mass assigned to the current layer, and uses that layer-specific mass for all later nutrient and carbon allocations. |
| 5. add liquid water to soil storage | Adds the manure's liquid-water depth to `soil(j)%phys(l)%st` for the current layer. |
| 6. add mineral nitrate from manure | Updates `soil1(j)%mn(l)%no3` with the manure's mineral nitrogen fraction after removing the ammonia-N share, so only the nitrate portion is added here. |
| 7. update old carbon-code pools | When `bsn_cc%cswat == 0`, adds manure organic N and P to the legacy total and active humus pools, splitting each element between `soil1(j)%tot(l)` and `soil1(j)%hact(l)` using `rtof`. |
| 8. update CENTURY manure pools | When `bsn_cc%cswat == 2`, adds manure carbon, organic N, and organic P to the CENTURY manure pool components in `soil1(j)%man(l)`. |
| 9. allocate CENTURY humus and litter pools | When `bsn_cc%cswat == 2`, adds organic P and N to slow humus, computes organic carbon and the metabolic fraction, constrains that fraction to 0.01-0.7, then updates metabolic, structural, lignin, and associated mass pools. |
| 10. add ammonium and labile phosphorus | Adds the manure's ammonium-N and soluble/mineral P fractions to `soil1(j)%mn(l)%nh4` and `soil1(j)%mp(l)%lab`. |
| 11. compute fertilizer summaries | Computes `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, and `fertorgp`, then accumulates the event totals into `fertn` and `fertp` for later reporting. |
| 12. return to caller | Ends the routine after all layer updates and summary-state calculations are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `chemapp_db` | `chemapp_db(fertop)%surf_frac` |
| [sym:fertilizer_data_module] | `manure_om` | `manure_om(ifrt)%frac_water, manure_om(ifrt)%fnh3n, manure_om(ifrt)%fminn, manure_om(ifrt)%forgn, manure_om(ifrt)%forgp, manure_om(ifrt)%fcbn, manure_om(ifrt)%fminp` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%cswat` |
| [sym:soil_module] | `soil` | `soil(j)%phys(l)%st` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(l)%no3, soil1(j)%tot(l)%n, soil1(j)%hact(l)%n, soil1(j)%tot(l)%p, soil1(j)%hsta(l)%p, soil1(j)%man(l)%c, soil1(j)%man(l)%n, soil1(j)%man(l)%p, soil1(j)%hs(l)%p, soil1(j)%hs(l)%n, soil1(j)%meta(l)%c, soil1(j)%meta(l)%m, soil1(j)%meta(l)%n, soil1(j)%str(l)%n, soil1(j)%str(l)%c, soil1(j)%lig(l)%c, soil1(j)%lig(l)%n, soil1(j)%str(l)%m, soil1(j)%lig(l)%m, soil1(j)%mn(l)%nh4, soil1(j)%mp(l)%lab` |
| [sym:hru_module] | `ihru, fertn, fertp, fertnh3, fertno3, fertorgn, fertorgp, fertsolp` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(j)%phys(l)%st` | On every layer pass after `liq_manure_mm` is computed. | `soil(j)%phys(l)%st` increases by the manure liquid water depth assigned to that layer, so the soil water storage reflects the water content of the applied manure. |
| `soil1(j)%mn(l)%no3` | On every layer pass after the mineral-N split is evaluated. | `soil1(j)%mn(l)%no3` increases by the nitrate portion of the manure's mineral nitrogen, using the manure type's mineral-N and ammonia-N fractions. |
| `soil1(j)%tot(l)%n` | Only when `bsn_cc%cswat == 0`. | `soil1(j)%tot(l)%n` receives the organic N routed to the legacy total organic pool, reflecting the carbon-mode-specific manure bookkeeping. |
| `soil1(j)%hact(l)%n` | Only when `bsn_cc%cswat == 0`. | `soil1(j)%hact(l)%n` receives the complementary organic N share routed to the active humus pool in the legacy carbon formulation. |
| `soil1(j)%tot(l)%p` | Only when `bsn_cc%cswat == 0`. | `soil1(j)%tot(l)%p` increases by the manure organic P share routed to the legacy total organic pool. |
| `soil1(j)%hsta(l)%p` | Only when `bsn_cc%cswat == 0`. | `soil1(j)%hsta(l)%p` receives the remaining organic P share routed to the stable humus pool in the legacy carbon formulation. |
| `soil1(j)%man(l)%c` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%man(l)%c` increases by the manure carbon assigned to the manure pool for the current layer. |
| `soil1(j)%man(l)%n` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%man(l)%n` increases by the manure organic nitrogen assigned to the manure pool. |
| `soil1(j)%man(l)%p` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%man(l)%p` increases by the manure organic phosphorus assigned to the manure pool. |
| `soil1(j)%hs(l)%p` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%hs(l)%p` increases by the stable humus phosphorus share of the manure organic P. |
| `soil1(j)%hs(l)%n` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%hs(l)%n` increases by the stable humus nitrogen share of the manure organic N. |
| `soil1(j)%meta(l)%c` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%meta(l)%c` increases by the manure carbon routed to the metabolic litter pool. |
| `soil1(j)%meta(l)%m` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%meta(l)%m` increases by the total metabolic litter mass derived from the metabolic carbon share. |
| `soil1(j)%meta(l)%n` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%meta(l)%n` increases by the nitrogen associated with the metabolic litter fraction. |
| `soil1(j)%str(l)%n` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%str(l)%n` increases by the remaining organic nitrogen that is not assigned to the metabolic pool. |
| `soil1(j)%str(l)%c` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%str(l)%c` increases by the manure carbon left after metabolic allocation. |
| `soil1(j)%lig(l)%c` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%lig(l)%c` increases by the lignin carbon share of the structural litter carbon. |
| `soil1(j)%lig(l)%n` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%lig(l)%n` increases by the non-lignin nitrogen share associated with the structural litter carbon. |
| `soil1(j)%str(l)%m` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%str(l)%m` increases by the total structural litter mass derived from the remaining structural carbon. |
| `soil1(j)%lig(l)%m` | Only when `bsn_cc%cswat == 2`. | `soil1(j)%lig(l)%m` increases by the lignin mass associated with the structural litter pool. |
| `soil1(j)%mn(l)%nh4` | On every layer pass after the mineral-N and organic pool updates. | `soil1(j)%mn(l)%nh4` increases by the ammonium portion of the manure's mineral nitrogen. |
| `soil1(j)%mp(l)%lab` | On every layer pass after the mineral P split is evaluated. | `soil1(j)%mp(l)%lab` increases by the manure's labile/mineral phosphorus fraction. |
| `fertno3` | After both layers are processed. | `fertno3` stores the manure-derived nitrate-N summary for reporting and later management output. |
| `fertnh3` | After both layers are processed. | `fertnh3` stores the manure-derived ammonia-N summary for reporting and later management output. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `pl_manure`: 561bc28 added the manure-application routine and its initial water and nutrient allocations; f7e26d7 introduced liquid-manure handling, the layer split, and the CENTURY C/N cycling blocks; 52a9a81 removed the unused `orgc_fr` assignment and switched to `man_coef%man_to_c`; 1c1d00d removed another unused local variable; 8ca9c1a removed the local `frt_ly`, added `fr_mass`, and rewired most nutrient allocations to use the layer mass instead of repeated `fr_ly * frt_kg` expressions.

- 561bc28 established `pl_manure` as the manure-management update routine and added the core HRU/soil state updates for water, mineral N, and manure carbon and nutrient pools.
- f7e26d7 changed the routine to compute liquid manure depth from manure water fraction, split application by surface fraction, and expand the CENTURY allocation logic for metabolic, structural, lignin, and slow-humus pools.
- 52a9a81 simplified the setup by removing the unused `orgc_fr` assignment, so the routine no longer depended on that local during pool calculations.
- 1c1d00d removed an unneeded local variable declaration, a no-behavior-change cleanup.
- 8ca9c1a changed the internal mass basis to `fr_mass`, removed the local `frt_ly`, and updated the manure carbon, nitrogen, phosphorus, and summary calculations to use the layer-specific mass consistently.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_manure' has no extracted documentation comment.
- algorithm_steps revised: condensed the two application-zone steps into a single split-by-layer step and aligned step numbering with the visible source blocks.
- Source uncertainty note: the extracted source comment at line 9 references `Erfc`, but no outgoing call was resolved in the procedure body.
