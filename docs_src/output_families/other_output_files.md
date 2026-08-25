---
kind: output_family
title: Other Output Files
status: filled
version_label: SWAT+ 62.0.0
---

**Kind:** output file catalog

## Bottom Line

This page catalogs SWAT+ output files that are not part of the standard day/month/year/average-annual time-series families. Most are legacy carbon/soil snapshots or diagnostic and log files: they are written once, per event, or as one-off dumps rather than on the standard reporting frequencies, and several write ad-hoc field lists (sometimes with a literal-string header) rather than a shared record type.

Because these files do not share the family record layout, they are listed here with their writer and purpose instead of a per-file column table. Follow the writer link for the exact fields each one writes.

## Catalog

| Output File | Written By | Purpose (from source) |
|---|---|---|
| `area_calc.out` | [`hyd_connect`](../procedures/hyd_connect.md) | — |
| `basin_carbon_all.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | — |
| `basin_crop_yld_aa.txt`, `basin_crop_yld_yr.txt` | [`time_control`](../procedures/time_control.md) | — |
| `basin_totc.txt` | _(not resolved)_ | — |
| `channel_sd_subday.csv`, `channel_sd_subday.txt` | [`sd_channel_output`](../procedures/sd_channel_output.md) | — |
| `checker.out` | [`proc_hru`](../procedures/proc_hru.md) | — |
| `co2.out` | [`co2_read`](../procedures/co2_read.md) | — |
| `diagnostics.out` | [`carbon_bsn_read`](../procedures/carbon_bsn_read.md) | — |
| `erosion.out` | [`proc_hru`](../procedures/proc_hru.md) | — |
| `files_out.out` | [`output_landscape_init`](../procedures/output_landscape_init.md) | — |
| `flow_duration_curve.out` | [`flow_dur_curve`](../procedures/flow_dur_curve.md) | — |
| `hru_begsim_soil_prop.csv`, `hru_begsim_soil_prop.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | — |
| `hru_carbvars.csv`, `hru_carbvars.txt` | [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md) | — |
| `hru_cbn_lyr.csv`, `hru_cbn_lyr.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | per-layer SOC totals + sequestered. Header written once at file open |
| `hru_cflux_stat.csv`, `hru_cflux_stat.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | per-layer C and N fluxes (37 vars) |
| `hru_cpool_stat.csv`, `hru_cpool_stat.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | per-layer C pools (10 vars) |
| `hru_endsim_soil_prop.csv`, `hru_endsim_soil_prop.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | — |
| `hru_n_p_pool_stat.csv`, `hru_n_p_pool_stat.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | per-layer N and P content of carbon pools |
| `hru_org_allo_vars.csv`, `hru_org_allo_vars.txt` | [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md) | — |
| `hru_org_ratio_vars.csv`, `hru_org_ratio_vars.txt` | [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md) | — |
| `hru_org_trans_vars.csv`, `hru_org_trans_vars.txt` | [`soil_carbvar_write_legacy`](../procedures/soil_carbvar_write_legacy.md) | — |
| `hru_orgc.txt` | _(not resolved)_ | — |
| `hru_plc_stat.csv`, `hru_plc_stat.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | HRU-level plant carbon state (no layers) |
| `hru_seq_lyr.csv`, `hru_seq_lyr.txt` | [`soil_nutcarb_write_legacy`](../procedures/soil_nutcarb_write_legacy.md) | — |
| `hru_totc.txt` | _(not resolved)_ | — |
| `hydcon.csv`, `hydcon.out` | [`hyd_connect_out`](../procedures/hyd_connect_out.md) | — |
| `lu_change_out.txt` | [`actions`](../procedures/actions.md) | — |
| `mgt_out.txt` | [`actions`](../procedures/actions.md) | — |
| `yield.csv`, `yield.out` | [`hru_lte_control`](../procedures/hru_lte_control.md) | — |

## Notes

- Files here are auto-detected outputs that do not match the standard output-family shape (they have fewer than the four day/mon/yr/aa frequencies).
- The carbon/soil snapshot files (`hru_*_stat`, `hru_*_vars`, `hru_cbn_lyr`, `*_soil_prop`, `basin_carbon_all`) are legacy carbon-module outputs; some have a newer parallel implementation opened elsewhere.
- For the exact columns of any file, see its writer procedure (linked above) and the `open_output_file` / header write in source.

## Evidence Used

- Output-file open and write statements across the SWAT+ source.
