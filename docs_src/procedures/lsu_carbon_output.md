---
kind: procedure
symbol: lsu_carbon_output
title: lsu_carbon_output
status: filled
source_hash: 3dee9d9f9d6b1b36
version_label: SWAT+ 62.0.0
locals:
  ilsu: Loop index for the LSU being aggregated and written. It also identifies the LSU slot
    in the output arrays such as `lsc_d(ilsu)` and `lsc_m(ilsu)`.
  ielem: Loop index over the LSU membership list `lsu_out(ilsu)%num`, used to step through
    the HRUs that contribute to one LSU.
  ihru: The HRU index retrieved from `lsu_out(ilsu)%num(ielem)`, used to access HRU-level
    carbon state and gain/loss arrays.
  iob: Object index for the LSU's output object identifier and label. It is set from `sp_ob1%ru
    + ilsu - 1` so the routine can write `ob(iob)%gis_id` and `ob(iob)%name` with each record.
  const: Temporary area-weight factor copied from `lsu_elem(ihru)%ru_frac` for the current
    HRU contribution.
  lsu_plt_c: Temporary LSU plant-carbon total for the current LSU, computed as the area-weighted
    sum of `pl_mass(ihru)%tot_com%c` across member HRUs and written to the plant-state output
    files.
uses:
  time_module: The routine needs the simulation clock to decide when it is writing daily,
    monthly, yearly, or average-annual output, and to label each record with the current day,
    month, day-of-month, and year. The end-of-month, end-of-year, and end-of-simulation flags
    control when the running monthly, yearly, and average-annual accumulators roll over and
    print.
  basin_module: The print-code structure controls whether each LSU carbon family is emitted
    at daily, monthly, yearly, or average-annual frequency, and whether CSV mirrors are written.
    Without `pco`, the routine would not know which output branches to execute.
  maximum_data_module: The LSU output count is the guard that determines whether this routine
    should do anything at all. If `db_mx%lsu_out` is zero or negative, the routine returns
    immediately and no LSU carbon aggregation or output is performed.
  calibration_data_module: These arrays define which HRUs belong to each LSU and how strongly
    each HRU contributes to the LSU total. `lsu_out` supplies the HRU membership list, while
    `lsu_elem` provides the LSU fraction and object type filter used to area-weight only valid
    HRU contributors.
  hydrograph_module: The routine uses the sequential RU start index to map each LSU to its
    corresponding object record, and it uses the object table to print the GIS identifier
    and object name alongside each carbon record.
  carbon_module: This module owns the LSU and HRU carbon gain/loss, transformation, and summary
    arrays that the routine reads, accumulates, resets, and writes. The routine uses the zero-value
    templates `hscz`, `hrcz`, `hpcz`, and `hscfz` to reinitialize LSU summaries after period
    closes, and it updates the LSU arrays from the HRU arrays on each day.
  plant_module: The routine imports `plant_module`, but the packet did not resolve a specific
    symbol from it. That module is likely present for plant-carbon state definitions or related
    plant state access, but the exact imported symbol is uncertain from the provided evidence.
  organic_mineral_mass_module: The routine reads plant community carbon mass from `pl_mass(ihru)%tot_com%c`
    to compute the LSU plant-carbon state snapshot. That value is area-weighted by LSU fraction
    and written whenever plant-state output is enabled.
  output_landscape_module: The routine imports `output_landscape_module`, but the packet does
    not show a specific symbol from that module being referenced in the visible source. It
    likely provides shared output infrastructure or file handles for landscape-level output,
    but the exact dependency is not identifiable from the extracted evidence.
---

<!-- facts:header -->

Aggregates and writes LSU-level carbon output for gain/loss, transformation, and plant carbon state families.

## Bottom Line

This subroutine runs once per day after the HRU carbon routines have filled the HRU-level daily carbon results. It area-weights those HRU values up to each LSU, stores daily/monthly/yearly/average-annual summaries, and writes them to the configured carbon output units when the matching print codes are enabled.

It reports three LSU carbon families: gain/loss totals for soil, residue, and plant carbon; soil carbon transformations; and a plant-carbon state snapshot. It skips per-layer carbon families because HRUs can have different soil profiles, so those are not aggregated here.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine after the main HRU processing has populated the HRU carbon gain/loss and transformation arrays for the day. The routine then converts those HRU results into LSU-level outputs and summary accumulators that downstream report files depend on for daily, monthly, yearly, and average-annual carbon reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Return immediately when there are no LSU outputs. | The routine checks `db_mx%lsu_out`; if no LSU output regions are configured, it exits without touching the carbon arrays or files. |
| 2. Initialize the daily LSU gain/loss and transformation summaries from zero templates. | For every LSU, it resets the daily LSU summary arrays to the zero-state templates `hscz`, `hrcz`, `hpcz`, and `hscfz` before any HRU contributions are added. |
| 3. Build each LSU's area-weighted carbon totals from member HRUs. | The routine loops over each LSU, maps it to its corresponding object index, then walks the LSU membership list. For each HRU with a valid `ru_frac` and `obtyp == 'hru'`, it adds the area-weighted HRU gain/loss, transformation, and plant-carbon mass into the LSU totals. |
| 4. Roll the daily LSU totals into monthly accumulators. | After the daily LSU totals are computed, the routine adds them into the monthly LSU summary arrays so the monthly reports can be printed at month end. |
| 5. Write daily LSU carbon outputs when daily print codes are enabled. | If the relevant daily print codes are on, the routine writes daily gain/loss, transformation, and plant-carbon records to their output units, and also writes CSV mirrors when `pco%csvout == 'y'`. |
| 6. At end of month, accumulate monthly totals into yearly summaries and print monthly records. | When `time%end_mo == 1`, the routine adds the monthly totals into the yearly accumulators, writes monthly records for each enabled LSU carbon family, and then resets the monthly arrays back to the zero templates. |
| 7. At end of year, accumulate yearly totals into annual summaries and print yearly records. | When `time%end_yr == 1`, the routine adds the yearly totals into the annual accumulators, writes yearly records for each enabled LSU carbon family, and then resets the yearly arrays back to the zero templates. |
| 8. At end of simulation, average annual totals over the printed years and write final records. | When `time%end_sim == 1`, the routine divides the accumulated annual totals by `time%yrs_prt` if any average-annual carbon output is enabled, then writes final average-annual records to the corresponding output units and CSV files. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:basin_module] | `pco` | `pco%cb_gl_lsu%d, pco%csvout, pco%cb_trf_lsu%d, pco%cb_plt_lsu%d, pco%cb_gl_lsu%m, pco%cb_trf_lsu%m, pco%cb_plt_lsu%m, pco%cb_gl_lsu%y, pco%cb_trf_lsu%y, pco%cb_plt_lsu%y, pco%cb_gl_lsu%a, pco%cb_trf_lsu%a, pco%cb_plt_lsu%a` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out` |
| [sym:calibration_data_module] | `lsu_out, lsu_elem` | `lsu_out(ilsu)%num_tot, lsu_out(ilsu)%num(ielem), lsu_elem(ihru)%ru_frac, lsu_elem(ihru)%obtyp` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%ru, ob(iob)%name` |
| [sym:carbon_module] | `lsc_d, lrc_d, lpc_d, lscf_d, hsc_d, hrc_d, hpc_d, hscf_d, lsc_m, lrc_m, lpc_m, lscf_m, lsc_y, lrc_y, lpc_y, lscf_y, lsc_a, lrc_a, lpc_a, lscf_a, hscz, hrcz, hpcz, hscfz` |  |
| [sym:plant_module] | `plant_module` | `No resolved candidate outside references were mapped to this module in the context packet.` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(ihru)%tot_com%c` |
| [sym:output_landscape_module] | `output_landscape_module` | `No candidate outside references were resolved to this module in the context packet.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `lsc_d(ilsu)` | Every time the routine runs and `db_mx%lsu_out > 0`, before any LSU aggregation begins. | `lsc_d(ilsu)` is reinitialized to the zero carbon gain/loss template `hscz` so the current day's LSU soil-carbon gain/loss total starts clean and can be rebuilt from the day’s HRU contributions. |
| `lrc_d(ilsu)` | Every time the routine runs and `db_mx%lsu_out > 0`, before any LSU aggregation begins. | `lrc_d(ilsu)` is reinitialized to `hrcz` so the current day's LSU residue-carbon gain/loss total starts from the zero template before area-weighted HRU contributions are added. |
| `lpc_d(ilsu)` | Every time the routine runs and `db_mx%lsu_out > 0`, before any LSU aggregation begins. | `lpc_d(ilsu)` is reinitialized to `hpcz` so the current day's LSU plant-carbon gain/loss total starts from the zero template before area-weighted HRU contributions are added. |
| `lscf_d(ilsu)` | Every time the routine runs and `db_mx%lsu_out > 0`, before any LSU aggregation begins. | `lscf_d(ilsu)` is reinitialized to `hscfz` so the current day's LSU soil-carbon transformation total starts from the zero template before area-weighted HRU contributions are added. |
| `lsc_m(ilsu)` | At every day-end LSU aggregation pass, after the daily LSU totals are computed from the member HRUs. | `lsc_m(ilsu)` is incremented by the day's LSU soil-carbon gain/loss total so monthly totals can be printed and later rolled into yearly summaries. |
| `lrc_m(ilsu)` | At every day-end LSU aggregation pass, after the daily LSU totals are computed from the member HRUs. | `lrc_m(ilsu)` is incremented by the day's LSU residue-carbon gain/loss total so monthly totals can be printed and later rolled into yearly summaries. |
| `lpc_m(ilsu)` | At every day-end LSU aggregation pass, after the daily LSU totals are computed from the member HRUs. | `lpc_m(ilsu)` is incremented by the day's LSU plant-carbon gain/loss total so monthly totals can be printed and later rolled into yearly summaries. |
| `lscf_m(ilsu)` | At every day-end LSU aggregation pass, after the daily LSU totals are computed from the member HRUs. | `lscf_m(ilsu)` is incremented by the day's LSU soil-carbon transformation total so monthly totals can be printed and later rolled into yearly summaries. |
| `lsc_y(ilsu)` | When `time%end_mo == 1`. | `lsc_y(ilsu)` accumulates the completed month's LSU soil-carbon gain/loss total, building the yearly summary that is printed at end-of-year. |
| `lrc_y(ilsu)` | When `time%end_mo == 1`. | `lrc_y(ilsu)` accumulates the completed month's LSU residue-carbon gain/loss total into the yearly summary. |
| `lpc_y(ilsu)` | When `time%end_mo == 1`. | `lpc_y(ilsu)` accumulates the completed month's LSU plant-carbon gain/loss total into the yearly summary. |
| `lscf_y(ilsu)` | When `time%end_mo == 1`. | `lscf_y(ilsu)` accumulates the completed month's LSU soil-carbon transformation total into the yearly summary. |
| `lsc_a(ilsu)` | When `time%end_yr == 1`. | `lsc_a(ilsu)` accumulates the completed year's LSU soil-carbon gain/loss total into the average-annual total that is normalized at simulation end. |
| `lrc_a(ilsu)` | When `time%end_yr == 1`. | `lrc_a(ilsu)` accumulates the completed year's LSU residue-carbon gain/loss total into the average-annual total. |
| `lpc_a(ilsu)` | When `time%end_yr == 1`. | `lpc_a(ilsu)` accumulates the completed year's LSU plant-carbon gain/loss total into the average-annual total. |
| `lscf_a(ilsu)` | When `time%end_yr == 1`. | `lscf_a(ilsu)` accumulates the completed year's LSU soil-carbon transformation total into the average-annual total. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The initial addition of `lsu_carbon_output` in bc7755a introduced the new LSU carbon aggregation subroutine, its module dependencies, the daily/monthly/yearly/average-annual rollups, and the LSU carbon output files. Commit 6329ff2 then changed the output unit numbers and corresponding CSV unit numbers throughout the routine to resolve carbon output unit collisions, while leaving the aggregation logic intact.

- bc7755a added the entire `lsu_carbon_output` procedure with LSU-level carbon aggregation, time-based rollups, and carbon output writes.
- 6329ff2 retargeted the routine's write statements to new unit numbers such as 4750/4758/4766 and their CSV counterparts to avoid collisions with other carbon output files.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'lsu_carbon_output' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into 8 execution steps aligned with the visible control flow and line numbers.
- plant_module and output_landscape_module are imported, but no resolved candidate outside references were exposed for those modules in the context packet.
- CSV companion writes are present in the source, but only the non-CSV unit writes were requested in Fill Targets.
