---
kind: procedure
symbol: mgt_newtillmix_wet
title: mgt_newtillmix_wet
status: filled
source_hash: 7e8b5c1a3aa095c0
version_label: SWAT+ 62.0.0
args:
  jj: '`jj` selects the HRU/wetland profile to update; every water, soil, and constituent
    array access in the routine is indexed by this HRU number.'
  idtill: '`idtill` selects the tillage database record in `tilldb`, which provides the mixing
    efficiency and tillage depth used to compute the redistribution fractions.'
locals:
  l: Loop index over soil layers in HRU `jj`; it is reused for the prepass, mixing pass, and
    reconstitution pass across all layers.
  k: Loop index over pesticide constituent slots in `cs_soil(jj)%ly(l)%pest(k)` when pesticides
    are present.
  npmx: Cached number of pesticides from `cs_db%num_pests`; it sets the pesticide loop bound
    and the size of pesticide-related offsets in `smix`.
  emix: Tillage mixing efficiency copied from `tilldb(idtill)%effmix`; it scales how much
    of each layer is considered mixed.
  dtil: Tillage mixing depth copied from `tilldb(idtill)%deptil`; it defines the soil depth
    interval that participates in mixing with ponded water.
  frac_mixed: Fraction of a layer's mass that is treated as mixed; computed from mixed soil
    mass divided by total layer mass and used to weight source pools into `smix`.
  frac_non_mixed: Fraction of a layer that remains unmixed; used to retain the un-mixed remainder
    of each soil and pesticide pool when reconstituting layers.
  smix: Scratch array that accumulates the mixed concentrations or pool amounts for water,
    mineral nutrients, organic pools, soil texture, and optionally carbon pools and pesticides.
  sol_mass: Total mass of each soil layer before mixing, used as the denominator for mixed
    and unmixed fractions.
  sol_msm: Portion of each layer's mass that participates in mixing.
  sol_msn: Portion of each layer's mass that does not mix and is preserved when layer pools
    are rebuilt.
  frac_dep: Fraction of a soil layer that lies within the tillage depth; used to map mixed
    totals back onto the layer thickness.
  frac_dep1: Fraction of a soil layer within the combined ponding-water plus tillage-depth
    interval; used for pools that are mixed with ponded water as well as soil.
  tdep: Combined ponding-water depth plus tillage depth in millimeters; it defines the vertical
    extent over which pond water and soil are redistributed.
uses:
  tillage_data_module: '`tillage_data_module` supplies the selected tillage operation''s mixing
    efficiency and mixing depth, and those two parameters control whether mixing occurs and
    how far it extends.'
  basin_module: '`basin_module` provides the basin carbon-code switch `bsn_cc%cswat`, which
    gates the additional carbon-pool mixing updates for SWAT-C/CENTURY-style behavior.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` holds the HRU soil-layer pools
    that are read, mixed, and written back here; without these layered masses the routine
    could not redistribute nitrate, ammonium, phosphorus, humus, residue, manure, or microbial
    pools.'
  hru_module: '`hru_module` provides the HRU area used to convert between areal pool masses
    and mixed pond-water concentrations, so the wetland water updates are scaled to the correct
    HRU size.'
  soil_module: '`soil_module` supplies layer thickness, depth, bulk density, rock fraction,
    and texture, all of which are needed to compute layer mass, identify which layers fall
    inside the tillage depth, and update clay/silt/sand proportions.'
  constituent_mass_module: '`constituent_mass_module` provides the pesticide count and layered
    pesticide storage that this routine loops over and rewrites when constituents are present.'
  plant_module: '`plant_module` is imported in the procedure but no plant state or type from
    it is referenced in the extracted source, so its direct role here is uncertain from the
    available evidence.'
  reservoir_module: '`reservoir_module` provides the wetland depth used to combine ponded
    water with tillage depth and define the total mixed depth.'
  hydrograph_module: '`hydrograph_module` holds the wetland output pools that this routine
    updates, so the mixed-state results become the wetland nutrient and sediment/pool outputs
    used by downstream reporting and routing.'
---

<!-- facts:header -->

Redistributes wetland pond water, soil nutrients, organic matter, soil texture, and pesticides across tilled and untilled layers during a wet tillage event.

## Bottom Line

`mgt_newtillmix_wet` applies the tillage mixing settings for one HRU and one tillage operation to the wetted soil profile. It computes how much of the ponded water plus soil column is mixed, then recomputes the affected wetland water-quality pools and each soil layer pool from the mixed and unmixed fractions.

The routine matters because it is the wetland-specific tillage mixer used by management actions and the scheduled management workflow. Its results directly update wetland nutrient outputs and the layered soil/constituent state that later watershed, channel, and wetland behavior depends on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a tillage action is applied to an HRU that has ponded water; both `actions` and `mgt_sched` call it after resolving the tillage record index `idtill` from `tilldb` and confirming that `wet_ob(jj)%depth > 0.001`. Its outputs feed the wetland water-quality state (`wet(jj)%...`) and the layered soil/constituent state, which later management, hydrology, nutrient, and constituent calculations use.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize mixing controls and scratch arrays | Load the pesticide count, reset mixing fractions and scratch arrays, copy tillage efficiency and depth from `tilldb(idtill)`, and compute total mixed depth as ponded-water depth plus tillage depth. |
| 2. compute total layer masses | For each soil layer, compute the layer mass from thickness, bulk density, and rock fraction so later steps can determine how much of each layer participates in mixing. |
| 3. enter the wet tillage branch | Proceed only when tillage depth is positive; very shallow values are forced up to a minimum mixing depth before layer-by-layer redistribution starts. |
| 4. classify each layer by mixed depth | For every layer, compute mixed and unmixed soil mass plus depth fractions based on whether the layer is fully inside the tillage depth, partially intersected, or outside the mix zone. |
| 5. accumulate mixed mineral and organic pools | Use the mixed mass fraction to add each layer's mineral N, mineral P, humus, manure, residue, and total organic pools into the `smix` accumulator. |
| 6. accumulate texture and optional carbon pools | Add clay, silt, and sand by depth fraction, and when `bsn_cc%cswat == 2` also accumulate structural, lignin, metabolic, microbial, and humus carbon pools into `smix`. |
| 7. average the texture totals | Convert the accumulated clay, silt, and sand totals into depth-averaged mixed values by dividing by tillage depth. |
| 8. update wetland water-quality outputs | Recompute wetland NO3, NH3, soluble P, organic N, and sediment P from the mixed water-and-soil concentrations, scaling back to HRU-area mass units. |
| 9. rebuild each soil layer's non-carbon pools | For each layer, combine the unmixed remainder with the mixed totals to write back mineral N, mineral P, humus, manure, and total organic pools. |
| 10. rebuild texture and pesticide pools | Update clay, silt, and sand from the mixed fractions, then loop over all pesticides to redistribute each pesticide pool between mixed and unmixed fractions. |
| 11. rebuild carbon pools when SWAT-C is active | When `bsn_cc%cswat == 2`, write back the mixed structural, lignin, metabolic, microbial, and humus carbon pools using the same mixed/unmixed partitioning. |
| 12. finish | Exit the wet-mixing branch and return to the caller after all wetland and soil states have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:tillage_data_module] | `tilldb` | `tilldb(idtill)%effmix, tilldb(idtill)%deptil` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%cswat` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(jj)%mn(l)%no3, soil1(jj)%hsta(l)%n, soil1(jj)%mn(l)%nh4, soil1(jj)%mp(l)%lab, soil1(jj)%hsta(l)%p, soil1(jj)%hact(l)%n, soil1(jj)%mp(l)%act, soil1(jj)%tot(l)%n, soil1(jj)%tot(l)%p, soil1(jj)%mp(l)%sta, soil1(jj)%tot(l)%m, soil1(jj)%man(l)%c, soil1(jj)%man(l)%n, soil1(jj)%man(l)%p, soil1(jj)%tot(l)%c, soil1(jj)%str(l)%c, soil1(jj)%lig(l)%c, soil1(jj)%lig(l)%n, soil1(jj)%meta(l)%c, soil1(jj)%meta(l)%m, soil1(jj)%lig(l)%m, soil1(jj)%str(l)%m, soil1(jj)%str(l)%n, soil1(jj)%meta(l)%n, soil1(jj)%microb(l)%n` |
| [sym:hru_module] | `hru` | `hru(jj)%area_ha` |
| [sym:soil_module] | `soil` | `soil(jj)%nly, soil(jj)%phys(1)%bd, soil(jj)%phys(l)%rock, soil(jj)%phys(l)%d, soil(jj)%phys(l-1)%d, soil(jj)%phys(l)%thick, soil(jj)%phys(l)%clay, soil(jj)%phys(l)%silt, soil(jj)%phys(l)%sand` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_pests, cs_soil(jj)%ly(l)%pest(k)` |
| [sym:plant_module] | `hru` | `hru(jj)%area_ha` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(jj)%depth` |
| [sym:hydrograph_module] | `wet` | `wet(jj)%no3, wet(jj)%nh3, wet(jj)%solp, wet(jj)%orgn, wet(jj)%sedp` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet(jj)%no3` | `dtil > 0.` and the HRU has ponded water, so the routine enters the wet-mixing branch | The wetland nitrate pool is recomputed from the mixed water-and-soil concentration and scaled back to the HRU's ponded-water mass after tillage mixing. |
| `wet(jj)%nh3` | `dtil > 0.` and the HRU has ponded water, so the routine enters the wet-mixing branch | The wetland ammonium pool is recomputed from the mixed water-and-soil concentration and scaled back to the HRU's ponded-water mass after tillage mixing. |
| `wet(jj)%solp` | `dtil > 0.` and the HRU has ponded water, so the routine enters the wet-mixing branch | The wetland soluble phosphorus pool is recomputed from the mixed concentration and rescaled to the HRU ponded-water amount. |
| `wet(jj)%orgn` | `dtil > 0.` and the HRU has ponded water, so the routine enters the wet-mixing branch | The wetland organic nitrogen pool is reset to the mixed water-and-soil value after tillage redistributes ponded-water and soil material. |
| `wet(jj)%sedp` | `dtil > 0.` and the HRU has ponded water, so the routine enters the wet-mixing branch | The wetland sediment phosphorus pool is reset from the mixed concentration and scaled back to the ponded-water mass after tillage mixing. |
| `soil1(jj)%mn(l)%no3` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Layer nitrate is reduced to the unmixed remainder and replenished with the mixed pool that includes ponded water and soil within the tillage depth. |
| `soil1(jj)%hsta(l)%n` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Stable humus nitrogen is partitioned between unmixed and mixed fractions so the layer reflects tillage redistribution. |
| `soil1(jj)%mn(l)%nh4` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Layer ammonium is rewritten from the unmixed remainder plus the mixed pool that includes ponded-water exchange. |
| `soil1(jj)%mp(l)%lab` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Labile phosphorus is redistributed between the unmixed and mixed portions of the soil layer. |
| `soil1(jj)%hsta(l)%p` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Stable humus phosphorus is updated from the mixed and unmixed layer fractions after tillage mixing. |
| `soil1(jj)%hact(l)%n` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Active humus nitrogen is recomputed from the layer's unmixed remainder and the mixed pool. |
| `soil1(jj)%mp(l)%act` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Active mineral phosphorus is redistributed with the mixed water-and-soil fraction. |
| `soil1(jj)%tot(l)%n` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Total organic nitrogen is updated from the unmixed remainder plus the mixed pool that includes ponded water and soil. |
| `soil1(jj)%tot(l)%p` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Total organic phosphorus is updated from the same tillage redistribution fractions. |
| `soil1(jj)%mp(l)%sta` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Stable mineral phosphorus is updated from the mixed and unmixed layer fractions. |
| `soil1(jj)%tot(l)%m` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Total organic mass in the layer is redistributed between mixed and unmixed fractions. |
| `soil1(jj)%man(l)%c` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Manure carbon is partly preserved and partly replaced by the mixed pool for that layer. |
| `soil1(jj)%man(l)%n` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Manure nitrogen is redistributed according to the mixed and unmixed fractions. |
| `soil1(jj)%man(l)%p` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Manure phosphorus is redistributed according to the mixed and unmixed fractions. |
| `soil1(jj)%tot(l)%c` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Total organic carbon is rebuilt from the unmixed fraction and the tillage-mixed pool. |
| `soil(jj)%phys(l)%clay` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Layer clay percentage is recomputed from the mixed depth-averaged texture and the unmixed remainder. |
| `soil(jj)%phys(l)%silt` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Layer silt percentage is recomputed from the mixed depth-averaged texture and the unmixed remainder. |
| `soil(jj)%phys(l)%sand` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Layer sand percentage is recomputed from the mixed depth-averaged texture and the unmixed remainder. |
| `cs_soil(jj)%ly(l)%pest(k)` | When a soil layer lies within the tillage depth or the mixed fraction is nonzero | Each pesticide constituent in the layer is redistributed between the unmixed residue and the mixed pool for the current tillage depth. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four behavior-changing commits for `mgt_newtillmix_wet`. The 2024-05-30 import brought in the wet-mixing routine itself. The 2024-08-08 update initialized local counters and mixing scalars (`l`, `k`, `npmx`, `emix`, `dtil`, `frac_mixed`, `frac_non_mixed`, `tdep`) and corrected the scratch array sizing comment/history in the source. The 2024-10-08 change was formatting-only (tab cleanup) with no logic change. The 2026-02-25 commit broadened the carbon-pool mixing guards from `bsn_cc%cswat == 2` to `bsn_cc%cswat == 2 .or. bsn_cc%cswat == 3`, affecting both the accumulation and reconstitution of structural, lignin, metabolic, microbial, and humus carbon pools. The 2026-04-15 commit removed commented-out C-Farm-specific `mgt_tillfactor` calls, leaving runtime behavior unchanged. The 2026-06-02 commit changed those carbon guards back to `bsn_cc%cswat == 2`, reserving code 1 for C-FARM again.

- Initialized the routine's local mixing state variables and scratch dimensions so the wet tillage mixing calculations start from defined values.
- Expanded wet-tillage carbon mixing to include `bsn_cc%cswat == 3` in addition to 2, then later reverted that logic so only code 2 triggers the carbon-pool updates.
- Removed obsolete commented-out `mgt_tillfactor` calls without changing executed behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_newtillmix_wet' has no extracted documentation comment.
- plant_module is imported but no resolved plant symbol was found in the extracted source; its direct usage here is uncertain.
- algorithm_steps revised: merged the source's wet-mixing initialization and layer loop into concise steps while keeping all cited line ranges real and preserving the routine's execution order.
