---
kind: io
source_symbols:
- gwflow_read
title: '`cells.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** `gw_state(:)` (per-cell groundwater state) and the companion cell arrays  
**Read by:** [sym:gwflow_read]

## Bottom Line

`cells.gw` defines the groundwater-flow grid: one record per cell giving its location, geometry, conductivity and specific-yield zones, initial head, and evapotranspiration extinction depth, plus optional streambed, tile-drain, boundary-condition, structured-grid, and initial-temperature overrides.

The reader (in `gwflow_read`) reads a meta line and a header, then one record per cell into `gw_state` and the companion cell arrays; rows must appear in cell-id order 1..ncell.

The file is required when gwflow is active; each row must have at least the 14 core columns, and trailing override columns are read only when present and not `null`.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Defines `gw_state` and the per-cell arrays (`cell_name`, `cell_gis_id`, `delay`, override arrays, `cell_row`/`cell_col`, `cell_init_temp`) filled from each row; K/Sy zones index `zones_aquK`/`zones_aquSy` from `zones.gw`. |
| [sym:input_file_module] | gwflow input filenames are opened directly by name (`cells.gw`) within `gwflow_read`. |

## File Variables

`cells.gw` has a meta line and a column-header line followed by one record per groundwater cell, in cell-id order. The first 14 columns are required (id, name, GIS id, status, elevation, thickness, K and Sy zones, delay, extinction depth, initial head, x, y, area). Columns 15-23 are optional overrides and grid indices; a `null` in any optional slot leaves the default in place. The reader errors if a row has fewer than 14 columns or an out-of-order id.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `id` | `cell_id_in` | integer |  | cell id; must equal the row index (rows must be in order 1..ncell) |
| 2 | `name` | `cell_name` | character |  | cell name |
| 3 | `gis_id` | `cell_gis_id` | integer |  | GIS id of the cell |
| 4 | `status` | `gw_state%stat` | integer |  | cell status flag (active/inactive/boundary) |
| 5 | `elev` | `gw_state%elev` | real |  | ground-surface elevation of the cell |
| 6 | `thck` | `gw_state%thck` | real |  | aquifer thickness (surface elevation minus aquifer bottom) |
| 7 | `K_zone` | `gw_state%zone` | integer |  | hydraulic-conductivity zone (indexes zones.gw aquifer K) |
| 8 | `Sy_zone` | `Sy_zone` | integer |  | specific-yield zone (indexes zones.gw aquifer specific yield) |
| 9 | `delay` | `delay` | real |  | groundwater delay time for the cell |
| 10 | `exdp` | `gw_state%exdp` | real |  | evapotranspiration extinction depth |
| 11 | `init` | `gw_state%init` | real |  | initial groundwater head (raised to the aquifer bottom if below it) |
| 12 | `x` | `gw_state%xcrd` | real |  | x coordinate of the cell |
| 13 | `y` | `gw_state%ycrd` | real |  | y coordinate of the cell |
| 14 | `area` | `gw_state%area` | real |  | cell area |
| 15 | `strK` | `cell_strK_over` | real |  | optional streambed hydraulic-conductivity override (`null` to omit) |
| 16 | `strthick` | `cell_strthick_over` | real |  | optional streambed-thickness override (`null` to omit) |
| 17 | `bc_type` | `bc_type_array` | integer |  | optional boundary-condition type (`null` to omit) |
| 18 | `tile_depth` | `cell_tile_depth_over` | real |  | optional tile-drain depth override (`null` to omit) |
| 19 | `tile_area` | `cell_tile_area_over` | real |  | optional tile-drain area override (`null` to omit) |
| 20 | `tile_K` | `cell_tile_K_over` | real |  | optional tile-drain conductivity override (`null` to omit) |
| 21 | `row` | `cell_row` | integer |  | optional structured-grid row index (`null` to omit) |
| 22 | `col` | `cell_col` | integer |  | optional structured-grid column index (`null` to omit) |
| 23 | `init_temp` | `cell_init_temp` | real |  | optional initial groundwater temperature for heat transport (`null` to omit) |

## Sample

```text
Schematic (meta + header + one row per cell; 14 required cols, optional overrides after):

<meta line>
id name  gis_id status elev   thck  K_zone Sy_zone delay exdp init  x      y      area   [strK strthick bc_type tile_depth tile_area tile_K row col init_temp]
1  cell1 1001   1      312.5  25.0  1      1       31.0  2.0  300.0 500.0  1200.0 10000.  null null null null null null 1 1 null
```

## Read Pattern

```fortran
open(in_gw,file='cells.gw')
read(in_gw,*) header
read(in_gw,'(a)') split_line_buf
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='cells.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,'(a)') split_line_buf` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read | Within the gwflow input read, opens `cells.gw`, reads the meta and header lines, then reads one row per cell (splitting each line into fields) into `gw_state` and the companion cell arrays, validates the id order and column count, derives aquifer bottom/hydraulic properties from the K/Sy zones, and applies any non-`null` override columns. |

## Review Notes

- Rows must be in cell-id order: the reader stops with an error if column 1 does not equal the row index, or if a row has fewer than 14 columns.
- `K_zone`/`Sy_zone` index the aquifer conductivity/specific-yield zones read from `zones.gw`; the cell bottom is computed as `elev - thck`.
- Initial head below the aquifer bottom is raised to the bottom.
- Columns 15-23 are optional; a `null` sentinel leaves the corresponding value unset (override flags stay false).
- Columns 21-22 (row/col) apply to structured grids; column 23 (init_temp) applies when heat transport is enabled.
