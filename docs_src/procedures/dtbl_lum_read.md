---
kind: procedure
symbol: dtbl_lum_read
title: dtbl_lum_read
status: filled
source_hash: bd07d5a70e951ef6
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from the top of the decision-table file before the table
    count is parsed.
  header: Scratch header string used to consume section labels or divider lines inside `lum.dtl`
    before reading the next block of records.
  eof: I/O status flag from each read; negative values signal end-of-file and stop parsing
    early.
  i: Loop counter for the decision-table records being loaded from `lum.dtl`.
  mdtbl: Number of land-use decision tables declared in the file and used to size `dtbl_lum`.
  ic: Counter for conditions within one decision table, including the pass that maps conditions
    to actions.
  ial: Counter for alternatives within a condition; also used to read the alternative labels
    and action outcomes.
  iac: Counter for actions within one decision table.
  i_exist: Logical file-existence flag from `inquire`; determines whether the routine should
    try to read the file or leave `dtbl_lum` empty.
  idb: Generic database index used while crosswalking file pointers or options to land-use,
    operation, fertilizer, pesticide, tillage, or snow database entries.
  iburn: Index used specifically when crosswalking burn actions to `fire_db`.
  ihru: Index used when counting HRUs that match a land-use condition and accumulating their
    area.
uses:
  maximum_data_module: '`maximum_data_module` provides the maximum record counts that bound
    the crosswalk loops and hold the final count of loaded land-use decision tables. Those
    limits are required to size the `dtbl_lum` array and to iterate safely over each external
    database referenced by an action.'
  reservoir_data_module: '`reservoir_data_module` was requested as an input dependency by
    the source, but the extracted line-based evidence in this packet does not show any resolved
    references from that module inside `dtbl_lum_read`. The module appears to be an unused
    carryover import here, so it has no evidenced effect on the routine beyond compilation
    context.'
  landuse_data_module: '`landuse_data_module` supplies the land-use management database whose
    names are matched against `file_pointer` values for `lu_change` actions. That crosswalk
    lets the routine convert a textual land-use target into the integer database index stored
    in `dtbl_lum(i)%act_typ(iac)`.'
  mgt_operations_module: '`mgt_operations_module` provides the operation databases that decision-table
    actions point to by name. The routine uses those name fields to translate action text
    into integer references for harvest, irrigation, chemical application, grazing, puddling,
    and fire operations.'
  tillage_data_module: '`tillage_data_module` matters because tillage actions are crosswalked
    by matching the action option string against `tilldb(idb)%tillnm`, allowing the routine
    to store the correct tillage-implementation index in `dtbl_lum(i)%act_typ(iac)`.'
  fertilizer_data_module: '`fertilizer_data_module` matters because fertilize-type actions
    store the fertilizer selected by name. The routine compares the action option string with
    `fertdb(idb)%fertnm` to resolve the fertilizer database index used later by management
    execution.'
  input_file_module: '`input_file_module` supplies `in_cond%dtbl_lum`, the configured path
    to the decision-table file. The routine depends on that path to decide whether the file
    exists and which file unit to open for reading.'
  conditional_module: '`conditional_module` defines the `decision_table` structure that this
    routine fills. Its fields hold the parsed names, condition records, alternatives, actions,
    action outcomes, and crosswalk pointers, so the module is the in-memory destination for
    everything read from `lum.dtl`.'
  pesticide_data_module: '`pesticide_data_module` is imported by the source, but the visible
    routine body in this packet crosswalks pesticide actions through `cs_db%num_pests` and
    `cs_db%pests(idb)` from `constituent_mass_module` rather than through any resolved pesticide-database
    symbols. The import therefore appears unused in the extracted evidence, though it may
    exist for broader source compatibility.'
  plant_data_module: '`plant_data_module` provides the transplant database whose names are
    matched for `plant` actions. The routine stores the matching transplant index in `dtbl_lum(i)%act_app(iac)`
    so later plant operations can look up the correct transplant parameters.'
  constituent_mass_module: '`constituent_mass_module` provides the list of pesticide constituent
    names that `pest_apply` actions are matched against. That lets the routine translate a
    pesticide name into the corresponding integer index stored in `dtbl_lum(i)%act_typ(iac)`.'
  hydrograph_module: '`hydrograph_module` supplies `sp_ob%hru`, the number of HRUs to scan
    when a condition depends on land use. The routine uses that count to tally matching HRUs
    and accumulate their area for probabilistic land-use or management application logic.'
  hru_module: '`hru_module` provides both the HRU table and the snow-parameter table used
    by this routine. HRU names and areas are needed to count and total land-use matches, and
    snow names are needed to resolve `snow_change` action pointers to the correct snow-database
    entry.'
---

<!-- facts:header -->

Reads the land-use management decision table file and loads decision tables, conditions, alternatives, actions, and crosswalk pointers into memory. It also derives land-use HRU counts/areas for probabilistic management logic and maps action names to the supporting operation databases.

## Bottom Line

`dtbl_lum_read` opens the conditional-management file named by `in_cond%dtbl_lum` (normally `lum.dtl`), scans the file for the number of decision tables, and allocates `dtbl_lum` accordingly. For each table it reads the table header, condition block, action block, and outcome flags, then converts text pointers into integer indexes against the land-use, management-op, fertilizer, pesticide, snow, and related databases.

The routine matters because later land-use management logic depends on these crosswalked decision tables rather than raw file text. It also precomputes land-use participation counts and areas for `land_use` conditions, which are used when the model applies probabilistic operations or land-use changes.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model input initialization after the conditional input path has been set in `in_cond%dtbl_lum`. It is an upstream data-loading step: it prepares the land-use decision tables that later management and conditional-action routines use to decide when to apply planting, harvesting, irrigation, fertilizer, pesticide, grazing, puddling, burn, land-use-change, and snow-change actions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the decision-table file is available | The routine queries `in_cond%dtbl_lum` with `inquire` and, if the file is missing or the configured name is `null`, allocates an empty `dtbl_lum(0:0)` array instead of attempting to parse records. |
| 2. Open and read the file title and table count | When the file exists, the routine opens unit 107 on the configured file path, reads the title line and the number of decision tables, discards the following separator line, and allocates `dtbl_lum(1:mdtbl)`. |
| 3. Loop over each decision table block | For each table, the routine reads a section header, then reads the table name and its condition, alternative, and action counts. It allocates the condition, alternative, action, and outcome arrays plus the land-use-change and snow-change limit arrays for that table. |
| 4. Read condition records and alternative labels | The routine reads the condition-section header, then loads each condition and its alternative labels from the file. If a condition variable is `prob_unif`, it backspaces and rereads that line to capture `frac_app` with the condition variable. |
| 5. Compute land-use population and area for land-use conditions | The routine initializes `hru_lu` and `ha_lu` to zero, then for any condition whose variable is `land_use`, it scans all HRUs and counts those whose `land_use_mgt_c` matches the condition limit value while summing their `area_ha`. |
| 6. Read action records and normalize `const2` | The routine reads the action-section header, then loads each action definition and its alternative outcomes. After reading each action, it enforces a minimum `const2` value of 1 by applying `Max(1., dtbl_lum(i)%act(iac)%const2)`. |
| 7. Crosswalk plant and harvest-style actions | The routine dispatches on `act(iac)%typ` and maps `plant`, `harvest`, and `harvest_kill` actions to database indexes by comparing `file_pointer` against `transpl(idb)%name` or `harvop_db(idb)%name`. It stores the resolved index in `act_app` for planting or `act_typ` for harvest actions. |
| 8. Crosswalk tillage and irrigation actions | For `till`, `irr_demand`, `irr_wallo`, and `irrigate`, the routine matches the action fields to the tillage or irrigation database names and stores the resulting operation index in `act_typ`. |
| 9. Crosswalk fertilizer and manure-demand actions | For `fertilize` and `fert_future`, the routine matches the fertilizer option to `fertdb(idb)%fertnm` and the chemical-application pointer to `chemapp_db(idb)%name`, storing the resolved indexes in `act_typ` and `act_app`. For `manure_demand`, it crosswalks the application pointer against `chemapp_db(idb)%name` and stores that application index. |
| 10. Crosswalk pesticide actions | For `pest_apply`, the routine matches the pesticide option string against `cs_db%pests(idb)` and stores the resulting constituent index in `act_typ`, then crosswalks the application pointer against `chemapp_db(idb)%name` and stores the chemical-application index in `act_app`. |
| 11. Crosswalk grazing and puddling actions | For `graze`, the routine matches the grazing option against `grazeop_db(idb)%name` and stores the grazing-operation index in `act_typ`. For `puddle`, it matches the option against `pudl_db(idb)%name` and stores the puddling-operation index in `act_typ`. |
| 12. Crosswalk burn, land-use change, and snow-change actions | For `burn`, `lu_change`, and `snow_change`, the routine matches the action option or file pointer against `fire_db(iburn)%name`, `lum(idb)%name`, or `snodb(idb)%name` and stores the resulting index in `act_typ`. |
| 13. Link conditions to their controlling actions | The routine scans each condition after actions are loaded and, when a condition limit variable matches an action name, stores that action index in `con_act(ic)` so later logic can find the action associated with a days-since-last-action condition. |
| 14. Save the table count and finish | After all tables are read, the routine stores the loaded count in `db_mx%dtbl_lum`, exits the file-reading loop, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%transplant, db_mx%harvop_db, db_mx%tillparm, db_mx%irrop_db, db_mx%fertparm, db_mx%chemapp_db, db_mx%grazeop_db, db_mx%pudl_db, db_mx%fireop_db, db_mx%landuse, db_mx%sno, db_mx%dtbl_lum` |
| [sym:reservoir_data_module] | `sp_ob` | `sp_ob%hru` |
| [sym:landuse_data_module] | `lum` | `lum(idb)%name` |
| [sym:mgt_operations_module] | `harvop_db, irrop_db, chemapp_db, grazeop_db, pudl_db, fire_db, graze` | `harvop_db(idb)%name, irrop_db(idb)%name, chemapp_db(idb)%name, grazeop_db(idb)%name, pudl_db(idb)%name, fire_db(iburn)%name` |
| [sym:tillage_data_module] | `tilldb` | `tilldb(idb)%tillnm` |
| [sym:fertilizer_data_module] | `fertdb` | `fertdb(idb)%fertnm` |
| [sym:input_file_module] | `in_cond` | `in_cond%dtbl_lum` |
| [sym:conditional_module] | `dtbl_lum` | `dtbl_lum(i)%name, dtbl_lum(i)%conds, dtbl_lum(i)%alts, dtbl_lum(i)%acts, dtbl_lum(i)%cond(ic), dtbl_lum(i)%alt(ic,ial), dtbl_lum(i)%cond(ic)%var, dtbl_lum(i)%frac_app, dtbl_lum(i)%hru_lu, dtbl_lum(i)%ha_lu, dtbl_lum(i)%cond(ic)%lim_var, dtbl_lum(i)%act(iac), dtbl_lum(i)%act_outcomes(iac,ial), dtbl_lum(i)%act(iac)%const2, dtbl_lum(i)%act(iac)%typ, dtbl_lum(i)%act(iac)%file_pointer, dtbl_lum(i)%act_app(iac), dtbl_lum(i)%act_typ(iac), dtbl_lum(i)%act(iac)%option, dtbl_lum(i)%act(iac)%name, dtbl_lum(i)%con_act(ic)` |
| [sym:pesticide_data_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(idb)` |
| [sym:plant_data_module] | `transpl` | `transpl(idb)%name` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(idb)` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:hru_module] | `hru, snodb` | `hru(ihru)%land_use_mgt_c, hru(ihru)%area_ha, snodb(idb)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `dtbl_lum(i)%hru_lu` | When a condition variable equals `land_use` during the land-use condition scan. | The routine counts how many HRUs match the condition's land-use management code and stores that count in `dtbl_lum(i)%hru_lu` so later probabilistic management or land-use change logic knows how many HRUs are eligible. |
| `dtbl_lum(i)%ha_lu` | When a condition variable equals `land_use` during the land-use condition scan. | The routine sums the areas of matching HRUs and stores the total in `dtbl_lum(i)%ha_lu` so later logic can work with the affected land-use area in hectares. |
| `dtbl_lum(i)%act(iac)%const2` | Whenever an action record is read from `lum.dtl`, before crosswalking starts. | The routine forces `dtbl_lum(i)%act(iac)%const2` to be at least 1, preventing zero or negative secondary constants from propagating into later action calculations. |
| `dtbl_lum(i)%act_app(iac)` | When an action type maps its application pointer to a database record, such as `plant`, `fertilize`, `fert_future`, `manure_demand`, `pest_apply`, or the action branches that use operation/application lookups. | The routine stores the matched application or operation database index in `dtbl_lum(i)%act_app(iac)` so later management code can retrieve the referenced operation record by integer index instead of by text. |
| `dtbl_lum(i)%act_typ(iac)` | When an action type maps its option string to a database record, such as `harvest`, `harvest_kill`, `till`, `irr_demand`, `irr_wallo`, `irrigate`, `fertilize`, `fert_future`, `pest_apply`, `graze`, `puddle`, `burn`, `lu_change`, or `snow_change`. | The routine stores the resolved database index in `dtbl_lum(i)%act_typ(iac)` so later model code can execute the correct operation or retrieve the correct parameter set. |
| `dtbl_lum(i)%con_act(ic)` | When a condition's `lim_var` matches an action's `name` during the condition-action crosswalk pass. | The routine records which action controls the given condition in `dtbl_lum(i)%con_act(ic)`, allowing later logic to associate 'days since last action' style conditions with the relevant action entry. |
| `db_mx%dtbl_lum` | After all decision tables have been read successfully and before the routine closes the file. | The routine stores the number of loaded land-use decision tables in `db_mx%dtbl_lum`, which downstream allocation and validation logic uses as the maximum available table count. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior changes after the initial addition of `dtbl_lum_read`: 39fabde initialized several local scalars and changed some allocations to use zero sources; 080211e added the `irr_wallo` action branch; and 57f3eea expanded the routine to allocate land-use/snow change counters and added `lu_change` and `snow_change` crosswalks. The original routine was introduced in df07e3f as a full file reader for land-use decision tables.

- 39fabde: initialized `titldum`, `header`, `eof`, `i`, `mdtbl`, `ic`, `ial`, `iac`, `idb`, `iburn`, and `ihru`; also changed `con_act`, `act_typ`, and `act_app` allocations to initialize to zero.
- 080211e: added the `irr_wallo` case so irrigation actions can resolve to `irrop_db` entries by name.
- 57f3eea: added `lu_chg_mx` and `snow_chg_mx` allocations and new `lu_change`/`snow_change` crosswalk branches that map to `lum` and `snodb` entries.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dtbl_lum_read' has no extracted documentation comment.
- reservoir_data_module and pesticide_data_module are imported in the source, but no resolved symbol usage from those modules appears in the extracted line-level evidence for this routine.
