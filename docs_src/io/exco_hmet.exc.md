---
kind: io
source_symbols:
- exco_read_hmet
title: '`exco_hmet.exc`'
status: filled
source_hash: 149085000fad88ce
version_label: SWAT+ 62.0.0
---

**Primary target:** exco_hmet(:)  
**Read by:** [sym:exco_read_hmet]

## Bottom Line

The file exco_hmet.exc contains export coefficient data for heavy metals used in the SWAT+ model.

It is optional and only read if the file exists and is not set to "null" in the input configuration.

The reader subroutine exco_read_hmet loads this file and populates the exco_hmet derived type array with heavy metal export coefficients.

This data configures the heavy metal export coefficients associated with export coefficient objects in the model state.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the ob, obcs, sp_ob, and sp_ob1 variables used to assign heavy metal export coefficients to hydrograph objects. |
| [sym:input_file_module] | Provides the in_exco variable that contains the filename for the heavy metal export coefficient input file. |
| [sym:organic_mineral_mass_module] | No direct usage detected in this reader for reading or storing this file. |
| [sym:constituent_mass_module] | Provides the cs_db derived type with the num_metals constant used to dimension the heavy metal arrays. |
| [sym:exco_module] | Provides the exco_db derived type array used to crosswalk export coefficient names to their indices and the exco_hmet_num array to store mapping indices. |
| [sym:maximum_data_module] | Provides the db_mx derived type with exco_hmet and exco counts used for allocation and looping. |

## File Variables

The exco_hmet.exc file consists of a header block followed by multiple records each containing an export coefficient name and an array of heavy metal export coefficients. The reader maps each record into an element of the exco_hmet derived type array, allocating arrays sized by the number of heavy metals defined in cs_db.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Title line` | `titldum` |  |  | The first line read from the file, typically a title or description line, stored temporarily but not used for model state. |
| 1 | `Header line` | `header` |  |  | The second line read from the file, typically a header describing columns, stored temporarily but not used for model state. |
| 1 | `Export coefficient name` | `exco_hmet_name(ii)` |  |  | The name of the export coefficient record read from the file, used to cross-reference with exco_db to map heavy metal coefficients to export coefficient objects. |
| 2 to end | `Heavy metal export coefficients` | `(exco_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)` |  |  | Array of heavy metal export coefficients for the given export coefficient name, dimensioned by the total number of metals defined in cs_db. |

## Sample

```text
Example lines from exco_hmet.exc:
Title line describing the file
Header line describing columns
ExportCoeff1 0.01 0.02 0.03 ... (for each metal)
ExportCoeff2 0.05 0.01 0.00 ... (for each metal)
...
```

## Read Pattern

```fortran
open (107,file=in_exco%hmet)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
backspace (107)
read (107,*,iostat=eof) exco_hmet_name(ii), (exco_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_exco%hmet)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) exco_hmet_name(ii), (exco_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:exco_read_hmet] | backspace, close, open, read, rewind | Reads the heavy metal export coefficient file exco_hmet.exc if it exists and is not set to "null". It counts the number of records, allocates arrays accordingly, reads the export coefficient names and their heavy metal coefficients, and crosswalks these names to the main export coefficient database. Finally, it assigns the heavy metal coefficients to the hydrograph objects' heavy metal state arrays. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists and is not "null".
- The reader uses the cs_db%num_metals constant to dimension heavy metal arrays.
- The crosswalk between exco_hmet names and exco_db names ensures proper mapping of heavy metal coefficients to export coefficient objects.
- The reader assigns the heavy metal coefficients to hydrograph objects via obcs(iob)%hd(1)%hmet.
