---
kind: io
source_symbols:
- basin_read_objs
- gwflow_chan_read
title: '`chancell.gw`'
status: filled
source_hash: 696504594efec7ec
version_label: SWAT+ 62.0.0
---

**Primary target:** sp_ob  
**Read by:** [sym:basin_read_objs]

## Bottom Line

The file 'chancell.gw' contains groundwater flow river cell data used to configure the groundwater flow (gwflow) component of the SWAT+ model.

It is optional and only read if the groundwater flow feature is active (bsn_cc%gwflow == 1) and the file exists.

The reader 'basin_read_objs' opens and reads this file to determine the number of groundwater river cells, adjusting the spatial object counts accordingly.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides routing and hydrograph-related types and variables used during object reading and routing setup. |
| [sym:input_file_module] | Supplies input file names and related configuration variables such as in_sim%object_cnt and in_con%gwflow_con. |
| [sym:organic_mineral_mass_module] | Used for organic and mineral mass types or variables during object reading. |
| [sym:constituent_mass_module] | Used for constituent mass types or variables during object reading. |
| [sym:basin_module] | Provides basin configuration variables such as bsn_cc and sp_ob for spatial object counts and groundwater flow activation flags. |
| [sym:gwflow_module] | Provides the output unit 'out_gw' used to write the groundwater flow record file. |

## File Variables

The 'chancell.gw' file contains a list of groundwater flow river cell IDs, one per line, used to configure the groundwater flow routing in the model. The reader counts these IDs to determine the number of groundwater river cells.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| entire line | `river cell ID` | `riv_id` |  |  | Each line contains a single integer representing a groundwater flow river cell ID. The reader counts these lines to determine the total number of groundwater river cells. |

## Sample

```text
Header line (string)
Blank or header line (string)
1
2
3
4
...
```

## Read Pattern

```fortran
open(107,file='chancell.gw')
read(107,*,iostat=eof) header
read(107,*,iostat=eof)
read(107,*,iostat=eof) header
do while (eof == 0)
  read(107,*,iostat=eof) riv_id
end do
close(107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open(107,file='chancell.gw')` |
| Input | `read` | 107 | `read(107,*,iostat=eof) header read(107,*,iostat=eof) read(107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) riv_id` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:basin_read_objs] | open, read, close | Reads the 'chancell.gw' file if groundwater flow is active to determine the number of groundwater river cells. It counts the IDs listed in the file to update the spatial object counts and sets related configuration variables accordingly. |
| [sym:gwflow_chan_read] | open, read, close | Also opens and reads 'chancell.gw' to process groundwater flow channel data, reading header lines and then the channel data lines into a buffer for further processing. |

## Review Notes

- The file 'chancell.gw' is optional and only read if groundwater flow is enabled and the file exists.
- The primary reader 'basin_read_objs' uses it to count groundwater river cells and adjust spatial object counts.
- The secondary reader 'gwflow_chan_read' also reads this file to load groundwater channel data lines.
- No explicit column headers or units are defined in the source; the file contains integer IDs per line after header lines.
- The sample read format is inferred from the reading pattern and may vary by dataset.
