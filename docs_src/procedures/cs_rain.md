---
kind: procedure
symbol: cs_rain
title: cs_rain
status: filled
source_hash: d083ae306f4461e4
version_label: SWAT+ 62.0.0
locals:
  iadep: Index of the atmospheric deposition dataset selected for the current HRU through
    the HRU's connected weather station.
  j: HRU index used to point into the HRU array and related per-HRU constituent balance and
    soil-mass arrays.
  iob: Object index for the current HRU, used to reach the hydrologic object connectivity
    record that holds the weather-station link.
  ist: Time-step selector within the atmospheric deposition control record; it chooses which
    monthly, yearly, or annual-average deposition entry to apply.
  ics: Loop counter over simulated constituents; it identifies the constituent whose rainfall
    and dry-deposition loads are being updated.
  const: Conversion constant for turning a monthly dry-deposition total into a per-day rate
    by dividing by the number of days in the month.
uses:
  basin_module: The routine runs inside the basin-wide simulation state, so the basin module
    matters as the broader execution context that owns shared model setup even though no specific
    basin_module member was directly referenced in the extracted lines.
  organic_mineral_mass_module: This module matters because cs_rain contributes to soil mass
    accounting alongside other landscape mass routines; even though no explicit symbol from
    the module appears in the extracted lines, it is part of the surrounding mass-balance
    infrastructure.
  hydrograph_module: The routine uses ob(iob)%wst to move from the current HRU object to its
    weather station, and that station supplies the atmospheric deposition dataset index needed
    to pick the right constituent deposition series.
  hru_module: The current HRU record provides obj_no, which lets the routine map the active
    HRU index j to the correct landscape object and then to its linked weather station.
  climate_module: This module supplies the atmospheric deposition control and deposition data.
    cs_rain reads the control timestep and valid range, then fetches rainfall and dry-deposition
    values for each constituent from the weather-station-linked deposition arrays.
  output_landscape_module: This module matters because cs_rain contributes to landscape-scale
    constituent accounting that is typically reported or aggregated with other output-landscape
    state, even though no direct symbol was extracted here.
  cs_module: The cs balance arrays in hcsb_d record the rainfall and dry-deposition additions
    for the current HRU and constituent, so this module holds the bookkeeping targets that
    cs_rain updates.
  constituent_mass_module: The soil constituent arrays in cs_soil store the actual mass in
    the top soil layer for each HRU and constituent; cs_rain adds the computed atmospheric
    loads there so later transport and balance routines see the updated soil pool.
---

<!-- facts:header -->

Adds atmospheric deposition of simulated constituents to each HRU soil surface layer. It converts rainfall concentration and dry-deposition inputs into daily, monthly, yearly, or annual-average masses and accumulates them in the soil and daily balance arrays.

## Bottom Line

cs_rain updates constituent mass loading from atmospheric deposition for the current HRU. For each simulated constituent, it computes rainfall-derived mass and dry-deposition mass using the active atmospheric deposition timestep and adds both to the top soil layer.

The routine is only active when constituents are being simulated and the current deposition index is valid. Its results feed the daily constituent balance bookkeeping in hcsb_d and the soil constituent storage in cs_soil, which later transport and accounting routines use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

cs_rain runs during HRU control after the HRU index and weather-station links have already been established and when atmospheric deposition for constituents is enabled. hru_control prepares that context by checking cs_db%num_cs and cs_atmo before calling this routine, and later constituent leaching and transport routines depend on the soil and balance values it writes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check constituent mode | Exit immediately unless at least one constituent is being simulated. This prevents any atmospheric deposition bookkeeping when cs_db%num_cs is zero. |
| 2. resolve current HRU links | Use the current HRU index to find the object number, weather-station index, atmospheric deposition file index, and deposition time-step selector for this HRU. |
| 3. apply only valid deposition entries | Continue only if the selected deposition time-step is within the valid range for the atmospheric deposition control record. |
| 4. monthly deposition branch | When the control timestep is monthly, compute the month length, loop over every simulated constituent, calculate rainfall and dry deposition for that month, and add both masses to the top soil layer. |
| 5. yearly deposition branch | When the control timestep is yearly, loop over every simulated constituent, convert yearly rainfall and dry deposition into daily rates, and add both masses to the top soil layer. |
| 6. annual-average deposition branch | When the control timestep is annual-average, loop over every simulated constituent, convert the annual-average rainfall and dry deposition inputs into daily masses, and add both to the top soil layer. |
| 7. return | Finish after updating the per-HRU constituent balance and soil storage arrays. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state used indirectly through basin-wide execution context` | `No specific basin_module symbol was resolved in the extracted source context.` |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module state used indirectly through landscape mass-accounting context` | `No specific organic_mineral_mass_module symbol was resolved in the extracted source context.` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:hru_module] | `hru, ihru` | `hru(j)%obj_no` |
| [sym:climate_module] | `wst, atmodep_cont, atmodep_cs, w` | `wst(iwst)%wco%atmodep, atmodep_cont%ts, atmodep_cont%num, atmodep_cont%timestep, atmodep_cs(iadep)%cs(ics)%rfmo(ist), w%precip, atmodep_cs(iadep)%cs(ics)%drymo(ist), atmodep_cs(iadep)%cs(ics)%rfyr(ist), atmodep_cs(iadep)%cs(ics)%dryyr(ist), atmodep_cs(iadep)%cs(ics)%rf, atmodep_cs(iadep)%cs(ics)%dry` |
| [sym:output_landscape_module] | `output_landscape_module state used indirectly through landscape output bookkeeping` | `No specific output_landscape_module symbol was resolved in the extracted source context.` |
| [sym:cs_module] | `hcsb_d` | `hcsb_d(j)%cs(ics)%rain, hcsb_d(j)%cs(ics)%dryd` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_cs, cs_soil(j)%ly(1)%cs(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | When the current HRU has a valid linked weather station and atmospheric deposition is enabled for constituents. | iwst is set to the weather-station index for the active HRU so the routine can read the correct atmospheric deposition dataset. |
| `hcsb_d(j)%cs(ics)%rain` | Inside the monthly, yearly, or annual-average branch for every simulated constituent. | The rainfall-derived constituent mass is stored in the daily balance array for the current HRU and constituent, reflecting the amount added from wet atmospheric deposition. |
| `hcsb_d(j)%cs(ics)%dryd` | Inside the monthly, yearly, or annual-average branch for every simulated constituent. | The dry-deposition mass is stored in the daily balance array for the current HRU and constituent, reflecting the amount added from dry atmospheric deposition. |
| `cs_soil(j)%ly(1)%cs(ics)` | Inside the monthly, yearly, or annual-average branch for every simulated constituent. | The top soil-layer constituent mass is increased by the sum of rainfall and dry deposition so later soil and transport routines work from the updated soil pool. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed cs_rain. df07e3f added the new subroutine with atmospheric-deposition deposition logic for monthly, yearly, and annual-average timesteps. 94b6dec introduced the same routine into the source tree as part of the imported upstream code. 39fabde initialized the local loop and helper variables to zero and preserved the deposition calculations; 2ee1889 later removed the unused timest import and trimmed a trailing blank line without changing the algorithm.

- df07e3f: created cs_rain with HRU-to-weather-station lookup, timestep gating, and deposition-to-soil accumulation for monthly, yearly, and annual-average constituent inputs.
- 39fabde: initialized iadep, j, iob, ist, ics, and const to zero; deposition formulas and state updates stayed the same.
- 2ee1889: removed the unused timest symbol from the hru_module import and made no behavioral change.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_rain' has no extracted documentation comment.
- algorithm_steps revised: collapsed the monthly/yearly/annual-average internals into clearer branch steps while preserving source-line coverage.
- Source context shows no resolved direct calls inside cs_rain.
