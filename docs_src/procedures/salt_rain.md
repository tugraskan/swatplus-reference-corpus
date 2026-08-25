---
kind: procedure
symbol: salt_rain
title: salt_rain
status: filled
source_hash: d7243ae179b52852
version_label: SWAT+ 62.0.0
locals:
  iadep: Atmospheric deposition data-set index for the current HRU’s weather station; it selects
    which `atmodep_salt` record provides salt deposition inputs.
  j: Current HRU index, copied from `ihru`, used to access the active HRU, its salt balances,
    and its soil constituent mass.
  iob: Object-connectivity index for the current HRU; it is used to find the linked weather
    station through `ob(iob)%wst`.
  ist: Atmospheric-deposition time-step index from `atmodep_cont%ts`; it selects the current
    monthly, yearly, or annual-average deposition record.
  isalt: Loop counter over salt ions, from 1 to `cs_db%num_salts`.
  const: Month-length conversion factor used in the monthly branch to turn monthly dry deposition
    totals into a per-day or per-step mass rate via the number of days in the month.
uses:
  basin_module: It gates the entire routine and sets the salt-ion loop bound, so no atmospheric
    salt is processed unless salts are configured in the constituent database.
  organic_mineral_mass_module: It is the soil-side storage that receives the rainfall and
    dry-deposition salt masses, so this module is where the added salt is accumulated for
    the current HRU.
  hydrograph_module: It provides the HRU-to-weather-station linkage used to find the correct
    atmospheric-deposition dataset for the current HRU, via `ob(iob)%wst`.
  hru_module: It identifies the active HRU (`ihru`) and provides the HRU object used to get
    the connectivity pointer `hru(j)%obj_no` before looking up deposition inputs.
  climate_module: It supplies the deposition-control settings, the weather station code, the
    rainfall depth, and the salt deposition arrays used to compute rainfall and dry deposition
    for monthly, yearly, and annual-average cases.
  output_landscape_module: No candidate state from `output_landscape_module` was resolved
    in the extracted source, so it does not contribute a visible symbol to the documented
    computation here.
  salt_module: It stores the per-HRU salt balance terms that this routine updates, specifically
    the rainfall and dry-deposition additions for each salt ion.
  constituent_mass_module: It defines how many salt ions are simulated and provides the soil
    constituent mass structure that receives the added salt in layer 1.
---

<!-- facts:header -->

Adds atmospheric salt deposition to the top soil layer for the active HRU. It handles rainfall-derived salt and dry deposition for monthly, yearly, or annual-average salt deposition inputs.

## Bottom Line

`salt_rain` is the atmospheric-deposition part of the salt accounting for the current HRU. It looks up the HRU’s weather station and atmospheric-deposition source, then converts salt concentration and dry-deposition data into salt mass added to the top soil layer.

The routine only runs when salts are being simulated and when the atmospheric-deposition index is valid. Depending on `atmodep_cont%timestep`, it uses monthly, yearly, or annual-average deposition arrays, stores the computed rainfall and dry-deposition masses in `hsaltb_d`, and adds those masses into `cs_soil(j)%ly(1)%salt(isalt)`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `hru_control` after salt simulation has been enabled for the current HRU (`cs_db%num_salts > 0` and `salt_atmo == 'y'`). `hru_control` prepares the HRU context and then calls `salt_rain` before road-salt application and salt leaching, so the atmospheric salt added here becomes part of the soil salt pool that later salt routines act on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check salt simulation | Skip the routine unless salts are enabled in `cs_db%num_salts`; this prevents any atmospheric salt bookkeeping when no salt ions are being simulated. |
| 2. resolve HRU and climate links | Use the current HRU index to find the HRU object, its connected weather station, the atmospheric-deposition dataset, and the deposition time-step index. |
| 3. limit to valid deposition records | Proceed only when the deposition time-step index is inside the valid range of atmospheric-deposition records. |
| 4. monthly deposition branch | When the deposition timestep is monthly, compute a month-length factor, loop over all salt ions, calculate rainfall-derived salt and dry deposition from the monthly arrays, and add both to the top soil layer. |
| 5. yearly deposition branch | When the deposition timestep is yearly, loop over all salt ions, calculate rainfall-derived salt and dry deposition from the yearly arrays, and add both to the top soil layer. |
| 6. annual-average deposition branch | When the deposition timestep is annual-average, loop over all salt ions, calculate rainfall-derived salt and dry deposition from the annual-average values, and add both to the top soil layer. |
| 7. return | Finish after the soil and salt-balance updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `cs_db` | `cs_db%num_salts` |
| [sym:organic_mineral_mass_module] | `cs_soil` | `cs_soil(j)%ly(1)%salt(isalt)` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:hru_module] | `hru, ihru` | `hru(j)%obj_no` |
| [sym:climate_module] | `wst, atmodep_cont, atmodep_salt, w` | `wst(iwst)%wco%atmodep, atmodep_cont%ts, atmodep_cont%num, atmodep_cont%timestep, atmodep_salt(iadep)%salt(isalt)%rfmo(ist), w%precip, atmodep_salt(iadep)%salt(isalt)%drymo(ist), atmodep_salt(iadep)%salt(isalt)%rfyr(ist), atmodep_salt(iadep)%salt(isalt)%dryyr(ist), atmodep_salt(iadep)%salt(isalt)%rf, atmodep_salt(iadep)%salt(isalt)%dry` |
| [sym:output_landscape_module] | `none resolved` |  |
| [sym:salt_module] | `hsaltb_d` | `hsaltb_d(j)%salt(isalt)%rain, hsaltb_d(j)%salt(isalt)%dryd` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_salts, cs_soil(j)%ly(1)%salt(isalt)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | When `cs_db%num_salts > 0`, the routine resolves `iwst` from `ob(iob)%wst` for the current HRU. | This selects the weather station linked to the HRU so the routine can fetch the correct atmospheric-deposition source. `iwst` is the bridge from HRU connectivity to climate/deposition data. |
| `hsaltb_d(j)%salt(isalt)%rain` | When `cs_db%num_salts > 0`, `ist` is valid, and `atmodep_cont%timestep` is one of `mo`, `yr`, or `aa`, the routine assigns rainfall salt mass to `hsaltb_d(j)%salt(isalt)%rain`. | This records the rainfall-derived salt load for each ion and each active HRU. It is the bookkeeping value used before the same mass is added into the soil profile. |
| `hsaltb_d(j)%salt(isalt)%dryd` | Under the same timestep-specific branches, the routine assigns dry-deposition mass to `hsaltb_d(j)%salt(isalt)%dryd`. | This stores the dry atmospheric deposition contribution for each salt ion so it can be accumulated into the HRU’s top soil layer alongside rainfall deposition. |
| `cs_soil(j)%ly(1)%salt(isalt)` | Within the monthly, yearly, or annual-average deposition branches, after `hsaltb_d(j)%salt(isalt)%rain` and `hsaltb_d(j)%salt(isalt)%dryd` are computed. | The top soil layer salt mass is increased by the combined rainfall and dry deposition load for each salt ion, so the atmospheric inputs become part of the HRU soil salt pool. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved for `salt_rain`. The initial addition in `df07e3f` created the routine and its atmospheric-deposition logic. `35b029c` only made whitespace cleanup near the end of the file. `2ee1889` removed `timest` from the `hru_module` use list. `39fabde` initialized the local counters and `const` to zero and also fixed indentation on the `enddo` blocks.

- df07e3f added the full `salt_rain` routine: HRU-to-weather-station lookup, timestep selection, monthly/yearly/annual-average salt deposition calculations, and top-layer soil updates.
- 35b029c made a non-functional formatting cleanup at the end of the file.
- 2ee1889 removed the unused `timest` import from `hru_module`.
- 39fabde initialized `iadep`, `j`, `iob`, `ist`, `isalt`, and `const` to zero and adjusted indentation in the loop endings.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_rain' has no extracted documentation comment.
