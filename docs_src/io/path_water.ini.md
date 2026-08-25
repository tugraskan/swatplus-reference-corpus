---
kind: io
source_symbols:
- path_cha_res_read
title: '`path_water.ini`'
status: filled
source_hash: 93803d0244a5e3eb
version_label: SWAT+ 62.0.0
---

**Primary target:** `path_water_ini(:)` (array of `type cs_water_init_concentrations`)  
**Read by:** [sym:path_cha_res_read]

## Bottom Line

The file `path_water.ini` configures initial concentrations of chemical constituents in water and benthic compartments for each path in the channel network at the start of the simulation.

It is optional and read only if the file exists and is not set to "null" in the initialization input structure.

The reader subroutine `path_cha_res_read` is responsible for loading this file.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_water_init_concentrations` which defines the structure of each record read from `path_water.ini`. The array `path_water_ini` of this type stores the initial constituent concentrations. |
| [sym:input_file_module] | Provides the input initialization structure `in_init` which contains the filename `path_water` used to open the `path_water.ini` file. |
| [sym:maximum_data_module] | Provides the variable `db_mx%pathw_ini` which stores the number of records read from the file. |
| [sym:channel_data_module] | Provides the variable `cs_db%num_paths` which defines the number of paths for which constituent data arrays are allocated and read. |
| [sym:hydrograph_module] | Used but no specific variables or types from this module are directly referenced in the reader. |
| [sym:sd_channel_module] | Used but no specific variables or types from this module are directly referenced in the reader. |
| [sym:organic_mineral_mass_module] | Used but no specific variables or types from this module are directly referenced in the reader. |

## File Variables

Each record in `path_water.ini` corresponds to an instance of `type cs_water_init_concentrations` and contains the constituent name followed by arrays of initial concentrations in water and benthic compartments for each path. The file is read into the array `path_water_ini` indexed by record.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `path_water_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `path_water_ini%water` | real | ppm,fracitons | amount of constituents (dissolved, salt minerals) in aquifer at start of simulation |
| 4 |  | `path_water_ini%benthic` | real | ppm or #cfu/m^2 | amount of constituent in benthic at start of simulation |
| 5 |  | `path_water_ini%reservoir` | real | ppm | amount of constituent in reservoir water at start of simulation |

## Sample

```text
Example record block from a typical dataset:
ConstituentName
0.005 0.010 0.015 ... (water concentrations for each path)
0.002 0.004 0.006 ... (benthic concentrations for each path)
```

## Read Pattern

```fortran
open (107,file=in_init%path_water)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) path_init_name(ipathi)
read (107,*,iostat=eof) titldum, path_water_ini(ipathi)%water, path_water_ini(ipathi)%benthic
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_init%path_water)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) path_init_name(ipathi)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum, path_water_ini(ipathi)%water, path_water_ini(ipathi)%benthic` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:path_cha_res_read] | close, open, read, rewind | Reads the `path_water.ini` file if it exists and is not set to "null". It first counts the number of records to allocate arrays, then rewinds and reads the constituent names and their initial water and benthic concentrations for each path. The data is stored in the global arrays `path_water_ini` and `path_init_name`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists and is not "null" in the input initialization structure.
- The `reservoir` field of `cs_water_init_concentrations` is declared but not read from the file in the current reader source; review if this is intentional or a partial implementation.
