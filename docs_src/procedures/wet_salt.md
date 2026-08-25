---
kind: procedure
symbol: wet_salt
title: wet_salt
status: filled
source_hash: a25c72151d9fa559
version_label: SWAT+ 62.0.0
args:
  icmd: Selects the command/hydrograph record whose surface-runon salt input is read from
    `obcs(icmd)%hin_sur(1)%salt(isalt)`.
  ihru: Selects the HRU/wetland whose water volume, salt storage, seepage, soil layer, and
    output arrays are updated.
locals:
  isalt: Loop index for each salt ion simulated in `cs_db%num_salts`; it is reused to reset,
    compute, and store balance terms for each constituent.
  salt_mass_beg: Stores the wetland salt mass at the start of the day from `wet_water(ihru)%salt(isalt)`
    so the balance can be started from existing storage.
  salt_conc_beg: Holds the starting salt concentration in wetland water, computed from starting
    mass and wetland water volume when volume is positive.
  salt_mass_end: Holds the computed end-of-day wetland salt mass after inflow, outflow, and
    seepage are applied.
  salt_conc_end: Holds the computed end-of-day wetland salt concentration from the ending
    mass and wetland water volume when volume is positive.
  salt_inflow: Holds the salt mass entering the wetland from surface runon for the current
    command and salt ion.
  salt_outflow: Holds the salt mass leaving the wetland with stream outflow, limited so it
    cannot exceed mass available in the wetland.
  salt_seep: Holds the salt mass leaving the wetland through seepage, limited so it cannot
    exceed remaining mass available.
  mass_avail: Tracks the salt mass still available in the wetland after inflow, outflow, and
    seepage deductions so losses cannot remove more mass than exists.
  seep_mass: Converts seeped salt from total mass to area-based loading (`kg/ha`) before adding
    it to the top soil layer and storing the seep output term.
uses:
  reservoir_data_module: This module supplies the salt-constituent database and the wetland
    surface-runon hydrograph structure, which determine how many salts are processed and how
    much salt enters the wetland from the command record.
  reservoir_module: This module holds the wetland salt balance output structure that `wet_salt`
    fills for later reporting and downstream mass-balance use.
  water_body_module: The wetland seepage volume comes from `wet_wat_d(ihru)%seep`; that water
    loss is what gets converted into salt seepage mass in this routine.
  hydrograph_module: Wetland water volume comes from `wet(ihru)%flo`, and outflow volume comes
    from `ht2%flo`; both are needed to convert salt mass to concentration and to compute salt
    lost in stream outflow.
  hru_module: The HRU area `hru(ihru)%area_ha` is required to convert wetland salt outflow
    and seepage from mass to per-hectare loads for runoff and soil accounting.
  constituent_mass_module: This module defines the constituent mass arrays and hydrograph
    containers used to read starting wetland salt storage, incoming salt, and the top-layer
    soil salt state that receives seeped mass.
  res_salt_module: The `res_salt_module` structure is the destination for the wetland salt
    balance terms that this routine computes and stores for output.
  climate_module: The hydrologic state from `climate_module`-driven water routing determines
    the wetland water volume and therefore the salt concentration and outflow/seepage calculations.
---

<!-- facts:header -->

Computes the wetland salt-ion mass balance for one HRU and command record. It updates wetland salt storage, concentration, seepage loading to soil, and runoff salt loading outputs.

## Bottom Line

wet_salt loops over every simulated salt ion and computes a daily wetland balance for the selected HRU. It starts from the stored wetland salt mass, adds incoming surface-runon salt, subtracts salt carried out by wetland outflow and seepage, then writes the ending mass and concentration back to the wetland state.

The routine also records the salt balance terms in `wetsalt_d`, converts outflow to the HRU runoff term `wetqsalt`, and adds seeped salt to the top soil layer through `cs_soil`. Those outputs are what later wetland, runoff, and soil-constituent accounting steps use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `wetland_control` after wetland water and other wetland state terms have been set for the current HRU/command step. Its results feed wetland constituent accounting, runoff salt loading through `wetqsalt`, and soil salt addition through `wtspsalt` and `cs_soil`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. reset outputs for each salt | Initialize every `wetsalt_d(ihru)%salt(isalt)` balance field to zero so the day's salt outputs start clean before any calculations. |
| 2. process each salt ion | Loop over all salts defined by `cs_db%num_salts` and compute the wetland balance one ion at a time. |
| 3. read start-of-day storage and concentration | Load the starting wetland salt mass from `wet_water`, compute the starting concentration from wetland water volume when water is present, and seed the available-mass tracker. |
| 4. add surface-runon salt inflow | Read incoming salt from `obcs(icmd)%hin_sur(1)%salt(isalt)` and add it to the available wetland salt mass. |
| 5. compute and limit stream outflow loss | Estimate salt carried out by stream outflow from `ht2%flo` and starting concentration, then cap the loss at the mass still available and subtract it from the balance. |
| 6. compute and limit seepage loss | Estimate salt lost with wetland seepage from `wet_wat_d(ihru)%seep` and starting concentration, then cap it at remaining mass and subtract it from the balance. |
| 7. compute ending storage and concentration | Form the end-of-day salt mass from inflow minus outflow minus seepage, then convert it to concentration when wetland water volume is positive. |
| 8. write wetland balance outputs | Store inflow, outflow, seep, ending mass, concentration, and wetland volume into `wetsalt_d` for the current HRU and salt ion. |
| 9. convert outflow to HRU runoff load | Convert the salt outflow mass to `kg/ha` using HRU area and store it in `wetqsalt` for runoff accounting. |
| 10. add seeped salt to soil and record seep load | Convert seeped salt to `kg/ha`, add it to the top soil layer `cs_soil(ihru)%ly(1)%salt(isalt)`, and save the seep load in `wtspsalt`. |
| 11. finish | Exit the salt-ion loop and return to the caller after all salt balances have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `cs_db, wet_water, obcs` | `cs_db%num_salts, wet_water(ihru)%salt(isalt), wet_water(ihru)%saltc(isalt), obcs(icmd)%hin_sur(1)%salt(isalt)` |
| [sym:reservoir_module] | `wetsalt_d` | `wetsalt_d(ihru)%salt(isalt)%inflow, wetsalt_d(ihru)%salt(isalt)%outflow, wetsalt_d(ihru)%salt(isalt)%seep, wetsalt_d(ihru)%salt(isalt)%mass, wetsalt_d(ihru)%salt(isalt)%conc, wetsalt_d(ihru)%salt(isalt)%volm` |
| [sym:water_body_module] | `wet_wat_d` | `wet_wat_d(ihru)%seep` |
| [sym:hydrograph_module] | `wet, ht2` | `wet(ihru)%flo, ht2%flo` |
| [sym:hru_module] | `wetqsalt, hru, wtspsalt` | `hru(ihru)%area_ha` |
| [sym:constituent_mass_module] | `cs_db, wet_water, obcs, cs_soil` | `cs_db%num_salts, wet_water(ihru)%salt(isalt), obcs(icmd)%hin_sur(1)%salt(isalt), wet_water(ihru)%saltc(isalt), cs_soil(ihru)%ly(1)%salt(isalt)` |
| [sym:res_salt_module] | `wetsalt_d` | `wetsalt_d(ihru)%salt(isalt)%inflow, wetsalt_d(ihru)%salt(isalt)%outflow, wetsalt_d(ihru)%salt(isalt)%seep, wetsalt_d(ihru)%salt(isalt)%mass, wetsalt_d(ihru)%salt(isalt)%conc, wetsalt_d(ihru)%salt(isalt)%volm` |
| [sym:climate_module] | `ht2, wet` | `ht2%flo, wet(ihru)%flo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wetsalt_d(ihru)%salt(isalt)%inflow` | For every salt ion processed in the main loop. | Stores the incoming surface-runon salt mass for the current HRU and command record so the daily wetland salt balance can report inflow separately from storage changes. |
| `wetsalt_d(ihru)%salt(isalt)%outflow` | For every salt ion processed in the main loop, after computing the mass carried by `ht2%flo` and capping it if necessary. | Stores the salt mass exported from the wetland with stream outflow so the balance can track how much salt leaves with routed water. |
| `wetsalt_d(ihru)%salt(isalt)%seep` | For every salt ion processed in the main loop, after computing seepage mass and limiting it to available mass. | Stores the salt mass lost through wetland seepage so seep-driven transfer out of the wetland can be reported separately from stream outflow. |
| `wetsalt_d(ihru)%salt(isalt)%mass` | For every salt ion processed in the main loop. | Stores the updated wetland salt inventory at the end of the day after inflow, outflow, and seepage are applied. |
| `wetsalt_d(ihru)%salt(isalt)%conc` | For every salt ion processed in the main loop when wetland water volume is positive; otherwise concentration is set to zero. | Stores the ending wetland salt concentration derived from the new salt mass and current water volume. |
| `wet_water(ihru)%salt(isalt)` | For every salt ion processed in the main loop. | Updates the wetland's stored salt mass for the current HRU so later wetland constituent steps start from the new end-of-day inventory. |
| `wet_water(ihru)%saltc(isalt)` | For every salt ion processed in the main loop. | Updates the wetland's stored salt concentration for the current HRU so later hydrologic or constituent routines can use the new concentration. |
| `wetsalt_d(ihru)%salt(isalt)%volm` | For every salt ion processed in the main loop. | Records the current wetland water volume alongside the salt balance so output tables can relate salt mass and concentration to the actual wetland storage volume. |
| `wetqsalt(ihru,isalt)` | For every salt ion processed in the main loop. | Stores the wetland salt load routed into HRU runoff, expressed on an area basis, for use in runoff accounting. |
| `cs_soil(ihru)%ly(1)%salt(isalt)` | For every salt ion processed in the main loop. | Adds seeped wetland salt to the top soil layer so the wetland seep loss becomes an input to soil constituent mass. |
| `wtspsalt(ihru,isalt)` | For every salt ion processed in the main loop. | Stores the seepage salt load on an area basis for output and mass-balance reporting. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed wet_salt. df07e3f added the routine with its wetland salt mass-balance logic, output assignments, and soil/runoff transfer terms. 35b029c made only whitespace cleanup at the end of the file. 2ee1889 trimmed the hydrograph_module import list and removed unused local variables `iwst` and `dum`. 39fabde initialized the local counters and balance variables to zero and fixed indentation in the two `else` blocks.

- df07e3f introduced the wetland salt balance subroutine and all of its storage, inflow/outflow, seepage, runoff, and soil-update behavior.
- 35b029c made no behavioral change; it only removed extra trailing blank lines near the return statement.
- 2ee1889 removed unused imports and unused local variables, reducing scope without changing the wetland salt calculations.
- 39fabde initialized the routine's local variables to zero and corrected indentation, but left the calculation flow unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wet_salt' has no extracted documentation comment.
