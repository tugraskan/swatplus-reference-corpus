---
kind: io
source_symbols:
- water_osrc_read
title: '`out_src.wal`'
status: filled
source_hash: e9d543c7662677ff
version_label: SWAT+ 62.0.0
---

**Primary target:** `osrc(:)` (array of `type outside_basin_source`)  
**Read by:** [sym:water_osrc_read]

## Bottom Line

The file `out_src.wal` configures outside basin water sources used in the SWAT+ model, specifying properties such as storage capacity, treatment lag, water loss, and constituent pointers.

This file is optional; if it does not exist or is named "null", an empty allocation is made.

The reader `water_osrc_read` loads this file and populates the `osrc` array of `type outside_basin_source` and associated constituent mass arrays `osrc_cs`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides file existence inquiry and related input utilities used by `water_osrc_read`. |
| [sym:water_allocation_module] | Defines the `outside_basin_source` type and the `osrc` array where the file data is stored. |
| [sym:recall_module] | Used for recalling or managing model state; exact variables used are not explicitly shown in the reader source. |
| [sym:mgt_operations_module] | Imported but no explicit variables or types used in the reader source. |
| [sym:maximum_data_module] | Provides `db_mx` which stores `out_src` maximum count read from the file. |
| [sym:hydrograph_module] | Imported but no explicit variables or types used in the reader source. |
| [sym:constituent_mass_module] | Defines the `constituent_mass` type and the `osrc_cs` array where constituent concentrations for pesticides and pathogens are stored. |
| [sym:sd_channel_module] | Imported but no explicit variables or types used in the reader source. |

## File Variables

The file `out_src.wal` contains records describing outside basin water sources, each with properties such as name, maximum storage, treatment lag time, water loss fraction, and pointers to constituent data. The reader maps each record into an element of the `osrc` array of `type outside_basin_source` and reads associated constituent mass data into `osrc_cs` arrays.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `osrc%name` | character (len=25) |  | name of outside basin source |
| 3 |  | `osrc%stor_mx` | real | m3 | m3 !maximum storage in plant |
| 4 |  | `osrc%lag_days` | real | days | days !treatement time - lag outflow |
| 5 |  | `osrc%loss_fr` | real |  | water loss during treament |
| 6 |  | `osrc%iorg_min` | integer |  | sediment, carbon, and nutrients - pointer to om_use.wal |
| 7 |  | `osrc%ipests` | integer |  | pesticides |
| 8 |  | `osrc%ipaths` | integer |  | pathogens |
| 9 |  | `osrc%isalts` | integer |  | salt ions |
| 10 |  | `osrc%iconstit` | integer |  | other constituents |
| 2 |  | `osrc_cs%pest` | real | kg/ha | pesticide (kg/ha) |
| 3 |  | `osrc_cs%path` | real | cfu | pathogen (cfu) |
| 4 |  | `osrc_cs%hmet` | real | kg/ha | heavy metal (kg/ha) |
| 5 |  | `osrc_cs%salt` | real | kg/ha | salt ion mass (kg/ha) |
| 6 |  | `osrc_cs%salt_min` | real |  | salt mineral hydrographs |
| 7 |  | `osrc_cs%saltc` | real | mg/L | salt ion concentrations (mg/L) |
| 8 |  | `osrc_cs%cs` | real | kg/ha | constituent mass (kg/ha) |
| 9 |  | `osrc_cs%csc` | real | mg/L | constituent concentration (mg/L) |
| 10 |  | `osrc_cs%cs_sorb` | real | kg/ha | sorbed constituent mass (kg/ha) |
| 11 |  | `osrc_cs%csc_sorb` | real | mg/kg | sorbed constituent concentration (mg/kg) |

## Sample

```text
1 OutsideSource1 10000.0 2.0 0.05
0.1 0.0 0.0 0.0 0.0
PathogenHeader
0.0
```

## Read Pattern

```fortran
open (107,file='out_src.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i, osrc(isrc)%name, osrc(isrc)%stor_mx, osrc(isrc)%lag_days, osrc(isrc)%loss_fr
read (107,*,iostat=eof) osrc_cs(isrc)%pest
read (107,*,iostat=eof) osrc_cs(isrc)%path
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='out_src.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, osrc(isrc)%name, osrc(isrc)%stor_mx, osrc(isrc)%lag_days, osrc(isrc)%loss_fr` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) osrc_cs(isrc)%pest` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) osrc_cs(isrc)%path` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:water_osrc_read] | open, read, close | Reads the `out_src.wal` file to populate the array of outside basin water sources (`osrc`) and their associated constituent mass data (`osrc_cs`). Handles file existence check and allocates arrays accordingly. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `out_src.wal` is optional; if missing or named "null", an empty `osrc` allocation is made.
- The reader reads only pesticide and pathogen constituent masses if the corresponding counts in `cs_db` are greater than zero; other constituent types are not read in this source code.
- The sample read format is inferred from the read statements and typical data structure but no explicit example block was found in the source.
