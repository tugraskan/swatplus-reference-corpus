---
kind: io
source_symbols:
- gwflow_read
title: '`hrucell.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** hru  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'hrucell.gw' configures groundwater-related HRU cell data for the SWAT+ model.

It is a required input file that specifies the spatial discretization of HRUs into groundwater cells.

The primary reader for this file is the 'gwflow_read' subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides groundwater flow related variables and arrays used during reading and storing groundwater cell data. |
| [sym:hydrograph_module] | Supplies hydrograph-related variables that may be updated during groundwater flow data reading. |
| [sym:sd_channel_module] | Used for channel cell information that relates to groundwater flow and HRU cell connectivity. |
| [sym:maximum_data_module] | Provides maximum data constants or arrays used during groundwater flow reading. |
| [sym:hru_module] | Provides the 'hru' derived type, which is the primary data structure populated by reading 'hrucell.gw'. |
| [sym:reservoir_data_module] | Provides reservoir-related data structures such as 'wet_dat' that may be referenced during groundwater flow reading. |
| [sym:cs_data_module] | Provides constituent source data structures used during groundwater flow reading. |
| [sym:constituent_mass_module] | Provides the 'cs_db' constituent mass database used during groundwater flow reading. |
| [sym:water_allocation_module] | Provides canal data structures such as 'canal' used during groundwater flow reading. |
| [sym:utils] | Provides utility routines such as 'split_line' used for parsing input lines. |

## File Variables

The 'hrucell.gw' input file contains records describing groundwater cells associated with each Hydrologic Response Unit (HRU). Each record includes the HRU identifier, the HRU area, the list of groundwater cell IDs composing the HRU, and the polygon area for each cell. The file is read sequentially by 'gwflow_read' and mapped into arrays within the 'hru' derived type and related groundwater flow data structures.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `hru_id` | `hru_id` |  |  | The unique identifier for each Hydrologic Response Unit (HRU) read from the file. |
| 2 | `hru_area` | `hru_area` |  |  | The total surface area of the HRU, used for scaling and spatial representation within the model. |
| 3 to n-1 | `hru_cells(k,cell_count)` | `hru_cells(k,cell_count)` |  |  | Array of groundwater cell IDs that spatially compose the HRU, defining the groundwater discretization within the HRU. |
| last | `poly_area` | `poly_area` |  |  | The polygon area associated with each groundwater cell within the HRU, used for spatial weighting and calculations. |

## Sample

```text
12345  1500.0  101 102 103 104  375.0
```

## Read Pattern

```fortran
open(in_hru_cell,file='hrucell.gw')
read(in_hru_cell,*)
read(in_hru_cell,*,iostat=eof) hru_id
rewind(in_hru_cell)
read(in_hru_cell,*) hru_id,hru_area,hru_cells(k,cell_count),poly_area
read(in_hru_cell,*,end=10) hru_id
backspace(in_hru_cell)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_hru_cell | `open(in_hru_cell,file='hrucell.gw')` |
| Input | `read` | in_hru_cell | `read(in_hru_cell,*)` |
| Input | `read` | in_hru_cell | `read(in_hru_cell,*)` |
| Input | `read` | in_hru_cell | `read(in_hru_cell,*,iostat=eof) hru_id` |
| File control | `rewind` | in_hru_cell | `rewind(in_hru_cell)` |
| Input | `read` | in_hru_cell | `read(in_hru_cell,*)` |
| Input | `read` | in_hru_cell | `read(in_hru_cell,*)` |
| Input | `read` | in_hru_cell | `read(in_hru_cell,*) hru_id,hru_area,hru_cells(k,cell_count),poly_area` |
| Input | `read` | in_hru_cell | `read(in_hru_cell,*,end=10) hru_id` |
| File control | `backspace` | in_hru_cell | `backspace(in_hru_cell)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | backspace, open, read, rewind | Reads the 'hrucell.gw' file to populate groundwater cell data for each HRU, including HRU IDs, areas, constituent groundwater cells, and polygon areas. This data is stored primarily in the 'hru' derived type and related groundwater flow data structures. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample record is inferred from typical variable usage; no explicit example was found in the source.
- The file 'hrucell.gw' appears to have variable-width records with HRU cell lists; exact column counts depend on the number of cells per HRU.
