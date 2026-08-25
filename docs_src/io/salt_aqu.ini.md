---
kind: io
source_symbols:
- salt_aqu_read
title: '`salt_aqu.ini`'
status: filled
source_hash: 3b65cf4931834eed
version_label: SWAT+ 62.0.0
---

**Primary target:** `salt_aqu_ini(:)` (array of `type salt_aqu_init_concentrations`)  
**Read by:** [sym:salt_aqu_read]

## Bottom Line

The file `salt_aqu.ini` configures initial salt ion concentrations and mineral fractions in aquifers for the SWAT+ model.

It is optional and only read if the file exists and is not named "null".

The reader subroutine `salt_aqu_read` loads this file and populates the array `salt_aqu_ini` with these initial conditions.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `salt_aqu_init_concentrations` which defines the structure of each salt constituent record, including fields `name`, `conc`, and `frac`. |
| [sym:input_file_module] | Used for general input file handling utilities and possibly global input file state (not explicitly detailed in this source). |
| [sym:maximum_data_module] | Provides the global variable `db_mx` where `db_mx%salt_gw_ini` stores the number of salt constituents read from the file. |

## File Variables

The file `salt_aqu.ini` consists of multiple records, each representing a salt constituent with its name, initial concentration, and mineral fraction. These records are read sequentially into an array of `type salt_aqu_init_concentrations` named `salt_aqu_ini`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `salt_aqu_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `salt_aqu_ini%conc` | real | g/m3 | salt ion concentration at start of simulation |
| 4 |  | `salt_aqu_ini%frac` | real | fractions | salt mineral fractions at start of simulation |

## Sample

```text
Example record line format (space or comma separated):
"NaCl"  35.0  0.2
"CaSO4" 10.5  0.1
```

## Read Pattern

```fortran
open (107,file="salt_aqu.ini")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) titldum
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) salt_aqu_ini(isalt)%name,salt_aqu_ini(isalt)%conc,salt_aqu_ini(isalt)%frac
close (107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="salt_aqu.ini")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) salt_aqu_ini(isalt)%name,salt_aqu_ini(isalt)%conc,salt_aqu_ini(isalt)%frac` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:salt_aqu_read] | open, read, rewind, close | Reads the file `salt_aqu.ini` if it exists and is not "null", counts the number of salt constituent records, allocates the `salt_aqu_ini` array accordingly, and then reads each constituent's name, initial concentration, and mineral fraction into the array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists and is not named "null".
- The reader first counts records by reading through the file, then rewinds and reads the data into allocated arrays.
- The `salt_aqu_ini` array elements allocate internal arrays for concentrations and fractions based on other module data (`cs_db%num_salts`), but the detailed structure of these internal arrays is outside this file's scope.
