---
kind: io
source_symbols:
- basin_read_objs
title: '`object.cnt`'
status: filled
source_hash: bfec865685d5c03d
version_label: SWAT+ 62.0.0
---

**Primary target:** `bsn(:)` (array of `type basin_inputs`)  
**Read by:** [sym:basin_read_objs]

## Bottom Line

The `object.cnt` input file configures the counts of spatial objects in the watershed, such as basins, HRUs, reaches, reservoirs, and groundwater flow cells.

It is a required file for the model to read routing and spatial object configuration.

The primary reader for this file is the `basin_read_objs` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the `type spatial_objects` used to store counts of various spatial objects read from the file into `sp_ob`. |
| [sym:input_file_module] | Provides the `in_sim` and `in_con` input configuration variables used to locate the file and store related configuration strings. |
| [sym:organic_mineral_mass_module] | Imported but no direct variables or types from this module are used in `basin_read_objs` for reading or storing this file. |
| [sym:constituent_mass_module] | Imported but no direct variables or types from this module are used in `basin_read_objs` for reading or storing this file. |
| [sym:basin_module] | Provides the `type basin_inputs` used to store basin-related data read from the file into `bsn`. |
| [sym:gwflow_module] | Provides the `out_gw` unit for writing the gwflow record file and the `bsn_cc` variable to check gwflow activation. |

## File Variables

`object.cnt` has one basin/count row. The first three columns identify the basin and its land/total area, and the remaining columns give the counts for each spatial-object family the model allocates at startup.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `name` | `bsn%name` | character(len=25) |  | Name identifier for the basin |
| 2 | `ls_area` | `bsn%area_ls_ha` | real | hectares | Area of the land segment in hectares |
| 3 | `tot_area` | `bsn%area_tot_ha` | real | hectares | Total area of the basin in hectares |
| 4 | `obj` | `sp_ob%objs` | integer |  | Number of spatial objects or first object command |
| 5 | `hru` | `sp_ob%hru` | integer |  | Number of hydrologic response units (HRUs) or first HRU command |
| 6 | `lhru` | `sp_ob%hru_lte` | integer |  | Number of HRU LTEs or first HRU LTE command |
| 7 | `rtu` | `sp_ob%ru` | integer |  | Number of response units (RUs) or first RU command |
| 8 | `mfl` | `sp_ob%gwflow` | integer |  | Number of groundwater flow (gwflow) objects or first gwflow command |
| 9 | `aqu` | `sp_ob%aqu` | integer |  | Number of aquifers or first aquifer command |
| 10 | `cha` | `sp_ob%chan` | integer |  | Number of channels or first channel command |
| 11 | `res` | `sp_ob%res` | integer |  | Number of reservoirs or first reservoir command |
| 12 | `rec` | `sp_ob%recall` | integer |  | Number of record days or first record day command |
| 13 | `exco` | `sp_ob%exco` | integer |  | Number of export coefficients or first export coefficient command |
| 14 | `dlr` | `sp_ob%dr` | integer |  | Number of delivery ratios or first delivery ratio command |
| 15 | `can` | `sp_ob%canal` | integer |  | Number of canals or first canal command |
| 16 | `pmp` | `sp_ob%pump` | integer |  | Number of pumps or first pump command |
| 17 | `out` | `sp_ob%outlet` | integer |  | Number of outlets or first outlet command |
| 18 | `lcha` | `sp_ob%chandeg` | integer |  | Number of SWAT-DEM channels or first SWAT-DEM channel command |
| 19 | `aqu2d` | `sp_ob%aqu2d` | integer |  | Not currently used (number of 2D aquifers or first 2D aquifer command) |
| 20 | `hrd` | `sp_ob%herd` | integer |  | Not currently used (number of herds) |
| 21 | `wro` | `sp_ob%wro` | integer |  | Not currently used (number of water rights) |

## Sample

```text
object.cnt: 
name                   ls_area      tot_area       obj       hru      lhru       rtu       mfl       aqu       cha       res       rec      exco       dlr       can       pmp       out      lcha     aqu2d       hrd       wro
demo                      1.          1            12         12         0         0         0         0         0         0         0         0         0         0         0         0         0         0         0         0
```

## Read Pattern

```fortran
open (107,file=in_sim%object_cnt)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) bsn, sp_ob
read(107,*,iostat=eof) header
read(107,*,iostat=eof)
read (107,*,iostat=eof) riv_id
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_sim%object_cnt)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) bsn, sp_ob` |
| File control | `close` | 107 | `close (107)` |
| Input | `read` | 107 | `read(107,*,iostat=eof) header` |
| Input | `read` | 107 | `read(107,*,iostat=eof)` |
| Input | `read` | 107 | `read(107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) riv_id` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:basin_read_objs] | close, open, read | Reads the `object.cnt` file to load routing and spatial object counts into the model state variables `bsn` and `sp_ob`. It also adjusts groundwater flow object counts if the gwflow module is active and manages related configuration. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is required and must exist; the reader stops execution if the file is missing or set to 'null'.
- The reader adjusts object counts if the gwflow module is active and the 'chancell.gw' file exists, replacing aquifer counts with gwflow river cell counts.
- Sample rows were replaced with a real bundled refdata example from `external/swatplus-62.0.0/refdata/Ames_sub1/object.cnt`.
