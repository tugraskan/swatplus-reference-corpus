---
kind: module
symbol: sd_channel_module
title: sd_channel_module
status: filled
source_hash: a1db21bc2305d2ee
version_label: SWAT+ 62.0.0
variables:
  maxint: integer; maximum number of hydrograph intervals used when building hydrograph-based
    degradation calculations. Declared in `sd_channel_module.f90:5` with initial value 0 and
    used with `timeint`, `hyd_rad`, `trav_time`, and `flo_dep` during `sd_hydsed_read`/`sd_hydsed_init`
    setup.
  wtemp: real; stream water temperature summary value in degrees C. Declared in `sd_channel_module.f90:6`
    with initial value 0. and written by `ch_temp` to support channel daily output; `sd_channel_output`
    appends it to the channel output record.
  peakrate: real; peak runoff rate placeholder shared by channel output and calibration logic.
    Declared in `sd_channel_module.f90:7` with initial value 0.; it is updated by channel/control
    and output routines such as `command`, `sd_channel_control3`, and `sd_ch_output` consumers,
    and it is part of the `sd_ch_output`/channel output state.
  sed_reduc_t: real; shared sediment reduction total initialized to 0. in `sd_channel_module.f90:8`.
    The source file exposes it as module state, but no direct consumer was isolated in the
    provided context; it is part of the shared channel reduction bookkeeping.
  no3_reduc_kg: real; shared nitrate reduction mass in kg initialized to 0. in `sd_channel_module.f90:9`.
    The module provides the state for channel nutrient reduction bookkeeping; no direct consumer
    was isolated in the provided context.
  tp_reduc_kg: real; shared total phosphorus reduction mass in kg initialized to 0. in `sd_channel_module.f90:10`.
    Module-owned reduction bookkeeping state; no direct consumer was isolated in the provided
    context.
  tp_reduc: real; shared total phosphorus reduction ratio or amount initialized to 0. in `sd_channel_module.f90:11`.
    The source gives only the declaration, so the exact downstream use is not explicit in
    the provided context.
  srp_reduc_kg: real; shared soluble reactive phosphorus reduction mass in kg initialized
    to 0. in `sd_channel_module.f90:12`. Module-owned reduction bookkeeping state; no direct
    consumer was isolated in the provided context.
  hyd_rad: allocatable real array; hydraulic radius for each hydrograph time step (`sd_channel_module.f90:13`).
    Allocated by hydrograph setup routines and cleared/filled by `ch_rthr`, `ch_rtmusk`, and
    `sd_hydsed_read` workflows.
  trav_time: allocatable real array; time spent in each hydrograph time step in days (`sd_channel_module.f90:14`).
    Populated by hydrograph setup routines and used by channel routing routines such as `ch_rthr`
    and `ch_rtmusk`.
  flo_dep: allocatable real array; flow depth for each hydrograph time step (`sd_channel_module.f90:15`).
    Populated by hydrograph setup routines and used by channel routing and water-quality routines.
  timeint: allocatable real array; time spent in each hydrograph time step in days (`sd_channel_module.f90:16`).
    Set during hydrograph-reading/setup and used when building hydrograph-based routing state.
  sd_chd: allocatable array of `swatdeg_hydsed_data`; the static channel hydrology/sediment
    parameter table read from `hyd-sed-lte.cha` and related setup files. It stores each channel's
    geometric and sediment properties used by routing, temperature, pesticide, and groundwater
    exchange routines.
  sd_chd1: allocatable array of `swatdeg_sednut_data`; the static channel sediment/nutrient
    parameter table read from `sed_nut.cha` and related setup files. It stores peak-flow,
    floodplain, settling, erosion, and transformation factors used by channel sediment/nutrient
    routines.
  ch_sed_bud: allocatable array of `channel_sediment_budget_output`; per-channel sediment/nutrient
    budget output for each SWAT-DEG channel. Filled, accumulated, and reset by `sd_chanbud_output`,
    `basin_chanbud_output`, and related output workflows.
  ch_sed_bud_m: allocatable array of `channel_sediment_budget_output`; per-channel monthly
    sediment/nutrient budget accumulator. Used by output routines to build month-end summaries.
  ch_sed_bud_y: allocatable array of `channel_sediment_budget_output`; per-channel yearly
    sediment/nutrient budget accumulator. Used by output routines to build year-end summaries.
  ch_sed_bud_a: allocatable array of `channel_sediment_budget_output`; per-channel average-annual
    sediment/nutrient budget accumulator. Used by output routines to build end-of-simulation
    averages.
  ch_sed_budz: channel_sediment_budget_output; zeroed template used to reset channel sediment-budget
    records after accumulation.
  bch_sed_bud_d: channel_sediment_budget_output; basin-wide daily channel sediment budget
    total rebuilt by basin output routines.
  bch_sed_bud_m: channel_sediment_budget_output; basin-wide monthly sediment budget accumulator.
  bch_sed_bud_y: channel_sediment_budget_output; basin-wide yearly sediment budget accumulator.
  bch_sed_bud_a: channel_sediment_budget_output; basin-wide average-annual sediment budget
    accumulator.
  ch_morph: allocatable array of `channel_morphology_output`; per-channel morphology output
    state used by channel morphology reporting and calibration summaries.
  ch_morph_ord: fixed 12-element array of `channel_morphology_output`; channel morphology
    summary by order.
  gully: allocatable array of `gully_data`; per-channel gully/headcut parameter records used
    for channel headcut erosion initialization and routing.
  sd_init: allocatable array of `swatdeg_init_datafiles`; per-channel initialization-file
    pointers that map channel initial-condition inputs such as `initial.cha`, `initial.cha_cs`,
    salt, and constituent files.
  sd_dat: allocatable array of `swatdeg_datafiles`; per-channel data-file crosswalk records
    that name and index the initialization, hydrology, sediment, nutrient, and sediment-nutrient
    input files.
  sd_ch: allocatable array of `swatdeg_channel_dynamic`; the dynamic SWAT-DEG channel state
    for each reach, including geometry, hydraulics, routing coefficients, floodplain parameters,
    groundwater links, and sediment/nutrient parameters.
  sdch_init: allocatable array of `swatdeg_channel_dynamic`; saved initialization copy of
    `sd_ch` used by calibration and reinitialization routines.
  rcurv: channel rating-curve parameter record at the current flow condition. Used as the
    shared interpolated curve state by `rcurv_interp_flo`, `rcurv_interp_dep`, `ch_rtmusk`,
    `ch_rthr`, and water-quality routines.
  rcz: zero rating-curve template used to reset or initialize rating-curve records before
    interpolation or routing.
  ch_rcurv: allocatable array of `channel_rating_curve`; per-channel stored rating curves
    and their depth/flow points used by routing and interpolation routines.
  chsd_d: allocatable array of `sd_ch_output`; per-channel daily morphology/geometry output
    record used by channel output and calibration routines.
  chsd_m: allocatable array of `sd_ch_output`; per-channel monthly morphology/output accumulator.
  chsd_y: allocatable array of `sd_ch_output`; per-channel yearly morphology/output accumulator.
  chsd_a: allocatable array of `sd_ch_output`; per-channel average-annual morphology/output
    accumulator.
  schsd_d: allocatable array of `sd_ch_output`; channel soft-calibration daily summary by
    region.
  schsd_m: allocatable array of `sd_ch_output`; channel soft-calibration monthly summary by
    region.
  schsd_y: allocatable array of `sd_ch_output`; channel soft-calibration yearly summary by
    region.
  schsd_a: allocatable array of `sd_ch_output`; channel soft-calibration average-annual summary
    by region.
  bchsd_d: allocatable array of `sd_ch_output`; basin-wide daily channel morphology total.
  bchsd_m: allocatable array of `sd_ch_output`; basin-wide monthly channel morphology total.
  bchsd_y: allocatable array of `sd_ch_output`; basin-wide yearly channel morphology total.
  bchsd_a: allocatable array of `sd_ch_output`; basin-wide average-annual channel morphology
    total.
  chsdz: '`sd_ch_output` zero template used to reset morphology/output records after accumulation.'
  sdch_hdr: '`sdch_header` record containing the field names for daily and subdaily SWAT-DEG
    channel morphology output.'
  sdch_hdr_units: '`sdch_header_units` record containing the units strings for daily and subdaily
    SWAT-DEG channel morphology output.'
  sdch_bud_hdr: '`sdch_bud` record containing the field names for channel sediment budget
    output.'
  sdch_bud_hdr_units: '`sdch_bud_units` record containing the units strings for channel sediment
    budget output.'
  sdch_hdr_subday: '`sdch_header_sub` record containing the field names for subdaily SWAT-DEG
    channel hydrograph output.'
  sdch_hdr_units_sub: '`sdch_header_units_sub` record containing the units strings for subdaily
    SWAT-DEG channel hydrograph output.'
  sd_chd_hdr: '`sd_chd_header` record containing the field labels for the static channel hydrology/sediment
    parameter table.'
type_components:
  swatdeg_hydsed_data:
    name: channel name or identifier string for the hydrology/sediment table row.
    order: channel order or ranking used with the hydrology/sediment table entry.
    chw: m          |channel width
    chd: m          |channel depth
    chs: m/m        |channel slope
    chl: km         |channel length
    chn: '|channel Manning''s n'
    chk: mm/h       |channel bottom conductivity
    bank_exp: '|bank erosion exponent'
    cov: 0-1        |channel cover factor
    sinu: none       |sinuousity - ratio of channel length and straight line length
    vcr_coef: '|critical velocity coefficient'
    d50: mm         |channel median sediment size
    ch_clay: '%          |clay percent of bank and bed'
    carbon: '%          |carbon percent of bank and bed'
    ch_bd: t/m3       |dry bulk density
    chss: '|channel side slope'
    bankfull_flo: '|bank full flow rate'
    fps: m/m        |flood plain slope
    fpn: '|flood plain Manning''s n'
    n_conc: mg/kg      |nitrogen concentration in channel bank
    p_conc: mg/kg      |phosphorus concentration in channel bank
    p_bio: frac       |fraction of p in bank that is bioavailable
  swatdeg_sednut_data:
    name: channel name or identifier string for the sediment/nutrient table row.
    order: channel order or label string for the sediment/nutrient table entry.
    pk_rto: ratio      |ratio of peak to mean daily flow in channel
    fp_inun_days: days       |number of days fllod plain is inundated after flood
    n_setl: ratio      |ratio of amount of N settling and sediment settling
    p_setl: ratio      |ratio of amount of P settling and sediment settling
    n_sol_part: '|instream nitrogen soluble to particulate transformation coefficient'
    p_sol_part: '|instream phosphorus soluble to particulate transformation coefficient'
    n_dep_enr: '|enrichment of N in remaining water - deposition = 1/enrichment ratio'
    p_dep_enr: '|enrichment of P in remaining water - deposition = 1/enrichment ratio'
    arc_len_fr: frac       |fraction of arc length where bank erosion occurs
    bed_exp: '|bed erosion exponential coefficient'
    wash_bed_fr: frac       |fraction of bank erosion that is washload
  channel_sediment_budget_output:
    in_sed: t          |incoming sediment to channel
    out_sed: t          |outgoing sediment from channel
    fp_dep: t          |flood plain deposition
    ch_dep: t          |channel deposition
    bank_ero: t          |channel bank erosion
    bed_ero: t          |channel bed erosion
    in_no3: t          |incoming no3 to channel
    in_orgn: t          |incoming organic n to channel
    out_no3: t          |outgoing no3 from channel
    out_orgn: t          |outgoing organic n from channel
    fp_no3: t          |flood plain no3 lost
    bank_no3: t          |bank no3 gain
    bed_no3: t          |bed no3 gain
    fp_orgn: t          |flood plain organic n deposited
    ch_orgn: t          |channel organic n deposited
    bank_orgn: t          |bank organic n gain from erosion
    bed_orgn: t          |bed organic n gain from erosion
    in_solp: t          |incoming soluble p to channel
    in_orgp: t          |incoming organic p to channel
    out_solp: t          |outgoing soluble p from channel
    out_orgp: t          |outgoing organic p from channel
    fp_solp: t          |flood plain soluble p lost
    bank_solp: t          |bank no3 gain
    bed_solp: t          |bed no3 gain
    fp_orgp: t          |flood plain organic p deposited
    ch_orgp: t          |channel organic p deposited
    bank_orgp: t          |bank organic p gain from erosion
    bed_orgp: t          |bed organic n gain from erosion
    no3_orgn: t          |in channel transformation from no3 to organic n
    solp_orgp: t          |in channel transformation from no3 to organic n
  channel_morphology_output:
    num: '|number of channels in each order'
    w_yr: ratio      |bank cutting - widths per year
    d_yr: ratio      |bed down cutting - depths per year
    fp_mm: mm/yr      |flood plain deposition - uniform across the flood plain
    ebank_m: tons       |bank cutting
    ebtm_m: m          |bed down cutting
    ebank_t: tons       |bank cutting
    ebtm_t: tons       |bed down cutting
    fp_t: mm/yr      |flood plain deposition
  gully_data:
    name: gully name or identifier.
    hc_kh: '|headcut erodibility'
    hc_hgt: m          |headcut height
    hc_ini: km         |initial channel length for gullies
  swatdeg_init_datafiles:
    init: initial data-points to initial.cha
    org_min: points to initial organic-mineral input file
    pest: points to initial pesticide input file
    path: points to initial pathogen input file
    hmet: points to initial heavy metals input file
    salt: points to initial salt input file (salt_channel.ini) (rtb salt)
    cs: points to initial constituent input file (cs_channel.ini) (rtb cs)
  swatdeg_datafiles:
    name: data bundle name or identifier.
    initc: name or path for initialization/crosswalk file.
    hydc: name or path for hydrology input file.
    sedc: name or path for sediment input file.
    nutc: name or path for nutrient input file.
    init: integer flag or record number for initialization input.
    hyd: integer flag or record number for hydrology input.
    sed: integer flag or record number for sediment input.
    nut: integer flag or record number for nutrient input.
    sednut: integer flag or record number for sediment+nient input.
  floodplain_parameters:
    name: '|name of flood plain'
    obj_tot: '|number of objects (hru and/or ru) in the flood plain'
    hru_tot: '|number of hru in the flood plain'
    ha: ha         |sum of area of all hru in flood plain
    obtyp: object type- 1=hru, 2=hru_lte, 11=export coef, etc
    obtypno: 2-number of hru_lte"s or 1st hru_lte command
    hru: '|flood plain hru number'
    hru_fr: '|hru area fraction of the flood plain'
  muskingum_parameters:
    nsteps: none       |number of daily time steps required for stability
    substeps: none       |number of time substeps required for stability
    c1: Muskingum routing coefficient c1 used in the channel storage update.
    c2: Muskingum routing coefficient c2 used in the channel storage update.
    c3: Muskingum routing coefficient c3 used in the channel storage update.
  swatdeg_channel_dynamic:
    name: channel name or identifier.
    props: integer property flag or object-property index associated with the channel.
    obj_no: object number for the channel reach.
    wallo: water allocation object number
    aqu_link: aquifer the channel is linked to
    aqu_link_ch: sequential channel number in the aquifer
    region: region or group label for the channel reach.
    order: stream order or channel order.
    chw: m          |channel width
    chd: m          |channel depth
    chs: m/m        |channel slope
    chl: km         |channel length
    chn: '|channel Manning''s n'
    chk: mm/h       |channel bottom conductivity
    cov: 0-1        |channel cover factor
    sinu: none       |sinuousity - ratio of channel length and straight line length
    vcr_coef: m/m        |critical velocity coefficient
    d50: median sediment size or grain-size property used by channel routines.
    ch_clay: clay fraction/percent of bank and bed material.
    carbon: organic carbon fraction/percent of bank and bed material.
    ch_bd: dry bulk density of channel bank/bed material.
    chss: channel side slope or sediment-supply side parameter depending on routine context;
      source comment is incomplete.
    bankfull_flo: bankfull flow rate for the reach.
    fps: flood plain slope.
    fpn: flood plain Manning's n.
    n_conc: mg/kg      |nitrogen concentration in channel bank
    p_conc: mg/kg      |phosphorus concentration in channel bank
    p_bio: frac       |fraction of p in bank that is bioavailable
    pk_rto: ratio      |ratio of peak to mean daily flow in channel
    fp_inun_days: days       |number of days fllod plain is inundated after flood
    n_setl: ratio      |ratio of amount of N settling and sediment settling
    p_setl: ratio      |ratio of amount of P settling and sediment settling
    n_sol_part: frac       |instream nitrogen soluble to particulate transformation coefficient
    p_sol_part: frac       |instream phosphorus soluble to particulate transformation coefficient
    n_dep_enr: '|enrichment of N in remaining water - deposition = 1/enrichment ratio'
    p_dep_enr: '|enrichment of P in remaining water - deposition = 1/enrichment ratio'
    arc_len_fr: frac       |fraction of arc length where bank erosion occurs
    bed_exp: mm         |bed erosion exponent
    wash_bed_fr: frac       |fraction of bank erosion that is washload
    hc_kh: headcut erodibility coefficient.
    hc_hgt: m          |headcut height
    hc_ini: initial channel length for gullies/headcut initialization.
    bank_exp: bank erosion exponent.
    shear_bnk: 0-1        |bank shear coefficient - fraction of bottom shear
    hc_erod: headcut erodibility.
    hc_co: m/m        |proportionality coefficient for head cut
    hc_len: m          |length of head cut
    in1_vol: m3         |inflow during previous time step for Muskingum
    out1_vol: m3         |outflow during previous time step for Muskingum
    stor_dis_01bf: hr         |storage time constant at 0.1*bankfull
    stor_dis_bf: hr         |storage time constant at bankfull
    msk: Muskingum routing parameters for the reach.
    fp: Floodplain linkage parameters for the reach.
    kd: aquatic mixing velocity (diffusion/dispersion)-using mol_wt
    aq_mix: m/day     |aquatic mixing velocity (diffusion/dispersion)-using mol_wt
    overbank: '"ib"=in bank; "ob"=overbank flood'
  channel_rating_curve_parameters:
    flo_rate: m^3/s      |flow rate
    xsec_area: m^2        |cross sectional area of flow
    surf_area: m^2        |total surface area
    dep: m          |depth of water
    top_wid: m          |depth of water
    vol: m^3        |total volume of water in reach and flood plain
    vol_fp: m^3        |volume of water in flood plain
    vol_ch: m^3        |volume of water in and above channel
    wet_perim: m          |wetted perimeter
    ttime: hr         |travel time
  channel_rating_curve:
    npts: none       |number of points on the rating curve
    wid_btm: m          |bottom width of main channel
    in1: 'elev - 1=.1 bf dep; 2=bf dep; 3=1.2*bf dep; 4=2*bf dep

      rating curve - inflow previous time step'
    in2: rating curve - inflow current time step
    out1: rating curve - outflow previous time step
    out2: rating curve - outflow current time step
    elev: rating curve at each depth
  sd_ch_output:
    flo_in: (m^3/s)       |average daily inflow rate during time step
    aqu_in: (m^3/s)       |geomorphic aquifer flow into channel/aquifer inflow using geomorphic
      baseflow method
    flo: (m^3/s)       |average daily outflow rate during timestep
    peakr: (m^3/s)       |average peak runoff rate during timestep
    sed_in: (tons)        |sediment in
    sed_out: (tons)        |sediment out
    washld: (tons)        |wash load (suspended) out
    bedld: (tons)        |bed load out
    dep: (tons)        |deposition in channel and flood plain
    deg_btm: (tons)        |erosion of channel bottom
    deg_bank: (tons)        |erosion of channel bank
    hc_sed: (tons)        |erosion from gully head cut
    width: m             |channel bank full top width at end of time step
    depth: m             |channel bank full depth at end of time step
    slope: m/m           |channel slope
    deg_btm_m: (m)           !downcutting of channel bottom
    deg_bank_m: (m)           |widening of channel banks
    hc_m: (m)           |headcut retreat
    flo_in_mm: (mm)          |inflow rate total sum for each time step
    aqu_in_mm: (mm)          |aquifer inflow rate total sum for each time step
    flo_mm: (mm)          |outflow rate total sum for each time step
    sed_stor: (tons)        |sed storage at end of timestep
    n_tot: (kg N)        |total nitrogen leaving the reach
    p_tot: (kg N)        |total phosphorus leaving the reach
    dep_bf: m             |depth of water when reach is at bankfull depth
    velav_bf: m/s           |average velocity when reach is at bankfull depth
  sdch_header:
    day: day column label.
    mo: month column label.
    day_mo: day-of-month label.
    yrc: year column label.
    isd: unit index label.
    id: GIS id label.
    name: name column label.
    flo_in: (m^3/s)
    aqu_in: (m^3/s)
    flo: (m^3/s)
    peakr: (m^3/s)
    sed_in: (tons)
    sed_out: (tons)
    washld: (tons)
    bedld: (tons)
    dep: (tons)
    deg_btm: (tons)
    deg_bank: (tons)
    hc_sed: (tons)
    width: (m)
    depth: (m)
    slope: (m/m)
    deg_btm_m: (m)
    deg_bank_m: (m)
    hc_len: (m)
    flo_in_mm: (mm)
    aqu_in_mm: (mm)
    flo_mm: (mm)
    sed_stor: (tons)
    n_tot: (kg_N)
    p_tot: (kg_N)
    dep_bf: (m/s)
    velav_bf: (m/s)
  sdch_header_units:
    day: date field separator placeholder.
    mo: date field separator placeholder.
    day_mo: date field separator placeholder.
    yrc: date field separator placeholder.
    isd: unit field placeholder.
    id: gis id field placeholder.
    name: name field placeholder.
    flo_in: (m^3/s)
    aqu_in: (m^3/s)
    flo: (m^3/s)
    peakr: (m^3/s)
    sed_in: (tons)
    sed_out: (tons)
    washld: (tons)
    bedld: (tons)
    dep: (tons)
    deg_btm: (tons)
    deg_bank: (tons)
    hc_sed: (tons)
    width: (m)
    depth: (m)
    slope: (m/m)
    deg_btm_m: (m)
    deg_bank_m: (m)
    hc_len: (m)
    flo_in_mm: (mm)
    aqu_in_mm: (mm)
    flo_mm: (mm)
    sed_stor: (tons)
    n_tot: (kg_N)
    p_tot: (kg_P)
    dep_bf: (m/s)
    velav_bf: (m/s)
  sdch_bud:
    day: day column label.
    mo: month column label.
    day_mo: day-of-month label.
    yrc: year column label.
    isd: unit index label.
    id: GIS id label.
    name: name column label.
    in_sed: (tons)
    out_sed: (tons)
    fp_dep: (tons)
    ch_dep: (tons)
    bank_ero: (tons)
    bed_ero: (tons)
    in_no3: (tons)
    in_orgn: (tons)
    out_no3: (tons)
    out_orgn: (tons)
    fp_no3: (tons)
    bank_no3: (tons)
    bed_no3: (tons)
    fp_orgn: (tons)
    ch_orgn: (tons)
    bank_orgn: (tons)
    bed_orgn: (tons)
    in_solp: (tons)
    in_orgp: (tons)
    out_solp: (tons)
    out_orgp: (tons)
    fp_solp: (tons)
    bank_solp: (tons)
    bed_solp: (tons)
    fp_orgp: (tons)
    ch_orgp: (tons)
    bank_orgp: (tons)
    bed_orgp: (tons)
    no3_orgn: (tons)
    solp_orgp: (tons)
  sdch_bud_units:
    day: date field separator placeholder.
    mo: date field separator placeholder.
    day_mo: date field separator placeholder.
    yrc: date field separator placeholder.
    isd: unit field placeholder.
    id: gis id field placeholder.
    name: name field placeholder.
    in_sed: (tons)
    out_sed: (tons)
    fp_dep: (tons)
    ch_dep: (tons)
    bank_ero: (tons)
    bed_ero: (tons)
    in_no3: (tons)
    in_orgn: (tons)
    out_no3: (tons)
    out_orgn: (tons)
    fp_no3: (tons)
    bank_no3: (tons)
    bed_no3: (tons)
    fp_orgn: (tons)
    ch_orgn: (tons)
    bank_orgn: (tons)
    bed_orgn: (tons)
    in_solp: (tons)
    in_orgp: (tons)
    out_solp: (tons)
    out_orgp: (tons)
    fp_solp: (tons)
    bank_solp: (tons)
    bed_solp: (tons)
    fp_orgp: (tons)
    ch_orgp: (tons)
    bank_orgp: (tons)
    bed_orgp: (tons)
    no3_orgp: (tons)
    solp_orgp: (tons)
  sdch_header_sub:
    day: day column label.
    mo: month column label.
    day_mo: day-of-month label.
    yrc: year column label.
    isd: unit index label.
    id: GIS id label.
    ii: subdaily timestep label.
    name: name column label.
    hyd_flo: (m^3/s)
  sdch_header_units_sub:
    day: date field separator placeholder.
    mo: date field separator placeholder.
    day_mo: date field separator placeholder.
    yrc: date field separator placeholder.
    isd: unit field placeholder.
    id: gis id field placeholder.
    ii: subdaily timestep field placeholder.
    name: name field placeholder.
    hyd_flo: (m^3/s)
  sd_chd_header:
    name: channel name label.
    order: channel order label.
    chw: m          |channel width
    chd: m          |channel depth
    chs: m/m        |channel slope
    chl: m          |channel length
    chn: '|channel Manning''s n'
    chk: mm/h       |channel bottom conductivity
    cherod: '|channel erodibility'
    cov: 0-1        |channel cover factor
    sinu: '|sinuousity - ratio of channel length and straight line length'
    chseq: m/m        |equilibrium channel slope
    d50: '|median particle size'
    ch_clay: '%          |clay percent of bank and bed'
    carbon: '%          |carbon percent of bank and bed'
    ch_bd: g/cm^3     |channel bank density
    chss: '|channel sediment supply'
    bankfull_flo: m^3/s |bankfull flow
    fps: '|flood plain slope'
    fpn: '|flood plain Manning''s n'
    n_conc: mg/kg      |nitrogen concentration in channel bank
    p_conc: mg/kg      |phosphorus concentration in channel bank
    p_bio: frac       |fraction of p in bank that is bioavailable
type_summaries:
  swatdeg_hydsed_data: Static hydrology/sediment property record for one SWAT-DEG channel
    reach.
  swatdeg_sednut_data: Static sediment and nutrient control record for one SWAT-DEG channel
    reach.
  channel_sediment_budget_output: Per-channel sediment and nutrient budget output record.
  channel_morphology_output: Per-channel channel-morphology summary record.
  gully_data: Gully/headcut initialization record used by channel erosion routines.
  swatdeg_init_datafiles: Pointers/flags for SWAT-DEG channel initialization files.
  swatdeg_datafiles: Crosswalk record naming the input files used to initialize one SWAT-DEG
    channel data bundle.
  floodplain_parameters: Floodplain linkage list for a channel reach.
  muskingum_parameters: Muskingum routing coefficients and step-count control.
  swatdeg_channel_dynamic: Dynamic per-reach SWAT-DEG channel state used by routing, sediment,
    groundwater exchange, and calibration.
  channel_rating_curve_parameters: Hydraulic geometry values at one rating-curve point.
  channel_rating_curve: Four-point channel rating curve with inflow/outflow points.
  sd_ch_output: Per-channel daily, monthly, yearly, or average-annual channel output record.
  sdch_header: Column labels for daily/summary SWAT-DEG channel output files.
  sdch_header_units: Units row for daily/summary SWAT-DEG channel output files.
  sdch_bud: Column labels for channel sediment budget output files.
  sdch_bud_units: Units row for channel sediment budget output files.
  sdch_header_sub: Subdaily channel hydrograph header labels.
  sdch_header_units_sub: Units row for subdaily channel hydrograph output.
  sd_chd_header: Column labels for the static SWAT-DEG channel hydrology/sediment table.
---

<!-- facts:header -->

`sd_channel_module` owns the shared SWAT-DEG channel state, lookup tables, output accumulators, header records, and channel-related derived types used by channel routing, sediment, nutrient, temperature, groundwater exchange, calibration, and output setup routines. The module is populated by initialization/readers such as `ch_read_init`, `ch_read_init_cs`, `sd_channel_read`, `sd_hydsed_read`, and `sd_hydsed_init`, and then consumed by routing, calibration, and reporting procedures throughout the model.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-state container. It does not define startup subroutines itself, but its variables are populated by readers and setup routines such as `ch_read_init`, `ch_read_init_cs`, `sd_channel_read`, `sd_hydsed_read`, `sd_hydsed_init`, `header_sd_channel`, `header_write`, `cal_allo_init`, and `re_initialize`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `maxint, wtemp, peakrate, sed_reduc_t, no3_reduc_kg, tp_reduc_kg` | Updates channel state during action execution; `actions` writes into `sd_ch` for calibration-related channel changes and consumes channel output/state as part of management operations. |
| [sym:aqu2d_init] | `aquifer-channel linkage setup from channel and aquifer topology` | `sd_ch, sd_chd` | Initializes aquifer linkage metadata on channel records and reads channel lengths from the hyd-sed table so geomorphic baseflow routing has the correct cross-reference state. |
| [sym:basin_chanbud_output] | `unit_2128, unit_2132, unit_2129, unit_2133, unit_2130, unit_2134, unit_2131, unit_2135` | `ch_sed_bud, bch_sed_bud_d, bch_sed_bud_m, bch_sed_bud_y, bch_sed_bud_a` | Aggregates per-channel sediment budgets into basin totals and writes the daily, monthly, yearly, and average-annual channel budget outputs. |
| [sym:basin_chanmorph_output] | `unit_2120, unit_2124, unit_2121, unit_2125, unit_2122, unit_2126, unit_2123, unit_2127` | `chsd_d, bchsd_d, bchsd_m, bchsd_y, bchsd_a` | Aggregates per-channel morphology outputs into basin totals and writes the daily, monthly, yearly, and average-annual channel morphology outputs. |
| [sym:cal_allo_init] | `calibration initialization state` | `sd_ch, sdch_init` | Copies the active `sd_ch` channel dynamic state into `sdch_init` so calibration can start from a preserved baseline channel condition. |
| [sym:cal_parm_select] | `calibration change request state` | `sd_ch` | Applies calibration changes directly to channel geometry and sediment/nutrient parameters stored in `sd_ch`. |
| [sym:calsoft_control] | `unit_4999, unit_5001, unit_5000` | `channel calibration state` | Controls soft-calibration workflow that later reads channel calibration state from this module. |
| [sym:calsoft_read_codes] | `codes.sft` | `calibration flags` | Reads the soft-calibration flag file and prepares channel-related soft-calibration flags that downstream routines inspect. |
| [sym:caltsoft_hyd] | `unit_4304` | `hydrologic calibration state` | Uses the shared calibration environment that includes channel-related state, although the extracted snippet does not isolate a direct channel symbol. |
| [sym:ch_read_elements] | `ch_catunit.def, ch_reg.def, element.ccu` | `schsd_d, schsd_m, schsd_y, schsd_a` | Allocates region-level channel soft-calibration output arrays and loads channel cataloging-unit and region definitions. |
| [sym:ch_read_init] | `initial.cha` | `sd_init` | Reads the channel initial-condition file and populates the shared `sd_init` initialization-file pointer array alongside `ch_init`. |
| [sym:ch_read_init_cs] | `initial.cha_cs` | `channel constituent initialization state` | Reads channel constituent initial conditions for the salt/constituent pathway; the provided snippet does not isolate a specific `sd_channel_module` symbol. |
| [sym:calsoft_sum_output] | `year-end calibration aggregation state` | `sd_ch, chsd_y` | Uses channel lengths and yearly channel morphology outputs to compute regional/channel calibration summaries. |
| [sym:header_sd_channel] | `output header setup` | `sdch_hdr_subday, sdch_hdr_units_sub, sdch_hdr, sdch_hdr_units, sdch_bud_hdr, sdch_bud_hdr_units` | Serializes the module-defined SWAT-DEG channel header and units records into the channel output files. |
| [sym:header_write] | `basin output setup` | `sdch_hdr, sdch_hdr_units, sdch_bud_hdr, sdch_bud_hdr_units` | Uses the SWAT-DEG channel header structures to initialize basin channel output files with correct labels and units. |
| [sym:overbank_read] | `chan-surf.lin` | `sd_ch` | Loads floodplain surface-linkage data into each channel's `fp` block so overbank relationships are available to routing and exchange routines. |
| [sym:sd_chanbud_output] | `daily/monthly/yearly/output scheduling state` | `ch_sed_bud, ch_sed_bud_m, ch_sed_bud_y, ch_sed_bud_a, ch_sed_budz` | Writes and resets per-channel sediment budget outputs on the configured print intervals. |
| [sym:sd_chanmorph_output] | `daily/monthly/yearly/output scheduling state` | `chsd_d, chsd_m, chsd_y, chsd_a, chsdz` | Writes and resets per-channel morphology outputs on the configured print intervals. |
| [sym:sd_channel_output] | `channel daily output state` | `wtemp` | Appends stream water temperature to the daily channel output record as one of the reported diagnostics. |
| [sym:sd_channel_read] | `channel-lte.cha and related channel initialization files` | `gully, sd_ch, ch_morph, ch_sed_bud, ch_sed_bud_m, ch_sed_bud_y, ch_sed_bud_a, ch_rcurv, chsd_d, chsd_m, chsd_y, chsd_a, sd_dat, sd_init, sd_chd, sd_chd1` | Reads SWAT-DEG channel configuration and initialization data, allocates channel dynamic/output arrays, and fills the shared static tables and initialization pointers. |
| [sym:sd_hydsed_init] | `channel hyd-sed and rating-curve setup` | `sd_dat, sd_ch, sd_chd, gully, sd_chd1, rcurv, sd_init, ch_rcurv` | Copies hyd-sed data into channel dynamic state, initializes rating curves and zeroed channel storage, and prepares channel sediment/nutrient state for simulation. |
| [sym:sd_hydsed_read] | `hyd-sed-lte.cha, sed_nut.cha` | `maxint, timeint, hyd_rad, trav_time, flo_dep, sd_chd, sd_chd1` | Reads the static hyd-sed and sediment/nutrient tables and prepares the hydrograph arrays used by channel routing setup. |
| [sym:swift_output] | `SWIFT/channel output file generation` | `sd_dat, sd_chd, sd_chd_hdr` | Uses the channel data-file mapping and header labels to write SWIFT channel data files. |

## Key Consumers

The main consumers are channel routing, sediment/nutrient processing, groundwater exchange, calibration, and output routines. The module also supports header writers and input readers that prepare or serialize SWAT-DEG channel state.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu2d_init] | sd_channel_module | Initializes aquifer linkage metadata on each SWAT-DEG channel record and reads the channel length from the hyd-sed data table so geomorphic baseflow routing can compute linked lengths and remaining length. |
| [sym:basin_chanbud_output] | sd_channel_module | Provides the per-channel sediment budget records and basin-level accumulators that are summed, written, and reset for daily, monthly, yearly, and average-annual basin reporting. |
| [sym:basin_chanmorph_output] | sd_channel_module | Provides the per-channel morphology records and basin-level accumulators that are summed, written, and reset for daily, monthly, yearly, and average-annual basin morphology reporting. |
| [sym:cal_allo_init] | sd_channel_module | Supplies the channel dynamic arrays that are copied into `sdch_init` so calibration starts from a preserved baseline channel condition. |
| [sym:cal_parm_select] | sd_channel_module | Supplies the channel dynamic state that receives calibration edits to geometry, sediment, and nutrient parameters for the selected channel element. |
| [sym:ch_read_elements] | sd_channel_module | Supplies the channel soft-calibration output arrays that are allocated per region so channel region membership can be written into daily, monthly, yearly, and average-annual summaries. |
| [sym:ch_read_init] | sd_channel_module | Supplies the allocatable `sd_init` array that is sized alongside `ch_init` so channel initialization data can be stored in parallel with the general channel initialization records. |
| [sym:ch_read_orders_cal] | sd_channel_module | Provides `sd_ch(ich)%chl`, which this routine sums to build total channel length for each calibration region/order entry. |
| [sym:header_sd_channel] | sd_channel_module | Supplies the SWAT-DEG channel header and units records that are written directly into the subdaily, daily, and budget output files. |
| [sym:header_write] | sd_channel_module | Supplies the SWAT-DEG channel morphology and budget header structures used to seed the basin channel output files with the correct labels and units. |
| [sym:overbank_read] | sd_channel_module | Provides the `sd_ch` channel objects whose floodplain parameter blocks are filled with surface type and object-number lists for overbank linkage. |
| [sym:sd_chanbud_output] | sd_channel_module | Provides the per-channel sediment budget state and zero template used to accumulate, write, and reset channel sediment budget outputs. |
| [sym:sd_chanmorph_output] | sd_channel_module | Provides the per-channel morphology state and zero template used to accumulate, write, and reset channel morphology outputs. |
| [sym:sd_channel_output] | sd_channel_module | Provides `wtemp`, the stream water temperature value appended to each daily channel output record. |
| [sym:sd_channel_read] | sd_channel_module | Owns the SWAT-DEG channel dynamic state, output arrays, and initialization pointers that are filled when channel configuration and initial-condition files are read. |
| [sym:sd_hydsed_init] | sd_channel_module | Provides the static channel tables and dynamic reach state that are copied and initialized for hydrology/sediment routing setup. |
| [sym:sd_hydsed_read] | sd_channel_module | Provides the hydrograph-based arrays and parsed hyd-sed tables used to initialize channel routing calculations. |
| [sym:swift_output] | sd_channel_module | Provides the channel data-file mapping and channel parameter table used to generate the SWIFT channel data file. |
| [sym:wallo_control] | sd_channel_module | Provides the channel-state objects updated by water-allocation transfers so demand, withdrawal, transfer, and receiving-object bookkeeping can be applied to channel-related allocations. |
| [sym:wet_fp_init] | sd_channel_module | Provides the per-reach floodplain metadata used to determine whether a reach has HRUs in its floodplain and how many to sum. |
| [sym:calsoft_read_codes] | sd_channel_module | Supplies the channel soft-calibration context that the loaded flags govern, especially channel sediment and nutrient calibration mode selection. |
| [sym:ch_read_init_cs] | sd_channel_module | Provides the channel-state context for the salt/constituent initialization pathway, although the extracted snippet does not isolate a specific symbol reference. |
| [sym:cs_cha_read] | sd_channel_module | Provides the channel-domain context that channel constituent initial concentrations must be consistent with, even though no direct symbol reference appears in the extracted lines. |
| [sym:gwflow_output_init] | sd_channel_module | No direct symbol reference from this module is resolved in the provided snippet, so its role in groundwater output initialization is uncertain from the available evidence. |

## Lineage

`sd_channel_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `23142ed` (2025-10-29, "Water allocation now has explicit structured output objects and headers, with pe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `sd_channel_module.f90` are listed.

- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `10e5ddc` (2025-08-27) — 08272025 updates
- `889136d` (2025-02-03) — Fix typos
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `7a9273b` (2024-08-21) — 08202024 updates sd_channel_control3 : - Updated nutrient transformation logic to ensure accurate updates to organic nitrogen and phosphorus…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `sd_channel_module` has no extracted module-level documentation comment.
- Reader entries are representative of the broader initialization/read surface; the module has many more importers and setup points than the reader table lists explicitly.
- The provided lineage section reported no resolved commits for this source span, so `lineage_impacts` remains empty.
- A few component comments in the source are terse or incomplete; where the file does not state ownership or units clearly, the overlay keeps the wording conservative.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
