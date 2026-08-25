---
kind: io
source_symbols:
- gwflow_read
title: '`cellcon.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module%gwcell(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'cellcon.gw' configures groundwater cell connectivity and properties for the SWAT+ groundwater flow model.

It is a required input file that defines the spatial and hydraulic characteristics of groundwater cells.

The primary reader that loads this file is the 'gwflow_read' subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the 'gwcell' derived type array where groundwater cell properties and connectivity are stored. |
| [sym:hydrograph_module] | Used for hydrograph separation arrays and output related to channel hydrology, indirectly related to groundwater flow. |
| [sym:sd_channel_module] | Used for channel cell information, including channel groundwater exchange cells. |
| [sym:maximum_data_module] | Provides constants or maximum sizes used in groundwater and channel data structures. |
| [sym:hru_module] | Provides the 'hru' derived type, which may be referenced for hydrologic response units related to groundwater cells. |
| [sym:reservoir_data_module] | Provides 'wet_dat' for reservoir properties that may interact with groundwater cells. |
| [sym:cs_data_module] | Used for constituent solute data related to groundwater and surface water interactions. |
| [sym:constituent_mass_module] | Provides 'cs_db' for constituent mass balance data used in groundwater solute transport. |
| [sym:water_allocation_module] | Provides 'canal' data structures for canal and water allocation information affecting groundwater flow. |
| [sym:utils] | Provides utility routines such as 'split_line' used for parsing lines from the input file. |

## File Variables

The 'cellcon.gw' file is a variable-width flat file where each record corresponds to a groundwater cell and its properties. The 'gwflow_read' subroutine reads this file line-by-line, parsing cell connectivity, hydraulic parameters, and spatial coordinates into the 'gwcell' array in the 'gwflow_module'.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| Multiple columns per line | `Groundwater cell properties and connectivity` | `header` |  |  | The 'header' variable reads the initial metadata or header lines of the 'cellcon.gw' file to identify the file structure and prepare for reading groundwater cell data. |
| Variable columns per line | `Cell connectivity and properties line` | `split_line_buf` |  |  | The 'split_line_buf' reads a full line of text from 'cellcon.gw' which is then parsed into fields representing groundwater cell connectivity and hydraulic properties. |

## Sample

```text
Example lines from 'cellcon.gw' might look like:
  1  4  2  3  5  6  7  8  9  10  100.0  50.0  25.0  0.001  0.2  0.3  1000.0  500.0
  2  3  1  4  5  6  7  8  9  10  120.0  60.0  30.0  0.002  0.25 0.35  1100.0  550.0
where each number represents cell ID, number of connections, connected cell IDs, and hydraulic properties.
```

## Read Pattern

```fortran
open(in_gw,file='cellcon.gw')
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,'(a)') split_line_buf
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='cellcon.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,'(a)') split_line_buf` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read, close | The 'gwflow_read' subroutine reads the 'cellcon.gw' file to load groundwater cell connectivity and hydraulic properties into the 'gwcell' array in 'gwflow_module'. It parses header lines and variable-width data lines, converting text fields into structured groundwater cell data used by the model. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The exact column structure and detailed field meanings of 'cellcon.gw' are not fully visible in the provided source snippet; the description is based on the file's role and typical groundwater cell connectivity files.
- The primary target is inferred as the 'gwcell' array from 'gwflow_module' based on module usage and typical groundwater cell data storage.
