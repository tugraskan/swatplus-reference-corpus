---
kind: procedure
symbol: caso4
title: caso4
status: filled
source_hash: b4865e124ed6af47
version_label: SWAT+ 62.0.0
locals:
  m1: Initial CaSO4 solid mass or amount read from Sol_CaSO4(c5) before any equilibrium adjustment.
  m2: Current dissolved calcium concentration read from Cal_Conc(c11+1) and used as the calcium
    reactant term.
  m3: Current dissolved sulfate concentration read from Sul_Conc(salt_c4) and used as the
    sulfate reactant term.
  ksp: The gypsum solubility product, taken from salt_K3, that defines the equilibrium limit
    for CaSO4.
  solv: The algebraic solution for the equilibrium solid-change term, used to estimate how
    much CaSO4 must precipitate or dissolve to reach Ksp.
  trial_ksp: The trial ion product M2*M3 used to test whether the dissolved ions are supersaturated
    relative to Ksp.
  possolv: A positive version of the solution term used as the amount to add or remove from
    the solid and dissolved pools.
  calsul_prep: Temporary precipitation amount for the supersaturated case; it is added to
    the solid pool and subtracted from calcium and sulfate concentrations.
  solid_caso4: The updated CaSO4 solid amount after precipitation or dissolution is applied.
  dissolved_solid: The amount of solid CaSO4 that dissolves in the dissolution branches.
  calcium_conc: The updated dissolved calcium concentration after the CaSO4 equilibrium adjustment.
  sulfate_conc: The updated dissolved sulfate concentration after the CaSO4 equilibrium adjustment.
uses:
  organic_mineral_mass_module: The module matters because CaSO4 is one of the mineral equilibrium
    routines that runs inside the larger constituent/mineral mass chemistry framework, even
    though this extracted subroutine segment does not reference a named symbol from that module
    directly.
  salt_data_module: salt_data_module provides the shared concentration arrays, index counters,
    and the gypsum solubility product that CaSO4 must read and update. Without that module,
    the routine would not know which array slots hold the current calcium, sulfate, and CaSO4
    state or where to store the updated values.
---

<!-- facts:header -->

Adjusts calcium and sulfate concentrations for CaSO4 equilibrium in a salt chemistry package. It updates the gypsum solid pool and the dissolved ion pools after testing for precipitation or dissolution.

## Bottom Line

CaSO4 is the gypsum equilibrium step used by the salt chemistry routines. It reads the current CaSO4 solid amount plus calcium and sulfate concentrations, compares the ion product to the solubility product, and then decides whether gypsum should precipitate, partially dissolve, or fully dissolve.

After the decision, it writes the updated solid CaSO4 amount and the adjusted dissolved calcium and sulfate concentrations back to the shared salt data arrays. Those updated arrays are then used by the caller’s precipitation-dissolution loop and by the error check that tests whether the ionic system has converged.

## Arguments

<!-- facts:arguments -->

## Where It Fits

CaSO4 runs inside the precipitation-dissolution loop of the salt chemistry routines after the caller has set the relevant index counters and current ion concentrations. It is invoked by salt_chem_aqu, salt_chem_hru, and salt_chem_soil_single before those drivers check the concentration differences for convergence, so its results directly affect whether the overall salt equilibrium iteration can stop.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load current gypsum state and equilibrium parameters. | Reads the existing CaSO4 solid amount, dissolved calcium, dissolved sulfate, and gypsum solubility product from shared module state. |
| 2. Compute the equilibrium solution and trial ion product. | Solves a quadratic form for the equilibrium change term and calculates the current calcium-sulfate ion product used for the supersaturation test. |
| 3. Check for supersaturation. | If the trial ion product exceeds Ksp, the water is supersaturated and gypsum precipitation is applied by converting a positive amount from dissolved ions into solid CaSO4. |
| 4. Check for partial dissolution. | If the system is not supersaturated but enough solid remains, the routine dissolves part of the CaSO4 solid and adds that amount back to calcium and sulfate concentrations. |
| 5. Fully dissolve remaining solid if needed. | If the available solid is smaller than the equilibrium dissolution demand, all solid CaSO4 is dissolved and the dissolved ions are increased by the full solid amount. |
| 6. Store the updated state back to shared arrays. | Writes the updated solid CaSO4 amount and the revised dissolved calcium and sulfate concentrations to the next-state slots in the shared salt arrays. |
| 7. Return to the caller. | Exits after updating the shared state so the caller can continue the equilibrium iteration and convergence checks. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` | `uses the module import only; no specific symbols from organic_mineral_mass_module are referenced in the extracted source lines` |
| [sym:salt_data_module] | `Sol_CaSO4, Cal_Conc, Sul_Conc, c5, c11, salt_c4, salt_K3` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `Sol_CaSO4(c5+1)` | When Trial_Ksp.gt.Ksp, meaning dissolved calcium and sulfate are supersaturated with respect to gypsum. | Sol_CaSO4(c5+1) is increased by the precipitation amount, because some dissolved calcium and sulfate are converted into solid CaSO4. |
| `Cal_Conc(c11+2)` | When Trial_Ksp.gt.Ksp, or when dissolution occurs in the other branches and calcium is adjusted from the solid pool. | Cal_Conc(c11+2) is overwritten with the post-equilibrium calcium concentration, either reduced by precipitation or increased by dissolution. |
| `Sul_Conc(salt_c4+1)` | When Trial_Ksp.gt.Ksp, or when dissolution occurs in the other branches and sulfate is adjusted from the solid pool. | Sul_Conc(salt_c4+1) is overwritten with the post-equilibrium sulfate concentration, either reduced by precipitation or increased by dissolution. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows one source-addition commit and one later cleanup commit affecting this routine. The initial 94b6dec import brought in the CaSO4 subroutine as part of the salt chemistry source drop, and 2ee1889 only changed the terminator style to an explicit `end subroutine CaSO4` without altering the CaSO4 logic. No resolved diff changed the actual equilibrium calculations in lines 457-500.

- 94b6dec introduced the CaSO4 subroutine into salt_chem_hru.f90 as part of the source import.
- 2ee1889 changed the procedure terminator to `end subroutine CaSO4` but left the precipitation/dissolution algorithm unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- organic_mineral_mass_module is imported but no specific symbol from it appears in the extracted CaSO4 lines; the dependency is therefore module-level rather than symbol-level in this snippet.
