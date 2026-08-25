---
kind: module
symbol: cs_module
title: cs_module
status: filled
source_hash: 92036523224a2b79
version_label: SWAT+ 62.0.0
variables:
  hcsb_d: Daily HRU constituent balance storage, one allocatable `object_cs_balance` record
    per HRU, with three `cs_balance` entries for seo4, seo3, and boron. It is initialized
    to zero by allocation/setup routines such as `hru_output_allo`, filled by daily process
    routines such as `cs_balance`, `cs_fert`, `cs_irrig`, `cs_rain`, `cs_rctn_hru`, `cs_sorb_hru`,
    and `cs_uptake`, and then read by output and routing routines.
  hcsb_m: Monthly HRU constituent balance storage, parallel to `hcsb_d` but holding month-to-date
    totals. It is allocated and zeroed at startup, accumulated from daily HRU balance terms
    by `hru_cs_output`, and written to monthly HRU output files.
  hcsb_y: Yearly HRU constituent balance storage, parallel to `hcsb_d` but holding year-to-date
    totals. It is allocated and zeroed at startup, accumulated from daily and monthly HRU
    balance terms by `hru_cs_output`, and written to yearly HRU output files.
  hcsb_a: Average-annual HRU constituent balance storage, parallel to `hcsb_d` but holding
    simulation-long totals or averages used for average-annual output. It is allocated and
    zeroed at startup, accumulated by `hru_cs_output`, and written to average-annual HRU output
    files.
  ru_hru_csb_d: Daily routing-unit constituent balance storage built from HRU contributions.
    It holds the summed HRU-derived sediment, seepage, irrigation, atmospheric deposition,
    fertilizer, uptake, reaction, and sorption terms for each constituent and is initialized
    by `ru_read` and populated by `ru_control`.
  ru_hru_csb_m: Monthly routing-unit constituent balance storage derived from HRU contributions.
    It is initialized by `ru_read`, accumulated by `ru_cs_output`, and written to monthly
    routing-unit constituent output.
  ru_hru_csb_y: Yearly routing-unit constituent balance storage derived from HRU contributions.
    It is initialized by `ru_read`, accumulated by `ru_cs_output`, and written to yearly routing-unit
    constituent output.
  ru_hru_csb_a: Average-annual routing-unit constituent balance storage derived from HRU contributions.
    It is initialized by `ru_read`, accumulated by `ru_cs_output`, and written to average-annual
    routing-unit constituent output.
  cs_basin_mo: Basin-wide constituent balance array for monthly reporting. It stores the 87-column
    basin balance totals for seo4, seo3, and boron during the month and is written and reset
    by `cs_balance`.
  cs_basin_yr: Basin-wide constituent balance array for yearly reporting. It stores the 87-column
    basin balance totals for seo4, seo3, and boron during the year and is written and reset
    by `cs_balance`.
  cs_basin_aa: Basin-wide constituent balance array for average-annual reporting. It stores
    simulation-long basin balance totals for seo4, seo3, and boron and is written by `cs_balance`
    at the end of simulation.
  fert_cs: Shared allocatable fertilizer constituent database loaded from `fertilizer.frt_cs`.
    Each record gives fertilizer name and constituent loads for seo4, seo3, and boron; it
    is allocated and filled by `cs_fert_read` and used by fertilizer application routines.
  fert_cs_flag: Integer flag showing whether the fertilizer constituent database was loaded.
    It is set to 1 by `cs_fert_read` after successful allocation and reading, and checked
    by fertilizer application routines before using `fert_cs`.
  cs_uptake_kg: Shared allocatable lookup table of prescribed daily constituent uptake mass
    by plant community and constituent, in kg/ha. It is allocated and filled by `cs_uptake_read`
    from the `cs_uptake` input file and consumed by `cs_uptake`.
  cs_uptake_on: Integer flag for enabling constituent uptake simulation. `cs_uptake_read`
    sets it to 1 when the `cs_uptake` file exists and is loaded; later uptake logic tests
    this flag before applying root uptake.
  cs_urban_conc: Shared allocatable table of urban constituent concentrations in suspended-solid
    loads from impervious areas, in mg cs/kg sed. It is allocated and filled by `cs_urban_read`
    from the `cs_urban` input file and used by urban constituent routines.
  csb_hdr: Basin constituent output header record. It stores the fixed column labels for basin
    daily, monthly, yearly, and average-annual constituent balance files and is written by
    `header_const`.
  cs_hdr_hru: HRU constituent output header record. It stores the fixed column labels for
    daily, monthly, yearly, and average-annual HRU constituent output files and is written
    by `header_const`.
type_components:
  cs_balance:
    soil: 'constituents = seo4,seo3,boron

      |kg/ha       |total mass in the soil profile'
    surq: '|kg/ha       |mass lost in surface runoff in HRU'
    sedm: '|kg/ha       |mass lost in sediment runoff in HRU'
    latq: '|kg/ha       |mass in lateral flow in HRU'
    urbq: '|kg/ha       |mass in urban runoff'
    wetq: '|kg/ha       |mass in wetland outflow'
    tile: '|kg/ha       |mass in tile flow in HRU'
    perc: '|kg/ha       |mass leached past bottom of soil'
    gwup: '|kg/ha       |mass from groundwater (to soil profile)'
    wtsp: '|kg/ha       |mass in wetland seepage (to soil profile)'
    irsw: '|kg/ha       |mass applied on soil via surface water irrigation'
    irgw: '|kg/ha       |mass applied on soil via groundwater irrigation'
    irwo: '|kg/ha       |mass applied on soil via irrigation from without (wo) the watershed'
    rain: '|kg/ha       |mass added to soil via rainfall'
    dryd: '|kg/ha       |mass added to soil via dry atmospheric deposition'
    fert: '|kg/ha       |mass added to soil via fertilizer'
    uptk: '|kg/ha       |mass taken up by crop roots'
    rctn: '|kg/ha       |mass transferred by chemical reaction'
    sorb: '|kg/ha       |mass transferred by sorption'
    conc: '|mg/L        |concentration in soil water (averaged over all soil layers)'
    srbd: '|kg/ha       |mass sorbed to soil'
  object_cs_balance:
    cs: array of `cs_balance` records, one per simulated constituent
  fert_db_cs:
    fertnm: fertilizer name
    seo4: kg seo4/ha      |fertilizer load of seo4 (kg/ha)
    seo3: kg seo3/ha      |fertilizer load of seo3 (kg/ha)
    boron: kg boron/ha     |fertilizer load of boron (kg/ha)
  output_csbal_header:
    yrc: year column label
    mon: month column label
    day: day-of-year column label
    latseo4: 'soil profile balance - seo4

      1'
    surseo4: '2'
    sedseo4: '3'
    urbseo4: '4'
    wetseo4: '5'
    tileseo4: '6'
    percseo4: '7'
    gwupseo4: '8'
    wtspseo4: '9'
    irswseo4: '10'
    irgwseo4: '11'
    irwoseo4: '12'
    rainseo4: '13'
    drydseo4: '14'
    fertseo4: '15'
    uptkseo4: '16'
    rctnseo4: '17'
    sorbseo4: '18'
    ptsoseo4: '19'
    poutseo4: '20'
    sldsseo4: '21'
    srbdseo4: '22'
    gwseo4: 'aquifer balance - seo4

      23'
    rchgseo4: '24'
    seepseo4: '25'
    rctaseo4: '26'
    srbaseo4: '27'
    aqdsseo4: '28'
    srdaseo4: '29'
    latseo3: 'soil profile balance - seo3

      30'
    surseo3: '31'
    sedseo3: '32'
    urbseo3: '33'
    wetseo3: '34'
    tileseo3: '35'
    percseo3: '36'
    gwupseo3: '37'
    wtspseo3: '38'
    irswseo3: '39'
    irgwseo3: '40'
    irwoseo3: '41'
    rainseo3: '42'
    drydseo3: '43'
    fertseo3: '44'
    uptkseo3: '45'
    rctnseo3: '46'
    sorbseo3: '47'
    ptsoseo3: '48'
    poutseo3: '49'
    sldsseo3: '50'
    srbdseo3: '51'
    gwseo3: 'aquifer balance - seo3

      52'
    rchgseo3: '53'
    seepseo3: '54'
    rctaseo3: '55'
    srbaseo3: '56'
    aqdsseo3: '57'
    srdaseo3: '58'
    latborn: 'soil profile balance - boron

      59'
    surborn: '60'
    sedborn: '61'
    urbborn: '62'
    wetborn: '63'
    tileborn: '64'
    percborn: '65'
    gwupborn: '66'
    wtspborn: '67'
    irswborn: '68'
    irgwborn: '69'
    irwoborn: '70'
    rainborn: '71'
    drydborn: '72'
    fertborn: '73'
    uptkborn: '74'
    rctnborn: '75'
    sorbborn: '76'
    ptsoborn: '77'
    poutborn: '78'
    sldsborn: '79'
    srbdborn: '80'
    gwborn: 'aquifer balance - boron

      81'
    rchgborn: '82'
    seepborn: '83'
    rctaborn: '84'
    srbaborn: '85'
    aqdsborn: '86'
    srdaborn: '87'
  output_cs_hdr_hru:
    day: day-of-year label
    mo: month label
    day_mo: day-of-month label
    yrc: year label
    isd: HRU unit label
    id: GIS ID label
    seo4sl: total cs in soil profile (solution; sorbed)
    seo3sl: total cs in soil profile for seo3
    bornsl: total cs in soil profile for boron
    seo4sq: surface runoff
    seo3sq: surface runoff for seo3
    bornsq: surface runoff for boron
    seo4sd: sediment runoff
    seo3sd: sediment runoff for seo3
    bornsd: sediment runoff for boron
    seo4lq: lateral flow
    seo3lq: lateral flow for seo3
    bornlq: lateral flow for boron
    seo4ub: urban sediment runoff
    seo3ub: urban sediment runoff for seo3
    bornub: urban sediment runoff for boron
    seo4wt: wetland outflow
    seo3wt: wetland outflow for seo3
    bornwt: wetland outflow for boron
    seo4tq: tile flow
    seo3tq: tile flow for seo3
    borntq: tile flow for boron
    seo4pc: percolation
    seo3pc: percolation for seo3
    bornpc: percolation for boron
    seo4gt: groundwater transfer
    seo3gt: groundwater transfer for seo3
    borngt: groundwater transfer for boron
    seo4ws: wetland seepage
    seo3ws: wetland seepage for seo3
    bornws: wetland seepage for boron
    seo4is: irrigation (surface water)
    seo3is: irrigation (surface water) for seo3
    bornis: irrigation (surface water) for boron
    seo4ig: irrigation (groundwater)
    seo3ig: irrigation (groundwater) for seo3
    bornig: irrigation (groundwater) for boron
    seo4io: irrigation (outside watershed)
    seo3io: irrigation (outside watershed) for seo3
    bornio: irrigation (outside watershed) for boron
    seo4rn: rainfall (wet deposition)
    seo3rn: rainfall (wet deposition) for seo3
    bornrn: rainfall (wet deposition) for boron
    seo4dd: dry deposition
    seo3dd: dry deposition for seo3
    borndd: dry deposition for boron
    seo4fz: fertilizer
    seo3fz: fertilizer for seo3
    bornfz: fertilizer for boron
    seo4up: cs uptake
    seo3up: cs uptake for seo3
    bornup: cs uptake for boron
    seo4rc: cs chemial reactions
    seo3rc: cs chemical reactions for seo3
    bornrc: cs chemical reactions for boron
    seo4sp: cs sorption
    seo3sp: cs sorption for seo3
    bornsp: cs sorption for boron
    seo4c: soil water concentration (averaged over layers)
    seo3c: soil water concentration (averaged over layers) for seo3
    bornc: soil water concentration (averaged over layers) for boron
    seo4srbd: sorbed mass (total over layers)
    seo3srbd: sorbed mass (total over layers) for seo3
    bornsrbd: sorbed mass (total over layers) for boron
type_summaries:
  cs_balance: One HRU or basin constituent balance record containing storage and flux terms
    for seo4, seo3, or boron on an areal basis.
  object_cs_balance: Allocatable wrapper around an array of `cs_balance` records for one reporting
    object such as an HRU or routing unit.
  fert_db_cs: Constituent fertilizer database record.
  output_csbal_header: Header for daily basin-wide constituent balance output.
  output_cs_hdr_hru: Header for daily, monthly, yearly, and average-annual HRU constituent
    output.
---

<!-- facts:header -->

cs_module owns the shared SWAT+ constituent-state types and module-level balance/output arrays for selenium species and boron. It provides the HRU, routing-unit, basin, fertilizer, uptake, urban, and header storage that initialization, mass-balance, irrigation, reaction, sorption, output, and input-reader routines populate and consume.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

cs_module is a declaration-and-shared-state module only; it contains no procedures. Its allocatable arrays and output-header records are populated by setup and reader routines such as `hru_output_allo`, `ru_read`, `cs_fert_read`, `cs_uptake_read`, `cs_urban_read`, and `header_const` before the time-stepping routines use them.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:cs_balance] | `unit_6080, unit_6082, unit_6084, unit_6086` | `hcsb_d, hcsb_m, hcsb_y, hcsb_a, ru_hru_csb_d, ru_hru_csb_m` | Reads the daily HRU balance state, aggregates HRU contributions into basin monthly/yearly/average-annual totals, and writes basin constituent output. |
| [sym:cs_fert_read] | `fertilizer.frt_cs` | `fert_cs, fert_cs_flag` | Opens the fertilizer constituent table, allocates `fert_cs`, reads each fertilizer record, and marks the table loaded with `fert_cs_flag = 1`. |
| [sym:cs_hru_init] | `constituent initialization databases` | `none resolved` | Initializes HRU constituent soil and irrigation state from constituent initialization databases. The packet does not resolve any `cs_module` symbols as used by this routine. |
| [sym:cs_uptake_read] | `cs_uptake` | `cs_uptake_kg, cs_uptake_on` | Checks for the `cs_uptake` file, allocates and fills the uptake table, and sets the uptake feature flag on when the file exists. |
| [sym:cs_urban_read] | `cs_urban` | `cs_urban_conc` | Reads urban constituent concentrations, allocates the urban lookup table, and fills rows that match the urban database names. |
| [sym:gwflow_canal_div] | `unit_canal_name, unit_out_canal_bal, unit_out_canal_sol` | `hcsb_d` | Uses the constituent balance arrays as the non-salt counterpart bookkeeping while canal-groundwater exchange is computed and written. |
| [sym:header_const] | `unit_6080, unit_6082, unit_6084, unit_6086, unit_6021, unit_6022, unit_6023, unit_6024, unit_6025, unit_6026, unit_6027, unit_6028, unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067, unit_6030, unit_6031, unit_6032, unit_6033, unit_6034, unit_6035, unit_6036, unit_6037, unit_6040, unit_6041, unit_6042, unit_6043, unit_6044, unit_6045, unit_6046, unit_6047, unit_6070, unit_6071, unit_6072, unit_6073, unit_6074, unit_6075, unit_6076, unit_6077, unit_6090, unit_6091, unit_6092, unit_6093, unit_6094, unit_6095, unit_6096, unit_6097` | `csb_hdr, cs_hdr_hru` | Writes the basin and HRU constituent output headers using the shared header records defined in this module. |
| [sym:hru_control] | `unit_100100` | `hcsb_d` | Builds the daily HRU constituent balance from soil concentration, mass, runoff, seepage, irrigation, and other process outputs before output routines read it. |
| [sym:hru_cs_output] | `unit_6021, unit_6022, unit_6023, unit_6024, unit_6025, unit_6026, unit_6027, unit_6028` | `hcsb_d, hcsb_m, hcsb_y, hcsb_a` | Rolls daily HRU constituent balances into monthly, yearly, and average-annual accumulators and writes the requested HRU constituent files. |
| [sym:ru_cs_output] | `unit_6070, unit_6071, unit_6072, unit_6073, unit_6074, unit_6075, unit_6076, unit_6077` | `ru_hru_csb_d, ru_hru_csb_m, ru_hru_csb_y, ru_hru_csb_a` | Rolls daily routing-unit HRU-derived constituent totals into longer-period accumulators and writes routing-unit constituent output. |
| [sym:ru_read] | `rout_unit.rtu` | `ru_hru_csb_d, ru_hru_csb_m, ru_hru_csb_y, ru_hru_csb_a` | Allocates and zeroes the routing-unit constituent balance arrays while reading routing-unit setup from the routing-unit file. |

## Key Consumers

This module is the shared state hub for constituent chemistry and accounting. Initialization, load readers, process routines, and output routines all import it to access the same HRU, routing-unit, basin, fertilizer, uptake, urban, and header records.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cs_balance] | cs_module | Calculates basin-wide constituent totals from the HRU balance arrays and writes daily, monthly, yearly, and average-annual basin balance output. |
| [sym:cs_fert_read] | cs_module | Loads the shared fertilizer constituent database into `fert_cs` and sets `fert_cs_flag` so later fertilizer routines can use the table. |
| [sym:cs_uptake_read] | cs_module | Enables constituent uptake and fills `cs_uptake_kg` from the `cs_uptake` input file for later root-uptake calculations. |
| [sym:cs_urban_read] | cs_module | Loads urban constituent concentration lookups into `cs_urban_conc` for later urban runoff constituent calculations. |
| [sym:header_const] | cs_module | Writes the basin and HRU constituent header records `csb_hdr` and `cs_hdr_hru` into the output files before simulation output begins. |
| [sym:hru_cs_output] | cs_module | Accumulates and prints HRU constituent balances at daily, monthly, yearly, and average-annual intervals using `hcsb_d`, `hcsb_m`, `hcsb_y`, and `hcsb_a`. |
| [sym:ru_cs_output] | cs_module | Accumulates and prints routing-unit HRU-derived constituent balances at daily, monthly, yearly, and average-annual intervals using `ru_hru_csb_*`. |
| [sym:ru_read] | cs_module | Allocates the routing-unit constituent balance arrays and zeroes each flux component so downstream routing starts from a clean baseline. |
| [sym:gwflow_canal_div] | hcsb_d | Uses the constituent balance arrays as the non-salt bookkeeping counterpart while canal-groundwater exchange is computed and recorded. |
| [sym:gwflow_pump_allo] | hcsb_d | Records groundwater-irrigation constituent additions in the HRU balance arrays when pumped water is routed to an HRU. |
| [sym:cs_fert] | cs_module | Uses `fert_cs` and `hcsb_d` to add fertilizer-borne seo4, seo3, and boron mass to the HRU soil pool and daily balance. |
| [sym:cs_fert_wet] | cs_module | Uses `fert_cs` to compute wetland fertilizer constituent additions and records the resulting mass in wetland balance arrays. |
| [sym:cs_irrig] | cs_module | Uses the HRU balance arrays to record irrigation-applied constituent mass from surface water, groundwater, diversions, and outside sources. |
| [sym:cs_rain] | cs_module | Records rainfall and dry-deposition constituent additions in the HRU daily balance arrays and updates top-layer soil storage. |
| [sym:cs_rctn_hru] | cs_module | Stores HRU reaction mass-balance terms for seo4 and seo3 after updating soil-layer concentrations and masses. |
| [sym:cs_sorb_hru] | cs_module | Stores HRU sorption mass-balance terms for seo4, seo3, and boron after equilibrium calculations update the soil profile. |
| [sym:cs_uptake] | cs_module | Adds root uptake to the HRU daily balance and subtracts the taken-up constituent mass from soil storage. |
| [sym:hru_output_allo] | cs_module | Allocates and zeroes the HRU constituent balance arrays so later HRU process routines have storage for daily, monthly, yearly, and average-annual values. |
| [sym:ru_control] | cs_module | Aggregates HRU constituent balances into routing-unit totals, including sediment, seepage, irrigation, rainfall, deposition, fertilizer, uptake, reaction, and sorption terms. |
| [sym:aqu_initial] | cs_module | Imports the module for aquifer constituent workflows, but the provided evidence does not identify direct `cs_module` symbols used by this routine. |
| [sym:cs_rctn_aqu] | cs_module | Provides the constituent configuration context used by groundwater reaction logic and keeps aquifer reaction mass-balance terms in shared state. |
| [sym:hru_control] | cs_module | Builds the daily HRU constituent balance from soil storage, runoff, seepage, irrigation, atmospheric deposition, fertilizer, uptake, reaction, and sorption outputs. |

## Lineage

`cs_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `2ee1889` (2025-11-17, "Cleanup of sine warnings."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cs_module.f90` are listed.

- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `35b029c` (2024-03-24) — Mar 19 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No lineage commits were resolved for the requested source span.
- The `cs_hru_init` importer is known from the context packet, but no direct `cs_module` symbol reference was resolved in its extracted evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
