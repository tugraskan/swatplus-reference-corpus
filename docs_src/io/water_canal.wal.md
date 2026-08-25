---
kind: io
source_symbols:
- water_canal_read
title: '`water_canal.wal`'
status: filled
source_hash: 0bfe8ce37babc4b3
version_label: SWAT+ 62.0.0
---

**Primary target:** `canal(:)` (array of `type water_canal_data`)  
**Read by:** [sym:water_canal_read]

## Bottom Line

The file `water_canal.wal` configures water canal parameters including geometry, operational timing, water loss, and aquifer seepage losses for the SWAT+ model.

It is optional; if the file does not exist or is set to "null", the canal array is allocated with zero size and no canal data is loaded.

The reader subroutine `water_canal_read` loads this file and populates the `canal` array of type `water_canal_data`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides general input file handling utilities used by `water_canal_read`. |
| [sym:water_allocation_module] | Defines the `water_canal_data` type and related variables such as `canal`, `canal_om_stor`, `canal_om_out`, and `canal_cs_stor` which are allocated and populated by `water_canal_read`. |
| [sym:mgt_operations_module] | Imported but no direct evidence of specific types or variables used from this module in `water_canal_read`. |
| [sym:maximum_data_module] | Provides `db_mx` which stores the maximum number of canals (`db_mx%canal`) read from the file. |
| [sym:hydrograph_module] | Imported but no direct evidence of specific types or variables used from this module in `water_canal_read`. |
| [sym:constituent_mass_module] | Imported but no direct evidence of specific types or variables used from this module in `water_canal_read`. |

## File Variables

The file `water_canal.wal` contains records describing water canal characteristics and operational parameters. Each record corresponds to one canal and is read into an element of the `canal` array of type `water_canal_data`. The file includes canal geometry, operational timing, water loss factors, and aquifer seepage loss data.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `canal%name` | character (len=25) |  | name of the canal |
| 3 |  | `canal%w_sta` | character (len=25) |  | name of nearby weather station |
| 4 |  | `canal%init` | character (len=25) |  | name of the intitial concentrations in canal |
| 5 |  | `canal%dtbl` | character (len=25) |  | name of decision table to determine canal outflow |
| 6 |  | `canal%ddown_days` | real | days | days !days to drawdown the storage to zero |
| 7 |  | `canal%w` | real | m | m !top width of canal |
| 8 |  | `canal%d` | real | m | m !depth of canal |
| 9 |  | `canal%s` | real | m | m !slope of canal |
| 10 |  | `canal%ss` | real | m/m | m/m !side slope of trapezoidal canal |
| 11 |  | `canal%sat_con` | real |  | to compute percolation from canal to groundwater |
| 12 |  | `canal%loss_fr` | real |  | water loss during treament |
| 13 |  | `canal%bed_thick` | real | m | m !bed sediment thickness for Darcy seepage (gwflow; 0 if not used) |
| 14 |  | `canal%div_id` | integer |  | recall diversion ID (gwflow; 0 if wallo-routed) |
| 15 |  | `canal%day_beg` | integer |  | Julian day canal begins operation (gwflow external; 0 otherwise) |
| 16 |  | `canal%day_end` | integer |  | Julian day canal ends operation (gwflow external; 0 otherwise) |
| 17 |  | `canal%num_aqu` | integer |  | number of aquifers |
| 18 |  | `canal%aqu_loss` | type (aquifer_loss) |  | array of aquifer loss data for each aquifer associated with the canal |

## Sample

```text
1 'MainCanal' 'WeatherStation1' 'InitConc' 'DecisionTbl1' 10.0 5.0 2.0 0.01 0.5 0.8 0.05 0 0 365 2
1 'MainCanal' 'WeatherStation1' 'InitConc' 'DecisionTbl1' 10.0 5.0 2.0 0.01 0.5 0.8 0.05 0 0 365 2 0.1 0.2 0.3 0.4
```

## Read Pattern

```fortran
open (107,file='water_canal.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i, canal(ic)%name, canal(ic)%w_sta, canal(ic)%init, canal(ic)%dtbl, canal(ic)%ddown_days, canal(ic)%w, canal(ic)%d, canal(ic)%s, canal(ic)%ss, canal(ic)%sat_con, canal(ic)%loss_fr, canal(ic)%bed_thick, canal(ic)%div_id, canal(ic)%day_beg, canal(ic)%day_end, num_aqu
backspace (107)
read (107,*,iostat=eof) i, canal(ic)%name, canal(ic)%w_sta, canal(ic)%init, canal(ic)%dtbl, canal(ic)%ddown_days, canal(ic)%w, canal(ic)%d, canal(ic)%s, canal(ic)%ss, canal(ic)%sat_con, canal(ic)%loss_fr, canal(ic)%bed_thick, canal(ic)%div_id, canal(ic)%day_beg, canal(ic)%day_end, canal(ic)%num_aqu, (canal(ic)%aqu_loss(iaq), iaq = 1, num_aqu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='water_canal.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, canal(ic)%name, canal(ic)%w_sta, canal(ic)%init, canal(ic)%dtbl, canal(ic)%ddown_days, canal(ic)%w, canal(ic)%d, canal(ic)%s, canal(ic)%ss, canal(ic)%sat_con, canal(ic)%loss_fr, canal(ic)%bed_thick, canal(ic)%div_id, canal(ic)%day_beg, canal(ic)%day_end, num_aqu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, canal(ic)%name, canal(ic)%w_sta, canal(ic)%init, canal(ic)%dtbl, canal(ic)%ddown_days, canal(ic)%w, canal(ic)%d, canal(ic)%s, canal(ic)%ss, canal(ic)%sat_con, canal(ic)%loss_fr, canal(ic)%bed_thick, canal(ic)%div_id, canal(ic)%day_beg, canal(ic)%day_end, canal(ic)%num_aqu, (canal(ic)%aqu_loss(iaq), iaq = 1, num_aqu)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:water_canal_read] | backspace, close, open, read | Reads the file `water_canal.wal` if it exists and is not set to "null". It reads the header lines to determine the number of canal records, allocates arrays for canal data and related storage and output variables, then reads each canal record including aquifer loss data. If the file does not exist, it allocates the canal array with zero size. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The reader imports several modules but only `water_allocation_module` and `maximum_data_module` have clearly used variables or types in this routine.
- The file is optional; if missing or set to "null", no canal data is loaded.
- Aquifer loss data is read as a variable-length array per canal, requiring a backspace and second read per record.
- No sample data was found in the source; the sample read format is a constructed example based on the read statement and type fields.
