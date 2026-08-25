---
kind: module
symbol: channel_data_module
title: channel_data_module
status: filled
source_hash: 9d1994baf08ee928
version_label: SWAT+ 62.0.0
variables:
  rte_nut: Allocatable array of `routing_nut_data` records for routing/nutrient reduction
    settings; it is populated by `rte_read_nut` from `nutrients.rte` and then consumed by
    channel and routing code that needs the 2-stage ditch / channel nutrient-reduction coefficients.
  ch_dat_c: Allocatable array of `channel_data_char_input` records holding the character links
    read from `channel.cha`; `ch_read` fills it and uses the names to resolve references to
    the shared initialization, hydrology, sediment, and nutrient tables.
  ch_init: Allocatable array of `channel_init_datafiles` records holding the file-name links
    for channel initial-condition inputs; `ch_read_init` fills it from `initial.cha` and later
    setup code uses it to crosswalk channel initial data to other initialization tables.
  ch_init_cs: Allocatable array of `channel_init_datafiles_cs` records holding the channel
    constituent/salt initial-condition links; `ch_read_init_cs` fills it from `initial.cha_cs`
    and later constituent setup routines use it to resolve pathogen, salt, and constituent
    initialization tables.
  ch_dat: Allocatable array of `channel_data` records holding integer indexes into the shared
    initialization, hydrology, sediment, and nutrient tables; `ch_read` resolves the character
    links in `ch_dat_c` into these integer references for downstream routines.
  ch_hyd: Allocatable array of `channel_hyd_data` records containing channel geometry and
    hydraulic properties; `ch_read_hyd` loads it from `hydrology.cha` and later routing routines
    such as `ch_rtday` and `ch_ttcoef` use it to compute flow capacity, travel time, and routing
    coefficients.
  ch_sed: Allocatable array of `channel_sed_data` records containing channel sediment-routing
    and erosion parameters; `ch_read_sed` loads it from `sediment.cha`, normalizes missing
    values, and later channel erosion and initialization routines use it.
  ch_nut: Allocatable array of `channel_nut_data` records containing QUAL2E-style channel
    nutrient and reaction parameters; `ch_read_nut` loads it from `nutrients.cha`, fills defaults,
    applies time-step scaling, and later water-quality routines such as `ch_watqual4` and
    calibration code consume it.
  w_temp: Allocatable array of `water_temperature_data` records containing channel temperature
    lag and heat-exchange controls; `ch_read_temp` loads it from `temperature.cha`, and `ch_temp`
    uses `w_temp(0)` as the active configuration for water-temperature calculations.
type_components:
  routing_nut_data:
    name: Record name for the routing-nutrient parameter set; the default value is `Drainage_Ditch`.
    len_inc: Segment length used for the reduction calculation, in meters.
    no3_slp: Slope of the denitrification relation versus inflow nitrate, in (mgN/m2/h)/ppm.
    no3_int: Intercept of the denitrification rate equation, in mgN/m2/h.
    no3_slp_ob: Observed-bank slope of the denitrification relation versus inflow nitrate,
      in (mgN/m2/h)/ppm.
    no3_int_ob: Observed-bank intercept of the denitrification rate equation, in mgN/m2/h.
    no3_slp_ub: Upper-bank slope of the denitrification relation versus inflow nitrate, in
      (mgN/m2/h)/ppm.
    no3_int_ub: Upper-bank intercept of the denitrification rate equation, in mgN/m2/h.
    turb_slp: Slope of turbidity reduction versus inflow turbidity, in delta ppm per ppm.
    turb_int: Intercept of the turbidity reduction equation, in ppm.
    tss_slp: Slope of total suspended solids reduction versus inflow turbidity, in delta ppm
      per ppm.
    tss_int: Intercept of the total suspended solids reduction equation, in ppm.
    tp_slp: Slope of total phosphorus reduction versus turbidity reduction, in delta ppm per
      ppm.
    tp_int: Intercept of the total phosphorus reduction equation, in ppm.
    srp_slp: Slope of soluble reactive phosphorus reduction versus total phosphorus reduction,
      in delta ppm per ppm.
    srp_int: Intercept of the soluble reactive phosphorus reduction equation, in ppm.
    turb_tss_slp: Slope relating turbidity and total suspended solids, typically 0.2 to 0.4.
    no3_min_conc: Minimum nitrate concentration, in ppm.
    tp_min_conc: Minimum total phosphorus concentration, in ppm.
    tss_min_conc: Minimum total suspended solids concentration, in ppm.
    srp_min_conc: Minimum soluble reactive phosphorus concentration, in ppm.
  channel_data_char_input:
    name: Channel record name used as the key for matching and identification.
    init: Name of the linked initial-condition record from `initial_cha`.
    hyd: Name of the linked hydrology record from `hydrology.res`.
    sed: Name of the linked sediment record from `sediment.res`.
    nut: Name of the linked nutrient record from `nutrient.res`.
  channel_init_datafiles:
    name: Channel initial-condition set name.
    org_min: Name of the linked organic-mineral initial input file.
    pest: Name of the linked pesticide initial input file.
    path: Name of the linked pathogen initial input file.
    hmet: Name of the linked heavy-metals initial input file.
    salt: Name of the linked salt initial input file.
  channel_init_datafiles_cs:
    name: Channel constituent initial-condition set name.
    pest: Name of the linked pesticide initial input file.
    path: Name of the linked pathogen initial input file.
    hmet: Name of the linked heavy-metals initial input file.
    salt: Name of the linked salt initial input file.
    cs: Name of the linked constituent initial input file.
  channel_data:
    name: Channel record name.
    init: Integer index into the initial-condition table, referencing `initial.res`.
    hyd: Integer index into the hydrology table, referencing `hydrology.res`.
    sed: Integer index into the sediment table, referencing `sediment.res`.
    nut: Integer index into the nutrient table, referencing `nutrient.res`.
  channel_hyd_data:
    name: Record name for the hydrology set; comments note that some fields are conditional
      on reservoir versus HRU impounding use.
    w: Average width of the main channel, in meters.
    d: Average depth of the main channel, in meters.
    s: Average slope of the main channel, in m/m.
    l: Main channel length in the subbasin, in km.
    n: Manning's n value for the main channel, dimensionless.
    k: Effective hydraulic conductivity of the main-channel alluvium, in mm/hr.
    wdr: Channel width-to-depth ratio, dimensionless.
    alpha_bnk: Bank storage recession alpha factor, in days.
    side: Change in horizontal distance per unit vertical distance for the side slope.
  channel_sed_data:
    name: Record name for the sediment set.
    eqn: 'Sediment routing method selector: 0 original SWAT, 1 Bagnold, 2 Kodatie, 3 Molinas-WU,
      4 Yang.'
    cov1: Channel erodibility factor, dimensionless, normally 0.0 to 1.0.
    cov2: Channel cover factor, dimensionless, normally 0.0 to 1.0.
    bnk_bd: Bulk density of channel bank sediment, in g/cc.
    bed_bd: Bulk density of channel bed sediment, in g/cc.
    bnk_kd: Bank sediment erodibility by jet test.
    bed_kd: Bed sediment erodibility by jet test.
    bnk_d50: Median particle size diameter for the channel bank material.
    bed_d50: Median particle size diameter for the channel bed material.
    tc_bnk: Critical shear stress of the channel bank, in N/m2.
    tc_bed: Critical shear stress of the channel bed, in N/m2.
    erod: Monthly erosion-resistance factors; zero means non-erosive and one means no resistance
      to erosion.
  channel_nut_data:
    name: Record name for the nutrient set.
    onco: Channel organic nitrogen concentration, in ppm.
    opco: Channel organic phosphorus concentration, in ppm.
    rs1: Local algal settling rate in the reach at 20 deg C.
    rs2: Benthic source rate for dissolved phosphorus at 20 deg C.
    rs3: Benthic source rate for ammonia nitrogen at 20 deg C.
    rs4: Rate coefficient for organic nitrogen settling at 20 deg C.
    rs5: Rate coefficient for organic phosphorus settling at 20 deg C.
    rs6: Rate coefficient for settling of an arbitrary non-conservative constituent.
    rs7: Benthic source rate for an arbitrary non-conservative constituent.
    rk1: CBOD deoxygenation rate coefficient at 20 deg C.
    rk2: Reaeration rate consistent with Fickian diffusion at 20 deg C.
    rk3: Rate of CBOD loss due to settling at 20 deg C.
    rk4: Sediment oxygen demand rate at 20 deg C.
    rk5: Coliform die-off rate in the reach.
    rk6: Decay rate for an arbitrary non-conservative constituent.
    bc1: Biological oxidation rate of NH3 to NO2 at 20 deg C.
    bc2: Biological oxidation rate of NO2 to NO3 at 20 deg C.
    bc3: Hydrolysis rate of organic N to ammonia at 20 deg C.
    bc4: Decay rate of organic P to dissolved P at 20 deg C.
    lao: QUAL2E light averaging option; SWAT uses option 2.
    igropt: QUAL2E option for computing local specific algal growth rate; SWAT uses option
      2.
    ai0: Chlorophyll-a to algal biomass ratio.
    ai1: Fraction of algal biomass that is nitrogen.
    ai2: Fraction of algal biomass that is phosphorus.
    ai3: Oxygen production per unit algal photosynthesis.
    ai4: Oxygen uptake per unit algae respiration.
    ai5: Oxygen uptake per unit NH3 oxidation.
    ai6: Oxygen uptake per unit NO2 oxidation.
    mumax: Maximum specific algal growth rate at 20 deg C.
    rhoq: Algal respiration rate.
    tfact: Fraction of solar radiation treated as photosynthetically active in the temperature
      heat balance.
    k_l: Half-saturation coefficient for light.
    k_n: Michaelis-Menten half-saturation constant for nitrogen.
    k_p: Michaelis-Menten half-saturation constant for phosphorus.
    lambda0: Non-algal portion of the light extinction coefficient.
    lambda1: Linear algal self-shading coefficient.
    lambda2: Nonlinear algal self-shading coefficient.
    p_n: Algal preference factor for ammonia.
  channel_temperature_data:
    name: Record name for the temperature set.
    sno_mlt: Coefficient influencing snowmelt temperature contributions.
    gw: Coefficient influencing groundwater temperature contributions.
    sur_lat: Coefficient influencing surface and lateral flow temperature contributions.
    bulk_co: Bulk coefficient of heat transfer, in 1/hour.
    air_lag: Average air temperature lag, in days.
  water_temperature_data:
    name: Record name for the water-temperature set.
    sno_mlt: Coefficient influencing snowmelt temperature contributions.
    gw: Coefficient influencing groundwater temperature contributions.
    sur_lat: Coefficient influencing surface and lateral flow temperature contributions.
    sno_lag: Average air temperature lag to snowmelt, in days.
    gw_lag: Average air temperature lag to groundwater flow, in days.
    surf_lag: Average air temperature lag to surface runoff, in days.
    lat_lag: Average air temperature lag to lateral flow, in days.
    lat_lag_coef: Lateral air lag coefficient.
    surf_lag_coef: Surface air lag coefficient, also used for snow.
    gw_lag_coef: Groundwater air lag coefficient.
    hex_coef1: Calibration coefficient for dew point.
    hex_coef2: Calibration coefficient for channel geometry.
    sf_on: Shade factor file activation flag; 1 uses file input, 0 uses calibration-file value.
    ssff: Shade factor default, with nominal value 0.5 and range 0 to 1.
type_summaries:
  routing_nut_data: One routing-nutrient reduction record for the 2-stage ditch / channel
    nutrient routing settings.
  channel_data_char_input: One channel record of character links to the shared channel setup
    tables.
  channel_init_datafiles: One channel initial-condition file-link record for the standard
    channel initialization set.
  channel_init_datafiles_cs: One channel constituent initial-condition file-link record for
    the salt/constituent workflow.
  channel_data: One channel record holding integer cross-references to the shared channel
    setup tables.
  channel_hyd_data: One channel hydrology record containing geometry and hydraulic coefficients
    for a reach.
  channel_sed_data: One channel sediment record defining routing method, erodibility, cover,
    and critical-shear parameters.
  channel_nut_data: One channel nutrient / QUAL2E parameter record for in-stream water quality.
  channel_temperature_data: One channel temperature control record for channel heat exchange
    calculations.
  water_temperature_data: One water-temperature control record used by `ch_temp` as the active
    temperature configuration.
---

<!-- facts:header -->

`channel_data_module` owns the shared channel configuration tables, lookup arrays, and default parameter records used by channel initialization, routing, water-quality, sediment, and temperature routines. It is populated by the various `ch_read*` setup readers and then consumed by channel-processing procedures that resolve channel names to integer indexes or read the stored hydraulic, sediment, nutrient, and temperature parameters.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container for shared channel state and default parameter records. It does not contain executable procedures; its arrays are populated by reader/setup routines such as `ch_read`, `ch_read_hyd`, `ch_read_init`, `ch_read_init_cs`, `ch_read_nut`, `ch_read_sed`, `ch_read_temp`, and `rte_read_nut`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:cal_parm_select] | `calibration request data already held in model state; no file read from this module` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Applies calibration changes to channel-related state, including selected channel nutrient parameters in `ch_nut`. |
| [sym:ch_read] | `channel.cha` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Reads channel definitions, stores the character links in `ch_dat_c`, and resolves them into integer table indexes in `ch_dat`. |
| [sym:ch_read_hyd] | `hydrology.cha` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Loads channel hydrology records into `ch_hyd`, then normalizes hydraulic parameters such as bank-storage alpha, slope, Manning's n, length, width-to-depth ratio, and side slope. |
| [sym:ch_read_init] | `initial.cha` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Reads the channel initial-condition file and fills `ch_init` with the loaded initialization file links. |
| [sym:ch_read_init_cs] | `initial.cha_cs` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Reads the channel constituent initial-condition file and fills `ch_init_cs` with the loaded salt and constituent links. |
| [sym:ch_read_nut] | `nutrients.cha` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Loads channel nutrient / QUAL2E parameters into `ch_nut`, fills missing fields with defaults, and scales selected rates to the model time step. |
| [sym:ch_read_sed] | `sediment.cha` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Loads channel sediment-routing parameters into `ch_sed`, assigns defaults for missing values, and prepares erosion-related fields for later channel processing. |
| [sym:ch_read_temp] | `temperature.cha` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Loads water-temperature control records into `w_temp`, making the active channel temperature settings available to `ch_temp`. |
| [sym:cs_cha_read] | `cs_channel.ini, cs_streamobs, cs_streamobs_output` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Reads channel constituent initialization and optional stream-observation setup that depend on the shared channel initialization tables from this module. |
| [sym:om_water_init] | `om_water.ini` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Loads organic-matter-in-water initialization records using the shared channel initialization context. |
| [sym:path_cha_res_read] | `path_water.ini` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Loads channel/pathogen initial-condition records as part of the shared channel constituent setup. |
| [sym:pest_cha_res_read] | `pest_water.ini` | `rte_nut, ch_dat_c, ch_init, ch_init_cs, ch_dat, ch_hyd, ch_sed, ch_nut, w_temp` | Loads pesticide initial-condition records as part of the shared channel constituent setup. |

## Key Consumers

The module is imported by channel setup routines that read and crosswalk input tables, by routing routines that need channel geometry, by water-quality routines that need nutrient parameters, and by calibration code that adjusts channel nutrient state.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_parm_select] | channel_data_module | Acts as the shared storage for channel nutrient calibration targets; this routine updates `ch_nut` entries for parameters such as `mumax`, `rs1`-`rs7`, `rk1`-`rk6`, and `bc1`-`bc4`. |
| [sym:ch_initial] | channel_data_module | Provides the sediment lookup tables used to map a channel's sediment class to bank/bed particle sizes and to derive critical shear stress defaults when those values are missing. |
| [sym:ch_read] | channel_data_module | Supplies the arrays that hold the channel record links and the resolved integer indexes for initial, hydrology, sediment, and nutrient setup tables. |
| [sym:ch_read_hyd] | channel_data_module | Supplies the shared `ch_hyd` storage that receives parsed hydrology records and stores normalized geometry and resistance parameters for later routing. |
| [sym:ch_read_init] | channel_data_module | Supplies the shared `ch_init` storage that receives channel initial-condition file links for later initialization crosswalks. |
| [sym:ch_read_init_cs] | channel_data_module | Supplies the shared `ch_init_cs` storage that receives channel constituent initial-condition links for later salt and constituent setup. |
| [sym:ch_read_nut] | channel_data_module | Supplies the shared `ch_nut` table that receives nutrient parameter records and is filled with defaults and time-step-scaled values before water-quality calculations. |
| [sym:ch_read_sed] | channel_data_module | Supplies the shared `ch_sed` table that receives sediment routing records and is normalized for later erosion and routing logic. |
| [sym:ch_read_temp] | channel_data_module | Supplies the shared `w_temp` table that receives water-temperature control records for the channel heat-balance routines. |
| [sym:rte_read_nut] | channel_data_module | Supplies the shared routing-nutrient parameter array `rte_nut` used by channel and routing nutrient-reduction logic. |
| [sym:sd_channel_read] | channel_data_module | Provides the channel initial-condition, constituent, and nutrient lookup tables that `sd_channel_read` crosswalks into its channel-DEG setup. |
| [sym:ch_rtday] | channel_data_module | Provides the hydraulic geometry in `ch_hyd` that `ch_rtday` uses to compute bankfull capacity, routing time, seepage loss, and floodplain overflow. |
| [sym:ch_rthr] | channel_data_module | Provides the channel setup and rating-curve-related hydraulic state used by subdaily reach routing. |
| [sym:ch_rtmusk] | channel_data_module | Provides the channel and routing data structures referenced by Muskingum and variable-storage channel routing. |
| [sym:ch_rtpest] | channel_data_module | Provides the channel depth and geometry inputs needed to scale pesticide reaction, settling, resuspension, diffusion, and burial calculations. |
| [sym:ch_temp] | channel_data_module | Provides the active `w_temp(0)` temperature controls used to compute channel water temperature from climate and flow mixing. |
| [sym:ch_ttcoef] | channel_data_module | Provides the channel hydraulic geometry used to derive bankfull width, area, velocity, celerity, and travel-time coefficients. |
| [sym:ch_watqual4] | channel_data_module | Provides the channel nutrient and reaction parameter table `ch_nut` used to compute algal growth, oxygen balance, settling, and benthic exchange. |
| [sym:cs_cha_read] | channel_data_module | Provides the channel initialization context that channel constituent input is matched against. |
| [sym:om_water_init] | channel_data_module | Provides the shared initialization context used to store organic-matter-in-water records loaded from `om_water.ini`. |
| [sym:path_cha_res_read] | channel_data_module | Provides the shared channel constituent initialization context for the path-water reader, although no direct symbol use was visible in the extracted span. |
| [sym:pest_cha_res_read] | channel_data_module | Provides the shared channel constituent initialization context for the pesticide initial-condition reader, although no direct symbol use was visible in the extracted span. |
| [sym:salt_cha_read] | channel_data_module | Provides the shared channel initialization context that the salt initial-condition reader populates for later channel salt accounting. |
| [sym:sd_channel_control3] | channel_data_module | Provides the channel state tables used by channel-DEG control logic for routing, water quality, temperature, and constituent accounting. |

## Lineage

`channel_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `channel_data_module.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `889136d` (2025-02-03) — Fix typos
- `54a9d44` (2024-08-12) — NP_flow.f90 - Subroutine NP_FLOW REMOVED
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `channel_data_module` has no extracted module-level documentation comment.
- `ch_temp` uses `w_temp(0)` as the active configuration, and the original `channel_temperature_data` type is retained in the module even though the associated allocatable array was replaced by `w_temp` because of a naming conflict.
- The parser-supplied importer list is preserved as a complete appendix; some consumer effects rely on completed procedure overlays, while a few imported routines had no direct symbol references visible in their extracted spans.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
