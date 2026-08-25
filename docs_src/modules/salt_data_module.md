---
kind: module
symbol: salt_data_module
title: salt_data_module
status: filled
source_hash: 16fec08e0a30211a
version_label: SWAT+ 62.0.0
variables:
  salt_tol_sim: integer flag read from `salt_plants` that turns salt stress on for plant growth;
    consumed by `pl_waterup` and `pl_biomass_gro`.
  salt_soil_type: integer selector read from `salt_plants` for the salinity response soil
    type, where 1 indicates CaSO4 soils and 2 indicates NaCl soils; used by `pl_waterup`.
  salt_effect: integer method selector read from `salt_plants` that controls whether salt
    stress is applied after other stresses or combined with them by taking the minimum; used
    by `pl_biomass_gro`.
  salt_tds_ec: real TDS-to-electrical-conductivity conversion factor read from `salt_plants`;
    used by `pl_waterup` when converting saturated paste TDS to ECe.
  salt_stress_a: allocatable real array of per-plant salinity threshold parameters read from
    `salt_plants`; used by `pl_waterup` and downstream plant-salt growth calculations.
  salt_stress_b: allocatable real array of per-plant salinity slope parameters read from `salt_plants`;
    used by `pl_waterup` and downstream plant-salt growth calculations.
  sul_conc: double precision working array for dissolved sulfate concentration in the salt-chemistry
    solves. It is shared across aquifer, HRU soil-layer, and soil-single chemistry routines,
    which read and rewrite the layer or compartment slot they are solving.
  cal_conc: double precision working array for dissolved calcium concentration in the salt-chemistry
    solves. It is shared across aquifer, HRU soil-layer, and soil-single chemistry routines,
    which read and rewrite the active slot while enforcing equilibrium.
  mg_conc: double precision working array for dissolved magnesium concentration in the salt-chemistry
    solves. It is updated by the mineral equilibrium routines and read by aquifer, HRU, and
    single-layer chemistry calculations.
  sod_conc: double precision working array for dissolved sodium concentration in the salt-chemistry
    solves. It is used by aquifer, HRU, and cation-exchange calculations.
  pot_conc: double precision working array for dissolved potassium concentration in the salt-chemistry
    solves. It is used by aquifer, HRU, and cation-exchange calculations.
  cl_conc: double precision working array for dissolved chloride concentration in the salt-chemistry
    solves. It is used by aquifer, HRU, and cation-exchange calculations.
  car_conc: double precision working array for dissolved carbonate concentration in the salt-chemistry
    solves. It is updated by carbonate mineral equilibrium routines in aquifer and HRU chemistry.
  bicar_conc: double precision working array for dissolved bicarbonate concentration in the
    salt-chemistry solves. It is used in the ionic-strength and equilibrium chemistry workflow.
  c11: integer index or offset used by the salt-equilibrium routines to address concentration-array
    slots during mineral updates. It is shared state for the chemistry solvers.
  c22: integer index or offset used by the salt-equilibrium routines to address concentration-array
    slots during mineral updates. It is shared state for the chemistry solvers.
  salt_c3: integer index or offset used by the salt-equilibrium routines to address concentration-array
    slots during mineral updates. It is shared state for the chemistry solvers.
  salt_c4: integer index or offset used by the salt-equilibrium routines to address concentration-array
    slots during mineral updates. It is shared state for the chemistry solvers.
  c5: integer index or offset used by the salt-equilibrium routines to address concentration-array
    slots during mineral updates. It is shared state for the chemistry solvers.
  salt_k1: double precision solubility product or equilibrium constant used by the CaCO3 equilibrium
    routine.
  salt_k2: double precision solubility product or equilibrium constant used by the MgCO3 equilibrium
    routine.
  salt_k3: double precision solubility product or equilibrium constant used by the CaSO4 equilibrium
    routine.
  salt_k4: double precision solubility product or equilibrium constant used by the MgSO4 equilibrium
    routine.
  salt_k5: double precision solubility product or equilibrium constant used by the NaCl equilibrium
    routine.
  ksp11: double precision solubility product for a soil-profile salt mineral case; the source
    comment labels these as soil profile solubility products.
  ksp21: double precision soil-profile solubility product constant used by the salt-chemistry
    package.
  ksp31: double precision soil-profile solubility product constant used by the salt-chemistry
    package.
  ksp41: double precision soil-profile solubility product constant used by the salt-chemistry
    package.
  ksp51: double precision soil-profile solubility product constant used by the salt-chemistry
    package.
  ksp12: double precision solubility product for an aquifer salt mineral case; the source
    comment labels these as aquifer solubility products.
  ksp22: double precision aquifer solubility product constant used by the salt-chemistry package.
  ksp32: double precision aquifer solubility product constant used by the salt-chemistry package.
  ksp42: double precision aquifer solubility product constant used by the salt-chemistry package.
  ksp52: double precision aquifer solubility product constant used by the salt-chemistry package.
  upion1: double precision shared ion concentration slot used by the aquifer salt chemistry
    solve.
  upion2: double precision shared ion concentration slot used by the aquifer salt chemistry
    solve and cation exchange; completed overlays show it carries exchange-adjusted calcium
    back to callers.
  upion3: double precision shared ion concentration slot used by the aquifer salt chemistry
    solve and cation exchange; completed overlays show it carries exchange-adjusted magnesium
    back to callers.
  upion4: double precision shared ion concentration slot used by the aquifer salt chemistry
    solve and cation exchange; completed overlays show it carries exchange-adjusted sodium
    back to callers.
  upion5: double precision shared ion concentration slot used by the aquifer salt chemistry
    solve and cation exchange; completed overlays show it carries exchange-adjusted potassium
    back to callers.
  upion6: double precision shared ion concentration slot used by the aquifer salt chemistry
    solve.
  upion7: double precision shared ion concentration slot used by the aquifer salt chemistry
    solve.
  upion8: double precision shared ion concentration slot used by the aquifer salt chemistry
    solve.
  sol_caco3: double precision working and storage array for CaCO3 solid concentration. It
    is read and rewritten by the aquifer and HRU equilibrium routines and by the single-layer
    soil chemistry solver.
  sol_mgco3: double precision working and storage array for MgCO3 solid concentration. It
    is read and rewritten by the aquifer and HRU equilibrium routines and by the single-layer
    soil chemistry solver.
  sol_caso4: double precision working and storage array for CaSO4 solid concentration. It
    is read and rewritten by the aquifer and HRU equilibrium routines and by the single-layer
    soil chemistry solver.
  sol_mgso4: double precision working and storage array for MgSO4 solid concentration. It
    is read and rewritten by the aquifer and HRU equilibrium routines and by the single-layer
    soil chemistry solver.
  sol_nacl: double precision working and storage array for NaCl solid concentration. It is
    read and rewritten by the aquifer and HRU equilibrium routines and by the single-layer
    soil chemistry solver.
  lamda: double precision array of seven activity coefficients filled by `activity_coefficient`
    and then reused by the salt-equilibrium routines to adjust equilibrium constants.
  soil_salt_conc: real array of eight salt-ion concentrations used as a scratch/work array
    for plant-water salinity calculations and, in the single-layer chemistry routine, as the
    current soil-water ion concentration set.
---

<!-- facts:header -->

salt_data_module owns the shared salinity-control parameters, ion concentration work arrays, mineral solubility products, activity-coefficient storage, and per-plant salinity stress tables used by the SWAT+ salt plant-growth and salt-chemistry routines. It is a declaration-and-state module: `salt_plant_read` populates the plant-growth settings from the `salt_plants` input file, while the chemistry and plant-water routines read and update the exported arrays and constants during later calculations.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a shared declaration container. Most state is initialized here by default values or array allocation at declaration time, and `salt_plant_read` later populates the plant-salinity control variables and allocates the per-plant stress arrays from the `salt_plants` file. The chemistry routines then read, overwrite, and pass these module variables through their equilibrium calculations.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:salt_plant_read] | `salt_plants` | `salt_tds_ec, salt_tol_sim, salt_soil_type, salt_effect, salt_stress_a, salt_stress_b` | Reads the salt-plants file, loads the TDS-to-EC conversion factor and salt-growth control flags, then allocates and fills the per-plant salinity threshold and slope arrays. |

## Key Consumers

The main consumers split into two roles: plant-growth routines that apply salinity stress, and salt-chemistry routines that maintain equilibrium among dissolved ions and solid salt minerals in aquifers and soil layers. The chemistry side also includes the activity-coefficient step and cation exchange support.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:pl_biomass_gro] | salt_effect | Chooses whether salt stress is applied after the other biomass-growth stress factors or folded into the minimum stress reduction. |
| [sym:pl_waterup] | salt_data_module | Uses the shared salinity controls and ion scratch array to convert layer salt concentrations into plant salinity stress and daily uptake reduction. |
| [sym:salt_chem_aqu] | salt_data_module | Uses the shared ion concentrations, solid mineral pools, solubility products, activity coefficients, and exchange-state slots to update aquifer salt chemistry. |
| [sym:salt_chem_hru] | salt_data_module | Uses the shared ion concentrations, solid mineral pools, solubility products, activity coefficients, and exchange-state slots to update HRU soil-layer salt chemistry. |
| [sym:Ionic_Strength] | salt_data_module | Computes ionic strength from the current salt-chemistry state; the module is a declared dependency for the surrounding chemistry file, though no specific symbol reference from this module was resolved in the extracted body. |
| [sym:activity_coefficient] | salt_data_module | Writes updated activity coefficients into the shared `LAMDA` array for later equilibrium-constant adjustments. |
| [sym:CaSO4] | salt_data_module | Reads and updates the shared CaSO4, calcium, and sulfate state while enforcing gypsum equilibrium in the salt chemistry loop. |
| [sym:MgCO3] | salt_data_module | Reads and updates the shared MgCO3, magnesium, and carbonate state while enforcing magnesium-carbonate equilibrium. |
| [sym:NaCl] | salt_data_module | Reads and updates the shared NaCl, sodium, and chloride state while enforcing sodium-chloride equilibrium. |
| [sym:MgSO4] | salt_data_module | Reads and updates the shared MgSO4, magnesium, and sulfate state while enforcing magnesium-sulfate equilibrium. |
| [sym:CaCO3] | salt_data_module | Reads and updates the shared CaCO3, calcium, and carbonate state while enforcing calcium-carbonate equilibrium. |
| [sym:cationexchange] | salt_data_module | Reads and overwrites the shared `upion2` through `upion5` solution concentrations with cation-exchange adjusted values. |
| [sym:salt_chem_soil_single] | salt_data_module | Uses the shared ion arrays, mineral pools, equilibrium constants, and activity coefficients to update one soil layer’s salt chemistry. |
| [sym:salt_plant_read] | salt_data_module | Populates the shared salt-growth control variables and per-plant salinity response arrays from the `salt_plants` file. |

## Lineage

`salt_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `salt_data_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `salt_data_module` has no extracted module-level documentation comment.
- No derived types were extracted for this module.
- Some chemistry consumers are declared dependencies of surrounding files; where the extracted snippet did not resolve a specific symbol reference, the effect text notes that uncertainty rather than inventing a direct use.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
