---
kind: io
source_symbols:
- cli_read_atmodep_salt
title: '`salt_atmo.cli`'
status: filled
source_hash: a7f8146c85b2244f
version_label: SWAT+ 62.0.0
---

**Primary target:** `atmodep_salt(:)` (array of `type object_deposition_cs`)  
**Read by:** [sym:cli_read_atmodep_salt]

## Bottom Line

The file `salt_atmo.cli` provides wet and dry atmospheric deposition values for salt ions at multiple stations.

It is only read if salt ions are included in the simulation (`cs_db%num_salts > 0`).

The file is optional and is read by the `cli_read_atmodep_salt` subroutine.

It configures the model state variable `atmodep_salt`, which stores deposition data by station and salt ion.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the container `atmodep_cont` which holds metadata such as the number of stations (`num_sta`), the timestep type (`timestep`), and the number of time periods (`num`). |
| [sym:input_file_module] | Used for general input file handling but no specific variables are referenced in this routine. |
| [sym:climate_module] | Defines the main data structures `atmodep_salt` (array of `object_deposition_cs`) and `cs_db` which holds the number of salt ions (`num_salts`). |
| [sym:time_module] | No specific variables used directly in this routine but likely related to time indexing. |
| [sym:maximum_data_module] | No specific variables used directly in this routine. |
| [sym:constituent_mass_module] | Provides `cs_db` which contains the number of salt ions (`num_salts`) to read and allocate. |

## File Variables

The `salt_atmo.cli` file contains atmospheric deposition data for salt ions at multiple stations. The data is organized by station and salt ion, with values provided for wet (rainfall) and dry deposition. The file format supports annual, monthly, or yearly time steps, and the data is read into the `atmodep_salt` array of `object_deposition_cs` types.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `atmodep_salt%salt` | type (atmospheric_deposition_cs) |  | Holds atmospheric deposition data for salt ions, including wet and dry deposition values, possibly time-resolved by month or year. |
| 3 |  | `atmodep_salt%cs` | type (atmospheric_deposition_cs) |  | Not directly assigned in this routine; likely related to constituent salt data but unused here. |

## Sample

```text
Example record block for annual timestep (timestep = "aa"):
StationName
NaCl 0.1
MgCl2 0.05
NaCl 0.02
MgCl2 0.01

Example record block for monthly timestep (timestep = "mo"):
StationName
NaCl 0.01 0.02 0.03 ... (num months)
MgCl2 0.005 0.006 0.007 ... (num months)
NaCl 0.002 0.003 0.004 ... (num months)
MgCl2 0.001 0.0015 0.002 ... (num months)

Example record block for yearly timestep (timestep = "yr"):
StationName
NaCl 0.1 0.11 0.12 ... (num years)
MgCl2 0.05 0.051 0.052 ... (num years)
NaCl 0.02 0.021 0.022 ... (num years)
MgCl2 0.01 0.011 0.012 ... (num years)
```

## Read Pattern

```fortran
open(5050,file='salt_atmo.cli')
read(5050,*)
read(5050,*)
read(5050,*)
read(5050,*)
read(5050,*)
read(5050,*)
read(5050,*) station_name
read(5050,*) salt_ion,atmodep_salt(iadep)%salt(isalt)%rf
read(5050,*) salt_ion,atmodep_salt(iadep)%salt(isalt)%dry
read(5050,*) station_name
read(5050,*) salt_ion,(atmodep_salt(iadep)%salt(isalt)%rfmo(imo),imo=1,atmodep_cont%num)
read(5050,*) salt_ion,(atmodep_salt(iadep)%salt(isalt)%drymo(imo),imo=1,atmodep_cont%num)
read(5050,*) station_name
read(5050,*) salt_ion,(atmodep_salt(iadep)%salt(isalt)%rfyr(iyr),iyr=1,atmodep_cont%num)
read(5050,*) salt_ion,(atmodep_salt(iadep)%salt(isalt)%dryyr(iyr),iyr=1,atmodep_cont%num)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 5050 | `open(5050,file='salt_atmo.cli')` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*) station_name` |
| Input | `read` | 5050 | `read(5050,*) salt_ion,atmodep_salt(iadep)%salt(isalt)%rf` |
| Input | `read` | 5050 | `read(5050,*) salt_ion,atmodep_salt(iadep)%salt(isalt)%dry` |
| Input | `read` | 5050 | `read(5050,*) station_name` |
| Input | `read` | 5050 | `read(5050,*) salt_ion,(atmodep_salt(iadep)%salt(isalt)%rfmo(imo),imo=1,atmodep_cont%num)` |
| Input | `read` | 5050 | `read(5050,*) salt_ion,(atmodep_salt(iadep)%salt(isalt)%drymo(imo),imo=1,atmodep_cont%num)` |
| Input | `read` | 5050 | `read(5050,*) station_name` |
| Input | `read` | 5050 | `read(5050,*) salt_ion,(atmodep_salt(iadep)%salt(isalt)%rfyr(iyr),iyr=1,atmodep_cont%num)` |
| Input | `read` | 5050 | `read(5050,*) salt_ion,(atmodep_salt(iadep)%salt(isalt)%dryyr(iyr),iyr=1,atmodep_cont%num)` |
| File control | `close` | 5050 | `close(5050)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_read_atmodep_salt] | close, open, read | Reads the `salt_atmo.cli` file if salt ions are present in the simulation. It reads wet and dry deposition values for each salt ion at each station, supporting annual, monthly, or yearly time steps. The data is stored in the `atmodep_salt` array of `object_deposition_cs` types, allocating arrays as needed based on the timestep. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The `atmodep_salt%cs` field is declared but not assigned or used in this reader; its purpose is uncertain from the current source.
- The file is optional and only read if salt ions are present (`cs_db%num_salts > 0`).
- The reader skips the first six lines of the file, which are assumed to be commentary or headers.
