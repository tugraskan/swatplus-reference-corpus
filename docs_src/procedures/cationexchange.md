---
kind: procedure
symbol: cationexchange
title: cationexchange
status: filled
source_hash: 04106da4ce0a53bc
version_label: SWAT+ 62.0.0
locals:
  cec: Cation exchange capacity used as the total exchange-site pool in the equilibrium formulas;
    it is hard-coded here to 15 meq/100g soil.
  sel_k1: Gapon selectivity coefficient used in the Ca/Mg exchange relationships.
  sel_k2: Gapon selectivity coefficient used to relate Ca and Na exchange terms.
  sel_k3: Gapon selectivity coefficient used to relate Ca and K exchange terms.
  sel_k4: Gapon selectivity coefficient used to relate Mg and Na exchange terms.
  sel_k5: Gapon selectivity coefficient used to relate Mg and K exchange terms.
  sel_k6: Gapon selectivity coefficient used in the Na/K exchange relationships.
  xcaini: Initial exchangeable calcium amount used as the baseline for computing the calcium
    exchange change.
  xmgini: Initial exchangeable magnesium amount used as the baseline for computing the magnesium
    exchange change.
  xnaini: Initial exchangeable sodium amount used as the baseline for computing the sodium
    exchange change.
  xkini: Initial exchangeable potassium amount used as the baseline for computing the potassium
    exchange change.
  deltax_ca: Difference between computed and initial exchangeable calcium; used to adjust
    `upion2`.
  deltax_mg: Difference between computed and initial exchangeable magnesium; used to adjust
    `upion3`.
  deltax_na: Difference between computed and initial exchangeable sodium; used to adjust `upion4`.
  deltax_k: Difference between computed and initial exchangeable potassium; used to adjust
    `upion5`.
  con_ca: Solution calcium concentration converted from `upion2` to mmol/L before exchange
    calculations.
  con_mg: Solution magnesium concentration converted from `upion3` to mmol/L before exchange
    calculations.
  con_na: Solution sodium concentration converted from `upion4` to mmol/L before exchange
    calculations.
  con_k: Solution potassium concentration converted from `upion5` to mmol/L before exchange
    calculations.
  x_ca: Computed exchangeable calcium amount after applying the selectivity equations.
  x_mg: Computed exchangeable magnesium amount after applying the selectivity equations.
  x_na: Computed exchangeable sodium amount after applying the selectivity equations.
  x_k: Computed exchangeable potassium amount after applying the selectivity equations.
uses:
  organic_mineral_mass_module: The routine uses no resolved symbols from `organic_mineral_mass_module`
    in the extracted source span, but the module is still part of the routine's dependency
    list and may provide soil or mass-state context elsewhere in the file.
  salt_data_module: '`salt_data_module` supplies the shared `upion2`, `upion3`, `upion4`,
    and `upion5` variables that this routine reads as input solution concentrations and then
    overwrites with the exchange-adjusted values.'
---

<!-- facts:header -->

Adjusts solution-phase calcium, magnesium, sodium, and potassium after cation exchange using a simple Gapon-style equilibrium calculation.

## Bottom Line

This subroutine performs the cation-exchange part of the salt chemistry package. It converts the solution calcium, magnesium, sodium, and potassium pools in `upion2` through `upion5` to mmol/L, applies fixed Gapon-style selectivity equations with an assumed CEC of 15 meq/100g soil, and writes exchange-adjusted concentrations back to the same `upion` variables.

It matters because `salt_chem_aqu` and `salt_chem_hru` call it immediately after assembling the solution ion pools. Those callers later test the returned `upion2` through `upion5`; if any ion is nonpositive, the routine has already marked that ion with `-10` so the caller can restore the original values and skip the exchange result.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the salt-chemistry workflow after the caller has populated `upion2` to `upion5` from the current calcium, magnesium, sodium, and potassium solution concentrations. `salt_chem_aqu` and `salt_chem_hru` both prepare those inputs and then call `cationexchange`; later logic in those callers checks whether any returned `upion` value is nonpositive and, if so, restores the original concentrations and skips the exchange result.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load module state and initialize locals | Imports the salt data state, declares local exchange variables, and initializes CEC, selectivity constants, reference exchange amounts, converted concentrations, and exchange results to zero. |
| 2. set soil CEC | Uses a fixed cation exchange capacity of 15 meq/100g soil as the simplified soil property for the calculation. |
| 3. convert solution ions | Converts `upion2` through `upion5` from ppm into mmol/L water and stores the results in `Con_Ca`, `Con_Mg`, `Con_Na`, and `Con_K`. |
| 4. require all ions positive | Runs the exchange calculation only when all four converted ion concentrations are positive. |
| 5. set Gapon selectivity constants | Assigns fixed Gapon selectivity coefficients for the Ca, Mg, Na, and K exchange relationships. |
| 6. set baseline exchange amounts | Loads fixed initial exchangeable amounts for Ca, Mg, Na, and K that serve as the baseline for computing exchange deltas. |
| 7. solve exchange equilibrium | Computes equilibrium exchange amounts `X_Ca`, `X_Mg`, `X_Na`, and `X_K` from CEC and the relative solution concentrations using Gapon-style formulas. |
| 8. compute exchange deltas | Subtracts the initial exchange amounts from the equilibrium amounts to obtain `DeltaX_Ca`, `DeltaX_Mg`, `DeltaX_Na`, and `DeltaX_K`. |
| 9. write adjusted solution concentrations | Updates `upion2` through `upion5` by converting the exchange deltas back to ppm and subtracting them from the solution pools. |
| 10. flag invalid calcium | If the converted calcium concentration was nonpositive, sets `upion2` to `-10` so the caller can recognize that the exchange result is invalid. |
| 11. flag invalid magnesium | If the converted magnesium concentration was nonpositive, sets `upion3` to `-10` so the caller can recognize that the exchange result is invalid. |
| 12. flag invalid sodium | If the converted sodium concentration was nonpositive, sets `upion4` to `-10` so the caller can recognize that the exchange result is invalid. |
| 13. flag invalid potassium and return | If the converted potassium concentration was nonpositive, sets `upion5` to `-10`, then returns to the caller with the adjusted or sentinel-marked ion pools. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:salt_data_module] | `upion2, upion3, upion4, upion5` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `upion2` | When all converted ion concentrations are positive, `upion2` is recomputed from the current Ca solution pool minus the Ca exchange delta; if converted Ca is nonpositive, `upion2` is forced to `-10`. | `upion2` is the updated calcium solution concentration passed back to the caller. It represents the exchange-corrected Ca pool unless the routine marks it as invalid for caller-side fallback. |
| `upion3` | When all converted ion concentrations are positive, `upion3` is recomputed from the current Mg solution pool minus the Mg exchange delta; if converted Mg is nonpositive, `upion3` is forced to `-10`. | `upion3` is the updated magnesium solution concentration passed back to the caller. It represents the exchange-corrected Mg pool unless the routine marks it as invalid for caller-side fallback. |
| `upion4` | When all converted ion concentrations are positive, `upion4` is recomputed from the current Na solution pool minus the Na exchange delta; if converted Na is nonpositive, `upion4` is forced to `-10`. | `upion4` is the updated sodium solution concentration passed back to the caller. It represents the exchange-corrected Na pool unless the routine marks it as invalid for caller-side fallback. |
| `upion5` | When all converted ion concentrations are positive, `upion5` is recomputed from the current K solution pool minus the K exchange delta; if converted K is nonpositive, `upion5` is forced to `-10`. | `upion5` is the updated potassium solution concentration passed back to the caller. It represents the exchange-corrected K pool unless the routine marks it as invalid for caller-side fallback. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four source-history points for `cationexchange`. The original addition in `df07e3f` introduced the subroutine and its cation-exchange formulas; `35b029c` made only a whitespace/end-of-file cleanup near the subroutine end; `94b6dec` preserved the routine while replacing the file-wide `end` with explicit `end subroutine` forms elsewhere; and `39fabde` initialized local variables to zero without changing the exchange logic.

- df07e3f added `cationexchange` with the CEC-based Gapon selectivity equations, the `upion2`-`upion5` conversions, and the invalid-value sentinels.
- 35b029c only adjusted the trailing `end`/blank-line formatting for the subroutine and did not change behavior.
- 39fabde initialized the routine's local variables to zero at declaration, improving determinism without changing the exchange calculations.

## Review Notes

- No direct file I/O was extracted for this procedure.
- organic_mineral_mass_module is listed as a dependency in the source, but no resolved symbols from that module were found in the extracted span.
