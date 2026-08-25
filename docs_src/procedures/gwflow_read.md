---
kind: procedure
symbol: gwflow_read
title: gwflow_read
status: filled
source_hash: e4fadc7d0121756a
version_label: SWAT+ 62.0.0
locals:
  gwflow_hdr: Character array reserved for groundwater water-balance output headers; it is
    declared here as part of the output-file setup section.
  gwflow_hdr_day: Daily groundwater water-balance header names used when writing daily groundwater
    output tables.
  gwflow_hdr_mon: Monthly groundwater water-balance header names used when writing monthly
    groundwater output tables.
  gwflow_hdr_yr: Yearly groundwater water-balance header names used when writing yearly groundwater
    output tables.
  gwflow_hdr_aa: Average-annual groundwater water-balance header names used when writing long-term
    summary tables.
  gwflow_hdr_day_grp: Daily grouped groundwater water-balance header names for grouped cell
    summaries.
  sol_hdr_day: Daily solute balance header names for groundwater solute output tables.
  sol_hdr_mo: Monthly solute balance header names for groundwater solute output tables.
  sol_hdr_yr: Yearly solute balance header names for groundwater solute output tables.
  sol_hdr_aa: Average-annual solute balance header names for groundwater solute output tables.
  heat_hdr_day: Daily groundwater heat-balance header names for heat output tables.
  heat_hdr_yr: Yearly groundwater heat-balance header names for heat output tables.
  heat_hdr_aa: Average-annual groundwater heat-balance header names for heat output tables.
  hydsep_hdr: Header names for the channel hydrograph-separation output written at the end
    of setup.
  header: Generic character buffer for file metadata and header lines read from the input
    files.
  read_type: String flag that tells the mineral reader whether a block is given as a single
    value or a grid array.
  cs_names: Buffer for constituent name strings when assembling solute lists.
  name: Temporary name field used while reading solute and related records.
  i_exist: Logical file-existence test for optional input files before opening them.
  i_exist2: Secondary logical file-existence test, used when a second optional file must also
    be checked.
  date_time: System date/time array filled by `DATE_AND_TIME` for the startup message.
  i: Primary loop index over cells, zones, groups, HRUs, LSUs, or records depending on the
    block.
  j: Secondary loop/index variable used inside nested loops and per-cell connection reads.
  k: Tertiary loop/index variable, often used for channels, cells, or group counts.
  m: Counter/index for solutes, observation wells, or other sequential record sets.
  n: Counter/index for years, shale groups, or other sequential record sets.
  s: Solute index used when reading or initializing solute arrays.
  isalt: Counter/flag related to salts during solute setup.
  count: General-purpose counter used during file scans and record counts.
  eof: I/O status flag used to detect end-of-file while scanning variable-length files.
  cell_num: Temporary cell identifier read from connection or group records.
  sol_index: Index into the solute list while assigning solute parameters or masses.
  div: Temporary diversion identifier or count while classifying canal records.
  channel: Temporary channel identifier used when linking cells to channels.
  chan_cell: Index of the closest channel-cell candidate for a groundwater cell.
  ob_num: Temporary observation-object identifier used while reading observation-related data.
  dum_id: Dummy integer used to count or hold IDs during file scans.
  active_cell: Stores the nearest active cell found for a boundary cell.
  cell_size: Parsed grid-cell size from `gwflow.codes`; used to configure the groundwater
    grid geometry.
  x_coord: Temporary x-coordinate read from `gwflow.cells` for each groundwater cell.
  y_coord: Temporary y-coordinate read from `gwflow.cells` for each groundwater cell.
  num_conn: Number of connections found for a cell or group while building linked arrays.
  sum: Accumulator used to average delay values before mapping them to HRUs.
  dist_x: X-direction offset between two cell centroids when finding nearest neighbors.
  dist_y: Y-direction offset between two cell centroids when finding nearest neighbors.
  min_dist: Current minimum distance while searching for the nearest active or channel cell.
  distance: Euclidean distance computed between two cell centroids.
  gw_cell_volume: Computed groundwater volume in a cell, used to convert initial concentrations
    to masses.
  in_gw: Input unit number used for the main groundwater configuration files.
  in_wtdepth: Input unit number reserved for the groundwater water-table-depth file.
  in_hru_cell: Input unit number for the HRU-cell connection file.
  in_res_cell: Input unit number for the reservoir-cell connection file.
  in_canal_cell: Input unit number for the canal-cell connection file.
  in_gw_minl: Input unit number for the mineral/constituent file.
  k_zone: Aquifer zone number read from each grid-cell record and used to look up hydraulic
    conductivity.
  sy_zone: Aquifer zone number read from each grid-cell record and used to look up specific
    yield.
  nzones_aquk: Count of hydraulic-conductivity zones found in `zones.gw`.
  nzones_aqusy: Count of specific-yield zones; set equal to the number of zone rows read from
    `zones.gw`.
  nzones_strk: Count of streambed hydraulic-conductivity zones; set from the zone table.
  nzones_strbed: Count of streambed-thickness zones; set from the zone table.
  zones_aquk: Allocated array of aquifer hydraulic conductivity values by zone.
  zones_aqusy: Allocated array of aquifer specific-yield values by zone.
  zones_strk: Allocated array of streambed hydraulic conductivity values by zone.
  zones_strbed: Allocated array of streambed thickness values by zone.
  zones_kt: Allocated array of thermal conductivity values by zone for groundwater heat transport.
  cell_init_temp: Allocated per-cell initial groundwater temperature values used when heat
    transport is enabled.
  nzones_wt: Count of water-table-depth zones used for initial head setup.
  zones_wt: Allocated array of water-table-depth values by zone.
  pumpex_cell: Temporary cell ID while reading external pumping periods from `pumpex.gw`.
  tile_depth_val: Default tile-drain depth read from `tile.gw` before any per-cell overrides
    are applied.
  tile_drain_area_val: Default tile-drain area read from `tile.gw` before any per-cell overrides
    are applied.
  tile_k_val: Default tile hydraulic conductivity read from `tile.gw` before any per-cell
    overrides are applied.
  res_cell: Temporary reservoir-linked cell ID while reading reservoir exchange data.
  res_id: Temporary reservoir ID used to count and assign reservoir-linked cells.
  res_stage: Temporary reservoir stage read from the reservoir-cell connection file.
  canal_out: Integer array marking canals that originate outside the model domain.
  canal_div: Integer array marking canals supplied by point-source diversion.
  con_row_buf: Temporary real buffer that holds one variable-width canal connection row before
    it is decoded.
  day_beg: Starting day for an outside-source canal reach or diversion period.
  day_end: Ending day for an outside-source canal reach or diversion period.
  canal_id: Canal identifier used while counting and storing canal-cell connections.
  ic: Loop index over canals while classifying canal types and properties.
  obj_tot: Number of cell records listed for a canal in the connection file.
  thick: General-purpose thickness value used while reading canal or reservoir geometry.
  depth: General-purpose depth value used while reading canal or reservoir geometry.
  width: General-purpose width value used while reading canal or reservoir geometry.
  bed_k: General-purpose bed conductivity value used while reading canal properties.
  length: General-purpose length value for a canal connection row.
  frc_ret: General-purpose return fraction placeholder declared for groundwater-related file
    parsing.
  stage: Canal stage or water surface elevation read from a connection record.
  fld_ro: General-purpose floodplain runoff placeholder declared for groundwater-related file
    parsing.
  spk_ro: General-purpose spike runoff placeholder declared for groundwater-related file parsing.
  drp_ro: General-purpose drip runoff placeholder declared for groundwater-related file parsing.
  month_days: Days per month array used to convert recharge-pond start dates into simulation-day
    counts.
  yr_start: Start year read for recharge ponds and converted into a model-day offset.
  mo_start: Start month read for recharge ponds and converted into a model-day offset.
  dy_start: Start day read for recharge ponds and converted into a model-day offset.
  num_yr: General counter used when converting dates or iterating annual records.
  num_dy: Simulation-day counter used while converting pond start dates.
  pe_yr_s: Start year of a pumping period from `pumpex.gw`.
  pe_dy_s: Start day-of-year of a pumping period from `pumpex.gw`.
  pe_yr_e: End year of a pumping period from `pumpex.gw`.
  pe_dy_e: End day-of-year of a pumping period from `pumpex.gw`.
  prev_cell: Previous cell ID used to detect runs of repeated pump-period records.
  ipump: Index of the current pumping feature while building the `gw_pumpex_*` arrays.
  iper: Index of the current pumping period within a pump feature.
  gw_pumpex_rates_tmp: Temporary pump rate read from `pumpex.gw` before storing it in the
    per-pump array.
  cell: General cell index used in HRU/LSU linkage and other per-cell setup loops.
  hru_count: Counter used while processing HRU linkage records.
  hru_cell: Temporary HRU-linked cell ID read from the HRU-cell connection file.
  nhru_connected: Number of HRUs that actually have at least one connected grid cell.
  num_hru: Total number of HRUs in the simulation, copied from `sp_ob%hru`.
  hru_area: Area of the current HRU record in the HRU-cell connection file.
  hru_id: Current HRU identifier used while counting and filling HRU-cell links.
  lsu: Current LSU identifier used while counting and filling LSU-cell links.
  nlsu: Total number of LSUs in the simulation, read from the LSU-cell file.
  nlsu_connected: Number of LSUs that are spatially connected to grid cells.
  lsu_id: LSU identifier read from the connected-LSU list.
  cell_count: Count of cells linked to the current HRU or LSU during first-pass scanning.
  poly_area: Polygon intersection area read from HRU/LSU-cell connection rows.
  cell_area: Cell area used when converting polygon intersections to fractions.
  lsu_area: Total LSU area used when converting polygon intersections to fractions.
  bc_type_int: Default boundary-condition type read from `gwflow.codes` and copied to all
    cells before per-cell overrides.
  in_tvh: Input unit number for the time-varying head file.
  cell_id: Temporary cell identifier used in time-varying head, observation, and transit-time
    file reads.
  in_transit_time: Input unit number for the groundwater transit-time file.
  cell_transit: Cell identifier read from `transit.gw` for transit-time tracking.
  gw_obs_cells_init: Allocated list of observation-cell IDs read directly from `outputs.gw`
    before structured-grid remapping.
  obs_cell_id: Temporary observation-cell ID read from the output configuration.
  dum: Dummy integer used for generic reads where the value is only being consumed.
  dum1: Dummy integer used for generic reads where the value is only being consumed.
  dum2: Dummy integer used for generic reads where the value is only being consumed.
  dum3: Dummy integer used for generic reads where the value is only being consumed.
  dum7: Dummy integer used for generic reads where the value is only being consumed.
  dum8: Dummy integer used for generic reads where the value is only being consumed.
  dum4: Dummy real used for generic reads where the value is only being consumed.
  dum5: Dummy real used for generic reads where the value is only being consumed.
  dum6: Dummy real used for generic reads where the value is only being consumed.
  single_value: Placeholder scalar used when a file block provides one value that must be
    broadcast or reused.
  max_num: Largest number of entries found in a variable-width file block while sizing arrays.
  max_cells: Maximum number of cells per HRU or LSU, used to dimension the connection arrays.
  wb_cell: Working cell index used while assembling grouped water-balance data.
  group_area: Area accumulator for grouped groundwater output calculations.
  split_line_buf: Raw line buffer passed to `split_line` for tokenizing wide or variable-width
    records.
  split_fields: Token array that receives fields from a parsed data line.
  code_keys: Token array that receives the key names from `gwflow.codes`.
  n_keys: Number of key tokens parsed from the `gwflow.codes` header row.
  n_vals: Number of value tokens parsed from the `gwflow.codes` value row.
  icode: Loop index used to walk through the key/value pairs in `gwflow.codes`.
  split_nf: Number of fields returned by `split_line` while reading variable-width files.
  combined_yrday: Combined year-day integer from `outputs.gw`, split into separate year and
    day arrays.
  cell_id_in: Cell ID read from input files and checked against the expected row order.
  code_key: Current key name from the `gwflow.codes` header row being dispatched in the select
    case.
  code_val: Current value string from the `gwflow.codes` value row being assigned or read.
  cell_strk_over: Per-cell streambed conductivity override values read from `gwflow.cells`.
  cell_strthick_over: Per-cell streambed thickness override values read from `gwflow.cells`.
  cell_tile_depth_over: Per-cell tile drain depth override values read from `gwflow.cells`.
  cell_tile_area_over: Per-cell tile drain area override values read from `gwflow.cells`.
  cell_tile_k_over: Per-cell tile hydraulic conductivity override values read from `gwflow.cells`.
  cell_strk_set: Logical mask showing which cells supplied a streambed conductivity override.
  cell_strthick_set: Logical mask showing which cells supplied a streambed thickness override.
  cell_tile_depth_set: Logical mask showing which cells supplied a tile drain depth override.
  cell_tile_area_set: Logical mask showing which cells supplied a tile drain area override.
  cell_tile_k_set: Logical mask showing which cells supplied a tile hydraulic conductivity
    override.
uses:
  gwflow_module: '`gwflow_module` owns the groundwater cell state, source/sink accumulators,
    and output arrays that this routine fills from the input files. The routine writes into
    `gw_state`, `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_aa` so the simulation starts with
    cell geometry, zone assignments, hydraulic properties, and zeroed flux summaries.'
  hydrograph_module: '`hydrograph_module` supplies `sp_ob`, which tells this routine how many
    HRUs and gwflow objects exist. That count controls array sizes and whether HRU-linked
    pumping, observation, and per-object outputs need to be prepared.'
  sd_channel_module: '`sd_channel_module` provides the channel-cell mapping and channel geometry
    inputs that this reader uses to attach groundwater cells to stream reaches, build channel-linked
    info arrays, and prepare channel observation and canal seepage bookkeeping.'
  maximum_data_module: '`maximum_data_module` matters because this routine uses `db_mx%canal`
    to size canal-processing arrays before reading `gwflow_canal.con`. Without that maximum-count
    metadata, the canal seepage connection structures could not be allocated correctly.'
  hru_module: '`hru_module` matters because the routine needs the total HRU count to allocate
    HRU-level pumping, recharge, and solute arrays and to map groundwater results back to
    HRUs.'
  reservoir_data_module: '`reservoir_data_module` matters because reservoir exchange setup
    depends on wetland/reservoir data structures being available elsewhere in the model; this
    routine allocates reservoir-cell links and uses reservoir-related counts when parsing
    exchange files.'
  cs_data_module: '`cs_data_module` matters because the solute setup reads `constituents.cs`-driven
    constituent metadata and allocates groundwater solute arrays accordingly. It determines
    how many extra solutes beyond `no3` and `p` are simulated and how they are named.'
  constituent_mass_module: '`constituent_mass_module` matters because `cs_db` provides the
    constituent database counts and names used to extend the groundwater solute list when
    constituent transport is enabled.'
  water_allocation_module: '`water_allocation_module` matters because canal seepage configuration
    depends on the canal database, including diversion identifiers and hydraulic properties
    stored in `canal`. The routine copies those canal properties into groundwater canal-link
    arrays.'
  utils: '`utils` matters because `split_line` tokenizes the wide and variable-width input
    records read from `gwflow.codes`, `gwflow.zones`, `gwflow.cells`, `outputs.gw`, and other
    flat files.'
---

<!-- facts:header -->

Reads and initializes groundwater-flow configuration, grid, connection, and optional transport/exchange inputs for the gwflow subsystem.

## Bottom Line

`gwflow_read` is the main startup routine for the groundwater model. It reads `gwflow.codes` and the other `*.gw` input files, allocates the groundwater state and source/sink arrays, and prepares all flags, mappings, and output files needed before time stepping begins.

It matters because later groundwater flow, heat, solute, pond, canal, reservoir, wetland, floodplain, pumping, and observation output logic all depend on the state this routine loads and derives.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`gwflow_read` runs after `hyd_connect` has read the gwflow connection metadata and after `gwflow_chan_read` has loaded the channel-cell information. Its results are then consumed by the groundwater solver and all later gwflow output routines, which rely on the allocated state, connection maps, flags, and observation/output arrays it prepares.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Print startup message and record time | Writes a timestamped console and log message announcing that groundwater input is being read. |
| 2. Assign input-unit numbers and HRU count | Sets the file-unit numbers used for the groundwater input files and copies the total HRU count from `sp_ob%hru`. |
| 3. Read `gwflow.codes` key/value settings | Opens `codes.gw`, tokenizes the header and value rows, and assigns grid type, cell count, grid dimensions, boundary type, connectivity type, and feature flags such as soil, saturation excess, pumping, tile, reservoir, wetland, floodplain, canal, solute, heat, time step, and output switches. |
| 4. Build default cell ID and boundary-type arrays | For structured grids, creates an identity `cell_id_list`; for all grids, allocates `bc_type_array` and fills it with the default boundary-condition type. |
| 5. Resolve HRU/LSU connection mode | Checks whether `hrucell.gw` or `lsucell.gw` exists, selects the active linkage type, and disables soil or wetland transfers when the linkage does not support them. |
| 6. Load zone property tables | Reads `zones.gw`, counts its zone rows, allocates zone property arrays, then fills hydraulic-conductivity, specific-yield, streambed, and optional thermal-conductivity values by zone. |
| 7. Read per-cell groundwater properties | Allocates the groundwater cell state and per-cell override masks, reads each `cells.gw` row, assigns elevation, thickness, zone, head, coordinates, area, derived bottom elevation, and optional per-cell overrides such as streambed and tile parameters. |
| 8. Read cell-to-cell connectivity | Reads `cellcon.gw`, checks row order, stores each cell's connection count, and allocates the list of connected neighbor cell IDs. |
| 9. Count active cells and boundary neighbors | Counts active cells, sums active groundwater area, and for each boundary cell finds the nearest active cell and its distance. |
| 10. Read output configuration and observation cells | Scans `outputs.gw` to count output times and observation wells, allocates output-date and observation-cell arrays, rereads the file to fill them, and remaps observation IDs for structured grids. |
| 11. Prepare channel-linked groundwater arrays | Allocates channel-related arrays, maps each gwflow cell to its connected channel, applies per-cell streambed overrides, and optionally builds channel observation-cell lists and outputs. |
| 12. Allocate and zero groundwater source/sink summaries | Allocates daily, yearly, average-annual, and monthly groundwater source/sink arrays and initializes all flux components to zero. |
| 13. Read and map pumping, tile, reservoir, wetland, floodplain, canal, heat, solute, pond, transit, and grouping inputs | Processes the optional feature files and external state needed for recharge, ET, lateral flow, channel exchange, saturation excess, pumping, tile drainage, reservoir exchange, wetland and floodplain exchange, canal seepage, phreatophytes, time-varying heads, solute transport, recharge ponds, HRU/LSU links, transit-time tracking, and gw-sw group output. |
| 14. Initialize outputs and starting groundwater state | Allocates hydrograph-separation arrays, opens the hydrograph separation output file, writes its headers, and finishes by writing a record marker to the gwflow log before returning. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state, gw_hyd_ss, gw_hyd_ss_yr, gw_hyd_ss_aa` | `gw_state(i)%zone, gw_state(i)%botm, gw_state(i)%elev, gw_state(i)%thck, gw_state(i)%hydc, gw_state(i)%spyd, gw_state(i)%init, gw_state(i)%ncon, gw_state(i)%area, gw_state(i)%xcrd, gw_state(j)%xcrd, gw_state(i)%ycrd, gw_state(j)%ycrd, gw_hyd_ss(i)%rech, gw_hyd_ss(i)%gwet, gw_hyd_ss(i)%gwsw, gw_hyd_ss(i)%swgw, gw_hyd_ss(i)%satx, gw_hyd_ss(i)%soil, gw_hyd_ss(i)%latl, gw_hyd_ss(i)%bndr, gw_hyd_ss(i)%ppag, gw_hyd_ss(i)%ppdf, gw_hyd_ss(i)%ppex, gw_hyd_ss(i)%tile, gw_hyd_ss(i)%resv, gw_hyd_ss(i)%wetl, gw_hyd_ss(i)%fpln, gw_hyd_ss(i)%canl, gw_hyd_ss(i)%pond, gw_hyd_ss(i)%phyt, gw_hyd_ss(i)%totl, gw_hyd_ss_yr(i)%rech, gw_hyd_ss_yr(i)%gwet, gw_hyd_ss_yr(i)%gwsw, gw_hyd_ss_yr(i)%swgw, gw_hyd_ss_yr(i)%satx, gw_hyd_ss_yr(i)%soil, gw_hyd_ss_yr(i)%latl, gw_hyd_ss_yr(i)%bndr, gw_hyd_ss_yr(i)%ppag, gw_hyd_ss_yr(i)%ppdf, gw_hyd_ss_yr(i)%ppex, gw_hyd_ss_yr(i)%tile, gw_hyd_ss_yr(i)%resv, gw_hyd_ss_yr(i)%wetl, gw_hyd_ss_yr(i)%fpln, gw_hyd_ss_yr(i)%canl, gw_hyd_ss_yr(i)%pond, gw_hyd_ss_yr(i)%phyt, gw_hyd_ss_aa(i)%rech, gw_hyd_ss_aa(i)%gwet, gw_hyd_ss_aa(i)%gwsw, gw_hyd_ss_aa(i)%swgw, gw_hyd_ss_aa(i)%satx, gw_hyd_ss_aa(i)%soil, gw_hyd_ss_aa(i)%latl, gw_hyd_ss_aa(i)%bndr, gw_hyd_ss_aa(i)%ppag, gw_hyd_ss_aa(i)%ppdf, gw_hyd_ss_aa(i)%ppex, gw_hyd_ss_aa(i)%tile, gw_hyd_ss_aa(i)%resv, gw_hyd_ss_aa(i)%wetl, gw_hyd_ss_aa(i)%fpln, gw_hyd_ss_aa(i)%canl, gw_hyd_ss_aa(i)%pond, gw_hyd_ss_aa(i)%phyt` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru, sp_ob%gwflow` |
| [sym:sd_channel_module] | `gw_chan_id, gw_chan_zone, gw_chan_len, gw_chan_elev, gw_chan_dep_flag, gw_chan_obs_flag, gw_chan_obs, gw_chan_nobs, gw_chan_chan, gw_chan_info, gw_chan_K, gw_chan_thick, gw_chan_cell, gw_chan_obs_cell, gw_chan_canl_info` | `gw_chan_id, gw_chan_zone, gw_chan_len, gw_chan_elev, gw_chan_dep_flag, gw_chan_obs_flag, gw_chan_obs, gw_chan_nobs, gw_chan_chan, gw_chan_info, gw_chan_K, gw_chan_thick, gw_chan_cell, gw_chan_obs_cell, gw_chan_canl_info` |
| [sym:maximum_data_module] | `db_mx, gw_ncanal, gw_canl_div_info, gw_canl_info, gw_canl_div_cell, gw_canl_out_info, gw_chan_canl_info, gw_canal_ncells_div, gw_canal_ncells_out, gw_canal_ncells` | `db_mx%canal, gw_ncanal, gw_canl_div_info, gw_canl_info, gw_canl_div_cell, gw_canl_out_info, gw_chan_canl_info, gw_canal_ncells_div, gw_canal_ncells_out, gw_canal_ncells` |
| [sym:hru_module] | `hru` | `hru` |
| [sym:reservoir_data_module] | `wet_dat` | `wet_dat` |
| [sym:cs_data_module] | `rct, rct_shale, gwsol_chem, gwsol_state, gwsol_ss, gwsol_ss_sum, gwsol_ss_sum_mo, gwsol_minl_state, gwsol_nm, gwsol_rctn, gwsol_sorb, mass_rct, mass_min, gwsol_minl, gwsol_salt, gwsol_cons, gwsol_minl, gw_nsolute, gw_nminl` | `rct, rct_shale, gwsol_chem, gwsol_state, gwsol_ss, gwsol_ss_sum, gwsol_ss_sum_mo, gwsol_minl_state, gwsol_nm, gwsol_rctn, gwsol_sorb, mass_rct, mass_min, gwsol_minl, gwsol_salt, gwsol_cons, gw_nsolute, gw_nminl` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db` |
| [sym:water_allocation_module] | `canal` | `canal` |
| [sym:utils] | `split_line` | `split_line` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `in_hru_pump_obs` | When `gwflow.codes` contains a `heat` key and its value is read at the select-case branch. | Enables groundwater heat transport setup; if the key is absent the flag stays at its default of zero and the heat-transport branch is skipped. |
| `in_lsu_cell` | When the routine reads a per-cell connection row in `hrucell.gw` and the active connection mode is HRU-cell. | Marks whether an HRU has one or more connected groundwater cells and drives allocation of HRU-cell mapping arrays. |
| `gw_heat_flag` | When the routine determines that `lsucell.gw` exists and LSU-cell linkage is active. | Marks that LSU-to-cell connectivity is being used instead of HRU-to-cell connectivity, which changes later area-fraction mapping and disables soil/wetland transfers. |
| `cell_id_list(i)` | When a structured-grid cell row is read from `cells.gw` and its cell-specific flags or parameters are present. | Stores the cell's per-row boundary-condition override so later groundwater calculations can treat that cell differently from the default `bc_type_int`. |
| `bc_type_array(i)` | When `cells.gw` supplies a non-`null` override column for streambed conductivity. | Records a per-cell streambed conductivity override that later replaces the zone-based channel-bed value for connected channels. |
| `hru_cells_link` | When `cells.gw` supplies a non-`null` override column for streambed thickness. | Records a per-cell streambed thickness override that later replaces the zone-based channel-bed thickness. |
| `lsu_cells_link` | When `cells.gw` supplies a non-`null` override column for tile depth. | Records a per-cell tile drain depth override so the tile-drain setup can use cell-specific values instead of the global defaults. |
| `gw_soil_flag` | When `cells.gw` supplies a non-`null` override column for tile area. | Records a per-cell tile drain area override that later replaces the default tile-drain area. |
| `gw_wet_flag` | When `cells.gw` supplies a non-`null` override column for tile hydraulic conductivity. | Records a per-cell tile hydraulic conductivity override that later replaces the default tile-drain conductivity. |
| `cell_name(i)` | When a structured-grid observation cell is remapped through `cell_id_list` or a direct cell ID is read from `outputs.gw`. | Stores the final groundwater cell IDs used for observation-well output and later head/solute/temperature reporting. |
| `gw_state(i)%zone` | When `outputs.gw` contains a `head_output_time` record. | Counts and stores the groundwater output year/day schedule used by later head output routines. |
| `gw_state(i)%botm` | When `outputs.gw` contains an `observation_cell` record. | Counts and stores the observation-well cell list used by later groundwater observation output. |
| `gw_state(i)%hydc` | When the routine reads a `detail_debug_cell` record from `outputs.gw`. | Stores the specific groundwater cell to use for detailed debug observation output. |
| `gw_state(i)%spyd` | When `gwflow.cells` row data are read for each cell. | Sets the groundwater cell zone used later to look up zone-based hydraulic and thermal parameters. |
| `gw_state(i)%init` | When each `gwflow.cells` row is read. | Computes the cell bottom elevation from surface elevation minus aquifer thickness for later head and volume calculations. |
| `num_active` | When each `gwflow.cells` row is read. | Assigns the cell hydraulic conductivity from the hydraulic-conductivity zone table. |
| `gwflow_area` | When each `gwflow.cells` row is read. | Assigns the cell specific yield from the specific-yield zone table. |
| `gw_bound_near(i)` | When each `gwflow.cells` row is read and the initial head lies below the computed cell bottom. | Raises the initial groundwater head to the bottom elevation so the simulation does not start with a head below the aquifer bottom. |
| `gw_bound_dist(i)` | When the cell scan finishes and active cells have been identified. | Stores the total number of active cells for later use in groundwater bookkeeping and output. |
| `gw_num_output` | When active-cell areas are summed over the cell list. | Stores the total active groundwater area for the model domain. |
| `gw_num_obs_wells` | When a boundary cell is processed and a nearest active cell is found. | Stores the index of the closest active cell so later boundary exchange can reference it. |
| `gw_cell_obs_ss` | When a boundary cell is processed and the nearest active cell distance is computed. | Stores the distance to the closest active cell for boundary-exchange calculations. |
| `gw_output_yr(n)` | When `outputs.gw` contains a `head_output_time` record. | Counts the number of head-output dates to size the year/day arrays. |
| `gw_output_day(n)` | When `gwflow_read` finishes parsing the cell table for a cell. | Stores the cell name string used later in observation and output files. |

## File I/O

<!-- facts:io -->


## Lineage

`gwflow_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 22 non-merge commit(s) since, most recently `3cc92b5` (2026-06-02, "gwflow input rework"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `gwflow_read.f90` are listed.

- `3cc92b5` (2026-06-02) — gwflow input rework
- `c38f3b8` (2026-04-05) — clean up and bugfixes
- `b78c4ea` (2026-04-04) — gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portability, dynamic array sizes
- `7ff5029` (2026-04-02) — gwflow re-merge: output redesign - long format, print.prt integration, standardized output
- `0ece228` (2026-03-31) — gwflow re-merge: canal and pond processes - canal, canal_ext, canal_div, pond
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_read' has no extracted documentation comment.
- algorithm_steps revised: condensed the long file-by-file setup into 14 model-level steps to match the documented procedure flow and cited only source lines visible in the packet.
- Source uncertainty: some optional module references were not resolved to explicit candidate refs in the packet, so their `outside_state` entries are described from the source usage without inventing additional owned symbols.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
