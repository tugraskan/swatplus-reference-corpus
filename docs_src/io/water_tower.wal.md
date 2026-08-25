---
kind: io
source_symbols:
- water_tower_read
title: '`water_tower.wal`'
status: filled
source_hash: 8b6a3d10a9230b52
version_label: SWAT+ 62.0.0
---

**Primary target:** `wtow(:)` (array of `type water_transfer_data`)  
**Read by:** [sym:water_tower_read]

## Bottom Line

The file `water_tower.wal` configures water tower or pipe storage parameters used in water allocation modeling within SWAT+. It is optional; if the file does not exist or is named "null", an empty allocation array is allocated. The reader `water_tower_read` loads this file and populates the `wtow` array of `type water_transfer_data` with the data.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides file-related utilities and possibly input file handling routines used by `water_tower_read`. |
| [sym:water_allocation_module] | Defines the `type water_transfer_data` and related variables such as `wtow`, which store the water tower data read from the file. |
| [sym:mgt_operations_module] | Imported but no direct evidence of specific variables or types used from this module in `water_tower_read`. |
| [sym:maximum_data_module] | Imported but no direct evidence of specific variables or types used from this module in `water_tower_read`. |
| [sym:hydrograph_module] | Imported but no direct evidence of specific variables or types used from this module in `water_tower_read`. |
| [sym:constituent_mass_module] | Imported but no direct evidence of specific variables or types used from this module in `water_tower_read`. |

## File Variables

The file `water_tower.wal` contains records describing water towers or pipes for water allocation. Each record corresponds to one `type water_transfer_data` instance in the `wtow` array. The file includes a title line, a count of records, and then lines with fields for each water tower's name, initial concentrations name, maximum storage, drawdown days, water loss fraction, number of aquifers, and aquifer loss data.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wtow%name` | character (len=25) |  | name of the water tower or pipe |
| 3 |  | `wtow%init` | character (len=25) |  | name of the intitial concentrations |
| 4 |  | `wtow%stor_mx` | real | m3 | maximum storage in plant |
| 5 |  | `wtow%ddown_days` | real | days | days to drawdown the storage to zero |
| 6 |  | `wtow%loss_fr` | real |  | water loss during treatment |
| 7 |  | `wtow%num_aqu` | integer |  | number of aquifers |
| 8 |  | `wtow%aqu_loss` | type (aquifer_loss) |  | aquifer loss data structure |

## Sample

```text
Example lines from `water_tower.wal` (format inferred from reader):
Title line (string): "Water Tower Storage Data"
Number of records (integer): 2
Header line (string): "ID Name Stor_mx Ddown_days Loss_fr"
Data lines:
1 TowerA 1000.0 10.0 0.05
2 TowerB 500.0 5.0 0.02
```

## Read Pattern

```fortran
open (107,file='water_tower.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i, wtow(iwtow)%name, wtow(iwtow)%stor_mx, wtow(iwtow)%ddown_days, wtow(iwtow)%loss_fr
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='water_tower.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, wtow(iwtow)%name, wtow(iwtow)%stor_mx, wtow(iwtow)%ddown_days, wtow(iwtow)%loss_fr` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:water_tower_read] | open, read, close | Reads the `water_tower.wal` file if it exists, allocates the `wtow` array to hold water tower data, and populates each element with the water tower's name, maximum storage, drawdown days, and water loss fraction. If the file does not exist or is named "null", it allocates an empty `wtow` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The source code reads only a subset of the declared fields in `type water_transfer_data` (name, stor_mx, ddown_days, loss_fr) but the type includes additional fields (init, num_aqu, aqu_loss) which are not read here; their initialization or usage is unclear from this source.
- The sample read format is inferred from the read statements and typical file structure; no explicit example data was found in the source.
