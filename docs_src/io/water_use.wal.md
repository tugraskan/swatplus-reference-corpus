---
kind: io
source_symbols:
- water_use_read
title: '`water_use.wal`'
status: filled
source_hash: b937a9d9c19006ac
version_label: SWAT+ 62.0.0
---

**Primary target:** `wuse(:)` (array of `type water_treatment_use_data`)  
**Read by:** [sym:water_use_read]

## Bottom Line

The file `water_use.wal` configures water treatment plant parameters used in water allocation modeling within SWAT+. It is optional, as the code checks for its existence and allocates zero-length arrays if missing or set to "null".

The file defines properties such as maximum storage, lag time, water loss fraction, and constituent names and pointers for organic minerals, pesticides, pathogens, salts, and other constituents.

It also provides pesticide and pathogen concentration data for treated water effluent.

The primary reader for this file is the subroutine `water_use_read`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides file existence inquiry and possibly general input utilities used by `water_use_read`. |
| [sym:water_allocation_module] | Supplies the derived type `water_treatment_use_data` and the arrays `wuse`, `wuse_om_stor`, `wuse_om_out`, `wuse_cs_stor`, `wal_use_omd`, `wal_use_omm`, `wal_use_omy`, and `wal_use_oma` that store water treatment use data and related state read from `water_use.wal`. |
| [sym:mgt_operations_module] | Imported but no direct variables or types from this module are explicitly referenced in `water_use_read` for reading or storing this file. |
| [sym:maximum_data_module] | Provides `db_mx` which stores the maximum number of uses (`db_mx%uses`) and is used to size arrays for water use data. |
| [sym:hydrograph_module] | Imported but no direct variables or types from this module are explicitly referenced in `water_use_read` for reading or storing this file. |
| [sym:constituent_mass_module] | Supplies the derived type `constituent_mass` and the array `wuse_cs_efflu` which stores pesticide and pathogen concentration data for each water use record read from the file. |
| [sym:sd_channel_module] | Imported but no direct variables or types from this module are explicitly referenced in `water_use_read` for reading or storing this file. |

## File Variables

The `water_use.wal` file contains records defining water treatment plant parameters and associated constituent concentrations. Each record corresponds to an element of the `wuse` array of type `water_treatment_use_data`. The file includes a header block, a count of records, and then per-record data fields including names, storage capacities, lag times, loss fractions, constituent identifiers, and descriptions. Additional blocks provide pesticide and pathogen concentration arrays stored in `wuse_cs_efflu`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wuse%name` | character (len=25) |  | name of the water treatment plant |
| 3 |  | `wuse%stor_mx` | real | m3 | maximum storage in plant |
| 4 |  | `wuse%lag_days` | real | days | treatment time - lag outflow |
| 5 |  | `wuse%loss_fr` | real | fraction | water loss during treatment |
| 6 |  | `wuse%org_min` | character (len=25) |  | sediment, carbon, and nutrients |
| 7 |  | `wuse%pests` | character (len=25) |  | pesticides - ppm |
| 8 |  | `wuse%paths` | character (len=25) |  | pathogens - cfu |
| 9 |  | `wuse%hmets` | character (len=25) |  | heavy metals - ppm |
| 10 |  | `wuse%salts` | character (len=25) |  | salt ions - ppm |
| 11 |  | `wuse%constit` | character (len=25) |  | other constituents - ppm |
| 12 |  | `wuse%descrip` | character (len=80) |  | description |
| 13 |  | `wuse%iorg_min` | integer |  | sediment, carbon, and nutrients - pointer to om_use.wal |
| 14 |  | `wuse%ipests` | integer |  | pesticides |
| 15 |  | `wuse%ipaths` | integer |  | pathogens |
| 16 |  | `wuse%isalts` | integer |  | salt ions |
| 17 |  | `wuse%iconstit` | integer |  | other constituents |
| 2 |  | `wuse_cs_efflu%pest` | real | kg/ha | pesticide (kg/ha) |
| 3 |  | `wuse_cs_efflu%path` | real | cfu | pathogen (cfu) |
| 4 |  | `wuse_cs_efflu%hmet` | real | kg/ha | heavy metal (kg/ha) |
| 5 |  | `wuse_cs_efflu%salt` | real | kg/ha | salt ion mass (kg/ha) |
| 6 |  | `wuse_cs_efflu%salt_min` | real |  | salt mineral hydrographs |
| 7 |  | `wuse_cs_efflu%saltc` | real | mg/L | salt ion concentrations (mg/L) |
| 8 |  | `wuse_cs_efflu%cs` | real | kg/ha | constituent mass (kg/ha) |
| 9 |  | `wuse_cs_efflu%csc` | real | mg/L | constituent concentration (mg/L) |
| 10 |  | `wuse_cs_efflu%cs_sorb` | real | kg/ha | sorbed constituent mass (kg/ha) |
| 11 |  | `wuse_cs_efflu%csc_sorb` | real | mg/kg | sorbed constituent concentration (mg/kg) |

## Sample

```text
1 WaterTreatmentPlant1 1000.0 2.0 0.05 OrganicMinerals Pesticides Pathogens Salts OtherConstituents Description of plant
0.01 0.02 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
100 200 0.0 0.0
```

## Read Pattern

```fortran
open (107,file='water_use.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i, wuse(iwuse)%name, wuse(iwuse)%stor_mx, wuse(iwuse)%lag_days, wuse(iwuse)%loss_fr, wuse(iwuse)%org_min, wuse(iwuse)%pests, wuse(iwuse)%paths, wuse(iwuse)%salts, wuse(iwuse)%constit, wuse(iwuse)%descrip
read (107,*,iostat=eof) wuse_cs_efflu(iwuse)%pest
read (107,*,iostat=eof) wuse_cs_efflu(iwuse)%path
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='water_use.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, wuse(iwuse)%name, wuse(iwuse)%stor_mx, wuse(iwuse)%lag_days, wuse(iwuse)%loss_fr, wuse(iwuse)%org_min, wuse(iwuse)%pests, wuse(iwuse)%paths, wuse(iwuse)%salts, wuse(iwuse)%constit, wuse(iwuse)%descrip` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) wuse_cs_efflu(iwuse)%pest` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) wuse_cs_efflu(iwuse)%path` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:water_use_read] | close, open, read | Reads the `water_use.wal` file to populate the water treatment use data arrays, including water treatment plant parameters and constituent concentrations for pesticides and pathogens. It checks for file existence, allocates arrays based on the number of records, reads each record into the `wuse` array of `water_treatment_use_data`, cross-references organic mineral names to pointers, and reads pesticide and pathogen concentration arrays into `wuse_cs_efflu`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as the reader checks for its existence and allocates zero-length arrays if missing or set to "null".
- The reader crosswalks the organic mineral name to an index pointer into the organic matter use data (`om_use_name`).
- No example record from a reference dataset was found in the source; the sample read format is a plausible constructed example.
