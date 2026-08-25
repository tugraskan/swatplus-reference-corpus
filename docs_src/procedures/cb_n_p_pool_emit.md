---
kind: procedure
symbol: cb_n_p_pool_emit
title: cb_n_p_pool_emit
status: filled
source_hash: b7e7afbf4efa2f19
version_label: SWAT+ 62.0.0
args:
  freq_in: Selects the output frequency branch. The routine maps ' d', ' m', ' y', or ' a'
    to specific text and CSV unit numbers and returns immediately unless the corresponding
    pco%cb_npool_hru flag is enabled.
  hru_j: Identifies which HRU profile to export. It is used to read the soil layer count and
    all layer pool values from soil(hru_j) and soil1(hru_j).
  hru_iob: Selects the HRU object metadata used in the row header. It is passed to the row-id
    emit helpers so the output line is labeled with the correct GIS ID and object name.
locals:
  u_txt: Text output unit number for the selected frequency; used for the fixed-width export
    rows.
  u_csv: CSV output unit number for the selected frequency; used only when pco%csvout is enabled.
  k: Loop index over soil layers when filling the buffer from layer-by-layer soil and pool
    arrays.
  n_use: Number of active soil layers in the HRU; used to limit writes and pad deeper columns
    with missing values.
  buf: Temporary layer-value buffer passed to the depth-row and variable-block writers one
    block at a time.
---

<!-- facts:header -->

Writes HRU soil N and P pool profiles as wide, depth-prefixed text and optional CSV tables for a chosen output frequency.

## Bottom Line

cb_n_p_pool_emit exports one HRU's soil nutrient pool profile in a fixed wide format. For the selected frequency, it writes a row identifier, a depth row, then 18 per-layer nutrient columns that summarize N pools followed by P pools.

The routine only runs when the matching carbon/nutrient pool output switch is enabled in pco%cb_npool_hru. It uses the HRU layer count to pad shorter profiles consistently through cb_write_depth_row and cb_write_var_block, so downstream text and CSV exports have aligned layer columns.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from soil_nutcarb_write after the model has finished updating soil carbon and nutrient state for the current HRU and output period. soil_nutcarb_write chooses the requested frequency and passes the HRU index and object index here; the results feed the HRU nutrient pool output files that later analysis and diagnostics depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active output stream for the requested frequency. | The routine switches on freq_in, assigns the matching text and CSV unit numbers, and immediately returns unless the corresponding pco%cb_npool_hru flag is enabled for that frequency. |
| 2. Cache the active layer count for this HRU. | It records soil(hru_j)%nly in n_use so later writes know how many soil layers contain real data for this HRU. |
| 3. Emit the text row identifier and layer-depth row. | The routine writes the standard text row prefix, fills buf with layer depths from soil(hru_j)%phys(k)%d, and sends that buffer to the depth-row writer for the text file. |
| 4. Write the N pool blocks to the text file. | It builds buf for the total N pool and then for each N pool component or family field, calling cb_write_var_block after each fill so the text record contains the full N profile. |
| 5. Write the P pool blocks to the text file. | It repeats the same buffer-fill and write pattern for total P and each P pool component, ending the text row only after the final block. |
| 6. Optionally emit the CSV row and matching profile blocks. | When pco%csvout is enabled, it writes the CSV row prefix, then repeats the depth, N pool, and P pool blocks with CSV formatting and terminates the row at the final block. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows one behavior-changing commit for this procedure: bc7755a expanded the frequency handling to include annual output (' a' / 'al') and replaced older begsim/endsim diagnostics gating with pco%cb_snap_hru for the related soil snapshot code in the same file. No other resolved commit diff in the provided evidence shows changes to cb_n_p_pool_emit itself.

- bc7755a: added annual frequency support in the soil_nutcarb_write file family and established the current frequency-to-unit mapping pattern that includes the ' a' branch used by cb_n_p_pool_emit.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cb_n_p_pool_emit' has no extracted documentation comment.
