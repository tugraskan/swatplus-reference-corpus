---
kind: procedure
symbol: proc_cond
title: proc_cond
status: filled
source_hash: 8c6777e6c28563fe
version_label: SWAT+ 62.0.0
locals:
  isched: Holds the management-schedule index taken from hru(ihru)%mgt_ops for the current
    HRU, so the routine can update the correct sched(isched) record.
  iauto: Loops over each automatic operation defined on the current management schedule and
    identifies which auto entry is being matched to a decision table.
  ictl: Loops over the available conditional land-use decision tables in dtbl_lum so the routine
    can find the table whose name matches the auto operation name.
uses:
  hru_module: The HRU module provides each HRU's management schedule pointer through hru(ihru)%mgt_ops.
    That link is what tells proc_cond which sched entry belongs to the current HRU.
  mgt_operations_module: The management-operations module holds the schedule records that
    proc_cond updates. It reads num_autos to decide whether auto operations exist, sets irr
    to flag the schedule, compares auto_name against decision-table names, and writes the
    matched table index into num_db.
  hydrograph_module: The hydrograph module provides sp_ob%hru, the number of HRUs to scan.
    Without that count, proc_cond would not know how many HRU schedule records to process.
  maximum_data_module: The maximum-data module provides db_mx%dtbl_lum, the upper bound for
    conditional land-use decision tables. proc_cond uses it as the loop limit when searching
    for a matching dtbl_lum entry.
  conditional_module: The conditional module owns dtbl_lum, the decision-table array whose
    name field is compared against each auto operation name. That is the target structure
    proc_cond cross-references into sched(isched)%num_db.
---

<!-- facts:header -->

Builds the crosswalk from HRU management schedules to conditional decision tables. It flags schedules that use automatic operations and stores each auto operation's matching decision-table index.

## Bottom Line

proc_cond scans every HRU, looks up that HRU's management schedule, and if the schedule has automatic operations it marks the schedule as irrigation-enabled and links each automatic operation name to the matching conditional decision table index. That crosswalk lets later management code find the right conditional table without searching by name again.

The routine does not take arguments or perform file I/O; it works entirely from shared model state in the HRU, schedule, maximum-data, and conditional-table modules. Its output is the populated schedule metadata that other management logic can use when evaluating automatic operations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

proc_cond runs after HRU and management-schedule data have been loaded so that hru(ihru)%mgt_ops, sched(isched)%num_autos, and dtbl_lum are already available. It prepares the schedule crosswalk used by later automatic management and conditional-operation behavior, so downstream code can resolve auto operation names to decision-table records efficiently.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop HRUs | Iterate over every HRU, fetch its management-schedule index from hru(ihru)%mgt_ops, and use that index to work on the corresponding schedule record. |
| 2. test autos | Only continue for schedules that define at least one automatic operation; for those schedules, set sched(isched)%irr to 1 to flag the schedule as having automatic irrigation/conditional management content. |
| 3. loop autos | Walk through each automatic operation name stored on the schedule so it can be matched to a conditional decision table. |
| 4. scan tables | Search all conditional land-use decision tables and compare each sched(isched)%auto_name(iauto) to dtbl_lum(ictl)%name. |
| 5. record match | When a table name matches an auto-operation name, save the matching table index in sched(isched)%num_db(iauto). |
| 6. finish loops | Close the nested loops after all automatic operations for all HRUs have been processed. |
| 7. return | Exit the subroutine after the crosswalk has been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, ihru` | `hru(ihru)%mgt_ops` |
| [sym:mgt_operations_module] | `sched` | `sched(isched)%num_autos, sched(isched)%irr, sched(isched)%auto_name(iauto), sched(isched)%num_db(iauto)` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dtbl_lum` |
| [sym:conditional_module] | `dtbl_lum` | `dtbl_lum(ictl)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sched(isched)%irr` | When sched(isched)%num_autos > 0 for the current HRU's schedule. | The routine sets sched(isched)%irr = 1 to mark that this schedule contains automatic operations, specifically in the crosswalk setup for conditional/irrigation-style management behavior. |
| `sched(isched)%num_db(iauto)` | When sched(isched)%auto_name(iauto) matches dtbl_lum(ictl)%name inside the nested search over decision tables. | The routine writes the matched decision-table index into sched(isched)%num_db(iauto) so the auto operation can be resolved directly to its conditional table later. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved for proc_cond. The initial addition in df07e3f introduced the full subroutine and its HRU-to-decision-table crosswalk logic. Commit 39fabde did not change behavior; it only initialized isched, iauto, and ictl to 0 and adjusted indentation/return formatting.

- df07e3f added proc_cond as a new subroutine that scans HRUs, flags schedules with automatic operations, and maps each auto_name to a dtbl_lum index through sched(isched)%num_db.
- 39fabde made no algorithmic change in proc_cond; it only initialized the local counters isched, iauto, and ictl and normalized the return statement formatting.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'proc_cond' has no extracted documentation comment.
