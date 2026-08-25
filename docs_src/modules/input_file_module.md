---
kind: module
symbol: input_file_module
title: input_file_module
status: filled
source_hash: df093952c99b31e0
version_label: SWAT+ 62.0.0
variables:
  in_sim: Public instance of `input_sim`; holds core simulation file names such as `time.sim`,
    `print.prt`, `object.prt`, `object.cnt`, and `constituents.cs`. It is declared with default
    string values in the module and is consumed by time, print-code, object-output, and constituent-database
    readers.
  in_basin: Public instance of `input_basin`; holds basin-level file names such as `codes.bsn`,
    `parameters.bsn`, and `carbon.bsn`. Readers use it to locate basin control, basin parameter,
    and carbon input files.
  in_cli: Public instance of `input_cli`; holds climate control filenames such as `weather-sta.cli`,
    `weather-wgn.cli`, `pet.cli`, `pcp.cli`, `tmp.cli`, `slr.cli`, `hmd.cli`, `wnd.cli`, and
    `atmodep.cli`. Climate readers use these names to locate measured and generator climate
    inputs.
  in_con: Public instance of `input_con`; holds connectivity filenames such as `hru.con`,
    `hru-lte.con`, `rout_unit.con`, `gwflow.con`, `aquifer.con`, `aquifer2d.con`, `channel.con`,
    `reservoir.con`, `recall.con`, `exco.con`, `delratio.con`, `outlet.con`, and `chandeg.con`.
    Hydrologic and connectivity readers use these paths to load or switch connection files.
  in_cha: Public instance of `input_cha`; holds channel input filenames such as `initial.cha`,
    `channel.cha`, `hydrology.cha`, `sediment.cha`, `nutrients.cha`, `channel-lte.cha`, `hyd-sed-lte.cha`,
    and `temperature.cha`. Channel readers use these names to load the channel databases and
    initialization files.
  in_res: Public instance of `input_res`; holds reservoir and wetland filenames such as `initial.res`,
    `reservoir.res`, `hydrology.res`, `sediment.res`, `nutrients.res`, `weir.res`, `wetland.wet`,
    and `hydrology.wet`. Reservoir and wetland readers use these names for setup and initialization.
  in_ru: Public instance of `input_ru`; holds routing-unit filenames `rout_unit.def`, `rout_unit.ele`,
    `rout_unit.rtu`, and `rout_unit.dr`. Routing-unit readers use these to load definitions,
    elements, and delivery-ratio data.
  in_hru: Public instance of `input_hru`; holds HRU filenames `hru-data.hru` and `hru-lte.hru`.
    HRU readers use these to load standard and LTE HRU databases.
  in_exco: Public instance of `input_exco`; holds exco recall-constant filenames `exco.exc`,
    `exco_om.exc`, `exco_pest.exc`, `exco_path.exc`, `exco_hmet.exc`, and `exco_salt.exc`.
    Exco readers use these to load recall-constant source databases.
  in_rec: Public instance of `input_rec`; holds the recall database file `recall.rec`. Recall
    readers use it to load daily, monthly, and annual recall definitions.
  in_delr: Public instance of `input_delr`; holds delivery-ratio filenames `delratio.del`,
    `dr_om.del`, `dr_pest.del`, `dr_path.del`, `dr_hmet.del`, and `dr_salt.del`. Delivery-ratio
    readers use these to load OM, pesticide, pathogen, metal, and salt delivery ratios.
  in_aqu: Public instance of `input_aqu`; holds aquifer filenames `initial.aqu` and `aquifer.aqu`.
    Aquifer readers use these names for aquifer database and initial-condition setup.
  in_herd: Public instance of `input_herd`; holds herd files `animal.hrd`, `herd.hrd`, and
    `ranch.hrd`. Herd-related readers use these to load animal, herd, and ranch setup data.
  in_watrts: Public instance of `input_water_rights`; holds water-rights filenames `water_allocation.wro`,
    `element.wro`, and `water_rights.wro`. Water-allocation routines use these names to read
    decision-table-driven transfer and compensation settings.
  in_link: Public instance of `input_link`; holds linkage filenames `chan-surf.lin` and `aqu_cha.lin`.
    Link readers use these to connect channels and aquifers to surface and 2-D groundwater
    structures.
  in_hyd: Public instance of `input_hydrology`; holds hydrology filenames `hydrology.hyd`,
    `topography.hyd`, and `field.fld`. Hydrology readers use these to load general hydrology,
    topography, and field data.
  in_str: Public instance of `input_structural`; holds structural practice filenames `tiledrain.str`,
    `septic.str`, `filterstrip.str`, `grassedww.str`, and `bmpuser.str`. Structural-practice
    readers use these filenames to load BMP and drainage settings.
  in_parmdb: Public instance of `input_parameter_databases`; holds parameter-database filenames
    for plants, fertilizer, tillage, pesticide, pathogen, metal, salt, urban, septic, and
    snow inputs. Database readers use these names to load the shared HRU parameter tables.
  in_ops: Public instance of `input_ops`; holds operation-scheduling filenames `harv.ops`,
    `graze.ops`, `irr.ops`, `chem_app.ops`, `fire.ops`, and `sweep.ops`. Operation readers
    use these to load management operation schedules.
  in_lum: Public instance of `input_lum`; holds land-use-management filenames `landuse.lum`,
    `management.sch`, `cntable.lum`, `cons_practice.lum`, and `ovn_table.lum`. Land-use readers
    use these to load management schedules, curve-number tables, conservation practices, and
    roughness tables.
  in_chg: Public instance of `input_chg`; holds calibration-change filenames `cal_parms.cal`,
    `calibration.cal`, `codes.sft`, `wb_parms.sft`, `water_balance.sft`, `ch_sed_budget.sft`,
    `ch_sed_parms.sft`, `plant_parms.sft`, and `plant_gro.sft`. Calibration readers use these
    names to load parameter changes, update definitions, and soft-calibration codes.
  in_init: Public instance of `input_init`; holds initial-condition filenames for plant, soil-plant,
    organic matter water, pesticide, pathogen, hmet, and salt state tables. Initial-condition
    readers use these names to load starting masses and concentrations.
  in_sol: Public instance of `input_soils`; holds soil database filenames `soils.sol`, `nutrients.sol`,
    and `soils_lte.sol`. Soil readers use these names to load soil and nutrient parameter
    tables.
  in_cond: Public instance of `input_condition`; holds conditional-decision-table filenames
    `lum.dtl`, `res_rel.dtl`, `scen_lu.dtl`, and `flo_con.dtl`. Conditional readers use these
    to load decision tables for land use, reservoirs, scenarios, and flow control.
  in_regs: Public instance of `input_regions`; holds region and catalog-unit filenames for
    landscape units, channel, aquifer, reservoir, and recall regions. Region readers use these
    names to load element lists, definition files, and regional calibration/output mappings.
  in_shf: Public instance of `shade_factor`; holds the shade-factor filename `shade_factor.shf`.
    Shade-factor readers use it to load channel temperature shade adjustments.
  in_path_pcp: Public instance of `input_path_pcp`; stores an optional directory prefix for
    precipitation station files. Precipitation climate readers use it to construct full station-file
    paths.
  in_path_tmp: Public instance of `input_path_tmp`; stores an optional directory prefix for
    measured temperature files. Temperature climate readers use it to construct full file
    paths.
  in_path_slr: Public instance of `input_path_slr`; stores an optional directory prefix for
    measured solar-radiation files. Solar-radiation climate readers use it to construct full
    file paths.
  in_path_hmd: Public instance of `input_path_hmd`; stores an optional directory prefix for
    measured humidity files. Humidity climate readers use it to construct full file paths.
  in_path_wnd: Public instance of `input_path_wnd`; stores an optional directory prefix for
    measured wind files. Wind climate readers use it to construct full file paths.
  in_path_pet: Public instance of `input_path_pet`; stores an optional directory prefix for
    measured PET files. PET climate readers use it to construct full file paths.
type_components:
  input_sim:
    time: Name of the simulation time-control file; defaults to `time.sim`.
    prt: Name of the print-code file; defaults to `print.prt`.
    object_prt: Name of the object-output print file; defaults to `object.prt`.
    object_cnt: Name of the basin object-connectivity/count file; defaults to `object.cnt`.
    cs_db: Name of the constituent database file; defaults to `constituents.cs`.
  input_basin:
    codes_bas: Name of the basin control-code file; defaults to `codes.bsn`.
    parms_bas: Name of the basin-parameter file; defaults to `parameters.bsn`.
    carbon_bsn: Name of the basin carbon file; defaults to `carbon.bsn`.
  input_cli:
    weat_sta: Name of the weather-station list file; defaults to `weather-sta.cli`.
    weat_wgn: Name of the weather-generator list file; defaults to `weather-wgn.cli`.
    pet_cli: Name of the PET control file; defaults to `pet.cli`.
    pcp_cli: Name of the precipitation-station list file; defaults to `pcp.cli`.
    tmp_cli: Name of the measured-temperature list file; defaults to `tmp.cli`.
    slr_cli: Name of the measured solar-radiation list file; defaults to `slr.cli`.
    hmd_cli: Name of the measured humidity list file; defaults to `hmd.cli`.
    wnd_cli: Name of the measured wind list file; defaults to `wnd.cli`.
    atmo_cli: Name of the atmospheric deposition file; defaults to `atmodep.cli`.
  input_con:
    hru_con: Name of the HRU connectivity file; defaults to `hru.con`.
    hruez_con: Name of the HRU-LTE connectivity file; defaults to `hru-lte.con`.
    ru_con: Name of the routing-unit connectivity file; defaults to `rout_unit.con`.
    gwflow_con: Name of the gwflow connectivity file; defaults to `gwflow.con`.
    aqu_con: Name of the aquifer connectivity file; defaults to `aquifer.con`.
    aqu2d_con: Name of the 2-D aquifer connectivity file; defaults to `aquifer2d.con`.
    chan_con: Name of the channel connectivity file; defaults to `channel.con`.
    res_con: Name of the reservoir connectivity file; defaults to `reservoir.con`.
    rec_con: Name of the recall connectivity file; defaults to `recall.con`.
    exco_con: Name of the exco connectivity file; defaults to `exco.con`.
    delr_con: Name of the delivery-ratio connectivity file; defaults to `delratio.con`.
    out_con: Name of the outlet connectivity file; defaults to `outlet.con`.
    chandeg_con: Name of the channel-degradation connectivity file; defaults to `chandeg.con`.
  input_cha:
    init: Name of the channel initial-condition file; defaults to `initial.cha`.
    dat: Name of the channel data file; defaults to `channel.cha`.
    hyd: Name of the channel hydrology file; defaults to `hydrology.cha`.
    sed: Name of the channel sediment file; defaults to `sediment.cha`.
    nut: Name of the channel nutrient file; defaults to `nutrients.cha`.
    chan_ez: Name of the channel-LTE data file; defaults to `channel-lte.cha`.
    hyd_sed: Name of the hydrology-sediment LTE file; defaults to `hyd-sed-lte.cha`.
    temp: Name of the channel temperature file; defaults to `temperature.cha`.
  input_res:
    init_res: Name of the reservoir initial-condition file; defaults to `initial.res`.
    res: Name of the reservoir data file; defaults to `reservoir.res`.
    hyd_res: Name of the reservoir hydrology file; defaults to `hydrology.res`.
    sed_res: Name of the reservoir sediment file; defaults to `sediment.res`.
    nut_res: Name of the reservoir nutrient file; defaults to `nutrients.res`.
    weir_res: Name of the reservoir weir file; defaults to `weir.res`.
    wet: Name of the wetland data file; defaults to `wetland.wet`.
    hyd_wet: Name of the wetland hydrology file; defaults to `hydrology.wet`.
  input_ru:
    ru_def: Name of the routing-unit definition file; defaults to `rout_unit.def`.
    ru_ele: Name of the routing-unit element file; defaults to `rout_unit.ele`.
    ru: Name of the routing-unit data file; defaults to `rout_unit.rtu`.
    ru_dr: Name of the routing-unit delivery-ratio file; defaults to `rout_unit.dr`.
  input_hru:
    hru_data: Name of the HRU data file; defaults to `hru-data.hru`.
    hru_ez: Name of the HRU-LTE data file; defaults to `hru-lte.hru`.
  input_exco:
    exco: Name of the general exco file; defaults to `exco.exc`.
    om: Name of the organic-matter exco file; defaults to `exco_om.exc`.
    pest: Name of the pesticide exco file; defaults to `exco_pest.exc`.
    path: Name of the pathogen exco file; defaults to `exco_path.exc`.
    hmet: Name of the metal exco file; defaults to `exco_hmet.exc`.
    salt: Name of the salt exco file; defaults to `exco_salt.exc`.
  input_rec:
    recall_rec: Name of the recall database file; defaults to `recall.rec`.
  input_delr:
    del_ratio: Name of the general delivery-ratio file; defaults to `delratio.del`.
    om: Name of the organic-matter delivery-ratio file; defaults to `dr_om.del`.
    pest: Name of the pesticide delivery-ratio file; defaults to `dr_pest.del`.
    path: Name of the pathogen delivery-ratio file; defaults to `dr_path.del`.
    hmet: Name of the metal delivery-ratio file; defaults to `dr_hmet.del`.
    salt: Name of the salt delivery-ratio file; defaults to `dr_salt.del`.
  input_aqu:
    init: Name of the aquifer initial-condition file; defaults to `initial.aqu`.
    aqu: Name of the aquifer data file; defaults to `aquifer.aqu`.
  input_herd:
    animal: Name of the animal file; defaults to `animal.hrd`.
    herd: Name of the herd file; defaults to `herd.hrd`.
    ranch: Name of the ranch file; defaults to `ranch.hrd`.
  input_water_rights:
    transfer_wro: Name of the water-allocation transfer file; defaults to `water_allocation.wro`.
    element: Name of the water-rights element file; defaults to `element.wro`.
    water_rights: Name of the water-rights database file; defaults to `water_rights.wro`.
  input_link:
    chan_surf: Name of the channel-surface linkage file; defaults to `chan-surf.lin`.
    aqu_cha: Name of the aquifer-channel linkage file; defaults to `aqu_cha.lin`.
  input_hydrology:
    hydrol_hyd: Name of the hydrology input file; defaults to `hydrology.hyd`.
    topogr_hyd: Name of the topography input file; defaults to `topography.hyd`.
    field_fld: Name of the field input file; defaults to `field.fld`.
  input_structural:
    tiledrain_str: Name of the tile-drain file; defaults to `tiledrain.str`.
    septic_str: Name of the septic-system file; defaults to `septic.str`.
    fstrip_str: Name of the filter-strip file; defaults to `filterstrip.str`.
    grassww_str: Name of the grassed-waterway file; defaults to `grassedww.str`.
    bmpuser_str: Name of the user-defined BMP file; defaults to `bmpuser.str`.
  input_parameter_databases:
    plants_plt: Name of the plants parameter database; defaults to `plants.plt`.
    fert_frt: Name of the fertilizer parameter database; defaults to `fertilizer.frt`.
    till_til: Name of the tillage parameter database; defaults to `tillage.til`.
    pest: Name of the pesticide parameter database; defaults to `pesticide.pes`.
    pathcom_db: Name of the pathogen parameter database; defaults to `pathogens.pth`.
    hmetcom_db: Name of the metal parameter database; defaults to `metals.mtl`.
    saltcom_db: Name of the salt parameter database; defaults to `salt.slt`.
    urban_urb: Name of the urban parameter database; defaults to `urban.urb`.
    septic_sep: Name of the septic parameter database; defaults to `septic.sep`.
    snow: Name of the snow parameter database; defaults to `snow.sno`.
  input_ops:
    harv_ops: Name of the harvest-operations file; defaults to `harv.ops`.
    graze_ops: Name of the grazing-operations file; defaults to `graze.ops`.
    irr_ops: Name of the irrigation-operations file; defaults to `irr.ops`.
    chem_ops: Name of the chemical-application operations file; defaults to `chem_app.ops`.
    fire_ops: Name of the fire-operations file; defaults to `fire.ops`.
    sweep_ops: Name of the sweep-operations file; defaults to `sweep.ops`.
  input_lum:
    landuse_lum: Name of the land-use database file; defaults to `landuse.lum`.
    management_sch: Name of the management-schedule file; defaults to `management.sch`.
    cntable_lum: Name of the curve-number lookup table; defaults to `cntable.lum`.
    cons_prac_lum: Name of the conservation-practice file; defaults to `cons_practice.lum`.
    ovn_lum: Name of the overland-N roughness table; defaults to `ovn_table.lum`.
  input_chg:
    cal_parms: Name of the calibration-parameter change file; defaults to `cal_parms.cal`.
    cal_upd: Name of the calibration update file; defaults to `calibration.cal`.
    codes_sft: Name of the soft-calibration codes file; defaults to `codes.sft` and was renamed
      from `codes.cal`.
    wb_parms_sft: Name of the watershed-balance parameter file; defaults to `wb_parms.sft`
      and was renamed from `ls_parms.cal`.
    water_balance_sft: Name of the water-balance region file; defaults to `water_balance.sft`
      and was renamed from `ls_regions.cal`.
    ch_sed_budget_sft: Name of the channel sediment-budget file; defaults to `ch_sed_budget.sft`
      and was renamed from `ch_orders.cal`.
    ch_sed_parms_sft: Name of the channel sediment-parameter file; defaults to `ch_sed_parms.sft`
      and was renamed from `ch_parms.cal`.
    plant_parms_sft: Name of the plant-parameter calibration file; defaults to `plant_parms.sft`
      and was renamed from `pl_parms.cal`.
    plant_gro_sft: Name of the plant-growth calibration file; defaults to `plant_gro.sft`
      and was renamed from `pl_regions.cal`.
  input_init:
    plant: Name of the plant initial-condition file; defaults to `plant.ini`.
    soil_plant_ini: Name of the soil-plant initial-condition file; defaults to `soil_plant.ini`.
    om_water: Name of the organic-matter water initial-condition file; defaults to `om_water.ini`.
    pest_soil: Name of the soil pesticide initial-condition file; defaults to `pest_hru.ini`.
    pest_water: Name of the water pesticide initial-condition file; defaults to `pest_water.ini`.
    path_soil: Name of the soil pathogen initial-condition file; defaults to `path_hru.ini`.
    path_water: Name of the water pathogen initial-condition file; defaults to `path_water.ini`.
    hmet_soil: Name of the soil metal initial-condition file; defaults to `hmet_hru.ini`.
    hmet_water: Name of the water metal initial-condition file; defaults to `hmet_water.ini`.
    salt_soil: Name of the soil salt initial-condition file; defaults to `salt_hru.ini`.
    salt_water: Name of the water salt initial-condition file; defaults to `salt_water.ini`.
  input_soils:
    soils_sol: Name of the soils database file; defaults to `soils.sol`.
    nut_sol: Name of the soils nutrient database file; defaults to `nutrients.sol`.
    lte_sol: Name of the LTE soils database file; defaults to `soils_lte.sol`.
  input_condition:
    dtbl_lum: Name of the land-use decision table file; defaults to `lum.dtl`.
    dtbl_res: Name of the reservoir decision table file; defaults to `res_rel.dtl`.
    dtbl_scen: Name of the scenario decision table file; defaults to `scen_lu.dtl`.
    dtbl_flo: Name of the flow-control decision table file; defaults to `flo_con.dtl`.
  input_regions:
    ele_lsu: Name of the landscape-unit element file; defaults to `ls_unit.ele`.
    def_lsu: Name of the landscape-unit definition file; defaults to `ls_unit.def`.
    ele_reg: Name of the landscape-region element file; defaults to `ls_reg.ele`.
    def_reg: Name of the landscape-region definition file; defaults to `ls_reg.def`.
    cal_lcu: Name of the landscape calibration-region file; defaults to `ls_cal.reg`.
    ele_cha: Name of the channel catalog-unit element file; defaults to `ch_catunit.ele`.
    def_cha: Name of the channel catalog-unit definition file; defaults to `ch_catunit.def`.
    def_cha_reg: Name of the channel calibration-region definition file; defaults to `ch_reg.def`.
    ele_aqu: Name of the aquifer catalog-unit element file; defaults to `aqu_catunit.ele`.
    def_aqu: Name of the aquifer catalog-unit definition file; defaults to `aqu_catunit.def`.
    def_aqu_reg: Name of the aquifer calibration-region definition file; defaults to `aqu_reg.def`.
    ele_res: Name of the reservoir catalog-unit element file; defaults to `res_catunit.ele`.
    def_res: Name of the reservoir catalog-unit definition file; defaults to `res_catunit.def`.
    def_res_reg: Name of the reservoir calibration-region definition file; defaults to `res_reg.def`.
    ele_psc: Name of the recall catalog-unit element file; defaults to `rec_catunit.ele`.
    def_psc: Name of the recall catalog-unit definition file; defaults to `rec_catunit.def`.
    def_psc_reg: Name of the recall calibration-region definition file; defaults to `rec_reg.def`.
  shade_factor:
    ssff_shf: Name of the shade-factor file; defaults to `shade_factor.shf`.
  input_path_pcp:
    pcp: Optional directory prefix for precipitation station files; default is blank.
  input_path_tmp:
    tmp: Optional directory prefix for measured temperature files; default is blank.
  input_path_slr:
    slr: Optional directory prefix for measured solar-radiation files; default is blank.
  input_path_hmd:
    hmd: Optional directory prefix for measured humidity files; default is blank.
  input_path_wnd:
    wnd: Optional directory prefix for measured wind files; default is blank.
  input_path_pet:
    peti: Optional directory prefix for measured PET files; default is blank.
type_summaries:
  input_sim: simulation
  input_basin: basin
  input_cli: climate
  input_con: connect
  input_cha: channel
  input_res: reservoir
  input_ru: routing unit
  input_hru: HRU
  input_exco: exco (recall constant)
  input_rec: recall (daily, monthly and annual)
  input_delr: delivery ratio
  input_aqu: aquifer
  input_herd: herd
  input_water_rights: water-rights
  input_link: link
  input_hydrology: hydrology
  input_structural: structural
  input_parameter_databases: HRU databases
  input_ops: operation scheduling
  input_lum: land use management
  input_chg: calibration change
  input_init: initial conditions
  input_soils: soils
  input_condition: conditional
  input_regions: regions
  shade_factor: shade factor
  input_path_pcp: precipitation file path prefix
  input_path_tmp: temperature file path prefix
  input_path_slr: solar-radiation file path prefix
  input_path_hmd: humidity file path prefix
  input_path_wnd: wind file path prefix
  input_path_pet: PET file path prefix
---

<!-- facts:header -->

`input_file_module` is the central declaration container for SWAT+ file-name state. It owns the typed input-file records used to name simulation, basin, climate, connectivity, channel, reservoir, routing-unit, HRU, exco, recall, delivery-ratio, aquifer, herd, water-rights, link, hydrology, structural, parameter-database, operations, land-use-management, calibration-change, initial-condition, soils, conditional, region, shade-factor, and climate-path inputs. The module itself contains no procedures; startup and reader routines in other modules populate or consume these public variables to determine which input files are opened and how related model databases are sized and loaded.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only: it defines public typed filename records with default string values, but contains no setup procedures itself. Other readers check these names, open the corresponding files, and may rewrite some fields during model setup when connectivity changes require substituted filenames.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:aqu2d_read] | `aqu_cha.lin` | `in_link%aqu_cha` | Uses the aquifer-channel linkage filename to open the 2-D groundwater linkage file and populate aquifer-to-element mappings. |
| [sym:aqu_read] | `aquifer.aqu` | `in_aqu%aqu` | Uses the aquifer database filename to open and load shallow-aquifer property records. |
| [sym:aqu_read_elements] | `aqu_catunit.def, aqu_catunit.ele` | `in_regs%def_aqu, in_regs%def_aqu_reg, in_regs%ele_aqu` | Uses the aquifer definition and element filenames to load aquifer catalog-unit and calibration-region memberships. |
| [sym:aqu_read_init] | `initial.aqu` | `in_aqu%init` | Uses the aquifer initial-condition filename to read aquifer startup records. |
| [sym:aqu_read_init_cs] | `initial.aqu_cs` | `input_file_module state for file-path/availability context` | Reads aquifer initial constituent settings from the aquifer constituent initialization file; the resolved symbol was not extracted in the packet. |
| [sym:basin_print_codes_read] | `print.prt, unit_*` | `in_sim%prt` | Uses the print-code filename to load basin output-control settings. |
| [sym:basin_read_cc] | `codes.bsn, pet.cli` | `in_basin%codes_bas` | Uses the basin control-code filename to load basin control settings and related PET header data. |
| [sym:basin_read_objs] | `unit_*, object.cnt, chancell.gw, gwflow_record` | `in_sim%object_cnt, in_con%gwflow_con, in_con%aqu_con` | Uses the object-count and connection filenames to read basin object connectivity and, when gwflow is active, substitute gwflow connection naming and disable aquifer connections. |
| [sym:basin_read_prm] | `parameters.bsn` | `in_basin%parms_bas` | Uses the basin parameter filename to load basin-wide parameter values. |
| [sym:cal_cond_read] | `scen_dtl.upd` | `input_file_module state for file-path/availability context` | Loads conditional calibration/update definitions from the scenario update file; no specific resolved filename symbol was extracted from the packet. |
| [sym:cal_parm_read] | `cal_parms.cal` | `in_chg%cal_parms` | Uses the calibration-parameter filename to read the list of parameter changes for calibration. |
| [sym:cal_parmchg_read] | `calibration.cal` | `in_chg%cal_upd` | Uses the calibration-update filename to read calibration update records and expand their targets. |

## Key Consumers

The main consumers are startup and input-reader routines that use these public filename records to decide which files to open, plus a smaller set of routines that rewrite selected names when gwflow or other connectivity substitutions are active. Climate readers, channel/reservoir/aquifer readers, calibration readers, land-use and operation database readers, and output/setup routines all depend on this module for their file paths.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:carbon_bsn_read] | `in_basin` | Reads `in_basin%carbon_bsn` to open the basin carbon file, and derives the companion layer file name from that same configured path so the carbon setup loads the intended records. |
| [sym:aqu2d_read] | input_file_module | Uses `in_link%aqu_cha` to locate the aquifer-channel linkage file and build the 2-D groundwater aquifer connectivity arrays. |
| [sym:aqu_read] | input_file_module | Uses `in_aqu%aqu` to open the aquifer property database and load shallow-aquifer records. |
| [sym:aqu_read_elements] | input_file_module | Uses `in_regs%def_aqu`, `in_regs%def_aqu_reg`, and `in_regs%ele_aqu` to load aquifer region definitions, calibration regions, and element memberships. |
| [sym:aqu_read_init] | input_file_module | Uses `in_aqu%init` to open the aquifer initial-condition file and size aquifer startup arrays. |
| [sym:basin_print_codes_read] | input_file_module | Uses `in_sim%prt` to open `print.prt` and load basin print intervals and output flags. |
| [sym:basin_read_cc] | input_file_module | Uses `in_basin%codes_bas` to open the basin control file and load basin control codes. |
| [sym:basin_read_objs] | input_file_module | Uses `in_sim%object_cnt`, `in_con%gwflow_con`, and `in_con%aqu_con` to read basin object counts and rewrite connection-file names when gwflow replaces aquifer objects. |
| [sym:basin_read_prm] | input_file_module | Uses `in_basin%parms_bas` to open the basin parameter file and populate `bsn_prm`. |
| [sym:cal_parm_read] | input_file_module | Uses `in_chg%cal_parms` to test, open, and read the calibration-parameter change file. |
| [sym:cal_parmchg_read] | input_file_module | Uses `in_chg%cal_upd` to open the calibration update file and expand the requested calibration targets. |
| [sym:calsoft_read_codes] | input_file_module | Uses `in_chg%codes_sft` to locate the soft-calibration codes file and set the active calibration flags. |
| [sym:ch_read] | input_file_module | Uses `in_cha%dat` to open `channel.cha` and load channel data records. |
| [sym:ch_read_elements] | input_file_module | Uses `in_regs%def_cha` and `in_regs%def_cha_reg` to load channel definitions and channel calibration-region definitions. |
| [sym:ch_read_hyd] | input_file_module | Uses `in_cha%hyd` to open the channel hydrology file and populate channel hydrology records. |
| [sym:ch_read_init] | input_file_module | Uses `in_cha%init` to open the channel initial-condition file and load channel startup data. |
| [sym:ch_read_init_cs] | input_file_module | Uses the channel constituent initial-condition file path to load channel constituent startup data, but the resolved module symbol was not extracted from the packet. |
| [sym:ch_read_nut] | input_file_module | Uses `in_cha%nut` to open the channel nutrient file and load nutrient reaction parameters. |
| [sym:ch_read_orders_cal] | input_file_module | Uses `in_chg%ch_sed_budget_sft` to open the channel sediment-budget calibration file and load order-based calibration data. |
| [sym:ch_read_parms_cal] | input_file_module | Uses `in_chg%ch_sed_parms_sft` to open the channel sediment-parameter calibration file and load sediment calibration parameters. |
| [sym:ch_read_sed] | input_file_module | Uses `in_cha%sed` to open the channel sediment file and load sediment routing parameters. |
| [sym:ch_read_temp] | input_file_module | Uses `in_cha%temp` to open the channel temperature file and load temperature records. |
| [sym:cli_hmeas] | input_file_module | Uses `in_cli%hmd_cli` and `in_path_hmd%hmd` to locate humidity-file lists and build each measured-humidity file path. |
| [sym:cli_petmeas] | input_file_module | Uses `in_cli%pet_cli` and `in_path_pet%peti` to locate PET control files and measured PET data files. |
| [sym:cli_pmeas] | input_file_module | Uses `in_cli%pcp_cli` and `in_path_pcp%pcp` to locate precipitation station lists and the referenced station files. |

## Lineage

`input_file_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `input_file_module.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `input_file_module` has no extracted module-level documentation comment.
- The importer table is deterministic and complete for this source span; the main Used By table is a curated subset of consumers with source-backed effects.
- No resolved Git lineage commits were available for this source span.
- Some reader entries in the draft overlay were representative placeholders; the completed reader list keeps only routines with source-backed evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
