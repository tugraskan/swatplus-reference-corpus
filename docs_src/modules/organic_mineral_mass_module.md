---
kind: module
symbol: organic_mineral_mass_module
title: organic_mineral_mass_module
status: filled
source_hash: c6f398920c6c73e9
version_label: SWAT+ 62.0.0
variables:
  meta_frac: Real scalar holding none.
  str_frac: Real scalar holding none.
  lig_frac: Real scalar holding none.
  orgz: Variable of `organic_mass` — see the `organic_mass` type.
  mix_org: Variable of `organic_mixing_mass` — see the `organic_mixing_mass` type.
  mnz: Variable of `mineral_nitrogen` — see the `mineral_nitrogen` type.
  mix_mn: Variable of `mineral_nitrogen` — see the `mineral_nitrogen` type.
  mpz: Variable of `mineral_phosphorus` — see the `mineral_phosphorus` type.
  mix_mp: Variable of `mineral_phosphorus` — see the `mineral_phosphorus` type.
  soil1: Allocatable 1-D array of `soil_profile_mass` — soil profile object - dimensioned
    to number of hrus, using the hru pointer.
  soil1_init: Allocatable 1-D array of `soil_profile_mass` — see the `soil_profile_mass` type.
  soil_prof_tot: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_root: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_root_frac: Real scalar — a module-level working variable holding a fraction (no
    inline source comment; interpreted from the name).
  soil_prof_rsd: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_srsd: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_hact: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_hsta: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_hs: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_hp: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_microb: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_seq_hs: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_seq_hp: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_seq_microb: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_str: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_lig: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_nonlig: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_meta: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_sstr: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_slig: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_smeta: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_man: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_water: Variable of `organic_mass` — see the `organic_mass` type.
  soil_org_z: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_somc: Variable of `organic_mass` — see the `organic_mass` type.
  soil_prof_mn: Variable of `mineral_nitrogen` — see the `mineral_nitrogen` type.
  soil_prof_mp: Variable of `mineral_phosphorus` — see the `mineral_phosphorus` type.
  soil_mn_z: Variable of `mineral_nitrogen` — see the `mineral_nitrogen` type.
  soil_mp_z: Variable of `mineral_phosphorus` — see the `mineral_phosphorus` type.
  bsn_org_soil: Variable of `organic_mass` — see the `organic_mass` type.
  bsn_org_pl: Variable of `organic_mass` — see the `organic_mass` type.
  bsn_org_rsd: Variable of `organic_mass` — see the `organic_mass` type.
  bsn_mn: Real scalar — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  bsn_mp: Real scalar — a module-level working variable shared across the importing routines
    (no inline source comment in the declaration).
  decomp: Variable of `organic_mass` — see the `organic_mass` type.
  photo_decomp: Variable of `organic_mass` — see the `organic_mass` type.
  transfer: Variable of `organic_mass` — see the `organic_mass` type.
  pl_burn: Variable of `organic_mass` — see the `organic_mass` type.
  rsd_meta: Variable of `organic_mass` — see the `organic_mass` type.
  rsd_str: Variable of `organic_mass` — see the `organic_mass` type.
  pl_mass: Allocatable 1-D array of `plant_community_mass` — see the `plant_community_mass`
    type.
  pl_mass_init: Allocatable 1-D array of `plant_community_mass` — see the `plant_community_mass`
    type.
  pl_yield: Variable of `organic_mass` — kg/ha.
  pl_mass_up: Variable of `organic_mass` — kg/ha.
  pl_residue: Variable of `organic_mass` — see the `organic_mass` type.
  harv_seed: Variable of `organic_mass` — see the `organic_mass` type.
  harv_leaf: Variable of `organic_mass` — see the `organic_mass` type.
  harv_stem: Variable of `organic_mass` — see the `organic_mass` type.
  harv_left: Variable of `organic_mass` — see the `organic_mass` type.
  graz_plant: Variable of `organic_mass` — see the `organic_mass` type.
  graz_seed: Variable of `organic_mass` — see the `organic_mass` type.
  graz_leaf: Variable of `organic_mass` — see the `organic_mass` type.
  graz_stem: Variable of `organic_mass` — see the `organic_mass` type.
  leaf_drop: Variable of `organic_mass` — kg/ha.
  abgr_drop: Variable of `organic_mass` — kg/ha.
  stem_drop: Variable of `organic_mass` — kg/ha.
  seed_drop: Variable of `organic_mass` — kg/ha.
  plt_mass_z: Variable of `organic_mass` — see the `organic_mass` type.
  fert: Allocatable 1-D array of `fertilizer_mass` — fertilizer object should be used as database
    input from fert.dat dimension to number of fertilzers in database.
  org_frt: Array of `organic_mass` — dimension to number of manures in database.
  manure: Allocatable 1-D array of `organic_mass` — manure object should be used as database
    input from manure.dat dimension to number of manures in database.
  obom: Allocatable 1-D array of `spatial_object_hydrographs` — track spatial_object_hydrographs
    with ob - use same pointer.
  rec_om: Allocatable 1-D array of `recall_organic_mineral_inputs` — see the `recall_organic_mineral_inputs`
    type.
  exco_om: Allocatable 2-D array of `organic_mineral_hydrograph` — export coefficient and
    delivery ratio pesticides.
  dr_om: Allocatable 2-D array of `organic_mineral_hydrograph` — export coefficient and delivery
    ratio pesticides.
  sub_e_hd: Allocatable 1-D array of `routing_unit_elements_hydrographs` — point to subbasin
    element objects - same as sub_elem.
  ch_sur_hd: Allocatable 1-D array of `channel_surface_elements_hydrographs` — point to channel-surface
    objects - same as ch_sur.
  o_m1: Variable of `organic_mineral_mass` — objects needed for operators.
  o_m2: Variable of `organic_mineral_mass` — objects needed for operators.
  o_m3: Variable of `organic_mineral_mass` — objects needed for operators.
  pmin_m1: Variable of `mineral_phosphorus` — see the `mineral_phosphorus` type.
  pmin_m2: Variable of `mineral_phosphorus` — see the `mineral_phosphorus` type.
  pmin_m3: Variable of `mineral_phosphorus` — see the `mineral_phosphorus` type.
  nmin_m1: Variable of `mineral_nitrogen` — see the `mineral_nitrogen` type.
  nmin_m2: Variable of `mineral_nitrogen` — see the `mineral_nitrogen` type.
  nmin_m3: Variable of `mineral_nitrogen` — see the `mineral_nitrogen` type.
type_components:
  organic_mass:
    m: kg/ha      |total object mass
    c: kg/ha      |carbon mass
    n: kg/ha      |organic nitrogen mass
    p: kg/ha      |organic phosphorus mass
  organic_mixing_mass:
    tot: '|total organic pool'
    surf_rsd: '|fresh surface residue mixed into layers'
    rsd: '|fresh soil residue (max 12 plants)'
    hact: 'humus pools for old mineralization model (static carbon)

      |active humus for old mineralization model'
    hsta: '|stable humus for old mineralization model'
    hs: 'organic pools used in CENTURY model

      |slow humus'
    hp: '|passive humus'
    microb: '|microbial biomass'
    str: '|structural litter pool'
    lig: '|lignin pool'
    nonlig: '|non lignin pool'
    meta: '|metabolic litter pool'
    man: '|manure pool'
    water: '|water soluble'
  clay_mass:
    m: kg or kg/ha      |total object mass
    nh4: kg or kg/ha      |ammonium mass
  sediment:
    m: kg or kg/ha      |total object mass
    sand: kg or kg/ha      |sand mass
    silt: kg or kg/ha      |silt mass
    clay: kg or kg/ha      |clay mass
    gravel: kg or kg/ha      |gravel mass
  mineral_nitrogen:
    no3: kg/ha  |nitrate dimensioned by layer
    nh4: kg/ha  |ammonium dimensioned by layer
  mineral_phosphorus:
    wsol: kg/ha  |water soluble p dimensioned by layer
    lab: kg/ha  |labile p dimensioned by layer
    act: kg/ha  |active mineral p dimensioned by layer
    sta: kg/ha  |stable mineral p dimensioned by layer
  plant_residue:
    rsd: '|fresh surface residue dimensioned by layer'
  soil_profile_mass:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    tot_mn: '|total mineral n pool (no3+nh4) in soil profile'
    tot_mp: '|mineral p pool (wsol+lab+act+sta) in soil profile'
    salt: '|total salt amount (kg/ha) in soil profile'
    tot_org: '|total organics in soil profile'
    seq_org: '|sequestered organics in soil profile wich does not include the surface layer'
    surf_org: '|soil surface layer soil soil profile'
    sw: mm     |soil water dimensioned by layer
    cbn: '%      |percent carbon'
    sed: '|sediment dimensioned by layer'
    mn: '|mineral n pool dimensioned by layer'
    mp: '|mineral p humus pool dimensioned by layer'
    tot: 'tot and rsd used for both carbon methods

      |total organic pool dimensioned by layer'
    seq: '|total sequestered organic pool dimensioned by layer, surface layer = 0.0'
    seq_tot_300_c: '|total sequestered equal to or above 300mm soil depth'
    tot_300_c: '|total carbon equal to or above 300mm soil depth'
    emix: '|the fraction of mixing that occurs from tillage or biomixing in each soil layer'
    pl: '|fresh surface residue dimensioned by plant and by layer'
    rsd_tot: '|total fresh surface residue dimensioned by layer'
    root_tot: '|total live roots dimensioned by layer'
    org_con_lr: 'humus pools for old mineralization model (static carbon)

      |organic contral variables by layer'
    org_allo_lr: '|organic allocation variables by layer'
    org_ratio_lr: '|organic nitrogen carbon ratios layer'
    org_tran_lr: '|portential organic transformations layer'
    org_flx_tot: '|total organic flux for soil profile'
    org_flx_lr: '|organic flux by layer'
    org_flx_cum_lr: '|cumulative organic flux by layer'
    hact: '|active humus for old mineralization model dimensioned by layer'
    hsta: '|stable humus for old mineralization model dimensioned by layer'
    hs: 'organic pools used in CENTURY model

      |slow humus dimensioned by layer'
    hp: '|passive humus dimensioned by layer'
    microb: 'rest are used in CENTURY model

      |microbial biomass'
    str: '|structural litter pool dimensioned by layer'
    lig: '|lignin pool dimensioned by layer'
    nonlig: '|non lignin pool dimensioned by layer'
    meta: '|metabolic litter pool dimensioned by layer'
    man: '|manure pool dimensioned by layer'
    water: '|water soluble'
  plant_community_mass:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    tot: kg/ha      |total biomass for individual plant in community
    ab_gr: kg/ha      |above ground biomass for individual plant in community
    leaf: kg/ha      |leaf mass for individual plant in community
    stem: kg/ha      |wood/stalk mass for individual plant in community
    root: kg/ha      |root mass for individual plant in community (by soil layer)
    seed: kg/ha      |seed (grain) mass for individual plant in community
    yield_tot: kg/ha      |running total sum of yield at harvest -  ave annual print
    yield_yr: kg/ha      |running yearly sum of yield at harvest - yearly print
    rsd: kg/ha      |fresh surface residue dimensioned by plant
    rsd_tot: kg/ha      |total fresh surface residue
    tot_com: kg/ha      |total biomass for entire community
    ab_gr_com: kg/ha      |above ground mass for entire community
    leaf_com: kg/ha      |leaf mass for entire community
    stem_com: kg/ha      |wood/stalk mass for entire community
    root_com: kg/ha      |root mass for entire community
    seed_com: kg/ha      |seed (grain) mass for entire community
  mineral_mass:
    m: kg or kg/ha      |total object mass
    no3: kg or kg/ha      |nitrate mass
    no2: kg or kg/ha      |nitrite mass
    nh4: kg or kg/ha      |ammonium mass
    po4: kg or kg/ha      |phosphate mass
  organic_mineral_mass:
    vol: '|a module-level working variable holding a volume (no inline source comment; interpreted
      from the name)'
    hum: '|nested `organic_mass` record'
    hum_act: '|nested `organic_mass` record'
    min: '|nested `mineral_mass` record'
  animal_herds:
    name: '|herd name (small_dairy, )'
    num_tot: '|total number of animals in the herd'
    herd_mass: kg         |total mass of herd
    typ: '|animal type (points to animal.hrd)'
    num: '|number of each type of animal'
    mass: '|mass of each type of animal'
    eat: '|biomass eaten by each type of animal'
    manure: '|manure from each type of animal'
  fertilizer_mass:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    org: soil matrix dimensioned by layer
    min: soil water dimensioned by layer
  organic_mineral_hydrograph:
    flo: m^3          |volume of water
    sed: metric tons  |sediment
    org: '|nested `organic_mass` record'
    min: '|nested `mineral_mass` record'
    chla: kg           |chlorophyll-a
    cbod: kg           |carbonaceous biological oxygen demand
    dox: kg           |dissolved oxygen
    temp: deg c        |temperature
    san: tons         |detached sand
    sil: tons         |detached silt
    cla: tons         |detached clay
    sag: tons         |detached small ag
    lag: tons         |detached large ag
    grv: tons         |gravel
  spatial_object_hydrographs:
    name: should match the object_connectivity object
    hin: 'water and soluble components

      inflow hydrograph for surface runon - sum of all inflow hyds'
    hin_sur: inflow hydrograph for surface flow - sum of all surface inflow hyds
    hin_lat: inflow hydrograph for lateral soil flow - sum of all lateral inflow hyds
    hin_til: inflow hydrograph for tile flow - sum of all tile inflow hyds
    hin_aqu: inflow hydrograph for aquifer flow - sum of all aquifer inflow hyds
    hd: generated hydrograph (ie 1=tot, 2= recharge, 3=surf, etc)
    ts: subdaily hydrographs
    tsin: inflow subdaily hydrograph
    hins: 'sediment (sorbed) in the water components

      inflow hydrograph for surface runon - sum of all inflow hyds'
    hin_ssur: inflow hydrograph for surface flow - sum of all surface inflow hyds
    hin_slat: inflow hydrograph for lateral soil flow - sum of all lateral inflow hyds
    hin_stil: inflow hydrograph for tile flow - sum of all tile inflow hyds
    hds: generated hydrograph (ie 1=tot, 2= recharge, 3=surf, etc)
    tss: subdaily hydrographs
    tsins: inflow subdaily hydrograph
    hin_d: hydrograph output variables
    hin_m: '|nested `organic_mineral_hydrograph` record'
    hin_y: '|nested `organic_mineral_hydrograph` record'
    hin_a: '|nested `organic_mineral_hydrograph` record'
    hout_m: '|nested `organic_mineral_hydrograph` record'
    hout_y: '|nested `organic_mineral_hydrograph` record'
    hout_a: '|nested `organic_mineral_hydrograph` record'
    hdep_m: '|nested `organic_mineral_hydrograph` record'
    hdep_y: '|nested `organic_mineral_hydrograph` record'
    hdep_a: '|nested `organic_mineral_hydrograph` record'
  recall_organic_mineral_inputs:
    name: '|a module-level working variable holding a count (no inline source comment; interpreted
      from the name)'
    num: number of elements
    typ: recall type - 1=day, 2=mon, 3=year
    filename: filename
    hd_om: 'hyd_output units are in cms and mg/L

      export coefficients'
  routing_unit_elements_hydrographs:
    name: should match the object_connectivity object
    hd: '|nested `organic_mineral_mass` record'
  channel_surface_elements_hydrographs:
    name: should match the channel_surface_elements object
    hd: '|nested `organic_mineral_mass` record'
type_summaries:
  organic_mass: One `organic_mass` record groups `m`, `c`, `n`, `p`.
  organic_mixing_mass: One `organic_mixing_mass` record groups `tot`, `surf_rsd`, `rsd`, `hact`,
    `hsta`, `hs`, and 8 more fields.
  clay_mass: One `clay_mass` record groups `m`, `nh4`.
  sediment: One `sediment` record groups `m`, `sand`, `silt`, `clay`, `gravel`.
  mineral_nitrogen: One `mineral_nitrogen` record groups `no3`, `nh4`.
  mineral_phosphorus: One `mineral_phosphorus` record groups `wsol`, `lab`, `act`, `sta`.
  plant_residue: One `plant_residue` record groups `rsd`.
  soil_profile_mass: One `soil_profile_mass` record groups `name`, `tot_mn`, `tot_mp`, `salt`,
    `tot_org`, `seq_org`, and 32 more fields.
  plant_community_mass: One `plant_community_mass` record groups `name`, `tot`, `ab_gr`, `leaf`,
    `stem`, `root`, and 11 more fields.
  mineral_mass: One `mineral_mass` record groups `m`, `no3`, `no2`, `nh4`, `po4`.
  organic_mineral_mass: One `organic_mineral_mass` record groups `vol`, `hum`, `hum_act`,
    `min`.
  animal_herds: Hru will point directly to herds - managed in schedule_ops and ultimately
    can be managed in conditional subroutine. Holds `name`, `num_tot`, `herd_mass`, `typ`,
    `num`, `mass`, and 2 more fields.
  fertilizer_mass: Fertilizer object. Holds `name`, `org`, `min`.
  organic_mineral_hydrograph: One `organic_mineral_hydrograph` record groups `flo`, `sed`,
    `org`, `min`, `chla`, `cbod`, and 8 more fields.
  spatial_object_hydrographs: One `spatial_object_hydrographs` record groups `name`, `hin`,
    `hin_sur`, `hin_lat`, `hin_til`, `hin_aqu`, and 20 more fields.
  recall_organic_mineral_inputs: Recall organic-mineral inputs. Holds `name`, `num`, `typ`,
    `filename`, `hd_om`.
  routing_unit_elements_hydrographs: One `routing_unit_elements_hydrographs` record groups
    `name`, `hd`.
  channel_surface_elements_hydrographs: One `channel_surface_elements_hydrographs` record
    groups `name`, `hd`.
---

<!-- facts:header -->

`organic_mineral_mass_module` owns the soil organic and mineral mass-pool types (`organic_mass`, `mineral_nitrogen`, `mineral_phosphorus`, `plant_residue`, `soil_profile_mass`, `plant_community_mass`, `organic_mineral_mass`) and the metabolic/structural/lignin fraction constants used to partition residue. The per-object mass storage (`obom`) and zero templates are allocated and initialized during setup and consumed by the carbon and nutrient cycling, tillage-mixing, and mass-balance routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-template container. The fraction constants and mass-type defaults are set in their declarations, the zero templates (`orgz`, `mnz`, `mix_org`) provide reset values, and the per-object mass arrays (`obom`) are allocated during basin object setup.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | References `organic_mineral_mass_module` state: references `fert`, `manure`, `pl_mass`, `pl_yield` (e.g. `actions.f90:51`). |
| [sym:basin_read_objs] | `unit_*, object.cnt, chancell.gw, gwflow_record` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Aggregates basin totals from `organic_mineral_mass_module` state: references `obom` (e.g. `basin_read_objs.f90:95`). |
| [sym:cal_allo_init] | `no direct file input (operates on in-memory state)` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Initializes `organic_mineral_mass_module` state: references `pl_mass_init`, `soil1`, `soil1_init`, `pl_mass` (e.g. `cal_allo_init.f90:29`). |
| [sym:cal_parm_select] | `calibration parameter selection (no direct file read here)` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Applies calibration changes to `organic_mineral_mass_module` state: references `soil1` (e.g. `cal_parm_select.f90:296`). |
| [sym:calsoft_read_codes] | `codes.sft` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Imports `organic_mineral_mass_module`; no specific module symbol from it was resolved in the extracted references for `calsoft_read_codes`. |
| [sym:command] | `unit_out_hyd_sep` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Updates `organic_mineral_mass_module` state: references `transfer`, `manure` (e.g. `command.f90:8`). |
| [sym:cs_balance] | `unit_6080, unit_6082, unit_6084, unit_6086` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | References `organic_mineral_mass_module` state: references `transfer` (e.g. `cs_balance.f90:139`). |
| [sym:cs_cha_read] | `cs_channel.ini, cs_streamobs, cs_streamobs_output` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Imports `organic_mineral_mass_module`; no specific module symbol from it was resolved in the extracted references for `cs_cha_read`. |
| [sym:cs_hru_init] | `no direct file input (operates on in-memory state)` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Imports `organic_mineral_mass_module`; no specific module symbol from it was resolved in the extracted references for `cs_hru_init`. |
| [sym:dr_path_read] | `dr_path.del` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Imports `organic_mineral_mass_module`; no specific module symbol from it was resolved in the extracted references for `dr_path_read`. |
| [sym:dr_read_hmet] | `dr_hmet.del` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | Imports `organic_mineral_mass_module`; no specific module symbol from it was resolved in the extracted references for `dr_read_hmet`. |
| [sym:dr_read_om] | `dr_om.del` | `meta_frac, str_frac, lig_frac, orgz, mix_org, mnz` | References `organic_mineral_mass_module` state: references `dr_om` (e.g. `dr_read_om.f90:78`). |

## Key Consumers

Importers include the basin object allocation routines that allocate the per-object mass storage, the carbon and nutrient cycling routines that read and update the organic and mineral pools, the tillage/mixing routines that redistribute mass across layers, and the mass-balance and output routines.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_read_objs] | organic_mineral_mass_module | `organic_mineral_mass_module` matters because this routine allocates `obom(sp_ob%objs)`, the per-object organic/mineral mass storage used later by mass-balance and routing code. |
| [sym:cal_allo_init] | organic_mineral_mass_module | `organic_mineral_mass_module` contains the plant and soil organic-mass structures that this routine allocates and copies. `pl_mass_init` and `soil1_init` must exist as baseline mass states so calibration routines can work with plant biomass and soil organic pools without altering the live model state. |
| [sym:cal_parm_select] | organic_mineral_mass_module | `organic_mineral_mass_module` provides the layered soil carbon and mineral-pool state (`soil1(ielem)%tot(ly)%c`) that is updated by carbon calibration cases such as `cbn`, `lab_p`, and `hum_c_*`. Those values feed the carbon balance and soil pool initialization logic. |
| [sym:cs_balance] | organic_mineral_mass_module | This module provides the constituent database size, point-source mass arrays, and soil-layer constituent arrays that cs_balance sums into basin totals and uses to locate the three simulated constituents in each balance table. |
| [sym:dr_read_om] | organic_mineral_mass_module | The `organic_mineral_mass_module` supplies the organic/mineral mass delivery-ratio state that is being loaded from `dr_om.del` and then assigned to object hydrographs. |
| [sym:exco_read_om] | organic_mineral_mass_module | These module arrays store the organic-matter export-coefficient name list and its numeric cross-reference. `exco_read_om` allocates and populates them from the file so later code can resolve names to records. |
| [sym:lsu_carbon_output] | organic_mineral_mass_module | The routine reads plant community carbon mass from `pl_mass(ihru)%tot_com%c` to compute the LSU plant-carbon state snapshot. That value is area-weighted by LSU fraction and written whenever plant-state output is enabled. |
| [sym:mallo_control] | organic_mineral_mass_module | Provides plant biomass and residue mass values written to management output. |
| [sym:obj_output] | organic_mineral_mass_module | The organic-mass module supplies the carbon, nitrogen, phosphorus, residue, humus, and microbial pools that are written in the nutrient and carbon diagnostics; the routine also updates profile residue and summary pools such as `soil_prof_microb` and `soil_prof_somc` from these states. |
| [sym:plant_init] | organic_mineral_mass_module | `organic_mineral_mass_module` provides the plant-residue and plant-mass types that are allocated, zeroed, and filled with residue and biomass values. Those pools are needed for residue cover, nutrient accounting, and later decomposition and harvest routines. |
| [sym:salt_balance] | organic_mineral_mass_module | The organic/mineral mass state carries the salt constituent storage arrays that are summed here for soil and aquifer stocks, plus point-source salt inputs. Without those arrays, salt_balance could not report dissolved and solid salt stores or point-source totals. |
| [sym:soil_carbvar_write_legacy] | organic_mineral_mass_module | `organic_mineral_mass_module` provides the per-HRU layered soil-carbon container `soil1`. The routine reads its layer-wise carbon controls, allocation ratios, ratio outputs, transformation outputs, and mixing fractions so the legacy files capture the soil carbon state by layer. |
| [sym:soil_nutcarb_init] | organic_mineral_mass_module | `organic_mineral_mass_module` defines the `soil1` per-HRU mass structure that this routine populates. Its layer-wise carbon, mineral nitrogen/phosphorus, humus, residue, and microbial fields are the actual outputs of the initialization. |
| [sym:soil_nutcarb_write_legacy] | organic_mineral_mass_module | `organic_mineral_mass_module` supplies the per-HRU carbon, nitrogen, phosphorus, residue, root, humus, microbial, and flux pools that this routine aggregates and writes. Without these shared mass objects, the routine could not form the layer and profile totals for soil, plant, residue, and organic-flux output. |
| [sym:soils_init] | organic_mineral_mass_module | The organic and mineral mass module matters because `soils_init` allocates the HRU-level carbon, sediment, residue, and nutrient state arrays stored there. Those arrays must match the soil-layer count created here so later carbon and nutrient routines can update per-layer mass pools. |
| [sym:wallo_control] | organic_mineral_mass_module | Routes one water-allocation transfer through demand, withdrawal, transfer, and receiving-object updates. |
| [sym:calsoft_read_codes] | organic_mineral_mass_module | This module is imported as part of the calibration dependency set for nutrient and sediment mass accounting, but no symbols from it are referenced in the visible routine body. |
| [sym:cs_cha_read] | organic_mineral_mass_module | Channel constituent initialization feeds the broader mass-transport system. This module matters because the concentrations read here are part of the model’s mass state that downstream transport and output routines depend on. |
| [sym:cs_hru_init] | organic_mineral_mass_module | No candidate outside references were resolved to `organic_mineral_mass_module` in the provided context, so its specific imported state is not identifiable from this packet. The module is listed as a dependency, but the source excerpt does not show any used symbols from it. |
| [sym:dr_path_read] | organic_mineral_mass_module | The module is imported by the routine, but no extracted symbols from it are used in the visible source, so it does not affect the documented behavior here. |
| [sym:dr_read_hmet] | organic_mineral_mass_module | These constituent-mass arrays hold the heavy-metal delivery-ratio coefficients that are read from file, sized by the number of simulated metals, and then copied into each object’s constituent hydrograph for later transport calculations. |
| [sym:dr_read_pest] | organic_mineral_mass_module | The organic/mineral mass module is imported, but no extracted references from it appear in this routine. The lineages and source excerpt show no direct use of its state here, so its presence appears unused in the visible body. |
| [sym:dr_read_salt] | organic_mineral_mass_module | `organic_mineral_mass_module` is listed in the routine’s uses list, but no candidate outside references from that module were resolved in the extracted source. It may be included for shared constituent/mass definitions or module-wide context even though no direct symbol use was captured here. |
| [sym:exco_read_hmet] | organic_mineral_mass_module | The source imports this module, but no symbol from it is referenced in the extracted procedure body. It matters only as a retained dependency in the routine's `use` list, not as an active data source in the shown code. |

## Lineage

`organic_mineral_mass_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 31 non-merge commit(s) since, most recently `e7b610a` (2026-05-13, "Finished changing code to output files to reflect lignin and non lignin n, c, an…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `organic_mineral_mass_module.f90` are listed.

- `e7b610a` (2026-05-13) — Finished changing code to output files to reflect lignin and non lignin n, c, and p amounts.
- `5323b15` (2026-05-13) — Initial changes to calculate non-lignin c and output to hru_cpool_stat
- `4abc737` (2026-03-18) — Added basic photo decomp to cbn_surfrsd_decomp.
- `0fee6d7` (2026-03-06) — Fixed issue with tillage events not happening in code when cswat=3 and added mixing efficiency to the output of hru_carbvars.txt and used ti…
- `413134d` (2026-03-04) — Calculated the 300 mm sum of total carbon and output it hru_cbn_lyr.txt. New column name is 300_sum. Similar column in hru_seq_lyr changed t…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `organic_mineral_mass_module` has no extracted module-level documentation comment.
- Reader rows show 12 candidate initialization/read routines out of 45; treat the table as representative, not exhaustive.
- This module is imported by 140 procedures; the main Used By table shows 24 ranked consumers and the collapsible importer list keeps the complete deterministic list.
- variable_notes and type_notes summaries were completed locally from the module's declaration metadata (type, shape, source comments) and the Derived Type Inventory; reader behaviors were grounded in source references found in each reader. 0 module-level scalar(s) had no inline source comment and were given name-based interpretations — these should be spot-checked.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
