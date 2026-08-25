---
kind: io
source_symbols:
- readpcom
title: '`plant.ini`'
status: filled
source_hash: 94e885fe9563d74d
version_label: SWAT+ 62.0.0
---

**Primary target:** `pcomdb(:)` (array of `type plant_community_db`)  
**Read by:** [sym:readpcom]

## Bottom Line

The file `plant.ini` configures plant community definitions for the SWAT+ model, specifying plant community names, the number of plants per community, rotation start years, and detailed plant initialization parameters.

It is optional; if the file does not exist or is set to "null", the model allocates empty plant community data structures.

The primary reader for this file is the `readpcom` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_init` variable which contains the filename for the plant community input file (`in_init%plant`). |
| [sym:maximum_data_module] | Provides the `db_mx` variable which stores maximum counts such as `db_mx%plantcom` (number of plant communities) and `db_mx%plantparm` (number of plant parameters). |
| [sym:plant_data_module] | Defines the `pcomdb` array of type `plant_community_db` where the plant community data is stored, and the `pldb` array of plant parameter records used to match plant names. |

## File Variables

The `plant.ini` file contains multiple plant community records. Each record includes a community name, the number of plants in the community, the initial rotation year, and a list of plants with their initialization parameters. These map to the `pcomdb` array of `type plant_community_db`, where each community holds an array of `pl` entries of type `plant_init_db`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 | `Community name` | `pcomdb%name` | character(len=40) |  | The name identifier for the plant community. |
| 3 | `Number of plants` | `pcomdb%plants_com` | integer |  | The number of individual plants defined within this plant community. |
| 4 | `Rotation start year` | `pcomdb%rot_yr_ini` | integer |  | The initial year for crop rotation within the plant community. |
| 5 | `Plant initialization parameters` | `pcomdb%pl` | type (plant_init_db) |  | Array of plant initialization data for each plant in the community, including species code, growth parameters, leaf area index, biomass, and other physiological parameters. |

## Sample

```text
Example snippet from `plant.ini` (format inferred from read statements):
Line 1: Title line (ignored by model)
Line 2: Header line (ignored by model)
Line 3+: For each plant community:
  Community name (character), number of plants (integer)
  For each plant in the community:
    Plant name (character)
After rewind:
  For each plant community:
    Community name (character), number of plants (integer), rotation start year (integer)
    For each plant:
      Species code (character), growth index (integer), leaf area index (real), biomass (real), photosynthetic capacity (real), population (real), fruit year maturity (integer), residue index (real)
```

## Read Pattern

```fortran
open (113,file=in_init%plant)
read (113,*,iostat=eof) titldum
read (113,*,iostat=eof) header
read (113,*,iostat=eof) name, numb
read (113,*,iostat=eof) name
rewind (113)
read (113,*,iostat=eof)  pcomdb(icom)%name, pcomdb(icom)%plants_com, pcomdb(icom)%rot_yr_ini
read (113,*,iostat=eof) pcomdb(icom)%pl(iplt)%cpnm, pcomdb(icom)%pl(iplt)%igro, pcomdb(icom)%pl(iplt)%lai, pcomdb(icom)%pl(iplt)%bioms, pcomdb(icom)%pl(iplt)%phuacc, pcomdb(icom)%pl(iplt)%pop, pcomdb(icom)%pl(iplt)%fr_yrmat, pcomdb(icom)%pl(iplt)%rsdin
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 113 | `open (113,file=in_init%plant)` |
| Input | `read` | 113 | `read (113,*,iostat=eof) titldum` |
| Input | `read` | 113 | `read (113,*,iostat=eof) header` |
| Input | `read` | 113 | `read (113,*,iostat=eof) name, numb` |
| Input | `read` | 113 | `read (113,*,iostat=eof) name` |
| File control | `rewind` | 113 | `rewind (113)` |
| Input | `read` | 113 | `read (113,*,iostat=eof) titldum` |
| Input | `read` | 113 | `read (113,*,iostat=eof) header` |
| Input | `read` | 113 | `read (113,*,iostat=eof)  pcomdb(icom)%name, pcomdb(icom)%plants_com, pcomdb(icom)%rot_yr_ini` |
| Input | `read` | 113 | `read (113,*,iostat=eof) pcomdb(icom)%pl(iplt)%cpnm, pcomdb(icom)%pl(iplt)%igro, pcomdb(icom)%pl(iplt)%lai, pcomdb(icom)%pl(iplt)%bioms, pcomdb(icom)%pl(iplt)%phuacc, pcomdb(icom)%pl(iplt)%pop, pcomdb(icom)%pl(iplt)%fr_yrmat, pcomdb(icom)%pl(iplt)%rsdin` |
| File control | `close` | 113 | `close (113)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:readpcom] | close, open, read, rewind | Reads the plant community definitions from `plant.ini`, populating the `pcomdb` array with community and plant initialization data. Handles the case where the file is missing or set to "null" by allocating empty data structures. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The `plant.ini` file is optional; if missing or set to "null", no plant communities are loaded and empty arrays are allocated.
- The file format includes a header and title line, followed by multiple plant community blocks each with a name, number of plants, and plant details.
- The reader matches plant names in the file to a plant parameter database (`pldb`) to assign indices.
- No sample data block was found in the source; the sample read format is inferred from the read statements.
