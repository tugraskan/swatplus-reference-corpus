---
kind: io
source_symbols:
- gwflow_read
title: '`minerals.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwsol_minl_state(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file minerals.gw configures the initial groundwater mineral solute fractions per grid cell for the SWAT+ groundwater flow model.

It is an optional input file read by the gwflow_read subroutine.

The file defines the number of mineral solutes, the reading mode, and the spatial distribution of mineral fractions in the groundwater solution state.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the gwsol_minl_state derived type array where mineral solute fractions per groundwater cell are stored. |
| [sym:hydrograph_module] |  |
| [sym:sd_channel_module] |  |
| [sym:maximum_data_module] |  |
| [sym:hru_module] |  |
| [sym:reservoir_data_module] |  |
| [sym:cs_data_module] |  |
| [sym:constituent_mass_module] |  |
| [sym:water_allocation_module] |  |
| [sym:utils] |  |

## File Variables

The minerals.gw input file contains metadata and spatial data for groundwater mineral solutes. The file is read sequentially by gwflow_read, mapping header lines and parameters to variables and arrays representing mineral solute counts, reading modes, single values, and grid cell mineral fractions.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | A character string read as a header or metadata line from the input file, used to identify or skip descriptive lines. |
| 1 | `gw_nminl` | `gw_nminl` |  |  | The number of groundwater mineral solutes defined in the file, determining the dimension of mineral fraction arrays. |
| 1 | `read_type` | `read_type` |  |  | A character string indicating the reading mode or type for the mineral solute data (e.g., single value or grid values). |
| 1 | `single_value` | `single_value` |  |  | A real value representing a single mineral solute fraction applied uniformly if the reading mode is single value. |
| 1-grid_ncol | `grid_val(i,j)` | `(grid_val(i,j),j=1,grid_ncol)` |  |  | An array of real values representing mineral solute fractions for each grid column in a row i, read when the reading mode is grid-based. |
| 1-gw_nminl | `gwsol_minl_state(i)%fract(m)` | `(gwsol_minl_state(i)%fract(m),m=1,gw_nminl)` |  |  | The mineral solute fraction array for groundwater cell i, with fractions for each mineral solute m, populated from the input file. |

## Sample

```text
Header line example
3
grid
0.0
0.1 0.2 0.3 0.4 0.5
0.05 0.10 0.15
```

## Read Pattern

```fortran
open(in_gw_minl,file='minerals.gw')
read(in_gw_minl,*) header
read(in_gw_minl,*) gw_nminl
read(in_gw_minl,*) read_type
read(in_gw_minl,*) single_value
read(in_gw_minl,*) (grid_val(i,j),j=1,grid_ncol)
read(in_gw_minl,*) (gwsol_minl_state(i)%fract(m),m=1,gw_nminl)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw_minl | `open(in_gw_minl,file='minerals.gw')` |
| Input | `read` | in_gw_minl | `read(in_gw_minl,*) header` |
| Input | `read` | in_gw_minl | `read(in_gw_minl,*) gw_nminl` |
| Input | `read` | in_gw_minl | `read(in_gw_minl,*) header` |
| Input | `read` | in_gw_minl | `read(in_gw_minl,*) header` |
| Input | `read` | in_gw_minl | `read(in_gw_minl,*) read_type` |
| Input | `read` | in_gw_minl | `read(in_gw_minl,*) single_value` |
| Input | `read` | in_gw_minl | `read(in_gw_minl,*) (grid_val(i,j),j=1,grid_ncol)` |
| Input | `read` | in_gw_minl | `read(in_gw_minl,*) (gwsol_minl_state(i)%fract(m),m=1,gw_nminl)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read | Reads the minerals.gw file to load groundwater mineral solute fractions into the gwsol_minl_state array, configuring the groundwater solution mineral composition for the SWAT+ groundwater flow model. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The minerals.gw file is optional and configures groundwater mineral solute fractions; the exact format and usage depend on the read_type parameter.
- No explicit sample data was found in the source; the sample_read_format is a plausible example based on typical usage.
