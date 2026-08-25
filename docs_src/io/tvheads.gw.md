---
kind: io
source_symbols:
- gwflow_read
title: '`tvheads.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gw_tvh_vals(:,:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'tvheads.gw' provides groundwater head time series data for model grid cells.

It is an optional input file used to initialize or force groundwater head values over time.

The primary reader for this file is the 'gwflow_read' subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the 'gw_tvh_vals' array and 'time' derived type used to store groundwater head values and time dimension. |
| [sym:hydrograph_module] | No direct variables or types from this module are used for reading 'tvheads.gw'. |
| [sym:sd_channel_module] | No direct variables or types from this module are used for reading 'tvheads.gw'. |
| [sym:maximum_data_module] | No direct variables or types from this module are used for reading 'tvheads.gw'. |
| [sym:hru_module] | No direct variables or types from this module are used for reading 'tvheads.gw'. |
| [sym:reservoir_data_module] | No direct variables or types from this module are used for reading 'tvheads.gw'. |
| [sym:cs_data_module] | No direct variables or types from this module are used for reading 'tvheads.gw'. |
| [sym:constituent_mass_module] | No direct variables or types from this module are used for reading 'tvheads.gw'. |
| [sym:water_allocation_module] | No direct variables or types from this module are used for reading 'tvheads.gw'. |
| [sym:utils] | Uses 'split_line' utility but not directly in the reading of 'tvheads.gw'. |

## File Variables

The 'tvheads.gw' file contains groundwater head time series data per cell. The file format includes a header line followed by multiple records, each with a cell ID and a time series of groundwater head values. These values are read into the 'gw_tvh_vals' array indexed by cell and time step.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Header line` | `header` |  |  | The first line read from the file, typically a descriptive header or metadata line. |
| 1 | `Cell ID` | `cell_id` |  |  | The unique identifier of the grid cell for which groundwater head time series data follows. |
| 2- | `Groundwater head values` | `(gw_tvh_vals(i,j),j=1,time%nbyr)` |  |  | A sequence of groundwater head values for the given cell, one value per time step over the simulation period. |

## Sample

```text
Example record block from 'tvheads.gw':
Header line (e.g. descriptive text or column names)
12345  10.5 10.7 10.8 10.9 11.0 ... (one groundwater head value per time step)
```

## Read Pattern

```fortran
open(in_tvh,file='tvheads.gw')
read(in_tvh,*) header
read(in_tvh,*,iostat=eof) cell_id
rewind(in_tvh)
read(in_tvh,*) header
read(in_tvh,*) header
read(in_tvh,*) cell_id,(gw_tvh_vals(i,j),j=1,time%nbyr)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_tvh | `open(in_tvh,file='tvheads.gw')` |
| Input | `read` | in_tvh | `read(in_tvh,*) header` |
| Input | `read` | in_tvh | `read(in_tvh,*) header` |
| Input | `read` | in_tvh | `read(in_tvh,*,iostat=eof) cell_id` |
| File control | `rewind` | in_tvh | `rewind(in_tvh)` |
| Input | `read` | in_tvh | `read(in_tvh,*) header` |
| Input | `read` | in_tvh | `read(in_tvh,*) header` |
| Input | `read` | in_tvh | `read(in_tvh,*) cell_id,(gw_tvh_vals(i,j),j=1,time%nbyr)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read, rewind | The 'gwflow_read' subroutine reads the 'tvheads.gw' file to load groundwater head time series data into the 'gw_tvh_vals' array, associating each time series with a specific model grid cell ID. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file 'tvheads.gw' is read by 'gwflow_read' to populate groundwater head values per cell over time.
- The exact format of the header lines is not fully detailed in the source; assumed to be descriptive or metadata lines.
- The file is optional and used to provide time-varying groundwater head boundary conditions or initial states.
