---
kind: procedure
symbol: cs_uptake
title: cs_uptake
status: filled
source_hash: ba32ae313aa55381
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index for the active landscape object. It is loaded from `ihru` and used
    to access plant, soil, constituent, and hydrograph state for that HRU.
  idp: Plant database identifier for the current HRU's plant community. It is taken from `pcom(j)%plcur(1)%idplt`
    and used to select the corresponding daily uptake demand in `cs_uptake_kg(idp,ics)`.
  jj: Soil-layer loop counter. It is used first to build layer root fractions and then to
    apply constituent uptake to each soil layer.
  ics: Constituent loop counter. It selects each simulated constituent in `cs_db%num_cs` so
    uptake and soil depletion are handled one constituent at a time.
  depth: Running cumulative soil depth to the bottom of the current layer. It is updated with
    each layer thickness to decide whether the layer is fully or partially within rooting
    depth.
  rd: Current root depth of the plant canopy in millimeters. It is copied from `pcom(j)%plg(1)%root_dep`
    and controls how much of each soil layer is considered rooted.
  rm: Total root mass for the HRU, converted from kg/ha to kg using `ob(j)%area_ha`. It provides
    the total mass that is partitioned into layer fractions.
  rm_layer: Root mass assigned to the current soil layer. It is calculated from total root
    mass and layer/root-depth overlap, then used to form the per-layer fraction `rm_fract(jj)`.
  rm_fract: Per-layer fraction of total root mass. Each element is set from `rm_layer / rm`
    for rooted layers and later scales daily constituent uptake into each soil layer.
  uptake_mass: Constituent mass taken up from the current layer for the current constituent,
    in kg/ha. It starts from the prescribed daily uptake demand times the layer root fraction
    and is capped by available soil constituent mass.
uses:
  basin_module: The routine is compiled against basin-level model state even though no specific
    basin symbol was resolved from the extracted references. That shared basin context is
    part of the global SWAT+ state environment in which HRU-level uptake is evaluated.
  organic_mineral_mass_module: '`pl_mass(j)%root(1)%m` supplies the current root biomass used
    to scale how much of the prescribed constituent uptake should be assigned to the current
    HRU''s rooted soil profile.'
  hru_module: '`ihru` identifies which HRU''s plant, soil, and constituent arrays are being
    updated, so the routine can map the current call to the correct spatial object.'
  hydrograph_module: '`ob(j)%area_ha` converts root mass from a per-hectare basis to total
    mass for the HRU, which is needed before distributing uptake across soil layers.'
  output_landscape_module: This module is part of the landscape output/state environment that
    accompanies HRU processing. It matters here because `cs_uptake` runs inside the landscape
    plant-growth workflow that maintains HRU-scale accounting, even though no specific output_landscape
    symbol was extracted.
  cs_module: '`hcsb_d(j)%cs(ics)%uptk` is the daily constituent-balance accumulator for the
    HRU. `cs_uptake` adds the taken-up mass there so later mass-balance reporting can include
    crop uptake.'
  constituent_mass_module: '`cs_db%num_cs` controls how many constituents are processed, and
    `cs_soil(j)%ly(jj)%cs(ics)` is the soil storage that gets depleted by uptake, so this
    module defines both the loop bounds and the mutable soil constituent state.'
  plant_data_module: This module holds plant database information used in the plant-growth
    sequence. `cs_uptake` depends on plant identity and uptake demand derived from that plant-data
    context, even though the extracted references do not isolate a specific symbol from this
    module.
  plant_module: '`pcom(j)%plcur(1)%idplt` identifies the active plant, and `pcom(j)%plg(1)%root_dep`
    gives the current rooting depth. Together they determine both the uptake lookup key and
    the root-zone depth distribution used in the calculation.'
  soil_module: '`soil(j)%nly` sets the number of layers to inspect, and `soil(j)%phys(jj)%thick`
    gives each layer thickness used to accumulate depth and determine whether the layer is
    fully or partially within the root zone.'
---

<!-- facts:header -->

Calculates root-zone constituent uptake for the current HRU and subtracts that uptake from soil-layer constituent mass. It also accumulates the taken-up mass in the HRU daily constituent balance.

## Bottom Line

This subroutine distributes a prescribed daily constituent uptake amount across the soil layers reached by plant roots. It uses the plant's rooting depth and root mass to build a layer-by-layer root fraction, then applies that fraction to `cs_uptake_kg(idp,ics)` for each simulated constituent.

For each layer, uptake is capped at the constituent mass actually present in `cs_soil(j)%ly(jj)%cs(ics)`. The routine adds the removed mass to `hcsb_d(j)%cs(ics)%uptk` and subtracts it from soil storage, so later carbon/constituent balance accounting and soil-state updates see the depletion.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during plant biomass growth for an HRU, after the plant-growth routine has established current plant state such as root depth and after `pl_biomass_gro` has already called nutrient uptake routines. If `cs_db%num_cs > 0`, `pl_biomass_gro` invokes `cs_uptake`, and the resulting soil depletion and `hcsb_d` uptake totals feed the later daily constituent mass balance and soil-state calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select HRU and plant | Load the active HRU index from `ihru` and fetch the plant database id from `pcom(j)%plcur(1)%idplt` so subsequent calculations target the correct plant community. |
| 2. require roots | Proceed only when the plant has positive rooting depth and positive root mass; otherwise, skip the uptake calculation entirely. |
| 3. initialize root-zone metrics | Copy rooting depth, convert root mass from kg/ha to total kg using HRU area, and reset cumulative depth and root-fraction storage before layer processing. |
| 4. build layer root fractions | Walk through each soil layer, accumulate layer thickness into depth, compute how much root mass lies in that layer based on whether the layer is fully or partially within rooting depth, and store the layer fraction when root mass is positive. |
| 5. loop over constituents | For each simulated constituent and each soil layer, compute the layer-specific uptake amount using the prescribed daily uptake rate scaled by the layer root fraction. |
| 6. cap by available soil mass | Limit uptake to the mass actually present in `cs_soil(j)%ly(jj)%cs(ics)` so the routine cannot remove more constituent than exists in the soil layer. |
| 7. record balance and deplete soil | Add the taken-up mass to the HRU daily constituent balance accumulator and subtract the same mass from the soil-layer constituent storage. |
| 8. return | Exit after all eligible HRU, layer, and constituent updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state` |  |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%root(1)%m` |
| [sym:hru_module] | `ihru` |  |
| [sym:hydrograph_module] | `ob` | `ob(j)%area_ha` |
| [sym:output_landscape_module] | `output_landscape_module state` |  |
| [sym:cs_module] | `hcsb_d, cs_uptake_kg` | `hcsb_d(j)%cs(ics)%uptk` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_cs, cs_soil(j)%ly(jj)%cs(ics)` |
| [sym:plant_data_module] | `plant_data_module state` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(1)%idplt, pcom(j)%plg(1)%root_dep` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(jj)%thick` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hcsb_d(j)%cs(ics)%uptk` | When the HRU has positive root depth and root mass, and for each constituent-layer pair after uptake is limited by available soil mass. | `hcsb_d(j)%cs(ics)%uptk` increases by the amount taken up from each soil layer. This preserves the daily crop-uptake total for constituent mass balance reporting. |
| `cs_soil(j)%ly(jj)%cs(ics)` | When the same uptake calculation runs for a layer and constituent, after capping uptake at available mass. | `cs_soil(j)%ly(jj)%cs(ics)` is reduced by the uptake amount, removing constituent mass from the soil water/storage pool so later processes see the depleted state. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `cs_uptake`. The original addition in `df07e3f` introduced the routine, its purpose comment, module dependencies, root-zone distribution logic, and per-layer constituent uptake update. Commit `94b6dec` imported the source from Bitbucket and already contained the same algorithm structure. Commit `39fabde` initialized local variables with default values and adjusted formatting around the `rm_fract` assignment and final `end subroutine` line. Commit `2ee1889` removed the unused `ep_day` import from `hru_module`, trimmed the local declarations by dropping unused variables, and left the uptake logic unchanged.

- df07e3f introduced `cs_uptake` with root-depth-based distribution of `cs_uptake_kg(idp,ics)` across soil layers and updates to `hcsb_d(j)%cs(ics)%uptk` and `cs_soil(j)%ly(jj)%cs(ics)`.
- 39fabde initialized local scalars/arrays to zero and did not change the uptake algorithm, aside from formatting cleanup.
- 2ee1889 removed the unused `ep_day` import and some unused local declarations, without changing the mass-balance calculations.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_uptake' has no extracted documentation comment.
