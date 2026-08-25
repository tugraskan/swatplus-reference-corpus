---
kind: procedure
symbol: swr_latsed
title: swr_latsed
status: filled
source_hash: 468a2e22f1a4443b
version_label: SWAT+ 62.0.0
locals:
  j: Loop-free index variable for the active HRU. It is initialized to 0, then assigned `ihru`
    so the routine updates the yield arrays for the current hydrologic response unit.
uses:
  hru_module: This module supplies the current HRU index, HRU geometry, lateral-flow state,
    and the sediment/nutrient yield arrays that `swr_latsed` increments. `hru(j)%area_ha`
    and `hru(j)%hyd%lat_sed` define the sediment load scale, while `latq`, `qtile`, and the
    various yield arrays provide the flow inputs and accumulation targets for the active HRU.
  soil_module: This module provides the soil detachment fractions used to split the lateral
    sediment load into texture classes. `soil(j)%det_san`, `det_sil`, `det_cla`, `det_sag`,
    and `det_lag` control how much of the sediment yield is attributed to each particle-size
    class for the current HRU.
---

<!-- facts:header -->

Adds lateral-flow sediment and associated nutrient loads to the current HRU's running yield totals. It also floors any negative yield values back to zero before returning.

## Bottom Line

swr_latsed updates the current HRU's sediment-yield bookkeeping from lateral flow and tile flow. It uses HRU state for lateral sediment concentration, HRU area, lateral flow, and lateral nutrient concentrations, then accumulates those loads into the yield arrays that other parts of the HRU workflow read later.

It also apportions the lateral sediment load into sand, silt, clay, small aggregate, and large aggregate yields using soil detachment fractions from `soil(j)`. After all additions, it clamps any negative yield values to zero so downstream sediment and nutrient routing does not carry invalid negative loads.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `hru_control` immediately after HRU daily or subdaily setup has populated the current HRU state, including `ihru`, `hru(j)%hyd%lat_sed`, `latq`, and `qtile`. Its results feed the later HRU storage and routing steps, especially `stor_surfstor` and the rest of the pollutant transport sequence, because those later routines use the updated sediment and nutrient yield arrays.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set current HRU index | Initializes the local HRU index `j` and assigns it from `ihru` so all later updates target the currently active hydrologic response unit. |
| 2. add sediment from lateral and tile flow | Adds lateral/tile sediment load to `sedyld(j)` using HRU sediment concentration, HRU area, and the sum of lateral flow and tile flow. |
| 3. update sand sediment yield | Adds the lateral-flow sediment contribution to the sand-size yield pool using the soil sand detachment fraction. |
| 4. update silt sediment yield | Adds the lateral-flow sediment contribution to the silt-size yield pool using the soil silt detachment fraction. |
| 5. update clay sediment yield | Adds the lateral-flow sediment contribution to the clay-size yield pool using the soil clay detachment fraction. |
| 6. update small aggregate sediment yield | Adds the lateral-flow sediment contribution to the small-aggregate yield pool using the soil small-aggregate detachment fraction. |
| 7. update large aggregate sediment yield | Adds the lateral-flow sediment contribution to the large-aggregate yield pool using the soil large-aggregate detachment fraction. |
| 8. add lateral organic nitrogen | Adds the organic nitrogen load carried by lateral flow to `sedorgn(j)` using `hru(j)%hyd%lat_orgn`. |
| 9. add lateral organic phosphorus | Adds the organic phosphorus load carried by lateral flow to `sedorgp(j)` using `hru(j)%hyd%lat_orgp`. |
| 10. floor negative sediment yield | If total sediment yield became negative, resets `sedyld(j)` to zero to keep the accumulated load nonnegative. |
| 11. floor negative sand yield | If sand yield became negative, resets `sanyld(j)` to zero. |
| 12. floor negative silt, clay, aggregate, and nutrient yields | Checks each remaining yield array and resets any negative value to zero for silt, clay, small aggregate, large aggregate, organic nitrogen, and organic phosphorus. |
| 13. return | Returns to the caller after the current HRU's sediment and nutrient yield bookkeeping has been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `sedyld, hru, sanyld, silyld, clayld, sagyld, lagyld, sedorgn, sedorgp, latq, ihru, qtile` | `hru(j)%area_ha, hru(j)%hyd%lat_sed` |
| [sym:soil_module] | `soil` | `soil(j)%det_san, soil(j)%det_sil, soil(j)%det_cla, soil(j)%det_sag, soil(j)%det_lag` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sedyld(j)` | When the current HRU has lateral and tile flow and a nonzero sediment concentration, the routine increments `sedyld(j)`; if the result is negative afterward, it is forced back to zero. | `sedyld(j)` stores the current HRU's total sediment yield contribution from lateral/tile transport. It is accumulated here so later HRU routing and storage routines can use a nonnegative sediment load. |
| `sanyld(j)` | When lateral flow carries sediment through the active HRU, `sanyld(j)` is incremented by the sand-class share; if the update leaves a negative value, it is reset to zero. | `sanyld(j)` holds the sand-size portion of the HRU's sediment yield after lateral-flow accounting, which downstream sediment partitioning can use. |
| `silyld(j)` | When lateral flow carries sediment through the active HRU, `silyld(j)` is incremented by the silt-class share; if negative, it is clamped to zero. | `silyld(j)` tracks the silt-size sediment yield component for the current HRU after lateral-flow contribution is added. |
| `clayld(j)` | When lateral flow carries sediment through the active HRU, `clayld(j)` is incremented by the clay-class share; if negative, it is clamped to zero. | `clayld(j)` tracks the clay-size sediment yield component for the current HRU after lateral-flow contribution is added. |
| `sagyld(j)` | When lateral flow carries sediment through the active HRU, `sagyld(j)` is incremented by the small-aggregate share; if negative, it is clamped to zero. | `sagyld(j)` stores the small-aggregate sediment yield component for the current HRU. |
| `lagyld(j)` | When lateral flow carries sediment through the active HRU, `lagyld(j)` is incremented by the large-aggregate share; if negative, it is clamped to zero. | `lagyld(j)` stores the large-aggregate sediment yield component for the current HRU. |
| `sedorgn(j)` | When lateral flow transports organic nitrogen, `sedorgn(j)` is incremented; if the updated value is negative, it is reset to zero. | `sedorgn(j)` records the lateral-flow organic nitrogen load for the active HRU so later pollutant routing can use a nonnegative mass value. |
| `sedorgp(j)` | When lateral flow transports organic phosphorus, `sedorgp(j)` is incremented; if the updated value is negative, it is reset to zero. | `sedorgp(j)` records the lateral-flow organic phosphorus load for the active HRU so later pollutant routing can use a nonnegative mass value. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 4:1.5.1 | sed_lat = (Q_lat+Q_gw)*area*conc_sed/1000 | $sed_{lat}=\frac{(Q_{lat}+Q_{gw})*area_{hru}*conc_{sed}}{1000}$ | Verified against SWAT+ 62.0.0 (swr_latsed.f90:42). sedyld += (latq+qtile)·lat_sed/100000.` — lateral+tile sediment |

## Lineage

Resolved lineage evidence shows two changes: the procedure was introduced in commit df07e3f, and commit 39fabde initialized local variable `j` to 0. The later commit did not change the algorithm, only the variable declaration.

- df07e3f added the full `swr_latsed` subroutine with its lateral-flow sediment and nutrient accumulation logic, including the negative-value clamps.
- 39fabde changed `integer :: j` to `integer :: j = 0`, adding an explicit initial value for the local HRU index without altering the calculations.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'swr_latsed' has no extracted documentation comment.
