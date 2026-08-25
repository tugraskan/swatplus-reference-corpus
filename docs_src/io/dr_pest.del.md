---
kind: io
source_symbols:
- dr_read_pest
title: '`dr_pest.del`'
status: filled
source_hash: 3a955b8ee39943e9
version_label: SWAT+ 62.0.0
---

**Primary target:** dr_pest(:)  
**Read by:** [sym:dr_read_pest]

## Bottom Line

The file dr_pest.del contains delivery ratio data for pesticides, configuring the pesticide delivery ratios used in the model's hydrological routing.

It is optional and only read if the file exists and is not set to 'null'.

The reader subroutine dr_read_pest loads this file and populates the dr_pest derived type array.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the sp_ob1 and sp_ob objects and the ob and obcs arrays used to assign pesticide delivery ratios to hydrograph objects. |
| [sym:dr_module] | Supplies the dr_pest derived type array and related variables dr_pest_name, dr_pest_num, and dr_db used to store and crosswalk pesticide delivery ratio data. |
| [sym:input_file_module] | Provides the in_delr object which contains the file path for the pesticide delivery ratio input file. |
| [sym:organic_mineral_mass_module] |  |
| [sym:constituent_mass_module] |  |
| [sym:maximum_data_module] | Provides the db_mx object which stores the maximum counts including db_mx%dr_pest used to size the dr_pest array. |

## File Variables

The dr_pest.del file is read as a text file with multiple header lines followed by records containing a pesticide delivery ratio name and an array of pesticide delivery ratio values for each pesticide in the database. The reader maps these records into the dr_pest derived type array and associated name and index arrays.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Title line` | `titldum` |  |  | Reads a title or descriptive line from the file, used to skip or identify the file section. |
| 1 | `Header line` | `header` |  |  | Reads a header line following the title, used to skip or identify the file section. |
| N/A | `Pesticide delivery ratio name` | `dr_pest_name(ii)` |  |  | Reads the name of the pesticide delivery ratio set for the current record. |
| N/A | `Pesticide delivery ratio values` | `(dr_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)` |  |  | Reads an array of pesticide delivery ratio values for each pesticide in the database, storing them in the dr_pest derived type. |

## Sample

```text
Example dr_pest.del file snippet:
Line 1: Title or comment line (ignored)
Line 2: Header line (ignored)
Line 3+: Each record consists of a pesticide delivery ratio name followed by a list of pesticide delivery ratio values, e.g.:
PestSet1 0.1 0.2 0.3 0.4 0.5
PestSet2 0.05 0.15 0.25 0.35 0.45
```

## Read Pattern

```fortran
open (107,file=in_delr%pest)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) dr_pest_name(ii), (dr_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_delr%pest)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dr_pest_name(ii), (dr_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dr_read_pest] | backspace, close, open, read, rewind | Reads the pesticide delivery ratio file dr_pest.del if it exists and is not 'null'. It counts the number of pesticide delivery ratio sets, allocates arrays accordingly, reads the names and pesticide delivery ratio values into the dr_pest derived type array, crosswalks these names with the dr database, and assigns the pesticide delivery ratios to the hydrograph objects for routing. |

## Review Notes

- Draft input-file overlay generated from static source facts; the pesticide delivery ratio file is optional and only read if it exists and is not 'null'.
- The reader counts records by reading lines until EOF, then rewinds and reads the actual data.
- The pesticide delivery ratio values are stored per pesticide for each delivery ratio set.
- Crosswalk with dr_db is done by matching dr_pest_name strings to dr_db(idr)%pest_file.
- The pesticide delivery ratios are assigned to hydrograph objects' pest arrays for routing.
- No explicit units or formats are stated in source; assumed free-format text with whitespace separation.
