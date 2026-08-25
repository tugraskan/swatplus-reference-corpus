---
kind: procedure
symbol: mgt_operatn
title: mgt_operatn
status: filled
source_hash: 66c26b06ca59f5b9
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index copied from `ihru` so the routine can access HRU-specific schedule
    and plant state.
  aphu: Current accumulated heat-unit fraction used to compare against management thresholds.
  isched: Management schedule index for the active HRU, taken from `hru(j)%mgt_ops`.
uses:
  mgt_operations_module: Provides the active management schedule and the current management
    operation record that this routine tests and advances.
  hru_module: Supplies the current HRU index, the HRU's management schedule pointer, the skip-year
    flag, and the plant heat-unit base used when no crop is growing.
  plant_module: Provides the current plant growth status and accumulated heat units used to
    decide whether a heat-unit-based management operation should fire.
  time_module: Provides the current month and day-of-month used to match scheduled management
    dates.
---

<!-- facts:header -->

Runs HRU management operations for the current day and plant state.

## Bottom Line

`mgt_operatn` is the HRU-level management dispatcher. It selects the active management schedule for the current HRU, checks whether the current date matches a scheduled operation, and advances through management actions by repeatedly calling `mgt_sched`.

It matters because it is the gatekeeper for plant and land-management events during HRU processing. The routine uses current time, HRU schedule selection, plant growth status, and heat-unit accumulation to decide when to execute or skip management operations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from `hru_control` after evapotranspiration is computed and before surface runoff processes begin. `hru_control` skips this routine when `yr_skip(j) /= 0`, so `mgt_operatn` runs only for HRUs that are not in a skipped year.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load HRU schedule | Copy the current HRU index, select its management schedule, and load the current management record from that schedule. |
| 2. Match calendar date | While the management record month and day match the current simulation date, call `mgt_sched` to advance through same-day operations. Stop early if the schedule has only one operation left or the HRU is marked to skip the year. |
| 3. Choose plant index | Set the plant index from the management record and choose the active heat-unit fraction from either the bare-soil base or the current plant's accumulated heat units. |
| 4. Advance by heat units | While the management threshold is positive and the accumulated heat units exceed it, advance the schedule, refresh the plant index and heat-unit fraction, optionally advance again for a `skip` operation, and stop if the HRU is flagged to skip the year. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `sched, mgt` | `sched(isched)%num_ops, mgt%mon, mgt%day, mgt%op2, mgt%husc, mgt%op` |
| [sym:hru_module] | `hru, yr_skip, phubase, ihru, ipl` | `hru(j)%mgt_ops` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%phuacc` |
| [sym:time_module] | `time` | `time%mo, time%day_mo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mgt` | After selecting `hru(j)%mgt_ops` and loading `sched(isched)%mgt_ops(hru(j)%cur_op)` | Copies the current schedule entry into the shared management record so later tests and `mgt_sched` calls operate on the active management operation. |
| `ipl` | After each `mgt_sched` call and `mgt%op2` refresh | Sets the plant index used to read `pcom(j)%plcur(ipl)`; this keeps the heat-unit comparison aligned with the management operation's target plant. |

## File I/O

<!-- facts:io -->


## Lineage

`mgt_operatn.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_operatn.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_operatn' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
