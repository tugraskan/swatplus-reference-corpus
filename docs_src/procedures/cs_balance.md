---
kind: procedure
symbol: cs_balance
title: cs_balance
status: filled
source_hash: b551f34167808cc2
version_label: SWAT+ 62.0.0
locals:
  i: Loop index used throughout the routine to iterate over HRUs, recalls, aquifers, cells,
    and output arrays.
  m: Inner loop index used when resetting per-constituent balance arrays and related state
    at the end of the routine.
  ob_ctr: Tracks the current aquifer object number when converting aquifer concentrations
    to basin totals using object area.
  num_days: Holds the number of days in the current month or year, or the number of print
    days for average-annual normalization.
  sol_index: Offsets into the groundwater solute arrays so the routine can reach the three
    constituent entries associated with the simulated salts.
  jj: Indexes soil layers when summing dissolved and sorbed soil constituent masses across
    each HRU profile.
  cssum1: Temporary accumulator for the first constituent, seo4, before storing the summed
    basin total.
  cssum2: Temporary accumulator for the second constituent, seo3, before storing the summed
    basin total.
  cssum3: Temporary accumulator for the third constituent, boron, before storing the summed
    basin total.
  cs_basin: Temporary 87-element array that holds the basin balance values for the current
    day before they are written and copied into period summaries.
uses:
  hydrograph_module: The routine uses `sp_ob%hru` and `sp_ob%recall` to know how many HRUs
    and recall point-source objects exist, which controls every loop that aggregates HRU and
    point-source constituent fluxes.
  organic_mineral_mass_module: This module provides the constituent database size, point-source
    mass arrays, and soil-layer constituent arrays that cs_balance sums into basin totals
    and uses to locate the three simulated constituents in each balance table.
  output_landscape_module: This module supplies the groundwater-flow switch used to choose
    between gwflow-based and legacy aquifer accounting, and it holds the monthly, yearly,
    and average-annual accumulator arrays that cs_balance updates and then resets.
  aquifer_module: When gwflow is off, cs_balance falls back to aquifer-module balances for
    groundwater loading, recharge, seepage, reactions, sorption, and total dissolved mass.
  hru_module: HRU area is the scaling factor that converts per-hectare balance rates into
    basin totals for every HRU-based flux and storage term.
  soil_module: The soil profile layer count determines how many layers cs_balance must traverse
    when summing dissolved and sorbed soil constituent masses for each HRU.
  time_module: 'The simulation clock controls record labeling and all period boundaries: daily
    writes always occur, while monthly, yearly, and average-annual writes and normalizations
    happen only at the corresponding time flags.'
  constituent_mass_module: This module defines the constituent database and the soil/point-source
    mass structures that cs_balance reads and later zeros, including the three-constituent
    arrays for dissolved and sorbed soil mass.
  cs_module: cs_balance reads and resets the HRU balance structure fields in `hcsb_d` for
    all three constituents and all daily flux pathways, so this module is the source of the
    daily soil-system balance state.
  cs_aquifer: When gwflow is disabled, these aquifer constituent totals supply the dissolved
    and sorbed groundwater mass terms that cs_balance uses in place of gwflow state arrays.
  res_cs_module: Reservoir constituent balance arrays are reset here because reservoir inflow,
    outflow, seepage, fertilization, irrigation, and diversion balances must start fresh for
    the next day after this summary routine runs.
  ch_cs_module: Channel constituent balance arrays are reset here because channel irrigation,
    diversion, and groundwater-inflow balances are accumulated daily and must be cleared after
    the basin summary is written.
  gwflow_module: The groundwater-flow module matters because, when gwflow is active, cs_balance
    pulls dissolved, recharge, reaction, and sorption terms from gwflow cell state instead
    of the legacy aquifer balances and then zeroes the daily gwflow solute accumulators.
---

<!-- facts:header -->

Builds daily, monthly, yearly, and average-annual basin constituent mass-balance totals for three constituents: seo4, seo3, and boron.

## Bottom Line

cs_balance computes basin-wide constituent fluxes and storage terms for three constituents by summing HRU, recall/point-source, aquifer, soil, reservoir, channel, and groundwater-flow states into an 87-element balance array. It then writes daily totals and rolls those values into monthly, yearly, and average-annual summaries for later output.

After writing the requested outputs, it clears the daily balance arrays in HRUs, aquifers, point sources, reservoirs, channels, and groundwater solute cells so the next day starts from zeroed flux accumulators.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after constituent simulations have populated the daily balance arrays for HRUs, aquifers, point sources, reservoirs, channels, and groundwater flow. Its results feed the basin output files for daily, monthly, yearly, and average-annual constituent accounting, and it also clears the daily balance state for the next day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local accumulators and the 87-element basin balance array. | The routine starts with zeroed counters and sum variables, including the daily basin balance array that will collect all flux and storage totals. |
| 2. Sum HRU lateral-load terms for the three constituents. | It loops over HRUs, multiplies lateral-flow loading by HRU area, and stores the three basin totals in `cs_basin(1)`, `cs_basin(30)`, and `cs_basin(59)`. |
| 3. Sum HRU surface-runoff loads. | It repeats the HRU loop for surface runoff loading and writes the basin totals to `cs_basin(2)`, `cs_basin(31)`, and `cs_basin(60)`. |
| 4. Sum sediment, urban, wetland, tile, leaching, groundwater-up, wetland-seepage, irrigation, deposition, uptake, reaction, and sorption terms from HRUs. | The routine computes each HRU-based constituent flux category in turn, with optional gwflow tile contributions, and maps each category into the proper slots of `cs_basin` for all three constituents. |
| 5. Add point-source inflow and outflow loads. | It sums internal recall inputs and external recall inflows across recall objects and stores the totals in the point-source positions of `cs_basin`. |
| 6. Sum dissolved and sorbed soil constituent storage. | The routine loops through HRUs and soil layers, summing dissolved constituent mass and sorbed constituent mass from `cs_soil` and placing the totals in the soil-storage slots. |
| 7. Compute groundwater/aquifer loads, reactions, and storage using gwflow or legacy aquifer state. | When gwflow is active, it sums groundwater solute fluxes and state mass from `gwsol_ss` and `gwsol_state`; otherwise it uses aquifer-module arrays such as `acsb_d` and `cs_aqu`. |
| 8. Write the daily basin balance record and accumulate period totals. | It writes the daily 87-field record to unit 6080 and adds every basin term into the monthly, yearly, and average-annual accumulators. |
| 9. On month end, normalize state-like terms and write the monthly record. | If `time%end_mo` is set, it divides selected monthly storage terms by the number of days in the month, writes the monthly record to unit 6082, and clears `cs_basin_mo`. |
| 10. On year end, normalize state-like terms and write the yearly record. | If `time%end_yr` is set, it divides selected yearly storage terms by the number of days in the year, writes the yearly record to unit 6084, and clears `cs_basin_yr`. |
| 11. On simulation end, convert accumulated totals to average-annual values and write the final record. | At `time%end_sim`, it divides non-state categories by simulated years, divides selected state-like outputs by print days, and writes the average-annual record to unit 6086. |
| 12. Reset daily HRU, aquifer, point-source, reservoir, channel, and gwflow balance arrays. | It clears all daily constituent-balance fields so the next model day starts with zeroed flux accumulators. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru, sp_ob%recall` |
| [sym:organic_mineral_mass_module] | `cs_db, reccsb_d, recoutcsb_d, cs_soil` | `cs_db%num_salts, reccsb_d(i)%cs(1), reccsb_d(i)%cs(2), reccsb_d(i)%cs(3), recoutcsb_d(i)%cs(1), recoutcsb_d(i)%cs(2), recoutcsb_d(i)%cs(3), cs_soil(i)%ly(jj)%cs(1), cs_soil(i)%ly(jj)%cs(2), cs_soil(i)%ly(jj)%cs(3), cs_soil(i)%ly(jj)%cs_sorb(1), cs_soil(i)%ly(jj)%cs_sorb(2), cs_soil(i)%ly(jj)%cs_sorb(3)` |
| [sym:output_landscape_module] | `bsn_cc, cs_basin_mo, cs_basin_yr, cs_basin_aa` | `bsn_cc%gwflow, cs_basin_mo, cs_basin_yr, cs_basin_aa` |
| [sym:aquifer_module] | `acsb_d` | `acsb_d(i)%cs(1)%csgw, acsb_d(i)%cs(2)%csgw, acsb_d(i)%cs(3)%csgw, acsb_d(i)%cs(1)%rchrg, acsb_d(i)%cs(2)%rchrg, acsb_d(i)%cs(3)%rchrg, acsb_d(i)%cs(1)%seep, acsb_d(i)%cs(2)%seep, acsb_d(i)%cs(3)%seep, acsb_d(i)%cs(1)%rctn, acsb_d(i)%cs(2)%rctn, acsb_d(i)%cs(3)%rctn, acsb_d(i)%cs(1)%sorb, acsb_d(i)%cs(2)%sorb, acsb_d(i)%cs(3)%sorb` |
| [sym:hru_module] | `hru` | `hru(i)%area_ha` |
| [sym:soil_module] | `soil` | `soil(i)%nly` |
| [sym:time_module] | `time` | `time%yrc, time%mo, time%day, time%end_mo, time%end_yr, time%end_sim, time%day_mo, time%day_end_yr, time%nbyr, time%days_prt` |
| [sym:constituent_mass_module] | `cs_db, reccsb_d, recoutcsb_d, cs_soil` | `cs_db%num_salts, reccsb_d(i)%cs(1), reccsb_d(i)%cs(2), reccsb_d(i)%cs(3), recoutcsb_d(i)%cs(1), recoutcsb_d(i)%cs(2), recoutcsb_d(i)%cs(3), cs_soil(i)%ly(jj)%cs(1), cs_soil(i)%ly(jj)%cs(2), cs_soil(i)%ly(jj)%cs(3), cs_soil(i)%ly(jj)%cs_sorb(1), cs_soil(i)%ly(jj)%cs_sorb(2), cs_soil(i)%ly(jj)%cs_sorb(3)` |
| [sym:cs_module] | `hcsb_d` | `hcsb_d(i)%cs(1)%latq, hcsb_d(i)%cs(2)%latq, hcsb_d(i)%cs(3)%latq, hcsb_d(i)%cs(1)%surq, hcsb_d(i)%cs(2)%surq, hcsb_d(i)%cs(3)%surq, hcsb_d(i)%cs(1)%sedm, hcsb_d(i)%cs(2)%sedm, hcsb_d(i)%cs(3)%sedm, hcsb_d(i)%cs(1)%urbq, hcsb_d(i)%cs(2)%urbq, hcsb_d(i)%cs(3)%urbq, hcsb_d(i)%cs(1)%wetq, hcsb_d(i)%cs(2)%wetq, hcsb_d(i)%cs(3)%wetq, hcsb_d(i)%cs(1)%tile, hcsb_d(i)%cs(2)%tile, hcsb_d(i)%cs(3)%tile, hcsb_d(i)%cs(1)%perc, hcsb_d(i)%cs(2)%perc, hcsb_d(i)%cs(3)%perc, hcsb_d(i)%cs(1)%gwup, hcsb_d(i)%cs(2)%gwup, hcsb_d(i)%cs(3)%gwup, hcsb_d(i)%cs(1)%wtsp, hcsb_d(i)%cs(2)%wtsp, hcsb_d(i)%cs(3)%wtsp, hcsb_d(i)%cs(1)%irsw, hcsb_d(i)%cs(2)%irsw, hcsb_d(i)%cs(3)%irsw, hcsb_d(i)%cs(1)%irgw, hcsb_d(i)%cs(2)%irgw, hcsb_d(i)%cs(3)%irgw, hcsb_d(i)%cs(1)%irwo, hcsb_d(i)%cs(2)%irwo, hcsb_d(i)%cs(3)%irwo, hcsb_d(i)%cs(1)%rain, hcsb_d(i)%cs(2)%rain, hcsb_d(i)%cs(3)%rain, hcsb_d(i)%cs(1)%dryd, hcsb_d(i)%cs(2)%dryd, hcsb_d(i)%cs(3)%dryd, hcsb_d(i)%cs(1)%fert, hcsb_d(i)%cs(2)%fert, hcsb_d(i)%cs(3)%fert, hcsb_d(i)%cs(1)%uptk, hcsb_d(i)%cs(2)%uptk, hcsb_d(i)%cs(3)%uptk, hcsb_d(i)%cs(1)%rctn, hcsb_d(i)%cs(2)%rctn, hcsb_d(i)%cs(3)%rctn, hcsb_d(i)%cs(1)%sorb, hcsb_d(i)%cs(2)%sorb, hcsb_d(i)%cs(3)%sorb` |
| [sym:cs_aquifer] | `cs_aqu` | `cs_aqu(i)%cs(1), cs_aqu(i)%cs(2), cs_aqu(i)%cs(3), cs_aqu(i)%cs_sorb(1), cs_aqu(i)%cs_sorb(2), cs_aqu(i)%cs_sorb(3)` |
| [sym:res_cs_module] | `wetcs_d, rescs_d` | `wetcs_d, rescs_d` |
| [sym:ch_cs_module] | `chcs_d` | `chcs_d` |
| [sym:gwflow_module] | `gw_solute_flag, gwsol_ss, ncell, gw_state, gwsol_state` | `gw_solute_flag, gwsol_ss, ncell, gw_state, gwsol_state` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_basin_mo(i)` | At every call, after the daily basin record is accumulated into the period arrays. | `cs_basin_mo(i)` stores the running monthly sum for each daily basin balance field until month end, when selected storage fields are divided by days in the month and the array is written and reset. |
| `cs_basin_yr(i)` | At every call, after the daily basin record is accumulated into the period arrays. | `cs_basin_yr(i)` stores the running yearly sum for each daily basin balance field until year end, when selected storage fields are divided by days in the year and the array is written and reset. |
| `cs_basin_aa(i)` | At every call, after the daily basin record is accumulated into the period arrays. | `cs_basin_aa(i)` stores the running simulation-total sum for each basin balance field until the final simulation step, when non-state categories are averaged by years and selected state-like terms are normalized by print days before writing. |
| `cs_basin_mo(21)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(21)` is converted from a monthly sum to a monthly mean dissolved-soil constituent storage value before the monthly output is written. |
| `cs_basin_mo(22)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(22)` is converted from a monthly sum to a monthly mean sorbed-soil constituent storage value before the monthly output is written. |
| `cs_basin_mo(28)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(28)` is converted from a monthly sum to a monthly mean dissolved-groundwater mass value before the monthly output is written. |
| `cs_basin_mo(29)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(29)` is converted from a monthly sum to a monthly mean sorbed-groundwater mass value before the monthly output is written. |
| `cs_basin_mo(50)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(50)` is converted from a monthly sum to a monthly mean dissolved-soil constituent storage value for the second constituent before the monthly output is written. |
| `cs_basin_mo(51)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(51)` is converted from a monthly sum to a monthly mean sorbed-soil constituent storage value for the second constituent before the monthly output is written. |
| `cs_basin_mo(57)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(57)` is converted from a monthly sum to a monthly mean dissolved-groundwater mass value for the second constituent before the monthly output is written. |
| `cs_basin_mo(58)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(58)` is converted from a monthly sum to a monthly mean sorbed-groundwater mass value for the second constituent before the monthly output is written. |
| `cs_basin_mo(79)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(79)` is converted from a monthly sum to a monthly mean dissolved-soil constituent storage value for the third constituent before the monthly output is written. |
| `cs_basin_mo(80)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(80)` is converted from a monthly sum to a monthly mean sorbed-soil constituent storage value for the third constituent before the monthly output is written. |
| `cs_basin_mo(86)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(86)` is converted from a monthly sum to a monthly mean dissolved-groundwater mass value for the third constituent before the monthly output is written. |
| `cs_basin_mo(87)` | At month end (`time%end_mo == 1`). | `cs_basin_mo(87)` is converted from a monthly sum to a monthly mean sorbed-groundwater mass value for the third constituent before the monthly output is written. |
| `cs_basin_mo` | Every call, before any period-end normalization; it is later cleared to zero at month end. | `cs_basin_mo` accumulates the daily basin balance terms so the routine can emit a monthly aggregate when the month ends. |
| `cs_basin_yr(21)` | At year end (`time%end_yr == 1`). | `cs_basin_yr(21)` is converted from a yearly sum to a yearly mean dissolved-soil constituent storage value before the yearly output is written. |
| `cs_basin_yr(22)` | At year end (`time%end_yr == 1`). | `cs_basin_yr(22)` is converted from a yearly sum to a yearly mean sorbed-soil constituent storage value before the yearly output is written. |
| `cs_basin_yr(28)` | At year end (`time%end_yr == 1`). | `cs_basin_yr(28)` is converted from a yearly sum to a yearly mean dissolved-groundwater mass value before the yearly output is written. |
| `cs_basin_yr(29)` | At year end (`time%end_yr == 1`). | `cs_basin_yr(29)` is converted from a yearly sum to a yearly mean sorbed-groundwater mass value before the yearly output is written. |
| `cs_basin_yr(50)` | At year end (`time%end_yr == 1`). | `cs_basin_yr(50)` is converted from a yearly sum to a yearly mean dissolved-soil constituent storage value for the second constituent before the yearly output is written. |
| `cs_basin_yr(51)` | At year end (`time%end_yr == 1`). | `cs_basin_yr(51)` is converted from a yearly sum to a yearly mean sorbed-soil constituent storage value for the second constituent before the yearly output is written. |
| `cs_basin_yr(57)` | At year end (`time%end_yr == 1`). | `cs_basin_yr(57)` is converted from a yearly sum to a yearly mean dissolved-groundwater mass value for the second constituent before the yearly output is written. |
| `cs_basin_yr(58)` | At year end (`time%end_yr == 1`). | `cs_basin_yr(58)` is converted from a yearly sum to a yearly mean sorbed-groundwater mass value for the second constituent before the yearly output is written. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The earliest resolved commit, c7c8e22, introduced the cs_balance procedure and its full basin mass-balance workflow. Later c38f3b8 removed a duplicate `ncell` import from `gwflow_module`; 2405a68 changed the import to `cs_aquifer_module` for compilation; 39fabde initialized the local counters, accumulators, and basin array to zero; 2ee1889 removed the unused `ihru` import and several unused local variables and changed the final statement to `end subroutine cs_balance`; f1e61a3 only fixed indentation in the gwflow reset loop.

- c38f3b8 removed the duplicated `ncell` symbol from the gwflow import list; the balance calculations and outputs stayed the same.
- f1e61a3 only corrected indentation in the gwflow reset loop; no logic changed.
- 39fabde initialized local counters, sums, and `cs_basin` to zero at declaration, which made the daily balance accumulation start from known values.
- 2405a68 changed the module reference from `cs_aquifer` to `cs_aquifer_module` so the routine compiled against the correct aquifer source.
- c7c8e22 added the `cs_balance` subroutine with its daily basin balance calculations, monthly/yearly/average-annual output writes, and end-of-day resets.
- 2ee1889 removed the unused `ihru` import and unused scalar locals, and changed the termination statement to `end subroutine cs_balance`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cs_balance' has no extracted documentation comment.
