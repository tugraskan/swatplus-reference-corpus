---
kind: procedure
symbol: nut_orgnc2
title: nut_orgnc2
status: filled
source_hash: 3230449d38eeafee
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; used to select the current HRU’s soil, residue, plant,
    and carbon state.
  ly: Soil-layer loop index used when distributing carbon and updating deeper layers from
    layer 2 down to the bottom layer.
  flo_loss_co: Flow-loss coefficient that combines water capacity with microbial carbon interaction
    to control how much microbial carbon is removed by flow.
  wt1: Conversion factor from soil bulk density and depth to the soil mass basis used to turn
    organic N mass into concentration.
  er: Organic nitrogen enrichment ratio used to scale sediment-associated organic N loss from
    the surface layer.
  conc: Computed concentration of organic nitrogen in the surface soil, derived from surface
    organic N and enrichment.
  sol_mass: Total mass of the surface soil layer, used as the denominator for erosion fraction
    and sediment carbon loss calculations.
  c_surlat: Dissolved carbon loss routed to surface runoff and lateral flow from the surface
    layer.
  c_vert: Dissolved carbon routed downward by percolation; also carried between deeper layers
    as the vertical flux variable.
  c_horiz: Temporary horizontal carbon transport term used to estimate microbial carbon associated
    with erosion and lateral movement.
  c_microb: Unused placeholder in the extracted source; initialized to zero but not referenced
    in the visible algorithm.
  c_sed: Carbon lost with sediment from the surface layer before microbial sediment adjustments.
  ero_fr: Fraction of the surface soil mass removed by erosion; limits sediment carbon loss
    to at most 0.9 of total surface carbon.
  koc: Carbon water coefficient `prmt_21` from `cb_wtr_coef`, used to control microbial carbon
    loss under flowing water.
  c_microb_fac: Helper factor built from `koc` and surface organic carbon to scale microbial
    carbon loss under runoff and percolation.
  flo_tot: Total water flux across the layer, combining surface runoff, percolation, and lateral
    storage flow.
  c_microb_loss: Microbial carbon removed by water flux from the surface layer when total
    flow is large enough.
  horiz_conc: Intermediate dissolved carbon concentration used to derive horizontal and vertical
    carbon transport terms.
  vert_conc: Intermediate dissolved carbon concentration in the vertical direction, derived
    from microbial loss and flow partitioning.
  perc_clyr: Unused in the visible source after initialization; likely a leftover accumulator
    for percolation carbon by layer.
  latc_clyr: Accumulator for lateral carbon transport through the profile; the sum becomes
    `hsc_d(j)%latq_c`.
  n_left_rto: Remaining nitrogen ratio after organic N is removed from the surface layer;
    used to scale surface-layer N pools.
  c_microb_perc: Temporary carbon available for deeper-layer percolation and redistribution
    at each layer.
  c_microb_sed: Microbial carbon removed with sediment from the surface layer when erosion
    is present.
  c_ly1: Total surface organic nitrogen pool used as the basis for organic N concentration
    and runoff loss.
uses:
  hru_module: The HRU module provides the current HRU index, erosion ratio, sediment yield,
    surface runoff, and the `sedorgn` output array. Those values define the event forcing
    and receive the computed organic N loss for this HRU.
  soil_module: The soil module supplies the physical soil properties and layer storage terms
    that determine soil mass, water-flow partitioning, and the lateral/percolation routing
    used in the carbon loss calculations.
  organic_mineral_mass_module: The organic mass module holds the carbon and nitrogen pools
    that are adjusted here. `nut_orgnc2` updates these surface and layer pools directly, so
    their definitions matter for understanding what is being reduced or recomputed.
  carbon_module: The carbon module defines the carbon gain/loss output structure and the water
    coefficients `prmt_21` and `prmt_44` that control microbial and dissolved carbon routing.
  plant_module: The plant module provides the number of plants in the community, which controls
    how many residue pools are iterated when surface residue carbon is scaled by erosion loss.
  plant_data_module: The plant-data module is imported alongside the plant community data
    so the routine can work with residue-by-plant bookkeeping in the current HRU. The extracted
    source does not show a direct symbol from this module being referenced in the visible
    lines, so its role is likely to support the plant-community residue structures used here.
---

<!-- facts:header -->

Updates organic nitrogen and carbon pools in an HRU after runoff, erosion, and soil water redistribution. It also tallies carbon losses to surface runoff, sediment, lateral flow, and percolation.

## Bottom Line

This subroutine is the CSWAT==2 organic matter bookkeeping step for an HRU. It uses the day’s HRU erosion, sediment yield, surface runoff, and soil profile water/storage state to compute organic N removed from the surface layer and carbon moved out of or within the soil profile.

It matters because it keeps the soil and residue pools consistent with transport losses. The routine updates surface residue, humus, microbial biomass, and layer-by-layer carbon routing, and records the exported carbon in `hsc_d(j)` for later output or downstream accounting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU processing when `bsn_cc%cswat == 2`, after `hru_control` has already selected the CSWAT-C pathway and set the current HRU context. Its results feed later nutrient and carbon accounting by updating the HRU organic N output (`sedorgn`) and the carbon loss summaries in `hsc_d(j)`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select HRU and reset accumulators | Copies the active HRU index into `j` and clears the running lateral/percolation and conversion variables before any loss calculations begin. |
| 2. compute surface organic N basis | Builds `c_ly1` from surface humus and residue nitrogen, then computes `wt1` from surface bulk density and depth to convert the pool to a concentration basis. |
| 3. choose enrichment ratio | Uses the HRU-specific organic N enrichment ratio when it is available; otherwise falls back to the basin/day enrichment ratio `enratio`. |
| 4. compute organic N leaving the HRU | Calculates surface organic N concentration and converts it to `sedorgn(j)` using sediment yield and HRU area. |
| 5. scale surface N pools by loss fraction | When the surface N pool is nontrivial, computes the remaining fraction after export and multiplies the surface organic N pools and residue nitrogen by that ratio. |
| 6. prepare surface carbon loss terms | Resets carbon accumulators, recomputes total surface organic carbon, estimates surface soil mass, and derives the erosion fraction that will be used to remove carbon with sediment. |
| 7. remove surface carbon by erosion | Uses the erosion fraction to reduce surface total carbon, humus carbon, passive humus carbon, and each plant residue carbon pool. |
| 8. compute microbial carbon loss setup | If surface microbial carbon is present, reads the carbon-water coefficient, rebuilds total surface carbon, computes the microbial loss factor, and sums surface flow for the dissolved-carbon calculation. |
| 9. route microbial carbon through water and sediment | When flow is sufficient, computes microbial carbon loss from water movement, partitions it into vertical and horizontal concentrations, removes it from the surface microbial pool, and adds any erosion-linked microbial sediment loss. |
| 10. finalize surface carbon pools and outputs | Subtracts microbial sediment loss from the surface microbial pool, rebuilds total surface carbon, and stores surface-runoff, lateral, sediment, and percolation carbon outputs in `hsc_d(j)` and the first soil layer. |
| 11. process deeper layers | Loops through layers 2 through the bottom layer, computes carbon available for deeper-layer flow, routes it through percolation and lateral flow, updates microbial carbon remaining in each layer, and recomputes total and sequestered carbon for that layer. |
| 12. store lateral carbon total | Saves the accumulated lateral carbon from all layers in `hsc_d(j)%latq_c` for later output or accounting. |
| 13. return | Ends the HRU carbon and organic N update for the current call. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, sedorgn, surfq, sedyld, enratio` | `hru(j)%hyd%erorgn` |
| [sym:soil_module] | `soil` | `soil(j)%phys(1)%bd, soil(j)%phys(1)%d, soil(j)%phys(1)%rock, soil(j)%phys(1)%ul, soil(j)%ly(1)%flat, soil(j)%ly(1)%prk, soil(j)%ly(1)%latc, soil(j)%ly(1)%percc, soil(j)%nly, soil(j)%ly(ly)%prk, soil(j)%ly(ly)%flat, soil(j)%phys(ly)%thick, soil(j)%phys(ly)%wpmm, soil(j)%ly(ly)%latc, soil(j)%ly(ly)%percc` |
| [sym:organic_mineral_mass_module] | `soil1, pl_mass` | `soil1(j)%hp(1)%n, soil1(j)%hs(1)%n, pl_mass(j)%rsd_tot%n, soil1(j)%tot(1)%n, pl_mass(j)%rsd(1)%n, soil1(j)%meta(1)%n, soil1(j)%str(1)%n, soil1(j)%lig(1)%n, soil1(j)%tot(1)%c, soil1(j)%hp(1)%c, soil1(j)%hs(1)%c, soil1(j)%meta(1)%c, soil1(j)%str(1)%c, pl_mass(j)%rsd(ipl)%c, soil1(j)%microb(1)%c, soil1(j)%microb(ly)%c, soil1(j)%water(1)%c, soil1(j)%tot(ly)%c, soil1(j)%str(ly)%c, soil1(j)%meta(ly)%c, soil1(j)%hp(ly)%c, soil1(j)%hs(ly)%c, soil1(j)%seq(ly)%c` |
| [sym:carbon_module] | `cb_wtr_coef, hsc_d` | `cb_wtr_coef%prmt_21, cb_wtr_coef%prmt_44, hsc_d(j)%surq_c, hsc_d(j)%sed_c, hsc_d(j)%perc_c, hsc_d(j)%latq_c` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |
| [sym:plant_data_module] | `pcom and plant-community metadata` | `pcom(j)%npl` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sedorgn(j)` | After computing `sedorgn(j)` from surface organic nitrogen, enrichment ratio, sediment yield, and HRU area. | Stores the HRU’s organic nitrogen export with sediment for this event. |
| `soil1(j)%tot(1)%n` | When `c_ly1 > 1.e-6`, after the surface N loss fraction is computed. | Reduces total surface organic nitrogen to the remaining fraction after sediment export. |
| `soil1(j)%hs(1)%n` | When `c_ly1 > 1.e-6`, after the surface N loss fraction is computed. | Reduces the slow-humus nitrogen pool in the top layer by the same remaining fraction. |
| `soil1(j)%hp(1)%n` | When `c_ly1 > 1.e-6`, after the surface N loss fraction is computed. | Reduces the passive-humus nitrogen pool in the top layer by the same remaining fraction. |
| `pl_mass(j)%rsd(1)%n` | During the surface-pool update block when `c_ly1 > 1.e-6`. | Reduces the plant residue nitrogen pool in the surface layer by the remaining fraction after sediment export. |
| `soil1(j)%meta(1)%n` | When `c_ly1 > 1.e-6`, after the surface N loss fraction is computed. | Reduces metabolic litter nitrogen in the surface layer to match the remaining surface N. |
| `soil1(j)%str(1)%n` | When `c_ly1 > 1.e-6`, after the surface N loss fraction is computed. | Reduces structural litter nitrogen in the surface layer to match the remaining surface N. |
| `soil1(j)%lig(1)%n` | When `c_ly1 > 1.e-6`, after the surface N loss fraction is computed. | Reduces lignin nitrogen in the surface layer to match the remaining surface N. |
| `soil1(j)%tot(1)%c` | Immediately before and after the erosion-loss calculation on the surface layer. | Recomputes total surface organic carbon and then reduces it by the sediment erosion fraction. |
| `soil1(j)%hs(1)%c` | After the erosion fraction is computed for the surface layer. | Reduces slow-humus carbon in the surface layer by the sediment erosion fraction. |
| `soil1(j)%hp(1)%c` | After the erosion fraction is computed for the surface layer. | Reduces passive-humus carbon in the surface layer by the sediment erosion fraction. |
| `pl_mass(j)%rsd(ipl)%c` | During the erosion-loss loop over all plants in the community. | Reduces each plant’s surface residue carbon by the fraction of soil lost to erosion. |
| `soil1(j)%microb(1)%c` | When surface microbial carbon exceeds the small threshold and the water-loss block runs. | Reduces surface microbial carbon by the amount lost to runoff and percolation. |
| `hsc_d(j)%surq_c` | After the surface dissolved-carbon loss is computed from microbial carbon. | Stores the carbon leaving the surface with runoff/lateral flow in the HRU carbon-loss summary. |
| `soil(j)%ly(1)%latc` | After the surface dissolved-carbon loss is computed. | Stores the lateral-flow carbon leaving the first soil layer. |
| `soil(j)%ly(1)%percc` | After the surface dissolved-carbon loss is computed. | Stores the percolating carbon leaving the first soil layer. |
| `hsc_d(j)%sed_c` | After the surface erosion and microbial sediment losses are computed. | Stores the carbon leaving with sediment for the current HRU. |
| `soil(j)%ly(ly)%latc` | Inside the deeper-layer loop for each layer `ly = 2, soil(j)%nly`. | Stores the lateral carbon routed through each deeper layer. |
| `soil(j)%ly(ly)%percc` | Inside the deeper-layer loop for each layer `ly = 2, soil(j)%nly`. | Stores the percolating carbon routed through each deeper layer. |
| `soil1(j)%microb(ly)%c` | Inside the deeper-layer loop when carbon is routed downward into the layer’s microbial pool. | Updates microbial carbon remaining in the layer after vertical transfer. |
| `hsc_d(j)%perc_c` | Inside the deeper-layer loop when carbon is routed downward. | Stores the percolating carbon reaching the HRU carbon summary. |
| `soil1(j)%tot(ly)%c` | Inside each deeper-layer loop iteration after layer carbon pools are adjusted. | Recomputes the total organic carbon pool for the current layer from structural, metabolic, humus, and microbial carbon. |
| `soil1(j)%seq(ly)%c` | Inside each deeper-layer loop iteration after layer carbon pools are adjusted. | Recomputes the sequestered carbon pool for the current layer from passive humus, slow humus, and microbial carbon. |
| `hsc_d(j)%latq_c` | After the deeper-layer loop accumulates lateral carbon across all layers. | Stores the total lateral carbon exported from the HRU profile. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved five commits that changed `nut_orgnc2`. In 72206bc, the routine switched to `plant_data_module`, added `ipl` as a loop variable, changed surface organic N basis from separate residue terms to `pl_mass(j)%rsd_tot%n`, and started scaling plant residue carbon through `pl_mass(j)%rsd(ipl)%c`. In 15bb350, the hard-coded carbon coefficients were replaced by `cb_wtr_coef%prmt_21` and `cb_wtr_coef%prmt_44`. In 081ff2e, the routine began recomputing total carbon and introduced deeper-layer total/sequestered carbon handling. In 17eb341, the surface sequestered carbon reset was removed so nonzero surface sequestration could persist. In 2d106f8, the deeper-layer loop began writing `soil1(j)%seq(k)%c` as passive plus slow humus plus microbial carbon.

- 72206bc: moved residue handling to the plant-community mass structure, added the plant loop index `ipl`, and changed the surface organic-N/carbon basis to use `pl_mass(j)%rsd_tot%n` and `pl_mass(j)%rsd(ipl)%c`.
- 15bb350: replaced fixed `prmt_21`/`prmt_44` assignments with values read from `cb_wtr_coef`, making carbon-loss routing use configurable coefficients.
- 081ff2e: added explicit recomputation of `soil1(j)%tot(1)%c` and began separating total carbon from sequestered carbon in deeper layers.
- 17eb341: stopped zeroing `soil1(j)%seq(1)%c`, preserving surface-layer sequestered carbon output.
- 2d106f8: populated `soil1(j)%seq(k)%c` for deeper layers and documented the layer sequestration output behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_orgnc2' has no extracted documentation comment.
- The extracted source header still describes organic nitrogen removal in runoff even though the body also performs substantial carbon routing and sequestration bookkeeping.
- The visible source contains `plant_data_module` use but no directly resolved symbol from that module in the extracted lines; its role is inferred from the residue/plant-community handling.
