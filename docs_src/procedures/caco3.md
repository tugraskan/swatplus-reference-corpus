---
kind: procedure
symbol: caco3
title: caco3
status: filled
source_hash: 57aec57981bd3318
version_label: SWAT+ 62.0.0
locals:
  m1: Current solid CaCO3 concentration read from `Sol_CaCO3(c5)`; it is the available calcium
    carbonate mass/amount in the solid phase before equilibrium adjustment.
  m2: Current calcium concentration read from `Cal_Conc(c11)`; it is one dissolved reactant
    used to test whether CaCO3 should precipitate or dissolve.
  m3: Current carbonate concentration read from `Car_Conc(c22)`; it is the other dissolved
    reactant used with calcium to determine saturation state.
  ksp: Solubility product threshold copied from `salt_K1`; it defines the equilibrium limit
    for CaCO3 in this routine.
  solv: Analytical equilibrium solution for the CaCO3 shift, computed from `M2`, `M3`, and
    `Ksp`; its sign and magnitude are used to decide how much solid should form or dissolve.
  trial_ksp: Trial ion product `M2*M3`; it checks whether the water is supersaturated relative
    to `Ksp` and therefore should precipitate CaCO3.
  possolv: A nonnegative working form of `Solv` used in the precipitation branch; it is taken
    as `abs(Solv)` so the code can compute how much solid CaCO3 should be added.
  calcar_prep: Amount of CaCO3 prepared/precipitated in the precipitation branch; it is set
    from `PosSolv` and added to the existing solid pool.
  solid_caco3: Updated solid-phase CaCO3 after the branch logic; it becomes either increased
    by precipitation, reduced by partial dissolution, or set to zero if all solid dissolves.
  dissolved_solid: Amount of solid CaCO3 dissolved during the chosen branch; it records how
    much of the solid phase was consumed in that step.
  calcium_conc: Updated dissolved calcium concentration after precipitation or dissolution;
    it is the calcium state written back to `Cal_Conc(c11+1)`.
  carbonate_conc: Updated dissolved carbonate concentration after precipitation or dissolution;
    it is the carbonate state written back to `Car_Conc(c22+1)`.
uses:
  organic_mineral_mass_module: This module is imported by the routine, so it is part of the
    broader mass-accounting context in which mineral phase changes are tracked; even though
    no resolved symbols were extracted here, the import indicates the routine participates
    in shared mass-state bookkeeping.
  salt_data_module: '`salt_data_module` provides the shared concentration arrays, indices,
    and solubility constant that CaCO3 reads and updates. Without these global states, the
    routine could not evaluate saturation or persist the new solid, calcium, and carbonate
    values for later chemistry steps.'
---

<!-- facts:header -->

Computes calcium carbonate precipitation or dissolution and updates the solid, calcium, and carbonate concentrations accordingly.

## Bottom Line

`CaCO3` is the calcium carbonate equilibrium step used inside the salt chemistry routines. It compares the current calcium and carbonate concentrations against the solubility product, then either forms solid CaCO3, dissolves part of an existing solid phase, or dissolves all available solid depending on which equilibrium branch applies.

After resolving that balance, the routine writes the updated values back into the shared salt-state arrays so later iterations and other salt-chemistry calculations can use the new solid and dissolved concentrations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the precipitation-dissolution package of the salt chemistry solvers, after upstream code has set the relevant calcium, carbonate, solid CaCO3, and solubility-product state in `salt_data_module`. It is called from `salt_chem_aqu`, `salt_chem_hru`, and `salt_chem_soil_single` during their iterative equilibrium loop, and its updated arrays feed the later error checks and downstream salt-mineral balance updates in those routines.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read current state and equilibrium constant. | The routine loads the present solid CaCO3, dissolved calcium, and dissolved carbonate values from shared arrays, then copies the CaCO3 solubility constant from `salt_K1` and computes the trial ion product and analytical equilibrium shift (`Solv`). |
| 2. Test for supersaturation. | If the trial ion product exceeds the solubility product, the water is supersaturated with respect to CaCO3 and the routine follows the precipitation branch. |
| 3. Add precipitated CaCO3. | The code uses the positive equilibrium shift to compute how much CaCO3 precipitates, increases the solid pool by that amount, and subtracts the same amount from dissolved calcium and carbonate. |
| 4. Test for partial dissolution. | If the system is not supersaturated but the existing solid CaCO3 exceeds the equilibrium amount, the routine takes the partial-dissolution branch. |
| 5. Dissolve part of the solid phase. | The routine applies the equilibrium shift as dissolved mass, raises dissolved calcium and carbonate, and reduces the solid CaCO3 by the dissolved amount. |
| 6. Dissolve all remaining solid when needed. | If neither precipitation nor partial dissolution applies, the routine removes all solid CaCO3 and transfers that amount into dissolved calcium and carbonate. |
| 7. Write updated concentrations back to shared state. | The final solid CaCO3, calcium, and carbonate concentrations are stored back into `Sol_CaCO3(c5+1)`, `Cal_Conc(c11+1)`, and `Car_Conc(c22+1)` for later iterations and callers. |
| 8. Return to caller. | The routine ends after updating the shared salt arrays; no further local processing occurs. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` | `No specific symbols were resolved from this module in the provided evidence.` |
| [sym:salt_data_module] | `Sol_CaCO3, Cal_Conc, Car_Conc, c5, c11, c22, salt_K1` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `Sol_CaCO3(c5+1)` | When `Trial_Ksp > Ksp` at line 720, meaning the solution is supersaturated with respect to CaCO3. | `Sol_CaCO3(c5+1)` is increased by the precipitated amount in the precipitation branch, so the shared solid-phase CaCO3 state reflects newly formed mineral. |
| `Cal_Conc(c11+1)` | When `Trial_Ksp <= Ksp` and the existing solid pool is large enough for the partial-dissolution branch (`M1 > Solv`). | `Cal_Conc(c11+1)` is updated to the new dissolved calcium level after part of the CaCO3 solid dissolves into solution. |
| `Car_Conc(c22+1)` | When neither the precipitation branch nor the partial-dissolution branch applies, so all remaining solid CaCO3 is dissolved. | `Car_Conc(c22+1)` is updated to the carbonate concentration after full dissolution of the available solid CaCO3. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in the initial `df07e3f` import of `salt_chem_hru.f90` with the CaCO3 equilibrium logic already present. The later resolved lineage commit `2ee1889` only changed the subroutine termination style for `CaCO3` from a bare `end` to `end subroutine CaCO3`; the body of the algorithm was unchanged in the diff evidence provided.

- `df07e3f` added the `CaCO3` subroutine and its precipitation/dissolution branch logic in the initial source import.
- `2ee1889` made a source-level cleanup by replacing the bare terminator with `end subroutine CaCO3` without changing the routine's behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- algorithm_steps revised: expanded the draft into eight source-backed steps to reflect the full precipitation/dissolution branch logic and the final state write-back.
- Source evidence for `organic_mineral_mass_module` did not resolve any specific imported symbols in the provided packet; its relevance is inferred from the import statement only.
- The lineage evidence resolved two commits; only the diff in `2ee1889` changed `CaCO3` directly, and that change was terminator syntax only.
