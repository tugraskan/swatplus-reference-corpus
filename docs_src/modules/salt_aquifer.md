---
kind: module
symbol: salt_aquifer
title: salt_aquifer
status: filled
source_hash: 226ecc028fa1b52f
version_label: SWAT+ 62.0.0
variables:
  testing_aquifer: A module-level real flag initialized to 0. Used as a simple testing or
    debug value within the salt aquifer module; no consuming routine is extracted in the context
    packet.
  asaltb_d: Daily aquifer salt balance state for each aquifer object. Each element holds one
    `object_salt_balance_aqu` record with per-salt fluxes and storage, initialized in `aqu_initial`
    and updated by `aqu_1d_control`, `salt_irrig`, `salt_chem_aqu`, `aqu_salt_output`, and
    `salt_balance`.
  asaltb_m: Monthly aquifer salt balance state for each aquifer object. Initialized to zero
    in `aqu_initial`, accumulated from daily values by `aqu_salt_output`, and reported by
    `aqu_salt_output` and `header_salt` consumers.
  asaltb_y: Yearly aquifer salt balance state for each aquifer object. Initialized to zero
    in `aqu_initial`, accumulated from daily values by `aqu_salt_output`, and used for yearly
    aquifer salt reporting.
  asaltb_a: Average-annual aquifer salt balance state for each aquifer object. Initialized
    to zero in `aqu_initial`, accumulated across simulation time by `aqu_salt_output`, and
    used for end-of-simulation aquifer salt reporting.
  basalt_d: Basin-wide aquifer salt balance record for the current day. Holds the aquifer-related
    salt summary that basin salt accounting routines can read for daily reporting.
  basalt_m: Basin-wide aquifer salt balance record accumulated for the current month.
  basalt_y: Basin-wide aquifer salt balance record accumulated for the current year.
  basalt_a: Basin-wide aquifer salt balance record accumulated for the average-annual basin
    summary.
  saltbz_aqu: Basin-wide aquifer salt balance record used for aquifer-zone or basin aquifer
    summary reporting; the source only shows the declaration and does not expose separate
    initialization logic.
  salt_hdr_aqu: Aquifer salt output header record used by `header_salt` when writing daily,
    monthly, yearly, and average-annual aquifer salt output files.
type_components:
  salt_balance_aqu:
    diss: '|kg       |salt ion mass transferred from sorbed phase to dissolved phase'
    rchrg: '|kg       |salt ion mass reaching the water table (recharge)'
    seep: '|kg       |salt ion mass seepage out of aquifer'
    saltgw: '|kg       |salt ion mass loaded to streams from the aquifer'
    irr: '|kg       |salt ion mass removed via irrigation (groundwater pumping)'
    div: '|kg       |salt ion mass removed via diversion'
    mass: '|kg       !salt ion mass in aquifer'
    conc: '|g/m3     |salt ion mass concentration in groundwater'
  object_salt_balance_aqu:
    salt: Allocatable array of `salt_balance_aqu` records, one per simulated salt ion.
  output_salt_header:
    day: Julian-day column label.
    mo: Month column label.
    day_mo: Day-of-month column label.
    yrc: Year column label.
    isd: Aquifer object unit label.
    id: GIS identifier label.
    so4: Groundwater sulfate column label.
    ca: Groundwater calcium column label.
    mg: Groundwater magnesium column label.
    na: Groundwater sodium column label.
    k: Groundwater potassium column label.
    cl: Groundwater chloride column label.
    co3: Groundwater carbonate column label.
    hco3: Groundwater bicarbonate column label.
    so4r: Recharge sulfate column label.
    car: Recharge calcium column label.
    mgr: Recharge magnesium column label.
    nar: Recharge sodium column label.
    kr: Recharge potassium column label.
    clr: Recharge chloride column label.
    co3r: Recharge carbonate column label.
    hco3r: Recharge bicarbonate column label.
    so4s: Seepage sulfate column label.
    cas: Seepage calcium column label.
    mgs: Seepage magnesium column label.
    nas: Seepage sodium column label.
    ks: Seepage potassium column label.
    cls: Seepage chloride column label.
    co3s: Seepage carbonate column label.
    hco3s: Seepage bicarbonate column label.
    so4i: Irrigation sulfate column label.
    cai: Irrigation calcium column label.
    mgi: Irrigation magnesium column label.
    nai: Irrigation sodium column label.
    ki: Irrigation potassium column label.
    cli: Irrigation chloride column label.
    co3i: Irrigation carbonate column label.
    hco3i: Irrigation bicarbonate column label.
    so4d: Diversion sulfate column label.
    cad: Diversion calcium column label.
    mgd: Diversion magnesium column label.
    nad: Diversion sodium column label.
    kd: Diversion potassium column label.
    cld: Diversion chloride column label.
    co3d: Diversion carbonate column label.
    hco3d: Diversion bicarbonate column label.
    so4m: Aquifer mass sulfate column label.
    cam: Aquifer mass calcium column label.
    mgm: Aquifer mass magnesium column label.
    nam: Aquifer mass sodium column label.
    km: Aquifer mass potassium column label.
    clm: Aquifer mass chloride column label.
    co3m: Aquifer mass carbonate column label.
    hco3m: Aquifer mass bicarbonate column label.
    so4c: Aquifer concentration sulfate column label.
    cac: Aquifer concentration calcium column label.
    mgc: Aquifer concentration magnesium column label.
    nac: Aquifer concentration sodium column label.
    kc: Aquifer concentration potassium column label.
    clc: Aquifer concentration chloride column label.
    co3c: Aquifer concentration carbonate column label.
    hco3c: Aquifer concentration bicarbonate column label.
    dssl: Dissolved-from-mineral total salt column label.
type_summaries:
  salt_balance_aqu: One aquifer salt-balance record for a single salt ion, storing fluxes
    into and out of groundwater plus the current aquifer salt mass and concentration.
  object_salt_balance_aqu: Container for the salt-balance array associated with one aquifer
    object.
  output_salt_header: Header record written to aquifer salt output tables and CSV files.
---

<!-- facts:header -->

Owns the shared aquifer-salt state used for groundwater salt balances and aquifer salt-output headers. It declares the per-aquifer daily, monthly, yearly, and average-annual salt balance arrays, a basin-wide aquifer salt accumulator, and the aquifer salt output header record that downstream salt accounting and reporting routines read and update.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container; it does not contain startup code itself. The working salt arrays are allocated and zeroed by `aqu_initial`, while `aqu_1d_control`, `salt_irrig`, `salt_chem_aqu`, `aqu_salt_output`, and `salt_balance` update the shared state during simulation.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:aqu_salt_output] | `unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067` | `testing_aquifer, asaltb_d, asaltb_m, asaltb_y, asaltb_a, basalt_d` | Reads the daily aquifer salt balance and accumulates it into monthly, yearly, and average-annual summaries before writing aquifer salt output files. |
| [sym:header_salt] | `unit_5080, unit_5082, unit_5084, unit_5086, unit_5021, unit_5022, unit_5023, unit_5024, unit_5025, unit_5026, unit_5027, unit_5028, unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067, unit_5030, unit_5031, unit_5032, unit_5033, unit_5034, unit_5035, unit_5036, unit_5037, unit_5040, unit_5041, unit_5042, unit_5043, unit_5044, unit_5045, unit_5046, unit_5047, unit_5070, unit_5071, unit_5072, unit_5073, unit_5074, unit_5075, unit_5076, unit_5077, unit_5090, unit_5091, unit_5092, unit_5093, unit_5094, unit_5095, unit_5096, unit_5097` | `testing_aquifer, asaltb_d, asaltb_m, asaltb_y, asaltb_a, basalt_d` | Uses the aquifer salt header record when opening and labeling the aquifer salt output files for each reporting interval. |
| [sym:salt_balance] | `unit_5080, unit_5082, unit_5084, unit_5086` | `testing_aquifer, asaltb_d, asaltb_m, asaltb_y, asaltb_a, basalt_d` | Reads daily aquifer salt fluxes when forming basin-wide daily, monthly, yearly, and average-annual salt balance totals. |

## Key Consumers

The module is consumed by aquifer state initialization, daily aquifer routing, irrigation salt transfers, aquifer salt chemistry, aquifer salt output, and basin salt-balance reporting.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu_salt_output] | salt_aquifer | Reads the daily aquifer salt balance arrays and rolls them into monthly, yearly, and average-annual summary records before writing the aquifer salt output files. |
| [sym:header_salt] | salt_aquifer | Writes the aquifer salt header record into each aquifer salt output file after the explanatory title text. |
| [sym:salt_balance] | salt_aquifer | Uses the daily aquifer salt flux arrays to build basin-wide salt totals and then resets the daily aquifer aquifer-salt bookkeeping fields. |
| [sym:aqu_1d_control] | salt_aquifer | Updates the daily aquifer salt balance as recharge enters storage, salt leaves with stream loading and seepage, and the per-ion mass and concentration are recomputed. |
| [sym:aqu_initial] | salt_aquifer | Allocates and zeros the daily, monthly, yearly, and average-annual aquifer salt balance arrays before simulation starts. |
| [sym:salt_chem_aqu] | salt_aquifer | Stores the dissolved salt mass change produced by the aquifer chemistry solve so later aquifer salt accounting can report mineral dissolution or precipitation effects. |
| [sym:salt_irrig] | salt_aquifer | Records the salt mass removed from aquifer water when irrigation pumping withdraws groundwater salt for transfer to the irrigated HRU or other source targets. |

## Lineage

`salt_aquifer.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `2ee1889` (2025-11-17, "Cleanup of sine warnings."). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `salt_aquifer.f90` are listed.

- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `2405a68` (2024-07-16) — Fixing for Compiling
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `salt_aquifer` has no extracted module-level documentation comment.
- `saltbz_aqu` is declared in the module source, but the context packet does not expose a separate initialization or consumer trace beyond its declaration and general aquifer-salt use.
- Source comments for `output_salt_header` are column labels rather than full field definitions; meanings were inferred directly from the header strings and the surrounding output code.
- No input-file contract is exposed by the source because this module declares state only and does not read external files directly.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
