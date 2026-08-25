---
kind: module
symbol: septic_data_module
title: septic_data_module
status: filled
source_hash: 02b083631326f79a
version_label: SWAT+ 62.0.0
variables:
  sepdb: Allocatable shared database of `septic_db` parameter records loaded from `septic.sep`
    by `septic_parm_read`; each entry stores septic effluent flow and constituent concentrations
    that downstream septic routines use when adding septic tank effluent to soil pools. Later
    consumers include `sep_biozone` and any routine that maps a septic type through `sep(isep)%typ`
    into `sepdb(...)`.
  sep: Allocatable shared array of `septic_system` records loaded from `septic.str` by `sep_read`;
    each record defines a septic system name, type, operational year, status, geometry, and
    process coefficients used by septic-related HRU setup and process routines. Later consumers
    include `landuse_read`, `soils_init`, `stmp_solt`, `swr_percmain`, `swr_percmicro`, `nut_nitvol`,
    `nut_nminrl`, `hru_control`, and `sep_biozone`.
type_components:
  septic_db:
    sepnm: Septic parameter name read from the septic database record; used as the lookup
      key when septic system definitions are matched to a type.
    qs: m3/d          |flow rate of the septic tank effluent per capita (sptq)
    bodconcs: mg/l          |biological oxygen demand of the septic tank effluent
    tssconcs: mg/l          |concentration of total suspended solid in the septic tank effluent
    nh4concs: mg/l          |concentration of total phosphorus in the septic tank effluent
    no3concs: mg/l          |concentration of nitrate in the septic tank effluent
    no2concs: mg/l          |concentration of nitrite in the septic tank effluent
    orgnconcs: mg/l          |concentration of organic nitrogen in the septic tank effluent
    minps: mg/l          |concentration of mineral phosphorus in the septic tank effluent
    orgps: mg/l          |concentration of organic phosphorus in the septic tank effluent
    fcolis: mg/l          |concentration of fecal coliform in the septic tank effluent
  septic_system:
    name: Septic system name used to link landuse pointers and septic database entries to
      a specific system definition.
    typ: none            |septic system type
    yr: '|year the septic system became operational'
    opt: none             |Septic system operation flag (1=active,2=failing,0=not operated)
    cap: none             |Number of permanent residents in the house
    area: m^2              |average area of drainfield of individual septic systems
    tfail: days             |time until falling systems gets fixed
    z: mm               |depth to the top of the biozone layer from the ground surface
    thk: mm               |thickness of biozone layer
    strm_dist: km               |distance to the stream from the septic
    density: '|number of septic systems per square kilometer'
    bd: kg/m^3           |density of biomass
    bod_dc: m^3/day          |BOD decay rate coefficient
    bod_conv: '|a conversion factor representing the proportion of mass'
    fc1: 'bacterial growth and mass BOD degraded in the STE.

      none             |Linear coefficient for calculation of field capacity in the biozone'
    fc2: none             |Exponential coefficient for calculation of field capacity in the
      biozone
    fecal: m^3/day          |fecal coliform bacteria decay rate coefficient
    plq: none             |conversion factor for plaque from TDS
    mrt: none             |mortality rate coefficient
    rsp: none             |respiration rate coefficient
    slg1: none             |slough-off calibration parameter
    slg2: none             |slough-off calibration parameter
    nitr: none             |nitrification rate coefficient
    denitr: none             |denitrification rate coefficient
    pdistrb: (L/kg)           |Linear P sorption distribution coefficient
    psorpmax: (mg P/kg Soil)   |Maximum P sorption capacity
    solpslp: '|Slope of the linear effluent soluble P equation'
    solpintc: '|Intercept of the linear effluent soluble P equation'
type_summaries:
  septic_db: Parameter record for one septic-system database entry. It stores the septic effluent
    name plus per-capita effluent flow and constituent concentrations used when septic discharge
    is routed into a biozone layer.
  septic_system: Operational and process-parameter record for one septic system definition.
    It combines system identity, activation timing, geometry, failure behavior, and biozone
    reaction coefficients for septic HRUs.
---

<!-- facts:header -->

Defines the shared septic-system data used throughout SWAT+ simulation and setup. The module owns the septic parameter database `sepdb` and the working septic-system array `sep`; these records feed septic HRU initialization, landuse pointer resolution, soil-profile adjustments, water routing, soil-temperature correction, and septic biozone chemistry routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it contains no procedures. Its allocatable arrays are populated by the reader routines `septic_parm_read` and `sep_read`, then consumed by septic-related setup and process routines during HRU initialization and daily simulation.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `sepdb, sep` | Uses septic-system names from `sep` when the actions database installs septic tanks, so action pointers can be resolved to the matching septic definition. |
| [sym:hru_control] | `unit_100100` | `sepdb, sep` | Checks `sep(isep)%opt` and `sep(isep)%yr` during daily HRU control to decide whether septic biozone processing should run for the current HRU. |
| [sym:landuse_read] | `landuse.lum, unit_9001` | `sepdb, sep` | Reads landuse records and compares `lum(ilu)%septic` against `sep(ipr)%name` so septic pointers in the landuse database can be converted to integer indices. |
| [sym:sep_read] | `septic.str` | `sepdb, sep` | Counts and loads the working septic-system array `sep` from the septic system input file. |
| [sym:septic_parm_read] | `septic.sep` | `sepdb, sep` | Counts and loads the septic parameter database `sepdb` from the septic parameter input file. |
| [sym:soils_init] | `soil_lyr_depths.sol` | `sepdb, sep` | Uses `sep(isep)%opt`, `sep(isep)%z`, and `sep(isep)%thk` when deciding whether a septic biozone layer must be inserted into the HRU soil profile. |

## Key Consumers

This module is imported by database readers, HRU setup, soil-profile initialization, water routing, temperature adjustment, nitrogen transformations, and the septic biozone process itself. Some consumers only need the septic operation flag, while others use the geometry and database records to add septic effluent and update biozone chemistry.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:landuse_read] | septic_data_module | Resolves a landuse septic pointer by matching `lum(ilu)%septic` to `sep(ipr)%name`, allowing the landuse record to store the septic-system index used later in HRU setup and septic routing. |
| [sym:sep_read] | septic_data_module | Allocates and fills the shared `sep` array so septic-system definitions are available to the rest of the model. |
| [sym:septic_parm_read] | septic_data_module | Allocates and fills the shared `sepdb` database so septic effluent concentrations and flow parameters are available for septic process calculations. |
| [sym:soils_init] | septic_data_module | Checks septic operation, depth, and thickness while splitting soil layers to create a septic biozone in affected HRUs before later hydrology and biogeochemistry routines run. |
| [sym:nut_nitvol] | septic_data_module | Skips the standard nitrification and volatilization update in the septic biozone layer when `sep(isep)%opt` indicates an active septic system. |
| [sym:nut_nminrl] | septic_data_module | Bypasses denitrification in the septic-affected layer when the septic system is active, preserving septic-specific nitrogen routing instead of applying the normal mineralization loss. |
| [sym:sep_biozone] | septic_data_module | Uses `sep(isep)` to control failure recovery, geometry, and process coefficients, and uses `sepdb(sep(isep)%typ)` to add septic effluent concentrations to the biozone soil pools. |
| [sym:stmp_solt] | septic_data_module | Applies a septic-specific soil-temperature correction in layers at and below the septic biozone when the septic system is active in the current year. |
| [sym:swr_percmain] | septic_data_module | Adds septic tank effluent water to the biozone layer when septic operation is active and the layer is warm enough to accept septic input. |
| [sym:swr_percmicro] | septic_data_module | Adjusts layer seepage resistance for active or failing septic systems and records capped biozone percolation for later water-balance accounting. |
| [sym:cbn_rsd_decomp] | septic_data_module | The completed overlay evidence does not show any resolved symbol from this module being used in the routine body, so no direct effect is visible from the extracted source. |
| [sym:cbn_rsd_transfer] | septic_data_module | The completed overlay evidence does not show any resolved symbol from this module being used in the routine body, so no direct effect is visible from the extracted source. |
| [sym:cbn_surfrsd_decomp] | septic_data_module | The completed overlay evidence does not show any resolved symbol from this module being used in the routine body, so no direct effect is visible from the extracted source. |
| [sym:actions] | septic_data_module | Installs septic tanks by matching an action file pointer against `sep(istr)%name`, so the action system can create or update the correct septic-system record. |
| [sym:hru_control] | septic_data_module | Drives daily septic HRU processing by checking `sep(isep)%opt` and `sep(isep)%yr` before calling `sep_biozone` for the current HRU. |
| [sym:stor_surfstor] | septic_data_module | The completed overlay evidence does not show any resolved symbol from this module being used in the routine body, so no direct effect is visible from the extracted source. |

## Lineage

`septic_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `septic_data_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module has no extracted module-level documentation comment.
- The source comment for `nh4concs` says nitrate/total phosphorus, which appears inconsistent with the variable name; the overlay preserves the source-backed text without correcting it.
- Completed procedure evidence shows `actions` uses `sep` for septic tank installation and `stor_surfstor` has no resolved module symbol use in the extracted body.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
