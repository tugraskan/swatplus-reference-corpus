---
kind: module
symbol: plant_module
title: plant_module
status: filled
source_hash: aad357a433ef47e6
version_label: SWAT+ 62.0.0
variables:
  basin_plants: Integer basin-wide counter of plant records; initialized to 0 in the module
    and filled by plant initialization routines such as `plant_all_init` as the basin plant
    inventory is built.
  yld_tbr: Module-level `plant_mass` record for tuber yield carbon/nutrient fractions. It
    is a shared output state, initialized to default zero fractions, and consumed by harvest
    and crop-yield accounting.
  yld_grn: Module-level `plant_mass` record for grain yield fractions. It is shared state
    for harvest accounting and output, initialized to default zero fractions and read by crop-yield
    routines.
  yld_veg: Module-level `plant_mass` record for vegetative yield fractions. It is shared state
    for harvest accounting and output, initialized to default zero fractions and read by crop-yield
    routines.
  yld_rsd: Module-level `plant_mass` record for residue yield fractions. It is shared state
    for harvest accounting and output, initialized to default zero fractions and read by harvest
    and residue routines.
  pcom: Allocatable array of `plant_community` records, one per HRU or active object needing
    plant state. It is allocated by setup routines such as `hru_allo` and populated by `hru_lum_init`,
    `plant_init`, `hru_dtbl_actions_init`, `cal_allo_init`, and related initialization code.
  pcom_init: Allocatable baseline copy of `pcom` used by calibration and re-initialization
    workflows. `cal_allo_init` allocates and fills it, and `re_initialize` restores active
    state from it.
  plmz: Module-level `plant_mass` scratch/summary record used as a zero or temporary plant-mass
    container. It is initialized by the module declaration and consumed by plant management
    and output routines that need a reusable mass record.
  o_m1: Module-level `plant_mass` scratch/summary record. It is declared in the shared module
    state and used by plant accounting workflows that need three reusable mass objects.
  o_m2: Module-level `plant_mass` scratch/summary record. It is declared in the shared module
    state and used by plant accounting workflows that need three reusable mass objects.
  o_m3: Module-level `plant_mass` scratch/summary record. It is declared in the shared module
    state and used by plant accounting workflows that need three reusable mass objects.
  plstrz: Module-level default `plant_stress` record used as a shared scratch or zero state.
    It is initialized by the type defaults and used by plant-management routines that need
    a reusable stress object.
  bsn_crop_yld: Allocatable basin crop-yield summary array. It stores area and harvested yield
    mass by basin crop and is initialized by `plant_all_init` for later use by `actions`,
    `time_control`, and `hru_output`.
  bsn_crop_yld_aa: Allocatable array of average-annual basin crop-yield summaries. It is initialized
    by `plant_all_init` and written by year-end and simulation-end crop-yield reporting.
  bsn_crop_yld_z: Single basin crop-yield summary record used as a zero/default accumulator.
    It is initialized in the module and used by basin and simulation-end yield reporting.
  c_frac: Shared `plant_carbon` record holding the default carbon fractions for leaf, stem,
    seed, and root pools. It is initialized in the module declaration and read by plant partitioning
    and carbon-accounting routines.
type_components:
  plant_growth:
    cht: m                |canopy height
    lai: m**2/m**2        |leaf area index
    plet: mm H2O           |actual ET simulated during life of plant
    plpet: mm H2O           |potential ET simulated during life of plant
    laimxfr: Leaf-area-transfer factor or fraction used during leaf-area decline/partitioning;
      it is a declared growth-state scalar and the source comment gives no fuller definition.
    laimxfr_p: Perennial version of the leaf-area-transfer factor/fraction; source comment
      is blank, so its exact physical meaning is uncertain from this packet.
    hi_adj: (kg/ha)/(kg/ha)  |temperature adjusted harvest index for current time during growing
      season
    hi_prev: (kg/ha)/(kg/ha)  |optimal harvest index for current time during growing season
    olai: '|leaf area index (0-1) when leaf area decline begins'
    dphu: '|phu accumulated (0-1) when leaf area decline begins'
    d_senes: days             !days since start of senescence
    leaf_frac: none             |fraction of above ground tree biomass that is leaf
    root_dep: mm               |root depth
    root_frac: kg/ha            |root fraction of total plant mass
    rtfr: none  |root fraction for each plant in community
  plant_mass:
    c_fr: carbon fraction stored for this plant mass record
    n_fr: nitrogen fraction stored for this plant mass record
    p_fr: phosphorus fraction stored for this plant mass record
  plant_status:
    idplt: none         land cover code from plants.plt
    bsn_num: none              |basin plant number
    gro: '|land cover status; ''n'' = no land cover growing; ''y'' = land cover growing'
    idorm: none         |dormancy status; 'n'=land cover growing; 'y'=land cover dormant
    mseas: none         |monsoon status;  'n'= not in monsoon season; 'y'= in monsoon season
    phumat: C            |heat units to maturity - annual
    phumat_p: C            |heat units to maturity for perennials
    phuacc: fraction     |fraction of plant heat unit accumulated
    phuacc_p: fraction     |fraction of perennial plant heat unit accumulated
    harv_num: '|number of harvest operations for entire simulation'
    harv_num_yr: '|number of harvest operations each year'
    curyr_mat: Current-year maturity flag or counter for the plant; the source comment is
      blank, so the exact intended wording is not explicit in this packet.
    pop_com: none
    days_senes: mm           |days since scenesence began (for moisture growth perennials)
    leaf_tov: none         |leaf turnover rate - decline in lai and leaf biomass
    lai_pot: none         |potential leaf area index
    harv_idx: fraction     |harvest index - grain fraction of above ground plant mass
    pest_stress: fraction     |pest (insect, disease) stress on harvest index
    epco: fraction     |water uptake compensation factor for each plant
    uptake: mm   |water uptake by layer
  plant_stress:
    reg: none         |stress factor that most limits plant growth
    strsw: 'on current day

      none         |frac of potential plant growth achieved on the day where the'
    strsa: 'reduction is caused by water stress

      |frac of potential plant growth achieved on the day where the'
    strsn: 'reduction is caused by air stress

      none         |frac of potential plant growth achieved on the day where the reduction'
    strsp: 'is caused by nit stress

      none         |frac of potential plant growth achieved on the day where the reduction'
    strst: 'is caused by phos stress

      none         |frac of potential plant growth achieved on the day where the reduction'
    strss: 'is caused by temp stress

      none         |frac of potential plant growth achieved on the day where the reduction'
    sum_w: 'is caused by salt stress (rtb salt)

      none         |sum of water stress'
    sum_tmp: none         |sum of temperature stress
    sum_n: none         |sum of nitrogen stress
    sum_p: none         |sum of phosphorus stress
    sum_a: none         |sum of aeration stress
  auto_operations:
    apply_day: day to apply in prob_unif1 condition
    num_actions: current number of actions - reset on January 1
    days_act: days since the action specified in lim_const
  fertilize_future:
    name: name of the fertilizer operation (from the dtbl)
    num: number of the future fertilizer application (from the dtbl)
    fertname: fertilizer name in fertilizer.frt
    fertnum: fertilizer number in fertilizer.frt
    day_fert: future julian day to apply fert (must be within a year of test)
    fert_kg: kg/ha - amount of fertilzer applied
    fertop: application type in chem_app.ops
    appnum: application number in chem_app.ops
  plant_community:
    name: Plant-community name associated with the HRU's selected land-use management record.
    npl: number of plants in community
    pl: N/A              |plant name
    pcomdb: current plant community database number
    rot_yr: rotation year
    days_plant: '|days since last planting - for conditional scheduling after planting'
    days_harv: '|days since last harvest - for conditional scheduling after harvest'
    days_kill: '|days since last kill - for conditional scheduling after kill'
    days_irr: '|days since last irrigation - for conditional scheduling after irrigation'
    last_kill: '|name of last plant killed'
    cht_mx: m             |height of tallest plant in community for pet calculation
    lai_sum: m/m           |sum of lai for each plant
    laimx_sum: m/m           |sum of maximum lai for each plant - for canopy interception
    rsd_covfac: '|average residue cover factor'
    dtbl: d_tble action - to limit number of actions per year
    fert_fut_num: Count of deferred fertilizer operations stored in `fert_fut` for this plant
      community.
    fert_fut: Deferred fertilizer-operation array copied from the decision table for later
      management execution.
    plg: plant growth variables
    plstr: plant stress variables
    plcur: plant status variables
    plm: kg/ha            |total biomass for individual plant in community
  basin_crop_yields:
    area_ha: ha         |area of crop harvested
    yield: t          |yield mass removed in harvest
  plant_carbon:
    leaf: none   |carbon fraction in leaves
    stem: none   |carbon fraction in stem
    seed: none   |carbon fraction in seeds
    root: none   |carbon fraction in roots
type_summaries:
  plant_growth: Per-plant growth-state record for canopy, ET, senescence, and rooting behavior.
  plant_mass: Per-plant biomass and elemental-fraction record used for live biomass, residue,
    and yield pools.
  plant_status: Per-plant phenology and management-status record for growth, dormancy, harvest,
    and uptake tracking.
  plant_stress: Per-plant stress accumulator record that tracks limiting factors and summed
    stress exposure.
  auto_operations: One decision-table auto-operation slot with day counters for conditional
    management actions.
  fertilize_future: Deferred fertilizer-operation record copied from the land-use decision
    table for later execution.
  plant_community: Per-HRU plant-community container holding names, plant arrays, management
    tables, and biomass/status fields.
  basin_crop_yields: Basin-level crop-harvest summary record holding harvested area and removed
    yield mass.
  plant_carbon: Default carbon-fraction record for plant biomass pools.
---

<!-- facts:header -->

Owns the shared plant-state data structures and basin crop-yield accumulators used throughout SWAT+. It defines the plant community, plant growth/status/stress, harvest/fertilizer scheduling, and carbon-fraction types, plus the allocatable module variables that hold active HRU and basin plant state. Initialization is performed by routines such as `hru_allo`, `plant_all_init`, `plant_init`, `hru_lum_init`, `hru_dtbl_actions_init`, and `cal_allo_init`, while growth, management, output, calibration, and erosion routines depend on the stored plant-community state.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container plus one helper routine (`plg_zero`). Its allocatable arrays and per-HRU plant-community records are populated by startup and calibration routines rather than by a module initialization subroutine.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `land-use decision tables through the management workflow` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Uses plant-community state and basin yield accumulators while executing management actions such as irrigation, fertilization, harvest, and planting. It updates `pcom` counters and records crop-yield totals. |
| [sym:aqu_pesticide_output] | `aquifer pesticide output units` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Declares the module dependency, but the extracted body does not show direct use of plant symbols. |
| [sym:basin_aqu_pest_output] | `basin aquifer pesticide output units` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Declares the module dependency, but the extracted body does not show direct use of plant symbols. |
| [sym:basin_ch_pest_output] | `basin channel pesticide output units` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Declares the module dependency, but the extracted body does not show direct use of plant symbols. |
| [sym:basin_ls_pest_output] | `basin landscape pesticide output units` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Declares the module dependency, but the extracted body does not show direct use of plant symbols. |
| [sym:basin_res_pest_output] | `basin reservoir pesticide output units` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Declares the module dependency, but the extracted body does not show direct use of plant symbols. |
| [sym:cal_allo_init] | `calibration working-copy initialization` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Allocates `pcom_init`, copies active plant-community state, and initializes auto-operation counters for calibration baselines. |
| [sym:cal_parm_select] | `calibration parameter selection workflow` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Uses `pcom` when applying plant-related calibration changes such as `epco`. |
| [sym:calsoft_read_codes] | `codes.sft` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Reads the soft-calibration code file, but the extracted source does not show plant-state access. |
| [sym:ch_cs_output] | `channel constituent-mass output units` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Declares the module dependency, but the extracted body does not show direct use of plant symbols. |
| [sym:ch_salt_output] | `channel salt output units` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Declares the module dependency, but the extracted body does not show direct use of plant symbols. |
| [sym:cha_pesticide_output] | `channel pesticide output units` | `basin_plants, yld_tbr, yld_grn, yld_veg, yld_rsd, pcom` | Declares the module dependency, but the extracted body does not show direct use of plant symbols. |

## Key Consumers

Plant management, growth, calibration, erosion, ET, nutrient, pathogen, pesticide, and output routines import this module to read or update HRU plant-community state and shared crop-yield accumulators. The most direct consumers are the initialization and management drivers, while many process and output routines read `pcom`, `pl_mass`, or the basin yield arrays during daily simulation and reporting.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:hru_dtbl_actions_init] | `pcom` | Allocates and initializes each HRU's auto-operation tables and future fertilizer records inside `pcom`, so later management processing can count actions and schedule deferred fertilizer applications. |
| [sym:hru_lum_init] | `pcom` | Assigns each HRU's plant-community name from the selected land-use record, linking management selection to the plant community that will be initialized next. |
| [sym:cal_allo_init] | plant_module | Allocates `pcom_init` and copies the active plant-community state into calibration working copies so later calibration runs can start from a preserved baseline. |
| [sym:cal_parm_select] | plant_module | Updates the plant-compensation factor `epco` in each plant status record when a plant-related calibration parameter is changed, keeping the community synchronized with the HRU-level setting. |
| [sym:hru_output] | plant_module | Provides the plant names and yield accumulators used to write crop-yield output rows at the end of the simulation. |
| [sym:mallo_control] | plant_module | Provides plant-community state referenced while executing management and manure-allocation output. |
| [sym:obj_output] | plant_module | Provides plant-community state needed to print object-level plant status, growth, and biomass summaries. |
| [sym:pathogen_init] | plant_module | Supplies each HRU's plant-community size so pathogen arrays can be allocated to match the number of plants present. |
| [sym:pesticide_init] | plant_module | Provides plant count and LAI so the initial pesticide-on-plant mass can be divided among plants according to canopy size. |
| [sym:pl_read_parms_cal] | plant_module | Supplies plant-community and plant-status storage where calibration values are written after matching plant and parameter names. |
| [sym:plant_all_init] | plant_module | Initializes the basin plant counter and basin crop-yield arrays, then hands off to `plant_init` for per-HRU plant-community setup. |
| [sym:plant_init] | plant_module | Allocates and populates plant-community state, including names, status, growth, biomass pools, residue cover, rotation year, and canopy fields. |
| [sym:soil_nutcarb_write_legacy] | plant_module | Reads plant-community counts and root-fraction arrays so plant carbon summaries and layer root contributions can be written. |
| [sym:soils_init] | plant_module | Reads each HRU's plant count while sizing soil-state initialization, so the soil setup matches the plant community layout. |
| [sym:wallo_control] | plant_module | Uses plant-community state while routing water-allocation transfers and related management bookkeeping. |
| [sym:aqu_pesticide_output] | plant_module | Imports the module as part of the output stack, but the extracted body does not show direct plant-state access. |
| [sym:basin_aqu_pest_output] | plant_module | Imports the module as part of the output stack, but the extracted body does not show direct plant-state access. |
| [sym:basin_ch_pest_output] | plant_module | Imports the module as part of the output stack, but the extracted body does not show direct plant-state access. |
| [sym:basin_ls_pest_output] | plant_module | Imports the module as part of the output stack, but the extracted body does not show direct plant-state access. |
| [sym:basin_res_pest_output] | plant_module | Imports the module as part of the output stack, but the extracted body does not show direct plant-state access. |
| [sym:calsoft_read_codes] | plant_module | Loads the soft-calibration code file; the visible code does not show direct plant-module symbol use. |
| [sym:ch_cs_output] | plant_module | Imports the module for shared output context, but no plant symbol is resolved in the extracted lines. |
| [sym:ch_salt_output] | plant_module | Imports the module for shared output context, but no plant symbol is resolved in the extracted lines. |
| [sym:cha_pesticide_output] | plant_module | Imports the module for shared output context, but no plant symbol is resolved in the extracted lines. |

## Lineage

`plant_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `3e18acf` (2026-02-17, "Integrate CENTURY residue/N updates and root-fraction tracking changes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `plant_module.f90` are listed.

- `3e18acf` (2026-02-17) — Integrate CENTURY residue/N updates and root-fraction tracking changes
- `1807dbb` (2025-03-26) — na
- `568154c` (2024-10-08) — Increase length of various character variables
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment is present in the extracted source.
- The importer appendix preserves the deterministic full importer list; the main Used By table is a concise subset of direct consumers with source-backed effects.
- Some symbol meanings, notably `laimxfr`, `laimxfr_p`, and `curyr_mat`, are only partially documented in source comments; the descriptions above reflect that uncertainty.
- No resolved Git lineage commits were available for this module source span.
- algorithm_steps revised: removed the draft algorithm section because this module overlay does not expose a meaningful procedure flow beyond the small `plg_zero` helper, and no source-backed step decomposition was needed.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
