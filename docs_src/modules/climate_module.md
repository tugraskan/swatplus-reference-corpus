---
kind: module
symbol: climate_module
title: climate_module
status: filled
source_hash: 01eee0ac8794dad4
version_label: SWAT+ 62.0.0
variables:
  ppet_ndays: 30            |number of days for precip/pet sum; used by weather-generator
    linked-list and climate indexing logic
  ppet_mce: 0             |current element in precip/pet linked list; advances weather-generator
    rolling precipitation/PET storage
  frad: allocatable real matrix |fraction of solar radiation occurring during each hour in
    day in HRU; filled by `cli_clgen` and used by subdaily radiation distribution
  wgncur: allocatable real matrix |current weather-generator residuals/derived state for each
    gage; updated by `cli_weatgn` and read by generator-dependent climate routines
  wgnold: allocatable real matrix |previous weather-generator residuals/state for each gage;
    paired with `wgncur` for recursive climate generation
  elevp: allocatable integer vector |elevation of precipitation gage station; used when lapse
    rates are computed from measured precipitation stations
  elevt: allocatable integer vector |elevation of temperature gage station; used when lapse
    rates are computed from measured temperature stations
  idg: allocatable integer vector |array location of random number seed; selects the stream
    used by climate random draws
  rndseed: allocatable integer matrix |random number generator seeds for weather/climate processes;
    used by generator routines and `gcycl`
  rnd2: allocatable real vector |random number between 0.0 and 1.0; stream used by climate
    generation
  rnd3: allocatable real vector |random number between 0.0 and 1.0; stream used by precipitation
    generation
  rnd8: allocatable real vector |random number between 0.0 and 1.0; stream used by weather-generator
    residual updates
  rnd9: allocatable real vector |random number between 0.0 and 1.0; stream used by weather-generator
    residual updates
  rndseed_cond: 748932582     |random number seed for dtbl conditional; shared conditional-random
    seed used by decision-table logic
  co2y: allocatable real vector |annual CO2 concentration series read by `co2_read` and consumed
    by ET and plant-growth routines
  wgn: allocatable array of `weather_generator_db` |monthly weather-generator database loaded
    from `weather-wgn.cli` and used by weather generation, dormancy, and plant initialization
  wgn_orig: allocatable array of `weather_generator_db` |copy of original weather-generator
    records preserved alongside `wgn` for later reference
  wgn_pms: allocatable array of `wgn_parms` |derived weather-generator parameters computed
    from `wgn` and consumed by climate, plant, and routing routines
  wnd_dir: allocatable array of `wind_direction_db` |monthly wind-direction probability tables
    used by wind generation
  w: weather_daily |current daily weather state snapshot for the active station; read and
    written by many climate and hydrologic routines
  wst: allocatable array of `weather_station` |shared weather-station database linking gages,
    generator codes, lapse adjustments, and daily weather state
  pcp: allocatable array of `climate_measured_data` |measured precipitation station database
    loaded from `pcp.cli` and used for observed precipitation input
  tmp: allocatable array of `climate_measured_data` |measured temperature station database
    loaded from `tmp.cli` and used for observed temperature input
  slr: allocatable array of `climate_measured_data` |measured solar-radiation station database
    loaded from `slr.cli` and used for observed solar input
  hmd: allocatable array of `climate_measured_data` |measured humidity station database loaded
    from `hmd.cli` and used for observed humidity input
  wnd: allocatable array of `climate_measured_data` |measured wind station database loaded
    from `wnd.cli` and used for observed wind input
  petm: allocatable array of `climate_measured_data` |measured PET station database loaded
    from `pet.cli` and used for observed PET input
  atmodep: allocatable array of `atmospheric_deposition` |atmospheric deposition station database
    for rainfall and dry deposition of ammonia/nitrate
  atmodep_cont: save `atmospheric_deposition_control` |persistent control record for atmospheric
    deposition timestep, start position, and station counts
  salt_atmo: n             |flag indicating whether salt atmospheric deposition input was
    loaded
  cs_atmo: n             |flag indicating whether constituent atmospheric deposition input
    was loaded
  atmodep_salt: allocatable array of `object_deposition_cs` |per-station/per-salt atmospheric
    deposition storage
  atmodep_cs: allocatable array of `object_deposition_cs` |per-station/per-constituent atmospheric
    deposition storage
  rdapp_salt: allocatable array of `object_road_salt` |applied road salt storage by object
    and salt ion
  wst_n: allocatable character vector |weather-station names loaded from `weather-sta.cli`
  wgn_n: allocatable character vector |weather-generator station names loaded from `weather-wgn.cli`
  pcp_n: allocatable character vector |precipitation station names loaded from `pcp.cli`
  tmp_n: allocatable character vector |temperature station names loaded from `tmp.cli`
  slr_n: allocatable character vector |solar-radiation station names loaded from `slr.cli`
  hmd_n: allocatable character vector |humidity station names loaded from `hmd.cli`
  wnd_n: allocatable character vector |wind station names loaded from `wnd.cli`
  atmo_n: allocatable character vector |atmospheric deposition station names loaded from `atmodep.cli`
  petm_n: allocatable character vector |PET station names loaded from `pet.cli`
type_components:
  weather_generator_db:
    lat: degrees      |latitude of weather station used to compile data
    long: degrees      |longitude of weather station
    elev: '|elevation of weather station used to compile weather generator data'
    rain_yrs: none         |number of years of recorded maximum 0.5h rainfall used to calculate
      values for rainhhmx(:)
    tmpmx: deg C        |avg monthly maximum air temperature
    tmpmn: deg C        |avg monthly minimum air temperature
    tmpstdmx: deg C        |standard deviation for avg monthly maximum air temperature
    tmpstdmn: deg C        |standard deviation for avg monthly minimum air temperature
    pcpmm: mm           |amount of precipitation in month
    pcpstd: mm/day       |standard deviation for the average daily
    pcpskw: none         |skew coefficient for the average daily precipitation
    pr_wd: none         |probability of wet day after dry day in month
    pr_ww: none         |probability of wet day after wet day in month
    pcpd: days         |average number of days of precipitation in the month
    rainhmx: mm           |maximum 0.5 hour rainfall in month
    solarav: MJ/m^2/day   |average daily solar radiation for the month
    dewpt: deg C        |average dew point temperature for the month
    windav: m/s          |average wind speed for the month
  wgn_parms:
    pr_wdays: none          |proportion of wet days in a month
    pcpmean: mm/day        |average amount of precipitation falling in one day for the month
    daylmn: '|minimum day length'
    daylth: '|day length threshold to trigger dormancy'
    latsin: '|sine of latitude'
    latcos: '|cosine of latitude'
    phutot: '|total base zero heat units for year'
    pcpdays: '|days of precip in year'
    tmp_an: '|average annual air temperature'
    pcp_an: '|average annual precipitation'
    ppet_an: '|average annual precip/pet'
    precip_sum: '|30 day sum of PET (mm)'
    pet_sum: '|30 day sum of PRECIP (mm)'
    p_pet_rto: '|30 day sum of PRECIP/PET ratio'
    pcf: '|normalization factor for precipitation'
    amp_r: '|alpha factor for rain(mo max 0.5h rain)'
    pet: '|average monthly PET (mm)'
    mne_ppet: none          |next element in precip-pet linked list
    precip_mce: mm            |precip on current day of 30 day list
    pet_mce: mm            |pet on current day of 30 day list
    ireg: '|annual precip category-1 <= 508 mm; 2 > 508 and <= 1016 mm; 3 > 1016 mm/yr'
    idewpt: '|0=dewpoint; 1=rel humididty input'
  wind_direction_db:
    name: station or generator label for the direction table
    dir: 1-16         |avg monthly wind direstion
  weather_daily:
    precip: daily precipitation depth at the station
    precip_next: mm           |precip generated for next day
    tmax: daily maximum air temperature at the station
    tmin: daily minimum air temperature at the station
    tave: daily mean air temperature at the station
    solrad: daily solar radiation at the station
    solradmx: daily clear-sky maximum solar radiation
    rhum: daily relative humidity at the station
    dewpt: daily dew-point temperature at the station
    windsp: daily wind speed at the station
    pet: daily potential evapotranspiration at the station
    wndir: 'real :: pet'
    phubase0: deg C        |cumulative base 0 heat units
    ppet: mm/mm        |climatic moisture index - cumulative p/pet
    daylength: hr           |day length
    precip_half_hr: frac         |fraction of total rainfall on day that occurs
    precip_prior_day: '|during 0.5h highest intensity rainfall

      |"dry" or "wet"'
    ts: mm           |subdaily precip - current day
    ts_next: mm           |subdaily precip - next day
  weather_codes_station:
    wgn: weather generator station number
    pgage: gage number for rainfall (sim if generating)
    tgage: gage number for temperature (sim if generating)
    sgage: gage number for solar radiation (sim if generating)
    hgage: gage number for relative humidity (sim if generating)
    wgage: gage number for windspeed (sim if generating)
    petgage: number of pet gage files used in sim
    atmodep: atmospheric depostion data file locator
  weather_codes_station_char:
    wgn: 'character (len=50) ::  wst = ""      !!  weather station name

      weather generator name'
    pgage: gage name for rainfall
    tgage: gage name for temperature
    sgage: gage name for solar radiation
    hgage: gage name for relative humidity
    wgage: gage name for windspeed
    petgage: name of pet gage
    atmodep: atmospheric depostion data file locator
  weather_station:
    name: station name used in climate and routing linkage
    lat: degrees    |latitude
    wco_c: character code bundle for linked weather sources
    wco: integer code bundle for linked weather sources
    weat: daily weather state for the station
    precip_aa: mm         |average annual precipitation
    pet_aa: mm         |average annual potential ET
    pcp_ts: 1/day      |precipitation time steps per day (0 or 1 = daily)
    rfinc: deg C      |monthly precipitation adjustment
    tmpinc: deg C      |monthly temperature adjustment
    radinc: MJ/m^2     |monthly solar radiation adjustment
    huminc: none       |monthly humidity adjustment
    tlag: deg C      |daily average temperature for channel temp lag
    airlag_temp: deg C      |average temperature w_temp%airlag_d days ago
    tlag_mne: '|next element (day) for the air temp linked list'
  climate_change_variables:
    name: label for the climate-change record
    ref_yr: none       |reference year to begin incremental adjustments
    co2inc: ppm        |annual CO2 increment
    rfinc: deg C      |monthly precipitation annual increment
    tmpinc: deg C      |monthly temperature annual increment
    radinc: MJ/m^2     |monthly solar radiation annual increment
    huminc: none       |monthly humidity annual increment
    co2scen: ppm        |annual CO2 scenario adjustment
    rfscen: deg C      |monthly precipitation scenario adjustment
    tmpscen: deg C      |monthly temperature scenario adjustment
    radscen: MJ/m^2     |monthly solar radiation scenario adjustment
    humscen: none       |monthly humidity scenario adjustment
  climate_measured_data:
    filename: source filename for the measured climate record
    lat: latitude of raingage
    long: longitude of raingage
    elev: elevation of raingage
    nbyr: number of years of daily rainfall
    tstep: timestep of precipitation
    days_gen: number of missing days - generated
    yrs_start: number of years of simulation before record starts
    start_day: daily precip start julian day
    start_yr: daily precip start year
    end_day: daily precip end julian day
    end_yr: daily precip end year
    mean_mon: same as variable unit        |mean monthly measured value
    max_mon: same as variable unit        |maximum monthly measured value
    min_mon: same as variable unit        |minimum monthly measured value
    ts: daily or time-step series for the primary measured variable
    ts2: secondary daily or time-step series, such as max/min temperature pair storage
    tss: third-dimensional measured time-series storage for subdaily or multi-series data
  atmospheric_deposition:
    nh4_rf: ave annual ammonia in rainfall - mg/l
    no3_rf: ave annual nitrate in rainfall - mg/l
    nh4_dry: ave annual ammonia dry deposition - kg/ha/yr
    no3_dry: ave annual nitrate dry deposition - kg/ha/yr
    name: station or record name for the deposition source
    nh4_rfmo: monthly ammonia-in-rainfall series
    no3_rfmo: monthly nitrate-in-rainfall series
    nh4_drymo: monthly ammonia dry-deposition series
    no3_drymo: monthly nitrate dry-deposition series
    nh4_rfyr: yearly ammonia-in-rainfall series
    no3_rfyr: yearly nitrate-in-rainfall series
    nh4_dryyr: yearly ammonia dry-deposition series
    no3_dryyr: yearly nitrate dry-deposition series
  atmospheric_deposition_control:
    num_sta: number of atmospheric deposition stations loaded
    timestep: deposition timestep code
    ts: current deposition time-step index
    mo_init: initial month for aligned monthly deposition data
    yr_init: initial year for aligned yearly deposition data
    num: number of monthly or yearly values to read
    first: one-time initialization/alignment flag
  atmospheric_deposition_cs:
    rf: concentration in rainfall - mg/l
    dry: dry deposition - kg/ha/yr
    rfmo: monthly rainfall-concentration series
    drymo: monthly dry-deposition series
    rfyr: yearly rainfall-concentration series
    dryyr: yearly dry-deposition series
  object_deposition_cs:
    salt: per-object salt atmospheric deposition records
    cs: per-object constituent atmospheric deposition records
  road_salt:
    road: ave annual salt ion loading via road salt application (kg/ha)
    roadday: daily salt ion loading via road salt application (kg/ha)
    roadmo: monthly salt ion loading via road salt application (kg/ha)
    roadyr: yearly salt ion loading via road salt application (kg/ha)
  object_road_salt:
    salt: salt-ion road-salt records for the object
type_summaries:
  weather_generator_db: One monthly weather-generator station record holding observed climate
    statistics used to generate daily weather.
  wgn_parms: Derived monthly weather-generator parameters cached for each station and used
    to generate daily climate and dormancy inputs.
  wind_direction_db: Monthly wind-direction probability table keyed by station name.
  weather_daily: Daily weather snapshot for one weather station, including generated or measured
    meteorology and derived climate indices.
  weather_codes_station: Integer code mapping from one weather station to linked gage and
    generator sources.
  weather_codes_station_char: Character-name counterpart to the weather-station source-code
    mapping.
  weather_station: A spatial weather station entry linking a station name, source codes, daily
    weather, and lapse-adjustment state.
  climate_change_variables: Annual or scenario climate-change increments applied to weather
    series.
  climate_measured_data: Measured climate-file container holding metadata, record bounds,
    and daily or subdaily time series.
  atmospheric_deposition: Atmospheric deposition inputs for rainfall and dry deposition of
    ammonia and nitrate by station.
  atmospheric_deposition_control: Persistent control record for atmospheric deposition time
    stepping and station alignment.
  atmospheric_deposition_cs: Constituent-specific atmospheric deposition values for rainfall
    and dry loading.
  object_deposition_cs: Per-object container for constituent or salt atmospheric deposition
    series.
  road_salt: Applied road-salt loading for a salt ion across annual, monthly, daily, and yearly
    storage.
  object_road_salt: Per-object road-salt container holding one or more salt-ion records.
---

<!-- facts:header -->

`climate_module` is the shared climate state container for SWAT+: it owns the weather-generator databases, measured climate series, weather-station records, atmospheric deposition records, road-salt storage, random-number streams, and related name lists used by climate setup, daily climate generation, routing, plant growth, erosion, water quality, and output routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only. It does not contain startup procedures; its allocatable arrays, control records, and random-state buffers are populated by the climate readers and generators such as `cli_wgnread`, `cli_staread`, `cli_pmeas`, `cli_tmeas`, `cli_smeas`, `cli_hmeas`, `cli_wmeas`, `cli_petmeas`, `cli_read_atmodep`, `cli_read_atmodep_cs`, `cli_read_atmodep_salt`, `co2_read`, and `climate_control`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `ppet_ndays, ppet_mce, frad, wgncur, wgnold, elevp` | Uses climate state indirectly during management actions that depend on weather-driven conditions and calibration state. |
| [sym:channel_output] | `unit_2480, unit_2484, unit_2481, unit_2485, unit_2482, unit_2486, unit_2483, unit_2487` | `ppet_ndays, ppet_mce, frad, wgncur, wgnold, elevp` | Imports the climate module but the extracted channel-output lines do not reference its symbols. |
| [sym:cli_hmeas] | `hmd.cli, hmd(i)%filename` | `hmd, hmd_n` | Reads the measured humidity control file and fills the shared humidity database and name list. |
| [sym:cli_petmeas] | `pet.cli, petm(i)%filename` | `petm, petm_n` | Reads the measured PET control file and fills the shared PET database and name list. |
| [sym:cli_pmeas] | `pcp.cli, pcp(i)%filename` | `pcp, pcp_n` | Reads the measured precipitation control file and fills the shared precipitation database and name list. |
| [sym:cli_read_atmodep] | `atmodep.cli` | `atmodep, atmo_n, atmodep_cont` | Reads atmospheric deposition control data and loads station deposition records into shared climate state. |
| [sym:cli_read_atmodep_cs] | `cs_atmo.cli` | `atmodep_cs, cs_atmo` | Reads constituent atmospheric deposition data and marks constituent deposition as active. |
| [sym:cli_read_atmodep_salt] | `salt_atmo.cli` | `atmodep_salt, salt_atmo` | Reads salt atmospheric deposition data and marks salt deposition as active. |
| [sym:cli_smeas] | `slr.cli, slr(i)%filename` | `slr, slr_n` | Reads the measured solar-radiation control file and fills the shared solar database and name list. |
| [sym:cli_staread] | `weather-sta.cli` | `wst, wst_n, wgn_n, pcp_n, tmp_n, slr_n, hmd_n, wnd_n, petm_n, atmo_n` | Reads the weather-station list and builds the station linkage tables and station-name arrays. |
| [sym:cli_tmeas] | `tmp.cli, tmp(i)%filename` | `tmp, tmp_n` | Reads the measured temperature control file and fills the shared temperature database and name list. |
| [sym:cli_wgnread] | `weather-wgn.cli` | `wgn, wgn_n, wgn_orig, wgn_pms, wgncur, wgnold, rnd2, rnd3, rnd8, rnd9, rndseed, idg` | Reads weather-generator station data, initializes derived weather-generator state, and seeds the random streams. |

## Key Consumers

The module is a shared climate and weather database used by setup readers, daily climate generators, routing, plant growth, wetland/reservoir/channel logic, erosion, atmospheric deposition, and output routines. Many consumers only need one or two symbols, but the module acts as the common home for all station-based climate state.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:hru_lum_init] | `wst` | After the HRU-to-object link is found, the routine reads the linked weather-station record to obtain the weather-generator code that determines the HRU's climatic context. |
| [sym:plant_init] | `wst`, `wgn`, `wgn_pms` | Uses station latitude and monthly weather-generator climate to derive heat units, planting timing, dormancy thresholds, and initial canopy conditions for plant communities. |
| [sym:cli_hmeas] | climate_module | Allocates and populates the shared humidity-file database and station-name list from `hmd.cli`. |
| [sym:cli_petmeas] | climate_module | Allocates and populates the shared PET-file database and station-name list from `pet.cli`. |
| [sym:cli_pmeas] | climate_module | Allocates and populates the shared precipitation-file database and station-name list from `pcp.cli`. |
| [sym:cli_read_atmodep] | climate_module | Loads the shared atmospheric deposition control record, station arrays, and station-name list from the atmospheric deposition input file. |
| [sym:cli_read_atmodep_cs] | climate_module | Loads constituent atmospheric deposition storage and sets the constituent deposition flag for later deposition and uptake routines. |
| [sym:cli_read_atmodep_salt] | climate_module | Loads salt atmospheric deposition storage and sets the salt deposition flag for later salt-routing routines. |
| [sym:cli_smeas] | climate_module | Allocates and populates the shared solar-radiation-file database and station-name list from `slr.cli`. |
| [sym:cli_staread] | climate_module | Builds the weather-station database, station-name array, and source-code links used by climate initialization and daily weather control. |
| [sym:cli_tmeas] | climate_module | Allocates and populates the shared temperature-file database and station-name list from `tmp.cli`. |
| [sym:cli_wgnread] | climate_module | Loads the weather-generator database, derived parameters, names, and random streams that all later climate generation depends on. |
| [sym:cli_wmeas] | climate_module | Allocates and populates the shared wind-file database and station-name list from `wnd.cli`. |
| [sym:co2_read] | climate_module | Allocates and fills the annual CO2 forcing series used by later climate and plant-growth routines. |
| [sym:gwflow_pond] | climate_module | Provides the station-linked precipitation and PET values used to compute pond rainfall and evaporation. |
| [sym:hru_lte_control] | climate_module | Supplies the daily weather inputs used for runoff, snow, PET, and growth calculations. |
| [sym:hru_lte_read] | climate_module | Provides weather-generator monthly temperatures used to estimate heat units for HRU LTE plants. |
| [sym:hyd_read_connect] | climate_module | Provides weather-station linkage state that influences groundwater-flow routing branches during hydraulic setup. |
| [sym:salt_roadsalt_read] | climate_module | Loads the road-salt deposition controls and storage used by salt routing and atmospheric deposition processing. |
| [sym:swift_output] | climate_module | Supplies weather-station climate totals that are averaged and written to the SWIFT precipitation output. |
| [sym:channel_output] | climate_module | Imported but no climate symbols are referenced in the extracted channel-output lines, so the dependency is not used in the visible routine body. |
| [sym:cs_uptake_read] | climate_module | Imported by the constituent uptake reader, but no resolved climate symbols appear in the extracted body. |
| [sym:salt_uptake_read] | climate_module | Imported by the salt uptake reader, but no resolved climate symbols appear in the extracted body. |
| [sym:aqu_1d_control] | `wst` | Provides daily PET from the linked weather station so the aquifer controller can compute revap and update groundwater storage. |

## Lineage

`climate_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `889136d` (2025-02-03, "Fix typos"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `climate_module.f90` are listed.

- `889136d` (2025-02-03) — Fix typos
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment was extracted from `climate_module.f90`.
- The module is a declaration container; all state is populated by external reader/generator routines rather than contained procedures.
- The used-by table is a ranked documentation subset; the full importer appendix is preserved in `all_importers`.
- Lineage evidence for this span reported no resolved commits, so no change history is available here.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
