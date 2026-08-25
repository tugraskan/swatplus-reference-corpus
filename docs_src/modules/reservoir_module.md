---
kind: module
symbol: reservoir_module
title: reservoir_module
status: filled
source_hash: 0e49ac1707b9d2f0
version_label: SWAT+ 62.0.0
variables:
  reactw: mg pst |amount of pesticide in reach that is lost through reactions
  volatpst: mg pst |amount of pesticide lost from reach by volatilization
  setlpst: mg pst |amount of pesticide moving from water to sediment due to settling
  resuspst: mg pst |amount of pesticide moving from sediment to reach due to resuspension
  difus: mg pst |diffusion of pesticide from sediment to reach
  reactb: mg pst |amount of pesticide in sediment that is lost through reactions
  bury: mg pst |loss of pesticide from active sediment layer by burial
  res_ob: Allocatable reservoir object array of type reservoir. It stores per-reservoir identity,
    geometry, operating parameters, Hanazaki release memory, irrigation tracking, and aquatic
    mixing coefficients. It is allocated in res_allo, filled in res_objects and res_initial,
    updated by res_read, res_control, res_hydro, cal_parm_select, wallo_control, and read
    by output and routing routines.
  wet_ob: Allocatable wetland object array of type wetland. It stores per-HRU wetland geometry
    and spillway parameters used by wetland control, routing, and output routines. It is allocated
    in hru_allo, populated by wet_initial and hru_fr_change, and read by ch_rtday, ch_rtmusk,
    conditions, mgt_sched, and wetland-related control and output procedures.
  res_pest_d: Allocatable daily reservoir pesticide process array of type reservoir_pest_processes.
    It stores daily reservoir pesticide reaction, volatilization, settling, resuspension,
    diffusion, benthic reaction, and burial diagnostics for each reservoir. It is allocated
    in res_allo and updated by res_pest.
  res_pest_m: Allocatable monthly reservoir pesticide process array of type reservoir_pest_processes.
    It stores monthly reservoir pesticide process diagnostics for each reservoir. It is allocated
    in res_allo and populated by res_pest and output routines.
  res_pest_y: Allocatable yearly reservoir pesticide process array of type reservoir_pest_processes.
    It stores yearly reservoir pesticide process diagnostics for each reservoir. It is allocated
    in res_allo and populated by res_pest and output routines.
  res_pest_a: Allocatable average-annual reservoir pesticide process array of type reservoir_pest_processes.
    It stores average-annual reservoir pesticide process diagnostics for each reservoir. It
    is allocated in res_allo and populated by res_pest and output routines.
  wet_pest_d: Allocatable daily wetland pesticide process array of type reservoir_pest_processes.
    It stores daily wetland pesticide process diagnostics for each wetland/reservoir object.
    It is allocated in res_allo and updated by wetland pesticide processing.
  wet_pest_m: Allocatable monthly wetland pesticide process array of type reservoir_pest_processes.
    It stores monthly wetland pesticide process diagnostics for each wetland/reservoir object.
    It is allocated in res_allo and updated by wetland pesticide processing.
  wet_pest_y: Allocatable yearly wetland pesticide process array of type reservoir_pest_processes.
    It stores yearly wetland pesticide process diagnostics for each wetland/reservoir object.
    It is allocated in res_allo and updated by wetland pesticide processing.
  wet_pest_a: Allocatable average-annual wetland pesticide process array of type reservoir_pest_processes.
    It stores average-annual wetland pesticide process diagnostics for each wetland/reservoir
    object. It is allocated in res_allo and updated by wetland pesticide processing.
  res_hdr: Singleton res_header record holding the column labels for reservoir input/output
    headers. It is a public module-level header template used by reservoir output setup.
  res_hdr1: Singleton res_header1 record holding alternate reservoir output header labels.
    It is a public module-level header template used by reservoir output setup.
  res_hdr2: Singleton reservoir_hdr record holding reservoir water-body output header labels
    and units. It is a public module-level header template used by reservoir output setup.
  res_hdrbsn: Singleton res_headerbsn record holding basin-level reservoir output header labels.
    It is a public module-level header template used by basin reservoir output and related
    header writers.
  res_hdr_unt: Singleton res_header_unit record holding unit-level reservoir output header
    labels. It is a public module-level header template used by unit reservoir output writers.
  res_hdr_unt1: Singleton res_header_unit1 record holding alternate unit-level reservoir output
    header labels. It is a public module-level header template used by unit reservoir output
    writers.
  res_hdr_unt2: Singleton res_header_unit2 record holding unit-level reservoir loss header
    labels. It is a public module-level header template used by unit reservoir output writers.
  res_hdr_untbsn: Singleton res_header_unitbsn record holding basin-level unit reservoir output
    header labels. It is a public module-level header template used by unit reservoir output
    writers.
type_components:
  reservoir:
    name: Reservoir name string; initialized to 'default' and used as the human-readable label
      for the reservoir object.
    ob: Global object number for the reservoir object, or HRU number when the record is used
      for an HRU-linked storage object.
    props: Pointer to the reservoir property record in res_dat.
    wallo_call: Flag showing whether wallo has already called this reservoir on the current
      day.
    iweir: Weir ID used to select the active reservoir/wetland weir definition.
    rel_tbl: Single-character release-table selector; 'd' means decision table and 'c' means
      conditions table.
    psa: ha | reservoir surface area when the reservoir is filled to the principal spillway.
    pvol: ha-m | volume needed to fill the reservoir to the principal spillway, read in ha-m
      and converted to m^3.
    esa: ha | reservoir surface area when the reservoir is filled to the emergency spillway.
    evol: ha-m | volume needed to fill the reservoir to the emergency spillway, read in ha-m
      and converted to m^3.
    br1: Coefficient used in the reservoir area-volume relation; estimated by the model when
      zero.
    br2: Volume-depth or volume-surface coefficient used in reservoir geometry calculations.
    depth: m | average water depth for the reservoir object.
    weir_hgt: m | height of the weir above the reservoir bottom.
    weir_wid: m | width of the weir opening above the reservoir bottom.
    seci: m | Secchi depth.
    prev_flo: m3 | previous day's flow used to smooth outflows.
    lag_up: Lag parameter that limits sudden increases in outflow.
    lag_down: Lag parameter that limits sudden decreases in outflow.
    kd: Allocatable array of aquatic mixing velocity values used in pesticide transport calculations.
    aq_mix: m/day | allocatable array of aquatic mixing velocity values used in pesticide
      transport calculations.
    i_mon_past: Allocatable monthly mean inflow memory used by the Hanazaki-style release
      method.
    i_mean: m3 | annual mean inflow computed from the rolling inflow memory.
    s_ini: m3 | storage at the beginning of the operational year.
    n_memory: Number of years stored in the inflow memory window.
    daily_inflow_array: Allocatable daily inflow buffer used to accumulate the current month's
      inflow history.
    c_ratio: Capacity ratio used by the Hanazaki-style release method.
    d_mean: m3 | annual mean irrigation demand.
    d_mon_past: Allocatable monthly mean irrigation demand memory used by the Hanazaki-style
      irrigation logic.
    daily_demand_array: Allocatable daily irrigation demand buffer used to accumulate the
      current month's demand history.
    d_irrig_day: m3 | daily irrigation demand.
    irrig_track: Counter used to track irrigation-demand updates for the reservoir on a given
      day.
  wetland:
    iweir: Weir ID used to select the active weir definition.
    psa: ha | reservoir surface area when the wetland is filled to the principal spillway.
    pvol: m^3 | volume needed to fill the wetland to the principal spillway, converted from
      ha-m.
    esa: ha | reservoir surface area when the wetland is filled to the emergency spillway.
    evol: m^3 | volume needed to fill the wetland to the emergency spillway, converted from
      ha-m.
    area_ha: ha | reservoir surface area.
    depth: m | average water depth.
    weir_hgt: m | height of the weir above the bottom.
    weir_wid: m | width of the weir.
    seci: m | Secchi depth.
  reservoir_pest_processes:
    react: kg | pesticide lost through reactions in the water layer.
    volat: kg | pesticide lost through volatilization.
    settle: kg | pesticide settling to the benthic layer.
    resus: kg | pesticide resuspended into lake or reservoir water.
    difus: kg | pesticide diffusing from benthic sediment to water.
    react_ben: kg | pesticide lost from the benthic layer by reactions.
    bury: Kg | pesticide lost from the benthic layer by burial.
  res_header:
    day: First column header for reservoir input/output date records.
    mo: Month header field for reservoir output.
    day_mo: Day-of-month header field for reservoir output.
    yrc: Year header field for reservoir output.
    j: Reservoir number header field.
    id: GIS identifier header field.
    name: Reservoir name header field.
    flo: ha-m | volume of water.
    sed: metric tons | sediment.
    orgn: kg N | organic N.
    sedp: kg P | organic P.
    no3: kg N | NO3-N.
    solp: kg P | mineral (soluble) P.
    chla: kg | chlorophyll-a.
    nh3: kg N | NH3.
    no2: kg N | NO2.
    cbod: kg | carbonaceous biological oxygen demand.
    dox: kg | dissolved oxygen.
    san: tons | detached sand.
    sil: tons | detached silt.
    cla: tons | detached clay.
    sag: tons | detached small ag.
    lag: tons | detached large ag.
    grv: tons | gravel.
    temp: deg c | temperature.
  res_header1:
    flo: ha-m | volume of water.
    sed: metric tons | sediment.
    orgn: kg N | organic N.
    sedp: kg P | organic P.
    no3: kg N | NO3-N.
    solp: kg P | mineral (soluble) P.
    chla: kg | chlorophyll-a.
    nh3: kg N | NH3.
    no2: kg N | NO2.
    cbod: kg | carbonaceous biological oxygen demand.
    dox: kg | dissolved oxygen.
    san: tons | detached sand.
    sil: tons | detached silt.
    cla: tons | detached clay.
    sag: tons | detached small ag.
    lag: tons | detached large ag.
    grv: tons | gravel.
    temp: deg c | temperature.
  reservoir_hdr:
    area_ha: Surface area field for the reservoir output-loss header.
    evap: mm | evaporation from reservoir surface area.
    seep: mm | seepage from reservoir bottom.
    sed_setl: t | sediment settling.
    seci: m | Secchi depth.
    solp_loss: kg | soluble phosphorus loss.
    sedp_loss: kg | sediment-attached phosphorus loss.
    orgn_loss: kg | organic nitrogen loss.
    no3_loss: kg | nitrate loss.
    nh3_loss: kg | ammonium nitrogen loss.
    no2_loss: kg | nitrite loss.
  res_headerbsn:
    flo: ha-m | volume of water.
    sed: metric tons | sediment.
    orgn: kg N | organic N.
    sedp: kg P | organic P.
    no3: kg N | NO3-N.
    solp: kg P | mineral (soluble) P.
    chla: kg | chlorophyll-a.
    nh3: kg N | NH3.
    no2: kg N | NO2.
    cbod: kg | carbonaceous biological oxygen demand.
    dox: kg | dissolved oxygen.
    san: tons | detached sand.
    sil: tons | detached silt.
    cla: tons | detached clay.
    sag: tons | detached small ag.
    lag: tons | detached large ag.
    grv: tons | gravel.
    temp: deg c | temperature.
  res_header_unit:
    day: Date field for unit-level reservoir output; the source comment notes uncertainty
      about res_out and hy_output alignment.
    mo: Month field for unit-level reservoir output.
    day_mo: Day-of-month field for unit-level reservoir output.
    yrc: Year field for unit-level reservoir output.
    j: Reservoir number field.
    id: GIS identifier field.
    name: Reservoir name field.
    flo: ha-m | volume of water.
    sed: metric tons | sediment.
    orgn: kg N | organic N.
    sedp: kg P | organic P.
    no3: kg N | NO3-N.
    solp: kg P | mineral (soluble) P.
    chla: kg | chlorophyll-a.
    nh3: kg N | NH3.
    no2: kg N | NO2.
    cbod: kg | carbonaceous biological oxygen demand.
    dox: kg | dissolved oxygen.
    san: tons | detached sand.
    sil: tons | detached silt.
    cla: tons | detached clay.
    sag: tons | detached small ag.
    lag: tons | detached large ag.
    grv: tons | gravel.
    temp: deg c | temperature.
  res_header_unit1:
    flo: ha-m | volume of water.
    sed: metric tons | sediment.
    orgn: kg N | organic N.
    sedp: kg P | organic P.
    no3: kg N | NO3-N.
    solp: kg P | mineral (soluble) P.
    chla: kg | chlorophyll-a.
    nh3: kg N | NH3.
    no2: kg N | NO2.
    cbod: kg | carbonaceous biological oxygen demand.
    dox: kg | dissolved oxygen.
    san: tons | detached sand.
    sil: tons | detached silt.
    cla: tons | detached clay.
    sag: tons | detached small ag.
    lag: tons | detached large ag.
    grv: tons | gravel.
    temp: deg c | temperature.
  res_header_unit2:
    area_ha: last part of units
    evap: mm | evaporation from reservoir surface area.
    seep: mm | seepage from reservoir bottom.
    sed_setl: t | sediment settling.
    seci: m | Secchi depth.
    solp_loss: kg | soluble phosphorus loss.
    sedp_loss: kg | sediment attached phosphorus loss.
    orgn_loss: kg | organic nitrogen loss.
    no3_loss: kg | nitrate loss.
    nh3_loss: kg | ammonium nitrogen loss.
    no2_loss: kg | nitrite loss.
  res_header_unitbsn:
    flo: m^3 | volume of water.
    sed: metric tons | sediment.
    orgn: kg N | organic N.
    sedp: kg P | organic P.
    no3: kg N | NO3-N.
    solp: kg P | mineral (soluble) P.
    chla: kg | chlorophyll-a.
    nh3: kg N | NH3.
    no2: kg N | NO2.
    cbod: kg | carbonaceous biological oxygen demand.
    dox: kg | dissolved oxygen.
    san: tons | detached sand.
    sil: tons | detached silt.
    cla: tons | detached clay.
    sag: tons | detached small ag.
    lag: tons | detached large ag.
    grv: tons | gravel.
    temp: deg c | temperature.
type_summaries:
  reservoir: Per-reservoir state record holding object identity, geometry, operational release
    metadata, irrigation tracking, and rolling inflow/demand memory used by reservoir routing
    and control.
  wetland: Per-HRU wetland geometry record holding spillway and surface-area data used by
    wetland routing, release, and flood storage logic.
  reservoir_pest_processes: Per-reservoir or per-wetland pesticide process record holding
    daily, monthly, yearly, or average-annual diagnostics for pesticide mass transfers.
  res_header: Reservoir header template for daily or standard reservoir input/output records.
  res_header1: Alternate reservoir output header template used for reservoir output formatting.
  reservoir_hdr: Reservoir output-loss header template used for reservoir water-body diagnostics.
  res_headerbsn: Basin-level reservoir header template used for basin reservoir output files.
  res_header_unit: Unit-level reservoir header template used for reservoir output files written
    in unit-based reports.
  res_header_unit1: Alternate unit-level reservoir header template used for unit-based reservoir
    output files.
  res_header_unit2: Unit-level reservoir loss header template used for unit-based reservoir
    output files.
  res_header_unitbsn: Basin-level unit reservoir header template used for basin reservoir
    output files in unit form.
---

<!-- facts:header -->

reservoir_module owns the shared reservoir and wetland state for SWAT+: object records, pesticide process accumulators, and the header records used by reservoir/wetland output. It is initialized by reservoir and wetland setup routines such as res_objects, res_allo, res_initial, wet_initial, and hru_allo, then read and updated by reservoir control, wetland control, calibration, routing, and output procedures throughout the run.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it does not contain procedures. Its variables are populated by separate setup routines such as res_objects, res_allo, res_initial, wet_initial, and hru_allo, then consumed by reservoir, wetland, routing, calibration, and output code.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `wet_ob, res_ob` | Uses wetland depth and reservoir irrigation tracking while applying irrigation and ponding actions; updates wetland depth and reservoir demand tracking based on action definitions. |
| [sym:basin_reservoir_output] | `unit_2100, unit_2104, unit_2101, unit_2105, unit_2102, unit_2106, unit_2103, unit_2107` | `res_ob, res_in_d, res_out_d` | Reads per-reservoir hydrologic totals from the shared reservoir arrays and aggregates them into basin-level summaries. |
| [sym:cal_parm_select] | `calibration selection input managed by cal_parm_select` | `res_ob` | Applies calibration changes to reservoir geometry and operational parameters in the shared reservoir object array. |
| [sym:caltsoft_hyd] | `unit_4304` | `none extracted` | Imported by the calibration soft-hydrology routine, but the provided context does not resolve a specific reservoir-module symbol in the extracted lines. |
| [sym:command] | `unit_out_hyd_sep` | `res_ob` | Resets reservoir wallo-call state at the start of the daily control loop and dispatches reservoir control when water-allocation transfers reach a reservoir. |
| [sym:header_const] | `unit_6080, unit_6082, unit_6084, unit_6086, unit_6021, unit_6022, unit_6023, unit_6024, unit_6025, unit_6026, unit_6027, unit_6028, unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067, unit_6030, unit_6031, unit_6032, unit_6033, unit_6034, unit_6035, unit_6036, unit_6037, unit_6040, unit_6041, unit_6042, unit_6043, unit_6044, unit_6045, unit_6046, unit_6047, unit_6070, unit_6071, unit_6072, unit_6073, unit_6074, unit_6075, unit_6076, unit_6077, unit_6090, unit_6091, unit_6092, unit_6093, unit_6094, unit_6095, unit_6096, unit_6097` | `res_hdr, res_hdr1, res_hdr2, res_hdrbsn, res_hdr_unt, res_hdr_unt1, res_hdr_unt2, res_hdr_untbsn, wet_ob` | Writes reservoir and wetland constituent header records into the configured output files before simulation output begins. |
| [sym:header_path] | `unit_2790, unit_9000, unit_2794, unit_2791, unit_2795, unit_2792, unit_2796, unit_2793, unit_2797` | `none extracted` | Imported as a dependency only; no reservoir-module symbol is resolved in the extracted lines. |
| [sym:header_pest] | `unit_2800, unit_9000, unit_2804, unit_2801, unit_2805, unit_2802, unit_2806, unit_2803, unit_2807, unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815, unit_2816, unit_2820, unit_2817, unit_2821, unit_2818, unit_2822, unit_2819, unit_2823, unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007, unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015, unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839, unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855, unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `none extracted` | Imported as a dependency only; no reservoir-module symbol is resolved in the extracted lines. |
| [sym:header_reservoir] | `unit_2540, unit_9000, unit_2544, unit_2541, unit_2545, unit_2542, unit_2546, unit_2543, unit_2547` | `none extracted` | Imported as a dependency only; no reservoir-module symbol is resolved in the extracted lines. |
| [sym:header_salt] | `unit_5080, unit_5082, unit_5084, unit_5086, unit_5021, unit_5022, unit_5023, unit_5024, unit_5025, unit_5026, unit_5027, unit_5028, unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067, unit_5030, unit_5031, unit_5032, unit_5033, unit_5034, unit_5035, unit_5036, unit_5037, unit_5040, unit_5041, unit_5042, unit_5043, unit_5044, unit_5045, unit_5046, unit_5047, unit_5070, unit_5071, unit_5072, unit_5073, unit_5074, unit_5075, unit_5076, unit_5077, unit_5090, unit_5091, unit_5092, unit_5093, unit_5094, unit_5095, unit_5096, unit_5097` | `res_hdr, res_hdr1, res_hdr2, res_hdrbsn, res_hdr_unt, res_hdr_unt1, res_hdr_unt2, res_hdr_untbsn, wet_ob` | Writes reservoir and wetland salt header records and the salt column definitions into the configured output files. |
| [sym:header_wetland] | `unit_2548, unit_9000, unit_2552, unit_2549, unit_2553, unit_2550, unit_2554, unit_2551, unit_2555` | `none extracted` | Imported as a dependency only; no reservoir-module symbol is resolved in the extracted lines. |
| [sym:header_write] | `unit_6000, unit_9000, hru-out.cal, hru-new.cal, hydrology-cal.hyd, unit_2090, unit_2094, unit_2091, unit_2095, unit_2092, unit_2096, unit_2093, unit_2097, unit_2100, unit_2104, unit_2101, unit_2105, unit_2102, unit_2106, unit_2103, unit_2107, unit_4600, unit_4604, unit_4601, unit_4605, unit_4602, unit_4606, unit_4603, unit_4607, unit_2110, unit_2114, unit_2111, unit_2115, unit_2112, unit_2116, unit_2113, unit_2117, unit_4900, unit_4904, unit_4901, unit_4905, unit_4902, unit_4906, unit_4903, unit_4907, unit_2120, unit_2124, unit_2121, unit_2125, unit_2122, unit_2126, unit_2123, unit_2127, unit_2128, unit_2132, unit_2129, unit_2133, unit_2130, unit_2134, unit_2131, unit_2135, unit_4500, unit_4504, unit_4501, unit_4505, unit_4502, unit_4506, unit_4503, unit_4507, unit_2600, unit_2604, unit_2601, unit_2605, unit_2602, unit_2606, unit_2603, unit_2607` | `res_hdr, res_hdrbsn, res_hdr_unt, res_hdr_untbsn` | Writes basin reservoir headers and other configured output headers during model startup. |
| [sym:res_read_elements] | `res_catunit.def, res_reg.def, res_catunit.ele` | `none extracted` | Reservoir-specific setup routine that belongs to the reservoir subsystem; the extracted lines do not name a reservoir-module symbol. |
| [sym:reservoir_output] | `unit_2540, unit_2544, unit_2541, unit_2545, unit_2542, unit_2546, unit_2543, unit_2547` | `res_ob, res_in_d, res_out_d, res_in_m, res_out_m, res_in_y, res_out_y, res_in_a, res_out_a, res_wat_d, res_wat_m, res_wat_y, res_wat_a` | Reads reservoir state and prints the daily, monthly, yearly, and average-annual reservoir summaries. |
| [sym:wet_read] | `wetland.wet` | `none extracted` | Wetland database loader; the extracted lines do not name a reservoir-module symbol. |
| [sym:wet_read_salt_cs] | `wetland.wet_cs` | `wet_ob` | Resolves wetland salt and constituent lookup references into the wetland object array. |

## Key Consumers

The module is used by reservoir, wetland, routing, calibration, management, and output routines. The main consumers update reservoir or wetland state, while the header writers and output routines use the shared header templates and object arrays to format reports consistently.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_parm_select] | reservoir_module | Allows calibration updates to write directly into reservoir geometry and release parameters stored in res_ob, so later reservoir control uses the adjusted values. |
| [sym:header_const] | reservoir_module | Provides the reservoir and wetland header records that header_const writes into the reservoir/wetland constituent output files. |
| [sym:header_salt] | reservoir_module | Provides the reservoir and wetland header records that header_salt writes into the reservoir/wetland salt output files. |
| [sym:hru_fr_change] | reservoir_module | Lets hru_fr_change rewrite wetland volume and surface-area geometry in wet_ob after HRU fraction changes, so later reservoir calculations see the updated storage geometry. |
| [sym:res_initial] | reservoir_module | Provides the reservoir object array that res_initial fills with object ids, geometry, spillway height, memory arrays, and mixing coefficients before simulation starts. |
| [sym:res_read] | reservoir_module | Provides the per-reservoir object records that res_read updates with release-table selection and other resolved reservoir setup data. |
| [sym:res_read_salt_cs] | reservoir_module | Provides the shared reservoir records that receive parsed salt and constituent lookup indexes during reservoir setup. |
| [sym:wallo_control] | reservoir_module | Allows water-allocation transfers to update reservoir storage and then route through res_control when a reservoir receives transferred water. |
| [sym:wet_read_salt_cs] | reservoir_module | Provides the wetland reservoir records that receive resolved salt and constituent indices during wetland setup. |
| [sym:basin_reservoir_output] | reservoir_module | Supplies the per-reservoir hydrologic totals that basin_reservoir_output aggregates into basin-wide reservoir summaries. |
| [sym:header_path] | reservoir_module | Imported in the routine scope, but no reservoir-module symbol is resolved in the provided source span. |
| [sym:header_pest] | reservoir_module | Supports reservoir pesticide output setup, but the extracted source span does not show a specific module symbol use. |
| [sym:header_reservoir] | reservoir_module | Imported for reservoir-output setup context, though no specific reservoir_module symbol is resolved in the extracted span. |
| [sym:header_wetland] | reservoir_module | Imported for the reservoir/wetland output family, though no specific reservoir_module symbol is resolved in the extracted span. |
| [sym:header_write] | reservoir_module | Provides the reservoir header types needed when header_write opens the basin reservoir output files and writes their column labels. |
| [sym:res_read_elements] | reservoir_module | Marks the routine as part of reservoir setup so reservoir-related allocation and membership lists can be prepared before later processing. |
| [sym:reservoir_output] | reservoir_module | Provides the reservoir state and object numbering used to print daily, monthly, yearly, and average-annual reservoir summaries. |
| [sym:wet_read] | reservoir_module | Marks the wetland database loader as part of the reservoir/wetland subsystem, which later routines use when linking wetlands to model objects. |
| [sym:wetland_output] | reservoir_module | Supports the wetland output family that prints wetland/reservoir summaries using the shared reservoir-module state. |
| [sym:cal_conditions] | reservoir_module | Provides reservoir principal-spillway volume used by the res_pvol calibration range check. |
| [sym:ch_rtday] | reservoir_module | Provides wetland capacity data through wet_ob so the routing routine can transfer excess channel flow into connected wetland storage. |
| [sym:ch_rtmusk] | reservoir_module | Provides wetland emergency-spillway capacity used when building wetland storage for the daily balance check. |
| [sym:conditions] | reservoir_module | Provides reservoir and wetland storage state used by decision-table conditions for release, irrigation, and wetland actions. |
| [sym:hru_allo] | reservoir_module | Provides the wetland object array that hru_allo allocates alongside the HRU and wetland bookkeeping arrays. |

## Lineage

`reservoir_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `reservoir_module.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `d3c291b` (2026-01-31) — integrate new reservoir routines
- `645ac00` (2025-12-11) — merge rice paddy management code
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module has no extracted module-level documentation comment.
- Lineage evidence resolved no commits for this source span.
- Reader table is representative of module imports and setup paths, not an exhaustive initialization map.
- Completed procedure overlay evidence was used to tighten used_by effects for reservoir and wetland consumers.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
