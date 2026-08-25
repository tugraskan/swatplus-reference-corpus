---
kind: module
symbol: hru_lte_module
title: hru_lte_module
status: filled
source_hash: 684c3e0afc99b33e
version_label: SWAT+ 62.0.0
variables:
  awct: Real 12-element array initialized to 0. at declaration. It is module-owned shared
    state used by HRU-LTE setup and control code as a calibration/helper array; the extracted
    source does not show a direct assignment path in this module, so downstream ownership
    beyond shared use is uncertain.
  port: Real 12-element array initialized to 0. at declaration. It is module-owned shared
    state used alongside `awct` and `scon`; the provided source does not show a direct in-module
    population path, so its downstream consumers are only known indirectly through module
    importers.
  scon: Real 12-element array initialized to 0. at declaration. `hru_lte_read` imports the
    module while building HRU-LTE state, and the shared array is part of the module's public
    state for HRU-LTE calculations; no direct in-module updates are visible in the excerpt.
  hlt_db: Allocatable array of `swatdeg_hru_data` records holding the persistent HRU-LTE database
    loaded from `hru-lte.hru`. `hru_lte_read` allocates and fills it from the file, `cal_parm_select`
    edits database parameters such as CN2, ET coefficient, soil depth, slope, and tile timing,
    `calsoft_control` writes its fields, and `dr_ru` reads `tc` for delivery-ratio timing.
  hlt: Allocatable array of `swatdeg_hru_dynamic` records holding the live HRU-LTE object
    state. `hru_lte_read` derives it from `hlt_db`, `hru_lte_control` updates its daily water-balance,
    growth, and sediment fields, `actions` changes growing-season state, `cal_allo_init` copies
    it to `hlt_init`, and `re_initialize` restores it from `hlt_init`.
  hlt_init: Allocatable array of `swatdeg_hru_dynamic` records holding the preserved baseline
    copy of `hlt`. `cal_allo_init` fills it from the current `hlt` state for calibration startup,
    and `re_initialize` copies it back into `hlt` to reset HRU-LTE objects before reruns.
type_components:
  swatdeg_hru_data:
    name: HRU-LTE database name field. It is the object label loaded into the persistent record
      and later copied into the live dynamic object name.
    dakm2: km^2          |drainage area
    cn2: none          |condition II curve number
    cn3_swf: none          |soil water factor for cn3 (used in calibration)
    tc: '|0 = fc; 1 = saturation (porosity)

      min           |time of concentration'
    soildep: mm            |soil profile depth
    perco: '|soil percolation coefficient'
    slope: m/m           |land surface slope
    slopelen: m             |land surface slope length
    etco: '|et coefficient - use with pet and aet'
    sy: mm            |specific yld of the shallow aquifer
    abf: '|alpha factor groundwater'
    revapc: '|revap coefficient amt of et from shallow aquifer'
    percc: '|percolation coeff from shallow to deep'
    sw: frac          |initial soil water (frac of awc)
    gw: mm            |initial shallow aquifer storage
    gwflow: mm            |initial shallow aquifer flow
    gwdeep: mm            |initial deep aquifer flow
    snow: mm            |initial snow water equivalent
    xlat: '|latitude'
    text: '|soil texture'
    tropical: '|1=sand 2=loamy_sand 3=sandy_loam 4=loam

      |5=silt_loam 6=silt 7=silty_clay 8=clay_loam

      |9=sandy_clay_loam 10=sandy_clay

      |11=silty_clay 12=clay

      |(0)="non_trop" (1)="trop"'
    igrow1: '|start of growing season for non-tropical (pl_grow_sum)'
    igrow2: '|start of monsoon initialization period for tropical

      |end of growing season for non-tropical (pl_end_sum)'
    plant: '|end of monsoon initialization period for tropical

      |plant type (as listed in plants.plt)'
    stress: frac          |plant stress - pest, root restriction, soil quality, nutrient,
      (non water, temp)
    ipet: '|potential ET method (0="harg"; 1="p_t")'
    irr: '|irrigation code 0="no_irr";  1="irr"'
    irrsrc: irrigation source 0="outside_bsn"; 1="shal_aqu" 2="deep_aqu"
    tdrain: hr            |design subsurface tile drain time
    uslek: '|usle soil erodibility factor'
    uslec: '|usle cover factor'
    uslep: none          |USLE equation support practice (P) factor
    uslels: none          |USLE equation length slope (LS) factor
  swatdeg_hru_dynamic:
    name: Live object name copied from the routed object table.
    props: Property-table index pointing back to `hlt_db`.
    obj_no: Routed object number for the HRU-LTE element.
    lsu: '|landscape unit - character'
    region: '|region - character'
    plant: '|plant type (as listed in plants.plt)'
    iplant: 'integer :: iplant = 1                !              |plant number xwalked from
      hlt_db()%plant and plants.plt

      |plant number xwalked from hlt_db()%plant and plants.plt'
    km2: km^2          |drainage area
    cn2: '|condition II curve number (used in calibration)'
    cn3_swf: none          |soil water factor for cn3 (used in calibration)
    soildep: '|0 = fc; 1 = saturation (porosity)

      mm            |soil profile depth'
    etco: '|et coefficient - use with pet and aet (used in calibration)'
    revapc: m/m           |revap from aquifer (used in calibration)
    perco: '|soil percolation coefficient (used in calibration)'
    tdrain: hr            |design subsurface tile drain time (used in calibration)
    stress: frac          |plant stress - pest, root restriction, soil quality, nutrient,
    uslefac: '|(non water, temp) (used in calibration)

      |USLE slope length factor'
    wrt1: Curve-number water retention parameter used in the CN runoff formulation.
    wrt2: Curve-number water retention parameter used in the CN runoff formulation.
    smx: Maximum soil water storage parameter derived from curve-number calculations.
    hk: Soil hydraulic conductivity/state factor carried in the dynamic HRU-LTE record.
    yls: Sediment yield slope-related factor stored for later erosion and yield calculations.
    ylc: Sediment yield cover-related factor stored for later erosion and yield calculations.
    awc: mm/mm        |available water capacity of soil
    g: Cumulative plant growth progress used by the daily control routine.
    hufh: Harvest/heat-unit style growth helper state tracked during the season.
    phu: Potential heat units accumulated toward crop development.
    por: Soil porosity used in water-balance calculations and runoff response.
    sc: Soil condition or soil-water calibration state carried in the dynamic object.
    sw: mm/mm         |initial soil water storage
    gw: mm            |initial shallow aquifer storage
    snow: mm            |initial water content of snow
    gwflow: mm            |initial groundwater flow
    gro: '|y=plant growing; n=not growing;'
    dm: t/ha          |plant biomass
    alai: '|leaf area index'
    yield: t/ha          |plant yield
    npp: t/ha          |net primary productivity
    lai_mx: '|maximum leaf area index'
    gwdeep: mm            |deep aquifer storage
    aet: mm            |sum of actual et during growing season (for hi water stress)
    pet: mm            |sum of potential et during growing season (for hi water stress)
    start: Integer day or code marking the start of the growing or management season.
    end: Integer day or code marking the end of the growing or management season.
type_summaries:
  swatdeg_hru_data: Persistent HRU-LTE input record for one landscape element. It stores the
    static database values read from `hru-lte.hru` that define area, soil, groundwater, vegetation,
    irrigation, and erosion properties for the corresponding HRU-LTE object.
  swatdeg_hru_dynamic: Live HRU-LTE state record for one routed object. It mirrors the database
    properties needed at runtime and adds evolving simulation state such as soil water, groundwater,
    growth, yield, seasonal dates, and calibration/tracking fields.
---

<!-- facts:header -->

hru_lte_module owns the shared HRU-LTE calibration and dynamic state used by SWAT+ for long-term landscape elements. It provides the persistent HRU-LTE database `hlt_db`, the live per-object state `hlt`, and the saved baseline copy `hlt_init`, along with calibration helper arrays `awct`, `port`, and `scon`. Startup and reset routines populate these variables from the HRU-LTE input file and restore them for calibration reruns; daily control, routing, calibration, and output routines depend on them.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it contains no procedures and no contained initialization logic. Its arrays are populated by external routines: `hru_lte_read` allocates and fills `hlt_db` and `hlt`, `cal_allo_init` snapshots `hlt` into `hlt_init`, and `re_initialize` restores `hlt` from `hlt_init`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `awct, port, scon, hlt_db, hlt, hlt_init` | Manages HRU-LTE grow-init and grow-end actions by setting `hlt` growth flags and resetting or using live season state. |
| [sym:cal_allo_init] | `none extracted` | `awct, port, scon, hlt_db, hlt, hlt_init` | Allocates `hlt_init` and copies `hlt` into it so calibration can preserve the current HRU-LTE baseline. |
| [sym:cal_parm_select] | `none extracted` | `awct, port, scon, hlt_db, hlt, hlt_init` | Adjusts LTE calibration parameters in `hlt_db` and `hlt`, including CN2, ET coefficient, soil depth, slope, slope length, tile drain time, and related values. |
| [sym:calsoft_control] | `unit_4999, unit_5001, unit_5000` | `awct, port, scon, hlt_db, hlt, hlt_init` | Reads and writes HRU-LTE soft-calibration summaries, using `hlt` and `hlt_db` to print the current LTE parameter state. |
| [sym:calsoft_read_codes] | `codes.sft` | `awct, port, scon, hlt_db, hlt, hlt_init` | Imports the module because the soft-calibration code set includes an HRU-LTE hydrologic flag, though the routine itself only reads the flag file. |
| [sym:caltsoft_hyd] | `unit_4304` | `awct, port, scon, hlt_db, hlt, hlt_init` | Uses `hlt` and `hlt_init` to rerun HRU-LTE hydrologic calibration cases from the saved baseline state. |
| [sym:command] | `unit_out_hyd_sep` | `awct, port, scon, hlt_db, hlt, hlt_init` | Routes HRU-LTE control and output work through `hru_lte_control` and `hru_lte_output`, which depend on `hlt` and `hlt_db`. |
| [sym:hru_lte_control] | `unit_4700, unit_4701` | `awct, port, scon, hlt_db, hlt, hlt_init` | Reads the live HRU-LTE object state and database properties to compute the daily water balance, growth, and sediment response. |
| [sym:hru_lte_read] | `hru-lte.hru` | `awct, port, scon, hlt_db, hlt, hlt_init` | Loads the HRU-LTE database file, allocates `hlt_db` and `hlt`, and derives each object's live state from the input records. |
| [sym:lcu_read_softcal] | `water_balance.sft` | `awct, port, scon, hlt_db, hlt, hlt_init` | Imports the module as part of the soft-calibration data setup used by landscape and HRU-LTE calibration structures. |
| [sym:soil_lte_db_read] | `soils_lte.sol` | `awct, port, scon, hlt_db, hlt, hlt_init` | Loads the LTE soil database first so HRU-LTE setup can rely on populated soil-related shared state. |
| [sym:time_control] | `unit_*, unit_9003, unit_5100, unit_5101, unit_8000, unit_8001` | `awct, port, scon, hlt_db, hlt, hlt_init` | Drives daily and annual control flow that calls HRU-LTE control and summaries, both of which use the module's live and saved state. |

## Key Consumers

The module is used by HRU-LTE setup, daily control, calibration, routing, and summary routines. Setup code loads `hlt_db` and allocates `hlt`; daily control and actions update `hlt`; calibration code reads and edits both `hlt_db` and `hlt`; routing and output code read `hlt_db` timing and live HRU-LTE state; reset code restores `hlt_init` back into `hlt`.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_allo_init] | hru_lte_module | Allocates `hlt_init` and snapshots the current `hlt` state so calibration reruns start from a preserved HRU-LTE baseline. |
| [sym:cal_parm_select] | hru_lte_module | Updates LTE database and live-object parameters such as curve number, soil depth, slope, slope length, ET coefficient, and tile timing for calibration cases. |
| [sym:hru_lte_control] | hru_lte_module | Reads the HRU-LTE database and live state to compute the daily water balance, crop growth, and sediment response for one object. |
| [sym:hru_lte_read] | hru_lte_module | Allocates and fills `hlt_db` and `hlt` from the HRU-LTE input file, establishing the shared persistent and dynamic state used later in the model. |
| [sym:calsoft_read_codes] | hru_lte_module | Provides the HRU-LTE symbols needed by the soft-calibration framework when hydrologic LTE calibration is enabled. |
| [sym:lcu_read_softcal] | hru_lte_module | Supplies the HRU-LTE symbols that share the same landscape-calibration framework used when soft-calibration regions are read. |
| [sym:soil_lte_db_read] | hru_lte_module | Provides shared LTE state used during the LTE-HRU input setup phase after the soil database is populated. |
| [sym:dr_ru] | hru_lte_module | Provides the HRU-LTE travel-time database so `dr_ru` can derive routing-element delivery ratios from `hlt_db(ihru)%tc` for `hlt` objects. |
| [sym:re_initialize] | hru_lte_module | Restores `hlt` from `hlt_init` so HRU-LTE objects return to their saved baseline before another simulation or calibration pass. |
| [sym:cal_conditions] | hru_lte_module | Imported by the calibration dispatcher, but no resolved outside references were identified in the provided source context. |
| [sym:calsoft_ave_output] | hru_lte_module | Provides the HRU-LTE branch state that soft-calibration averaging uses when the hydrologic LTE path is active. |
| [sym:calsoft_sum_output] | hru_lte_module | Provides `hltwb_y` and `hltls_y`, which supply yearly HRU-LTE water-balance and sediment totals for soft-calibration summaries. |
| [sym:actions] | hru_lte_module | Sets HRU-LTE growing-season state in `hlt`, turning growth on and resetting growth accumulators at season start and using the stored season totals at season end. |
| [sym:calsoft_control] | hru_lte_module | Uses `hlt` and `hlt_db` when writing HRU-LTE soft-calibration control and parameter summaries. |
| [sym:caltsoft_hyd] | hru_lte_module | Restores `hlt` from `hlt_init` and reuses the live HRU-LTE state while iterating hydrologic calibration adjustments. |
| [sym:command] | hru_lte_module | Dispatches HRU-LTE daily control and output routines that read the module's live and persistent HRU-LTE state. |
| [sym:time_control] | hru_lte_module | Coordinates model-day progression so HRU-LTE control, output, and calibration summaries can use the module's shared state at the correct times. |
| [sym:calsoft_hyd] | hru_lte_module | Reuses the HRU-LTE database and live state when applying hydrologic soft-calibration updates. |
| [sym:calsoft_hyd_bfr] | hru_lte_module | Calls the HRU-LTE hydrologic calibration branches that operate on the shared HRU-LTE state. |
| [sym:calsoft_hyd_bfr_et] | hru_lte_module | Applies the HRU-LTE calibration branch for ET-related hydrologic adjustments using the shared LTE object state. |
| [sym:calsoft_hyd_bfr_latq] | hru_lte_module | Applies the HRU-LTE calibration branch for lateral-flow adjustments using the shared LTE object state. |
| [sym:calsoft_hyd_bfr_perc] | hru_lte_module | Applies the HRU-LTE calibration branch for percolation adjustments using the shared LTE object state. |
| [sym:calsoft_hyd_bfr_pet] | hru_lte_module | Applies the HRU-LTE calibration branch for potential-ET adjustments using the shared LTE object state. |
| [sym:calsoft_hyd_bfr_surq] | hru_lte_module | Applies the HRU-LTE calibration branch for surface-runoff adjustments using the shared LTE object state. |

## Lineage

`hru_lte_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `889136d` (2025-02-03, "Fix typos"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_lte_module.f90` are listed.

- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `35b029c` (2024-03-24) — Mar 19 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `hru_lte_module` has no extracted module-level documentation comment.
- The source excerpt shows no contained procedures; this is a shared-state module only.
- Some component meanings are inferred from usage sites and may need human review, especially `awct`, `port`, `scon`, `g`, `hufh`, `phu`, `por`, `sc`, `wrt1`, `wrt2`, `smx`, `hk`, `yls`, and `ylc`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
