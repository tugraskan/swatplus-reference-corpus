---
kind: procedure
symbol: nacl
title: nacl
status: filled
source_hash: 07fa565145f3326d
version_label: SWAT+ 62.0.0
locals:
  m1: Current solid NaCl mass or amount at the active salt-state index, read from `Sol_NaCl(c5)`
    before equilibrium is recalculated.
  m2: Current dissolved sodium concentration at `Sod_Conc(c5)`, used as one of the two ion
    pools that determines whether NaCl precipitates or dissolves.
  m3: Current dissolved chloride concentration at `Cl_Conc(c5)`, paired with `M2` to test
    the NaCl solubility product.
  ksp: The NaCl solubility-product threshold taken from `salt_K5`; it defines the equilibrium
    limit for the sodium-chloride pair.
  solv: The solved equilibrium amount implied by the quadratic expression, used to estimate
    how much solid should be present or how much can dissolve.
  trial_ksp: The current ion product `M2*M3`, used to test whether the solution is oversaturated
    and should precipitate NaCl.
  possolv: A nonnegative working value derived from `Solv` for the precipitation or dissolution
    amount applied in the branch logic.
  sodiumchloride_prep: Temporary precipitation amount assigned when the ion product exceeds
    `Ksp`; it is added to the solid pool and removed from the dissolved ions.
  solid_nacl: The updated solid NaCl amount that remains after the branch logic finishes for
    this call.
  dissolved_solid: The amount of NaCl that dissolved during this call; it is set to zero in
    precipitation cases and to the dissolved amount in dissolution cases.
  sodium_conc: The updated dissolved sodium concentration after precipitation or dissolution
    is applied.
  chloride_conc: The updated dissolved chloride concentration after precipitation or dissolution
    is applied.
uses:
  organic_mineral_mass_module: This module is imported by the subroutine, but the extracted
    source snippet does not show any specific symbols from it being referenced. The import
    matters because the routine participates in the broader chemistry package, yet the visible
    NaCl logic itself only uses the salt-state arrays and constants from `salt_data_module`.
  salt_data_module: This module supplies the global salt concentrations, the state index `c5`,
    and the NaCl solubility constant `salt_K5` that drive the equilibrium calculation. The
    routine both reads and writes these shared arrays, so it depends on the module for its
    inputs and for publishing updated results.
---

<!-- facts:header -->

Computes sodium chloride equilibrium in the salt chemistry loop. It updates the dissolved sodium and chloride concentrations and the remaining solid NaCl for the current storage index.

## Bottom Line

NaCl evaluates whether the current sodium and chloride pool is above the NaCl solubility limit and then partitions mass between solid NaCl and dissolved ions. It is one of the precipitation-dissolution substeps that the salt chemistry routines repeat until the ion-system error is small.

The routine reads the current salt-state arrays at index `c5` and writes the updated equilibrium result to `c5+1`. Those updated values are then used by the caller to continue the convergence loop and to compute the remaining salt-error terms.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the precipitation-dissolution loop that the caller sets up after initializing `errorTotal` and `iter_count`. The upstream routines `salt_chem_aqu`, `salt_chem_hru`, and `salt_chem_soil_single` call it repeatedly while they converge the salt equilibrium, and its updated `Sol_NaCl`, `Sod_Conc`, and `Cl_Conc` values feed the error checks that determine when the loop can stop.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read the current NaCl state and solubility limit. | The routine loads solid NaCl, dissolved sodium, dissolved chloride, and the NaCl solubility-product constant from the shared salt arrays and `salt_K5`. These values form the starting point for the equilibrium test. |
| 2. Compute the equilibrium solution and current ion product. | It solves the quadratic form for the NaCl equilibrium amount in `Solv` and computes `Trial_Ksp = M2*M3` to see whether the dissolved ions exceed the solubility product. |
| 3. Precipitate NaCl when the ion product is too high. | If `Trial_Ksp.GT.Ksp`, the solution is oversaturated and the routine treats NaCl as precipitating. It uses the absolute value of `Solv` as the precipitation amount, adds that amount to the solid pool, and subtracts it from the dissolved sodium and chloride concentrations. |
| 4. Dissolve part of the solid when solid remains above equilibrium. | If the ion product does not exceed `Ksp` but there is more solid NaCl than the equilibrium amount, the routine dissolves only part of the solid. It adds the dissolved amount back to sodium and chloride, stores the dissolved mass, and reduces the solid pool accordingly. |
| 5. Dissolve all remaining solid when equilibrium allows it. | If neither oversaturation nor residual solid demand a partial adjustment, the routine dissolves all remaining solid NaCl. Sodium and chloride are increased by the full solid amount and the solid pool is set to zero. |
| 6. Publish the updated state and return. | The routine writes the updated solid NaCl, sodium concentration, and chloride concentration into the next storage slot at `c5+1`, then returns to the caller. The caller uses those updated values in the convergence loop. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` | `[]` |
| [sym:salt_data_module] | `Sol_NaCl, Sod_Conc, Cl_Conc, c5, salt_K5` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `Sol_NaCl(c5+1)` | When `Trial_Ksp.GT.Ksp` is true, meaning the dissolved sodium-chloride ion product exceeds the NaCl solubility product. | The routine treats the mixture as oversaturated and increases the solid NaCl pool while reducing the dissolved ion concentrations by the precipitation amount. |
| `Sod_Conc(c5+1)` | When `Trial_Ksp.GT.Ksp` is false and `M1.GT.Solv` is true, meaning some solid NaCl remains available to dissolve but the system is not oversaturated. | The routine increases or restores dissolved sodium according to the dissolved amount and lowers the solid NaCl pool by that amount. |
| `Cl_Conc(c5+1)` | When neither the precipitation branch nor the partial-dissolution branch applies, so the routine takes the final `else` path. | The routine dissolves all remaining solid NaCl and updates the dissolved ion pools to reflect the full mass transfer from solid to solution. |

## File I/O

<!-- facts:io -->


## Lineage

The source lineage resolved two commits for `NaCl`. The initial addition in `df07e3f` introduced the subroutine and its equilibrium logic. The later `2ee1889` cleanup changed only routine-ending syntax in the surrounding file (`end` to `end subroutine`), with no evidence in the diff that the NaCl algorithm itself changed.

- df07e3f added the `NaCl` subroutine with the precipitation/dissolution equilibrium branches, shared-array reads, and writes to `Sol_NaCl(c5+1)`, `Sod_Conc(c5+1)`, and `Cl_Conc(c5+1)`.
- 2ee1889 made cleanup-only edits to subroutine terminators in `salt_chem_hru.f90`; the diff does not show any behavioral change to `NaCl`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- algorithm_steps revised: expanded the draft from 3 coarse nodes to 6 source-backed steps to cover the read/compute/branch/store flow visible in lines 585-632.
- The source snippet contains a likely typo in the partial-dissolution branch: `PoSSolv` appears at line 611, but the local variable declared is `PosSolv`. This page describes the intended behavior from the visible control flow and surrounding assignments.
