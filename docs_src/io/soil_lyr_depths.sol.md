---
kind: io
source_symbols:
- soils_init
title: '`soil_lyr_depths.sol`'
status: filled
source_hash: 7347b60d72c2f7eb
version_label: SWAT+ 62.0.0
---

**Primary target:** sol_mm_db(:)  
**Read by:** [sym:soils_init]

## Bottom Line

The file `soil_lyr_depths.sol` provides custom soil layer depth definitions used to override or augment the default soil layer depths from the soil database.

It is optional and only read if present; if absent, the model uses default soil layer depths from the soil database.

The primary reader of this file is the `soils_init` subroutine, which uses it to initialize soil physical properties and layer depths for each soil in the database.

| Module | Role for this file |
| --- | --- |
| [sym:hru_module] | Provides the HRU data structures such as `hru`, `wfsh`, and indices like `ihru` used to assign soil properties to HRUs. |
| [sym:soil_module] | Supplies the soil data types and arrays like `soil`, `sol`, and `soildb` that store soil physical and chemical properties. |
| [sym:plant_module] | Used indirectly for plant community data (`pcom`) needed during soil initialization. |
| [sym:maximum_data_module] | Provides the maximum number of soils (`db_mx%soil`) used to allocate soil arrays. |
| [sym:soil_data_module] | Contains soil-related data structures and variables used during soil initialization. |
| [sym:organic_mineral_mass_module] | Used for soil organic and mineral mass variables initialized in the soil layers. |
| [sym:constituent_mass_module] | Provides constituent mass variables allocated per soil layer during initialization. |
| [sym:hydrograph_module] | Provides `sp_ob` which contains the number of HRUs (`sp_ob%hru`) for looping over HRUs. |
| [sym:time_module] | Used for time-related variables and control during initialization (not explicitly shown but imported). |
| [sym:basin_module] | Provides basin-level data structures used during soil initialization. |
| [sym:septic_data_module] | Provides septic system data (`sep`, `iseptic`, `i_sep`) used to create biozone layers in septic HRUs. |

## File Variables

The file `soil_lyr_depths.sol` contains soil layer depth definitions and associated soil physical and chemical properties. The file is read line-by-line into variables that map directly to soil layer attributes in the soil database structures.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `titldum` | `titldum` |  |  | Reads the title or descriptive string from the first line of the file, used as a header or identifier for the soil layer depth data. |
| 1 | `header` | `header` |  |  | Reads a second header line from the file, typically containing column headers or metadata for the soil layer depth data. |
| 1 | `units` | `units` |  |  | Reads the units line from the file, indicating the measurement units (e.g., millimeters) for the soil layer depths and properties. |
| 1 | `csld` | `csld` |  |  | Reads the current custom soil layer depth value in millimeters, which is used to override or define soil layer thicknesses. |

## Sample

```text
Example lines from `soil_lyr_depths.sol` might look like:
Title of Soil Layer Depths File
Layer Header Line
Units Line (e.g., mm)
10
20
30
40
```

## Read Pattern

```fortran
open (107,file="soil_lyr_depths.sol")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) units
read (107,*,iostat=eof) csld
rewind (107)
backspace 107
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="soil_lyr_depths.sol")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) units` |
| Input | `read` | 107 | `read (107,*,iostat=eof) csld` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) units` |
| Input | `read` | 107 | `read (107,*,iostat=eof) csld` |
| File control | `backspace` | 107 | `backspace 107` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:soils_init] | backspace, close, open, read, rewind | The `soils_init` subroutine reads `soil_lyr_depths.sol` to obtain custom soil layer depths and associated soil physical and chemical properties. It uses this data to initialize and override the default soil layer depths and properties in the soil database, allocating and setting soil layers accordingly for each soil and HRU. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `soil_lyr_depths.sol` is optional; if missing, default soil layer depths from the soil database are used.
- The reader `soils_init` uses the file to customize soil layer depths and initialize soil physical properties accordingly.
- No explicit sample data lines were found in the source; the sample read format is inferred from typical header and depth lines.
