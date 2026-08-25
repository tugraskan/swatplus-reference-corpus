---
kind: procedure
symbol: regres
title: regres
status: filled
source_hash: 8cb974993e914ee3
version_label: SWAT+ 62.0.0
args:
  k: '`k` chooses which urban constituent regression to use: 1 for carbonaceous oxygen demand,
    2 for suspended solid load, 3 for total nitrogen, and 4 for total phosphorus.'
locals:
  beta: '`beta` is the active 5x3 coefficient table for the selected constituent. It is reset
    to zero, then filled from one of the preset tables so the regression can use the precipitation-category-specific
    coefficients.'
  regres: '`regres` holds the computed urban constituent load returned by the function, first
    in pounds-equivalent form from the regression and then converted to kilograms before return.'
  ulu: '`ulu` stores the urban land-use database index for the current HRU so the function
    can look up the impervious fraction in `urbdb(ulu)%fimp`.'
  j: '`j` stores the current HRU index copied from `ihru`; it is used to fetch the HRU state
    from `hru(j)`.'
  ii: '`ii` stores the precipitation-category index from `wgn_pms(iwgen)%ireg` so the function
    can pick the correct column of the regression coefficient table.'
  bcod: '`bcod` is the hard-coded 5x3 regression coefficient table for carbonaceous oxygen
    demand from the USGS urban regression equations.'
  bsus: '`bsus` is the hard-coded 5x3 regression coefficient table for suspended solid load
    from the USGS urban regression equations.'
  btn: '`btn` is the hard-coded 5x3 regression coefficient table for total nitrogen from the
    USGS urban regression equations.'
  btp: '`btp` is the hard-coded 5x3 regression coefficient table for total phosphorus from
    the USGS urban regression equations.'
uses:
  hru_module: The HRU module provides the current HRU index and HRU attributes that identify
    which land unit is being processed and which urban land-use record applies. `hru(j)%luse%urb_lu`
    supplies the lookup key for urban database data, and `hru(j)%km` supplies the HRU area
    term used in the regression.
  climate_module: The climate module provides the precipitation category and current-day precipitation
    needed by the regression. `wgn_pms(iwgen)%ireg` selects the regression column for the
    climate regime, and `w%precip` supplies the rainfall amount used in the load calculation.
  urban_data_module: The urban data module provides the impervious-fraction value for the
    selected urban land-use record. `urbdb(ulu)%fimp` directly scales the regression terms
    and is also used by the caller to partition sediment loading.
---

<!-- facts:header -->

Computes urban constituent loads with USGS regression equations for a selected pollutant class. The result is used by urban HRU runoff handling.

## Bottom Line

regres selects one of four coefficient tables based on the input code `k`, then evaluates the USGS urban regression equation for the current HRU, weather-generator precipitation class, and urban impervious fraction. It returns an estimated constituent load in kilograms after converting from pounds.

This routine matters because `hru_urban` calls it to compute COD, suspended sediment, total nitrogen, and total phosphorus loads whenever the urban runoff option is `usgs_reg` and there is enough precipitation and surface runoff to proceed.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This function runs inside the urban HRU workflow after `hru_urban` has selected the `usgs_reg` branch and checked that precipitation and surface runoff are nontrivial. Its output feeds the caller's COD, suspended sediment, TN, and TP calculations, which then affect urban sediment and constituent routing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. copy HRU index | Copies the active HRU number from `ihru` into local `j` so the function can address the current HRU record. |
| 2. get precip class | Reads the annual precipitation category from the current weather generator record and stores it in `ii`. |
| 3. get urban land use | Looks up the urban land-use code for the current HRU and stores it in `ulu` so the impervious fraction can be retrieved. |
| 4. clear coefficients | Zeroes the coefficient matrix before selecting one pollutant's regression table. |
| 5. select COD table | Uses the carbonaceous oxygen demand coefficients when `k` equals 1. |
| 6. select suspended solids table | Uses the suspended-solid coefficients when `k` equals 2. |
| 7. select TN table | Uses the total-nitrogen coefficients when `k` equals 3. |
| 8. select TP table | Uses the total-phosphorus coefficients when `k` equals 4. |
| 9. evaluate regression | Computes the pollutant load from precipitation depth, HRU area, urban impervious fraction, and the selected coefficient set. |
| 10. convert units | Divides the computed load by 2.205 to convert pounds to kilograms before returning it. |
| 11. return result | Returns the computed load to the caller and ends the function. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, ihru, iwgen` | `hru(j)%luse%urb_lu, hru(j)%km` |
| [sym:climate_module] | `wgn_pms, w` | `wgn_pms(iwgen)%ireg, w%precip` |
| [sym:urban_data_module] | `urbdb` | `urbdb(ulu)%fimp` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 6:3.3.1 | USGS urban constituent loading regression | $Y=\frac{\beta_0*(R_{day}/25.4)^{\beta_1}*(DA*imp_{tot}/2.59)^{\beta_2}*(imp_{tot}*100+1)^{\beta_3}*\beta_4}{2.205}$ | regres=beta1*(precip/25.4)^beta2*(km*fimp/2.589)^beta3*(fimp*100+1)^beta4*beta5/2.205; exact match for Y=beta0*(R_day/25.4)^beta1*(DA*imp_tot/2.59)^beta2*(imp_tot*100+1)^beta3*beta4/2.205. Called from hru_urban.f90:95-99 for COD, sus_sol, TN, TP. |

## Lineage

Three resolved commits changed `regres.f90`. df07e3f added the function with its USGS regression logic and documentation comments. 39fabde initialized the coefficient array and loop/index locals with default values. 2ee1889 changed the closing statement from `end` to `end function regres`.

- df07e3f introduced the full urban constituent regression function, including the pollutant coefficient tables, HRU/weather/urban lookups, and pounds-to-kilograms conversion.
- 39fabde made the local coefficient matrix and index variables explicitly initialized at declaration, reducing dependence on implicit state.
- 2ee1889 updated the function terminator to an explicit `end function regres` without changing the calculation.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'regres' has no extracted documentation comment.
