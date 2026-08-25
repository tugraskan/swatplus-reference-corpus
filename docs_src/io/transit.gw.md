---
kind: io
source_symbols:
- gwflow_read
title: '`transit.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gw_transit_cells(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'transit.gw' provides groundwater transit time data for each cell in the model grid.

It is an optional input file used to configure groundwater transit times and cell mappings for the groundwater flow model state.

The primary reader that loads this file is the 'gwflow_read' subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the 'gw_transit_cells' array which stores the groundwater transit cell IDs read from 'transit.gw'. |
| [sym:hydrograph_module] | Imported but no direct evidence of usage for 'transit.gw' reading. |
| [sym:sd_channel_module] | Imported but no direct evidence of usage for 'transit.gw' reading. |
| [sym:maximum_data_module] | Imported but no direct evidence of usage for 'transit.gw' reading. |
| [sym:hru_module] | Imports the 'hru' type but no direct evidence of usage for 'transit.gw' reading. |
| [sym:reservoir_data_module] | Imports 'wet_dat' but no direct evidence of usage for 'transit.gw' reading. |
| [sym:cs_data_module] | Imported but no direct evidence of usage for 'transit.gw' reading. |
| [sym:constituent_mass_module] | Imports 'cs_db' but no direct evidence of usage for 'transit.gw' reading. |
| [sym:water_allocation_module] | Imports 'canal' but no direct evidence of usage for 'transit.gw' reading. |
| [sym:utils] | Imports 'split_line' but no direct evidence of usage for 'transit.gw' reading. |

## File Variables

The 'transit.gw' file contains groundwater transit time data per cell. The file is read line-by-line by 'gwflow_read', mapping transit times to cell IDs stored in the 'gw_transit_cells' array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | The first read line is a header or metadata line from the 'transit.gw' file, likely containing descriptive text or column headers. |
| 1 | `gw_transit_num` | `gw_transit_num` |  |  | Number of groundwater transit records or entries read from the file. |
| 1 | `cell_transit` | `cell_transit` |  |  | Individual groundwater transit time values per cell, which are mapped to cell IDs in the model grid. |

## Sample

```text
Example 'transit.gw' content:
Line 1: Header or descriptive text
Line 2: Number of transit entries (e.g., 100)
Line 3+: Transit time values per cell (e.g., 5, 10, 15, ...)
```

## Read Pattern

```fortran
open(in_transit_time,file='transit.gw')
read(in_transit_time,*) header
read(in_transit_time,*) header
read(in_transit_time,*) gw_transit_num
do i=1,gw_transit_num
  read(in_transit_time,*) cell_transit
enddo
close(in_transit_time)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_transit_time | `open(in_transit_time,file='transit.gw')` |
| Input | `read` | in_transit_time | `read(in_transit_time,*) header` |
| Input | `read` | in_transit_time | `read(in_transit_time,*) header` |
| Input | `read` | in_transit_time | `read(in_transit_time,*) gw_transit_num` |
| Input | `read` | in_transit_time | `read(in_transit_time,*) cell_transit` |
| File control | `close` | in_transit_time | `close(in_transit_time)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read, close | Reads the 'transit.gw' file to load groundwater transit time data into the 'gw_transit_cells' array, mapping transit times to model grid cells for groundwater flow simulation. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The 'transit.gw' file reading pattern includes two header reads before reading the number of transit records.
- The exact format and units of the transit times are not explicitly documented in the source; assumed to be days based on output file comments.
- No explicit column headers or units are read from the file beyond the initial header lines.
