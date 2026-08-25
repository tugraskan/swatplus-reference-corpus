---
kind: io
source_symbols:
- gwflow_read
title: '`cell_sol.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwsol_state(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'cell_sol.gw' contains groundwater solute concentration data per cell and solute species.

It is read by the 'gwflow_read' subroutine to initialize or update the groundwater solute state array 'gwsol_state'.

This file is required for configuring the groundwater solute concentrations in the model.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the 'gwsol_state' derived type array and 'gw_nsolute' integer for the number of solutes, which are populated by reading this file. |
| [sym:hydrograph_module] |  |
| [sym:sd_channel_module] |  |
| [sym:maximum_data_module] |  |
| [sym:hru_module] | Provides the 'hru' derived type, though not directly used for this file reading. |
| [sym:reservoir_data_module] | Provides 'wet_dat' but not directly used for this file reading. |
| [sym:cs_data_module] |  |
| [sym:constituent_mass_module] | Provides 'cs_db' but not directly used for this file reading. |
| [sym:water_allocation_module] | Provides 'canal' but not directly used for this file reading. |
| [sym:utils] | Provides the 'split_line' utility, not directly used in this file reading. |

## File Variables

The 'cell_sol.gw' file contains groundwater solute concentration data organized by cell ID and solute species concentrations. The file is read sequentially by 'gwflow_read' to populate the groundwater solute state array 'gwsol_state'. The file includes header lines and multiple data blocks with cell and grid integer arrays.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | The header line read from the file, typically containing metadata or column titles. |
| 1 | `cell_id` | `cell_id` |  |  | The integer cell identifier for the groundwater cell whose solute concentrations follow. |
| 2+ | `solute concentrations` | `(gwsol_state(i)%solute(s)%conc,s=1,gw_nsolute)` |  |  | Array of solute concentrations for each solute species in the groundwater cell identified by cell_id. |
| N/A | `cell_int array` | `(cell_int(i),i=1,ncell)` |  |  | Integer array representing cell-related integer data read from the file, possibly cell indices or flags. |
| N/A | `grid_int array` | `(grid_int(i,j),j=1,grid_ncol)` |  |  | 2D integer array representing grid-related integer data read from the file, possibly spatial indices or flags. |

## Sample

```text
GW_SOL_HEADER_1
GW_SOL_HEADER_2
12345 0.001 0.002 0.003 0.004

1 2 3 4 5
10 20 30 40 50
GW_SOL_HEADER_3
1 2 3 4 5
10 20 30 40 50
GW_SOL_HEADER_4
1 2 3 4 5
10 20 30 40 50
```

## Read Pattern

```fortran
open(in_gw,file='cell_sol.gw')
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,*) cell_id,(gwsol_state(i)%solute(s)%conc,s=1,gw_nsolute)
close(in_gw)
read(in_gw,*)
read(in_gw,*) (cell_int(i),i=1,ncell)
read(in_gw,*) (grid_int(i,j),j=1,grid_ncol)
read(in_gw,*) header
read(in_gw,*) (cell_int(i),i=1,ncell)
read(in_gw,*) (grid_int(i,j),j=1,grid_ncol)
read(in_gw,*) header
read(in_gw,*) (cell_int(i),i=1,ncell)
read(in_gw,*) (grid_int(i,j),j=1,grid_ncol)
close(in_gw)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='cell_sol.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) cell_id,(gwsol_state(i)%solute(s)%conc,s=1,gw_nsolute)` |
| File control | `close` | in_gw | `close(in_gw)` |
| Input | `read` | in_gw | `read(in_gw,*)` |
| Input | `read` | in_gw | `read(in_gw,*) (cell_int(i),i=1,ncell)` |
| Input | `read` | in_gw | `read(in_gw,*) (grid_int(i,j),j=1,grid_ncol)` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) (cell_int(i),i=1,ncell)` |
| Input | `read` | in_gw | `read(in_gw,*) (grid_int(i,j),j=1,grid_ncol)` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) (cell_int(i),i=1,ncell)` |
| Input | `read` | in_gw | `read(in_gw,*) (grid_int(i,j),j=1,grid_ncol)` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | close, open, read | The 'gwflow_read' subroutine reads the 'cell_sol.gw' file to populate groundwater solute concentrations into the 'gwsol_state' array, initializing groundwater solute state for the model. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file 'cell_sol.gw' is read multiple times with header and integer arrays, indicating multiple data blocks; exact semantics of cell_int and grid_int arrays are not fully clear from source alone.
