---
kind: module
symbol: hydrograph_module
title: hydrograph_module
status: filled
source_hash: 5ffcd5475d77732a
version_label: SWAT+ 62.0.0
variables:
  mhyd: Integer scalar holding none.
  mcmd: Integer scalar — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  inum2: Integer scalar holding none.
  jrch: Integer scalar holding none.
  jrchq: Integer scalar — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  mrte: Integer scalar — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  ihout: Integer scalar holding none.
  iwst: Integer scalar — a module-level working variable holding an index/counter (no inline
    source comment; interpreted from the name).
  isdch: Integer scalar — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  icmd: Integer scalar — a module-level working variable holding an index/counter (no inline
    source comment; interpreted from the name).
  ich: Integer scalar holding none.
  mobj_out: Integer scalar holding none.
  isd_chsur: Integer scalar — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  rcv_sum: Integer allocatable 1-D array — a module-level working variable holding a running
    sum (no inline source comment; interpreted from the name).
  dfn_sum: Integer allocatable 1-D array — a module-level working variable holding a running
    sum (no inline source comment; interpreted from the name).
  elem_cnt: Integer allocatable 1-D array — a module-level working variable holding a count
    (no inline source comment; interpreted from the name).
  defunit_num: Integer allocatable 1-D array — a module-level working variable holding a count
    (no inline source comment; interpreted from the name).
  ru_seq: Integer allocatable 1-D array — a module-level working variable shared across the
    importing routines (no inline source comment in the declaration).
  hyd_km2: Real allocatable 1-D array — a module-level working variable shared across the
    importing routines (no inline source comment in the declaration).
  ob_order: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  rchhr: Real allocatable 3-D array — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  wyld_rto: Real scalar holding mm=m3/(10*ha).
  hd: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  rec_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily values.
  rec_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  rec_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly values.
  rec_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  srec_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily values.
  srec_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  srec_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly
    values.
  srec_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  ru_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily values.
  ru_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly values.
  ru_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly values.
  ru_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  brec_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  brec_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  brec_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  brec_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  bru_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  bru_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  bru_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  bru_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  binhyd_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  hz: Variable of `hyd_output` — see the `hyd_output` type.
  dr1: Variable of `hyd_output` — see the `hyd_output` type.
  hcnst: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  hhr: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  ht1: Variable of `hyd_output` — see the `hyd_output` type.
  ht2: Variable of `hyd_output` — see the `hyd_output` type.
  ht3: Variable of `hyd_output` — see the `hyd_output` type.
  ht4: Variable of `hyd_output` — see the `hyd_output` type.
  ht5: Variable of `hyd_output` — see the `hyd_output` type.
  delrto: Variable of `hyd_output` — see the `hyd_output` type.
  fp_dep: Variable of `hyd_output` — see the `hyd_output` type.
  ch_dep: Variable of `hyd_output` — see the `hyd_output` type.
  bank_ero: Variable of `hyd_output` — see the `hyd_output` type.
  bed_ero: Variable of `hyd_output` — see the `hyd_output` type.
  ch_trans: Variable of `hyd_output` — see the `hyd_output` type.
  hdsep1: Variable of `hyd_sep` — rtb hydrograph separation.
  hdsep2: Variable of `hyd_sep` — rtb hydrograph separation.
  ch_stor_hdsep: Allocatable 1-D array of `hyd_sep` — see the `hyd_sep` type.
  hyd_sep_array: Real allocatable 2-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  om_init_name: Character allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  aqu: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  res: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wet: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  res_om_init: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wet_om_init: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wet_seep_day: Allocatable 1-D array of `hyd_output` — Jaehak 2022 wetland seepage volume.
  resz: Variable of `hyd_output` — see the `hyd_output` type.
  wbody: Pointer of `hyd_output` — used for reservoir and wetlands.
  om_init_water: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  ch_om_water_init: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  fp_om_water_init: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  ch_stor: Allocatable 1-D array of `hyd_output` — channel storage - max bankfull.
  fp_stor: Allocatable 1-D array of `hyd_output` — flood plain storage above wetland emergency.
  tot_stor: Allocatable 1-D array of `hyd_output` — total - channel + flood plain storage.
  wet_stor: Allocatable 1-D array of `hyd_output` — wetland storage in flood plain.
  ch_stor_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  ch_stor_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly
    values.
  ch_stor_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  chaz: Variable of `hyd_output` — see the `hyd_output` type.
  res_in_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily
    values.
  res_in_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  res_in_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly
    values.
  res_in_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  res_trap: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  bres_in_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  bres_in_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  bres_in_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  bres_in_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  res_out_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily
    values.
  res_out_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  res_out_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly
    values.
  res_out_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  bres: Variable of `hyd_output` — see the `hyd_output` type.
  bres_out_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  bres_out_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  bres_out_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  bres_out_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  resmz: Variable of `hyd_output` — see the `hyd_output` type.
  wet_in_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily
    values.
  wet_in_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  wet_in_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly
    values.
  wet_in_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  bwet_in_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  bwet_in_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  bwet_in_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  bwet_in_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  wet_out_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily
    values.
  wet_out_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  wet_out_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly
    values.
  wet_out_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  bwet_out_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  bwet_out_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  bwet_out_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  bwet_out_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  ch_in_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily
    values.
  ch_in_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  ch_in_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly
    values.
  ch_in_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  bch_stor_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  bch_stor_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  bch_stor_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  bch_stor_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  bch_in_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  bch_in_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  bch_in_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  bch_in_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  ch_out_d: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds daily
    values.
  ch_out_m: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds monthly
    values.
  ch_out_y: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds yearly
    values.
  ch_out_a: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type; holds average-annual
    values.
  bch_out_d: Variable of `hyd_output` — see the `hyd_output` type; holds daily values.
  bch_out_m: Variable of `hyd_output` — see the `hyd_output` type; holds monthly values.
  bch_out_y: Variable of `hyd_output` — see the `hyd_output` type; holds yearly values.
  bch_out_a: Variable of `hyd_output` — see the `hyd_output` type; holds average-annual values.
  chomz: Variable of `hyd_output` — see the `hyd_output` type.
  wal_omd: Allocatable 1-D array of `water_allocation_object` — see the `water_allocation_object`
    type.
  wal_omm: Allocatable 1-D array of `water_allocation_object` — see the `water_allocation_object`
    type.
  wal_omy: Allocatable 1-D array of `water_allocation_object` — see the `water_allocation_object`
    type.
  wal_oma: Allocatable 1-D array of `water_allocation_object` — see the `water_allocation_object`
    type.
  wdraw_om: Variable of `hyd_output` — water withdrawn from an individual source.
  wdraw_om_tot: Variable of `hyd_output` — total water withdrawn from all sources.
  outflo_om: Variable of `hyd_output` — outflow from an water allocation object - wtp or use.
  wtp_om_stor: Allocatable 1-D array of `hyd_output` — water treatment plant storage and outflow.
  wtp_om_out: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wtp_om_treat: Allocatable 1-D array of `hyd_output` — water treatment plant treated concentrations
    - input.
  wal_tr_omd: Allocatable 1-D array of `hyd_output` — amount of organic-mineral removed by
    treatment plants.
  wal_tr_omm: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wal_tr_omy: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wal_tr_oma: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wal_use_omd: Allocatable 1-D array of `hyd_output` — amount of organic-mineral added by
    uses.
  wal_use_omm: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wal_use_omy: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wal_use_oma: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wuse_om_stor: Allocatable 1-D array of `hyd_output` — water use storage and outflow.
  wuse_om_out: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wuse_om_efflu: Allocatable 1-D array of `hyd_output` — water use effluent concentrations
    - input.
  osrc_om: Allocatable 1-D array of `hyd_output` — outside source outflow.
  orcv_om: Allocatable 1-D array of `hyd_output` — outside receiving inflow.
  canal_om_stor: Allocatable 1-D array of `hyd_output` — canal storage and outflow.
  canal_om_out: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  wtow_om_stor: Allocatable 1-D array of `hyd_output` — water tower storage and outflow.
  wtow_om_out: Allocatable 1-D array of `hyd_output` — see the `hyd_output` type.
  ob_out: Allocatable 1-D array of `object_output` — see the `object_output` type.
  ch_fp_wb: Allocatable 1-D array of `channel_floodplain_water_balance` — see the `channel_floodplain_water_balance`
    type.
  ts: Allocatable 1-D array of `timestep` — see the `timestep` type.
  fdc_npts: Integer scalar — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  fdc_p: Real 1-D array holding percent.
  fdc_days: Integer 1-D array — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  fdc_n: Real 1-D array — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  fdc_norm_mean: Real 1-D array — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  ob: Allocatable 1-D array of `object_connectivity` — see the `object_connectivity` type.
  irrig: Allocatable 1-D array of `irrigation_water_transfer` — dimension by hru.
  recall: Allocatable 1-D array of `recall_hydrograph_inputs` — see the `recall_hydrograph_inputs`
    type.
  sp_ob: Variable of `spatial_objects` — total number of the object.
  sp_ob1: Variable of `spatial_objects` — first sequential number of the object.
  hd_tot: Variable of `object_total_hydrographs` — see the `object_total_hydrographs` type.
  ru_def: Allocatable 1-D array of `routing_unit_data` — see the `routing_unit_data` type.
  ru_elem: Allocatable 1-D array of `routing_unit_elements` — see the `routing_unit_elements`
    type.
  ielem_ru: Integer allocatable 1-D array holding sequential counter for ru the hru is in.
  ch_sur: Allocatable 1-D array of `channel_surface_elements` — see the `channel_surface_elements`
    type.
  aqu_cha: Allocatable 1-D array of `geomorphic_baseflow_channel_data` — unsorted.
  aq_ch: Allocatable 1-D array of `channel_aquifer_elements` — sorted by drainage area (smallest
    first).
  dr: Allocatable 1-D array of `hyd_output` — delivery ratio - all fractions delivery ratio
    for objects- chan, res, lu.
  exco: Allocatable 1-D array of `hyd_output` — export coefficient - m3, t, kg export coefficient.
  hyd_hdr: Variable of `hyd_header` — see the `hyd_header` type.
  hyd_stor_hdr: Variable of `hyd_stor_header` — see the `hyd_stor_header` type.
  hyd_in_hdr: Variable of `hyd_in_header` — see the `hyd_in_header` type.
  hyd_out_hdr: Variable of `hyd_out_header` — see the `hyd_out_header` type.
  hyd_inout_hdr: Variable of `hyd_inout_header` — see the `hyd_inout_header` type.
  wtmp_hdr: Variable of `wtmp_out_header` — see the `wtmp_out_header` type.
  sd_hyd_hdr: Variable of `sed_hyd_header` — see the `sed_hyd_header` type.
  sd_hyd_hdr_units: Variable of `sd_hyd_header_units` — see the `sd_hyd_header_units` type.
  sol_hdr: Variable of `sol_header` — see the `sol_header` type.
  plt_hdr: Variable of `plant_header` — see the `plant_header` type.
  fp_hdr: Variable of `flood_plain_header` — see the `flood_plain_header` type.
  ch_wbod_hdr: Variable of `ch_watbod_header` — see the `ch_watbod_header` type.
  ch_wbod_hdr_units: Variable of `ch_watbod_header_units` — see the `ch_watbod_header_units`
    type.
  ch_wbod_inouthdr: Variable of `ch_watbod_inoutheader` — see the `ch_watbod_inoutheader`
    type.
  ch_wbod_inouthdr_units: Variable of `ch_watbod_inoutheader_units` — see the `ch_watbod_inoutheader_units`
    type.
  hyd_hdr_units1: Variable of `hyd_header_units1` — see the `hyd_header_units1` type.
  hyd_hdr_units3: Variable of `hyd_header_units3` — see the `hyd_header_units3` type.
  hydinout_hdr_units1: Variable of `hydinout_header_units1` — see the `hydinout_header_units1`
    type.
  wtmp_units: Variable of `wtmp_header_units` — see the `wtmp_header_units` type.
  hyd_hdr_units: Variable of `hyd_header_units` — see the `hyd_header_units` type.
  hyd_hdr_units2: Variable of `hyd_header_units2` — see the `hyd_header_units2` type.
  hyd_hdr_time: Variable of `hyd_header_time` — see the `hyd_header_time` type.
  rec_hdr_time: Variable of `rec_header_time` — see the `rec_header_time` type.
  hyd_hdr_obj: Variable of `hyd_header_obj` — see the `hyd_header_obj` type.
  fdc_hdr: Variable of `output_flow_duration_header` — see the `output_flow_duration_header`
    type.
  calb_hdr: Variable of `calibration_header` — see the `calibration_header` type.
  calb2_hdr: Variable of `calibration2_header` — see the `calibration2_header` type.
  calb3_hdr: Variable of `calibration3_header` — see the `calibration3_header` type.
  chk_hdr: Variable of `output_checker_header` — see the `output_checker_header` type.
  chk_unit: Variable of `output_checker_unit` — see the `output_checker_unit` type.
  hru_swift_hdr: Variable of `hru_swift_header` — see the `hru_swift_header` type.
  shf_db: Allocatable 1-D array of `shade_factor_data` — see the `shade_factor_data` type.
type_components:
  hyd_output:
    flo: m^3           |volume of water
    sed: metric tons   |sediment
    orgn: kg N          |organic N
    sedp: kg P          |organic P
    no3: kg N          |NO3-N
    solp: kg P          |mineral (soluble P)
    chla: kg            |chlorophyll-a
    nh3: kg N          |NH3
    no2: kg N          |NO2
    cbod: kg            |carbonaceous biological oxygen demand
    dox: kg            |dissolved oxygen
    san: tons          |detached sand
    sil: tons          |detached silt
    cla: tons          |detached clay
    sag: tons          |detached small ag
    lag: tons          |detached large ag
    grv: tons          |gravel
    temp: deg c         |temperature
  hyd_sep:
    flo_surq: m3           |volume of water from surface runoff
    flo_latq: m3           |volume of water from surface runoff
    flo_gwsw: m3           |volume of water from groundwater discharge
    flo_swgw: m3           |volume of water from stream seepage
    flo_satex: m3           |volume of water from saturation excess (high water table; from
      gwflow module)
    flo_satexsw: m3           |volume of water from saturation excess (saturated profile)
    flo_tile: m3           |volume of water from tile flow
  wallo_source_object:
    hd: '|nested `hyd_output` record'
  wallo_transfer_object:
    h_tot: total for transfer object
    src: '|nested `wallo_source_object` record'
  water_allocation_object:
    trn: source and receiving objects
  object_output:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    obtyp: 'object type: hru,hlt,hs,rxc,dr,out,sdc'
    obtypno: 'object type number: 1=hru, 2=hru_lte, 3=channel'
    hydtyp: 'hydrograph type: tot,rhg,sur,lat,til'
    objno: object number
    hydno: code computes from hydtyp
    filename: file with hydrograph output from the object
    unitno: filename unit number
  channel_floodplain_water_balance:
    inflo: m3       | inflow
    outflo: m3       | outflow
    tl: m3       | transmission losses
    ev: m3       | evaporation
    ch_stor_init: m3       | channel storage at start of time step
    ch_stor: m3       | channel storage at end of time step
    fp_stor_init: m3       | flood plain storage at start of time step (all flood plain storage
      above wetland emergency volume)
    fp_stor: m3       | flood plain storage at end of time step
    tot_stor_init: m3       | total channel + wetland storage at start of time step
    tot_stor: m3       | total channel + wetland storage at end of time step
    wet_stor_init: m3       | wetland flood plain storage at start of time step
    wet_stor: m3       | wetland flood plain storage at end of time step
  timestep:
    hh: '|nested `hyd_output` record'
  sorted_duration_curve:
    val: linked list to sort the flow duration curves
    next: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
  duration_curve_points:
    min: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    max: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mean: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p: probabilities for all points on the fdc
  flow_duration_curve:
    mfe: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mle: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p_md: median of all years
    yr: flow on the fdc at given percents for each year
  inflow_unit_hyds:
    uh: 'need for incoming hru or ru that are a fraction of the hru or ru

      unit hydrograph'
    hyd_flo: flow hydrograph
  flashiness_index:
    sum_q_q1: 'flashiness index sum ((qi)-q(i-1)) / sum (qi)

      sum of difference in current day flow minus previous day flow'
    sum_q: sum of daily flow over simulation period
    q_prev: previous day flow
    index: index
  object_connectivity:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    typ: object type - ie hru, hru_lte, sub, chan, res, recall
    nhyds: hru=5, chan=3 - see type hd_tot for each object
    lat: latitude (degrees)
    long: longitude (degrees)
    elev: elevation (m)
    plaps: precipitation lapse applied to object precip
    tlaps: temperature lapse applied to object precip
    area_ha: input drainag area - ha
    sp_ob_no: 'spatial object number - ie: hru number, channel number, etc'
    area_ha_calc: calculated drainage area-ha. only for checking - doesn't work if routing
      across landscape
    props: properties number from data base (ie hru.dat, sub.dat) - change props to data
    wst_c: weather station name
    wst: weather station number
    constit: constituent data pointer to pesticides, pathogens, metals, salts
    props2: overbank connectivity pointer to landscape units - change props2 to overbank
    ruleset: points to the name of the dtbl in flo_con.dtl for out flow control
    flo_dtbl: dtbl pointer for flow fraction of hydrograph
    num: spatial object number- ie hru number corresponding to sequential command number
    fired: 0=not fired; 1=fired off as a command
    cmd_next: next command (object) number
    cmd_prev: previous command (object) number
    cmd_order: 1=headwater,2=2nd order,etc
    src_tot: total number of outgoing (source) objects
    rcv_tot: total number of incoming (receiving) hydrographs
    dfn_tot: total number of defining objects (ie hru"s within a subbasin)
    ru_tot: number of routing units that contain this object
    ru: subbasin the element is in
    elem: subbasins element number for this object- used for routing over (can only have one)
    flood_ch_lnk: channel the landscape unit is linked to
    flood_ch_elem: landscape unit number - 1 is nearest to stream
    flood_frac: fraction of flood flow assigned to the object
    obtyp_out: outflow object type (ie 1=hru, 2=sd_hru, 3=sub, 4=chan, etc)
    obtypno_out: outflow object type name
    obj_out: outflow object
    htyp_out: outflow hyd type (ie 1=tot, 2= recharge, 3=surf, etc)
    ihtyp_out: outflow hyd type (ie 1=tot, 2= recharge, 3=surf, etc)
    frac_out: fraction of hydrograph
    obtyp_in: inflow object type (ie 1=hru, 2=sd_hru, 3=sub, 4=chan, etc)
    obtypno_in: inflow object type number
    obj_in: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    htyp_in: inflow hyd type (ie 1=tot, 2= recharge, 3=surf, etc)
    ihtyp_in: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    frac_in: '|a module-level working variable holding a fraction (no inline source comment;
      interpreted from the name)'
    rcvob_inhyd: inflow hydrograph number of receiving object - used for dtbl flow fractions
    fdc: use for daily flows and then use to get median of annual fdc"s
    fdc_ll: linked list of daily flow for year - dimensioned to 366
    fdc_lla: linked list of annual flow for simulation - dimensioned to nbyr
    flash_idx: flashiness index object
    hin: inflow hydrograph for surface runon - sum of all inflow hyds
    hin_sur: inflow hydrograph for surface runoff - sum of all surface inflow hyds
    hin_lat: inflow hydrograph for lateral soil flow - sum of all lateral inflow hyds
    hin_til: inflow hydrograph for tile flow - sum of all tile inflow hyds
    hin_aqu: inflow hydrograph for aquifer flow - sum of all aquifer inflow hyds
    hd: daily hydrograph (ie 1=tot, 2= recharge, 3=surf, etc)
    hd_aa: ave annual hydrograph for hru for swift (ie 1=tot, 2= recharge, 3=surf, etc)
    ts: subdaily hydrographs
    hin_uh: inflow unit hydrographs
    uh: subdaily surface runoff unit hydrograph
    hyd_flo: subdaily surface runoff hydrograph
    tsin: inflow subdaily flow hydrograph
    trans: water transfer in water allocation
    hin_tot: total inflow hydrograph to the object
    hout_tot: total outflow hydrograph to the object
    conc_prev: concentration of previous timestep for watqual2e routine
    demand: water irrigation demand (ha-m)
    day_cur: current hydrograph day in ts
    day_max: maximum number of days to store the hydrograph
    peakrate: peak flow rate during time step - m3/s
    hin_d: '|nested `hyd_output` record'
    hin_m: '|nested `hyd_output` record'
    hin_y: '|nested `hyd_output` record'
    hin_a: '|nested `hyd_output` record'
    hout_m: '|nested `hyd_output` record'
    hout_y: '|nested `hyd_output` record'
    hout_a: '|nested `hyd_output` record'
    hdep_m: '|nested `hyd_output` record'
    hdep_y: '|nested `hyd_output` record'
    hdep_a: '|nested `hyd_output` record'
    hdsep: rtb gwflow
    hdsep_in: rtb gwflow
    obj_subs: subbasins object number that contain this object
  irrigation_water_transfer:
    demand: irrigation demand          |m3
    applied: irrigation applied         |mm
    runoff: irrigation surface runoff  |mm
    eff: irrigation efficiency as a fraction of irrigation. Jaehak 2022
    frac_surq: fraction of irrigation lost in runoff flow. Jaehak 2022
    no3: nitrate concentration in irrigation water  |kg   Jaehak 2023
    salt: salt concentration in irrigation water  |ppm
    water: 'hyd_output units are in mm and mg/L

      irrigation water'
  recall_hydrograph_inputs:
    hd: 'hd and hyd_flo units are in cms and mg/L

      m3/s for flow  |input total hyd for daily, monthly, annual and exco'
    hyd_flo: m3/s           |input total flow hyd only for subdaily recall
    start_yr: start year of point source file
    end_yr: end year of point source file
  spatial_objects:
    objs: number of objects or 1st object command
    hru: 1-number of hru"s or 1st hru command
    hru_lte: 2-number of hru_lte"s or 1st hru_lte command
    ru: 3-number of ru"s or 1st ru command
    gwflow: 4-number of gwflow"s or 1st gwflow command !rtb gwflow
    aqu: 5-number of aquifer"s or 1st aquifer command
    chan: 6-number of chan"s or 1st chan command
    res: 7-number of res"s or 1st res command
    recall: 8-number of recdays"s or 1st recday command
    exco: 11-number of exco"s or 1st export coeff command
    dr: 12-number of dr"s or 1st del ratio command
    canal: 13-number of canal"s or 1st canal command
    pump: 14-number of pump"s or 1st pump command
    outlet: 15-number of outlet"s or 1st outlet command
    chandeg: 16-number of swat-deg channel"s or 1st swat-deg channel command
    aqu2d: 17-not currently used (number of 2D aquifer"s or 1st 2D aquifer command)
    herd: 18-not currently used (number of herds)
    wro: 19-not currently used (number of water rights)
  object_total_hydrographs:
    hru: 1=total 2=recharge 3=surface 4=lateral 5= tile
    hru_lte: 1=total 2=recharge 3=surface 4=lateral 5= tile
    ru: 1=total 2=recharge 3=surface 4=lateral 5= tile
    gwflow: 1=total
    aqu: 1=return flow 2=deep perc
    chan: 1=total 2=recharge 3=overbank
    res: 1=total 2=recharge
    recall: 1=total
    exco: 1=surface 2=groundwater
    dr: 1=surface 2=groundwater
    pump: 1=total
    outlet: 1=total
    chandeg: 1=total 2=recharge 3=overbank
    aqu2d: 1=return flow 3=deep perc
    herd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wro: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  routing_unit_data:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    num_tot: '|a module-level working variable holding a total (no inline source comment;
      interpreted from the name)'
    num: points to subbasin element (sub_elem)
  routing_unit_elements:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    obj: object number
    obtyp: object type- 1=hru, 2=hru_lte, 11=export coef, etc
    obtypno: 2-number of hru_lte"s or 1st hru_lte command
    frac: fraction of element in ru (expansion factor)
    dr_name: name of dr in delratio.del
    dr: calculated (or input in delratio.del) dr's for element
  channel_surface_elements:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    num: number of elements
    chnum: channel number
    resnum: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    obtyp: object type- 1=hru, 2=hru_lte, 11=export coef, etc
    obtypno: 2-number of hru_lte"s or 1st hru_lte command
    wid: maxflood plain width for each element
    dep: max flood depth for each element
    flood_volmx: max flood volume for each landscape unit
    hd: flood water for each element
  geomorphic_baseflow_channel_data:
    area: 'linked list to sort the flow duration curves

      drainage area of the channel'
    len: length of the channel
    len_left: fraction of chan length left when channel becomes non-contributing
    flo_fr: fraction of aquifer baseflow for each channel
  channel_aquifer_elements:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    num_tot: number of elements
    num: channel numbers
    len_tot: total length of channels in aquifer (km)
    hd: baseflow hydrograph for the aquifer
    ch: '|nested `geomorphic_baseflow_channel_data` record'
  hyd_header:
    flo: ha-m         |volume of water
    sed: metric tons  |sediment
    orgn: kg N         |organic N
    sedp: kg P         |organic P
    no3: kg N         |NO3-N
    solp: kg P         |mineral (soluble P)
    chla: kg           |chlorophyll-a
    nh3: kg N         |NH3
    no2: kg N         |NO2
    cbod: kg           |carbonaceous biological oxygen demand
    dox: kg           |dissolved oxygen
    san: tons         |detached sand
    sil: tons         |detached silt
    cla: tons         |detached clay
    sag: tons         |detached small ag
    lag: tons         |detached large ag
    grv: tons         |gravel
    temp: deg c        |temperature
  hyd_stor_header:
    flo_stor: m^3/s        |water stored at the end of time period
    sed_stor: metric tons  |sediment stored at the end of time period
    orgn_stor: kg N         |organic N stored at the end of time period
    sedp_stor: kg P         |organic P stored at the end of time period
    no3_stor: kg N         |NO3-N stored at the end of time period
    solp_stor: kg P         |mineral (soluble P) stored at end of time period
    chla_stor: kg           |chlorophyll-a stored at end of time period
    nh3_stor: kg N         |NH3-N (ammonium) stored at end of time period
    no2_stor: kg N         |NO2-N (nitrite) stored at end of time period
    cbod_stor: kg           |carbonaceous biological oxygen demand at end of time period
    dox_stor: kg           |dissolved oxygen stored at end of time period
    san_stor: tons         |detached sand stored at end of time period
    sil_stor: tons         |detached silt stored at end of time period
    cla_stor: tons         |detached clay stored at end of time period
    sag_stor: tons         |detached small ag stored at end of time period
    lag_stor: tons         |detached large ag stored at end of time period
    grv_stor: tons         |gravel stored at end of time period
    temp_stor: deg c        |water temperature
  hyd_in_header:
    flo_in: m^3/s        |water in
    sed_in: metric tons  |sediment in
    orgn_in: kg N         |organic N in
    sedp_in: kg P         |organic P in
    no3_in: kg N         |NO3-N (nitrate) in
    solp_in: kg P         |mineral (soluble P) in
    chla_in: kg           |chlorophyll-a in
    nh3_in: kg N         |NH3-N (ammonium) in
    no2_in: kg N         |NO2-N (nitrate) in
    cbod_in: kg           |carbonaceous biological oxygen demand in
    dox_in: kg           |dissolved oxygen in
    san_in: tons         |detached sand in
    sil_in: tons         |detached silt in
    cla_in: tons         |detached clay in
    sag_in: tons         |detached small ag in
    lag_in: tons         |detached large ag in
    grv_in: tons         |gravel in
    temp_in: deg c        |temperature in
  hyd_out_header:
    flo_out: m^3/s        |water out
    sed_out: metric tons  |sediment out
    orgn_out: kg N         |organic N out
    sedp_out: kg P         |organic P out
    no3_out: kg N         |NO3-N out
    solp_out: kg P         |mineral (soluble P) out
    chla_out: kg           |chlorophyll-a out
    nh3_out: kg N         |NH3-N (ammonium) out
    no2_out: kg N         |NO2-N (nitrite) out
    cbod_out: kg           |carbonaceous biological oxygen demand out
    dox_out: kg           |dissolved oxygen out
    san_out: tons         |detached sand out
    sil_out: tons         |detached silt out
    cla_out: tons         |detached clay out
    sag_out: tons         |detached small ag out
    lag_out: tons         |detached large ag out
    grv_out: tons         |gravel out
    temp_out: deg c        |temperature out
  hyd_inout_header:
    flo_in: m^3/s        |water in
    flo_out: m^3/s        |water out
    sed_in: metric tons  |sediment in
    sed_out: metric tons  |sediment out
    orgn_in: kg N         |organic N in
    orgn_out: kg N         |organic N out
    sedp_in: kg P         |organic P in
    sedp_out: kg P         |organic P out
    no3_in: kg N         |NO3-N (nitrate) in
    no3_out: kg N         |NO3-N out
    solp_in: kg P         |mineral (soluble P) in
    solp_out: kg P         |mineral (soluble P) out
    chla_in: kg           |chlorophyll-a in
    chla_out: kg           |chlorophyll-a out
    nh3_in: kg N         |NH3-N (ammonium) in
    nh3_out: kg N         |NH3-N (ammonium) out
    no2_in: kg N         |NO2-N (nitrate) in
    no2_out: kg N         |NO2-N (nitrite) out
    cbod_in: kg           |carbonaceous biological oxygen demand in
    cbod_out: kg           |carbonaceous biological oxygen demand out
    dox_in: kg           |dissolved oxygen in
    dox_out: kg           |dissolved oxygen out
  wtmp_out_header:
    water_temp: deg c        |temperature
  sed_hyd_header:
    flo_in: m^3/s        |volume of water
    flo_out: m^3/s        |volume of water
    sed_in: metric tons  |sediment
    sed_out: metric tons  |sediment
    orgn_in: kg N         |organic N
    orgn_out: kg N         |organic N
    sedp_in: kg P         |organic P
    sedp_out: kg P         |organic P
    no3_in: kg N         |NO3-N
    no3_out: kg N         |NO3-N
    solp_in: kg P         |mineral (soluble P)
    solp_out: kg P         |mineral (soluble P)
    chla_in: kg           |chlorophyll-a
    chla_out: kg           |chlorophyll-a
    nh3_in: kg N         |NH3
    nh3_out: kg N         |NH3
    no2_in: kg N         |NO2
    no2_out: kg N         |NO2
    cbod_in: kg           |carbonaceous biological oxygen demand
    cbod_out: kg           |carbonaceous biological oxygen demand
    dox_in: kg           |dissolved oxygen
    dox_out: kg           |dissolved oxygen
    temp_in: deg c        |temperature
    temp_out: deg c        |temperature
  sd_hyd_header_units:
    flo_in: avg daily m^3/s        |volume of water
    flo_out: avg daily m^3/s        |volume of water
    sed_in: metric tons  |sediment
    sed_out: metric tons  |sediment
    orgn_in: kg N         |organic N
    orgn_out: kg N         |organic N
    sedp_in: kg P         |organic P
    sedp_out: kg P         |organic P
    no3_in: kg N         |NO3-N
    no3_out: kg N         |NO3-N
    solp_in: kg P         |mineral (soluble P)
    solp_out: kg P         |mineral (soluble P)
    chla_in: kg           |chlorophyll-a
    chla_out: kg           |chlorophyll-a
    nh3_in: kg N         |NH3
    nh3_out: kg N         |NH3
    no2_in: kg N         |NO2
    no2_out: kg N         |NO2
    cbod_in: kg           |carbonaceous biological oxygen demand
    cbod_out: kg           |carbonaceous biological oxygen demand
    dox_in: kg           |dissolved oxygen
    dox_out: kg           |dissolved oxygen
    temp_in: deg c        |temperature
    temp_out: deg c        |temperature
  sol_header:
    layer1: mm H2O       |plant name
    layer2: mm H2O       |amt of water stored in layer 2
    layer3: mm H2O       |amt of water stored in layer 3
    layer4: mm H2O       |amt of water stored in layer 4
    layer5: mm H2O       |amt of water stored in layer 5
    layer6: mm H2O       |amt of water stored in layer 6
    layer7: mm H2O       |amt of water stored in layer 7
    layer8: mm H2O       |amt of water stored in layer 8
    layer9: mm H2O       |amt of water stored in layer 9
    layer10: mm H2O       |amt of water stored in layer 10
  plant_header:
    name: none         |plant name
    growing: none         |plant growing
    dormant: none         |plant dormant
    lai: none         |leaf area index
    can_hgt: m            |canopy height
    root_dep: m            |root depth
    phuacc: 0-1          |accumulated heat units
    tot_m: kg/ha        |total biomass
    ab_gr_m: kg/ha        |above ground biomass
    leaf_m: kg/ha        |leaf biomass
    root_m: kg/ha        |root biomass
    stem_m: kg/ha        |stem biomass
    seed_m: kg/ha        |seed biomass
  flood_plain_header:
    inflo: m3        | inflow
    outflo: m3        | outflow
    dormant: m3        | evaporation
    tl: m3        | transmission losses
    ev: m3        | evaporation
    ch_stor_init: m3        | channel storage at start of time step
    ch_stor: m3        | channel storage at end of time step
    fp_stor_init: m3        | flood plain storage at start of time step (all flood plain storage
      above wetland emergency volume)
    fp_stor: m3        | flood plain storage at end of time step
    tot_stor_init: m3        | total channel + wetland storage at start of time step
    tot_stor: m3        | total channel + wetland storage at end of time step
    wet_stor_init: m3        | wetland flood plain storage at start of time step
    wet_stor: m3        | wetland flood plain storage at end of time step
  ch_watbod_header:
    day: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day_mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    isd: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    id: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    area_ha: '|a module-level working variable holding an area (no inline source comment;
      interpreted from the name)'
    precip: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    evap: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seep: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  ch_watbod_header_units:
    day: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day_mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    isd: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    id: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    area_ha: '|a module-level working variable holding an area (no inline source comment;
      interpreted from the name)'
    precip: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    evap: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seep: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  ch_watbod_inoutheader:
    day: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day_mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    id: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    gis_id: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
  ch_watbod_inoutheader_units:
    day: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day_mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    id: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    gis_id: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
  hyd_header_units1:
    flo: m^3/s        |volume of water
    sed: metric tons  |sediment
    orgn: kg N         |organic N
    sedp: kg P         |organic P
    no3: kg N         |NO3-N
    solp: kg P         |mineral (soluble P)
    chla: kg           |chlorophyll-a
    nh3: kg N         |NH3
    no2: kg N         |NO2
    cbod: kg           |carbonaceous biological oxygen demand
    dox: kg           |dissolved oxygen
    san: tons         |detached sand
    sil: tons         |detached silt
    cla: tons         |detached clay
    sag: tons         |detached small ag
    lag: tons         |detached large ag
    grv: tons         |gravel
    temp: deg c        |temperature
  hyd_header_units3:
    flo: m^3          |volume of water
    sed: metric tons  |sediment
    orgn: kg N         |organic N
    sedp: kg P         |organic P
    no3: kg N         |NO3-N
    solp: kg P         |mineral (soluble P)
    chla: kg           |chlorophyll-a
    nh3: kg N         |NH3
    no2: kg N         |NO2
    cbod: kg           |carbonaceous biological oxygen demand
    dox: kg           |dissolved oxygen
    san: tons         |detached sand
    sil: tons         |detached silt
    cla: tons         |detached clay
    sag: tons         |detached small ag
    lag: tons         |detached large ag
    grv: tons         |gravel
    temp: deg c        |temperature
  hydinout_header_units1:
    flo_in: avg daily m^3/s        |volume of water
    flo_out: avg daily m^3/s        |volume of water
    sed_in: metric tons  |sediment
    sed_out: metric tons  |sediment
    orgn_in: kg N         |organic N
    orgn_out: kg N         |organic N
    sedp_in: kg P         |organic P
    sedp_ouy: kg P         |organic P
    no3_in: kg N         |NO3-N
    no3_out: kg N         |NO3-N
    solp_in: kg P         |mineral (soluble P)
    solp_out: kg P         |mineral (soluble P)
    chla_in: kg           |chlorophyll-a
    chla_out: kg           |chlorophyll-a
    nh3_in: kg N         |NH3
    nh3_out: kg N         |NH3
    no2_in: kg N         |NO2
    no2_out: kg N         |NO2
    cbod_in: kg           |carbonaceous biological oxygen demand
    cbod_out: kg           |carbonaceous biological oxygen demand
    dox_in: kg           |dissolved oxygen
    dox_out: kg           |dissolved oxygen
  wtmp_header_units:
    wtmp: deg c        |temperature
  hyd_header_units:
    day: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day_mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    otype: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    flo: m^3/s        |volume of water
    sed: metric tons  |sediment
    orgn: kg N         |organic N
    sedp: kg P         |organic P
    no3: kg N         |NO3-N
    solp: kg P         |mineral (soluble P)
    chla: kg           |chlorophyll-a
    nh3: kg N         |NH3
    no2: kg N         |NO2
    cbod: kg           |carbonaceous biological oxygen demand
    dox: kg           |dissolved oxygen
    san: tons         |detached sand
    sil: tons         |detached silt
    cla: tons         |detached clay
    sag: tons         |detached small ag
    lag: tons         |detached large ag
    grv: tons         |gravel
    temp: deg c        |temperature
  hyd_header_units2:
    day: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day_mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    otype: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    iotyp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    iotypno: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hydio: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    objno: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    flo: m^3/s          |volume of water
    sed: metric tons  |sediment
    orgn: kg N         |organic N
    sedp: kg P         |organic P
    no3: kg N         |NO3-N
    solp: kg P         |mineral (soluble P)
    chla: kg           |chlorophyll-a
    nh3: kg N         |NH3
    no2: kg N         |NO2
    cbod: kg           |carbonaceous biological oxygen demand
    dox: kg           |dissolved oxygen
    san: tons         |detached sand
    sil: tons         |detached silt
    cla: tons         |detached clay
    sag: tons         |detached small ag
    lag: tons         |detached large ag
    grv: tons         |gravel
    temp: deg c        |temperature
  hyd_header_time:
    day: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day_mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    otype: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  rec_header_time:
    day: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day_mo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    blank: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  hyd_header_obj:
    iotyp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    iotypno: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hydio: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    objno: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_flow_duration_header:
    obtyp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    props: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    area: '|a module-level working variable holding an area (no inline source comment; interpreted
      from the name)'
    f_idx: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    mean: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    max: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p01: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p05: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p1: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p2: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p5: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p10: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p15: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p20: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p25: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p30: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p35: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p40: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p45: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p50: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p55: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p60: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p65: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p70: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p75: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p80: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p85: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p90: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p95: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p97: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p98: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    p99: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    min: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  calibration_header:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    ha: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    nbyr: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    prec: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    meas: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    srr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lfr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    pcr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    etr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tfr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sed: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    orgn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    orgp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    no3: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    solp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    srr_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lfr_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    pcr_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    etr_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tfr_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sed_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    orgn_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    orgp_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    no3_aa: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    solp_aa: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    cn_prm_aa: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    esco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lat_len: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    petco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    slope: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tconc: '|a module-level working variable holding a concentration (no inline source comment;
      interpreted from the name)'
    etco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    revapc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    cn3_swf: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  calibration2_header:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    dakm2: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    cn2: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    soildep: '|a module-level working variable holding a depth (no inline source comment;
      interpreted from the name)'
    perco_co: '|a module-level working variable holding a coefficient (no inline source comment;
      interpreted from the name)'
    slope: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    slopelen: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    etco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sy: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    abf: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    revapc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    percc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sw: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gw: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gwflow: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gwdeep: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    snow: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    xlat: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    itext: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tropical: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    igrow1: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    igrow2: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    plant: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    ipet: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    irr: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    irrsrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tdrain: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    uslek: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    uslec: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    uslep: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    uslels: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  calibration3_header:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    chgtyp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    val: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    conds: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lyr1: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lyr2: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    year1: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    year2: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day1: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    day2: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    objtot: '|a module-level working variable holding a total (no inline source comment; interpreted
      from the name)'
  output_checker_header:
    sname: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hydgrp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    zmx: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    usle_k: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sumfc: '|a module-level working variable holding a running sum (no inline source comment;
      interpreted from the name)'
    sumul: '|a module-level working variable holding a running sum (no inline source comment;
      interpreted from the name)'
    usle_p: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    usle_ls: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    esco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    epco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    cn3_swf: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_co: '|a module-level working variable holding a coefficient (no inline source comment;
      interpreted from the name)'
    tiledrain: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
  output_checker_unit:
    sname: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hydgrp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    zmx: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    usle_k: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sumfc: '|a module-level working variable holding a running sum (no inline source comment;
      interpreted from the name)'
    sumul: '|a module-level working variable holding a running sum (no inline source comment;
      interpreted from the name)'
    usle_p: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    usle_ls: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    esco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    epco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    cn3_swf: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perco: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_co: '|a module-level working variable holding a coefficient (no inline source comment;
      interpreted from the name)'
    tiledrain: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
  hru_swift_header_base:
    sed: metric tons  |sediment
    orgn: kg N         |organic N
    sedp: kg P         |organic P
    no3: kg N         |NO3-N
    solp: kg P         |mineral (soluble P)
    nh3: 'character (len=16) :: chla =    "chla "        !! kg           |chlorophyll-a

      kg N         |NH3'
    no2: kg N         |NO2
  hru_swift_header_baseunit:
    unitsed: 'character (len=16) :: unitflo    =  "m^3 "        !! m^3          |volume of
      water

      metric tons  |sediment'
    unitorgn: kg N         |organic N
    unitsedp: kg P         |organic P
    unitno3: kg N         |NO3-N
    unitsolp: kg P         |mineral (soluble P)
    unitnh3: 'character (len=16) :: unitchla   =  "kg "        !! kg           |chlorophyll-a

      kg N         |NH3'
    unitno2: kg N         |NO2
  hru_swift_header_base2:
    flo: ha-m         |volume of water
    base: '|nested `hru_swift_header_base` record'
  hru_swift_header_baseunit2:
    unitflo: m^3          |volume of water
    base: '|nested `hru_swift_header_baseunit` record'
  hru_swift_header:
    hd_type: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    exco: '|nested `hru_swift_header_base` record'
    exco_unit: '|nested `hru_swift_header_baseunit` record'
    dr: '|nested `hru_swift_header_base2` record'
    dr_unit: '|nested `hru_swift_header_baseunit2` record'
  shade_factor_data:
    jday: none          |day of the year
    lsu: none          |landscape unit
    value: none          |shade factor value
type_summaries:
  hyd_output: One `hyd_output` record groups `flo`, `sed`, `orgn`, `sedp`, `no3`, `solp`,
    and 12 more fields.
  hyd_sep: Rtb gwflow - hydrograph separation. Holds `flo_surq`, `flo_latq`, `flo_gwsw`, `flo_swgw`,
    `flo_satex`, `flo_satexsw`, and 1 more fields.
  wallo_source_object: Source and receiving objects. Holds `hd`.
  wallo_transfer_object: Source and receiving objects. Holds `h_tot`, `src`.
  water_allocation_object: Source and receiving objects. Holds `trn`.
  object_output: One `object_output` record groups `name`, `obtyp`, `obtypno`, `hydtyp`, `objno`,
    `hydno`, and 2 more fields.
  channel_floodplain_water_balance: One `channel_floodplain_water_balance` record groups `inflo`,
    `outflo`, `tl`, `ev`, `ch_stor_init`, `ch_stor`, and 6 more fields.
  timestep: One `timestep` record groups `hh`.
  sorted_duration_curve: One `sorted_duration_curve` record groups `val`, `next`.
  duration_curve_points: One `duration_curve_points` record groups `min`, `max`, `mean`, `p`.
  flow_duration_curve: One `flow_duration_curve` record groups `mfe`, `mle`, `p_md`, `yr`.
  inflow_unit_hyds: One `inflow_unit_hyds` record groups `uh`, `hyd_flo`.
  flashiness_index: One `flashiness_index` record groups `sum_q_q1`, `sum_q`, `q_prev`, `index`.
  object_connectivity: One `object_connectivity` record groups `name`, `typ`, `nhyds`, `lat`,
    `long`, `elev`, and 76 more fields.
  irrigation_water_transfer: Water allocation. Holds `demand`, `applied`, `runoff`, `eff`,
    `frac_surq`, `no3`, and 2 more fields.
  recall_hydrograph_inputs: Recall hydrograph inputs. Holds `hd`, `hyd_flo`, `start_yr`, `end_yr`.
  spatial_objects: One `spatial_objects` record groups `objs`, `hru`, `hru_lte`, `ru`, `gwflow`,
    `aqu`, and 12 more fields.
  object_total_hydrographs: One `object_total_hydrographs` record groups `hru`, `hru_lte`,
    `ru`, `gwflow`, `aqu`, `chan`, and 10 more fields.
  routing_unit_data: One `routing_unit_data` record groups `name`, `num_tot`, `num`.
  routing_unit_elements: One `routing_unit_elements` record groups `name`, `obj`, `obtyp`,
    `obtypno`, `frac`, `dr_name`, and 1 more fields.
  channel_surface_elements: Channel-surface element linkage for overbank flooding. Holds `name`,
    `num`, `chnum`, `resnum`, `obtyp`, `obtypno`, and 4 more fields.
  geomorphic_baseflow_channel_data: Channel data for channel-aquifer linkage for geomorphic
    base flow model. Holds `area`, `len`, `len_left`, `flo_fr`.
  channel_aquifer_elements: Channel-aquifer linkage for geomorphic base flow model. Holds
    `name`, `num_tot`, `num`, `len_tot`, `hd`, `ch`.
  hyd_header: One `hyd_header` record groups `flo`, `sed`, `orgn`, `sedp`, `no3`, `solp`,
    and 12 more fields.
  hyd_stor_header: One `hyd_stor_header` record groups `flo_stor`, `sed_stor`, `orgn_stor`,
    `sedp_stor`, `no3_stor`, `solp_stor`, and 12 more fields.
  hyd_in_header: One `hyd_in_header` record groups `flo_in`, `sed_in`, `orgn_in`, `sedp_in`,
    `no3_in`, `solp_in`, and 12 more fields.
  hyd_out_header: One `hyd_out_header` record groups `flo_out`, `sed_out`, `orgn_out`, `sedp_out`,
    `no3_out`, `solp_out`, and 12 more fields.
  hyd_inout_header: One `hyd_inout_header` record groups `flo_in`, `flo_out`, `sed_in`, `sed_out`,
    `orgn_in`, `orgn_out`, and 16 more fields.
  wtmp_out_header: One `wtmp_out_header` record groups `water_temp`.
  sed_hyd_header: One `sed_hyd_header` record groups `flo_in`, `flo_out`, `sed_in`, `sed_out`,
    `orgn_in`, `orgn_out`, and 18 more fields.
  sd_hyd_header_units: One `sd_hyd_header_units` record groups `flo_in`, `flo_out`, `sed_in`,
    `sed_out`, `orgn_in`, `orgn_out`, and 18 more fields.
  sol_header: One `sol_header` record groups `layer1`, `layer2`, `layer3`, `layer4`, `layer5`,
    `layer6`, and 4 more fields.
  plant_header: One `plant_header` record groups `name`, `growing`, `dormant`, `lai`, `can_hgt`,
    `root_dep`, and 7 more fields.
  flood_plain_header: One `flood_plain_header` record groups `inflo`, `outflo`, `dormant`,
    `tl`, `ev`, `ch_stor_init`, and 7 more fields.
  ch_watbod_header: One `ch_watbod_header` record groups `day`, `mo`, `day_mo`, `yrc`, `isd`,
    `id`, and 5 more fields.
  ch_watbod_header_units: One `ch_watbod_header_units` record groups `day`, `mo`, `day_mo`,
    `yrc`, `isd`, `id`, and 5 more fields.
  ch_watbod_inoutheader: One `ch_watbod_inoutheader` record groups `day`, `mo`, `day_mo`,
    `yrc`, `id`, `gis_id`, and 1 more fields.
  ch_watbod_inoutheader_units: One `ch_watbod_inoutheader_units` record groups `day`, `mo`,
    `day_mo`, `yrc`, `id`, `gis_id`, and 1 more fields.
  hyd_header_units1: One `hyd_header_units1` record groups `flo`, `sed`, `orgn`, `sedp`, `no3`,
    `solp`, and 12 more fields.
  hyd_header_units3: One `hyd_header_units3` record groups `flo`, `sed`, `orgn`, `sedp`, `no3`,
    `solp`, and 12 more fields.
  hydinout_header_units1: One `hydinout_header_units1` record groups `flo_in`, `flo_out`,
    `sed_in`, `sed_out`, `orgn_in`, `orgn_out`, and 16 more fields.
  wtmp_header_units: One `wtmp_header_units` record groups `wtmp`.
  hyd_header_units: One `hyd_header_units` record groups `day`, `mo`, `day_mo`, `yrc`, `name`,
    `otype`, and 18 more fields.
  hyd_header_units2: One `hyd_header_units2` record groups `day`, `mo`, `day_mo`, `yrc`, `name`,
    `otype`, and 22 more fields.
  hyd_header_time: One `hyd_header_time` record groups `day`, `mo`, `day_mo`, `yrc`, `name`,
    `otype`.
  rec_header_time: One `rec_header_time` record groups `day`, `mo`, `day_mo`, `yrc`, `name`,
    `blank`.
  hyd_header_obj: One `hyd_header_obj` record groups `iotyp`, `iotypno`, `hydio`, `objno`.
  output_flow_duration_header: One `output_flow_duration_header` record groups `obtyp`, `props`,
    `area`, `f_idx`, `mean`, `max`, and 28 more fields.
  calibration_header: One `calibration_header` record groups `name`, `ha`, `nbyr`, `prec`,
    `meas`, `srr`, and 30 more fields.
  calibration2_header: One `calibration2_header` record groups `name`, `dakm2`, `cn2`, `tc`,
    `soildep`, `perco_co`, and 26 more fields.
  calibration3_header: One `calibration3_header` record groups `name`, `chgtyp`, `val`, `conds`,
    `lyr1`, `lyr2`, and 5 more fields.
  output_checker_header: One `output_checker_header` record groups `sname`, `hydgrp`, `zmx`,
    `usle_k`, `sumfc`, `sumul`, and 8 more fields.
  output_checker_unit: One `output_checker_unit` record groups `sname`, `hydgrp`, `zmx`, `usle_k`,
    `sumfc`, `sumul`, and 8 more fields.
  hru_swift_header_base: One `hru_swift_header_base` record groups `sed`, `orgn`, `sedp`,
    `no3`, `solp`, `nh3`, and 1 more fields.
  hru_swift_header_baseunit: One `hru_swift_header_baseunit` record groups `unitsed`, `unitorgn`,
    `unitsedp`, `unitno3`, `unitsolp`, `unitnh3`, and 1 more fields.
  hru_swift_header_base2: One `hru_swift_header_base2` record groups `flo`, `base`.
  hru_swift_header_baseunit2: One `hru_swift_header_baseunit2` record groups `unitflo`, `base`.
  hru_swift_header: One `hru_swift_header` record groups `hd_type`, `exco`, `exco_unit`, `dr`,
    `dr_unit`.
  shade_factor_data: One `shade_factor_data` record groups `jday`, `lsu`, `value`.
---

<!-- facts:header -->

`hydrograph_module` owns the core hydrograph record type `hyd_output` — the water, sediment, nutrient, and constituent loads passed between spatial objects — together with the connectivity and routing scaffolding for SWAT+: the per-object hydrograph arrays (`hd`, `rec_d/m/y/a`, `ob`, `ob_out`), the water-allocation objects, the flow-duration-curve types, the channel-floodplain water balance, and the timestep hydrograph. The arrays are allocated and populated by the object/connectivity setup and command-routing code and are consumed throughout the routing, channel, reservoir, aquifer, and output routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is primarily a declaration container. Scalar counters and the `hyd_output` record default to zero, and the large hydrograph arrays (`hd`, `rec_*`, `ob`, water-allocation and duration-curve arrays) are allocated by the object/connectivity setup routines (`hyd_connect`, `obj_output_read`, command routing) before the simulation runs.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | References `hydrograph_module` state: references `irrig`, `aqu`, `ch_stor`, `res` (e.g. `actions.f90:133`). |
| [sym:aqu2d_init] | `no direct file input (operates on in-memory state)` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Initializes `hydrograph_module` state: references `sp_ob`, `aq_ch`, `aqu_cha`, `ich` (e.g. `aqu2d_init.f90:24`). |
| [sym:aqu2d_read] | `aqu_cha.lin` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Reads input and populates `hydrograph_module` state: references `aq_ch`, `sp_ob`, `elem_cnt`, `defunit_num` (e.g. `aqu2d_read.f90:31`). |
| [sym:aqu_cs_output] | `unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Writes output from `hydrograph_module` state: references `ob`, `sp_ob1` (e.g. `aqu_cs_output.f90:6`). |
| [sym:aqu_pest_output_init] | `no direct file input (operates on in-memory state)` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Initializes `hydrograph_module` state: references `sp_ob` (e.g. `aqu_pest_output_init.f90:5`). |
| [sym:aqu_pesticide_output] | `unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Writes output from `hydrograph_module` state: references `ob`, `sp_ob1` (e.g. `aqu_pesticide_output.f90:11`). |
| [sym:aqu_read_elements] | `aqu_catunit.def, aqu_catunit.ele` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | References `hydrograph_module` state: references `elem_cnt`, `defunit_num`, `sp_ob` (e.g. `aqu_read_elements.f90:58`). |
| [sym:aqu_read_init] | `initial.aqu` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Initializes `hydrograph_module` state: references `sp_ob`, `om_init_name` (e.g. `aqu_read_init.f90:63`). |
| [sym:aqu_read_init_cs] | `initial.aqu_cs` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | References `hydrograph_module` state: references `sp_ob`, `sp_ob1`, `ob` (e.g. `aqu_read_init_cs.f90:71`). |
| [sym:aqu_salt_output] | `unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Writes output from `hydrograph_module` state: references `ob`, `sp_ob1` (e.g. `aqu_salt_output.f90:6`). |
| [sym:aquifer_output] | `unit_2520, unit_2524, unit_2521, unit_2525, unit_2522, unit_2526, unit_2523, unit_2527` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Writes output from `hydrograph_module` state: references `ob`, `sp_ob1` (e.g. `aquifer_output.f90:6`). |
| [sym:basin_aqu_pest_output] | `unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007` | `mhyd, mcmd, inum2, jrch, jrchq, mrte` | Writes output from `hydrograph_module` state: references `ob`, `sp_ob`, `sp_ob1` (e.g. `basin_aqu_pest_output.f90:11`). |

## Key Consumers

Importers fall into setup/connectivity (object and hydrograph array allocation and command routing), the routing and storage routines that read and write `hyd_output` loads between objects (channels, reservoirs, aquifers, HRUs), the water-allocation routines, and the output routines that report and roll up the daily/monthly/yearly/average-annual hydrographs.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu_cs_output] | `ob`, `sp_ob1` | The hydrograph object mapping identifies which basin object corresponds to aquifer `iaq`, so the output can carry the correct GIS identifier. Without `sp_ob1` and `ob`, the routine could not label each aquifer record with `ob(iob)%gis_id`. |
| [sym:aqu_pest_output_init] | `sp_ob` | This module provides the spatial object counts used to size the aquifer loop. `sp_ob%aqu` tells the routine how many aquifer objects exist in the current simulation, so each one can have its output state initialized. |
| [sym:aqu_pesticide_output] | `sp_ob1`, `ob` | `hydrograph_module` provides the aquifer object offset (`sp_ob1%aqu`) and object metadata (`ob(iob)%name`, plus `ob(iob)%gis_id` from the same object table) needed to associate each output row with the correct aquifer object. The routine cannot produce object-labeled output without that mapping. |
| [sym:aqu_salt_output] | `ob`, `sp_ob1` | The hydrograph object connectivity provides the GIS/object identifier for the aquifer being printed, and the aquifer offset defines which global object index to use. This matters because every output row is labeled with `ob(iob)%gis_id` rather than only the local aquifer number. |
| [sym:aquifer_output] | `ob`, `sp_ob1` | The hydrograph object tables provide the spatial mapping and labels needed to identify which aquifer is being printed. `sp_ob1%aqu` gives the first aquifer object index, and `ob(iob)%name` supplies the object name written with each output row. |
| [sym:basin_aqu_pest_output] | `sp_ob`, `sp_ob1`, `ob` | `hydrograph_module` provides the aquifer count and object naming used to drive the loops and label the records. `sp_ob%aqu` sets how many aquifer objects are aggregated, `sp_ob1%aqu` identifies the basin aquifer object index, and `ob(iob)%name` is written to each output line. |
| [sym:basin_aquifer_output] | `sp_ob` | The hydrograph module provides `sp_ob%aqu`, the basin's aquifer-object count. That count sets the loop bound for summing all aquifer contributions into the basin daily aquifer summary. |
| [sym:basin_ch_pest_output] | `sp_ob`, `sp_ob1`, `ob` | The channel/hydrograph state provides the object context for the output record: `sp_ob1%chandeg` selects the channel object index used for `ob(iob)%name`, `sp_ob%chandeg` sets the channel-degree loop bound, and `ob(iob)%name` supplies the basin/channel object label written to the output files. |
| [sym:basin_channel_output] | `sp_ob` | The spatial object count provides the channel population size. `sp_ob%chan` is the upper bound for the loop over `ch_d(ich)`, so it controls how many channel outputs are included in the basin daily total. |
| [sym:basin_ls_pest_output] | `sp_ob`, `sp_ob1`, `ob` | `hydrograph_module` provides the spatial object counts and object names that identify the basin/HRU context for the written records; without these indices and names the output lines could not be tagged to the correct object. |
| [sym:basin_res_pest_output] | `sp_ob`, `sp_ob1`, `ob` | This module supplies the reservoir object counts and reservoir object names needed to select the reservoir index and label each output row. |
| [sym:ch_cs_output] | `sp_ob1`, `ob` | `hydrograph_module` provides channel-object metadata needed to label the output. `sp_ob1%chandeg` converts `jrch` into the proper object index, and `ob(iob)%gis_id` is written as the GIS identifier for the reported channel. |
| [sym:ch_salt_output] | `sp_ob1`, `ob` | `sp_ob1%chandeg` defines the starting object index for channel-degrees in the global object list. The routine adds `jrch - 1` to it to locate `ob(iob)%gis_id`, which is written to identify the channel reach in the output files. |
| [sym:cha_pesticide_output] | `sp_ob1`, `ob` | `sp_ob1%chandeg` anchors the channel-deg numbering used to derive `iob`, and `ob(iob)%name` provides the object name printed in the output rows. These hydrograph-module states tie the pesticide summaries to the correct channel object in the model network. |
| [sym:channel_output] | `ob`, `sp_ob1` | `hydrograph_module` links the channel index to the broader object table used in output records. `sp_ob1%chan` gives the starting object number for channels, and `ob(iob)%name` supplies the object label that is written beside the channel values so the output can be tied back to the correct channel object. |
| [sym:cn2_init_all] | `sp_ob` | cn2_init_all uses the total HRU count from sp_ob%hru to determine how many HRUs to initialize. |
| [sym:cs_hru_init] | `sp_ob` | hydrograph_module provides `sp_ob%hru`, the number of HRUs to iterate over. That count is the outer loop bound, so it determines how many HRU constituent arrays must be initialized before the simulation can proceed. |
| [sym:cs_reactions_read] | `sp_ob` | `hydrograph_module` supplies `sp_ob%hru` and `sp_ob%aqu`, which determine how many soil and aquifer reaction records the routine allocates and fills. |
| [sym:dtbl_lum_read] | `sp_ob` | `hydrograph_module` supplies `sp_ob%hru`, the number of HRUs to scan when a condition depends on land use. The routine uses that count to tally matching HRUs and accumulate their area for probabilistic land-use or management application logic. |
| [sym:gwflow_pond] | `ch_stor` | ch_stor holds the current-day storage for each channel reach. gwflow_pond reads ch_stor(chan_id)%flo to determine whether the channel can supply the full requested diversion, then reduces flo, no3, and solp by the diverted amounts so channel mass balance remains consistent after transfer to the pond. |
| [sym:header_aquifer] | `sp_ob` | hydrograph_module provides `sp_ob%aqu`, the aquifer object count used as a guard before any aquifer output files are opened. If no aquifer objects exist, this routine skips the corresponding header writes entirely. |
| [sym:header_channel] | `sp_ob` | This routine depends on `hydrograph_module` because `sp_ob%chan` is the gate that tells the routine whether any channel objects exist at all; if there are no channel objects, it skips creating the channel header files. |
| [sym:header_const] | `sp_ob` | This module provides `sp_ob`, which tells `header_const` whether aquifer, channel, reservoir, and routing-unit objects exist in the model. The routine uses those object counts to avoid opening output files for object types that are not present, even if print flags are enabled. |
| [sym:header_pest] | `sp_ob` | `hydrograph_module` matters because `sp_ob` carries the spatial object counts that decide whether HRU, channel, reservoir, and aquifer pesticide output branches run at all. `header_pest` uses `sp_ob%hru`, `sp_ob%chandeg`, `sp_ob%res`, and `sp_ob%aqu` as existence checks before opening the corresponding header files. |

## Lineage

`hydrograph_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 15 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hydrograph_module.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `e24da22` (2026-03-11) — Add allocatable variables for outside inflow and update water tower read logic
- `080211e` (2026-03-09) — water allocation operating properly
- `815ec79` (2026-01-07) — water allocation updates
- `90fa54f` (2025-10-29) — Channel deposition and erosion adjusment. Water allocation modeule related adjustemnts
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `hydrograph_module` has no extracted module-level documentation comment.
- Reader rows show 12 candidate initialization/read routines out of 192; treat the table as representative, not exhaustive.
- This module is imported by 320 procedures; the main Used By table shows 24 ranked consumers and the collapsible importer list keeps the complete deterministic list.
- variable_notes and type_notes summaries were completed locally from the module's declaration metadata (type, shape, source comments) and the Derived Type Inventory; reader behaviors were grounded in source references found in each reader. 4 module-level scalar(s) had no inline source comment and were given name-based interpretations — these should be spot-checked.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
