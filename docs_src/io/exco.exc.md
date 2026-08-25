---
kind: io
source_symbols:
- exco_db_read
title: '`exco.exc`'
status: filled
source_hash: 58fb877d1ce4036b
version_label: SWAT+ 62.0.0
---

**Primary target:** `exco_db(:)` (array of `type export_coefficient_datafiles`)  
**Read by:** [sym:exco_db_read]

## Bottom Line

The file `exco.exc` configures export coefficient data for various constituent types used in the SWAT+ model.

It is read by the `exco_db_read` subroutine, which loads the data into the `exco_db` array of `export_coefficient_datafiles`.

This file is optional, as the reader checks for its existence before attempting to read.

| Module | Role for this file |
| --- | --- |
| [sym:exco_module] | Provides the `export_coefficient_datafiles` type and the `exco_db` array where the file data is stored. |
| [sym:constituent_mass_module] | Provides the `cs_db` data structure used to determine which additional constituent-specific export coefficient files to read. |
| [sym:input_file_module] | Provides the `in_exco` variable containing the filename for `exco.exc`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable used to store the maximum number of export coefficient records read. |

## File Variables

The file `exco.exc` consists of multiple records each representing export coefficient data for a constituent type. Each record is read into an element of the `exco_db` array of type `export_coefficient_datafiles`. The file columns map directly to the components of this derived type.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `exco_db%name` | character(len=16) |  | Name identifier for the export coefficient record. |
| 3 |  | `exco_db%om_file` | character(len=16) |  | Filename for organic matter export coefficients. |
| 4 |  | `exco_db%pest_file` | character(len=16) |  | Filename for pesticide export coefficients. |
| 5 |  | `exco_db%path_file` | character(len=16) |  | Filename for pathogen export coefficients. |
| 6 |  | `exco_db%hmet_file` | character(len=16) |  | Filename for heavy metal export coefficients. |
| 7 |  | `exco_db%salts_file` | character(len=16) |  | Filename for salts export coefficients. |
| 8 |  | `exco_db%constit_file` | character(len=16) |  | Filename for constituent export coefficients. |
| 9 |  | `exco_db%descrip` | character(len=40) |  | Description or comment for the export coefficient record. |

## Sample

```text
1 'Name1' 'omfile1' 'pest1' 'path1' 'hmet1' 'salt1' 'constit1' 'Description text here'
2 'Name2' 'omfile2' 'pest2' 'path2' 'hmet2' 'salt2' 'constit2' 'Another description'
```

## Read Pattern

```fortran
open (107,file=in_exco%exco)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
do while not eof
  read (107,*,iostat=eof) titldum
end do
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
do ii = 1, imax
  read (107,*,iostat=eof) i
  backspace (107)
  read (107,*,iostat=eof) k, exco_db(i)
end do
close (107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_exco%exco)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, exco_db(i)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:exco_db_read] | backspace, close, open, read, rewind | Reads the export coefficient data from `exco.exc` into the `exco_db` array. It first checks if the file exists, counts the number of records, allocates the array, then reads each record. It also calls other readers to load constituent-specific export coefficient files if they exist. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample read format is inferred from the data type and reading pattern; no explicit example record was found in the source.
- The file is optional as the reader checks for file existence before reading.
- The reader calls other subroutines to read additional export coefficient files for pesticides, pathogens, metals, and salts based on the number of such constituents.
