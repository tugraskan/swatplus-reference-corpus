---
kind: io
source_symbols:
- urban_parm_read
title: '`urban.urb`'
status: filled
source_hash: 2afc81c87d5c7955
version_label: SWAT+ 62.0.0
---

**Primary target:** `urbdb(:)` (array of `type urban_db`)  
**Read by:** [sym:urban_parm_read]

## Bottom Line

The `urban.urb` input file configures urban land use parameters related to impervious surfaces and pollutant buildup/removal characteristics for Hydrologic Response Units (HRUs).

It is optional; if the file does not exist or is set to "null", an empty urban database array is allocated.

The file is read by the `urban_parm_read` subroutine, which loads its records into the `urbdb` array of `type urban_db`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_parmdb` variable that contains the filename for `urban_urb` used to open the input file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable whose `urban` field is set to the number of urban records read (imax). |
| [sym:urban_data_module] | Defines the `type urban_db` and the `urbdb` array where each record from the file is stored. |

## File Variables

The `urban.urb` file contains tabular records describing urban land use parameters for impervious areas, each record mapping to one element of the `urbdb` array of derived type `urban_db`. Each record includes fields such as urban name, impervious fractions, curb density, wash-off coefficients, pollutant buildup limits, and curve numbers.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `urbdb%urbnm` | character(len=16) |  | Urban land use name or identifier |
| 3 |  | `urbdb%fimp` | real | fraction | fraction of HRU area that is impervious |
| 4 |  | `urbdb%fcimp` | real | fraction | fraction of HRU classified as directly connected impervious |
| 5 |  | `urbdb%curbden` | real | km/ha | curb length density |
| 6 |  | `urbdb%urbcoef` | real | 1/mm | wash-off coefficient for removal of constituents from impervious surfaces |
| 7 |  | `urbdb%dirtmx` | real | kg/curb km | maximum amount of solids allowed to build up on impervious surfaces |
| 8 |  | `urbdb%thalf` | real | days | time for solids on impervious areas to build up to half the maximum level |
| 9 |  | `urbdb%tnconc` | real | mg N/kg sed | concentration of total nitrogen in suspended solids from impervious areas |
| 10 |  | `urbdb%tpconc` | real | mg P/kg sed | concentration of total phosphorus in suspended solids from impervious areas |
| 11 |  | `urbdb%tno3conc` | real | mg NO3-N/kg sed | concentration of nitrate nitrogen in suspended solids from impervious areas |
| 12 |  | `urbdb%urbcn2` | real | none | moisture condition II curve number for impervious areas |

## Sample

```text
Example record format (fields separated by spaces or tabs):
urbnm fimp fcimp curbden urbcoef dirtmx thalf tnconc tpconc tno3conc urbcn2
e.g.:
Urban01 0.10 0.08 0.5 0.02 1200.0 2.0 15.0 2.5 1.0 85.0
```

## Read Pattern

```fortran
open (108,file=in_parmdb%urban_urb)
read (108,*,iostat=eof) titldum
read (108,*,iostat=eof) header
rewind (108)
read (108,*,iostat=eof) urbdb(iu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 108 | `open (108,file=in_parmdb%urban_urb)` |
| Input | `read` | 108 | `read (108,*,iostat=eof) titldum` |
| Input | `read` | 108 | `read (108,*,iostat=eof) header` |
| Input | `read` | 108 | `read (108,*,iostat=eof) titldum` |
| File control | `rewind` | 108 | `rewind (108)` |
| Input | `read` | 108 | `read (108,*,iostat=eof) titldum` |
| Input | `read` | 108 | `read (108,*,iostat=eof) header` |
| Input | `read` | 108 | `read (108,*,iostat=eof) urbdb(iu)` |
| File control | `close` | 108 | `close (108)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:urban_parm_read] | open, read, rewind, close | Reads the `urban.urb` file if it exists and is not set to "null", counts the number of records, allocates the `urbdb` array accordingly, and loads each record into `urbdb`. If the file does not exist or is "null", allocates an empty `urbdb` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and can be disabled by setting its filename to "null" or by absence.
- The reader uses a two-pass approach: first counting records, then reading them into the allocated array.
- No sample data records were found in the source; the sample format is inferred from the type definition.
