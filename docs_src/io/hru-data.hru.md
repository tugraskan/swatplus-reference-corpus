---
kind: io
source_symbols:
- hru_read
title: '`hru-data.hru`'
status: filled
source_hash: 382d993953e4d8dc
version_label: SWAT+ 62.0.0
---

**Primary target:** `hru_db(:)` (array of `type hydrologic_response_unit_db`)  
**Read by:** [sym:hru_read]

## Bottom Line

The `hru-data.hru` file configures hydrologic response units (HRUs) for the SWAT+ model, defining land use, soil, topography, hydrology, snow, and field characteristics for each HRU.

This file is optional; if it does not exist or is set to "null", the HRU database array is allocated empty.

The primary reader for this file is the `hru_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | Provides the `db_mx` variable which holds maximum counts for various database categories used to loop over landuse, soil, topography, hydrology, snow, and field databases during HRU initialization. |
| [sym:reservoir_data_module] |  |
| [sym:landuse_data_module] | Provides the `lum` array containing land use management names used to match and assign land use indices to HRUs. |
| [sym:hydrology_data_module] | Provides the `hyd_db` array containing hydrology database names used to match and assign hydrology indices to HRUs. |
| [sym:topography_data_module] | Provides the `topo_db` array containing topography database names used to match and assign topography indices to HRUs. |
| [sym:soil_data_module] | Provides the `soildb` array containing soil database names used to match and assign soil indices to HRUs. |
| [sym:input_file_module] | Provides the `in_hru` variable which contains the file path for the HRU input file (`hru_data`). |
| [sym:hru_module] | Provides the `hru_db` array of type `hydrologic_response_unit_db` which stores the HRU data read from the file, and related types such as `hru_databases` and `hru_databases_char` used for storing indices and character names. |
| [sym:constituent_mass_module] | Provides soil and plant initial condition arrays such as `sol_plt_ini`, and constituent databases like `solt_db`, `pest_soil_ini`, `path_soil_ini`, `hmet_soil_ini`, `salt_soil_ini`, and `cs_soil_ini` used to initialize nutrient, pesticide, pathogen, heavy metal, salt, and constituent indices for HRUs. |

## File Variables

Each `hru-data.hru` row starts with an HRU id, then names the HRU and the database records that define its topography, hydrology, soil, land use/management, soil-plant initial conditions, optional surface storage, snow parameters, and field settings.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `id` | `k` | integer |  | HRU record id read from the file and used to select which `hru_db(i)` entry is being filled. |
| 2 | `name` | `hru_db%dbsc%name` | character(len=40) |  | HRU name stored in the raw character cross-reference block before later initialization resolves or copies it into runtime structures. |
| 3 | `topo` | `hru_db%dbsc%topo` | character(len=40) |  | Name of the topography database row to use for this HRU. |
| 4 | `hydro` | `hru_db%dbsc%hyd` | character(len=40) |  | Name of the hydrology database row to use for this HRU. |
| 5 | `soil` | `hru_db%dbsc%soil` | character(len=40) |  | Name of the soil database row to use for this HRU. |
| 6 | `lu_mgt` | `hru_db%dbsc%land_use_mgt` | character(len=40) |  | Name of the land use and management row to use for this HRU. |
| 7 | `soil_plant_init` | `hru_db%dbsc%soil_plant_init` | character(len=40) |  | Name of the soil and plant initialization row to use for this HRU. |
| 8 | `surf_stor` | `hru_db%dbsc%surf_stor` | character(len=40) |  | Name of the optional surface-storage record linked to this HRU. |
| 9 | `snow` | `hru_db%dbsc%snow` | character(len=40) |  | Name of the snow-parameter row to use for this HRU. |
| 10 | `field` | `hru_db%dbsc%field` | character(len=40) |  | Name of the optional field-geometry row to use for this HRU. |

## Sample

```text
hru-data.hru: 
      id  name                          topo             hydro              soil            lu_mgt   soil_plant_init         surf_stor              snow             field
       1  hru0001                topohru0001           hyd0001           soil_01-h1       cosy_lum        soilplant1              null           snow001              null
       2  hru0002                topohru0002           hyd0002           soil_02          mntill_corn_lum soilplant1              null           snow001              null
```

## Read Pattern

```fortran
open (113,file=in_hru%hru_data)
read (113,*,iostat=eof) titldum
read (113,*,iostat=eof) header
read (113,*,iostat=eof) i
rewind (113)
backspace (113)
read (113,*,iostat=eof) k, hru_db(i)%dbsc
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 113 | `open (113,file=in_hru%hru_data)` |
| Input | `read` | 113 | `read (113,*,iostat=eof) titldum` |
| Input | `read` | 113 | `read (113,*,iostat=eof) header` |
| Input | `read` | 113 | `read (113,*,iostat=eof) i` |
| File control | `rewind` | 113 | `rewind (113)` |
| Input | `read` | 113 | `read (113,*,iostat=eof) titldum` |
| Input | `read` | 113 | `read (113,*,iostat=eof) header` |
| Input | `read` | 113 | `read (113,*,iostat=eof) i` |
| File control | `backspace` | 113 | `backspace (113)` |
| Input | `read` | 113 | `read (113,*,iostat=eof) k, hru_db(i)%dbsc` |
| File control | `close` | 113 | `close (113)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:hru_read] | backspace, close, open, read, rewind | Reads the `hru-data.hru` file to populate the `hru_db` array of hydrologic response units. It first determines the maximum HRU index to allocate the array, then reads each HRU record's character database names, and maps these names to integer indices referencing land use, soil, topography, hydrology, snow, and field databases. It also initializes nutrient and constituent indices for soil and plants. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the existence check and allocation of an empty array if missing or set to "null".
- The mapping from character strings to integer indices is done by linear search over various database arrays, with warnings written if no match is found.
- The `hru_db%dbs` indices are assigned after reading the character names into `hru_db%dbsc`.
- Sample rows were replaced with a real bundled refdata example from `external/swatplus-62.0.0/refdata/Ames_sub1/hru-data.hru`.
