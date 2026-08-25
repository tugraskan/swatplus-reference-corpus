---
kind: io
source_symbols:
- om_osrc_read
title: '`om_osrc.wal`'
status: filled
source_hash: ed221937f8637e55
version_label: SWAT+ 62.0.0
---

**Primary target:** `osrc_om(:)` (array of `type hyd_output`)  
**Read by:** [sym:om_osrc_read]

## Bottom Line

The file `om_osrc.wal` contains water allocation output data records, each representing hydrological and constituent mass outputs for a water allocation source.

This file is optional; if it does not exist or is named "null", the arrays are allocated empty.

The reader subroutine `om_osrc_read` loads this file and populates the arrays `osrc_om` and `om_osrc_name` with the data.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `om_osrc_name` array to store source names read from the file. |
| [sym:water_allocation_module] | provides the `db_mx` variable, whose `om_treat` field is set to the number of records read (`imax`). |
| [sym:mgt_operations_module] | used but no specific variables or types are referenced in the reader for this file. |
| [sym:maximum_data_module] | used but no specific variables or types are referenced in the reader for this file. |
| [sym:hydrograph_module] | provides the `type hyd_output` and the `osrc_om` array of this type, which stores the hydrological output data read from the file. |
| [sym:constituent_mass_module] | used but no specific variables or types are referenced in the reader for this file. |

## File Variables

Each record in `om_osrc.wal` corresponds to one water allocation source's hydrological output data, stored in an array element of type `hyd_output`. The file columns map directly to the components of `type hyd_output` declared in `hydrograph_module`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `osrc_om%flo` | real | m^3 | volume of water |
| 3 |  | `osrc_om%sed` | real | metric tons | sediment |
| 4 |  | `osrc_om%orgn` | real | kg N | organic N |
| 5 |  | `osrc_om%sedp` | real | kg P | organic P |
| 6 |  | `osrc_om%no3` | real | kg N | NO3-N |
| 7 |  | `osrc_om%solp` | real | kg P | mineral (soluble P) |
| 8 |  | `osrc_om%chla` | real | kg | chlorophyll-a |
| 9 |  | `osrc_om%nh3` | real | kg N | NH3 |
| 10 |  | `osrc_om%no2` | real | kg N | NO2 |
| 11 |  | `osrc_om%cbod` | real | kg | carbonaceous biological oxygen demand |
| 12 |  | `osrc_om%dox` | real | kg | dissolved oxygen |
| 13 |  | `osrc_om%san` | real | tons | detached sand |
| 14 |  | `osrc_om%sil` | real | tons | detached silt |
| 15 |  | `osrc_om%cla` | real | tons | detached clay |
| 16 |  | `osrc_om%sag` | real | tons | detached small ag |
| 17 |  | `osrc_om%lag` | real | tons | detached large ag |
| 18 |  | `osrc_om%grv` | real | tons | gravel |
| 19 |  | `osrc_om%temp` | real | deg c | temperature |

## Sample

```text
Example record format from `om_osrc.wal` (fields separated by spaces):
"SourceName 1000.0 0.5 10.0 2.0 5.0 1.0 0.1 0.05 0.02 0.01 0.5 8.0 0.1 0.2 0.3 0.05 0.07 0.1 15.0"
Where the first field is the source name (string), followed by the hyd_output fields in order.
```

## Read Pattern

```fortran
open (107,file='om_osrc.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) om_osrc_name(iom_osrc), osrc_om(iom_osrc)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='om_osrc.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) om_osrc_name(iom_osrc), osrc_om(iom_osrc)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:om_osrc_read] | open, read, close | Reads the optional file `om_osrc.wal` containing water allocation hydrological output data. If the file exists and is not named "null", it reads the number of records, allocates arrays `osrc_om` and `om_osrc_name`, and reads each record into these arrays. It also sets the `db_mx%om_treat` variable to the number of records read. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `om_osrc.wal` is optional; if missing or named "null", empty arrays are allocated.
- The reader sets `db_mx%om_treat` to the number of records read, indicating the count of water allocation sources loaded.
- No sample data was found in the source; the sample read format is a constructed example based on the type definition and read pattern.
