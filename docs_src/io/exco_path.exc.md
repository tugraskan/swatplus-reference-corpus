---
kind: io
source_symbols:
- exco_read_path
title: '`exco_path.exc`'
status: filled
source_hash: af37be5a68e7874b
version_label: SWAT+ 62.0.0
---

**Primary target:** exco_path(:)  
**Read by:** [sym:exco_read_path]

## Bottom Line

The file exco_path.exc configures export coefficient paths for the model, specifying export coefficients for each path in the catchment.

It is optional and only read if the file exists and the path is not 'null'.

The reader exco_read_path loads this file and populates the exco_path derived type array and related variables.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the ob, obcs, sp_ob, and sp_ob1 objects used to assign export coefficient paths to hydrograph objects. |
| [sym:input_file_module] | Provides the in_exco object that contains the path to the exco_path.exc file. |
| [sym:organic_mineral_mass_module] | No direct usage evident in this reader. |
| [sym:constituent_mass_module] | No direct usage evident in this reader. |
| [sym:exco_module] | Provides the exco_path derived type array, exco_path_name, exco_path_num, and exco_db arrays used to store export coefficient path data. |
| [sym:maximum_data_module] | Provides db_mx and cs_db objects used for dimensioning and counts of export coefficient paths and catchment paths. |

## File Variables

The exco_path.exc file contains export coefficient path data with a header and multiple records. Each record includes a path name and an array of export coefficients for all catchment paths. The reader maps these records into the exco_path derived type array and associated name and index arrays.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| N/A | `Title line` | `titldum` |  |  | Reads a title or descriptive line from the file, used to skip or verify the file format header. |
| N/A | `Header line` | `header` |  |  | Reads a header line from the file, typically column headings or metadata, used to skip or verify the file format header. |
| 1 | `Export coefficient path name` | `exco_path_name(ii)` |  |  | Reads the name of the export coefficient path for the current record, used to identify and cross-reference paths. |
| 2 to cs_db%num_paths+1 | `Export coefficients for each catchment path` | `(exco_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |  |  | Reads an array of export coefficients corresponding to each catchment path, storing them in the exco_path derived type. |

## Sample

```text
Example exco_path.exc file snippet:
Title line (ignored)
Header line (ignored)
PathName1 0.1 0.2 0.3 0.4 ... (one coefficient per catchment path)
PathName2 0.05 0.1 0.15 0.2 ...
...
```

## Read Pattern

```fortran
open (107,file=in_exco%path)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) exco_path_name(ii), (exco_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_exco%path)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) exco_path_name(ii), (exco_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:exco_read_path] | backspace, close, open, read, rewind | Reads the exco_path.exc file if it exists and is not 'null', counts the number of export coefficient paths, allocates storage, reads all export coefficient path names and their associated export coefficient arrays, cross-references these paths with exco_db entries, and assigns the export coefficient path arrays to hydrograph objects' path state. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists and the path is not 'null'.
- The reader uses multiple reads and file rewinds/backspaces to count records and then read data.
- The exco_path array is allocated dynamically based on the number of records in the file.
- The crosswalk loop matches exco_db entries to exco_path names to assign indices.
- The export coefficient paths are assigned to hydrograph objects' path arrays for model use.
