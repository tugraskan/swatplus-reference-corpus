---
kind: module
symbol: ru_module
title: ru_module
status: filled
source_hash: e4f1429b6a7a07ec
version_label: SWAT+ 62.0.0
variables:
  iru: integer routing-unit counter/index used to loop over routing units and select the current
    RU; initialized to 0 in the declaration and updated by readers and routing routines.
  mru_db: integer count of routing-unit database records found in `rout_unit.rtu`; initialized
    to 0 and set by `ru_read` during input parsing.
  ru_tc: allocatable real array holding routing-unit time of concentration values in hours
    for each RU index; allocated and initialized by `ru_read` and updated by `time_conc_init`.
  ru_n: allocatable real array holding weighted Manning's n values for each routing unit;
    allocated and initialized by `ru_read` and recomputed by `hru_fr_change` and `time_conc_init`.
  itsb: allocatable integer array used as an end-of-loop marker/counter for routing-unit processing;
    initialized to 0 by `ru_read`.
  ru: allocatable array of `ru_parameters` records holding the public routing-unit database
    state for each routing unit, including its name, drainage area, database links, and field
    settings.
type_components:
  ru_databases_char:
    elem_def: Name of the routing-element definition database file for the routing unit.
    elem_dr: Name of the routing-element delivery-ratio database file for the routing unit.
    toposub_db: Name of the topography/subbasin database file associated with the routing
      unit.
    field_db: Name of the field database file associated with the routing unit.
  ru_databases:
    elem_def: Index of the routing-element definition database record.
    elem_dr: Index of the routing-element delivery-ratio database record.
    toposub_db: Index of the topography/subbasin database record.
    field_db: Index of the field database record.
  field:
    name: Field name string used to identify the field record.
    length: Field length in meters used for wind erosion calculations.
    wid: Field width in meters used for wind erosion calculations.
    ang: Field angle in degrees used for wind erosion calculations.
  ru_parameters:
    name: Routing-unit name.
    da_km2: Routing-unit drainage area in square kilometers.
    dbsc: Character file-name references for the routing-unit's related databases.
    dbs: Integer indices that resolve those database references to loaded database records.
    field: Field geometry record used by the routing unit.
type_summaries:
  ru_databases_char: Character file-name references for the four routing-unit database inputs
    associated with one routing unit.
  ru_databases: Integer selectors that point to the resolved database records for one routing
    unit after the file names are matched to loaded databases.
  field: Wind-erosion field geometry and identifier stored for a routing unit.
  ru_parameters: Complete routing-unit parameter record containing the RU name, drainage area,
    linked database selectors, and field geometry.
---

<!-- facts:header -->

Defines the shared routing-unit state and record types used throughout SWAT+ routing. It owns the routing-unit index counters, the per-routing-unit database selector and time-of-concentration arrays, and the `ru` array of routing-unit parameter records. Startup and update routines such as `ru_read`, `time_conc_init`, `hru_fr_change`, and `ru_control` populate and consume this module so routing units can be read from input, assigned travel times and roughness, and used in hydrologic routing.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container whose arrays and counts are populated by reader/setup routines rather than by contained procedures. `ru_read` allocates and fills the routing-unit database state from `rout_unit.rtu`, while `time_conc_init` and `hru_fr_change` later update the shared derived values `ru_tc` and `ru_n`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:caltsoft_hyd] | `unit_4304` | `iru, mru_db, ru_tc, ru_n, itsb, ru` | Uses the shared routing-unit module while calibrating hydrology; the context packet does not show it initializing these variables, so ownership remains uncertain. |
| [sym:command] | `unit_out_hyd_sep` | `iru, mru_db, ru_tc, ru_n, itsb, ru` | Reads routing-unit module state during hydrologic command execution, especially when dispatching routing-unit control and writing RU outputs. |
| [sym:hru_fr_change] | `ru_elem_upd, lsu_elem_upd` | `iru, mru_db, ru_tc, ru_n, itsb, ru` | Recomputes `ru_n` after updated routing and landscape element fractions are read from the fraction-update files. |
| [sym:hyd_connect] | `looping.con, unit_*, unit_9004` | `iru, mru_db, ru_tc, ru_n, itsb, ru` | Reads the routing-unit connectivity file, then calls `ru_read` and `ru_read_elements` so RU state is available when building the watershed network. |
| [sym:ru_read] | `rout_unit.rtu` | `iru, mru_db, ru_tc, ru_n, itsb, ru` | Reads `rout_unit.rtu`, counts routing-unit records, allocates the module arrays, and fills each `ru` record plus related per-unit state. |
| [sym:time_conc_init] | `routing-unit state from `ru_module` and landscape/topography data` | `iru, mru_db, ru_tc, ru_n, itsb, ru` | Walks the routing units to compute weighted Manning's n and routing-unit time of concentration values. |

## Key Consumers

The module is imported by the routing, connectivity, initialization, and output paths that need shared RU identifiers or RU parameter state. The strongest consumers are `ru_read`, `time_conc_init`, `ru_control`, `hru_fr_change`, and the channel/surface-link routines that expand routing units into their member HRUs.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:hru_fr_change] | ru_module | `ru_module` holds the routing-unit roughness accumulator `ru_n`, which this routine recomputes after element fractions and HRU areas change so routing behavior stays consistent with the updated landscape configuration. |
| [sym:hyd_connect] | ru_module | This routine calls `ru_read` after connecting routing units, so the shared `ru` database and `mru_db` count are available when the watershed network is assembled. |
| [sym:ru_read] | ru_module | The routine populates routing-unit state into `ru_module` storage (`ru`, `mru_db`, and related arrays). That module is the shared home for the routing-unit database after the file is read. |
| [sym:time_conc_init] | ru_module | ru_module supplies the shared routing-unit arrays that this routine updates: ru_n for weighted Manning's n, ru for drainage area and database pointers, ru_tc for the final routing-unit time of concentration, and iru as the module-level routing-unit index used by the loops. |
| [sym:unit_hyd_ru_hru] | `ru_tc` | The RU module supplies `ru_tc`, the time of concentration for each routing unit. This routine uses those values to build unit hydrographs for RU inflows in the same way it does for HRUs. |
| [sym:channel_surf_link] | ru_module | The routing-unit branch uses `iru` to select a routing unit and expands that routing unit through `ru_def(iru)%num_tot` and `ru_def(iru)%num`. The module matters because it provides the shared RU index and data model used for that expansion. |
| [sym:dr_ru] | ru_module | This module supplies the routing-unit travel-time array `ru_tc` and the routing-unit index `iru` used in the ratio calculation. The calculated delivery ratio divides by `ru_tc(iru)`, so this state determines the normalization for every eligible element in the routing unit. |
| [sym:ru_control] | ru_module | `ru_module` matters because `ru(iru)%da_km2` provides the routing-unit drainage area used to scale element fractions and convert mm-based flow to routed volume. |
| [sym:sd_channel_surf_link] | ru_module | The ru module supplies the shared routing-unit index variable `iru`, which this routine assigns when it encounters an RU floodplain object. That index is needed to look up the RU's HRU list in `ru_def` and to keep the current RU selection consistent across the expansion loop. |
| [sym:command] | ru_module | The command driver sets `iru` when processing an RU object, then calls `ru_control` and later writes RU outputs using the shared routing-unit database stored in this module. |
| [sym:caltsoft_hyd] | ru_module | This calibration routine uses the shared routing-unit state while adjusting hydrologic parameters; the packet does not show a direct write to `ru_module`, so the exact role is not fully resolved. |
| [sym:calsoft_hyd] | ru_module | This calibration routine imports the routing-unit module while evaluating hydrologic response, but the packet did not resolve a direct `ru_module` state change. |
| [sym:calsoft_hyd_bfr] | ru_module | This buffered hydrology calibration wrapper imports the shared routing-unit module so the calibration subroutines can work with routing-unit state during parameter adjustment. |
| [sym:calsoft_hyd_bfr_et] | ru_module | This ET calibration routine imports the shared routing-unit module while testing hydrologic response, but no direct RU variable write was resolved in the packet. |
| [sym:calsoft_hyd_bfr_latq] | ru_module | This lateral-flow calibration routine imports the routing-unit module so the hydrology calibration can access shared RU state. |
| [sym:calsoft_hyd_bfr_perc] | ru_module | This percolation calibration routine imports the routing-unit module and uses the shared hydrologic state during calibration. |
| [sym:calsoft_hyd_bfr_pet] | ru_module | This PET calibration routine imports the routing-unit module so the hydrologic calibration can use shared RU state. |
| [sym:calsoft_hyd_bfr_surq] | ru_module | This surface-runoff calibration routine imports the routing-unit module and uses the shared hydrologic state while adjusting runoff behavior. |
| [sym:calsoft_plant] | ru_module | This plant calibration routine imports the shared routing-unit module so plant-water interactions can be evaluated in the same model state as the routing units. |
| [sym:calsoft_sed] | ru_module | This sediment calibration routine imports the routing-unit module so sediment behavior can be evaluated using the shared routing-unit state. |

## Lineage

`ru_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ru_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment was present in the source.
- Some reader roles, especially calibration wrappers, are inferred from import/use context rather than a directly resolved write to `ru_module` state.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
