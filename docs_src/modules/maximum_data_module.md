---
kind: module
symbol: maximum_data_module
title: maximum_data_module
status: filled
source_hash: 6e3e476f723b547a
version_label: SWAT+ 62.0.0
variables:
  db_mx: Global saved instance of `data_files_max_elements`, initialized to zeroed component
    defaults in the type definition and then updated by many file readers and setup routines.
    It carries shared maximum or loaded-record counts for climate files, landuse/management
    databases, channel/aquifer/reservoir/wetland tables, calibration updates, output-region
    counts, and related model setup arrays.
type_components:
  data_files_max_elements:
    topo: nubz
    hyd: nubz
    soil: none     |number of types of soils
    landuse: none     |number of landuse types
    mgt_ops: none     |number of records in management
    cn_lu: none     |number of records in cntable.lum
    cons_prac: none     |number of records in conservation practice table
    pothole: none     |number of potholes
    sdr: none     |number of types of susbsurface drain systems
    str_ops: none     |number of management ops
    urban: none     |number of urban land use types in urban.urb
    ovn: none     |number of overland flow n types in ovn_table.lum
    septic: none     |number of types of septic systems
    plantparm: none     |number of total plants in plants.plt
    fertparm: none     |number of total fertilizer in fertilizer.frt
    manureparm: none     |number of total manures in manure.frt
    tillparm: none     |number of total tillages in tillage.til
    pestparm: none     !number of total pesticides in pesticide.pes
    pestcom: none     !number of total pesticides communities in pesticide.com
    plantcom: none     |number of plant communities
    soiltest: none     |number of soiltest
    sno: none     |number of snow props
    field: none     |number of field props
    atmodep: none     |atmospheric deposition props
    chemapp_db: none     |chemical application (fert and pest) operations
    grazeop_db: none     |grazing operations
    harvop_db: none     |harvest only operations
    irrop_db: none     |irrigation operations
    sweepop_db: none     |sweep operations
    filtop_db: none     |filter strip data
    fireop_db: none     |fire data
    grassop_db: none     |grassed waterways data
    plparmop_db: none     |plant parms update data
    rsdmgtop_db: none     |residue management data
    bmpuserop_db: none     |user defined upland CP removal
    cond: none     |conditional data
    initop_db: none     |initial.str
    wgnsta: none     |max wgn stations included in weather-wgn.cli
    wst: none     |max weather stations include in weather-sta.cli
    pcpfiles: none     |max pcp files included in pcp.cli
    tmpfiles: none     |max tmp files included in tmp.cli
    rhfiles: none     |max relative humidity files included in hmd.cli
    slrfiles: none     |max solar radiation files included in slr.cli
    petfiles: none     |max pet files included in pet.cli
    wndfiles: none     |max wind files included in the wnd.cli
    cal_parms: none     |max number of calibration parameters in cal_parms_upd
    cal_upd: none     |max number of calibration parameter updates
    sched_up: none     |max number of scheduled updates (parameters, structures, land_use_mgt)
    cond_up: none     |max number of conditional updates (parameters, structures, land_use_mgt)
    d_tbl: none     |max number of decision tables
    dtbl_lum: none     |max number of decision tables
    dtbl_res: none     |max number of decision tables
    dtbl_flo: none     |max number of decision tables
    dtbl_scen: none     |max number of decision tables
    cs_db: none     |number of constituent database records for the current run
    pathcom: none     |number of pathogen community records
    hmetcom: none     |number of heat-metabolite community records
    saltcom: none     |number of salt community records
    ru_elem: none     |number of routing-unit element records
    lsu_elem: none     |number of landscape-unit element records
    lsu_out: none     |max number of landscape regions for output
    reg_elem: none     |number of region element records
    lsu_reg: none     |max number of landscape regions for soft cal and output by lum
    lscal_reg: none     |max number of soft data for landscape calibration (for each cal region)
    aqu_elem: none     |number of aquifer element records
    aqu_out: none     |max number of aquifer regions for output
    aqu_reg: none     |max number of aquifer regions for soft cal and output by aquifer type
    cha_out: none     |max number of channel regions for output
    cha_reg: none     |max number of channel regions for soft cal and output by channel order
    res_out: none     |max number of reservoir regions for output
    res_reg: none     |max number of reservoir regions for soft cal and output by reservoir
      type
    rec_out: none     |max number of recall regions for output
    rec_reg: none     |max number of recall regions for soft cal and output by recall type
    plcal_reg: none     |max number of regions for plant calibration
    ch_reg: none     |max number of regions for channel calibration
    lscal_prms: none     |max number of parameters for landscape hru calibration
    res_dat: none     |number of reservoir data records
    res_init: none     |number of reservoir initial-condition records
    res_hyd: none     |number of reservoir hydrology records
    res_sed: none     |number of reservoir sediment records
    res_nut: none     |number of reservoir nutrient records
    res_salt: rtb salt
    res_cs: rtb cs
    res_weir: none     |number of reservoir weir records
    wet_dat: none     |number of wetland data records
    wet_hyd: none     |number of wetland hydrology records
    ch_surf: none     |number of channel-surface linkage records
    ch_dat: none     |number of channel data records
    ch_init: none     |number of channel initial-condition records
    ch_init_cs: rtb salt/cs
    ch_hyd: none     |number of channel hydrology records
    ch_sed: none     |number of channel sediment records
    ch_nut: none     |number of channel nutrient records
    ch_temp: none     |number of channel temperature records
    shf: none     |number of shade-factor records
    w_temp: none     |number of channel water-temperature records
    path: none     |number of pathogen parameter records
    exco: none     |number of export-coefficient database records
    exco_om: none     |number of organic-matter export-coefficient records
    exco_pest: none     |number of pesticide export-coefficient records
    exco_path: none     |number of pathogen export-coefficient records
    exco_hmet: none     |number of heat-metabolite export-coefficient records
    exco_salt: none     |number of salt export-coefficient records
    dr: none     |number of delivery-ratio database records
    dr_om: none     |number of organic-matter delivery-ratio records
    trt_om: none     |number of treatment organic-matter records
    dr_pest: none     |number of pesticide delivery-ratio records
    dr_path: none     |number of pathogen delivery-ratio records
    dr_hmet: none     |number of heat-metabolite delivery-ratio records
    dr_salt: none     |number of salt delivery-ratio records
    sol_plt_ini: none     |number of soil-plant initial-condition records
    pest_ini: none     |number of pesticide initial-condition records
    path_ini: none     |number of pathogen initial-condition records
    hmet_ini: none     |number of heat-metabolite initial-condition records
    salt_ini: rtb salt
    salt_gw_ini: rtb salt
    cs_ini: rtb cs
    pestw_ini: none     |number of groundwater pesticide initial-condition records
    pathw_ini: none     |number of groundwater pathogen initial-condition records
    hmetw_ini: none     |number of groundwater heat-metabolite initial-condition records
    salt_cha_ini: rtb salt
    cs_cha_ini: rtb cs
    sep: none     |number of septic system records
    ch_lte: none     |number of channel LTE records
    om_water_init: none     |number of organic-matter water initial-condition records
    sdc_dat: none     |number of SWAT-DEG channel data records
    aqudb: none     |number of aquifer database records
    aqu2d: none     |number of aquifer-channel linkage records
    wallo_db: none     |number of water-allocation database records
    mallo_db: none     |number of manure-allocation database records
    transplant: none     |number of transplant records
    pudl_db: none     |number of puddle records
    recalldb_max: none     |number of recall database records
    object_prt: none     |number of object print records
    ctbl_res: none     |number of reservoir conditional-table records
    ch_sednut: none     |number of channel sediment-nutrient records
    sat_buff: none     |number of saturated buffer records
    canal: none     |number of canal records
    pipe: none     |number of pipe records
    wtp: none     |number of water-treatment plant records
    treat: none     |number of treatment records
    uses: none     |number of water-use records
    stor: none     |number of storage records
    om_treat: none     |number of organic-matter treatment records
    om_use: none     |number of organic-matter use records
    out_src: none     |number of outside-source records
    out_rcv: none     |number of outside-receiver records
    manure_om: none     |number of manure organic matter types in manure_om.frt
type_summaries:
  data_files_max_elements: Container for SWAT+ maximum-count bookkeeping across input databases,
    calibration tables, climate station lists, and output-region dimensions.
---

<!-- facts:header -->

`maximum_data_module` owns the global `db_mx` record of model-wide maximum counts for input databases, region catalogs, calibration tables, climate file lists, and related allocation bounds. The module is used as shared sizing and bookkeeping state during startup and later read/setup routines, so procedures that read files or expand region lists can publish their record counts for downstream allocation, looping, and validation.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only: it defines the `data_files_max_elements` type and the saved `db_mx` instance, but it contains no startup procedures. The many reader and setup routines in other modules populate `db_mx` as they scan input files or build region tables.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `db_mx` | Uses `db_mx` as shared maximum-count bookkeeping while applying actions; for example, it iterates over bounds such as `db_mx%wet_dat`, `db_mx%pudl_db`, `db_mx%sdr`, `db_mx%septic`, `db_mx%filtop_db`, `db_mx%grassop_db`, and `db_mx%bmpuserop_db` to match action file pointers to database records. |
| [sym:aqu2d_init] | `aquifer-channel linkage state` | `db_mx` | Checks `db_mx%aqu2d` and returns immediately when the aquifer-channel linkage table is not enabled; otherwise the routine uses the loaded linkage count to allocate and organize 2-D aquifer routing structures. |
| [sym:aqu2d_read] | `aqu_cha.lin` | `db_mx` | Reads the aquifer-channel linkage file, counts its records, and stores the resulting maximum in `db_mx%aqu2d` before allocating the aquifer linkage arrays. |
| [sym:aqu_read] | `aquifer.aqu` | `db_mx` | Counts aquifer database records from `aquifer.aqu` and stores the record total in `db_mx%aqudb` for later aquifer setup and looping. |
| [sym:aqu_read_elements] | `aqu_catunit.def, aqu_catunit.ele` | `db_mx` | Reads aquifer output and soft-calibration region definitions and records the resulting counts in `db_mx%aqu_out`, `db_mx%aqu_reg`, and `db_mx%aqu_elem`. |
| [sym:aqu_read_init] | `initial.aqu` | `db_mx` | Uses `db_mx%om_water_init` as the loop bound for post-read aquifer organic-matter initialization. |
| [sym:aqu_read_init_cs] | `initial.aqu_cs` | `db_mx` | Uses the groundwater constituent limits in `db_mx%pestw_ini`, `db_mx%pathw_ini`, `db_mx%salt_gw_ini`, and `db_mx%cs_ini` to match aquifer crosswalk names to the correct initial pesticide, pathogen, salt, and constituent tables. |
| [sym:basin_sw_init] | `initial basin and landscape states` | `db_mx` | Uses `db_mx%lsu_out` as the upper bound when aggregating basin, RU, and HRU starting water-balance state into output structures. |
| [sym:cal_cond_read] | `scen_dtl.upd` | `db_mx` | Reads conditional-update definitions, stores their count in `db_mx%cond_up`, and uses `db_mx%dtbl_scen` to resolve scenario decision-table names. |
| [sym:cal_parm_read] | `cal_parms.cal` | `db_mx` | Reads calibration-parameter change records and stores the loaded count in `db_mx%cal_parms`. |
| [sym:cal_parmchg_read] | `calibration.cal` | `db_mx` | Uses `db_mx%cal_parms`, `db_mx%dtbl_res`, `db_mx%plantparm`, `db_mx%ch_nut`, `db_mx%pcpfiles`, and `db_mx%tmpfiles` when resolving calibration update targets, then stores the loaded update count in `db_mx%cal_upd`. |
| [sym:calsoft_control] | `unit_4999, unit_5001, unit_5000` | `db_mx` | Uses `db_mx%lsu_reg` and `db_mx%ch_reg` as loop bounds while writing calibrated landscape and channel outputs after the soft-calibration routines complete. |

## Key Consumers

The module is used wherever SWAT+ needs a shared count of records or region bounds before allocating arrays or traversing file-backed catalogs. The largest consumer groups are climate loaders, aquifer/channel/reservoir/wetland setup, calibration readers, and output or routing routines that need the maximum loaded sizes stored in `db_mx`.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu2d_init] | maximum_data_module | The `maximum_data_module` provides `db_mx%aqu2d`, which gates whether this initialization should run at all. When `aqu2d` is not enabled, the routine returns immediately and skips all aquifer-channel and constituent hydrograph allocation. |
| [sym:aqu2d_read] | maximum_data_module | `aqu2d_read` populates `db_mx%aqu2d` with the loaded aquifer-link record count so later aquifer setup can allocate and validate the 2-D linkage structures. |
| [sym:aqu_read] | maximum_data_module | Receives the total record count at line 42 (`db_mx%aqudb = msh_aqp`), recording how many `aquifer_database` entries were loaded so that downstream routines can size their own loops over `aqudb`. |
| [sym:aqu_read_elements] | maximum_data_module | The routine stores the number of aquifer output regions, aquifer soft-calibration regions, and aquifer elements in `db_mx%aqu_out`, `db_mx%aqu_reg`, and `db_mx%aqu_elem`, which later setup code uses to size aquifer-related arrays. |
| [sym:aqu_read_init] | maximum_data_module | This module provides `db_mx%om_water_init`, the limit used in the post-read constituent initialization loop for each aquifer object. |
| [sym:aqu_read_init_cs] | maximum_data_module | These limits bound how many initial pesticide, pathogen, salt, and constituent entries are searched when matching the aquifer crosswalk names to the corresponding initial-condition tables. |
| [sym:basin_sw_init] | maximum_data_module | `db_mx%lsu_out` gives the upper bound for the RU aggregation loop, allowing the routine to walk every configured landscape output region. |
| [sym:cal_cond_read] | maximum_data_module | The routine writes `db_mx%cond_up` from the file’s declared count and uses `db_mx%dtbl_scen` as the upper bound when searching for a matching decision table name. That module supplies the shared maxima used to size and interpret the conditional-update database. |
| [sym:cal_parm_read] | maximum_data_module | `maximum_data_module` provides `db_mx%cal_parms`, the shared counter that records how many calibration-parameter entries were found. That count is needed by later calibration routines that size or iterate over the loaded change set. |
| [sym:cal_parmchg_read] | maximum_data_module | The maximum-count fields in `db_mx` cap or describe how many calibration parameters and related file-backed objects exist, and `cal_parmchg_read` uses them to size loops and choose object counts for update targets. |
| [sym:ch_read] | maximum_data_module | The maxima in `db_mx` determine how many initial, hydrology, sediment, and nutrient definitions are available for matching. `ch_read` relies on those limits when it loops over the lookup tables, and it updates `db_mx%ch_dat` with the number of channel records discovered. |
| [sym:ch_read_elements] | maximum_data_module | The routine stores the number of channel regions it finds in `db_mx%cha_reg`. That maximum-data field is the shared count other setup and allocation code uses to size channel-region structures. |
| [sym:ch_read_hyd] | maximum_data_module | `maximum_data_module` provides `db_mx%ch_hyd`, the shared maximum/record-count slot this routine fills after scanning the file so downstream code knows how many channel hydrology entries were loaded. |
| [sym:ch_read_init] | maximum_data_module | This module stores maximum record counts. `ch_read_init` writes the number of channel initialization entries into `db_mx%ch_init` so other routines can size and iterate over the loaded data. |
| [sym:ch_read_init_cs] | maximum_data_module | `maximum_data_module` matters because this routine writes the scanned record count into `db_mx%ch_init_cs`, establishing the number of channel constituent initial records available for later processing. |
| [sym:ch_read_nut] | maximum_data_module | This shared maximum-data structure receives the record count for the nutrient table. That count is part of the model's global file-size bookkeeping and is used to size or validate downstream access to `ch_nut`. |
| [sym:ch_read_orders_cal] | maximum_data_module | `db_mx%cha_reg` and `db_mx%ch_reg` are the channel-region maxima bookkeeping fields in `maximum_data_module`; this routine checks the existing channel-region count before filling HRU-linked channel data and then records the total number of channel calibration regions it read. |
| [sym:ch_read_sed] | maximum_data_module | This module holds `db_mx%ch_sed`, the shared count of channel sediment records. The routine stores the scanned record total there so later channel-model code knows how many `ch_sed` entries are valid. |
| [sym:ch_read_temp] | maximum_data_module | maximum_data_module provides db_mx%w_temp, the shared count of loaded temperature records that this routine sets after scanning the file. |
| [sym:cli_hmeas] | maximum_data_module | The module provides `db_mx%rhfiles`, which this reader sets to the number of measured humidity files discovered in `hmd.cli`. |
| [sym:cli_petmeas] | maximum_data_module | `db_mx%petfiles` records how many measured PET files were found. Other parts of the model can use that count to know how many PET datasets are available after this loader runs. |
| [sym:cli_pmeas] | maximum_data_module | db_mx%pcpfiles is the shared count of precipitation files discovered in pcp.cli. Setting it here lets the rest of the model know how many precipitation stations were loaded and how large the precipitation station list is. |
| [sym:cli_read_atmodep] | maximum_data_module | The maximum-data module stores the number of atmospheric deposition stations discovered in the file so the rest of the model can know how many deposition entries were loaded. |
| [sym:cli_smeas] | maximum_data_module | The `maximum_data_module` provides `db_mx%slrfiles`, the shared count of solar-radiation files discovered in `slr.cli`. Other code can use that count to know how many `slr` entries were loaded. |

## Lineage

`maximum_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 12 non-merge commit(s) since, most recently `561bc28` (2026-04-10, "Add manure application (manu) management operation"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `maximum_data_module.f90` are listed.

- `561bc28` (2026-04-10) — Add manure application (manu) management operation
- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `080211e` (2026-03-09) — water allocation operating properly
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `815ec79` (2026-01-07) — water allocation updates
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `maximum_data_module` has no extracted module-level documentation comment.
- Reader rows shown here are representative of the many routines that populate `db_mx`; the importer appendix preserves the deterministic full list.
- Some component meanings were inferred directly from the in-source comments in `maximum_data_module.f90`; where the comment was blank, the description stays minimal and source-backed.
- No commits were resolved for the requested source span in the provided Git Lineage Evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
