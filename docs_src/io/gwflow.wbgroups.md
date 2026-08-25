---
kind: io
source_symbols:
- gwflow_output_init
title: '`gwflow.wbgroups`'
status: filled
source_hash: 1b76bd6ab57a763b
version_label: SWAT+ 62.0.0
---

**Primary target:** pco%gwflow_wb  
**Read by:** [sym:gwflow_output_init]

## Bottom Line

The file gwflow.wbgroups configures groundwater watershed groupings and their cell memberships used in the groundwater flow output calculations.

It is required if groundwater flow output is enabled and is read by the gwflow_output_init subroutine.

This file maps groundwater balance groups to their constituent spatial cells, enabling aggregation of groundwater fluxes and states at the group level.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the pco derived type instance which contains the gwflow_wb input data structure that stores groundwater balance group definitions read from this file. |
| [sym:hydrograph_module] |  |
| [sym:sd_channel_module] |  |
| [sym:time_module] |  |
| [sym:constituent_mass_module] | Provides cs_db which controls solute species information used in groundwater solute output initialization but not directly in reading this file. |
| [sym:basin_module] | Provides pco and bsn derived type instances; pco contains the gwflow_wb input data structure populated by this reader. |

## File Variables

The gwflow.wbgroups file contains groundwater watershed group metadata and cell membership lists. The file is read sequentially to populate the pco%gwflow_wb data structure, which holds the number of groups, maximum cells per group, and for each group, the number of cells and their cell indices.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Header line` | `header` |  |  | A text header line read from the file, likely a descriptive or comment line. |
| 1 | `Number of groundwater watershed groups` | `gw_wb_grp_num` |  |  | The total number of groundwater watershed groups defined in the file. |
| 1 | `Maximum number of cells per group` | `max_num` |  |  | The maximum number of cells that any groundwater watershed group can contain. |
| 1 | `Number of cells in group i` | `gw_wb_grp_ncell(i)` |  |  | For each groundwater watershed group i, the number of cells assigned to that group. |
| 1 | `Cell indices for group i` | `wb_cell` |  |  | The spatial cell indices that belong to the current groundwater watershed group being read. |

## Sample

```text
Example gwflow.wbgroups file snippet:
Header line text
3
100
Header line for group 1
50
1 2 3 4 5 ... 50
Header line for group 2
30
51 52 53 ... 80
Header line for group 3
20
81 82 83 ... 100
```

## Read Pattern

```fortran
open(in_gw,file='gwflow.wbgroups')
read(in_gw,*) header
read(in_gw,*) gw_wb_grp_num
read(in_gw,*) max_num
read(in_gw,*) header
read(in_gw,*) gw_wb_grp_ncell(i)
read(in_gw,*) wb_cell
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='gwflow.wbgroups')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) gw_wb_grp_num` |
| Input | `read` | in_gw | `read(in_gw,*) max_num` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) gw_wb_grp_ncell(i)` |
| Input | `read` | in_gw | `read(in_gw,*) wb_cell` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_output_init] | close, open, read | The gwflow_output_init subroutine reads gwflow.wbgroups to initialize groundwater watershed group definitions and their cell memberships into the pco%gwflow_wb data structure, enabling groundwater balance output aggregation. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file format appears to have header lines before group counts and cell lists, but the exact content of these headers is not detailed in the source.
- The primary target is inferred as pco%gwflow_wb based on module usage and typical SWAT+ input structure conventions.
