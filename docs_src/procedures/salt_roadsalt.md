---
kind: procedure
symbol: salt_roadsalt
title: salt_roadsalt
status: filled
source_hash: c4de7e8331349d25
version_label: SWAT+ 62.0.0
locals:
  iadep: Index of the atmospheric-deposition dataset linked to the HRU’s weather station;
    used to pick the road-salt input tables in `rdapp_salt`.
  j: HRU index for the current call. It is loaded from `ihru` and used to address HRU-specific
    storage such as `hru(j)`, `hsaltb_d(j)`, and `cs_soil(j)`.
  iob: Connectivity/object index for the current HRU. It is obtained from `hru(j)%obj_no`
    and used to find the linked weather station through `ob(iob)%wst`.
  ist: Atmospheric-deposition time-step index (`atmodep_cont%ts`). It selects which deposition
    record is active for the current day/month/year.
  isalt: Loop counter over simulated salt ions. Each pass updates road-salt loading for one
    salt species.
  const: Month-length divisor used only for monthly deposition. It is the number of days in
    the current month, so monthly road-salt inputs can be converted to a daily kg/ha addition.
uses:
  basin_module: This module tells the routine whether salt simulation is active and how many
    salt ions to loop over. If `num_salts` is zero, the routine does nothing.
  organic_mineral_mass_module: This module holds the HRU soil constituent masses that receive
    the added road-salt load. The routine increments the first soil layer’s salt mass for
    each ion here.
  hydrograph_module: '`hydrograph_module` provides the `ob` connectivity table and `iwst`
    weather-station pointer. `salt_roadsalt` uses them to move from the HRU object to the
    correct weather station, which is needed to choose the right atmospheric-deposition record.'
  hru_module: '`hru_module` provides the active HRU index `ihru` and the HRU table `hru`.
    The routine uses the current HRU’s `obj_no` to find the linked object and derive the weather-station
    connection for that HRU.'
  climate_module: '`climate_module` supplies the atmospheric-deposition controls and road-salt
    input tables. `atmodep_cont` selects the active deposition time step, and `rdapp_salt`
    contains the month-, day-, or annual-average road-salt loads added to the soil.'
  output_landscape_module: The output-landscape state is imported in this routine, but no
    resolved component from that module appears in the extracted source lines. It matters
    only if landscape output bookkeeping depends on the HRU-to-weather-station context established
    here; source-backed usage was not extracted.
  salt_module: '`salt_module` owns the salt-balance arrays updated by this routine. `hsaltb_d(j)%salt(isalt)%road`
    records the road-salt flux added for each salt ion before that same amount is added to
    the soil profile.'
  constituent_mass_module: '`constituent_mass_module` provides the salt-constituent database
    and soil constituent storage. `num_salts` controls the ion loop, and `cs_soil(j)%ly(1)%salt(isalt)`
    is the soil reservoir that receives the applied mass.'
---

<!-- facts:header -->

Adds applied road-salt mass to the active HRU soil profile, one salt ion at a time. The routine selects the correct weather/deposition record for the HRU and converts monthly, yearly, or annual-average road-salt inputs into per-day/per-interval soil additions.

## Bottom Line

`salt_roadsalt` is the road-salt input routine for salt constituents. For the current HRU, it finds the linked weather station and atmospheric-deposition record, then loads road-applied salt into the first soil layer for each simulated salt ion.

The amount added depends on the deposition time basis: monthly inputs are divided by the number of days in the month, yearly inputs use the day-specific yearly table, and annual-average inputs divide the annual rate by 365. The routine updates both the salt-balance bookkeeping (`hsaltb_d`) and the soil constituent mass state (`cs_soil`).

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `hru_control` during the HRU process after salt simulation has been enabled and atmospheric road-salt inputs are available. `hru_control` sets up the current HRU context, then calls `salt_roadsalt` before `salt_lch`, so the deposited road salt is in the soil profile before later salt-leaching calculations use it.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check salts enabled | The routine exits unless the constituent database says at least one salt ion is being simulated. This prevents any road-salt bookkeeping when salt constituents are off. |
| 2. map HRU to weather station | It uses the current HRU index to find the HRU object number, then follows that object to the linked weather station and atmospheric-deposition pointer. This establishes which road-salt input record belongs to the HRU. |
| 3. require valid deposition step | The routine only proceeds when the atmospheric-deposition time-step index is within the defined record count. That guards the table lookup for road-salt inputs. |
| 4. process monthly road salt | For monthly deposition, it computes the month length in days, loops over every salt ion, converts the monthly road-salt amount to a daily equivalent by dividing by the month length, stores that flux in the salt-balance array, and adds it to the first soil layer. |
| 5. process yearly road salt | For yearly deposition, it loops over each salt ion, reads the day-specific annual table entry for the current day and deposition step, records that flux in the salt-balance array, and adds it to the first soil layer. |
| 6. process annual-average road salt | For annual-average deposition, it loops over each salt ion, converts the annual road-salt rate to a daily value by dividing by 365, stores the flux in the salt-balance array, and adds it to the first soil layer. |
| 7. return | The subroutine returns after all eligible road-salt additions have been written to the salt-balance and soil constituent states. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `cs_db` | `cs_db%num_salts` |
| [sym:organic_mineral_mass_module] | `cs_soil` | `cs_soil(j)%ly(1)%salt(isalt)` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:hru_module] | `hru, ihru` | `hru(j)%obj_no` |
| [sym:climate_module] | `wst, atmodep_cont, rdapp_salt` | `wst(iwst)%wco%atmodep, atmodep_cont%ts, atmodep_cont%num, atmodep_cont%timestep, rdapp_salt(iadep)%salt(isalt)%roadmo(ist), rdapp_salt(iadep)%salt(isalt)%roadday, rdapp_salt(iadep)%salt(isalt)%road` |
| [sym:output_landscape_module] | `iwst` | `iwst` |
| [sym:salt_module] | `hsaltb_d` | `hsaltb_d(j)%salt(isalt)%road` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_salts, cs_soil(j)%ly(1)%salt(isalt)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | When `cs_db%num_salts > 0` and `ist` is a valid atmospheric-deposition step, the routine sets `iwst = ob(iob)%wst` before reading road-salt inputs. | `iwst` becomes the weather-station index for the current HRU, allowing the routine to find the deposition dataset linked to that HRU’s object connectivity. |
| `hsaltb_d(j)%salt(isalt)%road` | When monthly, yearly, or annual-average road-salt input is available for a salt ion, the routine assigns `hsaltb_d(j)%salt(isalt)%road` from the corresponding `rdapp_salt` table entry. | The salt-balance bookkeeping records the road-salt mass applied for that ion and HRU during the current time step. |
| `cs_soil(j)%ly(1)%salt(isalt)` | Whenever a road-salt flux is computed for a salt ion, the routine adds that flux to `cs_soil(j)%ly(1)%salt(isalt)`. | The first soil layer receives the applied salt mass so later soil/salt calculations can use the updated constituent pool. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `salt_roadsalt`. `df07e3f` introduced the routine and its road-salt-to-soil logic. `35b029c` only removed a trailing blank line, with no behavioral change. `2ee1889` simplified the `use hru_module` list by dropping `timest` and removed the unused `dum` variable. `39fabde` initialized the local scalars `iadep`, `j`, `iob`, `ist`, `isalt`, and `const`, and also made the same whitespace-only indentation cleanup in the loop endings.

- Added the full `salt_roadsalt` subroutine with HRU-to-weather-station lookup, timestep-gated monthly/yearly/annual road-salt loading, and updates to salt-balance and soil constituent state.
- Made the local counters and constant explicitly initialized, reducing uninitialized-variable risk without changing the algorithm.
- Removed an unused `timest` import from `hru_module` and an unused `dum` declaration, tightening the interface with no effect on calculations.
- Applied nonfunctional whitespace cleanup at the file end.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_roadsalt' has no extracted documentation comment.
- algorithm_steps revised: merged the initial variable assignments into a single step and reduced the list to seven behavior steps while preserving the source line coverage.
- `output_landscape_module` was imported, but no extracted source lines showed a specific symbol from that module being used; the overlay keeps the module entry minimal rather than guessing the missing usage.
