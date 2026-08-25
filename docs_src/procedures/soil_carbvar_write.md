---
kind: procedure
symbol: soil_carbvar_write
title: soil_carbvar_write
status: filled
source_hash: b353d481a73fe651
version_label: SWAT+ 62.0.0
args:
  out_freq: '`out_freq` selects which scheduled output branch to use: day, month, year, or
    annual (`" d"`, `" m"`, `" y"`, `" a"`). The routine uses it to choose the matching unit
    numbers and the corresponding driver/dynamic print gates from `pco`.'
locals:
  j: '`j` is the HRU loop index. It identifies which HRU row is being written from 1 through
    `sp_ob%hru`.'
  k: '`k` is the layer index used to copy depth values into the scratch buffer and to limit
    each per-layer variable to `min(cb_n_layers, n_use)` active layers.'
  iob: '`iob` is the object index for the current HRU. It is derived from `sp_ob1%hru + j
    - 1` so the row identifier routines can fetch `ob(hru_iob)%gis_id` and `ob(hru_iob)%name`.'
  n_use: '`n_use` stores the number of soil layers actually present in the current HRU, taken
    from `soil(j)%nly`. It tells the depth and variable writers how many layers are real versus
    padded.'
  u_drv_txt: '`u_drv_txt` is the text-file unit number for the driver-variable output stream
    selected by `out_freq`.'
  u_drv_csv: '`u_drv_csv` is the CSV-file unit number for the driver-variable output stream
    selected by `out_freq`.'
  u_dyn_txt: '`u_dyn_txt` is the text-file unit number for the dynamic-variable output stream
    selected by `out_freq`.'
  u_dyn_csv: '`u_dyn_csv` is the CSV-file unit number for the dynamic-variable output stream
    selected by `out_freq`.'
  buf: '`buf` is a layer-sized scratch array used to stage depth values before calling the
    depth-row writer. It is also passed to the driver and dynamic block writers so they can
    reuse the same per-layer buffer while filling it with each variable.'
  drv_gate: '`drv_gate` is the on/off flag for the requested driver output frequency. If it
    is not `"y"`, the driver branch is skipped.'
  dyn_gate: '`dyn_gate` is the on/off flag for the requested dynamic output frequency. If
    it is not `"y"`, the dynamic branch is skipped.'
uses:
  basin_module: '`basin_module` provides `pco`, which holds the print-code flags that decide
    whether driver and dynamic carbon outputs are written for day, month, year, or annual
    timing, and whether CSV output is enabled at all.'
  carbon_module: '`carbon_module` supplies `cb_n_layers`, the layer count that defines the
    width of each output row and the upper bound for filling the scratch depth buffer.'
  hydrograph_module: '`hydrograph_module` supplies the HRU counts and object lookup needed
    to walk the HRU list and label each row with the correct GIS object name.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides `soil1`, the HRU-linked
    soil mass profile whose driver and dynamic layer values are written out for each row.'
  calibration_data_module: '`calibration_data_module` is listed in the uses set, but no candidate
    symbols from it were resolved in the extracted source lines. Its presence may reflect
    broader module dependencies rather than a direct reference inside this routine.'
  soil_module: '`soil_module` provides `soil`, which supplies each HRU''s number of layers
    and physical layer depths used to populate the depth columns and limit the per-layer writes.'
  time_module: '`time_module` provides the current simulation date fields written into every
    row header so each output record is tied to the timestep being processed.'
---

<!-- facts:header -->

Writes per-layer soil carbon driver and dynamic variables for each HRU in a wide row format. It can produce text and CSV outputs, with one record per HRU per selected output time step.

## Bottom Line

`soil_carbvar_write` is the carbon-variable output routine for HRU soil profiles. It writes a row identifier followed by `cb_n_layers` depth columns and then the per-layer carbon driver or dynamic variables for each HRU.

The routine only runs for the output frequencies requested through `out_freq` and the print codes in `pco`. It writes the driver set, the dynamic set, or both, and it emits CSV versions only when `pco%csvout` is enabled.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called from `command` when carbon-variable HRU output is enabled for the selected frequency (`d`, `m`, `y`, or `a`) and `bsn_cc%cswat == 2`. Before the call, `command` has already checked the time boundary and the relevant `pco%cb_drv_hru` or `pco%cb_dyn_hru` gates; after this routine runs, the timestep's carbon driver and dynamic layer tables are appended to the prepared output units for later analysis.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Choose the output branch for the requested frequency. | The routine maps `out_freq` to one set of text and CSV unit numbers and to the matching driver/dynamic gates in `pco`. If the frequency is not one of the four supported codes, it returns immediately. |
| 2. Skip work when both output families are disabled. | After reading the gates, the routine exits if neither the driver nor dynamic branch is enabled for the selected frequency. |
| 3. Loop over every HRU that needs a carbon-variable row. | For each HRU, the routine computes the object index `iob` and looks up the HRU's active soil-layer count in `soil(j)%nly`. |
| 4. Write the driver branch when requested. | If the driver gate is on, the routine writes the text row id, fills the depth buffer from `soil(j)%phys(k)%d`, writes the depth row, and then emits the driver-variable blocks. When CSV output is enabled, it repeats the same sequence on the CSV unit. |
| 5. Write the dynamic branch when requested. | If the dynamic gate is on, the routine writes the text row id, fills the depth buffer again, writes the depth row, and emits the dynamic-variable blocks. When CSV output is enabled, it repeats the same sequence on the CSV unit. |
| 6. Finish after all HRUs are processed. | The HRU loop ends and the subroutine returns to its caller once all requested rows have been written. |
| 7. Emit the text row identifier. | The helper writes the current date, HRU number, GIS ID, and HRU name to the selected text unit without advancing the record, so later calls can continue the same row. |
| 8. Emit the CSV row identifier. | The helper writes the same row identity fields in comma-separated form to the CSV unit without advancing the record. |
| 9. Fill and write the driver-variable blocks. | The driver helper repeatedly clears `buf_in`, copies one layer variable into the active positions, and passes the buffer to `cb_write_var_block`. It covers soil organic content, tillage and mixing factors, temperature, and emission mixing. |
| 10. Fill and write the dynamic-variable blocks. | The dynamic helper repeatedly clears `buf_in`, copies one layer variable into the active positions, and passes the buffer to `cb_write_var_block`. It covers allocation, N:C ratio, and transformation variables for the HRU soil profile. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco` | `pco%cb_drv_hru%d, pco%cb_dyn_hru%d, pco%cb_drv_hru%m, pco%cb_dyn_hru%m, pco%cb_drv_hru%y, pco%cb_dyn_hru%y, pco%cb_drv_hru%a, pco%cb_dyn_hru%a, pco%csvout` |
| [sym:carbon_module] | `cb_n_layers` |  |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(hru_iob)%name` |
| [sym:organic_mineral_mass_module] | `soil1` |  |
| [sym:calibration_data_module] | `calibration_data_module` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `buf_in` | For each variable block inside `cv_drv_blocks` and `cv_dyn_blocks`, before the next call to `cb_write_var_block`. | `buf_in` is overwritten with the next per-layer variable series. Each time it changes, the routine replaces the previous contents with zeroes and the new HRU layer values so the shared block writer can emit one block at a time. |

## File I/O

<!-- facts:io -->


## Lineage

`soil_carbvar_write.f90` was introduced in `f66c8e6` (2025-03-17, "changes made to outpu an initial set of organic control variables to a file call…") and has been changed in 20 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `soil_carbvar_write.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `3a718e8` (2026-05-12) — Put in an if statement to prevent org_trans lmctp from getting to small. Fixed bmix not being output for csv type files when outputting hru_…
- `dff72aa` (2026-05-06) — Added bmix to carbvar output.
- `3ee775a` (2026-04-30) — Limited biomix linear increase to 30 days. Added tmpf2 and tmpf3 to code to biomix to limit biomix by soil layer temperature. Added tillagef…
- `f366611` (2026-03-18) — Added the parameter tillagef to soil_carbvars output file.
- `f66c8e6` (2025-03-17) — changes made to outpu an initial set of organic control variables to a file called hru_carbvars. Added new print object in print.prt called…

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'soil_carbvar_write' has no extracted documentation comment.
- calibration_data_module is used in the source, but no resolved outside reference from that module was provided in the context packet.
- lineage evidence resolved no commits for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
