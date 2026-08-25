---
kind: io
source_symbols:
- dr_read_salt
title: '`dr_salt.del`'
status: filled
source_hash: 54d7a4ec9882dcc3
version_label: SWAT+ 62.0.0
---

**Primary target:** dr_salt(:)  
**Read by:** [sym:dr_read_salt]

## Bottom Line

The file dr_salt.del contains export coefficient data for salts used in delivery ratio calculations within the model.

It is optional, as the reader checks for file existence before reading.

The reader subroutine dr_read_salt loads this file and populates the dr_salt derived type array with salt export coefficients and their associated names.

It also crosswalks these salts with the drainage database and assigns salt coefficients to hydrograph objects' salt state variables.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the hydrograph object arrays sp_ob1, sp_ob, ob, and obcs, which are updated with salt export coefficients read from the file. |
| [sym:dr_module] | Supplies the dr_salt derived type array, dr_salt_num integer array, dr_salt_name character array, and dr_db drainage database used for cross-referencing salt names. |
| [sym:input_file_module] | Provides the in_delr derived type containing the salt file path in in_delr%salt. |
| [sym:organic_mineral_mass_module] | No direct usage in this reader; imported but no variables or types referenced. |
| [sym:constituent_mass_module] | No direct usage in this reader; imported but no variables or types referenced. |
| [sym:maximum_data_module] | Provides db_mx, which contains the maximum counts for dr_salt and dr used for allocation and looping. |

## File Variables

The dr_salt.del file contains lines of export coefficient data for salts. The file is read line-by-line to determine the number of salt records, then each record is read into the dr_salt derived type array, including the salt name and an array of salt export coefficients for each salt type defined in cs_db.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Title line` | `titldum` |  |  | The first read line is a title or descriptive string from the salt file, stored temporarily in titldum but not used further. |
| 1 | `Header line` | `header` |  |  | The second read line is a header string from the salt file, stored temporarily in header but not used further. |
| 1 | `Salt name` | `dr_salt_name(ii)` |  |  | The salt name string for the ith salt export coefficient record, read from the file and stored in dr_salt_name array. |
| 2.. | `Salt export coefficients` | `(dr_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)` |  |  | An array of salt export coefficients for each salt type defined in cs_db, read from the file and stored in the salt component of the dr_salt derived type for each record. |

## Sample

```text
Example lines from dr_salt.del might look like:
Title of Salt Export Coefficients
SaltName HeaderInfo
Salt1 0.1 0.2 0.3 0.4
Salt2 0.05 0.1 0.15 0.2
```

## Read Pattern

```fortran
open (107,file=in_delr%salt)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) dr_salt_name(ii), (dr_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_delr%salt)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dr_salt_name(ii), (dr_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dr_read_salt] | backspace, close, open, read, rewind | Reads the dr_salt.del file if it exists, counts the number of salt export coefficient records, allocates arrays accordingly, reads salt names and their export coefficients, crosswalks these salts with the drainage database, and assigns the salt coefficients to hydrograph objects' salt state variables. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as the reader checks for existence before reading.
- The salt export coefficients are stored in dr_salt derived type array and linked to drainage and hydrograph objects.
- No explicit units or column headers are parsed from the file beyond the salt name and coefficients.
- The sample read format is inferred as the source code does not provide explicit example lines.
