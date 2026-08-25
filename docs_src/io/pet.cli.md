---
kind: io
source_symbols:
- basin_read_cc
- cli_petmeas
title: '`pet.cli`'
status: filled
source_hash: 338c12d3f52220df
version_label: SWAT+ 62.0.0
---

**Primary target:** bsn_cc%pet  
**Read by:** [sym:basin_read_cc]

## Bottom Line

The file 'pet.cli' configures potential evapotranspiration (PET) measurement settings used in the basin model state.

It is conditionally required when the basin's PET method code (bsn_cc%pet) equals 3.

The primary reader that loads this file is the 'basin_read_cc' subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file unit and file name variables such as in_basin%codes_bas used to locate input files. |
| [sym:basin_module] | Supplies the 'bsn_cc' derived type instance which stores basin configuration including the PET method code 'bsn_cc%pet'. |

## File Variables

The 'pet.cli' file contains textual header lines and configuration parameters related to potential evapotranspiration measurement. The file is read sequentially into character variables and the basin configuration type 'bsn_cc'.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1-80 | `Title line` | `titldum` |  |  | The first title line read from 'pet.cli', stored temporarily in the character variable 'titldum'. |
| 1-80 | `Header line` | `header` |  |  | The header line read from 'pet.cli', stored temporarily in the character variable 'header'. |
| 1-80 | `Additional title or parameter line` | `titldum` |  |  | A third line read from 'pet.cli', again stored in 'titldum', likely containing additional configuration or descriptive text. |

## Sample

```text
Example 'pet.cli' content lines as read by basin_read_cc:
Line 1 (titldum): 'Potential Evapotranspiration Measurement Settings'
Line 2 (header): 'Parameter1 Parameter2 Parameter3 ...'
Line 3 (titldum): 'Additional configuration or description line'
```

## Read Pattern

```fortran
open (140,file = 'pet.cli')
read (140,*,iostat=eof) titldum
read (140,*,iostat=eof) header
read (140,*,iostat = eof) titldum
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 140 | `open (140,file = 'pet.cli')` |
| Input | `read` | 140 | `read (140,*,iostat=eof) titldum` |
| Input | `read` | 140 | `read (140,*,iostat=eof) header` |
| Input | `read` | 140 | `read (140,*,iostat = eof) titldum` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:basin_read_cc] | open, read | Reads the 'pet.cli' file conditionally when the basin PET method code (bsn_cc%pet) equals 3, loading PET measurement configuration lines into temporary character variables and the basin configuration type. |
| [sym:cli_petmeas] | close, open, read, rewind | Reads the PET measurement configuration file specified by in_cli%pet_cli, parsing multiple header and data lines including counts and filenames for PET measurement data. This reader manages detailed PET measurement file metadata. |

## Review Notes

- The 'pet.cli' file is read by two procedures: 'basin_read_cc' reads a few header lines conditionally based on basin PET method, while 'cli_petmeas' reads detailed PET measurement metadata including counts and filenames.
- The exact format and semantics of the lines read into 'titldum' and 'header' are not fully documented in the source; further review of 'cli_petmeas' may clarify the detailed structure.
- The 'basin_read_cc' reader closes unit 107 (codes_bas) after reading but does not explicitly close unit 140 ('pet.cli'); this may be handled elsewhere.
