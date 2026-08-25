---
kind: module
symbol: plant_data_module
title: plant_data_module
status: filled
source_hash: 9be752cd89e4aff4
version_label: SWAT+ 62.0.0
variables:
  plts_bsn: Allocatable basin-wide list of simulated plant names. It is public module state
    and is populated by plant initialization and time-control setup code that builds the basin
    crop list; downstream routines use it for basin crop-yield summaries and plant-name lookups.
  pl_class: Allocatable basin-wide list of plant class labels such as row crop, tree, grass,
    and perennial. It is shared state used by calibration and plant-lookup logic to filter
    or classify plants.
  photo_degrade_factor: Real basin-scale coefficient, initialized to .01, that reduces surface
    residue by photo degradation. It is read from `carbon.bsn` by `carbon_bsn_read` and can
    also be adjusted by `cal_parm_select`; residue/carbon routines use it when computing surface-residue
    losses.
  cswat_1_part_fracs: Allocatable array of `lignin_derived_partition_fracs` records. It holds
    the derived above-ground and below-ground metabolic/structural/lignin partition fractions
    for each plant entry, loaded by `plant_parm_read` from `plants.plt` and then consumed
    by residue decomposition and transfer routines such as `cbn_rsd_decomp`, `cbn_rsd_transfer`,
    and `cbn_surfrsd_decomp`.
  pldb: Allocatable plant species database array of `plant_db` records. It stores the raw
    plant parameters loaded from `plants.plt` by `plant_parm_read`, can be adjusted by `cal_parm_select`,
    and is read throughout growth, dormancy, ET, harvest, residue, and management routines.
  pl_db: Pointer alias for the current `plant_db` record. It provides convenient access to
    the active plant database entry without copying data, and is used by plant-growth routines
    when stepping through the active plant species.
  plcp: Allocatable derived plant-curve coefficient array of `plant_cp` records. It stores
    curve and stress coefficients computed from `pldb` by `plantparm_init`, and downstream
    routines read it instead of recalculating the coefficients.
  pl_cp: Pointer alias for the current `plant_cp` record. It is a convenience handle for the
    active plant coefficient record used by growth and ET calculations.
  pcomdb: Allocatable plant community database array of `plant_community_db` records. It is
    populated by `readpcom` and `plant_init` and stores each community's name, plant count,
    rotation year start, and per-plant initialization records; management, landuse, and initialization
    routines resolve community names through this array.
  transpl: Allocatable transplant database array of `plant_transplant_db` records. It is populated
    by `plant_transplant_read` from `transplant.plt` and then used by management code such
    as `dtbl_lum_read`, `mgt_sched`, and `mgt_transplant` to apply transplant settings.
type_components:
  residue_partition_fracs:
    meta_frac: fraction of residue mass treated as metabolic material; source comment says
      it reads `plants.plt` avg_lig_frac, though the in-code note warns the names are misleading
      and the carbon model uses the values under different semantic labels.
    str_frac: fraction of residue mass treated as structural material; source comment says
      it reads `plants.plt` ab_lig_frac and is used as above-ground lignin.
    lig_frac: fraction of residue mass treated as lignin material; source comment says it
      reads `plants.plt` bg_lig_frac and is used as below-ground lignin.
  lignin_derived_partition_fracs:
    meta_frac_abg: fraction of above-ground biomass that is metabolic.
    str_frac_abg: fraction of above-ground biomass that is structural.
    lig_frac_abg: fraction of above-ground biomass that is lignin.
    meta_frac_blg: fraction of below-ground biomass that is metabolic.
    str_frac_blg: fraction of below-ground biomass that is structural.
    lig_frac_blg: fraction of below-ground biomass that is lignin.
  plant_db:
    plantnm: crop name
    typ: plant category
    trig: phenology trigger; values include warm_annual, cold_annual, warm_annual_tuber, cold_annual_tuber,
      and perennial
    nfix_co: nitrogen fixation coefficient (0.5 legume; 0 non-legume); values may be keyed
      to moisture or temperature growth triggers
    days_mat: days to maturity; if zero, use heat units for the entire growing season
    bio_e: biomass-energy ratio in kg/ha per MJ/m**2
    hvsti: 'harvest index: crop yield divided by aboveground biomass'
    blai: maximum potential leaf area index
    frgrw1: fraction of the growing season corresponding to the first optimal LAI curve point
    laimx1: fraction of max LAI at the first optimal LAI curve point
    frgrw2: fraction of the growing season corresponding to the second optimal LAI curve point
    laimx2: fraction of max LAI at the second optimal LAI curve point
    dlai: fraction of growing season when leaf area declines
    dlai_rate: exponent governing LAI decline rate
    chtmx: maximum canopy height in m
    rdmx: maximum root depth in m
    t_opt: optimal temperature for plant growth in deg C
    t_base: minimum temperature for plant growth in deg C
    cnyld: fraction of nitrogen in yield, kg N/kg yld
    cpyld: fraction of phosphorus in yield, kg P/kg yld
    pltnfr1: 'nitrogen uptake parameter #1, kg N/kg biomass'
    pltnfr2: 'nitrogen uptake parameter #2, kg N/kg biomass'
    pltnfr3: 'nitrogen uptake parameter #3, kg N/kg biomass'
    pltpfr1: 'phosphorus uptake parameter #1, kg P/kg biomass'
    pltpfr2: 'phosphorus uptake parameter #2, kg P/kg biomass'
    pltpfr3: 'phosphorus uptake parameter #3, kg P/kg biomass'
    wsyf: harvest index lower bound used by grain-harvest logic
    usle_c: minimum value of the USLE C factor for water erosion
    gsi: maximum stomatal conductance, m/s
    vpdfr: vapor pressure deficit at which GMAXFR is valid, kPa
    gmaxfr: fraction of max stomatal conductance achieved at VPDFR
    wavp: rate of decline in radiation use efficiency
    co2hi: CO2 concentration corresponding to the second point on the radiation use efficiency
      curve, uL CO2/L air
    bioehi: biomass-energy ratio in elevated CO2 conditions
    rsdco_pl: plant residue decomposition coefficient
    alai_min: minimum LAI during winter dormant period, m**2/m**2
    laixco_tree: coefficient to estimate max LAI during tree growth
    mat_yrs: years to maturity
    bmx_peren: maximum biomass for forest, metric tons/ha
    ext_coef: light extinction coefficient
    leaf_tov_min: perennial leaf turnover rate with minimum stress, months
    leaf_tov_max: perennial leaf turnover rate with maximum stress, months
    bm_dieoff: fraction of aboveground biomass that dies off at dormancy
    rsr1: initial root-to-shoot ratio at the beginning of the growing season
    rsr2: root-to-shoot ratio at the end of the growing season
    pop1: plant population at the first point on the population-LAI curve, plants/m^2
    frlai1: fraction of max LAI at the first point on the population-LAI curve
    pop2: plant population at the second point on the population-LAI curve, plants/m^2
    frlai2: fraction of max LAI at the second point on the population-LAI curve
    frsw_gro: 30-day sum of P-PET to initiate tropical plant growth during monsoon season
    aeration: aeration stress factor
    rsd_pctcov: residue factor for percent cover equation
    rsd_covfac: residue factor for surface cover (C factor) equation
    res_part_fracs: embedded `residue_partition_fracs` record
  plant_cp:
    popsc1: first population scaling coefficient
    popsc2: second population scaling coefficient
    leaf1: first shape parameter for leaf area
    leaf2: second shape parameter for leaf area
    ruc1: first shape parameter for radiation use efficiency
    ruc2: second shape parameter for radiation use efficiency
    nup1: first shape parameter for plant N uptake
    nup2: second shape parameter for plant N uptake
    pup1: first shape parameter for plant P uptake
    pup2: second shape parameter for plant P uptake
    gmaxfr: fraction of max stomatal conductance achieved at the specified VPD
    vpdfr: vapor pressure deficit at which GMAXFR is valid, kPa
    cvm: fraction of the maximum LAI corresponding to the second point on the stomatal conductance/LAI
      curve
    vpd2: vapor pressure deficit corresponding to the second point on the stomatal conductance
      curve, kPa
  plant_init_db:
    cpnm: plant/community name used to match the active plant record
    db_num: plant object index into the master plant database
    igro: land cover status flag; `n` means no land cover growing, `y` means land cover growing
    lai: leaf area index, m**2/m**2
    bioms: land cover/crop biomass, kg/ha
    phuacc: fraction of plant heat units accumulated
    pop: plant population
    fr_yrmat: fraction of current year of growth to years to maturity
    rsdin: initial residue cover, kg/ha
  plant_community_db:
    name: plant community name
    plants_com: number of plants in the community
    rot_yr_ini: initial rotation year
    pl: allocatable array of `plant_init_db` records for the community's plants
  plant_transplant_db:
    name: transplant name
    lai: leaf area index, m**2/m**2
    bioms: land cover/crop biomass, kg/ha
    phuacc: fraction of plant heat units accumulated
    fr_yrmat: fraction of current year of growth to years to maturity
    pop: plant population, plants/m^2
type_summaries:
  residue_partition_fracs: Per-plant residue lignin partition fractions as stored in the raw
    plant database record.
  lignin_derived_partition_fracs: Derived above-ground and below-ground partition fractions
    used by the carbon/residue routines.
  plant_db: Master plant species database record containing crop category, phenology, growth,
    stress, harvest, residue, and root-depth parameters.
  plant_cp: Derived plant curve coefficients used by growth, uptake, and stomatal-response
    equations.
  plant_init_db: Initialization record for one plant within a plant community.
  plant_community_db: Plant community record containing the community name, size, rotation
    start year, and per-plant initialization list.
  plant_transplant_db: Transplant record containing initial growth state and population settings
    for a named transplant option.
---

<!-- facts:header -->

`plant_data_module` owns the shared plant reference data used across SWAT+ plant growth, residue/carbon, management, calibration, and reporting code. It declares the basin plant name/class lists, plant species database, plant curve-parameter database, plant community database, transplant database, and the lignin-based partition-fraction types that downstream routines use to initialize, crosswalk, and update plant state.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

`plant_data_module` is primarily a declaration container for shared public plant state and type definitions. The module itself contains no procedures; its allocatable arrays and pointer aliases are populated by reader and initialization routines such as `plant_parm_read`, `plantparm_init`, `readpcom`, `plant_transplant_read`, `plant_init`, and `mgt_transplant`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `pcomdb, pldb, plts_bsn` | Uses plant community and plant database lookups when executing plant and harvest actions and when writing management output. |
| [sym:aqu_pesticide_output] | `unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015` | `none resolved` | Imports the module as a compile-time dependency; no direct plant-data symbol use was resolved in the supplied source span. |
| [sym:basin_aqu_pest_output] | `unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007` | `none resolved` | Imports the module as a compile-time dependency; no direct plant-data symbol use was resolved in the supplied source span. |
| [sym:basin_ch_pest_output] | `unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839` | `none resolved` | Imports the module as a compile-time dependency; no direct plant-data symbol use was resolved in the supplied source span. |
| [sym:basin_ls_pest_output] | `unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `none resolved` | Imports the module as a compile-time dependency; no direct plant-data symbol use was resolved in the supplied source span. |
| [sym:basin_res_pest_output] | `unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855` | `none resolved` | Imports the module as a compile-time dependency; no direct plant-data symbol use was resolved in the supplied source span. |
| [sym:cal_allo_init] | `derived model state` | `pcomdb` | Uses `pcomdb(icom)%plants_com` to size the per-HRU plant allocation arrays for calibration copies. |
| [sym:cal_parm_select] | `derived model state` | `pldb, photo_degrade_factor` | Adjusts selected plant and basin carbon parameters, including `pldb(ielem)%usle_c` and `photo_degrade_factor`. |
| [sym:calsoft_read_codes] | `codes.sft` | `none resolved` | Imports the module as a compile-time dependency; no direct plant-data symbol use was resolved in the supplied source span. |
| [sym:carbon_bsn_read] | `unit_*, unit_9001, carbon.bsn, _lyr.bsn` | `photo_degrade_factor` | Reads the basin-wide photo-degradation residue scalar from `carbon.bsn` into module state. |
| [sym:ch_cs_output] | `unit_6030, unit_6031, unit_6032, unit_6033, unit_6034, unit_6035, unit_6036, unit_6037` | `none resolved` | Imports the module as a compile-time dependency; no direct plant-data symbol use was resolved in the supplied source span. |
| [sym:ch_salt_output] | `unit_5030, unit_5031, unit_5032, unit_5033, unit_5034, unit_5035, unit_5036, unit_5037` | `none resolved` | Imports the module as a compile-time dependency; no direct plant-data symbol use was resolved in the supplied source span. |

## Key Consumers

Most importers use `plant_data_module` to look up plant species, plant-community, or transplant parameters during initialization, management, and daily growth control. A second group imports it for reporting or calibration support, often because those routines need plant names, plant categories, or plant-parameter state already populated elsewhere.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_allo_init] | plant_data_module | `plant_data_module` supplies `pcomdb`, which tells the routine how many plants belong to each plant community. That count drives the allocation size for `pcom_init` plant arrays and `pl_mass_init` plant mass arrays. |
| [sym:cal_parm_select] | plant_data_module | Updates selected plant database entries such as `pldb(ielem)%usle_c` and basin photo-degradation control so later erosion and carbon routines see the calibrated plant parameters. |
| [sym:carbon_bsn_read] | plant_data_module | Initializes `photo_degrade_factor` from `carbon.bsn`, giving residue-photo degradation routines the basin-wide scalar they apply to surface residue. |
| [sym:dtbl_lum_read] | plant_data_module | Resolves transplant names from `transpl` into management action indices so later plant actions can call the correct transplant record. |
| [sym:hru_lte_control] | plant_data_module | Supplies plant species parameters for growth, stress, and output labeling while the LTE controller computes daily plant development. |
| [sym:hru_lte_read] | plant_data_module | Provides the plant database used to match LTE plant names and to derive heat-unit accumulation limits from plant temperature and type parameters. |
| [sym:hru_output] | plant_data_module | Provides the plant-community and plant-name context used when the HRU output routine reports crop yield by plant. |
| [sym:landuse_read] | plant_data_module | Supplies `pcomdb`, which lets landuse records translate plant-community names into numeric community indices. |
| [sym:plant_all_init] | plant_data_module | Provides the basin-wide plant name list that this routine assembles from HRU communities. |
| [sym:plant_init] | plant_data_module | Supplies the plant community, plant species, and plant parameter records used to initialize HRU plant state and copy default growth settings into the simulation. |
| [sym:plant_parm_read] | plant_data_module | Fills `pldb`, `pl_class`, and `cswat_1_part_fracs` from `plants.plt`, establishing the shared plant parameter state used by growth and residue/carbon routines. |
| [sym:plant_transplant_read] | plant_data_module | Allocates and fills the shared transplant database `transpl` from `transplant.plt` for later transplant and management operations. |
| [sym:plantparm_init] | plant_data_module | Converts raw `pldb` entries into derived plant-curve coefficients stored in `plcp` for downstream growth and uptake calculations. |
| [sym:read_mgtops] | plant_data_module | Uses plant-community, plant, and transplant names to match management actions to the correct numeric database references. |
| [sym:readpcom] | plant_data_module | Allocates and fills `pcomdb`, resolving each community plant name to the corresponding master plant database index in `pldb`. |
| [sym:aqu_pesticide_output] | plant_data_module | No direct plant-data symbol use was extracted; the import remains a compilation dependency in the pesticide-output subsystem. |
| [sym:basin_aqu_pest_output] | plant_data_module | No direct plant-data symbol use was extracted; the import remains a compilation dependency in the pesticide-output subsystem. |
| [sym:basin_ch_pest_output] | plant_data_module | No direct plant-data symbol use was extracted; the import remains a compilation dependency in the pesticide-output subsystem. |
| [sym:basin_ls_pest_output] | plant_data_module | No direct plant-data symbol use was extracted; the import remains a compilation dependency in the pesticide-output subsystem. |
| [sym:basin_res_pest_output] | plant_data_module | No direct plant-data symbol use was extracted; the import remains a compilation dependency in the pesticide-output subsystem. |
| [sym:calsoft_read_codes] | plant_data_module | No direct plant-data symbol use was extracted; the module is only present as a shared dependency. |
| [sym:ch_cs_output] | plant_data_module | No direct plant-data symbol use was extracted; the module is only present as a shared dependency. |
| [sym:ch_salt_output] | plant_data_module | No direct plant-data symbol use was extracted; the module is only present as a shared dependency. |
| [sym:cha_pesticide_output] | plant_data_module | No direct plant-data symbol use was extracted; the module is only present as a shared dependency. |

## Lineage

`plant_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 12 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `plant_data_module.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `fc00a75` (2026-04-22) — Changes cswat_3_part_fracs to cswat_1_part_fracs to be consistent with cswat == 1
- `ddbd4bc` (2026-03-26) — Added photo degrade factor to plant_data_module.
- `5e0b0b1` (2026-02-27) — Updated the plants.plt to have above and below ground lignin fractions. Updated plant_data_module to have an additional data structure for a…
- `fd3d90f` (2025-12-08) — made changes to include residue partition fractions and read them in plant.plt and initilize the initial residue amounts.
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `plant_data_module` has no extracted module-level documentation comment.
- Reader rows are representative of the importers shown in the packet; the complete deterministic importer list is preserved in `all_importers`.
- Some importer routines are shown only as compile-time dependencies in the packet, with no direct symbol use resolved from `plant_data_module`.
- The source notes that `residue_partition_fracs` field names are misleading; the comments map the values to the carbon model's above-ground and below-ground partition usage.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
