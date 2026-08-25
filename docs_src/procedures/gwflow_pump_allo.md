---
kind: procedure
symbol: gwflow_pump_allo
title: gwflow_pump_allo
status: filled
source_hash: d89d2accffbed90b
version_label: SWAT+ 62.0.0
args:
  ob_id_dmd: '`ob_id_dmd` identifies the demand object to serve. The routine treats it as
    the HRU/object number that receives the groundwater allocation, and uses it to select
    either the connected HRU cells or the single source cell for municipal demand.'
  demand_vol: '`demand_vol` is the total water volume requested from groundwater, in cubic
    meters. The routine splits or assigns this volume to gwflow cells as the per-cell pumping
    target.'
  extracted: '`extracted` is reset on entry and then accumulated with the groundwater volume
    actually removed from the aquifer. It returns the met portion of demand to the caller.'
  dmd_unmet: '`dmd_unmet` is reset on entry and then accumulated with the part of demand that
    could not be supplied from groundwater storage. It returns the unmet portion of the request
    to the caller.'
locals:
  ob_id_src: Holds the source-object identifier for municipal-style allocation; zero means
    self-supplied HRU demand, while a positive value can be mapped to a gwflow cell through
    `cell_id_list` when the grid is structured.
  i: Loop counter over the gwflow cells connected to an HRU or over other per-object iterations
    in the routine.
  s: Loop counter over solute or constituent species when groundwater mass is transferred.
  cell_id: The gwflow cell currently being evaluated for available groundwater, pumping, heat,
    and solute updates.
  wetland: Flag used to detect whether the demand object is a wetland/reservoir-type object
    so the irrigation mass is routed to wetland mass balances instead of HRU soil pools.
  isalt: Loop counter over salt species when updating salt-specific irrigation mass balances.
  ics: Loop counter over other constituent species when updating constituent-specific irrigation
    mass balances.
  sol_index: Index used to map a groundwater solute to the corresponding HRU or wetland constituent
    slot.
  hru_id: Resolved HRU identifier for the demand object or source object, used to access HRU-linked
    cells and downstream state arrays.
  cell_demand: The portion of the total demand assigned to one gwflow cell.
  gwvol_avail: Groundwater volume available in the current cell based on head above bottom,
    cell area, and specific yield.
  gwvol_removed: Groundwater volume actually removed from the current cell for this demand.
  gwvol_unmet: Per-cell demand volume that could not be met because the cell lacked enough
    groundwater.
  gw_mass: Available mass of a solute in the current groundwater cell, used to cap irrigation
    mass extraction.
  irr_mass: Per-solute irrigation mass removed from the pumped groundwater before it is added
    to the receiving object.
  mass_diff: The amount by which requested irrigation mass exceeds available groundwater mass;
    used to prevent negative or overdrawn solute removal.
  sum_pump: Running total of groundwater pumping assigned to the HRU across all connected
    cells.
  hru_area_m2: HRU area in square meters, used when converting mass additions to area-based
    soil or wetland rates.
  heat_flux: Heat energy carried by the pumped groundwater for the current cell, capped by
    available groundwater heat storage.
  soil_volm: Volume of soil water in the receiving layer, used when translating added irrigation
    mass into soil concentrations or mass fractions.
  soil_heat: Heat content of the receiving soil water layer, used when translating pumped-water
    heat into a soil update.
uses:
  gwflow_module: '`gwflow_module` provides the per-cell groundwater state, the shared daily/monthly/yearly
    source-sink summary arrays, and the HRU-to-cell mapping that this routine uses to find
    connected cells, compute available storage, and record pumping, deficit, heat, and solute
    transfers.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` holds the HRU soil mineral nitrogen
    and phosphorus pools that receive irrigation-borne nutrient mass when the demand object
    is an HRU.'
  hru_module: '`hru_module` supplies the HRU structure and its surface-storage pointer so
    the routine can resolve the target HRU and route irrigation-related updates to the correct
    object.'
  hydrograph_module: '`hydrograph_module` supplies wetland hydrograph storage, which matters
    when the demand object is a wetland and pumped-water nutrients must be added to wetland
    water-quality outputs instead of HRU soil pools.'
  soil_module: '`soil_module` is the soil-state source needed to update the receiving profile
    when pumped groundwater adds water, heat, or solute mass to the soil system.'
  constituent_mass_module: '`constituent_mass_module` provides the water-borne salt and other
    constituent containers for wetlands and soils, which this routine updates when groundwater
    pumping carries dissolved mass to the demand object.'
  res_salt_module: '`res_salt_module` tracks wetland salt irrigation mass so groundwater-derived
    salt additions can be accumulated for wetland balance reporting.'
  res_cs_module: '`res_cs_module` tracks wetland non-salt constituent irrigation mass for
    the same reason as the salt wetland balance, but for the other constituent pool.'
  salt_module: '`salt_module` stores HRU soil salt balance terms, including groundwater irrigation
    additions, which must be updated when pumped water is routed to an HRU.'
  cs_module: '`cs_module` stores HRU soil non-salt constituent balances, including groundwater
    irrigation additions, which must be updated when pumped water is routed to an HRU.'
---

<!-- facts:header -->

Allocates groundwater pumping demand from SWAT+ HRUs or municipal objects to connected gwflow cells. It updates groundwater water, heat, and solute/constituent mass balance outputs and returns extracted versus unmet demand.

## Bottom Line

`gwflow_pump_allo` distributes a requested water volume across the gwflow grid cells connected to the demand object. For HRU irrigation it splits demand across all connected cells; for municipal demand it uses one source cell, with the cell chosen directly or through `cell_id_list` when the grid is structured.

For each affected cell it computes available groundwater from head and bottom elevation, removes as much as possible up to the cell demand, and records the result in gwflow summary arrays. When heat or solute tracking is active, it also removes corresponding heat and mass from the aquifer and adds the irrigated mass to the receiving HRU or wetland/surface-water bookkeeping arrays.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `wallo_withdraw` after that routine has identified a withdrawal request and determined that gwflow is active. `wallo_withdraw` passes the demand object number and requested volume here, and the results feed back into the caller's withdrawn and unmet totals as well as the gwflow water, heat, and solute balance accumulators used later by gwflow simulation and output reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize demand accounting and determine whether the request is HRU irrigation or municipal withdrawal. | The routine imports the groundwater, HRU, wetland, soil, and constituent balance modules, declares cell- and species-level working variables, zeroes `extracted` and `dmd_unmet`, and branches on `demand_type`/`ob_id_src` so it can treat HRU self-supply and municipal source-cell pumping differently. |
| 2. For HRU irrigation, resolve the HRU, split demand across connected gwflow cells, and loop over those cells. | The routine maps `ob_id_dmd` to `hru_id`, checks that the HRU has connected gwflow cells, and divides the requested volume by `hru_num_cells(hru_id)` to get a per-cell target before iterating over each linked cell in `hru_cells(hru_id,i)`. |
| 3. Compute each cell's available groundwater and determine how much of the per-cell demand can be met. | For each cell, the routine checks whether groundwater head is above the bottom, converts saturated thickness to available volume with area and specific yield, and sets `gwvol_removed` and `gwvol_unmet` so the cell withdraws at most the available storage. It then accumulates the met and unmet portions into `extracted` and `dmd_unmet`. |
| 4. Record HRU pumping and deficit in groundwater water-balance outputs. | The routine writes negative pumping to `gw_hyd_ss(cell_id)%ppag`, adds to the monthly and yearly `ppag` sums, stores unmet demand in `ppdf`, and accumulates the yearly `ppdf` total so later gwflow balance reporting can reconstruct extraction and shortfall. |
| 5. If groundwater heat tracking is active, remove heat associated with the pumped water. | When `gw_heat_flag == 1`, the routine computes `heat_flux` from groundwater temperature, density, heat capacity, and removed volume, caps it at available heat storage, and writes the negative flux to daily and yearly heat summaries. This keeps heat balance consistent with the water withdrawal. |
| 6. If groundwater solute tracking is active, compute soluble mass withdrawn and add it to the HRU/wetland receiving state. | When `gw_solute_flag == 1`, the routine loops through `gw_nsolute`, computes the solute mass removed with the pumped water, caps it to the available cell mass, and then routes the mass to the receiving HRU or wetland state: HRU nutrient pools and soil salt/constituent balances for HRU demand, or wetland water and wetland balance arrays for wetland demand. |
| 7. Update HRU soil, wetland, and balance bookkeeping for each solute or constituent class. | The routine distributes irrigation mass into the correct downstream pools: `soil1` and `cs_soil` for HRU mineral N/P and soil constituents, `wet`/`wet_water` for wetland nutrient and constituent water quality, and `hsaltb_d`/`hcsb_d` or `wetsalt_d`/`wetcs_d` for irrigation balance reporting. This step preserves mass balance for every species transferred with groundwater. |
| 8. Complete the HRU loop and accumulate total pumping for the object. | After all connected cells are processed, the routine finishes the HRU branch by maintaining the object-level pumping total and leaving the daily/monthly/yearly gwflow summary arrays ready for later output use. |
| 9. For municipal demand, resolve a single source cell and apply the same groundwater accounting. | When `demand_type == "muni"` and `ob_id_src > 0`, the routine uses `cell_id_list(ob_id_src)` for structured grids, sets the whole request as the cell demand, computes available groundwater, and updates `extracted` and `dmd_unmet` exactly once for that source cell. |
| 10. Record municipal pumping and deficit in the same gwflow summary arrays used for HRU irrigation. | The routine stores negative extraction in `gw_hyd_ss(cell_id)%ppex`, adds to yearly and monthly `ppex` totals, and records unmet demand in `ppdf`/yearly `ppdf` so the municipal withdrawal contributes to the same groundwater output accounting as irrigation. |
| 11. If enabled, remove heat from the municipal source cell. | The routine computes the heat carried by the municipal pump, caps it by cell heat storage, and stores the negative heat flux in daily and yearly `gw_heat_ss` entries, keeping the thermal mass balance aligned with the pumped volume. |
| 12. If enabled, compute source-cell solute removal for municipal pumping and update the groundwater solute summaries. | The routine loops over `gw_nsolute`, limits solute removal by available groundwater mass, and writes negative mass fluxes to `gwsol_ss`, `gwsol_ss_sum`, and `gwsol_ss_sum_mo` so later gwflow simulation and reporting can account for the material removed with the municipal withdrawal. |
| 13. Return to the caller with extracted and unmet demand totals updated. | The routine exits after both demand branches, leaving `extracted`, `dmd_unmet`, and the various gwflow summary arrays updated for `wallo_withdraw` and later groundwater balance calculations. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_mo, gw_heat_ss, gw_heat_ss_yr, hru_num_cells, hru_cells, cell_id_list` | `gw_state(cell_id)%botm, gw_state(cell_id)%head, gw_state(cell_id)%area, gw_state(cell_id)%spyd, gw_hyd_ss(cell_id)%ppag, gw_hyd_ss_yr(cell_id)%ppag, gw_hyd_ss_mo(cell_id)%ppag, gw_hyd_ss(cell_id)%ppdf, gw_hyd_ss_yr(cell_id)%ppdf, gw_heat_ss(cell_id)%ppag, gw_heat_ss_yr(cell_id)%ppag, gw_hyd_ss(cell_id)%ppex, gw_hyd_ss_yr(cell_id)%ppex, gw_hyd_ss_mo(cell_id)%ppex, gw_heat_ss(cell_id)%ppex, gw_heat_ss_yr(cell_id)%ppex` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(hru_id)%mn(1)%no3, soil1(hru_id)%mp(1)%lab` |
| [sym:hru_module] | `hru` | `hru(hru_id)%dbs%surf_stor` |
| [sym:hydrograph_module] | `wet` | `wet(hru_id)%no3, wet(hru_id)%solp` |
| [sym:soil_module] | `soil` | `soil` |
| [sym:constituent_mass_module] | `cs_db, wet_water, cs_soil` | `cs_db%num_salts, wet_water(hru_id)%salt(isalt), cs_db%num_cs, wet_water(hru_id)%cs(ics), cs_soil(hru_id)%ly(1)%salt(isalt), cs_soil(hru_id)%ly(1)%cs(ics)` |
| [sym:res_salt_module] | `wetsalt_d` | `wetsalt_d(hru_id)%salt(isalt)%irrig` |
| [sym:res_cs_module] | `wetcs_d` | `wetcs_d(hru_id)%cs(ics)%irrig` |
| [sym:salt_module] | `hsaltb_d` | `hsaltb_d(hru_id)%salt(isalt)%irgw` |
| [sym:cs_module] | `hcsb_d` | `hcsb_d(hru_id)%cs(ics)%irgw` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `gw_hyd_ss(cell_id)%ppag` | When HRU demand is served from connected gwflow cells and each cell removal is computed. | Stores the negative daily pumping volume removed from the aquifer for irrigation from the current cell. |
| `gw_hyd_ss_yr(cell_id)%ppag` | When HRU demand is served from connected gwflow cells and each cell removal is accumulated into yearly hydrology summaries. | Accumulates the yearly total of negative pumping volume removed from the aquifer for irrigation. |
| `gw_hyd_ss_mo(cell_id)%ppag` | When HRU demand is served from connected gwflow cells and each cell removal is accumulated into monthly hydrology summaries. | Accumulates the monthly total of negative pumping volume removed from the aquifer for irrigation. |
| `gw_hyd_ss(cell_id)%ppdf` | When HRU demand or municipal demand leaves unmet groundwater volume for a cell. | Stores the unmet pumping deficit for the current day so output can report demand that groundwater could not satisfy. |
| `gw_hyd_ss_yr(cell_id)%ppdf` | When unmet demand is added into the yearly hydrology summary for the cell. | Accumulates yearly unmet pumping deficit from all applicable withdrawal events. |
| `gw_heat_ss(cell_id)%ppag` | When heat tracking is enabled and irrigation or municipal pumping removes thermal energy from groundwater. | Stores the negative heat flux associated with the pumped groundwater for the current day. |
| `gw_heat_ss_yr(cell_id)%ppag` | When heat tracking is enabled and irrigation or municipal pumping removes thermal energy from groundwater. | Accumulates the yearly negative heat flux removed with pumped groundwater. |
| `if(irr_mass(s).lt.0)irr_mass(s)` | When solute mass removal is computed and a mass cap forces negative irrigation mass to zero. | Prevents any solute from being reported as negative after capping by available groundwater mass; if the corrected mass drops below zero, it is reset to zero before it is written to balance arrays. |
| `wet(hru_id)%no3` | When HRU irrigation water is routed to the receiving object and groundwater solute tracking is enabled. | Receives nitrate mass for a wetland demand object through the wetland hydrograph balance path. |
| `wet(hru_id)%solp` | When HRU irrigation water is routed to the receiving object and groundwater solute tracking is enabled. | Receives soluble phosphorus mass for a wetland demand object through the wetland hydrograph balance path. |
| `wet_water(hru_id)%salt(isalt)` | When groundwater irrigation adds salt mass to a wetland or wetland-water balance is updated. | Stores the pumped-water salt mass in the wetland water constituent pool for the matching salt species. |
| `wetsalt_d(hru_id)%salt(isalt)%irrig` | When wetland salt irrigation bookkeeping is updated for a pumped groundwater transfer. | Accumulates the salt mass removed from groundwater and applied through irrigation to the wetland balance output. |
| `wet_water(hru_id)%cs(ics)` | When groundwater irrigation adds other constituent mass to a wetland or wetland-water balance is updated. | Stores the pumped-water mass for the matching non-salt constituent in the wetland water constituent pool. |
| `wetcs_d(hru_id)%cs(ics)%irrig` | When wetland constituent irrigation bookkeeping is updated for a pumped groundwater transfer. | Accumulates the non-salt constituent mass removed from groundwater and applied through irrigation to the wetland balance output. |
| `soil1(hru_id)%mn(1)%no3` | When groundwater irrigation adds nitrate to the receiving HRU soil profile. | Updates the top-layer soil nitrate pool for the HRU receiving pumped groundwater. |
| `soil1(hru_id)%mp(1)%lab` | When groundwater irrigation adds labile phosphorus to the receiving HRU soil profile. | Updates the top-layer soil labile phosphorus pool for the HRU receiving pumped groundwater. |
| `cs_soil(hru_id)%ly(1)%salt(isalt)` | When groundwater irrigation adds salt mass to the HRU soil profile. | Updates the top soil-layer salt constituent pool for the HRU receiving pumped groundwater. |
| `hsaltb_d(hru_id)%salt(isalt)%irgw` | When groundwater irrigation updates the HRU salt balance for groundwater-applied salts. | Accumulates groundwater-irrigation salt mass in the HRU salt balance output. |
| `cs_soil(hru_id)%ly(1)%cs(ics)` | When groundwater irrigation adds non-salt constituent mass to the HRU soil profile. | Updates the top soil-layer non-salt constituent pool for the HRU receiving pumped groundwater. |
| `hcsb_d(hru_id)%cs(ics)%irgw` | When groundwater irrigation updates the HRU non-salt constituent balance for groundwater-applied mass. | Accumulates groundwater-irrigation constituent mass in the HRU constituent balance output. |
| `gwsol_ss(cell_id)%solute(s)%ppag` | When solute mass removal is computed for a pumped groundwater cell. | Stores the negative per-cell solute mass removed with irrigation pumping for the day. |
| `gwsol_ss_sum(cell_id)%solute(s)%ppag` | When solute mass removal is accumulated into the yearly groundwater solute summary. | Accumulates yearly solute mass removed with irrigation pumping for the cell. |
| `gwsol_ss_sum_mo(cell_id)%solute(s)%ppag` | When solute mass removal is accumulated into the monthly groundwater solute summary. | Accumulates monthly solute mass removed with irrigation pumping for the cell. |
| `hru_pump(hru_id)` | When the routine totals pumping over all cells connected to an HRU demand object. | Captures the total groundwater pumping applied to the HRU across its linked gwflow cells. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage evidence shows the routine was first added in commit 9d9069f as a new gwflow pumping-allocation subroutine for water allocation, then substantially expanded in 05cc429 to support the new 4-argument call from `wallo_withdraw`, structured HRU versus municipal demand handling, monthly/yearly summaries, and heat/solute mass bookkeeping. The later 23142ed commit added explicit structured output objects and CSV/header support for water-body outputs, but no diff for this file was available in the packet, so no file-specific changes can be confirmed from that commit. The 39fabde, 94b6dec, and 2ee1889 entries have no diff available here for this file.

- Introduced `gwflow_pump_allo` as a new gwflow extraction-allocation routine with HRU-linked cell looping and water-balance recording.
- Changed the routine to accept `ob_id_dmd`, `demand_vol`, `extracted`, and `dmd_unmet`, added `ob_id_src`/`demand_type`, imported `soil`, `irrn`, `irrp`, and `ob`, and expanded the logic to handle both HRU irrigation and municipal single-cell pumping.
- Added monthly/yearly accumulation and heat/solute bookkeeping for the new pumping allocation path.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_pump_allo' has no extracted documentation comment.
- algorithm_steps revised: consolidated the original eight coarse blocks into thirteen source-tied steps to match the two demand branches and the explicit water/heat/solute bookkeeping visible in the source.
- Source shows no resolved outgoing callees.
