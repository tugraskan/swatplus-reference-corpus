---
kind: module
symbol: output_landscape_module
title: output_landscape_module
status: filled
source_hash: 09eb864988d4f61f
version_label: SWAT+ 62.0.0
variables:
  h: Pointer of `output_waterbal` — see the `output_waterbal` type.
  hwb_d: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    daily values.
  hwb_m: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    monthly values.
  hwb_y: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    yearly values.
  hwb_a: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    average-annual values.
  hwbz: Variable of `output_waterbal` — see the `output_waterbal` type.
  hltwb_d: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    daily values.
  hltwb_m: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    monthly values.
  hltwb_y: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    yearly values.
  hltwb_a: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    average-annual values.
  lsu_wb_d: Allocatable 1-D array of `output_waterbal` — output for using components of lsus
    in ch_temp; holds daily values.
  ruwb_d: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    daily values.
  ruwb_m: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    monthly values.
  ruwb_y: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    yearly values.
  ruwb_a: Allocatable 1-D array of `output_waterbal` — see the `output_waterbal` type; holds
    average-annual values.
  bwb_d: Variable of `output_waterbal` — see the `output_waterbal` type; holds daily values.
  bwb_m: Variable of `output_waterbal` — see the `output_waterbal` type; holds monthly values.
  bwb_y: Variable of `output_waterbal` — see the `output_waterbal` type; holds yearly values.
  bwb_a: Variable of `output_waterbal` — see the `output_waterbal` type; holds average-annual
    values.
  rwb_d: Allocatable 1-D array of `regional_output_waterbal` — see the `regional_output_waterbal`
    type; holds daily values.
  rwb_m: Allocatable 1-D array of `regional_output_waterbal` — see the `regional_output_waterbal`
    type; holds monthly values.
  rwb_y: Allocatable 1-D array of `regional_output_waterbal` — see the `regional_output_waterbal`
    type; holds yearly values.
  rwb_a: Allocatable 1-D array of `regional_output_waterbal` — see the `regional_output_waterbal`
    type; holds average-annual values.
  hnb_d: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds daily
    values.
  hnb_m: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds monthly
    values.
  hnb_y: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds yearly
    values.
  hnb_a: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds average-annual
    values.
  hnbz: Variable of `output_nutbal` — see the `output_nutbal` type.
  hltnb_d: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds
    daily values.
  hltnb_m: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds
    monthly values.
  hltnb_y: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds
    yearly values.
  hltnb_a: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds
    average-annual values.
  runb_d: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds daily
    values.
  runb_m: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds monthly
    values.
  runb_y: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds yearly
    values.
  runb_a: Allocatable 1-D array of `output_nutbal` — see the `output_nutbal` type; holds average-annual
    values.
  bnb_d: Variable of `output_nutbal` — see the `output_nutbal` type; holds daily values.
  bnb_m: Variable of `output_nutbal` — see the `output_nutbal` type; holds monthly values.
  bnb_y: Variable of `output_nutbal` — see the `output_nutbal` type; holds yearly values.
  bnb_a: Variable of `output_nutbal` — see the `output_nutbal` type; holds average-annual
    values.
  rnb_d: Allocatable 1-D array of `regional_output_nutbal` — see the `regional_output_nutbal`
    type; holds daily values.
  rnb_m: Allocatable 1-D array of `regional_output_nutbal` — see the `regional_output_nutbal`
    type; holds monthly values.
  rnb_y: Allocatable 1-D array of `regional_output_nutbal` — see the `regional_output_nutbal`
    type; holds yearly values.
  rnb_a: Allocatable 1-D array of `regional_output_nutbal` — see the `regional_output_nutbal`
    type; holds average-annual values.
  hcyl_d: Allocatable 1-D array of `output_nutcarb_cycling` — see the `output_nutcarb_cycling`
    type; holds daily values.
  hcyl_m: Allocatable 1-D array of `output_nutcarb_cycling` — see the `output_nutcarb_cycling`
    type; holds monthly values.
  hcyl_y: Allocatable 1-D array of `output_nutcarb_cycling` — see the `output_nutcarb_cycling`
    type; holds yearly values.
  hcyl_a: Allocatable 1-D array of `output_nutcarb_cycling` — see the `output_nutcarb_cycling`
    type; holds average-annual values.
  hycl_z: Variable of `output_nutcarb_cycling` — see the `output_nutcarb_cycling` type.
  hls_d: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds daily
    values.
  hls_m: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds monthly
    values.
  hls_y: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds yearly
    values.
  hls_a: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds average-annual
    values.
  hlsz: Variable of `output_losses` — see the `output_losses` type.
  hltls_d: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds
    daily values.
  hltls_m: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds
    monthly values.
  hltls_y: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds
    yearly values.
  hltls_a: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds
    average-annual values.
  ruls_d: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds daily
    values.
  ruls_m: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds monthly
    values.
  ruls_y: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds yearly
    values.
  ruls_a: Allocatable 1-D array of `output_losses` — see the `output_losses` type; holds average-annual
    values.
  bls_d: Variable of `output_losses` — see the `output_losses` type; holds daily values.
  bls_m: Variable of `output_losses` — see the `output_losses` type; holds monthly values.
  bls_y: Variable of `output_losses` — see the `output_losses` type; holds yearly values.
  bls_a: Variable of `output_losses` — see the `output_losses` type; holds average-annual
    values.
  rls_d: Allocatable 1-D array of `regional_output_losses` — see the `regional_output_losses`
    type; holds daily values.
  rls_m: Allocatable 1-D array of `regional_output_losses` — see the `regional_output_losses`
    type; holds monthly values.
  rls_y: Allocatable 1-D array of `regional_output_losses` — see the `regional_output_losses`
    type; holds yearly values.
  rls_a: Allocatable 1-D array of `regional_output_losses` — see the `regional_output_losses`
    type; holds average-annual values.
  hpw_d: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather` type;
    holds daily values.
  hpw_m: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather` type;
    holds monthly values.
  hpw_y: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather` type;
    holds yearly values.
  hpw_a: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather` type;
    holds average-annual values.
  hpwz: Variable of `output_plantweather` — see the `output_plantweather` type.
  hltpw_d: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather`
    type; holds daily values.
  hltpw_m: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather`
    type; holds monthly values.
  hltpw_y: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather`
    type; holds yearly values.
  hltpw_a: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather`
    type; holds average-annual values.
  rupw_d: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather` type;
    holds daily values.
  rupw_m: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather` type;
    holds monthly values.
  rupw_y: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather` type;
    holds yearly values.
  rupw_a: Allocatable 1-D array of `output_plantweather` — see the `output_plantweather` type;
    holds average-annual values.
  bpw_d: Variable of `output_plantweather` — see the `output_plantweather` type; holds daily
    values.
  bpw_m: Variable of `output_plantweather` — see the `output_plantweather` type; holds monthly
    values.
  bpw_y: Variable of `output_plantweather` — see the `output_plantweather` type; holds yearly
    values.
  bpw_a: Variable of `output_plantweather` — see the `output_plantweather` type; holds average-annual
    values.
  rpw_d: Allocatable 1-D array of `regional_output_plantweather` — see the `regional_output_plantweather`
    type; holds daily values.
  rpw_m: Allocatable 1-D array of `regional_output_plantweather` — see the `regional_output_plantweather`
    type; holds monthly values.
  rpw_y: Allocatable 1-D array of `regional_output_plantweather` — see the `regional_output_plantweather`
    type; holds yearly values.
  rpw_a: Allocatable 1-D array of `regional_output_plantweather` — see the `regional_output_plantweather`
    type; holds average-annual values.
  wb_hdr: Variable of `output_waterbal_header` — see the `output_waterbal_header` type.
  wb_hdr_units: Variable of `output_waterbal_header_units` — see the `output_waterbal_header_units`
    type.
  nb_hdr: Variable of `output_nutbal_header` — see the `output_nutbal_header` type.
  nb_hdr_units: Variable of `output_nutbal_header_units` — see the `output_nutbal_header_units`
    type.
  ls_hdr: Variable of `output_losses_header` — see the `output_losses_header` type.
  ls_hdr_units: Variable of `output_losses_header_units` — see the `output_losses_header_units`
    type.
  nb_hdr1: Variable of `output_nutcarb_cycling_header` — see the `output_nutcarb_cycling_header`
    type.
  nb_hdr_units1: Variable of `output_nutbal_header_units1` — see the `output_nutbal_header_units1`
    type.
  carbon_hdr1: Variable of `output_carbon_header` — see the `output_carbon_header` type.
  carbon_hdr_units1: Variable of `output_carbon_header_units1` — see the `output_carbon_header_units1`
    type.
  carb_gl_hdr: Variable of `output_carb_gl_header` — see the `output_carb_gl_header` type.
  carb_gl_hdr_units: Variable of `output_carb_gl_header_units` — see the `output_carb_gl_header_units`
    type.
  hscf_hdr: Variable of `output_hscf_header` — see the `output_hscf_header` type.
  hscf_hdr_units: Variable of `output_hscf_header_units` — see the `output_hscf_header_units`
    type.
  ls_hdr1: Variable of `output_losses_header1` — see the `output_losses_header1` type.
  ls_hdr_units1: Variable of `output_losses_header_units1` — see the `output_losses_header_units1`
    type.
  pw_hdr: Variable of `output_plantweather_header` — see the `output_plantweather_header`
    type.
  pw_hdr_units: Variable of `output_plantweather_header_units` — see the `output_plantweather_header_units`
    type.
type_components:
  output_waterbal:
    precip: mm H2O        |precipitation falling as rain and snow
    snofall: mm H2O        |precipitation falling as snow, sleet or freezing rain
    snomlt: mm H2O        |snow or melting ice
    surq_gen: mm H2O        |surface runoff generated from the landscape
    latq: mm H2O        |lateral soil flow
    wateryld: mm H2O        |water yield - sum of surface runoff, lateral soil flow and tile
      flow
    perc: mm H2O        |amt of water perc out of the soil profile & into the vadose zone
    et: mm H2O        |actual evapotranspiration from the soil
    ecanopy: mm H2O        |not reported
    eplant: mm H2O        |plant transpiration
    esoil: mm H2O        |soil evaporation
    surq_cont: mm H2O        |surface runoff leaving the landscape
    cn: none          |average curve number value for timestep
    sw_init: mm H2O        |initial soil water content of soil profile at start of time step
    sw_final: mm H2O        |final soil water content of soil profile at end of time step
    sw: mm H2O        |average soil water content of soil profile
    sw_300: mm H2O        |final soil water content of upper 300 mm at end of time step
    sno_init: mm H2O        |initial soil water content of snow pack
    sno_final: mm H2O        |final soil water content of snow pack
    snopack: mm            |water equivalent in snow pack
    pet: mm H2O        |potential evapotranspiration
    qtile: mm H2O        |subsurface tile flow leaving the landscape
    irr: mm H2O        |irrigation water applied
    surq_runon: mm H2O        |surface runoff from upland landscape
    latq_runon: mm H2O        |lateral soil flow from upland landscape
    overbank: mm H2O        |overbank flooding from channels
    surq_cha: mm H2O        |surface runoff flowing into channels
    surq_res: mm H2O        |surface runoff flowing into reservoirs
    surq_ls: mm H2O        |surface runoff flowing onto the landscape
    latq_cha: mm H2O        |lateral soil flow into channels
    latq_res: mm H2O        |lateral soil flow into reservoirs
    latq_ls: mm H2O        |lateral soil flow into a landscape element
    gwsoil: mm H2O        |groundwater transferred to soil profile (when water table is in
      soil profile) !rtb gwflow
    satex: mm H2O        |saturation excess flow developed from high water table !rtb gwflow
    satex_chan: mm H2O        |saturation excess flow reaching main channel !rtb gwflow
    delsw: mm H2O        |change in soil water volume !rtb gwflow
    lagsurf: mm H2O        |surface runoff in transit to channel
    laglatq: "mm H2O\t     |lateral flow in transit to channel"
    lagsatex: "mm H2O\t     |saturation excess flow in transit to channel"
    wet_evap: "mm H2O\t     |evaporation from wetland surface"
    wet_out: "mm H2O\t     |outflow (spill) from wetland"
    wet_stor: "mm H2O\t     |volume stored in wetland at end of time period"
  regional_output_waterbal:
    lum: '|nested `output_waterbal` record'
  output_nutbal:
    grazn: kg N/ha        |total nitrogen added to soil from grazing
    grazp: kg P/ha        |total phophorous added to soil from grazing
    lab_min_p: kg P/ha        |phosphoros moving from the labile mineral pool to the active
      mineral pool
    act_sta_p: kg P/ha        |phosphorus moving from the active mineral pool to the stable
      mineral pool
    fertn: kg N/ha        |total nitrogen applied to soil
    fertp: kg P/ha        |total phosphorus applied to soil
    fixn: kg N/ha        |nitrogen added to plant biomass via fixation
    denit: kg N/ha        |nitrogen lost from nitrate pool by denitrification
    act_nit_n: kg N/ha        |nitrogen moving from active organic pool to nitrate pool
    act_sta_n: kg N/ha        |nitrogen moving from active organic pool to stable pool
    org_lab_p: kg P/ha        |phosphorus moving from the organic pool to labile pool
    rsd_nitorg_n: kg N/ha        |nitrogen moving from the fresh organic pool (residue) to
      the nitrate (80%)
    rsd_laborg_p: 'and active org (20%) pools

      kg P/ha        |phosphorus moving from the fresh organic pool (residue) to the labile
      (80%)'
    no3atmo: 'and org (20%) pools

      kg N/ha        |nitrate added to the soil from atmospheric deposition'
    nh4atmo: kg N/ha        |ammonia added to the soil from atmospheric deposition
    nuptake: kg N/ha        |plant nitrogen uptake
    puptake: kg P/ha        |plant phosphorus uptake
    gwsoiln: kg N/ha        |nitrate added to the soil from the aquifer (rtb gwflow)
    gwsoilp: kg P/ha        |Phos added to the soil from the aquifer (rtb gwflow)
  regional_output_nutbal:
    lum: '|nested `output_nutbal` record'
  output_nutcarb_cycling:
    lab_min_p: kg P/ha        |phosphorus moving from the labile mineral pool to the active
      mineral pool
    act_sta_p: kg P/ha        |phosphorus moving from the active mineral pool to the stable
      mineral pool
    act_nit_n: kg N/ha        |nitrogen moving from active organic pool to nitrate pool
    act_sta_n: kg N/ha        |nitrogen moving from active organic pool to stable pool
    org_lab_p: kg P/ha        |phosphorus moving from the organic pool to labile pool
    rsd_hs_c: kg C/ha        |amt of carbon moving from the fresh org (residue) to soil slow
      humus
    rsd_nitorg_n: kg N/ha        |nitrogen moving from the fresh organic pool (residue) to
      nitrate
    rsd_laborg_p: kg P/ha        |phosphorus moving from the fresh organic pool (residue)
      to the labile (80%)
  output_losses:
    sedyld: metric tons/ha |sediment yield leaving the landscape caused by water erosion
    sedorgn: kg N/ha        |organic nitrogen transported in surface runoff
    sedorgp: kg P/ha        |organic phosphorus transported in surface runoff
    surqno3: kg N/ha        |nitrate NO3-N transported in surface runoff
    latno3: kg N/ha        |nitrate NO3-N transported in lateral runoff
    surqsolp: kg P/ha        |soluble phosphorus transported in surface runoff
    usle: metric tons/ha |sediment erosion predicted with the USLE equation
    sedminp: kg P/ha        |mineral phosphorus leaving the landscape transported in sediment
    tileno3: kg N/ha        |nitrate NO3 in tile flow
    lchlabp: kg P/ha        |soluble P (labile) leaching past bottom soil layer
    tilelabp: kg P/ha        |soluble P (labile) in tile flow
    satexn: kg N/ha        | amt of NO3-N in saturation excess surface runoff in HRU for the
      day
  regional_output_losses:
    lum: '|nested `output_losses` record'
  output_plantweather:
    lai: m**2/m**2     |average leaf area index during timestep
    bioms: kg/ha         |average total plant biomass during timestep
    yield: kg/ha         |harvested biomass yield (dry weight) during timestep
    residue: kg/ha         |average surface residue cover during timestep
    sol_tmp: deg C         |average temperature of soil layer 2 during timestep
    strsw: days          |limiting water (drought) stress
    strsa: days          |excess water (aeration) stress
    strstmp: days          |temperature stress
    strsn: days          |nitrogen stress
    strsp: days          |phosphorus stress
    strss: days          |salinity stress
    nplnt: kg N/ha       |plant uptake of nitrogen
    percn: kg N/ha       |nitrate NO3-N leached from bottom of soil profile
    pplnt: kg P/ha       |plant uptake of phosphorus
    tmx: deg C         |average maximum temperature during timestep
    tmn: deg C         |average minimum temperature during timestep
    tmpav: deg C         |average of daily air temperature during timestep
    solrad: MJ/m^2        |average solar radiation during timestep
    wndspd: m/s           |average windspeed during timestep
    rhum: none          |average relative humidity during timestep
    phubase0: deg c/deg c   |base zero potential heat units
    lai_max: m**2/m**2     |maximum leaf area index during timestep
    bm_max: kg/ha         |maximum total plant biomass during timestep
    bm_grow: kg/ha         |total plant biomass growth during timestep
    c_gro: kg/ha         |total plant carbon growth during timestep
  regional_output_plantweather:
    lum: '|nested `output_plantweather` record'
  output_waterbal_header:
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
    precip: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    snofall: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    snomlt: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_gen: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wateryld: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    et: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    ecanopy: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    eplant: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    esoil: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_cont: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    cn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sw_init: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sw_final: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sw_ave: '|a module-level working variable holding an average value (no inline source comment;
      interpreted from the name)'
    sw_300: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sno_init: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sno_final: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    snopack: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    pet: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    qtile: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    irr: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    surq_runon: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    latq_runon: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    overbank: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_cha: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_res: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_ls: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_cha: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_res: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_ls: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gwsoilq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    satex: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    satex_chan: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    sw_change: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    lagsurf: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    laglatq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lagsatex: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wet_evap: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wet_oflo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wet_stor: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    plt_cov: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgt_ops: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_waterbal_header_units:
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
    precip: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    snofall: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    snomlt: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_gen: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wateryld: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    et: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    ecanopy: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    eplant: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    esoil: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_cont: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    cn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sw_init: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sw_final: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sw_ave: '|a module-level working variable holding an average value (no inline source comment;
      interpreted from the name)'
    sw_300: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sno_init: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sno_final: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    snopack: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    pet: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    qtile: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    irr: '|a module-level working variable holding an index/counter (no inline source comment;
      interpreted from the name)'
    surq_runon: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    latq_runon: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    overbank: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_cha: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_res: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_ls: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_cha: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_res: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_ls: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gwsoilq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    satex: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    satex_chan: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    sw_change: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    lagsurf: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    laglatq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lagsatex: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wet_evap: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wet_oflo: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wet_stor: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_nutbal_header:
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
    grazn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    grazp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lab_min_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_sta_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    fertn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fertp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fixn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    denit: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    act_nit_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_sta_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    org_lab_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_nitorg_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_laborg_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    no3atmo: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    nh4atmo: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    nuptake: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    puptake: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gwsoiln: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gwsoilp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    plt_cov: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgt_ops: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_nutbal_header_units:
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
    grazn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    grazp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lab_min_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_sta_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    fertn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fertp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fixn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    denit: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    act_nit_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_sta_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    org_lab_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_nitorg_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_laborg_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    no3atmo: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    nh4atmo: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    nuptake: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    puptake: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gwsoiln: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    gwsoilp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_losses_header:
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
    sedyld: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surqno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surqsolp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    usle: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedminp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tileno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lchlabp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tilelabp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    satexn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    plt_cov: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgt_ops: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    percn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_losses_header_units:
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
    sedyld: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surqno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surqsolp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    usle: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedmin: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tileno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lchlabp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tilelabp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    satexn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    plt_cov: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgt_ops: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    percn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_nutcarb_cycling_header:
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
    lab_min_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_sta_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_nit_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_sta_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    org_lab_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_hs_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    rsd_nitorg_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_laborg_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
  output_nutbal_header_units1:
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
    lab_min_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_sta_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_nit_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    act_sta_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    org_lab_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_hs_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    rsd_nitorg_n: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_laborg_p: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
  output_carbon_header:
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
    sed_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_doc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_dic: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_doc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_dic: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc_doc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc_dic: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    npp_c: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    rsd_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    grain_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    stover_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    rsp_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    emit_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_carbon_header_units1:
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
    sed_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_doc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_dic: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_doc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_dic: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc_doc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc_dic: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    npp_c: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    rsd_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    grain_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    stover_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    rsp_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    emit_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_carb_gl_header:
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
    sed_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    res_decay: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    man_app_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    man_graze_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsp_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    soil_emit_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    plant_surf_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    plant_root_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_surfdecay_c: '|a module-level working variable shared across the importing routines
      (no inline source comment in the declaration)'
    rsd_rootdecay_c: '|a module-level working variable shared across the importing routines
      (no inline source comment in the declaration)'
    harv_stov_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_emit_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    npp_c: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    harv_abgr_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    harv_root_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    drop_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    grazeat_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    plant_emit_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
  output_carb_gl_header_units:
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
    sed_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surq_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latq_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    perc_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    res_decay: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    man_app_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    man_graze_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsp_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    soil_emit_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    plant_surf_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    plant_root_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_surfdecay_c: '|a module-level working variable shared across the importing routines
      (no inline source comment in the declaration)'
    rsd_rootdecay_c: '|a module-level working variable shared across the importing routines
      (no inline source comment in the declaration)'
    harv_stov_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    rsd_emit_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    npp_c: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    harv_abgr_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    harv_root_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    drop_c: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    grazeat_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    plant_emit_c: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
  output_hscf_header:
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
    meta_micr: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    str_micr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    str_hs: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_meta: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_str: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    micr_hs: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    micr_hp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hs_micr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hs_hp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hp_micr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_micr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_hs: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_hp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_hscf_header_units:
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
    meta_micr: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    str_micr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    str_hs: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_meta: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_str: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    micr_hs: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    micr_hp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hs_micr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hs_hp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hp_micr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_micr: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_hs: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co2_hp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_losses_header1:
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
    sedyld: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    usle: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surqno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surqsolp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedminp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tileno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    no3atmo: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    nh4atmo: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    manurec: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    manuren: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    manurep: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fertc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fertn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fertp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    grazc_eat: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    gracn_eat: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    gracp_eat: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    grazc_man: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    gracn_man: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    gracp_man: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    fixn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    denit: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yieldc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yieldn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yieldp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_losses_header_units1:
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
    sedyld: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    usle: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedorgp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surqno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    latno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    surqsolp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sedmin: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tileno3: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    no3atmo: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    nh4atmo: '|a module-level working variable holding a count (no inline source comment;
      interpreted from the name)'
    manurec: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    manuren: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    manurep: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fertc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fertn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    fertp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    grazc_eat: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    gracn_eat: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    gracp_eat: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    grazc_man: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    gracn_man: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    gracp_man: '|a module-level working variable shared across the importing routines (no
      inline source comment in the declaration)'
    fixn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    denit: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yieldc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yieldn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yieldp: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_plantweather_header:
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
    lai: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bioms: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yield: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    residue: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sol_tmp: '|a module-level working variable holding a temperature or temporary value (no
      inline source comment; interpreted from the name)'
    strsw: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strsa: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strstmp: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strsn: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strsp: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strss: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    nplnt: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    percn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    pplnt: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tmx: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tmn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tmpav: '|a module-level working variable holding a temperature or temporary value (no
      inline source comment; interpreted from the name)'
    solrad: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wndspd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    rhum: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    phubase0: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lai_max: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bm_max: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bm_grow: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    c_gro: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    plt_cov: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgt_ops: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  output_plantweather_header_units:
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
    lai: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bioms: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    yield: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    residue: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sol_tmp: '|a module-level working variable holding a temperature or temporary value (no
      inline source comment; interpreted from the name)'
    strsw: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strsa: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strstmp: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strsn: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strsp: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    strss: '|a module-level working variable holding a plant/soil stress value (no inline
      source comment; interpreted from the name)'
    nplnt: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    percn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    pplnt: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tmx: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tmn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    tmpav: '|a module-level working variable holding a temperature or temporary value (no
      inline source comment; interpreted from the name)'
    solrad: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    wndspd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    rhum: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    phubase0: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    lai_max: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bm_max: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bm_grow: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    c_gro: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
type_summaries:
  output_waterbal: One `output_waterbal` record groups `precip`, `snofall`, `snomlt`, `surq_gen`,
    `latq`, `wateryld`, and 36 more fields.
  regional_output_waterbal: One `regional_output_waterbal` record groups `lum`.
  output_nutbal: One `output_nutbal` record groups `grazn`, `grazp`, `lab_min_p`, `act_sta_p`,
    `fertn`, `fertp`, and 13 more fields.
  regional_output_nutbal: One `regional_output_nutbal` record groups `lum`.
  output_nutcarb_cycling: One `output_nutcarb_cycling` record groups `lab_min_p`, `act_sta_p`,
    `act_nit_n`, `act_sta_n`, `org_lab_p`, `rsd_hs_c`, and 2 more fields.
  output_losses: One `output_losses` record groups `sedyld`, `sedorgn`, `sedorgp`, `surqno3`,
    `latno3`, `surqsolp`, and 6 more fields.
  regional_output_losses: One `regional_output_losses` record groups `lum`.
  output_plantweather: One `output_plantweather` record groups `lai`, `bioms`, `yield`, `residue`,
    `sol_tmp`, `strsw`, and 19 more fields.
  regional_output_plantweather: One `regional_output_plantweather` record groups `lum`.
  output_waterbal_header: One `output_waterbal_header` record groups `day`, `mo`, `day_mo`,
    `yrc`, `isd`, `id`, and 45 more fields.
  output_waterbal_header_units: One `output_waterbal_header_units` record groups `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 43 more fields.
  output_nutbal_header: One `output_nutbal_header` record groups `day`, `mo`, `day_mo`, `yrc`,
    `isd`, `id`, and 22 more fields.
  output_nutbal_header_units: One `output_nutbal_header_units` record groups `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 20 more fields.
  output_losses_header: One `output_losses_header` record groups `day`, `mo`, `day_mo`, `yrc`,
    `isd`, `id`, and 16 more fields.
  output_losses_header_units: One `output_losses_header_units` record groups `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 16 more fields.
  output_nutcarb_cycling_header: One `output_nutcarb_cycling_header` record groups `day`,
    `mo`, `day_mo`, `yrc`, `isd`, `id`, and 9 more fields.
  output_nutbal_header_units1: One `output_nutbal_header_units1` record groups `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 9 more fields.
  output_carbon_header: Carbon output. Holds `day`, `mo`, `day_mo`, `yrc`, `isd`, `id`, and
    17 more fields.
  output_carbon_header_units1: One `output_carbon_header_units1` record groups `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 17 more fields.
  output_carb_gl_header: One `output_carb_gl_header` record groups `day`, `mo`, `day_mo`,
    `yrc`, `isd`, `id`, and 22 more fields.
  output_carb_gl_header_units: One `output_carb_gl_header_units` record groups `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 22 more fields.
  output_hscf_header: One `output_hscf_header` record groups `day`, `mo`, `day_mo`, `yrc`,
    `isd`, `id`, and 14 more fields.
  output_hscf_header_units: One `output_hscf_header_units` record groups `day`, `mo`, `day_mo`,
    `yrc`, `isd`, `id`, and 14 more fields.
  output_losses_header1: One `output_losses_header1` record groups `day`, `mo`, `day_mo`,
    `yrc`, `isd`, `id`, and 30 more fields.
  output_losses_header_units1: One `output_losses_header_units1` record groups `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 30 more fields.
  output_plantweather_header: One `output_plantweather_header` record groups `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 28 more fields.
  output_plantweather_header_units: One `output_plantweather_header_units` record groups `day`,
    `mo`, `day_mo`, `yrc`, `isd`, `id`, and 26 more fields.
---

<!-- facts:header -->

`output_landscape_module` owns the landscape output record types reported at the HRU and region level — water balance (`output_waterbal`), nutrient balance (`output_nutbal`), losses (`output_losses`), plant/weather (`output_plantweather`), and nutrient-carbon cycling (`output_nutcarb_cycling`) — their regional variants, and the header/units records, together with the daily/monthly/yearly/average-annual instances. The arrays are allocated during setup and accumulated and written by the HRU output routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container. The output-record types default to zero in their declarations, and the daily/monthly/yearly/average-annual arrays are allocated during output setup; the header and units records are initialized with their column labels in the module.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `actions`. |
| [sym:aqu_pesticide_output] | `unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `aqu_pesticide_output`. |
| [sym:basin_aqu_pest_output] | `unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `basin_aqu_pest_output`. |
| [sym:basin_ch_pest_output] | `unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `basin_ch_pest_output`. |
| [sym:basin_ls_pest_output] | `unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `basin_ls_pest_output`. |
| [sym:basin_output] | `unit_2050, unit_2054, unit_2060, unit_2064, unit_2070, unit_2074, unit_2080, unit_2084, unit_2051, unit_2055, unit_2061, unit_2065, unit_2071, unit_2075, unit_2081, unit_2085, unit_2052, unit_2056, unit_2062, unit_2066, unit_2072, unit_2076, unit_2082, unit_2086, unit_2053, unit_2057, unit_2063, unit_2067, unit_2073, unit_2077, unit_2083, unit_2087` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Writes output from `output_landscape_module` state: references `bwb_d`, `hwbz`, `bnb_d`, `hnbz` (e.g. `basin_output.f90:19`). |
| [sym:basin_res_pest_output] | `unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `basin_res_pest_output`. |
| [sym:basin_sw_init] | `no direct file input (operates on in-memory state)` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Initializes `output_landscape_module` state: references `hwb_d`, `hwb_m`, `hwb_y`, `hwb_a` (e.g. `basin_sw_init.f90:22`). |
| [sym:ch_cs_output] | `unit_6030, unit_6031, unit_6032, unit_6033, unit_6034, unit_6035, unit_6036, unit_6037` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `ch_cs_output`. |
| [sym:ch_salt_output] | `unit_5030, unit_5031, unit_5032, unit_5033, unit_5034, unit_5035, unit_5036, unit_5037` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `ch_salt_output`. |
| [sym:cha_pesticide_output] | `unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `cha_pesticide_output`. |
| [sym:cs_balance] | `unit_6080, unit_6082, unit_6084, unit_6086` | `h, hwb_d, hwb_m, hwb_y, hwb_a, hwbz` | Imports `output_landscape_module`; no specific module symbol from it was resolved in the extracted references for `cs_balance`. |

## Key Consumers

Importers are mainly the HRU and region output routines that accumulate the water-balance, nutrient-balance, loss, plant/weather, and nutrient-carbon-cycling records and write the daily/monthly/yearly/average-annual landscape output files, plus the header writers.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_output] | output_landscape_module | These basin and landscape output records hold the daily, monthly, yearly, and average-annual water-balance, nutrient-balance, losses, and plant-weather values that `basin_output` accumulates, resets, scales, and writes. |
| [sym:basin_sw_init] | output_landscape_module | These water-balance records are the destination for the initial soil-water and snow-water values that the rest of the output system will compare against during daily, monthly, yearly, and annual reporting. |
| [sym:hru_lte_control] | output_landscape_module | Receives the daily water-balance and loss outputs produced by this routine. |
| [sym:hru_lte_output] | output_landscape_module | `output_landscape_module` contains the HRU-LTE accumulation arrays and zero-state templates that this routine updates and resets. Those arrays are the actual water-balance, nutrient-balance, losses, and plant-weather states being reported. |
| [sym:hru_lte_read] | output_landscape_module | The `output_landscape_module` contains the landscape water-balance arrays that are allocated to match the number of HRU LTE objects. `hltwb_d`, `hltwb_m`, `hltwb_y`, and `hltwb_a` are initialized here because later output routines need per-object storage for soil-water diagnostics such as `sw_init`. |
| [sym:hru_output] | output_landscape_module | Supplies the HRU output accumulator arrays and zero-state templates that are summed, averaged, reset, and written by this routine. |
| [sym:lcu_read_softcal] | output_landscape_module | These output containers are allocated to the same region count so later landscape reporting can store annual water, nutrient, loss, and plant/weather summaries for each landuse within each region. |
| [sym:lsreg_output] | output_landscape_module | `output_landscape_module` provides the regional output arrays that this routine fills and prints. The daily, monthly, yearly, and average-annual water balance, nutrient balance, loss, and plant-weather structures are all stored in `rwb_*`, `rnb_*`, `rls_*`, and `rpw_*` arrays before being written to output units. |
| [sym:lsu_output] | output_landscape_module | `output_landscape_module` owns the daily, monthly, yearly, and average-annual LSU result containers that this routine fills and then writes. The routine reads member HRU/HRU_LTE outputs from the HRU arrays and stores the aggregated LSU values in the `ruwb_*`, `runb_*`, `ruls_*`, and `rupw_*` structures before output. |
| [sym:lsu_read_elements] | output_landscape_module | output_landscape_module provides the LSU-level output arrays that are allocated here using the LSU count so later landscape output can store water, nutrient, loss, and plant-weather balances per LSU. |
| [sym:reg_read_elements] | output_landscape_module | The landscape output arrays are dimensioned by region and land-use group here so later accumulated water-balance, nutrient, loss, and plant-weather reporting has storage for each regional land-use bin. |
| [sym:aqu_pesticide_output] | output_landscape_module | This module is imported as part of the landscape output subsystem, so it matters to the routine’s output placement even though no direct symbol references were extracted from it in the source snippet. |
| [sym:basin_aqu_pest_output] | output_landscape_module | `output_landscape_module` is imported in the source but no direct symbols from it are visible in the extracted lines. It is therefore a declared dependency without a shown in-routine use. |
| [sym:basin_ch_pest_output] | output_landscape_module | This module is a dependency of the pesticide output path, so it provides shared landscape-output definitions or interfaces used by the broader output system even though no specific symbol from it is referenced in the extracted source lines. |
| [sym:basin_ls_pest_output] | output_landscape_module | `output_landscape_module` is imported but no symbol from it is referenced in the extracted source lines, so it does not affect the visible logic of this routine. |
| [sym:basin_res_pest_output] | output_landscape_module | The module is imported but no symbol from it appears in the extracted source lines, so it does not affect the visible output control or data accumulation. |
| [sym:ch_cs_output] | output_landscape_module | `output_landscape_module` is imported, but the extracted lines show no referenced symbols from it. It appears to be part of the broader output infrastructure rather than a directly used data source in this routine. |
| [sym:ch_salt_output] | output_landscape_module | The module is imported, but no specific symbol from it appears in the extracted source. It still matters as a dependency because the routine belongs to the broader output subsystem and may rely on shared output definitions from this module. |
| [sym:cha_pesticide_output] | output_landscape_module | No candidate state from `output_landscape_module` was resolved in the context packet, so there is no source-backed module member to describe for this routine. |
| [sym:cs_balance] | output_landscape_module | This module supplies the groundwater-flow switch used to choose between gwflow-based and legacy aquifer accounting, and it holds the monthly, yearly, and average-annual accumulator arrays that cs_balance updates and then resets. |
| [sym:hru_carbon_output] | output_landscape_module | The module is imported in the source, but no symbol from `output_landscape_module` is directly referenced in the extracted procedure body. It is therefore a surrounding dependency for the landscape output framework, not a visible line-level dependency here. |
| [sym:hru_pathogen_output] | output_landscape_module | The module is imported but no extracted symbol from it appears in the visible routine body, so no direct state usage can be confirmed from the supplied evidence. |
| [sym:hru_pesticide_output] | output_landscape_module | `output_landscape_module` is imported but no explicit symbol from it appears in the extracted lines. It likely participates in the broader landscape output framework that this HRU routine belongs to, even though the visible code does not directly reference one of its named objects. |
| [sym:lsu_carbon_output] | output_landscape_module | The routine imports `output_landscape_module`, but the packet does not show a specific symbol from that module being referenced in the visible source. It likely provides shared output infrastructure or file handles for landscape-level output, but the exact dependency is not identifiable from the extracted evidence. |

## Lineage

`output_landscape_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 59 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `output_landscape_module.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `c3a99cb` (2026-05-15) — Updated code to include root_mass in hru_cpool output and in jupyter notebook code. Removed hru_rsdc graphs from jupyter notebook.
- `a96057d` (2026-05-15) — Fixed issue of tillagef not being initialized to 0. in cbn_zhang2. Corrected mgt_biomass to correctly reflect the potentional bio mixing for…
- `28c64c3` (2026-05-14) — Removed output files no longer needed. hru_soilc_stat hru_rsdc_stat, hru_soilcarb_mb_stat
- `e7b610a` (2026-05-13) — Finished changing code to output files to reflect lignin and non lignin n, c, and p amounts.
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `output_landscape_module` has no extracted module-level documentation comment.
- Reader rows show 12 candidate initialization/read routines out of 37; treat the table as representative, not exhaustive.
- This module is imported by 65 procedures; the main Used By table shows 24 ranked consumers and the collapsible importer list keeps the complete deterministic list.
- variable_notes and type_notes summaries were completed locally from the module's declaration metadata (type, shape, source comments) and the Derived Type Inventory; reader behaviors were grounded in source references found in each reader. 0 module-level scalar(s) had no inline source comment and were given name-based interpretations — these should be spot-checked.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
