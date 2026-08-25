---
kind: procedure
symbol: output_landscape_init
title: output_landscape_init
status: filled
source_hash: ce2f746b4da75b29
version_label: SWAT+ 62.0.0
locals:
  jhru: HRU loop counter used to scan all HRUs for the maximum soil-layer count when defaulting
    `cb_n_layers`.
uses:
  hydrograph_module: Provides spatial-object counts (`sp_ob%hru`, etc.) used to decide whether
    HRU/object outputs are created.
  channel_module: Supplies channel state/types referenced when opening channel-related landscape
    outputs.
  sd_channel_module: Supplies SWAT-deg channel data referenced for channel output headers.
  basin_module: Provides the basin name (`bsn%name`) and the print-control flags (`pco%...`)
    that gate every output file and its time interval.
  maximum_data_module: Provides database dimension maxima used when sizing output headers.
  calibration_data_module: Provides calibration configuration referenced by some output headers.
  aquifer_module: Supplies aquifer state/types referenced when opening aquifer outputs.
  output_landscape_module: Provides the header and units strings (e.g. `wb_hdr`, `wb_hdr_units`)
    written into each output file.
  time_module: Provides the simulation time configuration used to choose which time-interval
    outputs to open.
  carbon_module: Provides carbon-output configuration, including `cb_n_layers` used to size
    carbon output records.
  output_path_module: Provides pesticide/pathogen output header definitions.
  soil_module: Provides per-HRU soil-layer counts (`soil(jhru)%nly`) used to default `cb_n_layers`.
  carbon_legacy_module: Provides the legacy carbon output opener (`carbon_legacy_open`).
---

<!-- facts:header -->

Opens every landscape output file and writes its header and units records. Each output (HRU, land-unit, and basin water balance, nutrient and carbon cycling, losses, and plant/weather) is created only when its print-control flag (`pco%...`) is set for the requested time step.

## Bottom Line

`output_landscape_init` is a startup routine that creates the landscape output files. For each output type and time interval (daily/monthly/yearly/average) it checks the matching print-control flag, calls `open_output_file` to open the file, and writes the basin name, program version, and the column-header and units lines.

It also registers each file in the print-code registry (unit 9000) and sizes the carbon output record length from `cb_n_layers`. Because it only opens files and writes headers, the daily/periodic output routines later append data rows to the files prepared here.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Runs once at model startup, called from `proc_open` during output initialization. It prepares (opens and writes headers for) all landscape output files so the per-time-step output routines can append data rows during the simulation. Nothing computes results here; it only reflects the print-control configuration (`pco`) into the set of open output files.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Default the carbon layer count | If `cb_n_layers` was not set explicitly, scans all HRUs for the maximum soil-layer count (falling back to 7) so carbon outputs include every layer. |
| 2. Open files per print-control flag | For each landscape output type and time interval, checks the matching `pco%...` print flag and, when set, calls `open_output_file` (or the carbon `open_cb_*`/legacy openers) to create the file. |
| 3. Write header records | For each opened file, writes the basin name and program version, the column-header line, and the units line, and registers the file name in the print-code registry (unit 9000). |
| 4. Size carbon output records | Computes the carbon output record length `rl` from `cb_n_layers` so any layer count fits the fixed-width record. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru, sp_ob%hru_lte, sp_ob%ru` |
| [sym:channel_module] | `no resolved imported state` |  |
| [sym:sd_channel_module] | `no resolved imported state` |  |
| [sym:basin_module] | `pco, bsn, bsn_cc` | `pco%wb_hru%d, bsn%name, pco%csvout, pco%wb_hru%m, pco%wb_hru%y, pco%wb_hru%a, pco%nb_hru%d, pco%nb_hru%m, pco%nb_hru%y, pco%nb_hru%a, pco%cb_gl_hru%d, pco%cb_gl_hru%m, pco%cb_gl_hru%y, pco%cb_gl_hru%a, pco%cb_trf_hru%d, pco%cb_trf_hru%m, pco%cb_trf_hru%y, pco%cb_trf_hru%a, pco%cb_lyr_hru%d, pco%cb_lyr_hru%m, pco%cb_lyr_hru%y, pco%cb_lyr_hru%a, pco%cb_npool_hru%d, pco%cb_npool_hru%m, pco%cb_npool_hru%y, pco%cb_npool_hru%a, pco%cb_snap_hru%d, pco%cb_snap_hru%m, pco%cb_snap_hru%y, pco%cb_snap_hru%a, bsn_cc%cswat, pco%cb_plt_hru%d, pco%cb_plt_hru%m, pco%cb_plt_hru%y, pco%cb_plt_hru%a, pco%cb_flux_hru%d, pco%cb_flux_hru%m, pco%cb_flux_hru%y, pco%cb_flux_hru%a, pco%cb_cpool_hru%d, pco%cb_cpool_hru%m, pco%cb_cpool_hru%y, pco%cb_cpool_hru%a, pco%cb_drv_hru%d, pco%cb_drv_hru%m, pco%cb_drv_hru%y, pco%cb_drv_hru%a, pco%cb_dyn_hru%d, pco%cb_dyn_hru%m, pco%cb_dyn_hru%y, pco%cb_dyn_hru%a, pco%ls_hru%d, pco%ls_hru%m, pco%ls_hru%y, pco%ls_hru%a, pco%pw_hru%d, pco%pw_hru%m, pco%pw_hru%y, pco%pw_hru%a, pco%wb_sd%d, pco%wb_sd%m, pco%wb_sd%y, pco%wb_sd%a, pco%ls_sd%d, pco%ls_sd%m, pco%ls_sd%y, pco%ls_sd%a, pco%pw_sd%d, pco%pw_sd%m, pco%pw_sd%y, pco%pw_sd%a, pco%wb_lsu%d, pco%wb_lsu%m, pco%wb_lsu%y, pco%wb_lsu%a` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out` |
| [sym:calibration_data_module] | `no resolved imported state` |  |
| [sym:aquifer_module] | `no resolved imported state` |  |
| [sym:output_landscape_module] | `wb_hdr, wb_hdr_units (and other header/units strings)` | `wb_hdr, wb_hdr_units` |
| [sym:time_module] | `no resolved imported state` |  |
| [sym:carbon_module] | `cb_n_layers` | `cb_n_layers, cb_n_layers_explicit` |
| [sym:output_path_module] | `no resolved imported state` |  |
| [sym:soil_module] | `soil` | `soil(jhru)%nly` |
| [sym:carbon_legacy_module] | `carbon_legacy_open` | `carbon_legacy_open` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cb_n_layers` | At entry, only when `cb_n_layers_explicit` is false. | Defaults the number of carbon output layers to the largest soil-layer count across all HRUs (or 7 if none), so no real layer is truncated in carbon outputs. |
| `rl` | When opening the carbon (per-layer) output files. | Record length for fixed-width carbon output files, sized so any layer count fits. |

## File I/O

<!-- facts:io -->


## Lineage

`output_landscape_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 48 non-merge commit(s) since, most recently `6329ff2` (2026-06-05, "Fix carbon.bsn reader and LSU carbon output unit collisions"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `output_landscape_init.f90` are listed.

- `6329ff2` (2026-06-05) — Fix carbon.bsn reader and LSU carbon output unit collisions
- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `821a63e` (2026-06-02) — reinstate CSU outputs and print flags
- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `28c64c3` (2026-05-14) — Removed output files no longer needed. hru_soilc_stat hru_rsdc_stat, hru_soilcarb_mb_stat
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'output_landscape_init' has no extracted documentation comment.
- Header/output-file initializer: io_references are the 676 open/write header statements (meanings filled mechanically from the extracted unit/file/fields); logic is minimal beyond gating on print-control flags.
- Several use-imported modules (channel_module, sd_channel_module, calibration_data_module, aquifer_module, time_module, output_path_module) had no specific imported symbol resolved to the body; they are recorded as no resolved imported state.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
