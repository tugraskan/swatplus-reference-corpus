---
kind: procedure
symbol: plant_init
title: plant_init
status: filled
source_hash: 33d641346a788fcf
version_label: SWAT+ 62.0.0
args:
  init: Controls whether the routine only initializes a fresh HRU plant state (`0`) or first
    deallocates and resets any existing plant-community and residue arrays before rebuilding
    them (`> 0`).
  iihru: Selects the HRU index whose plant-community state is being initialized and whose
    linked land-use, soil, weather, and management records are read and updated.
locals:
  day_mo: Day-of-month returned by `xmon` when a Julian day is converted to month/day for
    temperature and heat-unit calculations.
  icom: Plant-community database index taken from `hru(j)%plant_cov`; it selects which community
    definition to copy into the HRU.
  idp: Plant database index for the active plant species, taken from `pcomdb(icom)%pl(ipl)%db_num`,
    and used to read species traits from `pldb` and `plcp`.
  j: HRU index copied from `iihru`; it is the primary index used to read and write the HRU’s
    plant, management, and land-use state.
  iob: Object index from `hru(j)%obj_no`; it links the HRU to the containing object so the
    weather station can be found.
  iwgn: Weather-generator index resolved from the object’s weather station; it selects monthly
    temperature and day-length parameters.
  mo: Month number returned by `xmon` and used to pick monthly climate-generator temperatures.
  iday: Julian day counter used in annual loops for heat-unit accumulation, dormancy timing,
    and planting-day search.
  icp: Conservation-practice index from the land-use management structure; it selects slope-length
    and P-factor parameters.
  ilum: Land-use management index for the HRU; it is used to look up the current land-use
    and management data.
  idb: Loop index used to search lookup tables for urban land-use names and overland roughness
    names.
  isched: Management-schedule index from `hru(j)%mgt_ops`; it identifies the schedule to inspect
    for the first active operation.
  iop: Loop index over management operations in a schedule while searching for the first valid
    operation for the current year.
  irot: Rotation-year counter used while scanning the schedule to find the operation that
    matches the initialized rotation year.
  igrow: Julian day when plant growth begins; it is determined from heat units or dormancy-daylength
    rules.
  iday_sum: Counter used to shift Julian days when evaluating southern-hemisphere planting
    windows.
  iday_sh: Adjusted Julian day for southern-hemisphere month/day conversion during seasonal
    calculations.
  jday_prev: Previous operation Julian day, used to detect a new rotation year or skipped
    operation while scanning the schedule.
  phutot: Running total of accumulated heat units for the selected growth window; it is used
    to set maturity heat units.
  tave: Monthly mean temperature computed from the weather generator’s monthly maximum and
    minimum temperatures.
  phuday: Daily heat-unit increment, either base-zero temperature or temperature above base,
    depending on the branch.
  xx: Intermediate population scaling factor used when converting plant population into potential
    canopy height.
  xm: Exponent in the USLE topographic factor, computed from slope.
  sin_sl: Sine of slope angle, used in the USLE LS-factor formula.
  sl_len: Slope length limited by conservation-practice maximum, used in the USLE LS-factor
    calculation.
  phu0: Annual base-zero heat-unit total accumulated from positive monthly mean temperatures
    and later scaled to a planting threshold.
  sd: Solar declination angle used in the dormancy/daylength calculation for null plant types.
  sdlat: Intermediate latitude/daylength term computed from solar declination and latitude.
  h: Hour-angle term used to derive day length from solar declination and latitude.
  daylength: Computed daylight hours used to decide when dormancy should end for null plant
    types.
  laimx_pop: Population-adjusted maximum LAI used to initialize potential canopy size.
  matur_frac: Fraction-to-maturity value used to initialize canopy height and leaf-area scaling
    for annuals and perennials.
  f: Intermediate logistic-growth fraction used to compute annual canopy height from heat-unit
    accumulation.
  dd: Relative earth-sun distance term used in the daylength/dormancy branch.
uses:
  hru_module: '`hru_module` supplies the HRU record being initialized. Its `plant_cov`, `obj_no`,
    `mgt_ops`, and `cur_op` fields determine which plant community to load, which weather/object
    context to use, and which management operation should be active when initialization finishes.'
  soil_module: '`soil_module` matters because layer allocations for plant water uptake and
    root fractions are sized from the HRU soil profile’s number of layers.'
  plant_module: '`plant_module` holds the plant-community state that `plant_init` allocates
    and populates: plant names, current status, growth variables, biomass pools, residue cover
    factor, rotation year, and canopy-related fields are all initialized here for later plant-growth
    and management routines.'
  hydrograph_module: '`hydrograph_module` provides the HRU’s connected object record so the
    routine can follow `hru(j)%obj_no` to the object weather-station number used in climate-based
    initialization.'
  climate_module: '`climate_module` provides the weather station and weather-generator data
    used to compute annual heat units, planting day, dormancy timing, and initial canopy conditions
    from monthly temperature and latitude information.'
  time_module: '`time_module` matters because the schedule scan uses `time%day_start` to choose
    the first management operation that should be active at the start of the simulation year.'
  maximum_data_module: '`maximum_data_module` provides the maximum counts for the urban and
    overland-naming lookup tables that this routine loops through when cross-walking land-use
    names to internal codes.'
  plant_data_module: '`plant_data_module` supplies the plant community database, plant species
    database, and plant parameter records that define the number of plants, their names and
    status flags, maturity settings, residue inputs, canopy height limits, and heat-unit traits
    copied into the HRU state.'
  landuse_data_module: '`landuse_data_module` matters because the routine finishes by translating
    the HRU’s land-use management into urban runoff and overland roughness codes, and by finding
    the conservation-practice entry used for slope and P-factor calculations.'
  mgt_operations_module: '`mgt_operations_module` supplies the management schedule and operation
    records that `plant_init` scans to determine the first valid operation and current rotation
    year for the HRU.'
  urban_data_module: '`urban_data_module` matters because urban land-use names are cross-walked
    to an internal urban database index before the HRU land-use state is finalized.'
  conditional_module: '`conditional_module` matters because the land-use cross-walk uses overland
    roughness names and codes that feed conditional land-use behavior after initialization.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides the plant-residue and
    plant-mass types that are allocated, zeroed, and filled with residue and biomass values.
    Those pools are needed for residue cover, nutrient accounting, and later decomposition
    and harvest routines.'
---

<!-- facts:header -->

Initializes or resets plant-community state for one HRU and loads the plant, residue, canopy, and scheduling values needed for subsequent growth and management simulation.

## Bottom Line

`plant_init` builds the plant-community data for a single HRU from the current land-use and plant database settings. When `init > 0`, it first tears down previously allocated plant, growth, mass, and soil-residue arrays so the HRU can be reinitialized cleanly after a land-use change.

It then allocates and fills the active plant list, copies plant database fields into community state, computes starting residue and heat-unit/maturity values, sets the first management operation, and initializes canopy, root, and partition state for plants that are growing. The routine also updates HRU-level erosion and land-use lookup values that later plant, management, and soil routines depend on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when plant communities are first created for all HRUs in `plant_all_init`, and again from `actions` when an HRU’s land use changes and the plant state must be rebuilt. Upstream routines provide the HRU’s land-use, soil, object, weather, and management pointers; after initialization, later plant-growth, residue, erosion, and management operations rely on the allocated arrays, canopy state, rooting state, residue pools, and first-operation pointers set here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the HRU and plant community | Copies the input HRU index into `j`, reads the HRU’s plant-community pointer `icom`, and exits early for HRUs with no plant community by setting `pcom(j)%npl` to zero. |
| 2. Reset and allocate plant arrays when needed | If this is a reinitialization (`init > 0`), deallocates prior plant, growth, mass, and soil-residue arrays, then allocates per-plant community arrays, plant-mass pools, uptake arrays, root-fraction arrays, and residue-layer arrays using the community plant count. |
| 3. Initialize community-level residue and cover state | Zeroes residue cover factor, community cover modifier, rotation year, and maximum-LAI sum, and sets the plant residue pools to the zero-mass template before plant-specific values are filled. |
| 4. Load each plant’s database values and residue inputs | For every plant in the community, copies the plant name and growth flag from the plant community database, marks it dormant, looks up the plant database index, fills residue mass, carbon, nitrogen, and phosphorus pools from the database residue input, and accumulates the community residue total. |
| 5. Determine weather context and annual heat units | Finds the HRU’s object and weather generator, then loops over the year with `xmon` and monthly temperatures to accumulate positive base-zero heat units for annual scheduling. |
| 6. Set maturity heat units or maturity timing by plant type | Chooses one of three maturity branches: use the full-season heat-unit sum for plants with zero days-to-maturity, flip a stored maturity value when a negative value indicates heat units were supplied directly, or derive planting day and maturity heat units from plant type, latitude, temperature, and day-length rules for positive days-to-maturity entries. |
| 7. Find the first management operation | Reads the HRU management schedule, scans operations to match the initialized rotation year and simulation start day, and stores the first active operation in both `sched(isched)%first_op` and `hru(j)%cur_op`. |
| 8. Copy community and plant database values into active state | Copies the community name, rotation year, plant heat-unit accumulation, canopy height, LAI, biomass fractions, residue cover factor, plant identifier, and potential LAI values from the plant databases into the active plant-community state. |
| 9. Initialize growing plants' root and biomass partitioning | For plants marked as growing, calls root-growth, seed-growth, partitioning, and root-fraction routines so the initial biomass and rooting state is internally consistent before simulation continues. |
| 10. Average community residue cover factors | Converts accumulated community residue cover factor and community canopy modifier to averages across the number of plants, or sets them to zero when the community has no plants. |
| 11. Set HRU-level plant and land-use factors | Copies the HRU’s water-stress compensation factor into each plant, computes the USLE slope-length factor and P factor from land-use management and slope, and cross-walks urban and overland roughness codes from the land-use tables into the HRU land-use state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` | `hru(j)%plant_cov, hru(j)%obj_no, hru(j)%mgt_ops, hru(j)%cur_op` |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%pl, pcom(j)%plg, pcom(j)%plm, pcom(j)%plstr, pcom(j)%plcur, pcom(j)%pl(ipl), pcom(j)%plg(ipl), pcom(j)%plm(ipl), pcom(j)%plstr(ipl), pcom(j)%plcur(ipl), pcom(j)%plcur(ipl)%uptake, pcom(j)%rsd_covfac, pcom(j)%pcomdb, pcom(j)%rot_yr, pcom(j)%laimx_sum, pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%idorm, pcom(j)%plcur(ipl)%phumat, pcom(j)%name, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plg(ipl)%cht` |
| [sym:hydrograph_module] | `ob` | `ob(iob)%wst` |
| [sym:climate_module] | `wst, wgn, wgn_pms` | `wst(iwst)%wco%wgn, wgn(iwgn)%tmpmx(mo), wgn(iwgn)%tmpmn(mo), wgn(iwgn)%lat, wgn_pms(iwgn)%latsin, wgn_pms(iwgn)%daylth, wgn_pms(iwgn)%daylmn` |
| [sym:time_module] | `time` | `time%day_start` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%urban, db_mx%ovn` |
| [sym:plant_data_module] | `pcomdb, pldb` | `pcomdb(icom)%plants_com, pcomdb(icom)%pl(ipl)%cpnm, pcomdb(icom)%pl(ipl)%igro, pcomdb(icom)%pl(ipl)%db_num, pcomdb(icom)%pl(ipl)%rsdin, pldb(idp)%days_mat, pldb(idp)%t_base, pldb(idp)%typ, pcomdb(icom)%rot_yr_ini, pcomdb(icom)%name, pcomdb(icom)%pl(ipl)%phuacc, pcomdb(icom)%pl(ipl)%fr_yrmat, pldb(idp)%chtmx` |
| [sym:landuse_data_module] | `lum, lum_str, overland_n, urbdb` | `lum(ilum)%urb_ro, lum(ilum)%urb_lu, lum(ilum)%ovn, lum_str(ilum)%cons_prac, overland_n(idb)%name, overland_n(idb)%ovn, urbdb(idb)%urbnm` |
| [sym:mgt_operations_module] | `sched` | `sched(isched)%num_ops, sched(isched)%mgt_ops(1)%jday, sched(isched)%mgt_ops(iop)%jday, sched(isched)%mgt_ops(iop)%op, sched(isched)%first_op` |
| [sym:urban_data_module] | `urbdb` | `urbdb(idb)%urbnm` |
| [sym:conditional_module] | `overland_n` | `overland_n(idb)%name, overland_n(idb)%ovn` |
| [sym:organic_mineral_mass_module] | `pl_mass, soil1` | `pl_mass(j)%tot, pl_mass(j)%ab_gr, pl_mass(j)%leaf, pl_mass(j)%stem, pl_mass(j)%seed, pl_mass(j)%root, pl_mass(j)%yield_tot, pl_mass(j)%yield_yr, pl_mass(j)%rsd, soil1(j)%pl, pl_mass(j)%tot(ipl), pl_mass(j)%ab_gr(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%seed(ipl), pl_mass(j)%root(ipl), pl_mass(j)%yield_tot(ipl), pl_mass(j)%yield_yr(ipl), pl_mass(j)%rsd(ipl), soil1(j)%pl(ipl), pl_mass(j)%rsd(:), pl_mass(j)%rsd_tot, pl_mass(j)%rsd(ipl)%m, pl_mass(j)%rsd(ipl)%c, pl_mass(j)%rsd(ipl)%n, pl_mass(j)%rsd(ipl)%p` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%npl` | When `hru(j)%plant_cov` is zero, indicating no plant community is assigned to the HRU. | Set to zero so the HRU’s plant-community state reflects that no plants should be initialized or simulated. |
| `ipl` | When the HRU has a plant community and the routine is rebuilding state, `ipl` is first used as the community plant count and then reused as the loop index over plants. | Holds the number of plants for allocation, then becomes the per-plant loop counter used to initialize each plant slot. |
| `pcom(j)%plcur(ipl)%uptake` | For each plant after its active state is copied from the plant database, the routine assigns a fresh uptake array sized by soil layers. | Initialized to zero so later plant-water-uptake calculations can accumulate layer uptake from a clean starting state. |
| `pcom(j)%rsd_covfac` | After the residue factor for each plant is added and later averaged across the community. | Stores the community residue cover factor used later in cover/erosion calculations. |
| `cvm_com(j)` | After the mean residue-cover value is accumulated from all plants in the community. | Stores the HRU/community canopy-modifier sum that is later averaged and used in cover-related calculations. |
| `pcom(j)%pcomdb` | When the current plant-community database index is known for the HRU. | Records which plant-community database entry was used so later routines can trace the source community definition. |
| `pcom(j)%rot_yr` | For every HRU with a plant community, after the plant community database rotation-year initial value is copied. | Initializes the community’s rotation year so date-table and management scheduling can start from the correct rotation position. |
| `pcom(j)%laimx_sum` | After each plant’s maximum LAI contribution is added. | Accumulates the sum of plant maximum LAI values used later for canopy interception and community-level canopy scaling. |
| `pl_mass(j)%rsd(:)` | Immediately after residue-mass initialization, when the routine sets each plant residue array to the zero template and later adds per-plant residue mass. | Holds per-plant residue mass and nutrient pools for all plant slots in the community. |
| `pl_mass(j)%rsd_tot` | After all per-plant residue pools have been added. | Stores the total residue pool across all plants, used as the community-wide residue summary. |
| `pcom(j)%pl(ipl)` | For each plant after the community plant name, growth flag, residue input, and biomass-related fields are copied from the database. | Contains the plant name for each active community slot so later routines can reference the selected species or cultivar. |
| `pcom(j)%plcur(ipl)%gro` | When the active plant is marked as growing (`pcom(j)%plcur(ipl)%gro == "y"`). | Carries the plant’s grow/dormant flag copied from the database and controls whether root, seed, and partition initialization runs. |
| `pcom(j)%plcur(ipl)%idorm` | For each plant, the routine explicitly sets dormancy before growth initialization unless later logic changes it. | Marks the plant dormant at initialization until growth-state routines or later seasonal logic change it. |
| `pl_mass(j)%rsd(ipl)%m` | During the residue initialization for each plant, after the residue mass template has been offset by the database residue input. | Stores the plant’s initial residue mass on the soil surface. |
| `pl_mass(j)%rsd(ipl)%c` | During the same residue initialization block. | Stores the plant’s initial residue carbon mass, derived from residue mass using the fixed carbon fraction. |
| `pl_mass(j)%rsd(ipl)%n` | During the same residue initialization block. | Stores the plant’s initial residue nitrogen mass, derived from residue mass using the fixed N fraction. |
| `pl_mass(j)%rsd(ipl)%p` | During the same residue initialization block. | Stores the plant’s initial residue phosphorus mass, derived from residue mass using the fixed P fraction. |
| `iwst` | After the HRU’s object index is read and the object’s weather station pointer is followed. | Holds the weather-station index for the current HRU so the routine can read monthly climate-generator values and day-length parameters. |
| `pcom(j)%plcur(ipl)%phumat` | When the active plant species is being initialized and canopy height is assigned. | Stores the initialized heat units to maturity for the active plant, based on species type and climate-driven scheduling rules. |
| `pldb(idp)%typ` | When the active plant species is looked up from the plant database and its category is copied into the active state. | Used as the species-type selector for annual, perennial, and special dormancy/planting-day branches. |
| `sched(isched)%first_op` | After the management schedule is scanned. | Stores the first operation that should run for the current simulation year, based on the schedule and rotation-year logic. |
| `hru(j)%cur_op` | After `sched(isched)%first_op` is set. | Initializes the HRU’s current management operation pointer so later management execution starts at the right schedule entry. |
| `pcom(j)%name` | After the plant community name is copied from the database. | Stores the active plant-community name used in outputs and later community-level references. |
| `pcom(j)%plcur(ipl)%phuacc` | When the active plant heat-unit accumulation is copied from the plant community database. | Stores the initial fraction of accumulated heat units for the active plant, which later canopy and maturity calculations use. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 4:1.1.12 | LS_USLE topographic factor | $LS_{USLE}=(\frac{L_{hill}}{22.1})^m*(65.41*sin^2(\alpha_{hill})+4.56*sin\alpha_{hill}+0.065)$ | usle_ls = (slope_len/22.128)^xm * (65.41*sin^2(alpha)+4.56*sin(alpha)+0.065); 22.128 vs theory 22.1 is a minor rounding difference. |
| 4:1.1.13 | Slope length exponent m | $m=0.6*(1-exp[-35.835*slp])$ | xm = .6*(1-exp(-35.835*slope)); exact match for m=0.6*(1-exp(-35.835*slp)). |
| 5:1.1.3 | Base-zero daily heat unit for scheduling | $HU_0=\overline T_{av}$ | Base-zero annual heat units are accumulated from positive daily mean temperature, then 15% of that annual total is used to identify planting day for annual scheduling. |

## Lineage

`plant_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 14 non-merge commit(s) since, most recently `f1d1ac1` (2026-04-22, "Hopefulle some finally cleanup to implement cswat == 3 to cswat = 1. Added/chang…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `plant_init.f90` are listed.

- `f1d1ac1` (2026-04-22) — Hopefulle some finally cleanup to implement cswat == 3 to cswat = 1. Added/changed subroutines in external specificaitons due to subroutine…
- `3e18acf` (2026-02-17) — Integrate CENTURY residue/N updates and root-fraction tracking changes
- `0d74307` (2026-01-07) — Fixed Warnings, removed unused variable declarations and update external function references
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `fd3d90f` (2025-12-08) — made changes to include residue partition fractions and read them in plant.plt and initilize the initial residue amounts.
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'plant_init' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 11 source-backed steps and kept each step aligned to visible line ranges.
- Source uncertainty: `soil_module`, `maximum_data_module`, `urban_data_module`, `conditional_module`, and `landuse_data_module` had no candidate outside references resolved in the packet, so their imported names were inferred only from usage in `plant_init.f90`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
