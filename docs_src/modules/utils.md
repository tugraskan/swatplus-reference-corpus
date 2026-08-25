---
kind: module
symbol: utils
title: utils
status: filled
source_hash: 99930186f802a70f
version_label: SWAT+ 62.0.0
variables:
  max_table_cols: Public integer parameter set to 100 in `utils.f90:4`. It bounds header and
    data field arrays in `table_reader` and is consumed by the table parsing helpers that
    split and validate wide input records.
  max_name_len: Public integer parameter set to 50 in `utils.f90:5`. It sets the fixed length
    for header and row-field character arrays inside `table_reader` and constrains stored
    column names and field tokens.
  max_line_len: Public integer parameter set to 2500 in `utils.f90:6`. It bounds the raw input
    line buffer `table_reader%line` for table parsing routines that read full text rows before
    splitting them.
type_components:
  table_reader:
    header_cols: array of header column names
    row_field: array of data fields in a data row of data
    line: character string used to read in lines from data table
    left_str: portion of line left of comment delimiter '#'
    file_name: name of the file being read
    min_cols: string of minimum required column names
    titldum: first line in data file that that will be ignored
    nrow: data row number
    lrow: row number of the of line in the raw input data file to be read next
    ncols: number of header columns
    nfields: number of data columns/fields in a data row
    start_row_numbr: the number of the row in the file to start reading table data
    start_data_row_numbr: 'This number cannot greater than the line number of the header row.

      The line number that the actual data starts.'
    unit: file unit number
    found_header_row: flag to indicate if header row has been found
    col_okay: 'array used to track if warning message has already

      been printed out for unknown column headers'
    file_exists: flag to indicate if file exists
type_summaries:
  table_reader: Mutable file-reading context for a delimited table input stream. It stores
    the current file name, unit, line buffers, header and field arrays, row counters, and
    flags needed to scan a table, validate its columns, and extract data rows.
---

<!-- facts:header -->

`utils` owns the shared table-reader support type, the safe exponential helper, and basic string-splitting/case-conversion routines used by multiple SWAT+ readers and calculations. It also defines the public dimension limits `MAX_TABLE_COLS`, `MAX_NAME_LEN`, and `MAX_LINE_LEN` that bound table parsing and shared text storage.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

The module is mostly a declaration-and-utility container. Its public parameters are compile-time constants, while the `table_reader` state is initialized by the contained `init` routine and then populated by the table-scanning methods such as `get_header_columns` and `get_row_fields`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:gwflow_chan_read] | `unit_out_gw, chancell.gw, unit_fields(1), unit_fields(2), unit_fields(3), unit_fields(4), unit_fields(5), chan_depth.gw` | `MAX_TABLE_COLS, MAX_NAME_LEN, MAX_LINE_LEN` | Uses the shared split_line helper to parse channel-connection rows from `chancell.gw` into fields before internal reads assign the groundwater channel mapping arrays. |
| [sym:gwflow_read] | `unit_*, unit_out_gw, codes.gw, zones.gw, unit_split_fields(2), unit_split_fields(3), unit_split_fields(4), unit_split_fields(5), unit_split_fields(6), cells.gw, unit_split_fields(1), unit_split_fields(7), unit_split_fields(8), unit_split_fields(9), unit_split_fields(10), unit_split_fields(11), unit_split_fields(12), unit_split_fields(13), unit_split_fields(14), unit_split_fields(15), unit_split_fields(16), unit_split_fields(17), unit_split_fields(18), unit_split_fields(19), unit_split_fields(20), unit_split_fields(21), unit_split_fields(22), unit_split_fields(23), cellcon.gw, unit_split_fields(2+j), outputs.gw, gwflow_obs_day.txt, gwflow_obs_mon.txt, gwflow_obs_yr.txt, gwflow_obs_aa.txt, gwflow_chan_obs_flow_day.txt, gwflow_chan_obs_no3_day.txt, gwflow_hru_pump_day.txt, gwflow_hru_pump_mon.txt, gwflow_hru_pump_yr.txt, gwflow_hru_pump_aa.txt, hru_pump.gw, gwflow_cell_wb_ppag_obs_day.txt, pumpex.gw, tile.gw, gwflow_tile_group_day.txt, rescell.gw, floodplain.gw, gwflow_canal.con, gwflow_canal_wb_day.txt, gwflow_canal_sol_day.txt, phreato.gw, phreato_cell.gw, tvheads.gw, solute.gw, cell_sol.gw, minerals.gw, ponds.gw, pond_cell.gw, pond_div.gw, gwflow_pond_wb_day.txt, gwflow_pond_sol_day.txt, gwflow_pond_mass_day.txt, gwflow_pond_conc_day.txt, lsucell.gw, hrucell.gw, transit.gw, gwflow_transit_cell, gwflow_transit_chan, gwflow_transit_tile, sw_group.gw, gwflow_gwsw_group_day.txt, gwflow_chan_hydsep_day.txt` | `MAX_TABLE_COLS, MAX_NAME_LEN, MAX_LINE_LEN` | Uses split_line repeatedly while reading gwflow setup tables and output-control files so it can tokenize wide or variable-width records before populating groundwater configuration, connection, and output arrays. |
| [sym:pest_parm_read] | `pesticide.pes` | `MAX_TABLE_COLS, MAX_NAME_LEN, MAX_LINE_LEN` | Uses the module's safe exponential helper while loading pesticide parameters so half-life values can be converted to decay factors without numerical underflow. |

## Key Consumers

This module is imported mainly by input readers and process routines that need the shared tokenizer or the safe exponential helper. The reader side is led by groundwater setup and pesticide database loading, while the calculation side uses `exp_w` in basin, erosion, tillage, nutrient, plant, sediment, and water-quality formulas.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:gwflow_chan_read] | `split_line` | split_line breaks each text record from chancell.gw into separate columns so the routine can read the numeric values with internal reads and detect whether the optional trailing columns are present. |
| [sym:gwflow_read] | `split_line` | `split_line` tokenizes the gwflow setup rows and output-control records before the routine allocates arrays, loads configuration values, and builds the groundwater exchange and observation mappings. |
| [sym:pest_parm_read] | utils | The routine uses `exp_w` from `utils` while converting pesticide half-lives into decay factors, so later pesticide fate calculations can use numerically stable exponential decay values. |
| [sym:basin_prm_default] | utils | This routine calls `exp_w` when computing `uptake%p_norm`; the wrapped exponential avoids underflow for the phosphorus uptake normalization when `-bsn_prm%p_updis` is very negative. |
| [sym:ero_cfactor] | utils | `exp_w` is used in the cover-factor equations so the erosion calculation can evaluate steep exponentials safely without underflow. |
| [sym:mgt_tillfactor] | utils | `mgt_tillfactor` calls `exp_w` to evaluate exponentials safely when computing the inverse and forward tillage-factor equations. |
| [sym:nut_solp] | utils | nut_solp calls `exp_w` for the exponential attenuation term in the leaching and tile-drain calculations, keeping the phosphorus-loss formulas stable for large negative arguments. |
| [sym:pl_pup] | utils | The routine uses `Exp_w` in the depth-distribution formula for phosphorus uptake so the exponential term remains numerically safe. |
| [sym:sd_channel_sediment3] | utils | The routine calls `exp_w` to evaluate the logistic bank-erosion response safely, which supports the channel bank-erosion calculation. |
| [sym:wq_k2m] | utils | The routine relies on `exp_w` to compute `exp(-t2 / t1)` with underflow protection, stabilizing the semi-analytic m-term calculation. |
| [sym:wq_semianalyt] | utils | The procedure uses `exp_w` to evaluate the concentration update exponential safely, avoiding underflow when the timestep-rate product is very negative. |

## Lineage

`utils.f90` was introduced in `e44625c` (2025-09-23, "Missed adding add utils.f90 on the previous commit. Removed reducing meta, str,…") and has been changed in 10 non-merge commit(s) since, most recently `c2352ba` (2026-04-24, "added additional bounds checks in utils.f90 to check for large positive exponent…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `utils.f90` are listed.

- `c2352ba` (2026-04-24) — added additional bounds checks in utils.f90 to check for large positive exponents
- `4983fdc` (2026-01-22) — updates to utils.f90 to allow for better backwards compatiblity by recoginizing a description column and all data associated with that colum…
- `0af2e22` (2026-01-14) — added chack for required columns in utils.f90
- `71f139b` (2026-01-14) — tmp change
- `7218654` (2026-01-14) — Add table_reader type to utils.f90 and associated methods for file data handling when reading a simple table.
- `e44625c` (2025-09-23) — Missed adding add utils.f90 on the previous commit. Removed reducing meta, str, and lig pools in pl_dormant.f90 because that reduction is do…

## Review Notes

- Module `utils` has no extracted module-level documentation comment.
- Lineage evidence did not resolve any commits for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
