---
kind: io
source_symbols:
- gwflow_read
title: '`outputs.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module.gwflow(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'outputs.gw' is an output record file containing daily groundwater flow results used for model diagnostics and analysis.

It is read by the 'gwflow_read' subroutine to populate groundwater flow data structures in the model state.

This file is required for groundwater flow post-processing and output reporting.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the 'gwflow' derived type array which stores groundwater flow data read from 'outputs.gw'. |
| [sym:hydrograph_module] | Used for hydrograph separation arrays and output related to groundwater flow. |
| [sym:sd_channel_module] | Used for channel cell processing related to groundwater flow outputs. |
| [sym:maximum_data_module] | Provides constants or maximum sizes used in groundwater flow data structures. |
| [sym:hru_module] | Imports the 'hru' type for hydrologic response unit data related to groundwater flow. |
| [sym:reservoir_data_module] | Imports 'wet_dat' for reservoir data that may interact with groundwater flow. |
| [sym:cs_data_module] | Used for constituent mass data related to groundwater flow solutes. |
| [sym:constituent_mass_module] | Provides 'cs_db' for constituent mass database used in groundwater flow solute tracking. |
| [sym:water_allocation_module] | Imports 'canal' type for canal water allocation data related to groundwater flow. |
| [sym:utils] | Provides the 'split_line' utility subroutine used for parsing lines read from 'outputs.gw'. |

## File Variables

The 'outputs.gw' file contains daily groundwater flow output records with header lines followed by data lines. The 'gwflow_read' subroutine reads this file line-by-line, parsing header metadata and groundwater flow data into the 'gwflow' derived type array for use in model post-processing and output reporting.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| entire line | `header` | `header` |  |  | The 'header' variable reads metadata or descriptive header lines from the 'outputs.gw' file to identify the data block or provide context for subsequent groundwater flow data records. |
| entire line | `split_line_buf` | `split_line_buf` |  |  | Reads a full line of groundwater flow data as a character string for parsing into individual data fields representing groundwater flow variables for each cell or time step. |

## Sample

```text
Example 'outputs.gw' snippet:
Header lines:
  'Groundwater Flow Output'
  'Date       CellID    Flow(m3/day)    Head(m)    Recharge(m)'
Data lines:
  '2023 01 01  1001      12.34          5.67       0.89'
  '2023 01 01  1002      15.67          6.12       1.02'
```

## Read Pattern

```fortran
open(in_gw,file='outputs.gw')
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,'(a)',iostat=eof) split_line_buf
rewind(in_gw)
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,'(a)',iostat=eof) split_line_buf
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='outputs.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,'(a)',iostat=eof) split_line_buf` |
| File control | `rewind` | in_gw | `rewind(in_gw)` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,'(a)',iostat=eof) split_line_buf` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read, rewind, close | Reads the 'outputs.gw' file to load groundwater flow daily output data into the model's groundwater flow data structures for post-processing and reporting. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The 'outputs.gw' file is an output record file for groundwater flow daily results, read by 'gwflow_read' to populate groundwater flow data structures.
- No explicit detailed file format or column definitions are visible in the provided source lines; the file appears to contain header metadata lines followed by data lines parsed as strings for further processing.
- The 'gwflow_read' subroutine uses 'split_line' utility to parse data lines after reading them as raw strings.
- The exact mapping of file columns to data fields in the 'gwflow' derived type is not fully visible in the provided source snippet.
