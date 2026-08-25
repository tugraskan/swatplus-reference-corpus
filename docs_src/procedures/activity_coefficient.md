---
kind: procedure
symbol: activity_coefficient
title: activity_coefficient
status: filled
source_hash: 9608cf1387ae90da
version_label: SWAT+ 62.0.0
args:
  i_prep_in: '`I_Prep_in` is the prepared ionic-strength value passed in by the caller. The
    routine uses it to choose the low-, normal-, or high-strength formula branch and to compute
    the coefficients stored in `LAMDA`.'
locals:
  charbal: Fixed charge factors for the seven ions represented in `LAMDA`; they are squared
    in the exponent so stronger charges get larger activity corrections.
  a_size: Fixed ion-size parameters used in the low-ionic-strength branch to scale the denominator
    of the activity-coefficient formula.
  ii: Loop index over the seven ions in `LAMDA`; initialized to 0 and then reused in each
    branch to write one coefficient per ion.
  a: Empirical constant set to 0.5 at 298 K and used as the leading scale factor in the exponent.
  b: Empirical constant set to 0.33 at 298 K and used only in the low-ionic-strength denominator
    term.
uses:
  salt_data_module: '`salt_data_module` owns the shared `LAMDA(7)` array that this routine
    updates; without that module, the computed coefficients would not be available to the
    later salt-equilibrium routines that adjust equilibrium constants.'
  organic_mineral_mass_module: The source imports `organic_mineral_mass_module`, but no specific
    symbols from that module are referenced in the extracted lines, so its direct role here
    is uncertain from the provided evidence.
---

<!-- facts:header -->

Computes salt ion activity coefficients from the current ionic strength. It fills the shared `LAMDA` array for later salt-equilibrium calculations.

## Bottom Line

This routine takes an ionic-strength-like input, `I_Prep_in`, and converts it into seven activity coefficients in the shared `LAMDA(7)` array. The coefficients are computed with a temperature-fixed Debye-Hückel-style expression, using charge values from `CharBal` and ion-size terms from `a_size`.

It matters because the salt chemistry routines use `LAMDA` to adjust equilibrium constants before solving precipitation, dissolution, and complexation behavior. The callers in the aquifer, HRU, and single-soil salt chemistry paths all depend on these updated coefficients.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the salt-chemistry workflow after a caller has prepared `I_Prep_in` from the current solution conditions. `salt_chem_aqu`, `salt_chem_hru`, and `salt_chem_soil_single` call it before they form adjusted equilibrium constants such as `K_ADJ1` through `K_ADJ5`; those later constants drive the precipitation/dissolution and complexation calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set constants | Load fixed ion-charge values into `CharBal`, ion-size values into `a_size`, initialize the loop index, and set the temperature constants `A` and `B` used by the activity-coefficient formula. |
| 2. low-strength branch | If `I_Prep_in` is very small, compute each of the seven `LAMDA` values with the low-ionic-strength expression that includes the ion-size correction term. |
| 3. cap very high input | If `I_Prep_in` is 5 or greater, replace it with 0.5 and compute the seven coefficients with the alternate high-strength expression. |
| 4. normal-strength branch | For intermediate `I_Prep_in` values, compute the same alternate expression used in the high-strength branch without changing the input first. |
| 5. return | Return to the caller after the shared `LAMDA` array has been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:salt_data_module] | `LAMDA` |  |
| [sym:organic_mineral_mass_module] | `none resolved` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `LAMDA(ii)` | When `I_Prep_in.LE.1e-1`, `I_Prep_in.GE.5`, or the value falls in the middle range handled by the `else` branch. | `LAMDA(1:7)` is overwritten with new activity coefficients based on the current ionic-strength input. The values change because later salt-equilibrium calculations need updated coefficients for the current chemistry state. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows two behavior-changing edits for this routine. Commit 39fabde converted local declarations to explicit initialized forms, but did not change the coefficient formulas. Commit 2ee1889 changed the routine ending to a named `end subroutine activity_coefficient`; the coefficient logic itself remained the same.

- 39fabde initialized local variables in `salt_chem_hru.f90`, including the `activity_coefficient` locals, but left the activity-coefficient calculations unchanged.
- 2ee1889 changed the terminator to `end subroutine activity_coefficient`; this was a cleanup edit and did not alter the computed `LAMDA` values.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'activity_coefficient' documentation is very short.
- algorithm_steps revised: collapsed the three branch-specific loops into one step per branch and removed the separate loop step for the repeated `do ii = 1,7` body.
- The imported `organic_mineral_mass_module` appears in the use list, but no referenced symbols from it were visible in the extracted lines.
