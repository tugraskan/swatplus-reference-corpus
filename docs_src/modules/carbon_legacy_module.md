---
kind: module
symbol: carbon_legacy_module
title: carbon_legacy_module
status: filled
source_hash: 5aee71a83f05c318
version_label: SWAT+ 62.0.0
variables:
  plc_hdr: Module-owned fixed-column header for legacy plant carbon statistics output. It
    is declared in this module and written by `carbon_legacy_open` to `hru_plc_stat.txt/csv`
    when legacy HRU carbon output is enabled. The fields name the frequency/date identifiers,
    unit and GIS identifiers, and plant carbon quantities.
  plc_hdr_units: Module-owned units row for `plc_hdr`. Initialized with blank labels for header
    fields and `kg/ha` for the plant carbon quantity columns. Written by `carbon_legacy_open`
    alongside `plc_hdr` for legacy plant carbon statistics files.
  soil_org_flux_hdr: Module-owned fixed-column header for legacy soil organic flux output.
    Declared here and written by `carbon_legacy_open` to `hru_cflux_stat.txt/csv` when the
    legacy carbon path is active. The fields identify frequency, soil layer/depth, time, unit/GIS
    IDs, and carbon/nitrogen flux terms.
  soil_org_flux_hdr_units: Module-owned units row for `soil_org_flux_hdr`. It supplies blank
    labels for identifiers and `kg_C/ha` or `kg_N/ha` units for the flux columns, and is written
    with the header in legacy soil flux files.
  cpool_hdr: Module-owned fixed-column header for legacy carbon pool output. Written by `carbon_legacy_open`
    to `hru_cpool_stat.txt/csv` and contains the time, unit/GIS, and soil carbon pool names
    for residue, structural, metabolic, humus, microbial, lignin, nonlignin, water, manure,
    root mass, and soil water.
  cpool_units: Module-owned units row for `cpool_hdr`. It leaves identifier fields blank and
    assigns `kg/ha` to carbon pool masses, with `mm/mm` for soil water. Written with `cpool_hdr`
    in the legacy carbon pool files.
  n_p_pool_hdr: Module-owned fixed-column header for legacy nitrogen and phosphorus pool output.
    It defines the same time and location identifiers as the carbon pool header and names
    the N and P pool quantities for residue, structural, metabolic, humus, microbial, lignin,
    nonlignin, water, and manure pools.
  n_p_pool_units: Module-owned units row for `n_p_pool_hdr`. It uses blank labels for identifiers,
    `kg/ha` for the N and P pool quantities, and is intended for the legacy N/P pool output
    family.
  carbvars_hdr: Module-owned fixed-column header for legacy carbon variables output. It is
    written by `carbon_legacy_open` to `hru_carbvars.txt/csv` when the legacy HRU carbon variables
    option is enabled. The columns name tillage, residue/soil mixing, soil chemistry, respiration,
    temperature, and related carbon process variables.
  org_allow_hdr: Module-owned fixed-column header for legacy organic allocation output. It
    is written by `carbon_legacy_open` to `hru_org_allo_vars.txt/csv` and names the organic
    allocation variables for aspiration, above/below-ground partitioning, and CO2 terms.
  org_ratio_hdr: Module-owned fixed-column header for legacy organic ratio output. It is written
    by `carbon_legacy_open` to `hru_org_ratio_vars.txt/csv` and names the carbon ratio variables
    for biomass, humus, and structural pools.
  org_trans_hdr: Module-owned fixed-column header for legacy organic transfer output. It is
    written by `carbon_legacy_open` to `hru_org_trans_vars.txt/csv` and names biomass, humus,
    humic product, microbial, lignin, and structural transfer quantities.
  org_trans_units: Module-owned units row for `org_trans_hdr`. It assigns `kg/ha` units to
    the transfer quantities and is written with the header in the legacy organic transfer
    files.
  endsim_soil_prop_hdr: Module-owned fixed-column header for end-of-simulation soil property
    output. It is written by `carbon_legacy_open` to `hru_endsim_soil_prop.txt/csv` and names
    soil property columns such as bulk density, AWC, soil K, carbon, texture fractions, rock,
    albedo, USLE K, EC, CaCO3, and pH.
  bsn_carb_hdr: Module-owned fixed-column header for basin carbon summary output. It is written
    by `carbon_legacy_open` to `basin_carbon_all.txt` when legacy HRU carbon output is enabled
    and basin HRU annual output is requested.
  bsn_carb_hdr_units: Module-owned units row for `bsn_carb_hdr`. It leaves date fields blank
    and assigns `kg/ha` to basin soil carbon, plant carbon, and residue carbon totals.
type_components:
  output_plc_header:
    freq: Print frequency label.
    day: Julian-day time column label.
    day_mo: Day-of-month time column label.
    mo: Month time column label.
    yrc: Year time column label.
    isd: Landscape unit or HRU unit label.
    id: GIS identifier label.
    name: Name label.
    tot_c: Total plant carbon column label.
    ab_gr_c: Above-ground carbon column label.
    leaf_c: Leaf carbon column label.
    stem_c: Stem carbon column label.
    seed_c: Seed carbon column label.
    root_c: Root carbon column label.
    rsd_c: Surface residue carbon column label.
  output_plc_header_units:
    freq: Blank units field for frequency.
    day: Blank units field for Julian day.
    day_mo: Blank units field for day-of-month.
    mo: Blank units field for month.
    yrc: Blank units field for year.
    isd: Blank units field for the unit identifier.
    id: Blank units field for the GIS identifier.
    name: Blank units field for the name column.
    tot_c: Plant carbon total in kg/ha.
    ab_gr_c: Above-ground carbon in kg/ha.
    leaf_c: Leaf carbon in kg/ha.
    stem_c: Stem carbon in kg/ha.
    seed_c: Seed carbon in kg/ha.
    root_c: Root carbon in kg/ha.
    rsd_c: Surface residue carbon in kg/ha.
  output_soil_org_flux_header:
    freq: Print frequency label.
    soil_lyr: Soil layer label.
    soil_depth: Soil depth label.
    day: Julian-day time column label.
    mo: Month time column label.
    day_mo: Day-of-month time column label.
    yrc: Year time column label.
    isd: Unit label.
    id: GIS identifier label.
    name: Name label.
    cfmets1: Carbon flux between metabolic and structural pools in layer 1.
    cfstrs1: Carbon flux from structural to structural/state 1 pool.
    cfstrs2: Carbon flux from structural to structural/state 2 pool.
    efmets1: Nitrogen flux between metabolic and structural pools in layer 1.
    efstrs1: Nitrogen flux from structural to structural/state 1 pool.
    efstrs2: Nitrogen flux from structural to structural/state 2 pool.
    immmets1: Nitrogen immobilization/metabolic flux for state 1.
    immstrs1: Nitrogen immobilization/structural flux for state 1.
    immstrs2: Nitrogen immobilization/structural flux for state 2.
    mnrmets1: Nitrogen mineralization/metabolic flux for state 1.
    mnrstrs1: Nitrogen mineralization/structural flux for state 1.
    mnrstrs2: Nitrogen mineralization/structural flux for state 2.
    co2fmet: CO2 flux from metabolic decomposition.
    co2fstr: CO2 flux from structural decomposition.
    cfs1s2: Carbon flux from state 1 to state 2.
    cfs1s3: Carbon flux from state 1 to state 3.
    cfs2s1: Carbon flux from state 2 to state 1.
    cfs2s3: Carbon flux from state 2 to state 3.
    cfs3s1: Carbon flux from state 3 to state 1.
    efs1s2: Nitrogen flux from state 1 to state 2.
    efs1s3: Nitrogen flux from state 1 to state 3.
    efs2s1: Nitrogen flux from state 2 to state 1.
    efs2s3: Nitrogen flux from state 2 to state 3.
    efs3s1: Nitrogen flux from state 3 to state 1.
    imms1s2: Nitrogen immobilization flux from state 1 to state 2.
    imms1s3: Nitrogen immobilization flux from state 1 to state 3.
    imms2s1: Nitrogen immobilization flux from state 2 to state 1.
    imms2s3: Nitrogen immobilization flux from state 2 to state 3.
    imms3s1: Nitrogen immobilization flux from state 3 to state 1.
    mnrs1s2: Nitrogen mineralization flux from state 1 to state 2.
    mnrs1s3: Nitrogen mineralization flux from state 1 to state 3.
    mnrs2s1: Nitrogen mineralization flux from state 2 to state 1.
    mnrs2s3: Nitrogen mineralization flux from state 2 to state 3.
    mnrs3s1: Nitrogen mineralization flux from state 3 to state 1.
    co2fs1: CO2 flux from state 1.
    co2fs2: CO2 flux from state 2.
    co2fs3: CO2 flux from state 3.
  output_soil_org_flux_header_units:
    freq: Blank units field for frequency.
    soil_lyr: Blank units field for soil layer.
    soil_depth: Soil depth in mm.
    day: Blank units field for Julian day.
    mo: Blank units field for month.
    day_mo: Blank units field for day-of-month.
    yrc: Blank units field for year.
    isd: Blank units field for unit identifier.
    id: Blank units field for GIS identifier.
    name: Blank units field for name.
    cfmets1: Carbon flux in kg_C/ha.
    cfstrs1: Carbon flux in kg_C/ha.
    cfstrs2: Carbon flux in kg_C/ha.
    efmets1: Nitrogen flux in kg_N/ha.
    efstrs1: Nitrogen flux in kg_N/ha.
    efstrs2: Nitrogen flux in kg_N/ha.
    immmets1: Nitrogen flux in kg_N/ha.
    immstrs1: Nitrogen flux in kg_N/ha.
    immstrs2: Nitrogen flux in kg_N/ha.
    mnrmets1: Nitrogen flux in kg_N/ha.
    mnrstrs1: Nitrogen flux in kg_N/ha.
    mnrstrs2: Nitrogen flux in kg_N/ha.
    co2fmet: CO2-related carbon flux in kg_C/ha.
    co2fstr: CO2-related carbon flux in kg_C/ha.
    cfs1s2: Carbon flux in kg_C/ha.
    cfs1s3: Carbon flux in kg_C/ha.
    cfs2s1: Carbon flux in kg_C/ha.
    cfs2s3: Carbon flux in kg_C/ha.
    cfs3s1: Carbon flux in kg_C/ha.
    efs1s2: Nitrogen flux in kg_N/ha.
    efs1s3: Nitrogen flux in kg_N/ha.
    efs2s1: Nitrogen flux in kg_N/ha.
    efs2s3: Nitrogen flux in kg_N/ha.
    efs3s1: Nitrogen flux in kg_N/ha.
    imms1s2: Nitrogen flux in kg_N/ha.
    imms1s3: Nitrogen flux in kg_N/ha.
    imms2s1: Nitrogen flux in kg_N/ha.
    imms2s3: Nitrogen flux in kg_N/ha.
    imms3s1: Nitrogen flux in kg_N/ha.
    mnrs1s2: Nitrogen flux in kg_N/ha.
    mnrs1s3: Nitrogen flux in kg_N/ha.
    mnrs2s1: Nitrogen flux in kg_N/ha.
    mnrs2s3: Nitrogen flux in kg_N/ha.
    co2fs2: CO2-related carbon flux in kg_C/ha.
    co2fs3: CO2-related carbon flux in kg_C/ha.
  output_cpool_header:
    freq: Print frequency label.
    soil_lyr: Soil layer label.
    soil_depth: Soil depth label.
    day: Julian-day time column label.
    mo: Month time column label.
    day_mo: Day-of-month time column label.
    yrc: Year time column label.
    isd: Unit label.
    id: GIS identifier label.
    name: Name label.
    residue_c: Residue carbon pool label.
    str_c: Structural carbon pool label.
    meta_c: Metabolic carbon pool label.
    hs_c: Humus stable carbon pool label.
    hp_c: Humus passive carbon pool label.
    microb_c: Microbial carbon pool label.
    lig_c: Lignin carbon pool label.
    nonlig_c: Nonlignin carbon pool label.
    water_c: Water carbon pool label.
    manure_c: Manure carbon pool label.
    root_mass: Root mass column label.
    soil_water: Soil water column label.
  output_cpool_header_units:
    freq: Blank units field for frequency.
    soil_lyr: Blank units field for soil layer.
    soil_depth: Soil depth in mm.
    day: Blank units field for Julian day.
    mo: Blank units field for month.
    day_mo: Blank units field for day-of-month.
    yrc: Blank units field for year.
    isd: Blank units field for unit identifier.
    id: Blank units field for GIS identifier.
    name: Blank units field for name.
    residue_c: Carbon pool in kg/ha.
    str_c: Carbon pool in kg/ha.
    meta_c: Carbon pool in kg/ha.
    hs_c: Carbon pool in kg/ha.
    hp_c: Carbon pool in kg/ha.
    microb_c: Carbon pool in kg/ha.
    lig_c: Carbon pool in kg/ha.
    nonlig_c: Carbon pool in kg/ha.
    water_c: Carbon pool in kg/ha.
    manure_c: Carbon pool in kg/ha.
    root_mass: Root mass in kg/ha.
    soil_water: Soil water in mm/mm.
  output_n_p_pool_header:
    freq: Print frequency label.
    soil_lyr: Soil layer label.
    soil_depth: Soil depth label.
    day: Julian-day time column label.
    mo: Month time column label.
    day_mo: Day-of-month time column label.
    yrc: Year time column label.
    isd: Unit label.
    id: GIS identifier label.
    name: Name label.
    total_pool_n: Total nitrogen pool label.
    residue_n: Residue nitrogen pool label.
    str_n: Structural nitrogen pool label.
    meta_n: Metabolic nitrogen pool label.
    hs_n: Humus stable nitrogen pool label.
    hp_n: Humus passive nitrogen pool label.
    microb_n: Microbial nitrogen pool label.
    lig_n: Lignin nitrogen pool label.
    nonlig_n: Nonlignin nitrogen pool label.
    water_n: Water nitrogen pool label.
    manure_n: Manure nitrogen pool label.
    total_pool_p: Total phosphorus pool label.
    residue_p: Residue phosphorus pool label.
    str_p: Structural phosphorus pool label.
    meta_p: Metabolic phosphorus pool label.
    hs_p: Humus stable phosphorus pool label.
    hp_p: Humus passive phosphorus pool label.
    microb_p: Microbial phosphorus pool label.
    lig_p: Lignin phosphorus pool label.
    nonlig_p: Nonlignin phosphorus pool label.
    water_p: Water phosphorus pool label.
    manure_p: Manure phosphorus pool label.
  output_n_p_pool_header_units:
    freq: Blank units field for frequency.
    soil_lyr: Blank units field for soil layer.
    soil_depth: Soil depth in mm.
    day: Blank units field for Julian day.
    mo: Blank units field for month.
    day_mo: Blank units field for day-of-month.
    yrc: Blank units field for year.
    isd: Blank units field for unit identifier.
    id: Blank units field for GIS identifier.
    name: Blank units field for name.
    total_pool_n: Nitrogen pool in kg/ha.
    residue_n: Nitrogen pool in kg/ha.
    str_n: Nitrogen pool in kg/ha.
    meta_n: Nitrogen pool in kg/ha.
    hs_n: Nitrogen pool in kg/ha.
    hp_n: Nitrogen pool in kg/ha.
    microb_n: Nitrogen pool in kg/ha.
    lig_n: Nitrogen pool in kg/ha.
    nonlig_n: Nitrogen pool in kg/ha.
    water_n: Nitrogen pool in kg/ha.
    manure_n: Nitrogen pool in kg/ha.
    total_pool_p: Phosphorus pool in kg/ha.
    residue_p: Phosphorus pool in kg/ha.
    str_p: Phosphorus pool in kg/ha.
    meta_p: Phosphorus pool in kg/ha.
    hs_p: Phosphorus pool in kg/ha.
    hp_p: Phosphorus pool in kg/ha.
    microb_p: Phosphorus pool in kg/ha.
    lig_p: Phosphorus pool in kg/ha.
    nonlig_p: Phosphorus pool in kg/ha.
    water_p: Phosphorus pool in kg/ha.
    manure_p: Phosphorus pool in kg/ha.
  output_carb_vars_header:
    freq: Print frequency label.
    soil_lyr: Soil layer label.
    soil_depth: Soil depth label.
    day: Julian-day time column label.
    mo: Month time column label.
    day_mo: Day-of-month time column label.
    yrc: Year time column label.
    isd: Unit label.
    id: GIS identifier label.
    name: Name label.
    sut: Surface tillage or disturbance identifier.
    tillagef: Tillage factor.
    bmix: Conservation biomass mixing factor.
    tillagef_biomix: Combined tillage/biomix factor.
    tillagef_tillmix: Combined tillage/tillmix factor.
    till_eff: Tillage effectiveness.
    cdg: Carbon decomposition/gasification variable.
    ox: Oxidation variable.
    cs: Carbon storage or carbon state variable.
    no3: Nitrate variable.
    nh4: Ammonium variable.
    resp: CO2 respiration variable.
    soil_tmp: Soil temperature variable.
    emix: Mixing efficiency variable.
  output_org_allo_header:
    freq: Print frequency label.
    soil_lyr: Soil layer label.
    soil_depth: Soil depth label.
    day: Julian-day time column label.
    mo: Month time column label.
    day_mo: Day-of-month time column label.
    yrc: Year time column label.
    isd: Unit label.
    id: GIS identifier label.
    name: Name label.
    asp: Aspiration or allocation state variable.
    abpt: Above/below partitioning variable.
    abco2: Above-ground CO2 variable.
    a1co2: Allocation CO2 stage 1 variable.
    asco2: Allocation CO2 stage variable.
    apco2: Allocation CO2 stage variable.
  output_org_ratio_header:
    freq: Print frequency label.
    soil_lyr: Soil layer label.
    soil_depth: Soil depth label.
    day: Julian-day time column label.
    mo: Month time column label.
    day_mo: Day-of-month time column label.
    yrc: Year time column label.
    isd: Unit label.
    id: GIS identifier label.
    name: Name label.
    ncbm: Carbon-to-biomass nitrogen ratio.
    nchp: Carbon-to-humus passive nitrogen ratio.
    nchs: Carbon-to-humus stable nitrogen ratio.
  output_org_trans_header:
    freq: Print frequency label.
    soil_lyr: Soil layer label.
    soil_depth: Soil depth label.
    day: Julian-day time column label.
    mo: Month time column label.
    day_mo: Day-of-month time column label.
    yrc: Year time column label.
    isd: Unit label.
    id: GIS identifier label.
    name: Name label.
    bmctp: Biomass carbon transferred to phosphorus.
    bmntp: Biomass nitrogen transferred to phosphorus.
    hsctp: Humus stable carbon transfer to phosphorus.
    hsntp: Humus stable nitrogen transfer to phosphorus.
    hpctp: Humus passive carbon transfer to phosphorus.
    hpntp: Humus passive nitrogen transfer to phosphorus.
    lmctp: Lignin or litter mass carbon transfer to phosphorus.
    lmntp: Lignin or litter mass nitrogen transfer to phosphorus.
    lsctp: Labile structural carbon transfer to phosphorus.
    lslctp: Labile structural lignin carbon transfer to phosphorus.
    lslnctp: Labile structural lignin-nitrogen carbon transfer to phosphorus.
    lsntp: Labile structural nitrogen transfer to phosphorus.
  output_org_trans_header_units:
    freq: Blank units field for frequency.
    soil_lyr: Blank units field for soil layer.
    soil_depth: Soil depth in mm.
    day: Blank units field for Julian day.
    mo: Blank units field for month.
    day_mo: Blank units field for day-of-month.
    yrc: Blank units field for year.
    isd: Blank units field for unit identifier.
    id: Blank units field for GIS identifier.
    name: Blank units field for name.
    bmctp: Transfer quantity in kg/ha.
    bmntp: Transfer quantity in kg/ha.
    hsctp: Transfer quantity in kg/ha.
    hsntp: Transfer quantity in kg/ha.
    hpctp: Transfer quantity in kg/ha.
    hpntp: Transfer quantity in kg/ha.
    lmctp: Transfer quantity in kg/ha.
    lmntp: Transfer quantity in kg/ha.
    lsctp: Transfer quantity in kg/ha.
    lslctp: Transfer quantity in kg/ha.
    lslnctp: Transfer quantity in kg/ha.
    lsntp: Transfer quantity in kg/ha.
  output_endsim_soil_prop_header:
    freq: Print frequency label.
    soil_name: Soil name label.
    soil_lyr: Soil layer label.
    soil_depth: Soil depth label.
    day: Julian-day time column label.
    mo: Month time column label.
    day_mo: Day-of-month time column label.
    yrc: Year time column label.
    isd: Unit label.
    id: GIS identifier label.
    name: Name label.
    bd: Bulk density label.
    awc: Available water capacity label.
    soil_k: Soil hydraulic conductivity label.
    carbon: Soil carbon label.
    clay: Clay fraction label.
    silt: Silt fraction label.
    sand: Sand fraction label.
    rock: Rock fraction label.
    alb: Albedo label.
    usle_k: USLE K factor label.
    ec: Electrical conductivity label.
    caco3: Calcium carbonate label.
    ph: Soil pH label.
  output_bsn_carb_header:
    day: Julian-day time column label.
    yrc: Year time column label.
    blnk: Spacer column.
    org_soilc: Basin organic soil carbon total.
    org_plc: Basin organic plant carbon total.
    org_resc: Basin organic residue carbon total.
  output_bsn_carb_header_units:
    day: Blank units field for Julian day.
    yrc: Blank units field for year.
    blnk: Spacer column.
    org_soilc: Basin organic soil carbon in kg/ha.
    org_plc: Basin organic plant carbon in kg/ha.
    org_resc: Basin organic residue carbon in kg/ha.
type_summaries:
  output_plc_header: Fixed-column header record for legacy plant carbon statistics output.
  output_plc_header_units: Units row that accompanies the legacy plant carbon statistics header.
  output_soil_org_flux_header: Fixed-column header record for legacy soil organic flux output.
  output_soil_org_flux_header_units: Units row that accompanies the legacy soil organic flux
    header.
  output_cpool_header: Fixed-column header record for legacy carbon pool output.
  output_cpool_header_units: Units row that accompanies the legacy carbon pool header.
  output_n_p_pool_header: Fixed-column header record for legacy nitrogen and phosphorus pool
    output.
  output_n_p_pool_header_units: Units row that accompanies the legacy nitrogen and phosphorus
    pool header.
  output_carb_vars_header: Fixed-column header record for legacy carbon variables output.
  output_org_allo_header: Fixed-column header record for legacy organic allocation output.
  output_org_ratio_header: Fixed-column header record for legacy organic ratio output.
  output_org_trans_header: Fixed-column header record for legacy organic transfer output.
  output_org_trans_header_units: Units row that accompanies the legacy organic transfer header.
  output_endsim_soil_prop_header: Fixed-column header record for end-of-simulation soil properties.
  output_bsn_carb_header: Fixed-column header record for basin carbon summary output.
  output_bsn_carb_header_units: Units row that accompanies the basin carbon summary header.
---

<!-- facts:header -->

Owns the legacy carbon output header records and the `carbon_legacy_open` routine that opens the old CSU carbon files. It exists to preserve the non-standard legacy carbon output path, while the newer carbonDev output families continue through the standard `print.prt` flags.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container plus one opener routine. The derived-type header variables are module state with initial literal labels, and `carbon_legacy_open` writes them to the legacy output files when the corresponding legacy carbon flags are enabled.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:output_landscape_init] | `unit_2000, unit_9000, unit_2004, unit_2001, unit_2005, unit_2002, unit_2006, unit_2003, unit_2007, unit_2020, unit_2024, unit_3333, unit_3334, unit_3335, unit_3336, unit_3337, unit_3338, unit_3339, unit_3340, unit_2021, unit_2025, unit_2022, unit_2026, unit_2023, unit_2027, unit_4520, unit_4524, unit_4521, unit_4525, unit_4522, unit_4526, unit_4523, unit_4527, unit_4550, unit_4554, unit_4551, unit_4555, unit_4552, unit_4556, unit_4553, unit_4557, unit_2030, unit_2034, unit_2031, unit_2035, unit_2032, unit_2036, unit_2033, unit_2037, unit_2040, unit_2044, unit_2041, unit_2045, unit_2042, unit_2046, unit_2043, unit_2047, unit_2300, unit_2304, unit_2301, unit_2305, unit_2302, unit_2306, unit_2303, unit_2307, unit_2440, unit_2444, unit_2441, unit_2445, unit_2442, unit_2446, unit_2443, unit_2447, unit_2460, unit_2464, unit_2461, unit_2465, unit_2462, unit_2466, unit_2463, unit_2467, unit_2140, unit_2144, unit_2141, unit_2145, unit_2142, unit_2146, unit_2143, unit_2147, unit_2150, unit_2154, unit_2151, unit_2155, unit_2152, unit_2156, unit_2153, unit_2157, unit_2160, unit_2164, unit_2161, unit_2165, unit_2162, unit_2166, unit_2163, unit_2167, unit_2170, unit_2174, unit_2171, unit_2175, unit_2172, unit_2176, unit_2173, unit_2177, unit_2050, unit_2054, unit_2051, unit_2055, unit_2052, unit_2056, unit_2053, unit_2057, unit_2060, unit_2064, unit_2061, unit_2065, unit_2062, unit_2066, unit_2063, unit_2067, unit_2070, unit_2074, unit_2071, unit_2075, unit_2072, unit_2076, unit_2073, unit_2077, unit_2080, unit_2084, unit_2081, unit_2085, unit_2082, unit_2086, unit_2083, unit_2087, unit_4010, unit_4011, unit_4008, unit_4009, unit_4750, unit_4754, unit_4751, unit_4755, unit_4752, unit_4756, unit_4753, unit_4757, unit_4758, unit_4762, unit_4759, unit_4763, unit_4760, unit_4764, unit_4761, unit_4765, unit_4766, unit_4770, unit_4767, unit_4771, unit_4768, unit_4772, unit_4769, unit_4773` | `plc_hdr, plc_hdr_units, soil_org_flux_hdr, soil_org_flux_hdr_units, cpool_hdr, cpool_units` | Calls `carbon_legacy_open` so the legacy CSU carbon output headers are opened and written when the legacy carbon flags are active. |

## Key Consumers

This module is imported by the landscape initialization path, which invokes the opener routine to create the legacy CSU carbon files before later HRU and basin carbon output phases run.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:output_landscape_init] | `carbon_legacy_open` | Opens the old fixed-column legacy carbon outputs and writes the beginning soil snapshot for the CSU carbon files. |

## Lineage

`carbon_legacy_module.f90` was introduced in `821a63e` (2026-06-02, "reinstate CSU outputs and print flags") and has been changed in 2 non-merge commit(s) since, most recently `dfce092` (2026-06-02, "move carbon activation to cswat = 2, reserve 1 for C-FARM"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `carbon_legacy_module.f90` are listed.

- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `821a63e` (2026-06-02) — reinstate CSU outputs and print flags

## Review Notes

- Module `carbon_legacy_module` has no extracted module-level documentation comment.
- The source comment says this path will be removed in revision 63 and is gated by legacy `hru_cb` / `hru_cb_vars` rows in `print.prt`; those rows are not emitted by the SWAT+ editor.
- The `output_landscape_init` import list is parser-derived and the only confirmed importer in the provided evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
