---
kind: procedure
symbol: cs_fert_wet
title: cs_fert_wet
status: filled
source_hash: 4f2e4617e6dcf99c
version_label: SWAT+ 62.0.0
args:
  jj: HRU index. It selects which wetland cell receives the constituent fertilizer mass update
    through `wet_water(jj)` and `wetcs_d(jj)`.
  ifrt: Fertilizer database index. If it is positive, the routine uses `fert_cs(ifrt)` to
    look up the constituent fractions; if it is not positive, no fertilizer mass is added.
  frt_kg: Applied fertilizer rate in kg/ha. The routine multiplies this rate by constituent
    fractions and HRU area to compute how much seo4, seo3, and boron mass is added.
uses:
  mgt_operations_module: This module controls whether constituent simulation is active at
    all. The routine exits unless `cs_db%num_cs > 0`, so the whole update depends on the constituent
    count stored here.
  cs_module: This module provides the constituent fertilizer database entry for the selected
    fertilizer type. The routine reads `fert_cs(ifrt)%seo4`, `%seo3`, and `%boron` to turn
    a fertilizer application rate into constituent-specific mass additions.
  constituent_mass_module: This module holds the wetland constituent storage arrays that are
    updated by this routine. `wet_water(jj)%cs(1:3)` receives the added constituent mass so
    downstream wetland accounting reflects the fertilizer application.
  fertilizer_data_module: This module supplies the fertilizer-to-constituent conversion factors
    used in the mass calculations. Without these per-fertilizer fractions, the routine cannot
    determine how much of each constituent is applied.
  hru_module: This module supplies the HRU area used to convert an application rate from kg/ha
    into total mass for the selected wetland HRU. The area scaling is required for both the
    wetland storage update and the balance terms.
  res_cs_module: This module holds the wetland constituent fertilizer balance outputs. The
    routine writes the fertilizer contribution into `wetcs_d(jj)%cs(1:3)%fert` so wetland
    balance reporting can track the applied mass.
---

<!-- facts:header -->

Adds constituent fertilizer mass to a wetland HRU. It updates both the wetland constituent storage and the wetland constituent fertilizer balance for sulfur and boron species.

## Bottom Line

This subroutine applies a wetland fertilizer operation for chemical constituents. When constituents are enabled and a valid fertilizer ID is supplied, it takes the applied fertilizer rate in kg/ha, multiplies it by the fertilizer database fractions for seo4, seo3, and boron, and scales by HRU area to get added mass.

The routine then adds those masses to the wetland constituent storage array and mirrors the same amounts into the wetland constituent balance outputs under the fertilizer term. That makes the fertilizer application visible to later wetland constituent accounting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during management scheduling when a fertilizer operation is processed for a wetland HRU. `mgt_sched` sets the fertilizer ID in `ifrt` and the application rate in `frt_kg` from the management operation, then calls `cs_fert_wet` to add the constituent portion of that wetland fertilizer application. Its results feed later wetland constituent mass accounting and the wetland balance outputs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check constituent simulation | The routine first tests `cs_db%num_cs > 0` so it only applies constituent fertilizer updates when the model is simulating constituent transport and storage. |
| 2. Check fertilizer ID | If constituents are active, it tests `ifrt > 0` to ensure a valid fertilizer database record is available before using its constituent fractions. |
| 3. Add seo4 mass to wetland storage | It adds `frt_kg * fert_cs(ifrt)%seo4 * hru(jj)%area_ha` to `wet_water(jj)%cs(1)`, increasing the wetland's stored seo4 constituent mass. |
| 4. Add seo3 mass to wetland storage | It adds `frt_kg * fert_cs(ifrt)%seo3 * hru(jj)%area_ha` to `wet_water(jj)%cs(2)`, increasing the wetland's stored seo3 constituent mass. |
| 5. Add boron mass to wetland storage | It adds `frt_kg * fert_cs(ifrt)%boron * hru(jj)%area_ha` to `wet_water(jj)%cs(3)`, increasing the wetland's stored boron constituent mass. |
| 6. Record seo4 fertilizer balance | It writes the same seo4 mass into `wetcs_d(jj)%cs(1)%fert` so the wetland constituent balance records fertilizer input separately from other sources. |
| 7. Record seo3 fertilizer balance | It writes the seo3 application mass into `wetcs_d(jj)%cs(2)%fert` for wetland balance reporting. |
| 8. Record boron fertilizer balance | It writes the boron application mass into `wetcs_d(jj)%cs(3)%fert` so the fertilizer contribution to boron is available in the balance output. |
| 9. Return | The subroutine returns to the caller after updating the wetland storage and balance arrays, or after skipping them if the guard conditions failed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `cs_db` | `cs_db%num_cs` |
| [sym:cs_module] | `fert_cs` | `fert_cs(ifrt)%seo4, fert_cs(ifrt)%seo3, fert_cs(ifrt)%boron` |
| [sym:constituent_mass_module] | `cs_db, wet_water` | `cs_db%num_cs, wet_water(jj)%cs(1), wet_water(jj)%cs(2), wet_water(jj)%cs(3)` |
| [sym:fertilizer_data_module] | `fert_cs` | `fert_cs(ifrt)%seo4, fert_cs(ifrt)%seo3, fert_cs(ifrt)%boron` |
| [sym:hru_module] | `hru` | `hru(jj)%area_ha` |
| [sym:res_cs_module] | `wetcs_d` | `wetcs_d(jj)%cs(1)%fert, wetcs_d(jj)%cs(2)%fert, wetcs_d(jj)%cs(3)%fert` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet_water(jj)%cs(1)` | When `cs_db%num_cs > 0` and `ifrt > 0`. | This wetland constituent storage increases by the seo4 mass contributed by the fertilizer application, converted from kg/ha to total kg using HRU area. |
| `wet_water(jj)%cs(2)` | When `cs_db%num_cs > 0` and `ifrt > 0`. | This wetland constituent storage increases by the seo3 mass contributed by the fertilizer application, converted from kg/ha to total kg using HRU area. |
| `wet_water(jj)%cs(3)` | When `cs_db%num_cs > 0` and `ifrt > 0`. | This wetland constituent storage increases by the boron mass contributed by the fertilizer application, converted from kg/ha to total kg using HRU area. |
| `wetcs_d(jj)%cs(1)%fert` | When `cs_db%num_cs > 0` and `ifrt > 0`. | This wetland constituent balance entry records the seo4 fertilizer mass added to the HRU so later mass-balance output can attribute that amount to fertilizer. |
| `wetcs_d(jj)%cs(2)%fert` | When `cs_db%num_cs > 0` and `ifrt > 0`. | This wetland constituent balance entry records the seo3 fertilizer mass added to the HRU so later mass-balance output can attribute that amount to fertilizer. |
| `wetcs_d(jj)%cs(3)%fert` | When `cs_db%num_cs > 0` and `ifrt > 0`. | This wetland constituent balance entry records the boron fertilizer mass added to the HRU so later mass-balance output can attribute that amount to fertilizer. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The procedure was introduced in df07e3f with the constituent fertilizer update logic for wetland storage and balance arrays. c7c8e22 preserved that implementation when the source was synced from Bitbucket. 39fabde initialized the local variable `ics` to zero, and 2ee1889 later removed that unused local variable without changing the wetland fertilizer calculations.

- df07e3f added the full `cs_fert_wet` procedure, including the `cs_db%num_cs` and `ifrt` guards and the three wetland constituent/balance updates using `fert_cs` and `hru(jj)%area_ha`.
- 39fabde changed only the local declaration of `ics` to initialize it to zero; the fertilizer application behavior remained the same.
- 2ee1889 removed the unused `ics` declaration; the wetland constituent update logic was unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_fert_wet' has no extracted documentation comment.
