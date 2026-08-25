---
kind: io
source_symbols:
- aqu_read_init_cs
title: '`initial.aqu_cs`'
status: filled
source_hash: 306f311e7549659e
version_label: SWAT+ 62.0.0
---

**Primary target:** `aqu_init_dat_c_cs(:)` (array of `type aquifer_init_data_char_cs`)  
**Read by:** [sym:aqu_read_init_cs]

## Bottom Line

The file `initial.aqu_cs` configures initial conditions for aquifer chemical species including pesticides, pathogens, heavy metals, salts, and other constituents.

It is optional and only read if present.

The reader `aqu_read_init_cs` loads this file and populates the array `aqu_init_dat_c_cs` of type `aquifer_init_data_char_cs`.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides `sp_ob` and `sp_ob1` objects used to loop over aquifers and access aquifer counts and indices. |
| [sym:input_file_module] | No explicit variables used directly from this module in the reader. |
| [sym:maximum_data_module] | Provides `db_mx` which contains maximum counts for pesticide, pathogen, salt, and constituent initializations. |
| [sym:aquifer_module] | Provides the derived type `aquifer_init_data_char_cs` and the array `aqu_init_dat_c_cs` where file data is stored; also provides `aqudb` for aquifer database lookup and `aqu_d` for aquifer storage. |
| [sym:aqu_pesticide_module] | Provides pesticide initial data arrays such as `pest_init_name` and `pest_water_ini` used to initialize pesticide concentrations. |
| [sym:hydrograph_module] | Provides `ob` array representing objects including aquifers, used for area and property lookups. |
| [sym:constituent_mass_module] | Provides `cs_db` with counts of pesticides, pathogens, salts, and constituents; also provides initial data arrays like `path_init_name`, `path_soil_ini`, `salt_aqu_ini`, and `cs_aqu_ini` used to initialize chemical species in aquifers. |

## File Variables

The file `initial.aqu_cs` contains records of initial aquifer chemical species data, each record mapping to an element of the array `aqu_init_dat_c_cs` of type `aquifer_init_data_char_cs`. Each record includes names of initial input files for pesticides, pathogens, heavy metals, salts, and other constituents associated with each aquifer.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `aqu_init_dat_c_cs%name` | character (len=16) |  | xwalk with aqudb(iaqu)%aqu_ini |
| 3 |  | `aqu_init_dat_c_cs%pest` | character (len=16) |  | points to initial pesticide input file |
| 4 |  | `aqu_init_dat_c_cs%path` | character (len=16) |  | points to initial pathogen input file |
| 5 |  | `aqu_init_dat_c_cs%hmet` | character (len=16) |  | points to initial heavy metals input file |
| 6 |  | `aqu_init_dat_c_cs%salt` | character (len=16) |  | points to initial salt input file (salt_aqu.ini) |
| 7 |  | `aqu_init_dat_c_cs%cs` | character (len=16) |  | points to initial constituent input file (cs_aqu.ini) |

## Sample

```text
Example record block from initial.aqu_cs:
AquiferName1  PestFile1      PathFile1      HMetFile1      SaltFile1      CsFile1
AquiferName2  PestFile2      PathFile2      HMetFile2      SaltFile2      CsFile2
```

## Read Pattern

```fortran
open (105,file="initial.aqu_cs")
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
read (105,*,iostat=eof) aqu_init_dat_c_cs(iaqu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file="initial.aqu_cs")` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) aqu_init_dat_c_cs(iaqu)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:aqu_read_init_cs] | close, open, read, rewind | Reads the file `initial.aqu_cs` if it exists, counts the number of records, allocates the array `aqu_init_dat_c_cs`, and reads each record into this array. Then initializes aquifer chemical species concentrations (pesticides, pathogens, salts, constituents) in groundwater and benthic compartments by cross-referencing the read initial file names with corresponding initial data arrays and aquifer properties. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only processed if present, as indicated by the inquire statement.
- The reader initializes multiple aquifer chemical species arrays after reading the file, linking input file names to initial data arrays.
- No sample data block was found in the source; the sample_read_format is a constructed example based on the file variables.
