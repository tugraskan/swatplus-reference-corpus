---
kind: module
symbol: ch_pesticide_module
title: ch_pesticide_module
status: filled
source_hash: b31229ac483873da
version_label: SWAT+ 62.0.0
variables:
  frsol: real scalar initialized to 0.0; fraction of pesticide in the reach that is soluble,
    computed during routing and used by channel pesticide process formulas and output.
  frsrb: real scalar initialized to 0.0; fraction of pesticide in the reach that is sorbed,
    computed during routing and used by channel pesticide process formulas and output.
  ch_pestbz: Baseline `ch_pesticide_processes` record initialized by default component values
    at declaration time; used as the zero/reset template for daily and period pesticide summaries
    in output and routing routines.
  chpst_d: Allocatable saved array of `ch_pesticide_output` records for daily channel pesticide
    outputs, one per channel-deg object; allocated in `sd_channel_read` and filled by routing/output
    routines, then read by basin and channel pesticide writers.
  chpst_m: Allocatable saved array of `ch_pesticide_output` records for monthly channel pesticide
    outputs, one per channel-deg object; allocated in `sd_channel_read`, accumulated from
    daily state, and written by channel pesticide output routines.
  chpst_y: Allocatable saved array of `ch_pesticide_output` records for yearly channel pesticide
    outputs, one per channel-deg object; allocated in `sd_channel_read`, accumulated from
    monthly state, and written by channel pesticide output routines.
  chpst_a: Allocatable saved array of `ch_pesticide_output` records for average-annual channel
    pesticide outputs, one per channel-deg object; allocated in `sd_channel_read`, accumulated
    from yearly state, and written at annual summary time.
  bchpst_d: Basin-level daily channel pesticide output record; allocated when pesticides are
    simulated, updated by basin output aggregation, and written to basin/channel pesticide
    day files.
  bchpst_m: Basin-level monthly channel pesticide output record; updated from daily basin
    totals and written to monthly basin/channel pesticide files.
  bchpst_y: Basin-level yearly channel pesticide output record; updated from monthly basin
    totals and written to yearly basin/channel pesticide files.
  bchpst_a: Basin-level average-annual channel pesticide output record; updated from yearly
    basin totals and written to average-annual basin/channel pesticide files.
  chpst: Single `ch_pesticide_output` record used as a working/current pesticide process container
    for a channel reach; filled by routing calculations and then copied into the channel-deg
    summary arrays.
  chpstz: Zero-valued `ch_pesticide_output` template allocated when pesticides are simulated;
    used to initialize or reset per-reach pesticide hydrograph records.
  chpest_hdr: Shared `ch_pesticide_header` record holding the text labels for pesticide output
    columns; written by header setup routines to channel and basin-channel pesticide files.
type_components:
  ch_pesticide_processes:
    tot_in: kg; total pesticide into reservoir/reach for the interval.
    sol_out: kg; soluble pesticide leaving the reservoir/reach.
    sor_out: kg; sorbed pesticide leaving the reservoir/reach.
    react: kg; pesticide lost through reactions in the water layer.
    metab: kg; pesticide metabolized from parent in the water layer.
    volat: kg; pesticide lost through volatilization.
    settle: kg; pesticide settling to the sediment layer.
    resus: kg; pesticide resuspended into lake/channel water.
    difus: kg; pesticide diffusing from sediment to water.
    react_bot: kg; pesticide lost from benthic sediment by reactions.
    metab_bot: kg; pesticide metabolized from parent in the benthic layer.
    bury: kg; pesticide lost from benthic sediment by burial.
    water: kg; pesticide in water at end of day.
    benthic: kg; pesticide in benthic sediment at end of day.
  ch_pesticide_output:
    pest: allocatable pesticide hydrographs
  ch_pesticide_header:
    day: column label for Julian day
    mo: column label for month
    day_mo: column label for day-of-month
    yrc: column label for year
    isd: column label for unit/object identifier
    id: column label for GIS identifier
    name: column label for object name
    pest: column label for pesticide name
    tot_in: total input mass column label, in kg
    sol_out: soluble خروج/output mass column label, in kg
    sor_out: sorbed خروج/output mass column label, in kg
    react: water-layer reaction loss column label, in kg
    metab: water-layer metabolite formation column label, in kg
    volat: volatilization loss column label, in kg
    settle: settling loss column label, in kg
    resus: resuspension column label, in kg
    difus: diffusion column label, in kg
    react_bot: benthic reaction loss column label, in kg
    metab_bot: benthic metabolite formation column label, in kg
    bury: benthic burial loss column label, in kg
    water: water storage column label, in kg
    benthic: benthic storage column label, in kg
type_summaries:
  ch_pesticide_processes: A single pesticide process balance record for one reach and one
    reporting interval. It stores mass entering, leaving, transforming, or remaining in the
    channel water and benthic sediment compartments.
  ch_pesticide_output: A container that holds an allocatable pesticide hydrograph vector for
    one reporting stream, such as daily, monthly, yearly, or average-annual outputs for a
    channel or basin-channel object.
  ch_pesticide_header: Column-label record used for pesticide output tables. It holds the
    fixed text headers for time/object identifiers and the pesticide process columns written
    to text and CSV output files.
---

<!-- facts:header -->

`ch_pesticide_module` owns the shared channel pesticide state used by SWAT+ routing and reporting: the soluble/sorbed fraction scalars, the zero baseline process record, the daily/monthly/yearly/average-annual channel and basin-channel pesticide hydrograph containers, and the header labels for pesticide output files. It also defines the pesticide process record and output/header types, plus overloaded operators for combining and scaling process records.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is primarily a declaration container. It does not contain startup procedures of its own; instead, `sd_channel_read` allocates the pesticide output arrays when pesticides are simulated, and the running routing/output procedures populate and reset the records during simulation.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:basin_ch_pest_output] | `unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839` | `frsol, frsrb, ch_pestbz, chpst_d, chpst_m, chpst_y` | Aggregates channel-day pesticide balances into basin-level daily, monthly, yearly, and average-annual summaries and writes them when the corresponding output flags are enabled. |
| [sym:cha_pesticide_output] | `unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815` | `frsol, frsrb, ch_pestbz, chpst_d, chpst_m, chpst_y` | Accumulates a selected channel-deg object's daily pesticide balance into monthly, yearly, and average-annual summary records and writes the period outputs. |
| [sym:header_pest] | `unit_2800, unit_9000, unit_2804, unit_2801, unit_2805, unit_2802, unit_2806, unit_2803, unit_2807, unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815, unit_2816, unit_2820, unit_2817, unit_2821, unit_2818, unit_2822, unit_2819, unit_2823, unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007, unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015, unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839, unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855, unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `frsol, frsrb, ch_pestbz, chpst_d, chpst_m, chpst_y` | Writes pesticide header rows to the active channel, basin-channel, and related pesticide output files. |
| [sym:sd_channel_read] | `channel-lte.cha` | `frsol, frsrb, ch_pestbz, chpst_d, chpst_m, chpst_y` | Allocates and initializes the channel pesticide output containers during channel-deg setup when pesticides are simulated. |

## Key Consumers

These routines import the module because it supplies the shared pesticide fractions, baseline record, summary containers, and header labels needed by routing, setup, and output code.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_ch_pest_output] | ch_pesticide_module | Builds basin-level channel pesticide daily, monthly, yearly, and average-annual balances from the per-channel daily records and uses `ch_pestbz` to reset the daily accumulator. |
| [sym:cha_pesticide_output] | ch_pesticide_module | Accumulates per-channel daily pesticide mass into monthly, yearly, and average-annual summaries, then resets period state back to the zero baseline after output. |
| [sym:header_pest] | ch_pesticide_module | Writes `chpest_hdr` to the open pesticide output files so the channel and basin pesticide reports have the correct column labels. |
| [sym:sd_channel_read] | ch_pesticide_module | Allocates the pesticide hydrograph containers for each channel-deg object and creates the zero-valued working records used later by routing and output code. |
| [sym:ch_rtpest] | ch_pesticide_module | Computes channel pesticide process masses into `chpst` and `chpst_d`, while `frsol` and `frsrb` provide the soluble and sorbed fractions used in the process formulas. |
| [sym:aqu_1d_control] | ch_pesticide_module | Supports the aquifer pesticide branch by providing the channel-side pesticide bookkeeping objects used when pesticide mass is routed onward to connected objects. |
| [sym:sd_channel_control3] | ch_pesticide_module | Copies the computed pesticide process fractions and masses into the channel-deg daily output records, including soluble/sorbed outflow and reaction, volatilization, settling, resuspension, diffusion, and burial masses. |

## Lineage

`ch_pesticide_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `15ff92f` (2026-04-08, "Refactor erosion and pesticide modules to incorporate biomass and ground cover f…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ch_pesticide_module.f90` are listed.

- `15ff92f` (2026-04-08) — Refactor erosion and pesticide modules to incorporate biomass and ground cover factors in calculations
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module-level documentation comment is absent in the source.
- No resolved Git lineage commits were available for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
