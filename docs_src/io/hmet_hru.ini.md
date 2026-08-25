---
kind: io
source_symbols:
- hmet_hru_aqu_read
title: '`hmet_hru.ini`'
status: filled
source_hash: 90294d93062d783f
version_label: SWAT+ 62.0.0
---

**Primary target:** `hmet_soil_ini(:)` (array of `type cs_soil_init_concentrations`)  
**Read by:** [sym:hmet_hru_aqu_read]

## Bottom Line

The `hmet_hru.ini` file configures initial concentrations of heavy metals in soil and on plants for each constituent at the start of the simulation.

It is optional and only read if the file exists and is not set to "null" in the initialization structure.

The primary reader for this file is the `hmet_hru_aqu_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_soil_init_concentrations` which defines the structure of each record read from the file, including constituent name and initial soil and plant concentrations. |
| [sym:input_file_module] | Supplies the `in_init` structure which contains the filename `hmet_soil` pointing to `hmet_hru.ini`. |
| [sym:maximum_data_module] | Provides the `db_mx` structure where the number of heavy metal initializations (`hmet_ini`) is stored. |

## File Variables

The file contains records of initial heavy metal concentrations for each constituent, with each record mapped to an element of the `hmet_soil_ini` array of type `cs_soil_init_concentrations`. Each record includes a constituent name, and arrays of soil and plant concentrations for all metals.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `hmet_soil_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `hmet_soil_ini%soil` | real | ppm | amount of constituent in soil at start of simulation |
| 4 |  | `hmet_soil_ini%plt` | real | ppm or #cfu/m^2 | amount of constituent on plant at start of simulation |

## Sample

```text
Example record block from `hmet_hru.ini` (format inferred from reader):
ConstituentName
Label SoilConcentration
Label PlantConcentration
For each metal:
  <string> <soil concentration in ppm>
  <string> <plant concentration in ppm or #cfu/m^2>
```

## Read Pattern

```fortran
open (107,file=in_init%hmet_soil)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) hmet_soil_ini(ihmeti)%name
read (107,*,iostat=eof) titldum, hmet_soil_ini(ihmeti)%soil(ihmet)
read (107,*,iostat=eof) titldum, hmet_soil_ini(ihmeti)%plt(ihmet)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_init%hmet_soil)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) hmet_soil_ini(ihmeti)%name` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum, hmet_soil_ini(ihmeti)%soil(ihmet)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum, hmet_soil_ini(ihmeti)%plt(ihmet)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:hmet_hru_aqu_read] | open, read, rewind, close | Reads the `hmet_hru.ini` file if it exists and is not set to "null". It first counts the number of constituent records, allocates the `hmet_soil_ini` array accordingly, then rewinds and reads each constituent's name and associated initial soil and plant heavy metal concentrations into the `hmet_soil_ini` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists and is not set to "null" in the initialization structure.
- The exact format of the file is inferred from the reader's read statements; no example data block was found in the source.
