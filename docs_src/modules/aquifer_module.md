---
kind: module
symbol: aquifer_module
title: aquifer_module
status: filled
source_hash: d4104ecc72591c79
version_label: SWAT+ 62.0.0
variables:
  aqudb: Allocatable array of `aquifer_database` records read from `aquifer.aqu`; this is
    the persistent aquifer property table used by aquifer initialization, routing, chemistry,
    irrigation withdrawal, conditions, and calibration routines.
  aqu_dat: Allocatable working copy of `aquifer_database` records used as mutable aquifer
    properties during simulation. It is populated from `aqudb` in `aqu_initial` and then read
    by groundwater routing, chemistry, irrigation, and calibration routines.
  aqu_prm: Allocatable `aquifer_data_parameters` array holding derived per-aquifer parameters
    such as `area_ha`, `alpha_e`, `nloss`, and previous recharge trackers. It is initialized
    in `aqu_initial` and then used by routing, withdrawal, and output routines.
  aqu_om_init: Allocatable initial snapshot of `aquifer_dynamic` state used as the calibration/reset
    baseline. It is populated in `aqu_initial` and copied back into `aqu_d` by `cal_allo_init`;
    `re_initialize` references it as saved aquifer state.
  aqu_d: Allocatable daily working aquifer dynamic state for each aquifer object. It carries
    storage, depth to water, recharge, seepage, revap, flows, and chemistry masses, and is
    updated by routing, chemistry, irrigation, calibration, and condition checks.
  aqu_m: Allocatable monthly aquifer dynamic accumulator. It is filled from `aqu_d` by aquifer
    reporting routines and printed or reset at month end.
  aqu_y: Allocatable yearly aquifer dynamic accumulator. It is filled from monthly values
    and printed or reset at year end.
  aqu_a: Allocatable average-annual aquifer dynamic accumulator. It stores the simulation-long
    summary values written by aquifer output routines.
  saqu_d: Allocatable daily aquifer-region dynamic array used for aquifer region output or
    calibration tables.
  saqu_m: Allocatable monthly aquifer-region dynamic array used for aquifer region output
    or calibration tables.
  saqu_y: Allocatable yearly aquifer-region dynamic array used for aquifer region output or
    calibration tables.
  saqu_a: Allocatable average-annual aquifer-region dynamic array used for aquifer region
    output or calibration tables.
  baqu_d: Basin-scale daily aquifer summary record of type `aquifer_dynamic`. It is assembled
    from all aquifers as the basin aquifer daily output state.
  baqu_m: Basin-scale monthly aquifer summary record of type `aquifer_dynamic`. It accumulates
    daily basin aquifer values before monthly reporting.
  baqu_y: Basin-scale yearly aquifer summary record of type `aquifer_dynamic`. It accumulates
    monthly basin aquifer values before yearly reporting.
  baqu_a: Basin-scale average-annual aquifer summary record of type `aquifer_dynamic`. It
    stores the long-term basin aquifer aggregate for final reporting.
  aquz: Zero-valued `aquifer_dynamic` template used to reset aquifer accumulators and initialize
    basin summary records.
  aqu_init_dat_c: Allocatable character crosswalk records from `initial.aqu`; each record
    names the initial organic-mineral, pesticide, pathogen, heavy-metals, and salt input files
    associated with an aquifer initial-condition name.
  aqu_init_dat_c_cs: Allocatable character crosswalk records from `initial.aqu_cs`; each record
    maps an aquifer initial-condition name to pesticide, pathogen, heavy-metals, salt, and
    constituent initial files.
  aqu_init: Allocatable integer crosswalk records derived from `initial.aqu`; each record
    stores the integer selection indices for the initial organic-mineral, pesticide, pathogen,
    heavy-metals, salt, and constituent files.
  aqu_hdr: Shared aquifer output column-name header record written to aquifer day, month,
    year, and average-annual output files.
  aqu_hdr_units: Shared aquifer output units header record written alongside `aqu_hdr` in
    aquifer output files.
type_components:
  aquifer_database:
    aqunm: Aquifer name.
    aqu_ini: Name of the matching initial-condition record in `initial.aqu`.
    flo: Current aquifer flow parameter in mm.
    dep_bot: Depth from mid-slope surface to the aquifer bottom, in m.
    dep_wt: Initial depth from mid-slope surface to the water table, in m.
    no3: Initial nitrate-N concentration in the aquifer, in ppm.
    minp: Initial mineral phosphorus concentration in the aquifer, in ppm.
    cbn: Initial organic carbon fraction in the aquifer, in percent.
    flo_dist: Average flow distance to stream or object, in m.
    bf_max: Maximum daily baseflow when all channels contribute, in mm.
    alpha: Groundwater recession lag factor, in 1/days.
    revap_co: Coefficient used to compute evapotranspiration as `pet*revap_co`.
    seep: Fraction of recharge that seeps from the aquifer.
    spyld: Aquifer specific yield, in m^3/m^3.
    hlife_n: Nitrogen half-life in groundwater, in days.
    flo_min: Water-table depth threshold for return flow, in m.
    revap_min: Water-table depth threshold for revap, in m.
  aquifer_data_parameters:
    area_ha: Aquifer surface area, in ha.
    alpha_e: '`Exp(-alpha)`, the exponential recession factor.'
    nloss: Nitrogen loss factor derived from half-life.
    rchrg_prev: Previous-day recharge, in m^3.
    rchrgn_prev: Previous-day nitrogen recharge, in m^3.
  aquifer_dynamic:
    flo: Lateral flow from the aquifer, in mm.
    dep_wt: Average depth from surface to water table, in m.
    stor: Aquifer water storage for the timestep, in mm.
    rchrg: Recharge entering the aquifer from other objects, in mm.
    seep: Seepage from the bottom of the aquifer, in mm.
    revap: Plant uptake and evaporation from the aquifer, in mm.
    no3_st: Current total NO3-N mass in the aquifer, in kg/ha N.
    minp: Mineral phosphorus transported in return flow, in kg/ha P.
    cbn: Organic carbon in the aquifer, currently static, in percent.
    orgn: Organic nitrogen in the aquifer, currently static, in kg/ha N.
    no3_rchg: Nitrate NO3-N flowing into the aquifer from another object, in kg/ha N.
    no3_loss: Nitrate NO3-N loss, in kg/ha.
    no3_lat: Nitrate loading to reaches in groundwater, in kg/ha N.
    no3_seep: Nitrate seepage to the next object, in kg/ha N.
    flo_cha: Surface runoff flowing into channels, in mm H2O.
    flo_res: Surface runoff flowing into reservoirs, in mm H2O.
    flo_ls: Surface runoff flowing into a landscape element, in mm H2O.
  aquifer_init_data_char:
    name: Crosswalk name matching `aqudb(iaqu)%aqu_ini`.
    org_min: Points to the initial organic-mineral input file.
    pest: Points to the initial pesticide input file.
    path: Points to the initial pathogen input file.
    hmet: Points to the initial heavy-metals input file.
    salt: Points to the initial salt input file.
  aquifer_init_data_char_cs:
    name: Crosswalk name matching `aqudb(iaqu)%aqu_ini`.
    pest: Points to the initial pesticide input file.
    path: Points to the initial pathogen input file.
    hmet: Points to the initial heavy-metals input file.
    salt: Points to the initial salt input file (`salt_aqu.ini`).
    cs: Points to the initial constituent input file (`cs_aqu.ini`).
  aquifer_init_data:
    org_min: Index of the initial organic-mineral input file.
    pest: Index of the initial pesticide input file.
    path: Index of the initial pathogen input file.
    hmet: Index of the initial heavy-metals input file.
    salt: Index of the initial salt input file.
    cs: Index of the initial constituent input file.
  aqu_header:
    day: Column label for day of year.
    mo: Column label for month.
    day_mo: Column label for day-of-month or day/month composite.
    yrc: Column label for year.
    isd: Column label for unit identifier.
    id: Column label for GIS identifier.
    name: Column label for aquifer name.
    flo: Flow output label.
    dep_wt: Depth-to-water label.
    stor: Storage label.
    rchrg: Recharge label.
    seep: Seepage label.
    revap: Revap label.
    no3_st: NO3 storage label.
    minp: Mineral phosphorus label.
    orgn: Organic nitrogen label.
    orgp: Organic phosphorus label.
    no3_rchg: NO3 recharge label.
    no3_loss: NO3 loss label.
    no3_lat: NO3 lateral loading label.
    no3_seep: NO3 seepage label.
    flo_cha: Channel flow label.
    flo_res: Reservoir flow label.
    flo_ls: Landscape flow label.
  aqu_header_units:
    day: Blank units field for day.
    mo: Blank units field for month.
    day_mo: Blank units field for day/month composite.
    yrc: Blank units field for year.
    isd: Blank units field for unit identifier.
    id: Blank units field for GIS identifier.
    name: Blank units field for aquifer name.
    flo: Units label `mm`.
    depwt: Units label `m`.
    stor: Units label `mm`.
    rchrg: Units label `mm`.
    seep: Units label `mm`.
    revap: Units label `mm`.
    no3_st: Units label `kg/ha_N`.
    minp: Units label `kg/ha_P`.
    orgn: Units label `kg/ha_N`.
    orgp: Units label `kg/ha_P`.
    no3_rchg: Units label `kg/ha_N`.
    no3_loss: Units label `kg/ha_N`.
    no3_lat: Units label `kg/ha_N`.
    no3_seep: Units label `kg/ha_N`.
    flo_cha: Units label `mm`.
    flo_res: Units label `mm`.
    flo_ls: Units label `mm`.
type_summaries:
  aquifer_database: One aquifer property record defining the static database values for a
    modeled aquifer object.
  aquifer_data_parameters: Derived per-aquifer parameter record used to carry area and lag/recharge
    helper values for routing calculations.
  aquifer_dynamic: Mutable aquifer water-balance and chemistry state for one aquifer object
    at a reporting or calculation step.
  aquifer_init_data_char: Character crosswalk record that links an aquifer initial-condition
    name to the source files used to seed organic-mineral, pesticide, pathogen, heavy-metals,
    and salt state.
  aquifer_init_data_char_cs: Character crosswalk record for aquifer initial conditions when
    salt and constituent initialization are both enabled.
  aquifer_init_data: Integer crosswalk record that stores the selected initial-condition indices
    for each aquifer.
  aqu_header: Aquifer output label row used for the day, month, year, and average-annual report
    files.
  aqu_header_units: Aquifer output units row paired with `aqu_header` for the report files.
---

<!-- facts:header -->

`aquifer_module` owns the aquifer object database, per-object parameter state, working aquifer dynamics, initial-condition crosswalk records, and aquifer output header templates. It is the shared state container for groundwater routing, aquifer chemistry, aquifer initialization, calibration setup, and aquifer reporting routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-operator container, not a standalone startup routine. Its allocatable arrays and header records are populated by reader/setup procedures such as `aqu_read`, `aqu_read_init`, `aqu_read_init_cs`, `aqu_read_elements`, `aqu_initial`, and `cal_allo_init`, which allocate, fill, or reset the shared aquifer state.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Uses aquifer storage and parameter state to compute aquifer-source irrigation withdrawals and update remaining aquifer storage and constituent mass. |
| [sym:aqu_cs_output] | `unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Reads aquifer constituent balance arrays and writes daily, monthly, yearly, and average-annual aquifer constituent outputs. |
| [sym:aqu_read] | `aquifer.aqu` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Reads aquifer property records from `aquifer.aqu` into `aqudb` during model setup. |
| [sym:aqu_read_elements] | `aqu_catunit.def, aqu_catunit.ele` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Allocates aquifer-region output arrays and loads aquifer region and element mapping tables. |
| [sym:aqu_read_init] | `initial.aqu` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Reads aquifer initial-condition crosswalk records and allocates the aquifer initial-data arrays. |
| [sym:aqu_read_init_cs] | `initial.aqu_cs` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Reads aquifer constituent initial-condition crosswalk records and populates starting pesticide, pathogen, salt, and constituent state. |
| [sym:aqu_salt_output] | `unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Reads aquifer salt-balance arrays and writes daily, monthly, yearly, and average-annual salt outputs. |
| [sym:aquifer_output] | `unit_2520, unit_2524, unit_2521, unit_2525, unit_2522, unit_2526, unit_2523, unit_2527` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Reads aquifer dynamic state and writes daily, monthly, yearly, and average-annual aquifer outputs. |
| [sym:basin_aquifer_output] | `unit_2090, unit_2094, unit_2091, unit_2095, unit_2092, unit_2096, unit_2093, unit_2097` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Reads aquifer parameter and dynamic state to build basin-scale daily, monthly, yearly, and average-annual aquifer summaries. |
| [sym:cal_allo_init] | `none resolved in packet` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Copies `aqu_om_init` into `aqu_d` to restore aquifer dynamic state for calibration startup. |
| [sym:cal_parm_select] | `none resolved in packet` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Adjusts aquifer database, dynamic, and parameter values during parameter-calibration selection. |
| [sym:caltsoft_hyd] | `unit_4304` | `aqudb, aqu_dat, aqu_prm, aqu_om_init, aqu_d, aqu_m` | Uses aquifer-related calibration state as part of the hydrologic soft-calibration workflow. |

## Key Consumers

The module is most heavily used by aquifer setup, daily groundwater routing, chemistry and salt/constituent accounting, output/header routines, calibration reset logic, and water-allocation workflows that need aquifer storage, concentration, or parameter state.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu_read] | aquifer_module | Provides the allocatable `aqudb` array that this routine allocates and fills from `aquifer.aqu`; later aquifer setup and routing routines consume the loaded database. |
| [sym:aqu_read_elements] | aquifer_module | Provides the aquifer-region state arrays `saqu_d`, `saqu_m`, `saqu_y`, and `saqu_a` that are allocated for region-level aquifer output and calibration mapping. |
| [sym:aqu_read_init] | aquifer_module | Provides the allocatable aquifer initial-condition arrays that this routine sizes and fills from `initial.aqu`. |
| [sym:aqu_read_init_cs] | aquifer_module | Provides the aquifer initialization crosswalk and working aquifer state used to match initial-condition names to aquifer objects and populate starting constituent masses. |
| [sym:aquifer_output] | aquifer_module | Provides the daily, monthly, yearly, annual, and zero-template aquifer dynamic records that this routine accumulates, averages, prints, and resets for aquifer output files. |
| [sym:basin_aquifer_output] | aquifer_module | Provides the aquifer parameter and dynamic state records used to build basin-scale daily, monthly, yearly, and average-annual aquifer summaries. |
| [sym:cal_allo_init] | aquifer_module | Provides the aquifer dynamic baseline array copied from `aqu_om_init` into `aqu_d` so calibration starts from the saved aquifer state. |
| [sym:cal_parm_select] | aquifer_module | Provides aquifer database, parameter, and dynamic storage fields that calibration cases update when aquifer properties or groundwater state are selected for change. |
| [sym:header_aquifer] | aquifer_module | Provides the shared aquifer header and unit records that are written into every aquifer output file before data rows are appended. |
| [sym:header_write] | aquifer_module | Provides the aquifer header and unit records written to basin aquifer output files so the file columns are labeled consistently. |
| [sym:aqu_cs_output] | aquifer_module | Provides the aquifer constituent balance arrays that this routine rolls from daily values into monthly, yearly, and average-annual output records. |
| [sym:aqu_salt_output] | aquifer_module | Provides the aquifer salt-balance arrays that this routine aggregates and writes for daily, monthly, yearly, and average-annual salt reporting. |
| [sym:cs_balance] | aquifer_module | Provides aquifer-related constituent state used when groundwater-flow coupling is off and basin constituent balances fall back to aquifer-module storage and loading fields. |
| [sym:salt_balance] | aquifer_module | Provides aquifer-related salt state in the dependency set, though the visible extracted calculations rely on salt-specific groundwater arrays rather than directly referenced aquifer-module symbols. |
| [sym:swift_output] | aquifer_module | Provides the declared aquifer-state dependency for SWIFT output generation, including aquifer-specific export files, even though no concrete aquifer symbol use was resolved in the excerpt. |
| [sym:aqu_1d_control] | aquifer_module | Provides the aquifer database, parameters, and dynamic state that this controller updates for recharge, storage, flow, seepage, revap, and nitrogen/phosphorus transport. |
| [sym:aqu_initial] | aquifer_module | Provides the aquifer arrays that are allocated, initialized from `aqudb`, and seeded with starting dynamic values for simulation startup. |
| [sym:conditions] | aquifer_module | Provides aquifer depth state used by the `aqu_dep` condition to compare current water-table depth against the configured threshold. |
| [sym:cs_irrig] | aquifer_module | Provides aquifer storage used to convert irrigation withdrawal volume into groundwater constituent mass removal and updated aquifer concentration. |
| [sym:cs_rctn_aqu] | aquifer_module | Provides aquifer storage and nitrate state used in the groundwater reaction step that updates dissolved concentrations and nitrate mass. |
| [sym:cs_sorb_aqu] | aquifer_module | Provides aquifer storage, aquifer geometry, and specific-yield state needed to compute groundwater volume and sorption mass conversions. |
| [sym:re_initialize] | aquifer_module | Provides aquifer initialization state that is preserved for reruns; the extracted branch shows the saved aquifer state being left unchanged. |
| [sym:salt_chem_aqu] | aquifer_module | Provides aquifer storage used to compute groundwater volume for salt-concentration to mass conversions and back-conversions. |
| [sym:salt_irrig] | aquifer_module | Provides aquifer storage used to convert irrigation withdrawal volume into remaining aquifer salt mass and updated salt concentration. |

## Lineage

`aquifer_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `aquifer_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment was extracted from the source.
- `all_importers` is preserved as the deterministic full importer list from the context packet.
- Lineage evidence reported no resolved commits for this source span.
- The procedure set shows three contained operators (`aqu_add`, `aqu_div`, `aqu_mult`) but no module-level callable initialization routine within `aquifer_module` itself.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
