---
kind: module
symbol: soil_data_module
title: soil_data_module
status: filled
source_hash: e515b0f34f0e314e
version_label: SWAT+ 62.0.0
variables:
  soil_lte: Allocatable LTE texture-to-property lookup table. Each record is keyed by `texture`
    and provides profile-scaling factors `awc`, `por`, and `scon` used by `hru_lte_read` to
    derive HRU water capacity, porosity, and conductivity from the HRU LTE texture code. It
    is populated by `soil_lte_db_read` from `soils_lte.sol`; if the file is absent or null,
    that routine creates a one-element placeholder array.
  solt_db: Allocatable soil-test nutrient database. Each record stores a named initialization
    set for starting soil nutrients and humus coefficients, including nitrate, labile P, active
    humus fraction, and humus C:N and C:P ratios. It is populated by `solt_db_read` from `nutrients.sol`
    and consumed by `hru_read` and `soil_nutcarb_init` when matching HRU initialization names
    and seeding layer nutrient/carbon pools.
  soildb: Allocatable soil profile database. Each record combines a profile header `s` with
    a layer array `ly`, representing one loaded soil series and its physical properties by
    layer. It is populated by `soil_db_read` from `soils.sol`, then copied and reshaped by
    `soils_init` and adjusted by `soils_test_adjust` for downstream soil physics and HRU setup.
type_components:
  soil_lte_database:
    texture: Texture label used as the lookup key when HRU LTE code is matched to soil properties.
    awc: Available water capacity factor associated with that texture.
    por: Porosity factor associated with that texture.
    scon: Conductivity factor associated with that texture.
  soiltest_db:
    name: Initialization name used to match the soil-test record against HRU soil/nutrient
      setup names.
    exp_co: '|depth coefficient to adjust concentrations for depth'
    lab_p: ppm     |labile P in soil surface
    nitrate: ppm     |nitrate N in soil surface
    fr_hum_act: 0-1     |fraction of soil humus that is active
    hum_c_n: ratio   |humus C:N ratio (range 8-12)
    hum_c_p: ratio   |humus C:P ratio (range 70-90)
    inorgp: ppm     |inorganic P in soil surface - not currently used
    watersol_p: ppm     |water soluble P in soil surface - not currently used
    h3a_p: ppm     |h3a P in soil surface - not currently used
    mehlich_p: ppm     |Mehlich P in soil surface - not currently used
    bray_strong_p: ppm     |Bray P in soil surface - not currently used
  soiltest_db_old:
    name: Initialization name used to identify the old soil-test record.
    exp_co: '|depth coefficient to adjust concentrations for depth'
    totaln: ppm     |total N in soil
    inorgn: ppm     |inorganic N in soil surface
    orgn: ppm     |organic N in soil surface
    totalp: ppm     |total P in soil surface
    inorgp: ppm     |inorganic P in soil surface
    orgp: ppm     |organic P in soil surface
    watersol_p: ppm     |water soluble P in soil surface
    h3a_p: ppm     |h3a P in soil surface
    mehlich_p: ppm     |Mehlich P in soil surface
    bray_strong_p: ppm     |Bray P in soil surface
  soilayer_db:
    z: mm             |depth to bottom of soil layer
    bd: Mg/m**3        |bulk density of the soil
    awc: mm H20/mm soil |available water capacity of soil layer
    k: mm/hr          |saturated hydraulic conductivity of soil layer. Index:(layer,HRU)
    cbn: '%              |percent organic carbon in soil layer'
    clay: none           |fraction clay content in soil material (UNIT CHANGE!)
    silt: '%              |percent silt content in soil material'
    sand: none           |fraction of sand in soil material
    rock: '%              |percent of rock fragments in soil layer'
    alb: none           |albedo when soil is moist
    usle_k: '|USLE equation soil erodibility (K) factor'
    ec: dS/m           |electrical conductivity of soil layer
    cal: '%              |soil CaCo3'
    ph: '|soil Ph'
  soil_profile_db:
    snam: NA            |soil series name
    nly: none          |number of soil layers
    hydgrp: NA            |hydrologic soil group
    zmx: mm            |maximum rooting depth
    anion_excl: none          |fraction of porosity from which anions are excluded
    crk: none          |crack volume potential of soil
    texture: '|texture of soil'
  soil_database:
    s: Profile header component of type `soil_profile_db` for the soil series metadata.
    ly: Allocatable layer array of type `soilayer_db` containing the soil profile's layer
      properties.
type_summaries:
  soil_lte_database: A single LTE soil texture lookup record that maps a texture label to
    profile-level water and hydraulic scaling factors.
  soiltest_db: A named soil-test initialization record that supplies starting nutrient concentrations
    and humus ratios for a soil or HRU.
  soiltest_db_old: Legacy soil-test initialization record type retained in the module as an
    old schema.
  soilayer_db: One soil layer record holding the physical and chemical properties for a single
    depth interval.
  soil_profile_db: A soil profile header record with the series name, layer count, hydrologic
    group, rooting depth, and texture metadata.
  soil_database: A complete soil record combining one profile header with its allocatable
    layer array.
---

<!-- facts:header -->

`soil_data_module` owns the shared soil lookup and database state used across SWAT+ startup and soil setup: the LTE texture lookup table `soil_lte`, the soil-test nutrient database `solt_db`, and the loaded soil profile database `soildb`. Reader routines populate these allocatable arrays from `soils_lte.sol`, `nutrients.sol`, and `soils.sol`, and later setup routines use them to map HRU soil names and textures into working soil properties and initial nutrient/carbon conditions.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it contains no procedures and no startup logic of its own. The shared allocatable arrays are populated by external reader routines such as `soil_db_read`, `soil_lte_db_read`, and `solt_db_read` before setup routines consume them.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:hru_lte_read] | `hru-lte.hru` | `soil_lte` | Uses the LTE texture lookup table to map each HRU texture code to water capacity, porosity, and conductivity values. |
| [sym:hru_read] | `hru-data.hru` | `solt_db, soildb` | Resolves HRU soil-test names against `solt_db` and soil-series names against `soildb` so each HRU points to the correct initialization and soil profile records. |
| [sym:soil_db_read] | `soils.sol` | `soildb` | Allocates and fills the shared soil profile database from the soils file, including each profile header and layer array. |
| [sym:soil_lte_db_read] | `soils_lte.sol` | `soil_lte` | Allocates and fills the shared LTE texture lookup table from the LTE soils file, or creates a placeholder when the file is unavailable. |
| [sym:soil_nutcarb_init] | `solt_db` | `solt_db` | Reads the selected soil-test record to seed layer nitrate, labile phosphorus, and humus ratio initialization. |
| [sym:soils_init] | `soil_lyr_depths.sol` | `soildb` | Copies `soildb` into the working soil database and may remap layer structure using the custom soil-layer depth file. |
| [sym:solt_db_read] | `nutrients.sol` | `solt_db` | Allocates and fills the soil-test nutrient database from the nutrients file and normalizes out-of-range exponential coefficients. |
| [sym:topohyd_init] | `none extracted` | `soil_lte, solt_db, soildb` | Imported alongside other setup state, but the extracted body shows no direct references to this module's soil state. |

## Key Consumers

Imported by setup and initialization routines that need shared soil lookup tables or loaded soil databases. Some consumers use the texture table, others use the soil-test database, and the soil-profile loaders and adjusters use the soil series database itself.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:hru_lte_read] | soil_data_module | The module supplies the texture-to-property lookup table used to derive HRU LTE soil-water and hydraulic attributes from the texture code. The loaded `soil_lte` values drive the HRU's available water capacity, porosity, and conductivity calculations. |
| [sym:hru_read] | soil_data_module | The module provides the soil-test table and soil profile database used to resolve HRU soil initialization names and soil-series names into numeric indices. Those resolved indices are then available for later HRU initialization and setup. |
| [sym:soil_db_read] | soil_data_module | The module owns the allocatable `soildb` structure that this routine allocates and fills from `soils.sol`, making the loaded soil profile database available to later initialization and soil physics routines. |
| [sym:soil_lte_db_read] | soil_data_module | The module owns the allocatable `soil_lte` lookup array that this routine creates from `soils_lte.sol`, providing the shared texture-to-property table used by HRU LTE setup. |
| [sym:soil_nutcarb_init] | soil_data_module | The module supplies the selected soil-test record that seeds layer nitrate, labile P, active humus fraction, and humus C:N and C:P ratios for soil nutrient and carbon initialization. |
| [sym:soils_init] | soil_data_module | The module contains the source soil database that `soils_init` copies into the working soil arrays before any custom-depth remapping or soil physics initialization occurs. |
| [sym:solt_db_read] | soil_data_module | The module owns the allocatable soil-test database array `solt_db`; this routine allocates it, fills each record from file input, and normalizes `exp_co` when needed. |
| [sym:topohyd_init] | soil_data_module | The module is imported here, but the extracted body does not reference its soil state directly. The completed procedure overlay shows no resolved `soil_data_module` use beyond import visibility. |
| [sym:soils_test_adjust] | soil_data_module | The module provides the source soil profile database that this routine expands into millimeter resolution before averaging adjusted layer properties back into the active soil profile. |

## Lineage

`soil_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `f1e61a3` (2024-10-08, "fixed tabs"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `soil_data_module.f90` are listed.

- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `soil_data_module` has no extracted module-level documentation comment.
- No lineage commits were resolved for the requested source span.
- The `topohyd_init` import is visible in the importer list, but the completed procedure evidence shows no direct use of `soil_data_module` symbols in the extracted body.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
