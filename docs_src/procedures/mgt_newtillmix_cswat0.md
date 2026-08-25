---
kind: procedure
symbol: mgt_newtillmix_cswat0
title: mgt_newtillmix_cswat0
status: filled
source_hash: 1d59e204e936a329
version_label: SWAT+ 62.0.0
args:
  jj: Selects the HRU whose soil profile, residue pools, and tillage counters are being mixed.
  bmix: Provides the biological mixing fraction; when it is greater than `1.e-6`, the routine
    treats the event as biomixing instead of a tillage operation.
  idtill: Selects the tillage database entry that supplies the mixing efficiency and tillage
    depth for a tillage-driven event.
locals:
  l: Loop index over soil layers while computing layer masses, building mixed pools, and reconstructing
    the profile.
  kk: Holds the deepest soil layer index used to cap biomixing depth from the bottom of the
    profile.
  npmx: Stores `cs_db%num_pests`, the number of pesticides simulated; it is present for the
    commented pest-mixing code.
  ipl: Loop index over plant communities when mixing and redistributing plant residue pools.
  emix: Active mixing efficiency used to scale how much of each layer enters the mixed pool.
  dtil: Active mixing depth in mm used to decide which soil layers are affected.
  frac_mixed: Fraction of a layer's mass that participates in the mixed pool during the current
    layer pass.
  frac_non_mixed: Fraction of a layer's mass that remains in place when the layer is reconstructed.
  sol_mass: Total mass of each soil layer, used as the denominator for all mass fractions.
  sol_msm: Portion of each soil layer mass that is mixed into the blended pool.
  sol_msn: Portion of each soil layer mass that is not mixed and therefore remains in place.
  frac_dep: Fraction of each layer thickness that lies within the mixing depth, used to weight
    how much mixed material is returned to that layer.
  mix_clay: Depth-weighted clay content accumulated from the mixed portion of affected layers.
  mix_silt: Depth-weighted silt content accumulated from the mixed portion of affected layers.
  mix_sand: Depth-weighted sand content accumulated from the mixed portion of affected layers.
  mix_sw: Depth-weighted soil water storage accumulated from the mixed portion of affected
    layers.
  mix_rock: Depth-weighted rock-fragment content accumulated for tillage mixing; it is skipped
    for biomixing.
  mix_bd: Depth-weighted bulk density accumulator; the code computes it but does not apply
    it back to the soil profile in this routine.
  bio_mix_event: Flags whether the event is biomixing (`.true.` when `bmix > 1.e-6`) or a
    tillage operation (`.false.` otherwise).
uses:
  tillage_data_module: '`tillage_data_module` provides the tillage-event parameters that control
    how aggressively and how deep the soil is mixed when the routine is called for a tillage
    operation.'
  basin_module: '`basin_module` matters because the routine reads the basin-level constituent
    count to size the optional pesticide-related mixing setup, even though that path is not
    active in the extracted source.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` defines the organic and mineral
    mass containers that hold the mixed pools and the per-layer HRU masses. This routine updates
    those containers directly so residue, humus, and nutrient mass can be rebalanced after
    tillage or biomixing.'
  hru_module: '`hru_module` supplies the per-HRU tillage tracking arrays. The routine resets
    those counters when a tillage event occurs so later management logic knows a tillage operation
    happened and what depth was applied.'
  soil_module: '`soil_module` provides the HRU soil profile geometry and physical properties
    used to compute layer masses, determine which layers fall within the mixing depth, and
    write back the redistributed sand, silt, clay, rock, water storage, and bulk-density-related
    state.'
  constituent_mass_module: '`constituent_mass_module` matters because the routine sizes pesticide-related
    mixing support from the basin constituent database, even though the actual pest redistribution
    code is commented out in the extracted source.'
  plant_module: '`plant_module` provides the number of plant communities in the HRU. That
    count determines how many separate residue pools must be mixed and reconstructed for each
    layer.'
---

<!-- facts:header -->

Mixes soil residue, organic matter, and mineral nutrients through a soil profile during tillage or biological mixing.

## Bottom Line

`mgt_newtillmix_cswat0` redistributes mineral nitrogen, mineral phosphorus, organic pools, surface residue, and some soil physical properties across HRU soil layers based on a mixing efficiency and mixing depth. It is used for both tillage operations and biological mixing events, with the biological-mixing path handled differently for rock fragments and the tillage path updating tillage counters.

The routine first builds a depth-weighted mixed pool from the affected layers, then reconstructs each soil layer from the mixed pool plus the unmixed remainder. It also updates surface residue totals for each plant community and writes the resulting mixed values back into `soil1`, `pl_mass`, and selected `soil(jj)%phys` fields so later daily HRU behavior starts from the mixed profile state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during management updates when a tillage event is executed, and also during daily time control when biomixing is enabled for an HRU. Upstream callers prepare the HRU index, the tillage type, and either a biomixing fraction or a tillage database code; `actions` and `mgt_sched` pass a tillage operation, while `time_control` passes the daily biomix rate. Its results feed later soil-water, residue, nutrient, and plant-mass behavior because it rewrites the mixed profile state that subsequent processes read.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize module-driven mixing state and local accumulators. | Imports the needed modules, reads the pesticide count into `npmx`, seeds the mixed mineral and organic pools from zeroed template masses, and clears local accumulators for layer mass, fractions, and mixed soil properties. |
| 2. Allocate per-layer working arrays sized to the HRU soil profile. | Creates working arrays for total layer mass, mixed mass, unmixed mass, and depth fraction using the number of soil layers in `soil(jj)`. |
| 3. Choose biomixing or tillage mixing parameters. | Uses `bmix` to decide whether the event is biomixing or tillage, sets `emix` and `dtil` accordingly, and for tillage resets the HRU tillage counters and stores the applied depth. |
| 4. Skip pathogen mixing logic unless the tillage depth is large enough. | Leaves a placeholder for pathogen incorporation when the mixing depth exceeds 10 mm; no active pathogen redistribution is performed in the extracted code. |
| 5. Compute layer masses and partition each affected layer into mixed and unmixed portions. | For layers within the soil profile, calculates total layer mass from thickness, bulk density, and rock content, then derives mixed and unmixed portions based on depth and mixing efficiency. |
| 6. Accumulate the mixed pool across all affected layers. | Uses the mixed fraction to build depth-weighted averages for soil water, bulk density, sand, silt, clay, mineral N and P, total organic matter, and each plant residue/organic pool across the layers involved in the event. |
| 7. Reconstitute each soil layer from the unmixed remainder plus a share of the mixed pool. | Restores each layer's mineral, organic, residue, and texture state from the unmixed fraction plus the depth-weighted mixed pool, and transfers a portion of surface residue into the soil profile for each plant community. |
| 8. Release temporary storage and return to the caller. | Deallocates the working arrays and exits after the soil and residue state has been updated in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:tillage_data_module] | `tilldb` | `tilldb(idtill)%effmix, tilldb(idtill)%deptil` |
| [sym:basin_module] | `cs_db` | `cs_db%num_pests` |
| [sym:organic_mineral_mass_module] | `mix_org, soil1, pl_mass, mix_mn, mnz, mix_mp, mpz` | `mix_org%tot, mix_org%rsd, mix_org%hact, mix_org%hsta, mix_org%hs, mix_org%hp, mix_org%microb, mix_org%str, mix_org%lig, mix_org%meta, mix_org%man, mix_org%water, soil1(jj)%mn(l), soil1(jj)%mp(l), soil1(jj)%tot(l), mix_org%rsd(ipl), pl_mass(jj)%rsd(ipl), soil1(jj)%hact(l), soil1(jj)%hsta(l), soil1(jj)%hs(l), soil1(jj)%hp(l), soil1(jj)%microb(l), soil1(jj)%str(l), soil1(jj)%lig(l), soil1(jj)%meta(l), soil1(jj)%man(l), soil1(jj)%water(l), soil1(jj)%pl(ipl)%rsd(l), mix_org%surf_rsd, pl_mass(jj)%rsd_tot` |
| [sym:hru_module] | `tillage_days, tillage_depth, tillage_switch` |  |
| [sym:soil_module] | `soil` | `soil(jj)%nly, soil(jj)%phys(1)%bd, soil(jj)%phys(l)%rock, soil(jj)%phys(l)%d, soil(jj)%phys(l-1)%d, soil(jj)%phys(l)%thick, soil(jj)%phys(l)%st, soil(jj)%phys(l)%bd, soil(jj)%phys(l)%sand, soil(jj)%phys(l)%silt, soil(jj)%phys(l)%clay` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests` |
| [sym:plant_module] | `pcom` | `pcom(jj)%npl` |
| [sym:tillage_data_module] | `tilldb` | `tilldb(idtill)%effmix, tilldb(idtill)%deptil` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mix_mn` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_mn` becomes the depth-weighted mixed mineral nitrogen pool that will be redistributed back into each layer. |
| `mix_mp` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_mp` becomes the depth-weighted mixed mineral phosphorus pool that will be redistributed back into each layer. |
| `mix_org%tot` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%tot` becomes the depth-weighted mixed total organic pool for the soil profile. |
| `mix_org%rsd` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%rsd` becomes the depth-weighted mixed residue pool for each plant community. |
| `mix_org%hact` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%hact` becomes the depth-weighted mixed active humus pool. |
| `mix_org%hsta` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%hsta` becomes the depth-weighted mixed stable humus pool. |
| `mix_org%hs` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%hs` becomes the depth-weighted mixed slow-humus pool. |
| `mix_org%hp` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%hp` becomes the depth-weighted mixed passive-humus pool. |
| `mix_org%microb` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%microb` becomes the depth-weighted mixed microbial-biomass pool. |
| `mix_org%str` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%str` becomes the depth-weighted mixed structural-litter pool. |
| `mix_org%lig` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%lig` becomes the depth-weighted mixed lignin pool. |
| `mix_org%meta` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%meta` becomes the depth-weighted mixed metabolic-litter pool. |
| `mix_org%man` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%man` becomes the depth-weighted mixed manure pool. |
| `mix_org%water` | When the routine computes the mixed pool for affected soil layers (`dtil > 0.` and the layer contributes to `frac_mixed`). | `mix_org%water` becomes the depth-weighted mixed water-soluble organic pool. |
| `tillage_days(jj)` | When the routine is called for tillage rather than biomixing (`bmix <= 1.e-6`). | The HRU tillage counter is cleared so management tracking starts a new tillage event window. |
| `tillage_depth(jj)` | When the routine is called for tillage rather than biomixing (`bmix <= 1.e-6`). | The HRU stores the applied tillage depth so later management logic knows how deep the operation mixed the soil. |
| `tillage_switch(jj)` | When the routine is called for tillage rather than biomixing (`bmix <= 1.e-6`). | The HRU tillage switch is turned on to indicate that a tillage operation occurred. |
| `mix_org%rsd(ipl)` | When a layer is partially included in the mixed depth and plant residue is rebuilt for each plant community. | `mix_org%rsd(ipl)` holds the mixed residue pool for plant `ipl`, so each layer can receive the correct share of that plant's residue. |
| `soil1(jj)%mn(l)` | When a layer is reconstructed from the unmixed fraction and the mixed pool (`dtil > 0.`). | `soil1(jj)%mn(l)` is replaced by its unmixed remainder plus a depth-weighted share of the mixed mineral N pool. |
| `soil1(jj)%mp(l)` | When a layer is reconstructed from the unmixed fraction and the mixed pool (`dtil > 0.`). | `soil1(jj)%mp(l)` is replaced by its unmixed remainder plus a depth-weighted share of the mixed mineral P pool. |
| `soil1(jj)%tot(l)` | When a layer is reconstructed from the unmixed fraction and the mixed pool (`dtil > 0.`). | `soil1(jj)%tot(l)` is replaced by its unmixed remainder plus a depth-weighted share of the mixed total organic pool. |
| `soil1(jj)%pl(ipl)%rsd(l)` | When the routine redistributes residue for each plant community inside each affected layer. | `soil1(jj)%pl(ipl)%rsd(l)` is rebuilt from the unmixed layer residue plus the mixed residue share for plant `ipl`. |
| `mix_org%surf_rsd` | When the routine redistributes surface residue into the soil profile for a layer. | `mix_org%surf_rsd` records the amount of surface residue moved into the layer from plant `ipl` at the current mixing fraction. |
| `pl_mass(jj)%rsd(ipl)` | When the routine redistributes surface residue into the soil profile for a layer. | `pl_mass(jj)%rsd(ipl)` is reduced by the amount of plant residue moved from the surface into the profile. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage evidence shows six behavioral change points for this procedure. The 2025-10-29 change removed rock mixing during biomixing in the older tillage-mix routine, the 2025-10-29 update then made the procedure consistent with cswat=1 naming/compatibility, the 2026-01-07 update adjusted water allocation and soil cover calculations, the 2026-02-17 change integrated CENTURY residue/nutrient updates and root-fraction tracking, the 2026-02-19 change decremented `rsd_tot` for decomposition and tillage, and the 2026-04-22 change standardized internal names for cswat=0 versus cswat=1.

- Removed rock mixing from biomixing behavior so rock fragments are no longer blended during that event path.
- Updated the routine's naming/compatibility layer for cswat=1.
- Adjusted water allocation and soil cover calculations used during mixing.
- Integrated CENTURY residue and nitrogen updates plus root-fraction tracking into the mixing workflow.
- Decremented `pl_mass(jj)%rsd_tot` when residue is removed by decomposition or tillage.
- Standardized internal names so the cswat=0 and cswat=1 versions stay aligned.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_newtillmix_cswat0' has no extracted documentation comment.
