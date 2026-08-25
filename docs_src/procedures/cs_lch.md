---
kind: procedure
symbol: cs_lch
title: cs_lch
status: filled
source_hash: ee7095bd9d7d2aed
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index. It is assigned from `ihru` and used to access the active HRU, soil
    profile, and all HRU-sized constituent arrays.
  jj: Current soil-layer index within the active HRU. It drives the layer-by-layer looping
    for groundwater addition, transport, and concentration recalculation.
  gw_soil_flag: Flag that controls whether groundwater-to-soil constituent additions are processed.
    In this procedure it gates the block that reads `hru_soil` and adds aquifer-delivered
    mass to each soil layer.
  ics: Current constituent index within `cs_db%num_cs`. It selects which constituent pool
    and concentration slot is being updated.
  sol_index: Offset index into the combined solute/constituent dimension of `hru_soil` and
    `gwflow_percsol`. It starts after salts (`2 + cs_db%num_salts`) and is incremented for
    each constituent.
  cocs: Concentration of the constituent in mobile soil water for the current layer, computed
    from constituent mass and available water volume.
  cosurfcs: Surface-runoff constituent concentration factor, formed from `hru(j)%nut%nperco`
    times the mobile-water concentration. It scales how much constituent is lost with surface
    runoff.
  perccslyr: Percolation loss from the current layer for each constituent, stored as a small
    array so the amount removed from an upper layer can be passed to the next lower layer.
  ssfcslyr: Lateral-flow constituent loss from the current layer. It is computed separately
    for the surface layer and deeper layers and then subtracted from the soil pool.
  vcs: Intermediate estimate of mobile constituent mass in the layer water. It is used with
    `ww` and `vv` to derive `cocs`.
  hru_area_m2: HRU area converted from hectares to square meters. It is used to convert layer
    water storage to volume when calculating concentration.
  water_volume: Estimated water volume in the current soil layer, derived from soil storage
    (`st`) and HRU area. It is used to compute mg/L concentration from remaining mass.
  cs_mass_kg: Remaining constituent mass in the layer converted to kilograms using HRU area.
    It is the numerator used when recalculating concentration.
  ro_mass: Mass of constituent removed by surface runoff from the top soil layer. It is capped
    by the available layer mass before subtraction.
  sro: Surface runoff depth used in the mobile-water calculation for the top soil layer only.
    It is zero in deeper layers.
  vv: Total mobile water volume term used in the exponential concentration calculation. It
    combines percolation, surface runoff, lateral flow storage, and optional tile flow.
  ww: Exponential argument controlling how much constituent mass is available in mobile water.
    It reflects water volume relative to soil storage capacity and anion exclusion.
uses:
  hru_module: The HRU module supplies the active HRU index, HRU area, land management drainage
    depth, constituent routing parameters, and the HRU-sized runoff/lateral/tile/percolation
    arrays that `cs_lch` reads and updates. Without this state, the routine cannot determine
    which layer receives tile drainage or where to store export masses.
  basin_module: The basin control flag `bsn_cc%gwflow` decides whether percolation losses
    are copied into `gwflow_percsol` for the groundwater flow subsystem. That makes basin-level
    gwflow configuration directly relevant to whether this routine exports constituent recharge
    for later use.
  constituent_mass_module: The constituent-mass module defines how many constituents are simulated
    and stores the per-HRU soil constituent pools that this routine modifies. It is also the
    source of the soil-layer concentration field that is recalculated after transport and
    groundwater additions.
  soil_module: The soil module provides the number of soil layers and the layer water/storage
    properties used to convert mass to concentration and to partition constituent losses among
    runoff, tile flow, lateral flow, and percolation. These soil-layer hydraulic terms control
    the transport calculations inside the loops.
  gwflow_module: The gwflow module provides the groundwater solute flag, the groundwater-to-soil
    constituent flux array, and the groundwater recharge export array. `cs_lch` uses those
    values to add aquifer-delivered mass to soil layers and to hand off percolation losses
    to the groundwater solute workflow.
---

<!-- facts:header -->

Routes constituent mass losses and concentrations through each HRU soil profile. It updates soil-layer constituent pools, tracks export to runoff, lateral flow, tile flow, percolation, and optional groundwater recharge bookkeeping.

## Bottom Line

`cs_lch` computes daily movement of generic constituents through the soil profile for the current HRU. It adds any groundwater-delivered mass into the soil layers, then partitions each constituent among surface runoff, tile drainage, lateral flow, and percolation using soil water and routing properties.

The routine also converts the remaining soil constituent mass back to concentration for each layer so later water-quality and mass-balance routines can use the updated profile state. When gwflow is active, it stores percolation losses in `gwflow_percsol` for later groundwater recharge/solute handling.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU control after constituent-atmosphere processing (`cs_rain`) and before pathogen transport routines. `hru_control` prepares the active HRU context and constituent arrays, and later model behavior depends on `cs_lch` having updated soil pools and the runoff/lateral/tile/percolation mass accounting arrays.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set the active HRU and optionally add groundwater-delivered constituent mass into each soil layer. | The routine takes the current HRU from `ihru`, then, when both groundwater-to-soil and groundwater solute processing are enabled, loops through every soil layer and constituent to add `hru_soil(j,jj,sol_index)` into `cs_soil(j)%ly(jj)%cs(ics)` and accumulate the same amount into `gwupcs(j,ics)` for mass-balance reporting. |
| 2. Initialize percolation carryover for the constituent loop. | The percolation transfer array is reset to zero, then the routine begins looping over each simulated constituent and sets the solute/constituent index offset used by the groundwater export array. |
| 3. Add incoming percolation from the layer above and compute mobile-water concentration terms for the current layer. | For each soil layer, the routine adds `perccslyr(ics)` from the previous layer into the current soil constituent pool, then builds the mobile-water volume term `vv`, includes tile drainage only on the designated tile layer, computes the exponential factor `ww`, derives mobile mass `vcs`, and converts it to concentration `cocs`. |
| 4. Remove constituent mass in surface runoff from the top soil layer. | When processing the surface layer, the routine multiplies runoff depth by `cosurfcs` to get surface-runoff constituent mass, limits that mass to what is available in the layer, subtracts it from soil storage, and stores the result in `surqcs(j,ics)`. |
| 5. Remove constituent mass in tile drainage from the designated drainage layer. | If the current layer matches the HRU tile-drain layer, the routine computes tile export as `cocs * qtile`, caps it by the available soil mass, and subtracts it from the layer pool. |
| 6. Remove constituent mass in lateral flow from each layer. | The routine computes a lateral-flow loss for the current layer using either `cosurfcs` on the surface layer or `cocs` below the surface, scales it by the layer's lateral-flow storage `flat`, caps it by available mass, adds it to `latqcs(j,ics)`, and subtracts it from the soil pool. |
| 7. Remove constituent mass in percolation and pass it down the profile. | Percolation loss is computed as `cocs * soil(j)%ly(jj)%prk`, limited to the remaining layer mass, subtracted from the current layer, and stored in `perccslyr(ics)` so the next lower layer can inherit it. |
| 8. Save profile percolation losses for groundwater routing when gwflow is active. | After the layer loop finishes for a constituent, the routine records the final percolation amount in `perccs(j,ics)` and, if basin gwflow and groundwater solute processing are enabled, writes the same loss to `gwflow_percsol(j,sol_index)`. |
| 9. Recalculate each soil-layer constituent concentration from remaining mass. | The routine loops over all soil layers and constituents, converts area to square meters, converts layer storage to water volume, floors any negative soil mass at zero, computes mass in kilograms, and then derives `cs_soil(j)%ly(jj)%csc(ics)` in mg/L; if water volume is zero, concentration is set to zero. |
| 10. Return to the caller with updated HRU soil and routing state. | The procedure ends after all soil-pool, runoff, lateral-flow, tile-flow, percolation, and groundwater bookkeeping updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, gwupcs, surfq, surqcs, tilecs, latqcs, perccs, ihru, qtile` | `hru(j)%lumv%ldrain, hru(j)%nut%nperco, hru(j)%area_ha` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_salts, cs_db%num_cs, cs_soil(j)%ly(jj)%cs(ics), cs_soil(j)%ly(jj)%csc(ics)` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%ly(jj)%prk, soil(j)%ly(jj)%flat, soil(j)%anion_excl, soil(j)%phys(jj)%ul, soil(j)%phys(jj)%st` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:gwflow_module] | `gwflow_percsol, gw_solute_flag, hru_soil` | `gwflow_percsol, gw_solute_flag, hru_soil` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(j)%ly(jj)%cs(ics)` | For every HRU soil layer and constituent after the transport loops, with negative values forced to zero before concentration is computed. | This is the remaining soil constituent mass after groundwater addition and after losses to runoff, tile flow, lateral flow, and percolation. It is the core soil reservoir that downstream routines use for subsequent transport and mass-balance accounting. |
| `gwupcs(j,ics)` | Only when `gw_soil_flag == 1 .and. gw_solute_flag == 1` while looping through the HRU's soil layers and constituents. | This array accumulates constituent mass added from groundwater into the soil profile. It provides mass-balance bookkeeping for groundwater-to-soil exchanges. |
| `surqcs(j,ics)` | Only for the top soil layer (`jj == 1`) after computing `ro_mass` from surface runoff depth and `cosurfcs`. | This stores the constituent mass lost to direct surface runoff from the surface layer so later routing and reporting routines can use the runoff export amount. |
| `tilecs(j,ics)` | Only when the current layer equals the HRU tile-drain layer (`hru(j)%lumv%ldrain == jj`). | This records the constituent mass removed by tile drainage from the drainage layer. It is the tile-flow export that later routing and accounting routines rely on. |
| `latqcs(j,ics)` | For every layer when lateral-flow loss is computed; the surface layer uses `cosurfcs`, deeper layers use `cocs`. | This accumulates constituent mass exported laterally from the soil profile. It represents the lateral-flow constituent load for the HRU. |
| `perccs(j,ics)` | For every layer and constituent after lateral loss is removed and before moving to the next layer. | This stores the percolation-exported constituent mass used to pass losses downward through the soil profile and to define the profile-scale percolation loss. |
| `gwflow_percsol(j,sol_index)` | When basin gwflow is enabled and groundwater solute processing is active (`bsn_cc%gwflow == 1 .and. gw_solute_flag == 1`). | This records the constituent mass leaving the soil profile in percolation for the groundwater flow module to consume later. |
| `cs_soil(j)%ly(jj)%csc(ics)` | After all mass removals are complete, for every layer and constituent when water volume is positive. | This is the recalculated constituent concentration in layer water, derived from the remaining mass and layer water storage. It is the concentration field available to later transport or output routines. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show one behavioral change and three non-behavioral updates. In `b3dc2c2`, the surface-runoff constituent concentration factor was changed from basin-level `bsn_prm%nperco` to HRU-level `hru(j)%nut%nperco`. In `f1e61a3`, `39fabde`, `35b029c`, and `2ee1889`, the diffs only changed indentation, variable initialization, use-list membership, and the final `end` statement style; those did not change model behavior.

- b3dc2c2 changes surface-runoff constituent loss so it now uses each HRU's nutrient parameter `hru(j)%nut%nperco` instead of the basin parameter `bsn_prm%nperco`, making runoff constituent export HRU-specific.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_lch' has no extracted documentation comment.
