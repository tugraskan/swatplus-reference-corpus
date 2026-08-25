---
kind: io
source_symbols:
- soil_plant_init
title: '`soil_plant.ini`'
status: filled
source_hash: 2601642861994e67
version_label: SWAT+ 62.0.0
---

**Primary target:** `sol_plt_ini(:)` (array of `type soil_plant_initialize`)  
**Read by:** [sym:soil_plant_init]

## Bottom Line

The file `soil_plant.ini` configures soil-plant export coefficients used in water quality modeling within SWAT+.

It is optional and only read if the file exists or is not set to "null" in the initialization input.

The reader subroutine `soil_plant_init` loads this file, storing each record into the array `sol_plt_ini` of type `soil_plant_initialize`.

| Module | Role for this file |
| --- | --- |
| [sym:hru_module] | Provides the derived type `soil_plant_initialize` and the array `sol_plt_ini` where the file data are stored. |
| [sym:basin_module] | Provides the variable `bsn_cc%nam1` which controls conditional reading of the `csc` field in the input records. |
| [sym:input_file_module] | Provides the input file path variable `in_init%soil_plant_ini` used to locate the `soil_plant.ini` file. |
| [sym:maximum_data_module] | Provides the variable `db_mx%sol_plt_ini` which stores the number of records read from the file. |
| [sym:constituent_mass_module] | No direct usage evident in the reader for this file. |

## File Variables

The `soil_plant.ini` file consists of records defining soil-plant export coefficients, each mapped to an element of the `sol_plt_ini` array of type `soil_plant_initialize`. Each record includes a name, fractional soil water content, character codes for nutrient and pesticide constituents, and integer flags or indices for these constituents.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `sol_plt_ini%name` | character(len=40) |  | Name identifier for the soil-plant export coefficient record. |
| 3 |  | `sol_plt_ini%sw_frac` | real |  | Fraction of soil water content associated with this export coefficient. |
| 4 |  | `sol_plt_ini%nutc` | character(len=40) |  | Character code for nutrient constituent associated with this record. |
| 5 |  | `sol_plt_ini%pestc` | character(len=40) |  | Character code for pesticide constituent associated with this record. |
| 6 |  | `sol_plt_ini%pathc` | character(len=40) |  | Character code for pathogen constituent associated with this record. |
| 7 |  | `sol_plt_ini%saltc` | character(len=40) |  | Character code for salt constituent associated with this record. |
| 8 |  | `sol_plt_ini%hmetc` | character(len=40) |  | Character code for herbicide/metabolite constituent associated with this record. |
| 9 |  | `sol_plt_ini%csc` | character(len=40) |  | Character code for constituent source control (rtb cs). |
| 10 |  | `sol_plt_ini%nut` | integer |  | Integer flag or index related to nutrient constituent. |
| 11 |  | `sol_plt_ini%pest` | integer |  | Integer flag or index related to pesticide constituent. |
| 12 |  | `sol_plt_ini%path` | integer |  | Integer flag or index related to pathogen constituent. |
| 13 |  | `sol_plt_ini%salt` | integer |  | Integer flag or index related to salt constituent. |
| 14 |  | `sol_plt_ini%hmet` | integer |  | Integer flag or index related to herbicide/metabolite constituent. |
| 15 |  | `sol_plt_ini%cs` | integer |  | Integer flag or index related to constituent source control (rtb cs). |

## Sample

```text
Example record lines from `soil_plant.ini` might look like:
"Corn", 0.25, "NUT1", "PEST1", "PATH1", "SALT1", "HMET1", "CSC1", 0, 1, 1, 1, 1, 1
"Soybean", 0.30, "NUT2", "PEST2", "PATH2", "SALT2", "HMET2", "CSC2", 0, 1, 1, 1, 1, 1
```

## Read Pattern

```fortran
open (107,file=in_init%soil_plant_ini)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) sol_plt_ini(ii)%name, sol_plt_ini(ii)%sw_frac, sol_plt_ini(ii)%nutc, sol_plt_ini(ii)%pestc, sol_plt_ini(ii)%pathc, sol_plt_ini(ii)%saltc, sol_plt_ini(ii)%hmetc
read (107,*,iostat=eof) sol_plt_ini(ii)%name, sol_plt_ini(ii)%sw_frac, sol_plt_ini(ii)%nutc, sol_plt_ini(ii)%pestc, sol_plt_ini(ii)%pathc, sol_plt_ini(ii)%saltc, sol_plt_ini(ii)%hmetc, sol_plt_ini(ii)%csc
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_init%soil_plant_ini)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) sol_plt_ini(ii)%name, sol_plt_ini(ii)%sw_frac, sol_plt_ini(ii)%nutc, sol_plt_ini(ii)%pestc, sol_plt_ini(ii)%pathc, sol_plt_ini(ii)%saltc, sol_plt_ini(ii)%hmetc` |
| Input | `read` | 107 | `read (107,*,iostat=eof) sol_plt_ini(ii)%name, sol_plt_ini(ii)%sw_frac, sol_plt_ini(ii)%nutc, sol_plt_ini(ii)%pestc, sol_plt_ini(ii)%pathc, sol_plt_ini(ii)%saltc, sol_plt_ini(ii)%hmetc, sol_plt_ini(ii)%csc` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:soil_plant_init] | open, read, rewind, close | Reads the `soil_plant.ini` file if it exists or is not set to "null", counts the number of records, allocates the `sol_plt_ini` array accordingly, then reads each record into `sol_plt_ini`. The reading includes conditional logic to read an extra field `csc` if `bsn_cc%nam1` is not zero. |

## Review Notes

- The file is optional and only read if it exists or is not set to "null" in the initialization input.
- The conditional reading of the `csc` field depends on the value of `bsn_cc%nam1` from `basin_module`.
- No explicit sample data was found in the source; the sample format is inferred from the read statements and type declarations.
- No direct usage of `constituent_mass_module` variables is evident in the reader, though it is imported.
