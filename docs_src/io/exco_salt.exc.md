---
kind: io
source_symbols:
- exco_read_salt
title: '`exco_salt.exc`'
status: filled
source_hash: 37873258e28555ed
version_label: SWAT+ 62.0.0
---

**Primary target:** exco_salt(:)  
**Read by:** [sym:exco_read_salt]

## Bottom Line

The file `exco_salt.exc` contains export coefficient data for salts, which configure salt export coefficients used in the model's export coefficient calculations.

This file is optional and is read if it exists or if the filename is not set to "null".

The reader `exco_read_salt` loads this file and populates the `exco_salt` derived type array.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the `ob`, `obcs`, `sp_ob`, and `sp_ob1` variables used to assign salt export coefficients to hydrograph objects. |
| [sym:input_file_module] | Provides the `in_exco` variable which contains the filename for the export coefficient salt file. |
| [sym:organic_mineral_mass_module] | No direct usage detected in this reader for reading or storing this file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable which stores the count of export coefficient salt records (`db_mx%exco_salt`). |
| [sym:exco_module] | Provides the `exco_salt`, `exco_salt_name`, `exco_salt_num`, and `exco_db` variables which hold the salt export coefficient data and metadata. |
| [sym:constituent_mass_module] | Provides the `cs_db` variable which contains the number of salts (`cs_db%num_salts`) used to dimension arrays. |

## File Variables

The file `exco_salt.exc` is a text file containing export coefficient salt data. It has a header section followed by multiple records, each with a salt name and a list of salt export coefficients corresponding to salts defined in the constituent mass database. The reader maps each record into the `exco_salt` derived type array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Title line` | `titldum` |  |  | The first title or label line read from the file, used to skip or verify the file format. |
| 1 | `Header line` | `header` |  |  | The header line following the title, also used to skip or verify file format before reading data records. |
| 1 | `Salt export coefficient name` | `exco_salt_name(ii)` |  |  | The name of the export coefficient salt record, used to cross-reference with the export coefficient database. |
| 2 to (1 + cs_db%num_salts) | `Salt export coefficients` | `(exco_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)` |  |  | The array of salt export coefficients for each salt defined in the constituent mass database, associated with the named export coefficient record. |

## Sample

```text
Example lines from `exco_salt.exc` might look like:
"Export Coefficient Salt Data"
"SaltName Coeff1 Coeff2 Coeff3 ..."
SaltRecord1 0.1 0.2 0.3 ...
SaltRecord2 0.05 0.1 0.15 ...
```

## Read Pattern

```fortran
open (107,file=in_exco%salt)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) exco_salt_name(ii), (exco_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_exco%salt)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) exco_salt_name(ii), (exco_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:exco_read_salt] | backspace, close, open, read, rewind | Reads the export coefficient salt file `exco_salt.exc` if it exists or is not set to "null", counts the number of salt export coefficient records, allocates arrays, reads the salt export coefficient names and values into the `exco_salt` array, cross-references these with the export coefficient database, and assigns the salt export coefficients to hydrograph objects. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and read only if it exists or if the filename is not "null".
- The reader uses multiple file control operations (rewind, backspace) to count records before reading data.
- Salt export coefficients are stored in the `exco_salt` derived type array, dimensioned by the number of salts in `cs_db`.
- The crosswalk between `exco_salt_name` and `exco_db` links the salt export coefficients to the export coefficient database.
- The reader assigns salt export coefficients to hydrograph objects' headwaters (`obcs(iob)%hd(1)%salt`).
