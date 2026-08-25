---
kind: module
symbol: urban_data_module
title: urban_data_module
status: filled
source_hash: 2ed5cd3aee407726
version_label: SWAT+ 62.0.0
variables:
  urbdb: Allocatable, saved array of `urban_db` records declared in `urban_data_module.f90:18`.
    It is the shared urban parameter database used throughout the model after `urban_parm_read`
    allocates and fills it from `urban.urb`; other readers such as `cs_urban_read` and `salt_urban_read`
    match their records to `urbdb(iu)%urbnm`, and process routines use fields such as `fimp`,
    `fcimp`, `dirtmx`, `thalf`, `urbcoef`, `curbden`, `tnconc`, `tpconc`, and `tno3conc`.
type_components:
  urban_db:
    urbnm: character(len=16) name of the urban land-use type used to cross-walk input records
      and HRU urban land-use codes.
    fimp: fraction of HRU area that is impervious; used by urban runoff, regression, erosion,
      and load partitioning routines.
    fcimp: fraction of HRU that is classified as directly connected impervious; used to blend
      pervious and impervious runoff.
    curbden: km/ha curb length density used to convert street dirt mass to area-based loading.
    urbcoef: 1/mm wash-off coefficient for removal of constituents from an impervious surface.
    dirtmx: kg/curb km maximum amount of solids allowed to build up on impervious surfaces.
    thalf: days time for solids on impervious areas to build up to one-half of the maximum
      level.
    tnconc: mg N/kg sed concentration of total nitrogen in suspended solid load from impervious
      areas.
    tpconc: mg P/kg sed concentration of total phosphorus in suspended solid load from impervious
      areas.
    tno3conc: mg NO3-N/kg sed concentration of nitrate in suspended solid load from impervious
      areas.
    urbcn2: curve number for impervious areas under moisture condition II.
type_summaries:
  urban_db: One `urban_db` record represents the parameter set for a single urban land-use
    type.
---

<!-- facts:header -->

`urban_data_module` owns the shared urban land-use parameter table `urbdb` and the `urban_db` derived type that defines each urban record. It serves as in-memory storage for urban names, impervious fractions, street-dirt buildup and wash-off parameters, constituent concentrations, and urban curve numbers used by urban runoff, erosion, sweeping, and input-reader routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

`urban_data_module` is a declaration-and-storage module; it does not contain startup procedures. Its `urbdb` array is populated by reader routines, especially `urban_parm_read`, which allocates the array and reads `urban.urb` into it. Other routines then look up urban records by name or by the HRU's urban land-use index.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:urban_parm_read] | `urban.urb` | `urbdb` | Reads the urban land-use parameter database, counts records, allocates `urbdb`, and loads each `urban_db` entry into the shared module array. |
| [sym:cs_urban_read] | `cs_urban` | `urbdb` | Uses `urbdb(iu)%urbnm` to match each `cs_urban` urban type name to the correct urban database slot before filling constituent concentrations. |
| [sym:salt_urban_read] | `salt_urban` | `urbdb` | Uses `urbdb(iu)%urbnm` to match each `salt_urban` urban type name to the correct urban database slot before filling salt-ion concentrations. |
| [sym:plant_init] | `urban.urb` | `urbdb` | Cross-walks an HRU urban land-use name to an index in `urbdb` so the HRU land-use state can store the correct urban database slot. |

## Key Consumers

Urban input readers and urban-process routines import this module to access the shared urban database. Some routines use the stored urban names to resolve input files, while runoff, erosion, sweeping, and urban load routines use the parameter fields to compute impervious runoff and wash-off behavior.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cs_urban_read] | urban_data_module | The urban database supplies `urbdb(iu)%urbnm`, letting the reader match each `cs_urban` urban type to the correct shared urban slot before storing constituent concentrations. |
| [sym:plant_init] | urban_data_module | The module supplies urban land-use names so the HRU's urban land-use string can be cross-walked to an index in `urbdb` before the HRU land-use state is finalized. |
| [sym:salt_urban_read] | urban_data_module | The reader uses `urbdb(iu)%urbnm` to match each urban type in `salt_urban` to the correct urban database row before loading salt-ion concentrations. |
| [sym:urban_parm_read] | urban_data_module | This routine allocates and fills `urbdb`, making the module the shared in-memory destination for the parsed urban parameter table from `urban.urb`. |
| [sym:ero_ovrsed] | urban_data_module | `urbdb(ulu)%fimp` reduces splash and overland-flow sediment for urban HRUs by scaling the computed erosion on impervious land. |
| [sym:hru_sweep] | urban_data_module | `urbdb(ulu)%dirtmx` and `urbdb(ulu)%thalf` provide the street-dirt maximum and buildup half-time used to convert between dirt mass and buildup time during sweeping. |
| [sym:hru_urban] | urban_data_module | `urbdb(ulu)%fimp`, `dirtmx`, `urbcoef`, `tnconc`, `tpconc`, and `tno3conc` control the impervious fraction, dirt buildup, wash-off rate, and nutrient partitioning used in daily urban loading. |
| [sym:hru_urbanhr] | urban_data_module | `urbdb(ulu)%dirtmx`, `urbcoef`, `tnconc`, `tpconc`, `tno3conc`, and `fimp` drive subdaily street dirt buildup, wash-off, and associated solids and nutrient loads. |
| [sym:regres] | urban_data_module | `urbdb(ulu)%fimp` supplies the impervious-fraction term used in the USGS urban regression equation for constituent loads. |
| [sym:sq_daycn] | urban_data_module | `urbdb(ulu)%fcimp` provides the directly connected impervious fraction used to blend pervious and impervious runoff in the daily curve-number calculation. |
| [sym:sq_greenampt] | urban_data_module | `urbdb(ulu)%fcimp` sets the impervious runoff fraction in the Green-Ampt runoff calculation so the routine can split runoff between pervious and urban impervious branches. |
| [sym:pl_waterup] | urban_data_module | The procedure imports the module, but the extracted refs do not show a direct `urbdb` access; its exact use is uncertain from the packet. |
| [sym:surface] | urban_data_module | The procedure imports the module for urban-HRU support, but the extracted refs do not show a direct `urbdb` access; the precise effect is not visible in the packet. |

## Lineage

`urban_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `urban_data_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `urban_data_module` has no extracted module-level documentation comment.
- Source packet resolved no lineage commits for this span.
- pl_waterup and surface import the module, but the extracted references do not show direct `urbdb` access, so their module-level effect is marked uncertain.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
