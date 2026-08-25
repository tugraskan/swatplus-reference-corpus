---
kind: module
symbol: salt_module
title: salt_module
status: filled
source_hash: 50254af95ede3209
version_label: SWAT+ 62.0.0
variables:
  hsaltb_d: Daily HRU salt balance storage for each HRU and simulated salt ion. It is allocated
    by `hru_output_allo`, populated by salt process routines such as `salt_rain`, `salt_irrig`,
    `salt_roadsalt`, `salt_fert`, `salt_uptake`, and `salt_chem_hru`, and read by HRU, routing-unit,
    and basin output routines.
  hsaltb_m: Monthly HRU salt balance storage for each HRU and salt ion. It is allocated by
    `hru_output_allo`, zeroed at setup, and accumulated from `hsaltb_d` by `hru_salt_output`
    before monthly reporting.
  hsaltb_y: Yearly HRU salt balance storage for each HRU and salt ion. It is allocated by
    `hru_output_allo`, accumulated from `hsaltb_m` by `hru_salt_output`, and used for yearly
    salt reporting.
  hsaltb_a: Average-annual HRU salt balance storage for each HRU and salt ion. It is allocated
    by `hru_output_allo`, scaled and accumulated by `hru_salt_output`, and used for average
    annual salt output.
  ru_hru_saltb_d: Daily routing-unit salt totals formed by summing HRU contributions into
    routing-unit accounting. It is allocated by `ru_read` and populated by `ru_control` from
    `hsaltb_d` and other HRU salt fluxes.
  ru_hru_saltb_m: Monthly routing-unit salt totals accumulated from `ru_hru_saltb_d`. It is
    allocated by `ru_read` and updated by `ru_salt_output` for monthly routing-unit salt reporting.
  ru_hru_saltb_y: Yearly routing-unit salt totals accumulated from `ru_hru_saltb_m`. It is
    allocated by `ru_read` and updated by `ru_salt_output` for yearly routing-unit salt reporting.
  ru_hru_saltb_a: Average-annual routing-unit salt totals accumulated from `ru_hru_saltb_y`.
    It is allocated by `ru_read` and updated by `ru_salt_output` for final average annual
    routing-unit salt reporting.
  salt_basin_mo: Monthly basin salt balance array with 28 basin-wide salt summary categories.
    It is zeroed in the module declaration, filled by `salt_balance`, and written to basin
    monthly output.
  salt_basin_yr: Yearly basin salt balance array with 28 basin-wide salt summary categories.
    It is zeroed in the module declaration, filled by `salt_balance`, and written to basin
    yearly output.
  salt_basin_aa: Average-annual basin salt balance array with 28 basin-wide salt summary categories.
    It is zeroed in the module declaration, filled by `salt_balance`, and written to basin
    average-annual output.
  fert_salt: Allocatable table of fertilizer salt composition records. It is loaded by `salt_fert_read`
    from `salt_fertilizer.frt` and consumed by fertilizer and wetland salt application routines.
  fert_salt_flag: Integer feature flag that indicates whether `fert_salt` has been loaded.
    It is reset and set by `salt_fert_read` and checked by salt fertilizer routines before
    using the database.
  salt_uptake_kg: Allocatable table of specified daily salt uptake demand by plant community
    and salt ion in kg/ha. It is loaded by `salt_uptake_read` from the `salt_uptake` file
    and used by `salt_uptake`.
  salt_uptake_on: Integer feature flag for salt uptake simulation. It is set by `salt_uptake_read`
    when the file exists and checked by plant growth routines before calling `salt_uptake`.
  salt_urban_conc: Allocatable table of urban salt ion concentrations in suspended solid load
    from impervious areas, in mg salt per kg sediment. It is loaded by `salt_urban_read` from
    the `salt_urban` file.
  saltb_hdr: Basin salt output header record. It is written by `header_salt` into basin daily,
    monthly, yearly, and average-annual salt output files.
  salt_hdr_hru: HRU salt output header record. It is written by `header_salt` into HRU daily,
    monthly, yearly, and average-annual salt output files.
type_components:
  salt_balance:
    soil: 'salt ions = so4,ca,mg,na,k,cl,co3,hco3

      |kg/ha       |total salt ion mass in the soil profile'
    diss: '|kg/ha       |salt ion mass transferred from sorbed phase to dissolved phase'
    surq: '|kg/ha       |salt ion mass lost in surface runoff in HRU'
    latq: '|kg/ha       |salt ion mass in lateral flow in HRU'
    urbq: '|kg/ha       |salt ion mass in urban runoff'
    wetq: '|kg/ha       |salt ion mass in wetland runoff'
    tile: '|kg/ha       |salt ion mass in tile flow in HRU'
    perc: '|kg/ha       |salt ion mass leached past bottom of soil'
    gwup: '|kg/ha       |salt ion mass from groundwater (to soil profile)'
    wtsp: '|kg/ha       |salt ion mass in wetland seepage (to soil profile)'
    irsw: '|kg/ha       |salt ion mass applied on soil via surface water irrigation'
    irgw: '|kg/ha       |salt ion mass applied on soil via groundwater irrigation'
    irwo: '|kg/ha       |salt ion mass applied on soil via girrigation from without (wo) the
      watershed'
    rain: '|kg/ha       |salt ion mass added to soil via rainfall'
    dryd: '|kg/ha       |salt ion mass added to soil via dry atmospheric deposition'
    road: '|kg/ha       |salt ion mass added to soil via applied road salt'
    fert: '|kg/ha       |salt ion mass added to soil via fertilizer'
    amnd: '|kg/ha       |salt ion mass added to soil via salt amendments'
    uptk: '|kg/ha       |salt ion mass taken up by crop roots'
    conc: '|mg/L        |salt ion concentration in soil water (averaged over all soil layers)'
  object_salt_balance:
    salt: Allocatable array of `salt_balance` records, one entry per simulated salt ion
  fert_db_salt:
    fertnm: Fertilizer name read from the salt fertilizer database
    so4: kg so4/ha      |fertilizer load of so4 (kg/ha)
    ca: kg ca/ha       |fertilizer load of ca (kg/ha)
    mg: kg mg/ha       |fertilizer load of mg (kg/ha)
    na: kg na/ha       |fertilizer load of na (kg/ha)
    k: kg k/ha        |fertilizer load of k (kg/ha)
    cl: kg cl/ha       |fertilizer load of cl (kg/ha)
    co3: kg co3/ha      |fertilizer load of co3 (kg/ha)
    hco3: kg hco3/ha     |fertilizer load of hco3 (kg/ha)
  output_saltbal_header:
    yrc: calendar year column label
    mon: calendar month column label
    day: day-of-year column label
    lat: lateral flow salt column label
    gw: groundwater salt column label
    sur: surface runoff salt column label
    urb: urban runoff salt column label
    wet: wetland runoff salt column label
    tile: tile drainage salt column label
    perc: percolation salt column label
    gwup: groundwater-to-soil salt column label
    wtsp: wetland seepage-to-soil salt column label
    irsw: surface-water irrigation salt column label
    irgw: groundwater irrigation salt column label
    irwo: outside-watershed irrigation salt column label
    rain: rainfall salt column label
    dryd: dry deposition salt column label
    road: road-salt application column label
    fert: fertilizer salt column label
    amnd: amendment salt column label
    uptk: plant uptake salt column label
    ptso: soil-to-channel transfer column label
    pout: point output transfer column label
    rchg: aquifer recharge salt column label
    seep: aquifer seepage salt column label
    dssl: soil mineral dissolution column label
    dsaq: aquifer mineral dissolution column label
    slds: dissolved soil salt column label
    slmn: soil mineral salt column label
    aqds: dissolved aquifer salt column label
    aqmn: aquifer mineral salt column label
  output_salt_hdr_hru:
    day: day-of-year column label
    mo: month column label
    day_mo: day-of-month column label
    yrc: calendar year column label
    isd: HRU unit identifier label
    id: GIS identifier label
    so4sl: total sulfate in soil profile
    casl: total calcium in soil profile
    mgsl: total magnesium in soil profile
    nasl: total sodium in soil profile
    ksl: total potassium in soil profile
    clsl: total chloride in soil profile
    co3sl: total carbonate in soil profile
    hco3sl: total bicarbonate in soil profile
    so4sq: sulfate in surface runoff
    casq: calcium in surface runoff
    mgsq: magnesium in surface runoff
    nasq: sodium in surface runoff
    ksq: potassium in surface runoff
    clsq: chloride in surface runoff
    co3sq: carbonate in surface runoff
    hco3sq: bicarbonate in surface runoff
    so4lq: sulfate in lateral flow
    calq: calcium in lateral flow
    mglq: magnesium in lateral flow
    nalq: sodium in lateral flow
    klq: potassium in lateral flow
    cllq: chloride in lateral flow
    co3lq: carbonate in lateral flow
    hco3lq: bicarbonate in lateral flow
    so4uq: sulfate in urban runoff
    cauq: calcium in urban runoff
    mguq: magnesium in urban runoff
    nauq: sodium in urban runoff
    kuq: potassium in urban runoff
    cluq: chloride in urban runoff
    co3uq: carbonate in urban runoff
    hco3uq: bicarbonate in urban runoff
    so4wt: sulfate in wetland runoff
    cawt: calcium in wetland runoff
    mgwt: magnesium in wetland runoff
    nawt: sodium in wetland runoff
    kwt: potassium in wetland runoff
    clwt: chloride in wetland runoff
    co3wt: carbonate in wetland runoff
    hco3wt: bicarbonate in wetland runoff
    so4tq: sulfate in tile flow
    catq: calcium in tile flow
    mgtq: magnesium in tile flow
    natq: sodium in tile flow
    ktq: potassium in tile flow
    cltq: chloride in tile flow
    co3tq: carbonate in tile flow
    hco3tq: bicarbonate in tile flow
    so4pc: sulfate in percolation
    capc: calcium in percolation
    mgpc: magnesium in percolation
    napc: sodium in percolation
    kpc: potassium in percolation
    clpc: chloride in percolation
    co3pc: carbonate in percolation
    hco3pc: bicarbonate in percolation
    so4gt: sulfate in groundwater transfer
    cagt: calcium in groundwater transfer
    mggt: magnesium in groundwater transfer
    nagt: sodium in groundwater transfer
    kgt: potassium in groundwater transfer
    clgt: chloride in groundwater transfer
    co3gt: carbonate in groundwater transfer
    hco3gt: bicarbonate in groundwater transfer
    so4ws: sulfate in wetland seepage to soil
    caws: calcium in wetland seepage to soil
    mgws: magnesium in wetland seepage to soil
    naws: sodium in wetland seepage to soil
    kws: potassium in wetland seepage to soil
    clws: chloride in wetland seepage to soil
    co3ws: carbonate in wetland seepage to soil
    hco3ws: bicarbonate in wetland seepage to soil
    so4is: sulfate in surface-water irrigation
    cais: calcium in surface-water irrigation
    mgis: magnesium in surface-water irrigation
    nais: sodium in surface-water irrigation
    kis: potassium in surface-water irrigation
    clis: chloride in surface-water irrigation
    co3is: carbonate in surface-water irrigation
    hco3is: bicarbonate in surface-water irrigation
    so4ig: sulfate in groundwater irrigation
    caig: calcium in groundwater irrigation
    mgig: magnesium in groundwater irrigation
    naig: sodium in groundwater irrigation
    kig: potassium in groundwater irrigation
    clig: chloride in groundwater irrigation
    co3ig: carbonate in groundwater irrigation
    hco3ig: bicarbonate in groundwater irrigation
    so4io: sulfate in outside-watershed irrigation
    caio: calcium in outside-watershed irrigation
    mgio: magnesium in outside-watershed irrigation
    naio: sodium in outside-watershed irrigation
    kio: potassium in outside-watershed irrigation
    clio: chloride in outside-watershed irrigation
    co3io: carbonate in outside-watershed irrigation
    hco3io: bicarbonate in outside-watershed irrigation
    so4rn: sulfate in rainfall
    carn: calcium in rainfall
    mgrn: magnesium in rainfall
    narn: sodium in rainfall
    krn: potassium in rainfall
    clrn: chloride in rainfall
    co3rn: carbonate in rainfall
    hco3rn: bicarbonate in rainfall
    so4dd: sulfate in dry deposition
    cadd: calcium in dry deposition
    mgdd: magnesium in dry deposition
    nadd: sodium in dry deposition
    kdd: potassium in dry deposition
    cldd: chloride in dry deposition
    co3dd: carbonate in dry deposition
    hco3dd: bicarbonate in dry deposition
    so4rd: sulfate in road salt application
    card: calcium in road salt application
    mgrd: magnesium in road salt application
    nard: sodium in road salt application
    krd: potassium in road salt application
    clrd: chloride in road salt application
    co3rd: carbonate in road salt application
    hco3rd: bicarbonate in road salt application
    so4fz: sulfate in fertilizer application
    cafz: calcium in fertilizer application
    mgfz: magnesium in fertilizer application
    nafz: sodium in fertilizer application
    kfz: potassium in fertilizer application
    clfz: chloride in fertilizer application
    co3fz: carbonate in fertilizer application
    hco3fz: bicarbonate in fertilizer application
    so4am: sulfate in amendment application
    caam: calcium in amendment application
    mgam: magnesium in amendment application
    naam: sodium in amendment application
    kam: potassium in amendment application
    clam: chloride in amendment application
    co3am: carbonate in amendment application
    hco3am: bicarbonate in amendment application
    so4up: sulfate removed by uptake
    caup: calcium removed by uptake
    mgup: magnesium removed by uptake
    naup: sodium removed by uptake
    kup: potassium removed by uptake
    clup: chloride removed by uptake
    co3up: carbonate removed by uptake
    hco3up: bicarbonate removed by uptake
    so4c: sulfate concentration in soil water
    cac: calcium concentration in soil water
    mgc: magnesium concentration in soil water
    nac: sodium concentration in soil water
    kc: potassium concentration in soil water
    clc: chloride concentration in soil water
    co3c: carbonate concentration in soil water
    hco3c: bicarbonate concentration in soil water
    dssl: total mineral dissolution and precipitation
type_summaries:
  salt_balance: One salt balance record for a single salt ion, holding soil storage, dissolved
    transfer, and all HRU salt flux components on an area basis.
  object_salt_balance: Container holding a one-dimensional allocatable array of `salt_balance`
    records for an HRU, routing unit, or other object that tracks one record per salt ion.
  fert_db_salt: Salt fertilizer composition record used to store the ion loads associated
    with one fertilizer definition.
  output_saltbal_header: Header labels for basin-wide daily, monthly, yearly, and average-annual
    salt balance output.
  output_salt_hdr_hru: Header labels for HRU daily, monthly, yearly, and average-annual salt
    output.
---

<!-- facts:header -->

Owns the shared salt state used across SWAT+ HRU, routing-unit, basin, aquifer, and wetland salt accounting. It defines the salt balance record types, the per-HRU and per-routing-unit accumulator arrays, fertilizer and uptake lookup tables, urban salt concentrations, and the header records written by the salt output setup routine. The module itself contains no procedures; other routines allocate, initialize, update, and print these public variables.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only. It does not contain startup code, but its public arrays and header records are allocated, zeroed, loaded, and printed by other routines such as `hru_output_allo`, `ru_read`, `salt_fert_read`, `salt_uptake_read`, `salt_urban_read`, `header_salt`, and the salt process routines.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:gwflow_canal_div] | `unit_canal_name, unit_out_canal_bal, unit_out_canal_sol` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Uses the shared salt balance state when canal seepage exchanges with groundwater so transferred solute mass can feed the model's salt bookkeeping. |
| [sym:header_salt] | `unit_5080, unit_5082, unit_5084, unit_5086, unit_5021, unit_5022, unit_5023, unit_5024, unit_5025, unit_5026, unit_5027, unit_5028, unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067, unit_5030, unit_5031, unit_5032, unit_5033, unit_5034, unit_5035, unit_5036, unit_5037, unit_5040, unit_5041, unit_5042, unit_5043, unit_5044, unit_5045, unit_5046, unit_5047, unit_5070, unit_5071, unit_5072, unit_5073, unit_5074, unit_5075, unit_5076, unit_5077, unit_5090, unit_5091, unit_5092, unit_5093, unit_5094, unit_5095, unit_5096, unit_5097` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Writes the basin and HRU salt header records to the configured salt output files after the descriptive text. |
| [sym:hru_control] | `unit_100100` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Copies HRU salt fluxes into the daily HRU salt balance arrays so later routing and output routines can use them. |
| [sym:hru_salt_output] | `unit_5021, unit_5022, unit_5023, unit_5024, unit_5025, unit_5026, unit_5027, unit_5028` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Aggregates daily HRU salt fluxes into monthly, yearly, and average-annual accumulators before writing HRU salt output. |
| [sym:ru_read] | `rout_unit.rtu` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Allocates and zeroes the routing-unit salt balance arrays during routing-unit database setup. |
| [sym:ru_salt_output] | `unit_5070, unit_5071, unit_5072, unit_5073, unit_5074, unit_5075, unit_5076, unit_5077` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Rolls routing-unit salt loads forward from daily to monthly, yearly, and average-annual accumulators and writes routing-unit salt output. |
| [sym:salt_balance] | `unit_5080, unit_5082, unit_5084, unit_5086` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Uses the daily HRU salt balance arrays to accumulate basin-wide salt loads and storage terms for salt mass-balance output. |
| [sym:salt_fert_read] | `salt_fertilizer.frt` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Loads the fertilizer salt composition database and sets the readiness flag used by fertilizer salt application routines. |
| [sym:salt_hru_init] | `salt soil and irrigation initialization tables` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Seeds HRU soil and irrigation salt state from initialization tables so later salt processes start from consistent initial conditions. |
| [sym:salt_uptake_read] | `salt_uptake` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Loads the optional salt uptake table and turns on the salt uptake feature flag. |
| [sym:salt_urban_read] | `salt_urban` | `hsaltb_d, hsaltb_m, hsaltb_y, hsaltb_a, ru_hru_saltb_d, ru_hru_saltb_m` | Loads the urban salt concentration lookup table used by later urban salt calculations. |

## Key Consumers

This module is the shared storage layer for the model's salt accounting. Readers and setup routines allocate and populate the arrays, process routines update them during daily salt transport and chemistry, and output routines use the same records to write HRU, routing-unit, and basin salt summaries.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:header_salt] | salt_module | Writes `saltb_hdr` and `salt_hdr_hru` into the configured basin and HRU salt output files after the descriptive text so the reports have the correct column labels. |
| [sym:hru_salt_output] | salt_module | Uses the HRU salt balance arrays as the source of daily, monthly, yearly, and average-annual salt output, rolling `hsaltb_d` into `hsaltb_m`, `hsaltb_y`, and `hsaltb_a`. |
| [sym:ru_read] | salt_module | Allocates the routing-unit salt balance arrays and initializes the daily, monthly, yearly, and average-annual routing-unit salt storage to zero. |
| [sym:ru_salt_output] | salt_module | Accumulates routing-unit salt loads from daily into monthly, yearly, and average-annual totals and writes the resulting routing-unit salt output. |
| [sym:salt_balance] | salt_module | Reads the daily HRU salt flux arrays to build basin-wide salt mass-balance totals and writes those totals to the basin output files. |
| [sym:salt_fert_read] | salt_module | Populates `fert_salt` and sets `fert_salt_flag`, making fertilizer salt composition available to later fertilizer and wetland salt routines. |
| [sym:salt_uptake_read] | salt_module | Loads `salt_uptake_kg` and turns on `salt_uptake_on`, enabling plant salt uptake demand to be applied later in the simulation. |
| [sym:salt_urban_read] | salt_module | Loads `salt_urban_conc`, which later urban salt calculations use as the shared concentration lookup table. |
| [sym:gwflow_canal_div] | hsaltb_d | Transfers canal seepage-related solute mass into the shared salt bookkeeping when canal water exchanges with groundwater. |
| [sym:salt_hru_init] | salt_module | Imports the salt state and initialization tables needed to seed HRU soil and irrigation salt values before simulation starts. |
| [sym:gwflow_pump_allo] | hsaltb_d | Adds groundwater irrigation salt mass into the HRU soil salt balance when pumped water is routed to an HRU. |
| [sym:pl_biomass_gro] | salt_uptake_on | Checks the salt uptake feature flag before calling `salt_uptake`, so biomass growth only includes salt uptake when the feature is enabled. |
| [sym:hru_output_allo] | salt_module | Allocates the HRU salt balance records that all later HRU salt process and output routines update. |
| [sym:ru_control] | salt_module | Aggregates HRU salt flux balances into routing-unit totals for irrigation, rainfall, deposition, fertilizer, amendment, uptake, and dissolved salt, then passes them onward in routing-unit output state. |
| [sym:salt_chem_hru] | salt_module | Writes the HRU dissolved-to-solid salt change into `hsaltb_d(j)%salt(1)%diss` after the soil chemistry update. |
| [sym:salt_fert] | salt_module | Uses the fertilizer salt composition database and updates the HRU salt balance arrays with amendment or fertilizer salt additions. |
| [sym:salt_fert_wet] | salt_module | Uses the fertilizer salt composition database to add fertilizer salts into wetland water storage and wetland salt balance outputs. |
| [sym:salt_irrig] | salt_module | Adds irrigation-delivered salt mass to HRU soil, wetland, or aquifer state and updates the corresponding salt balance arrays. |
| [sym:salt_rain] | salt_module | Adds rainfall and dry-deposition salt inputs to the HRU soil profile and records the corresponding daily salt balance terms. |
| [sym:salt_roadsalt] | salt_module | Adds road-salt inputs to the first soil layer and records the road-salt mass in the daily HRU salt balance. |
| [sym:salt_uptake] | salt_module | Uses the configured plant salt uptake demand to remove salt from the soil profile and accumulate the uptake flux in the HRU salt balance. |
| [sym:aqu_1d_control] | salt_module | Keeps the daily aquifer salt-processing path connected to the shared salt bookkeeping used by the 1-D aquifer controller. |
| [sym:aqu_initial] | salt_module | Makes salt-related aquifer state and output arrays available during aquifer initialization. |
| [sym:salt_chem_aqu] | salt_module | Provides the shared ion arrays and equilibrium constants used to update aquifer salt chemistry and mineral reactions. |

## Lineage

`salt_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `2ee1889` (2025-11-17, "Cleanup of sine warnings."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `salt_module.f90` are listed.

- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `35b029c` (2024-03-24) — Mar 19 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment was extracted from the source.
- The module is a shared state container only; initialization and output setup are handled by other routines in the salt, HRU, routing-unit, and basin workflows.
- The completed-procedure evidence identifies 26 importers; the complete importer list is preserved in `all_importers`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
