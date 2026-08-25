---
kind: io
source_symbols:
- gwflow_read
title: '`gwflow_canal.con`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** canal(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'gwflow_canal.con' configures canal and recharge pond properties for the water allocation module in SWAT+. It is read by the 'gwflow_read' subroutine and is required to initialize canal-related model state such as canal IDs, object counts, and connection data.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides general groundwater flow variables and state used by gwflow_read. |
| [sym:hydrograph_module] | Used for hydrograph-related variables accessed during reading. |
| [sym:sd_channel_module] | Supplies channel-related types and variables used in canal and channel cell processing. |
| [sym:maximum_data_module] | Provides constants or maximum sizes used during reading. |
| [sym:hru_module] | Provides the 'hru' derived type used for hydrologic response units, referenced in gwflow_read. |
| [sym:reservoir_data_module] | Provides 'wet_dat' type or variables related to reservoir data used in reading. |
| [sym:cs_data_module] | Provides constituent source data used in reading canal and constituent mass data. |
| [sym:constituent_mass_module] | Provides 'cs_db' for constituent mass balance data accessed during reading. |
| [sym:water_allocation_module] | Provides the 'canal' derived type array which is the primary target of this file's data. |
| [sym:utils] | Provides utility routines such as 'split_line' used during parsing. |

## File Variables

The 'gwflow_canal.con' file contains canal and recharge pond configuration data. It is read sequentially by 'gwflow_read' into the 'canal' derived type array and related buffers, mapping file columns to Fortran variables representing canal IDs, object counts, and connection data.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | The first line read from the file, typically a descriptive header or metadata line. |
| 1 | `canal_id` | `canal_id` |  |  | An integer identifier for each canal or recharge pond record read from the file. |
| 2 | `obj_tot` | `obj_tot` |  |  | The total number of objects or connections associated with the canal record. |
| 3+ | `(con_row_buf(j),j=1,obj_tot*3)` | `(con_row_buf(j),j=1,obj_tot*3)` |  |  | A buffer array holding connection data triples for each object related to the canal, read as floating-point values. |

## Sample

```text
Example lines from gwflow_canal.con:
Header line (metadata or description)
1 3
1 2 0.5 0.7 1.0 2 3 0.6 0.8 1.1 3 1 0.4 0.9 1.2
```

## Read Pattern

```fortran
open(in_canal_cell,file='gwflow_canal.con')
read(in_canal_cell,*) header
read(in_canal_cell,*,iostat=eof) canal_id, obj_tot
rewind(in_canal_cell)
read(in_canal_cell,*) header
read(in_canal_cell,*,iostat=eof) canal_id, obj_tot
backspace(in_canal_cell)
read(in_canal_cell,*) canal_id, obj_tot, (con_row_buf(j),j=1,obj_tot*3)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_canal_cell | `open(in_canal_cell,file='gwflow_canal.con')` |
| Input | `read` | in_canal_cell | `read(in_canal_cell,*) header` |
| Input | `read` | in_canal_cell | `read(in_canal_cell,*,iostat=eof) canal_id, obj_tot` |
| File control | `rewind` | in_canal_cell | `rewind(in_canal_cell)` |
| Input | `read` | in_canal_cell | `read(in_canal_cell,*) header` |
| Input | `read` | in_canal_cell | `read(in_canal_cell,*,iostat=eof) canal_id, obj_tot` |
| File control | `backspace` | in_canal_cell | `backspace(in_canal_cell)` |
| Input | `read` | in_canal_cell | `read(in_canal_cell,*) canal_id, obj_tot, (con_row_buf(j),j=1,obj_tot*3)` |
| File control | `close` | in_canal_cell | `close(in_canal_cell)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | backspace, close, open, read, rewind | Reads the 'gwflow_canal.con' file to load canal and recharge pond configuration data into the 'canal' derived type array and related buffers. It parses header lines, canal IDs, object counts, and connection data to initialize canal-related model state for water allocation. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
