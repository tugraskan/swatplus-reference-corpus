---
kind: procedure
symbol: hru_lum_init
title: hru_lum_init
status: filled
source_hash: ef35841e0c303af8
version_label: SWAT+ 62.0.0
args:
  iihru: '`iihru` selects which HRU entry in `hru` and `pcom` to initialize. The routine reads
    and updates the shared state for that one HRU only, using `hru(iihru)%land_use_mgt` and
    `hru(iihru)%obj_no` to find the matching land-use, object, and weather data.'
locals:
  iob: Holds the HRU's connected object number from `hru(iihru)%obj_no`, then is used to look
    up the object-to-weather-station link in `ob(iob)%wst`.
  ilu: Holds the land-use management index for this HRU, copied from `hru(iihru)%land_use_mgt`,
    and is used to read the matching entries in `lum` and `lum_str`.
  ilug: Loop counter over `lum_grp%num` that searches the configured land-use management groups
    for a name match to the HRU's calibration-group string.
  isched: Temporary copy of `lum_str(ilu)%mgt_ops`; it captures the management-schedule pointer
    for the selected land-use structure, although the value is not written back in this routine.
  iwst: Weather-station index resolved from the HRU's object connectivity (`ob(iob)%wst`)
    so the routine can reach the station's weather-generator code.
  iwgn: Weather-generator index copied from `wst(iwst)%wco%wgn`; it identifies the generator
    attached to the resolved weather station, though this routine does not pass it onward.
uses:
  hru_module: '`hru_module` holds the HRU record being initialized, so its fields are the
    destination for the land-use, group, management, and practice codes copied here. The procedure
    reads `hru(iihru)%land_use_mgt`, `hru(iihru)%obj_no`, and `hru(iihru)%lum_group_c`, then
    writes the HRU''s plant cover, land-use group index, and management/practice pointers
    back into the same record.'
  plant_module: '`plant_module` provides the plant community array whose `name` entry is assigned
    from the selected land-use management record. That name links the HRU''s management selection
    to the plant initialization that happens later in the workflow.'
  landuse_data_module: '`landuse_data_module` contains the land-use management table, the
    structure table, and the group list that this routine uses to translate an HRU''s land-use
    code into concrete pointers and integer selectors. Without these shared tables, the routine
    could not map `land_use_mgt` into plant cover, management operations, conservation practice
    codes, or the HRU''s land-use group.'
  hydrograph_module: '`hydrograph_module` supplies the object connectivity that connects an
    HRU to its spatial object. That connection is needed to find the object''s weather-station
    assignment before the routine can resolve the weather-generator code associated with this
    HRU.'
  climate_module: '`climate_module` provides the weather-station array whose `wco%wgn` code
    is read after the object-to-station link is found. This matters because the HRU''s object
    connection determines which weather generator is associated with the HRU''s location.'
---

<!-- facts:header -->

Initializes land-use-related pointers and indices for one HRU. It copies management codes from land-use tables into the HRU, resolves the HRU's land-use group, and aligns management settings with the HRU's connected object and weather station.

## Bottom Line

`hru_lum_init` takes a single HRU index and uses that HRU's assigned land-use management number to pull the matching plant community, land-use structure, management schedule, and conservation settings from the shared land-use tables. It also resolves the HRU's land-use group index by comparing the HRU's calibration-group string against the configured group names.

The routine matters because later HRU initialization and land-use-change processing depend on these pointers and codes being in sync. In `actions`, it is called right after `hru(j)%land_use_mgt` is updated, and in `hru_lum_init_all` it is used to populate every HRU from its database land-use pointer before the rest of the model setup continues.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU setup and again during land-use change handling. `hru_lum_init_all` prepares each HRU's `land_use_mgt` from its database pointer before calling it for every HRU, and `actions` updates one HRU's land-use assignment before calling it so the HRU's derived plant, management, and practice fields stay consistent. Downstream initialization such as `plant_init` and `cn2_init`, plus later HRU behavior that depends on `mgt_ops`, `tiledrain`, `septic`, `fstrip`, `grassww`, `bmpuser`, and `luse` codes, rely on the results.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load land-use index | Read the HRU's assigned land-use management number from `hru(iihru)%land_use_mgt` into `ilu` so the routine can use that index to find the matching land-use records. |
| 2. assign plant community | Copy the selected land-use management's `plant_cov` string into `pcom(iihru)%name`, linking this HRU to the plant community initialization record for that land use. |
| 3. assign plant cover code | Copy the integer plant-cover selector from `lum_str(ilu)%plant_cov` into `hru(iihru)%plant_cov` so the HRU carries the structure-based plant cover pointer. |
| 4. assign calibration group string | Copy `lum(ilu)%cal_group` into `hru(iihru)%lum_group_c`, preserving the land-use calibration group name on the HRU. |
| 5. search group list | Loop through the configured land-use groups and compare the HRU's calibration-group string to each group name; when a match is found, store the matching group number in `hru(iihru)%lum_group`. |
| 6. load object number | Copy the HRU's spatial object number into `iob` so the routine can look up the connected object's weather assignment. |
| 7. load weather station | Use the object connectivity table to read the weather-station index `ob(iob)%wst` into `iwst`. |
| 8. load weather generator | Read the weather generator code from `wst(iwst)%wco%wgn` into `iwgn`, tying the HRU's location to its climate generator assignment. |
| 9. load management schedule | Copy the selected land-use structure's management-operations selector into `isched` as a local schedule pointer. |
| 10. assign management and practice codes | Copy the land-use structure's management and BMP-related selectors into the HRU record, including `mgt_ops`, `tiledrain`, `septic`, `fstrip`, `grassww`, `bmpuser`, `luse%cn_lu`, and `luse%cons_prac`. |
| 11. return | Exit after the HRU's land-use, group, weather, and management pointers have been synchronized with the lookup tables. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` | `hru(iihru)%land_use_mgt, hru(iihru)%plant_cov, hru(iihru)%lum_group_c, hru(iihru)%lum_group, hru(iihru)%obj_no, hru(iihru)%mgt_ops, hru(iihru)%tiledrain, hru(iihru)%septic, hru(iihru)%fstrip, hru(iihru)%grassww, hru(iihru)%bmpuser, hru(iihru)%luse%cn_lu, hru(iihru)%luse%cons_prac` |
| [sym:plant_module] | `pcom` | `pcom(iihru)%name` |
| [sym:landuse_data_module] | `lum, lum_str, lum_grp` | `lum(ilu)%plant_cov, lum_str(ilu)%plant_cov, lum(ilu)%cal_group, lum_grp%num, lum_grp%name(ilu), lum_str(ilu)%mgt_ops, lum_str(ilu)%tiledrain, lum_str(ilu)%septic, lum_str(ilu)%fstrip, lum_str(ilu)%grassww, lum_str(ilu)%bmpuser, lum_str(ilu)%cn_lu, lum_str(ilu)%cons_prac` |
| [sym:hydrograph_module] | `ob` | `ob(iob)%wst` |
| [sym:climate_module] | `wst` | `wst(iwst)%wco%wgn` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(iihru)%name` | When the selected land-use management record is loaded for `ilu = hru(iihru)%land_use_mgt`. | `pcom(iihru)%name` is set to the plant-community name referenced by the land-use management table, so later plant initialization can use the correct community for this HRU. |
| `hru(iihru)%plant_cov` | When the selected land-use structure is loaded for the HRU's land-use index. | `hru(iihru)%plant_cov` is updated to the integer plant-cover pointer from `lum_str(ilu)`, giving the HRU the structure-based plant initialization code it should use. |
| `hru(iihru)%lum_group_c` | When `lum(ilu)%cal_group` is read for the HRU's land-use index. | `hru(iihru)%lum_group_c` stores the calibration-group name tied to the selected land use, which is then used to resolve the numeric land-use group. |
| `hru(iihru)%lum_group` | When the calibration-group string matches one of the configured names in `lum_grp%name` during the `do ilug` search. | `hru(iihru)%lum_group` is set to the matching group number so the HRU has a numeric land-use-group identifier for later calibration or output logic. |
| `hru(iihru)%mgt_ops` | When the selected land-use structure provides a management-operations pointer. | `hru(iihru)%mgt_ops` is copied from `lum_str(ilu)%mgt_ops`, giving the HRU the management schedule selector associated with its land-use structure. |
| `hru(iihru)%tiledrain` | When the selected land-use structure includes a tile-drain pointer. | `hru(iihru)%tiledrain` is set from `lum_str(ilu)%tiledrain` so the HRU carries the correct tile-drain configuration for later hydrology calculations. |
| `hru(iihru)%septic` | When the selected land-use structure includes a septic-system pointer. | `hru(iihru)%septic` is set from `lum_str(ilu)%septic` so later septic loading and routing logic uses the HRU's assigned septic configuration. |
| `hru(iihru)%fstrip` | When the selected land-use structure includes a filter-strip pointer. | `hru(iihru)%fstrip` is copied from `lum_str(ilu)%fstrip` so the HRU keeps the correct filter-strip setting. |
| `hru(iihru)%grassww` | When the selected land-use structure includes a grass-waterway pointer. | `hru(iihru)%grassww` is copied from `lum_str(ilu)%grassww` so the HRU's grass waterway configuration matches the land-use table. |
| `hru(iihru)%bmpuser` | When the selected land-use structure includes a user BMP pointer. | `hru(iihru)%bmpuser` is copied from `lum_str(ilu)%bmpuser` so the HRU retains the user-specified BMP removal-efficiency linkage. |
| `hru(iihru)%luse%cn_lu` | When the selected land-use structure includes a curve-number land-use code. | `hru(iihru)%luse%cn_lu` is set from `lum_str(ilu)%cn_lu` so curve-number computations later in the model use the correct land-use table entry. |
| `hru(iihru)%luse%cons_prac` | When the selected land-use structure includes a conservation-practice code. | `hru(iihru)%luse%cons_prac` is set from `lum_str(ilu)%cons_prac` so later runoff and conservation-practice logic use the correct practice code. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved for `hru_lum_init`. The routine was introduced in `df07e3f` with the full HRU land-use initialization logic. `94b6dec` later replaced the file with the same routine body as an imported source drop, without changing the algorithm. `39fabde` only initialized the local scalar variables (`iob`, `ilu`, `ilug`, `isched`, `iwst`, `iwgn`) to zero; the assignment and lookup logic remained the same.

- `df07e3f` added `hru_lum_init` and its land-use, group, weather, and management pointer assignments for each HRU.
- `39fabde` made the local integer temporaries explicitly start at zero, removing uninitialized-variable risk without changing the lookup flow.
- `94b6dec` refreshed the file contents from upstream source while preserving the same procedure structure and behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_lum_init' has no extracted documentation comment.
