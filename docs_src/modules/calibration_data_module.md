---
kind: module
symbol: calibration_data_module
title: calibration_data_module
status: filled
source_hash: 3c383e83cf291a8b
version_label: SWAT+ 62.0.0
variables:
  cal_parms: Allocatable table of calibration parameter definitions. Each record describes
    one adjustable parameter name, object type, and allowed absolute range. It is populated
    by `cal_parm_read` from `cal_parms.cal` and consumed by calibration readers and update
    application code.
  cal_upd: Allocatable table of calibration update definitions. Each record stores a change
    name, type, value, optional conditions, target layers or dates, and explicit target element
    numbers. It is populated by `cal_parmchg_read` from `calibration.cal` and consumed by
    `cal_conditions` and related calibration logic.
  chg: Single working `update_parameters` record used as a scratch/current update container
    in calibration processing. It has the same structure as `cal_upd` and is not initialized
    here; downstream calibration code can copy or build update state into it.
  upd_cond: Allocatable table of conditional-update scheduling records. Each record stores
    the maximum and current hit counts, update-table type, decision-table name, and resolved
    decision-table index. It is populated by `cal_cond_read` from `scen_dtl.upd` and used
    by time-control/conditional-update logic.
  cal_codes: Soft-calibration mode flags. This record holds the single-character switches
    that enable hydrologic, plant, sediment, nutrient, channel, and reservoir calibration
    branches. It is populated by `calsoft_read_codes` from `codes.sft` and read by calibration
    and output routines.
  cal_soft: Global soft-calibration master switch. It starts as `n` and is set when any soft-calibration
    code is active, especially by `calsoft_read_codes`; output and initialization routines
    test it before creating calibration files or running calibration setup.
  cal_hard: Global hard-calibration switch. It starts as `n` and is available for setup logic
    that distinguishes hard calibration from soft calibration, although no reader for it was
    extracted in the packet.
  ls_prms: Allocatable table of landscape calibration parameter bounds and change settings.
    Each record stores a parameter name, database crosswalk number, change type, and negative/positive
    and lower/upper limits. It is populated by `ls_read_lsparms_cal` and consumed by soft
    landscape hydrology calibration routines.
  ch_prms: Allocatable table of channel calibration parameter bounds and change settings.
    Each record stores a parameter name, database crosswalk number, change type, and negative/positive
    and lower/upper limits. It is populated by `ch_read_parms_cal` and consumed by channel
    soft-calibration logic.
  lscal_z: Zero-valued template record for `soft_calib_ls_processes`. It is used to reset
    landscape calibration accumulators to a clean state before a new pass.
  lscal: Allocatable landscape soft-calibration container by region. Each element holds land-use
    membership, measured and simulated landscape calibration values, annual averages, and
    adjustment state for HRU-based soft calibration. It is populated by `lcu_read_softcal`
    and consumed by landscape calibration and output routines.
  lscalt: Allocatable landscape soft-calibration container by region for hru_lte objects.
    It mirrors `lscal` but stores HRU_LTE-based calibration summaries and adjustments. It
    is populated by `lcu_read_softcal` and consumed by landscape calibration and output routines.
  pl_prms: Allocatable plant calibration-region container. Each element stores a region name,
    HRU membership, plant parameter definitions, and per-parameter initial values and bounds.
    It is populated by `pl_read_parms_cal` and consumed by plant calibration routines and
    `pl_write_parms_cal`.
  region: Allocatable landscape-region container used for HRU-based calibration and regional
    output summaries. Each region stores its HRU membership, land-use counts, land-use areas,
    and region labels. It is populated by `reg_read_elements` and `lcu_read_softcal` and consumed
    by landscape output and calibration routines.
  ccu_cal: Allocatable channel calibration-region container. Each region stores calibrated
    channel membership, HRU areas, and accumulated land-use counts/areas. It is populated
    by `ch_read_elements` and `ch_read_orders_cal` and consumed by channel soft-calibration
    code.
  acu_cal: Allocatable aquifer calibration-region container. Each region stores aquifer membership
    and area bookkeeping. It is populated by `aqu_read_elements` and consumed by aquifer output/calibration
    routines.
  rcu_cal: Allocatable reservoir calibration-region container. Each region stores reservoir
    membership and area bookkeeping. It is populated by `res_read_elements` and consumed by
    reservoir output/calibration routines.
  pcu_cal: Allocatable recall-point calibration-region container. Each region stores point-source
    membership and area bookkeeping. It is populated by `rec_read_elements` and consumed by
    recall/output calibration routines.
  lsu_out: Allocatable landscape-unit output membership container. Each element stores an
    LSU name, area, explicit member list, and member count. It is populated by `lsu_read_elements`
    and consumed by basin and LSU output routines.
  lsu_reg: Allocatable landscape-unit region membership container mirroring `lsu_out` for
    regional bookkeeping. It stores region names, areas, explicit member lists, and counts
    for landscape calibration and output workflows.
  acu_out: Allocatable aquifer output membership container. Each element stores an aquifer
    output region name, area, explicit member list, and member count. It is populated by `aqu_read_elements`
    and consumed by aquifer output routines.
  acu_reg: Allocatable aquifer region membership container mirroring `acu_out` for calibration
    bookkeeping. It is populated by `aqu_read_elements` and consumed by aquifer calibration/output
    routines.
  ccu_out: Allocatable channel output membership container. Each element stores a channel
    output region name, area, explicit member list, and member count. It is populated by `ch_read_elements`
    and consumed by channel output routines.
  ccu_reg: Allocatable channel region membership container mirroring `ccu_out` for calibration
    bookkeeping. It is populated by `ch_read_elements` and consumed by channel calibration/output
    routines.
  rcu_out: Allocatable reservoir output membership container. Each element stores a reservoir
    output region name, area, explicit member list, and member count. It is populated by `res_read_elements`
    and consumed by reservoir output routines.
  rcu_reg: Allocatable reservoir region membership container mirroring `rcu_out` for calibration
    bookkeeping. It is populated by `res_read_elements` and consumed by reservoir calibration/output
    routines.
  pcu_out: Allocatable recall-point output membership container. Each element stores a recall
    output region name, area, explicit member list, and member count. It is populated by `rec_read_elements`
    and consumed by recall/output routines.
  pcu_reg: Allocatable recall-point region membership container mirroring `pcu_out` for calibration
    bookkeeping. It is populated by `rec_read_elements` and consumed by recall calibration/output
    routines.
  reg_elem: Allocatable region-element list used for landscape-region membership bookkeeping.
    Each record stores the element name, area, object number, object type, and object-type
    number. It is populated by `reg_read_elements` and consumed by regional calibration/output
    routines.
  lsu_elem: Allocatable landscape-element list used for LSU-to-HRU/HRU_LTE mapping and fraction
    weighting. Each record stores object identity, type, and basin/RU/region fractions. It
    is populated by `lsu_read_elements` and consumed widely by basin, LSU, climate, and calibration
    routines.
  ccu_elem: Allocatable channel-element list used for channel calibration and area weighting.
    Each record stores object identity, type, and basin/RU/region fractions. It is populated
    by `ch_read_elements` and consumed by channel calibration/output routines.
  acu_elem: Allocatable aquifer-element list used for aquifer calibration and area weighting.
    Each record stores object identity, type, and basin/RU/region fractions. It is populated
    by `aqu_read_elements` and consumed by aquifer routines.
  rcu_elem: Allocatable reservoir-element list used for reservoir calibration and area weighting.
    Each record stores object identity, type, and basin/RU/region fractions. It is populated
    by `res_read_elements` and consumed by reservoir routines.
  pcu_elem: Allocatable point-source-element list used for recall calibration and area weighting.
    Each record stores object identity, type, and basin/RU/region fractions. It is populated
    by `rec_read_elements` and consumed by recall routines.
  plcal_z: Zero-valued template record for `soft_calib_pl_processes`. It is used to reset
    plant calibration accumulators to a clean state before a new pass.
  plcal: Allocatable plant calibration-region container. Each element stores a region name,
    HRU membership, land-use/plant records, measured and simulated plant outputs, and adjustment
    state. It is populated by `pl_read_regions_cal` and `pl_read_parms_cal` and consumed by
    plant calibration routines.
  chcal_z: Zero-valued template record for `soft_calib_chan_processes`. It is used to reset
    channel calibration accumulators to a clean state before a new pass.
  chcal: Allocatable channel calibration-region container. Each element stores a region name,
    channel-order membership, measured and simulated channel-process records, and adjustment
    state. It is populated by `ch_read_orders_cal` and consumed by channel calibration routines.
type_components:
  calibration_parameters:
    name: Parameter name such as cn2, esco, awc, or similar model parameter label.
    ob_typ: Object type the parameter applies to, such as hru, chan, res, basin, or plant.
    absmin: Minimum absolute value or lower bound allowed for the parameter.
    absmax: Maximum absolute change or upper bound allowed for the parameter.
    units: Units string recorded for the parameter.
  calibration_conditions:
    var: State variable name being tested.
    alt: Alternate variable or comparison value name.
    targ: Numeric target value used in the condition.
    targc: Comparison-code or comparator label associated with the target.
  update_parameters:
    name: Parameter, structure, land use, or management name being updated.
    num_db: Crosswalk index into the calibration-parameter database for the named target.
    chg_typ: Change type such as absval, abschg, or pctchg.
    val: Requested change value.
    val1: Lower bound of a numerical condition.
    val2: Upper bound of a numerical condition.
    conds: Number of condition records attached to the update.
    lyr1: First soil layer included when the update targets soil variables.
    lyr2: Last soil layer included when the update targets soil variables.
    year1: First year included when the update targets precipitation or temperature updates.
    year2: Last year included when the update targets precipitation or temperature updates.
    day1: First day included when the update targets precipitation or temperature updates.
    day2: Last day included when the update targets precipitation or temperature updates.
    num_tot: Total number of integers read for explicit membership data.
    num_elem: Total number of target elements affected by the update.
    num: Explicit list of target element numbers.
    num_cond: Number of resolved condition records stored in `cond`.
    cond: Explicit array of condition records attached to the update.
  update_conditional:
    max_hits: Maximum number of times the table may be executed.
    num_hits: Current number of times the table has been executed.
    typ: Table type, such as `lu_change` or `hru_fr_change`.
    dtbl: Decision-table name used to schedule the update.
    cond_num: Resolved index of the matching decision table.
  soft_calibration_codes:
    hyd_hru: If a, calibrate all hydrologic balance processes for HRU by land use in each
      region; if b, calibrate baseflow and total runoff; if y, defaults to b for existing
      NAM simulations.
    hyd_hrul: If y, calibrate hydrologic balance for hru_lte by land use in each region.
    plt: If y, calibrate plant growth by land use (by plant) in each region.
    sed: If y, calibrate sediment yield by land use in each region.
    nut: If y, calibrate nutrient balance by land use in each region.
    chsed: If y, calibrate channel widening and bank accretion by stream order.
    chnut: If y, calibrate channel nutrient balance by stream order.
    res: If y, calibrate reservoir budgets by reservoir.
  soft_calib_parms:
    name: Parameter or land-use name.
    num_db: Database crosswalk index for the parameter or land use.
    chg_typ: Type of change such as absval, abschg, or pctchg.
    neg: Negative limit of change.
    pos: Positive limit of change.
    lo: Lower limit of the parameter.
    up: Upper limit of the parameter.
  soft_calib_ls_adjust:
    cn: CN2 adjustment or at-limit flag.
    esco: ESCO adjustment or at-limit flag.
    lat_len: Lateral flow soil-length adjustment or at-limit flag.
    petco: Lowest-layer K or PET coefficient adjustment or at-limit flag.
    slope: Slope adjustment or at-limit flag.
    tconc: Time of concentration adjustment or at-limit flag.
    etco: ETCO adjustment or at-limit flag.
    perco: Percolation coefficient adjustment or at-limit flag.
    revapc: Revap coefficient adjustment or at-limit flag.
    cn3_swf: CN3_SWF adjustment or at-limit flag.
  soft_calib_ls_processes:
    name: Database label for the landscape calibration record.
    srr: Surface runoff ratio or surface runoff/precipitation.
    lfr: Lateral flow ratio or lateral flow/precipitation.
    pcr: Percolation ratio or percolation/precipitation.
    etr: Evapotranspiration ratio or ET/precipitation.
    tfr: Tile flow ratio or tile flow/total runoff.
    pet: Average annual potential evapotranspiration.
    sed: Sediment yield.
    wyr: Water-yield ratio or organic nitrogen yield field when used for nutrient calibration.
    bfr: Baseflow ratio or baseflow/precipitation after subtracting lateral, percolation,
      and tile components.
    solp: Soluble phosphorus yield.
  ls_calib_regions:
    name: Land-use class or calibration label for the record.
    lum_no: Crosswalk number from `lum()%name` to `lscal()%lum()%name`.
    ha: Area in hectares for the land-use class.
    nbyr: Number of years the land use occurred.
    meas: Measured soft-calibration process values for the land-use class.
    precip: Accumulated precipitation used to normalize ratios.
    precip_aa: Average annual precipitation used to normalize ratios.
    precip_aa_sav: Saved average annual precipitation for final output.
    pet: Accumulated potential evapotranspiration used to normalize ratios.
    pet_aa: Average annual potential evapotranspiration used to normalize ratios.
    petco: Potential ET coefficient used for linear adjustment.
    sim: Simulated totals for the class.
    aa: Average annual simulated values for the class.
    prev: Previous-run simulated values.
    prm: Current parameter adjustments used in landscape calibration.
    prm_prev: Previous parameter adjustments used in landscape calibration.
    prm_lim: At-limit flags for current parameter adjustments.
    pcur: Current parameter state.
    phi: High parameter state.
    plo: Low parameter state.
    scur: Current simulated totals.
    shi: Current average-annual simulated values.
    slo: Previous-run simulated totals.
  soft_data_calib_landscape:
    name: Region name.
    lum_num: Number of land uses in the region.
    num_tot: Number of HRUs in the region.
    num: HRU membership list for the region.
    num_reg: Number of regions the soft data applies to.
    reg: Region-name list or label array.
    ireg: Region index list or label array.
    lum: Array of land-use calibration records within the region.
  pl_parms_cal:
    var: Plant variable name being calibrated.
    name: Plant parameter or land-use name.
    init_val: Initial calibrated value for the parameter.
    chg_typ: Type of change such as absval, abschg, or pctchg.
    neg: Negative limit per iteration.
    pos: Positive limit per iteration.
    lo: Ultimate lower limit of the parameter.
    up: Ultimate upper limit of the parameter.
  pl_parm_region:
    name: Region name.
    lum_num: Number of land uses in the region.
    parms: Number of plant parameters used in calibration.
    num_tot: Number of HRUs in the region.
    num: HRU membership list for the region.
    prm: Array of plant parameter calibration records for the region.
  cataloging_units:
    name: Region name.
    area_ha: Total area of the cataloging unit in hectares.
    num_tot: Number of HRUs or member elements in the region.
    num: Explicit member list for the region.
    nlum: Number of land-use and management groups in the region.
    lumc: Land-use group labels.
    lum_num: Database land-use numbers for the region.
    lum_num_tot: Database land-use numbers accumulated over time.
    lum_ha: Land-use area in hectares for the region.
    lum_ha_tot: Accumulated land-use area totals for the region.
    hru_ha: Area of HRUs in the region.
  landscape_units:
    name: Region name.
    area_ha: Area of the landscape cataloging unit in hectares.
    num_tot: Number of HRUs in the region.
    num: Explicit HRU member list for the region.
  landscape_region_elements:
    name: Element name.
    ha: Area of the region element in hectares.
    obj: Object number.
    obtyp: Object type such as hru, hru_lte, lsu, or similar.
    obtypno: Object-type number or first command index for the element.
  landscape_elements:
    name: Element name.
    obj: Object number.
    obtyp: Object type code such as 1 for hru, 2 for hru_lte, or 11 for export coefficient.
    obtypno: Object-type number or first command index for the element.
    bsn_frac: Fraction of the element in the basin expansion.
    ru_frac: Fraction of the element in the routing unit expansion.
    reg_frac: Fraction of the element in the calibration region expansion.
  soft_calib_pl_adjust:
    epco: Plant water-uptake compensation factor (0-1) adjustment or at-limit flag.
    pest_stress: Pest stress adjustment or at-limit flag.
    harv_idx: Harvest index adjustment or at-limit flag.
    lai_pot: Potential leaf-area index adjustment or at-limit flag.
  soft_calib_pl_processes:
    name: Database label for the plant calibration record.
    yield: Crop yield.
    npp: Net primary productivity dry weight.
    lai_mx: Maximum leaf area index.
    wstress: Water stress sum.
    astress: Aeration stress sum.
    tstress: Temperature stress sum.
  pl_calib_regions:
    name: Region or plant-class name.
    plant_no: Crosswalk number from `lum()%name` to `lscal()%lum()%name`.
    ha: Area in hectares for the plant class.
    nbyr: Number of years the plant occurred.
    meas: Measured soft-calibration process values for the plant class.
    precip: Accumulated precipitation used to normalize ratios.
    precip_aa: Average annual precipitation used to normalize ratios.
    precip_aa_sav: Saved average annual precipitation for final output.
    sim: Simulated totals for the plant class.
    aa: Average annual simulated values for the plant class.
    prev: Previous-run simulated values.
    prm: Current plant parameter adjustments.
    prm_prev: Previous plant parameter adjustments.
    prm_lim: At-limit flags for current plant parameter adjustments.
    prm_uplim: Upper-limit adjustment state.
    prm_lowlim: Lower-limit adjustment state.
  soft_data_calib_plant:
    name: Region name.
    lum_num: Number of land uses in the region.
    num_tot: Number of HRUs in the region.
    num: HRU membership list for the region.
    lum: Array of plant calibration records within the region.
  soft_calib_chan_adjust:
    cov: Cover adjustment or at-limit flag.
    erod: Channel erodibility adjustment or at-limit flag.
    shear_bnk: Bank shear coefficient adjustment or at-limit flag.
    hc_erod: Head-cut erodibility adjustment or at-limit flag.
  soft_calib_chan_processes:
    name: Database label for the channel calibration record.
    chw: Channel widening in mm/yr.
    chd: Channel downcutting or accretion in mm/yr.
    hc: Head-cut advance in m/yr.
    fpd: Floodplain accretion in mm/yr.
  chan_calib_regions:
    name: Region or order-class name.
    length: Channel length for the class.
    nbyr: Number of years the class occurred.
    meas: Measured soft-calibration process values for the class.
    sim: Simulated totals for the class.
    aa: Average annual simulated values for the class.
    prev: Previous-run simulated values.
    prm: Current channel parameter adjustments.
    prm_prev: Previous channel parameter adjustments.
    prm_lim: At-limit flags for current channel parameter adjustments.
  soft_data_calib_channel:
    name: Region name.
    ord_num: Number of stream orders in the region.
    num_tot: Number of channels in the region.
    num: Channel membership list for the region.
    ord: Array of channel calibration records by stream order.
type_summaries:
  calibration_parameters: One calibration parameter definition with a name, object type, absolute
    range, and units label.
  calibration_conditions: One condition used to gate an update, identifying the state variable,
    alternate value, numeric target, and comparison code.
  update_parameters: One calibration update request with target name, change type, bounds,
    optional conditions, and explicit member lists.
  update_conditional: One conditional-update scheduling record linking a scenario update table
    to its execution limits and decision-table index.
  soft_calibration_codes: Run-level soft-calibration switches that enable specific hydrologic,
    plant, sediment, nutrient, channel, and reservoir calibration branches.
  soft_calib_parms: One calibration parameter-bound record used by soft calibration routines.
  soft_calib_ls_adjust: Landscape adjustment flags or values for hydrologic calibration variables.
  soft_calib_ls_processes: Soft calibration process totals for a landscape land-use class,
    holding measured, simulated, and averaged hydrologic and sediment quantities.
  ls_calib_regions: One land-use calibration record inside a landscape calibration region,
    storing measured values, simulated totals, averages, and adjustment state for a single
    land-use class.
  soft_data_calib_landscape: One landscape soft-calibration region containing the region name,
    land-use counts, HRU membership, and land-use records.
  pl_parms_cal: One plant calibration parameter record with a variable name, parameter name,
    starting value, change type, and bounds.
  pl_parm_region: One plant calibration region containing a region name, HRU membership, and
    a list of plant parameter records.
  cataloging_units: One cataloging-unit region record describing membership, areas, and land-use
    accounting for basin, channel, aquifer, reservoir, or point-source groupings.
  landscape_units: One landscape output unit describing a group name, area, and explicit member
    list.
  landscape_region_elements: One element entry belonging to a regional landscape list, recording
    the member name, area, object number, and object type.
  landscape_elements: One landscape element record with object identity, object type, and
    basin/RU/region fractions.
  soft_calib_pl_adjust: Plant calibration adjustment flags or values for plant-process variables.
  soft_calib_pl_processes: Soft calibration process totals for a plant class, holding measured,
    simulated, and averaged plant growth variables.
  pl_calib_regions: One plant calibration record inside a plant region, storing measured values,
    simulated totals, averages, and adjustment state for a single plant class.
  soft_data_calib_plant: One plant soft-calibration region containing the region name, land-use
    counts, HRU membership, and plant calibration records.
  soft_calib_chan_adjust: Channel calibration adjustment flags or values for channel-process
    variables.
  soft_calib_chan_processes: Soft calibration process totals for a channel class, holding
    measured, simulated, and averaged channel morphology variables.
  chan_calib_regions: One channel calibration record inside a channel-order region, storing
    measured values, simulated totals, averages, and adjustment state for a single stream-order
    class.
  soft_data_calib_channel: One channel soft-calibration region containing the region name,
    order count, channel membership, and channel calibration records.
---

<!-- facts:header -->

Shared calibration state and record types for SWAT+ soft/hard calibration. This module owns the global calibration parameter tables, conditional update records, soft-calibration flags, regional landscape/channel/aquifer/reservoir/recall membership containers, and the zero-value templates used to reset calibration accumulators. It is populated by calibration readers and setup routines, then consumed by calibration, output, and initialization procedures across the model.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-storage container rather than an executable initializer. It defines the global calibration variables and derived types with default values, while startup and reader routines such as `cal_parm_read`, `cal_parmchg_read`, `calsoft_read_codes`, `lcu_read_softcal`, `lsu_read_elements`, `ch_read_elements`, `aqu_read_elements`, `res_read_elements`, `rec_read_elements`, `pl_read_regions_cal`, and `pl_read_parms_cal` allocate and populate the state.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Uses `cal_codes` and `plcal` during management actions to gate plant-related soft-calibration accumulation and to update regional plant calibration totals when soft calibration is active. |
| [sym:aqu_read_elements] | `aqu_catunit.def, aqu_catunit.ele` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Allocates and fills aquifer region, output, calibration, and element arrays in this module from the aquifer definition files. |
| [sym:basin_aquifer_output] | `unit_2090, unit_2094, unit_2091, unit_2095, unit_2092, unit_2096, unit_2093, unit_2097` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Imports the module but no specific symbol reference was resolved in the extracted source; the routine does not show a direct use of module-owned calibration state in the provided evidence. |
| [sym:basin_ls_pest_output] | `unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Uses `lsu_elem` basin-fraction and object-type mapping while aggregating pesticide outputs to the basin scale. |
| [sym:basin_output] | `unit_2050, unit_2054, unit_2060, unit_2064, unit_2070, unit_2074, unit_2080, unit_2084, unit_2051, unit_2055, unit_2061, unit_2065, unit_2071, unit_2075, unit_2081, unit_2085, unit_2052, unit_2056, unit_2062, unit_2066, unit_2072, unit_2076, unit_2082, unit_2086, unit_2053, unit_2057, unit_2063, unit_2067, unit_2073, unit_2077, unit_2083, unit_2087` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Uses `lsu_elem` to map basin-level HRU and hru_lte contributions and weight them into basin output summaries. |
| [sym:basin_sw_init] | `unit_?` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Uses `lsu_elem` and `lsu_out` to initialize basin and RU soil-water and snow-water outputs from the current HRU and HRU_LTE state. |
| [sym:cal_allo_init] | `setup state and existing model arrays` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Consumes calibration mode state to decide whether calibration allocation and baseline-state initialization should run. |
| [sym:cal_cond_read] | `scen_dtl.upd` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Reads conditional-update definitions into `upd_cond` and resolves each table name to a decision-table index. |
| [sym:cal_parm_read] | `cal_parms.cal` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Reads calibration parameter definitions into `cal_parms` and records the number of loaded entries. |
| [sym:cal_parmchg_read] | `calibration.cal` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Reads calibration update definitions into `cal_upd`, crosswalks target names to `cal_parms`, and expands explicit target element lists. |
| [sym:calsoft_control] | `unit_4999, unit_5001, unit_5000` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Uses `cal_codes`, `region`, `lscal`, `lscalt`, `chcal`, and `ch_prms` to route the active soft-calibration branches and invoke the specific calibration routines. |
| [sym:calsoft_read_codes] | `codes.sft` | `cal_parms, cal_upd, chg, upd_cond, cal_codes, cal_soft` | Reads `cal_codes` from `codes.sft` and sets the global `cal_soft` flag when any soft-calibration mode is active. |

## Key Consumers

This module is shared by the calibration bootstrap, region readers, soft-calibration controllers, basin and landscape output routines, and the calibration-aware initialization/output paths that need the same membership tables and flags.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu_read_elements] | calibration_data_module | Later aquifer output and calibration code can rely on the aquifer membership, region, and element arrays that this routine populated in the shared calibration module. |
| [sym:basin_ls_pest_output] | calibration_data_module | Later basin pesticide output uses the LSU membership and basin-fraction metadata stored in the shared module to map HRU contributions into basin totals. |
| [sym:basin_output] | calibration_data_module | Later basin output uses the LSU-to-HRU/HRU_LTE mapping and basin fractions stored in the shared module to weight daily, monthly, yearly, and average-annual summaries. |
| [sym:basin_sw_init] | calibration_data_module | Later basin water-balance output uses the LSU membership and fraction tables from the shared module to seed basin and RU initial soil-water and snow-water totals. |
| [sym:cal_cond_read] | calibration_data_module | Later conditional-update execution uses the `upd_cond` records populated here to find each update's limit, type, and decision-table index. |
| [sym:cal_parm_read] | calibration_data_module | Later calibration setup and update application use the loaded `cal_parms` table as the shared parameter-definition database. |
| [sym:cal_parmchg_read] | calibration_data_module | Later calibration logic uses the populated `cal_upd` records and explicit target lists to apply parameter changes to the intended model elements. |
| [sym:calsoft_read_codes] | calibration_data_module | Later soft-calibration branches use `cal_codes` and `cal_soft` to decide which calibration modes are active. |
| [sym:ch_read_elements] | calibration_data_module | Later channel calibration and output routines use the channel membership, region, and element tables populated here to map channel regions onto explicit channel and HRU members. |
| [sym:ch_read_orders_cal] | calibration_data_module | Later channel calibration uses the populated `chcal`, `ccu_reg`, `ccu_cal`, and `ccu_elem` tables to evaluate channel-order lengths and member areas. |
| [sym:ch_read_parms_cal] | calibration_data_module | Later channel soft-calibration routines use the `ch_prms` bounds and change definitions loaded here. |
| [sym:header_write] | calibration_data_module | Later output-file setup uses `cal_soft` and `cal_codes` to decide whether calibration output files should be opened and written. |
| [sym:hru_fr_change] | calibration_data_module | Later basin and object-geometry calculations use the updated LSU element fractions stored in the shared module to recompute HRU areas and related routed-object geometry. |
| [sym:lcu_read_softcal] | calibration_data_module | Later landscape calibration routines use the populated `lscal` region records and `region` membership tables to compare simulated and measured hydrologic outputs. |
| [sym:ls_read_lsparms_cal] | calibration_data_module | Later landscape calibration routines use the loaded `ls_prms` bounds and change definitions to adjust hydrologic calibration parameters. |
| [sym:lsreg_output] | calibration_data_module | Later regional output routines use the `region` membership and land-use area tables populated here to aggregate and print region summaries. |
| [sym:lsu_carbon_output] | calibration_data_module | Later LSU carbon output uses the LSU membership and fraction tables from the shared module to area-weight HRU carbon values into LSU summaries. |
| [sym:lsu_output] | calibration_data_module | Later LSU output uses the LSU membership and fraction tables from the shared module to map HRU and HRU_LTE outputs into LSU summaries. |
| [sym:lsu_read_elements] | calibration_data_module | Later landscape and basin output routines use the LSU membership and element metadata that this reader loaded into the shared module. |
| [sym:pl_read_parms_cal] | calibration_data_module | Later plant calibration routines use the populated `pl_prms` region records and HRU memberships to apply plant parameter settings. |
| [sym:pl_read_regions_cal] | calibration_data_module | Later plant calibration routines use the populated `plcal` region records and HRU memberships to compare plant simulation results against calibration targets. |
| [sym:pl_write_parms_cal] | calibration_data_module | Later runs read the written plant parameter file using the `pl_prms` values updated here, with `plcal` providing the soft-calibration adjustments applied to those parameter records. |
| [sym:rec_read_elements] | calibration_data_module | Later recall/output routines use the point-source membership and element metadata populated here to map recall regions onto explicit element numbers and areas. |
| [sym:reg_read_elements] | calibration_data_module | Later regional calibration and output routines use the region and element tables populated here to map landscape regions onto HRUs and LSU fragments. |

## Lineage

`calibration_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `09420df` (2025-02-06, "Added two new real-type variables, `val1` and `val2`, to the `update_parameters`…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `calibration_data_module.f90` are listed.

- `09420df` (2025-02-06) — Added two new real-type variables, `val1` and `val2`, to the `update_parameters` type. These variables represent the lower and upper bounds…
- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `calibration_data_module` has no extracted module-level documentation comment.
- Reader rows are representative rather than exhaustive; the source file is a declaration container and the packet extracted 12 setup/reader routines with direct module-state usage.
- The complete importer appendix is preserved in `all_importers`; the main Used By table highlights a smaller set of representative consumers with source-backed later effects.
- No Git commits were resolved for this source span, so lineage impacts are intentionally empty.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
