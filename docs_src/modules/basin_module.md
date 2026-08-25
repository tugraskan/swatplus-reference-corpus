---
kind: module
symbol: basin_module
title: basin_module
status: filled
source_hash: b7c09c786d5db775
version_label: SWAT+ 62.0.0
variables:
  prog: Character program/run label stored in the basin module for use by header writers and
    other routines that need the simulation name. It is initialized to an empty string here
    and is consumed by output-header routines such as `header_*` writers that import `basin_module`.
  ban_precip_aa: Basin average annual precipitation accumulator used by basin output code.
    It is initialized to 0.0 here and is read by `basin_output` as part of basin-average reporting.
  bsn: Basin input record holding the basin name and total basin area in hectares. It is initialized
    with blank name and zero areas here, then filled by basin/object readers such as `basin_read_objs`;
    downstream consumers use `bsn%name` for labels and `bsn%area_tot_ha` for basin-wide weighting.
  bsn_cc: Basin control-code record that holds model switches for PET, routing, carbon mode,
    GWFLOW, and other basin-wide options. It is initialized with default codes here and populated
    by `basin_read_cc`; many setup and process routines consult these flags to choose model
    branches.
  bsn_prm: Basin-parameter record holding routing, ET, erosion, carbon, climate lapse, and
    other basin-scale calibration values. It is initialized with defaults here and then read
    by `basin_read_prm` and normalized by `basin_prm_default`; hydrology, ET, routing, nutrient,
    and calibration routines read these values later.
  pco: Global print-control record that stores the requested output intervals and file-type
    switches from `print.prt`. It is initialized with defaults here and populated by `basin_print_codes_read`;
    nearly all output routines read it to decide whether to write daily, monthly, yearly,
    average-annual, and CSV records.
  pco_init: Saved initial copy of the print-control record. It is declared in the basin module
    so print settings can be preserved or reset during initialization workflows.
  bsn_sedbud: Basin sediment-budget accumulator used to track upland sediment, bank erosion,
    floodplain deposition, and reservoir trapping. It is initialized to zeroed totals here
    and consumed by basin sediment-budget reporting routines.
  mgt_hdr: Management-output header record containing column labels such as HRU, year, month,
    day, crop, operation, PHU, soil water, biomass, residue, nitrate, phosphorus, and variable
    slots. It is initialized with fixed text labels here and used by management output/header
    writers.
  mgt_hdr_unt1: Alternate management-output header record that stores unit strings for the
    same management columns. It is initialized here for management output writers that need
    units instead of field names.
  bsn_yld_hdr: Yield-output header record containing labels for year, plant number, plant
    name, harvested area, yield, and yield per hectare. It is initialized here and used by
    yield header writers.
type_components:
  basin_inputs:
    name: Basin name string used on basin-level output records.
    area_ls_ha: Land-surface area in hectares for the basin input record; used as the basin-area
      weighting basis.
    area_tot_ha: Total basin area in hectares; used for basin-wide averaging and output weighting.
  basin_control_codes:
    petfile: Potential ET filename used by basin control logic.
    wwqfile: Watershed stream water quality filename.
    pet: Potential ET method code.
    nam1: 'PET method selector: 0 Priestley-Taylor, 1 Penman-Monteith, 2 Hargreaves; marked
      not used in this source comment.'
    crk: Crack flow code.
    swift_out: Switch that controls writing SWIFT input.
    sed_det: Peak rate method / SWIFT write control as documented in source comments.
    rte: Water routing method code.
    deg: Variable storage / Muskingum code marked not used.
    wq: Not used.
    nostress: Reused as the sequence number and changed to no nutrient stress.
    cn: Plant stress control code.
    cfac: Not used.
    cswat: 'Carbon model code: 0 static, 1 C-FARM, 2 CENTURY/SWAT-C.'
    lapse: Precipitation and temperature lapse-rate control.
    uhyd: Unit hydrograph method selector.
    sed_ch: Triangular versus gamma unit hydrograph selector, marked not used.
    tdrn: Tile drainage equation code.
    wtdn: Shallow water table depth algorithm code.
    sol_p_model: Soil phosphorus model selector.
    gampt: Green-Ampt infiltration selector.
    atmo: Not used.
    smax: Not used.
    qual2e: QUAL2E instream nutrient routing code.
    gwflow: GWFLOW activation flag.
    idc_till: Tillage method selector used when `cswat = 2`.
  basin_parms:
    evlai: Leaf area index threshold at which no evap occurs.
    ffcb: Initial soil water content as a fraction of field capacity.
    surlag: Surface runoff lag time in days.
    adj_pkr: Peak-rate adjustment factor in the subbasin.
    prf: Peak rate factor for the peak-rate equation.
    spcon: Not used.
    spexp: Not used.
    cmn: Mineralization rate factor for active organic nitrogen.
    n_updis: Nitrogen uptake distribution parameter.
    p_updis: Phosphorus uptake distribution parameter.
    nperco: Nitrate percolation coefficient.
    pperco: Phosphorus percolation coefficient.
    phoskd: Soil phosphorus partitioning coefficient.
    psp: Phosphorus availability index.
    rsdco: Residue decomposition coefficient.
    percop: Pesticide percolation coefficient.
    msk_co1: Storage calibration coefficient.
    msk_co2: Reach storage calibration coefficient at bankfull depth.
    msk_x: Low-flow storage weighting factor.
    nperco_lchtile: N concentration coefficient for tile flow and bottom-layer leachate.
    evrch: Reach evaporation adjustment factor.
    scoef: Channel storage coefficient.
    cdn: Denitrification exponential rate coefficient.
    sdnco: Denitrification threshold fraction of field capacity.
    bact_swf: Fraction of manure containing active colony-forming units.
    tb_adj: Subdaily unit hydrograph basetime adjustment.
    cn_froz: Frozen-soil adjustment factor for infiltration/runoff.
    dorm_hr: Dormancy-hour threshold.
    plaps: Precipitation lapse rate in mm per km of elevation difference.
    tlaps: Temperature lapse rate in degrees C per km.
    nfixmx: Maximum daily nitrogen fixation in kg/ha.
    decr_min: Minimum daily residue decay.
    rsd_covco: Residue cover factor.
    urb_init_abst: Maximum initial abstraction for urban areas with Green-Ampt.
    petco_pmpt: PET adjustment percent for Penman-Monteith and Priestley-Taylor.
    uhalpha: Alpha coefficient for gamma-function unit hydrograph.
    eros_spl: Splash-erosion coefficient.
    rill_mult: Rill-erosion coefficient.
    eros_expo: Overland-flow exponential coefficient.
    c_factor: Cover and management scaling factor for overland-flow erosion.
    ch_d50: Median particle diameter of the main channel in mm.
    co2: Initial CO2 concentration in ppm.
    day_lag_mx: Maximum number of lag days for HRU, RU, and channel hydrographs.
    igen: Random-generator code for non-draining soils.
  print_interval:
    d: Daily output flag.
    m: Monthly output flag.
    y: Yearly output flag.
    a: Average-annual output flag.
    already_read_in: Logical marker that the corresponding print object has already been read
      from `print.prt`.
  basin_print_codes:
    day_print: Gate for daily output timing.
    day_print_over: Daily-output override flag.
    nyskip: Number of years to skip output summarization.
    sw_init: Switch marking whether soil-water output has been initialized.
    day_start: Julian day to start printing output.
    day_end: Julian day to end printing output.
    yrc_start: Calendar year to start printing output.
    yrc_end: Calendar year to end printing output.
    int_day: Daily print interval.
    int_day_cur: Current day since last print.
    aa_numint: Number of average-annual print intervals.
    aa_yrs: End years for average-annual output.
    csvout: CSV output switch.
    use_obj_labels: Label-driven print.prt parsing switch.
    cdfout: NetCDF output switch.
    crop_yld: Crop-yield output switch.
    mgtout: Management output switch.
    hydcon: Hydrograph-connect output switch.
    fdcout: Flow-duration-curve output switch.
    wb_bsn: Basin water-balance print interval.
    nb_bsn: Basin nutrient-balance print interval.
    ls_bsn: Basin losses print interval.
    pw_bsn: Basin plant-weather print interval.
    aqu_bsn: Basin aquifer print interval.
    res_bsn: Basin reservoir print interval.
    chan_bsn: Basin channel print interval.
    sd_chan_bsn: Basin SWAT-DEG channel print interval.
    recall_bsn: Basin recall print interval.
    wb_reg: Region water-balance print interval.
    nb_reg: Region nutrient-balance print interval.
    ls_reg: Region losses print interval.
    pw_reg: Region plant-weather print interval.
    aqu_reg: Region aquifer print interval.
    res_reg: Region reservoir print interval.
    sd_chan_reg: Region SWAT-DEG channel print interval.
    recall_reg: Region recall print interval.
    water_allo: Water-allocation print interval.
    wb_lsu: LSU water-balance print interval.
    nb_lsu: LSU nutrient-balance print interval.
    ls_lsu: LSU losses print interval.
    pw_lsu: LSU plant-weather print interval.
    wb_hru: HRU water-balance print interval.
    nb_hru: HRU nutrient-balance print interval.
    ls_hru: HRU losses print interval.
    pw_hru: HRU plant-weather print interval.
    cb_hru: Legacy carbon flag kept for print.prt backward compatibility.
    cb_vars_hru: Legacy carbon variable flag.
    cb_gl_hru: HRU carbon gain/loss family print flags.
    cb_trf_hru: HRU carbon transformations print flags.
    cb_lyr_hru: Per-layer SOC totals and sequestered carbon print flags.
    cb_cpool_hru: Per-layer carbon pool print flags.
    cb_npool_hru: Per-layer N and P pool print flags.
    cb_plt_hru: Plant carbon state print flags.
    cb_flux_hru: Per-layer carbon flux diagnostic flags.
    cb_drv_hru: Per-layer carbon driver diagnostic flags.
    cb_dyn_hru: Per-layer carbon dynamics diagnostic flags.
    cb_snap_hru: Soil-property snapshot print flags.
    cb_gl_lsu: LSU area-weighted carbon gain/loss family flags.
    cb_trf_lsu: LSU area-weighted carbon transformation flags.
    cb_plt_lsu: LSU area-weighted plant carbon state flags.
    wb_sd: HRU-LTE water-balance print interval.
    nb_sd: HRU-LTE nutrient-balance print interval.
    ls_sd: HRU-LTE losses print interval.
    pw_sd: HRU-LTE plant-weather print interval.
    chan: Channel output interval.
    sd_chan: SWAT-DEG channel output interval.
    aqu: Aquifer output interval.
    res: Reservoir output interval.
    recall: Recall output interval.
    hyd: Hyd input/output interval.
    ru: Routing-unit print interval.
    pest: Pesticide output interval across object families.
    salt_basin: Basin salt output interval.
    salt_hru: HRU salt output interval.
    salt_ru: Routing-unit salt output interval.
    salt_aqu: Aquifer salt output interval.
    salt_chn: Channel salt output interval.
    salt_res: Reservoir salt output interval.
    salt_wet: Wetland salt output interval.
    cs_basin: Basin constituent output interval.
    cs_hru: HRU constituent output interval.
    cs_ru: Routing-unit constituent output interval.
    cs_aqu: Aquifer constituent output interval.
    cs_chn: Channel constituent output interval.
    cs_res: Reservoir constituent output interval.
    cs_wet: Wetland constituent output interval.
    gwflow_wb: GWFLOW cell and basin water-balance output interval.
    gwflow_flux: GWFLOW diagnostic flux output interval.
    gwflow_heat: GWFLOW basin heat-balance output interval.
    gwflow_solute: GWFLOW basin solute-balance output interval.
    gwflow_obs: GWFLOW observation-well output interval.
    gwflow_pump: GWFLOW HRU pumping output interval.
  basin_sediment_budget:
    upland_t: Total upland sediment yield in tons.
    ch_ebank_t: Total bank erosion in tons.
    up_ch_rto: Upland-to-channel ratio.
    ch_w_yr: Basin-average channel width per year.
    fp_dep_t: Total floodplain deposition in tons.
    fp_dep_mm: Basin floodplain deposition in mm/year.
    res_dep_t: Total reservoir deposition in tons.
    res_trap_eff: Average reservoir trap efficiency.
  mgt_header:
    hru: HRU label column.
    year: Year column.
    mon: Month column.
    day: Day column.
    crop: Crop / fertilizer / pesticide label column.
    oper: Operation column.
    phub: PHU base column.
    phua: Plant PHU accumulated column.
    sw: Soil water column.
    bio: Plant biomass column.
    rsd: Surface residue column.
    solno3: Soil nitrate column.
    solp: Soil soluble phosphorus column.
    op_var: Operation-variable label column.
    var1: Variable 1 label column.
    var2: Variable 2 label column.
    var3: Variable 3 label column.
    var4: Variable 4 label column.
    var5: Variable 5 label column.
    var6: Variable 6 label column.
    var7: Variable 7 label column.
  mgt_header_unit1:
    hru: HRU units/placeholder label.
    year: Year units/placeholder label.
    mon: Month units/placeholder label.
    day: Day units/placeholder label.
    crop: Crop units/placeholder label.
    oper: Operation units/placeholder label.
    phub: PHU-base unit label.
    phua: Plant PHU unit label.
    sw: Soil-water unit label.
    bio: Biomass unit label.
    rsd: Residue unit label.
    solno3: Soil nitrate unit label.
    solp: Soil phosphorus unit label.
    op_var: Operation-variable units/placeholder label.
    var1: Variable 1 units/placeholder label.
    var2: Variable 2 units/placeholder label.
    var3: Variable 3 units/placeholder label.
    var4: Variable 4 units/placeholder label.
    var5: Variable 5 units/placeholder label.
    var6: Variable 6 units/placeholder label.
    var7: Variable 7 units/placeholder label.
  basin_yld_header:
    year: Year label column.
    plant_no: Plant number label column.
    plant_name: Plant name label column.
    area_ha: Harvested area in hectares label.
    yield_t: Yield in tons label.
    yield_tha: Yield in tons per hectare label.
type_summaries:
  basin_inputs: Basin-wide input record for basin identity and total land area.
  basin_control_codes: Basin-level control-code record containing simulation switches and
    method selections.
  basin_parms: Basin-scale parameter record for routing, ET, erosion, carbon, climate lapse,
    and related model behavior.
  print_interval: Single output-interval selector with day, month, year, and average-annual
    flags plus a duplicate-read marker.
  basin_print_codes: Complete basin print-control table for simulation timing, file switches,
    and per-object output intervals.
  basin_sediment_budget: Basin sediment-budget accumulator.
  mgt_header: Management output header labels for standard management tables.
  mgt_header_unit1: Unit-label counterpart to the management header record.
  basin_yld_header: Yield output header labels for basin crop-yield tables.
---

<!-- facts:header -->

`basin_module` is the shared basin-state container for SWAT+. It owns basin identifiers, basin control codes, basin parameter defaults, print-interval settings, sediment-budget totals, and reusable output-header records. Startup readers such as `basin_read_cc`, `basin_read_prm`, `basin_print_codes_read`, and `basin_prm_default` populate or normalize that state, and many hydrology, routing, management, output, and calibration routines consume it throughout the run.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is primarily a declaration container. It defines shared basin state and output-header records; the actual values are populated by setup/read routines such as `basin_read_cc`, `basin_read_prm`, `basin_print_codes_read`, `basin_prm_default`, and `basin_read_objs`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:basin_read_cc] | `codes.bsn` | `bsn_cc` | Reads the basin control-code record from `codes.bsn` into `bsn_cc`, and if `bsn_cc%pet == 3` it also opens `pet.cli` to advance through the PET file structure. |
| [sym:basin_read_prm] | `parameters.bsn` | `bsn_prm` | Reads the basin parameter record from `parameters.bsn` into `bsn_prm` after skipping the title/header lines. |
| [sym:basin_print_codes_read] | `print.prt` | `pco` | Reads the simulation print-control file into `pco`, including timing fields, CSV/CDF switches, object-label mode, and the basin/region/LSU/HRU/routing/salt/carbon/gwflow output intervals. |
| [sym:basin_prm_default] | `none; defaults only` | `bsn_prm` | Fills missing basin-parameter values with defaults and derives normalized uptake coefficients and `day_lag_mx`. |
| [sym:basin_read_objs] | `object.cnt` | `bsn, bsn_cc` | Reads basin object counts and, when GWFLOW is active, may adjust object totals and deactivate GWFLOW if the supporting file is absent. |
| [sym:actions] | `unit_2612, unit_3612` | `pco, bsn_cc` | Reads `pco` to decide whether management output is written and checks `bsn_cc%cswat` to choose the tillage-mixing branch. |
| [sym:basin_sw_init] | `none` | `bsn` | Uses basin context during water-balance initialization; no specific basin symbol was resolved in the source snippet. |
| [sym:basin_read_prm] | `parameters.bsn` | `bsn_prm` | Populates the basin parameter structure before basin setup and output routines use it. |
| [sym:basin_prm_default] | `none` | `bsn_prm` | Applies basin parameter defaults and derived coefficients. |
| [sym:basin_print_codes_read] | `print.prt` | `pco` | Loads print timing and output switches for all basin output families. |

## Key Consumers

The module is used by basin setup routines, output writers, management/calibration code, and groundwater/transport processes. The strongest consumers are the initialization readers (`basin_read_cc`, `basin_read_prm`, `basin_print_codes_read`, `basin_prm_default`), basin output writers (`basin_output`, `basin_channel_output`, `basin_chanbud_output`, `basin_recall_output`, `basin_aquifer_output`, `basin_reservoir_output`), and hydrology/management routines that need `bsn_prm` or `bsn_cc` to choose method branches.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:gwflow_output_init] | `pco`, `bsn` | The print-control record gates which groundwater output files are opened, and the basin name is available for labeling those files and records. |
| [sym:gwflow_output_day] | `bsn` | The basin name labels the groundwater balance output, and the basin area is available for basin-wide normalization of daily groundwater volumes. |
| [sym:gwflow_output_mon] | `bsn` | The basin name is written into monthly groundwater balance records as the basin identifier. |
| [sym:gwflow_output_yr] | `bsn` | The basin name is written into yearly groundwater balance records to identify the simulated basin. |
| [sym:gwflow_output_aa] | `bsn` | The basin name appears in the average-annual groundwater summary headers and records. |
| [sym:hyd_read_connect] | `bsn_cc` | The gwflow control flag determines whether aquifer outflow is removed from the source totals while reading hydrologic connectivity. |
| [sym:aqu_cs_output] | `pco` | The aquifer constituent writer uses the print-control flags to decide whether daily, monthly, yearly, and average-annual constituent summaries are emitted and whether CSV duplicates are written. |
| [sym:aqu_pesticide_output] | `pco` | The aquifer pesticide writer uses the print-control flags to decide which interval outputs and CSV duplicates are written. |
| [sym:aqu_read] | `bsn_cc` | The routine contains an unreachable assignment to `bsn_cc%gwflow = 0` after an `exit`; in practice it does not modify the gwflow control flag. |
| [sym:aqu_salt_output] | `pco` | The aquifer salt writer uses the print-control flags to decide whether daily, monthly, yearly, and average-annual salt reports and CSV copies are written. |
| [sym:aquifer_output] | `pco` | The aquifer output writer uses the print-control flags to decide whether daily, monthly, yearly, and average-annual aquifer reports and CSV copies are written. |
| [sym:basin_aqu_pest_output] | `pco` | The basin aquifer pesticide writer uses the print-control flags to decide which interval outputs and CSV duplicates are written. |
| [sym:basin_aquifer_output] | `bsn`, `pco` | The basin name and basin area are used to form basin-scale weighted aquifer summaries, and the print-control flags decide which interval files and CSV copies are written. |
| [sym:basin_ch_pest_output] | `pco` | The basin/channel pesticide writer uses the print-control flags to decide which interval outputs and CSV duplicates are written. |
| [sym:basin_chanbud_output] | `pco`, `bsn` | The basin print-control flags decide whether basin channel sediment-budget output is written for each interval and whether CSV copies are emitted; the basin name labels every record. |
| [sym:basin_chanmorph_output] | `pco`, `bsn` | The basin print-control flags decide which channel-morphology intervals are written and whether CSV copies are emitted; the basin name labels every record. |
| [sym:basin_channel_output] | `pco`, `bsn` | The basin print-control flags decide whether basin channel output is written at daily, monthly, yearly, and average-annual intervals, and the basin name labels each record. |
| [sym:basin_ls_pest_output] | `pco` | The basin land-surface pesticide writer uses the print-control flags to decide which interval outputs and CSV duplicates are written. |
| [sym:basin_output] | `pco`, `bsn`, `ban_precip_aa` | The basin output writer uses print-control flags to gate each basin output block, writes the basin name on every record, and carries basin-average precipitation through the basin reporting path. |
| [sym:basin_print_codes_read] | `pco` | This parser populates the print-control structure that later output routines consult for all basin-level output families. |
| [sym:basin_read_cc] | `bsn_cc` | This reader loads the basin control-code structure from `codes.bsn` and checks the PET mode before advancing through `pet.cli`. |
| [sym:basin_read_objs] | `bsn`, `bsn_cc` | The basin object reader uses basin counts and the GWFLOW control flag to decide whether to adjust object totals and read the GWFLOW connectivity file. |
| [sym:basin_read_prm] | `bsn_prm` | This reader populates the basin parameter structure from `parameters.bsn` for later basin setup and process routines. |
| [sym:basin_recall_output] | `pco`, `bsn` | The basin recall writer uses the print-control flags to select daily, monthly, yearly, and average-annual recall outputs, and the basin name labels each record. |

## Lineage

`basin_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 24 non-merge commit(s) since, most recently `dfce092` (2026-06-02, "move carbon activation to cswat = 2, reserve 1 for C-FARM"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `basin_module.f90` are listed.

- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `f7e26d7` (2026-05-01) — Incremental improvements to pl_fert and pl_manure
- `7ff5029` (2026-04-02) — gwflow re-merge: output redesign - long format, print.prt integration, standardized output
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `basin_module` has no extracted module-level documentation comment.
- The reader table is representative rather than exhaustive; the full importer appendix contains the deterministic complete importer list.
- No git lineage commits were resolved for this source span, so lineage impacts are intentionally empty.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
