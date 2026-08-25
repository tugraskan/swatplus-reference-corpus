---
kind: io
source_symbols:
- gwflow_read
title: '`tile.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** `gw_state(:)` (array of `type groundwater_state`)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file `tile.gw` configures tile drainage properties and tile drainage flags for groundwater cells in the SWAT+ groundwater flow model.

It is read by the `gwflow_read` subroutine, which loads tile drainage parameters such as tile depth, tile drainage area, tile hydraulic conductivity, tile group flags, and tile group memberships.

The file also sets the `tile` flag in each groundwater cell's `gw_state` record to indicate the presence or absence of tile drainage (0 = no tile; 1 = tile present).

This file is optional and only used if tile drainage is enabled in the model configuration.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the `groundwater_state` type and the `gw_state` array where tile drainage flags (`tile`) are stored. |
| [sym:hydrograph_module] | Imported but no direct evidence of usage for tile.gw reading; likely used elsewhere in `gwflow_read`. |
| [sym:sd_channel_module] | Imported but no direct evidence of usage for tile.gw reading; likely used elsewhere in `gwflow_read`. |
| [sym:maximum_data_module] | Imported but no direct evidence of usage for tile.gw reading; likely used elsewhere in `gwflow_read`. |
| [sym:hru_module] | Imports `hru` type, no direct evidence of usage for tile.gw reading. |
| [sym:reservoir_data_module] | Imports `wet_dat` type, no direct evidence of usage for tile.gw reading. |
| [sym:cs_data_module] | Imported but no direct evidence of usage for tile.gw reading. |
| [sym:constituent_mass_module] | Imports `cs_db` type, no direct evidence of usage for tile.gw reading. |
| [sym:water_allocation_module] | Imports `canal` type, no direct evidence of usage for tile.gw reading. |
| [sym:utils] | Imports `split_line` utility, no direct evidence of usage for tile.gw reading. |

## File Variables

The `tile.gw` input file contains tile drainage parameters and tile drainage flags for groundwater cells. The file is read sequentially by `gwflow_read` and maps to variables controlling tile drainage depth, drainage area, hydraulic conductivity, group flags, group memberships, and per-cell tile presence flags stored in the `gw_state(:)%tile` field.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` | character(len=13) |  | file header line |
| 2 | `tile_depth_val` | `tile_depth_val` | real | m | tile drainage depth |
| 3 | `tile_drain_area_val` | `tile_drain_area_val` | real | m2 | tile drainage area |
| 4 | `tile_K_val` | `tile_K_val` | real | m/day | tile hydraulic conductivity |
| 5 | `gw_tile_group_flag` | `gw_tile_group_flag` | integer |  | tile group flag |
| 6 | `gw_tile_num_group` | `gw_tile_num_group` | integer |  | number of tile groups |
| 7 | `num_tile_cells(i)` | `num_tile_cells(i)` | integer array |  | number of cells in each tile group |
| 8 | `gw_tile_groups(i,j)` | `gw_tile_groups(i,j)` | integer array |  | tile group cell memberships |
| 9 | `header` | `header` | character(len=13) |  | secondary header line |
| 10 | `(grid_int(i,j),j=1,grid_ncol)` | `grid_int(i,j)` | integer array |  | grid integer map |
| 11 | `gw_state(i)%tile` | `gw_state(i)%tile` | integer |  | tile drainage flag (0=no tile; 1=tile present) |

## Sample

```text
Example tile.gw file snippet:
Header line
1.5
1000.0
0.01
1
3

10
1 2 3 4 5 6 7 8 9 10
Header line
1 1 0 0 1 0 0 1 0 0
0 1 0 0 1 0 0 1 0 0
```

## Read Pattern

```fortran
open(in_gw,file='tile.gw')
read(in_gw,*) header
read(in_gw,*) tile_depth_val
read(in_gw,*) tile_drain_area_val
read(in_gw,*) tile_K_val
read(in_gw,*) gw_tile_group_flag
read(in_gw,*) gw_tile_num_group
read(in_gw,*)
read(in_gw,*) num_tile_cells(i)
read(in_gw,*) gw_tile_groups(i,j)
read(in_gw,*) header
read(in_gw,*) (grid_int(i,j),j=1,grid_ncol)
read(in_gw,*) gw_state(i)%tile
close(in_gw)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='tile.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) tile_depth_val` |
| Input | `read` | in_gw | `read(in_gw,*) tile_drain_area_val` |
| Input | `read` | in_gw | `read(in_gw,*) tile_K_val` |
| Input | `read` | in_gw | `read(in_gw,*) gw_tile_group_flag` |
| Input | `read` | in_gw | `read(in_gw,*) gw_tile_num_group` |
| Input | `read` | in_gw | `read(in_gw,*)` |
| Input | `read` | in_gw | `read(in_gw,*) num_tile_cells(i)` |
| Input | `read` | in_gw | `read(in_gw,*) gw_tile_groups(i,j)` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) (grid_int(i,j),j=1,grid_ncol)` |
| Input | `read` | in_gw | `read(in_gw,*) gw_state(i)%tile` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | close, open, read | Reads the `tile.gw` file to load tile drainage parameters and flags into the groundwater flow model state. It opens the file, reads tile drainage depth, drainage area, hydraulic conductivity, tile group flags and memberships, and finally reads the tile drainage presence flag for each groundwater cell into `gw_state(i)%tile`. This configures tile drainage behavior in the groundwater simulation. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The `tile.gw` file is optional and only relevant if tile drainage is enabled in the model.
- The `gwflow_read` subroutine reads this file and sets tile drainage parameters and flags in the groundwater state array `gw_state`.
- No evidence of other modules contributing variables specifically for tile.gw reading beyond `gwflow_module` for `gw_state`.
- Sample read format is inferred from the read statements and typical file structure; no explicit example found in source.
