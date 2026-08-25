---
kind: module
symbol: carbon_module
title: carbon_module
status: filled
source_hash: 9716a6044e524b14
version_label: SWAT+ 62.0.0
variables:
  cbn_diagnostics: legacy CSU carbon-output switch. set by `carbon_legacy_open` from the HRU
    carbon print flags at startup; not read from an input file directly in this module. default
    `.false.` is only a pre-run placeholder. controls legacy plc/cflux/cpool and soil-property
    files.
  n_act_frac: basin-wide carbon initialization / decomposition tunable read from `carbon.bsn`.
    fraction of organic N in the active humus pool; used in nutrient mineralization logic
    and calibrated via `cal_parm_select`.
  cnr_cap: basin-wide residue decomposition cap read from `carbon.bsn`. upper bound on residue
    C:N ratio before the decomposition response is computed.
  cnr_ref: basin-wide residue decomposition reference read from `carbon.bsn`. C:N ratio where
    the decomposition factor equals 1.
  cpr_cap: basin-wide residue decomposition cap read from `carbon.bsn`. upper bound on residue
    C:P ratio before the decomposition response is computed.
  cpr_ref: basin-wide residue decomposition reference read from `carbon.bsn`. C:P ratio where
    the decomposition factor equals 1.
  cb_n_layers: number of soil layers written by the carbon per-layer output routines. defaults
    to 7, may be overridden by `carbon_layers.prt`, and otherwise is expanded by `output_landscape_init`
    to the largest HRU soil-layer count.
  cb_n_layers_explicit: flag that records whether `cb_n_layers` came from `carbon_layers.prt`.
    `.true.` means the optional file supplied an explicit count.
  cb_lyr_missing: sentinel value written into per-layer output rows when a soil profile has
    fewer layers than `cb_n_layers`.
  cpool_vars: column-name list for wide carbon pool output files. `cb_write_wide_header` appends
    `_lyr1..._lyrN` to each base name when building per-layer headers.
  n_p_pool_vars: column-name list for wide per-layer carbon pool nitrogen/phosphorus output
    files. used by the output initialization and writer helpers to label `hru_n_p_pool_stat`
    rows.
  cflux_vars: column-name list for organic carbon/nitrogen flux output files. used by the
    carbon output helpers for the wide layer-expanded flux tables.
  carb_drv_vars: column-name list for carbon driver output files. names correspond to soil
    water, temperature, oxygen, tillage, and related controls.
  carb_dyn_vars: column-name list for carbon dynamic-state output files. names correspond
    to organic fractions, ratios, and transformation rates.
  soil_snap_vars: column-name list for per-layer soil property snapshot outputs. used by the
    carbon output initialization code for `hru_soil_snap` files.
  carbdb: global per-layer carbon input coefficients. array of `carbon_inputs` records populated
    from `carbon.bsn` / `_lyr.bsn` and consumed by carbon transformation and initialization
    routines.
  carbz: single `carbon_inputs` working record used as a zero/default template for carbon
    input coefficients.
  man_coef: global manure conversion coefficient record populated from `carbon.bsn`. used
    when routing manure solids into carbon pools and by calibration.
  org_allo: global organic allocation coefficient array populated from `carbon.bsn` / `_lyr.bsn`.
    drives how decomposed carbon is partitioned among CO2 and humus pools.
  org_alloz: single `organic_allocations` zero/default template used for reset or comparison
    of allocation coefficients.
  org_con: global organic control record holding soil-water, temperature, oxygen, tillage,
    respiration, and response-curve controls used by carbon transformation routines and `fcgd`.
  org_frac: global organic fraction record holding litter fractions and initial sequestered-pool
    fractions; populated during carbon initialization and used by `soil_nutcarb_init` and
    carbon calibration.
  org_ratio: global organic ratio record used to hold active carbon/nitrogen ratio state for
    standing dead and humus pools during carbon transformations.
  org_ratio_zero: zero-value template for `org_ratio`, used when resetting or copying carbon
    ratio state.
  cb_wtr_coef: global carbon-water coefficient record populated from `carbon.bsn`; used by
    carbon and nutrient routing routines to control dissolved carbon movement.
  org_tran: global organic transformation record accumulating potential or realized carbon/nitrogen
    transformations among litter, microbial biomass, slow humus, and passive humus.
  org_tran_zero: zero-value template for `org_tran`, used to reset carbon transformation state.
  org_flux: global organic flux record accumulating carbon and nitrogen fluxes among pools
    for reporting and accounting.
  org_flux_zero: zero-value template for `org_flux`, used to reset flux state.
  hscfz: zero-value template for HRU/LSU/basin carbon transformation summary records (`carbon_soil_transformations`).
  hscf_d: daily HRU carbon transformation summary record. used by daily and period carbon
    output routines.
  hscf_m: monthly HRU carbon transformation summary record.
  hscf_y: yearly HRU carbon transformation summary record.
  hscf_a: average-annual HRU carbon transformation summary record.
  lscf_d: daily LSU carbon transformation summary record.
  lscf_m: monthly LSU carbon transformation summary record.
  lscf_y: yearly LSU carbon transformation summary record.
  lscf_a: average-annual LSU carbon transformation summary record.
  lcsf_a: average-annual basin/landscape carbon transformation summary record used in basin-scale
    reporting.
  bscf_d: daily basin carbon transformation summary record.
  bscf_m: monthly basin carbon transformation summary record.
  bscf_y: yearly basin carbon transformation summary record.
  bscf_a: average-annual basin carbon transformation summary record.
  hscz: zero-value template for HRU/LSU/basin soil carbon gain/loss records (`carbon_soil_gain_losses`).
  hsc_d: daily HRU soil carbon gain/loss record. records runoff, sediment, percolation, residue
    decay, manure, respiration, and emission losses or gains.
  hsc_m: monthly HRU soil carbon gain/loss record.
  hsc_y: yearly HRU soil carbon gain/loss record.
  hsc_a: average-annual HRU soil carbon gain/loss record.
  lsc_d: daily LSU soil carbon gain/loss record.
  lsc_m: monthly LSU soil carbon gain/loss record.
  lsc_y: yearly LSU soil carbon gain/loss record.
  lsc_a: average-annual LSU soil carbon gain/loss record.
  bsc_d: daily basin soil carbon gain/loss record.
  bsc_m: monthly basin soil carbon gain/loss record.
  bsc_y: yearly basin soil carbon gain/loss record.
  bsc_a: average-annual basin soil carbon gain/loss record.
  hrcz: zero-value template for HRU/LSU/basin residue carbon gain/loss records (`carbon_residue_gain_losses`).
  hrc_d: daily HRU residue carbon gain/loss record. tracks residue inputs, decay losses, harvest
    removal, and burn emissions.
  hrc_m: monthly HRU residue carbon gain/loss record.
  hrc_y: yearly HRU residue carbon gain/loss record.
  hrc_a: average-annual HRU residue carbon gain/loss record.
  lrc_d: daily LSU residue carbon gain/loss record.
  lrc_m: monthly LSU residue carbon gain/loss record.
  lrc_y: yearly LSU residue carbon gain/loss record.
  lrc_a: average-annual LSU residue carbon gain/loss record.
  brc_d: daily basin residue carbon gain/loss record.
  brc_m: monthly basin residue carbon gain/loss record.
  brc_y: yearly basin residue carbon gain/loss record.
  brc_a: average-annual basin residue carbon gain/loss record.
  hpcz: zero-value template for HRU/LSU/basin plant carbon gain/loss records (`carbon_plant_gain_losses`).
  hpc_d: daily HRU plant carbon gain/loss record. tracks growth, harvest, drop, grazing, and
    burn emission carbon.
  hpc_m: monthly HRU plant carbon gain/loss record.
  hpc_y: yearly HRU plant carbon gain/loss record.
  hpc_a: average-annual HRU plant carbon gain/loss record.
  lpc_d: daily LSU plant carbon gain/loss record.
  lpc_m: monthly LSU plant carbon gain/loss record.
  lpc_y: yearly LSU plant carbon gain/loss record.
  lpc_a: average-annual LSU plant carbon gain/loss record.
  bpc_d: daily basin plant carbon gain/loss record.
  bpc_m: monthly basin plant carbon gain/loss record.
  bpc_y: yearly basin plant carbon gain/loss record.
  bpc_a: average-annual basin plant carbon gain/loss record.
type_components:
  carbon_inputs:
    hp_rate: rate of transformation of passive humus under optimal conditions
    hs_rate: rate of transformation of slow humus under optimal conditions
    microb_rate: rate of transformation of microbial biomass and associated products under
      optimal conditions
    meta_rate: rate of transformation of metabolic litter under optimal conditions
    str_rate: rate of potential transformation of structural litter under optimal conditions
    microb_top_rate: coefficient adjusting microbial activity in the top soil layer
    hs_hp: coefficient in Century-style allocation from slow to passive humus
    microb_koc: liquid-solid partition coefficient for microbial biomass
    min_n_frac: fraction of mineral N sorbed to litter
    c_org_frac: carbon fraction of organic materials
  manure_coef:
    rtof: weighting factor used to partition septic effluent organic N and P between fresh
      and stable organic pools
    man_to_c: conversion factor from manure solids to carbon
  organic_allocations:
    abp: fraction of decomposed microbial biomass allocated to passive humus
    asp: fraction of decomposed slow humus allocated to passive humus
    a1co2: fraction of decomposed metabolic and passive pools routed to CO2
    asco2: fraction of decomposed slow humus allocated to CO2
    apco2: fraction of decomposed passive humus allocated to CO2
    abco2: fraction of decomposed microbial biomass allocated to CO2
  organic_controls:
    sut: soil water control on biological processes
    cdg: soil temperature control on biological processes
    cs: combined factor controlling biological processes
    ox: oxygen control on biological processes
    till_eff: tillage effect
    x1: tillage control on residue decomposition
    no3: NO3 adjustment used in `cbn_zhang2`
    nh4: NH4 adjustment used in `cbn_zhang2`
    resp: CO2 respiration
    tn: minimum temperature bound
    top: optimum temperature bound
    tx: maximum temperature bound
    tmpf: temperature factor approach used in `cbn_zhang2`
    watf: water factor approach used in `cbn_zhang2`
  organic_fractions:
    lmf: fraction of litter that is metabolic
    lmnf: fraction of metabolic litter that is nitrogen
    lsf: fraction of litter that is structural
    lslf: fraction of structural litter that is lignin
    lsnf: fraction of structural litter that is nitrogen
    frac_seq: fraction of total carbon assigned to sequestered carbon during initialization
    frac_not_seq: fraction of total carbon assigned to non-sequestered carbon during initialization
    frac_hum_microb: fraction of carbon that is microbial pool during initialization
    frac_hum_slow: fraction of carbon that is slow humus pool during initialization
    frac_hum_passive: fraction of carbon that is passive humus pool during initialization
    mathers_method: logical flag for the Mathers slow-humus initialization method
  organic_ratio:
    ncbm: C/N ratio of standing dead and related biomass state
    nchp: N/C ratio of passive humus
    nchs: N/C ratio of slow humus
  carbon_water_coef:
    prmt_21: KOC for carbon loss in water and sediment
    prmt_44: ratio of soluble carbon concentration in runoff to percolate
  organic_transformations:
    bmctp: potential transformation of C in microbial biomass
    bmntp: potential transformation of N in microbial biomass
    hsctp: potential transformation of C in slow humus
    hsntp: potential transformation of N in slow humus
    hpctp: potential transformation of C in passive humus
    hpntp: potential transformation of N in passive humus
    lmctp: potential transformation of C in metabolic litter
    lmntp: potential transformation of N in metabolic litter
    lsctp: potential transformation of C in structural litter
    lslctp: potential transformation of C in lignin of structural litter
    lslnctp: potential transformation of C in nonlignin structural litter
    lsntp: potential transformation of N in structural litter
  organic_flux:
    cfmets1: C transformed from metabolic litter to microbial biomass
    cfstrs1: C transformed from structural litter to microbial biomass
    cfstrs2: C transformed from structural litter to slow humus
    efmets1: N transformed from metabolic litter to microbial biomass
    efstrs1: N transformed from structural litter to microbial biomass
    efstrs2: N transformed from structural litter to slow humus
    immmets1: N immobilization from metabolic litter to microbial biomass transformation
    immstrs1: N immobilization from structural litter to microbial biomass transformation
    immstrs2: N immobilization from structural litter to slow humus transformation
    mnrmets1: N mineralization from metabolic litter to microbial biomass transformation
    mnrstrs1: N mineralization from structural litter to microbial biomass transformation
    mnrstrs2: N mineralization from structural litter to slow humus transformation
    co2fmet: CO2 production from metabolic litter transformations
    co2fstr: CO2 production from lignin structural litter transformations
    cfs1s2: C transformed from microbial biomass to slow humus
    cfs1s3: C transformed from microbial biomass to passive humus
    cfs2s1: C transformed from slow humus to microbial biomass
    cfs2s3: C transformed from slow humus to passive humus
    cfs3s1: C transformed from passive humus to microbial biomass
    efs1s2: N transformed from microbial biomass to slow humus
    efs1s3: N transformed from microbial biomass to passive humus
    efs2s1: N transformed from slow humus to microbial biomass
    efs2s3: N transformed from slow humus to passive humus
    efs3s1: N transformed from passive humus to microbial biomass
    imms1s2: N immobilization from microbial biomass to slow humus transformation
    imms1s3: N immobilization from microbial biomass to passive humus transformation
    imms2s1: N immobilization from slow humus to microbial biomass transformation
    imms2s3: N immobilization from slow humus to passive humus transformation
    imms3s1: N immobilization from passive humus to microbial biomass transformation
    mnrs1s2: N mineralization from microbial biomass to slow humus transformation
    mnrs1s3: N mineralization from microbial biomass to passive humus transformation
    mnrs2s1: N mineralization from slow humus to microbial biomass transformation
    mnrs2s3: N mineralization from slow humus to passive humus transformation
    mnrs3s1: N mineralization from passive humus to microbial biomass transformation
    co2fs1: CO2 production from microbial biomass transformations
    co2fs2: CO2 production from slow humus transformations
    co2fs3: CO2 production from passive humus transformations
  carbon_soil_transformations:
    meta_micr: C transformed from metabolic litter to microbial biomass
    str_micr: C transformed from structural litter to microbial biomass
    str_hs: C transformed from structural litter to slow humus
    co2_meta: CO2 production from metabolic litter transformations
    co2_str: CO2 production from lignin structural litter transformations
    micr_hs: C transformed from microbial biomass to slow humus
    micr_hp: C transformed from microbial biomass to passive humus
    hs_micr: C transformed from slow humus to microbial biomass
    hs_hp: C transformed from slow humus to passive humus
    hp_micr: C transformed from passive humus to microbial biomass
    co2_micr: CO2 production from microbial biomass transformations
    co2_hs: CO2 production from slow humus transformations
    co2_hp: CO2 production from passive humus transformations
  carbon_soil_gain_losses:
    sed_c: carbon transported with sediment yield
    surq_c: dissolved carbon transported with surface runoff
    latq_c: dissolved organic carbon transported with lateral flow
    perc_c: total dissolved carbon transported with percolate
    rsd_decay_c: carbon added to soil from residue decay
    man_app_c: carbon applied to soil from manure
    man_graz_c: carbon manure from grazing animals
    rsp_c: CO2 production from soil respiration summarized for the profile
    emit_c: CO2 production from burning soil carbon
  carbon_residue_gain_losses:
    plant_surf_c: carbon added to surface residue from leaf drop and kill
    plant_root_c: carbon added to soil residue from root kill
    rsd_surfdecay_c: carbon lost from surface residue decay
    rsd_rootdecay_c: carbon lost from soil/root and incorporated residue decay
    harv_stov_c: carbon removed during surface residue harvest
    emit_c: CO2 production from burning surface residue carbon
  carbon_plant_gain_losses:
    npp_c: plant carbon growth from photosynthesis
    harv_abgr_c: carbon removed during grain/biomass harvest
    harv_root_c: carbon removed during tuber/root harvest
    drop_c: carbon added to residue from leaf drop and kill
    grazeat_c: carbon eaten by animals during grazing
    emit_c: CO2 production from burning residue carbon
type_summaries:
  carbon_inputs: Per-layer carbon coefficient set used by soil carbon initialization and carbon-rate
    calculations.
  manure_coef: Manure-to-carbon conversion coefficients used in basin carbon initialization
    and grazing/manure routing.
  organic_allocations: Carbon allocation fractions that split decomposed pool carbon among
    passive humus and CO2.
  organic_controls: Environmental and response-curve controls for organic matter transformations.
  organic_fractions: Initial litter and sequestered-carbon fraction settings for soil carbon
    initialization.
  organic_ratio: Working carbon/nitrogen ratio state for standing dead and humus pools.
  carbon_water_coef: Water-routing coefficients that affect dissolved carbon loss pathways.
  organic_transformations: Potential transformation rates among litter, microbial biomass,
    slow humus, and passive humus pools.
  organic_flux: Detailed carbon and nitrogen flux bookkeeping among litter, microbial, slow,
    and passive pools.
  carbon_soil_transformations: Carbon transformation summaries for litter, microbial, slow,
    and passive pool exchanges at soil scale.
  carbon_soil_gain_losses: Soil-scale carbon gains and losses from runoff, sediment, percolation,
    residue decay, manure, respiration, and emissions.
  carbon_residue_gain_losses: Residue-scale carbon gains and losses from plant input, decay,
    harvest, and burning.
  carbon_plant_gain_losses: Plant-scale carbon gains and losses from photosynthesis, harvest,
    drop, grazing, and burning.
---

<!-- facts:header -->

`carbon_module` owns the shared carbon parameter state, carbon-control structures, carbon pool output labels, and daily/monthly/yearly/annual carbon accounting records used across SWAT+ soil, residue, plant, and landscape output workflows. It also provides the small header-writing helpers for the carbon output files, so initialization and reporting code can use the same module-level configuration and zero-value templates consistently.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

`carbon_module` is a declaration-and-state module: it defines carbon control variables, derived-type records, zero templates, and output label arrays, while startup/setup routines such as `carbon_bsn_read`, `carbon_layers_read`, `carbon_legacy_open`, `output_landscape_init`, and `soil_nutcarb_init` populate or adjust those variables before carbon reporting and process routines run.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:basin_output] | `unit_2050, unit_2054, unit_2060, unit_2064, unit_2070, unit_2074, unit_2080, unit_2084, unit_2051, unit_2055, unit_2061, unit_2065, unit_2071, unit_2075, unit_2081, unit_2085, unit_2052, unit_2056, unit_2062, unit_2066, unit_2072, unit_2076, unit_2082, unit_2086, unit_2053, unit_2057, unit_2063, unit_2067, unit_2073, unit_2077, unit_2083, unit_2087` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Listed as a module user, but no concrete carbon-module symbol references were extracted from the routine body in the provided evidence. |
| [sym:cal_parm_select] | `calibration change selector input` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Applies calibration updates to carbon basin tunables and carbon response coefficients when the selected parameter belongs to the carbon submodel. |
| [sym:carbon_bsn_read] | `unit_*, unit_9001, carbon.bsn, _lyr.bsn` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Reads basin-scale carbon controls and per-layer carbon coefficients from the carbon configuration files into module state. |
| [sym:carbon_layers_read] | `carbon_layers.prt, unit_9001` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Reads an optional per-layer output count and updates the carbon layer configuration used by output writers. |
| [sym:carbon_legacy_module::carbon_legacy_open] | `unit_8348, unit_9000, unit_8349, unit_8358, unit_8359, unit_8382, unit_8383, unit_8386, unit_8387, unit_8384, unit_8385, unit_8360, unit_8363, unit_8367, unit_8368, unit_8372, unit_8373, unit_8374, unit_8375, unit_8376, unit_8377, unit_8378, unit_8379, unit_8380, unit_8381, unit_8366` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Initializes legacy carbon output units and sets the `cbn_diagnostics` legacy-output switch from the HRU carbon print flags. |
| [sym:hru_carbon_output] | `unit_4520, unit_4550, unit_4521, unit_4551, unit_4522, unit_4552, unit_4523, unit_4553` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Reads and rolls HRU carbon gain/loss and transformation accumulators, then resets period totals to the module zero templates after printing. |
| [sym:hru_control] | `unit_100100` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Resets daily HRU carbon summary records to their zero templates before daily process routines accumulate new carbon fluxes. |
| [sym:hru_output] | `unit_2000, unit_2004, unit_2020, unit_2024, unit_2030, unit_2034, unit_2040, unit_2044, unit_2001, unit_2005, unit_2021, unit_2025, unit_2031, unit_2035, unit_2041, unit_2045, unit_2002, unit_2006, unit_2022, unit_2026, unit_2032, unit_2036, unit_2042, unit_2046, unit_2003, unit_2007, unit_2023, unit_2027, unit_2033, unit_2037, unit_2043, unit_2047, unit_4008, unit_4009` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Handles HRU output file routing; carbon-module use is present in the build, but no direct carbon symbol references were extracted from the visible routine body. |
| [sym:lsu_carbon_output] | `unit_4750, unit_4758, unit_4766, unit_4751, unit_4759, unit_4767, unit_4752, unit_4760, unit_4768, unit_4753, unit_4761, unit_4769` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Area-weights HRU carbon outputs to LSU totals, writes LSU carbon summaries, and resets LSU period accumulators using the module zero templates. |
| [sym:output_landscape_init] | `unit_2000, unit_9000, unit_2004, unit_2001, unit_2005, unit_2002, unit_2006, unit_2003, unit_2007, unit_2020, unit_2024, unit_3333, unit_3334, unit_3335, unit_3336, unit_3337, unit_3338, unit_3339, unit_3340, unit_2021, unit_2025, unit_2022, unit_2026, unit_2023, unit_2027, unit_4520, unit_4524, unit_4521, unit_4525, unit_4522, unit_4526, unit_4523, unit_4527, unit_4550, unit_4554, unit_4551, unit_4555, unit_4552, unit_4556, unit_4553, unit_4557, unit_2030, unit_2034, unit_2031, unit_2035, unit_2032, unit_2036, unit_2033, unit_2037, unit_2040, unit_2044, unit_2041, unit_2045, unit_2042, unit_2046, unit_2043, unit_2047, unit_2300, unit_2304, unit_2301, unit_2305, unit_2302, unit_2306, unit_2303, unit_2307, unit_2440, unit_2444, unit_2441, unit_2445, unit_2442, unit_2446, unit_2443, unit_2447, unit_2460, unit_2464, unit_2461, unit_2465, unit_2462, unit_2466, unit_2463, unit_2467, unit_2140, unit_2144, unit_2141, unit_2145, unit_2142, unit_2146, unit_2143, unit_2147, unit_2150, unit_2154, unit_2151, unit_2155, unit_2152, unit_2156, unit_2153, unit_2157, unit_2160, unit_2164, unit_2161, unit_2165, unit_2162, unit_2166, unit_2163, unit_2167, unit_2170, unit_2174, unit_2171, unit_2175, unit_2172, unit_2176, unit_2173, unit_2177, unit_2050, unit_2054, unit_2051, unit_2055, unit_2052, unit_2056, unit_2053, unit_2057, unit_2060, unit_2064, unit_2061, unit_2065, unit_2062, unit_2066, unit_2063, unit_2067, unit_2070, unit_2074, unit_2071, unit_2075, unit_2072, unit_2076, unit_2073, unit_2077, unit_2080, unit_2084, unit_2081, unit_2085, unit_2082, unit_2086, unit_2083, unit_2087, unit_4010, unit_4011, unit_4008, unit_4009, unit_4750, unit_4754, unit_4751, unit_4755, unit_4752, unit_4756, unit_4753, unit_4757, unit_4758, unit_4762, unit_4759, unit_4763, unit_4760, unit_4764, unit_4761, unit_4765, unit_4766, unit_4770, unit_4767, unit_4771, unit_4768, unit_4772, unit_4769, unit_4773` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Determines the effective per-layer carbon output width and opens the carbon output files using the module's variable-name arrays. |
| [sym:soil_carbvar_write_legacy] | `unit_8374, unit_8375, unit_8376, unit_8377, unit_8378, unit_8379, unit_8380, unit_8381` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Writes legacy CSU carbon variable output using the module's carbon-control and carbon-state record types embedded in HRU soil structures. |
| [sym:soil_nutcarb_init] | `HRU soil and soil-plant initialization records` | `cbn_diagnostics, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | Initializes layer-by-layer soil nutrient and carbon pools, including the organic-fraction settings stored in `org_frac`. |

## Key Consumers

The main consumers are carbon initialization readers, the legacy carbon-output opener, the HRU/LSU carbon output writers, and the carbon process routines that compute residue, soil, and plant carbon transformations. Output initialization also relies on the module's variable-name arrays and the optional carbon layer-count control.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:carbon_layers_read] | `cb_n_layers`, `cb_n_layers_explicit` | Later carbon output code uses the layer-count setting and the explicit-file flag that this routine updates, so per-layer carbon outputs can match the optional `carbon_layers.prt` configuration. |
| [sym:cal_parm_select] | carbon_module | Later calibration steps can adjust carbon basin tunables, organic fractions, carbon-water coefficients, and allocation fractions stored in this module. |
| [sym:carbon_bsn_read] | carbon_module | Later carbon initialization and transformation code reads the basin carbon controls, per-layer coefficients, and allocation settings populated by this reader. |
| [sym:hru_carbon_output] | carbon_module | Later HRU carbon reporting uses the HRU soil, residue, plant, and transformation records stored here, then rolls them into monthly, yearly, and average-annual totals before resetting them to the module zero templates. |
| [sym:lsu_carbon_output] | carbon_module | Later LSU reporting uses the HRU and LSU carbon records stored here, area-weights the HRU values to LSU totals, and resets the daily LSU summaries to the zero templates after output. |
| [sym:soil_nutcarb_init] | carbon_module | Later soil carbon initialization uses the organic-fraction settings from this module to split initial carbon into passive, slow, microbial, and residue pools. |
| [sym:soil_nutcarb_write_legacy] | carbon_module | Later legacy soil-carbon output uses the shared carbon-control and carbon-state record types from this module to write HRU and basin summary files. |
| [sym:basin_output] | carbon_module | No direct carbon-module symbol references were extracted, but the module remains part of the compile-time state used by basin output routines. |
| [sym:soil_carbvar_write_legacy] | carbon_module | Later legacy carbon-variable output writes the carbon-control, allocation, ratio, and transformation records embedded in the HRU soil state. |
| [sym:cbn_rsd_decomp] | `cnr_cap`, `cnr_ref`, `cpr_cap`, `cpr_ref` | Later residue decomposition calculations use these ratio caps and reference values to compute C:N and C:P limitation factors. |
| [sym:cbn_surfrsd_decomp] | `cnr_cap`, `cnr_ref`, `cpr_cap`, `cpr_ref` | Later surface-residue decomposition uses these ratio caps and reference values to limit daily residue decay by residue quality. |
| [sym:fcgd] | `org_con` | Later temperature-factor calculations use the shared organic-control thresholds `org_con%tn`, `org_con%top`, and `org_con%tx` instead of hard-coded bounds. |
| [sym:rsd_decomp] | `hrc_d` | Later residue-decay bookkeeping uses `hrc_d(j)%rsd_surfdecay_c` to store the HRU carbon loss from surface residue decay. |
| [sym:cbn_zhang2] | carbon_module | Later soil organic-matter calculations use the shared organic controls, fractions, allocation coefficients, and flux records populated in this module. |
| [sym:hru_output_allo] | carbon_module | Later HRU output allocation uses the carbon gain/loss and transformation record types defined here to size the daily, monthly, yearly, and annual carbon output arrays. |
| [sym:mgt_harvbiomass] | carbon_module | Later harvest bookkeeping uses `hrc_d(j)%plant_surf_c` and `hpc_d(j)%harv_abgr_c` so harvested above-ground biomass is reflected in residue and plant carbon accounting. |
| [sym:mgt_harvgrain] | carbon_module | Later grain-harvest bookkeeping uses `hpc_d(j)%harv_abgr_c` to track carbon removed in the harvested yield. |
| [sym:mgt_harvresidue] | carbon_module | Later residue-harvest bookkeeping uses `hrc_d(j)%harv_stov_c` to store the carbon removed from surface residue. |
| [sym:mgt_killop] | carbon_module | Later plant-kill bookkeeping uses `hrc_d(j)%plant_surf_c`, `hrc_d(j)%plant_root_c`, and `hpc_d(j)%drop_c` to record the carbon transferred into residue pools. |
| [sym:nut_orgnc2] | carbon_module | Later runoff and percolation routing uses `cb_wtr_coef%prmt_21` and `cb_wtr_coef%prmt_44` to move dissolved and biomass carbon, while `hsc_d(j)` stores the resulting HRU carbon losses. |
| [sym:pl_biomass_gro] | carbon_module | Later plant-growth carbon accounting uses `hpc_d(j)%npp_c` to record daily plant carbon growth when the basin carbon option is active. |
| [sym:pl_burnop] | carbon_module | Later burn accounting uses `hrc_d(j)%emit_c` and `hpc_d(j)%emit_c` to record carbon emitted by fire. |
| [sym:pl_leaf_senes] | carbon_module | Later senescence accounting uses `hrc_d(j)%plant_surf_c` and `hpc_d(j)%drop_c` to record carbon transferred from the plant to residue pools. |
| [sym:soil_carbvar_write] | carbon_module | Later soil carbon variable output uses `cb_n_layers` to determine how many layer columns to write in each wide output row. |

## Lineage

`carbon_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 34 non-merge commit(s) since, most recently `821a63e` (2026-06-02, "reinstate CSU outputs and print flags"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `carbon_module.f90` are listed.

- `821a63e` (2026-06-02) — reinstate CSU outputs and print flags
- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `c2f2f97` (2026-05-22) — Intial implementation of Mather's method.
- `663b2e8` (2026-05-04) — Made several modifications to implement a cbn_diagnostics flag in carb_coefs.cbn to reduce the output of files from soil_nutcarb_write when…
- `f9662d3` (2026-04-29) — Reverted the addition of tmpf1 in carb_coefs.cbn because it is handled as an idc_till input in codes.bsn
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module-level documentation comment is present only as inline comments above `cbn_diagnostics`; there is no separate banner comment block.
- Reader coverage is representative rather than exhaustive: the context packet lists 13 reader/setup consumers, but only the rows backed by extracted evidence are described here.
- The deterministic importer list contains 40 procedures; the `used_by` table highlights the major carbon initialization, output, and process consumers first.
- `mgt_harvtuber`, `pl_grow`, `pl_leaf_gro`, `pl_mortality`, `pl_root_gro`, `pl_seed_gro`, `soil_nutcarb_write`, and `swr_subwq` have module-use evidence in the importer table, but no direct carbon-module symbol references were extracted in the provided snippets.
- lineage evidence was unavailable for this source span, so `lineage_summary` reports no resolved commits and `lineage_impacts` is empty.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
