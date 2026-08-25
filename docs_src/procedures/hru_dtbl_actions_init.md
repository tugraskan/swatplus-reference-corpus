---
kind: procedure
symbol: hru_dtbl_actions_init
title: hru_dtbl_actions_init
status: filled
source_hash: 55c28466ad837705
version_label: SWAT+ 62.0.0
locals:
  id: Decision-table identifier for the currently selected management or transfer table. It
    is set from `sched(isched)%num_db(iauto)` for ordinary auto operations, or from `hru(ihru)%man_trn_dtbl`
    when the manure-transfer slot is being initialized.
  iauto: Loop index over the automatic decision-table slots for one HRU. It is used to visit
    each slot in `pcom(ihru)%dtbl` and to detect whether the current slot is the manure-transfer
    auto slot.
  ihru: Actual HRU index being initialized for the current loop iteration. It is derived from
    the spatial object starting offset `sp_ob1%hru` plus the loop counter.
  iihru: Loop counter over the HRUs in the current spatial-object block. It runs from 1 to
    `sp_ob%hru`.
  isched: Management schedule index for the current HRU, taken from `hru(ihru)%mgt_ops`. It
    selects the base automatic-operation database entries in `sched(isched)`.
  num_fut: Temporary counter for how many `fert_future` actions are found in the chosen decision
    table. It is first used to size `pcom(ihru)%fert_fut` and then reused to fill its entries.
  iac: Loop counter over actions inside the selected decision table `dtbl_lum(id)`. It is
    used both to count future fertilizer actions and to copy their fields into `pcom(ihru)%fert_fut`.
  idb: Database index used while crosswalking future fertilizer actions to `fertdb` and `chemapp_db`.
    It identifies the matching fertilizer name or chemical application name.
  m_autos: Total number of automatic decision-table slots for the current HRU. It starts from
    `sched(isched)%num_autos` and is incremented when a manure-transfer decision table is
    present so the extra slot can be allocated and indexed.
uses:
  conditional_module: '`conditional_module` provides `dtbl_lum`, the decision-table array
    whose `acts` count determines allocation sizes and whose action records supply the metadata
    copied into future fertilizer entries. Without it, the routine could not size or inspect
    the land-use/management actions it is organizing.'
  mgt_operations_module: '`mgt_operations_module` provides the management schedule database
    that tells this routine how many base automatic decision-table slots exist for the HRU
    and which database entry each slot points to, plus the chemical-application database used
    to map a future fertilizer action to an application operation name.'
  hydrograph_module: '`hydrograph_module` provides `sp_ob%hru` and `sp_ob1%hru`, which define
    the HRU block being processed and the offset needed to translate the block-local loop
    counter into the global HRU index.'
  hru_module: '`hru_module` holds the HRU management pointers that drive the initialization,
    especially the selected management schedule (`mgt_ops`), the manure-transfer decision
    table pointer (`man_trn_dtbl`), and the slot index written back for manure-transfer auto
    handling (`man_trn_iauto`).'
  plant_module: '`plant_module` provides the per-HRU plant-community structures that receive
    the allocated auto-operation arrays and future fertilizer list. The routine fills `pcom(ihru)%dtbl`
    so later management processing can count daily actions, and fills `pcom(ihru)%fert_fut`
    so later fertilizer scheduling can use the stored operation details.'
  maximum_data_module: '`maximum_data_module` supplies the database-size limits `db_mx%fertparm`
    and `db_mx%chemapp_db`, which bound the loops used to match a future fertilizer action
    against the fertilizer and chemical-application databases.'
  fertilizer_data_module: '`fertilizer_data_module` provides `fertdb`, the fertilizer lookup
    table used to translate a future fertilizer action''s `option` text into the fertilizer
    database index stored in `pcom(ihru)%fert_fut(num_fut)%fertnum`.'
---

<!-- facts:header -->

Initializes per-HRU decision-table action arrays and future fertilizer-operation metadata from the HRU management schedule and land-use decision tables.

## Bottom Line

For each HRU covered by the current spatial object block, `hru_dtbl_actions_init` counts the automatic management decision tables that must be tracked, allocates the per-table counters in `pcom(ihru)%dtbl`, and records which auto slot belongs to manure-transfer demand when `hru(ihru)%man_trn_dtbl` is present.

It also scans the selected decision table actions for `fert_future` entries, builds `pcom(ihru)%fert_fut`, and crosswalks each future fertilizer action to the fertilizer database and chemical-application database so later management code can schedule the correct product and application operation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization after the HRU set and management schedules have been loaded, so the spatial object counts (`sp_ob`, `sp_ob1`) and HRU management pointers (`hru(ihru)%mgt_ops`, `hru(ihru)%man_trn_dtbl`) are already available. It prepares the per-HRU decision-table and future-fertilizer bookkeeping that later management and crop-operation routines depend on when they evaluate automatic actions during the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over the HRUs in the active spatial block. | For each block-local HRU index, compute the global HRU index from `sp_ob1%hru`, read its management schedule from `hru(ihru)%mgt_ops`, and start the auto-slot count from `sched(isched)%num_autos`. |
| 2. Add the manure-transfer slot when configured. | If `hru(ihru)%man_trn_dtbl > 0`, increment the auto-slot count and store the resulting slot index in `hru(ihru)%man_trn_iauto` so the manure-transfer table can be recognized later. |
| 3. Allocate the per-HRU automatic decision-table array. | When at least one automatic slot exists, allocate `pcom(ihru)%dtbl(m_autos)` to hold the per-slot counters for this HRU. |
| 4. Visit each automatic slot and choose its decision-table id. | For each slot, use `sched(isched)%num_db(iauto)` for normal slots, or `hru(ihru)%man_trn_dtbl` when the slot matches `man_trn_iauto`, then keep that decision-table id in `id`. |
| 5. Allocate and initialize action counters for the selected table. | Size `pcom(ihru)%dtbl(iauto)%num_actions` and `days_act` from `dtbl_lum(id)%acts`, initialize the counters, and set the current action count to 1 for the slot. |
| 6. Count future-fertilizer actions in the decision table. | Scan the decision-table actions for `typ == 'fert_future'`, count them in `num_fut`, allocate `pcom(ihru)%fert_fut(num_fut)` when any are found, and save the count in `pcom(ihru)%fert_fut_num`. |
| 7. Copy each future-fertilizer action into plant-community storage. | Rescan the actions, and for each `fert_future` action copy its object number, name, fertilizer name, fertilizer amount, zeroed day field, and application-pointer text into the corresponding `pcom(ihru)%fert_fut` entry. |
| 8. Crosswalk fertilizer name and application type to database indices. | Match the copied fertilizer name against `fertdb` using `db_mx%fertparm` and store the fertilizer index in `fertnum`; match the application pointer against `chemapp_db` using `db_mx%chemapp_db` and store the application index in `appnum`. |
| 9. Finish the loops and return. | After all actions and HRUs are processed, exit the nested loops and return to the caller with the initialized plant-community state in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:conditional_module] | `dtbl_lum` | `dtbl_lum(id)%acts, dtbl_lum(id)%act(iac)%typ, dtbl_lum(id)%act(iac)%ob_num, dtbl_lum(id)%act(iac)%name, dtbl_lum(id)%act(iac)%option, dtbl_lum(id)%act(iac)%const, dtbl_lum(id)%act(iac)%file_pointer` |
| [sym:mgt_operations_module] | `sched, chemapp_db` | `sched(isched)%num_autos, sched(isched)%num_db(iauto), chemapp_db(idb)%name` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1` | `sp_ob%hru, sp_ob1%hru` |
| [sym:hru_module] | `hru` | `hru(ihru)%mgt_ops, hru(ihru)%man_trn_dtbl, hru(ihru)%man_trn_iauto, hru(ihru)%irr_trn_iauto` |
| [sym:plant_module] | `pcom` | `pcom(ihru)%dtbl(m_autos), pcom(ihru)%dtbl(iauto)%num_actions, pcom(ihru)%dtbl(iauto)%days_act, pcom(ihru)%fert_fut(num_fut), pcom(ihru)%fert_fut_num, pcom(ihru)%fert_fut(num_fut)%num, pcom(ihru)%fert_fut(num_fut)%name, pcom(ihru)%fert_fut(num_fut)%fertname, pcom(ihru)%fert_fut(num_fut)%fert_kg, pcom(ihru)%fert_fut(num_fut)%day_fert, pcom(ihru)%fert_fut(num_fut)%fertop, pcom(ihru)%fert_fut(num_fut)%fertnum, pcom(ihru)%fert_fut(num_fut)%appnum` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%fertparm, db_mx%chemapp_db` |
| [sym:fertilizer_data_module] | `fertdb` | `fertdb(idb)%fertnm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(ihru)%man_trn_iauto` | When `hru(ihru)%man_trn_dtbl > 0` for the current HRU. | `hru(ihru)%man_trn_iauto` is set to the newly added auto-slot index so later processing can identify which `pcom(ihru)%dtbl` entry belongs to manure-transfer demand. |
| `pcom(ihru)%dtbl(iauto)%num_actions` | When `m_autos > 0` after counting schedule autos and any manure-transfer slot. | `pcom(ihru)%dtbl` is allocated to hold one `auto_operations` record per automatic decision-table slot for this HRU. |
| `pcom(ihru)%dtbl(iauto)%days_act` | For each auto slot after `id` has been selected and `dtbl_lum(id)%acts` is known. | `pcom(ihru)%dtbl(iauto)%num_actions` is allocated, initialized, and set to 1 so the routine can track how many actions are available in that decision-table slot. |
| `pcom(ihru)%fert_fut_num` | For each auto slot after `id` has been selected and `dtbl_lum(id)%acts` is known. | `pcom(ihru)%dtbl(iauto)%days_act` is allocated and initialized to 0 so the routine can track elapsed days for each action window in that slot. |
| `pcom(ihru)%fert_fut(num_fut)%num` | When the selected decision table contains one or more actions with `typ == 'fert_future'`. | `pcom(ihru)%fert_fut_num` is set to the number of future-fertilizer actions so later routines know how many stored fertilizer operations to expect. |
| `pcom(ihru)%fert_fut(num_fut)%name` | For each `fert_future` action encountered during the second scan of `dtbl_lum(id)%acts`. | `pcom(ihru)%fert_fut(num_fut)%num` stores the source action's object number (`ob_num`) so the future fertilizer operation can be traced back to its decision-table entry. |
| `pcom(ihru)%fert_fut(num_fut)%fertname` | For each `fert_future` action encountered during the second scan of `dtbl_lum(id)%acts`. | `pcom(ihru)%fert_fut(num_fut)%name` stores the action name copied from the decision table for later identification and reporting. |
| `pcom(ihru)%fert_fut(num_fut)%fert_kg` | For each `fert_future` action encountered during the second scan of `dtbl_lum(id)%acts`. | `pcom(ihru)%fert_fut(num_fut)%fertname` stores the fertilizer name text from the decision table so it can be matched against `fertdb`. |
| `pcom(ihru)%fert_fut(num_fut)%day_fert` | For each `fert_future` action encountered during the second scan of `dtbl_lum(id)%acts`. | `pcom(ihru)%fert_fut(num_fut)%fert_kg` stores the fertilizer amount constant from the decision table for later application calculations. |
| `pcom(ihru)%fert_fut(num_fut)%fertop` | For each `fert_future` action encountered during the second scan of `dtbl_lum(id)%acts`. | `pcom(ihru)%fert_fut(num_fut)%day_fert` is initialized to 0 so the later scheduling logic can fill the actual future application day. |
| `pcom(ihru)%fert_fut(num_fut)%fertnum` | For each `fert_future` action encountered during the second scan of `dtbl_lum(id)%acts`. | `pcom(ihru)%fert_fut(num_fut)%fertop` stores the chemical-application operation pointer from the decision table so it can be matched to `chemapp_db`. |
| `pcom(ihru)%fert_fut(num_fut)%appnum` | When the copied fertilizer name matches an entry in `fertdb` during the lookup loop. | `pcom(ihru)%fert_fut(num_fut)%fertnum` is set to the matching fertilizer database index so later code can retrieve fertilizer properties from `fertdb`. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed lineage commits were resolved. The initial addition in `df07e3f` created `hru_dtbl_actions_init` with HRU looping, manure-demand handling, decision-table allocation, and future-fertilizer crosswalk logic. Commit `94b6dec` did not change the routine's behavior beyond preserving that initial implementation in a later imported source snapshot. Commit `39fabde` initialized the local counter variables and added `source = 0` to the `num_actions` and `days_act` allocations. Commit `29e2d36` renamed the manure and irrigation transfer fields from the earlier demand names to `man_trn_*` and `irr_trn_*`, and updated the slot-selection tests accordingly. Commit `080211e` then removed the irrigation-transfer branch from this routine and commented out the irrigation decision-table selection, leaving only the manure-transfer special handling.

- `df07e3f` introduced the routine and its core initialization flow: HRU iteration, auto-slot counting, decision-table allocation, and future-fertilizer metadata extraction.
- `39fabde` changed initialization behavior by zeroing local counters and using `source = 0` during allocation of `pcom(ihru)%dtbl(iauto)%num_actions` and `days_act`.
- `29e2d36` changed the special-slot logic from the earlier `*_dmd_*` names to the current `man_trn_*` and `irr_trn_*` names, including the slot tests and decision-table selection.
- `080211e` removed the irrigation-transfer slot handling from this routine, so only manure-transfer demand remains as the special-case auto slot in the current source.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_dtbl_actions_init' has no extracted documentation comment.
- algorithm_steps revised: merged the loop/setup logic into nine source-backed steps and expanded the fertilizer crosswalk path for clarity.
- Source snapshot shows irrigation-transfer handling commented out in the current file, while lineage evidence confirms it existed in earlier revisions.
