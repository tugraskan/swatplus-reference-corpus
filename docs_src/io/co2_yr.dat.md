---
kind: io
source_symbols:
- co2_read
title: '`co2_yr.dat`'
status: filled
source_hash: 5c3047cbac6a83b3
version_label: SWAT+ 62.0.0
---

**Primary target:** co2_inc  
**Read by:** [sym:co2_read]

## Bottom Line

The file `co2_yr.dat` provides annual atmospheric CO2 concentration data used to configure the model's CO2 time series state.

It is optional; if missing or empty, the model defaults to a constant CO2 value from basin parameters.

The reader subroutine `co2_read` loads this file and populates the derived type `co2_inc` with year and CO2 data.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `open_output_file` procedure used to open the CO2 output file. |
| [sym:basin_module] | Provides the `bsn_prm` variable, specifically `bsn_prm%co2`, used as a default CO2 value if the input file is missing. |
| [sym:time_module] | Provides the `time` variable with fields `nbyr`, `yrc`, and `yrc_start` used to size and index the CO2 time series arrays. |
| [sym:climate_module] | Provides the `co2y` array that stores the final CO2 time series for the simulation period. |
| [sym:output_path_module] | No direct variables or types used from this module in the reader. |

## File Variables

The file `co2_yr.dat` is read sequentially with three header lines followed by annual CO2 data lines. The reader maps these lines into a derived type `co2_annual` containing the number of years and an array of `co2` records with year and CO2 concentration.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Title line` | `titldum` |  |  | The first line read as a character string representing a title or description of the CO2 data file. |
| 1 | `Number of years` | `co2_inc%yrs` |  |  | An integer specifying the number of annual CO2 records that follow in the file. |
| 1 | `Header line` | `header` |  |  | A second character string header line, likely describing the data columns or units. |
| 1 | `Annual CO2 records` | `co2_inc%co2_yr(itot)` |  |  | Each subsequent line contains a record of year and CO2 concentration, stored in the `co2_inc%co2_yr` array. |

## Sample

```text
Example `co2_yr.dat` content:
Atmospheric CO2 Data for Model
50
Year CO2(ppm)
1850 280.0
1851 281.2
1852 282.5
...
1899 295.3
```

## Read Pattern

```fortran
open (107,file="co2_yr.dat")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) co2_inc%yrs
read (107,*,iostat=eof) header
read (107,*,iostat=eof) co2_inc%co2_yr(itot)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="co2_yr.dat")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) co2_inc%yrs` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) co2_inc%co2_yr(itot)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:co2_read] | close, open, read | Reads the annual atmospheric CO2 concentration data from `co2_yr.dat` into the derived type `co2_inc`. It handles missing or absent files by defaulting to a constant CO2 value from basin parameters. It also populates the simulation CO2 time series array `co2y` for the model's time span. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
