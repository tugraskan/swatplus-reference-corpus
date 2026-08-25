---
kind: io
source_symbols:
- om_water_init
title: '`om_water.ini`'
status: filled
source_hash: 0ac8f6b35b608c10
version_label: SWAT+ 62.0.0
---

**Primary target:** `om_init_water(:)` (array of `type hyd_output`)  
**Read by:** [sym:om_water_init]

## Bottom Line

The file `om_water.ini` provides initial conditions for water volume and associated constituents in the model's hydrological output state.

It is optional; if the file does not exist or is set to "null", the model allocates empty arrays for these initial conditions.

The reader subroutine `om_water_init` loads this file, reading each record into the array `om_init_water` of type `hyd_output`.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `in_init` variable which contains the file path for `om_water.ini`. |
| [sym:input_file_module] | Provides the `in_init` variable used to access the input file name `om_water`. |
| [sym:maximum_data_module] | Provides `db_mx%om_water_init` which stores the count of records read from the file. |
| [sym:channel_data_module] | No direct variables or types used for reading or storing this file. |
| [sym:hydrograph_module] | Defines the `type hyd_output` which is the data structure used to store each record read from the file into `om_init_water`. |
| [sym:sd_channel_module] | No direct variables or types used for reading or storing this file. |
| [sym:constituent_mass_module] | No direct variables or types used for reading or storing this file. |

## File Variables

The file `om_water.ini` consists of records each representing initial hydrological output data for a spatial unit, stored as an array of `type hyd_output` in Fortran. Each record contains multiple real-valued fields representing water volume, sediment, nutrients, and other constituents.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `om_init_water%flo` | real | m^3 | volume of water |
| 3 |  | `om_init_water%sed` | real | metric tons | sediment |
| 4 |  | `om_init_water%orgn` | real | kg N | organic N |
| 5 |  | `om_init_water%sedp` | real | kg P | organic P |
| 6 |  | `om_init_water%no3` | real | kg N | NO3-N |
| 7 |  | `om_init_water%solp` | real | kg P | mineral (soluble P) |
| 8 |  | `om_init_water%chla` | real | kg | chlorophyll-a |
| 9 |  | `om_init_water%nh3` | real | kg N | NH3 |
| 10 |  | `om_init_water%no2` | real | kg N | NO2 |
| 11 |  | `om_init_water%cbod` | real | kg | carbonaceous biological oxygen demand |
| 12 |  | `om_init_water%dox` | real | kg | dissolved oxygen |
| 13 |  | `om_init_water%san` | real | tons | detached sand |
| 14 |  | `om_init_water%sil` | real | tons | detached silt |
| 15 |  | `om_init_water%cla` | real | tons | detached clay |
| 16 |  | `om_init_water%sag` | real | tons | detached small ag |
| 17 |  | `om_init_water%lag` | real | tons | detached large ag |
| 18 |  | `om_init_water%grv` | real | tons | gravel |
| 19 |  | `om_init_water%temp` | real | deg c | temperature |

## Sample

```text
Example record line from `om_water.ini` (after the leading ID):
  12345  1000.0  10.0  5.0  2.0  1.0  0.5  0.1  0.05  0.02  0.01  0.5  8.0  0.2  0.3  0.1  0.05  0.02  0.01  0.0  15.0
```

## Read Pattern

```fortran
open (105,file=in_init%om_water)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) om_init_name(ichi), om_init_water(ichi)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_init%om_water)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) om_init_name(ichi), om_init_water(ichi)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:om_water_init] | backspace, close, open, read, rewind | Reads the `om_water.ini` file to initialize the hydrological output state array `om_init_water`. It first checks if the file exists or is set to "null". If present, it counts the number of records, allocates arrays accordingly, then reads each record into `om_init_water` and the associated names into `om_init_name`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or set to "null", empty arrays are allocated.
- The reader uses multiple reads to count records before allocation, then reads data records into `om_init_water` and `om_init_name` arrays.
- No explicit sample data was found in source; the sample record line is a constructed example based on the data fields and types.
