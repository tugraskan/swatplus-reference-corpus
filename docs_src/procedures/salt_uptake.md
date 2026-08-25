---
kind: procedure
symbol: salt_uptake
title: salt_uptake
status: filled
source_hash: 9c4078cf8d542117
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; it selects the current landscape object and is used to
    index plant, soil, salt-balance, and area state for the active HRU.
  idp: Plant database ID taken from `pcom(j)%plcur(1)%idplt`; it chooses the plant-specific
    daily salt uptake demand from `salt_uptake_kg(idp,isalt)`.
  jj: Soil-layer loop counter; it walks through `soil(j)%nly` layers while computing root
    fractions and then applying salt uptake layer by layer.
  isalt: Salt-ion loop counter; it iterates over the configured salts in `cs_db%num_salts`.
  depth: Running depth to the bottom of the current soil layer, accumulated from `soil(j)%phys(jj)%thick`
    and compared to root depth.
  rd: Current rooting depth in mm copied from `pcom(j)%plg(1)%root_dep`; it defines how much
    of the soil profile can receive root mass and uptake allocation.
  rm: Total root mass for the HRU in kg, computed from per-area root mass times `ob(j)%area_ha`;
    it is the basis for converting layer root mass into fractions.
  rm_layer: Root mass assigned to the current soil layer in kg; it is computed from `rm` and
    the layer’s overlap with rooting depth, then converted to a fraction if positive.
  rm_fract: Array of per-layer root-mass fractions; each element stores `rm_layer / rm` for
    a soil layer and is later used to apportion salt uptake by layer.
  uptake_mass: Per-layer salt uptake in kg/ha; it starts from the plant’s daily salt uptake
    demand for the ion and is reduced if the soil layer does not contain enough salt.
uses:
  basin_module: This module is imported here, so its basin-level state can influence the broader
    simulation context in which the HRU salt balances are updated, even though no specific
    symbol was extracted from it for this routine.
  organic_mineral_mass_module: It provides `pl_mass`, including `pl_mass(j)%root(1)%m`, which
    supplies the current root mass needed to decide whether uptake can occur and to compute
    the root fraction by layer.
  hru_module: It provides `ihru`, which identifies the active HRU so the routine can select
    the correct plant, soil, and salt-balance records.
  hydrograph_module: It provides `ob(j)%area_ha`, which converts per-hectare root mass to
    total HRU root mass so the uptake allocation matches the actual object area.
  output_landscape_module: This module is imported for landscape output/state context; it
    matters because salt uptake is part of the HRU landscape mass accounting that later output
    routines may report.
  salt_module: It provides `hsaltb_d(j)%salt(isalt)%uptk` and `salt_uptake_kg`, the first
    to accumulate daily root uptake by salt ion and the second to supply the plant-specific
    daily uptake demand used in the allocation.
  constituent_mass_module: It provides `cs_db%num_salts` to control the salt-ion loop and
    `cs_soil(j)%ly(jj)%salt(isalt)` to read and reduce the available salt mass in each soil
    layer.
  plant_data_module: This module is imported because the plant-specific uptake demand table
    and related plant data are part of the routine’s plant-dependent salt allocation logic,
    even though no direct symbol from the module was separately resolved beyond the plant-state
    references already captured.
  plant_module: It provides `pcom`, including `pcom(j)%plcur(1)%idplt` and `pcom(j)%plg(1)%root_dep`;
    these determine the plant identity and rooting depth that control whether uptake runs
    and how uptake is split among layers.
  soil_module: It provides `soil`, including `soil(j)%nly` and `soil(j)%phys(jj)%thick`; these
    define how many layers are processed and how each layer’s thickness contributes to root
    distribution and salt depletion.
---

<!-- facts:header -->

Computes daily salt uptake from the root zone for the current HRU. It allocates a specified crop salt uptake across soil layers by root fraction, caps uptake by available soil salt, and updates salt balance state.

## Bottom Line

This routine runs for the current HRU and only does work when the plant has both positive root depth and positive root mass. It uses the plant’s rooting depth, the HRU area, the soil layer thicknesses, and the configured daily salt uptake demand to distribute salt uptake across layers and salt ions.

For each salt ion and soil layer, it computes an uptake amount from `salt_uptake_kg(idp,isalt)` scaled by the layer root fraction, limits that uptake to the salt mass present in `cs_soil(j)%ly(jj)%salt(isalt)`, adds the accepted amount to the daily salt balance `hsaltb_d(j)%salt(isalt)%uptk`, and subtracts it from soil storage. The result is a depletion of soil salt and a matching crop uptake balance entry for downstream mass accounting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `pl_biomass_gro` after nutrient uptake routines and only when `cs_db%num_salts > 0` and `salt_uptake_on == 1`. It depends on the plant growth state, plant mass, soil profile, and salt inventory already being set up for the current HRU, and its updated `hsaltb_d` and `cs_soil` values feed later daily mass-balance accounting and any output that reports salt uptake or soil salt depletion.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. assign HRU and plant identity | The routine copies the active HRU index from `ihru` into `j` and reads the plant database ID from `pcom(j)%plcur(1)%idplt` so the correct plant and HRU state can be used for uptake calculations. |
| 2. test whether uptake is possible | It proceeds only if the plant has positive rooting depth and positive root mass; otherwise, no salt uptake is computed for this HRU. |
| 3. initialize root-depth variables | The routine stores root depth in `rd`, converts per-area root mass to total HRU root mass in `rm`, resets cumulative layer depth to zero, and clears the root-fraction array before layer processing begins. |
| 4. distribute root mass across soil layers | For each soil layer, it accumulates layer thickness into `depth`, computes the amount of root mass assigned to that layer based on whether the layer lies fully or partially within the rooting depth, and stores the resulting fraction in `rm_fract(jj)` when positive. |
| 5. loop over salt ions | After the root distribution is known, the routine iterates over every simulated salt ion using `cs_db%num_salts`. |
| 6. loop over soil layers for each salt ion | For each salt ion, it walks through all soil layers and computes the layer uptake demand by multiplying the plant’s prescribed daily salt uptake for that ion by the layer root fraction. |
| 7. cap uptake by available soil salt | If the computed uptake exceeds the salt mass present in `cs_soil(j)%ly(jj)%salt(isalt)`, the uptake is reduced to the available soil salt so the routine does not remove more salt than exists. |
| 8. update daily balance and soil storage | The accepted uptake is added to `hsaltb_d(j)%salt(isalt)%uptk` and subtracted from `cs_soil(j)%ly(jj)%salt(isalt)` to record crop uptake and reduce soil salt storage. |
| 9. finish the guarded computation | If the rooting-depth test failed, or after all salts and layers are processed, the subroutine returns to the caller without additional side effects. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` |  |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%root(1)%m` |
| [sym:hru_module] | `ihru` |  |
| [sym:hydrograph_module] | `ob` | `ob(j)%area_ha` |
| [sym:output_landscape_module] | `output_landscape_module` |  |
| [sym:salt_module] | `hsaltb_d, salt_uptake_kg` | `hsaltb_d(j)%salt(isalt)%uptk` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_salts, cs_soil(j)%ly(jj)%salt(isalt)` |
| [sym:plant_data_module] | `plant_data_module` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(1)%idplt, pcom(j)%plg(1)%root_dep` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(jj)%thick` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hsaltb_d(j)%salt(isalt)%uptk` | When the HRU has positive root depth and root mass, and for each salt ion and soil layer after uptake is capped by the available soil salt. | `hsaltb_d(j)%salt(isalt)%uptk` accumulates the amount of salt taken up by roots for the current day and HRU. It increases by the accepted `uptake_mass` for each layer so the daily salt balance records total crop uptake by ion. |
| `cs_soil(j)%ly(jj)%salt(isalt)` | When uptake is computed for a soil layer and salt ion, after any cap to the available soil salt has been applied. | `cs_soil(j)%ly(jj)%salt(isalt)` is reduced by the accepted uptake mass, representing depletion of salt from that soil layer’s stored salt pool. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `salt_uptake`: df07e3f added the routine with root-depth checking, layer-wise root-fraction logic, and salt uptake subtraction from soil; 35b029c made only a formatting/end-statement adjustment; bd18ad4 removed the unused `ep_day` import and commented out unused local declarations for `irrig_mass`, `uptake_mass_total`, and `dum`; 39fabde initialized local variables with default values and fixed an indentation line in the root-fraction block.

- df07e3f introduced the full salt-uptake algorithm and the `hsaltb_d`/`cs_soil` state updates.
- 35b029c only changed trailing source formatting and did not alter behavior.
- bd18ad4 removed an unused `hru_module` import and commented out unused locals, leaving the runtime logic unchanged.
- 39fabde added explicit initial values to local variables and corrected indentation in the layer root-fraction section; the core calculations stayed the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_uptake' has no extracted documentation comment.
