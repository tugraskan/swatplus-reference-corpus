---
kind: procedure
symbol: cs_sorb_hru
title: cs_sorb_hru
status: filled
source_hash: 0a576d14e5f1f5ec
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru` so the subroutine works on the current hydrologic response
    unit.
  jj: Loop index for soil layers within the current HRU.
  cseo4: Current dissolved selenate concentration in soil water for the active layer, read
    from `cs_soil(j)%ly(jj)%csc(1)` in mg/L before equilibrium is recomputed.
  cseo3: Current dissolved selenite concentration in soil water for the active layer, read
    from `cs_soil(j)%ly(jj)%csc(2)` in mg/L before equilibrium is recomputed.
  cborn: Current dissolved boron concentration in soil water for the active layer, read from
    `cs_soil(j)%ly(jj)%csc(3)` in mg/L before equilibrium is recomputed.
  ccseo4: Current sorbed selenate concentration for the active layer, read from `cs_soil(j)%ly(jj)%csc_sorb(1)`
    in mg/kg before recomputing equilibrium.
  ccseo3: Current sorbed selenite concentration for the active layer, read from `cs_soil(j)%ly(jj)%csc_sorb(2)`
    in mg/kg before recomputing equilibrium.
  ccborn: Current sorbed boron concentration for the active layer, read from `cs_soil(j)%ly(jj)%csc_sorb(3)`
    in mg/kg before recomputing equilibrium.
  hru_area_m2: Current HRU area converted from hectares to square meters, used to compute
    soil and water volumes.
  water_volume: Volume of water stored in the current soil layer, computed from `soil(j)%phys(jj)%st`
    and HRU area.
  mass_seo4_sol: Mass of dissolved selenate in the current layer, expressed in mg before and
    after the equilibrium update.
  mass_seo3_sol: Mass of dissolved selenite in the current layer, expressed in mg before and
    after the equilibrium update.
  mass_born_sol: Mass of dissolved boron in the current layer, expressed in mg before and
    after the equilibrium update.
  mass_seo4_sorb: Mass of sorbed selenate in the current layer, expressed in mg before and
    after the equilibrium update.
  mass_seo3_sorb: Mass of sorbed selenite in the current layer, expressed in mg before and
    after the equilibrium update.
  mass_born_sorb: Mass of sorbed boron in the current layer, expressed in mg before and after
    the equilibrium update.
  sol_thick: Thickness of the current soil layer, used to derive layer volume and soil mass.
  volume: Geometric volume of the current soil layer in cubic meters, used in sorption and
    concentration conversions.
  ratio: Diagnostic ratio of sorbed to dissolved concentration after the update; the code
    notes it should equal the Kd value.
  mass_total: Total constituent mass in the current layer before equilibrium is split between
    solution and sorbed pools.
  val_num: Intermediate numerator used to form the equilibrium denominator term from Kd, soil
    volume, and bulk density.
  val_den: Intermediate denominator term equal to the water volume in milliliters used in
    the equilibrium calculation.
  val: Intermediate factor for solving the two-equation mass balance between dissolved and
    sorbed phases.
  cseo4_new: Updated dissolved selenate concentration in mg/L after enforcing Kd and mass
    conservation.
  ccseo4_new: Updated sorbed selenate concentration in mg/kg after enforcing Kd and mass conservation.
  cseo3_new: Updated dissolved selenite concentration in mg/L after enforcing Kd and mass
    conservation.
  ccseo3_new: Updated sorbed selenite concentration in mg/kg after enforcing Kd and mass conservation.
  cborn_new: Updated dissolved boron concentration in mg/L after enforcing Kd and mass conservation.
  ccborn_new: Updated sorbed boron concentration in mg/kg after enforcing Kd and mass conservation.
  soil_volume: Physical soil volume for the current layer in cubic meters, derived from HRU
    area and layer thickness.
  soil_mass: Mass of soil in the current layer in kilograms, derived from soil volume and
    bulk density.
  sorbed_seo4: Layer sorbed selenate concentration in kg/ha before conversion to mg/kg and
    equilibrium update.
  sorbed_seo3: Layer sorbed selenite concentration in kg/ha before conversion to mg/kg and
    equilibrium update.
  sorbed_born: Layer sorbed boron concentration in kg/ha before conversion to mg/kg and equilibrium
    update.
  mass_seo4_before: Running total of dissolved selenate mass before sorption equilibrium updates
    across all layers.
  mass_seo4_after: Running total of dissolved selenate mass after sorption equilibrium updates
    across all layers.
  mass_seo3_before: Running total of dissolved selenite mass before sorption equilibrium updates
    across all layers.
  mass_seo3_after: Running total of dissolved selenite mass after sorption equilibrium updates
    across all layers.
  mass_born_before: Running total of dissolved boron mass before sorption equilibrium updates
    across all layers.
  mass_born_after: Running total of dissolved boron mass after sorption equilibrium updates
    across all layers.
uses:
  hru_module: The current HRU index and its area determine which landscape object is updated
    and provide the spatial scale for converting between per-layer masses, per-hectare masses,
    and absolute masses.
  soil_module: Soil layer count, thickness, bulk density, and stored water content define
    the volume and mass of each layer, which are required to convert concentrations into masses
    and back during the sorption equilibrium update.
  organic_mineral_mass_module: This module carries the per-HRU, per-layer constituent state
    that the routine reads, updates, and converts between dissolved, sorbed, and areal-mass
    forms.
  constituent_mass_module: These structures hold the soil-layer constituent concentrations
    and masses that are directly recalculated here for selenate, selenite, and boron.
  cs_module: This module stores the HRU-level sorption mass balance output; the routine writes
    the net sorbed transfer for each constituent into `hcsb_d(j)%cs(:)%sorb`.
  cs_data_module: The Kd values in this module control how much of each constituent partitions
    between soil water and the sorbed phase in every layer.
---

<!-- facts:header -->

Updates selenium and boron sorption equilibrium in each soil layer of the current HRU. It converts between solution concentration, sorbed concentration, and per-area mass while conserving total constituent mass.

## Bottom Line

This routine recalculates soil-layer constituent state for selenium as selenate, selenite, and boron after sorption. For each HRU layer it uses soil water content, bulk density, layer thickness, and the layer-specific Kd values to convert between mg/L, mg/kg, and kg/ha, then writes the updated concentrations back to `cs_soil`.

It also tallies the change in sorbed mass across the soil profile and stores that transfer in `hcsb_d(j)%cs(:)%sorb` for later balance reporting. The final loop converts the updated sorbed concentrations back to the kg/ha form used by later HRU transport calculations such as `se_sed`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU chemistry processing after `cs_rctn_hru` and before later soil/transport calculations. `hru_control` calls it when constituent chemistry is enabled, and its updated layer concentrations and sorption balance feed later HRU transport behavior, including the soil-transport calculations that use `cs_soil` state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set current HRU and area | Copy the active HRU index from `ihru` into `j` and convert the HRU area from hectares to square meters for layer-volume calculations. |
| 2. convert sorbed kg/ha to mg/kg | Loop through every soil layer, compute layer soil mass from thickness and bulk density, and convert existing sorbed selenate, selenite, and boron from kg/ha to mg/kg so the equilibrium solve uses concentration units consistent with Kd. |
| 3. reset mass-balance accumulators | Initialize running totals that track dissolved mass before and after the equilibrium update for each constituent across all layers. |
| 4. read layer concentrations | For each soil layer, load the current dissolved concentrations and sorbed concentrations for selenate, selenite, and boron from `cs_soil`. |
| 5. compute current masses | Compute dissolved mass from soil-water volume and sorbed mass from layer volume and bulk density so the routine can conserve total mass during the Kd-based redistribution. |
| 6. solve selenate equilibrium | Use the selenate Kd value and the conserved total mass to solve new dissolved and sorbed masses, convert them back to mg/L and mg/kg, store them in `cs_soil`, and update the layer selenate mass in kg/ha. |
| 7. solve selenite equilibrium | Repeat the same Kd-based mass-conserving solve for selenite, then write the updated dissolved, sorbed, and areal-mass values back to `cs_soil`. |
| 8. solve boron equilibrium | Repeat the Kd-based mass-conserving solve for boron and store the updated concentrations and areal mass in the soil-layer state. |
| 9. store sorption transfer | Write the net change in dissolved mass across the profile to `hcsb_d(j)%cs(1:3)%sorb` as kg/ha transfer values for the three constituents. |
| 10. convert sorbed mg/kg back to kg/ha | Loop through the soil layers again and convert the updated sorbed concentrations from mg/kg back to kg/ha so later HRU transport routines can use the areal mass form. |
| 11. return | Exit after the soil-layer constituent states and sorption balance outputs have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, ihru` | `hru(j)%area_ha` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(jj)%thick, soil(j)%phys(jj)%bd, soil(j)%phys(jj)%st` |
| [sym:organic_mineral_mass_module] | `cs_soil` | `cs_soil(j)%ly(jj)%cs_sorb(1), cs_soil(j)%ly(jj)%cs_sorb(2), cs_soil(j)%ly(jj)%cs_sorb(3), cs_soil(j)%ly(jj)%csc_sorb(1), cs_soil(j)%ly(jj)%csc_sorb(2), cs_soil(j)%ly(jj)%csc_sorb(3), cs_soil(j)%ly(jj)%csc(1), cs_soil(j)%ly(jj)%csc(2), cs_soil(j)%ly(jj)%csc(3), cs_soil(j)%ly(jj)%cs(1), cs_soil(j)%ly(jj)%cs(2), cs_soil(j)%ly(jj)%cs(3)` |
| [sym:constituent_mass_module] | `cs_soil` | `cs_soil(j)%ly(jj)%cs_sorb(1), cs_soil(j)%ly(jj)%cs_sorb(2), cs_soil(j)%ly(jj)%cs_sorb(3), cs_soil(j)%ly(jj)%csc_sorb(1), cs_soil(j)%ly(jj)%csc_sorb(2), cs_soil(j)%ly(jj)%csc_sorb(3), cs_soil(j)%ly(jj)%csc(1), cs_soil(j)%ly(jj)%csc(2), cs_soil(j)%ly(jj)%csc(3), cs_soil(j)%ly(jj)%cs(1), cs_soil(j)%ly(jj)%cs(2), cs_soil(j)%ly(jj)%cs(3)` |
| [sym:cs_module] | `hcsb_d` | `hcsb_d(j)%cs(1)%sorb, hcsb_d(j)%cs(2)%sorb, hcsb_d(j)%cs(3)%sorb` |
| [sym:cs_data_module] | `cs_rct_soil` | `cs_rct_soil(j)%kd_seo4, cs_rct_soil(j)%kd_seo3, cs_rct_soil(j)%kd_born` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(j)%ly(jj)%csc_sorb(1)` | When the routine converts existing sorbed selenate from kg/ha to mg/kg, then later recomputes equilibrium in each soil layer. | `cs_soil(j)%ly(jj)%csc_sorb(1)` is updated to the new sorbed selenate concentration that satisfies the layer Kd relation and mass conservation. |
| `cs_soil(j)%ly(jj)%csc_sorb(2)` | When the routine converts existing sorbed selenite from kg/ha to mg/kg, then later recomputes equilibrium in each soil layer. | `cs_soil(j)%ly(jj)%csc_sorb(2)` is updated to the new sorbed selenite concentration that satisfies the layer Kd relation and mass conservation. |
| `cs_soil(j)%ly(jj)%csc_sorb(3)` | When the routine converts existing sorbed boron from kg/ha to mg/kg, then later recomputes equilibrium in each soil layer. | `cs_soil(j)%ly(jj)%csc_sorb(3)` is updated to the new sorbed boron concentration that satisfies the layer Kd relation and mass conservation. |
| `cs_soil(j)%ly(jj)%csc(1)` | After the selenate equilibrium solve for each soil layer. | `cs_soil(j)%ly(jj)%csc(1)` is replaced with the updated dissolved selenate concentration in soil water, in mg/L. |
| `cs_soil(j)%ly(jj)%cs(1)` | After the selenate equilibrium solve for each soil layer. | `cs_soil(j)%ly(jj)%cs(1)` is updated to the layer's dissolved selenate mass expressed as kg/ha for later HRU transport calculations. |
| `cs_soil(j)%ly(jj)%csc(2)` | After the selenite equilibrium solve for each soil layer. | `cs_soil(j)%ly(jj)%csc(2)` is replaced with the updated dissolved selenite concentration in soil water, in mg/L. |
| `cs_soil(j)%ly(jj)%cs(2)` | After the selenite equilibrium solve for each soil layer. | `cs_soil(j)%ly(jj)%cs(2)` is updated to the layer's dissolved selenite mass expressed as kg/ha for later HRU transport calculations. |
| `cs_soil(j)%ly(jj)%csc(3)` | After the boron equilibrium solve for each soil layer. | `cs_soil(j)%ly(jj)%csc(3)` is replaced with the updated dissolved boron concentration in soil water, in mg/L. |
| `cs_soil(j)%ly(jj)%cs(3)` | After the boron equilibrium solve for each soil layer. | `cs_soil(j)%ly(jj)%cs(3)` is updated to the layer's dissolved boron mass expressed as kg/ha for later HRU transport calculations. |
| `hcsb_d(j)%cs(1)%sorb` | After accumulating dissolved-mass totals across all layers. | `hcsb_d(j)%cs(1)%sorb` stores the net selenate mass transferred by sorption over the HRU profile, normalized to kg/ha. |
| `hcsb_d(j)%cs(2)%sorb` | After accumulating dissolved-mass totals across all layers. | `hcsb_d(j)%cs(2)%sorb` stores the net selenite mass transferred by sorption over the HRU profile, normalized to kg/ha. |
| `hcsb_d(j)%cs(3)%sorb` | After accumulating dissolved-mass totals across all layers. | `hcsb_d(j)%cs(3)%sorb` stores the net boron mass transferred by sorption over the HRU profile, normalized to kg/ha. |
| `cs_soil(j)%ly(jj)%cs_sorb(1)` | After converting the updated sorbed selenate concentration back from mg/kg to kg/ha in the final layer loop. | `cs_soil(j)%ly(jj)%cs_sorb(1)` is refreshed to the areal sorbed selenate mass used by later soil transport routines. |
| `cs_soil(j)%ly(jj)%cs_sorb(2)` | After converting the updated sorbed selenite concentration back from mg/kg to kg/ha in the final layer loop. | `cs_soil(j)%ly(jj)%cs_sorb(2)` is refreshed to the areal sorbed selenite mass used by later soil transport routines. |
| `cs_soil(j)%ly(jj)%cs_sorb(3)` | After converting the updated sorbed boron concentration back from mg/kg to kg/ha in the final layer loop. | `cs_soil(j)%ly(jj)%cs_sorb(3)` is refreshed to the areal sorbed boron mass used by later soil transport routines. |

## File I/O

<!-- facts:io -->


## Lineage

`cs_sorb_hru` was introduced in commit `df07e3f` with the initial sorption-equilibrium implementation. Commit `39fabde` did not alter the algorithm; it only initialized the local variables to zero. Commit `2ee1889` made a small source-text cleanup by changing the closing statement from `end` to `end subroutine cs_sorb_hru` and removing an extra blank line.

- df07e3f added the full HRU sorption routine: layer-by-layer conversion of sorbed mass to mg/kg, Kd-based mass-conserving updates for selenate, selenite, and boron, balance writes to `hcsb_d`, and conversion back to kg/ha.
- 39fabde changed only local declarations by assigning zero initial values to the scalars; the computational steps and outputs stayed the same.
- 2ee1889 made a non-behavioral source cleanup, replacing the plain `end` with `end subroutine cs_sorb_hru`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_sorb_hru' has no extracted documentation comment.
