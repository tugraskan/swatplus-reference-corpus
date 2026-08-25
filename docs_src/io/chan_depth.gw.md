---
kind: io
source_symbols:
- gwflow_chan_read
title: '`chan_depth.gw`'
status: filled
source_hash: 3ed2725dbd1f4d2a
version_label: SWAT+ 62.0.0
---

**Primary target:** `gw_chan_dep(:)` (daily channel depth per depth zone)  
**Read by:** [sym:gwflow_chan_read]

## Bottom Line

`chan_depth.gw` is an optional gwflow time-series file giving the daily channel-water depth for each depth zone. It supplies the channel stage used by the groundwater-channel exchange calculation.

The reader `gwflow_chan_read` (which reads `chancell.gw`) checks for `chan_depth.gw`; if present it sets `gw_chan_dep_flag`, reads the meta and header lines, sizes `gw_chan_dep` from the number of depth zones, and the daily rows are then read during the simulation (`gwflow_simulate`).

The file is optional; when absent, gwflow uses its internally computed channel depths.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the gwflow depth-zone arrays (`gw_chan_dpzn`, `gw_chan_ndpzn`, `gw_chan_dep`) and the `gw_chan_dep_flag` set when this file exists. |
| [sym:hydrograph_module] | Provides spatial-object counts used when reading the companion `chancell.gw` connections. |
| [sym:utils] | Provides `split_line` used to parse the connection rows in the companion file. |

## File Variables

`chan_depth.gw` has a meta line and a column-header line followed by one row per simulation day. Each row carries the julian day, the year, and one channel-depth value per depth zone. The header and metadata are read up front by `gwflow_chan_read`; the daily rows are consumed during the simulation. The number of depth-zone columns equals the maximum depth zone assigned in `chancell.gw`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `jday` | `jday` | integer |  | julian day of the simulation row |
| 2 | `yr` | `yr` | integer |  | year of the simulation row |
| 3.. | `depth_zone` | `gw_chan_dep(1:gw_chan_ndpzn)` | real |  | channel depth for each depth zone; one column per zone (number of zones = max gw_chan_dpzn from chancell.gw) |

## Sample

```text
Schematic (meta + header + one row per simulation day):

<meta line>
jday  yr    depth_zone1  depth_zone2 ...
1     2000  0.85         1.20
2     2000  0.83         1.18
```

## Read Pattern

```fortran
open(1421,file='chan_depth.gw')
read(1421,*) header
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 1421 | `open(1421,file='chan_depth.gw')` |
| Input | `read` | 1421 | `read(1421,*) header` |
| Input | `read` | 1421 | `read(1421,*) header` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_chan_read] | open, read | Reads the companion `chancell.gw` channel-cell connections, then, if `chan_depth.gw` exists, sets `gw_chan_dep_flag`, reads its meta and header lines, and sizes `gw_chan_dep` from the number of depth zones; the daily depth rows are read later in `gwflow_simulate`. |

## Review Notes

- This file was split out of the former `gwflow.chancells_depth`: the zone assignment lives in `chancell.gw` (column 6) and the daily depths live here.
- Only the meta and header lines are read by `gwflow_chan_read`; the daily rows are read during the simulation.
- The number of depth columns equals `gw_chan_ndpzn` = maxval of the depth-zone column in `chancell.gw`.
- The file is optional; `gw_chan_dep_flag` is set only when it exists.
