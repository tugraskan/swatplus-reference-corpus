---
kind: module
symbol: hru_module
title: hru_module
status: filled
source_hash: 73bf44a565d31c37
version_label: SWAT+ 62.0.0
variables:
  isep: integer switch shared by septic-related HRU logic; initialized to 0 in the module
    and read by septic, HRU balance, and output routines that branch on septic presence.
  ilu: integer index shared across land-use-management lookup and HRU setup; initialized to
    0 and used by readers and selection routines that resolve land-use tables.
  ulu: integer index shared across land-use-management lookup and HRU setup; initialized to
    0 and used by readers and selection routines that resolve land-use tables.
  iwgen: integer switch shared by HRU initialization and management routines; initialized
    to 0 and used where water-generation or irrigation-related behavior is selected.
  timest: single-character time-step flag initialized to blank and used by routines that distinguish
    daily versus smaller time-step processing.
  uptake: Module-global uptake_parameters record initialized with hardwired water distribution
    and zero normalization factors; used by plant uptake routines to apply water, nitrogen,
    and phosphorus uptake settings.
  snodb: Allocatable snow_parameters database initialized by snowdb_read and consumed by snow
    and dtbl lookup routines to resolve snow behavior by name.
  sdr: Allocatable subsurface_drainage_parameters database initialized by sdr_read and consumed
    by drainage, land-use, and HRU initialization routines to resolve tile-drain settings.
  satbuff_db: Allocatable saturated_buffer_parameters database initialized by sat_buff_read
    and used by saturated-buffer routing and HRU linkage routines.
  luse: Allocatable landuse database initialized by landuse_read and used by HRU land-use-management
    initialization, runoff, erosion, and urban-process routines.
  sol_plt_ini: Allocatable soil_plant_initialize database initialized by soil_plant_init and
    consumed by HRU crop, carbon, pathogen, pesticide, and soil-plant initialization routines.
  hru_db: Allocatable hydrologic_response_unit_db database initialized by hru_read and used
    by HRU construction and database-to-active-state transfer routines.
  hru: Allocatable hydrologic_response_unit array holding the active HRU state for the simulation;
    populated by hru_read, hrudb_init, hru_lum_init_all, and related initialization routines
    and then read by nearly all HRU-level process routines.
  hru_init: Allocatable hydrologic_response_unit array used as the initialization copy of
    HRU state; populated during allocation and calibration setup so active HRUs can be reset
    or compared against initial conditions.
  precip_eff: mm   |daily effective precip for runoff calculations = precipday + ls_overq
    + snomlt - canstor
  qday: mm   |surface runoff that reaches main channel during day in HRU; the comment also
    notes the effective precipitation expression used with snow and canopy storage terms.
  satexq_chan: mm   |saturation excess runoff that reaches main channel during day in HRU
  ipl: integer index for the plant-competition arrays added in this module; initialized to
    0 and used by plant competition routines.
  isol: integer index used with the plant-competition arrays and soil/solute selection; initialized
    to 0 and shared by plant and soil routines.
  strsa_av: Average available plant stress on water or related stress factor for plant competition
    routines; initialized to 0 and consumed by plant growth and competition logic.
  strsn_av: Average available nitrogen stress factor for plant competition routines; initialized
    to 0 and consumed by plant growth and competition logic.
  strsp_av: Average available phosphorus stress factor for plant competition routines; initialized
    to 0 and consumed by plant growth and competition logic.
  strstmp_av: Average temperature stress factor for plant competition routines; initialized
    to 0 and consumed by plant growth and competition logic.
  rto_no3: Ratio or routing factor for nitrate uptake or demand in plant competition logic;
    initialized to 0 and used by plant nutrient routines.
  rto_solp: Ratio or routing factor for soluble phosphorus uptake or demand in plant competition
    logic; initialized to 0 and used by plant nutrient routines.
  uno3d_tot: Total daily nitrate uptake accumulator for plant competition and nutrient balance
    routines; initialized to 0.
  uapd_tot: Total daily phosphorus uptake accumulator for plant competition and nutrient balance
    routines; initialized to 0.
  sum_no3: Running sum of nitrate uptake or demand used by plant competition and nutrient
    balance routines; initialized to 0.
  sum_solp: Running sum of soluble phosphorus uptake or demand used by plant competition and
    nutrient balance routines; initialized to 0.
  epmax: Maximum evapotranspiration or uptake-limited water demand used in plant calculations;
    shared by plant growth and soil-water routines.
  cvm_com: Composite canopy or community variable used in plant competition calculations;
    shared by plant growth routines.
  translt: Transpiration-related plant competition variable shared by plant water uptake routines.
  uno3d: Daily nitrate uptake variable shared by plant nutrient routines.
  uapd: Daily phosphorus uptake variable shared by plant nutrient routines.
  par: Photosynthetically active radiation or plant competition driver shared by plant growth
    routines.
  htfac: Plant height factor used in plant competition and growth routines.
  un2: Nitrogen uptake variable used by plant competition and nutrient routines.
  up2: Phosphorus uptake variable used by plant competition and nutrient routines.
  iseptic: Integer septic-system switch shared by septic HRU routines; used to turn septic
    behavior on and off.
  qp_cms: Septic-system flow variable in cubic meters per second used for output.std and septic
    routing.
  sw_excess: Soil-water excess accumulator used by runoff and soil-water routing routines;
    initialized to 0.
  albday: Daily albedo-related state used by HRU surface-energy routines; initialized to 0.
  wt_shall: Shallow water table state used by HRU hydrology and wetland routines; initialized
    to 0.
  sq_rto: Surface runoff ratio used by HRU hydrology and runoff routines; initialized to 0.
  snomlt: Daily snowmelt amount used in runoff and snow routines; initialized to 0.
  snofall: Daily snowfall amount used in runoff and snow routines; initialized to 0.
  fixn: Nitrogen fixation amount used by plant and nutrient routines; initialized to 0.
  qtile: Tile-drain flow used by drainage and routing routines; initialized to 0.
  latlyr: mm            |lateral flow in soil layer for the day
  inflpcp: mm            |amount of precipitation that infiltrates
  fertn: Daily fertilizer nitrogen amount used by fertilizer and nutrient routing routines;
    initialized to 0.
  sepday: Daily septic-system discharge or septic-day flux used by septic routines; initialized
    to 0.
  bioday: Daily biological or septic-related flux used by septic routines; initialized to
    0.
  sepcrk: Septic crack-flow flux used by septic routines; initialized to 0.
  sepcrktot: Total septic crack-flow accumulator used by septic routines; initialized to 0.
  fertno3: Daily nitrate fertilizer amount used by fertilizer and nutrient routines; initialized
    to 0.
  fertnh3: Daily ammonium fertilizer amount used by fertilizer and nutrient routines; initialized
    to 0.
  fertorgn: Daily organic nitrogen fertilizer amount used by fertilizer and nutrient routines;
    initialized to 0.
  fertsolp: Daily soluble phosphorus fertilizer amount used by fertilizer and nutrient routines;
    initialized to 0.
  fertorgp: Daily organic phosphorus fertilizer amount used by fertilizer and nutrient routines;
    initialized to 0.
  fertp: Daily total phosphorus fertilizer amount used by fertilizer and nutrient routines;
    initialized to 0.
  grazn: Daily nitrogen removed by grazing used by grazing and nutrient routines; initialized
    to 0.
  grazp: Daily phosphorus removed by grazing used by grazing and nutrient routines; initialized
    to 0.
  sdti: Sediment or drainage-time index used by HRU drainage and routing routines; initialized
    to 0.
  voltot: mm            |total volume of cracks expressed as depth per area unit
  volcrmin: mm            |minimum crack volume allowed in any soil layer
  canev: Daily canopy evaporation used by evaporation and canopy-interception routines; initialized
    to 0.
  usle: Daily USLE erosion factor or erosion output used by erosion routines; initialized
    to 0.
  rcn: Runoff curve number state used by CN and runoff routines; initialized to 0.
  enratio: Enrichment ratio used by sediment and nutrient transport routines; initialized
    to 0.
  vpd: Vapor pressure deficit used by evapotranspiration routines; initialized to 0.
  pet_day: Potential evapotranspiration for the day used by ET routines; initialized to 0.
  ep_day: Potential evaporation for the day used by ET routines; initialized to 0.
  snoev: Daily snow evaporation used by snow and ET routines; initialized to 0.
  es_day: Daily soil evaporation used by ET routines; initialized to 0.
  ls_overq: Daily landscape overland flow contribution used in runoff and precipitation-effective
    calculations; initialized to 0.
  latqrunon: Lateral runon to the HRU used by hydrology and runoff routing routines; initialized
    to 0.
  tilerunon: Tile runon to the HRU used by drainage and routing routines; initialized to 0.
  ep_max: Maximum evaporation or ET demand used by plant and hydrology routines; initialized
    to 0.
  bsprev: Previous basin or baseflow-related state used by runoff and routing routines; initialized
    to 0.
  usle_ei: USLE rainfall erosivity factor used by erosion routines; initialized to 0.
  snocov1: Snow cover threshold or state variable used by snow routines; initialized to 0.
  snocov2: Snow cover threshold or state variable used by snow routines; initialized to 0.
  lyrtile: Tile-drain layer indicator used by drainage routines; initialized to 0.
  etday: Daily evapotranspiration used by ET routines; initialized to 0.
  mo: Integer month indicator shared by daily and subdaily routines; initialized to 0.
  ihru: none          |HRU number
  nd_30: Integer count used in 30-day nutrient or routing logic; initialized to 0.
  mpst: Integer management or septic/pesticide state index used by HRU routines; initialized
    to 0.
  mlyr: Integer soil-layer index used by HRU soil and routing routines; initialized to 0.
  date: character date stamp for the current day or time step used by output and control routines.
  isep_ly: Septic-layer change flag added for septic logic; used by septic HRU routines.
  qstemm: Stemflow or septic-related flow variable used by septic routines; initialized to
    0.
  bio_bod: Biological oxygen demand related septic variable added with septic changes; used
    by septic routines.
  biom: Septic or biomass-related variable used by septic routines; initialized to 0.
  rbiom: Residual biomass-related septic variable used by septic routines; initialized to
    0.
  fcoli: Fecal coliform variable used by septic water-quality routines; initialized to 0.
  bz_perc: Biological zone percolation or septic percolation variable used by septic routines;
    initialized to 0.
  plqm: Plant or septic quality metric used by septic routines; initialized to 0.
  i_sep: Septic system by Jaehak Jeong; integer control used by septic routines.
  sep_tsincefail: Time since septic failure used by septic failure logic; initialized to 0.
  sol_sumno3: Total soil nitrate sum used by soil nutrient summary routines; initialized to
    0.
  sol_sumsolp: Total soil soluble phosphorus sum used by soil nutrient summary routines; initialized
    to 0.
  sanyld: Sand yield used by erosion and sediment-class accounting routines; initialized to
    0.
  silyld: Silt yield used by erosion and sediment-class accounting routines; initialized to
    0.
  clayld: Clay yield used by erosion and sediment-class accounting routines; initialized to
    0.
  sagyld: Sand aggregate yield used by erosion and sediment-class accounting routines; initialized
    to 0.
  lagyld: Large aggregate yield used by erosion and sediment-class accounting routines; initialized
    to 0.
  grayld: Gravel yield used by erosion and sediment-class accounting routines; initialized
    to 0.
  itb: Integer bookkeeping index used by drain or routing routines; initialized from the module
    default.
  wnan: Drainage-related working array noted by the source comment `!!!!! drains`; used by
    drainmod and drainage routines.
  phusw: Soil water pH or a hydrology switch value used by HRU chemical/routing routines;
    initialized by the module and consumed by drainage and water-quality logic.
  yr_skip: Integer year-skip flag used by burn or sweep management routines; initialized to
    0.
  isweep: Integer sweep-management flag used by burn or residue-management routines; initialized
    to 0.
  sweepeff: Sweep efficiency used by management routines; initialized to 0.
  ranrns_hru: Randomness or residue-related HRU array used by management routines; initialized
    by the module.
  itill: Integer tillage counter or index used by tillage routines; initialized by the module.
  tc_gwat: Groundwater travel-time or concentration-time variable used by groundwater routing
    routines; initialized by the module.
  wfsh: Flow-shape or watershed factor used by routing routines; initialized by the module.
  sed_con: Sediment concentration used by sediment routing and filter-strip routines; initialized
    by the module.
  orgn_con: Organic nitrogen concentration used by nutrient routing routines; initialized
    by the module.
  orgp_con: Organic phosphorus concentration used by nutrient routing routines; initialized
    by the module.
  soln_con: Soluble nitrogen concentration used by nutrient routing routines; initialized
    by the module.
  solp_con: Soluble phosphorus concentration used by nutrient routing routines; initialized
    by the module.
  filterw: Filter-strip width used by filter-strip and runoff routing routines; initialized
    by the module.
  cn2: Curve number array used by runoff and calibration routines; allocated here and updated
    by cn2_init and calibration procedures.
  smx: Maximum soil moisture or storage variable used by hydrology routines; initialized by
    the module.
  cnday: Daily curve number used by runoff routines; initialized by the module.
  tconc: Time of concentration used by runoff and routing routines; initialized by the module.
  usle_cfac: USLE cover-management factor used by erosion routines; initialized by the module.
  usle_eifac: USLE rainfall erosivity factor modifier used by erosion routines; initialized
    by the module.
  t_ov: Overland travel time used by routing routines; initialized by the module.
  canstor: Canopy storage used by interception and runoff routines; initialized by the module.
  ovrlnd: Overland flow depth or runoff state used by runoff routines; initialized by the
    module.
  cumei: Drainmod tile-equation cumulative evaporation/infiltration term used by drainage
    routines.
  cumeira: Drainmod tile-equation cumulative irrigation/rainfall term used by drainage routines.
  cumrt: Drainmod tile-equation cumulative runoff term used by drainage routines.
  cumrai: Drainmod tile-equation cumulative rain/irrigation term used by drainage routines.
  sstmaxd: Drainmod tile-equation maximum soil storage term used by drainage routines.
  stmaxd: Drainmod tile-equation maximum storage term used by drainage routines.
  surqsolp: Drainmod tile-equation soluble phosphorus runoff term used by drainage and water-quality
    routines.
  cklsp: USLE combined LS or channel-length slope factor used by erosion routines; initialized
    by the module.
  pplnt: Plant phosphorus-related variable used by plant nutrient routines; initialized by
    the module.
  brt: Biomass or residue-related variable used by management routines; initialized by the
    module.
  twash: Tillage or wash-off variable used by management and sediment routines; initialized
    by the module.
  doxq: Dissolved oxygen concentration in runoff or channel water used by water-quality routines;
    initialized by the module.
  percn: Percolation nitrate variable used by nutrient and percolation routines; initialized
    by the module.
  cbodu: Carbonaceous biochemical oxygen demand in upland flow used by water-quality routines;
    initialized by the module.
  chl_a: Chlorophyll-a variable used by water-quality routines; initialized by the module.
  qdr: Drainage flow used by drainage and routing routines; initialized by the module.
  latno3: Lateral nitrate load used by lateral-flow nutrient routing routines; initialized
    by the module.
  latq: Lateral flow used by hydrology and routing routines; initialized by the module.
  nplnt: Plant nitrogen variable used by plant nutrient routines; initialized by the module.
  tileno3: Tile-drain nitrate load used by tile drainage nutrient routing routines; initialized
    by the module.
  sedminpa: Sediment-mineral phosphorus attached to the active sediment class used by sediment
    nutrient routines; initialized by the module.
  sedminps: Sediment-mineral phosphorus attached to the stable sediment class used by sediment
    nutrient routines; initialized by the module.
  sedorgn: Sediment organic nitrogen used by sediment nutrient routines; initialized by the
    module.
  sedorgp: Sediment organic phosphorus used by sediment nutrient routines; initialized by
    the module.
  sedyld: Sediment yield used by erosion and sediment routing routines; initialized by the
    module.
  sepbtm: Septic bottom or septic-system seepage variable used by septic routines; initialized
    by the module.
  surfq: Surface runoff used by runoff and routing routines; initialized by the module.
  surqno3: Surface runoff nitrate load used by nutrient routing routines; initialized by the
    module.
  surqsalt: Surface runoff salt load array used by salinity routing routines.
  latqsalt: Lateral-flow salt load array used by salinity routing routines.
  tilesalt: Tile-drain salt load array used by salinity routing routines.
  percsalt: Percolation salt load array used by salinity routing routines.
  gwupsalt: Groundwater uptake salt load array used by salinity routing routines.
  urbqsalt: Urban runoff salt load array used by salinity routing routines.
  irswsalt: Irrigation surface-water salt load array used by salinity routing routines.
  irgwsalt: Irrigation groundwater salt load array used by salinity routing routines.
  wetqsalt: Wetland outflow salt load array used by salinity routing routines.
  wtspsalt: Wetland seepage or storage salt load array used by salinity routing routines.
  surqcs: rtb cs
  latqcs: rtb cs
  tilecs: rtb cs
  perccs: rtb cs
  gwupcs: rtb cs
  urbqcs: rtb cs
  sedmcs: rtb cs
  irswcs: rtb cs
  irgwcs: rtb cs
  wetqcs: rtb cs
  wtspcs: rtb cs
  phubase: Base pH or pH-related state used by soil chemistry routines; initialized by the
    module.
  dormhr: Dormancy-hour accumulator used by plant phenology routines; initialized by the module.
  wrt: Water routing or storage array used by HRU routing routines; initialized by the module.
  bss: Baseflow or subsurface storage array used by hydrology and calibration routines; initialized
    by the module.
  surf_bs: Surface-base storage array used by hydrology and routing routines; initialized
    by the module.
  swtrg: Integer soil-water trigger used by soil-water management routines; initialized by
    the module.
  rateinf_prev: Previous infiltration rate used by runoff and infiltration routines; initialized
    by the module.
  urb_abstinit: Initial urban abstraction used by urban runoff routines; initialized by the
    module.
  grz_days: burn
  igrz: Integer grazing counter or switch used by grazing routines; initialized by the module.
  ndeat: Integer death counter used by grazing or burn routines; initialized by the module.
  gwsoilq: Groundwater soil-water flux used by groundwater flow routines; marked `rtb gwflow`
    in the source.
  satexq: Saturation-excess groundwater or soil-water flux used by groundwater flow routines;
    marked `rtb gwflow` in the source.
  bss_ex: Baseflow/subsurface storage exchange array used by groundwater flow routines; marked
    `rtb gwflow` in the source.
  gwsoiln: Groundwater soil nitrate used by groundwater flow routines; marked `rtb gwflow`
    in the source.
  gwsoilp: Groundwater soil phosphorus used by groundwater flow routines; marked `rtb gwflow`
    in the source.
  satexn: Saturation-excess nitrogen flux used by groundwater flow routines; marked `rtb gwflow`
    in the source.
  irrn: rtb irrig (irrigation nutrient mass)
  irrp: rtb irrig (irrigation nutrient mass)
  mgt_ops: Integer management-operations matrix added for SDR/drainage logic; used by HRU
    management and scheduling routines.
  hhqday: Daily subarea or hillslope hydrology array used by routing and output routines.
  ubnrunoff: Upstream/basin runoff array used by routing and output routines.
  ubntss: Upstream/basin total suspended solids array used by routing and output routines.
  ovrlnd_dt: Overland flow by time-step array used by subdaily runoff routines.
  hhsurfq: Subdaily surface runoff array used by hillslope routing and output routines.
  hhsurf_bs: Subdaily surface-base storage array used by hillslope routing and output routines.
  hhsedy: Subdaily erosion modeling by Jaehak Jeong
  init_abstrc: Initial abstraction used by runoff and curve-number routines; initialized by
    the module.
  tillage_switch: Integer per-HRU tillage switch used by management routines to enable or
    disable tillage effects.
  tillage_depth: Tillage depth used by management routines; initialized by the module.
  tillage_days: Integer tillage-day counter used by management routines; initialized by the
    module.
  tillage_factor: Tillage factor used by management routines; initialized by the module.
type_components:
  uptake_parameters:
    water_dis: hardwired water uptake distribution coefficient.
    water_norm: water uptake normalization parameter.
    n_norm: nitrogen uptake normalization parameter.
    p_norm: phosphorus uptake normalization parameter.
  irrigation_sources:
    flag: 0 = do not irrigate, 1 = irrigate.
    chan: Allocatable channel-source index list for irrigation water.
    res: Allocatable reservoir-source index list for irrigation water.
    pond: Allocatable pond-source index list for irrigation water.
    shal: Allocatable shallow-source index list for irrigation water.
    deep: Allocatable deep-source index list for irrigation water.
  topography:
    name: Topography record name.
    elev: HRU elevation in meters.
    slope: Average HRU slope steepness in m/m.
    slope_len: Average slope length for erosion calculations in meters.
    dr_den: Drainage density in km/km2.
    lat_len: Slope length for lateral subsurface flow in meters.
    dis_stream: Average distance to stream in meters.
    dep_co: Deposition coefficient.
    field_db: Pointer to a field.fld record.
    channel_db: Pointer to a channel.dat record.
  hydrology:
    name: Hydrology record name.
    lat_ttime: Days of lateral soil flow across the hillslope.
    lat_sed: Sediment concentration in lateral flow in g/L.
    canmx: Maximum canopy storage in mm H2O.
    esco: Soil evaporation compensation factor.
    epco: Plant water uptake compensation factor (0-1).
    erorgn: Organic nitrogen enrichment ratio; if left blank the model calculates it for each
      event.
    erorgp: Organic phosphorus enrichment ratio; if left blank the model calculates it for
      each event.
    cn3_swf: Curve-number adjustment factor at CN3 based on soil water.
    biomix: Biological mixing efficiency.
    perco: Percolation coefficient as a linear adjustment to daily percolation.
    lat_orgn: Lateral organic nitrogen coefficient.
    lat_orgp: Lateral organic phosphorus coefficient.
    pet_co: Potential ET coefficient.
    latq_co: Lateral soil-flow coefficient as a linear adjustment to daily lateral flow.
    perco_lim: Limits percolation from the bottom layer.
  snow_parameters:
    name: Snow record name.
    falltmp: Snowfall temperature in degrees C.
    melttmp: Snowmelt base temperature in degrees C.
    meltmx: Maximum melt rate during the year in mm/deg C/day.
    meltmn: Minimum melt rate during the year in mm/deg C/day.
    timp: Snowpack temperature lag factor.
    covmx: Snow water content at full ground cover in mm H2O.
    cov50: Fraction of covmx at 50% snow cover.
    init_mm: Initial snow water content at simulation start in mm H2O.
  subsurface_drainage_parameters:
    name: Drainage record name.
    depth: Depth of the drain tube from the soil surface in mm.
    time: Time to drain soil to field capacity in hours.
    lag: Drain tile lag time in hours.
    radius: Effective drain radius in mm.
    dist: Distance between drain tubes or tiles in mm.
    drain_co: Drainage coefficient in mm/day.
    pumpcap: Pump capacity in mm/hr.
    latksat: Multiplication factor used to determine lateral saturated hydraulic conductivity
      for the profile.
  saturated_buffer_parameters:
    name: Saturated-buffer record name.
    hru_src: Source HRU for tile inflow.
    frac_src: Fraction of the source HRU contributing to tile flow.
    flocon_dtbl: Decision table that controls flow into the buffer HRU.
    hru_rcv: Receiving buffer HRU.
    lyr: Soil layer receiving incoming tile flow; 0 means surface.
  saturated_buffer:
    sb_db: Embedded saturated_buffer_parameters definition used by the active buffer.
    dtbl: Decision-table index selected for the buffer.
    inflo: Incoming buffer inflow.
    no3: Nitrate mass associated with the buffer inflow.
  landuse:
    name: Land-use record name.
    cn_lu: Curve-number land-use identifier.
    cons_prac: Conservation-practice code.
    usle_p: Daily USLE support-practice (P) factor.
    urb_ro: Urban runoff model selector; valid text options are `usgs_reg` and `buildup_washoff`.
    urb_lu: Urban land type identification number.
    ovn: Manning's n value for overland flow.
  soil_plant_initialize:
    name: Initialization record name.
    sw_frac: Soil-water fraction used for initialization.
    nutc: Nutrient initialization code or reference.
    pestc: Pesticide initialization code or reference.
    pathc: Pathogen initialization code or reference.
    saltc: Salt initialization code or reference.
    hmetc: Heavy-metal initialization code or reference.
    csc: Carbon-state initialization code or reference.
    nut: Switch or pointer for nutrient initialization.
    pest: Switch or pointer for pesticide initialization.
    path: Switch or pointer for pathogen initialization.
    salt: Switch or pointer for salt initialization.
    hmet: Switch or pointer for heavy-metal initialization.
    cs: Switch or pointer for carbon-state initialization.
  hru_databases:
    name: HRU database record name.
    topo: Index of the topography record.
    hyd: Index of the hydrology record.
    soil: Index of the soil record.
    land_use_mgt: Index of the land-use-management record.
    soil_plant_init: Index of the soil-plant initialization record.
    surf_stor: Index of the surface-storage record.
    snow: Index of the snow record.
    field: Index of the field record.
  hru_databases_char:
    name: HRU database record name.
    topo: Topography record name.
    hyd: Hydrology record name.
    soil: Soil record name.
    land_use_mgt: Land-use-management record name.
    soil_plant_init: Soil-plant initialization record name.
    surf_stor: Surface-storage record name.
    snow: Snow record name.
    field: Field record name.
  hydrologic_response_unit_db:
    name: HRU database name.
    dbs: Integer database pointers for the HRU.
    dbsc: Character-name database pointers for the HRU.
  land_use_mgt_variables:
    usle_p: USLE conservation practice (P) factor.
    usle_ls: USLE length-slope (LS) factor.
    usle_mult: Product of USLE K, P, LS, and exp(rock).
    sdr_dep: Subsurface drainage depression-related factor.
    ldrain: Soil layer where the drainage tile is located.
    tile_ttime: Exponential of the tile-flow travel time.
    vfsi: On/off flag for vegetative filter strip simulation.
    vfsratio: Contouring USLE P factor.
    vfscon: Fraction of the total runoff from the entire field.
    vfsch: Fraction of flow entering the most concentrated 10% of the VFS.
    ngrwat: Count or indicator for waterway channels that are fully channelized.
    grwat_i: On/off flag for grassed waterway simulation.
    grwat_n: Manning's n for the grassed waterway.
    grwat_spcon: User-defined sediment transport coefficient.
    grwat_d: Depth of the grassed waterway in meters.
    grwat_w: Width of the grass waterway.
    grwat_l: Length of the grass waterway in kilometers.
    grwat_s: Slope of the grass waterway in m/m.
    bmp_flag: On/off flag for user-defined BMP efficiency.
    bmp_sed: Sediment removal by BMP in percent.
    bmp_pp: Particulate phosphorus removal by BMP in percent.
    bmp_sp: Soluble phosphorus removal by BMP in percent.
    bmp_pn: Particulate nitrogen removal by BMP in percent.
    bmp_sn: Soluble nitrogen removal by BMP in percent.
    bmp_bac: Bacteria removal by BMP in percent.
  nutrient_parameters:
    phoskd: Phosphorus distribution coefficient in kg/m3.
    pperco: Phosphorus percolation coefficient in kg/m3.
    psp: Phosphorus soil partition coefficient in kg/m3.
    nperco: Nitrogen percolation coefficient in kg/m3.
    cmn: Carbon-to-mineralization or mineralization coefficient in kg/m3.
    nperco_lchtile: Nitrogen percolation coefficient for lateral/ch tile flow in kg/m3.
  hydrologic_response_unit:
    name: HRU name.
    obj_no: Object number linking the HRU to the basin object list.
    area_ha: HRU area in hectares.
    km: HRU area converted to square kilometers.
    surf_stor: Pointer to res() for surface storage.
    dbs: Integer database pointers for the HRU.
    dbsc: Character-name database pointers for the HRU.
    land_use_mgt: Index of the active land-use-management record.
    land_use_mgt_c: Character name of the active land-use-management record.
    lum_group: Numeric land-use-management group.
    lum_group_c: Land-use group for soft calibration and output.
    cal_group: Calibration-group name.
    plant_cov: Plant-cover switch used by initialization and calibration routines.
    mgt_ops: Management-operations switch used by scheduling and drainage logic.
    tiledrain: Tile-drain switch.
    septic: Septic-system switch.
    fstrip: Filter-strip switch.
    grassww: Grassed-waterway switch.
    bmpuser: User-defined BMP switch.
    crop_reg: Crop-regime switch.
    paddy_irr: Paddy irrigation switch added by Jaehak Jeong in 2022.
    topo: Embedded topography record.
    field: Embedded field record.
    hyd: Embedded hydrology record.
    hydcal: Calibration hydrology record.
    luse: Embedded landuse record.
    lumv: Embedded land-use-management variables.
    sdr: Embedded subsurface drainage parameters.
    sno: Embedded snow parameters.
    nut: Embedded nutrient parameters.
    sb: Embedded saturated buffer state.
    snocov1: Snow cover state 1.
    snocov2: Snow cover state 2.
    cur_op: Current management-operation pointer.
    irr: Set to 1 if irrigated during simulation for water-balance soft calibration.
    man_trn_dtbl: Manure-transfer decision-table pointer.
    irr_trn_iauto: Auto-irrigation transfer flag or index.
    man_trn_iauto: Auto manure-transfer flag or index.
    wet_db: Pointer to wetland data; saved so wetland on/off state can be restored.
    wet_hc: Hydraulic conductivity of the upper wetland layer in mm/h.
    sno_mm: Amount of water in snow on the current day in mm H2O.
    water_seep: Water seepage from the HRU.
    water_evap: Water evaporation from the HRU.
    wet_obank_in: Inflow from overbank into wetlands in mm.
    precip_aa: Annual-accumulated precipitation or precipitation accounting value.
    irr_yr: Annual irrigation total in mm used as a decision-table condition.
    wet_fp: Wetland flag character, initialized to `n`.
    irr_src: Irrigation source identifier, initialized to `unlim`.
    strsa: Stress-related state variable used by plant and calibration routines.
    irr_hmax: Target ponding depth during paddy irrigation in mm H2O.
    irr_hmin: Threshold ponding depth to trigger paddy irrigation in mm H2O.
    irr_isc: Source identifier for paddy irrigation from channel, reservoir, aquifer, or other
      source.
    flow: 'Average annual flow class code: 1 = wyld, 2 = perc, 3 = surface, 4 = lateral, 5
      = tile.'
type_summaries:
  uptake_parameters: Module-level plant uptake coefficients controlling water, nitrogen, and
    phosphorus uptake distribution and normalization.
  irrigation_sources: Per-HRU irrigation source selector describing which water sources are
    allowed and how irrigation is enabled.
  topography: Topographic characteristics attached to an HRU for runoff, erosion, and routing
    calculations.
  hydrology: Hydrologic coefficients and adjustment factors attached to an HRU.
  snow_parameters: Snowpack temperature and melt parameters for an HRU snow database record.
  subsurface_drainage_parameters: Subsurface drain-tile geometry and flow coefficients for
    an HRU drainage database record.
  saturated_buffer_parameters: Decision-table-controlled saturated buffer routing parameters
    for tile inflow and receiving HRUs.
  saturated_buffer: Runtime saturated-buffer state pairing the buffer definition with routed
    inflow and nitrate mass.
  landuse: Land-use database record controlling curve number, conservation practice, and urban
    runoff behavior.
  soil_plant_initialize: Database selector for initial soil-plant, pesticide, pathogen, salt,
    heat, and carbon starting conditions.
  hru_databases: Integer pointers to the database records used to build an HRU.
  hru_databases_char: Character-name version of the HRU database pointer set, used while resolving
    names to indices.
  hydrologic_response_unit_db: HRU database wrapper combining integer and character database
    pointers for one HRU definition.
  land_use_mgt_variables: Per-HRU land-use-management parameters for erosion control, drains,
    waterways, and BMPs.
  nutrient_parameters: Nutrient transport and partitioning coefficients for HRU soil and water
    chemistry.
  hydrologic_response_unit: Active HRU state combining database pointers, process switches,
    and hydrologic/water-quality storages for one land unit.
---

<!-- facts:header -->

hru_module is the shared HRU state container for SWAT+: it defines the database record types for topography, hydrology, snow, drainage, irrigation, land use, soil-plant initialization, and HRU records, and it exposes the global HRU-related arrays and scalars that initialization, management, routing, calibration, and output routines read and update.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container; it owns the shared HRU database records and active-state arrays, but the actual population comes from reader and initialization routines such as snowdb_read, sdr_read, landuse_read, soil_plant_init, hru_read, hrudb_init, hru_lum_init_all, cn2_init, and related calibration/setup procedures.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:snowdb_read] | `snow database file` | `snodb` | Reads snow parameter records into the allocatable `snodb` table for later HRU snow initialization and name-based lookup. |
| [sym:sdr_read] | `subsurface drainage database file` | `sdr` | Reads drain-tile records into the allocatable `sdr` table so HRUs can reference drainage geometry and lag settings. |
| [sym:sat_buff_read] | `saturated buffer database file` | `satbuff_db` | Reads saturated-buffer routing records into `satbuff_db` for tile-flow diversion and buffer-HRU routing. |
| [sym:landuse_read] | `landuse database file` | `luse` | Reads land-use records into `luse` so HRUs can resolve curve numbers, conservation practices, and urban runoff options. |
| [sym:soil_plant_init] | `soil-plant initialization file` | `sol_plt_ini` | Reads initial soil-plant and related chemistry records into `sol_plt_ini` for HRU startup conditions. |
| [sym:hru_read] | `hru-data.hru` | `hru_db` | Reads the HRU definition tables, resolving database names to indices for the active HRU database wrappers. |
| [sym:hrudb_init] | `module-internal HRU database tables` | `hru` | Copies resolved database pointers and core scalar properties from `hru_db` into the active `hru` array. |
| [sym:hru_lum_init_all] | `module-internal HRU and land-use tables` | `hru` | Initializes each HRU's land-use-management state from the selected land-use database record. |
| [sym:cn2_init] | `module-internal HRU and land-use tables` | `cn2` | Builds the shared curve-number array from HRU land-use and soil references. |
| [sym:dtbl_lum_read] | `lum.dtl` | `hru, snodb` | Uses the HRU table and snow table to resolve land-use decision-table actions and snow-change pointers. |
| [sym:dtbl_scen_read] | `scen_lu.dtl` | `snodb` | Resolves scenario decision-table snow-change references against the snow database. |
| [sym:cal_allo_init] | `module-internal HRU state` | `hru, hru_init, bss` | Allocates and resets calibration-state storage based on the active HRU set and initial HRU copy. |
| [sym:cal_parm_select] | `calibration selector inputs` | `hru, cn2, brt, tconc` | Selects calibration targets and updates HRU-linked parameters and routing state from the active HRU record. |

## Key Consumers

The module is used by nearly every HRU-level process in the model: startup and calibration routines build and reset HRU state, management and routing routines read the active records, and water-quality, sediment, plant, septic, irrigation, drainage, and output routines consume the shared arrays and embedded database pointers.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_sw_init] | `hru` | Copies each HRU's snow water equivalent from `hru(ihru)%sno_mm` so the initial basin snow balance can be recorded. |
| [sym:cal_allo_init] | `hru`, `hru_init`, `bss` | Uses the active HRU definitions and initial HRU copy to allocate or reset calibration storage, while clearing `bss` for a fresh balance state. |
| [sym:cal_parm_select] | `hru`, `cn2`, `brt`, `tconc` | Updates the selected HRU's hydrology, land-use, snow, drainage, and nutrient parameters so later runoff, erosion, and plant-growth routines read the calibrated values. |
| [sym:cn2_init] | `cn2`, `hru` | Uses each HRU's land-use and soil pointers to populate the shared curve-number array consumed by runoff calculations. |
| [sym:cs_balance] | `hru` | Scales HRU-level fluxes and storage terms by HRU area so basin totals can be accumulated correctly. |
| [sym:cs_hru_init] | `hru`, `sol_plt_ini` | Reads each HRU's soil-plant initialization pointer and area so carbon-state initial values can be converted into HRU-scaled mass values. |
| [sym:dtbl_lum_read] | `hru`, `snodb` | Uses HRU names, areas, and snow names to resolve land-use decision-table matches and snow-change action pointers. |
| [sym:dtbl_scen_read] | `snodb` | Looks up snow-table names so scenario decision tables can translate snow-change references into numeric indices. |
| [sym:gwflow_canal_div] | `hru` | Historically routed canal diversions into HRU state; the routine still depends on the HRU array as the land-unit target structure even though the irrigation branch is inactive in the extracted version. |
| [sym:gwflow_read] | `hru` | Allocates groundwater arrays and maps groundwater results back to the HRU set using the total HRU count and HRU-linked routing state. |
| [sym:hru_dtbl_actions_init] | `hru` | Initializes manure-transfer and management action pointers inside each HRU's management state. |
| [sym:hru_fr_change] | `hru` | Recomputes HRU area, kilometer-scale area, object linkage, and surface-storage pointers when an HRU fraction changes. |
| [sym:hru_lum_init] | `hru` | Copies land-use-management codes and related group pointers into the active HRU record so later process routines can read them from one place. |
| [sym:hru_lum_init_all] | `hru` | Populates every HRU's land-use-management selection from the database defaults before detailed initialization. |
| [sym:hru_read] | `hru_db`, `ihru`, `sol_plt_ini`, `snodb` | Builds the HRU database tables from `hru-data.hru`, resolving names to indices that later initialization routines depend on. |
| [sym:hrudb_init] | `hru`, `hru_db` | Copies database pointers and scalar attributes from the HRU database wrappers into the active HRU array. |
| [sym:hydro_init] | `hru`, `sdr`, `dormhr`, `ihru` | Uses HRU, drainage, and dormancy state to compute hydrologic factors that later feed erosion and water-balance calculations. |
| [sym:landuse_read] | `sdr` | Searches the drainage database to resolve tile-drain references stored in the land-use records. |
| [sym:lcu_read_softcal] | `ihru` | Uses the HRU loop index to enumerate HRUs while populating region counts and areas for soft calibration output. |
| [sym:lsreg_output] | `hru`, `ihru` | Walks the HRU array to produce regional land-use output, using HRU areas and land-use-management codes for weighting and grouping. |
| [sym:manure_allocation_read] | `hru` | Writes the matched manure-transfer decision-table index back into each targeted HRU for later management operations. |
| [sym:obj_output] | `ihru` | Uses the active HRU index when seeding residue and object-level output arrays for basin-wide reporting. |
| [sym:pathogen_init] | `hru`, `ihru`, `sol_plt_ini` | Selects the soil-plant initialization record for each HRU so pathogen starting conditions can be loaded. |
| [sym:pesticide_init] | `hru`, `sol_plt_ini` | Selects the pesticide initialization record for each HRU so pesticide starting conditions can be loaded. |

## Lineage

`hru_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 15 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_module.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `29e2d36` (2025-10-29) — Bug fixes and changes related to water allocation
- `1c812c1` (2025-08-21) — Refactor soil-plant initialization and pesticide calculations
- `a03cc8b` (2025-06-26) — Add yearly irrigation calculations across modules
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `hru_module` has no extracted module-level documentation comment.
- Reader rows are based on the explicitly evidenced setup/read routines in the source packet; the importer appendix is the complete deterministic list.
- Some variable meanings remain inferred from source comments only where no caller-specific overlay evidence was provided; those entries should be rechecked if stricter downstream documentation is needed.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
