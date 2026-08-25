---
kind: module
symbol: channel_module
title: channel_module
status: filled
source_hash: 7df9ffd80dee3170
version_label: SWAT+ 62.0.0
variables:
  jhyd: units         |description
  jsed: units         |description
  jnut: units         |description
  rttime: hr            |reach travel time
  ben_area: m2            |benthic area (bottom sediments)
  rchdep: m             |depth of flow on day
  rtevp: m^3 H2O       |evaporation from reach on day
  rttlc: m^3 H2O       |transmission losses from reach on day
  pet_ch: mm           |potential evaporation from reach on day
  hrtwtr: m^3 H2O       |water leaving reach
  hharea: m^2           |cross-sectional area of flow
  hdepth: m             |depth of flow
  rhy: m H2O         |main channel hydraulic radius
  hsdti: m^3/s         |flow rate in reach for hour
  hhtime: hr            |flow travel time for hour
  hrttlc: m^3 H2O       |transmission losses from reach during time step
  hrtevp: m^3 H2O       |evaporation from reach during time step
  hhstor: m^3 H2O       |water stored in reach at end of hour
  hrchwtr: m^3 H2O       |water stored at beginning of day
  halgae: mg alg/L      |algal biomass concentration in reach
  hbactlp: '# cfu/100mL   |less persistent bacteria in reach/outflow during hour'
  hbactp: '# cfu/100mL   |persistent bacteria in reach/outflow during hour'
  hbod: mg O2/L       |carbonaceous biochemical oxygen demand inreach at end of hour
  hchla: mg chl-a/L    |chlorophyll-a concentration in reach at end of hour
  hdisox: mg O2/L       |dissolved oxygen concentration in reach at end of hour
  hnh4: mg N/L        |ammonia concentration in reach at end of hour
  hno2: mg N/L        |nitrite concentration in reach at end of hour
  hno3: mg N/L        |nitrate concentration in reach at end of hour
  horgn: mg N/L        |organic nitrogen concentration in reach at end of hour
  horgp: mg P/L        |organic phosphorus concentration in reach at end of hour
  hsedst: metric tons   |amount of sediment stored in reach at the end of hour
  hsedyld: metric tons   |sediment transported out of reach during hour
  hsolp: mg P/L        |dissolved phosphorus concentration in reach at end of hour
  hsolpst: mg pst/m^3    |soluble pesticide concentration in outflow on day
  hsorpst: mg pst/m^3    |sorbed pesticide concentration in outflow on day
  rchsep: real array placeholder for channel separation state; initialized to zero/blank allocation
    and not annotated in source comments, so downstream ownership is uncertain from the extracted
    source alone.
  peakr: peak discharge accumulator for the current reach/day; initialized to 0 and used by
    routing and morphology output routines.
  rcharea: cross-sectional flow area accumulator for the current reach/day; initialized to
    0 and recomputed by routing.
  sdti: daily reach discharge accumulator; initialized to 0 and used by routing calculations
    and outputs.
  bnkrte: bank erosion rate accumulator; initialized to 0 and used in channel sediment routing/output.
  degrte: channel degradation rate accumulator; initialized to 0 and used in channel sediment
    routing/output.
  sedrch: metric tons       |sediment transported out of reach on day
  rch_san: daily sand mass routed out of the reach; initialized to 0 and used in sediment
    bookkeeping.
  rch_sil: daily silt mass routed out of the reach; initialized to 0 and used in sediment
    bookkeeping.
  rch_cla: daily clay mass routed out of the reach; initialized to 0 and used in sediment
    bookkeeping.
  rch_sag: daily small-aggregate mass routed out of the reach; initialized to 0 and used in
    sediment bookkeeping.
  rtwtr_d: m^3 H2O           |water leaving reach during day
  rt_delt: calculation time step in days
  rch_lag: daily large-aggregate mass routed out of the reach; initialized to 0 and used in
    sediment bookkeeping.
  rch_gra: daily gravel mass routed out of the reach; initialized to 0 and used in sediment
    bookkeeping.
  rtwtr: m^3 H2O           |water leaving reach on day
  wtrin: m^3               |water entering reach during day
  sed_ch: integer flag/index used in channel sediment calculations; initialized to 0 and later
    read by routing/sediment logic.
  ch: allocated array of per-reach `channel` records holding channel geometry, sediments,
    water quality, and stored mass state used by reach routing and initializers.
  rch_d: daily regional channel output record of type `regional_output_channel` used to hold
    basin/channel summary values at the daily interval.
  rch_m: monthly regional channel output record of type `regional_output_channel` used to
    accumulate basin/channel summaries.
  rch_y: yearly regional channel output record of type `regional_output_channel` used to accumulate
    basin/channel summaries.
  rch_a: average-annual regional channel output record of type `regional_output_channel` used
    for end-of-simulation summaries.
  ch_d: daily channel output record of type `ch_output` used by channel and basin output writers.
  ch_m: monthly channel output record of type `ch_output` used to accumulate daily channel
    outputs.
  ch_y: yearly channel output record of type `ch_output` used to accumulate monthly channel
    outputs.
  ch_a: average-annual channel output record of type `ch_output` used to accumulate yearly
    channel outputs before final averaging.
  bch_d: basin-wide daily channel output record of type `ch_output` used by basin_channel_output.
  bch_m: basin-wide monthly channel output accumulator of type `ch_output`.
  bch_y: basin-wide yearly channel output accumulator of type `ch_output`.
  bch_a: basin-wide average-annual channel output accumulator of type `ch_output`.
  chz: zeroed `ch_output` record used to reset channel and basin output accumulators.
  ch_hdr: channel output header record used when writing channel-day, channel-month, channel-year,
    and channel-average output files.
  ch_hdr_units: channel output units/header row record paired with `ch_hdr` for file output.
type_components:
  channel:
    algae: mg alg/L      |algal biomass concentration in reach
    ammonian: mg N/L        |ammonia concentration in reach
    bankst: m^3 H2O       |bank storage
    li: km            |initial length of main channel
    orgn: '|organic nitrogen contribution from channel erosion'
    orgp: '|organic phosphorus contribution from channel erosion'
    si: (m/n)          |slope of main channel
    wi: (m)            |width of main channel at top of bank
    di: (m)            |depth of main channel from top of bank to bottom
    chlora: mg chl-a/L    |chlorophyll-a concentration in reach
    pst_conc: mg/(m**3)     |initial pesticide concentration in reach
    dep_chan: m             |average daily water depth in channel
    disolvp: mg P/L        |dissolved P concentration in reach
    drift: kg            |amount of pesticide drifting onto main channel in subbasin
    flwin: m^3 H2O       |flow into reach on previous day
    flwout: m^3 H2O       |flow out of reach on previous day
    nitraten: mg N/L        |nitrate concentration in reach
    nitriten: mg N/L        |nitrite concentration in reach
    organicn: mg N/L        |organic nitrogen concentration in reach
    organicp: mg P/L        |organic phosphorus concentration in reach
    rch_bactlp: '# cfu/100ml   |less persistent bacteria stored in reach'
    rch_bactp: '# cfu/100ml   |persistent bacteria stored in reach'
    rch_cbod: mg O2/L       |carbonaceous biochemical oxygen demand in reach
    rch_dox: mg O2/L       |dissolved oxygen concentration in reach
    rchstor: m^3 H2O       |water stored in reach
    sedst: metric tons   |amount of sediment stored in reach
    vel_chan: m/s           |average flow velocity in channel
    bed_san: sand fraction in the channel bed; initialized to 0 in `channel_module` and assigned
      by `ch_initial`
    bed_sil: silt fraction in the channel bed; initialized to 0 in `channel_module` and assigned
      by `ch_initial`
    bed_cla: clay fraction in the channel bed; initialized to 0 in `channel_module` and assigned
      by `ch_initial`
    bed_gra: gravel fraction in the channel bed; initialized to 0 in `channel_module` and
      assigned by `ch_initial`
    bnk_san: sand fraction in the channel bank; initialized to 0 in `channel_module` and assigned
      by `ch_initial`
    bnk_sil: silt fraction in the channel bank; initialized to 0 in `channel_module` and assigned
      by `ch_initial`
    bnk_cla: clay fraction in the channel bank; initialized to 0 in `channel_module` and assigned
      by `ch_initial`
    bnk_gra: gravel fraction in the channel bank; initialized to 0 in `channel_module` and
      assigned by `ch_initial`
    depfp: floodplain deposition mass/state carried in the channel record; initialized to
      0 and used by routing/sediment routines
    depprfp: floodplain phosphorus deposition mass/state carried in the channel record; initialized
      to 0 and used by routing/sediment routines
    depsilfp: floodplain silt deposition mass/state carried in the channel record; initialized
      to 0 and used by routing/sediment routines
    depclafp: floodplain clay deposition mass/state carried in the channel record; initialized
      to 0 and used by routing/sediment routines
    depch: channel deposition mass/state carried in the channel record; initialized to 0 and
      used by routing/sediment routines
    depprch: channel phosphorus deposition mass/state carried in the channel record; initialized
      to 0 and used by routing/sediment routines
    depsanch: channel sand deposition mass/state carried in the channel record; initialized
      to 0 and used by routing/sediment routines
    depsilch: channel silt deposition mass/state carried in the channel record; initialized
      to 0 and used by routing/sediment routines
    depclach: channel clay deposition mass/state carried in the channel record; initialized
      to 0 and used by routing/sediment routines
    depsagch: channel small-aggregate deposition mass/state carried in the channel record;
      initialized to 0 and used by routing/sediment routines
    deplagch: channel large-aggregate deposition mass/state carried in the channel record;
      initialized to 0 and used by routing/sediment routines
    depgrach: channel gravel deposition mass/state carried in the channel record; initialized
      to 0 and used by routing/sediment routines
    sanst: stored sand mass in the channel; initialized to 0 and used by routing/sediment
      routines
    silst: stored silt mass in the channel; initialized to 0 and used by routing/sediment
      routines
    clast: stored clay mass in the channel; initialized to 0 and used by routing/sediment
      routines
    sagst: stored small aggregate mass in the channel; initialized to 0 and used by routing/sediment
      routines
    lagst: stored large aggregate mass in the channel; initialized to 0 and used by routing/sediment
      routines
    grast: stored gravel mass in the channel; initialized to 0 and used by routing/sediment
      routines
    wattemp: water temperature in the channel; initialized to 0 and used by water-quality/pathogen
      routines
    bactp: persistent bacteria mass/state in the channel; initialized to 0 and used by pathogen
      routing
    chfloodvol: channel flood volume accumulator; initialized to 0 and used by daily routing
    bactlp: less persistent bacteria mass/state in the channel; initialized to 0 and used
      by pathogen routing
  ch_output:
    flo_in: (ha-m)     |streamflow into reach during time step
    flo_out: (ha-m)     |streamflow out of reach during time step
    evap: (m^3/s)    |daily rate of water loss from reach by evaporation
    tloss: (m^3/s)    |rate of water loss from reach by transmission through the streambed
    sed_in: (tons)     |sediment transported with water into reach
    sed_out: (tons)     |sediment transported with water out of reach
    sed_conc: (mg/L)     |concentration of sediment in reach
    orgn_in: (kg N)     |organic nitrogen transported with water into reach
    orgn_out: (kg N)     |organic nitrogen transported with water out of reach
    orgp_in: (kg P)     |organic phosphorus transported with water into reach
    orgp_out: (kg P)     |organic phosphorus transported with water out of reach
    no3_in: (kg N)     |nitrate transported with water into reach
    no3_out: (kg N)     |nitrate transported with water out of reach
    nh4_in: (kg)       |ammonium transported with water into reach
    nh4_out: (kg)       |ammonium transported with water out of reach
    no2_in: (kg)       |nitrite transported with water into reach
    no2_out: (kg)       |nitrite transported with water out of reach
    solp_in: (kg P)     |soluble pesticide transported with water into reach
    solp_out: (kg P)     |soluble pesticide transported with water out of reach
    chla_in: (kg)       |amount of chlorophyll a transported into reach
    chla_out: (kg)       |amount of chlorophyll a transported out of reach
    cbod_in: (kg)       |carbonaceous biochemical oxygen demand of material transported into
      reach
    cbod_out: (kg)       |carbonaceous biochemical oxygen demand of material transported out
      of reach
    dis_in: (kg)       |amount of dissolved oxygen transported into reach
    dis_out: (kg)       |amount of dissolved oxygen transported out of reach
    solpst_in: (mg pst)   |soluble pesticide transported with water into reach
    solpst_out: (mg pst)   |soluble pesticide transported with water out of reach
    sorbpst_in: (mg pst)   |pesticide sorbed to sediment transported with water into reach
    sorbpst_out: (mg pst)   |pesticide sorbed to sediment transported with water out of reach
    react: (mg pst)   |loss of pesticide from water from reaction
    volat: (mg)       |loss of pesticide from water by volatilization
    setlpst: (mg pst)   |transfer of pesticide from water to river bed sediment by settling
    resuspst: (mg)       |transfer of pesticide from river bed sediment to water by resuspension
    difus: mg         |transfer of pesticide from water to river bed sediment by diffusion
    reactb: (mg)       |loss of pesticide from river bed sediment by reaction
    bury: (mg)       |loss of pesticide from river bed sediment by burial
    sedpest: mg         |pesticide in river bed sediment
    bacp: '# cfu/100mL  |number of persistent bacteria transported out of reach'
    baclp: '# cfu/100mL  |number of less persistent bacteria transported out of reach'
    met1: 'kg         |conservative metal #1 transported out of reach'
    met2: 'kg         |conservative metal #2 transported out of reach'
    met3: 'kg         |conservative metal #3 transported out of reach'
    sand_in: tons       |sand in
    sand_out: tons       |sand out
    silt_in: tons       |silt_in
    silt_out: tons       |silt_out
    clay_in: tons       |clay_in
    clay_out: tons       |clay_out
    smag_in: tons       |small aggregates transported into reach
    smag_out: tons       |small aggregates transported out of reach
    lag_in: tons       |large aggregates transported into reachlg ag in
    lag_out: tons       |large aggregates transported out of reach
    grvl_in: tons       |gravel in
    grvl_out: tons       |gravel out
    bnk_ero: tons       |bank erosion
    ch_deg: tons       |channel degradation
    ch_dep: tons       |channel deposition
    fp_dep: tons       |flood deposition
    tot_ssed: mg/L       |total suspended sediments
  regional_output_channel:
    ord: channel output payload stored as a `ch_output` record for a regional summary interval
  ch_header:
    day: day-of-year label
    mo: month label
    day_mo: day-month label
    yrc: year label
    isd: unit label for output files
    id: GIS identifier label
    name: object name label
    flo_in: column header for inflow values
    flo_out: column header for outflow values
    evap: column header for evaporation values
    tloss: column header for transmission-loss values
    sed_in: column header for sediment inflow values
    sed_out: column header for sediment outflow values
    sed_conc: column header for sediment concentration values
    orgn_in: column header for organic nitrogen inflow values
    orgn_out: column header for organic nitrogen outflow values
    orgp_in: column header for organic phosphorus inflow values
    orgp_out: column header for organic phosphorus outflow values
    no3_in: column header for nitrate inflow values
    no3_out: column header for nitrate outflow values
    nh4_in: column header for ammonium inflow values
    nh4_out: column header for ammonium outflow values
    no2_in: column header for nitrite inflow values
    no2_out: column header for nitrite outflow values
    solp_in: column header for soluble phosphorus inflow values
    solp_out: column header for soluble phosphorus outflow values
    chla_in: column header for chlorophyll-a inflow values
    chla_out: column header for chlorophyll-a outflow values
    cbod_in: column header for CBOD inflow values
    cbod_out: column header for CBOD outflow values
    dis_in: column header for dissolved oxygen inflow values
    dis_out: column header for dissolved oxygen outflow values
    solpst_in: column header for soluble pesticide inflow values
    solpst_out: column header for soluble pesticide outflow values
    sorbpst_in: column header for sorbed pesticide inflow values
    sorbpst_out: column header for sorbed pesticide outflow values
    react: column header for pesticide reaction losses
    volat: column header for volatilization losses
    setlpst: column header for settling transfers
    resuspst: column header for resuspension transfers
    difus: column header for diffusion transfers
    reactb: column header for benthic pesticide reaction losses
    bury: column header for benthic burial losses
    sedpest: column header for benthic pesticide mass
    bacp: column header for persistent bacteria outflow
    baclp: column header for less persistent bacteria outflow
    met1: column header for conservative metal 1
    met2: column header for conservative metal 2
    met3: column header for conservative metal 3
    sand_in: column header for sand inflow
    sand_out: column header for sand outflow
    silt_in: column header for silt inflow
    silt_out: column header for silt outflow
    clay_in: column header for clay inflow
    clay_out: column header for clay outflow
    smag_in: column header for small aggregate inflow
    smag_out: column header for small aggregate outflow
    lag_in: column header for large aggregate inflow
    lag_out: column header for large aggregate outflow
    grvl_in: column header for gravel inflow
    grvl_out: column header for gravel outflow
    bnk_ero: column header for bank erosion
    ch_deg: column header for channel degradation
    ch_dep: column header for channel deposition
    fp_dep: column header for flood deposition
    tot_ssed: column header for total suspended sediments
  ch_header_units:
    day: blank or spacer field
    mo: blank or spacer field
    day_mo: blank or spacer field
    yrc: blank or spacer field
    isd: blank or spacer field
    id: blank or spacer field
    name: blank or spacer field
    flo_in: (ha-m)
    flo_out: (ha-m)
    evap: (ha-m)
    tloss: (ha-m)
    sed_in: (tons)
    sed_out: (tons)
    sed_conc: (mg/L)
    orgn_in: (kg N)
    orgn_out: (kg N)
    orgp_in: (kg P)
    orgp_out: (kg P)
    no3_in: (kg N)
    no3_out: (kg N)
    nh4_in: (kg)
    nh4_out: (kg)
    no2_in: (kg)
    no2_out: (kg)
    solp_in: (kg P)
    solp_out: (kg P)
    chla_in: (kg)
    chla_out: (kg)
    cbod_in: (kg)
    cbod_out: (kg)
    dis_in: (kg)
    dis_out: (kg)
    solpst_in: (mg pst)
    solpst_out: (mg pst)
    sorbpst_in: (mg pst)
    sorbpst_out: (mg pst)
    react: (mg pst)
    volat: (mg)
    setlpst: (mg pst)
    resuspst: (mg)
    difus: (mg pst)
    reactb: pst/sed (mg)
    bury: pst bury (mg)
    sedpest: pst in rivbed sed mg
    bacp: persistent bact out
    baclp: lpersistent bact out
    met1: 'cmetal #1'
    met2: 'cmetal #2'
    met3: 'cmetal #3'
    sand_in: sand in
    sand_out: sand out
    silt_in: silt_in
    silt_out: silt_out
    clay_in: clay_in
    clay_out: clay_out
    smag_in: sm ag in
    smag_out: sm ag out
    lag_in: lg ag in
    lag_out: lg ag out
    grvl_in: gravel in
    grvl_out: gravel out
    bnk_ero: bank erosion
    ch_deg: channel degradation
    ch_dep: channel deposition
    fp_dep: flood deposition
    tot_ssed: total suspended sediments
type_summaries:
  channel: Per-reach channel state used by routing, sediment, water-quality, and initial-condition
    routines.
  ch_output: Per-reach or basin-aggregated channel routing output record holding water, sediment,
    nutrient, pesticide, bacteria, and erosion terms for a reporting interval.
  regional_output_channel: Regional channel output record used for basin/channel summaries
    at daily, monthly, yearly, and average-annual intervals.
  ch_header: Character labels for the channel output file header row.
  ch_header_units: Character unit row paired with `ch_hdr` for channel output files.
---

<!-- facts:header -->

Owns the shared channel state, channel output accumulators, and channel header/type definitions used by routing, calibration, water-quality, sediment, pathogen, and output-writing routines. It also provides the channel arithmetic helpers `ch_add`, `ch_div`, and `ch_mult` for combining and scaling channel output records.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is primarily a shared declaration container: it defines channel state, output records, and header templates, while initialization is performed by importing routines such as `ch_initial`, `ch_rchinit`, `ch_rtday`, `ch_rthr`, `ch_rtmusk`, `ch_rtpath`, `ch_rtpest`, `ch_watqual4`, `header_channel`, and `header_write` rather than by any contained startup procedure in this module itself.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:basin_channel_output] | `unit_2110, unit_2114, unit_2111, unit_2115, unit_2112, unit_2116, unit_2113, unit_2117` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Uses `ch_d`, `bch_d`, `bch_m`, `bch_y`, `bch_a`, and `chz` to aggregate per-channel daily output into basin totals, reset the daily channel records, and write basin channel output records at daily, monthly, yearly, and average-annual intervals. |
| [sym:cal_parm_select] | `procedure arguments and calibration state in `cal_parm_select.f90`` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Imports the module so channel-related calibration branches can update channel state when a matching parameter is selected; the extracted procedure body did not resolve specific channel members from this module in the available snippet. |
| [sym:channel_output] | `unit_2480, unit_2484, unit_2481, unit_2485, unit_2482, unit_2486, unit_2483, unit_2487` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Uses `ch_m`, `ch_d`, `ch_y`, `ch_a`, and `chz` to roll a channel's daily output into monthly, yearly, and average-annual records and to write the selected output files. |
| [sym:command] | `unit_out_hyd_sep` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Uses `peakr` when assembling channel morphology/output records in the command workflow; this module provides the shared channel-state storage that those command-time outputs update. |
| [sym:header_channel] | `unit_2480, unit_9000, unit_2484, unit_2481, unit_2485, unit_2482, unit_2486, unit_2483, unit_2487` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Writes `ch_hdr` and `ch_hdr_units` into the channel output files so the channel-day, channel-month, channel-year, and channel-average records have the expected column names and unit rows. |
| [sym:header_write] | `unit_6000, unit_9000, hru-out.cal, hru-new.cal, hydrology-cal.hyd, unit_2090, unit_2094, unit_2091, unit_2095, unit_2092, unit_2096, unit_2093, unit_2097, unit_2100, unit_2104, unit_2101, unit_2105, unit_2102, unit_2106, unit_2103, unit_2107, unit_4600, unit_4604, unit_4601, unit_4605, unit_4602, unit_4606, unit_4603, unit_4607, unit_2110, unit_2114, unit_2111, unit_2115, unit_2112, unit_2116, unit_2113, unit_2117, unit_4900, unit_4904, unit_4901, unit_4905, unit_4902, unit_4906, unit_4903, unit_4907, unit_2120, unit_2124, unit_2121, unit_2125, unit_2122, unit_2126, unit_2123, unit_2127, unit_2128, unit_2132, unit_2129, unit_2133, unit_2130, unit_2134, unit_2131, unit_2135, unit_4500, unit_4504, unit_4501, unit_4505, unit_4502, unit_4506, unit_4503, unit_4507, unit_2600, unit_2604, unit_2601, unit_2605, unit_2602, unit_2606, unit_2603, unit_2607` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Writes the channel header and units records from `ch_hdr` and `ch_hdr_units` into basin-channel output files during model setup, so downstream record writing uses a consistent layout. |
| [sym:hydro_init] | `procedure arguments and hydrology setup state in `hydro_init.f90`` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Imports the module so hydrology initialization can share the channel-state namespace; the extracted snippet did not resolve specific module members from this module. |
| [sym:output_landscape_init] | `unit_2000, unit_9000, unit_2004, unit_2001, unit_2005, unit_2002, unit_2006, unit_2003, unit_2007, unit_2020, unit_2024, unit_3333, unit_3334, unit_3335, unit_3336, unit_3337, unit_3338, unit_3339, unit_3340, unit_2021, unit_2025, unit_2022, unit_2026, unit_2023, unit_2027, unit_4520, unit_4524, unit_4521, unit_4525, unit_4522, unit_4526, unit_4523, unit_4527, unit_4550, unit_4554, unit_4551, unit_4555, unit_4552, unit_4556, unit_4553, unit_4557, unit_2030, unit_2034, unit_2031, unit_2035, unit_2032, unit_2036, unit_2033, unit_2037, unit_2040, unit_2044, unit_2041, unit_2045, unit_2042, unit_2046, unit_2043, unit_2047, unit_2300, unit_2304, unit_2301, unit_2305, unit_2302, unit_2306, unit_2303, unit_2307, unit_2440, unit_2444, unit_2441, unit_2445, unit_2442, unit_2446, unit_2443, unit_2447, unit_2460, unit_2464, unit_2461, unit_2465, unit_2462, unit_2466, unit_2463, unit_2467, unit_2140, unit_2144, unit_2141, unit_2145, unit_2142, unit_2146, unit_2143, unit_2147, unit_2150, unit_2154, unit_2151, unit_2155, unit_2152, unit_2156, unit_2153, unit_2157, unit_2160, unit_2164, unit_2161, unit_2165, unit_2162, unit_2166, unit_2163, unit_2167, unit_2170, unit_2174, unit_2171, unit_2175, unit_2172, unit_2176, unit_2173, unit_2177, unit_2050, unit_2054, unit_2051, unit_2055, unit_2052, unit_2056, unit_2053, unit_2057, unit_2060, unit_2064, unit_2061, unit_2065, unit_2062, unit_2066, unit_2063, unit_2067, unit_2070, unit_2074, unit_2071, unit_2075, unit_2072, unit_2076, unit_2073, unit_2077, unit_2080, unit_2084, unit_2081, unit_2085, unit_2082, unit_2086, unit_2083, unit_2087, unit_4010, unit_4011, unit_4008, unit_4009, unit_4750, unit_4754, unit_4751, unit_4755, unit_4752, unit_4756, unit_4753, unit_4757, unit_4758, unit_4762, unit_4759, unit_4763, unit_4760, unit_4764, unit_4761, unit_4765, unit_4766, unit_4770, unit_4767, unit_4771, unit_4768, unit_4772, unit_4769, unit_4773` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Imports the module so landscape output setup can share channel-state definitions when opening the many output units used by the model. |
| [sym:pathogen_init] | `procedure arguments and pathogen setup state in `pathogen_init.f90`` | `jhyd, jsed, jnut, rttime, ben_area, rchdep` | Imports the module so pathogen initialization shares the global channel-state namespace; no direct channel member from this module was resolved in the extracted snippet. |

## Key Consumers

`channel_module` is used most heavily by the channel routing and output stack: initialization routines seed `ch` and the reach-level scalars, routing and water-quality routines read and update that state, and the output writers consume `ch_*`, `bch_*`, `ch_hdr`, and `ch_hdr_units` to produce basin and reach reports.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_channel_output] | channel_module | Collects `ch_d` across all channel objects, stores the basin-wide daily sum in `bch_d`, rolls that daily total into `bch_m`, `bch_y`, and `bch_a`, and clears `ch_d` and period accumulators with `chz` after each report boundary. |
| [sym:channel_output] | channel_module | Uses `ch_d`, `ch_m`, `ch_y`, `ch_a`, and `chz` to accumulate a routed channel's daily output into monthly, yearly, and average-annual records and write the selected daily/monthly/yearly/average output files. |
| [sym:header_channel] | channel_module | Writes the channel header labels and units from `ch_hdr` and `ch_hdr_units` into the channel output files when channel reporting is enabled. |
| [sym:header_write] | channel_module | Writes `ch_hdr` and `ch_hdr_units` into the basin channel output setup files so the channel output streams have the correct column names and unit rows. |
| [sym:cal_parm_select] | channel_module | Provides the shared channel-state namespace for calibration branches that may adjust channel-related parameters and reach state during parameter selection. |
| [sym:pathogen_init] | channel_module | Imports the shared channel-state namespace while setting up pathogen arrays, even though the extracted snippet does not reference a specific channel member. |
| [sym:ch_initial] | channel_module | Supplies the per-reach `ch` array that this initializer populates with bank and bed texture fractions for later erosion and transport calculations. |
| [sym:ch_rchinit] | channel_module | Provides the shared reach-state variables that are reset and seeded for the active reach, including `peakr`, `rcharea`, `rchdep`, `rtevp`, `rttime`, `rttlc`, `rtwtr`, `sdti`, `sedrch`, and `ch(jrch)%vel_chan`. |
| [sym:ch_rtday] | channel_module | Provides the reach geometry and routing scalars that the daily routing step uses to compute bankfull overflow, depth, travel time, evaporation, transmission loss, and routed outflow. |
| [sym:ch_rthr] | channel_module | Supplies `jhyd`, which is loaded from the active reach's hydrology index so the subdaily routing step uses the correct hydraulic data set. |
| [sym:ch_rtmusk] | channel_module | Supplies `jhyd` and the shared channel routing state used by the Muskingum/variable-storage channel routing workflow. |
| [sym:ch_rtpath] | channel_module | Provides the reach-state variables `rtwtr`, `rchdep`, `rttime`, and `ch(jrch)%bactp` that control whether pathogen routing runs and how much decay and dilution occur. |
| [sym:ch_rtpest] | channel_module | Provides `wtrin` and `rttime`, which gate in-stream pesticide processing and scale the day-length of pesticide reactions, settling, resuspension, diffusion, burial, and solubility checks. |
| [sym:ch_watqual4] | channel_module | Provides the shared reach timestep, nutrient calibration index, benthic area, and reach depth used to scale reaction rates and perform the channel water-quality update. |
| [sym:sd_channel_sediment3] | channel_module | Stores reach velocity and routing time computed by the SWAT-DEG sediment routing step so later temperature or transport routines can reuse those hydraulic values. |
| [sym:ch_ttcoef] | channel_module | Acts as the host module for the channel routing state that this coefficient routine belongs to, even though the extracted snippet did not resolve a direct module-specific state reference. |
| [sym:channel_surf_link] | channel_module | Provides the shared object-connectivity namespace used when channel-surface links assign flooded-object back-references and resolved object numbers. |
| [sym:wetland_control] | channel_module | Provides the connectivity/state namespace tied to channel-linked wetland routing and bookkeeping. |
| [sym:command] | channel_module | Provides the shared channel output and morphology state that the command workflow updates when it assembles channel and basin output records. |
| [sym:hydro_init] | channel_module | Provides the shared channel-state namespace for hydrology initialization, allowing startup routines to populate channel-related model state. |
| [sym:output_landscape_init] | channel_module | Provides the channel-state definitions needed when the landscape output setup opens the various output units that include channel-related records. |
| [sym:sd_channel_control3] | channel_module | Provides the channel state, nutrient index, benthic area, and routing-time variables that the SWAT-DEG channel controller updates before calling sediment, routing, pathogen, pesticide, and water-quality subroutines. |
| [sym:calsoft_hyd] | channel_module | Provides the shared channel-state namespace used by soft calibration hydrology setup. |

## Lineage

`channel_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `23142ed` (2025-10-29, "Water allocation now has explicit structured output objects and headers, with pe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `channel_module.f90` are listed.

- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `9b7f630` (2025-09-23) — Remvoved whitespace in carbon_module and channel_module that was causing compiler warnings. Added function/module utils.f90 that implements…
- `10e5ddc` (2025-08-27) — 08272025 updates
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `channel_module` has no extracted module-level documentation comment.
- Some reader ownership and importer effects are inferred from import references and completed procedure overlays; where the extracted snippet did not resolve a specific channel member, the note says so rather than guessing.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
