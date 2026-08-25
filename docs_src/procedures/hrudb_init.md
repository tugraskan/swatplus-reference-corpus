---
kind: procedure
symbol: hrudb_init
title: hrudb_init
status: filled
source_hash: a884bd99d9a17463
version_label: SWAT+ 62.0.0
locals:
  imp: '`imp` is a local integer placeholder that is set to 0 and not used in the extracted
    logic. In this routine it appears to exist only as an initialized scratch variable.'
  ihru: '`ihru` is the loop counter over HRU objects. It runs from 1 to `sp_ob%hru` and selects
    which active HRU is being initialized on each pass.'
  iob: '`iob` holds the current object index in `ob`, computed from the first HRU object number
    (`sp_ob1%hru`) plus the loop offset. It is used to fetch the spatial object’s area and
    property pointer.'
  ihru_db: '`ihru_db` is the HRU database record index taken from `ob(iob)%props`. It identifies
    which row in `hru_db` supplies the database values copied into the active HRU.'
  ilu: '`ilu` stores the land-use-management index looked up from `hru(ihru)%dbs%land_use_mgt`.
    It is then used to read the matching `lum(ilu)%cal_group` value.'
uses:
  hydrograph_module: '`hydrograph_module` provides the spatial object counts and per-object
    metadata that determine which HRU entries get initialized and what area/object identity
    they receive. `sp_ob%hru` sets the loop range, `sp_ob1%hru` provides the starting object
    number, and `ob(iob)%props` and `ob(iob)%area_ha` link each spatial object to its HRU
    database record and area.'
  hru_module: '`hru_module` holds both the active HRU state and the HRU database tables that
    this routine copies from. `hrudb_init` transfers database pointers and scalar properties
    into `hru(ihru)`, so the active HRU objects carry the correct database references, land-use
    code, calibration group, and nutrient parameters for later processing.'
  landuse_data_module: '`landuse_data_module` matters because the HRU database stores a land-use-management
    index, not the calibration group text itself. `hrudb_init` uses `lum(ilu)%cal_group` to
    convert that index into the HRU’s calibration group string.'
  basin_module: '`basin_module` supplies basin-wide default nutrient parameters. `hrudb_init`
    copies those basin defaults into each HRU’s nutrient structure so all HRUs start with
    consistent phosphorus and nitrogen coefficients unless changed later.'
---

<!-- facts:header -->

Initializes each HRU’s database pointers and key properties from the HRU and basin lookup tables. It also assigns calibration group and nutrient defaults used later in HRU setup.

## Bottom Line

`hrudb_init` walks through every HRU object and copies the linked database records into the active `hru(ihru)` structure. It uses the spatial object map (`sp_ob`, `sp_ob1`, `ob`) to find the matching HRU database entry, then stores the database pointers, object number, area, and area-derived kilometers for each HRU.

It also pulls the land-use management code from the HRU database, resolves that code to a calibration group through `lum`, and seeds the HRU nutrient parameters from basin-wide defaults in `bsn_prm`. These values are part of the HRU initialization path that later routines, such as `hru_lum_init_all`, build on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU initialization after `hru_allo` and `hru_read` have prepared the HRU arrays and loaded the HRU database. `proc_hru` calls it before `hru_lum_init_all`, `topohyd_init`, and output allocation, because later setup depends on each HRU already having its database pointers, area, land-use code, calibration group, and nutrient defaults.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop over HRUs | Iterate through each active HRU object, derive the matching object index in `ob`, and prepare to copy database-backed values into `hru(ihru)`. |
| 2. resolve HRU database row | Use `ob(iob)%props` to find which HRU database record belongs to the current object. The comment indicates this property points to `hru.dat`. |
| 3. copy database structures | Copy the numeric and character database pointer structures from `hru_db(ihru_db)` into the active HRU so the HRU retains both forms of the database links. |
| 4. assign object identity and geometry | Set the HRU object number, copy the area from the spatial object, and compute `km` as area divided by 100. |
| 5. copy land-use-management code | Transfer the land-use-management string from the HRU database character record into the active HRU. |
| 6. resolve calibration group | Use the HRU’s land-use-management index to look up `lum(ilu)%cal_group` and store that calibration group on the active HRU. |
| 7. seed nutrient parameters | Copy basin-wide phosphorus and nitrogen coefficients from `bsn_prm` into the HRU nutrient structure for later process calculations. |
| 8. return to caller | Finish initialization and hand control back to `proc_hru` after all HRUs have been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(iob)%props, ob(iob)%area_ha` |
| [sym:hru_module] | `hru, hru_db` | `hru(ihru)%dbs, hru_db(ihru_db)%dbs, hru(ihru)%dbsc, hru_db(ihru_db)%dbsc, hru(ihru)%obj_no, hru(ihru)%area_ha, hru(ihru)%km, hru(ihru)%land_use_mgt_c, hru_db(ihru_db)%dbsc%land_use_mgt, hru(ihru)%dbs%land_use_mgt, hru(ihru)%cal_group, hru(ihru)%nut%phoskd, hru(ihru)%nut%pperco, hru(ihru)%nut%psp, hru(ihru)%nut%nperco, hru(ihru)%nut%cmn, hru(ihru)%nut%nperco_lchtile` |
| [sym:landuse_data_module] | `lum` | `lum(ilu)%cal_group` |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%phoskd, bsn_prm%pperco, bsn_prm%psp, bsn_prm%nperco, bsn_prm%cmn, bsn_prm%nperco_lchtile` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(ihru)%dbs` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%dbs` is overwritten with the database-pointer values from the matching `hru_db(ihru_db)%dbs`, so each active HRU knows which database entries it is tied to. |
| `hru(ihru)%dbsc` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%dbsc` is overwritten with the matching character database pointers from `hru_db(ihru_db)%dbsc`, preserving the text form of the HRU database links. |
| `hru(ihru)%obj_no` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%obj_no` is set to the current spatial object number (`sp_ob1%hru + ihru - 1`) so the HRU can be identified consistently in later workflows. |
| `hru(ihru)%area_ha` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%area_ha` is refreshed from `ob(iob)%area_ha` so the active HRU carries the spatial object’s area in hectares. |
| `hru(ihru)%km` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%km` is recalculated from the object area as `ob(iob)%area_ha / 100.`, providing a derived area-based length-scale used elsewhere in the model. |
| `hru(ihru)%land_use_mgt_c` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%land_use_mgt_c` is set to the character land-use-management name from the HRU database, which later routines use when reading management and land-use settings. |
| `hru(ihru)%cal_group` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%cal_group` is filled from the land-use management table entry referenced by the HRU’s database land-use index, enabling calibration-group-based grouping later in setup or output. |
| `hru(ihru)%nut%phoskd` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%nut%phoskd` is initialized from the basin default `bsn_prm%phoskd`, giving each HRU the same starting phosphorus partition coefficient. |
| `hru(ihru)%nut%pperco` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%nut%pperco` is initialized from `bsn_prm%pperco`, so the HRU starts with the basin phosphorus percolation coefficient. |
| `hru(ihru)%nut%psp` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%nut%psp` is initialized from `bsn_prm%psp`, setting the phosphorus availability index used by later nutrient calculations. |
| `hru(ihru)%nut%nperco` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%nut%nperco` is initialized from `bsn_prm%nperco`, establishing the basin nitrate percolation coefficient on each HRU. |
| `hru(ihru)%nut%cmn` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%nut%cmn` is initialized from `bsn_prm%cmn`, setting the active organic nitrogen mineralization factor used later in nutrient cycling. |
| `hru(ihru)%nut%nperco_lchtile` | For every `ihru` from 1 to `sp_ob%hru`. | `hru(ihru)%nut%nperco_lchtile` is initialized from `bsn_prm%nperco_lchtile`, giving each HRU the basin default tile/leaching nitrogen concentration coefficient. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `hrudb_init`. The file was added in `df07e3f` with the basic HRU-to-database transfer loop, `39fabde` only initialized the local counters (`imp`, `ihru`, `iob`, `ihru_db`) to zero, `e18817a` added calibration-group lookup through `landuse_data_module`, and `c55897a` added `basin_module` plus the nutrient parameter assignments copied from `bsn_prm`.

- `df07e3f` introduced the initial HRU database initialization loop that copies HRU database pointers, object numbers, area, and land-use-management text into each active HRU.
- `39fabde` changed only local-variable initialization by setting `imp`, `ihru`, `iob`, and `ihru_db` to zero at declaration; the loop logic stayed the same.
- `e18817a` extended the routine to derive `ilu` from `hru(ihru)%dbs%land_use_mgt` and set `hru(ihru)%cal_group` from `lum(ilu)%cal_group`.
- `c55897a` extended initialization with basin defaults for `hru(ihru)%nut%phoskd`, `pperco`, `psp`, `nperco`, `cmn`, and `nperco_lchtile`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hrudb_init' has no extracted documentation comment.
