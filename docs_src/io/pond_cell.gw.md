---
kind: io
source_symbols:
- gwflow_read
title: '`pond_cell.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module.pond_cell  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file pond_cell.gw configures groundwater recharge pond cell information used in the groundwater flow model.

It is read by the gwflow_read subroutine and is required for groundwater recharge pond setup.

The file contains metadata header lines followed by records with pond cell identifiers and related parameters.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the derived type pond_cell and related groundwater flow data structures where pond cell information is stored. |
| [sym:hydrograph_module] | Imported but no direct evidence of usage for pond_cell.gw reading. |
| [sym:sd_channel_module] | Imported but no direct evidence of usage for pond_cell.gw reading. |
| [sym:maximum_data_module] | Imported but no direct evidence of usage for pond_cell.gw reading. |
| [sym:hru_module] | Imports the hru type but no direct evidence of usage for pond_cell.gw reading. |
| [sym:reservoir_data_module] | Imports wet_dat but no direct evidence of usage for pond_cell.gw reading. |
| [sym:cs_data_module] | Imported but no direct evidence of usage for pond_cell.gw reading. |
| [sym:constituent_mass_module] | Imports cs_db but no direct evidence of usage for pond_cell.gw reading. |
| [sym:water_allocation_module] | Imports canal but no direct evidence of usage for pond_cell.gw reading. |
| [sym:utils] | Imports split_line utility but no direct evidence of usage for pond_cell.gw reading. |

## File Variables

The pond_cell.gw file is a text input file with a header followed by rows of groundwater recharge pond cell data. The gwflow_read subroutine reads this file line-by-line, parsing header lines and then reading pond cell identifiers and parameters into the pond_cell derived type array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | The header lines are read as character strings and represent metadata or column headers for the pond_cell.gw file. |
| 1 | `dum_id` | `dum_id` |  |  | An integer read as a dummy or placeholder ID, likely used to detect end-of-file or to skip unused values. |
| 1 | `dum_id` | `dum_id` |  |  | A dummy integer field read along with cell_num and dum4, possibly a redundant or unused ID. |
| 2 | `cell_num` | `cell_num` |  |  | The integer cell number identifying the groundwater recharge pond cell in the model grid. |
| 3 | `dum4` | `dum4` |  |  | A fourth dummy or placeholder integer field read from the file, purpose unclear from source. |

## Sample

```text
HEADER LINE 1
HEADER LINE 2
1
1 100 0
2 101 0
3 102 0
```

## Read Pattern

```fortran
open(in_ponds,file='pond_cell.gw')
read(in_ponds,*) header
read(in_ponds,*) header
read(in_ponds,*,iostat=eof) dum_id
rewind(in_ponds)
read(in_ponds,*) header
read(in_ponds,*) header
read(in_ponds,*,iostat=eof) dum_id,cell_num,dum4
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_ponds | `open(in_ponds,file='pond_cell.gw')` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*,iostat=eof) dum_id` |
| File control | `rewind` | in_ponds | `rewind(in_ponds)` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*,iostat=eof) dum_id,cell_num,dum4` |
| File control | `close` | in_ponds | `close(in_ponds)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | close, open, read, rewind | Reads the pond_cell.gw file to load groundwater recharge pond cell data into the pond_cell array in gwflow_module, parsing header lines and then reading pond cell IDs and parameters. |

## Review Notes

- The file pond_cell.gw is required for groundwater recharge pond cell configuration and is read by gwflow_read.
- The dummy integer fields (dum_id, dum4) appear to be placeholders or unused values; their exact purpose is not documented in source.
- No sample data block from a reference dataset was found in the source; the sample_read_format is a plausible example based on the read pattern.
- Module usage for many imported modules is broad; only gwflow_module clearly provides the pond_cell type used for storing this file's data.
