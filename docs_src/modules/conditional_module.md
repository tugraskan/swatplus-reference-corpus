---
kind: module
symbol: conditional_module
title: conditional_module
status: filled
source_hash: 7ef6aaee066c8595
version_label: SWAT+ 62.0.0
variables:
  dtbl_lum: Loaded land-use and management decision tables. `dtbl_lum_read` allocates and
    fills this array from `lum.dtl`, including conditions, alternatives, actions, hit flags,
    and crosswalk pointers; other routines such as `proc_cond`, `hru_control`, `hru_dtbl_actions_init`,
    `mallo_control`, `manure_allocation_read`, and `hru_lte_read` use it as the management
    rule catalog.
  dtbl_res: Loaded reservoir release decision tables. `dtbl_res_read` allocates and fills
    this array from `res_rel.dtl`, and reservoir and calibration routines such as `res_control`,
    `res_read`, `wetland_control`, `cal_conditions`, and `cal_parm_select` use it when reservoir
    behavior is driven by conditional release rules.
  dtbl_scen: Loaded scenario or landuse-update decision tables. `dtbl_scen_read` allocates
    and fills this array from `scen_lu.dtl`, and `cal_cond_read` and `time_control` use it
    to resolve conditional-update table names into numeric table indices.
  dtbl_flo: Loaded flow-control decision tables. `dtbl_flocon_read` allocates and fills this
    array from `flo_con.dtl`, and routines such as `hru_control`, `sat_buff_read`, `wallo_demand`,
    and `water_allocation_read` use it to resolve flow-control table names into indices.
  d_tbl: Active decision-table pointer used during condition evaluation and action execution.
    It is associated by caller routines such as `hru_control`, `mallo_control`, `res_control`,
    `wetland_control`, `wallo_demand`, `hru_lte_control`, `cond_integer`, `cond_real`, and
    `conditions` before they evaluate or execute a specific table.
type_components:
  conditions_var:
    var: condition variable (ie volume, flow, sw, time, etc)
    ob: object variable (ie res, hru, canal, etc)
    ob_num: object number
    lim_var: limit variable (ie evol, pvol, fc, ul, etc)
    lim_op: limit operator (*,+,-)
    lim_const: limit constant
  actions_var:
    typ: type of action (ie reservoir release, irrigate, fertilize, etc)
    ob: object variable (ie res, hru, canal, etc)
    ob_num: object number
    name: name of action
    option: action option - specific to type of action (ie for reservoir, option to
    const: 'input rate, days of drawdown, weir equation pointer, etc

      constant used for rate, days, etc'
    const2: additional constant used for rate, days, etc
    file_pointer: pointer for option (ie weir equation pointer)
  decision_table:
    name: name of the decision table
    conds: number of conditions
    alts: number of alternatives
    acts: number of actions
    cond: conditions
    alt: condition alternatives
    act: actions
    lu_chg_mx: max times lu change can occur
    snow_chg_mx: max times snow change can occur
    act_outcomes: action outcomes ("y" to perform action; "n" to not perform)
    act_hit: '"y" if all condition alternatives (rules) are met; "n" if not'
    act_typ: pointer to action type (ie plant, fert type, tillage implement, release type,
      etc)
    act_app: pointer to operation or application type (ie harvest.ops, chem_app.ops, wier
      shape, etc)
    con_act: pointer for days since last action condition to point to appropriate action
    hru_lu: number of hru's in the land_use condition(s) - used for probabilistic mgt operations
      or lu change
    ha_lu: area of land_use in ha
    hru_lu_cur: number of hru's in the land_use condition(s) that have currently been applied
    hru_ha_cur: area of land_use in ha that has currently been applied
    days_prob: days since start of application window
    day_prev: to check if same day - don't increment day in application window
    prob_cum: cumulative probability of application on current day of window
    frac_app: fraction of time (during each window) the application occurs
type_summaries:
  conditions_var: One rule row used to describe a single conditional limit on a model state
    variable for a specific object.
  actions_var: One action record describing what management or release operation to perform
    when a decision-table alternative is satisfied.
  decision_table: One complete conditional rule set with conditions, alternatives, actions,
    and bookkeeping for probabilistic or one-time management execution.
---

<!-- facts:header -->

`conditional_module` owns the shared decision-table data model for SWAT+ conditional management. It defines the record types used to express condition checks, action definitions, and complete decision tables, and it exposes the loaded decision-table arrays (`dtbl_lum`, `dtbl_res`, `dtbl_scen`, `dtbl_flo`) plus the active table pointer `d_tbl`. Reader routines populate those arrays from decision-table input files, and later management, calibration, reservoir, HRU, wetland, and allocation routines use them to evaluate conditions and execute actions.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is primarily a declaration container. It defines the shared decision-table types and allocatable table arrays, but it does not contain startup procedures of its own; the arrays are populated by external reader/setup routines such as `dtbl_lum_read`, `dtbl_res_read`, `dtbl_scen_read`, and `dtbl_flocon_read`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:dtbl_lum_read] | `lum.dtl` | `dtbl_lum` | Allocates and fills the land-use decision-table catalog from the input file, including condition rows, alternatives, actions, action outcomes, and crosswalk fields. |
| [sym:dtbl_res_read] | `res_rel.dtl` | `dtbl_res` | Allocates and fills the reservoir decision-table catalog from the input file, including condition rows, alternatives, actions, action outcomes, and action pointer lookups. |
| [sym:dtbl_scen_read] | `scen_lu.dtl` | `dtbl_scen` | Allocates and fills the scenario decision-table catalog from the input file, including condition rows, alternatives, actions, action outcomes, and resolved action indices. |
| [sym:dtbl_flocon_read] | `flo_con.dtl` | `dtbl_flo` | Allocates and fills the flow-control decision-table catalog from the input file, including condition rows, alternatives, actions, action outcomes, and resolved action indices. |
| [sym:cal_cond_read] | `scen_dtl.upd` | `dtbl_scen` | Reads conditional-update entries and crosswalks each entry's decision-table name against `dtbl_scen(icond)%name` to resolve the scenario table index used by later calibration update logic. |
| [sym:cal_allo_init] | `baseline model state` | `dtbl_lum` | Uses the already loaded land-use decision tables to size per-HRU auto-management work arrays during calibration initialization. |
| [sym:cal_parm_select] | `calibration selection inputs` | `dtbl_res` | Uses reservoir decision tables as mutable calibration targets for release-related parameters such as drawdown days and withdraw rate. |
| [sym:calsoft_read_codes] | `codes.sft` | `none` | No direct conditional-module symbols are referenced in the extracted body, so this import is part of the shared calibration startup environment rather than a confirmed reader of module state. |
| [sym:caltsoft_hyd] | `unit_4304` | `none` | The imported module is present in the setup environment, but the extracted evidence does not show a direct read or write of conditional-module state. |
| [sym:actions] | `unit_2612, unit_3612` | `d_tbl` | Consumes the active decision table and executes the matching action records for the alternatives whose condition hits remain valid. |
| [sym:hru_control] | `unit_100100` | `d_tbl, dtbl_lum, dtbl_flo` | Selects the active land-use or flow-control decision table, evaluates its conditions, and runs the corresponding actions during HRU management and saturated-buffer processing. |
| [sym:mallo_control] | `manure allocation state` | `d_tbl, dtbl_lum` | Selects the manure-demand decision table for the current demand object, evaluates conditions, and executes the resulting management action. |

## Key Consumers

The main consumers are the rule-evaluation routines that test conditions and dispatch actions, plus the file readers and crosswalk/setup routines that load and index decision tables. Most downstream use falls into management control, reservoir and wetland release control, calibration/update readers, and allocation crosswalks.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_allo_init] | conditional_module | Loads the baseline management environment needed for calibration, then sizes each HRU's auto-management work arrays from the already loaded land-use decision tables so later calibration logic can reuse a stable starting state. |
| [sym:cal_cond_read] | conditional_module | Uses the scenario decision-table catalog to crosswalk each update entry's named table to a numeric `cond_num`, linking the update file to the in-memory table registry. |
| [sym:cal_parm_select] | conditional_module | Uses the reservoir decision-table array as a calibration target when adjusting release-related parameters, so the table contents stay synchronized with calibration edits. |
| [sym:dtbl_flocon_read] | conditional_module | Builds the `dtbl_flo` decision-table database in memory from `flo_con.dtl`, creating the table array that later flow-control routines evaluate. |
| [sym:dtbl_lum_read] | conditional_module | Builds the `dtbl_lum` decision-table database in memory from `lum.dtl`, including the land-use condition, action, and crosswalk fields that later management code executes. |
| [sym:dtbl_res_read] | conditional_module | Builds the `dtbl_res` reservoir decision-table database in memory from `res_rel.dtl`, preparing the release rules used by later reservoir routing logic. |
| [sym:dtbl_scen_read] | conditional_module | Builds the `dtbl_scen` scenario decision-table database in memory from `scen_lu.dtl`, preparing the land-use and scenario rules used by later table lookups. |
| [sym:hru_dtbl_actions_init] | conditional_module | Uses `dtbl_lum` to size per-HRU action bookkeeping and to copy future-fertilizer action metadata into the HRU's future-operation arrays. |
| [sym:hru_lte_control] | conditional_module | Switches `d_tbl` to the active HRU LTE start and end decision tables, then evaluates those tables to trigger growth-start and growth-end actions for the selected HRU. |
| [sym:hru_lte_read] | conditional_module | Crosswalks HRU LTE growing-season markers to the names stored in `dtbl_lum`, converting text table references into start and end table indices for later control. |
| [sym:mallo_control] | conditional_module | Associates `d_tbl` with the active land-use decision table for a manure demand object, then evaluates that table and executes the selected manure-management actions. |
| [sym:manure_allocation_read] | conditional_module | Uses `dtbl_lum` as the table registry for manure-transfer demand records, matching named demand tables to numeric indices and resolving the linked application option. |
| [sym:res_control] | conditional_module | Associates `d_tbl` with the selected reservoir release decision table before release evaluation so reservoir outflow can follow the loaded rule set. |
| [sym:res_hydro] | conditional_module | Evaluates the active reservoir decision table, checks which alternatives still hit, and uses those action records to compute the release volume for the current time step. |
| [sym:res_read] | conditional_module | Uses `dtbl_res` as the registry for reservoir release definitions and resolves named release tables into numeric indices during reservoir input loading. |
| [sym:sat_buff_read] | conditional_module | Uses `dtbl_flo` to convert each saturated-buffer flow-control table name into the numeric table index stored on the source HRU. |
| [sym:time_control] | conditional_module | Uses the scenario decision-table catalog while processing timed updates so calendar-driven update logic can evaluate the correct conditional table entries. |
| [sym:wallo_demand] | conditional_module | Selects the relevant flow-control or land-use decision table, evaluates its conditions, and runs the corresponding demand-side actions before computing the water-transfer demand. |
| [sym:water_allocation_read] | conditional_module | Uses both `dtbl_lum` and `dtbl_flo` to resolve water-allocation table names into numeric indices and irrigation-operation references during allocation file loading. |
| [sym:wet_initial] | conditional_module | Uses `dtbl_res` to resolve the wetland release rule name into the numeric reservoir-style decision table index used by later wetland release logic. |
| [sym:wetland_control] | conditional_module | Associates `d_tbl` with the wetland release decision table and evaluates it so paddy or wetland releases follow the loaded conditional rules. |
| [sym:cal_conditions] | conditional_module | Compares reservoir-type names against `dtbl_res(ielem)%name` while applying conditional calibration updates, so the module's reservoir table registry is part of the calibration condition check. |
| [sym:cond_integer] | conditional_module | Reads the active decision table from `d_tbl`, scans each alternative, and disables alternatives whose integer comparison fails. |
| [sym:cond_real] | conditional_module | Reads the active decision table from `d_tbl`, scans each alternative, and disables alternatives whose real-valued comparison fails. |
| [sym:conditions] | conditional_module | Evaluates the active decision table in `d_tbl`, resets hit flags, tests each condition row, and updates the bookkeeping fields that govern probabilistic or one-time management actions. |
| [sym:proc_cond] | conditional_module | Crosswalks automatic management names against `dtbl_lum` so each auto operation stores the correct decision-table index for later execution. |
| [sym:res_control] | conditional_module | Associates `d_tbl` with the reservoir release table selected for the current reservoir, then passes that table to the release-condition logic. |

## Lineage

`conditional_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `57f3eea` (2026-03-02, "Snow change (#149)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `conditional_module.f90` are listed.

- `57f3eea` (2026-03-02) — Snow change (#149)
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `e08326e` (2024-11-08) — Simplify conditions and update variable assignments
- `568154c` (2024-10-08) — Increase length of various character variables
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `conditional_module` has no extracted module-level documentation comment.
- No commits were resolved for the requested source span in the lineage evidence.
- Reader/setup coverage is representative rather than exhaustive; the packet shows 12 candidate reader entries while the importer inventory lists many more consumers.
- The module is a shared declaration-and-state container; it does not contain contained procedures in the extracted source.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
