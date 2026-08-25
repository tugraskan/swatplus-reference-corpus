---
kind: module
symbol: constituent_mass_module
title: constituent_mass_module
status: filled
source_hash: e152518356a9c0ba
version_label: SWAT+ 62.0.0
variables:
  pest_init_name: Character allocatable 1-D array — a module-level working variable shared
    across the importing routines (no inline source comment in the declaration).
  path_init_name: Character allocatable 1-D array — a module-level working variable shared
    across the importing routines (no inline source comment in the declaration).
  hmet_init_name: Character allocatable 1-D array — a module-level working variable shared
    across the importing routines (no inline source comment in the declaration).
  salt_init_name: Character allocatable 1-D array — a module-level working variable shared
    across the importing routines (no inline source comment in the declaration).
  cs_init_name: Character allocatable 1-D array holding rtb cs.
  cs_db: Variable of `constituents` — see the `constituents` type.
  exco_pest: Allocatable 1-D array of `exco_pesticide` — export coefficients.
  dr_pest: Allocatable 1-D array of `dr_pesticide` — delivery ratios.
  exco_path: Allocatable 1-D array of `exco_pathogens` — export coefficients.
  dr_path: Allocatable 1-D array of `dr_pathogens` — delivery ratios.
  exco_hmet: Allocatable 1-D array of `exco_heavy_metals` — export coefficients.
  dr_hmet: Allocatable 1-D array of `dr_heavy_metals` — delivery ratios.
  exco_salt: Allocatable 1-D array of `exco_salts` — export coefficients.
  dr_salt: Allocatable 1-D array of `dr_salts` — delivery ratios.
  sol_salt_solid: Allocatable 1-D array of `salt_solids_soil` — salt solid by hru.
  cs_irr: Allocatable 1-D array of `constituent_mass` — irrigation water constituent mass
    - dimensioned by hru.
  cs_soil: Allocatable 1-D array of `soil_constituent_mass` — see the `soil_constituent_mass`
    type.
  cs_pl: Allocatable 1-D array of `plant_constituent_mass` — see the `plant_constituent_mass`
    type.
  cs_aqu: Allocatable 1-D array of `constituent_mass` — aquifer constituent mass.
  cs_aqu_init: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type.
  ch_water: Allocatable 1-D array of `constituent_mass` — storing water and benthic constituents
    in channel.
  ch_benthic: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type.
  ch_water_init: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass`
    type.
  ch_benthic_init: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass`
    type.
  wtp_cs_stor: Allocatable 1-D array of `constituent_mass` — water treatment plant storage.
  wtp_cs_treat: Allocatable 1-D array of `constituent_mass` — water treatment plant treated
    concentrations.
  wuse_cs_stor: Allocatable 1-D array of `constituent_mass` — water use storage.
  wuse_cs_efflu: Allocatable 1-D array of `constituent_mass` — water use effluent concentrations.
  osrc_cs: Allocatable 1-D array of `constituent_mass` — outside source constituents.
  canal_cs_stor: Allocatable 1-D array of `constituent_mass` — canal storage.
  wtow_cs_stor: Allocatable 1-D array of `constituent_mass` — water tower storage.
  wdraw_cs: Variable of `constituent_mass` — water withdrawn from an individual source.
  wdraw_cs_tot: Variable of `constituent_mass` — total water withdrawn from all sources.
  outflo_cs: Variable of `constituent_mass` — constituent outflow from an water allocation
    object - wtp or use.
  res_water: Allocatable 1-D array of `constituent_mass` — storing salt and constituent mass
    in reservoirs.
  res_benthic: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type.
  wet_water: Allocatable 1-D array of `constituent_mass` — storing salt and constituent mass
    in wetlands.
  hcs1: Variable of `constituent_mass` — hydrographs used in command for adding incoming hyds.
  hcs2: Variable of `constituent_mass` — hydrographs used in command for adding incoming hyds.
  hcs3: Variable of `constituent_mass` — hydrographs used in command for adding incoming hyds.
  hin_csz: Variable of `constituent_mass` — set zero constituent hydrograph.
  obcs: Allocatable 1-D array of `all_constituent_hydrograph` — see the `all_constituent_hydrograph`
    type.
  obcs_alloc: Integer allocatable 1-D array holding array for indicating if object has obcs
    allocated.
  aq_chcs: Allocatable 1-D array of `gw_load_hydrograph` — see the `gw_load_hydrograph` type.
  hcsz: Variable of `all_constituent_hydrograph` — set zero all constituent hydrograph.
  rusaltb_d: Allocatable 1-D array of `all_constituent_hydrograph` — routing unit salt mass
    (rtb salt); holds daily values.
  rusaltb_m: Allocatable 1-D array of `all_constituent_hydrograph` — see the `all_constituent_hydrograph`
    type; holds monthly values.
  rusaltb_y: Allocatable 1-D array of `all_constituent_hydrograph` — see the `all_constituent_hydrograph`
    type; holds yearly values.
  rusaltb_a: Allocatable 1-D array of `all_constituent_hydrograph` — see the `all_constituent_hydrograph`
    type; holds average-annual values.
  rucsb_d: Allocatable 1-D array of `all_constituent_hydrograph` — routing unit constituent
    mass (rtb cs); holds daily values.
  rucsb_m: Allocatable 1-D array of `all_constituent_hydrograph` — see the `all_constituent_hydrograph`
    type; holds monthly values.
  rucsb_y: Allocatable 1-D array of `all_constituent_hydrograph` — see the `all_constituent_hydrograph`
    type; holds yearly values.
  rucsb_a: Allocatable 1-D array of `all_constituent_hydrograph` — see the `all_constituent_hydrograph`
    type; holds average-annual values.
  rec_salt: Allocatable 1-D array of `recall_salt_inputs` — see the `recall_salt_inputs` type.
  rec_cs: Allocatable 1-D array of `recall_cs_inputs` — see the `recall_cs_inputs` type.
  recsaltb_d: Allocatable 1-D array of `constituent_mass` — salt balance arrays (rtb salt)
    point sources originating from within the watershed (e.g. WWTP effluent); holds daily
    values.
  recsaltb_m: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds monthly values.
  recsaltb_y: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds yearly values.
  recsaltb_a: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds average-annual values.
  recoutsaltb_d: Allocatable 1-D array of `constituent_mass` — point sources originating from
    outside the watershed (e.g. inflow from upstream watersheds); holds daily values.
  recoutsaltb_m: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass`
    type; holds monthly values.
  recoutsaltb_y: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass`
    type; holds yearly values.
  recoutsaltb_a: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass`
    type; holds average-annual values.
  reccsb_d: Allocatable 1-D array of `constituent_mass` — constituent balance arrays (rtb
    cs) point sources originating from within the watershed (e.g. WWTP effluent); holds daily
    values.
  reccsb_m: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds monthly values.
  reccsb_y: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds yearly values.
  reccsb_a: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds average-annual values.
  recoutcsb_d: Allocatable 1-D array of `constituent_mass` — point sources originating from
    outside the watershed (e.g. inflow from upstream watersheds); holds daily values.
  recoutcsb_m: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds monthly values.
  recoutcsb_y: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds yearly values.
  recoutcsb_a: Allocatable 1-D array of `constituent_mass` — see the `constituent_mass` type;
    holds average-annual values.
  rec_pest: Allocatable 1-D array of `recall_pesticide_inputs` — see the `recall_pesticide_inputs`
    type.
  pest_soil_ini: Allocatable 1-D array of `cs_soil_init_concentrations` — see the `cs_soil_init_concentrations`
    type.
  path_soil_ini: Allocatable 1-D array of `cs_soil_init_concentrations` — see the `cs_soil_init_concentrations`
    type.
  hmet_soil_ini: Allocatable 1-D array of `cs_soil_init_concentrations` — see the `cs_soil_init_concentrations`
    type.
  salt_soil_ini: Allocatable 1-D array of `cs_soil_init_concentrations` — first 8 values of
    soil and plt are salt ion concentrations and next 5 are salt mineral fractions.
  cs_soil_ini: Allocatable 1-D array of `cs_soil_init_concentrations` — rtb cs.
  salt_aqu_ini: Allocatable 1-D array of `salt_aqu_init_concentrations` — see the `salt_aqu_init_concentrations`
    type.
  cs_aqu_ini: Allocatable 1-D array of `cs_aqu_init_concentrations` — see the `cs_aqu_init_concentrations`
    type.
  salt_cha_ini: Allocatable 1-D array of `salt_cha_init_concentrations` — see the `salt_cha_init_concentrations`
    type.
  cs_cha_ini: Allocatable 1-D array of `cs_cha_init_concentrations` — see the `cs_cha_init_concentrations`
    type.
  pest_water_ini: Allocatable 1-D array of `cs_water_init_concentrations` — see the `cs_water_init_concentrations`
    type.
  path_water_ini: Allocatable 1-D array of `cs_water_init_concentrations` — see the `cs_water_init_concentrations`
    type.
  hmet_water_ini: Allocatable 1-D array of `cs_water_init_concentrations` — see the `cs_water_init_concentrations`
    type.
  salt_water_irr: Allocatable 1-D array of `cs_irrigation_concentrations` — see the `cs_irrigation_concentrations`
    type.
  cs_water_irr: Allocatable 1-D array of `cs_irrigation_concentrations` — see the `cs_irrigation_concentrations`
    type.
  cs_obs_file: Integer scalar — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  cs_str_nobs: Integer scalar — a module-level working variable shared across the importing
    routines (no inline source comment in the declaration).
  cs_str_obs: Integer allocatable 1-D array — a module-level working variable shared across
    the importing routines (no inline source comment in the declaration).
  rusaltb_hdr: Variable of `output_rusaltb_header` — see the `output_rusaltb_header` type.
  rucsb_hdr: Variable of `output_rucsb_header` — see the `output_rucsb_header` type.
  csin_hyd_hdr: Variable of `constituents_header_in` — see the `constituents_header_in` type.
  csout_hyd_hdr: Variable of `constituents_header_out` — see the `constituents_header_out`
    type.
  cs_pest_solsor: Allocatable 1-D array of `sol_sor` — see the `sol_sor` type.
  cs_path_solsor: Allocatable 1-D array of `sol_sor` — see the `sol_sor` type.
  cs_hmet_solsor: Allocatable 1-D array of `sol_sor` — see the `sol_sor` type.
  cs_salt_solsor: Allocatable 1-D array of `sol_sor` — see the `sol_sor` type.
type_components:
  constituents:
    num_tot: number of total constituents simulated
    num_pests: number of pesticides simulated
    pests: name of the pesticides- points to pesticide database
    pest_num: 'need to crosswalk pests to get pest_num for database - use sequential for object

      number of the pesticides- points to pesticide database'
    num_paths: number of pathogens simulated
    paths: name of the pathogens- points to pathogens database
    path_num: number of the pathogens- points to pathogens database
    num_metals: number of heavy metals simulated
    metals: name of the heavy metals- points to heavy metals database
    metals_num: number of the heavy metals- points to heavy metals database
    num_salts: number of salt ions simulated
    salts: name of the salts - points to salts database
    salts_num: number of the salts - points to salts database
    num_cs: number of other constituents simulated
    cs: name of the constituents - points to cs database
    cs_num: number of the constituents - points to salts database
  exco_pesticide:
    pest: pesticide hydrographs
  dr_pesticide:
    pest: pesticide delivery
  exco_pathogens:
    path: pesticide hydrographs
  dr_pathogens:
    path: pathogen delivery
  exco_heavy_metals:
    hmet: heavy metals hydrographs
  dr_heavy_metals:
    hmet: heavy metals delivery
  exco_salts:
    salt: salts hydrographs
  dr_salts:
    salt: salts delivery
  salt_solids_soil:
    solid: salt solid by soil layer
  constituent_mass:
    pest: pesticide (kg/ha)
    path: pathogen (cfu)
    hmet: heavy metal (kg/ha)
    salt: salt ion mass (kg/ha)
    salt_min: salt mineral hydrographs
    saltc: salt ion concentrations (mg/L)
    cs: constituent mass (kg/ha)
    csc: constituent concentration (mg/L)
    cs_sorb: sorbed constituent mass (kg/ha)
    csc_sorb: sorbed constituent concentration (mg/kg)
  soil_constituent_mass:
    ly: '|nested `constituent_mass` record'
  plant_constituent_mass:
    pl_in: constituent in plant
    pl_on: constituent on plant
    pl_up: constituent uptake by plant
  all_constituent_hydrograph:
    hd: '|nested `constituent_mass` record'
    hin: '|nested `constituent_mass` record'
    hin_sur: '|nested `constituent_mass` record'
    hin_lat: '|nested `constituent_mass` record'
    hin_til: '|nested `constituent_mass` record'
    hin_aqu: '|nested `constituent_mass` record'
    hcsin_d: '|nested `constituent_mass` record'
    hcsin_m: '|nested `constituent_mass` record'
    hcsin_y: '|nested `constituent_mass` record'
    hcsin_a: '|nested `constituent_mass` record'
    hcsout_m: '|nested `constituent_mass` record'
    hcsout_y: '|nested `constituent_mass` record'
    hcsout_a: '|nested `constituent_mass` record'
  gw_load_hydrograph:
    hd: '|nested `constituent_mass` record'
  recall_salt_inputs:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    typ: recall type - 1=day, 2=mon, 3=year
    filename: filename
    start_yr: start year of point source file
    end_yr: end year of point source file
    pts_type: 1 = within watershed; 2 = from outside watershed
    hd_salt: '|nested `constituent_mass` record'
  recall_cs_inputs:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    typ: recall type - 1=day, 2=mon, 3=year
    filename: filename
    start_yr: start year of point source file
    end_yr: end year of point source file
    pts_type: 1 = within watershed; 2 = from outside watershed
    hd_cs: '|nested `constituent_mass` record'
  recall_pesticide_inputs:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    num: number of elements
    typ: recall type - 1=day, 2=mon, 3=year
    filename: filename
    hd_pest: hyd_output units are in cms and mg/L
  cs_soil_init_concentrations:
    name: name of the constituent - points to constituent database
    soil: ppm                  |amount of constituent in soil at start of simulation
    plt: 'ppm or #cfu/m^2      |amount of constituent on plant at start of simulation'
  salt_aqu_init_concentrations:
    name: name of the constituent - points to constituent database
    conc: g/m3                 |salt ion concentration at start of simulation
    frac: fractions            |salt mineral fractions at start of simulation
  cs_aqu_init_concentrations:
    name: name of the constituent - points to constituent database
    aqu: ppm                  |concentration, sorbed mass at start of simulation
  salt_cha_init_concentrations:
    name: name of the constituent - points to salt ion database
    conc: g/m3                 |salt ion concentration at start of simulation
  cs_cha_init_concentrations:
    name: name of the constituent - points to salt ion database
    conc: g/m3                 |constituent concentration at start of simulation
  cs_water_init_concentrations:
    name: name of the constituent - points to constituent database
    water: ppm,fracitons        |amount of constituents (dissolved, salt minerals) in aquifer
      at start of simulation
    benthic: 'ppm or #cfu/m^2      |amount of constituent in benthic at start of simulation'
    reservoir: ppm                  |amount of constituent in reservoir water at start of
      simulation
  cs_irrigation_concentrations:
    name: name of the constituent - points to constituent database
    water: ppm                  |amount of constituent in water at start of simulation
  output_rusaltb_header:
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
    so4tot: total salt out (surq + latq + tile) --> see hru_hyds subroutine
    castot: '|a module-level working variable holding a total (no inline source comment; interpreted
      from the name)'
    mgstot: '|a module-level working variable holding a total (no inline source comment; interpreted
      from the name)'
    nastot: '|a module-level working variable holding a total (no inline source comment; interpreted
      from the name)'
    kstot: '|a module-level working variable holding a total (no inline source comment; interpreted
      from the name)'
    clstot: '|a module-level working variable holding a total (no inline source comment; interpreted
      from the name)'
    co3stot: '|a module-level working variable holding a total (no inline source comment;
      interpreted from the name)'
    hco3stot: '|a module-level working variable holding a total (no inline source comment;
      interpreted from the name)'
    so4pc: percolation
    capc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgpc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    napc: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kpc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clpc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3pc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3pc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4sq: surface runoff
    casq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgsq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    nasq: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    ksq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clsq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3sq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3sq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4lq: lateral flow
    calq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mglq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    nalq: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    klq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    cllq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3lq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3lq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4tq: tile flow
    catq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgtq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    natq: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    ktq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    cltq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3tq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3tq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4ws: wetland seepage to soil profile
    caws: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgws: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    naws: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kws: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clws: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3ws: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3ws: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4is: irrigation (surface water)
    cais: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgis: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    nais: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kis: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clis: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3is: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3is: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4ig: irrigation (groundwater)
    caig: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgig: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    naig: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kig: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clig: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3ig: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3ig: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4io: irrigation (outside watershed)
    caio: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgio: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    naio: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kio: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clio: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3io: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3io: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4rn: rainfall (wet deposition)
    carn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgrn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    narn: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    krn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clrn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3rn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3rn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4dd: dry deposition
    cadd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgdd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    nadd: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kdd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    cldd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3dd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3dd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4rd: road salt application
    card: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgrd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    nard: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    krd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clrd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3rd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3rd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4fz: fertilizer application
    cafz: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgfz: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    nafz: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kfz: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clfz: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3fz: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3fz: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4am: soil salt amendments
    caam: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgam: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    naam: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kam: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clam: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3am: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3am: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    so4up: plant salt uptake
    caup: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    mgup: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    naup: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    kup: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    clup: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    co3up: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    hco3up: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    dssl: salt mineral dissolution and precipitation
  output_rucsb_header:
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
    seo4tot: total cs out (surq + latq + tile) --> see hru_hyds subroutine
    seo3tot: '|a module-level working variable holding a total (no inline source comment;
      interpreted from the name)'
    borntot: '|a module-level working variable holding a total (no inline source comment;
      interpreted from the name)'
    seo4pc: percolation
    seo3pc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornpc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4sq: surface runoff
    seo3sq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornsq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4lq: lateral flow
    seo3lq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornlq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4tq: tile flow
    seo3tq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    borntq: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4sd: sediment runoff
    seo3sd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornsd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4ws: wetland seepage to soil profile
    seo3ws: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornws: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4is: irrigation (surface water)
    seo3is: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornis: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4ig: irrigation (groundwater)
    seo3ig: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornig: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4io: irrigation (outside watershed)
    seo3io: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornio: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4rn: rainfall (wet deposition)
    seo3rn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornrn: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4dd: dry deposition
    seo3dd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    borndd: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4fz: fertilizer
    seo3fz: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornfz: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4up: plant selenium uptake
    seo3up: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornup: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4rc: chemical reactions
    seo3rc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornrc: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    seo4sb: mass transfer from sorption
    seo3sb: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    bornsb: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  constituents_header_in:
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
    type: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    num: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    obout: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    obno_out: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    htyp_out: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    frac: '|a module-level working variable holding a fraction (no inline source comment;
      interpreted from the name)'
    sol: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sor: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
  constituents_header_out:
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
    type: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    num: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    obout: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    obno_out: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    htyp_out: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    frac: '|a module-level working variable holding a fraction (no inline source comment;
      interpreted from the name)'
  sol_sor:
    sol: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
    sor: '|a module-level working variable shared across the importing routines (no inline
      source comment in the declaration)'
type_summaries:
  constituents: One `constituents` record groups `num_tot`, `num_pests`, `pests`, `pest_num`,
    `num_paths`, `paths`, and 10 more fields.
  exco_pesticide: One `exco_pesticide` record groups `pest`.
  dr_pesticide: One `dr_pesticide` record groups `pest`.
  exco_pathogens: One `exco_pathogens` record groups `path`.
  dr_pathogens: One `dr_pathogens` record groups `path`.
  exco_heavy_metals: One `exco_heavy_metals` record groups `hmet`.
  dr_heavy_metals: One `dr_heavy_metals` record groups `hmet`.
  exco_salts: One `exco_salts` record groups `salt`.
  dr_salts: One `dr_salts` record groups `salt`.
  salt_solids_soil: One `salt_solids_soil` record groups `solid`.
  constituent_mass: Constituent mass - soil, plant, aquifer, and channels. Holds `pest`, `path`,
    `hmet`, `salt`, `salt_min`, `saltc`, and 4 more fields.
  soil_constituent_mass: Soil constituent mass - dimensioned by hru. Holds `ly`.
  plant_constituent_mass: Plant constituent mass - dimensioned by hru. Holds `pl_in`, `pl_on`,
    `pl_up`.
  all_constituent_hydrograph: Hydrographs for all constituents - dimension to number of each
    constituent. Holds `hd`, `hin`, `hin_sur`, `hin_lat`, `hin_til`, `hin_aqu`, and 7 more
    fields.
  gw_load_hydrograph: Hydrographs for groundwater loading to streams. Holds `hd`.
  recall_salt_inputs: Recall salinity inputs (rtb salt). Holds `name`, `typ`, `filename`,
    `start_yr`, `end_yr`, `pts_type`, and 1 more fields.
  recall_cs_inputs: Recall constituent inputs (rtb cs). Holds `name`, `typ`, `filename`, `start_yr`,
    `end_yr`, `pts_type`, and 1 more fields.
  recall_pesticide_inputs: Recall pesticide inputs. Holds `name`, `num`, `typ`, `filename`,
    `hd_pest`.
  cs_soil_init_concentrations: Initial constituent soil-plant concentrations for hrus. Holds
    `name`, `soil`, `plt`.
  salt_aqu_init_concentrations: Initial salt ion groundwater concentrations and mineral fractions
    for aquifers. Holds `name`, `conc`, `frac`.
  cs_aqu_init_concentrations: Initial constituent groundwater concentrations for aquifers.
    Holds `name`, `aqu`.
  salt_cha_init_concentrations: Initial salt ion water concentrations for channels. Holds
    `name`, `conc`.
  cs_cha_init_concentrations: Initial constituent water concentrations for channels. Holds
    `name`, `conc`.
  cs_water_init_concentrations: Initial constituent water-benthic concentrations for reservoirs
    and channels. Holds `name`, `water`, `benthic`, `reservoir`.
  cs_irrigation_concentrations: Concentration in irrigation water (outside source). Holds
    `name`, `water`.
  output_rusaltb_header: Header for routing unit salt balance output. Holds `day`, `mo`, `day_mo`,
    `yrc`, `isd`, `id`, and 121 more fields.
  output_rucsb_header: Header for routing unit constituent balance output. Holds `day`, `mo`,
    `day_mo`, `yrc`, `isd`, `id`, and 48 more fields.
  constituents_header_in: One `constituents_header_in` record groups `day`, `mo`, `day_mo`,
    `yrc`, `name`, `otype`, and 8 more fields.
  constituents_header_out: One `constituents_header_out` record groups `day`, `mo`, `day_mo`,
    `yrc`, `name`, `otype`, and 6 more fields.
  sol_sor: One `sol_sor` record groups `sol`, `sor`.
---

<!-- facts:header -->

`constituent_mass_module` owns the bookkeeping types for SWAT+ water-quality constituents (pesticides, pathogens, heavy metals, and salts): the `constituents` master list, the export-coefficient (`exco_*`) and delivery-ratio (`dr_*`) parameter types per constituent class, and the `constituent_mass`/`soil_constituent_mass` mass records. The arrays are populated by the constituent read/initialization routines and consumed by the constituent transport, soil, reservoir, channel, and output code.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container. The constituent type defaults are zero/empty in their declarations, and the constituent name lists and mass arrays are allocated and populated by the constituent setup routines (`constituent_mass_read`, `cs_*`/`salt_*` readers, basin object allocation).

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | References `constituent_mass_module` state: references `cs_irr`, `cs_db`, `cs_aqu`, `ch_water` (e.g. `actions.f90:151`). |
| [sym:aqu2d_init] | `no direct file input (operates on in-memory state)` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Initializes `constituent_mass_module` state: references `cs_db`, `aq_chcs` (e.g. `aqu2d_init.f90:86`). |
| [sym:aqu_cs_output] | `unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Writes output from `constituent_mass_module` state: references `cs_db` (e.g. `aqu_cs_output.f90:24`). |
| [sym:aqu_pest_output_init] | `no direct file input (operates on in-memory state)` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Initializes `constituent_mass_module` state: references `cs_db`, `cs_aqu` (e.g. `aqu_pest_output_init.f90:16`). |
| [sym:aqu_pesticide_output] | `unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Writes output from `constituent_mass_module` state: references `cs_db` (e.g. `aqu_pesticide_output.f90:27`). |
| [sym:aqu_read_init] | `initial.aqu` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Imports `constituent_mass_module`; no specific module symbol from it was resolved in the extracted references for `aqu_read_init`. |
| [sym:aqu_read_init_cs] | `initial.aqu_cs` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | References `constituent_mass_module` state: references `pest_init_name`, `cs_db`, `cs_aqu`, `pest_water_ini` (e.g. `aqu_read_init_cs.f90:84`). |
| [sym:aqu_salt_output] | `unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Writes output from `constituent_mass_module` state: references `cs_db` (e.g. `aqu_salt_output.f90:23`). |
| [sym:basin_aqu_pest_output] | `unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Writes output from `constituent_mass_module` state: references `cs_db` (e.g. `basin_aqu_pest_output.f90:27`). |
| [sym:basin_ch_pest_output] | `unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Writes output from `constituent_mass_module` state: references `cs_db` (e.g. `basin_ch_pest_output.f90:26`). |
| [sym:basin_ls_pest_output] | `unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Writes output from `constituent_mass_module` state: references `cs_db` (e.g. `basin_ls_pest_output.f90:27`). |
| [sym:basin_read_objs] | `unit_*, object.cnt, chancell.gw, gwflow_record` | `pest_init_name, path_init_name, hmet_init_name, salt_init_name, cs_init_name, cs_db` | Aggregates basin totals from `constituent_mass_module` state: references `obcs`, `obcs_alloc` (e.g. `basin_read_objs.f90:92`). |

## Key Consumers

Importers include the constituent and salt/pesticide/pathogen setup routines that read the databases and allocate the mass arrays, the soil and routing transport routines that move constituent mass between objects, and the output routines that report constituent mass.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:gwflow_output_init] | `cs_db` | The solute file setup depends on `cs_db%num_salts` and `cs_db%num_cs` to decide which additional solute output files to create beyond nitrate and phosphorus. Those counters control whether salt-ion and other-constituent solute outputs are included. |
| [sym:gwflow_read] | `cs_db` | `constituent_mass_module` matters because `cs_db` provides the constituent database counts and names used to extend the groundwater solute list when constituent transport is enabled. |
| [sym:aqu2d_init] | constituent_mass_module | The `constituent_mass_module` matters because this routine conditionally allocates groundwater-loading hydrographs for salt ions and other constituents. `cs_db%num_tot` decides whether any constituent hydrograph state is needed, and `cs_db%num_salts` / `cs_db%num_cs` determine whether the `aq_chcs(iaq)%hd(1)%salt` and `aq_chcs(iaq)%hd(1)%cs` arrays must be allocated and zeroed. |
| [sym:aqu_cs_output] | constituent_mass_module | The constituent database count controls how many constituent records are looped over in every accumulation, averaging, and write statement. If `cs_db%num_cs` is zero, the constituent output loops do not execute. |
| [sym:aqu_pest_output_init] | constituent_mass_module | This module supplies the number of pesticide constituents to loop over and the aquifer constituent-mass array that provides the source values copied into output initialization. Without it, the routine would not know how many pesticide slots exist or what mass to place into each aquifer record. |
| [sym:aqu_pesticide_output] | constituent_mass_module | `constituent_mass_module` provides `cs_db%num_pests` for the pesticide loop bound and `cs_db%pests(ipest)` for the pesticide name written to every record. That module is what lets the routine iterate over the simulated pesticide list and label each output row correctly. |
| [sym:aqu_read_init_cs] | constituent_mass_module | This module owns the constituent-count metadata, aquifer constituent state arrays, and the initial-condition tables that supply the actual values written into `cs_aqu` for pesticides, pathogens, salts, and generic constituents. |
| [sym:aqu_salt_output] | constituent_mass_module | The number of simulated salts determines whether the salt-output branch runs at all. `command` only calls this routine when `cs_db%num_salts > 0`, and inside the routine the same value sets the loop bounds for all per-salt fields. |
| [sym:basin_aqu_pest_output] | constituent_mass_module | `constituent_mass_module` provides `cs_db%num_pests` for the loop bound and `cs_db%pests(ipest)` for the pesticide name written into each record. Without this database the routine could not iterate over or label the pesticide outputs. |
| [sym:basin_ch_pest_output] | constituent_mass_module | The routine needs `cs_db%num_pests` to know how many pesticides to process and `cs_db%pests(ipest)` to label each output record with the pesticide name. Without this database, the routine would not know the loop bounds or the text name to write for each pesticide summary. |
| [sym:basin_ls_pest_output] | constituent_mass_module | `constituent_mass_module` provides cs_db, which tells the routine how many pesticides exist and supplies the pesticide names written into each output record. |
| [sym:basin_read_objs] | constituent_mass_module | `constituent_mass_module` matters because it defines `obcs_alloc`, the allocation-tracking array that is sized here alongside the object count so later constituent-loading code can tell which objects have basin constituent storage initialized. |
| [sym:basin_res_pest_output] | constituent_mass_module | This module provides the shared constituent database used to count pesticides and name each pesticide in the output records. |
| [sym:ch_cs_output] | constituent_mass_module | `constituent_mass_module` supplies `cs_db%num_cs`, the number of simulated constituent species. That value drives the loop bounds and the array sections written for each channel output record. |
| [sym:ch_salt_output] | constituent_mass_module | `cs_db%num_salts` sets the number of salt constituents to iterate over. Every accumulation loop and every write statement uses it to size the salt-vector output for the current model setup. |
| [sym:cha_pesticide_output] | constituent_mass_module | `cs_db` provides the count of pesticide constituents to loop over and the pesticide names written to the report rows. That makes it the source of both the iteration bound and the human-readable constituent label in each output record. |
| [sym:cli_read_atmodep_cs] | constituent_mass_module | This module provides `cs_db%num_cs`, the count of simulated constituent substances. The routine uses that count to decide whether to process `cs_atmo.cli` at all and how many constituent records to allocate and read for each station. |
| [sym:cli_read_atmodep_salt] | constituent_mass_module | `constituent_mass_module` provides `cs_db%num_salts`, which is the simulation-wide count of salt ions. That count determines whether salt atmospheric deposition should be read and how many salt records to expect per station. |
| [sym:constit_db_read] | constituent_mass_module | `constituent_mass_module` provides the shared `cs_db` structure that this routine fills. The routine reads counts and names into its allocatable arrays and later stores database crosswalk indices and the total constituent count there. |
| [sym:cs_aqu_read] | constituent_mass_module | The `constituent_mass_module` provides the shared aquifer constituent database and storage that this routine fills. `cs_db%num_cs` determines how large each aquifer concentration array must be, and `cs_aqu_ini(ics)%name` plus `cs_aqu_ini(ics)%aqu` receive the parsed name and values for every record. |
| [sym:cs_balance] | constituent_mass_module | This module defines the constituent database and the soil/point-source mass structures that cs_balance reads and later zeros, including the three-constituent arrays for dissolved and sorbed soil mass. |
| [sym:cs_cha_read] | constituent_mass_module | This module owns the channel constituent initialization array and the daily-output selection state that `cs_cha_read` fills. `cs_db%num_cs` supplies the number of constituent values to allocate for each channel, `cs_cha_ini` stores the per-channel names and concentrations read from `cs_channel.ini`, and `cs_str_obs`, `cs_str_nobs`, and `cs_obs_file` control and retain the optional daily stream-observation channel list. |
| [sym:cs_hru_init] | constituent_mass_module | constituent_mass_module provides the constituent databases and storage arrays that this routine populates. `cs_db%num_cs` sets the number of constituents, `cs_soil_ini(ics_db)%soil(ics)` and `cs_water_irr(ics_db)%water(ics)` supply the starting concentrations, and `cs_soil(ihru)%ly(ly)%cs`, `csc`, `cs_sorb`, `csc_sorb`, and `cs_irr(ihru)%csc` are the target state arrays being allocated and filled for each HRU and soil layer. |
| [sym:cs_hru_read] | constituent_mass_module | This module holds the shared constituent database types and storage that `cs_hru_read` fills. The routine allocates `cs_soil_ini(imax)` and then populates each element's `name`, `soil`, and `plt` fields, while `cs_db%num_cs` determines the length of the soil and plant concentration arrays that are allocated for each record. |

## Lineage

`constituent_mass_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 9 non-merge commit(s) since, most recently `815ec79` (2026-01-07, "water allocation updates"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `constituent_mass_module.f90` are listed.

- `815ec79` (2026-01-07) — water allocation updates
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `10e5ddc` (2025-08-27) — 08272025 updates
- `889136d` (2025-02-03) — Fix typos
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `constituent_mass_module` has no extracted module-level documentation comment.
- Reader rows show 12 candidate initialization/read routines out of 121; treat the table as representative, not exhaustive.
- This module is imported by 203 procedures; the main Used By table shows 24 ranked consumers and the collapsible importer list keeps the complete deterministic list.
- variable_notes and type_notes summaries were completed locally from the module's declaration metadata (type, shape, source comments) and the Derived Type Inventory; reader behaviors were grounded in source references found in each reader. 4 module-level scalar(s) had no inline source comment and were given name-based interpretations — these should be spot-checked.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
