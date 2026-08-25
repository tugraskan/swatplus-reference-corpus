---
kind: module
symbol: soil_module
title: soil_module
status: filled
source_hash: cc5e77c81ce339b2
version_label: SWAT+ 62.0.0
variables:
  layer1: Allocatable working array of `soilayer` records used as a temporary copy of an HRU
    soil-layer sequence during profile editing. The source type holds per-layer chemistry,
    water, conductivity, and tillage/mixing fields, and `layersplit` saves and restores layers
    through `layer1` before rebuilding `soil(ihru)%ly`.
  phys1: Allocatable working array of `soil_physical_properties` records used as a temporary
    copy of an HRU soil-physics sequence during profile editing. It mirrors layer depth, thickness,
    bulk density, water capacity, and texture fields and is used by `layersplit` to reconstruct
    `soil(ihru)%phys` after a split.
  sol_test: Allocatable array of `soil_test` records holding soil carbon test observations
    for calibration and soil-profile adjustment. Each record stores soil series name, test
    depth, bulk density, organic carbon, sand, silt, and clay.
  nmbr_soil_test_layers: integer number of soil carbon test layers loaded for the current
    soil test database; initialized to 0 and used by `soils_test_adjust` and `soils_init`
    when matching test profiles to model layers.
  soil: Allocatable array of `soil_profile` records, one per HRU, that stores the working
    soil profile used by the model. Each profile carries series metadata, hydrologic group,
    layer arrays, profile-scale water and texture state, and output/calibration fields such
    as `sw`, `sumfc`, `sumul`, `usle_k`, and `zmx`.
  soil_init: Allocatable baseline copy of `soil` used by calibration and re-initialization
    workflows. `cal_allo_init` allocates and copies it from `soil`, and `re_initialize` imports
    both arrays so the active soil profile can be restored from the saved initial state.
  sol: Allocatable array of `soil_hru_database` records holding the database soil profile
    for each HRU soil series. It contains a nested `soil_profile` plus per-layer physical
    and `soilayer` arrays, and `soil_phys_init` / `soils_init` populate the active `soil`
    profiles from it.
type_components:
  soilayer:
    ec: electrical conductivity value for the layer; declared as a layer property but not
      further documented in the extracted source.
    cal: calcium-related layer property; declared as a layer property but not further documented
      in the extracted source.
    ph: soil pH for the layer; declared as a layer property but not further documented in
      the extracted source.
    alb: none          albedo when soil is moist
    usle_k: USLE equation soil erodibility (K) factor
    conk: mm/hr          lateral saturated hydraulic conductivity for each profile layer in
      a give HRU.
    flat: mm H2O         lateral flow storage array
    prk: mm H2O         percolation from soil layer on current day
    volcr: mm             crack volume for soil layer
    tillagef: daily combined tillage/mixing factor for the layer; used by tillage and carbon/mixing
      routines to apply disturbance effects.
    tillagef_biomix: biological-mixing contribution to the layer tillage factor; set separately
      from tillage mixing so both effects can be combined later.
    tillagef_tillmix: tillage-induced contribution to the layer tillage factor; stores the
      mixing effect from an explicit tillage event.
    bmix: layer biological mixing coefficient used by management mixing routines.
    init_bmix: initial biological mixing coefficient saved as the starting reference for later
      mixing adjustments.
    watp: layer water availability or water pressure parameter used by management and hydrologic
      routines.
    a_days: days counter associated with the layer's mixing or aging state.
    b_days: days counter associated with the layer's mixing or aging state.
    psp_store: layer phosphorus storage pool for the PSP/SSP bookkeeping.
    ssp_store: layer phosphorus storage pool for the PSP/SSP bookkeeping.
    percc: layer percolation control coefficient.
    latc: layer lateral flow control coefficient.
    vwt: layer water/transport weighting factor used in soil-process bookkeeping.
  soil_physical_properties:
    d: mm           ! depth to bottom of soil layer
    thick: mm           ! thickness of soil layer
    bd: Mg/m**3      ! bulk density of the soil
    k: mm/hr        ! saturated hydraulic conductivity of soil layer. Index:(layer,HRU)
    cbn: mm/hr        ! percent organic carbon of soil layer
    clay: '%            ! percent clay content in soil material (UNIT CHANGE!)'
    silt: '%            ! percent silt content in soil material'
    sand: '%            ! percent of sand in soil material'
    rock: '%            ! percent of rock fragments in soil layer'
    conv_wt: none         ! factor which converts kg/kg to kg/ha
    crdep: mm           ! maximum or potential crack volume
    awc: mm H20/mm    | soil available water capacity of soil layer
    fc: mm H2O       | amount of water available to plants in soil layer at field capacity
      (fc - wp),Index:(layer,HRU)
    hk: none         ! beta coefficient to calculate hydraulic conductivity
    por: none         ! total porosity of soil layer expressed as a fraction of the total
      volume, Index:(layer,HRU)
    st: mm H2O       ! amount of water stored in the soil layer on any given day (less wp
      water)
    tmp: deg C        ! daily average temperature of second soil layer
    ul: mm H2O       ! amount of water held in the soil layer at saturation (sat - wp water)
    up: mm H2O/mm    ! soil water content of soil at -0.033 MPa (field capacity)
    wp: mm H20/mm    ! soil water content of soil at -1.5 MPa (wilting point)
    wpmm: mm H20       ! water content of soil at -1.5 MPa (wilting point)
    tot_sw: mm H20       ! total soil water content in mm/mm by layer that includes wilting
      point water content
  soil_test:
    snam: NA            soil series name
    d: mm           ! depth in mm of soil carbon test
    bd: Mg/m^3       | bulk density soil test
    cbn: '%            ! percent organic carbon from soil test'
    sand: '%            | percent sand'
    silt: '%            | percent silt'
    clay: '%            | percent clay'
  soil_profile:
    snam: NA            soil series name
    hydgrp: NA            hydrologic soil group
    texture: soil textural class label for the HRU profile.
    nly: none          number of soil layers
    phys: allocatable per-layer `soil_physical_properties` array for the profile.
    ly: allocatable per-layer `soilayer` array for the profile.
    pest: kg/ha    total pesticide in the soil profile
    zmx: mm            maximum rooting depth in soil
    anion_excl: none          fraction of porosity from which anions are excluded
    crk: none          crack volume potential of soil
    alb: none          albedo when soil is moist
    usle_k: USLE equation soil erodibility (K) factor
    det_san: detached sand fraction stored for erosion bookkeeping.
    det_sil: detached silt fraction stored for erosion bookkeeping.
    det_cla: detached clay fraction stored for erosion bookkeeping.
    det_sag: detached small aggregate fraction stored for erosion bookkeeping.
    det_lag: detached large aggregate fraction stored for erosion bookkeeping.
    sumul: mm H2O         amount of water held in soil profile at saturation
    sumfc: mm H2O         amount of water held in the soil profile at field capacity
    sw: mm H2O         amount of water stored in soil profile
    sw_300: mm H2O         amount of water stored to 300 mm
    sumwp: mm H2O         amount of water held in soil profile at wilting point.
    swpwt: mm H2O         water held at wilting point for profile bookkeeping.
    ffc: none           initial HRU soil water content expressed as fraction of field capacity
    wat_tbl: depth to the water table or a related groundwater table indicator used by soil-water
      logic.
    avpor: none           average porosity for entire soil profile
    avbd: Mg/m^3         average bulk density for soil profile
    tmp_srf: celsius        surface temperature of the soil
  soil_hru_database:
    snam: NA            soil series name
    hydgrp: NA            hydrologic soil group
    texture: soil textural class label for the database entry.
    s: embedded `soil_profile` record for the HRU soil series.
    phys: allocatable per-layer `soil_physical_properties` array for the database soil.
    ly: allocatable per-layer `soilayer` array for the database soil.
type_summaries:
  soilayer: One soil-layer management record for layer-specific chemistry, water, and tillage/mixing
    state.
  soil_physical_properties: One physical soil-layer record giving geometry, texture, hydraulic
    properties, and water-state variables for a profile layer.
  soil_test: One measured soil test record used for carbon/texture calibration and adjustment.
  soil_profile: One HRU soil profile record combining series metadata, layer arrays, and profile-scale
    hydrologic/texture state.
  soil_hru_database: One soil-series database entry that packages a profile record plus its
    per-layer physical and management arrays.
---

<!-- facts:header -->

Declares the shared soil-state types and global soil arrays used across SWAT+ for HRU soil profiles, layer physical properties, soil test data, and calibration/init copies. It owns the core soil profile databases (`soil`, `sol`, `soil_init`) that downstream hydrology, nutrient, carbon, sediment, pesticide, salt, groundwater, and management routines read and update.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is primarily a declaration container. It does not contain extracted procedures, but several startup and calibration routines allocate and populate its arrays: `soils_init` builds `soil` from database inputs, `soil_phys_init` and `soil_text_init` derive layer properties, `cal_allo_init` snapshots `soil` into `soil_init`, and `soils_test_adjust` fills the soil-test arrays.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `soil, sol, soil_init, layer1, phys1, sol_test, nmbr_soil_test_layers` | Reads and writes soil profile state during management actions, including irrigation, fertilizer, manure, tillage, planting, transplanting, and calibration-triggered updates. |
| [sym:basin_sw_init] | `none` | `soil` | Copies each HRU's current soil water into basin, RU, and HRU water-balance initial conditions before simulation starts. |
| [sym:cal_allo_init] | `none` | `soil, soil_init` | Allocates the initial soil arrays and copies the active soil profiles into `soil_init` for calibration baselines. |
| [sym:cal_parm_select] | `none` | `soil, sol` | Applies calibration changes directly to soil profile fields and recalculates dependent soil-water parameters. |
| [sym:calsoft_control] | `unit_4999, unit_5001, unit_5000` | `soil, soil_init` | Coordinates soft-calibration workflows that may eventually adjust soil-related parameters through downstream routines. |
| [sym:calsoft_read_codes] | `codes.sft` | `none resolved` | Imports the module as part of calibration setup, but the extracted source does not reference any soil symbols inside the routine. |
| [sym:cn2_init] | `none` | `sol` | Reads the HRU soil hydrologic group from the soil database entry to select the appropriate curve number. |
| [sym:cn2_init_all] | `none` | `none resolved` | Loops over HRUs and calls `cn2_init`; the soil module is present so that curve-number initialization can access soil-group state. |
| [sym:command] | `unit_out_hyd_sep` | `soil` | Uses soil state indirectly through the model's central command/output flow. |
| [sym:cs_balance] | `unit_6080, unit_6082, unit_6084, unit_6086` | `soil` | Traverses every soil layer in each HRU when aggregating constituent mass balances. |
| [sym:cs_hru_init] | `none` | `soil` | Allocates and initializes soil-layer constituent arrays using the HRU soil layer count and layer water/bulk-density properties. |
| [sym:gwflow_simulate] | `unit_out_gw, unit_out_hru_pump_obs, unit_out_tile_cells, unit_out_gwsw_groups, unit_out_gwsw_chanobs_flow, unit_out_gwsw_chanobs_no3, unit_1421` | `soil` | Uses soil profile state during groundwater-soil exchange, recharge lag, and output accounting. |

## Key Consumers

The module is used broadly by HRU setup, soil-profile initialization, hydrology, nutrient and constituent routing, carbon and residue cycling, groundwater exchange, management operations, and output writers. The strongest consumers are the soil/profile initialization routines (`soils_init`, `soil_phys_init`, `soil_text_init`, `cal_allo_init`), the daily HRU process drivers (`hru_control`, `proc_hru`, `mgt_sched`), and the soil-constituent/cycle routines (`cs_*`, `nut_*`, `salt_*`, `cbn_*`, `gwflow_*`).

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_sw_init] | soil_module | The current soil-profile water content is copied from `soil(ihru)%sw` into the HRU water-balance outputs, making soil state the source of the initial basin water balance. |
| [sym:cal_allo_init] | soil_module | `soil_module` provides the active soil profile and soil initialization structures. `cal_allo_init` uses the current HRU soil layer count to size `soil_init`, then copies `soil` into `soil_init` so calibration can reference a preserved soil profile baseline. |
| [sym:cal_parm_select] | soil_module | `soil_module` provides the soil profile and layer arrays that are recalibrated when soil depth, bulk density, water capacity, conductivity, texture, or chemistry parameters change. These values control soil-water initialization, erosion factors, and layer-dependent hydrology for `soil(ielem)`. |
| [sym:cn2_init] | soil_module | The soil module matters because the hydrologic soil group controls which of the four curve-number values is selected. `sol(isol)%s%hydgrp` is the soil-group label that drives the A/B/C/D branch selection. |
| [sym:cs_balance] | soil_module | The soil profile layer count determines how many layers cs_balance must traverse when summing dissolved and sorbed soil constituent masses for each HRU. |
| [sym:cs_hru_init] | soil_module | soil_module provides the per-HRU soil layering and layer properties needed to size the initialization loops and convert concentrations into soil-water and sorbed mass. `soil(ihru)%nly`, `soil(ihru)%phys(ly)%st`, `soil(ihru)%phys(ly)%thick`, and `soil(ihru)%phys(ly)%bd` control how much water and soil mass each layer contains, which is required for the kg/ha calculations. |
| [sym:mallo_control] | soil_module | Provides soil-water state referenced in management output. |
| [sym:obj_output] | soil_module | Soil-layer water output uses `soil(j)%phys(nly)%st` and `soil(iob)%phys(nly)%st` to print per-layer soil water storage, and `soil% nly` defines how many layer records each object contributes. |
| [sym:pathogen_init] | soil_module | This module provides each HRU’s soil-layer count, which determines how many soil pathogen arrays to allocate and which layer index is valid for initialization. |
| [sym:pesticide_init] | soil_module | The soil profile defines how many layers each HRU has and supplies the layer bulk density and thickness needed to convert the initial soil pesticide concentration into kg/ha for each layer. |
| [sym:plant_init] | soil_module | `soil_module` matters because layer allocations for plant water uptake and root fractions are sized from the HRU soil profile’s number of layers. |
| [sym:proc_hru] | soil_module | Provides the soil profile fields written to the checker output for each HRU. |
| [sym:salt_balance] | soil_module | Soil profile metadata determines how many layers to scan and how to convert layer thickness and bulk density into soil mass. Those values are needed to compute total solid salt stored in soil layers from layer salt concentrations. |
| [sym:salt_hru_init] | soil_module | `soil_module` provides the number of layers in each HRU and each layer's stored water (`st`), both of which control the nested loops and the concentration-to-mass conversion. |
| [sym:soil_awc_init] | soil_module | `soil_module` is the core data store this routine updates. Its `soil` profiles provide the layer counts and physical properties being recalculated, and the results written back here become the soil-water inputs used by later hydrologic calculations. |
| [sym:soil_carbvar_write_legacy] | soil_module | `soil_module` provides the HRU soil profile, layer counts, physical layer depth, layer temperature, and tillage/mixing factors that are written alongside the carbon variables. Without this module the routine would not know how many layers to loop over or which soil-layer properties to report. |
| [sym:soil_nutcarb_init] | soil_module | `soil_module` holds the soil profile for the current HRU, including layer count, layer depths, bulk density, thickness, organic carbon, and texture. Those properties determine how many layers to initialize, how to compute mass conversion factors, how deep-decay concentrations are applied, and how the Mathers carbon split responds to texture. |
| [sym:soil_nutcarb_write_legacy] | soil_module | `soil_module` provides the HRU soil profile metadata and layer properties that this routine prints, including layer count, soil series name, layer depths, and physical properties such as bulk density, water capacity, carbon content, texture, and surface-layer attributes. Those values define the per-HRU soil snapshot records and the depth basis for the layered and profile summaries. |
| [sym:soil_phys_init] | soil_module | `soil_module` defines the `sol` database and the nested soil profile, physical-layer, and layer-output components that this routine reads and updates. The entire procedure operates by initializing those fields in place, so the module provides both the target state and the type definitions that make the assignments possible. |
| [sym:soil_text_init] | soil_module | `soil_module` owns the `soil` array and the `soil_profile` fields that this routine reads and overwrites. Without that shared profile state, the routine could not translate the current sand, clay, and silt contents into the stored detached sediment fractions used later by the model. |
| [sym:soils_init] | soil_module | The soil module holds the working soil profiles that `soils_init` builds and the layer objects it fills. The routine copies profile metadata and layer properties into `sol`, then later routines rely on those initialized `soil_module` records for hydrology, erosion, and constituent calculations. |
| [sym:swift_output] | soil_module | The soil module matters because the HRU data file writes the hydrologic soil group for each HRU. That field is part of the SWIFT HRU summary and is read directly from `soil(ihru)%hydgrp`. |
| [sym:wallo_control] | soil_module | Routes one water-allocation transfer through demand, withdrawal, transfer, and receiving-object updates. |
| [sym:calsoft_read_codes] | soil_module | The module is imported, but the extracted source does not reference any soil symbols inside this routine. It is part of the broader calibration dependency set rather than an active data source here. |

## Lineage

`soil_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 21 non-merge commit(s) since, most recently `e69242a` (2026-05-06, "added init_bmix to soil module and initialized it in soil_nutcarb_init"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `soil_module.f90` are listed.

- `e69242a` (2026-05-06) — added init_bmix to soil module and initialized it in soil_nutcarb_init
- `af7aeda` (2026-05-05) — Fixed logical comparisotn to .eqv.
- `452f563` (2026-05-01) — Update to comments to correct units and definitions. Updates to pl_manure equations to utilize input carbon in manure_om.frt file.
- `1b2a997` (2026-04-27) — Made changes to implement a linear increase in biomixing after a tillage event.
- `08d78c9` (2026-04-15) — Changes to use surface temperature of soil to determine when surface residue decomposition occurs. Removed unnecessary code from cbn_zhang2…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `soil_module` has no extracted module-level documentation comment.
- Reader list is representative of the main initialization and read paths; the full importer set is preserved separately in `all_importers`.
- Some component meanings are only partially documented in-source (for example `ec`, `cal`, `ph`, `wat_tbl`, and the detached sediment fields), so those descriptions were kept conservative.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
