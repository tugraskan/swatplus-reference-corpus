---
kind: io
source_symbols:
- om_treat_read
title: '`om_treat.wal`'
status: filled
source_hash: ba7a048f81acc6f2
version_label: SWAT+ 62.0.0
---

**Primary target:** `wtp_om_treat(:)` (array of `type hyd_output`)  
**Read by:** [sym:om_treat_read]

## Bottom Line

The file `om_treat.wal` contains water allocation treatment data for hydrological output variables.

It is optional; if the file does not exist or is named 'null', empty arrays are allocated.

The reader subroutine `om_treat_read` loads this file, reading an array of treatment records into `wtp_om_treat` and their names into `om_treat_name`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the variable `om_treat_name` which stores the names of the water allocation treatments read from the file. |
| [sym:water_allocation_module] | Provides the variable `wtp_om_treat`, an array of `type hyd_output`, which stores the water allocation treatment data read from the file. |
| [sym:mgt_operations_module] | Imported but no specific variables or types from this module are directly referenced in the reader. |
| [sym:maximum_data_module] | Provides the variable `db_mx%om_treat` which stores the maximum number of water allocation treatments read from the file. |
| [sym:hydrograph_module] | Defines the derived type `hyd_output` used for `wtp_om_treat` to hold hydrological output variables. |
| [sym:constituent_mass_module] | Imported but no specific variables or types from this module are directly referenced in the reader. |

## File Variables

The file `om_treat.wal` consists of a header section followed by multiple records, each containing a treatment name and a set of hydrological output variables. Each record is read into an element of the `wtp_om_treat` array of type `hyd_output`, with corresponding names stored in `om_treat_name`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wtp_om_treat%flo` | real | m^3 | volume of water |
| 3 |  | `wtp_om_treat%sed` | real | metric tons | sediment |
| 4 |  | `wtp_om_treat%orgn` | real | kg N | organic N |
| 5 |  | `wtp_om_treat%sedp` | real | kg P | organic P |
| 6 |  | `wtp_om_treat%no3` | real | kg N | NO3-N |
| 7 |  | `wtp_om_treat%solp` | real | kg P | mineral (soluble P) |
| 8 |  | `wtp_om_treat%chla` | real | kg | chlorophyll-a |
| 9 |  | `wtp_om_treat%nh3` | real | kg N | NH3 |
| 10 |  | `wtp_om_treat%no2` | real | kg N | NO2 |
| 11 |  | `wtp_om_treat%cbod` | real | kg | carbonaceous biological oxygen demand |
| 12 |  | `wtp_om_treat%dox` | real | kg | dissolved oxygen |
| 13 |  | `wtp_om_treat%san` | real | tons | detached sand |
| 14 |  | `wtp_om_treat%sil` | real | tons | detached silt |
| 15 |  | `wtp_om_treat%cla` | real | tons | detached clay |
| 16 |  | `wtp_om_treat%sag` | real | tons | detached small ag |
| 17 |  | `wtp_om_treat%lag` | real | tons | detached large ag |
| 18 |  | `wtp_om_treat%grv` | real | tons | gravel |
| 19 |  | `wtp_om_treat%temp` | real | deg c | temperature |

## Sample

```text
Example record format from `om_treat.wal` (not from source, illustrative only):
TreatmentName  1000.0  2.5  10.0  1.5  5.0  0.5  0.2  0.1  0.05  0.3  8.0  0.1  0.2  0.3  0.05  0.02  0.01  0.005  15.0
```

## Read Pattern

```fortran
open (107,file='om_treat.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) om_treat_name(iom_tr), wtp_om_treat(iom_tr)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='om_treat.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) om_treat_name(iom_tr), wtp_om_treat(iom_tr)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:om_treat_read] | close, open, read | Reads the water allocation treatment file `om_treat.wal` if it exists and is not named 'null'. It reads a header and the number of treatment records, allocates arrays accordingly, and reads each treatment's name and hydrological output data into `om_treat_name` and `wtp_om_treat` respectively. If the file does not exist or is 'null', it allocates empty arrays. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; the reader handles missing or 'null' file by allocating zero-length arrays.
- No explicit sample data record is present in source; sample format is illustrative based on variable types and order.
