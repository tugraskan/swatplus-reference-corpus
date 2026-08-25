---
kind: procedure
symbol: salt_chem_soil_single
title: salt_chem_soil_single
status: filled
source_hash: 8d761ff26f1d18ae
version_label: SWAT+ 62.0.0
args:
  hru_num: Selects which HRU profile `cs_soil(j)` and `soil(j)` are read and updated; the
    routine uses it to pick the soil and constituent-mass state for this call.
  lay_num: Selects which soil layer within the chosen HRU is processed; the routine reads
    mineral salts, bulk density, and layer state for that layer only.
  waterc: Gives the water content used in the unit conversions from stored solid salt mass
    to concentration; it controls how the solid salt pools are scaled into mg/L-equivalent
    equilibrium inputs.
locals:
  j: Copies `hru_num` so the routine can index the HRU-level soil and constituent-mass arrays
    while keeping the input argument unchanged.
  jj: Copies `lay_num` so the routine can index the selected soil layer in `cs_soil(j)%ly(jj)`
    and `soil(j)%phys(jj)`.
  iter_count: Counts precipitation-dissolution iterations and provides a safety stop if the
    loop exceeds 500 passes.
  ion1: Holds the incoming sulfate concentration from `soil_salt_conc(1)` before conversion
    to mol/L.
  ion2: Holds the incoming calcium concentration from `soil_salt_conc(2)` before conversion
    to mol/L.
  ion3: Holds the incoming magnesium concentration from `soil_salt_conc(3)` before conversion
    to mol/L.
  ion4: Holds the incoming sodium concentration from `soil_salt_conc(4)` before conversion
    to mol/L.
  ion5: Holds the incoming potassium concentration from `soil_salt_conc(5)` before conversion
    to mol/L.
  ion6: Holds the incoming chloride concentration from `soil_salt_conc(6)` before conversion
    to mol/L.
  ion7: Holds the incoming carbonate concentration from `soil_salt_conc(7)` before conversion
    to mol/L.
  ion8: Holds the incoming bicarbonate concentration from `soil_salt_conc(8)` before conversion
    to mol/L.
  sol_bd: Stores the soil bulk density for the selected layer so the mineral salt mass can
    be converted to a concentration basis.
  sol_caco3_p: Temporary storage for the CaCO3 mineral amount read from `cs_soil(j)%ly(jj)%salt_min(1)`
    before conversion.
  sol_mgco3_p: Temporary storage for the MgCO3 mineral amount read from `cs_soil(j)%ly(jj)%salt_min(2)`
    before conversion.
  sol_caso4_p: Temporary storage for the CaSO4 mineral amount read from `cs_soil(j)%ly(jj)%salt_min(3)`
    before conversion.
  sol_mgso4_p: Temporary storage for the MgSO4 mineral amount read from `cs_soil(j)%ly(jj)%salt_min(4)`
    before conversion.
  sol_nacl_p: Temporary storage for the NaCl mineral amount read from `cs_soil(j)%ly(jj)%salt_min(5)`
    before conversion.
  i_prep_in: Holds the ionic-strength value passed into `activity_coefficient` after it is
    computed by `Ionic_strength`.
  i_diff: Set to 1 as a flag-like helper value before the activity-coefficient call; it is
    not otherwise used in the visible source.
  ionstr: Stores the computed ionic strength copied from `IS_temp` so it can be passed into
    the activity-coefficient calculation.
  is_temp: Receives the ionic-strength result from `Ionic_strength` before the value is copied
    into `IonStr`.
  k_adj1: Holds the activity-coefficient product `LAMDA(1)*LAMDA(3)` used to normalize the
    first solubility product.
  k_adj2: Holds the activity-coefficient product `LAMDA(5)*LAMDA(3)` used to normalize the
    second solubility product.
  k_adj3: Holds the activity-coefficient product `LAMDA(1)*LAMDA(2)` used to normalize the
    third solubility product.
  k_adj4: Holds the activity-coefficient product `LAMDA(5)*LAMDA(2)` used to normalize the
    fourth solubility product.
  k_adj5: Holds the activity-coefficient product `LAMDA(6)*LAMDA(6)` used to normalize the
    fifth solubility product.
  error1st: Stores the carbonate convergence error as the difference between successive carbonate
    concentration slots.
  error2nd: Stores the calcium convergence error as the difference between successive calcium
    concentration slots.
  error3rd: Stores the sulfate convergence error as the difference between successive sulfate
    concentration slots.
  errortotal: Tracks the largest absolute convergence error among carbonate, calcium, and
    sulfate to decide whether the precipitation-dissolution loop should continue.
uses:
  basin_module: '`basin_module` is imported for shared basin-wide state that can be referenced
    by salt chemistry routines in the model, even though this extraction did not resolve a
    specific basin variable use inside the source span.'
  constituent_mass_module: '`constituent_mass_module` provides `cs_soil`, which holds the
    per-HRU, per-layer mineral salt inventories that are the starting point for the equilibrium
    calculations.'
  salt_data_module: '`salt_data_module` is imported because the routine works with shared
    salt arrays and constants such as the ion concentrations, mineral pools, and equilibrium
    parameters that the chemistry update reads and writes.'
  soil_module: '`soil_module` supplies `soil(j)%phys(jj)%bd`, the layer bulk density needed
    to convert the stored mineral salt amounts into concentration units for the chemistry
    solve.'
  salt_module: '`salt_module` matters because it supplies the salt-equilibrium globals such
    as solubility products, activity coefficients, and concentration arrays that the routine
    updates in place.'
  time_module: '`time_module` is imported as part of the shared model state used by SWAT+
    routines; this procedure does not resolve a specific time variable in the extracted span,
    but it runs inside the model time-step framework driven by that module.'
---

<!-- facts:header -->

Computes equilibrium salt-ion chemistry for one HRU soil layer. It converts stored mineral salts and pore-water ion concentrations into updated dissolved and solid-phase concentrations, then writes the adjusted soil-salt state back for later model use.

## Bottom Line

salt_chem_soil_single updates the salt chemistry of one soil layer in one HRU. It starts from the current solid salt pools and dissolved ion concentrations, converts them into consistent units, computes ionic strength and activity coefficients, then iterates precipitation-dissolution reactions until the carbonate, calcium, and sulfate concentrations stop changing enough.

The routine matters because it is the chemistry step that turns the water-updated soil salt concentrations into equilibrium-adjusted values. Its results overwrite the shared soil-salt concentration arrays that later water and salt balance calculations use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the soil-water update path after `pl_waterup` has computed the layer water content `theta_w` and scaled the soil salt concentrations into `soil_salt_conc`. `pl_waterup` calls it only when the layer has water (`theta_w.gt.(1e-5)`), and the results are then used to recompute layer total dissolved salts and to overwrite `soil_salt_conc` for subsequent salt and water balance calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the caller's HRU and layer into local indices. | Copies `hru_num` into `j` and `lay_num` into `jj` so the routine can use those indices for the shared soil and constituent-mass arrays. |
| 2. Read the solid salt inventories for the selected layer. | Loads CaCO3, MgCO3, CaSO4, MgSO4, and NaCl mineral pools from `cs_soil(j)%ly(jj)%salt_min` into temporary working arrays. |
| 3. Convert solid mineral amounts to concentration form. | Uses the layer bulk density and the incoming water content to convert the stored mineral masses into concentration values for the equilibrium solve. |
| 4. Read current dissolved ion concentrations and convert them to molar units. | Pulls sulfate, calcium, magnesium, sodium, potassium, chloride, carbonate, and bicarbonate from `soil_salt_conc` and converts each from mg/L to mol/L. |
| 5. Compute ionic strength and prepare activity-coefficient input. | Calls `Ionic_strength`, copies the result into `IonStr`, and stores it in `I_Prep_in` for the activity-coefficient calculation. |
| 6. Initialize the concentration-slot counters used in the iteration loop. | Sets `c11`, `c22`, `salt_c3`, `salt_c4`, and `c5` to 1 so the reaction routines can write their next values into known array slots. |
| 7. Compute activity coefficients for the current ionic strength. | Calls `activity_coefficient` to populate `LAMDA`, which is then used to adjust solubility products. |
| 8. Build activity-adjusted solubility constants and guard against zero divisors. | Forms `K_ADJ1` through `K_ADJ5` from `LAMDA` products and computes `salt_K1` through `salt_K5` only when the corresponding adjustment factor is positive. |
| 9. Enter the precipitation-dissolution loop. | Initializes `errorTotal` and `iter_count`, then repeats the mineral-equilibrium package until the maximum concentration change falls below the tolerance. |
| 10. Apply the five mineral equilibrium reactions each pass. | Calls `CaCO3`, `MgCO3`, `CaSO4`, `MgSO4`, and `NaCl` in sequence to update the dissolved and solid salt pools. |
| 11. Measure convergence from the updated carbonate, calcium, and sulfate slots. | Computes three successive-state differences and sets `errorTotal` to the largest absolute error so the loop can decide whether another iteration is needed. |
| 12. Advance the slot counters and iteration count. | Increments the concentration indices for the next pass and stops early with `goto 10` if the loop exceeds 500 iterations. |
| 13. Export the final ion concentrations and overwrite shared soil-salt state. | Copies the converged molar concentrations into `upion1` through `upion8` and converts them back to mg/L in `soil_salt_conc(1:8)`. |
| 14. Return to the caller. | Ends the subroutine after the soil-salt concentrations have been updated in shared state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state and types` | `No candidate outside references were resolved to this module.` |
| [sym:constituent_mass_module] | `cs_soil` |  |
| [sym:salt_data_module] | `salt_data_module state and types` | `No candidate outside references were resolved to this module.` |
| [sym:soil_module] | `soil` | `soil(j)%phys(jj)%bd` |
| [sym:salt_data_module] | `salt_data_module state and types` | `No candidate outside references were resolved to this module.` |
| [sym:salt_module] | `salt_module state and types` | `No candidate outside references were resolved to this module.` |
| [sym:time_module] | `time_module state and types` | `No candidate outside references were resolved to this module.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `Sol_CaCO3(1)` | After the precipitation-dissolution loop runs, using the converged calcium slot `Cal_Conc(c11)`. | Stores the equilibrated calcium mineral pool so later iterations and the final back-conversion can use the updated CaCO3 state. |
| `Sol_MgCO3(1)` | After the precipitation-dissolution loop runs, using the converged magnesium/carbonate reaction state. | Stores the equilibrated MgCO3 mineral pool so later iterations can continue from the updated magnesium-carbonate state. |
| `Sol_CaSO4(1)` | After the precipitation-dissolution loop runs, using the converged sulfate-calcium reaction state. | Stores the equilibrated CaSO4 mineral pool so later iterations and the final soil-salt update use the updated gypsum-like state. |
| `Sol_MgSO4(1)` | After the precipitation-dissolution loop runs, using the converged magnesium-sulfate reaction state. | Stores the equilibrated MgSO4 mineral pool so later iterations and the final soil-salt update use the updated magnesium sulfate state. |
| `Sol_NaCl(1)` | After the precipitation-dissolution loop runs, using the converged sodium/chloride slot `Sod_Conc(c5)` and `Cl_Conc(c5)`. | Stores the equilibrated NaCl mineral pool so the final back-conversion reflects any precipitation or dissolution of sodium chloride. |
| `Sul_Conc(1)` | After each mineral-equilibrium iteration, because `MgSO4` updates the shared sulfate concentration and the final back-conversion reads `Sul_Conc(salt_c4)`. | Updates sulfate concentration in the shared concentration array so the convergence check and final `soil_salt_conc` write-out reflect the equilibrated sulfate state. |
| `Cal_Conc(1)` | After each CaCO3 iteration and in the final state export. | Updates calcium concentration in the shared concentration array so the convergence test and the returned `soil_salt_conc(2)` reflect equilibrium calcium. |
| `Mg_Conc(1)` | After the MgCO3 and MgSO4 reactions update the magnesium slots. | Updates magnesium concentration in the shared concentration array so the final soil-water salt concentration reflects the equilibrated magnesium pool. |
| `Sod_Conc(1)` | After NaCl and related cation-exchange effects update the sodium slot. | Updates sodium concentration in the shared concentration array so the final soil-salt output includes equilibrated sodium. |
| `Pot_Conc(1)` | After NaCl equilibrium and final state export. | Updates potassium concentration in the shared concentration array; even though potassium is not reacted here, it is carried through and written back unchanged from the latest slot. |
| `Cl_Conc(1)` | After NaCl equilibrium and final state export. | Updates chloride concentration in the shared concentration array so the final soil-water salt state reflects the equilibrated chloride pool. |
| `Car_Conc(1)` | After the carbonate-bearing reactions and final state export. | Updates carbonate concentration in the shared concentration array so the loop convergence and output state track carbonate equilibrium. |
| `BiCar_Conc(1)` | After the carbonate-bearing reactions and final state export. | Updates bicarbonate concentration in the shared concentration array; this species is carried through the chemistry solve and written back to shared state. |
| `c11` | Before the precipitation-dissolution loop, after `LAMDA` has been computed. | Stores the first activity-adjustment factor used to normalize the first solubility-product ratio. |
| `c22` | Before the precipitation-dissolution loop, after `LAMDA` has been computed. | Stores the second activity-adjustment factor used to normalize the second solubility-product ratio. |
| `salt_c3` | Before the precipitation-dissolution loop, after `LAMDA` has been computed. | Stores the third activity-adjustment factor used to normalize the third solubility-product ratio. |
| `salt_c4` | Before the precipitation-dissolution loop, after `LAMDA` has been computed. | Stores the fourth activity-adjustment factor used to normalize the fourth solubility-product ratio. |
| `c5` | Before the precipitation-dissolution loop, after `LAMDA` has been computed. | Stores the fifth activity-adjustment factor used to normalize the fifth solubility-product ratio. |
| `salt_K1` | When `K_ADJ1.gt.0.`. | Holds the activity-corrected solubility product ratio for the first mineral reaction; otherwise it is set to zero to avoid division by zero. |
| `salt_K2` | When `K_ADJ2.gt.0.`. | Holds the activity-corrected solubility product ratio for the second mineral reaction; otherwise it is set to zero to avoid division by zero. |
| `salt_K3` | When `K_ADJ3.gt.0.`. | Holds the activity-corrected solubility product ratio for the third mineral reaction; otherwise it is set to zero to avoid division by zero. |
| `salt_K4` | When `K_ADJ4.gt.0.`. | Holds the activity-corrected solubility product ratio for the fourth mineral reaction; otherwise it is set to zero to avoid division by zero. |
| `salt_K5` | When `K_ADJ5.gt.0.`. | Holds the activity-corrected solubility product ratio for the fifth mineral reaction; otherwise it is set to zero to avoid division by zero. |
| `upion2` | After the loop has converged or been exited through the iteration limit. | Stores the equilibrated calcium concentration for export back to the shared state and to the caller-side soil salt concentrations. |

## File I/O

<!-- facts:io -->


## Lineage

`salt_chem_soil_single.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `salt_chem_soil_single.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `35b029c` (2024-03-24) — Mar 19 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_chem_soil_single' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
