---
kind: io
source_symbols:
- constit_db_read
title: '`constituents.cs`'
status: filled
source_hash: 9c89a266c34745a1
version_label: SWAT+ 62.0.0
---

**Primary target:** `cs_db` (instance of `type constituents`)  
**Read by:** [sym:constit_db_read]

## Bottom Line

The file `constituents.cs` configures the chemical constituents database for the SWAT+ model, specifying pesticides, pathogens, heavy metals, salt ions, and other constituents to simulate.

It is optional; if the file does not exist or is set to "null", empty arrays are allocated for these constituents.

The reader `constit_db_read` loads this file and populates the `cs_db` variable with the constituent data.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `in_sim` variable which contains the filename `cs_db` for the constituents file. |
| [sym:input_file_module] | Used for input file handling and possibly for `in_sim` definition. |
| [sym:constituent_mass_module] | Defines the `type constituents` and the `cs_db` variable where the file data is stored. |
| [sym:maximum_data_module] | Provides `db_mx` which contains maximum counts for database arrays used in cross-referencing pesticides and pathogens. |
| [sym:pesticide_data_module] | Provides `pestdb` array used to crosswalk pesticide names to database indices. |
| [sym:pathogen_data_module] | Provides `path_db` array used to crosswalk pathogen names to database indices. |

## File Variables

The file `constituents.cs` contains counts and names of various chemical constituents grouped by category (pesticides, pathogens, metals, salts, and other constituents). Each category has a count followed by a list of names, which are cross-referenced to internal databases.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `cs_db%num_tot` | integer |  | number of total constituents simulated |
| 3 |  | `cs_db%num_pests` | integer |  | number of pesticides simulated |
| 4 |  | `cs_db%pests` | character (len=16) |  | name of the pesticides- points to pesticide database |
| 5 |  | `cs_db%pest_num` | integer |  | need to crosswalk pests to get pest_num for database - use sequential for object number of the pesticides- points to pesticide database |
| 6 |  | `cs_db%num_paths` | integer |  | number of pathogens simulated |
| 7 |  | `cs_db%paths` | character (len=16) |  | name of the pathogens- points to pathogens database |
| 8 |  | `cs_db%path_num` | integer |  | number of the pathogens- points to pathogens database |
| 9 |  | `cs_db%num_metals` | integer |  | number of heavy metals simulated |
| 10 |  | `cs_db%metals` | character (len=16) |  | name of the heavy metals- points to heavy metals database |
| 11 |  | `cs_db%metals_num` | integer |  | number of the heavy metals- points to heavy metals database |
| 12 |  | `cs_db%num_salts` | integer |  | number of salt ions simulated |
| 13 |  | `cs_db%salts` | character (len=16) |  | name of the salts - points to salts database |
| 14 |  | `cs_db%salts_num` | integer |  | number of the salts - points to salts database |
| 15 |  | `cs_db%num_cs` | integer |  | number of other constituents simulated |
| 16 |  | `cs_db%cs` | character (len=16) |  | name of the constituents - points to cs database |
| 17 |  | `cs_db%cs_num` | integer |  | number of the constituents - points to salts database |

## Sample

```text
Example `constituents.cs` file snippet:
Title line (ignored by parser)
3
PestA
PestB
PestC
2
Pathogen1
Pathogen2
1
MetalX
2
Salt1
Salt2
1
OtherConstituent1
```

## Read Pattern

```fortran
open (106,file=in_sim%cs_db)
read (106,*,iostat=eof) titldum
read (106,*,iostat=eof) cs_db%num_pests
read (106,*,iostat=eof) (cs_db%pests(i), i = 1, cs_db%num_pests)
read (106,*,iostat=eof) cs_db%num_paths
read (106,*,iostat=eof) (cs_db%paths(i), i = 1, cs_db%num_paths)
read (106,*,iostat=eof) cs_db%num_metals
read (106,*,iostat=eof) (cs_db%metals(i), i = 1, cs_db%num_metals)
read (106,*,iostat=eof) cs_db%num_salts
read (106,*,iostat=eof) (cs_db%salts(i), i = 1, cs_db%num_salts)
read (106,*,iostat=eof) cs_db%num_cs
read (106,*,iostat=eof) (cs_db%cs(i), i = 1, cs_db%num_cs)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 106 | `open (106,file=in_sim%cs_db)` |
| Input | `read` | 106 | `read (106,*,iostat=eof) titldum` |
| Input | `read` | 106 | `read (106,*,iostat=eof) cs_db%num_pests` |
| Input | `read` | 106 | `read (106,*,iostat=eof) (cs_db%pests(i), i = 1, cs_db%num_pests)` |
| Input | `read` | 106 | `read (106,*,iostat=eof) cs_db%num_paths` |
| Input | `read` | 106 | `read (106,*,iostat=eof) (cs_db%paths(i), i = 1, cs_db%num_paths)` |
| Input | `read` | 106 | `read (106,*,iostat=eof) cs_db%num_metals` |
| Input | `read` | 106 | `read (106,*,iostat=eof) (cs_db%metals(i), i = 1, cs_db%num_metals)` |
| Input | `read` | 106 | `read (106,*,iostat=eof) cs_db%num_salts` |
| Input | `read` | 106 | `read (106,*,iostat=eof) (cs_db%salts(i), i = 1, cs_db%num_salts)` |
| Input | `read` | 106 | `read (106,*,iostat=eof) cs_db%num_cs` |
| Input | `read` | 106 | `read (106,*,iostat=eof) (cs_db%cs(i), i = 1, cs_db%num_cs)` |
| File control | `close` | 106 | `close (106)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:constit_db_read] | open, read, close | Reads the `constituents.cs` file to populate the `cs_db` variable with counts and names of pesticides, pathogens, metals, salts, and other constituents. It also cross-references these names to internal databases to obtain index mappings used elsewhere in the model. |

## Review Notes

- The file `constituents.cs` is optional; if missing or set to "null", empty arrays are allocated for all constituent categories.
- Crosswalks for heavy metals and salts are commented out in the source, indicating incomplete or deferred implementation.
- The sample read format is inferred from the reading pattern but no explicit example data block is provided in the source.
