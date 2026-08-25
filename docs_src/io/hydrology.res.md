---
kind: io
source_symbols:
- res_read_hyd
title: '`hydrology.res`'
status: filled
source_hash: 30e959f2310f0a78
version_label: SWAT+ 62.0.0
---

**Primary target:** `res_hyddb(:)` (array of `type reservoir_hyd_data`)  
**Read by:** [sym:res_read_hyd]

## Bottom Line

The input file `hydrology.res` configures reservoir hydrology parameters for the SWAT+ model, specifying reservoir properties such as surface area, volume, and operational start date.

This file is optional; if not present or set to "null", the reservoir hydrology database array is allocated empty.

The reader subroutine `res_read_hyd` loads this file and populates the `res_hyddb` array with reservoir hydrology data.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `in_res` variable which contains the filename `hyd_res` for the reservoir hydrology input file. |
| [sym:input_file_module] | Used for input file handling and possibly for file existence checks or related input utilities. |
| [sym:maximum_data_module] | Defines the `db_mx` variable where `res_hyd` maximum count is stored after reading the file. |
| [sym:reservoir_data_module] | Defines the `type reservoir_hyd_data` and the `res_hyddb` array where each record from the file is stored. |

## File Variables

The file `hydrology.res` contains tabular reservoir hydrology data records, each mapped to an element of the `res_hyddb` array of type `reservoir_hyd_data`. Each record includes reservoir name, operational start year and month, surface areas, volumes, hydraulic conductivity, evaporation coefficient, and volume-surface area coefficients.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `res_hyddb%name` | character(len=25) |  | Reservoir name identifier |
| 3 |  | `res_hyddb%iyres` | integer | none | Year of the simulation when the reservoir becomes operational |
| 4 |  | `res_hyddb%mores` | integer | none | Month of the simulation when the reservoir becomes operational |
| 5 |  | `res_hyddb%psa` | real | ha | Reservoir surface area when filled to principal spillway |
| 6 |  | `res_hyddb%pvol` | real | ha-m | Volume of water to fill reservoir to principal spillway (read in as ha-m) |
| 7 |  | `res_hyddb%esa` | real |  | Reservoir surface area when filled to emergency spillway (converted to m^3) |
| 8 |  | `res_hyddb%evol` | real | ha-m | Volume of water to fill reservoir to emergency spillway (read in as ha-m) |
| 9 |  | `res_hyddb%k` | real |  | Hydraulic conductivity of the reservoir bottom |
| 10 |  | `res_hyddb%evrsv` | real | none | Lake evaporation coefficient |
| 11 |  | `res_hyddb%br1` | real | none | Volume-surface area coefficient for reservoirs (model estimates if zero) |
| 12 |  | `res_hyddb%br2` | real | none | Volume-surface area coefficient for reservoirs (model estimates if zero) |

## Sample

```text
Example record format (fields separated by spaces or tabs):
ReservoirName 2000 5 10.0 500.0 15.0 600.0 0.01 0.7 0.0 0.0
```

## Read Pattern

```fortran
open (105,file=in_res%hyd_res)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
read (105,*,iostat=eof) res_hyddb(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_res%hyd_res)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) res_hyddb(ires)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_hyd] | close, open, read, rewind | Reads the reservoir hydrology input file `hydrology.res` and populates the `res_hyddb` array with reservoir hydrology data. It first checks if the file exists and is not set to "null". If present, it counts the number of reservoir records, allocates the array, rewinds the file, and reads each reservoir record into the array. It also applies default values and corrections to certain fields if they are zero or missing. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or set to "null", an empty reservoir hydrology array is allocated.
- Default values for volume and surface area fields are set in the reader if input values are zero or missing.
- The sample read format is inferred from the type declaration and typical usage; no explicit example record was found in the source.
