---
kind: io
source_symbols:
- gwflow_read
title: '`rescell.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** wet_dat(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'rescell.gw' configures reservoir cell properties for the groundwater flow model component.

It is read by the 'gwflow_read' subroutine.

This file is required to specify reservoir thickness, hydraulic conductivity, and stage information for reservoir cells.

The data populates arrays in the 'wet_dat' derived type from the 'reservoir_data_module'.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides general groundwater flow variables and constants used during reading. |
| [sym:hydrograph_module] | Used for hydrograph-related variables but not directly for 'rescell.gw' reading. |
| [sym:sd_channel_module] | Used for channel-related data, not directly involved in 'rescell.gw' reading. |
| [sym:maximum_data_module] | Provides maximum data constants used in reading but not specific to 'rescell.gw'. |
| [sym:hru_module] | Imports the 'hru' derived type, not directly used for 'rescell.gw' reading. |
| [sym:reservoir_data_module] | Provides the 'wet_dat' derived type arrays where reservoir cell data from 'rescell.gw' is stored. |
| [sym:cs_data_module] | Used for constituent solute data, not directly related to 'rescell.gw'. |
| [sym:constituent_mass_module] | Provides 'cs_db' for constituent mass balance, unrelated to 'rescell.gw'. |
| [sym:water_allocation_module] | Provides 'canal' data structures, not used for 'rescell.gw'. |
| [sym:utils] | Provides utility routines such as 'split_line', not directly used for 'rescell.gw' reading. |

## File Variables

The 'rescell.gw' file contains reservoir cell data records including thickness, hydraulic conductivity, and stage information. Each record corresponds to a reservoir cell and is read into arrays within the 'wet_dat' derived type in the 'reservoir_data_module'.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Header lines` | `header` |  |  | The initial header lines read from the file, likely metadata or descriptive text skipped or stored for verification. |
| 1 | `Reservoir thickness` | `res_thick` |  |  | Reservoir thickness values read for each reservoir cell, representing the vertical thickness of the reservoir layer. |
| 1 | `Reservoir hydraulic conductivity` | `res_K` |  |  | Hydraulic conductivity values for each reservoir cell, indicating the ease with which water can move through the reservoir material. |
| 1 | `Number of reservoir cells` | `num_res_cells` |  |  | The total number of reservoir cells defined in the file, used to allocate arrays and control reading loops. |
| 1 | `Reservoir cell IDs` | `res_cell` |  |  | Integer identifiers for each reservoir cell, linking the data to model grid cells. |
| 2 | `Reservoir IDs` | `res_id` |  |  | Reservoir identifiers associating cells with specific reservoirs or reservoir groups. |
| 3 | `Reservoir stage` | `res_stage` |  |  | Stage or water surface elevation for each reservoir cell, used in water balance and flow calculations. |

## Sample

```text
Example 'rescell.gw' file snippet:
Header line 1
Header line 2
3.5
0.0012
10
Header line 3
101 1 5.0
102 1 5.2
103 2 4.8
```

## Read Pattern

```fortran
open(in_res_cell,file='rescell.gw')
read(in_res_cell,*) header
read(in_res_cell,*) header
read(in_res_cell,*) res_thick
read(in_res_cell,*) res_K
read(in_res_cell,*) num_res_cells
read(in_res_cell,*) header
read(in_res_cell,*) res_cell,res_id,res_stage
rewind(in_res_cell)
read(in_res_cell,*) header
read(in_res_cell,*) header
read(in_res_cell,*) res_thick
read(in_res_cell,*) res_K
read(in_res_cell,*) num_res_cells
read(in_res_cell,*) header
read(in_res_cell,*) res_cell,res_id,res_stage
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_res_cell | `open(in_res_cell,file='rescell.gw')` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) header` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) header` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) res_thick` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) res_K` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) num_res_cells` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) header` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) res_cell,res_id,res_stage` |
| File control | `rewind` | in_res_cell | `rewind(in_res_cell)` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) header` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) header` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) res_thick` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) res_K` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) num_res_cells` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) header` |
| Input | `read` | in_res_cell | `read(in_res_cell,*) res_cell,res_id,res_stage` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read, rewind | The 'gwflow_read' subroutine reads the 'rescell.gw' file to load reservoir cell properties into the groundwater flow model. It reads header lines, reservoir thickness, hydraulic conductivity, number of reservoir cells, and then reads arrays of reservoir cell IDs, reservoir IDs, and reservoir stage values. This data is stored in the 'wet_dat' derived type arrays from the 'reservoir_data_module' for use in groundwater flow and reservoir simulations. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file 'rescell.gw' is read twice with a rewind in between, indicating possible verification or reinitialization steps in 'gwflow_read'.
- The exact format of header lines is not detailed in the source; assumed to be metadata or descriptive text.
- The 'gwflow_read' subroutine uses the 'wet_dat' derived type from 'reservoir_data_module' to store reservoir cell data, as indicated by the variable names and module usage.
- No explicit units are given in the source; typical units for thickness (meters), hydraulic conductivity (m/s or m/day), and stage (meters) are assumed based on groundwater modeling conventions.
