---
kind: procedure
symbol: hru_carbon_output
title: hru_carbon_output
status: filled
source_hash: 1014fbb983833d4b
version_label: SWAT+ 62.0.0
args:
  ihru: Selects which HRU to report. The routine copies `ihru` into local index `j`, then
    uses that HRU index to access the carbon arrays and the matching hydrograph object.
locals:
  j: Local HRU index used throughout the routine. It is initialized to 0, then set equal to
    `ihru` so the subroutine can use `j` when indexing carbon arrays and output records.
  iob: Local object index into `ob` for the current HRU. It is initialized to 0, then computed
    from `sp_ob1%hru + j - 1` so the routine can write the HRU's GIS id and name from the
    matching object record.
uses:
  plant_module: The routine imports `plant_module`, but no specific symbol from that module
    is referenced in the extracted source lines. It is likely included for shared plant-related
    state needed by the surrounding carbon workflow, but the exact symbol use is not visible
    here.
  plant_data_module: The routine imports `plant_data_module`, but the extracted source does
    not show any direct reference to a symbol from that module. It is part of the carbon reporting
    context, yet the exact dependency is not visible in the snippet.
  time_module: '`time_module` supplies the simulation date flags and labels written to every
    output record. `time%day`, `time%mo`, `time%day_mo`, and `time%yrc` identify when the
    record was produced, while `time%end_mo`, `time%end_yr`, `time%end_sim`, and `time%yrs_prt`
    control when monthly, yearly, and average-annual totals are accumulated, printed, and
    normalized.'
  basin_module: '`basin_module` provides the print-code switches that gate each family of
    outputs. The routine checks `pco%cb_gl_hru` for soil/residue/plant gain-loss output and
    `pco%cb_trf_hru` for soil transformation output at the daily, monthly, yearly, and average-annual
    intervals, and it uses `pco%csvout` to decide whether to emit the parallel CSV records.'
  output_landscape_module: The module is imported in the source, but no symbol from `output_landscape_module`
    is directly referenced in the extracted procedure body. It is therefore a surrounding
    dependency for the landscape output framework, not a visible line-level dependency here.
  hydrograph_module: '`hydrograph_module` provides the HRU-to-object mapping used in the output
    records. `sp_ob1%hru` gives the first HRU object index, and `ob(iob)%gis_id` plus `ob(iob)%name`
    supply the identifiers written alongside the carbon values so the output can be tied back
    to a specific HRU.'
  organic_mineral_mass_module: '`carbon_module` holds the HRU carbon arrays that this routine
    reports and resets. The daily values `hsc_d`, `hrc_d`, `hpc_d`, and `hscf_d` are accumulated
    into monthly totals, the monthly totals feed yearly totals, and the end-of-period reset
    values come from `hscz`, `hrcz`, `hpcz`, and `hscfz`.'
  soil_module: The module is imported, but no symbol from `soil_module` is directly used in
    the extracted lines. It likely supports the broader carbon balance context, but its exact
    role is not visible in this subroutine body.
  carbon_module: '`carbon_module` is the data source and sink for every quantity this routine
    processes. The procedure reads the daily state variables, writes the period aggregates,
    and then resets the monthly, yearly, and annual accumulators back to the zero-state templates
    stored in `hscz`, `hrcz`, `hpcz`, and `hscfz`.'
---

<!-- facts:header -->

Writes HRU carbon gain/loss and transformation outputs for daily, monthly, yearly, and average annual reporting. It also advances the HRU carbon accumulators at each reporting boundary.

## Bottom Line

This subroutine packages HRU carbon results for reporting. On each call it uses the current HRU index to write daily, monthly, yearly, and end-of-simulation values for soil carbon gains/losses, residue carbon gains/losses, plant carbon gains/losses, and soil carbon transformations.

It matters because it is the routine that turns the carbon state stored in `carbon_module` into the text output streams controlled by the basin print codes. It also rolls the daily totals into monthly, yearly, and average-annual accumulators and resets the period accumulators after they are printed.

## Arguments

<!-- facts:arguments -->

## Where It Fits

The routine runs once per HRU when `command` loops over `ihru` and calls `hru_carbon_output`. It depends on the HRU list and print-code setup prepared earlier in the command workflow, and its results feed the carbon output files used for daily, monthly, yearly, and average-annual reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Map the incoming HRU index to local indices. | The routine copies `ihru` into `j` and converts the HRU number into the matching object index `iob = sp_ob1%hru + j - 1`. That mapping lets later writes use the correct HRU carbon arrays and the correct `ob` entry for GIS and name metadata. |
| 2. Accumulate daily gain/loss values into the monthly totals. | The daily carbon gain/loss values are added into the monthly accumulators for soil, residue, plant, and soil transformation outputs. These running totals are what the monthly and longer-period reports will later print. |
| 3. Write daily carbon output when the daily print code is enabled. | If `pco%cb_gl_hru%d` is enabled, the routine writes the daily soil, residue, and plant gain/loss record to unit 4520 and the CSV version to unit 4524 when `pco%csvout` is enabled. If `pco%cb_trf_hru%d` is enabled, it writes the daily soil-transformation record to unit 4550 and the CSV version to unit 4554. |
| 4. On end-of-month, roll monthly totals into yearly totals. | When `time%end_mo == 1`, the routine adds the monthly accumulators into the yearly accumulators for all four carbon families. This preserves the month total for later yearly and average-annual reporting. |
| 5. Write monthly output and reset monthly accumulators. | If the monthly gain/loss print code is enabled, the routine writes the monthly soil, residue, and plant totals to unit 4521 and the monthly transformation total to unit 4551, with CSV companions on units 4525 and 4555 when requested. It then resets the monthly accumulators to the zero-state templates `hscz`, `hrcz`, `hpcz`, and `hscfz`. |
| 6. On end-of-year, roll yearly totals into annual totals. | When `time%end_yr == 1`, the routine adds the yearly accumulators into the average-annual accumulators for soil, residue, plant, and transformation output families. This prepares the values that will later be normalized for average-annual reporting. |
| 7. Write yearly output and reset yearly accumulators. | If the yearly gain/loss print code is enabled, the routine writes the yearly soil, residue, and plant totals to unit 4522 and the yearly transformation total to unit 4552, with CSV companions on units 4526 and 4556 when requested. It then resets the yearly accumulators back to `hscz`, `hrcz`, `hpcz`, and `hscfz`. |
| 8. At end of simulation, average the annual accumulators and write final output. | When `time%end_sim == 1` and at least one average-annual carbon print code is enabled, the routine divides the annual accumulators by `time%yrs_prt` to form average annual values. It then writes the averaged soil, residue, and plant totals to unit 4523 and the averaged transformation total to unit 4553, with CSV companions on units 4527 and 4557, and finally resets the average-annual accumulators to the zero-state templates. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_module] | `plant_module state referenced by the routine` |  |
| [sym:plant_data_module] | `plant_data_module state referenced by the routine` |  |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%cb_gl_hru%d, pco%csvout, pco%cb_trf_hru%d, pco%cb_gl_hru%m, pco%cb_trf_hru%m, pco%cb_gl_hru%y, pco%cb_trf_hru%y, pco%cb_gl_hru%a, pco%cb_trf_hru%a` |
| [sym:output_landscape_module] | `output_landscape_module state referenced by the routine` |  |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%hru, ob(iob)%name` |
| [sym:organic_mineral_mass_module] | `carbon_module state referenced by the routine` |  |
| [sym:soil_module] | `soil_module state referenced by the routine` |  |
| [sym:carbon_module] | `hsc_m, hsc_d, hrc_m, hrc_d, hpc_m, hpc_d, hscf_m, hscf_d, hsc_y, hrc_y, hpc_y, hscf_y, hsc_a, hrc_a, hpc_a, hscf_a, hscz, hrcz, hpcz, hscfz` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hsc_m(j)` | Each call adds the current daily soil carbon gain/loss `hsc_d(j)` into `hsc_m(j)` before any print gating. | `hsc_m(j)` becomes the running monthly soil carbon gain/loss total for the selected HRU. It is later written at month end, rolled into the yearly total, and then reset to `hscz` after monthly printing. |
| `hrc_m(j)` | Each call adds the current daily residue carbon gain/loss `hrc_d(j)` into `hrc_m(j)` before any print gating. | `hrc_m(j)` becomes the running monthly residue carbon gain/loss total for the selected HRU. It is used in the monthly and yearly reports and then reset to `hrcz` after the month is printed. |
| `hpc_m(j)` | Each call adds the current daily plant carbon gain/loss `hpc_d(j)` into `hpc_m(j)` before any print gating. | `hpc_m(j)` becomes the running monthly plant carbon gain/loss total for the selected HRU. It feeds the monthly and yearly reports and is reset to `hpcz` after monthly output. |
| `hscf_m(j)` | Each call adds the current daily soil transformation total `hscf_d(j)` into `hscf_m(j)` before any print gating. | `hscf_m(j)` becomes the running monthly soil transformation total for the selected HRU. It is printed at month end, rolled into the yearly and average-annual totals, and then reset to `hscfz`. |
| `hsc_y(j)` | When `time%end_mo == 1`, the routine adds `hsc_m(j)` into `hsc_y(j)`. | `hsc_y(j)` becomes the running yearly soil carbon gain/loss total. It collects monthly totals until year end, then is printed and reset to `hscz`. |
| `hrc_y(j)` | When `time%end_mo == 1`, the routine adds `hrc_m(j)` into `hrc_y(j)`. | `hrc_y(j)` becomes the running yearly residue carbon gain/loss total. It is printed at year end and reset to `hrcz`. |
| `hpc_y(j)` | When `time%end_mo == 1`, the routine adds `hpc_m(j)` into `hpc_y(j)`. | `hpc_y(j)` becomes the running yearly plant carbon gain/loss total. It feeds the yearly output and is reset to `hpcz` after the year is reported. |
| `hscf_y(j)` | When `time%end_mo == 1`, the routine adds `hscf_m(j)` into `hscf_y(j)`. | `hscf_y(j)` becomes the running yearly soil transformation total. It is written at year end and then reset to `hscfz`. |
| `hsc_a(j)` | When `time%end_yr == 1`, the routine adds `hsc_y(j)` into `hsc_a(j)`. | `hsc_a(j)` becomes the average-annual soil carbon gain/loss accumulator. At simulation end it is divided by `time%yrs_prt`, written, and then reset to `hscz`. |
| `hrc_a(j)` | When `time%end_yr == 1`, the routine adds `hrc_y(j)` into `hrc_a(j)`. | `hrc_a(j)` becomes the average-annual residue carbon gain/loss accumulator. It is normalized at simulation end and then reset to `hrcz`. |
| `hpc_a(j)` | When `time%end_yr == 1`, the routine adds `hpc_y(j)` into `hpc_a(j)`. | `hpc_a(j)` becomes the average-annual plant carbon gain/loss accumulator. It is written after normalization and then reset to `hpcz`. |
| `hscf_a(j)` | When `time%end_yr == 1`, the routine adds `hscf_y(j)` into `hscf_a(j)`. | `hscf_a(j)` becomes the average-annual soil transformation accumulator. It is divided by `time%yrs_prt` at simulation end, written, and reset to `hscfz`. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved for five commits. The routine was introduced in the imported source snapshot, then later changes removed the `hru_module` use, initialized local counters `j` and `iob`, changed the carbon output structure from legacy `nb_hru`/separate-per-family writes to the newer `cb_gl_hru` and `cb_trf_hru` families with combined soil/residue/plant records, updated CSV precision from `G0.3` to `G0.6`, and moved monthly, yearly, and average-annual reset assignments so the accumulators are cleared after the period-specific gates.

- 94b6dec brought in the initial `hru_carbon_output` implementation with daily, monthly, yearly, and average-annual reporting, using `pco%nb_hru` flags and separate output writes for each carbon family.
- 39fabde initialized local variables `j` and `iob` to zero, leaving the routine logic otherwise unchanged.
- 8b8ec15 delayed the monthly reset assignments until after the monthly print gate, added yearly reset assignments after the yearly print gate, and kept the average-annual averaging logic in place.
- 2fe89fd changed CSV output formatting from `G0.3` to `G0.6` for all carbon output families.
- bc7755a refactored the routine to use `pco%cb_gl_hru` and `pco%cb_trf_hru`, combined the soil/residue/plant gain-loss values into single records, and removed the old `nb_hru`-based separate family writes.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_carbon_output' has no extracted documentation comment.
- plant_module and plant_data_module are imported but no direct symbol use was visible in the extracted source lines.
- output_landscape_module is imported but no direct symbol use was visible in the extracted source lines.
- algorithm_steps revised: expanded the draft into the full source-driven sequence and aligned the steps with the visible monthly, yearly, and average-annual branches.
- lineage_summary and lineage_impacts derived only from resolved Git Lineage Evidence diffs.
