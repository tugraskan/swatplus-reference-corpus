---
kind: io
source_symbols:
- path_hru_aqu_read
title: '`path_hru.ini`'
status: filled
source_hash: 14f292eab168c664
version_label: SWAT+ 62.0.0
---

**Primary target:** `path_soil_ini(:)` (array of `type cs_soil_init_concentrations`)  
**Read by:** [sym:path_hru_aqu_read]

## Bottom Line

The `path_hru.ini` input file configures initial concentrations of constituents in soil and on plants at the start of the simulation.

It is optional and only read if the file exists and is not set to "null".

The reader subroutine `path_hru_aqu_read` loads this file and stores its data into the `path_soil_ini` array.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_soil_init_concentrations` which defines the structure of each record in `path_soil_ini`. |
| [sym:input_file_module] | Supplies the `in_init` variable which contains the file path `in_init%path_soil` used to open `path_hru.ini`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable used to store the count of records read (`db_mx%path_ini`). |

## File Variables

Each record in `path_hru.ini` corresponds to an element of the `path_soil_ini` array of type `cs_soil_init_concentrations`. The file contains constituent names and their initial concentrations in soil and on plants.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `path_soil_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `path_soil_ini%soil` | real | ppm | amount of constituent in soil at start of simulation |
| 4 |  | `path_soil_ini%plt` | real | ppm or #cfu/m^2 | amount of constituent on plant at start of simulation |

## Sample

```text
Example record block from `path_hru.ini` (format inferred from reader):
ConstituentName
 0.0  0.0
Where the first line is the constituent name (character string up to 16 chars),
and the second line contains two real numbers: soil concentration (ppm) and plant concentration (ppm or #cfu/m^2).
```

## Read Pattern

```fortran
open (107,file=in_init%path_soil)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) path_soil_ini(ipathi)%name
read (107,*,iostat=eof) titldum, path_soil_ini(ipathi)%soil, path_soil_ini(ipathi)%plt
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_init%path_soil)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) path_soil_ini(ipathi)%name` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum, path_soil_ini(ipathi)%soil, path_soil_ini(ipathi)%plt` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:path_hru_aqu_read] | open, read, rewind, close | Reads the `path_hru.ini` file if it exists and is not "null", counts the number of constituent records, allocates arrays accordingly, and loads initial constituent concentrations in soil and on plants into the `path_soil_ini` array. |

## Review Notes

- The file is optional and only processed if it exists and is not set to "null" in `in_init%path_soil`.
- The reader counts records by scanning the file once, then rewinds and reads data into allocated arrays.
- The `titldum` and `header` variables are used to read and discard non-data lines such as titles or headers.
- The exact format of the file beyond the constituent name and two concentration values per record is not fully documented in the source.
- No explicit error handling beyond EOF checks is implemented.
