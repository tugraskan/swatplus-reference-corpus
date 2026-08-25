---
kind: io
source_symbols:
- gwflow_read
title: '`floodplain.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gw_fp_cellid(:), gw_fp_chanid(:), gw_fp_K(:), gw_fp_area(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file floodplain.gw configures groundwater floodplain cell properties used in the SWAT+ groundwater flow model.

It is an optional input file that specifies floodplain groundwater cells, their associated channel IDs, hydraulic conductivity, and area.

The primary reader for this file is the gwflow_read subroutine, which reads and stores these properties for use in groundwater flow calculations.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides groundwater flow related variables and arrays such as gw_fp_cellid, gw_fp_chanid, gw_fp_K, and gw_fp_area that store floodplain groundwater cell data read from floodplain.gw. |
| [sym:hydrograph_module] | Imported but no direct evidence of usage for floodplain.gw reading. |
| [sym:sd_channel_module] | Imported but no direct evidence of usage for floodplain.gw reading. |
| [sym:maximum_data_module] | Imported but no direct evidence of usage for floodplain.gw reading. |
| [sym:hru_module] | Imports the derived type hru, but no direct evidence of usage for floodplain.gw reading. |
| [sym:reservoir_data_module] | Imports wet_dat, no direct evidence of usage for floodplain.gw reading. |
| [sym:cs_data_module] | Imported but no direct evidence of usage for floodplain.gw reading. |
| [sym:constituent_mass_module] | Imports cs_db, no direct evidence of usage for floodplain.gw reading. |
| [sym:water_allocation_module] | Imports canal, no direct evidence of usage for floodplain.gw reading. |
| [sym:utils] | Imports the utility subroutine split_line, but no direct evidence of usage for floodplain.gw reading. |

## File Variables

The floodplain.gw file contains a header line, a count of floodplain groundwater cells, and then multiple records each specifying a floodplain groundwater cell's ID, associated channel ID, hydraulic conductivity (K), and area. These values are read into arrays in the gwflow_module for use in groundwater flow modeling.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | A character string read as a header line from the floodplain.gw file, typically containing descriptive metadata or column titles. |
| 1 | `gw_fp_ncells` | `gw_fp_ncells` |  |  | An integer specifying the number of floodplain groundwater cells described in the file. |
| 1 | `gw_fp_cellid(i)` | `gw_fp_cellid(i)` |  |  | The unique identifier for the ith floodplain groundwater cell. |
| 2 | `gw_fp_chanid(i)` | `gw_fp_chanid(i)` |  |  | The channel ID associated with the ith floodplain groundwater cell, linking the cell to a surface water channel. |
| 3 | `gw_fp_K(i)` | `gw_fp_K(i)` |  |  | The hydraulic conductivity value for the ith floodplain groundwater cell, representing the ease with which water can move through the cell's material. |
| 4 | `gw_fp_area(i)` | `gw_fp_area(i)` |  |  | The area of the ith floodplain groundwater cell, typically in square meters. |

## Sample

```text
Example floodplain.gw content:
Header line (e.g., 'Floodplain GW Cell Data')
5
101 2001 0.0005 1500.0
102 2002 0.0007 1600.0
103 2003 0.0006 1550.0
104 2004 0.0004 1400.0
105 2005 0.0005 1450.0
```

## Read Pattern

```fortran
open(in_fp_cell,file='floodplain.gw')
read(in_fp_cell,*) header
read(in_fp_cell,*) gw_fp_ncells
read(in_fp_cell,*) header
read(in_fp_cell,*) gw_fp_cellid(i),gw_fp_chanid(i),gw_fp_K(i),gw_fp_area(i)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_fp_cell | `open(in_fp_cell,file='floodplain.gw')` |
| Input | `read` | in_fp_cell | `read(in_fp_cell,*) header` |
| Input | `read` | in_fp_cell | `read(in_fp_cell,*) gw_fp_ncells` |
| Input | `read` | in_fp_cell | `read(in_fp_cell,*) header` |
| Input | `read` | in_fp_cell | `read(in_fp_cell,*) gw_fp_cellid(i),gw_fp_chanid(i),gw_fp_K(i),gw_fp_area(i)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read | The gwflow_read subroutine opens and reads the floodplain.gw file to load floodplain groundwater cell properties into arrays for groundwater flow modeling. It reads the header, number of cells, and then each cell's ID, associated channel ID, hydraulic conductivity, and area. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The gwflow_read subroutine imports many modules, but only gwflow_module variables are clearly used to store floodplain.gw data.
- No explicit evidence of whether floodplain.gw is required or optional in the source; assumed optional based on typical SWAT+ usage.
- Sample read format is inferred from typical file structure; no explicit example found in source.
