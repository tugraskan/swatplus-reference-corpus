---
kind: module
symbol: reservoir_data_module
title: reservoir_data_module
status: filled
source_hash: 48d0067cc1145a56
version_label: SWAT+ 62.0.0
variables:
  res_dat_c: Allocatable character-based reservoir lookup table. `res_read` fills it from
    `reservoir.res` so each reservoir's named inputs can be crosswalked to indices used by
    later reservoir setup and control.
  wet_dat_c: Allocatable character-based wetland lookup table. `wet_read` fills it from `wetland.wet`,
    and `actions` uses `wet_dat(ires)%name` / `wet_dat_c`-linked wetland pointers to resolve
    wetland objects during management actions.
  res_dat_c_cs: Allocatable character-based reservoir salt/constituent lookup table. `res_read_salt_cs`
    fills it from `reservoir.res_cs` so salt and constituent names can be converted to numeric
    links.
  wet_dat_c_cs: Allocatable character-based wetland salt/constituent lookup table. `wet_read_salt_cs`
    fills it from `wetland.wet_cs` so wetland salt and constituent names can be converted
    to numeric links.
  res_dat: Allocatable resolved reservoir record table. `res_read` fills its integer pointers
    from `res_dat_c`, `res_read_salt_cs` fills `salt` and `cs`, and downstream routines such
    as `res_control`, `res_initial`, `res_pest`, `res_cs`, and `dtbl_res_read` use it to find
    reservoir setup and release data.
  wet_dat: Allocatable resolved wetland record table. `wet_read` fills it from `wet_dat_c`,
    `wet_read_salt_cs` fills salt/constituent links, and downstream routines such as `wet_initial`,
    `et_act`, `hru_fr_change`, `actions`, and `swift_output` use it to find wetland setup
    and hydrology data.
  res_datz: Single default reservoir record used as a zero/working placeholder. The source
    shows it declared with type `reservoir_data`; no initializer routine was extracted for
    it in the packet.
  res_init_dat_c: Allocatable character-based reservoir initial-condition lookup table. `res_read_init`
    fills it from `initial.res`, and `res_read` uses it to crosswalk reservoir initial-condition
    names to indices.
  res_init: Allocatable resolved reservoir initial-condition table. `res_read_init` allocates
    and fills it, and `res_read`/`res_initial` use it to select organic-mineral, pesticide,
    pathogen, heavy-metal, salt, and constituent startup records.
  wet_init: Allocatable resolved wetland initial-condition table. `res_read_init` allocates
    it, and `wet_initial` uses it to select organic-mineral, pesticide, and pathogen startup
    records for wetlands.
  res_hyd: Allocatable reservoir hydrology table used by the simulation. `res_read_hyd` fills
    the shared database, `res_read` copies matched entries into the reservoir records, and
    `res_initial`, `res_control`, `res_hydro`, `cal_parm_select`, and `swift_output` use it
    for reservoir geometry and release behavior.
  res_hyddb: Allocatable reservoir hydrology database loaded from `hydrology.res`. `res_read_hyd`
    fills it and default-fixes missing geometry; `res_read` crosswalks reservoir hydrology
    names against it.
  wet_hyd: Allocatable wetland hydrology table used by the simulation. `wet_read_hyd` fills
    the shared database, `wet_initial` copies matched entries into wetland state, and `et_act`,
    `hru_fr_change`, `hru_allo`, `wetland_control`, and `swift_output` use it for wetland
    geometry and evaporation behavior.
  wet_hyddb: Allocatable wetland hydrology database loaded from `hydrology.wet`. `wet_read_hyd`
    fills it and applies defaults for missing spillway and evaporation settings.
  res_sed: Allocatable reservoir sediment parameter table. `res_read_sed` fills it from `sediment.res`;
    `res_initial`, `res_pest`, `cal_parm_select`, and reservoir sediment-processing routines
    use it for sediment density and settling properties.
  res_nut: Allocatable reservoir nutrient parameter table. `res_read_nut` fills it from `nutrients.res`
    and converts yearly rates to daily rates; `res_initial` and nutrient-process routines
    use it for settling and soluble-loss behavior.
  res_prm: Allocatable reservoir water-body parameter bundle. Each element embeds one `reservoir_sed_data`
    and one `reservoir_nut_data` record plus derived coefficients. `res_read` fills it from
    the reservoir lookup tables, `cal_parm_select` edits its fields, and `res_control`, `res_initial`,
    and `res_nutrient` use it as the shared reservoir parameter record.
  wet_prm: Allocatable wetland water-body parameter bundle. Each element embeds one `reservoir_sed_data`
    and one `reservoir_nut_data` record plus derived coefficients. `hru_allo`, `wet_initial`,
    `wetland_control`, and `hru_fr_change` use it for wetland parameter storage.
  wbody_prm: Pointer to the active water-body parameter bundle for the current reservoir or
    wetland. It is used by reservoir and wetland process routines to access the selected sediment
    and nutrient parameters for the object currently being updated.
  res_weir: Allocatable reservoir weir outflow table. `res_read_weir` fills it from `weir.res`;
    `dtbl_res_read`, `mgt_sched`, and `res_hydro` use it to resolve and compute weir-controlled
    releases.
type_components:
  reservoir_data_char_input:
    name: Reservoir or wetland name key used to match a row in the input file and later identify
      the object in lookup routines.
    init: initial data-points to initial.res
    hyd: points to hydrology.res for hydrology inputs
    release: 0=simulated; 1=measured outflow
    sed: sediment inputs-points to sediment.res
    nut: nutrient inputs-points to nutrient.res
  reservoir_data_char_input_cs:
    pst: pesticide inputs-points to pesticide.res
    weir: weir inputs-points to weir.res    Jaehak 2022
    salt: salt inputs - points to salt_res rtb salt
    cs: constituent inputs - points to cs_res rtb cs
  reservoir_data:
    name: Reservoir or wetland name key used for matching and reporting.
    init: initial data-points to initial.res
    hyd: points to hydrology.res for hydrology inputs
    release: 0=simulated; 1=measured outflow
    sed: sediment inputs-points to sediment.res
    nut: nutrient inputs-points to nutrient.res
    pst: pesticide inputs-points to pesticide.res
    salt: salt input-points to salt.res
    cs: constituent inputs-points to cs.res
    weir: weir inputs-points to weir.res  Jaehak 2022
  reservoir_init_data_char:
    init: initial data-points to initial.cha
    org_min: points to initial organic-mineral input file
    pest: points to initial pesticide input file
    path: points to initial pathogen input file
    hmet: points to initial heavy metals input file
    salt: points to initial salt input file
  reservoir_init_data:
    init: initial data-points to initial.cha
    org_min: points to initial organic-mineral input file
    pest: points to initial pesticide input file
    path: points to initial pathogen input file
    hmet: points to initial heavy metals input file
    salt: points to initial salt input file
    cs: points to initial constituent input file (rtb cs)
  reservoir_hyd_data:
    name: Reservoir or wetland name key used to match the hydrology record to a water body.
    iyres: none          |year of the sim that the res becomes operational
    mores: none          |month the res becomes operational
    psa: ha            |res surface area when res is filled to princ spillway
    pvol: ha-m          |vol of water needed to fill the res to the princ spillway (read in
      as ha-m
    esa: 'and converted to m^3)

      ha            |res surface area when res is filled to emerg spillway'
    evol: ha-m          |vol of water needed to fill the res to the emerg spillway (read in
      as ha-m
    k: 'and converted to m^3)

      mm/hr         |hydraulic conductivity of the res bottom'
    evrsv: none          |lake evap coeff
    br1: none          |vol-surface area coefficient for reservoirs (model estimates if zero)
    br2: none          |vol-surface area coefficient for reservoirs (model estimates if zero)
  wetland_hyd_data:
    name: Wetland or HRU storage name key used to match the hydrology record to an HRU wetland.
    psa: 'frac          |fraction of hru area at principal spillway (ie: when surface inlet
      riser flow starts)'
    pdep: mm            |average depth of water at principal spillway
    esa: 'frac          |fraction of hru area at emergency spillway (ie: when starts to spill
      into ditch)'
    edep: mm            |average depth of water at emergency spillway
    k: mm/hr         |hydraulic conductivity of the wetland bottom
    evrsv: none          |wetland evap coeff
    acoef: none          |vol-surface area coefficient for hru impoundment
    bcoef: none          |vol-depth coefficient for hru impoundment
    ccoef: none          |vol-depth coefficient for hru impoundment
    frac: none          |fraction of hru that drains into impoundment
  reservoir_sed_data:
    name: Reservoir or wetland name key for the sediment parameter row.
    nsed: kg/L       |normal amt of sed in res (read in as mg/L and convert to kg/L)
    d50: um         |median particle size of suspended and benthic sediment
    carbon: '%          |organic carbon in suspended and benthic sediment'
    bd: t/m^3      |bulk density of benthic sediment
    sed_stlr: none       |sediment settling rate
    velsetlr: m/d        |sediment settling velocity
  reservoir_nut_data:
    name: Reservoir or wetland name key for the nutrient parameter row.
    ires1: none       |beg of mid-year nutrient settling "season"
    ires2: none       |end of mid-year nutrient settling "season"
    nsetlr1: frac       |nit mass loss rate for mid-year period
    nsetlr2: frac       |nit mass loss rate for remainder of year
    psetlr1: frac       |phos mass loss rate for mid-year period
    psetlr2: frac       |phos mass loss rate for remainder of year
    nsolr: none       |loss rate for souble n - no3, nh3, no2
    psolr: none       |loss rate for soluble p
    theta_n: none       |temperature adjustment for nitrogen loss (settling)
    theta_p: none       |temperature adjustment for phosphorus loss (settling)
    conc_nmin: ppm        |minimum nitrogen concentration for settling
    conc_pmin: ppm        |minimum phosphorus concentration for settling
  water_body_data_parameters:
    sed: Reservoir sediment property record embedded for the active water body.
    nut: Reservoir nutrient property record embedded for the active water body.
    sed_stlr_co: none       |
    soln_stl_fr: none       |
    solp_stl_fr: none       |
  reservoir_weir_outflow:
    name: Weir name key used to match an action or management setting to a discharge row.
    c: none          |weir discharge linear coefficient
    k: none          |weir discharge exponential coefficient
    w: m             |width
    h: m             |height of weir above bottoom of impoundment
type_summaries:
  reservoir_data_char_input: Character lookup record for a reservoir or wetland entry. It
    stores the names of the initial-condition, hydrology, release, sediment, and nutrient
    inputs that will be crosswalked to numeric indices later.
  reservoir_data_char_input_cs: Character lookup record for reservoir or wetland salt and
    constituent links.
  reservoir_data: Resolved reservoir or wetland record. It stores numeric indices for the
    selected startup, hydrology, release, sediment, nutrient, pesticide, salt, and constituent
    records, plus the weir pointer string.
  reservoir_init_data_char: Character lookup record for reservoir initial-condition inputs.
    It names the initial organic-mineral, pesticide, pathogen, heavy-metal, and salt files
    that belong to one reservoir startup record.
  reservoir_init_data: Resolved reservoir initial-condition record. It stores numeric pointers
    to the selected organic-mineral, pesticide, pathogen, heavy-metal, salt, and optional
    constituent initial-condition records.
  reservoir_hyd_data: Reservoir hydrology and geometry record. It supplies activation timing,
    spillway areas and volumes, bottom conductivity, evaporation coefficient, and volume-area
    coefficients for reservoir routing and initialization.
  wetland_hyd_data: Wetland hydrology and geometry record. It supplies spillway fractions,
    depths, bottom conductivity, evaporation coefficient, impoundment coefficients, and drained-area
    fraction for HRU wetlands.
  reservoir_sed_data: Reservoir sediment property record used by reservoir and wetland water-body
    parameters.
  reservoir_nut_data: Reservoir nutrient property record used by reservoir and wetland water-body
    parameters.
  water_body_data_parameters: Combined water-body parameter bundle containing sediment and
    nutrient records plus derived coefficients for shared reservoir/wetland process calculations.
  reservoir_weir_outflow: Weir discharge parameter record for reservoir or wetland outflow.
---

<!-- facts:header -->

Shared reservoir and wetland data container. This module owns the character lookup tables, resolved numeric records, hydrology and initialization databases, sediment and nutrient parameter records, water-body parameter bundles, and weir coefficients used by reservoir, wetland, irrigation, routing, and output routines. It is populated by the reservoir and wetland reader/setup procedures and then consumed by control, balance, calibration, and output code.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container rather than an executable initializer. Its state is populated by the reservoir and wetland reader/setup routines (`res_read*`, `wet_read*`, `res_initial`, `wet_initial`, `hru_allo`, and related allocators), then consumed by simulation and calibration procedures.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `wet_dat` | Looks up the wetland record whose `name` matches the action file pointer, writes the matching index into `hru(j)%dbs%surf_stor`, and then calls `wet_initial` so the HRU wetland state is rebuilt from `wet_dat`. |
| [sym:cal_allo_init] | `calibration workflow state` | `reservoir_data_module state` | Initializes calibration-time working copies for model state. The packet shows this module imported, but no specific reservoir symbols were resolved in the extracted evidence. |
| [sym:cal_parm_select] | `calibration workflow state` | `res_prm, res_hyd` | Applies calibration changes to reservoir sediment parameters, derived sediment settling coefficients, and reservoir hydrology fields. The routine edits `res_prm` and `res_hyd` entries in place. |
| [sym:dtbl_lum_read] | `lum.dtl` | `reservoir_data_module state` | Imports the module but the extracted evidence does not show a resolved use of any reservoir symbol from it in this reader. |
| [sym:dtbl_res_read] | `res_rel.dtl` | `res_weir` | Uses `res_weir(idb)%name` as the lookup key for release actions with `typ='release'` and `option='weir'`, then stores the matched weir index in the reservoir decision table. |
| [sym:dtbl_scen_read] | `scen_lu.dtl` | `reservoir_data_module state` | Imports the module but the extracted evidence does not show a resolved use of any reservoir symbol from it in this reader. |
| [sym:gwflow_read] | `gwflow inputs and exchange files` | `wet_dat` | Imports the module because groundwater exchange setup depends on wetland/reservoir data structures being available elsewhere in the model. The extracted evidence does not show a direct symbol reference from this module in the reader body. |
| [sym:hru_control] | `unit_100100` | `wet_dat_c` | Uses `wet_dat_c(ires)%hyd` to check whether the active wetland is a paddy storage before writing wetland diagnostics. |
| [sym:hru_fr_change] | `ru_elem_upd, lsu_elem_upd` | `wet_dat, wet_hyd` | Uses the wetland hydrology lookup to rebuild wetland geometry after HRU area changes by translating the wetland pointer into hydrology fractions and depths. |
| [sym:hru_read] | `hru-data.hru` | `reservoir_data_module state` | Imports the module, but the provided evidence does not show a direct reservoir symbol reference in the extracted body. |
| [sym:mgt_sched] | `unit_2612` | `res_weir` | Maps management action weir names to `res_weir` indices so wetland management can select the correct weir coefficient row. |
| [sym:res_initial] | `unit_105` | `res_dat, res_hyd, res_init, res_sed` | Copies the resolved reservoir hydrology and initialization records into the reservoir object state, computes geometry-derived coefficients, and prepares the reservoir for simulation. |
| [sym:res_read] | `reservoir.res` | `res_dat_c, res_dat, res_init_dat_c, res_init, res_hyd, res_hyddb, res_sed, res_prm, res_nut` | Reads reservoir definitions, resolves their linked initial-condition and hydrology records, and fills the shared reservoir parameter tables. |
| [sym:res_read_csdb] | `cs_res` | `reservoir_data_module state` | Loads the reservoir constituent database into shared storage; the completed overlay evidence confirms the routine sizes and fills its own database, but this module-specific shared array was not named in the extracted snippet. |
| [sym:res_read_hyd] | `hydrology.res` | `res_hyddb` | Loads reservoir hydrology definitions, fills defaults for missing values, and updates the shared reservoir hydrology database. |
| [sym:res_read_init] | `initial.res` | `res_init, wet_init, res_init_dat_c` | Loads reservoir and wetland initial-condition lookup records and the shared initialization arrays. |
| [sym:res_read_nut] | `nutrients.res` | `res_nut` | Loads reservoir nutrient settings and converts the stored yearly settling and soluble-loss rates to daily values for simulation use. |
| [sym:res_read_salt_cs] | `reservoir.res_cs` | `res_dat_c_cs, res_dat` | Loads reservoir salt and constituent lookup names and resolves them to numeric indices in the reservoir records. |
| [sym:res_read_saltdb] | `salt_res` | `reservoir_data_module state` | Imports the module as part of reservoir initialization context; the packet does not expose a resolved symbol reference from this module in the reader body. |
| [sym:res_read_sed] | `sediment.res` | `res_sed` | Loads reservoir sediment settings into the shared sediment array after counting and allocating the file records. |
| [sym:res_read_weir] | `weir.res` | `res_weir` | Loads reservoir weir discharge settings into the shared weir array after counting and allocating the file records. |
| [sym:swift_output] | `model state` | `wet_dat, wet_hyd, res_hyd` | Uses wetland and reservoir hydrology tables when writing SWIFT output files so the exported descriptors match the active reservoir and wetland setup. |
| [sym:wet_read] | `wetland.wet` | `wet_dat_c, wet_dat` | Reads wetland lookup records and resolves them into the wetland character and numeric databases. |
| [sym:wet_read_hyd] | `hydrology.wet` | `wet_hyddb, wet_hyd` | Reads wetland hydrology definitions, fills defaults for missing values, and updates the shared wetland hydrology database. |
| [sym:wet_read_salt_cs] | `wetland.wet_cs` | `wet_dat_c_cs, wet_dat` | Loads wetland salt and constituent lookup names and resolves them to numeric indices in the wetland records. |

## Key Consumers

The module is used by reservoir, wetland, routing, calibration, irrigation, and output workflows. The main consumers are the reader/setup routines that populate shared state and the control routines that need reservoir and wetland geometry, initial conditions, and water-quality parameters.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_parm_select] | reservoir_data_module | Edits reservoir sediment, sediment-settling, and reservoir hydrology parameter records in place so later reservoir calculations use the calibrated values. |
| [sym:dtbl_res_read] | reservoir_data_module | Uses the reservoir weir table to resolve release-action file pointers to numeric weir indices for later decision-table execution. |
| [sym:hru_fr_change] | reservoir_data_module | Rebuilds wetland geometry after HRU fraction changes by translating the stored wetland pointer into hydrology fractions and spillway depths. |
| [sym:res_initial] | reservoir_data_module | Copies reservoir hydrology, startup, and sediment records into reservoir object state and derives the geometry coefficients used later in routing and release calculations. |
| [sym:res_read] | reservoir_data_module | Loads reservoir lookup records and resolves named initial-condition, hydrology, sediment, nutrient, salt, and constituent inputs into numeric state. |
| [sym:res_read_hyd] | reservoir_data_module | Populates the shared reservoir hydrology database that later reservoir setup and control routines use for geometry and coefficients. |
| [sym:res_read_init] | reservoir_data_module | Allocates and fills the shared reservoir and wetland initial-condition tables from the initialization file. |
| [sym:res_read_nut] | reservoir_data_module | Populates the shared reservoir nutrient parameter table and converts the loaded yearly rates to daily simulation values. |
| [sym:res_read_salt_cs] | reservoir_data_module | Maps reservoir salt and constituent names to numeric indices in the reservoir lookup table for later reservoir setup and simulation. |
| [sym:res_read_sed] | reservoir_data_module | Allocates and fills the shared reservoir sediment parameter table from the sediment input file. |
| [sym:res_read_weir] | reservoir_data_module | Allocates and fills the shared reservoir weir coefficient table from the weir input file. |
| [sym:swift_output] | reservoir_data_module | Writes reservoir and wetland geometry descriptors into SWIFT output files using the loaded hydrology tables. |
| [sym:wet_read] | reservoir_data_module | Allocates and fills the shared wetland lookup tables from the wetland definition file. |
| [sym:wet_read_hyd] | reservoir_data_module | Populates the shared wetland hydrology database and default values used by wetland initialization and geometry calculations. |
| [sym:wet_read_salt_cs] | reservoir_data_module | Maps wetland salt and constituent names to numeric indices in the wetland lookup table for later wetland setup and simulation. |
| [sym:gwflow_read] | wet_dat | Depends on the wetland/reservoir data structures being available elsewhere in the model when parsing groundwater exchange links. |
| [sym:cal_allo_init] | reservoir_data_module | Participates in calibration setup because reservoir state needs to exist in the preserved baseline model state. |
| [sym:dtbl_lum_read] | reservoir_data_module | The imported module appears to have no resolved in-body use in this reader based on the provided evidence. |
| [sym:dtbl_scen_read] | reservoir_data_module | The imported module appears to have no resolved in-body use in this reader based on the provided evidence. |
| [sym:hru_read] | reservoir_data_module | The imported module appears to have no resolved in-body use in this reader based on the provided evidence. |
| [sym:res_read_csdb] | reservoir_data_module | Loads the reservoir constituent database needed by reservoir setup and downstream water-quality routines. |
| [sym:res_read_saltdb] | reservoir_data_module | Loads the reservoir salt database needed by reservoir setup and downstream salt routines. |
| [sym:et_act] | reservoir_data_module | Provides the wetland hydrology record used to scale ponded-water evaporation from an HRU wetland. |
| [sym:hru_allo] | reservoir_data_module | Allocates the wetland parameter and hydrology arrays that will later be filled by wetland initialization routines. |

## Lineage

`reservoir_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `1807dbb` (2025-03-26, "na"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `reservoir_data_module.f90` are listed.

- `1807dbb` (2025-03-26) — na
- `44fa729` (2025-02-06) — Added two new real variables, `soln_stl_fr` and `solp_stl_fr`, to the `water_body_data_parameters` type. Used in wet_inital sediment xwalk a…
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment was extracted from the source.
- The source span shows a declaration-only module; no contained procedures are defined here.
- Importing procedures are numerous; the `used_by` list is a curated subset and the full deterministic importer appendix is preserved in `all_importers`.
- No lineage commits were resolved for this source span, so no file-change summary is available beyond the unresolved status.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
