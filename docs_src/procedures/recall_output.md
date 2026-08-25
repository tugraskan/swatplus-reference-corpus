---
kind: procedure
symbol: recall_output
title: recall_output
status: filled
source_hash: 4f756533000a3b6f
version_label: SWAT+ 62.0.0
args:
  irec: '`irec` selects which recall object record to process within the recall object block;
    the routine maps it to the global object index with `iob = sp_ob1%recall + irec - 1` and
    then reads/writes the matching `rec_*` element.'
locals:
  iob: '`iob` is the resolved hydrograph object index for this recall entry. It starts at
    0 and is set from `sp_ob1%recall` plus the incoming `irec` so the routine can access the
    correct `ob(iob)` metadata for file output.'
uses:
  time_module: '`time_module` provides the current simulation date and end-of-period flags
    that decide when daily, monthly, yearly, and average-annual recall output should be written.
    Its fields also supply the timestamps printed with each output record.'
  basin_module: '`basin_module` holds the print-control state that turns recall output on
    or off for each interval and controls whether CSV copies are emitted. Without `pco`, this
    routine would not know which recall streams to write.'
  hydrograph_module: '`hydrograph_module` supplies the object table and the recall hydrograph
    arrays that are being summarized. The routine uses `sp_ob1%recall` to locate the object,
    `ob(iob)%name` and `ob(iob)%typ` to label output, and `rec_d`, `rec_m`, `rec_y`, `rec_a`,
    and `hz` to update and write the stored values.'
---

<!-- facts:header -->

Writes recall hydrograph outputs for a selected object at daily, monthly, yearly, and average-annual intervals.

## Bottom Line

`recall_output` records the current recall hydrograph values for one object into the standard SWAT+ output streams. It uses the simulation date, the object name/type, and the current `rec_d`, `rec_m`, `rec_y`, and `rec_a` values to produce daily, monthly, yearly, and average-annual recall output when the corresponding print flags are enabled.

It also updates the running monthly, yearly, and average-annual accumulators that back those outputs. That makes this routine part of the output summarization path: it both writes the report lines and advances `rec_m`, `rec_y`, and `rec_a` so later time steps have the correct totals.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` during the output phase, after the model has already populated the recall hydrograph arrays and print-control flags for the current time step. Its results feed the model's daily/monthly/yearly/average-annual recall reports and the running accumulators used to build those summaries.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Resolve the recall object index. | Take the incoming recall record index `irec` and convert it to the matching global object index `iob` using `sp_ob1%recall + irec - 1`. |
| 2. Accumulate the daily value into the monthly total. | Add the current daily recall output `rec_d(irec)` to the running monthly accumulator `rec_m(irec)`. |
| 3. Write daily recall output when the daily print controls allow it. | If daily printing is enabled for the current day and recall daily output is turned on, write the daily record to unit 4600 and optionally write the CSV form to unit 4604. |
| 4. Roll monthly totals into yearly totals and reset the monthly accumulator at month end. | When `time%end_mo == 1`, add `rec_m(irec)` into `rec_y(irec)`, write the monthly record to unit 4601 and optionally unit 4605 if monthly recall output is enabled, then reset `rec_m(irec)` to `hz`. |
| 5. Roll yearly totals into average-annual totals and reset the yearly accumulator at year end. | When `time%end_yr == 1`, add `rec_y(irec)` into `rec_a(irec)`, write the yearly record to unit 4602 and optionally unit 4606 if yearly recall output is enabled, then reset `rec_y(irec)` to `hz`. |
| 6. Finish average-annual output at the end of the simulation. | If the simulation is ending and average-annual recall output is enabled, divide `rec_a(irec)` by `time%yrs_prt`, write the average-annual record to unit 4603, and optionally write the CSV form to unit 4607. |
| 7. Return to the caller. | Exit the subroutine after all applicable outputs and accumulator updates are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%recall%d, pco%csvout, pco%recall%m, pco%recall%y, pco%recall%a` |
| [sym:hydrograph_module] | `sp_ob1, ob, rec_m, rec_d, rec_y, rec_a, hz` | `sp_ob1%recall, ob(iob)%name, ob(iob)%typ` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rec_m(irec)` | When `time%end_mo == 1` after the monthly accumulation step. | `rec_m(irec)` is cleared back to `hz` after its value has been rolled into `rec_y(irec)` and optionally written as the monthly recall output. |
| `rec_y(irec)` | When `time%end_yr == 1` after the yearly accumulation step. | `rec_y(irec)` is cleared back to `hz` after its value has been rolled into `rec_a(irec)` and optionally written as the yearly recall output. |
| `rec_a(irec)` | When `time%end_sim == 1 .and. pco%recall%a == 'y'` at the end of the simulation. | `rec_a(irec)` is converted from a running sum to an average by dividing by `time%yrs_prt` before the final average-annual recall record is written. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `recall_output`: df07e3f added the routine with daily, monthly, yearly, and average-annual recall writes; 94b6dec brought the same logic into the imported source and kept the monthly reset to `hz`; 39fabde initialized `iob` to 0 and preserved the existing output flow; 2fe89fd changed the CSV writes from `G0.3` to `G0.6` formatting on units 4604, 4605, 4606, and 4607.

- df07e3f introduced the subroutine and its full recall output/accumulation workflow, including the `sp_ob1%recall` to `iob` mapping, the four print intervals, and the monthly/yearly resets.
- 94b6dec imported the same recall-output logic into the new source snapshot, preserving the same control flow and accumulator updates.
- 39fabde made `iob` explicitly initialized to zero before it is assigned from `sp_ob1%recall + irec - 1`.
- 2fe89fd increased the precision of the CSV-formatted recall outputs by changing the format descriptor on units 4604, 4605, 4606, and 4607 from `G0.3` to `G0.6`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'recall_output' has no extracted documentation comment.
- algorithm_steps revised: replaced the draft's generic three-step outline with source-line-aligned steps that reflect the actual accumulator updates and output branches.
- Source uses `hz` as the reset value for `rec_m` and `rec_y`; this appears to be a zero-valued `hyd_output` placeholder from `hydrograph_module`.
- Lineage evidence resolved four commits; CSV precision change in 2fe89fd is source-backed by the diff.
