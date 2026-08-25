---
kind: io
source_symbols:
- exco_read_pest
title: '`exco_pest.exc`'
status: filled
source_hash: 99a9f96bdd2f1df8
version_label: SWAT+ 62.0.0
---

**Primary target:** exco_pest(:)  
**Read by:** [sym:exco_read_pest]

## Bottom Line

The file exco_pest.exc contains pesticide export coefficient data used to configure pesticide export coefficients in the SWAT+ model.

It is optional and only read if the file exists and is not set to "null".

The reader subroutine exco_read_pest loads this file and populates the exco_pest derived type array.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the sp_ob1, sp_ob, and ob arrays used to assign pesticide export coefficients to hydrograph objects. |
| [sym:input_file_module] | Provides the in_exco object which contains the file path for the pesticide export coefficient file (in_exco%pest). |
| [sym:organic_mineral_mass_module] | No direct variables used from this module in this reader. |
| [sym:constituent_mass_module] | No direct variables used from this module in this reader. |
| [sym:exco_module] | Provides the exco_pest derived type array and related variables (exco_pest_name, exco_pest_num) to store pesticide export coefficient data. |
| [sym:maximum_data_module] | Provides db_mx which stores maximum counts including db_mx%exco_pest for the number of pesticide export coefficients. |

## File Variables

The file exco_pest.exc consists of a header block followed by multiple records each containing a pesticide export coefficient name and a list of pesticide export coefficient values corresponding to the number of pesticides defined in the model. The reader maps each record into the exco_pest derived type array, storing the pesticide export coefficients for each pesticide.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Title line` | `titldum` |  |  | Reads a title or descriptive line from the file, used for informational or header purposes but not stored persistently. |
| 1 | `Header line` | `header` |  |  | Reads a header line from the file, used for informational or header purposes but not stored persistently. |
| N/A | `Pesticide export coefficient name` | `exco_pest_name(ii)` |  |  | Stores the name of the pesticide export coefficient set read from the file for record ii. |
| N/A | `Pesticide export coefficients` | `(exco_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)` |  |  | Stores the array of pesticide export coefficient values for each pesticide in the model, read from the file for record ii. |

## Sample

```text
Example lines from exco_pest.exc:
Title line describing the file
Header line with column descriptions
PestName1 0.1 0.2 0.3 0.4
PestName2 0.05 0.15 0.25 0.35
```

## Read Pattern

```fortran
open (107,file=in_exco%pest)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) exco_pest_name(ii), (exco_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_exco%pest)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) exco_pest_name(ii), (exco_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:exco_read_pest] | backspace, close, open, read, rewind | Reads the pesticide export coefficient file exco_pest.exc if it exists and is not set to "null". It counts the number of pesticide export coefficient records, allocates storage arrays, reads the pesticide export coefficient names and values, and cross-references them with the main export coefficient database. Finally, it assigns the pesticide export coefficients to hydrograph objects for use in the model. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and read only if it exists and is not "null".
- The reader uses multiple reads and file control statements (rewind, backspace) to count records and then read data.
- The pesticide export coefficients are stored in the exco_pest derived type array and linked to hydrograph objects via sp_ob1 and sp_ob arrays.
- No explicit file format example was found in the source; the sample read format is inferred from the read statements.
