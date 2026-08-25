---
kind: procedure
symbol: mgco3
title: mgco3
status: filled
source_hash: 10da13f980939585
version_label: SWAT+ 62.0.0
locals:
  m1: Current solid MgCO3 amount read from `Sol_MgCO3(c5)`; it is the starting solid-phase
    reservoir used to decide whether any solid remains after equilibrium adjustment.
  m2: Current dissolved magnesium concentration read from `Mg_Conc(salt_c3)`; it is one reactant
    concentration used in the solubility check and updated by precipitation or dissolution.
  m3: Current dissolved carbonate concentration read from `Car_Conc(c22+1)`; it is the other
    reactant concentration used in the solubility check and updated by precipitation or dissolution.
  ksp: The MgCO3 solubility product threshold, taken from `salt_K2`, that defines the equilibrium
    limit for dissolved Mg and carbonate.
  solv: The equilibrium dissolved amount implied by the quadratic solubility expression; it
    is used to estimate how much solid can precipitate or dissolve.
  trial_ksp: The current ion-product `M2*M3`; it is compared to `Ksp` to decide whether the
    system is supersaturated and should precipitate.
  possolv: A nonnegative working copy of `Solv` used as the amount to transfer between solid
    and dissolved phases during precipitation or dissolution.
  mgcar_prep: The amount of MgCO3 that precipitates when the ion product exceeds the solubility
    product; it is added to the solid pool and subtracted from dissolved ions.
  solid_mgco3: The updated solid MgCO3 amount after the equilibrium adjustment; it becomes
    the new stored solid-phase state.
  dissolved_solid: The amount of solid MgCO3 dissolved in this step; it records how much solid
    phase was consumed to restore equilibrium.
  mag_conc: The updated dissolved magnesium concentration after precipitation or dissolution;
    it replaces the old Mg concentration for the next chemistry pass.
  carbonate_conc: The updated dissolved carbonate concentration after precipitation or dissolution;
    it replaces the old carbonate concentration for the next chemistry pass.
uses:
  organic_mineral_mass_module: This module is imported by `MgCO3`, but the extracted source
    snippet does not show any explicit symbols from it being referenced inside the routine.
    The module therefore appears to be a shared dependency of the salt chemistry file rather
    than a directly used state source in this subroutine.
  salt_data_module: '`salt_data_module` supplies the concentration arrays, index offsets,
    and solubility constant that `MgCO3` reads and writes. Without `Sol_MgCO3`, `Mg_Conc`,
    `Car_Conc`, `c5`, `salt_c3`, `c22`, and `salt_K2`, the routine could not locate the correct
    storage slots or evaluate MgCO3 equilibrium.'
---

<!-- facts:header -->

Solves the MgCO3 precipitation/dissolution balance for a salt compartment. It updates magnesium, carbonate, and solid magnesium carbonate concentrations to enforce the solubility condition.

## Bottom Line

`MgCO3` is the magnesium-carbonate equilibrium step used inside the salt chemistry loops. It compares the current dissolved Mg and carbonate concentrations against the MgCO3 solubility product, then either precipitates MgCO3, partially dissolves existing solid, or dissolves all solid to bring the system back toward equilibrium.

The routine has no arguments and works entirely from module state. When it finishes, it writes the updated solid and dissolved concentrations back into `Sol_MgCO3`, `Mg_Conc`, and `Car_Conc` so the calling salt-chemistry routines can continue iterating their precipitation/dissolution package.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`MgCO3` runs inside the precipitation-dissolution iteration used by `salt_chem_aqu`, `salt_chem_hru`, and `salt_chem_soil_single`. Those callers set the current compartment state and then repeatedly call the salt mineral routines until the concentration error is small; the results from `MgCO3` feed the later error check and ultimately determine the compartment’s updated solid and dissolved salt state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load the current MgCO3 state and constants. | Reads the existing solid MgCO3 amount, dissolved magnesium, dissolved carbonate, and the MgCO3 solubility product from module arrays and constants. |
| 2. Compute the equilibrium dissolved amount and trial ion product. | Solves the quadratic expression for the equilibrium dissolved amount and computes the current Mg-by-carbonate ion product used to test supersaturation. |
| 3. Precipitate MgCO3 when the ion product exceeds Ksp. | If `M2*M3` is greater than `Ksp`, the compartment is supersaturated; the routine treats the excess as precipitation, adds the precipitated amount to the solid pool, and subtracts it from dissolved Mg and carbonate. |
| 4. Dissolve part of the solid when solid remains above equilibrium. | If the ion product is not supersaturated but there is still more solid MgCO3 than the equilibrium dissolved amount, the routine dissolves part of the solid and adds that amount back to dissolved Mg and carbonate. |
| 5. Dissolve all remaining solid otherwise. | If neither precipitation nor partial dissolution applies, the routine removes all remaining solid MgCO3 and transfers that mass into dissolved Mg and carbonate. |
| 6. Store the updated concentrations and return. | Writes the updated solid MgCO3, dissolved Mg, and dissolved carbonate back to the module arrays for the next iteration and exits the subroutine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:organic_mineral_mass_module] | `use organic_mineral_mass_module` |  |
| [sym:salt_data_module] | `Sol_MgCO3, Mg_Conc, Car_Conc, c5, salt_c3, c22, salt_K2` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `Sol_MgCO3(c5+1)` | When `Trial_Ksp.GT.Ksp` at lines 528-536. | Supersaturation causes MgCO3 to precipitate, so the solid pool increases and the dissolved Mg and carbonate concentrations decrease by the precipitated amount. |
| `Mg_Conc(salt_c3+1)` | When `Trial_Ksp.GT.Ksp` or `elseif(M1.GT.Solv)` at lines 528-550. | The dissolved magnesium concentration is reduced by precipitation or increased by dissolution so the compartment moves toward MgCO3 equilibrium. |
| `Car_Conc(c22+2)` | When `Trial_Ksp.GT.Ksp` or `elseif(M1.GT.Solv)` at lines 528-550. | The dissolved carbonate concentration is reduced by precipitation or increased by dissolution so the compartment moves toward MgCO3 equilibrium. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolves to two commits. `df07e3f` introduced `salt_chem_hru.f90` and the `MgCO3` subroutine as part of the initial import. `2ee1889` changed the procedure-end statements in this file, including `MgCO3`, from bare `end` to `end subroutine MgCO3` without changing the equilibrium logic.

- df07e3f added the `MgCO3` routine in the initial source import, along with the MgCO3 equilibrium update logic and writes back to `Sol_MgCO3`, `Mg_Conc`, and `Car_Conc`.
- 2ee1889 updated the subroutine terminator for `MgCO3` to an explicit `end subroutine MgCO3`; the algorithm and state updates in the body were unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- The imported `organic_mineral_mass_module` is not shown supplying any explicit symbols inside the extracted `MgCO3` body, so its role here may be indirect or only for broader file-level availability.
- algorithm_steps revised: expanded the original three-node draft into six source-backed steps to cover state load, equilibrium calculation, each branch, and the write-back.
