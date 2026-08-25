---
kind: io
source_symbols:
- cli_read_atmodep_cs
title: '`cs_atmo.cli`'
status: filled
source_hash: f90aa75107652769
version_label: SWAT+ 62.0.0
---

**Primary target:** `atmodep_cs(:)` (array of `type object_deposition_cs`)  
**Read by:** [sym:cli_read_atmodep_cs]

## Bottom Line

The file `cs_atmo.cli` provides wet and dry atmospheric deposition values for chemical constituents at multiple stations.

It is optional and only read if constituents are present in the simulation and the file exists.

The reader subroutine `cli_read_atmodep_cs` loads this file and populates the `atmodep_cs` array with deposition data.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides `atmodep_cont` which contains metadata such as the number of stations (`num_sta`), timestep type (`timestep`), and number of time steps (`num`) used to control reading and allocation. |
| [sym:input_file_module] | No explicit variables or types from this module are directly referenced in the reader. |
| [sym:climate_module] | Supplies the `atmodep_cs` array of type `object_deposition_cs` where the deposition data is stored, and the `cs_db` object which holds the number of constituents (`num_cs`). |
| [sym:time_module] | No explicit variables or types from this module are directly referenced in the reader. |
| [sym:maximum_data_module] | No explicit variables or types from this module are directly referenced in the reader. |
| [sym:constituent_mass_module] | No explicit variables or types from this module are directly referenced in the reader. |

## File Variables

The file `cs_atmo.cli` contains atmospheric deposition data for chemical constituents at multiple stations. Each station record includes wet and dry deposition values, which may be provided as average annual, monthly, or yearly time series depending on the configured timestep. The reader maps these data into the `atmodep_cs` array of `type object_deposition_cs`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `atmodep_cs%salt` | type (atmospheric_deposition_cs) |  | Represents atmospheric deposition data related to salt constituents, stored as wet and dry deposition values. |
| 3 |  | `atmodep_cs%cs` | type (atmospheric_deposition_cs) |  | Represents atmospheric deposition data for other chemical constituents, including wet and dry deposition values. |

## Sample

```text
Example for average annual timestep (aa):
  (skip 3 header lines)
  station_name
  rf (wet deposition concentration in mg/L) for each constituent
  dry (dry deposition mass in kg/ha) for each constituent

Example for monthly timestep (mo):
  station_name
  rfmo (wet deposition monthly values) array for each constituent
  drymo (dry deposition monthly values) array for each constituent

Example for yearly timestep (yr):
  station_name
  rfyr (wet deposition yearly values) array for each constituent
  dryyr (dry deposition yearly values) array for each constituent
```

## Read Pattern

```fortran
open(5050,file='cs_atmo.cli')
read(5050,*)
read(5050,*)
read(5050,*)
read(5050,*) station_name
read(5050,*) atmodep_cs(iadep)%cs(ics)%rf
read(5050,*) atmodep_cs(iadep)%cs(ics)%dry
read(5050,*) station_name
read(5050,*) (atmodep_cs(iadep)%cs(ics)%rfmo(imo),imo=1,atmodep_cont%num)
read(5050,*) (atmodep_cs(iadep)%cs(ics)%drymo(imo),imo=1,atmodep_cont%num)
read(5050,*) station_name
read(5050,*) (atmodep_cs(iadep)%cs(ics)%rfyr(iyr),iyr=1,atmodep_cont%num)
read(5050,*) (atmodep_cs(iadep)%cs(ics)%dryyr(iyr),iyr=1,atmodep_cont%num)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 5050 | `open(5050,file='cs_atmo.cli')` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*)` |
| Input | `read` | 5050 | `read(5050,*) station_name` |
| Input | `read` | 5050 | `read(5050,*) atmodep_cs(iadep)%cs(ics)%rf` |
| Input | `read` | 5050 | `read(5050,*) atmodep_cs(iadep)%cs(ics)%dry` |
| Input | `read` | 5050 | `read(5050,*) station_name` |
| Input | `read` | 5050 | `read(5050,*) (atmodep_cs(iadep)%cs(ics)%rfmo(imo),imo=1,atmodep_cont%num)` |
| Input | `read` | 5050 | `read(5050,*) (atmodep_cs(iadep)%cs(ics)%drymo(imo),imo=1,atmodep_cont%num)` |
| Input | `read` | 5050 | `read(5050,*) station_name` |
| Input | `read` | 5050 | `read(5050,*) (atmodep_cs(iadep)%cs(ics)%rfyr(iyr),iyr=1,atmodep_cont%num)` |
| Input | `read` | 5050 | `read(5050,*) (atmodep_cs(iadep)%cs(ics)%dryyr(iyr),iyr=1,atmodep_cont%num)` |
| File control | `close` | 5050 | `close(5050)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cli_read_atmodep_cs] | close, open, read | Reads the `cs_atmo.cli` file if it exists and if chemical constituents are present in the simulation. It opens the file, skips header lines, allocates the `atmodep_cs` array for stations, and for each station reads wet and dry deposition data for each constituent. The deposition data can be average annual, monthly, or yearly depending on the configured timestep in `atmodep_cont`. The data are stored in the `atmodep_cs` array of `type object_deposition_cs`. |

## Review Notes

- Draft input-file overlay generated from static source facts; all fields filled based on source code evidence.
- The file is optional and only read if constituents exist and the file is present.
- The station name is read repeatedly but not stored in this routine; presumably handled elsewhere.
- No explicit parsing of station names or validation beyond reading is performed here.
