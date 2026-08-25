---
kind: procedure
symbol: salt_chem_hru
title: salt_chem_hru
status: filled
source_hash: 346a95289ae66980
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; used to select the active HRU entry and its soil/salt state.
  jj: Soil-layer loop index for the current HRU; steps through `soil(j)%nly` layers.
  m: Generic salt/species loop index used to traverse salt ions, mineral pools, and min/max
    bookkeeping arrays.
  iter_count: Iteration counter for the precipitation-dissolution convergence loop; used to
    stop runaway looping after 500 passes.
  ion1: Temporary storage for sulfate concentration in the current layer before converting
    to mol/L.
  ion2: Temporary storage for calcium concentration in the current layer before converting
    to mol/L.
  ion3: Temporary storage for magnesium concentration in the current layer before converting
    to mol/L.
  ion4: Temporary storage for sodium concentration in the current layer before converting
    to mol/L.
  ion5: Temporary storage for potassium concentration in the current layer before converting
    to mol/L.
  ion6: Temporary storage for chloride concentration in the current layer before converting
    to mol/L.
  ion7: Temporary storage for carbonate concentration in the current layer before converting
    to mol/L.
  ion8: Temporary storage for bicarbonate concentration in the current layer before converting
    to mol/L.
  hru_area_m2: HRU area converted from hectares to square meters for volume and mass conversions.
  water_volume: Current layer water volume in m3, computed from soil water depth and HRU area.
  sol_water: Soil water storage for the current layer, copied from `soil(j)%phys(jj)%st`.
  sol_thick: Soil layer thickness, copied from `soil(j)%phys(jj)%thick`.
  waterc: Layer water-content ratio used in solid-to-dissolved conversion formulas; set from
    `sol_water/sol_thick`, with a floor value when zero.
  sol_caco3_p: Percent solid CaCO3 pool for the current layer, read from `cs_soil` and later
    rewritten after chemistry.
  sol_mgco3_p: Percent solid MgCO3 pool for the current layer, read from `cs_soil` and later
    rewritten after chemistry.
  sol_caso4_p: Percent solid CaSO4 pool for the current layer, read from `cs_soil` and later
    rewritten after chemistry.
  sol_mgso4_p: Percent solid MgSO4 pool for the current layer, read from `cs_soil` and later
    rewritten after chemistry.
  sol_nacl_p: Percent solid NaCl pool for the current layer, read from `cs_soil` and later
    rewritten after chemistry.
  i_prep_in: Input ionic-strength value passed to `activity_coefficient` after `Ionic_strength`
    computes the layer value.
  i_diff: Placeholder convergence-difference flag for the chemistry loop; initialized before
    the activity-coefficient solve.
  skipediex: Counter for how many layers skipped cation exchange because one of the adjusted
    cation concentrations became nonpositive.
  soil_volume: Current layer soil volume in m3, derived from HRU area and layer thickness.
  mass_before: Accumulated dissolved salt mass in kg/ha before chemistry updates.
  mass_after: Accumulated dissolved salt mass in kg/ha after chemistry updates.
  salt_mass_kg: Temporary dissolved-salt mass for one salt species in one layer, in kg.
  soil_mass: Approximate soil mass for the current layer, in kg, used to convert percent mineral
    content to mass.
  sol_bd: Bulk density of the current soil layer, copied from `soil(j)%phys(jj)%bd`.
  mass_before_dis: Accumulated total dissolved mass before chemistry across processed layers.
  mass_before_sol: Accumulated solid-mineral mass before chemistry across processed layers.
  total_before: Accumulated total salt mass before chemistry, combining dissolved and solid
    pools.
  mass_after_dis: Accumulated total dissolved mass after chemistry across processed layers.
  mass_after_sol: Accumulated solid-mineral mass after chemistry across processed layers.
  total_after: Accumulated total salt mass after chemistry, combining updated dissolved and
    solid pools.
  ionstr: Double-precision ionic strength computed from the current layer ion concentrations.
  is_temp: Temporary double-precision output slot passed to `Ionic_Strength`.
  k_adj1: Activity-coefficient product used to adjust the CaCO3 solubility constant.
  k_adj2: Activity-coefficient product used to adjust the MgCO3 solubility constant.
  k_adj3: Activity-coefficient product used to adjust the CaSO4 solubility constant.
  k_adj4: Activity-coefficient product used to adjust the MgSO4 solubility constant.
  k_adj5: Activity-coefficient product used to adjust the NaCl solubility constant.
  error1st: Carbonate convergence error, computed from successive carbonate concentration
    slots in the precipitation loop.
  error2nd: Calcium convergence error, computed from successive calcium concentration slots
    in the precipitation loop.
  error3rd: Sulfate convergence error, computed from successive sulfate concentration slots
    in the precipitation loop.
  errortotal: Maximum absolute convergence error across carbonate, calcium, and sulfate used
    to continue or stop the precipitation-dissolution loop.
uses:
  hru_module: '`hru_module` provides the active HRU record selected by `ihru`; `salt_chem_hru`
    needs `hru(j)%area_ha` to convert between layer concentrations, layer masses, and per-area
    HRU salt balances.'
  basin_module: '`basin_module` is imported here even though no specific resolved symbol was
    extracted; that matters because this routine runs in the basin-level HRU control flow
    and may rely on basin-wide salt settings or shared simulation state defined there.'
  constituent_mass_module: '`constituent_mass_module` holds the shared salt inventory structures
    `cs_soil` and `cs_db` that this routine reads and writes. The routine uses them to iterate
    over the number of salts, read the current dissolved and mineral pools, and store the
    updated concentrations back into the layer state.'
  salt_data_module: '`salt_data_module` matters because the routine performs salt-species
    equilibrium chemistry, and the salt-species names, constants, or shared chemistry parameters
    used in that solve are expected to live in this module even though no specific reference
    was resolved in the extracted packet.'
  soil_module: '`soil_module` supplies layer count, water storage, thickness, and bulk density
    for the current HRU. Those values define the current layer volume and mass basis used
    to convert between percent mineral content, kg/ha, and mg/L.'
  salt_module: '`salt_module` provides the HRU salt balance structure `hsaltb_d`; `salt_chem_hru`
    writes `hsaltb_d(j)%salt(1)%diss` to record how much salt moved from sorbed/solid storage
    into dissolved storage during the chemistry update.'
  time_module: '`time_module` matters because this routine runs as part of the time-stepped
    HRU simulation and likely shares temporal context with other chemistry and balance routines,
    even though no explicit time variable was extracted here.'
---

<!-- facts:header -->

Balances salt chemistry in each HRU soil layer by converting between dissolved ions and solid salt minerals, then applies cation exchange. The routine updates layer concentrations and salt balance totals used by downstream SWAT+ salt accounting.

## Bottom Line

`salt_chem_hru` runs once per active HRU when salt simulation is enabled. It walks each soil layer, converts between salt mass, concentration, and mineral percentage forms, then equilibrates dissolved ions with solid salts and cation exchange so the layer’s salt chemistry stays physically consistent.

The routine matters because it updates `cs_soil` in place and records the HRU dissolved-salt mass change in `hsaltb_d(j)%salt(1)%diss`, which downstream SWAT+ routines use for later constituent accounting and HRU-level salt balance.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`salt_chem_hru` is called from `hru_control` after albedo is computed and before constituent reaction/sorption routines. `hru_control` calls it only when `cs_db%num_salts > 0`, so the upstream setup is the current HRU index, soil profile, and salt state already loaded for the day; downstream model behavior depends on the updated layer concentrations and on `hsaltb_d(j)%salt(1)%diss` for salt balance accounting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and reset mass tracking | The routine clears the cation-exchange skip counter, copies the active HRU index from `ihru`, converts the HRU area from hectares to square meters, and initializes the before/after mass accumulators before processing any soil layers. |
| 2. Initialize layer-level totals | It zeros the dissolved, solid, and total mass accumulators that will be updated across the layer loop. |
| 3. Loop through each soil layer | The routine iterates from the top layer to `soil(j)%nly`, applying the salt chemistry solve separately to each layer. |
| 4. Read layer water and solid-salt state | For the current layer it reads soil water content, thickness, and bulk density, copies the five solid salt mineral percentages into working arrays, computes layer soil volume and soil mass, and accumulates the initial solid mineral mass. |
| 5. Convert the solid minerals to working concentration form | The code forces a small nonzero water-content floor when needed and converts the five solid salt mineral percentages into solution-equivalent working concentrations for the precipitation-dissolution solve. |
| 6. Convert dissolved salts to concentration units and track initial dissolved mass | It computes the layer water volume, clamps negative dissolved salt masses and concentrations to zero, converts each dissolved salt mass to mg/L, and accumulates the pre-chemistry dissolved mass. |
| 7. Accumulate the pre-chemistry layer mass | The routine adds the dissolved mass to the layer’s pre-chemistry total so it can compare before and after salt balances later in the loop. |
| 8. Map dissolved concentrations to ion molarity | It copies the layer’s dissolved salt concentrations into ion work variables and converts sulfate, calcium, magnesium, sodium, potassium, chloride, carbonate, and bicarbonate from mg/L to mol/L. |
| 9. Compute ionic strength and prepare activity coefficients | The routine calls `Ionic_strength` with the current ion molarities, stores the result in `I_Prep_in`, sets the ionic-strength difference flag, and initializes the equilibrium-array indices used by the iterative chemistry solve. |
| 10. Call the activity-coefficient routine and form adjusted equilibrium constants | It calls `activity_coefficient` to fill `LAMDA`, combines those coefficients into five adjusted equilibrium products, and derives the mineral-specific solubility constants when the adjusted terms are positive. |
| 11. Iterate precipitation-dissolution reactions to convergence | The routine sets the error metric, loops while the maximum absolute change in carbonate, calcium, and sulfate remains above `1e-3`, and within each pass calls `CaCO3`, `MgCO3`, `CaSO4`, `MgSO4`, and `NaCl` to update the shared ion and solid pools. |
| 12. Stop the iteration if it runs too long | An iteration counter increments on each pass through the equilibrium loop; if it exceeds 500, the routine exits the loop through the labeled branch. |
| 13. Convert the updated dissolved ions back to stored concentrations and apply cation exchange | After the equilibrium loop, the routine copies the updated molar ion concentrations into the `upion` working variables, converts them to ppm-style values, calls `cationexchange`, and restores the pre-exchange calcium, magnesium, sodium, and potassium concentrations if the exchange result is invalid. |
| 14. Save the updated layer state and finish HRU mass balance | The routine writes the updated dissolved concentrations back to `cs_soil(j)%ly(jj)%saltc(1:8)`, converts dissolved concentrations back to kg/ha for `cs_soil(j)%ly(jj)%salt(1:cs_db%num_salts)`, recomputes the solid mineral percentages and clamps them to 100, accumulates post-chemistry dissolved and solid masses, and finally stores the HRU-level dissolved-vs-solid salt change in `hsaltb_d(j)%salt(1)%diss`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` | `hru(j)%area_ha` |
| [sym:basin_module] | `basin_module imported state is not resolved in the extracted refs, so the specific symbol list is uncertain.` | `No candidate outside references were resolved to `basin_module` in the context packet.` |
| [sym:constituent_mass_module] | `cs_soil, cs_db` | `cs_soil(j)%ly(jj)%salt_min(m), cs_db%num_salts, cs_soil(j)%ly(jj)%salt(m), cs_soil(j)%ly(jj)%saltc(m), cs_soil(j)%ly(jj)%saltc(1), cs_soil(j)%ly(jj)%saltc(2), cs_soil(j)%ly(jj)%saltc(3), cs_soil(j)%ly(jj)%saltc(4), cs_soil(j)%ly(jj)%saltc(5), cs_soil(j)%ly(jj)%saltc(6), cs_soil(j)%ly(jj)%saltc(7), cs_soil(j)%ly(jj)%saltc(8), cs_soil(j)%ly(jj)%salt_min(1), cs_soil(j)%ly(jj)%salt_min(2), cs_soil(j)%ly(jj)%salt_min(3), cs_soil(j)%ly(jj)%salt_min(4), cs_soil(j)%ly(jj)%salt_min(5)` |
| [sym:salt_data_module] | `salt_data_module imported state is not resolved in the extracted refs, so the specific symbol list is uncertain.` | `No candidate outside references were resolved to `salt_data_module` in the context packet.` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(jj)%st, soil(j)%phys(jj)%thick, soil(j)%phys(jj)%bd` |
| [sym:salt_data_module] | `salt_data_module imported state is not resolved in the extracted refs, so the specific symbol list is uncertain.` | `No candidate outside references were resolved to `salt_data_module` in the context packet.` |
| [sym:salt_module] | `hsaltb_d` | `hsaltb_d(j)%salt(1)%diss` |
| [sym:time_module] | `time_module imported state is not resolved in the extracted refs, so the specific symbol list is uncertain.` | `No candidate outside references were resolved to `time_module` in the context packet.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `Sol_CaCO3(1)` | After each layer’s initial solid-mineral read, before the equilibrium loop | Loaded from `cs_soil(j)%ly(jj)%salt_min(1)` as the current layer’s solid calcium carbonate percentage-equivalent, then later overwritten with the updated post-chemistry value. |
| `Sol_MgCO3(1)` | After each layer’s initial solid-mineral read, before the equilibrium loop | Loaded from `cs_soil(j)%ly(jj)%salt_min(2)` as the current layer’s solid magnesium carbonate percentage-equivalent, then later overwritten with the updated post-chemistry value. |
| `Sol_CaSO4(1)` | After each layer’s initial solid-mineral read, before the equilibrium loop | Loaded from `cs_soil(j)%ly(jj)%salt_min(3)` as the current layer’s solid calcium sulfate percentage-equivalent, then later overwritten with the updated post-chemistry value. |
| `Sol_MgSO4(1)` | After each layer’s initial solid-mineral read, before the equilibrium loop | Loaded from `cs_soil(j)%ly(jj)%salt_min(4)` as the current layer’s solid magnesium sulfate percentage-equivalent, then later overwritten with the updated post-chemistry value. |
| `Sol_NaCl(1)` | After each layer’s initial solid-mineral read, before the equilibrium loop | Loaded from `cs_soil(j)%ly(jj)%salt_min(5)` as the current layer’s solid sodium chloride percentage-equivalent, then later overwritten with the updated post-chemistry value. |
| `cs_soil(j)%ly(jj)%salt(m)` | When dissolved salt mass is nonnegative and water volume is available | Negative dissolved salt masses are reset to zero, then the dissolved salt concentration is converted from kg/ha to mg/L and written back into the layer’s dissolved salt storage. |
| `cs_soil(j)%ly(jj)%saltc(m)` | When dissolved salt mass is nonnegative and water volume is available | Any negative concentration is reset to zero, then the layer’s dissolved salt concentration array is overwritten with the current mg/L values derived from dissolved mass and water volume. |
| `Sul_Conc(1)` | After converting updated ions to concentration units | Holds the current dissolved sulfate concentration in mol/L for the precipitation-dissolution solve, then is updated by the mineral routines during iteration. |
| `Cal_Conc(1)` | After converting updated ions to concentration units | Holds the current dissolved calcium concentration in mol/L for the precipitation-dissolution solve, then is updated by the mineral routines during iteration. |
| `Mg_Conc(1)` | After converting updated ions to concentration units | Holds the current dissolved magnesium concentration in mol/L for the precipitation-dissolution solve, then is updated by the mineral routines during iteration. |
| `Sod_Conc(1)` | After converting updated ions to concentration units | Holds the current dissolved sodium concentration in mol/L and later becomes part of the exchange-adjusted solution state. |
| `Pot_Conc(1)` | After converting updated ions to concentration units | Holds the current dissolved potassium concentration in mol/L and later becomes part of the exchange-adjusted solution state. |
| `Cl_Conc(1)` | After converting updated ions to concentration units | Holds the current dissolved chloride concentration in mol/L and later becomes part of the post-chemistry solution state. |
| `Car_Conc(1)` | After converting updated ions to concentration units | Holds the current dissolved carbonate concentration in mol/L for the equilibrium solve, and is updated by the mineral calls until convergence. |
| `BiCar_Conc(1)` | After converting updated ions to concentration units | Holds the current dissolved bicarbonate concentration in mol/L for the equilibrium solve and remains part of the shared ion state. |
| `c11` | Before and during the precipitation-dissolution loop | Acts as the calcium concentration-slot index used by the mineral routines and the caller-side error checks; it advances by 2 each iteration to track successive values. |
| `c22` | Before and during the precipitation-dissolution loop | Acts as the carbonate concentration-slot index used by the mineral routines and the caller-side error checks; it advances by 2 each iteration to track successive values. |
| `salt_c3` | Before and during the precipitation-dissolution loop | Acts as the magnesium concentration-slot index used by the mineral routines and the caller-side error checks; it advances by 2 each iteration to track successive values. |
| `salt_c4` | Before and during the precipitation-dissolution loop | Acts as the sulfate concentration-slot index used by the mineral routines and the caller-side error checks; it advances by 2 each iteration to track successive values. |
| `c5` | Before and during the precipitation-dissolution loop | Acts as the solid/mineral storage index used to access the current and next salt-mineral values; it increments by 1 each iteration. |
| `salt_K1` | After activity-coefficient adjustment | Stores the adjusted CaCO3 equilibrium constant for the current layer when the activity product is positive; otherwise it is reset to zero. |
| `salt_K2` | After activity-coefficient adjustment | Stores the adjusted MgCO3 equilibrium constant for the current layer when the activity product is positive; otherwise it is reset to zero. |
| `salt_K3` | After activity-coefficient adjustment | Stores the adjusted CaSO4 equilibrium constant for the current layer when the activity product is positive; otherwise it is reset to zero. |
| `salt_K4` | After activity-coefficient adjustment | Stores the adjusted MgSO4 equilibrium constant for the current layer when the activity product is positive; otherwise it is reset to zero. |

## File I/O

<!-- facts:io -->


## Lineage

`salt_chem_hru.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 9 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `salt_chem_hru.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `fd90e36` (2025-02-06) — variable initialization changes
- `889136d` (2025-02-03) — Fix typos
- `dab22e1` (2024-10-08) — Remove unused format labels in Fortran source files
- `f1e61a3` (2024-10-08) — fixed tabs
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_chem_hru' has no extracted documentation comment.
- algorithm_steps revised: expanded the four draft steps into 14 source-backed steps aligned to the actual control flow and line ranges.
- Source mentions `salt_K5` in the code, but it was not included in the fill targets; it is therefore left undocumented here.
- `basin_module`, `salt_data_module`, and `time_module` had no resolved outside refs in the packet, so their descriptions are necessarily uncertain and kept at module-level only.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
