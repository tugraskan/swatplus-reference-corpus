---
kind: io
source_symbols:
- dr_path_read
title: '`dr_path.del`'
status: filled
source_hash: c86642e688cfe1ff
version_label: SWAT+ 62.0.0
---

**Primary target:** dr_path(:)  
**Read by:** [sym:dr_path_read]

## Bottom Line

The file dr_path.del configures delivery ratio path data used in routing hydrologic flows through the model.

It is optional and read only if the path file exists or is not set to 'null'.

The reader dr_path_read loads this file, populating the dr_path derived type array with path names and delivery ratio values.

This data is then cross-referenced with dr_db and assigned to hydrograph objects to configure flow routing paths.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the hydrograph object arrays ob, obcs, and sp_ob1/sp_ob used to assign delivery ratio paths to hydrograph states. |
| [sym:dr_module] | Supplies the dr_path derived type array and dr_db database used to store delivery ratio path names and link them to delivery ratio objects. |
| [sym:input_file_module] | Provides the in_delr input file descriptor holding the path to the dr_path.del file. |
| [sym:organic_mineral_mass_module] | No direct usage in this reader; imported but no variables referenced. |
| [sym:constituent_mass_module] | No direct usage in this reader; imported but no variables referenced. |
| [sym:maximum_data_module] | Provides db_mx which holds counts such as dr_path and dr used for array sizing and loops. |

## File Variables

The file dr_path.del contains delivery ratio path names and associated delivery ratio values for each path. The reader dr_path_read opens this file, reads header lines, counts the number of path records, allocates arrays accordingly, and then reads each path name and its delivery ratio values into the dr_path derived type array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Title line` | `titldum` |  |  | Reads a title or descriptive line from the file, used as a placeholder or to skip header text. |
| 1 | `Header line` | `header` |  |  | Reads a header line from the file, likely containing column labels or metadata. |
| N/A | `Path name` | `dr_path_name(ii)` |  |  | Reads the name of the delivery ratio path for the current record. |
| N/A | `Delivery ratio path values` | `(dr_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |  |  | Reads an array of delivery ratio values for each path index, representing the fraction of flow delivered along each path. |

## Sample

```text
Example dr_path.del snippet:
Title line text
Header line text
PathName1 0.1 0.2 0.3 0.4
PathName2 0.3 0.3 0.2 0.2
PathName3 0.25 0.25 0.25 0.25
```

## Read Pattern

```fortran
open (107,file=in_delr%path)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) dr_path_name(ii), (dr_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_delr%path)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dr_path_name(ii), (dr_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dr_path_read] | backspace, close, open, read, rewind | Reads the delivery ratio path file dr_path.del if it exists, counts the number of path records, allocates arrays, reads path names and delivery ratio values into dr_path, cross-references with dr_db to assign path indices, and sets the delivery ratio paths in hydrograph objects. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and read only if it exists or is not 'null'.
- The reader uses multiple reads and file control statements to count records before allocating arrays.
- The delivery ratio paths read here are linked to dr_db and assigned to hydrograph objects for routing.
- No explicit units or detailed format beyond Fortran list-directed reads are documented in source.
