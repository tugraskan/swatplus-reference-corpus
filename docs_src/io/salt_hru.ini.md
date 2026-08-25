---
kind: io
source_symbols:
- salt_hru_read
title: '`salt_hru.ini`'
status: filled
source_hash: 637dc63c33735aff
version_label: SWAT+ 62.0.0
---

**Primary target:** `salt_soil_ini(:)` (array of `type cs_soil_init_concentrations`)  
**Read by:** [sym:salt_hru_read]

## Bottom Line

The file `salt_hru.ini` provides initial concentrations of salt constituents in soil and on plants for the simulation.

It is optional and only read if the file exists.

The reader subroutine `salt_hru_read` loads this file and stores the data into the `salt_soil_ini` array.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_soil_init_concentrations` and the `salt_soil_ini` array where the file data are stored. |
| [sym:input_file_module] | Used for file input operations and possibly for input file handling conventions. |
| [sym:maximum_data_module] | Provides the global variable `db_mx` whose member `salt_ini` is set to the number of salt constituents read from the file. |

## File Variables

The file `salt_hru.ini` consists of multiple records, each describing initial salt constituent concentrations for soil and plants. Each record is read into an element of the `salt_soil_ini` array of type `cs_soil_init_concentrations`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `salt_soil_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `salt_soil_ini%soil` | real | ppm | amount of constituent in soil at start of simulation |
| 4 |  | `salt_soil_ini%plt` | real | ppm or #cfu/m^2 | amount of constituent on plant at start of simulation |

## Sample

```text
Example record block from `salt_hru.ini` (format inferred from reader):
ConstituentName
soil_concentration_value
plant_concentration_value
```

## Read Pattern

```fortran
open (107,file='salt_hru.ini')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) salt_soil_ini(isalti)%name
read (107,*,iostat=eof) salt_soil_ini(isalti)%soil
read (107,*,iostat=eof) salt_soil_ini(isalti)%plt
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='salt_hru.ini')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) salt_soil_ini(isalti)%name` |
| Input | `read` | 107 | `read (107,*,iostat=eof) salt_soil_ini(isalti)%soil` |
| Input | `read` | 107 | `read (107,*,iostat=eof) salt_soil_ini(isalti)%plt` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:salt_hru_read] | open, read, rewind, close | Reads the `salt_hru.ini` file if it exists, counts the number of salt constituent records, allocates the `salt_soil_ini` array accordingly, and loads initial salt concentrations for soil and plants into this array. |

## Review Notes

- The file `salt_hru.ini` is optional and only read if it exists.
- The reader first counts the number of records by reading through the file, then allocates arrays accordingly before reading the data again.
- The file format includes header lines that are skipped before reading the actual data records.
- The units for soil concentrations are ppm, and for plant concentrations are ppm or colony forming units per square meter (#cfu/m^2).
- No explicit sample data records were found in the source; the sample read format is inferred from the reader's read statements.
- The reader uses the global `db_mx%salt_ini` to store the number of salt constituents read.
