---
kind: io
source_symbols:
- water_treatment_read
title: '`water_treat.wal`'
status: filled
source_hash: 6929dd2f1287e8b9
version_label: SWAT+ 62.0.0
---

**Primary target:** `wtp(:)` (array of `type water_treatment_use_data`)  
**Read by:** [sym:water_treatment_read]

## Bottom Line

The file `water_treat.wal` configures water treatment plant parameters including storage, lag time, losses, and constituent names and descriptions.

It is optional; if the file does not exist or is set to "null", no water treatment plants are allocated.

The primary reader for this file is the subroutine `water_treatment_read`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides file handling utilities and possibly global input file state used by `water_treatment_read`. |
| [sym:water_allocation_module] | Defines the derived type `water_treatment_use_data` and variables such as `wtp`, `wtp_om_stor`, `wtp_cs_stor`, `wtp_om_out`, and arrays for organic matter treatment crosswalks used to store water treatment plant data read from the file. |
| [sym:mgt_operations_module] | Used for management operation data structures or constants referenced during reading or allocation (exact variables not explicitly shown in source). |
| [sym:maximum_data_module] | Provides the global maximum counts such as `db_mx%treat` and `db_mx%om_treat` used to dimension arrays and loop limits. |
| [sym:hydrograph_module] | Defines hydrograph data structures used for storage and treatment outputs, e.g., `wtp_om_stor`, `wal_tr_omd`, `wal_tr_omm`, `wal_tr_omy`, `wal_tr_oma` arrays allocated in the reader. |
| [sym:constituent_mass_module] | Defines the derived type `constituent_mass` and variables like `wtp_cs_treat` used to store pesticide and pathogen concentrations read from the file. |

## File Variables

The file `water_treat.wal` contains records describing water treatment plants and their associated constituent concentrations. Each record corresponds to one water treatment plant and includes plant metadata, storage and lag parameters, and constituent names and descriptions. Additional lines provide pesticide and pathogen concentration data arrays for each plant. These data are read into arrays of derived types `water_treatment_use_data` and `constituent_mass`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wtp%name` | character (len=25) |  | name of the water treatment plant |
| 3 |  | `wtp%stor_mx` | real | m3 | maximum storage in plant |
| 4 |  | `wtp%lag_days` | real | days | treatment time - lag outflow |
| 5 |  | `wtp%loss_fr` | real | fraction | water loss during treatment |
| 6 |  | `wtp%org_min` | character (len=25) |  | sediment, carbon, and nutrients |
| 7 |  | `wtp%pests` | character (len=25) |  | pesticides - ppm |
| 8 |  | `wtp%paths` | character (len=25) |  | pathogens - cfu |
| 9 |  | `wtp%hmets` | character (len=25) |  | heavy metals - ppm |
| 10 |  | `wtp%salts` | character (len=25) |  | salt ions - ppm |
| 11 |  | `wtp%constit` | character (len=25) |  | other constituents - ppm |
| 12 |  | `wtp%descrip` | character (len=80) |  | description |
| 13 |  | `wtp%iorg_min` | integer |  | sediment, carbon, and nutrients - pointer to om_use.wal |
| 14 |  | `wtp%ipests` | integer |  | pesticides |
| 15 |  | `wtp%ipaths` | integer |  | pathogens |
| 16 |  | `wtp%isalts` | integer |  | salt ions |
| 17 |  | `wtp%iconstit` | integer |  | other constituents |
| 2 |  | `wtp_cs_treat%pest` | real | kg/ha | pesticide (kg/ha) |
| 3 |  | `wtp_cs_treat%path` | real | cfu | pathogen (cfu) |
| 4 |  | `wtp_cs_treat%hmet` | real | kg/ha | heavy metal (kg/ha) |
| 5 |  | `wtp_cs_treat%salt` | real | kg/ha | salt ion mass (kg/ha) |
| 6 |  | `wtp_cs_treat%salt_min` | real |  | salt mineral hydrographs |
| 7 |  | `wtp_cs_treat%saltc` | real | mg/L | salt ion concentrations (mg/L) |
| 8 |  | `wtp_cs_treat%cs` | real | kg/ha | constituent mass (kg/ha) |
| 9 |  | `wtp_cs_treat%csc` | real | mg/L | constituent concentration (mg/L) |
| 10 |  | `wtp_cs_treat%cs_sorb` | real | kg/ha | sorbed constituent mass (kg/ha) |
| 11 |  | `wtp_cs_treat%csc_sorb` | real | mg/kg | sorbed constituent concentration (mg/kg) |

## Sample

```text
1 PlantA 1000.0 2.0 0.05 OrgMinGroup PestGroup PathGroup HMetGroup SaltGroup ConstitGroup Description text
0
0.01 0.02 0.03
0
100 200 300
```

## Read Pattern

```fortran
open (107,file='water_treat.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i, wtp(iwtp)%name, wtp(iwtp)%stor_mx, wtp(iwtp)%lag_days, wtp(iwtp)%loss_fr, wtp(iwtp)%org_min, wtp(iwtp)%pests, wtp(iwtp)%paths, wtp(iwtp)%salts, wtp(iwtp)%constit, wtp(iwtp)%descrip
read (107,*,iostat=eof) wtp_cs_treat(iwtp)%pest
read (107,*,iostat=eof) wtp_cs_treat(iwtp)%path
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='water_treat.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, wtp(iwtp)%name, wtp(iwtp)%stor_mx, wtp(iwtp)%lag_days, wtp(iwtp)%loss_fr, wtp(iwtp)%org_min, wtp(iwtp)%pests, wtp(iwtp)%paths, wtp(iwtp)%salts, wtp(iwtp)%constit, wtp(iwtp)%descrip` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) wtp_cs_treat(iwtp)%pest` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) wtp_cs_treat(iwtp)%path` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:water_treatment_read] | open, read, close | Reads the water treatment plant configuration file `water_treat.wal`. It checks if the file exists, then reads the number of water treatment plants, allocates arrays accordingly, and reads each plant's parameters and constituent concentration data into the arrays `wtp` and `wtp_cs_treat`. |

## Review Notes

- The file `water_treat.wal` is optional; if missing or set to "null", no water treatment plants are allocated.
- The reader crosswalks organic mineral names to indices in `om_treat_name` from `maximum_data_module`.
- Pesticide and pathogen concentrations are read only if the corresponding counts in `cs_db` are greater than zero.
- Sample read format is inferred from the read statements and type declarations; no explicit example record was found in the source.
