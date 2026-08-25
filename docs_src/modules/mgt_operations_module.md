---
kind: module
symbol: mgt_operations_module
title: mgt_operations_module
status: filled
source_hash: 6bd9ab346bd25d6d
version_label: SWAT+ 62.0.0
variables:
  irrop_db: Allocatable database of `irrigation_operation` records defined by `mgt_operations_module`
    and populated by `mgt_read_irrops`. Each record holds irrigation name, application amount
    in mm, in-field efficiency, surface runoff ratio, subsurface application depth, and salt/nutrient
    concentrations. It is consumed by irrigation and water-allocation logic such as `actions`,
    `water_allocation_read`, and `dtbl_lum_read`.
  pudl_db: Allocatable database of `puddle_operation` records defined here and populated by
    `mgt_read_puddle`. Each record stores the puddling name and modified near-surface hydraulic
    and constituent values. It is used by management actions and decision-table crosswalks
    that reference puddling operations.
  filtstrip_db: Allocatable database of `filtstrip_operation` records owned by this module
    and filled by `scen_read_filtstrip`. Records hold the vegetative filter-strip flag and
    runoff-routing factors. It is used by land-use setup, structure parameter setup, and management
    decision-table crosswalks.
  fire_db: Allocatable database of `fire_operation` records owned by this module and populated
    by `mgt_read_fireops`. Each record stores the fire operation name, curve-number update,
    and fraction burned. It is used by burn-management routines such as `actions`, `pl_burnop`,
    and `dtbl_lum_read`.
  grwaterway_db: Allocatable database of `grwaterway_operation` records owned by this module
    and populated by `scen_read_grwway`. Records store grassed-waterway simulation flags and
    geometric/transport parameters. It is used by land-use setup and management crosswalks
    that need grassed-waterway definitions.
  bmpuser_db: Allocatable database of `bmpuser_operation` records owned by this module and
    populated by `scen_read_bmpuser`. Each record stores a BMP name, on/off flag, and removal
    efficiencies for sediment, phosphorus, nitrogen, and bacteria. It is consumed by land-use
    setup, structure parameter setup, and management actions.
  chemapp_db: Allocatable database of `chemical_application_operation` records owned by this
    module and populated by `mgt_read_chemapp`. Each record stores the chemical application
    name, form, application type, efficiencies, injection depth, surface fraction, drift potential,
    and aerial uniformity. It is used by fertilizer, manure, pesticide, and chemical-application
    management routines, including `cs_fert`, `pl_fert`, `pl_manure`, `pest_apply`, and decision-table
    readers.
  harvop_db: Allocatable database of `harvest_operation` records owned by this module and
    populated by `mgt_read_harvops`. Each record stores the harvest name, crop type, harvest-index
    override, harvest efficiency, and minimum biomass threshold. It is consumed by harvest-management
    routines such as `actions`, `mgt_harvbiomass`, `mgt_harvgrain`, `mgt_harvresidue`, `mgt_harvtuber`,
    `dtbl_lum_read`, and `read_mgtops`.
  harvop: A single working `harvest_operation` record in module state. It is available as
    a shared scratch/current-operation object for harvest management logic and mirrors the
    same field structure as `harvop_db`.
  hkop: A second single working `harvest_operation` record in module state. It provides another
    shared harvest-operation slot for routines that need a separate harvest-kill or alternative
    harvest record.
  grazeop_db: Allocatable database of `grazing_operation` records owned by this module and
    populated by `mgt_read_grazeops`. Each record stores the grazing name, fertilizer name,
    manure fertilizer cross-reference, grazing/trampling/manure rates, and minimum biomass.
    It is used by grazing routines and decision-table crosswalks.
  graze: A single working `grazing_operation` record in module state. It is the shared current
    grazing-operation object used by grazing management logic and action execution.
  sweepop_db: Allocatable database of `streetsweep_operation` records owned by this module
    and populated by `mgt_read_sweepops`. Records store the sweep operation name, efficiency,
    and curb availability factor. It is used by street-sweeping management routines and decision-table
    crosswalks.
  sweepop: A single working `streetsweep_operation` record in module state. It serves as the
    shared current street-sweep operation object used by management execution code.
  mgt: A shared working `management_ops` record that holds the active management action being
    evaluated or executed. It stores the operation name, operation code, calendar fields,
    heat-unit trigger, operation text, and numeric cross-reference fields used by management
    dispatch routines.
  mgt1: A second shared `management_ops` record used as module-level scratch/current-operation
    state. It has the same fields as `mgt` and can hold a separate management record when
    needed by execution logic.
  mgt2: A one-element `management_ops` array used as a shared module-level management record
    container. It provides an indexed slot for routines that expect an array form of the current
    management operation.
  sched: Allocatable database of `management_schedule` records owned by this module and populated
    by `mgt_read_mgtops`. Each schedule stores the schedule name, operation counts, auto-operation
    names, linked decision-table indices, crop lists, and irrigation flag. It is the central
    schedule database used by `cal_allo_init`, `conditions`, `hru_control`, `mgt_operatn`,
    `proc_cond`, `read_mgtops`, `plant_init`, and `cal_allo_init`-style setup routines.
type_components:
  irrigation_operation:
    name: Operation name used to crosswalk text pointers to an irrigation record.
    amt_mm: Application amount in millimeters applied by the irrigation operation.
    eff: In-field irrigation efficiency used to reduce the applied amount.
    surq: Fraction of applied irrigation routed to surface runoff.
    dep_mm: Depth of application for subsurface irrigation.
    salt: Concentration of total salt in the irrigation water, in mg/kg.
    no3: Concentration of nitrate in the irrigation water, in mg/kg.
    po4: Concentration of phosphate in the irrigation water, in mg/kg.
  puddle_operation:
    name: Operation name used to identify the puddling record.
    wet_hc: Hydraulic conductivity of the upper soil layer after puddling, in mm/h.
    sed: Sediment concentration after puddling, in ppm.
    orgn: Organic nitrogen concentration after puddling, in ppm.
    sedp: Organic phosphorus concentration after puddling, in ppm.
    no3: NO3-N concentration after puddling, in ppm.
    solp: Mineral soluble phosphorus concentration after puddling, in ppm.
    nh3: NH3 concentration after puddling, in ppm.
    no2: NO2 concentration after puddling, in ppm.
  filtstrip_operation:
    name: Operation name used to crosswalk the filter-strip record.
    vfsi: On/off flag for the vegetative filter strip.
    vfsratio: Contouring USLE P factor used by the filter strip.
    vfscon: Fraction of the total runoff from the entire field routed through the filter strip.
    vfsch: Fraction of flow entering the most concentrated 10% of the VFS.
  fire_operation:
    name: Operation name used to identify the burn record.
    cn2_upd: Change in SCS curve number II value caused by the burn.
    fr_burn: Fraction of biomass or surface material burned.
  grwaterway_operation:
    name: Operation name used to crosswalk the grassed-waterway record.
    grwat_i: On/off flag for waterway simulation.
    grwat_n: Manning's n for the grassed waterway.
    grwat_spcon: Sediment transport coefficient defined by the user.
    grwat_d: Depth of the grassed waterway, in meters.
    grwat_w: Width of the grass waterway.
    grwat_l: Length of the grassed waterway, in kilometers.
    grwat_s: Slope of the grass waterway, in m/m.
  bmpuser_operation:
    name: Operation name used to identify the BMP record.
    bmp_flag: On/off flag for the BMP operation.
    bmp_sed: Sediment removal efficiency, in percent.
    bmp_pp: Particulate phosphorus removal efficiency, in percent.
    bmp_sp: Soluble phosphorus removal efficiency, in percent.
    bmp_pn: Particulate nitrogen removal efficiency, in percent.
    bmp_sn: Soluble nitrogen removal efficiency, in percent.
    bmp_bac: Bacteria removal efficiency, in percent.
  bmpuser_operation1:
    name: Operation name used to identify the BMP record.
    bmp_flag: On/off flag for the BMP operation.
    surf_flo: Surface flow removal efficiency, in percent.
    surf_sed: Surface sediment removal efficiency, in percent.
    surf_pp: Surface particulate phosphorus removal efficiency, in percent.
    surf_sp: Surface soluble phosphorus removal efficiency, in percent.
    surf_pn: Surface particulate nitrogen removal efficiency, in percent.
    surf_sn: Surface soluble nitrogen removal efficiency, in percent.
    surf_bac: Surface bacteria removal efficiency, in percent.
    sub_flo: Subsurface flow removal efficiency, in percent.
    sub_sed: Subsurface sediment removal efficiency, in percent.
    sub_pp: Subsurface particulate phosphorus removal efficiency, in percent.
    sub_sp: Subsurface soluble phosphorus removal efficiency, in percent.
    sub_pn: Subsurface particulate nitrogen removal efficiency, in percent.
    sub_sn: Subsurface soluble nitrogen removal efficiency, in percent.
    sub_bac: Subsurface bacteria removal efficiency, in percent.
    tile_flo: Tile flow removal efficiency, in percent.
    tile_sed: Tile sediment removal efficiency, in percent.
    tile_pp: Tile particulate phosphorus removal efficiency, in percent.
    tile_sp: Tile soluble phosphorus removal efficiency, in percent.
    tile_pn: Tile particulate nitrogen removal efficiency, in percent.
    tile_sn: Tile soluble nitrogen removal efficiency, in percent.
    tile_bac: Tile bacteria removal efficiency, in percent.
  chemical_application_operation:
    name: Operation name used to crosswalk the application record.
    form: Application form, such as solid or liquid.
    op_typ: Application type, such as spread, spray, inject, or direct.
    app_eff: Application efficiency.
    foliar_eff: Foliar efficiency.
    inject_dep: Injection depth, in mm.
    surf_frac: Surface fraction applied to the upper 10 mm.
    drift_pot: Drift potential.
    aerial_unif: Aerial uniformity.
  harvest_operation:
    name: Operation name used to identify the harvest record.
    typ: Harvest type, such as grain, biomass, residue, tree, or tuber.
    hi_ovr: Harvest index override, expressed as a ratio of harvested yield to total biomass.
    eff: Harvest efficiency, the fraction of harvested yield that is removed.
    bm_min: Minimum biomass required before harvest is allowed.
  grazing_operation:
    name: Operation name used to identify the grazing record.
    fertnm: Fertilizer name associated with the manure source.
    manure_id: Fertilizer number from `fertilizer.frt` used as a cross-reference.
    eat: Dry biomass removed by grazing each day, in kg/ha/day.
    tramp: Dry biomass removed by trampling each day, in kg/ha/day.
    manure: Dry manure deposited each day, in kg/ha/day.
    biomin: Minimum plant biomass required for grazing, in kg/ha.
  streetsweep_operation:
    name: Operation name used to identify the sweeping record.
    eff: Removal efficiency of the sweeping operation.
    fr_curb: Availability factor, the fraction of curb length that is sweepable.
  management_ops:
    name: Operation name used by schedules and crosswalks.
    op: Operation code or text tag describing the action type.
    mon: Month field used with the schedule date. The comments enumerate operation codes such
      as plant, harvest, kill, tillage, irrigation, fertilizer, pesticide, grazing, burn,
      street sweep, print plant variables, and skip.
    day: Day-of-month field for the scheduled operation.
    jday: Julian day-of-year derived from the month/day pair.
    year: Management year assigned to the operation as the schedule is read.
    husc: Heat-unit trigger used to schedule the operation on plant development.
    op_char: String field holding the operation character code or related text.
    op_plant: String field holding the plant name or operation plant label.
    op1: Primary database index resolved for the operation target.
    op2: Plant number in the community for heat-unit scheduling.
    op3: Application amount in mm or kg/ha.
    op4: Fertilizer or pesticide type index pointing to the corresponding database.
  management_schedule:
    name: Schedule name.
    num_ops: Number of scheduled operations in the schedule.
    num_autos: Number of automatic or decision-table-driven operations.
    first_op: Index of the first operation to execute.
    mgt_ops: Allocatable array of `management_ops` records for this schedule.
    auto_name: Allocatable array of automatic operation names.
    auto_crop: Allocatable array of crop names associated with a generic automatic operation.
    auto_crop_num: Number of crop-name entries stored in `auto_crop`.
    num_db: Allocatable array of linked decision-table or database indices for automatic operations.
    irr: Flag set when the schedule contains irrigation-related automatic operations.
type_summaries:
  irrigation_operation: One irrigation-operation database record describing how a named irrigation
    action applies water and associated constituents.
  puddle_operation: One puddling-operation database record defining the post-puddling near-surface
    soil conditions for a named operation.
  filtstrip_operation: One vegetative-filter-strip operation record describing whether a filter
    strip is active and how it partitions runoff.
  fire_operation: One prescribed-burn operation record defining the effect of a named burn
    action on curve number and burned fraction.
  grwaterway_operation: One grassed-waterway operation record describing whether the feature
    is active and what geometry and routing parameters it uses.
  bmpuser_operation: One user-defined BMP operation record describing a named BMP and its
    removal efficiencies for major pollutants.
  bmpuser_operation1: Alternate user-defined BMP operation record that separates removal efficiencies
    by flow path.
  chemical_application_operation: One chemical-application operation record describing how
    a fertilizer, pesticide, or manure is applied.
  harvest_operation: One harvest-operation record describing a named harvest action and its
    removal limits.
  grazing_operation: One grazing-operation record describing the grazing and manure rates
    for a named grazing action.
  streetsweep_operation: One street-sweeping operation record describing removal efficiency
    and curb availability for a named sweeping action.
  management_ops: One scheduled management operation record containing a date, operation code,
    and database cross-references used during execution.
  management_schedule: One management-schedule record holding a named schedule, its operation
    counts, auto-operation metadata, and linked operation database indices.
---

<!-- facts:header -->

`mgt_operations_module` owns the shared management-operation databases and record types used across SWAT+ management, decision-table, and water-allocation workflows. It defines the allocatable operation tables for irrigation, puddling, filter strips, fire, grassed waterways, user BMPs, chemical applications, harvest, grazing, and street sweeping, plus the active management-operation and schedule records that other routines populate, crosswalk, and execute.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-shared-state container rather than a computational routine module. Its allocatable databases and working records are populated by dedicated reader/setup procedures such as `mgt_read_irrops`, `mgt_read_puddle`, `mgt_read_chemapp`, `mgt_read_harvops`, `mgt_read_grazeops`, `mgt_read_sweepops`, `mgt_read_mgtops`, `scen_read_bmpuser`, `scen_read_filtstrip`, and `scen_read_grwway`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:mgt_read_irrops] | `irr.ops` | `irrop_db` | Allocates and fills the shared irrigation-operation database from the irrigation operations file, publishing the record count for later management use. |
| [sym:mgt_read_puddle] | `puddle.ops` | `pudl_db` | Allocates and fills the shared puddling-operation database from the puddling file, making the loaded puddle records available to management code. |
| [sym:mgt_read_chemapp] | `chem_app.ops` | `chemapp_db` | Allocates and fills the shared chemical-application database from the chemical application operations file. |
| [sym:mgt_read_harvops] | `harv.ops` | `harvop_db` | Allocates and fills the shared harvest-operation database from the harvest-only operations file. |
| [sym:mgt_read_grazeops] | `graze.ops` | `grazeop_db` | Allocates and fills the shared grazing-operation database and crosswalks each grazing record to a fertilizer index. |
| [sym:mgt_read_fireops] | `fire.ops` | `fire_db` | Allocates and fills the shared fire-operation database from the fire operations file. |
| [sym:mgt_read_sweepops] | `sweep.ops` | `sweepop_db` | Allocates and fills the shared street-sweeping database from the sweep operations file. |
| [sym:mgt_read_mgtops] | `management.sch` | `sched` | Allocates and fills the shared management-schedule database, including schedule names, operation counts, auto-operation names, crop lists, and linked database indices. |
| [sym:scen_read_bmpuser] | `bmpuser.str` | `bmpuser_db` | Allocates and fills the shared user-BMP database from the BMP definition file. |
| [sym:scen_read_filtstrip] | `filterstrip.str` | `filtstrip_db` | Allocates and fills the shared filter-strip database from the scenario/structure file. |
| [sym:scen_read_grwway] | `grassedww.str` | `grwaterway_db` | Allocates and fills the shared grassed-waterway database from the scenario/structure file. |
| [sym:read_mgtops] | `unit_107` | `sched` | Decodes one schedule's operations into calendar fields and database indices after `mgt_read_mgtops` has allocated the schedule array. |

## Key Consumers

This module is used primarily by management schedulers, decision-table readers, HRU control, land-use setup, calibration setup, and application routines that need the shared operation databases or current management records.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_allo_init] | mgt_operations_module | Uses `sched` to size each HRU's auto-operation table and allocate the matching per-table action counters before calibration work begins. |
| [sym:dtbl_lum_read] | mgt_operations_module | Uses the operation databases to crosswalk decision-table action text into numeric references for harvest, irrigation, chemical application, grazing, puddling, and fire actions. |
| [sym:hru_dtbl_actions_init] | mgt_operations_module | Uses `sched` and `chemapp_db` to allocate per-HRU decision-table action slots and to map future fertilizer actions to chemical-application records. |
| [sym:landuse_read] | mgt_operations_module | Uses `sched`, `filtstrip_db`, `grwaterway_db`, and `bmpuser_db` to resolve land-use pointer names to database indices. |
| [sym:manure_allocation_read] | mgt_operations_module | Uses `chemapp_db` to translate a manure decision-table option into the chemical-application method index stored on each demand object. |
| [sym:mgt_read_chemapp] | mgt_operations_module | Fills the shared `chemapp_db` array with parsed chemical application records. |
| [sym:mgt_read_fireops] | mgt_operations_module | Fills the shared `fire_db` array with parsed fire-operation records. |
| [sym:mgt_read_grazeops] | mgt_operations_module | Fills the shared `grazeop_db` array and assigns each grazing record a fertilizer cross-reference. |
| [sym:mgt_read_harvops] | mgt_operations_module | Fills the shared `harvop_db` array with parsed harvest-operation records. |
| [sym:mgt_read_irrops] | mgt_operations_module | Fills the shared `irrop_db` array with parsed irrigation-operation records. |
| [sym:mgt_read_mgtops] | mgt_operations_module | Allocates and fills the shared `sched` database with management schedules and their auto-operation metadata. |
| [sym:mgt_read_puddle] | mgt_operations_module | Fills the shared `pudl_db` array with parsed puddling-operation records. |
| [sym:mgt_read_sweepops] | mgt_operations_module | Fills the shared `sweepop_db` array with parsed street-sweeping records. |
| [sym:plant_init] | mgt_operations_module | Uses `sched` to determine the first valid management operation and the current rotation year for plant initialization. |
| [sym:read_mgtops] | mgt_operations_module | Writes derived dates, operation pointers, and irrigation flags into `sched(isched)%mgt_ops(iop)` so later management logic can execute the schedule without repeated string matching. |
| [sym:scen_read_bmpuser] | mgt_operations_module | Fills the shared `bmpuser_db` array with parsed user BMP records. |
| [sym:scen_read_filtstrip] | mgt_operations_module | Fills the shared `filtstrip_db` array with parsed filter-strip records. |
| [sym:scen_read_grwway] | mgt_operations_module | Fills the shared `grwaterway_db` array with parsed grassed-waterway records. |
| [sym:water_allocation_read] | mgt_operations_module | Uses `irrop_db` to look up irrigation-operation parameters by name so the current transfer object can copy the matching efficiency and runoff split. |
| [sym:calsoft_read_codes] | mgt_operations_module | Imported as part of the shared management state context for calibration, but no direct symbol reference is shown in the extracted body. |
| [sym:dtbl_res_read] | mgt_operations_module | Uses the shared action structures and downstream databases to resolve reservoir release action pointers to numeric indices. |
| [sym:dtbl_scen_read] | mgt_operations_module | Uses the land-use and snow-change decision-table infrastructure shared by this module to resolve scenario actions to numeric indices. |
| [sym:om_osrc_read] | mgt_operations_module | Imported as part of the shared management-state context for outside-source records, but no concrete symbol usage is visible in the extracted lines. |
| [sym:om_treat_read] | mgt_operations_module | Imported as part of the shared treatment-management state context, but no concrete symbol usage is visible in the extracted lines. |

## Lineage

`mgt_operations_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `1807dbb` (2025-03-26, "na"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_operations_module.f90` are listed.

- `1807dbb` (2025-03-26) — na
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `mgt_operations_module` has no extracted module-level documentation comment.
- The importer list is complete and deterministic; the used_by table is a concise subset of the most informative consumers.
- No resolved Git lineage commits were available for this source span.
- Some reader/used-by effects are based on completed procedure overlays that reference the shared databases by name; where a procedure body was not fully extracted, the effect is limited to the visible references.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
