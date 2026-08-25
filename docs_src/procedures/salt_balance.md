---
kind: procedure
symbol: salt_balance
title: salt_balance
status: filled
source_hash: fae8ff6fabc56d17
version_label: SWAT+ 62.0.0
locals:
  i: Loop index used repeatedly over HRUs, aquifer cells/objects, reservoirs, channels, recalls,
    soil layers, and salts.
  m: Loop index over salt constituents; it selects each salt ion entry in the per-object balance
    arrays and constituent mass arrays.
  ob_ctr: Sequential object counter for aquifer objects in the hydrograph connectivity list;
    it is advanced while mapping aquifer-related calculations to object positions.
  num_days: Temporary day-count divisor used to convert monthly and yearly accumulated totals
    into average daily values before writing period output.
  jj: Loop index over soil layers when summing soil salt storage and soil mineral salt content.
  saltsum: Running accumulator for one basin summary term at a time; it is reset for each
    flux or storage category and then assigned into salt_basin().
  hru_area_m2: HRU area converted from hectares to square meters for volume and mass calculations,
    especially the solid groundwater and soil storage terms.
  soil_volume: Intermediate soil-layer volume in cubic meters, computed from HRU area and
    layer thickness.
  soil_mass: Intermediate soil-layer mass in kilograms, computed from soil volume and bulk
    density for the solid salt calculation.
  aquifer_thickness: Fixed aquifer thickness assumption used to estimate aquifer volume for
    the solid groundwater salt stock.
  aquifer_volume: Intermediate aquifer volume in cubic meters, computed from HRU area and
    assumed aquifer thickness.
  aquifer_mass: Estimated aquifer mass in kilograms, computed from aquifer volume and an assumed
    density factor for solid groundwater salt storage.
  soil_thick: Current soil layer thickness in millimeters, used while converting layer depth
    into volume and mass.
  salt_basin: Local 28-element basin summary array that collects the current day’s salt flux
    and stock totals before they are written out and rolled into longer-period accumulators.
uses:
  hydrograph_module: The hydrograph module supplies the basin object counts and connectivity
    offsets that determine which HRUs, aquifers, recalls, reservoirs, and channels exist and
    how they are indexed. salt_balance uses those counts to iterate over the correct objects
    and to convert object-area information into basin totals.
  organic_mineral_mass_module: The organic/mineral mass state carries the salt constituent
    storage arrays that are summed here for soil and aquifer stocks, plus point-source salt
    inputs. Without those arrays, salt_balance could not report dissolved and solid salt stores
    or point-source totals.
  output_landscape_module: The output landscape module was listed as a dependency, but no
    specific imported state or type from it was resolved in the extracted references. It therefore
    appears to be a compile-time dependency rather than a source of directly used symbols
    in the extracted lines.
  aquifer_module: The aquifer module is part of the routine’s dependency set, but no explicit
    aquifer_module symbols were resolved in the extracted references. The salt accounting
    instead uses aquifer-related arrays from salt_aquifer and gwflow state for the visible
    calculations.
  hru_module: HRU area is the scaling factor that converts per-hectare HRU salt fluxes into
    basin kilograms for the HRU-based categories. That area controls nearly every land-surface
    salt total written by this routine.
  soil_module: Soil profile metadata determines how many layers to scan and how to convert
    layer thickness and bulk density into soil mass. Those values are needed to compute total
    solid salt stored in soil layers from layer salt concentrations.
  time_module: The current simulation date and end-of-period flags control when daily totals
    are written, when monthly and yearly averages are formed, and when average annual output
    is produced. The date fields are also written as the record header on each output line.
  salt_module: The daily HRU salt balance arrays hold the fluxes being accumulated for runoff,
    leaching, irrigation, deposition, and uptake. salt_balance sums those per-HRU/per-salt
    terms into basin totals and then zeroes the daily arrays for the next day.
  salt_aquifer: The aquifer salt balance arrays hold groundwater-related salt fluxes such
    as recharge, seepage, groundwater-to-stream loading, irrigation removal, and diversion.
    salt_balance uses them to report aquifer-side salt transport and to reset daily aquifer
    salt bookkeeping.
  constituent_mass_module: The constituent mass module provides the salt-constituent count
    and the soil/aquifer salt storage arrays used in stock calculations and point-source totals.
    Those shared constituent arrays are what make the basin salt balance consistent with the
    rest of the mass-balance system.
  res_salt_module: Reservoir and wetland salt output arrays capture inflow, outflow, seepage,
    fertilizer, irrigation, and diversion salt terms. salt_balance includes them in basin
    totals and then clears them after the daily report is written.
  ch_salt_module: Channel salt output arrays hold irrigation, diversion, and groundwater inflow
    terms for channels. salt_balance resets these daily channel salt bookkeeping values after
    the basin summary is written.
  gwflow_module: The groundwater-flow state determines whether the routine uses gwflow cell-based
    solute fields or the normal aquifer-module salt arrays. It also supplies the per-cell
    recharge, transport, and groundwater mass values that replace the aquifer-module paths
    when gwflow is active.
---

<!-- facts:header -->

Computes basin-wide daily salt loads and salt stocks for HRUs, aquifers, reservoirs, channels, and groundwater, then writes them to output files.

## Bottom Line

salt_balance totals the day’s salt fluxes and storage terms across the basin. It accumulates HRU, aquifer, reservoir, channel, and groundwater salt mass balance components into a 28-field basin summary, writes the daily record, and rolls the totals into monthly, yearly, and average-annual outputs.

After writing the outputs, it clears the per-day salt balance arrays so the next simulation day starts from zeroed flux accumulators. That makes this routine the daily bookkeeping step that supports the salt mass-balance reports used by SWAT+ output processing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

salt_balance runs after command has advanced the simulation through a day and after upstream routing, HRU, aquifer, reservoir, and groundwater processes have filled the daily salt balance arrays. Its outputs feed the basin salt mass-balance files used for daily, monthly, yearly, and average-annual reporting, while its zeroing step prepares those same daily arrays for the next day’s calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Sum HRU salt loadings and groundwater/channel contributions | The routine starts by summing lateral HRU salt loading into channels. It then adds groundwater-to-channel loading, using gwflow cell solute state when gwflow is active or the normal aquifer salt arrays otherwise, and stores the result in salt_basin(1:2). |
| 2. Sum surface routing, tile, recharge, and land-management fluxes | It accumulates basin totals for surface runoff, urban runoff, wetland runoff, tile drainage, soil leaching, groundwater upflux, wetland seepage, irrigation sources, rainfall, dry deposition, road salt, fertilizer, soil amendments, and plant uptake. Each category is aggregated over HRUs and salt constituents and written into salt_basin(3:18). |
| 3. Sum point sources and aquifer exchange terms | The routine totals point-source salt from internal recalls and outside recalls, then sums recharge to the aquifer and seepage from the aquifer. It also totals dissolved soil salt and dissolved groundwater salt, choosing gwflow-cell state or aquifer-module state depending on whether gwflow is active. |
| 4. Sum solid soil and solid groundwater storage | It computes dissolved soil salt storage from cs_soil, then estimates solid soil salt from soil layer thickness and bulk density, and finally estimates solid groundwater salt using ob area, a fixed aquifer thickness, and cs_aqu solid-salt fractions. These results are stored in salt_basin(25:28). |
| 5. Write the daily basin record and roll totals into period accumulators | The routine writes the daily 28-field salt_basin record to output unit 5080. It then adds the day’s totals into monthly, yearly, and average-annual accumulator arrays for later period output. |
| 6. Emit monthly output if the month ended | When time%end_mo is set, the routine divides the monthly stock terms by the number of days in the month, writes the monthly record to unit 5082, and clears salt_basin_mo back to zero for the next month. |
| 7. Emit yearly output if the year ended | When time%end_yr is set, it divides the yearly stock terms by the number of days in the year, writes the yearly record to unit 5084, and clears salt_basin_yr back to zero for the next year. |
| 8. Emit average-annual output at simulation end | When time%end_sim is set, the routine averages the annual totals across simulation years and the stock terms across the reporting days, then writes the final average-annual record to unit 5086. |
| 9. Clear daily salt balance arrays for the next day | After reporting, the routine zeros the daily HRU, wetland, aquifer, point-source, reservoir, channel, and gwflow salt balance arrays so that the next timestep starts with fresh accumulators. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%aqu, sp_ob%aqu, sp_ob%recall, ob(ob_ctr)%area_ha, sp_ob%res, sp_ob%chandeg` |
| [sym:organic_mineral_mass_module] | `cs_db, recsaltb_d, recoutsaltb_d, cs_soil, cs_aqu` | `cs_db%num_salts, recsaltb_d(i)%salt(m), recoutsaltb_d(i)%salt(m), cs_soil(i)%ly(jj)%salt(m), cs_soil(i)%ly(jj)%salt_min(m), cs_aqu(i)%salt(m), cs_aqu(i)%salt_min(m)` |
| [sym:output_landscape_module] | `No candidate outside references were resolved to this module` |  |
| [sym:aquifer_module] | `No candidate outside references were resolved to this module` |  |
| [sym:hru_module] | `hru` | `hru(i)%area_ha` |
| [sym:soil_module] | `soil` | `soil(i)%nly, soil(i)%phys(jj)%thick, soil(i)%phys(jj)%bd` |
| [sym:time_module] | `time` | `time%yrc, time%mo, time%day, time%end_mo, time%day_mo, time%end_yr, time%day_end_yr, time%end_sim, time%nbyr, time%days_prt` |
| [sym:salt_module] | `hsaltb_d` | `hsaltb_d(i)%salt(m)%latq, hsaltb_d(i)%salt(m)%surq, hsaltb_d(i)%salt(m)%urbq, hsaltb_d(i)%salt(m)%wetq, hsaltb_d(i)%salt(m)%tile, hsaltb_d(i)%salt(m)%perc, hsaltb_d(i)%salt(m)%gwup, hsaltb_d(i)%salt(m)%wtsp, hsaltb_d(i)%salt(m)%irsw, hsaltb_d(i)%salt(m)%irgw, hsaltb_d(i)%salt(m)%irwo, hsaltb_d(i)%salt(m)%rain, hsaltb_d(i)%salt(m)%dryd, hsaltb_d(i)%salt(m)%road, hsaltb_d(i)%salt(m)%fert, hsaltb_d(i)%salt(m)%amnd, hsaltb_d(i)%salt(m)%uptk, hsaltb_d(i)%salt(1)%diss, hsaltb_d(i)%salt(m)%soil` |
| [sym:salt_aquifer] | `asaltb_d` | `asaltb_d(i)%salt(m)%saltgw, asaltb_d(i)%salt(m)%rchrg, asaltb_d(i)%salt(m)%seep, asaltb_d(i)%salt(1)%diss, asaltb_d(i)%salt(m)%irr, asaltb_d(i)%salt(m)%div` |
| [sym:constituent_mass_module] | `cs_db, recsaltb_d, recoutsaltb_d, cs_soil, cs_aqu` | `cs_db%num_salts, recsaltb_d(i)%salt(m), recoutsaltb_d(i)%salt(m), cs_soil(i)%ly(jj)%salt(m), cs_soil(i)%ly(jj)%salt_min(m), cs_aqu(i)%salt(m), cs_aqu(i)%salt_min(m)` |
| [sym:res_salt_module] | `wetsalt_d, ressalt_d` | `wetsalt_d(i)%salt(m)%inflow, wetsalt_d(i)%salt(m)%outflow, wetsalt_d(i)%salt(m)%seep, wetsalt_d(i)%salt(m)%fert, wetsalt_d(i)%salt(m)%irrig, wetsalt_d(i)%salt(m)%div, ressalt_d(i)%salt(m)%inflow, ressalt_d(i)%salt(m)%outflow, ressalt_d(i)%salt(m)%seep, ressalt_d(i)%salt(m)%fert, ressalt_d(i)%salt(m)%irrig, ressalt_d(i)%salt(m)%div` |
| [sym:ch_salt_module] | `chsalt_d` | `chsalt_d(i)%salt(m)%irr, chsalt_d(i)%salt(m)%div, chsalt_d(i)%salt(m)%gw_in` |
| [sym:gwflow_module] | `gw_solute_flag, gwsol_ss, ncell, gw_state, gwsol_state` | `gw_solute_flag, gwsol_ss, ncell, gw_state, gwsol_state` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `salt_basin_mo(i)` | Every call, after the daily basin totals are computed and before the daily values are reset. | salt_basin_mo is incremented by the current day’s 28 salt totals so the routine can later form a monthly average or monthly total record. |
| `salt_basin_yr(i)` | Every call, after the daily basin totals are computed and before the yearly values are reset. | salt_basin_yr is incremented by the current day’s 28 salt totals so the routine can later form a yearly average or yearly total record. |
| `salt_basin_aa(i)` | Every call, after the daily basin totals are computed and before the average-annual values are written. | salt_basin_aa is incremented by the current day’s 28 salt totals so the end-of-simulation average annual report can be formed from all simulated days. |
| `salt_basin_mo(25)` | At month end, when time%end_mo == 1, before writing unit 5082. | Element 25 is divided by the number of days in the month so the monthly dissolved-soil-salt stock is reported as an average daily value rather than a cumulative sum. |
| `salt_basin_mo(26)` | At month end, when time%end_mo == 1, before writing unit 5082. | Element 26 is divided by the number of days in the month so the monthly solid-soil-salt stock is reported as an average daily value. |
| `salt_basin_mo(27)` | At month end, when time%end_mo == 1, before writing unit 5082. | Element 27 is divided by the number of days in the month so the monthly dissolved-groundwater-salt stock is reported as an average daily value. |
| `salt_basin_mo(28)` | At month end, when time%end_mo == 1, before writing unit 5082. | Element 28 is divided by the number of days in the month so the monthly solid-groundwater-salt stock is reported as an average daily value. |
| `salt_basin_mo` | At month end, after the monthly record is written. | The whole monthly accumulator array is reset to zero so the next month starts with no carried-over salt totals. |
| `salt_basin_yr(25)` | At year end, when time%end_yr == 1, before writing unit 5084. | Element 25 is divided by the number of days in the year so the yearly dissolved-soil-salt stock is reported as an average daily value. |
| `salt_basin_yr(26)` | At year end, when time%end_yr == 1, before writing unit 5084. | Element 26 is divided by the number of days in the year so the yearly solid-soil-salt stock is reported as an average daily value. |
| `salt_basin_yr(27)` | At year end, when time%end_yr == 1, before writing unit 5084. | Element 27 is divided by the number of days in the year so the yearly dissolved-groundwater-salt stock is reported as an average daily value. |
| `salt_basin_yr(28)` | At year end, when time%end_yr == 1, before writing unit 5084. | Element 28 is divided by the number of days in the year so the yearly solid-groundwater-salt stock is reported as an average daily value. |
| `salt_basin_yr` | At year end, after the yearly record is written. | The whole yearly accumulator array is reset to zero so the next year starts with no carried-over salt totals. |
| `salt_basin_aa(25)` | At simulation end, when time%end_sim == 1, before writing unit 5086. | Element 25 is divided by the total number of reporting days so the average-annual dissolved-soil-salt stock is reported on a daily average basis. |
| `salt_basin_aa(26)` | At simulation end, when time%end_sim == 1, before writing unit 5086. | Element 26 is divided by the total number of reporting days so the average-annual solid-soil-salt stock is reported on a daily average basis. |
| `salt_basin_aa(27)` | At simulation end, when time%end_sim == 1, before writing unit 5086. | Element 27 is divided by the total number of reporting days so the average-annual dissolved-groundwater-salt stock is reported on a daily average basis. |
| `salt_basin_aa(28)` | At simulation end, when time%end_sim == 1, before writing unit 5086. | Element 28 is divided by the total number of reporting days so the average-annual solid-groundwater-salt stock is reported on a daily average basis. |
| `hsaltb_d(i)%salt(m)%soil` | After the daily basin totals are written, during the reset loop over HRUs and salts. | The HRU soil salt storage term is cleared to zero so the next day’s soil-salt bookkeeping begins fresh. |
| `hsaltb_d(i)%salt(m)%surq` | After the daily basin totals are written, during the reset loop over HRUs and salts. | The HRU surface-runoff salt term is cleared so the next day’s runoff salt loading is not double counted. |
| `hsaltb_d(i)%salt(m)%latq` | After the daily basin totals are written, during the reset loop over HRUs and salts. | The HRU lateral-flow salt term is cleared so the next day’s lateral salt loading starts from zero. |
| `hsaltb_d(i)%salt(m)%urbq` | After the daily basin totals are written, during the reset loop over HRUs and salts. | The HRU urban-runoff salt term is cleared so the next day’s urban salt loading starts from zero. |
| `hsaltb_d(i)%salt(m)%wetq` | After the daily basin totals are written, during the reset loop over HRUs and salts. | The HRU wetland-runoff salt term is cleared so the next day’s wetland salt loading starts from zero. |
| `hsaltb_d(i)%salt(m)%tile` | After the daily basin totals are written, during the reset loop over HRUs and salts. | The HRU tile-drain salt term is cleared so the next day’s tile salt loading starts from zero. |
| `hsaltb_d(i)%salt(m)%perc` | After the daily basin totals are written, during the reset loop over HRUs and salts. | The HRU percolation salt term is cleared so the next day’s leaching salt loading starts from zero. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four source-history changes to salt_balance. On 2024-05-30 the file was imported from Bitbucket and already contained the daily basin salt balance logic and output/reset structure; on 2024-07-16 the salt_aquifer module name was corrected to salt_aquifer_module for compilation; on 2024-08-08 several local variables were initialized to zero; on 2024-10-08 the unused format label 7001 was commented out and a tab indentation was fixed; on 2025-11-17 the routine was cleaned up by removing unused local variables and changing the final terminator to end subroutine salt_balance.

- 2024-07-16: corrected the module import name from salt_aquifer to salt_aquifer_module so the routine compiles against the current salt aquifer module.
- 2024-08-08: initialized the local loop counters, accumulators, and salt_basin array to zero at declaration time to avoid uninitialized values.
- 2024-10-08: removed the live 7001 format label by commenting it out and fixed one indentation/tab issue in the gwflow reset loop.
- 2025-11-17: removed unused locals and replaced the bare end statement with end subroutine salt_balance.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_balance' has no extracted documentation comment.
- organic_mineral_mass_module and output_landscape_module were listed as uses but no resolved outside references were extracted for them.
- aquifer_module was listed as a use but no resolved outside references were extracted for it.
- The source shows conditional use of gwflow cell state versus aquifer-module salt arrays; the documented behavior follows the visible branches in the extracted lines.
