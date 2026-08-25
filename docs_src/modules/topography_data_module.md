---
kind: module
symbol: topography_data_module
title: topography_data_module
status: filled
source_hash: 86b3653772839db5
version_label: SWAT+ 62.0.0
variables:
  topo_db: Allocatable array of `topography_db` records owned by this module. It is populated
    by `topo_read` from `topography.hyd`, then queried by `hru_read`, `ru_read`, `time_conc_init`,
    and `topohyd_init` to resolve named topography entries and use slope, slope length, lateral-flow
    length, stream distance, and deposition coefficient values.
  field_db: Allocatable array of `fields_db` records owned by this module. It is populated
    by `field_read` from `field.fld`, then queried by `hru_read`, `ru_read`, and `topohyd_init`
    to resolve named field entries and use field length, width, and angle values.
type_components:
  topography_db:
    name: Character label for the topography record; used as the key that other routines match
      against when resolving `topo_db` entries.
    slope: hru_slp(:) |m/m           |average slope steepness in HRU
    slope_len: slsubbsn(:)   |m             |average slope length for erosion
    lat_len: slsoil(:)     |m             |slope length for lateral subsurface flow
    dis_stream: dis_stream(:) |m             |average distance to stream
    dep_co: '|              |deposition coefficient'
  fields_db:
    name: Character label for the field record; used as the key that other routines match
      against when resolving `field_db` entries.
    length: '|m             |field length for wind erosion'
    wid: '|m             |field width for wind erosion'
    ang: '|deg           |field angle for wind erosion'
type_summaries:
  topography_db: A named topography lookup record for one shared topographic parameter set
    used by HRUs and routing units.
  fields_db: A named field geometry record for one shared field parameter set used in HRU
    setup and wind-erosion geometry.
---

<!-- facts:header -->

Declares the shared topography and field database types plus the allocatable tables that hold loaded topographic and field parameter records. Other SWAT+ readers and initialization routines populate these tables from input files and then use them to resolve HRU and routing-unit geometry, slope, and field-erosion parameters.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it contains no procedures. Its allocatable arrays are populated by separate file readers, with `topo_read` filling `topo_db` and `field_read` filling `field_db` before later setup routines consume them.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:field_read] | `field.fld` | `field_db` | Reads `field.fld`, counts records, allocates `field_db`, and stores each parsed field record for later lookup by name. |
| [sym:hru_read] | `hru-data.hru` | `topo_db, field_db` | Reads HRU definitions and resolves each HRU's `topo` and `field` names against `topo_db` and `field_db` so later HRU setup can use numeric database indices. |
| [sym:ru_read] | `rout_unit.rtu` | `topo_db, field_db` | Reads routing-unit definitions and resolves routing-unit topography and field names against `topo_db` and `field_db`, copying field dimensions into the routing-unit record. |
| [sym:time_conc_init] | `none extracted` | `topo_db` | Uses `topo_db` slope and slope-length values while computing routing-unit and HRU travel times; it does not read an input file from this module. |
| [sym:topo_read] | `topography.hyd` | `topo_db` | Reads `topography.hyd`, counts records, allocates `topo_db`, and loads each topography record into the shared database. |
| [sym:topohyd_init] | `none extracted` | `topo_db, field_db` | Copies selected topography and field database values into each HRU's live state during initialization; it does not read a file directly from this module. |

## Key Consumers

The module is used by input readers that load and resolve database names, by time-of-concentration setup that needs topographic slopes, and by HRU initialization that copies the selected topography and field parameters into live HRU state.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:field_read] | topography_data_module | Populates the module-owned `field_db` array with parsed field records, making the field database available to later lookups. |
| [sym:hru_read] | topography_data_module | Uses `topo_db` and `field_db` to resolve each HRU's named topography and field references into numeric database indices for later HRU setup. |
| [sym:ru_read] | topography_data_module | Uses `topo_db` and `field_db` to resolve routing-unit topography and field names; the matched field record also supplies field length, width, and angle to the routing-unit state. |
| [sym:time_conc_init] | topography_data_module | Uses `topo_db` slope and slope-length values in the routing-unit and HRU time-of-concentration calculations. |
| [sym:topo_read] | topography_data_module | Allocates and fills the module-owned `topo_db` array from `topography.hyd`, establishing the shared topography database. |
| [sym:topohyd_init] | topography_data_module | Copies the selected topography and field database values into each HRU, setting HRU topographic names, slopes, slope lengths, lateral-flow lengths, stream distance, deposition coefficient, and field dimensions. |
| [sym:sd_channel_surf_link] | topography_data_module | The module is imported, but the extracted source shows no referenced symbols from it, so no traced runtime effect is visible in the available evidence. |

## Lineage

`topography_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `f1e61a3` (2024-10-08, "fixed tabs"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `topography_data_module.f90` are listed.

- `f1e61a3` (2024-10-08) — fixed tabs
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `topography_data_module` has no extracted module-level documentation comment.
- No lineage commits were resolved for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
