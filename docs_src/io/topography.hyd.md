---
kind: io
source_symbols:
- topo_read
title: '`topography.hyd`'
status: filled
source_hash: 93c5add219e97d71
version_label: SWAT+ 62.0.0
---

**Primary target:** `topo_db(:)` (array of `type topography_db`)  
**Read by:** [sym:topo_read]

## Bottom Line

The file `topography.hyd` provides topographic parameters for each hydrologic response unit (HRU) or subbasin, configuring slope, slope length, lateral flow length, distance to stream, and deposition coefficient used in hydrologic and erosion modeling.

This file is optional; if it does not exist or is set to "null", the model allocates an empty topography database.

The reader `topo_read` is responsible for loading this file into the `topo_db` array.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_hyd%topogr_hyd` used to locate `topography.hyd` |
| [sym:maximum_data_module] | provides the global data structure `db_mx` where the number of topography records `db_mx%topo` is stored |
| [sym:topography_data_module] | provides the derived type `topography_db` and the allocatable array `topo_db` where the file records are stored |

## File Variables

The file `topography.hyd` consists of multiple records each corresponding to a topographic unit, read into an array of `type topography_db`. Each record includes fields such as name, slope, slope length, lateral flow length, distance to stream, and deposition coefficient, matching the Fortran type definition.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `topo_db%name` | character(len=16) |  | Name identifier for the topographic unit |
| 3 |  | `topo_db%slope` | real | hru_slp(:) | average slope steepness in HRU |
| 4 |  | `topo_db%slope_len` | real | slsubbsn(:) | average slope length for erosion |
| 5 |  | `topo_db%lat_len` | real | slsoil(:) | slope length for lateral subsurface flow |
| 6 |  | `topo_db%dis_stream` | real | dis_stream(:) | average distance to stream |
| 7 |  | `topo_db%dep_co` | real |  | deposition coefficient |

## Sample

```text
Example records from a typical `topography.hyd` file (e.g. Ames_sub1) might look like:
"HRU1           0.05  100.0  75.0  200.0  1.0"
"HRU2           0.10  150.0  80.0  150.0  1.2"
```

## Read Pattern

```fortran
open (107,file=in_hyd%topogr_hyd)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) topo_db(ith)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_hyd%topogr_hyd)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) topo_db(ith)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:topo_read] | close, open, read, rewind | Reads the `topography.hyd` file if it exists, counts the number of records, allocates the `topo_db` array accordingly, and reads all topographic records into `topo_db`. If the file does not exist or is set to "null", it allocates an empty array. Updates the global count `db_mx%topo` with the number of records read. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
