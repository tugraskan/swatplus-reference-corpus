---
kind: io
source_symbols:
- dr_read_hmet
title: '`dr_hmet.del`'
status: filled
source_hash: dc89ddefc19e91f5
version_label: SWAT+ 62.0.0
---

**Primary target:** dr_hmet(:)  
**Read by:** [sym:dr_read_hmet]

## Bottom Line

The file dr_hmet.del contains delivery ratio data for hydrometals, configuring the hydrometal export coefficients used in the delivery ratio model state.

This file is optional and is read by the dr_read_hmet subroutine.

The data read from this file populates the dr_hmet derived type array and associated name and index mappings.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the ob, obcs, sp_ob, and sp_ob1 objects used to assign hydrometal coefficients to hydrograph objects. |
| [sym:dr_module] | Supplies the dr_hmet derived type array, dr_hmet_name, dr_hmet_num arrays, and dr_db data structures used to store delivery ratio hydrometal data and crosswalk with dr records. |
| [sym:input_file_module] | Provides the in_delr object which contains the filename for the hydrometal delivery ratio file (in_delr%hmet). |
| [sym:organic_mineral_mass_module] | No direct variables or types used from this module in dr_read_hmet. |
| [sym:constituent_mass_module] | No direct variables or types used from this module in dr_read_hmet. |
| [sym:maximum_data_module] | Provides the db_mx object which stores the count of delivery ratio hydrometal records (db_mx%dr_hmet). |

## File Variables

The dr_hmet.del file consists of a header section followed by multiple records each containing a hydrometal name and a vector of hydrometal delivery ratio coefficients. These records are read into the dr_hmet derived type array, with each element holding the hydrometal name and an array of coefficients corresponding to metals.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Title line` | `titldum` |  |  | Reads the first title line of the file, used as a descriptive header but not stored persistently. |
| 1 | `Header line` | `header` |  |  | Reads the second header line of the file, also descriptive and not stored persistently. |
| 1 | `Hydrometal name` | `dr_hmet_name(ii)` |  |  | Reads the hydrometal name string for each record, used to identify and cross-reference hydrometal delivery ratio data. |
| 2 to end | `Hydrometal delivery ratios` | `(dr_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)` |  |  | Reads an array of delivery ratio coefficients for each hydrometal, one coefficient per metal defined in cs_db%num_metals. |

## Sample

```text
Example dr_hmet.del file snippet:
Line 1: "Hydrometal Delivery Ratio Data"
Line 2: "Header describing columns"
Line 3+: "HydrometalName 0.1 0.2 0.3 0.4 ..." (one line per hydrometal, with coefficients for each metal)
```

## Read Pattern

```fortran
open (107,file=in_delr%hmet)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) dr_hmet_name(ii), (dr_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_delr%hmet)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) dr_hmet_name(ii), (dr_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:dr_read_hmet] | backspace, close, open, read, rewind | Reads the hydrometal delivery ratio data from dr_hmet.del, populates the dr_hmet array with hydrometal names and their delivery ratio coefficients, crosswalks these with dr records, and assigns the hydrometal coefficients to hydrograph objects. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the existence check and conditional reading in dr_read_hmet.
- The exact format of hydrometal delivery ratio lines is inferred from the read statement and array dimensions.
- No explicit sample data was found in the source; the sample read format is based on typical file structure implied by the code.
