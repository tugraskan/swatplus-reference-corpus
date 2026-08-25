---
kind: procedure
symbol: hru_lte_read
title: hru_lte_read
status: filled
source_hash: a7b2c77f98367fca
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from `hru-lte.hru`; the routine uses it to skip the file's
    first header record during both the scan pass and the data-read pass.
  header: Temporary second header line read from `hru-lte.hru`; it is skipped before scanning
    or loading the actual database records.
  eof: I/O status flag used to detect end-of-file or read failure while scanning and loading
    `hru-lte.hru`.
  imax: Maximum record index found in `hru-lte.hru`; it determines the size of `hlt_db` before
    the file is reread.
  i_exist: Logical flag from `inquire` that tells the routine whether the configured HRU LTE
    input file exists.
  grow_start: Working copy of the start-of-growing-season day index chosen for the current
    HRU, used to count heat units.
  grow_end: Working copy of the end-of-growing-season day index chosen for the current HRU,
    used to count heat units.
  ipl: Loop index used to search `pldb` for the plant record matching the HRU LTE plant name.
  istart: Loop index used to search `dtbl_lum` for the start decision table matching `igrow1`.
  iend: Loop index used to search `dtbl_lum` for the end decision table matching `igrow2`.
  itext: Loop index used to search `soil_lte` for the soil texture matching the HRU LTE texture
    code.
  rtos: Derived fraction used as one of the shape-curve inputs passed to `ascrv`; it is computed
    from the curve-number retention parameter for CN1 versus CN2.
  rto3: Derived fraction used as one of the shape-curve inputs passed to `ascrv`; it is computed
    from the curve-number retention parameter for CN3 versus CN1.
  a1: Constant initialized to 0.2 before the file scan; in this routine it is set but not
    otherwise used in the visible source.
  a2: Constant initialized to 0.8 before the file scan; in this routine it is set but not
    otherwise used in the visible source.
  i: Record index read from `hru-lte.hru` during the scan and load passes; it identifies the
    current HRU database row.
  isd_h: Loop counter that iterates through database rows when loading `hlt_db` after the
    file is rewound.
  k: Leading integer read with each HRU LTE record; it is a record prefix used to read the
    full `hlt_db(i)` entry.
  idb: Database index for the current HRU object; it points into `hlt_db` after being copied
    from `ob(icmd)%props`.
  mo: Current month index used while accumulating heat units from monthly weather generator
    temperatures.
  qn1: Intermediate retention/curve-number value used to compute `smx` and the curve-number
    shape parameters.
  qn3: Intermediate retention/curve-number value used to compute the CN3-based shape parameter.
  s3: Retention parameter for curve number 3, used in the `rto3` calculation.
  sumul: Water held at saturation in the soil profile; used with `sumfc` as input to `ascrv`.
  sumfc: Water held at field capacity in the soil profile; used with `sumul` as input to `ascrv`.
  xi: Temporary angular/day-of-year value computed during the heat-unit section; it is assigned
    but not used further in the visible source.
  xx: Latitude converted to radians for sine/cosine calculations that set seasonal terms.
  sin: Intrinsic sine function called to derive the seasonal latitude term `yls` and the slope
    term `sin_sl`.
  cos: Intrinsic cosine function called to derive the seasonal latitude term `ylc`.
  iwgn: Weather-generator index taken from the HRU's weather-station linkage; it selects monthly
    temperatures.
  iplt: Plant-index copy of `hlt(i)%iplant`; it selects the plant database record used for
    heat-unit calculations.
  imo: Month counter used alongside `mo` while walking through the 365-day heat-unit accumulation
    loop.
  hu_init: Initial guess flag for heat-unit season logic; the code assigns 0.15 or 0.85 based
    on whether the growing season crosses year end, but the visible source does not use it
    later.
  phutot: Accumulator for total potential heat units over the growing season before scaling
    to `hlt(i)%phu`.
  iday: Day-of-year loop counter used to accumulate heat units over 365 days.
  tave: Average daily temperature derived from monthly weather-generator maxima and minima
    during heat-unit accumulation.
  phuday: Daily heat units above the plant base temperature before they are added to `phutot`.
  xm: Exponent used in the USLE slope-length factor calculation.
  sin_sl: Sine of the landscape slope angle, used in the USLE slope-length factor equation.
  ch_len: Temporary channel length value used when computing time of concentration with the
    Kirpich equation.
  ch_sl: Temporary channel slope value read from the HRU database; it is assigned in the concentration-time
    section but not used in the visible formula.
  sd_sl: Temporary slope-length term used in the Kirpich time-of-concentration calculation;
    the visible source assigns it to 0 and never updates it before use, so that formula appears
    suspicious.
  msd_h: Number of HRU LTE landscape objects used to size the landscape output arrays.
uses:
  maximum_data_module: The `maximum_data_module` provides the database-size limits that let
    this routine search the `plants.plt` and `lum.dtl` tables by index. `db_mx%plantparm`
    bounds the plant crosswalk loop, and `db_mx%dtbl_lum` bounds the decision-table crosswalk
    loops.
  plant_data_module: The `plant_data_module` supplies the plant database used to convert each
    HRU LTE plant name into a plant index and to get plant properties for heat-unit accumulation.
    `pldb(ipl)%plantnm`, `pldb(iplt)%t_base`, and `pldb(iplt)%typ` determine which plant record
    matches and how the routine computes and caps `hlt(i)%phu`.
  hru_lte_module: The `hru_lte_module` holds both the persistent HRU LTE database (`hlt_db`)
    and the per-object dynamic state (`hlt`) that this routine fills. The routine copies file
    data into `hlt_db`, then derives each object's live properties such as area, curve number,
    plant linkage, seasonal markers, hydraulic parameters, and initial soil water for later
    model steps.
  hydrograph_module: The `hydrograph_module` connects HRU LTE objects to the routed simulation
    network. `sp_ob%hru_lte` and `sp_ob1%hru_lte` define how many HRU LTE objects exist and
    where their object-command numbering starts, while `ob(icmd)%props`, `ob(icmd)%name`,
    and `ob(icmd)%wst` let the routine map each HRU LTE object to its database row, object
    name, and weather station.
  input_file_module: The `input_file_module` supplies the configured filename that this routine
    opens. `in_hru%hru_ez` is the user-facing switch for the HRU LTE input file, so it determines
    whether the routine can read any HRU LTE database records at all.
  output_landscape_module: The `output_landscape_module` contains the landscape water-balance
    arrays that are allocated to match the number of HRU LTE objects. `hltwb_d`, `hltwb_m`,
    `hltwb_y`, and `hltwb_a` are initialized here because later output routines need per-object
    storage for soil-water diagnostics such as `sw_init`.
  climate_module: The `climate_module` provides the weather-generator monthly temperature
    arrays used to estimate heat units for each HRU LTE plant. `wst(iwst)%wco%wgn` maps the
    HRU to a weather generator, and `wgn(iwgn)%tmpmx(mo)`/`tmpmn(mo)` supply the monthly temperatures
    used in the growing-season accumulation loop.
  time_module: The `time_module` contributes the current simulation month through `time%mo`.
    That month value is used when computing the angular season term and when initializing
    the monthly walk through the weather-generator temperature arrays.
  soil_data_module: The `soil_data_module` supplies the texture-to-property lookup table used
    to derive soil-water and hydraulic attributes from the HRU LTE texture code. `soil_lte(itext)%texture`,
    `awc`, `por`, and `scon` determine the profile water capacity, porosity, conductivity,
    and derived water-state values for each HRU.
  conditional_module: The `conditional_module` provides the decision-table names used to crosswalk
    HRU LTE growing-season markers into table indices. `dtbl_lum(istart)%name` and `dtbl_lum(iend)%name`
    let the routine translate `igrow1` and `igrow2` from the HRU database into the start and
    end decision-table references stored in `hlt(i)`.
---

<!-- facts:header -->

Reads the HRU LTE database file, builds the shared HRU-LTE data structures, and crosswalks each HRU-LTE object to plants, decision tables, weather, soil, and output-state arrays.

## Bottom Line

hru_lte_read is the setup routine for HRU LTE landscape units. It opens the configured `hru-lte.hru` file, scans it to determine how many database rows exist, allocates the `hlt_db` and `hlt` arrays plus the landscape output arrays, then reads each database record into `hlt_db`.

After the database is loaded, the routine populates each `hlt(i)` object by linking it to the corresponding connectivity object, plant entry, decision-table entries, weather generator, and soil texture. It also derives calibration and initial-condition values such as curve number limits, heat units, USLE factors, time of concentration, hydraulic conductivity, and initial soil water, so later HRU LTE simulation steps can use a fully prepared state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization after the input-file module has selected the HRU LTE file and after the spatial object/connectivity tables, plant database, decision tables, climate data, and soil database have already been prepared. Its results feed the later HRU LTE landscape simulation because `hlt_db` and `hlt` hold the object properties, derived parameters, and initial conditions that downstream hydrology, plant growth, erosion, and output routines use.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the HRU LTE input file is available. | The routine tests `in_hru%hru_ez` with `inquire` and, if the file is missing or set to `null`, allocates a minimal `hlt_db(0:0)` array instead of loading any records. |
| 2. Scan the file to determine the highest HRU database index. | The routine opens unit 1, skips the title and header records, then reads record indices until end-of-file to compute `imax`. |
| 3. Allocate the HRU LTE database and dynamic object arrays. | Using `imax` and `sp_ob%hru_lte`, the routine allocates `hlt_db`, `hlt`, and the daily/monthly/yearly/annual landscape output arrays sized by `msd_h`. |
| 4. Rewind the file and load each structured database record. | The routine rewinds the file, skips the title and header again, then loops over the database rows and reads each line into `hlt_db(i)`. |
| 5. Walk each HRU LTE object and map it to the connectivity database. | For each object, the routine computes the command index `icmd`, looks up the property index `idb`, and copies the object name, property pointer, object number, area, curve number, ET/percolation/revap/tile-drain coefficients, plant name, stress, and soil depth into `hlt(i)`. |
| 6. Derive curve-number and seasonal geometry terms. | The routine transforms `abf`, computes `qn1`, `qn3`, `smx`, `s3`, `rto3`, `rtos`, and seasonal latitude terms, then initializes plant-growth placeholders such as `phu`, `dm`, `alai`, and `g`. |
| 7. Crosswalk the plant, growing-season, and weather references. | The routine matches the HRU plant name to `pldb`, finds the `dtbl_lum` entries for `igrow1` and `igrow2`, and reports missing crosswalks to unit 9001. |
| 8. Accumulate heat units over the growing season. | Using the linked weather station and weather generator, the routine loops over 365 days, adds positive daily heat units above the plant base temperature, and converts the total to `hlt(i)%phu`, with caps for annual crop types. |
| 9. Compute USLE slope-length and composite erosion factors. | The routine calculates the USLE slope-length factor from slope and slope length, then combines it with `uslek`, `uslep`, and `uslec` to form `hlt(i)%uslefac`. |
| 10. Estimate time of concentration when it is not preset. | If `hlt_db(idb)%tc` is near zero, the routine computes a Kirpich-style concentration time from channel length and slope and then converts it to minutes. |
| 11. Crosswalk the soil texture and derive soil-water state. | The routine matches the HRU texture to `soil_lte`, computes available water, porosity, hydraulic conductivity, initial soil water, and the S-curve shape inputs, then calls `ascrv` to obtain `wrt1` and `wrt2`. |
| 12. Finish the pass and close the input file. | After converting `tc` to seconds, leaving the object loop, and closing unit 1, the routine returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantparm, db_mx%dtbl_lum` |
| [sym:plant_data_module] | `pldb` | `pldb(ipl)%plantnm, pldb(iplt)%t_base, pldb(iplt)%typ` |
| [sym:hru_lte_module] | `hlt, hlt_db` | `hlt(i)%name, hlt(i)%props, hlt(i)%obj_no, hlt(i)%km2, hlt_db(idb)%dakm2, hlt(i)%cn2, hlt_db(idb)%cn2, hlt(i)%etco, hlt_db(idb)%etco, hlt(i)%perco, hlt_db(idb)%perco, hlt(i)%tdrain, hlt_db(idb)%tdrain, hlt(i)%revapc, hlt_db(idb)%revapc, hlt(i)%plant, hlt_db(idb)%plant, hlt(i)%stress, hlt_db(idb)%stress, hlt(i)%soildep, hlt_db(idb)%soildep, hlt_db(idb)%abf, hlt(i)%smx, hlt_db(idb)%xlat, hlt(i)%yls, hlt(i)%ylc, hlt(i)%phu, hlt(i)%dm, hlt(i)%alai, hlt(i)%g, hlt(i)%iplant, hlt_db(idb)%igrow1, hlt(i)%start, hlt_db(idb)%igrow2, hlt(i)%end, hlt_db(idb)%uslels, hlt_db(idb)%slopelen, hlt(i)%uslefac, hlt_db(idb)%uslek, hlt_db(idb)%uslep, hlt_db(idb)%uslec, hlt_db(idb)%tc, hlt_db(idb)%slope, hlt_db(idb)%text, hlt(i)%awc, hlt(i)%por, hlt(i)%sc, hlt(i)%sw, hlt_db(idb)%sw, hlt(i)%hk, hlt_db(idb)%cn3_swf, hlt(i)%wrt2` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru_lte, sp_ob1%hru_lte, ob(icmd)%props, ob(icmd)%name, ob(icmd)%wst` |
| [sym:input_file_module] | `in_hru` | `in_hru%hru_ez` |
| [sym:output_landscape_module] | `hltwb_d, hltwb_m, hltwb_y, hltwb_a` | `hltwb_d(i)%sw_init` |
| [sym:climate_module] | `wst, wgn` | `wst(iwst)%wco%wgn, wgn(iwgn)%tmpmx(mo), wgn(iwgn)%tmpmn(mo)` |
| [sym:time_module] | `time` | `time%mo` |
| [sym:soil_data_module] | `soil_lte` | `soil_lte(itext)%texture, soil_lte(itext)%awc, soil_lte(itext)%por, soil_lte(itext)%scon` |
| [sym:conditional_module] | `dtbl_lum` | `dtbl_lum(istart)%name, dtbl_lum(iend)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `icmd` | For each HRU LTE object in `do i = 1, sp_ob%hru_lte` after `icmd` is computed from `sp_ob1%hru_lte + i - 1`. | `icmd` becomes the current HRU LTE object-command number so the routine can pull connectivity data from `ob(icmd)` and assign the correct weather-station link. |
| `hlt(i)%name` | When the loop processes a specific HRU LTE object and copies `ob(icmd)%name` into the dynamic object. | `hlt(i)%name` stores the routed object's name so the dynamic HRU LTE record carries the connectivity name for later identification and output. |
| `hlt(i)%props` | When the loop processes a specific HRU LTE object and copies `ob(icmd)%props` into the dynamic object. | `hlt(i)%props` stores the property-table index associated with the object so later routines can trace the object back to its database row. |
| `hlt(i)%obj_no` | When the loop processes a specific HRU LTE object and copies the command index into the dynamic record. | `hlt(i)%obj_no` stores the object-command number for the HRU LTE element so later routines know which connectivity object this dynamic state belongs to. |
| `hlt(i)%km2` | When the loop copies `hlt_db(idb)%dakm2` into the dynamic object. | `hlt(i)%km2` becomes the drainage area in square kilometers used by subsequent hydrologic and concentration-time calculations. |
| `hlt(i)%cn2` | When the loop copies and then bounds the curve number from the database row. | `hlt(i)%cn2` stores the HRU's condition-II curve number, clipped to the valid range used by the model's runoff and retention formulas. |
| `hlt(i)%etco` | When the loop copies `hlt_db(idb)%etco` into the dynamic object. | `hlt(i)%etco` stores the evapotranspiration coefficient used by later water-balance calculations. |
| `hlt(i)%perco` | When the loop copies `hlt_db(idb)%perco` into the dynamic object. | `hlt(i)%perco` stores the soil percolation coefficient that later controls drainage through the profile. |
| `hlt(i)%tdrain` | When the loop copies `hlt_db(idb)%tdrain` into the dynamic object. | `hlt(i)%tdrain` stores the tile-drain design time used later in subsurface drainage behavior. |
| `hlt(i)%revapc` | When the loop copies `hlt_db(idb)%revapc` into the dynamic object. | `hlt(i)%revapc` stores the shallow-aquifer evaporation coefficient for later groundwater-to-ET calculations. |
| `hlt(i)%plant` | When the loop copies `hlt_db(idb)%plant` into the dynamic object. | `hlt(i)%plant` stores the plant name associated with the HRU so the routine can crosswalk it to `pldb` and later growth routines can use the same plant identity. |
| `hlt(i)%stress` | When the loop copies `hlt_db(idb)%stress` into the dynamic object. | `hlt(i)%stress` stores the plant-stress calibration factor used by later growth and water-stress logic. |
| `hlt(i)%soildep` | When the loop copies `hlt_db(idb)%soildep` into the dynamic object. | `hlt(i)%soildep` stores the soil-profile depth used to scale soil texture properties into profile-level water capacity and porosity. |
| `hlt_db(idb)%abf` | When the routine transforms `hlt_db(idb)%abf` with `EXP(-hlt_db(idb)%abf)`. | `hlt_db(idb)%abf` is converted from its input form into the exponential groundwater alpha factor used by later aquifer-response calculations. |
| `hlt(i)%smx` | When the routine computes `hlt(i)%smx = 254. * (100. / qn1 - 1.)`. | `hlt(i)%smx` stores the maximum soil-water retention parameter derived from the curve-number relationship, and it is later used to derive the S-curve shape and runoff response. |
| `hlt(i)%yls` | When the routine computes `hlt(i)%yls = SIN(xx)` after converting latitude to radians. | `hlt(i)%yls` stores the sine of latitude for seasonal geometry calculations used in downstream phenology or radiation-related routines. |
| `hlt(i)%ylc` | When the routine computes `hlt(i)%ylc = COS(xx)` after converting latitude to radians. | `hlt(i)%ylc` stores the cosine of latitude for seasonal geometry calculations used in downstream phenology or radiation-related routines. |
| `hlt(i)%phu` | When the routine sets `hlt(i)%phu` from accumulated heat units and possibly caps it for annual crops. | `hlt(i)%phu` stores the estimated potential heat units to maturity for the current HRU plant setup, which later growth routines use to schedule development. |
| `hlt(i)%dm` | When the routine initializes `hlt(i)%dm = 0.` before any growth simulation. | `hlt(i)%dm` starts as zero biomass so later plant-growth routines can accumulate biomass from a known initial state. |
| `hlt(i)%alai` | When the routine initializes `hlt(i)%alai = .15`. | `hlt(i)%alai` stores the starting leaf area index used as the initial canopy condition for later growth and evapotranspiration calculations. |
| `hlt(i)%g` | When the routine initializes `hlt(i)%g = 0.`. | `hlt(i)%g` starts as zero growth-state value so later plant-development code can update it from a clean initial condition. |
| `hlt(i)%iplant` | When the routine finds a matching plant name in `pldb` and assigns its index to `hlt(i)%iplant`. | `hlt(i)%iplant` becomes the plant database index for the HRU, letting later code access plant parameters such as base temperature and type. |
| `hlt(i)%start` | When the routine finds a matching start decision table name in `dtbl_lum`. | `hlt(i)%start` stores the decision-table index for the HRU's growing-season start, which later code uses to interpret seasonal timing. |
| `hlt(i)%end` | When the routine finds a matching end decision table name in `dtbl_lum`. | `hlt(i)%end` stores the decision-table index for the HRU's growing-season end, which later code uses to interpret seasonal timing. |

## File I/O

<!-- facts:io -->


## Lineage

`hru_lte_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_lte_read.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_lte_read' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 12 source-backed steps and aligned them to visible line ranges.
- The visible source assigns `sd_sl = 0.` and then uses it in the Kirpich time-of-concentration expression; that appears suspicious but is documented here exactly as written.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
