---
kind: procedure
symbol: mgso4
title: mgso4
status: filled
source_hash: e25f0a1ad4a8e3b6
version_label: SWAT+ 62.0.0
locals:
  m1: Current stored solid MgSO4 amount pulled from Sol_MgSO4(c5) and used as the starting
    solid phase for this update.
  m2: Current magnesium concentration in solution from Mg_Conc(salt_c3+1).
  m3: Current sulfate concentration in solution from Sul_Conc(salt_c4+1).
  ksp: The MgSO4 solubility product used as the equilibrium threshold, taken from salt_K4.
  solv: The solved equilibrium adjustment from the quadratic expression; it represents the
    amount the system would need to shift to satisfy the solubility relation.
  trial_ksp: The trial product M2*M3 used to test whether the current dissolved state exceeds
    the solubility product.
  possolv: A nonnegative adjustment magnitude derived from Solv and reused as the amount to
    precipitate or dissolve.
  mgsul_prep: The amount of MgSO4 precipitation computed when the dissolved ions are supersaturated.
  solid_mgso4: The updated solid MgSO4 mass after precipitation or dissolution is applied.
  dissolved_solid: The amount of solid MgSO4 that dissolved during the current update.
  mag_conc: The updated dissolved magnesium concentration after equilibrium adjustment.
  sulfate_conc: The updated dissolved sulfate concentration after equilibrium adjustment.
uses:
  organic_mineral_mass_module: This module matters because MgSO4 participates in the model's
    mass-balance chemistry. Even though the extracted lines only show the use statement, the
    routine belongs to the shared chemistry/mass accounting context that tracks solid and
    dissolved pools.
  salt_data_module: salt_data_module supplies the shared salt-state arrays and indices that
    MgSO4 reads and writes. The routine depends on Sol_MgSO4, Mg_Conc, Sul_Conc, c5, salt_c3,
    salt_c4, and salt_K4 to pull the current state, evaluate equilibrium, and store the updated
    concentrations back for later chemistry checks.
---

<!-- facts:header -->

Adjusts magnesium sulfate partitioning between dissolved Mg/SO4 and solid MgSO4. It enforces equilibrium/solubility behavior for the current salt state before later error checks continue the iterative chemistry solve.

## Bottom Line

MgSO4 is the magnesium-sulfate precipitation/dissolution step used inside the salt chemistry iteration. It reads the current Mg and sulfate solution concentrations plus the stored solid MgSO4 amount, compares them to the salt solubility product, and then updates the dissolved ion concentrations and remaining solid mass to keep the system consistent.

The routine matters because the caller loop uses these updated values to test convergence for the precipitation-dissolution package. In the aquifer, HRU, and single-soil workflows, this is one of the equilibrium updates that must settle before the model can move on to later salt behavior.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the precipitation-dissolution package inside salt_chem_aqu, salt_chem_hru, and salt_chem_soil_single, after those callers have entered the iterative loop and set the error accumulator. The upstream caller prepares the current salt-state concentrations, and the updated MgSO4, Mg, and sulfate values feed the caller's convergence check and the rest of the salt equilibrium sequence.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load current solid and dissolved state | Read the current solid MgSO4 amount, dissolved magnesium, dissolved sulfate, and the MgSO4 solubility product from shared module state. |
| 2. compute equilibrium adjustment | Solve the quadratic form for the equilibrium adjustment and form a trial product M2*M3 for the supersaturation test. |
| 3. precipitate if supersaturated | If the trial ionic product is greater than Ksp, treat the water as supersaturated: use the absolute equilibrium adjustment as a precipitation amount, add that mass to solid MgSO4, and reduce dissolved Mg and sulfate by the same amount. |
| 4. dissolve partially if solid remains above equilibrium | If the dissolved product is not supersaturated but solid MgSO4 still exceeds the equilibrium amount, dissolve part of the solid and add that amount back to dissolved magnesium and sulfate. |
| 5. fully dissolve remaining solid | Otherwise, dissolve all remaining solid MgSO4 and add its mass to both dissolved ions. |
| 6. store updated concentrations | Write the updated solid MgSO4, dissolved magnesium, and dissolved sulfate values back into the shared arrays for later chemistry checks. |
| 7. return to caller | Finish the subroutine and hand the updated state back to the caller's iterative precipitation-dissolution loop. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module is used for the MgSO4 subroutine's access to the broader mass/state framework that owns mineral or constituent inventories referenced by the chemistry solve.` | `module use only; no individual symbols from organic_mineral_mass_module are referenced in the extracted source lines` |
| [sym:salt_data_module] | `Sol_MgSO4, Mg_Conc, Sul_Conc, c5, salt_c3, salt_c4, salt_K4` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `Sol_MgSO4(c5+1)` | When Trial_Ksp > Ksp, meaning the dissolved Mg and sulfate product exceeds the solubility product. | The routine creates precipitated MgSO4 from solution, increases the stored solid pool, and lowers the dissolved Mg and sulfate concentrations by the precipitation amount. |
| `Mg_Conc(salt_c3+2)` | When Trial_Ksp <= Ksp and M1 > Solv, meaning some solid remains and only part of it dissolves. | The routine increases dissolved magnesium by the dissolution amount and stores the updated dissolved magnesium concentration for the next chemistry check. |
| `Sul_Conc(salt_c4+2)` | When Trial_Ksp <= Ksp and M1 <= Solv, meaning all remaining solid can dissolve. | The routine increases dissolved sulfate by the dissolution amount and stores the updated dissolved sulfate concentration for the next chemistry check. |

## File I/O

<!-- facts:io -->


## Lineage

This routine was introduced in the initial salt_chem_hru.f90 import in df07e3f. The later 2ee1889 cleanup changed the subroutine termination style from bare end statements to explicit end subroutine names, but the MgSO4 algorithm itself was not altered in the resolved diffs.

- df07e3f added MgSO4 as part of the initial salt chemistry routine set in salt_chem_hru.f90.
- 2ee1889 updated the file's subroutine endings to explicit named end subroutine statements; the MgSO4 logic and state updates remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- algorithm_steps revised: expanded the draft three-node control flow into the actual seven source-backed operations in the subroutine.
- Source lines show three different outcome branches for MgSO4, but the extracted line numbers for caller loops and state writes are sufficient to document the behavior without guessing any hidden helpers.
- organic_mineral_mass_module is used only by a USE statement in the extracted lines; no direct symbol references from that module were resolved in the packet.
