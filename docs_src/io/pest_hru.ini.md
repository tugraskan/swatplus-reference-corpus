---
kind: io
source_symbols:
- pest_hru_aqu_read
title: '`pest_hru.ini`'
status: filled
source_hash: 6a190fabcf434ccc
version_label: SWAT+ 62.0.0
---

**Primary target:** `pest_soil_ini(:)` (array of `type cs_soil_init_concentrations`)  
**Read by:** [sym:pest_hru_aqu_read]

## Bottom Line

The file `pest_hru.ini` provides initial concentrations of pesticide constituents in soil and on plants for the simulation.

It is optional and only read if the file exists and is not set to "null" in the input initialization structure.

The reader subroutine `pest_hru_aqu_read` loads this file and stores the data into the `pest_soil_ini` array.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_soil_init_concentrations` which defines the structure of each pesticide constituent's initial concentrations in soil and plants, and the global database `cs_db` with `num_pests` used for array dimensions. |
| [sym:input_file_module] | Provides the input initialization structure `in_init` which contains the filename `pest_soil` pointing to `pest_hru.ini`. |
| [sym:maximum_data_module] | Provides the global database `db_mx` where the maximum number of pesticide initial records `pest_ini` is stored. |

## File Variables

The file consists of multiple records, each describing initial pesticide constituent concentrations for a given constituent name. Each record contains a name field followed by soil and plant concentration values for each pesticide in the database.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pest_soil_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `pest_soil_ini%soil` | real | ppm | amount of constituent in soil at start of simulation |
| 4 |  | `pest_soil_ini%plt` | real | ppm or #cfu/m^2 | amount of constituent on plant at start of simulation |

## Sample

```text
Example record block from pest_hru.ini:
CONSTITUENT_NAME
soil_concentration_1 plant_concentration_1
soil_concentration_2 plant_concentration_2
...
soil_concentration_N plant_concentration_N
```

## Read Pattern

```fortran
open (107,file=in_init%pest_soil)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) pest_soil_ini(ipesti)%name
read (107,*,iostat=eof) titldum, pest_soil_ini(ipesti)%soil(ipest), pest_soil_ini(ipesti)%plt(ipest)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_init%pest_soil)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pest_soil_ini(ipesti)%name` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum, pest_soil_ini(ipesti)%soil(ipest), pest_soil_ini(ipesti)%plt(ipest)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:pest_hru_aqu_read] | open, read, rewind, close | Reads the `pest_hru.ini` file if it exists and is not "null", counts the number of pesticide initial records, allocates arrays accordingly, and loads initial pesticide constituent concentrations in soil and plants into the `pest_soil_ini` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists and is not set to "null" in the input initialization structure.
- The exact format of the file beyond the Fortran read pattern is inferred from the code but no example data lines were found in the source.
- The reader uses the global `cs_db%num_pests` to determine how many soil and plant concentration values to read per record.
