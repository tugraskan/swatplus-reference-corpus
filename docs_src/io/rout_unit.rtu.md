---
kind: io
source_symbols:
- ru_read
title: '`rout_unit.rtu`'
status: filled
source_hash: c365a75ded660d49
version_label: SWAT+ 62.0.0
---

**Primary target:** `ru(:)` (array of `type ru_parameters`)  
**Read by:** [sym:ru_read]

## Bottom Line

The file `rout_unit.rtu` configures routing unit parameters, including drainage area and topographic inputs, for the SWAT+ model.

It is an optional input file checked for existence before reading.

The primary reader that loads this file is the `ru_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the global object `sp_ob` which holds the total number of routing units (`sp_ob%ru`) used to allocate arrays for routing unit data. |
| [sym:input_file_module] | Provides the input file path `in_ru%ru` which stores the filename `rout_unit.rtu` to be opened and read by `ru_read`. |
| [sym:time_module] | No explicit variables or types are directly referenced in `ru_read` from this module in the shown source. |
| [sym:ru_module] | Defines the derived type `ru_parameters` and related types `ru_databases_char`, `ru_databases`, and `field` used to store routing unit parameters read from the file. |
| [sym:hydrograph_module] | Provides arrays `ru_d`, `ru_m`, `ru_y`, `ru_a` and the object `sp_ob` used for allocation and storage of routing unit hydrograph and auxiliary data. |
| [sym:maximum_data_module] | Provides `db_mx` which holds maximum counts for database arrays used to match string names to database indices. |
| [sym:topography_data_module] | Provides `topo_db` array used to match the routing unit's topographic database name string to an index stored in `ru(i)%dbs%toposub_db`. |
| [sym:constituent_mass_module] | Provides `cs_db` which holds counts of salts and constituents used to allocate salt and constituent arrays for routing units. |
| [sym:salt_module] | Used to allocate and initialize salt-related arrays for routing units if salts are defined in `cs_db`. |
| [sym:cs_module] | Used to allocate and initialize constituent-related arrays for routing units if constituents are defined in `cs_db`. |

## File Variables

The `rout_unit.rtu` file contains records of routing unit parameters, each record identified by an integer index followed by fields such as name, drainage area, and database strings. These are read sequentially and stored into an array of `type ru_parameters` in Fortran.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ru%name` | character(len=16) |  | Routing unit name identifier |
| 3 |  | `ru%da_km2` | real | km2 | Drainage area of the routing unit |
| 4 |  | `ru%dbsc` | type (ru_databases_char) |  | Character strings for database names associated with the routing unit |
| 5 |  | `ru%dbs` | type (ru_databases) |  | Integer indices referencing databases matched from `dbsc` strings |
| 6 |  | `ru%field` | type (field) |  | Field parameters associated with the routing unit |

## Sample

```text
1 Ames_sub1 12.5 Ames_topo Ames_field
2 Ames_sub2 8.3 Ames_topo Ames_field
3 Ames_sub3 15.0 Ames_topo Ames_field
```

## Read Pattern

```fortran
open (107,file=in_ru%ru)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat=eof) k, ru(i)%name, ru(i)%dbsc
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_ru%ru)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, ru(i)%name, ru(i)%dbsc` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ru_read] | backspace, close, open, read, rewind | Reads the routing unit parameters from the `rout_unit.rtu` file into the `ru` array of `type ru_parameters`. It checks for file existence, determines the maximum routing unit index, allocates necessary arrays, initializes salt and constituent data if present, matches database name strings to indices, and stores all data for use in routing computations. |

## Review Notes

- The file `rout_unit.rtu` is optional and only read if it exists and is not set to "null".
- The reader `ru_read` performs multiple passes: first to determine the maximum routing unit index, then to allocate arrays, and finally to read and store detailed routing unit parameters.
- Salt and constituent arrays are conditionally allocated and initialized based on the presence of salts and constituents in the `cs_db` database.
- Database string fields in the file are matched to integer indices referencing topographic and field databases for efficient lookup during simulation.
- No explicit sample records were found in the source; the sample read format is inferred from the read statements and typical naming conventions.
