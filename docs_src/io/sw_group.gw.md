---
kind: io
source_symbols:
- gwflow_read
title: '`sw_group.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gw_gwsw_group(:,:), gw_gwsw_ncell(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'sw_group.gw' configures groups of groundwater-to-surface water exchange cells, defining sets of cells for which daily groundwater-surface water exchange volumes are aggregated.

This file is optional and only read if it exists.

It is read by the 'gwflow_read' subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the variables 'gw_gwsw_group', 'gw_gwsw_ncell', 'gw_gwsw_ngroup', 'gw_gwsw_max', and 'gw_gwsw_group_flag' which store the group counts, maximum group size, and the cell groups read from 'sw_group.gw'. |
| [sym:hydrograph_module] | No direct variables used from this module in the reading of 'sw_group.gw'. |
| [sym:sd_channel_module] | No direct variables used from this module in the reading of 'sw_group.gw'. |
| [sym:maximum_data_module] | No direct variables used from this module in the reading of 'sw_group.gw'. |
| [sym:hru_module] | No direct variables used from this module in the reading of 'sw_group.gw'. |
| [sym:reservoir_data_module] | No direct variables used from this module in the reading of 'sw_group.gw'. |
| [sym:cs_data_module] | No direct variables used from this module in the reading of 'sw_group.gw'. |
| [sym:constituent_mass_module] | No direct variables used from this module in the reading of 'sw_group.gw'. |
| [sym:water_allocation_module] | No direct variables used from this module in the reading of 'sw_group.gw'. |
| [sym:utils] | Uses the 'split_line' subroutine to parse each line of the input file into fields. |

## File Variables

The file 'sw_group.gw' is a flat, variable-width text file where each row represents a groundwater-surface water cell group. Each row contains a group ID, the number of cells in the group, followed by the cell IDs belonging to that group. The reader parses these lines into arrays storing group sizes and cell IDs.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Group ID` | `header` |  |  | The first read line is a meta line, likely a file title or comment, stored in 'header' but not used for data. |
| 1 | `Column Header` | `header` |  |  | The second read line is the column header line, stored in 'header' but not used for data. |
| variable | `Group ID, Number of Cells, Cell IDs` | `split_line_buf` |  |  | Each subsequent line contains a group ID, the number of cells in the group, and the list of cell IDs. These are parsed and stored into 'gw_gwsw_ncell' and 'gw_gwsw_group' arrays. |

## Sample

```text
Example lines from 'sw_group.gw':
GroupID NumberOfCells CellID1 CellID2 CellID3 ...
1 3 101 102 103
2 2 201 202
3 4 301 302 303 304
```

## Read Pattern

```fortran
open(1235,file='sw_group.gw')
read(1235,*) header
read(1235,*) header
do
  read(1235,'(a)',iostat=eof) split_line_buf
  if(eof /= 0) exit
  call split_line(split_line_buf, split_fields, split_nf)
  read(split_fields(2),*) k
enddo
rewind(1235)
read(1235,*) header
read(1235,*) header
do i=1,gw_gwsw_ngroup
  read(1235,'(a)') split_line_buf
  call split_line(split_line_buf, split_fields, split_nf)
  read(split_fields(2),*) gw_gwsw_ncell(i)
  do j=1,gw_gwsw_ncell(i)
    read(split_fields(2+j),*) gw_gwsw_group(i,j)
  enddo
enddo
close(1235)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 1235 | `open(1235,file='sw_group.gw')` |
| Input | `read` | 1235 | `read(1235,*) header` |
| Input | `read` | 1235 | `read(1235,*) header` |
| Input | `read` | 1235 | `read(1235,'(a)',iostat=eof) split_line_buf` |
| File control | `rewind` | 1235 | `rewind(1235)` |
| Input | `read` | 1235 | `read(1235,*) header` |
| Input | `read` | 1235 | `read(1235,*) header` |
| Input | `read` | 1235 | `read(1235,'(a)') split_line_buf` |
| File control | `close` | 1235 | `close(1235)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | close, open, read, rewind | Reads the 'sw_group.gw' file to load groundwater-surface water cell groups into arrays for use in daily groundwater-surface water exchange calculations. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file 'sw_group.gw' is optional and only read if it exists, as indicated by the inquire statement.
- The reader uses 'split_line' from 'utils' to parse variable-width lines.
- The primary target arrays 'gw_gwsw_group' and 'gw_gwsw_ncell' are allocated dynamically based on file contents.
- No explicit units or detailed field descriptions are present in the source; the manual description is inferred from code structure.
