---
kind: module
symbol: pathogen_data_module
title: pathogen_data_module
status: filled
source_hash: 59b53aef9475acdb
version_label: SWAT+ 62.0.0
variables:
  path_db: Allocatable module-wide array of `pathogen_db` records. `path_parm_read` allocates
    and fills it from `in_parmdb%pathcom_db` (`pathogens.pth` when configured), and downstream
    routines read it as shared pathogen parameter state. It is not itself a unit-bearing quantity;
    it stores one record per pathogen definition.
type_components:
  pathogen_db:
    pathnm: Pathogen name key, stored as a 16-character identifier and used to match constituent
      pathogen names to database records.
    do_soln: 1/day         |Die-off factor for pers bac in soil solution
    gr_soln: 1/day         |Growth factor for pers bac in soil solution
    do_sorb: 1/day         |Die-off factor for pers bac adsorbed to soil part
    gr_sorb: 1/day         |Growth factor for pers bac adsorbed to soil part
    kd: none          |Pathogen part coeff bet sol and sorbed phase in surf runoff
    t_adj: none          |temp adj factor for bac die-off/growth
    washoff: none          |frac of pers bac on foliage washed off by a rainfall event
    do_plnt: 1/day         |Die-off factor for pers bac on foliage
    gr_plnt: 1/day         |Growth factor for persistent pathogen on foliage
    fr_manure: none          |frac of manure containing active colony forming units (cfu)
    perco: none          |Pathogen perc coeff ratio of solution bacteria in surf layer
    det_thrshd: '# cfu/m^2     |Threshold detection level for less pers bac when pathogen
      levels'
    do_stream: 'drop to this amt the model considers bac in the soil to be

      insignificant and sets the levels to zero

      1/day         |Die-off factor for persistent pathogen in streams'
    gr_stream: 1/day         |growth factor for persistent pathogen in streams
    do_res: 1/day         |Die-off factor for less persistent pathogen in reservoirs
    gr_res: 1/day         |growth factor for less persistent pathogen in reservoirs
    conc_min: '|minimum pathogen concentration'
type_summaries:
  pathogen_db: One pathogen parameter record holding the name and tuning coefficients for
    a pathogen type used throughout SWAT+ constituent and transport calculations.
---

<!-- facts:header -->

`pathogen_data_module` owns the pathogen parameter database type and the shared allocatable `path_db` array. `path_parm_read` populates that array from the pathogen parameter file, and later pathogen and septic/channel routines import the module to look up per-pathogen coefficients such as die-off, growth, transport, and minimum concentration limits.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it does not contain initialization code. `path_parm_read` allocates and loads `path_db`, while other routines use the shared array after that setup step.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:path_parm_read] | `pathogens.pth` | `path_db` | Checks whether the configured pathogen database file exists, counts its records, allocates `path_db`, and reads each pathogen record into the shared array. |
| [sym:constit_db_read] | `constituents.cs` | `path_db` | Uses `path_db(ipathdb)%pathnm` to resolve pathogen constituent names to `cs_db%path_num` indices while reading the constituent database. |
| [sym:pathogen_init] | `no direct file input visible in the extracted references` | `path_db` | Reads the shared pathogen count and uses pathogen-related initialization tables to size and seed HRU pathogen state. |
| [sym:sd_channel_read] | `channel-lte.cha` | `path_db` | Imports the module during channel setup, but the extracted references do not show a specific `path_db` symbol use in the routine body. |

## Key Consumers

Pathogen database values are consumed by constituent lookup, land-surface pathogen updates, runoff and leaching calculations, channel routing, and septic biozone processing. The module is also imported during setup routines that size or initialize pathogen-related state.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:ch_rtpath] | path_db | Uses `path_db(ipath)%do_stream` and `path_db(ipath)%t_adj` to compute the temperature-adjusted die-off factor applied before the routed channel pathogen concentration is stored. |
| [sym:constit_db_read] | path_db | Uses `path_db(ipathdb)%pathnm` to match each pathogen name from the constituent list to its pathogen database index in `cs_db%path_num`. |
| [sym:path_ls_process] | path_db | Uses pathogen-specific coefficients from `path_db` to apply rainfall wash-off, foliage die-off/growth, soil die-off/growth, and minimum concentration limits for each HRU pathogen. |
| [sym:path_ls_runoff] | path_db | Uses `path_db(ipath_db)%kd` to scale the surface-runoff pathogen transport calculation from the top soil layer. |
| [sym:path_ls_swrouting] | path_db | Uses `path_db(ipath_db)%kd` and `path_db(ipath_db)%perco` to compute pathogen loss from the first soil layer by percolation. |
| [sym:path_parm_read] | `path_db` | Creates and fills the allocatable pathogen database array from the configured pathogen parameter file so later routines can query pathogen properties. |
| [sym:pathogen_init] | pathogen_data_module | Provides the shared pathogen database count and initialization tables that drive allocation and initial HRU pathogen concentrations. |
| [sym:sd_channel_read] | pathogen_data_module | The module is imported during channel setup, but the extracted references do not show a resolved `path_db` access in the procedure body. |
| [sym:sep_biozone] | pathogen_data_module | Supports septic biozone pathogen accounting by making pathogen-related shared state available during septic effluent and biozone updates. |

## Lineage

`pathogen_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pathogen_data_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `16e54aa` (2024-07-05) — BB 61.0.1
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `pathogen_data_module` has no extracted module-level documentation comment.
- The extracted references show `sd_channel_read` imports the module, but no specific `path_db` symbol use was resolved there.
- The `do_stream` source comment spans two lines in the type definition; the text has been preserved as a combined description.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
