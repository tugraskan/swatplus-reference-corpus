---
kind: procedure
symbol: pest_apply
title: pest_apply
status: filled
source_hash: e0b090ded89c6e89
version_label: SWAT+ 62.0.0
args:
  jj: HRU index copied into local `j`; selects which plant community, soil profile, and pesticide-balance
    records receive the application.
  ipest: Sequential pesticide identifier used to choose the pesticide slot within `cs_pl`,
    `cs_soil`, and `hpestb_d` for this HRU.
  pest_kg: Pesticide mass to apply, in kg/ha, after any application-efficiency adjustment
    performed by the caller.
  pestop: Chemical-application database index used to retrieve the surface-fraction split
    in `chemapp_db(pestop)%surf_frac`.
locals:
  j: '`j` is the working HRU index used after copying `jj`; it indexes all HRU-specific plant,
    soil, and balance state updates.'
  ipl: '`ipl` is the plant-loop index used to distribute intercepted pesticide across the
    plants in the HRU community.'
  gc: '`gc` holds the computed fraction of applied pesticide intercepted by foliage from the
    current LAI-based ground-cover estimate.'
  surf_frac: '`surf_frac` holds the fraction of the soil-applied pesticide routed to the upper
    soil layer, read from `chemapp_db(pestop)%surf_frac`.'
  pl_frac: '`pl_frac` is the per-plant share of intercepted pesticide, computed as each plant''s
    LAI divided by the community LAI sum.'
uses:
  mgt_operations_module: '`mgt_operations_module` provides the chemical application database
    entry that controls how much of the non-foliage pesticide goes to the upper soil layer
    versus the second layer.'
  basin_module: '`basin_module` is listed as a dependency in the source, but no candidate
    outside reference from this procedure was resolved to it. The plant-community values that
    actually drive the calculation come from `plant_module`.'
  soil_module: '`soil_module` is imported by the routine, but the resolved state updates for
    pesticide mass are stored through the constituent-mass soil structure. These soil-layer
    pesticide fields are where the routine deposits the non-foliage share.'
  plant_module: '`plant_module` matters because `pcom(j)%lai_sum` determines canopy interception,
    `pcom(j)%npl` sets the number of plants to loop over, and `pcom(j)%plg(ipl)%lai` provides
    the LAI weights used to split intercepted pesticide among plants.'
  output_ls_pesticide_module: '`output_ls_pesticide_module` matters because this routine updates
    `hpestb_d(j)%pest(ipest)%apply_f` and `%apply_s`, which capture the foliage and soil application
    totals for later pesticide balance output.'
  constituent_mass_module: '`constituent_mass_module` matters because it holds the HRU pesticide
    mass arrays on plants and in soil layers. This routine writes the applied pesticide into
    `cs_pl` and `cs_soil` so later mass-balance and process routines can see the updated state.'
---

<!-- facts:header -->

Applies an HRU pesticide dose and splits it between plant foliage and soil layers based on canopy cover and the selected chemical application operation.

## Bottom Line

pest_apply takes a pesticide amount for one HRU and partitions it into foliage and soil deposits. It uses the current plant community leaf area to estimate canopy interception, then sends the intercepted share to each plant in proportion to its LAI and the remainder to soil layers 1 and 2 using the chemical application's surface fraction.

The routine also records the applied foliage and soil totals in the pesticide balance output structure. Those balance fields support later pesticide accounting and output reporting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a management action or scheduled management operation applies pesticide to an HRU. The caller prepares the HRU index, pesticide type, application-operation index, and an already efficiency-adjusted applied mass before calling `pest_apply`. Its results feed later pesticide accounting through `hpestb_d`, and they directly alter plant and soil pesticide stores used by subsequent model processes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set HRU index | Copies the incoming HRU identifier `jj` into local `j` so the rest of the routine can index HRU-specific state arrays. |
| 2. compute canopy cover | Computes `gc` from total LAI using the erfc-based canopy cover relationship, then truncates negative values to zero. |
| 3. check plant cover | Only distributes pesticide across plants when the HRU has meaningful total LAI; otherwise the canopy-routing loop is skipped. |
| 4. loop over plants | Walks through each plant in the community, computes that plant's LAI fraction, and adds the intercepted share of pesticide to the plant-on pesticide mass. |
| 5. read soil split fraction | Loads the surface-soil fraction for this application option from the chemical application database. |
| 6. apply to upper soil | Adds the non-intercepted pesticide share multiplied by the surface fraction to soil layer 1. |
| 7. apply to lower soil | Adds the remaining non-intercepted pesticide share to soil layer 2. |
| 8. record foliage balance | Stores the total pesticide intercepted by foliage in the daily pesticide-balance field `apply_f`. |
| 9. record soil balance | Stores the total pesticide reaching the soil in the daily pesticide-balance field `apply_s`. |
| 10. return | Exits after updating the HRU pesticide stores and balance totals. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `chemapp_db` | `chemapp_db(pestop)%surf_frac` |
| [sym:basin_module] | `pcom` | `pcom(j)%lai_sum, pcom(j)%npl, pcom(j)%plg(ipl)%lai` |
| [sym:soil_module] | `cs_soil` | `cs_soil(j)%ly(1)%pest(ipest), cs_soil(j)%ly(2)%pest(ipest)` |
| [sym:plant_module] | `pcom` | `pcom(j)%lai_sum, pcom(j)%npl, pcom(j)%plg(ipl)%lai` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(ipest)%apply_f, hpestb_d(j)%pest(ipest)%apply_s` |
| [sym:constituent_mass_module] | `cs_pl, cs_soil` | `cs_pl(j)%pl_on(ipl)%pest(ipest), cs_soil(j)%ly(1)%pest(ipest), cs_soil(j)%ly(2)%pest(ipest)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_pl(j)%pl_on(ipl)%pest(ipest)` | When `pcom(j)%lai_sum > 1.e-6`, inside the loop over `ipl = 1, pcom(j)%npl`. | The pesticide mass on each plant's foliage increases by the intercepted fraction assigned to that plant: `gc * pl_frac * pest_kg`. This only happens when the HRU has enough LAI to distribute a canopy-intercepted application among individual plants. |
| `cs_soil(j)%ly(1)%pest(ipest)` | Always, after `surf_frac = chemapp_db(pestop)%surf_frac` is read. | The upper soil layer receives the surface portion of the non-intercepted pesticide: `(1. - gc) * surf_frac * pest_kg` is added to layer 1 so later soil processes can act on the applied chemical. |
| `cs_soil(j)%ly(2)%pest(ipest)` | Always, after `surf_frac = chemapp_db(pestop)%surf_frac` is read. | The second soil layer receives the remainder of the non-intercepted pesticide: `(1. - gc) * (1. - surf_frac) * pest_kg` is added to layer 2. |
| `hpestb_d(j)%pest(ipest)%apply_f` | Always, after canopy cover `gc` has been computed. | `apply_f` stores the total amount intercepted by foliage, `gc * pest_kg`, for pesticide balance output and later accounting. |
| `hpestb_d(j)%pest(ipest)%apply_s` | Always, after canopy cover `gc` has been computed. | `apply_s` stores the total amount that reaches the soil surface system, `(1. - gc) * pest_kg`, for pesticide balance output and later accounting. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 6:1.10.1 | Effective pesticide applied after efficiency | $pest'=ap_{ef}*pest$ | pest' = ap_ef*pest: no explicit application-efficiency multiplication visible in pest_apply.f90. pest_kg is taken as the full applied amount; ap_ef may be applied in the calling controller before pest_kg is passed in. |
| 6:1.10.2 | Ground cover gc for pesticide foliage fraction | $gc=\frac{1.99532-erfc[1.333*LAI-1]}{2.1}$ | FLAG: code uses erfc(1.333*lai_sum - 2.) but the pesticide theory specifies offset -1 (not -2). Offset -2 matches the fertilizer-bacteria gc formula (6:1.7.8). Structure and constants otherwise match gc=(1.99532-erfc(...))/2.1. |
| 6:1.10.3 | Pesticide deposited on foliage | $pest_{fol}=gc*pest'$ | cs_pl%pl_on(ipl)%pest += gc*pl_frac*pest_kg; pl_frac distributes among plants by LAI fraction. |
| 6:1.10.4 | Pesticide deposited on soil surface | $pest_{surf}=(1-gc)*pest'$ | ly(1)%pest += (1-gc)*surf_frac*pest_kg; ly(2)%pest += (1-gc)*(1-surf_frac)*pest_kg. Additionally partitioned between soil layers 1 and 2 by chemapp_db surf_frac. |

## Lineage

Source-backed lineage resolved four commits affecting `pest_apply`. The initial addition in df07e3f introduced the routine with canopy-based foliage interception and soil partitioning. 94b6dec added the earlier documented implementation and module uses, including the same application logic and balance updates. 39fabde initialized local working variables `j`, `ipl`, `gc`, `surf_frac`, and `pl_frac` to zero. 4d173cc only removed the old inline documentation block and left the executable logic unchanged.

- df07e3f introduced the new `pest_apply` subroutine and its pesticide partitioning logic.
- 94b6dec added the implementation used here, including LAI-based canopy interception, soil-layer routing, and pesticide-balance updates.
- 39fabde changed local variable declarations to initialize `j`, `ipl`, `gc`, `surf_frac`, and `pl_frac` to zero.
- 4d173cc removed the old specification comment block without changing the executable behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pest_apply' has no extracted documentation comment.
- algorithm_steps revised: merged the original minimal step list into a fuller sequence that matches the visible source-line actions.
