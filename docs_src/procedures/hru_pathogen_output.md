---
kind: procedure
symbol: hru_pathogen_output
title: hru_pathogen_output
status: filled
source_hash: dd2fd31fc4c7a9a9
version_label: SWAT+ 62.0.0
args:
  ihru: '`ihru` is the HRU index passed in by the caller; the routine copies it to `j` and
    uses that HRU slot to read and update the pathogen balance arrays and to select the matching
    object connectivity record.'
locals:
  ipath: Loop index over pathogen paths, from 1 to `cs_db%num_paths`, so the routine can process
    and report each pathogen constituent separately.
  j: Local HRU index copied from `ihru`; it is the array index used for pathogen balance storage
    and output record selection.
  iob: Sequential object index for the same HRU in `ob`; computed from `sp_ob1%hru + j - 1`
    so output records can print the correct GIS ID and object name.
  const: Monthly day-count scaling factor computed from `ndays(time%mo + 1) - ndays(time%mo)`;
    it is used to normalize the monthly pathogen balance before it is accumulated into yearly
    and annual summaries.
uses:
  output_ls_pathogen_module: This module holds the pathogen balance state that the routine
    both reads and updates. `hpath_bal(j)%path(ipath)` is the current-period balance written
    to the daily output, while `hpathb_m`, `hpathb_y`, and `hpathb_a` store the running monthly,
    yearly, and average-annual summaries that are accumulated and reset inside this routine.
  plant_module: The imported `plant_module` is not directly referenced by any extracted symbol
    in the visible code span, so no specific runtime state from that module can be tied to
    this routine from the provided evidence.
  plant_data_module: The imported `plant_data_module` is not directly referenced by any extracted
    symbol in the visible code span, so no specific runtime state from that module can be
    tied to this routine from the provided evidence.
  time_module: The current date and simulation-end flags from `time_module` determine which
    reporting branches execute and what timestamps are written to the output files. They also
    control the month-end, year-end, and final-simulation accumulation/reset logic.
  basin_module: '`basin_module` holds the print-control flags that gate each output class
    and CSV duplicate. Those flags are the user-facing switches that determine whether the
    HRU pathogen summary is written at daily, monthly, yearly, or final-simulation intervals.'
  output_landscape_module: The module is imported but no extracted symbol from it appears
    in the visible routine body, so no direct state usage can be confirmed from the supplied
    evidence.
  constituent_mass_module: '`cs_db%num_paths` defines how many pathogen paths exist for the
    model run, which directly sets the loop extent and therefore how many pathogen balance
    summaries are updated and reported.'
  hydrograph_module: '`sp_ob1%hru` gives the base object offset for HRUs, and `ob(iob)%name`
    identifies the particular HRU object being reported. The routine needs both to align HRU
    indices with the correct object metadata in the output rows.'
---

<!-- facts:header -->

Writes HRU pathogen balance outputs at daily, monthly, yearly, and average-annual intervals. It updates running pathogen balance summaries and emits them to the configured text and CSV output units.

## Bottom Line

`hru_pathogen_output` is the HRU-level pathogen reporting routine. For each pathogen path in the selected HRU, it accumulates the current balance into monthly, yearly, and average-annual summary arrays, then writes the requested daily, monthly, yearly, or end-of-simulation records when the corresponding print flags are enabled.

Its output depends on the simulation clock, basin print codes, and the number of pathogen paths configured in `cs_db`. The routine does not call other subroutines; instead, it formats the current pathogen balance state from `output_ls_pathogen_module` together with HRU identifiers from `hydrograph_module` and timestamps from `time_module`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` after HRU-level constituent outputs are enabled and `cs_db%num_tot > 0` is true. It depends on the current simulation timestep, print-control settings, and the HRU/object mapping prepared earlier in the run, and its accumulated monthly, yearly, and average-annual values feed the pathogen summary output files used later for diagnostics and reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the caller’s HRU index to local and object indices. | The routine copies `ihru` into `j` and derives `iob` from `sp_ob1%hru + j - 1` so it can access the correct HRU slot and matching object metadata. |
| 2. Loop over every configured pathogen path. | It iterates `ipath` from 1 to `cs_db%num_paths` and immediately adds the current pathogen balance into the running monthly summary for that HRU/path. |
| 3. Write daily pathogen balances when daily output is enabled. | If daily printing is active and the current day matches the requested interval, the routine writes the current pathogen balance to the text daily unit and optionally to the CSV daily unit. |
| 4. On month end, scale and accumulate monthly summaries. | At month end it computes the number of days in the month, scales the monthly balance by that day count, and adds the result into the yearly summary accumulator. |
| 5. Write monthly pathogen summaries when requested. | If monthly pathogen output is enabled, the routine writes the monthly summary to the monthly text unit and optionally to the monthly CSV unit, then resets the monthly accumulator to `pathbz`. |
| 6. On year end, scale and accumulate yearly summaries. | At year end it scales the yearly summary by 12 months and adds that value into the average-annual accumulator. |
| 7. Write yearly pathogen summaries when requested. | If year-end yearly output is enabled, the routine writes the yearly summary to the yearly text unit and optionally to the yearly CSV unit. |
| 8. Emit and reset average-annual pathogen summaries at simulation end. | At the end of the simulation, if average-annual output is enabled, the routine divides the accumulated annual summary by `time%yrs_prt`, writes it to the average-annual output units, and resets the accumulator to `pathbz`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pathogen_module] | `hpathb_m, hpath_bal, hpathb_y, hpathb_a, pathbz` | `hpathb_m(j)%path(ipath), hpath_bal(j)%path(ipath), hpathb_y(j)%path(ipath), hpathb_a(j)%path(ipath)` |
| [sym:plant_module] | `none resolved` | `none resolved` |
| [sym:plant_data_module] | `none resolved` | `none resolved` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%day_print, pco%int_day_cur, pco%int_day, pco%wb_hru%d, pco%csvout, pco%wb_hru%m, pco%wb_hru%y, pco%wb_hru%a` |
| [sym:output_landscape_module] | `none resolved` | `none resolved` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_paths` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%hru, ob(iob)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpathb_m(j)%path(ipath)` | When the loop advances over each pathogen path, before any print gating. | The current pathogen balance is added into the running monthly accumulator for that HRU/path so month-end output can report a period total. |
| `hpathb_y(j)%path(ipath)` | When `time%end_mo == 1`, after monthly scaling and before the monthly accumulator is reset. | The scaled monthly balance is added into the yearly accumulator so the year-end output can reflect the sum of monthly values. |
| `hpathb_a(j)%path(ipath)` | When `time%end_sim == 1 .and. pco%wb_hru%a == 'y'`, after averaging by `time%yrs_prt`. | The final average-annual value is written from the accumulated annual total, then the accumulator is reset to `pathbz` to clear the state after output. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The routine was added in `df07e3f` with the initial HRU pathogen output logic, local-variable initialization, and daily/monthly/yearly/average-annual write branches. `39fabde` initialized the local counters (`ipath`, `j`, `iob`, `const`) and `2fe89fd` changed the CSV pathogen output formatting on units 2794, 2795, and 2796 from `G0.3` to `G0.6`. `dab22e1` only commented out unused format labels 101-103 and did not change runtime behavior.

- `df07e3f` introduced the pathogen HRU output routine itself, including the accumulation of monthly/yearly/annual pathogen balances and the conditional writes to units 2790-2797.
- `39fabde` made the local indices and scaling variable explicitly initialized at declaration time, reducing uninitialized-state risk without changing the output logic.
- `2fe89fd` increased CSV numeric precision for the daily, monthly, and yearly pathogen CSV outputs by switching the format descriptor from `G0.3` to `G0.6`.
- `dab22e1` removed unused format labels from active use by commenting them out, but left the routine’s calculations and output behavior unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_pathogen_output' has no extracted documentation comment.
- algorithm_steps revised: merged the draft into 8 source-backed steps aligned to the visible control-flow branches and loop structure.
- Source imports `plant_module` and `plant_data_module`, but no extracted symbols from those modules appear in the visible body; their direct runtime role here is uncertain from the provided evidence.
