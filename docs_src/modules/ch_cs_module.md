---
kind: module
symbol: ch_cs_module
title: ch_cs_module
status: filled
source_hash: a5f89e9d1466a00a
version_label: SWAT+ 62.0.0
variables:
  ch_csbz: Zero-valued balance template for one constituent record. Visible source declares
    it but the scanned direct channel path mainly resets fields explicitly rather than assigning
    this whole template.
  chcs_d: Daily SWAT-deg channel constituent output array. `sd_channel_read` allocates one
    channel slot per `sp_ob%chandeg` and one constituent slot per `cs_db%num_cs`; routing
    and balance code write daily values here.
  chcs_m: Monthly accumulation array. `ch_cs_output` adds daily channel values into this array,
    averages `water` and `conc` at month end, prints optional monthly reports, then zeros
    the monthly fields.
  chcs_y: Yearly accumulation array. `ch_cs_output` adds monthly values into this array, averages
    `water` and `conc` at year end, prints optional yearly reports, then zeros the yearly
    fields.
  chcs_a: Average-annual accumulation array. `ch_cs_output` adds yearly values here and divides
    by `time%nbyr` for average annual channel constituent output.
  chcs_hdr: Column-label record for constituent channel output files. `header_const` writes
    its label groups to the daily, monthly, yearly, and average annual channel constituent
    outputs.
type_components:
  ch_cs_balance:
    tot_in: Total constituent mass entering the channel during the interval.
    gw_in: Constituent mass entering from groundwater interaction.
    tot_out: Constituent mass leaving the channel.
    seep: Constituent mass lost through channel seepage.
    irr: Constituent mass removed by irrigation withdrawal.
    div: Constituent mass added or removed by channel diversion.
    water: Constituent mass remaining in channel water at the end of the interval; output
      code averages this state over monthly/yearly periods.
    conc: End-of-interval constituent concentration in channel water; output code averages
      this state over monthly/yearly periods.
  ch_cs_output:
    cs: Dynamic constituent dimension sized from `cs_db%num_cs` in `sd_channel_read`.
  ch_cs_header:
    day: Julian-day label.
    mo: Month label.
    day_mo: Day-of-month label.
    yrc: Year label.
    isd: Channel unit label.
    id: GIS id label.
    seo4in: Selenate inflow label.
    seo3in: Selenite inflow label.
    bornin: Boron inflow label.
    seo4gw: Selenate groundwater inflow label.
    seo3gw: Selenite groundwater inflow label.
    borngw: Boron groundwater inflow label.
    seo4out: Selenate outflow label.
    seo3out: Selenite outflow label.
    bornout: Boron outflow label.
    seo4seep: Selenate seepage label.
    seo3seep: Selenite seepage label.
    bornseep: Boron seepage label.
    seo4irr: Selenate irrigation-withdrawal label.
    seo3irr: Selenite irrigation-withdrawal label.
    bornirr: Boron irrigation-withdrawal label.
    seo4div: Selenate diversion label.
    seo3div: Selenite diversion label.
    borndiv: Boron diversion label.
    seo4: Selenate channel-water mass label.
    seo3: Selenite channel-water mass label.
    born: Boron channel-water mass label.
    seo4c: Selenate concentration label.
    seo3c: Selenite concentration label.
    bornc: Boron concentration label.
type_summaries:
  ch_cs_balance: Mass and concentration fields for one constituent in one SWAT-deg channel
    over one reporting interval.
  ch_cs_output: Per-channel wrapper that allocates one `ch_cs_balance` element for each configured
    constituent.
  ch_cs_header: Fixed-width header labels for channel constituent output files. The visible
    labels cover selenium forms and boron.
---

<!-- facts:header -->

Channel storage for generic constituent output and mass-balance terms. The module declares one per-constituent balance record, wraps it in allocatable channel arrays, and provides fixed output-header labels for channel constituent reports.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module owns data declarations, not file parsing. `sd_channel_read` allocates the report arrays after the SWAT-deg channel count and constituent counts are known.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:sd_channel_read] | `sp_ob%chandeg and cs_db%num_cs` | `chcs_d, chcs_m, chcs_y, chcs_a` | Allocates one output wrapper per SWAT-deg channel, then allocates each wrapper `%cs` array when `cs_db%num_cs > 0`. It initializes monthly, yearly, and average annual output state fields to zero and also allocates channel water/benthic constituent arrays. |

## Key Consumers

The module is shared by channel constituent routing, output, headers, and basin-wide mass-balance reset logic.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:sd_channel_read] | chcs_d, chcs_m, chcs_y, chcs_a | Allocates the channel constituent report arrays and initializes reporting state when generic constituents are configured. |
| [sym:sd_channel_control3] | chcs_d | Stores daily groundwater input, seepage loss, and water/conc channel constituent state for later output. |
| [sym:ch_cs_output] | chcs_d, chcs_m, chcs_y, chcs_a | Accumulates daily values to monthly/yearly/average annual arrays, writes channel constituent reports, and zeros interval arrays after printing. |
| [sym:cs_balance] | chcs_d | Resets daily channel constituent irrigation, diversion, and groundwater-input terms after basin-wide constituent balance output. |
| [sym:header_const] | chcs_hdr | Writes the channel constituent header labels for daily, monthly, yearly, and average annual outputs. |
| [sym:cs_irrig] | chcs_d | Updates channel constituent output terms for irrigation withdrawals. |
| [sym:recall_cs] | chcs_d | Adds recall/point-source constituent mass into the channel reporting path. |

## Lineage

`ch_cs_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ch_cs_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The module name and comments mark this as an RTB generic constituent addition, but there is no module-level purpose comment.
- The header type hard-codes selenium and boron labels even though allocation is driven by the generic `cs_db%num_cs` count.
- `ch_csbz` is declared as a zero template, but visible consumers mostly zero fields explicitly.
- Monthly and yearly output average `water` and `conc` but sum flux-like fields such as `tot_in`, `tot_out`, `seep`, `irr`, and `div`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
