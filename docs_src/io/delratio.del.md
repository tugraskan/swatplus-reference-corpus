---
kind: io
source_symbols:
- dr_db_read
title: '`delratio.del`'
status: filled
source_hash: a64a6078898ef4dc
version_label: SWAT+ 62.0.0
---

**Primary target:** `dr_db(:)` (array of `type delivery_ratio_datafiles`)  
**Read by:** [sym:dr_db_read]

## Bottom Line

The file `delratio.del` configures delivery ratio data used in SWAT+ to specify how different constituent types are delivered through the watershed.

It is read by the `dr_db_read` subroutine, which loads the data into an array of `type delivery_ratio_datafiles` named `dr_db`.

This file is optional and only processed if it exists or the filename is not "null".

After reading the main delivery ratio data, `dr_db_read` also calls other readers to load delivery ratio data for specific constituent types such as pesticides, pathogens, heavy metals, and salts.

| Module | Role for this file |
| --- | --- |
| [sym:dr_module] | Provides the derived type `delivery_ratio_datafiles` and the array `dr_db` where the delivery ratio records are stored. |
| [sym:input_file_module] | Provides the input file name container `in_delr%del_ratio` used to locate the `delratio.del` file. |
| [sym:constituent_mass_module] | Provides the `cs_db` data structure which contains counts of constituent types (`num_pests`, `num_paths`, `num_metals`, `num_salts`) used to conditionally read additional delivery ratio data. |
| [sym:maximum_data_module] | Provides the `db_mx` module variable where `db_mx%dr` is set to the number of delivery ratio records read, controlling allocation of `dr_db`. |

## File Variables

The `delratio.del` file consists of multiple records each corresponding to a delivery ratio datafile entry. Each record is read into an element of the `dr_db` array of `type delivery_ratio_datafiles`. The file columns map directly to the components of this derived type, with each field being a fixed-length character string representing filenames or identifiers related to delivery ratios for different constituent types.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `dr_db%name` | character(len=16) |  | The name identifier for the delivery ratio datafile entry. |
| 3 |  | `dr_db%om_file` | character(len=16) |  | Filename for organic matter delivery ratio data associated with this record. |
| 4 |  | `dr_db%pest_file` | character(len=16) |  | Filename for pesticide delivery ratio data associated with this record. |
| 5 |  | `dr_db%path_file` | character(len=16) |  | Filename for pathogen delivery ratio data associated with this record. |
| 6 |  | `dr_db%hmet_file` | character(len=16) |  | Filename for heavy metal delivery ratio data associated with this record. |
| 7 |  | `dr_db%salts_file` | character(len=16) |  | Filename for salts delivery ratio data associated with this record. |

## Sample

```text
Example record block from `delratio.del` (from Ames_sub1 dataset):
  "DeliveryRatio1"
  "OM_File1       PEST_File1     PATH_File1     HMet_File1     Salts_File1  "
```

## Read Pattern

```fortran
open (107,file=in_delr%del_ratio)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) dr_db(ii)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_delr%del_ratio)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dr_db(ii)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dr_db_read] | close, open, read, rewind | Reads the main delivery ratio data from `delratio.del` into the `dr_db` array. It first checks if the file exists or is not set to "null", then counts the number of records to allocate the array. After reading the main data, it calls specialized readers to load delivery ratio data for organic matter, pesticides, pathogens, heavy metals, and salts based on the counts of those constituent types. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists or the filename is not "null".
- The sample record format is inferred from typical usage; no explicit example record block was found in the source.
- The `dr_db_read` subroutine calls other readers conditionally based on constituent counts in `cs_db` to load additional delivery ratio data for specific constituent types.
