---
kind: procedure
symbol: salt_lch
title: salt_lch
status: filled
source_hash: 294201a7cf9e042a
version_label: SWAT+ 62.0.0
locals:
  j: HRU index for the profile currently being processed; it is set from ihru and used to
    access the active HRU's soil, hydrologic, and salt-state arrays.
  jj: Soil-layer loop counter. It steps through each layer in the current HRU while salt is
    added, removed, and re-concentrated.
  isalt: Salt-ion loop counter. It indexes the simulated salt constituent being processed
    within each soil layer.
  sol_index: Offset index into the groundwater solute transfer array hru_soil and the groundwater
    percolation storage array. It maps each salt ion to its groundwater bookkeeping slot.
  gw_soil_flag: Flag controlling whether groundwater-to-soil salt transfer is active for this
    HRU. When on, the routine adds hru_soil groundwater salt to the soil profile.
  cosalt: Salt concentration in mobile water for the current layer, computed from the layer's
    remaining salt mass and available moving water.
  cosurfsalt: Salt concentration factor used for surface runoff export. It scales the mobile-water
    concentration by the HRU nitrogen percolation factor hru(j)%nut%nperco.
  percsaltlyr: Temporary per-salt accumulator for the amount leached downward from the current
    layer. It carries the percolation loss to the next lower layer and becomes the HRU's bottom-of-profile
    percolation export.
  ssfsaltlyr: Temporary amount of salt transported laterally from the current layer. It is
    computed from lateral flow and the mobile-water salt concentration.
  vsalt: Salt mass available in the mobile water of the current layer before scaling to a
    concentration.
  hru_area_m2: HRU area converted from hectares to square meters for computing water volume
    in a layer.
  water_volume: Estimated water volume stored in the current soil layer, used to convert salt
    mass to concentration in mg/L.
  salt_mass_kg: Current layer salt mass converted from kg/ha to kg for concentration calculations.
  ro_mass: Salt mass exported by surface runoff from the top layer; it is capped so runoff
    cannot remove more salt than is stored in the layer.
  sro: Surface runoff amount used when computing the mobile-water salt concentration in the
    top layer.
  vv: Total mobile-water volume available to transport salt in the current layer, including
    percolation, surface runoff, lateral flow, and tile drainage where applicable.
  ww: Exponential argument used in the soil-solution mixing calculation; it converts available
    water and excluded porosity into a fraction of salt in mobile water.
uses:
  hru_module: hru_module holds the active HRU's management and flux state that determines
    how much salt can leave each layer. The routine needs hru(j)%lumv%ldrain to know which
    layer has tile drainage, hru(j)%nut%nperco to scale runoff salt concentration, hru(j)%area_ha
    to convert mass and volume units, and the salt output arrays to accumulate fluxes by HRU
    and salt ion.
  basin_module: basin_module matters because the groundwater-salt bookkeeping to gwflow_percsol
    only runs when basin-wide groundwater flow is enabled. That basin flag gates whether percolation
    salt is exported to the groundwater solute array.
  constituent_mass_module: constituent_mass_module provides the salt-constituent database
    and the per-HRU/per-layer salt storage being updated. The routine uses cs_db%num_salts
    to loop over all simulated salts and updates cs_soil(j)%ly(jj)%salt(isalt) and cs_soil(j)%ly(jj)%saltc(isalt)
    as the layer mass and concentration state.
  soil_module: soil_module provides the soil-layer hydrologic properties that control transport
    and concentration calculations. Layer counts, percolation, lateral flow, anion exclusion,
    saturation water, and current stored water determine how much salt can move and what concentration
    results after redistribution.
  gwflow_module: gwflow_module provides the groundwater-solute transfer arrays and flags that
    link this HRU salt routine to the groundwater flow solver. gw_solute_flag and hru_soil
    determine whether groundwater salt enters the profile and where the corresponding recharge-percolation
    salt is stored for later groundwater processing.
---

<!-- facts:header -->

Computes salt redistribution and losses from each HRU soil profile. It moves salt through groundwater input, surface runoff, tile flow, lateral flow, and percolation, then updates layer concentrations.

## Bottom Line

salt_lch updates the salt mass stored in each soil layer for the current HRU by adding groundwater-borne salt when groundwater solute transport is active, then subtracting salt exported by surface runoff, tile drainage, lateral flow, and percolation. It also records those fluxes in the HRU salt-balance arrays so downstream reporting and mass balance can track where salt left or entered the profile.

After the layer masses are adjusted, the routine recomputes salt concentration in each soil layer from the updated mass and the layer water volume. That concentration state is what later salt and groundwater calculations rely on, so this routine is the daily bookkeeping step that keeps the HRU salt profile internally consistent.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from hru_control after atmospheric salt deposition and road-salt additions have already been applied to the HRU. It uses the current day's HRU runoff, drainage, percolation, and groundwater-solute state to update layer salt masses before later model steps and output reporting rely on those updated concentrations and flux totals.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the active HRU and optionally add groundwater-borne salt to each soil layer. | The routine sets j from ihru, then if groundwater soil solute routing is enabled it loops over all soil layers and salt ions, adds hru_soil groundwater salt into cs_soil(j)%ly(jj)%salt(isalt), and accumulates the same amount in gwupsalt(j,isalt) for mass-balance output. |
| 2. Clear the per-salt percolation accumulator and start the salt-ion loop. | percsaltlyr is reset to zero so each salt ion starts with no downward carryover from previous ions, then the routine begins iterating over every simulated salt constituent. |
| 3. March through each soil layer for the current salt ion and add salt arriving from above. | For each layer, the routine adds the downward-leached salt from the layer above, then zeroes very small residual masses so numerical roundoff does not leave tiny negative or near-zero values in storage. |
| 4. Compute the mobile-water salt concentration driving all transport pathways. | The routine selects surface runoff only for the top layer, builds the mobile-water volume from percolation, runoff, lateral flow, and optional tile drainage, applies the anion-exclusion adjustment, and uses an exponential mixing relation to estimate the salt mass in mobile water and its concentration cosalt. |
| 5. Route salt out with surface runoff from the top layer. | Using hru(j)%nut%nperco times cosalt, the routine computes surface-runoff salt mass only for the surface layer, caps it at the layer's remaining salt mass, subtracts it from storage, and records it in surqsalt(j,isalt). |
| 6. Route salt out with tile drainage from the designated drainage layer. | If the current layer is the HRU's tile-drain layer, the routine computes tile salt as cosalt multiplied by qtile, limits the removal to the stored mass, and subtracts it from the layer salt pool. |
| 7. Route salt out with lateral flow and with percolation to the next layer. | The routine computes lateral-flow salt from cosurfsalt or cosalt depending on layer position, caps and subtracts it, then computes percolation salt from cosalt and layer prk, caps and subtracts it, stores the current ion's downward carryover in percsaltlyr, writes the bottom-of-profile loss to percsalt(j,isalt), and copies it to gwflow_percsol when basin groundwater routing is active. |
| 8. Recompute concentration for every salt ion in every soil layer. | After all mass transfers are finished, the routine converts each layer's remaining salt mass to kg, estimates the layer water volume from soil water storage and HRU area, and updates cs_soil(j)%ly(jj)%saltc(isalt) as mg/L when water_volume is positive; otherwise it sets concentration to zero and clears any negative mass first. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, gwupsalt, surfq, surqsalt, tilesalt, latqsalt, percsalt, ihru, qtile` | `hru(j)%lumv%ldrain, hru(j)%nut%nperco, hru(j)%area_ha` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_salts, cs_soil(j)%ly(jj)%salt(isalt), cs_soil(j)%ly(jj)%saltc(isalt)` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%ly(jj)%prk, soil(j)%ly(jj)%flat, soil(j)%anion_excl, soil(j)%phys(jj)%ul, soil(j)%phys(jj)%st` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:gwflow_module] | `gwflow_percsol, gw_solute_flag, hru_soil` | `gwflow_percsol, gw_solute_flag, hru_soil` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(j)%ly(jj)%salt(isalt)` | Each layer after percolation, lateral flow, tile flow, and surface-runoff removal have been applied for the current salt ion. | This is the residual salt mass left in the soil layer after incoming groundwater salt, downward carryover from the layer above, and all outgoing transport pathways have been accounted for. It is the primary storage state that the rest of the salt routine balances. |
| `gwupsalt(j,isalt)` | When gw_soil_flag == 1 and gw_solute_flag == 1 at the start of the routine. | This records the amount of salt added from groundwater into the soil profile for mass-balance tracking. Later groundwater-salt reporting can separate this inflow from other soil-profile salt changes. |
| `surqsalt(j,isalt)` | When jj == 1, using surface runoff and the computed mobile-water concentration. | This stores the salt mass transported away by surface runoff from the top soil layer. It is part of the HRU salt export used in the daily salt balance. |
| `tilesalt(j,isalt)` | When the current layer index matches hru(j)%lumv%ldrain. | This stores the salt mass removed with tile drainage from the designated drainage layer. It captures an HRU-specific subsurface export route for salt. |
| `latqsalt(j,isalt)` | For every soil layer, using the current layer's lateral flow amount. | This stores the salt transported laterally out of the layer. It contributes to the HRU's lateral salt export total. |
| `percsalt(j,isalt)` | For every soil layer, after computing cosalt from the layer's mobile water and prk. | This stores the salt that percolates downward out of the current layer. The last layer's value becomes the HRU's percolation loss from the profile. |
| `gwflow_percsol(j,sol_index)` | When bsn_cc%gwflow == 1 and gw_solute_flag == 1 after percolation is computed. | This copies the layer's percolation salt into the groundwater flow solute array so the groundwater model can use the HRU salt export as recharge input. |
| `cs_soil(j)%ly(jj)%saltc(isalt)` | After all flux removals are finished and water_volume is positive for the current layer and salt ion. | This updates the stored salt concentration in the soil water for the layer. Later routines use that concentration as the basis for subsequent salt transport and reporting. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four source-affecting commits. df07e3f introduced salt_lch with the salt runoff, lateral flow, tile flow, percolation, and groundwater bookkeeping structure. 35b029c changed the gwflow_module import to drop gw_soil_flag from the module-only list and make it a local variable, while preserving the same groundwater-gated logic. 94b6dec brought in the source with the same overall algorithm and existing documentation block. 39fabde initialized local variables and added numerical guards, and ffb8cce changed the surface-runoff salt concentration factor from bsn_prm%nperco to hru(j)%nut%nperco.

- df07e3f: established the salt-lch algorithm and its HRU soil-salt, runoff, tile, lateral, percolation, and groundwater bookkeeping outputs.
- 35b029c: changed the gwflow import pattern so gw_soil_flag became a local control variable while keeping the groundwater-solute gating logic in place.
- 39fabde: initialized local variables and added zero/negative safeguards that stabilize the salt balance and concentration calculations.
- ffb8cce: redirected the surface runoff salt scaling to the HRU nutrient parameter nperco, changing which parameter controls runoff salt export.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_lch' has no extracted documentation comment.
