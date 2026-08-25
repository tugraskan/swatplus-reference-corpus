---
kind: procedure
symbol: mgt_newtillmix_cswat1
title: mgt_newtillmix_cswat1
status: filled
source_hash: 2ea77bc8f9a472b2
version_label: SWAT+ 62.0.0
args:
  jj: Selects the HRU whose soil profile, plant community, and tillage state are mixed and
    updated.
  bmix: Controls whether the event is treated as a biological mixing event; if it is zero,
    the routine marks `bio_mix_event` false before continuing with tillage-mixing setup.
  idtill: Selects the tillage operation database entry that supplies mixing efficiency and
    tillage depth for this event.
locals:
  fcgd: External routine declared but not called in the extracted source; no direct role is
    visible in this procedure.
  l: Loop counter over soil layers while calculating mixed mass, reconstituting layer pools,
    and stopping at the first layer below the tillage depth.
  npmx: Stores the number of pesticides from `cs_db%num_pests`; it is only assigned here and
    not used in the visible active code.
  ipl: Loop counter over plant positions in the HRU's plant community; used to mix and then
    remove surface residue for each plant.
  lyr_exit: Records the first soil layer below the tillage depth so later reconstitution stops
    at the correct layer.
  emix: Holds the mixing efficiency read from the tillage database and is used to scale how
    much of each layer is mixed.
  dtil: Holds the tillage mixing depth read from the tillage database and controls how many
    layers are fully or partially mixed.
  frac_mixed: Fraction of a layer's soil mass that is mixed; used to weight all mixed-pool
    additions from that layer.
  frac_non_mixed: Fraction of a layer's soil mass that remains unmixed; used when rebuilding
    the layer after the mixed pools are accumulated.
  sol_mass: Layer-by-layer soil mass used as the denominator for mixed and unmixed fractions
    and for texture weighting.
  sol_msm: Portion of each layer's soil mass that is mixed by tillage.
  sol_msn: Portion of each layer's soil mass that is not mixed by tillage.
  frac_dep: Fraction of the tillage depth represented by each layer; used to scale pool updates
    when a layer is only partly inside the tillage depth.
  mix_clay: Accumulated clay mass from all mixed soil portions, later used to reconstitute
    layer clay content.
  mix_silt: Accumulated silt mass from all mixed soil portions, later used to reconstitute
    layer silt content.
  mix_sand: Accumulated sand mass from all mixed soil portions, later used to reconstitute
    layer sand content.
  mix_sw: Accumulated soil-water storage from the mixed portions, later used to reconstitute
    layer storage.
  mix_rock: Accumulated rock-fragment mass from the mixed portions, later used to reconstitute
    layer rock content.
  mix_bd: Declared accumulator for bulk density, but the visible active update is commented
    out so it does not affect results in this source.
  bio_mix_event: Flags whether the event is biological mixing rather than a standard tillage
    mixing event; it is set false when `bmix` is zero and passed to `mgt_tillfactor`.
uses:
  tillage_data_module: These HRU-level tillage bookkeeping arrays are reset or populated when
    the operation occurs, and they carry the event timing, depth, and active-switch state
    forward for later management and output logic.
  basin_module: The routine reads the constituent database count to size pesticide-related
    logic, even though the active pesticide mixing loop is commented out in the visible source.
  organic_mineral_mass_module: This module defines the mixed organic and mineral pool containers
    that the routine accumulates from each mixed layer and then writes back into the HRU soil
    profile and residue states.
  hru_module: These HRU management arrays are the persistent state this procedure updates
    so later management scheduling and reporting can know that a tillage operation occurred
    and what depth was applied.
  soil_module: The soil profile provides the layer count, layer depths, physical thickness,
    texture, water storage, and layer tillage factor state needed to compute which layers
    are fully or partly mixed and how their properties change.
  constituent_mass_module: The pesticide constituent database supplies the pesticide count
    that would govern pesticide mixing logic; it matters because the source shows pesticide
    mixing was considered, even though that code is commented out.
  plant_module: Plant-community size determines how many residue pools must be mixed and reconstituted
    for each HRU, because residue redistribution is done plant by plant.
  plant_data_module: This plant-community state tells the routine how many plant residue components
    exist in the HRU so it can loop over each plant when mixing residue.
---

<!-- facts:header -->

Simulates residue and nutrient mixing caused by tillage or biological mixing in a single HRU.

## Bottom Line

This subroutine updates an HRU's soil and residue pools to reflect tillage mixing depth and efficiency. It redistributes mineral nitrogen and phosphorus, multiple organic matter pools, soil texture/structure properties, and plant residue between mixed and unmixed portions of the profile.

It also updates tillage bookkeeping for the HRU and then calls `mgt_tillfactor` so the layer-level tillage mixing factors are available for later soil and residue routines.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a scheduled or triggered tillage operation is executed for an HRU. The caller provides the HRU index and tillage type, and upstream code has already selected the operation and ensured the corresponding tillage database entry is known; afterward, later soil, residue, and management reporting depend on the updated soil layers, residue pools, and tillage flags.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize mixed-pool accumulators and HRU tillage bookkeeping | Reads the pesticide count, zeroes the mixed mineral and organic accumulators, resets per-event fractions and layer counters, allocates temporary layer arrays, optionally marks the event as non-biological when `bmix` is zero, and loads tillage efficiency and depth from `tilldb(idtill)` while resetting the HRU tillage day/depth/switch state. |
| 2. Prepare layer masses and determine which layers are mixed | For each soil layer, clears the layer mixing fraction, computes the soil mass for that layer, then classifies the layer as fully mixed, partially mixed, or unmixed based on its depth relative to `dtil`. Partial layers get proportional mixing and the routine stops after the first layer fully below the tillage depth. |
| 3. Accumulate the mixed fraction of each layer into shared soil and organic pools | Uses the mixed fraction to accumulate water storage, bulk density, rock, sand, silt, clay, mineral N, mineral P, total organic matter, humus pools, microbial biomass, litter pools, manure, and water-soluble pools from the mixed portion of each layer. It also loops over each plant in the community to add mixed residue from within the soil and from the surface residue pool. |
| 4. Rebuild each affected soil layer from mixed and unmixed portions | For each layer up to the exit layer, combines the unmixed fraction with the accumulated mixed pools to update mineral N, mineral P, total organic matter, all organic subpools, and the plant residue pool for each plant. It also subtracts the residue removed from the surface and recomputes layer texture and storage properties from the mixed and unmixed contributions. |
| 5. Finalize tillage factors and release temporary storage | Calls `mgt_tillfactor` to update layer tillage factors using the event's biological-mixing flag, mixing efficiency, and depth, then deallocates the temporary layer arrays and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:tillage_data_module] | `tillage_days, tillage_depth, tillage_switch` | `tillage_days, tillage_depth, tillage_switch` |
| [sym:basin_module] | `cs_db` | `cs_db%num_pests` |
| [sym:organic_mineral_mass_module] | `mix_org, soil1, pl_mass` | `mix_org%tot, mix_org%rsd, mix_org%hact, mix_org%hsta, mix_org%hs, mix_org%hp, mix_org%microb, mix_org%str, mix_org%lig, mix_org%meta, mix_org%man, mix_org%water, soil1(jj)%emix(l), soil1(jj)%mn(l), soil1(jj)%mp(l), soil1(jj)%tot(l), soil1(jj)%hact(l), soil1(jj)%hsta(l), soil1(jj)%hs(l), soil1(jj)%hp(l), soil1(jj)%microb(l), soil1(jj)%str(l), soil1(jj)%lig(l), soil1(jj)%meta(l), soil1(jj)%man(l), soil1(jj)%water(l), mix_org%rsd(ipl), mix_org%surf_rsd, soil1(jj)%pl(ipl)%rsd(l), pl_mass(jj)%rsd(ipl), pl_mass(jj)%rsd_tot` |
| [sym:hru_module] | `tillage_days, tillage_depth, tillage_switch` |  |
| [sym:soil_module] | `soil` | `soil(jj)%nly, soil(jj)%phys(1)%bd, soil(jj)%phys(l)%rock, soil(jj)%phys(l)%d, soil(jj)%phys(l-1)%d, soil(jj)%phys(l)%thick, soil(jj)%ly(l)%tillagef, soil(jj)%phys(l)%st, soil(jj)%phys(l)%bd, soil(jj)%phys(l)%sand, soil(jj)%phys(l)%silt, soil(jj)%phys(l)%clay` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests` |
| [sym:plant_module] | `pcom` | `pcom(jj)%npl` |
| [sym:plant_data_module] | `pcom` | `pcom(jj)%npl` |
| [sym:tillage_data_module] | `tilldb` | `tilldb(idtill)%effmix, tilldb(idtill)%deptil` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mix_mn` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `mnz`, then accumulates `frac_mixed * soil1(jj)%mn(l)` across mixed layers to pool the mineral nitrogen drawn out of the tilled layers. |
| `mix_mp` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `mpz`, then accumulates `frac_mixed * soil1(jj)%mp(l)` across mixed layers to pool the mineral phosphorus drawn out of the tilled layers. |
| `mix_org%tot` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%tot(l)` across mixed layers to pool the total organic mass drawn out of the tilled layers. |
| `mix_org%rsd` | At the start of a mixing event (`dtil > 1.e-6`), before the per-layer loop. | Initializes the residue mixing-pool array to the zero-mass template `orgz`; the per-plant entries are then accumulated separately as `mix_org%rsd(ipl)`. |
| `mix_org%hact` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%hact(l)` across mixed layers to pool the active (fast) humus pool drawn out of the tilled layers. |
| `mix_org%hsta` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%hsta(l)` across mixed layers to pool the stable humus pool drawn out of the tilled layers. |
| `mix_org%hs` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%hs(l)` across mixed layers to pool the slow humus pool drawn out of the tilled layers. |
| `mix_org%hp` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%hp(l)` across mixed layers to pool the passive humus pool drawn out of the tilled layers. |
| `mix_org%microb` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%microb(l)` across mixed layers to pool the microbial biomass pool drawn out of the tilled layers. |
| `mix_org%str` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%str(l)` across mixed layers to pool the structural litter pool drawn out of the tilled layers. |
| `mix_org%lig` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%lig(l)` across mixed layers to pool the lignin pool drawn out of the tilled layers. |
| `mix_org%meta` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%meta(l)` across mixed layers to pool the metabolic litter pool drawn out of the tilled layers. |
| `mix_org%man` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%man(l)` across mixed layers to pool the manure pool drawn out of the tilled layers. |
| `mix_org%water` | During a tillage/mixing event (`dtil > 1.e-6`); accumulated over each layer within the mixing depth. | Reset to the zero-mass template `orgz`, then accumulates `frac_mixed * soil1(jj)%water(l)` across mixed layers to pool the residue water pool drawn out of the tilled layers. |
| `tillage_days(jj)` | On every tillage operation (unconditionally, near the top of the routine). | Resets the days-since-tillage counter for the HRU to zero because a tillage event has just occurred. |
| `tillage_depth(jj)` | On every tillage operation (unconditionally, near the top of the routine). | Stores this operation's tillage depth (`tilldb(idtill)%deptil`, held in `dtil`) for the HRU. |
| `tillage_switch(jj)` | On every tillage operation (unconditionally, near the top of the routine). | Sets the HRU tillage flag to 1 to mark that tillage is active. |
| `soil1(jj)%emix(l)` | For each soil layer during a mixing event: full layers within `dtil`, the boundary layer straddling `dtil`, or layers below it. | Per-layer mixing efficiency: `emix` for layers fully within the tillage depth, a depth-scaled fraction for the boundary layer, and 0 for layers below the tillage depth. |
| `soil(jj)%ly(l)%tillagef` | In the branch for the first layer below the tillage depth (the loop exit layer). | Cleared to 0 for layers below the tillage depth, which receive no mixing this operation. |
| `mix_org%rsd(ipl)` | For each plant in the community (`ipl = 1..pcom(jj)%npl`) in each mixed layer. | Accumulates the residue mixed for plant `ipl` from in-soil residue plus the surface residue incorporated into the layer. |
| `mix_org%surf_rsd` | For each plant in each layer, both while gathering (accumulation loop) and while reconstituting layers. | Surface residue incorporated into the current layer for plant `ipl`; in the reconstitution loop the same amount is subtracted from the surface residue pool. |
| `soil1(jj)%mn(l)` | During the reconstitution loop, for each mixed layer (`dtil > 1.e-6`). | Each layer's mineral nitrogen is rebuilt as the unmixed fraction left in place plus its depth-weighted share of the pooled `mix_mn`. |
| `soil1(jj)%mp(l)` | During the reconstitution loop, for each mixed layer (`dtil > 1.e-6`). | Each layer's mineral phosphorus is rebuilt as the unmixed fraction left in place plus its depth-weighted share of the pooled `mix_mp`. |
| `soil1(jj)%tot(l)` | During the reconstitution loop, for each mixed layer (`dtil > 1.e-6`). | Each layer's total organic mass is rebuilt as the unmixed fraction left in place plus its depth-weighted share of the pooled `mix_org%tot`. |

## File I/O

<!-- facts:io -->


## Lineage

`mgt_newtillmix_cswat1.f90` was introduced in `50ba5c8` (2026-04-22, "Fixed files with wrong extension in the file name.") and has been changed in 3 non-merge commit(s) since, most recently `774d6c3` (2026-04-29, "Adjusted the tillage factor computation in mgt_tillfactor to decrease the tillag…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_newtillmix_cswat1.f90` are listed.

- `774d6c3` (2026-04-29) — Adjusted the tillage factor computation in mgt_tillfactor to decrease the tillage factor each day based on the moisture content of the soil.…
- `1b2a997` (2026-04-27) — Made changes to implement a linear increase in biomixing after a tillage event.
- `50ba5c8` (2026-04-22) — Fixed files with wrong extension in the file name.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_newtillmix_cswat1' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
