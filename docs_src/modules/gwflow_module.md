---
kind: module
symbol: gwflow_module
title: gwflow_module
status: filled
source_hash: 0e116fba945f7e30
version_label: SWAT+ 62.0.0
variables:
  ncell: Integer scalar holding number of gwflow cells.
  num_active: Integer scalar holding number of active cells.
  gw_time_step: Real scalar holding flow solution time step (units days).
  gwflag_day: Integer scalar holding flag for writing daily mass balance file.
  gwflag_mon: Integer scalar holding flag for writing monthly mass balance file.
  gwflag_yr: Integer scalar holding flag for writing yearly mass balance file.
  gwflag_aa: Integer scalar holding flag for writing average annual mass balance file.
  gwflag_obs: Integer scalar holding flag for writing observation well output (default on).
  gwflag_pump: Integer scalar holding flag for writing HRU pumping output (default on).
  gwflag_heat: Integer scalar holding flag for writing heat balance output (default on if
    heat active).
  gwflag_solute: Integer scalar holding flag for writing solute balance output (default on
    if solute active).
  gwflag_flux: Integer scalar holding flag for writing specialty diagnostic output (default
    on).
  bc_type: Integer scalar holding boundary conditions (1=constant head; 2=no-flow).
  conn_type: Integer scalar holding recharge/ET connections (1=HRU; 2=LSU).
  gw_daycount: Integer scalar holding simulation day counter (for pumping time series).
  bc_type_array: Real allocatable 1-D array holding generic array for reading in values for
    structured grid.
  grid_nrow: Integer scalar holding number of rows in structured grid.
  grid_ncol: Integer scalar holding number of columns in structured grid.
  cell_id_usg: Integer allocatable 2-D array holding usg cell number, for cell in structured
    grid (array).
  cell_id_list: Integer allocatable 1-D array holding usg cell number, for cell in structured
    grid (list).
  grid_status: Integer allocatable 2-D array holding cell status for structured grid.
  grid_int: Integer allocatable 2-D array holding generic array for reading in values for
    structured grid.
  grid_val: Real allocatable 2-D array holding generic array for reading in values for structured
    grid.
  cell_row: Integer allocatable 1-D array holding structured grid row for each cell (for cell
    definition output).
  cell_col: Integer allocatable 1-D array holding structured grid column for each cell (for
    cell definition output).
  cell_gis_id: Integer allocatable 1-D array holding authoritative gis_id per cell (gwflowcells.shp
    id), from gwflow.cells col 22.
  cell_name: Character allocatable 1-D array holding authoritative cell name (cellNNNN), from
    gwflow.cells col 2.
  out_gw_celldef: Integer scalar holding file unit for cell definition output.
  gw_state: Allocatable 1-D array of `groundwater_state` — see the `groundwater_state` type.
  gw_ttime: Integer scalar — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  gw_transit_num: Integer scalar — a module-level working variable holding a count (no inline
    source comment; interpreted from the name).
  gw_transit_cells: Integer allocatable 1-D array — a module-level working variable shared
    across the importing routines (no inline source comment in the declaration).
  gw_cell_chan_flag: Integer allocatable 1-D array — a module-level working variable holding
    a control flag (no inline source comment; interpreted from the name).
  gw_cell_chan_time: Real allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_cell_tile_time: Real allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_transit: Allocatable 1-D array of `groundwater_transit` — see the `groundwater_transit`
    type.
  hru_cells_link: Integer scalar holding variables for linking HRUs to grid cells.
  hru_num_cells: Integer allocatable 1-D array — a module-level working variable holding a
    count (no inline source comment; interpreted from the name).
  hru_cells: Integer allocatable 2-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  hru_cells_fract: Real allocatable 2-D array — a module-level working variable holding a
    fraction (no inline source comment; interpreted from the name).
  cells_fract: Real allocatable 2-D array — a module-level working variable holding a fraction
    (no inline source comment; interpreted from the name).
  hrus_connected: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  lsu_cells_link: Integer scalar holding variables for linking LSUs (landscape units) to grid
    cells.
  in_lsu_cell: Integer scalar — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  lsu_num_cells: Integer allocatable 1-D array — a module-level working variable holding a
    count (no inline source comment; interpreted from the name).
  lsu_cells: Integer allocatable 2-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  lsu_cells_fract: Real allocatable 2-D array — a module-level working variable holding a
    fraction (no inline source comment; interpreted from the name).
  lsus_connected: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_hyd_ss: Allocatable 1-D array of `groundwater_ss` — daily.
  gw_hyd_ss_mo: Allocatable 1-D array of `groundwater_ss` — monthly sums.
  gw_hyd_ss_yr: Allocatable 1-D array of `groundwater_ss` — yearly sums.
  gw_hyd_ss_aa: Allocatable 1-D array of `groundwater_ss` — average annual sums.
  gw_head_sum_aa: Real allocatable 1-D array holding head sum across all years for AA avg.
  gw_hyd_grid_mo: Variable of `groundwater_ss` — monthly grid total.
  gw_hyd_grid_yr: Variable of `groundwater_ss` — yearly grid total.
  gw_hyd_grid_aa: Variable of `groundwater_ss` — accumulates simulation total; divided by
    nbyr at end.
  sol_grid_mbef: Real scalar holding kg total solute mass at start of day.
  sol_grid_maft: Real scalar holding kg total solute mass at end of day.
  sim_month: Integer scalar holding month counter for simulation.
  gw_heat_ss: Allocatable 1-D array of `groundwater_ss` — daily.
  gw_heat_ss_mo: Allocatable 1-D array of `groundwater_ss` — monthly sums.
  gw_heat_ss_yr: Allocatable 1-D array of `groundwater_ss` — yearly sums.
  gw_heat_grid_mo: Variable of `groundwater_ss` — monthly grid total.
  gw_heat_grid_yr: Variable of `groundwater_ss` — yearly grid total.
  gw_heat_grid_aa: Variable of `groundwater_ss` — accumulates simulation total; divided by
    nbyr at end.
  gw_bound_near: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_bound_dist: Real allocatable 1-D array holding m.
  gwflow_perc: Real allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_delay: Real allocatable 1-D array — a module-level working variable shared across the
    importing routines (no inline source comment in the declaration).
  gw_rech: Real allocatable 1-D array — a module-level working variable shared across the
    importing routines (no inline source comment in the declaration).
  delay: Real allocatable 1-D array — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  gw_et_flag: Integer scalar — a module-level working variable holding a control flag (no
    inline source comment; interpreted from the name).
  etremain: Real allocatable 1-D array — a module-level working variable shared across the
    importing routines (no inline source comment in the declaration).
  num_chancells: Integer scalar — a module-level working variable holding a count (no inline
    source comment; interpreted from the name).
  gw_chan_id: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_cell: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_chan: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_zone: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_ncell: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_len: Real allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_elev: Real allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_k: Real allocatable 1-D array — a module-level working variable shared across the
    importing routines (no inline source comment in the declaration).
  gw_chan_thick: Real allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_bed_change: Real scalar — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  gw_chan_dpzn: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_obs: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  gw_chan_dep_flag: Integer scalar — a module-level working variable holding a control flag
    (no inline source comment; interpreted from the name).
  gw_chan_ndpzn: Integer scalar — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  gw_chan_dep: Real allocatable 1-D array holding m.
type_components:
  groundwater_state:
    elev: m            |ground surface elevation
    thck: m            |aquifer thickness
    botm: m            |bottom (bedrock) elevation
    xcrd: m            |x coordinate of cell centroid
    ycrd: m            |y coordinate of cell centroid
    area: m2           |surface area
    init: m            |initial groundwater head (beginning of simulation)
    head: m            |current simulated groundwater head
    hydc: m/day        |aquifer hydraulic conductivity
    spyd: m3/m3        |aquifer specific yield
    exdp: m            |groundwater ET extinction depth
    stat: '|status (0=inactive; 1=active; 2=boundary)'
    zone: '|aquifer zone'
    ncon: '|number of connected cells'
    tile: '|tile drainage flag (0=no tile; 1=tile is present)'
    hnew: m            |new groundwater head (at end of day)
    hold: m            |old groundwater head (at beginning of day)
    stor: m3           |currently available groundwater storage
    vbef: m3           |groundwater volume at beginning of day
    vaft: m3           |groundwater volume at end of day
    hdmo: m            |monthly average groundwater head
    hdyr: m            |annual average groundwater head
    delx: m            |change in groundwater position (x direction) for current time step
    dely: m            |change in groundwater position (y direction) for current time step
  groundwater_transit:
    cell: '|current cell where groundwater is located'
    t: d            |cumulative groundwater travel time from recharge area
    t_chan: d            |time for groundwater to reach a channel
    t_tile: d            |time for groundwater to reach a tile drain
    t_well: d            |time for groundwater to reach pumping well
  groundwater_ss:
    chng: '|change in storage (grid summaries only)'
    rech: '|recharge'
    gwet: '|groundwater ET'
    gwsw: '|groundwater discharge to channels'
    swgw: '|channel seepage to groundwater'
    satx: '|saturation excess flow'
    soil: '|groundwater added to soil profile'
    latl: '|lateral flow between cells'
    disp: '|dispersion (heat/solute transport)'
    bndr: '|boundary exchange'
    ppag: '|allocation-driven pumping (irrigation)'
    ppdf: '|pumping deficit (unmet demand)'
    ppex: '|external pumping'
    tile: '|tile drainage outflow'
    resv: '|reservoir exchange'
    wetl: '|wetland exchange'
    fpln: '|floodplain exchange'
    canl: '|canal exchange'
    pond: '|recharge pond seepage'
    phyt: '|phreatophyte transpiration'
    totl: '|sum of inputs and outputs'
  cell_channel_info:
    ncon: '|number of cells connected to the channel'
    cells: '|cells connected to the channel'
    leng: m          |length of channel in the cell
    elev: m          |elevation of channel bed in the cell
    hydc: m          |hydraulic conductivity of channel bed in the cell
    thck: m          |thickness of channel bed in the cell
    dpzn: '|channel depth zone (optional)'
  satx_channel_info:
    ncon: '|number of cells connected to the channel'
    cells: '|cells connected to the channel'
  cell_connections:
    cell_id: '|cells connected to the cell'
    latl: m3         |groundwater flow to/from connected cell
    sat: m          |saturated thickness of connected cell
  tile_channel_info:
    ncon: '|number of cells connected to the channel'
    cells: '|cells connected to the channel'
  cell_reservoir_info:
    ncon: '|number of cells connected to the channel'
    cells: '|cells connected to the channel'
    elev: m    |elevation of channel bed in the cell
    hydc: m    |hydraulic conductivity of channel bed in the cell
    thck: m    |thickness of channel bed in the cell
  cell_floodplain_info:
    ncon: '|number of cells connected to the channel'
    cells: '|cells connected to the channel'
    hydc: m    |hydraulic conductivity of floodplain bottom in the cell
    area: m    |floodplain area in connection with cell
    mtch: '|matching channel cell'
  canal_chan_info:
    ncanal: '|number of canals connected to the channel'
    canals: '|canals connected to the channel'
    wdth: m    |canal width
    dpth: m    |canal depth
    thck: m    |canal thickness
    hydc: m/d  |hydraulic conductivity of canal bed sediments
    dayb: '|beginning day of active canal'
    daye: '|ending day of active canal'
  cell_canal_info:
    ncon: '|number of cells connected to the canal'
    cells: '|cells connected to the canal'
    leng: m    |length of canal in the cell
    elev: m    |stage of canal in the cell
    hydc: m    |hydraulic conductivity of canal bed in the cell
  cell_canal_out_info:
    cell_id: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wdth: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    dpth: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    thck: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    leng: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    elev: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hydc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    dayb: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    daye: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  cell_canal_div_info:
    cell_id: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    canal_id: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    leng: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    elev: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  canal_info:
    canal_id: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    divr: '|recall diversion ID (0 = no recall)'
    width: m    |canal width
    depth: m    |canal water depth
    thick: m    |canal bed thickness
    bed_k: m/day|canal bed hydraulic conductivity
    div: m3   |volume of water diverted from channel source
    stor: m3   |current volume of canal water
    out_seep: m3   |volume of canal water seeped to aquifer
    out_pond: m3   |volume of canal water routed to recharge pond
  cell_pond_info:
    id: '|recharge pond id'
    chan: '|channel which provides water to the recharge pond'
    canal: '|canal which provides water to the recharge pond'
    unl: '|flag for outside source (1 = outside source)'
    ncell: '|number of cells connected to the recharge pond'
    wsta: '|weather station id'
    area: m2   |recharge pond surface area
    bed_k: m/d  |hydraulic conductivity of the pond bed sediments
    evap_co: '|pond evaporation coefficient'
    stor: m3   |current daily volume of the recharge pond
    seep: m3   |current daily seepage from the pond to the aquifer
    div: m3   |current daily specified diversion volume
    div_uns: m3   |unsatisfied diversion volume
    evap: m3   |current daily volume of evaporation from the recharge pond
    dy_start: '|year when recharge pond begins operation'
    cells: '|cells connected to the recharge pond'
    conn_area: m2   |connection area between recharge pond and cell
    sol_mass: kg   |solute mass in the pond water
    sol_conc: g/m3 |solute concentration in the pond water
    unl_conc: g/m3 |solute concentrations for an outside water source
  groundwater_heat_state:
    stor: Joule        |current heat stored in groundwater
    thmc: J/(d m K)    |thermal conductivity
    temp: C            |current groundwater temperature
    tnew: C            |new groundwater temperature (at end of day)
    told: C            |old groundwater temperature (at beginning of day)
    hbef: Joule        |groundwater heat at beginning of day
    haft: Joule        |groundwater heat at end of day
    tpmo: C            |monthly average groundwater temperature
    tpyr: C            |annual average groundwater temperature
  solute_state:
    mass: g            |solute mass in groundwater
    init: g/m3         |solute concentration in groundwater at beginning of simulation
    conc: g/m3         |solute concentration in groundwater
    cnew: g/m3         |new concentrations at end of time step
    mbef: g            |solute mass at beginning of time step
    maft: g            |solute mass at end of time step
    cnmo: g/m3         |monthly average concentration
    cnyr: g/m3         |annual average concentration
  object_solute_state:
    solute: '|nested `solute_state` record'
  minl_state:
    fract: '|fraction of cell that is the salt mineral'
  solute_chem:
    ino3: '|selenium reduction inhibition factor'
    oxyg: g/m3         |oxygen concentration in groundwater
    kd_seo4: '|seo4 sorption partitioning coefficient'
    kd_seo3: '|seo3 sorption partitioning coefficient'
    kd_boron: '|boron sorption partitioning coefficient'
    kseo4: 1/day        |seo4 microbial reduction rate
    kseo3: 1/day        |seo3 microbial reduction rate
    nshale: '|number of shale formations'
    shale: '|presence of shale in cell'
    shale_sseratio: '|sulfur:se ratio in shale'
    shale_o2a: 1/day   |o2 oxidation rate in presence of shale
    shale_no3a: 1/day   |no3 oxidation rate in presence of shale
    bed_flag: '|flag (0,1) for presence of shale in bedrock'
    bed_sse: '|sulfur:se ratio in bedrock shale'
    bed_o2a: 1/day        |o2 oxidation rate in presence of bedrock shale
    bed_no3a: 1/day        |no3 oxidation rate in presence of bedrock shale
    ripar: '|flag: 1=cell in riparian area; 0=not'
  solute_ss:
    rech: g            |solute mass entering cell via recharge water
    gwsw: g            |solute mass leaving cell via groundwater discharging to channels
    swgw: g            |solute mass entering cell via channel water seeping to groundwater
    soil: g            |solute mass leaving cell via gw-->soil transfer
    satx: g            |solute mass leaving cell via saturation excess flow
    ppag: g            |solute mass leaving cell via pumping (for agriculture)
    ppex: g            |solute mass leaving cell via pumping (external demand)
    tile: g            |solute mass leaving cell via tile drainage outflow
    resv: g            |solute mass exchanged with reservoir
    wetl: g            |solute mass exchanged with wetland
    fpln: g            |solute mass exchanged with channel in floodplain
    canl: g            |solute mass exchanged with irrigation canal
    pond: g            |solute mass in recharge pond seepage water
    advn: g            |solute mass advected to/from cell
    disp: g            |solute mass dispersed to/from cell
    rcti: g            |solute mass of chemical reaction (input)
    rcto: g            |solute mass of chemical reaction (output)
    minl: g            |solute mass added (dissolution) or removed (precipitation) via salt
      mineral interactions
    sorb: g            |solute mass of sorption
    totl: g            |sum of mass inputs and outputs
  object_solute_ss:
    solute: '|nested `solute_ss` record'
  solute_ss_sum:
    rech: g            |solute mass entering cell via recharge water
    gwsw: g            |solute mass leaving cell via groundwater discharging to channels
    swgw: g            |solute mass entering cell via channel water seeping to groundwater
    soil: g            |solute mass leaving cell via gw-->soil transfer
    satx: g            |solute mass leaving cell via saturation excess flow
    ppag: g            |solute mass leaving cell via pumping (for agriculture)
    ppex: g            |solute mass leaving cell via pumping (external demand)
    tile: g            |solute mass leaving cell via tile drainage outflow
    resv: g            |solute mass exchanged with reservoir
    wetl: g            |solute mass exchanged with wetland
    fpln: g            |solute mass exchanged with channel in floodplain
    canl: g            |solute mass exchanged with irrigation canal
    pond: g            |solute mass in recharge pond seepage water
    advn: g            |solute mass advected to/from cell
    disp: g            |solute mass dispersed to/from cell
    rcti: g            |solute mass produced by chemical reaction
    rcto: g            |solute mass consumed by chemical reaction
    minl: g            |solute mass produced by salt mineral dissolution
    sorb: g            |solute mass of sorption
  object_solute_ss_sum:
    solute: '|nested `solute_ss_sum` record'
type_summaries:
  groundwater_state: Groundwater state variables for each cell. Holds `elev`, `thck`, `botm`,
    `xcrd`, `ycrd`, `area`, and 18 more fields.
  groundwater_transit: One `groundwater_transit` record groups `cell`, `t`, `t_chan`, `t_tile`,
    `t_well`.
  groundwater_ss: Unified source/sink type -- used for water fluxes, heat fluxes, and grid
    summaries. Holds `chng`, `rech`, `gwet`, `gwsw`, `swgw`, `satx`, and 15 more fields.
  cell_channel_info: Channel-cell connection. Holds `ncon`, `cells`, `leng`, `elev`, `hydc`,
    `thck`, and 12 more fields.
  satx_channel_info: One `satx_channel_info` record groups `ncon`, `cells`, `gw_satx_info`,
    `gw_soil_flag`, `hru_soil`.
  cell_connections: 'Latl: variables for groundwater lateral flow. Holds `cell_id`, `latl`,
    `sat`, `cell_con`, `hru_pump`, `hru_pump_mo`, and 23 more fields.'
  tile_channel_info: Channel-tile connection. Holds `ncon`, `cells`, `gw_tile_info`, `gw_res_flag`,
    `res_thick`, `res_K`, and 1 more fields.
  cell_reservoir_info: Cell-reservoir connection. Holds `ncon`, `cells`, `elev`, `hydc`, `thck`,
    `gw_resv_info`, and 10 more fields.
  cell_floodplain_info: Channel-cell connection. Holds `ncon`, `cells`, `hydc`, `area`, `mtch`,
    `gw_fpln_info`, and 5 more fields.
  canal_chan_info: Canal-channel connection. Holds `ncanal`, `canals`, `wdth`, `dpth`, `thck`,
    `hydc`, and 3 more fields.
  cell_canal_info: Canal-cell connection. Holds `ncon`, `cells`, `leng`, `elev`, `hydc`, `gw_canl_info`,
    and 277 more fields.
  cell_canal_out_info: Canal-cell connection for canals that receive water outside of the
    model domain. Holds `cell_id`, `wdth`, `dpth`, `thck`, `leng`, `elev`, and 3 more fields.
  cell_canal_div_info: Canal-cell connection for canals that receive water from a point source
    diversion. Holds `cell_id`, `canal_id`, `leng`, `elev`.
  canal_info: Canal diversion characteristics. Holds `canal_id`, `divr`, `width`, `depth`,
    `thick`, `bed_K`, and 4 more fields.
  cell_pond_info: Pond features. Holds `id`, `chan`, `canal`, `unl`, `ncell`, `wsta`, and
    14 more fields.
  groundwater_heat_state: One `groundwater_heat_state` record groups `stor`, `thmc`, `temp`,
    `tnew`, `told`, `hbef`, and 3 more fields.
  solute_state: Solute cell state variables. Holds `mass`, `init`, `conc`, `cnew`, `mbef`,
    `maft`, and 2 more fields.
  object_solute_state: One `object_solute_state` record groups `solute`.
  minl_state: One `minl_state` record groups `fract`.
  solute_chem: One `solute_chem` record groups `ino3`, `oxyg`, `kd_seo4`, `kd_seo3`, `kd_boron`,
    `kseo4`, and 11 more fields.
  solute_ss: Solute cell mass sources and sinks (inputs and outputs). Holds `rech`, `gwsw`,
    `swgw`, `soil`, `satx`, `ppag`, and 14 more fields.
  object_solute_ss: One `object_solute_ss` record groups `solute`.
  solute_ss_sum: Summed values for solutes. Holds `rech`, `gwsw`, `swgw`, `soil`, `satx`,
    `ppag`, and 13 more fields.
  object_solute_ss_sum: One `object_solute_ss_sum` record groups `solute`.
---

<!-- facts:header -->

`gwflow_module` owns the gwflow groundwater-model state: the per-cell `groundwater_state` (head, elevation, conductivity, specific yield), the source/sink flux record (`groundwater_ss`), the cell connection and transit types, and the output flags and mass-balance accumulators. It is populated by the gwflow read and initialization routines and consumed by the gwflow solver, the channel/reservoir/wetland/tile/canal exchange routines, the solute and heat routines, and the gwflow output routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container. The flags and scalar counters default in their declarations, and the cell-state, connection, and source/sink arrays are allocated and populated by the gwflow read/initialization routines (`gwflow_read`, `gwflow_*_read`).

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:basin_read_objs] | `unit_*, object.cnt, chancell.gw, gwflow_record` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Imports `gwflow_module`; no specific module symbol from it was resolved in the extracted references for `basin_read_objs`. |
| [sym:cal_parm_select] | `calibration parameter selection (no direct file read here)` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Applies calibration changes to `gwflow_module` state: references `gw_state`, `gw_delay`, `gw_bed_change` (e.g. `cal_parm_select.f90:1062`). |
| [sym:cal_parmchg_read] | `calibration.cal` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Reads input and populates `gwflow_module` state: references `ncell` (e.g. `cal_parmchg_read.f90:24`). |
| [sym:command] | `unit_out_hyd_sep` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Updates `gwflow_module` state: references `gw_daycount` (e.g. `command.f90:657`). |
| [sym:cs_balance] | `unit_6080, unit_6082, unit_6084, unit_6086` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | References `gwflow_module` state: references `gw_state`, `ncell` (e.g. `cs_balance.f90:19`). |
| [sym:gwflow_canal_div] | `unit_canal_name, unit_out_canal_bal, unit_out_canal_sol` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | References `gwflow_module` state: references `gw_state`, `gw_hyd_ss`, `gw_hyd_ss_yr`, `gw_hyd_ss_mo` (e.g. `gwflow_canal_div.f90:80`). |
| [sym:gwflow_chan_read] | `unit_out_gw, chancell.gw, unit_fields(1), unit_fields(2), unit_fields(3), unit_fields(4), unit_fields(5), chan_depth.gw` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Reads input and populates `gwflow_module` state: references `num_chancells`, `gw_chan_id`, `gw_chan_chan`, `gw_chan_len` (e.g. `gwflow_chan_read.f90:37`). |
| [sym:gwflow_lateral] | `unit_out_gw_transit` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | References `gwflow_module` state: references `gw_time_step`, `ncell`, `gw_state`, `bc_type_array` (e.g. `gwflow_lateral.f90:32`). |
| [sym:gwflow_output_init] | `unit_out_gw, gwflow_basin_wb_day.txt, gwflow_basin_wb_mon.txt, gwflow_basin_wb_yr.txt, gwflow_basin_wb_aa.txt, gwflow.wbgroups, unit_aString, gwflow_group_wb_day_, gwflow_basin_heat_day.txt, gwflow_basin_heat_yr.txt, gwflow_basin_heat_aa.txt, file_name(n), gwflow_cell_wb_day.txt, gwflow_cell_wb_mon.txt, gwflow_cell_wb_yr.txt, gwflow_cell_wb_aa.txt` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Imports `gwflow_module`; no specific module symbol from it was resolved in the extracted references for `gwflow_output_init`. |
| [sym:gwflow_output_day] | `unit_obs_name, unit_out_gwobs, unit_out_gwbal_grp+i, unit_out_gwbal, unit_out_heatbal_dy, unit_out_solbal_dy+s, unit_out_gwcell_day, unit_out_hru_pump_day` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Imports `gwflow_module`; no specific module symbol from it was resolved in the extracted references for `gwflow_output_day`. |
| [sym:gwflow_output_mon] | `unit_out_hru_pump_mo, unit_out_gwcell_mon, unit_obs_name, unit_out_gwobs_mon, unit_out_gwbal_mon, unit_out_solbal_mo+s` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Imports `gwflow_module`; no specific module symbol from it was resolved in the extracted references for `gwflow_output_mon`. |
| [sym:gwflow_output_yr] | `unit_out_gwcell_yr, unit_obs_name, unit_out_gwobs_yr, unit_out_hru_pump_yr, unit_out_gwbal_yr, unit_out_heatbal_yr, unit_out_solbal_yr+s` | `ncell, num_active, gw_time_step, gwflag_day, gwflag_mon, gwflag_yr` | Imports `gwflow_module`; no specific module symbol from it was resolved in the extracted references for `gwflow_output_yr`. |

## Key Consumers

Importers include the gwflow read/initialization routines that build the cell grid and connections, the solver and exchange routines (channel, reservoir, wetland, tile, canal, pumping) that read cell state and accumulate source/sink fluxes, the solute and heat transport routines, and the gwflow output routines.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_read_objs] | `out_gw` | `gwflow_module` matters because it provides `out_gw`, the output unit used to create the gwflow record file when gwflow is active. |
| [sym:cal_parmchg_read] | `ncell` | The groundwater-flow cell count `ncell` is the fallback total used when an update targets `gwf` objects, so it determines the size of the explicit element list for groundwater calibration updates. |
| [sym:cs_balance] | `gw_solute_flag`, `gwsol_ss`, `ncell`, `gw_state`, `gwsol_state` | The groundwater-flow module matters because, when gwflow is active, cs_balance pulls dissolved, recharge, reaction, and sorption terms from gwflow cell state instead of the legacy aquifer balances and then zeroes the daily gwflow solute accumulators. |
| [sym:salt_balance] | `gw_solute_flag`, `gwsol_ss`, `ncell`, `gw_state`, `gwsol_state` | The groundwater-flow state determines whether the routine uses gwflow cell-based solute fields or the normal aquifer-module salt arrays. It also supplies the per-cell recharge, transport, and groundwater mass values that replace the aquifer-module paths when gwflow is active. |
| [sym:wet_read_hyd] | `in_wet_cell`, `wet_thick`, `gw_wet_flag`, `out_gw` | `gwflow_module` matters because it provides the shared thickness array `wet_thick`, the gwflow activation flag `gw_wet_flag`, the input unit `in_wet_cell`, and the log unit `out_gw` used by the gwflow-specific file-processing branch. |
| [sym:cal_parm_select] | gwflow_module | `gwflow_module` matters because the aquifer, stream, floodplain, and pond calibration branches update groundwater-flow state and derived coefficients in that module when GW flow is enabled. |
| [sym:gwflow_canal_div] | gwflow_module | The groundwater module provides the per-cell groundwater state and summary arrays that this routine reads and updates. `gw_state(cell_id)%head` and `%stor` determine the seepage direction and limit groundwater withdrawal, while `gw_hyd_ss`, `gw_hyd_ss_yr`, `gw_hyd_ss_mo`, `gw_heat_ss`, and `gw_heat_ss_yr` accumulate canal exchange totals that later groundwater reporting depends on; `gwflag_flux` controls whether the diagnostic output rows are written. |
| [sym:gwflow_chan_read] | gwflow_module | gwflow_module owns the global channel-connection arrays and flags that this reader populates, sizes, and initializes; without that shared state the rest of gwflow would not know which cell-channel links exist or whether depth-zone and observation data are active. |
| [sym:gwflow_lateral] | gwflow_module | Provides the groundwater cell geometry, hydraulic properties, connectivity, boundary classification, transit tracking arrays, and summary accumulators that this routine reads and updates while computing lateral flow and travel time. |
| [sym:gwflow_output_init] | gwflow_module | The routine uses `gw_state(wb_cell)%area` to sum the area of each water-balance group, and `cell_id_list(wb_cell)` to translate structured-grid water-balance cell numbers into actual groundwater cell IDs. Those groundwater state arrays are what make the group bookkeeping and area totals meaningful. |
| [sym:gwflow_output_day] | gwflow_module | This module holds the simulated groundwater state and daily source/sink flux arrays that the routine reads to compute balances and write output. Without `gw_state`, `gw_hyd_ss`, and `gw_hyd_grid_mo`, there is nothing to summarize or accumulate. |
| [sym:gwflow_output_mon] | gwflow_module | This module owns the groundwater state and monthly accumulators that the routine averages, writes, and resets. Without `gw_state`, `gw_hyd_ss_mo`, and `gw_hyd_grid_mo`, there would be no month-end groundwater heads, flux totals, or basin balance values to report. |
| [sym:gwflow_output_yr] | gwflow_module | `gwflow_module` owns all the groundwater state and yearly summary arrays that this routine averages, writes, accumulates into AA storage, and resets. Without those module arrays, the annual groundwater cell, basin, heat, and solute outputs could not be produced. |
| [sym:gwflow_output_aa] | gwflow_module | `gwflow_module` provides the accumulated groundwater state, balance totals, per-cell head sums, and transit-time arrays that this routine converts into average-annual output. Without these shared arrays and totals, there would be nothing to summarize or write. |
| [sym:gwflow_write_celldef] | gwflow_module | `gwflow_module` supplies the cell count, grid layout, output unit, and per-cell state that determine what gets written. `ncell` sets the loop bounds, `out_gw_celldef` identifies the file unit, `cell_row` and `cell_col` provide structured-grid positions, and `gw_state(i)%xcrd`, `%ycrd`, `%zone`, `%stat`, and `%area` provide the fields written to the definition file. |
| [sym:gwflow_pond] | gwflow_module | gwflow_module is the primary data repository for all groundwater state. gwflow_pond reads pond geometry (gw_pond_info), cell connectivity (cells, conn_area, bed_k), diversion amounts (gw_pond_info(r)%div), and control flags (gw_pond_flag, gw_pond_div_flag, gw_solute_flag, gwsol_salt, gwsol_cons, gwflag_flux, gw_daycount). It writes daily, monthly, and yearly per-cell pond recharge flux into gw_hyd_ss(cell_id)%pond, gw_hyd_ss_mo(cell_id)%pond, and gw_hyd_ss_yr(cell_id)%pond for gwflow_simulate's mass-balance pass. |
| [sym:gwflow_read] | gwflow_module | `gwflow_module` owns the groundwater cell state, source/sink accumulators, and output arrays that this routine fills from the input files. The routine writes into `gw_state`, `gw_hyd_ss`, `gw_hyd_ss_yr`, and `gw_hyd_ss_aa` so the simulation starts with cell geometry, zone assignments, hydraulic properties, and zeroed flux summaries. |
| [sym:gwflow_write_cell_array] | `gw_state` | `gw_state` is imported from `gwflow_module`, so this routine is tied to the groundwater model state context even though the extracted body does not reference any `gw_state` component directly; it marks the procedure as part of the groundwater flow output subsystem. |
| [sym:cs_lch] | `gwflow_percsol`, `gw_solute_flag`, `hru_soil` | The gwflow module provides the groundwater solute flag, the groundwater-to-soil constituent flux array, and the groundwater recharge export array. `cs_lch` uses those values to add aquifer-delivered mass to soil layers and to hand off percolation losses to the groundwater solute workflow. |
| [sym:nut_nlch] | `gw_soil_flag`, `gw_solute_flag`, `hru_soil` | Adds groundwater-derived nitrate mass into the soil profile before pathway losses are computed. |
| [sym:nut_solp] | `gw_soil_flag`, `gw_solute_flag`, `hru_soil`, `gwflow_percsol` | gw_soil_flag and gw_solute_flag gate the groundwater-to-soil phosphorus mass transfer, hru_soil provides the transferred mass by HRU and layer, and gwflow_percsol stores the leaching export for later groundwater routing. These states determine whether the routine adds groundwater P to the soil profile and whether it hands leached P off to gwflow. |
| [sym:recall_cs] | `div_conc_cs` | `gwflow_module` supplies `div_conc_cs`, which stores the concentration associated with a diversion for each constituent and recall index. This matters because the routine records the concentration used to compute diversion mass, making that value available to groundwater/flow coupling and later diagnostics. |
| [sym:recall_salt] | `div_conc_salt` | `gwflow_module` matters because it contributes `div_conc_salt`, the diversion salt concentration array. The routine resets and fills that array so groundwater/flow-related salt transport logic can use the diversion concentration later in the simulation. |
| [sym:salt_lch] | `gwflow_percsol`, `gw_solute_flag`, `hru_soil` | gwflow_module provides the groundwater-solute transfer arrays and flags that link this HRU salt routine to the groundwater flow solver. gw_solute_flag and hru_soil determine whether groundwater salt enters the profile and where the corresponding recharge-percolation salt is stored for later groundwater processing. |

## Lineage

`gwflow_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 15 non-merge commit(s) since, most recently `3cc92b5` (2026-06-02, "gwflow input rework"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `gwflow_module.f90` are listed.

- `3cc92b5` (2026-06-02) — gwflow input rework
- `c38f3b8` (2026-04-05) — clean up and bugfixes
- `b78c4ea` (2026-04-04) — gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portability, dynamic array sizes
- `7ff5029` (2026-04-02) — gwflow re-merge: output redesign - long format, print.prt integration, standardized output
- `0ece228` (2026-03-31) — gwflow re-merge: canal and pond processes - canal, canal_ext, canal_div, pond
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `gwflow_module` has no extracted module-level documentation comment.
- Reader rows show 12 candidate initialization/read routines out of 21; treat the table as representative, not exhaustive.
- This module is imported by 50 procedures; the main Used By table shows 24 ranked consumers and the collapsible importer list keeps the complete deterministic list.
- variable_notes and type_notes summaries were completed locally from the module's declaration metadata (type, shape, source comments) and the Derived Type Inventory; reader behaviors were grounded in source references found in each reader. 5 module-level scalar(s) had no inline source comment and were given name-based interpretations — these should be spot-checked.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
