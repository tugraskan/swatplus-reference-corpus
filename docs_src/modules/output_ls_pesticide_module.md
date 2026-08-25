---
kind: module
symbol: output_ls_pesticide_module
title: output_ls_pesticide_module
status: filled
source_hash: 2fe76ecde0071d2e
version_label: SWAT+ 62.0.0
variables:
  pestbz: Zero-valued template instance of pesticide_balance. It provides the reset state
    used by output and time-control routines when clearing daily, monthly, yearly, or average-annual
    pesticide balance accumulators.
  hpestb_d: Allocatable per-HRU daily pesticide balance array. It is populated during the
    HRU pesticide process sequence and later read by output routines, transport routines,
    and basin aggregation routines. Units are kg/ha for the balance components stored in each
    pesticide_balance record.
  hpestb_m: Allocatable per-HRU monthly pesticide balance array. It stores month-to-date pesticide
    balances for HRU reporting and is accumulated from hpestb_d before month-end output.
  hpestb_y: Allocatable per-HRU yearly pesticide balance array. It stores year-to-date pesticide
    balances for HRU reporting and is accumulated from hpestb_m before year-end output; time_control
    resets it to pestbz after use in calibration/output sequencing.
  hpestb_a: Allocatable per-HRU average-annual pesticide balance array. It stores accumulated
    multi-year pesticide balances for HRU reporting and is written at simulation end before
    being reset.
  rupestb_d: Allocatable per-object daily pesticide balance array for aquifer/reservoir-related
    pesticide output paths. The context shows it as module state available to the aquifer
    and basin pesticide output family, but no direct source comments or initialization lines
    were extracted.
  rupestb_m: Allocatable per-object monthly pesticide balance array for aquifer/reservoir-related
    pesticide output paths. The context packet lists it as public module state, but no direct
    initialization or consumption line was resolved here.
  rupestb_y: Allocatable per-object yearly pesticide balance array for aquifer/reservoir-related
    pesticide output paths. The context packet lists it as public module state, but no direct
    initialization or consumption line was resolved here.
  rupestb_a: Allocatable per-object average-annual pesticide balance array for aquifer/reservoir-related
    pesticide output paths. The context packet lists it as public module state, but no direct
    initialization or consumption line was resolved here.
  bpestb_d: Basin-level daily pesticide balance container. basin_ls_pest_output sums HRU daily
    balances into bpestb_d before writing daily basin pesticide output.
  bpestb_m: Basin-level monthly pesticide balance container. basin_ls_pest_output accumulates
    bpestb_d into bpestb_m for month-end reporting.
  bpestb_y: Basin-level yearly pesticide balance container. basin_ls_pest_output rolls monthly
    basin balances into bpestb_y for year-end reporting.
  bpestb_a: Basin-level average-annual pesticide balance container. basin_ls_pest_output accumulates
    yearly balances into bpestb_a for simulation-average reporting.
  pestb_hdr: Character header record for pesticide output tables. header_pest writes this
    record into HRU and basin pesticide text/CSV files so the output columns match the pesticide-balance
    fields.
type_components:
  pesticide_balance:
    plant: 'kg/ha: pesticide on plant foliage'
    soil: 'kg/ha: pesticide in soil'
    sed: 'kg/ha: pesticide loading from HRU sorbed onto sediment'
    surq: 'kg/ha: amount of pesticide type lost in surface runoff in HRU'
    latq: 'kg/ha: amount of pesticide in lateral flow in HRU'
    tileq: 'kg/ha: amount of pesticide in tile flow in HRU'
    perc: 'kg/ha: amount of pesticide leached past bottom of soil'
    apply_s: 'kg/ha: amount of pesticide applied on soil'
    apply_f: 'kg/ha: amount of pesticide applied on foliage'
    decay_s: 'kg/ha: amount of pesticide decayed on soil'
    decay_f: 'kg/ha: amount of pesticide decayed on foliage'
    wash: 'kg/ha: amount of pesticide washed off from plant to soil'
    metab_s: 'kg/ha: amount of pesticide metabolized from parent in soil'
    metab_f: 'kg/ha: amount of pesticide metabolized from parent on foilage'
    pl_uptake: 'kg/ha: amount of pesticide taken up by plants'
    in_plant: 'kg/ha: pesticide in plant foliage'
  object_pesticide_balance:
    pest: Allocatable array of pesticide_balance records, one entry per simulated pesticide.
  output_pestbal_header:
    day: Printed column label for Julian day
    mo: Printed column label for month number
    day_mo: Printed column label for calendar day within month
    yrc: Printed column label for year count
    isd: Printed column label for unit index
    id: Printed column label for GIS identifier
    name: Printed column label for object name
    pest: Printed column label for pesticide name
    on_plant: Printed column label for pesticide mass on plant foliage
    soil: Printed column label for pesticide mass in soil
    sed: Printed column label for pesticide mass on sediment
    surq: Printed column label for pesticide mass in surface runoff
    latq: Printed column label for pesticide mass in lateral flow
    tileq: Printed column label for pesticide mass in tile flow
    perc: Printed column label for pesticide mass leached below the soil profile
    apply_s: Printed column label for pesticide applied to soil
    apply_f: Printed column label for pesticide applied to foliage
    decay_s: Printed column label for pesticide decayed in soil
    decay_f: Printed column label for pesticide decayed on foliage
    wash: Printed column label for pesticide washed from foliage to soil
    metab_s: Printed column label for soil-side metabolite mass
    metab_f: Printed column label for foliage-side metabolite mass
    uptake: Printed column label for plant uptake mass
    in_plant: Printed column label for pesticide mass inside plant tissue
type_summaries:
  pesticide_balance: Per-pesticide mass-balance record for HRU and basin reporting. It carries
    current pesticide mass on foliage and in soil, plus route-specific and process-specific
    gains/losses needed for daily-to-annual pesticide output accounting.
  object_pesticide_balance: Container that groups pesticide_balance records by reporting period
    for one object or basin. The allocatable pest array holds the per-pesticide balances for
    that period.
  output_pestbal_header: Fixed-width header strings for pesticide balance output tables. Each
    component names one printed column in the HRU and basin pesticide output files.
---

<!-- facts:header -->

Owns the shared pesticide-balance data structures and output header record used by HRU, basin, channel, reservoir, aquifer, wetland, and initialization/output routines. It also defines the overloaded arithmetic operators that combine and scale pesticide balance records for reporting and accumulator management.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-operator container. It does not contain a startup subroutine; its public arrays and header record are allocated or seeded by other routines such as hru_output_allo, pesticide_init, hru_control, and time_control.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:aqu_pesticide_output] | `unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015` | `pestbz, rupestb_d` | Reads the shared pesticide-balance template and object-level pesticide balance state to format aquifer pesticide output records for daily, monthly, yearly, and average-annual reporting. |
| [sym:basin_aqu_pest_output] | `unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007` | `pestbz, rupestb_d` | Uses the shared pesticide-balance state as part of basin-level aquifer pesticide reporting across the configured time steps. |
| [sym:basin_ch_pest_output] | `unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839` | `pestbz` | Uses the pesticide-balance template and shared output state while assembling basin/channel pesticide output records. |
| [sym:basin_ls_pest_output] | `unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `pestbz, hpestb_d, bpestb_d, bpestb_m, bpestb_y, bpestb_a` | Aggregates daily HRU pesticide balances into basin totals, writes them to output units, and resets the basin accumulators to the zero template after reporting. |
| [sym:basin_res_pest_output] | `unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855` | `pestbz, rupestb_d` | Uses the module as shared pesticide output state for reservoir-related basin reporting. |
| [sym:ch_cs_output] | `unit_6030, unit_6031, unit_6032, unit_6033, unit_6034, unit_6035, unit_6036, unit_6037` | `pestbz` | Imports the module as part of the shared output-state dependency set for channel constituent output processing. |
| [sym:ch_salt_output] | `unit_5030, unit_5031, unit_5032, unit_5033, unit_5034, unit_5035, unit_5036, unit_5037` | `pestbz` | Imports the module as a shared output dependency while writing channel salt reports. |
| [sym:cha_pesticide_output] | `unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815` | `pestbz` | Uses the shared pesticide-balance definitions while writing channel pesticide balance output. |
| [sym:cs_hru_init] | `unit_100100` | `pestbz` | Imports the module as a shared dependency in HRU initialization, but the extracted source does not show a direct reference to its public state. |
| [sym:header_pest] | `unit_2800, unit_9000, unit_2804, unit_2801, unit_2805, unit_2802, unit_2806, unit_2803, unit_2807, unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815, unit_2816, unit_2820, unit_2817, unit_2821, unit_2818, unit_2822, unit_2819, unit_2823, unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007, unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015, unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839, unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855, unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `pestb_hdr` | Writes the shared pesticide header record into the active pesticide output files so printed columns match the balance fields. |
| [sym:hru_control] | `unit_100100` | `hpestb_d` | Zeros the daily HRU pesticide balance record by multiplying it by zero before the next HRU time step. |
| [sym:hru_pesticide_output] | `unit_2800, unit_2804, unit_2801, unit_2805, unit_2802, unit_2806, unit_2803, unit_2807` | `pestbz, hpestb_d, hpestb_m, hpestb_y, hpestb_a` | Reads the daily HRU pesticide balance, rolls it into monthly/yearly/average-annual accumulators, writes the selected report intervals, and resets the accumulators after use. |

## Key Consumers

The module is used mainly by three groups: setup routines that allocate or seed pesticide balance storage, HRU/process routines that update daily balance components during pesticide movement and fate calculations, and output/header routines that print daily-to-annual pesticide summaries.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_ls_pest_output] | output_ls_pesticide_module | Uses the shared pesticide balance containers to sum daily HRU pesticide balances into basin daily, monthly, yearly, and average-annual totals, then writes and resets those basin accumulators. |
| [sym:header_pest] | output_ls_pesticide_module | Writes the shared pesticide header record into the HRU and basin pesticide output files so the printed columns match the balance fields. |
| [sym:hru_pesticide_output] | output_ls_pesticide_module | Reads the daily HRU pesticide balance, rolls it into monthly, yearly, and average-annual accumulators, writes the selected report intervals, and resets the accumulators after use. |
| [sym:pesticide_init] | output_ls_pesticide_module | Seeds the daily HRU pesticide balance state, including the initial plant-side pesticide load, so later pesticide output routines can report a complete starting balance. |
| [sym:aqu_pesticide_output] | output_ls_pesticide_module | Uses the module as shared pesticide output state while constructing aquifer pesticide reports for the configured time steps. |
| [sym:basin_aqu_pest_output] | output_ls_pesticide_module | Relies on the shared pesticide output module as part of basin aquifer pesticide reporting, though no specific symbol was resolved from the excerpt. |
| [sym:basin_ch_pest_output] | output_ls_pesticide_module | Imports the module as shared output state for basin/channel pesticide reporting, with no direct symbol use resolved in the packet. |
| [sym:basin_res_pest_output] | output_ls_pesticide_module | Uses the module as shared pesticide output state for reservoir basin reporting, though the excerpt does not resolve a direct symbol reference. |
| [sym:ch_cs_output] | output_ls_pesticide_module | Imports the module as part of the shared output-state dependency set for channel constituent reporting. |
| [sym:ch_salt_output] | output_ls_pesticide_module | Imports the module as a shared dependency in channel salt output processing, with no direct symbol reference shown in the extracted source. |
| [sym:cha_pesticide_output] | output_ls_pesticide_module | Uses the shared pesticide balance definitions while writing channel pesticide output for the selected reach and time step. |
| [sym:cs_hru_init] | output_ls_pesticide_module | The module is imported as part of HRU initialization dependencies, but the extracted source does not show a direct use of its public state. |
| [sym:res_cs_output] | output_ls_pesticide_module | Imports the module as shared output-state context for reservoir constituent reporting. |
| [sym:res_pesticide_output] | output_ls_pesticide_module | Imports the module as the shared pesticide output dependency used by reservoir pesticide reporting routines. |
| [sym:res_salt_output] | output_ls_pesticide_module | Imports the module as a shared output dependency within the reservoir salt reporting family. |
| [sym:salt_hru_init] | output_ls_pesticide_module | The module is imported in the salt initialization workflow, but the excerpt does not show a direct use of its state. |
| [sym:wet_cs_output] | output_ls_pesticide_module | Imports the module as a shared output dependency for wetland constituent reporting. |
| [sym:wet_salt_output] | output_ls_pesticide_module | Imports the module as shared output-state context for wetland salt reporting. |
| [sym:hru_hyds] | output_ls_pesticide_module | Uses the daily HRU pesticide balances to populate the pesticide loads routed into surface runoff, percolation, lateral flow, and tile flow hydrographs. |
| [sym:hru_output_allo] | output_ls_pesticide_module | Allocates the HRU and basin pesticide balance arrays so later daily, monthly, yearly, and average-annual accumulation can store mass balances. |
| [sym:pest_apply] | output_ls_pesticide_module | Updates the daily pesticide balance fields for foliage and soil application so later pesticide output can report management additions. |
| [sym:pest_decay] | output_ls_pesticide_module | Updates daily pesticide balance fields for soil and foliage decay plus metabolite production so later output can report parent loss and daughter gains. |
| [sym:pest_lch] | output_ls_pesticide_module | Updates daily pesticide balance fields for runoff, lateral, tile, and percolation losses so later pesticide output can report soluble transport. |
| [sym:pest_pesty] | output_ls_pesticide_module | Updates the daily sediment-bound pesticide export field so later output can report sorbed pesticide loss with sediment. |
| [sym:pest_pl_up] | output_ls_pesticide_module | Tracks total plant uptake in the daily pesticide balance so the reporting layer can include plant-removal mass. |
| [sym:pest_soil_tot] | output_ls_pesticide_module | Aggregates foliage, in-plant, and soil pesticide stores into the daily HRU balance used by downstream pesticide reporting. |
| [sym:pest_washp] | output_ls_pesticide_module | Updates the daily wash-off balance so pesticide output can report mass moved from foliage to soil. |
| [sym:res_cs_output] | output_ls_pesticide_module | Imports the module as shared output-state context for reservoir constituent reporting. |
| [sym:res_pesticide_output] | output_ls_pesticide_module | Imports the module as the shared pesticide output dependency used by reservoir pesticide reporting routines. |
| [sym:res_salt_output] | output_ls_pesticide_module | Imports the module as a shared output dependency within the reservoir salt reporting family. |
| [sym:salt_hru_init] | output_ls_pesticide_module | The module is imported in the salt initialization workflow, but the excerpt does not show a direct use of its state. |
| [sym:smp_filter] | output_ls_pesticide_module | Scales the daily HRU pesticide runoff and sediment balances to reflect filter-strip removal before those balances are reported or routed onward. |
| [sym:smp_grass_wway] | output_ls_pesticide_module | Scales the daily HRU pesticide runoff and sediment balances to reflect grassed-waterway removal before those balances are reported or routed onward. |
| [sym:stor_surfstor] | output_ls_pesticide_module | No direct symbol from this module was resolved in the extracted source; the routine imports the module as part of the shared output dependency set. |
| [sym:swr_substor] | output_ls_pesticide_module | No direct symbol from this module was resolved in the extracted source; the routine imports the module as part of the shared output dependency set. |
| [sym:time_control] | output_ls_pesticide_module | Resets the yearly HRU pesticide balance array to the zero template after the annual output/calibration pass so the next reporting cycle starts clean. |
| [sym:wet_cs_output] | output_ls_pesticide_module | Imports the module as a shared output dependency for wetland constituent reporting. |
| [sym:wet_salt_output] | output_ls_pesticide_module | Imports the module as shared output-state context for wetland salt reporting. |

## Lineage

`output_ls_pesticide_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `output_ls_pesticide_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `output_ls_pesticide_module` has no extracted module-level documentation comment.
- Reader rows are representative rather than exhaustive for initialization and output dependencies; some imported procedures are listed only in the importer appendix.
- No Git lineage commits were resolved for this source span, so lineage_impacts is intentionally empty.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
