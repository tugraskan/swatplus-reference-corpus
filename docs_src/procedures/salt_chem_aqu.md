---
kind: procedure
symbol: salt_chem_aqu
title: salt_chem_aqu
status: filled
source_hash: 6a5f28e437f9b60d
version_label: SWAT+ 62.0.0
locals:
  iaq: Aquifer index for the current hydrograph object; it is taken from `ob(icmd)%num` and
    used to read and write the matching aquifer and salt-state records.
  m: Loop index over `cs_db%num_salts` for accumulating aquifer salt mass and converting between
    stored mass and concentration.
  iter_count: Counts precipitation-dissolution iterations so the loop can stop on convergence
    or bail out after 500 passes.
  ion1: Temporary copy of sulfate concentration from `cs_aqu(iaq)%saltc(1)` before conversion
    to molar units.
  ion2: Temporary copy of calcium concentration from `cs_aqu(iaq)%saltc(2)` before conversion
    to molar units.
  ion3: Temporary copy of magnesium concentration from `cs_aqu(iaq)%saltc(3)` before conversion
    to molar units.
  ion4: Temporary copy of sodium concentration from `cs_aqu(iaq)%saltc(4)` before conversion
    to molar units.
  ion5: Temporary copy of potassium concentration from `cs_aqu(iaq)%saltc(5)` before conversion
    to molar units.
  ion6: Temporary copy of chloride concentration from `cs_aqu(iaq)%saltc(6)` before conversion
    to molar units.
  ion7: Temporary copy of carbonate concentration from `cs_aqu(iaq)%saltc(7)` before conversion
    to molar units.
  ion8: Temporary copy of bicarbonate concentration from `cs_aqu(iaq)%saltc(8)` before conversion
    to molar units.
  hru_area_m2: Aquifer HRU area converted from hectares to square meters so groundwater volume
    can be computed.
  gw_volume: Working groundwater volume for the aquifer; used to convert between salt mass
    and concentration.
  waterc: Assumed saturated water content/porosity factor used in solid-mineral concentration
    conversions.
  sol_caco3_p: One-element working array holding CaCO3 solid percentage before converting
    to and from concentration units.
  sol_mgco3_p: One-element working array holding MgCO3 solid percentage before converting
    to and from concentration units.
  sol_caso4_p: One-element working array holding CaSO4 solid percentage before converting
    to and from concentration units.
  sol_mgso4_p: One-element working array holding MgSO4 solid percentage before converting
    to and from concentration units.
  sol_nacl_p: One-element working array holding NaCl solid percentage before converting to
    and from concentration units.
  i_prep_in: Prepared ionic-strength value passed to `activity_coefficient` after `Ionic_strength`
    computes the initial solution strength.
  i_diff: Initialization flag for the ionic-strength comparison logic; set to 1 after preparing
    the ionic-strength input.
  skipediex: Counts how many times cation exchange had to be skipped because one or more adjusted
    cation concentrations were nonpositive.
  mass_before: Accumulator for total dissolved salt mass before the chemistry updates, used
    to compute net mass change.
  mass_after: Accumulator for total dissolved salt mass after the chemistry updates, used
    to compute the aquifer mass change.
  ionstr: Double-precision copy of the computed ionic strength returned by `Ionic_strength`.
  is_temp: Temporary output slot for the ionic-strength calculation before copying to `IonStr`.
  k_adj1: Activity-corrected equilibrium multiplier used to adjust the CaCO3 solubility constant.
  k_adj2: Activity-corrected equilibrium multiplier used to adjust the MgCO3 solubility constant.
  k_adj3: Activity-corrected equilibrium multiplier used to adjust the CaSO4 solubility constant.
  k_adj4: Activity-corrected equilibrium multiplier used to adjust the MgSO4 solubility constant.
  k_adj5: Activity-corrected equilibrium multiplier used to adjust the NaCl solubility constant.
  error1st: Difference between successive carbonate concentrations used as one convergence
    measure for the precipitation-dissolution loop.
  error2nd: Difference between successive calcium concentrations used as one convergence measure
    for the precipitation-dissolution loop.
  error3rd: Difference between successive sulfate concentrations used as one convergence measure
    for the precipitation-dissolution loop.
  errortotal: Maximum absolute concentration change across the tracked ions; it controls when
    the mineral-equilibrium loop stops.
uses:
  aquifer_module: The aquifer dynamic storage in `aqu_d(iaq)%stor` is needed to compute groundwater
    volume, which converts between stored salt mass and dissolved concentration.
  basin_module: The hydrograph connectivity state identifies which aquifer object is being
    processed and provides the aquifer area used in the groundwater-volume calculation.
  constituent_mass_module: The constituent-mass database supplies the salt count and the per-aquifer
    salt mass/concentration arrays that this routine reads, updates, and converts back to
    mass.
  salt_data_module: The constituent-mass module holds the aquifer salt pools and the number
    of salt species, which are the core shared state this chemistry solver updates.
  soil_module: The soil module matters because the routine uses the shared solid-phase conversion
    logic and saturation factor convention to express mineral concentrations in the model's
    soil/aqueous units.
  hydrograph_module: The hydrograph module provides the current object index and area so the
    routine can select the right aquifer and convert storage to volume.
  salt_module: The salt module matters because it contains the shared ion arrays and equilibrium
    constants that are adjusted during precipitation, dissolution, and cation exchange.
  salt_aquifer: The aquifer salt-balance state stores the dissolved mass change this routine
    computes so later aquifer accounting can report chemical gains or losses.
---

<!-- facts:header -->

Updates groundwater salt chemistry in an aquifer by converting stored salt mass to concentrations, iterating mineral equilibrium reactions, and applying cation exchange.

## Bottom Line

This subroutine takes the aquifer salt state for the current object, converts the dissolved and solid pools into working concentrations, and then iterates through precipitation-dissolution reactions for CaCO3, MgCO3, CaSO4, MgSO4, and NaCl until the solution changes are small. It also computes ionic strength and activity coefficients before the equilibrium loop so the solubility calculations use the current chemistry.

After the mineral reactions converge, it runs cation exchange, restores invalid exchange results when needed, writes the updated dissolved concentrations back to aquifer state, converts them back to salt mass, updates the solid mineral fractions, and records the dissolved mass change in the aquifer salt balance. Those results feed later groundwater salt and constituent accounting in the aquifer workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `aqu_1d_control` after recharge has been converted to aquifer units and only when there is at least one salt species to process. It prepares the aquifer salt state for the groundwater chemistry step, and its updated concentrations, solid mineral pools, and dissolved mass balance are then used by later aquifer salt and constituent routines.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the current aquifer and derive working geometry | Reads the aquifer object number from `ob(icmd)%num`, converts the aquifer area from hectares to square meters, clears the mass accumulators, and assigns the working water content used for solid-phase conversions. |
| 2. Load solid salt pools and convert them to working concentrations | Copies the five solid mineral pools from `cs_aqu(iaq)%salt_min` into local arrays and converts each from stored percentage-like units to the concentration form used by the chemistry equations. |
| 3. Convert stored aquifer salt mass to dissolved concentration | Computes groundwater volume from aquifer storage and area, clamps negative salt masses or concentrations to zero, accumulates pre-reaction mass, and derives dissolved salt concentration for each salt species when volume is available. |
| 4. Split dissolved salt concentrations into ion variables | Maps the eight salt-ion concentrations into local ion slots and converts them from mg/L to mol/L for sulfate, calcium, magnesium, sodium, potassium, chloride, carbonate, and bicarbonate. |
| 5. Compute ionic strength and initialize the solver state | Calls `Ionic_strength`, stores the result in `IonStr`, copies it to `I_Prep_in`, marks the ionic-strength difference flag, and initializes the concentration index counters used by the iterative reaction loop. |
| 6. Compute activity coefficients and adjusted solubility constants | Calls `activity_coefficient` and then combines selected `LAMDA` values to form activity corrections and adjusted equilibrium constants `salt_K1` through `salt_K5`. |
| 7. Iterate precipitation-dissolution reactions until convergence | Initializes the convergence error, then repeatedly calls the five mineral equilibrium routines, evaluates changes in carbonate, calcium, and sulfate concentrations, advances the working indices, and stops when the error is below the threshold or the loop exceeds 500 iterations. |
| 8. Convert the converged molar concentrations back to mg/L | After the mineral loop, multiplies the working molar ion concentrations by molecular weights to produce updated groundwater concentrations in mg/L. |
| 9. Apply cation exchange and guard against invalid results | Calls `cationexchange`, then checks whether calcium, magnesium, sodium, or potassium became nonpositive; if so, it restores the pre-exchange values and increments the skip counter. |
| 10. Write updated dissolved salt concentrations back to aquifer state | Stores the final updated dissolved ion concentrations into `cs_aqu(iaq)%saltc(1:8)` for the current aquifer. |
| 11. Convert updated concentrations back to salt mass and accumulate post-reaction mass | Recomputes groundwater volume, converts each dissolved salt concentration back to kg of salt in `cs_aqu(iaq)%salt(m)`, and sums the post-reaction dissolved mass. |
| 12. Save updated solid mineral pools and dissolved mass change | Converts the working solid concentrations back to solid percentages, writes them to `cs_aqu(iaq)%salt_min(1:5)`, and records the dissolved mass change in `asaltb_d(iaq)%salt(1)%diss`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:aquifer_module] | `aqu_d` | `aqu_d(iaq)%stor` |
| [sym:basin_module] | `ob, icmd` | `ob(icmd)%num, ob(icmd)%area_ha` |
| [sym:constituent_mass_module] | `cs_db, cs_aqu` | `cs_db%num_salts, cs_aqu(iaq)%salt(m), cs_aqu(iaq)%saltc(m), cs_aqu(iaq)%saltc(1), cs_aqu(iaq)%saltc(2), cs_aqu(iaq)%saltc(3), cs_aqu(iaq)%saltc(4), cs_aqu(iaq)%saltc(5), cs_aqu(iaq)%saltc(6), cs_aqu(iaq)%saltc(7), cs_aqu(iaq)%saltc(8), cs_aqu(iaq)%salt_min(1), cs_aqu(iaq)%salt_min(2), cs_aqu(iaq)%salt_min(3), cs_aqu(iaq)%salt_min(4), cs_aqu(iaq)%salt_min(5)` |
| [sym:salt_data_module] | `cs_db, cs_aqu` | `cs_db%num_salts, cs_aqu(iaq)%salt(m), cs_aqu(iaq)%saltc(m), cs_aqu(iaq)%saltc(1), cs_aqu(iaq)%saltc(2), cs_aqu(iaq)%saltc(3), cs_aqu(iaq)%saltc(4), cs_aqu(iaq)%saltc(5), cs_aqu(iaq)%saltc(6), cs_aqu(iaq)%saltc(7), cs_aqu(iaq)%saltc(8), cs_aqu(iaq)%salt_min(1), cs_aqu(iaq)%salt_min(2), cs_aqu(iaq)%salt_min(3), cs_aqu(iaq)%salt_min(4), cs_aqu(iaq)%salt_min(5)` |
| [sym:soil_module] | `Sol_CaCO3, Sol_MgCO3, Sol_CaSO4, Sol_MgSO4, Sol_NaCl, waterC` | `waterC` |
| [sym:salt_data_module] | `upion1, upion2, upion3, upion4, upion5, upion6, upion7, upion8, LAMDA, Ksp12, Ksp22, Ksp32, Ksp42, Ksp52, salt_K1, salt_K2, salt_K3, salt_K4, salt_K5, c11, c22, salt_c3, salt_c4, c5` | `LAMDA(1), LAMDA(2), LAMDA(3), LAMDA(5), LAMDA(6), Ksp12, Ksp22, Ksp32, Ksp42, Ksp52, salt_K1, salt_K2, salt_K3, salt_K4, salt_K5, upion1, upion2, upion3, upion4, upion5, upion6, upion7, upion8` |
| [sym:hydrograph_module] | `ob, icmd` | `ob(icmd)%num, ob(icmd)%area_ha` |
| [sym:salt_module] | `upion1, upion2, upion3, upion4, upion5, upion6, upion7, upion8, LAMDA, Ksp12, Ksp22, Ksp32, Ksp42, Ksp52, salt_K1, salt_K2, salt_K3, salt_K4, salt_K5` | `LAMDA(1), LAMDA(2), LAMDA(3), LAMDA(5), LAMDA(6), Ksp12, Ksp22, Ksp32, Ksp42, Ksp52, salt_K1, salt_K2, salt_K3, salt_K4, salt_K5, upion1, upion2, upion3, upion4, upion5, upion6, upion7, upion8` |
| [sym:salt_aquifer] | `asaltb_d` | `asaltb_d(iaq)%salt(1)%diss` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `Sol_CaCO3(1)` | After the solid-mineral conversion block at lines 76-86, with no special condition other than the current aquifer state being loaded. | This stores the updated CaCO3 solid percentage for the current aquifer after converting the working concentration back from the loop variables. |
| `Sol_MgCO3(1)` | After the solid-mineral conversion block at lines 76-86, with no special condition other than the current aquifer state being loaded. | This stores the updated MgCO3 solid percentage for the current aquifer after converting the working concentration back from the loop variables. |
| `Sol_CaSO4(1)` | After the solid-mineral conversion block at lines 76-86, with no special condition other than the current aquifer state being loaded. | This stores the updated CaSO4 solid percentage for the current aquifer after converting the working concentration back from the loop variables. |
| `Sol_MgSO4(1)` | After the solid-mineral conversion block at lines 76-86, with no special condition other than the current aquifer state being loaded. | This stores the updated MgSO4 solid percentage for the current aquifer after converting the working concentration back from the loop variables. |
| `Sol_NaCl(1)` | After the solid-mineral conversion block at lines 76-86, with no special condition other than the current aquifer state being loaded. | This stores the updated NaCl solid percentage for the current aquifer after converting the working concentration back from the loop variables. |
| `cs_aqu(iaq)%salt(m)` | During the post-chemistry save step at lines 228-236 after precipitation-dissolution and cation exchange are finished. | This writes the final dissolved salt mass for each species back into aquifer storage, using the converged groundwater concentration and groundwater volume. |
| `cs_aqu(iaq)%saltc(m)` | During the post-chemistry save step at lines 228-236 after precipitation-dissolution and cation exchange are finished. | This writes the final dissolved salt concentration for each species back into the aquifer's shared salt-concentration array. |
| `Sul_Conc(1)` | When the mineral-equilibrium loop has converged and the working sulfate concentration is converted back to mg/L. | Sulfate concentration is updated to the converged aquifer solution value, and later saved into `cs_aqu(iaq)%saltc(1)`. |
| `Cal_Conc(1)` | When the mineral-equilibrium loop has converged and the working calcium concentration is converted back to mg/L. | Calcium concentration is updated to the converged aquifer solution value, and later saved into `cs_aqu(iaq)%saltc(2)`. |
| `Mg_Conc(1)` | When the mineral-equilibrium loop has converged and the working magnesium concentration is converted back to mg/L. | Magnesium concentration is updated to the converged aquifer solution value, and later saved into `cs_aqu(iaq)%saltc(3)`. |
| `Sod_Conc(1)` | When the mineral-equilibrium loop has converged and the working sodium concentration is converted back to mg/L. | Sodium concentration is updated to the converged aquifer solution value, and later saved into `cs_aqu(iaq)%saltc(4)`. |
| `Pot_Conc(1)` | When the mineral-equilibrium loop has converged and the working potassium concentration is converted back to mg/L. | Potassium concentration is updated to the converged aquifer solution value, and later saved into `cs_aqu(iaq)%saltc(5)`. |
| `Cl_Conc(1)` | When the mineral-equilibrium loop has converged and the working chloride concentration is converted back to mg/L. | Chloride concentration is updated to the converged aquifer solution value, and later saved into `cs_aqu(iaq)%saltc(6)`. |
| `Car_Conc(1)` | When the mineral-equilibrium loop has converged and the working carbonate concentration is converted back to mg/L. | Carbonate concentration is updated to the converged aquifer solution value, and later saved into `cs_aqu(iaq)%saltc(7)`. |
| `BiCar_Conc(1)` | When the mineral-equilibrium loop has converged and the working bicarbonate concentration is converted back to mg/L. | Bicarbonate concentration is updated to the converged aquifer solution value, and later saved into `cs_aqu(iaq)%saltc(8)`. |
| `c11` | Inside the precipitation-dissolution loop after the mineral calls, when the loop advances the calcium index counter. | The calcium working index advances by two slots so the next iteration compares the next before/after pair of calcium concentrations. |
| `c22` | Inside the precipitation-dissolution loop after the mineral calls, when the loop advances the carbonate index counter. | The carbonate working index advances by two slots so the next iteration compares the next before/after pair of carbonate concentrations. |
| `salt_c3` | Inside the precipitation-dissolution loop after the mineral calls, when the loop advances the magnesium index counter. | The magnesium working index advances by two slots so the next iteration compares the next before/after pair of magnesium concentrations. |
| `salt_c4` | Inside the precipitation-dissolution loop after the mineral calls, when the loop advances the sulfate index counter. | The sulfate working index advances by two slots so the next iteration compares the next before/after pair of sulfate concentrations. |
| `c5` | Inside the precipitation-dissolution loop after the mineral calls, when the loop advances the potassium/chloride index counter. | The shared index for potassium and chloride advances by one so the next loop pass writes the next updated cation/anion pair. |
| `salt_K1` | Immediately after the activity-coefficient calculation at lines 143-154. | Stores the activity-corrected CaCO3 solubility constant used by the mineral equilibrium routines. |
| `salt_K2` | Immediately after the activity-coefficient calculation at lines 143-154. | Stores the activity-corrected MgCO3 solubility constant used by the mineral equilibrium routines. |
| `salt_K3` | Immediately after the activity-coefficient calculation at lines 143-154. | Stores the activity-corrected CaSO4 solubility constant used by the mineral equilibrium routines. |
| `salt_K4` | Immediately after the activity-coefficient calculation at lines 143-154. | Stores the activity-corrected MgSO4 solubility constant used by the mineral equilibrium routines. |

## File I/O

<!-- facts:io -->


## Lineage

`salt_chem_aqu.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `salt_chem_aqu.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `fd90e36` (2025-02-06) — variable initialization changes
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `2405a68` (2024-07-16) — Fixing for Compiling
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_chem_aqu' has no extracted documentation comment.
- algorithm_steps revised: replaced the draft's broad loop/call descriptions with 12 source-backed steps that follow the actual control flow and line numbers in `salt_chem_aqu.f90`.
- The source includes `use salt_data_module` twice; this appears intentional in the extracted file but may be a duplicate import.
- The variable name `SkipedIEX` is preserved from source spelling.
- No commits were resolved for lineage, so lineage impacts are empty.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
