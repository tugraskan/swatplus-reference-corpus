---
kind: module
symbol: cs_aquifer
title: cs_aquifer
status: filled
source_hash: 4ca185856a8554da
version_label: SWAT+ 62.0.0
variables:
  acsb_d: Daily aquifer constituent balance array, allocated per aquifer and per simulated
    constituent; initialized to zero in aqu_initial and populated by aqu_1d_control, cs_irrig,
    cs_rctn_aqu, and cs_sorb_aqu before aquifer output and basin accounting read it.
  acsb_m: Monthly aquifer constituent balance array, allocated per aquifer and per simulated
    constituent; zeroed in aqu_initial, accumulated from acsb_d in aqu_cs_output, and printed
    in monthly aquifer constituent reports.
  acsb_y: Yearly aquifer constituent balance array, allocated per aquifer and per simulated
    constituent; zeroed in aqu_initial, accumulated from acsb_d in aqu_cs_output, and printed
    in yearly aquifer constituent reports.
  acsb_a: Average-annual aquifer constituent balance array, allocated per aquifer and per
    simulated constituent; zeroed in aqu_initial, accumulated from acsb_d in aqu_cs_output,
    and printed in average-annual aquifer constituent reports.
  bacs_d: Basin-wide aquifer constituent balance container for daily reporting; used by basin
    constituent accounting when aquifer fluxes are rolled into basin totals.
  bacs_m: Basin-wide aquifer constituent balance container for monthly reporting; used by
    basin constituent accounting when aquifer fluxes are rolled into basin totals.
  bacs_y: Basin-wide aquifer constituent balance container for yearly reporting; used by basin
    constituent accounting when aquifer fluxes are rolled into basin totals.
  bacs_a: Basin-wide aquifer constituent balance container for average-annual reporting; used
    by basin constituent accounting when aquifer fluxes are rolled into basin totals.
  csbz_aqu: Basin-zone aquifer constituent balance container; declared as a public object
    balance record for aquifer constituent bookkeeping and basin-level summaries.
  cs_hdr_aqu: Public output header record for aquifer constituent files; initialized with
    fixed column labels for daily, monthly, yearly, and average-annual aquifer output tables.
type_components:
  cs_balance_aqu:
    csgw: kg; mass loaded to streams from the aquifer.
    rchrg: kg; mass reaching the water table by recharge.
    seep: kg; mass seepage out of the aquifer.
    irr: kg; mass removed via irrigation pumping.
    div: kg; mass removed or added via diversion.
    sorb: kg; mass transferred from sorbed phase to dissolved phase.
    rctn: kg; mass transferred by chemical reaction.
    mass: kg; mass stored in the aquifer.
    conc: g/m3; concentration in groundwater.
    srbd: kg; mass sorbed to aquifer material.
  object_cs_balance_aqu:
    cs: Allocatable array of `cs_balance_aqu` records for the simulated constituents tracked
      for that aquifer.
  output_cs_header:
    day: Daily time label column.
    mo: Month label column.
    day_mo: Day-of-month label column.
    yrc: Year label column.
    isd: Unit or identifier label column.
    id: GIS identifier label column.
    seo4: Groundwater selenate mass column.
    seo3: Groundwater selenite mass column.
    born: Groundwater boron mass column.
    seo4r: Recharge selenate mass column.
    seo3r: Recharge selenite mass column.
    bornr: Recharge boron mass column.
    seo4s: Seepage selenate mass column.
    seo3s: Seepage selenite mass column.
    borns: Seepage boron mass column.
    seo4i: Irrigation selenate mass column.
    seo3i: Irrigation selenite mass column.
    borni: Irrigation boron mass column.
    seo4v: Diversion selenate mass column.
    seo3v: Diversion selenite mass column.
    bornv: Diversion boron mass column.
    seo4b: Sorption selenate mass column.
    seo3b: Sorption selenite mass column.
    bornb: Sorption boron mass column.
    seo4t: Reaction selenate mass column.
    seo3t: Reaction selenite mass column.
    bornt: Reaction boron mass column.
    seo4m: Stored selenate mass column.
    seo3m: Stored selenite mass column.
    bornm: Stored boron mass column.
    seo4c: Groundwater selenate concentration column.
    seo3c: Groundwater selenite concentration column.
    bornc: Groundwater boron concentration column.
    seo4d: Sorbed selenate mass column.
    seo3d: Sorbed selenite mass column.
    bornd: Sorbed boron mass column.
type_summaries:
  cs_balance_aqu: One aquifer constituent mass-balance record for a single aquifer and constituent,
    holding fluxes, storage, concentration, and sorbed mass used by aquifer chemistry and
    output routines.
  object_cs_balance_aqu: Container for one aquifer's constituent balance array, with allocatable
    per-constituent `cs` records.
  output_cs_header: Fixed text labels for aquifer constituent output columns across daily,
    monthly, yearly, and average-annual reports.
---

<!-- facts:header -->

cs_aquifer owns the aquifer constituent balance records and the aquifer constituent output header. It provides the daily, monthly, yearly, and average-annual balance containers used by aquifer chemistry, irrigation, sorption, reaction, and output routines, and it also holds the formatted column labels that the constituent output writers print.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container. It does not define startup procedures itself; `aqu_initial` allocates and zeroes the balance arrays, while `header_const` uses the header record when opening aquifer constituent output files.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:aqu_cs_output] | `unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067` | `acsb_d, acsb_m, acsb_y, acsb_a, bacs_d, bacs_m` | Reads daily balances from `acsb_d`, accumulates them into monthly, yearly, and average-annual aquifer constituent totals, and writes the requested output units. |
| [sym:cs_balance] | `unit_6080, unit_6082, unit_6084, unit_6086` | `acsb_d, acsb_m, acsb_y, acsb_a, bacs_d, bacs_m` | Reads aquifer daily constituent flux totals from `acsb_d` when building basin constituent balance summaries. |
| [sym:header_const] | `unit_6080, unit_6082, unit_6084, unit_6086, unit_6021, unit_6022, unit_6023, unit_6024, unit_6025, unit_6026, unit_6027, unit_6028, unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067, unit_6030, unit_6031, unit_6032, unit_6033, unit_6034, unit_6035, unit_6036, unit_6037, unit_6040, unit_6041, unit_6042, unit_6043, unit_6044, unit_6045, unit_6046, unit_6047, unit_6070, unit_6071, unit_6072, unit_6073, unit_6074, unit_6075, unit_6076, unit_6077, unit_6090, unit_6091, unit_6092, unit_6093, unit_6094, unit_6095, unit_6096, unit_6097` | `acsb_d, acsb_m, acsb_y, acsb_a, bacs_d, bacs_m` | Uses `cs_hdr_aqu` to print aquifer constituent header rows for the configured output units and CSV files. |

## Key Consumers

Aquifer chemistry and accounting routines use this module as the shared balance-store and header definition. Some routines update daily aquifer constituent state, others roll that state into period summaries or print it to output files.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu_cs_output] | cs_aquifer | Uses the shared aquifer balance records to accumulate daily values into monthly, yearly, and average-annual outputs and to print the aquifer constituent headers. |
| [sym:cs_balance] | cs_aquifer | Uses the daily aquifer constituent totals when building basin-wide constituent mass-balance summaries for seo4, seo3, and boron. |
| [sym:header_const] | cs_aquifer | Writes `cs_hdr_aqu` into aquifer constituent output files so the daily, monthly, yearly, and average-annual columns are labeled consistently. |
| [sym:aqu_1d_control] | cs_aquifer | Stores daily recharge, groundwater discharge, seepage, mass, and concentration into `acsb_d` for each simulated constituent. |
| [sym:aqu_initial] | cs_aquifer | Allocates the aquifer constituent balance arrays and resets their monthly, yearly, and average-annual accumulators before simulation begins. |
| [sym:cs_irrig] | cs_aquifer | Increments the aquifer irrigation-loss accumulator in `acsb_d` when groundwater irrigation withdraws constituent mass. |
| [sym:cs_rctn_aqu] | cs_aquifer | Stores the reaction-induced mass change for aquifer selenium species in `acsb_d` after the groundwater chemistry step. |
| [sym:cs_sorb_aqu] | cs_aquifer | Stores sorption transfer and sorbed-phase mass in `acsb_d` after enforcing aquifer equilibrium sorption. |

## Lineage

`cs_aquifer.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `2ee1889` (2025-11-17, "Cleanup of sine warnings."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cs_aquifer.f90` are listed.

- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `2405a68` (2024-07-16) — Fixing for Compiling
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No Git Lineage Evidence commits were resolved for cs_aquifer.f90:2-77.
- The parser-extracted importer list and completed procedure evidence indicate `bacs_y`, `bacs_a`, and `csbz_aqu` are declared here, but the provided completed overlays do not show direct use of those specific objects.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
