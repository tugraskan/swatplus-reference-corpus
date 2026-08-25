---
kind: module
symbol: ch_salt_module
title: ch_salt_module
status: filled
source_hash: bf826cf6959e5d6a
version_label: SWAT+ 62.0.0
variables:
  ch_saltbz: Zero-valued salt balance template for one ion. Visible source declares it, while
    direct output and balance routines reset fields explicitly.
  chsalt_d: Daily SWAT-deg channel salt output array. `sd_channel_read` allocates one channel
    slot per `sp_ob%chandeg` and one salt slot per `cs_db%num_salts`.
  chsalt_m: Monthly accumulation array. `ch_salt_output` adds daily salt values, averages
    `water` and `conc` at month end, optionally writes monthly output, then zeros the monthly
    fields.
  chsalt_y: Yearly accumulation array. `ch_salt_output` adds monthly values, averages `water`
    and `conc` at year end, optionally writes yearly output, then zeros the yearly fields.
  chsalt_a: Average-annual accumulation array. `ch_salt_output` adds yearly values and divides
    by `time%nbyr` for average annual channel salt output.
  chsalt_hdr: Column-label record for channel salt output files. `header_salt` writes label
    groups for sulfate, calcium, magnesium, sodium, potassium, chloride, carbonate, and bicarbonate.
type_components:
  ch_salt_balance:
    tot_in: Total salt-ion mass entering the channel during the interval.
    gw_in: Salt-ion mass entering from groundwater interaction.
    tot_out: Salt-ion mass leaving the channel.
    seep: Salt-ion mass lost through channel seepage.
    irr: Salt-ion mass removed by irrigation withdrawal.
    div: Salt-ion mass added or removed by diversion.
    water: Salt-ion mass remaining in channel water at the end of the interval; output code
      averages this state over monthly/yearly periods.
    conc: End-of-interval salt-ion concentration in channel water; output code averages this
      state over monthly/yearly periods.
  ch_salt_output:
    salt: Dynamic salt-ion dimension sized from `cs_db%num_salts` in `sd_channel_read`.
  ch_salt_header:
    day: Julian-day label.
    mo: Month label.
    day_mo: Day-of-month label.
    yrc: Year label.
    isd: Channel unit label.
    id: GIS id label.
    so4in: Sulfate inflow label.
    cain: Calcium inflow label.
    mgin: Magnesium inflow label.
    nain: Sodium inflow label.
    kin: Potassium inflow label.
    clin: Chloride inflow label.
    co3in: Carbonate inflow label.
    hco3in: Bicarbonate inflow label.
    so4gw: Sulfate groundwater inflow label.
    cagw: Calcium groundwater inflow label.
    mggw: Magnesium groundwater inflow label.
    nagw: Sodium groundwater inflow label.
    kgw: Potassium groundwater inflow label.
    clgw: Chloride groundwater inflow label.
    co3gw: Carbonate groundwater inflow label.
    hco3gw: Bicarbonate groundwater inflow label.
    so4out: Sulfate outflow label.
    caout: Calcium outflow label.
    mgout: Magnesium outflow label.
    naout: Sodium outflow label.
    kout: Potassium outflow label.
    clout: Chloride outflow label.
    co3out: Carbonate outflow label.
    hco3out: Bicarbonate outflow label.
    so4seep: Sulfate seepage label.
    caseep: Calcium seepage label.
    mgseep: Magnesium seepage label.
    naseep: Sodium seepage label.
    kseep: Potassium seepage label.
    clseep: Chloride seepage label.
    co3seep: Carbonate seepage label.
    hco3seep: Bicarbonate seepage label.
    so4irr: Sulfate irrigation-withdrawal label.
    cairr: Calcium irrigation-withdrawal label.
    mgirr: Magnesium irrigation-withdrawal label.
    nairr: Sodium irrigation-withdrawal label.
    kirr: Potassium irrigation-withdrawal label.
    clirr: Chloride irrigation-withdrawal label.
    co3irr: Carbonate irrigation-withdrawal label.
    hco3irr: Bicarbonate irrigation-withdrawal label.
    so4div: Sulfate diversion label.
    cadiv: Calcium diversion label.
    mgdiv: Magnesium diversion label.
    nadiv: Sodium diversion label.
    kdiv: Potassium diversion label.
    cldiv: Chloride diversion label.
    co3div: Carbonate diversion label.
    hco3div: Bicarbonate diversion label.
    so4: Sulfate channel-water mass label.
    ca: Calcium channel-water mass label.
    mg: Magnesium channel-water mass label.
    na: Sodium channel-water mass label.
    k: Potassium channel-water mass label.
    cl: Chloride channel-water mass label.
    co3: Carbonate channel-water mass label.
    hco3: Bicarbonate channel-water mass label.
    so4c: Sulfate concentration label.
    cac: Calcium concentration label.
    mgc: Magnesium concentration label.
    nac: Sodium concentration label.
    kc: Potassium concentration label.
    clc: Chloride concentration label.
    co3c: Carbonate concentration label.
    hco3c: Bicarbonate concentration label.
type_summaries:
  ch_salt_balance: Mass and concentration fields for one salt ion in one SWAT-deg channel
    over one reporting interval.
  ch_salt_output: Per-channel wrapper that allocates one `ch_salt_balance` element for each
    configured salt ion.
  ch_salt_header: Fixed-width header labels for channel salt output files.
---

<!-- facts:header -->

Channel storage for salt-ion output and mass-balance terms. The module declares one salt balance record, allocatable per-channel/per-ion reporting arrays, and fixed output-header labels for SWAT-deg channel salt reports.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module has no reader of its own. `sd_channel_read` allocates and initializes the per-channel salt arrays after channel counts and configured salt-ion counts are available.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:sd_channel_read] | `sp_ob%chandeg and cs_db%num_salts` | `chsalt_d, chsalt_m, chsalt_y, chsalt_a` | Allocates one output wrapper per SWAT-deg channel, then allocates each wrapper `%salt` array when `cs_db%num_salts > 0`. It initializes monthly, yearly, and average annual output state fields to zero and allocates channel water/benthic salt arrays. |

## Key Consumers

The module is shared by channel salt routing, channel salt output, headers, and basin-wide salt mass-balance reset logic.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:sd_channel_read] | chsalt_d, chsalt_m, chsalt_y, chsalt_a | Allocates the channel salt report arrays and initializes reporting state when salt ions are configured. |
| [sym:sd_channel_control3] | chsalt_d | Stores daily groundwater input, seepage loss, and water/conc channel salt state for later output. |
| [sym:ch_salt_output] | chsalt_d, chsalt_m, chsalt_y, chsalt_a | Accumulates daily values to monthly/yearly/average annual arrays, writes channel salt reports, and zeros interval arrays after printing. |
| [sym:salt_balance] | chsalt_d | Resets daily channel salt irrigation, diversion, and groundwater-input terms after basin-wide salt balance output. |
| [sym:header_salt] | chsalt_hdr | Writes the channel salt header labels for daily, monthly, yearly, and average annual outputs. |
| [sym:salt_irrig] | chsalt_d | Updates channel salt output terms for irrigation withdrawals. |
| [sym:recall_salt] | chsalt_d | Adds recall/point-source salt mass into the channel reporting path. |

## Lineage

`ch_salt_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ch_salt_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The module has no module-level purpose comment.
- `ch_salt_header` hard-codes eight named ions, while the report arrays are allocated from `cs_db%num_salts`.
- `ch_saltbz` is declared as a zero template, but visible consumers mostly zero fields explicitly.
- Monthly and yearly output average `water` and `conc` but sum flux-like fields such as `tot_in`, `tot_out`, `seep`, `irr`, and `div`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
