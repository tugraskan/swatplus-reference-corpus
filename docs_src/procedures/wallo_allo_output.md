---
kind: procedure
symbol: wallo_allo_output
title: wallo_allo_output
status: filled
source_hash: 860bc9d55c33ae47
version_label: SWAT+ 62.0.0
args:
  iwallo: Selects which water-allocation object in `wallo`, `wallom_out`, `wallod_out`, `walloy_out`,
    and `walloa_out` this call will process and print.
locals:
  itrn: 'Loop index for each transfer object within `wallo(iwallo)`; it drives accumulation
    and output for one transfer object at a time. Initial value: `0`.'
  isrc: 'Loop index for each source within the current transfer object; it is used to sum
    and print source-level output fields. Initial value: `0`.'
uses:
  time_module: '`time` supplies the current day, month, year, and end-of-period flags that
    control when each output file is written and which timestamps are printed in the records.
    `time%yrs_prt` is also used to convert accumulated annual totals into an average-annual
    value at the end of the simulation.'
  hydrograph_module: '`hydrograph_module` is imported here because this procedure runs in
    the broader hydrograph/output workflow and relies on module-managed simulation state already
    prepared elsewhere. Even though no candidate `hydrograph_module` reference was resolved
    in the packet, the module import is part of the routine’s execution context and keeps
    the output step integrated with the model’s flow/timing state.'
  water_allocation_module: '`water_allocation_module` defines the allocation object arrays
    being traversed, the nested transfer/source types being printed, and the accumulator structures
    (`wallod_out`, `wallom_out`, `walloy_out`, `walloa_out`) that this routine updates and
    resets. It also provides the zero-valued `walloz` used to clear the shorter-period source
    outputs after they are written.'
---

<!-- facts:header -->

Writes water-allocation demand outputs for one allocation object across daily, monthly, yearly, and average-annual reporting intervals.

## Bottom Line

`wallo_allo_output` iterates over every transfer object in the selected water-allocation object and accumulates source-level output totals. It writes those totals to the daily, monthly, yearly, and average-annual allocation output files when the corresponding `pco%water_allo` flags are enabled, and it optionally mirrors the same records to CSV-formatted files when `pco%csvout == "y"`.

The routine also resets the shorter-period accumulators after they are printed so each reporting window starts fresh. That makes it the handoff point between the allocation calculations and the model’s report files for demand, withdrawals, and unmet demand.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine during the model’s output phase after `time%yrs > pco%nyskip`, so the allocation outputs are produced only after the configured skip period. Upstream allocation logic must already have filled `wallod_out`, `wallom_out`, `walloy_out`, and `walloa_out`; downstream reporting depends on these written records and on the periodic resets that prevent double counting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over transfer objects | Iterate from the first to the last transfer object in `wallo(iwallo)%trn_obs`, processing one transfer object at a time. |
| 2. Accumulate daily source output | For each source in the current transfer object, add the daily withdrawal/unmet output stored in `wallod_out` into the monthly accumulator `wallom_out`. |
| 3. Write daily output when enabled | If daily water-allocation output is enabled, write the daily record to unit 3110 and, when CSV output is enabled, also write the CSV-formatted record to unit 3114. |
| 4. Reset daily accumulator | Clear each `wallod_out` source entry back to `walloz` so the next day’s daily totals start at zero. |
| 5. Accumulate monthly output at month end | When `time%end_mo == 1`, add the monthly accumulator `wallom_out` into `walloy_out` for each source. |
| 6. Write monthly output when enabled | If month-end water-allocation output is enabled, write the monthly record to unit 3111 and, when CSV output is enabled, also write the CSV-formatted record to unit 3115. |
| 7. Reset monthly accumulator | Clear each `wallom_out` source entry back to `walloz` so the next month’s totals start at zero. |
| 8. Accumulate yearly output at year end | When `time%end_yr == 1`, add the yearly accumulator `walloy_out` into `walloa_out` for each source. |
| 9. Write yearly output when enabled | If year-end water-allocation output is enabled, write the yearly record to unit 3112 and, when CSV output is enabled, also write the CSV-formatted record to unit 3116. |
| 10. Convert to average annual values at simulation end | When `time%end_sim == 1`, divide each `walloa_out` source entry by `time%yrs_prt` to convert accumulated totals into average annual values. |
| 11. Write average-annual output when enabled | If average-annual output is enabled, write the final record to unit 3113 and, when CSV output is enabled, also write the CSV-formatted record to unit 3117. |
| 12. Continue to next transfer object | Finish the current transfer object loop iteration and return to the caller after all transfer objects have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:hydrograph_module] | `wallo, wallod_out, wallom_out, walloy_out, walloa_out, walloz` | `wallo(iwallo)%trn_obs, wallo(iwallo)%trn(itrn)%src_num, wallom_out(iwallo)%trn(itrn)%src(isrc), wallod_out(iwallo)%trn(itrn)%src(isrc), wallo(iwallo)%trn(itrn)%trn_typ, wallo(iwallo)%trn(itrn)%num, wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloy_out(iwallo)%trn(itrn)%src(isrc), walloa_out(iwallo)%trn(itrn)%src(isrc)` |
| [sym:water_allocation_module] | `wallo, wallom_out, wallod_out, walloy_out, walloa_out, walloz` | `wallo(iwallo)%trn_obs, wallo(iwallo)%trn(itrn)%src_num, wallom_out(iwallo)%trn(itrn)%src(isrc), wallod_out(iwallo)%trn(itrn)%src(isrc), wallo(iwallo)%trn(itrn)%trn_typ, wallo(iwallo)%trn(itrn)%num, wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloy_out(iwallo)%trn(itrn)%src(isrc), walloa_out(iwallo)%trn(itrn)%src(isrc)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wallom_out(iwallo)%trn(itrn)%src(isrc)` | At the daily step, before `wallod_out` is reset, the routine adds `wallod_out(iwallo)%trn(itrn)%src(isrc)` into `wallom_out(iwallo)%trn(itrn)%src(isrc)` for every source. | This converts daily source outputs into the monthly accumulator so month-end output can report the sum of all daily values in the reporting window. |
| `wallod_out(iwallo)%trn(itrn)%src(isrc)` | Immediately after the daily record is written, each source entry in `wallod_out(iwallo)%trn(itrn)%src(isrc)` is assigned `walloz`. | This clears the daily source output accumulator so the next day starts from zero and the same daily values are not carried forward. |
| `walloy_out(iwallo)%trn(itrn)%src(isrc)` | At month end (`time%end_mo == 1`), before monthly values are reset, the routine adds `wallom_out(iwallo)%trn(itrn)%src(isrc)` into `walloy_out(iwallo)%trn(itrn)%src(isrc)` for each source. | This rolls monthly totals into the yearly accumulator so the year-end report reflects the sum of all completed months. |
| `walloa_out(iwallo)%trn(itrn)%src(isrc)` | Immediately after the monthly record is written, each source entry in `wallom_out(iwallo)%trn(itrn)%src(isrc)` is assigned `walloz`. | This clears the monthly accumulator after output so the next month starts from zero and does not double count prior months. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits changed `wallo_allo_output`. Commit `d70017a` introduced the subroutine in this file with the daily, monthly, yearly, and average-annual accumulation/output logic, including the resets to `walloz`. Commit `2fe89fd` kept the logic intact but changed the CSV write format for units 3114, 3115, 3116, and 3117 from `G0.3` to `G0.6`.

- `d70017a` added the full `wallo_allo_output` routine: module imports, loops over `wallo(iwallo)%trn_obs`, accumulation into `wallom_out`, `walloy_out`, and `walloa_out`, writes to units 3110/3111/3112/3113 and CSV companions, and resets of `wallod_out` and `wallom_out` after printing.
- `2fe89fd` changed only the CSV formatting for the allocation output files, increasing precision in the `G0.*` format from `G0.3` to `G0.6` for units 3114, 3115, 3116, and 3117.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wallo_allo_output' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into source-backed daily, monthly, yearly, and average-annual processing steps with explicit reset and write phases.
- hydrograph_module is imported by the source but no resolved candidate outside references were available in the packet; its role is inferred only from the import context.
- Lineage evidence resolved; commit `d70017a` introduced the routine and `2fe89fd` changed CSV precision only.
