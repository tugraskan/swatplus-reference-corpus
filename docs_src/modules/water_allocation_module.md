---
kind: module
symbol: water_allocation_module
title: water_allocation_module
status: filled
source_hash: a94a85b1922f07c2
version_label: SWAT+ 62.0.0
variables:
  trans_m3: real scalar initialized to 0.0 in `water_allocation_module.f90:5`; shared transfer-volume
    scratch/state used by allocation workflows, especially demand and withdrawal logic in
    routines such as `actions`, `wallo_demand`, `wallo_control`, and `wallo_withdraw`. The
    source packet shows no unit comment on this declaration.
  trn_m3: m3     |demand
  walloz: Shared zero-valued `source_output` instance declared at `water_allocation_module.f90:66`.
    It is used as the canonical reset value for source-level demand/withdrawal/unmet accounting,
    including in `time_control` and `wallo_control`.
  wallo: Allocatable array of `water_allocation` records declared at `water_allocation_module.f90:77`;
    this is the main in-memory water-allocation database. It is populated by `water_allocation_read`
    and consumed by `command`, `conditions`, `wallo_control`, `wallo_demand`, `wallo_transfer`,
    `wallo_withdraw`, and the allocation output routines.
  wal: Pointer to a `water_allocation` record declared at `water_allocation_module.f90:78`.
    The source packet does not show its target assignment in this module; downstream routines
    treat it as shared water-allocation state, but the exact ownership initialization is not
    visible here.
  wtp: Allocatable array of `water_treatment_use_data` declared at `water_allocation_module.f90:100`.
    Populated by `water_treatment_read` and used by `wallo_control`, `wallo_demand`, `wallo_treatment`,
    and treatment-related output routines as the persistent water-treatment database.
  wuse: Allocatable array of `water_treatment_use_data` declared at `water_allocation_module.f90:101`.
    Populated by `water_use_read` and used by `wallo_use` and related output/accounting routines
    as the persistent water-use database.
  osrc: Allocatable array of `outside_basin_source` declared at `water_allocation_module.f90:115`.
    Populated by `water_osrc_read` and used by `wallo_demand`, `wallo_withdraw`, `wallo_control`,
    and outside-source allocation logic.
  orcv: Allocatable array of `outside_basin_receive` declared at `water_allocation_module.f90:122`.
    Populated by `water_orcv_read` and used where outside-basin receiving-object metadata
    is required.
  wtow: Allocatable array of `water_transfer_data` declared at `water_allocation_module.f90:139`.
    Populated by `water_tower_read` and consumed by transfer/withdrawal routines for water-tower
    routing and accounting.
  pipe: Allocatable array of `water_transfer_data` declared at `water_allocation_module.f90:140`.
    Populated by `water_pipe_read` and consumed by `wallo_transfer` for conveyance-loss handling.
  canal: Allocatable array of `water_canal_data` declared at `water_allocation_module.f90:162`.
    Populated by `water_canal_read` and consumed by `gwflow_read` and `wallo_canal` for canal
    routing, seepage, and aquifer-loss handling.
  om_init_name: Allocatable character array declared at `water_allocation_module.f90:164`.
    The source packet does not show a direct reader in this module; it is a shared name table
    for organic/mineral initialization entries used by allocation crosswalks.
  om_treat_name: Allocatable character array declared at `water_allocation_module.f90:165`.
    Populated by `om_treat_read` and used by `water_treatment_read` and `wallo_treat_output`
    as the human-readable treatment-name table.
  om_use_name: Allocatable character array declared at `water_allocation_module.f90:166`.
    Populated by `om_use_read` and used by `water_use_read` and `wallo_use_output` as the
    human-readable use-name table.
  om_osrc_name: Allocatable character array declared at `water_allocation_module.f90:167`.
    Populated by `om_osrc_read` and used as the name table for outside-source allocation records.
  wallod_out: Allocatable array of `water_allocation_output` declared at `water_allocation_module.f90:179`.
    It holds the daily source-level demand/withdrawal/unmet results for each allocation object
    and is written and reset by `wallo_control` and the various output routines.
  wallom_out: Allocatable array of `water_allocation_output` declared at `water_allocation_module.f90:180`.
    It accumulates monthly source-level allocation results for later monthly output and yearly
    roll-up.
  walloy_out: Allocatable array of `water_allocation_output` declared at `water_allocation_module.f90:181`.
    It accumulates yearly source-level allocation results for later yearly output and average-annual
    roll-up.
  walloa_out: Allocatable array of `water_allocation_output` declared at `water_allocation_module.f90:182`.
    It holds average-annual source-level allocation totals across the simulation period.
  wallo_hdr: Static `wallo_header` record declared at `water_allocation_module.f90:212`. It
    stores the printable column labels for the water-allocation report headers written by
    `header_water_allocation`.
  wallo_hdr_units: Static `wallo_header_units` record declared at `water_allocation_module.f90:242`.
    It stores the printable unit labels for the water-allocation report headers written by
    `header_water_allocation`.
type_components:
  transfer_source_objects:
    typ: source object type
    num: number of the source object
    conv_typ: conveyance type - pipe or pump
    conv_num: number of the conveyance object
    dtbl_lim: decision table name to set withdrawal limit of the source object
    wdraw_lim: actual withdrawal limit of source object (res-frac principal, aqu-max depth
      (m); cha-min flow (m3/s))
    frac: fraction of transfer supplied by the source
    comp: compensate if other source objects are past withdrawal threshold (y/n)
  transfer_receiving_objects:
    typ: receiving object type
    num: number of the receiving object
    frac: 'character (len=25) :: dtbl_rob = ""     !decision table name to set fraction to
      each receiving object

      soil layer to receive incoming tile flow'
  outside_basin_objects:
    daymoyr: recall file number - recall_db - daily, monthly or yearly
    aa: exco number in exco_db - ave annual constant
  water_transfer_objects:
    num: transfer object number
    ch_src: channel number in transfer object (0 if no channel)
    trn_typ: transfer type - decision table, recall, ave daily
    trn_typ_name: transfer type name of table or recall
    dtbl_num: number of decision table for demand amount (if used)
    dtbl_lum: number of decision table for demand amount for irrigation (if used)
    rec_num: number of recall file for demand amount (if used)
    amount: m3 per day for urban objects and mm for hru
    right: water right (sr -senior or jr - junior right)
    src_num: number of source objects
    dtbl_src: decision table name to allocate sources
    dtbl_src_num: number of source allocation decision table
    src: sequential source objects as listed in wallo object
    osrc: number of outside basin source object - recall_db.rec file
    rcv_num: number of receiving objects
    rcv: 'character (len=25) :: dtbl_rcv = ""     !decision table name to allocate receiving
      objects

      receiving object'
    unmet_m3: m3     |unmet demand for the object
    withdr_tot: m3     |total withdrawal of demand object from all sources
    irr_eff: irrigation in-field efficiency
    surq: surface runoff ratio
  source_output:
    demand: ha-m       !demand
    withdr: ha-m       |amoount withdrawn from the source
    unmet: ha-m       |unmet demand
  water_allocation:
    name: name of the water allocation object
    rule_typ: rule type to allocate water
    trn_cur: current transfer object
    trn_obs: number of transfer objects
    tot: total demand, withdrawal and unmet for entire allocation object
    trn: dimension by transfer objects
  water_treatment_use_data:
    name: name of the water treatment plant
    stor_mx: 'character (len=25) :: init = ""         !name of the intitial concentrations
      in wtp storage

      m3   !maximum storage in plant'
    lag_days: days !treatement time - lag outflow
    loss_fr: water loss during treament
    org_min: sediment, carbon, and nutrients
    pests: pesticides - ppm
    paths: pathogens - cfu
    hmets: heavy metals - ppm
    salts: salt ions - ppm
    constit: other constituents - ppm
    descrip: description
    iorg_min: sediment, carbon, and nutrients - pointer to om_use.wal
    ipests: pesticides
    ipaths: pathogens
    isalts: salt ions
    iconstit: other constituents
  outside_basin_source:
    name: name of outside basin source
    stor_mx: m3   !maximum storage in plant
    lag_days: days !treatement time - lag outflow
    loss_fr: water loss during treament
    iorg_min: sediment, carbon, and nutrients - pointer to om_use.wal
    ipests: pesticides
    ipaths: pathogens
    isalts: salt ions
    iconstit: other constituents
  outside_basin_receive:
    name: name of outside basin receiving object
    filename: name of outside basin receiving object
  aquifer_loss:
    aqu_num: aquifer number
    frac: fraction of loss in specific aquifer
  water_transfer_data:
    name: name of the water tower or pipe
    init: name of the intitial concentrations
    stor_mx: m3   !maximum storage in plant
    ddown_days: days !days to drawdown the storage to zero
    loss_fr: water loss during treament
    num_aqu: number of aquifers
    aqu_loss: aquifer-loss fractions by aquifer in `aqu_loss(:)`
  water_canal_data:
    name: name of the canal
    w_sta: name of nearby weather station
    init: name of the intitial concentrations in canal
    dtbl: name of decision table to determine canal outflow
    ddown_days: days !days to drawdown the storage to zero
    w: m    !top width of canal
    d: m    !depth of canal
    s: m    !slope of canal
    ss: m/m  !side slope of trapezoidal canal
    sat_con: to compute percolation from canal to groundwater
    loss_fr: water loss during treament
    bed_thick: m    !bed sediment thickness for Darcy seepage (gwflow; 0 if not used)
    div_id: recall diversion ID (gwflow; 0 if wallo-routed)
    day_beg: Julian day canal begins operation (gwflow external; 0 otherwise)
    day_end: Julian day canal ends operation (gwflow external; 0 otherwise)
    num_aqu: number of aquifers
    aqu_loss: aquifer-loss fractions by aquifer in `aqu_loss(:)`
  transfer_object_output:
    trn_flo: m3     |total transfer of the transfer object
    src: per-source `source_output` array stored in `src(:)`
  water_allocation_output:
    trn: transfer-object output array stored in `trn(:)`
  wallo_header:
    day: calendar day label
    mo: month label
    day_mo: day/month label
    yrc: year label
    itrn: transfer index label
    trn_typ: transfer type label
    trn_num: transfer number label
    rcv_typ: receiving object type label
    rcv_num: receiving object number label
    src1_obj: first source object label
    src1_typ: first source type label
    src1_num: first source number label
    trn1: demand label for source 1
    s1out: withdrawal label for source 1
    s1un: unmet label for source 1
    src2_typ: second source type label
    src2_num: second source number label
    trn2: demand label for source 2
    s2out: withdrawal label for source 2
    s2un: unmet label for source 2
    src3_typ: third source type label
    src3_num: third source number label
    trn3: demand label for source 3
    s3out: withdrawal label for source 3
    s3un: unmet label for source 3
  wallo_header_units:
    day: blank unit cell for day column
    mo: blank unit cell for month column
    day_mo: blank unit cell for day/month column
    yrc: blank unit cell for year column
    itrn: blank unit cell for transfer index column
    trn_typ: blank unit cell for transfer type column
    trn_num: blank unit cell for transfer number column
    rcv_typ: blank unit cell for receiving type column
    rcv_num: blank unit cell for receiving number column
    src1_obj: blank unit cell for source-object label column
    src1_typ: blank unit cell for source-type label column
    src1_num: blank unit cell for source-number label column
    trn1: m^3 units for source-1 demand
    s1out: m^3 units for source-1 withdrawal
    s1un: m^3 units for source-1 unmet
    src2_typ: blank unit cell for source-2 type column
    src2_num: blank unit cell for source-2 number column
    trn2: m^3 units for source-2 demand
    s2out: m^3 units for source-2 withdrawal
    s2un: m^3 units for source-2 unmet
    src3_typ: blank unit cell for source-3 type column
    src3_num: blank unit cell for source-3 number column
    trn3: m^3 units for source-3 demand
    s3out: m^3 units for source-3 withdrawal
    s3un: m^3 units for source-3 unmet
type_summaries:
  transfer_source_objects: transfer source objects
  transfer_receiving_objects: source and receiving objects
  outside_basin_objects: counters for outside basin source objects
  water_transfer_objects: water transfer objects
  source_output: source output
  water_allocation: water allocation
  water_treatment_use_data: water treatment and use data
  outside_basin_source: outside basin source object data
  outside_basin_receive: outside basin receivng object data
  aquifer_loss: aquifer loss
  water_transfer_data: water_transfer_data
  water_canal_data: canal data
  transfer_object_output: transfer object output
  water_allocation_output: water allocation output
  wallo_header: water allocation header labels
  wallo_header_units: water allocation header units
---

<!-- facts:header -->

Defines and owns the shared water-allocation state used across SWAT+ for transfer objects, source/receiving metadata, treatment and use databases, outside-basin records, canal/pipe/tower transfer data, and the daily/monthly/yearly/average-annual allocation output buffers. The module also provides the `source_output` arithmetic helpers used by allocation accounting. Initialization is performed by the various `*_read` routines and by `time_control`, while `wallo_control`, `wallo_demand`, `wallo_withdraw`, `wallo_transfer`, and the allocation output routines consume the state during simulation.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-helper container; it does not define startup routines. Shared state is populated by reader/setup procedures such as `water_allocation_read`, `water_treatment_read`, `water_use_read`, `water_osrc_read`, `water_orcv_read`, `water_pipe_read`, `water_tower_read`, `water_canal_read`, `om_treat_read`, `om_use_read`, `om_osrc_read`, and reset by `time_control`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Uses shared water-allocation state during management actions; the extracted snippets show `trn_m3` as the working transfer volume for action options such as flow diversion and transfer setting. |
| [sym:command] | `unit_out_hyd_sep` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Uses `wallo` while stepping through routing objects and calling `wallo_control`; the module provides the transfer database that command-driven allocation depends on. |
| [sym:gwflow_pond] | `unit_in_ponds, unit_pond_name, unit_out_pond_bal, unit_out_pond_sol, unit_out_pond_mass, unit_out_pond_conc` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Imports the module, but the visible source comment notes that some concentration handling was temporarily moved out of the wallo integration path, so the direct module-level role in the shown snippet is uncertain. |
| [sym:gwflow_read] | `unit_*, unit_out_gw, codes.gw, zones.gw, unit_split_fields(2), unit_split_fields(3), unit_split_fields(4), unit_split_fields(5), unit_split_fields(6), cells.gw, unit_split_fields(1), unit_split_fields(7), unit_split_fields(8), unit_split_fields(9), unit_split_fields(10), unit_split_fields(11), unit_split_fields(12), unit_split_fields(13), unit_split_fields(14), unit_split_fields(15), unit_split_fields(16), unit_split_fields(17), unit_split_fields(18), unit_split_fields(19), unit_split_fields(20), unit_split_fields(21), unit_split_fields(22), unit_split_fields(23), cellcon.gw, unit_split_fields(2+j), outputs.gw, gwflow_obs_day.txt, gwflow_obs_mon.txt, gwflow_obs_yr.txt, gwflow_obs_aa.txt, gwflow_chan_obs_flow_day.txt, gwflow_chan_obs_no3_day.txt, gwflow_hru_pump_day.txt, gwflow_hru_pump_mon.txt, gwflow_hru_pump_yr.txt, gwflow_hru_pump_aa.txt, hru_pump.gw, gwflow_cell_wb_ppag_obs_day.txt, pumpex.gw, tile.gw, gwflow_tile_group_day.txt, rescell.gw, floodplain.gw, gwflow_canal.con, gwflow_canal_wb_day.txt, gwflow_canal_sol_day.txt, phreato.gw, phreato_cell.gw, tvheads.gw, solute.gw, cell_sol.gw, minerals.gw, ponds.gw, pond_cell.gw, pond_div.gw, gwflow_pond_wb_day.txt, gwflow_pond_sol_day.txt, gwflow_pond_mass_day.txt, gwflow_pond_conc_day.txt, lsucell.gw, hrucell.gw, transit.gw, gwflow_transit_cell, gwflow_transit_chan, gwflow_transit_tile, sw_group.gw, gwflow_gwsw_group_day.txt, gwflow_chan_hydsep_day.txt` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Reads canal database values from this module while configuring gwflow canal links and seepage properties; the canal array is the shared state source used by gwflow canal setup. |
| [sym:header_water_allocation] | `unit_3110, unit_9000, unit_3114, unit_3111, unit_3115, unit_3112, unit_3116, unit_3113, unit_3117` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Writes the report headers using `wallo_hdr` and `wallo_hdr_units`, which are the shared printable labels owned by this module. |
| [sym:om_osrc_read] | `om_osrc.wal` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Reads outside-source organic/mineral name records into `om_osrc_name`, a shared name table in this module. |
| [sym:om_treat_read] | `om_treat.wal` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Reads treatment-name records into `om_treat_name`, a shared name table in this module. |
| [sym:om_use_read] | `om_use.wal` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Reads water-use-name records into `om_use_name`, a shared name table in this module. |
| [sym:recalldb_read] | `recall_db.rec` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Participates in shared allocation setup state before recall-based transfers are used; the packet does not show direct symbol references from this module in the visible procedure body. |
| [sym:time_control] | `unit_*, unit_9003, unit_5100, unit_5101, unit_8000, unit_8001` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Resets the shared allocation totals at the start of each day by assigning `wallo(:)%tot = walloz` and clearing treated-use outputs. |
| [sym:wallo_allo_output] | `unit_3110, unit_3114, unit_3111, unit_3115, unit_3112, unit_3116, unit_3113, unit_3117` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Traverses the module's allocation object graph and output buffers to print daily, monthly, yearly, and average-annual source-level totals; it uses `walloz` to clear daily outputs after reporting. |
| [sym:wallo_control] | `unit_2612` | `trans_m3, trn_m3, walloz, wallo, wal, wtp` | Uses the allocation database, source/receiver metadata, and output buffers to compute demand, withdraw water, route transfers, and update cumulative accounting. |

## Key Consumers

The module is used by the water-allocation driver, transfer/control routines, treatment/use readers and outputs, canal routing, groundwater canal setup, irrigation constituent/salt accounting, and selected condition and reservoir logic. Most consumers rely on the shared `wallo` hierarchy or the transfer/output buffers; a smaller set uses treatment/use name tables or canal data.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:gwflow_read] | `canal` | `gwflow_read` uses the canal database from this module to classify canals and copy their hydraulic parameters into groundwater canal-link arrays before groundwater canal seepage is simulated. |
| [sym:gwflow_pond] | water_allocation_module | The module is imported into the pond-groundwater exchange workflow, but the visible snippet does not resolve a specific owned symbol beyond the broader shared allocation state; the exact contribution is uncertain from the provided context. |
| [sym:header_water_allocation] | water_allocation_module | Provides the header records `wallo_hdr` and `wallo_hdr_units` that `header_water_allocation` writes into the daily, monthly, yearly, and average-annual report files. |
| [sym:om_osrc_read] | water_allocation_module | Provides the shared `om_osrc_name` array that `om_osrc_read` populates from `om_osrc.wal` so outside-source organic/mineral records have persistent in-memory names. |
| [sym:om_treat_read] | water_allocation_module | Provides the shared `om_treat_name` array that `om_treat_read` fills from `om_treat.wal`, establishing the name table used by treatment records. |
| [sym:om_use_read] | water_allocation_module | Provides the shared `om_use_name` array that `om_use_read` fills from `om_use.wal`, establishing the name table used by water-use records. |
| [sym:wallo_allo_output] | water_allocation_module | Supplies the allocation object tree and output buffers that this routine traverses; it accumulates source totals into `wallom_out`, writes the daily/monthly/yearly/average outputs, and uses `walloz` to clear daily source records after reporting. |
| [sym:wallo_control] | water_allocation_module | Supplies the transfer definitions, source and receiving metadata, and cumulative accounting records that `wallo_control` reads, updates, and writes back during the allocation pass. |
| [sym:wallo_treat_output] | water_allocation_module | Provides the treatment-name table and treatment accounting state used when reporting treated-water totals for each treatment object. |
| [sym:wallo_trn_output] | water_allocation_module | Provides the selected allocation object and its nested transfer/source records so the routine can write source-by-source hydrograph output and reset the daily/monthly/yearly summary holders. |
| [sym:wallo_use_output] | water_allocation_module | Provides the human-readable use-name labels and shared use-accounting state that this routine writes to the water-allocation output files. |
| [sym:water_allocation_read] | water_allocation_module | This reader allocates and fills the `wallo` hierarchy and the `wallod_out`, `wallom_out`, `walloy_out`, and `walloa_out` buffers, establishing the in-memory allocation database that later control and output routines use. |
| [sym:water_canal_read] | water_allocation_module | Provides the `canal` array and `wal` pointer target that the canal reader populates with canal geometry, losses, diversion IDs, and aquifer-loss fractions. |
| [sym:water_orcv_read] | water_allocation_module | Provides the `orcv` array that stores outside-basin receiving-object names and filenames loaded from `outside_rcv.wal`. |
| [sym:water_osrc_read] | water_allocation_module | Provides the `osrc` array and shared allocation state that the outside-source reader populates with outside-basin source metadata and loss parameters. |
| [sym:water_pipe_read] | water_allocation_module | Provides the `pipe` array and shared allocation state that the pipe reader populates with pipe-transfer configuration and aquifer-loss data. |
| [sym:water_tower_read] | water_allocation_module | Provides the `wtow` array and shared allocation state that the tower reader populates with storage, drawdown, and loss parameters. |
| [sym:water_treatment_read] | water_allocation_module | Provides the treatment database arrays that the treatment reader populates and crosswalks so later treatment and allocation logic can use the resolved records. |
| [sym:water_use_read] | water_allocation_module | Provides the `wuse` database and name table that the water-use reader populates and resolves for later use accounting. |
| [sym:recalldb_read] | water_allocation_module | Participates in shared model setup for recall-based transfers; the packet shows the import but does not expose a direct owned symbol in the visible body, so the exact dependency is not fully resolved here. |
| [sym:conditions] | water_allocation_module | Provides water-allocation demand state to the decision-table evaluator so the irrigation-demand-by-water-right condition can compare live allocation demand against the table limit and enable or suppress actions accordingly. |
| [sym:cs_irrig] | water_allocation_module | Supplies the transfer-source list and withdrawn-volume output used to route constituent mass with irrigation water and to choose the correct source-specific mass-storage arrays. |
| [sym:res_hydro] | water_allocation_module | Supplies allocation demand bookkeeping for irrigation-transfer branches; the reservoir release logic can use the allocation object's total demand when release rules depend on water-right or transfer demand. |
| [sym:salt_irrig] | water_allocation_module | Supplies the transfer-source definition and source-level withdrawal output used to route salt mass with irrigation and to update the appropriate source and receiving salt budgets. |

## Lineage

`water_allocation_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 11 non-merge commit(s) since, most recently `b78c4ea` (2026-04-04, "gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portabili…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `water_allocation_module.f90` are listed.

- `b78c4ea` (2026-04-04) — gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portability, dynamic array sizes
- `080211e` (2026-03-09) — water allocation operating properly
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `815ec79` (2026-01-07) — water allocation updates
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `water_allocation_module` has no extracted module-level documentation comment.
- `wal` is a pointer declaration in the source, but the provided context does not show its initialization target inside this module; callers rely on it as shared state.
- The importer list is complete and deterministic from the context packet; the shorter Used By table is a curated subset of concrete consumers.
- No Git commits were resolved for this source span, so lineage analysis is unavailable from the provided evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
