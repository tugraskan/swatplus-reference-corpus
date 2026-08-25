---
kind: io
source_symbols:
- wet_read_hyd
title: '`gwflow.wetland`'
status: filled
source_hash: 4c0d4e12af970b21
version_label: SWAT+ 62.0.0
---

**Primary target:** wet_thick(:)  
**Read by:** [sym:wet_read_hyd]

## Bottom Line

The file `gwflow.wetland` is an optional input file used when the groundwater flow (gwflow) model is active and wetland bed thickness specification is enabled (gw_wet_flag=1).

It configures the wetland bottom sediment thickness values for individual HRUs by reading wetland names and their corresponding thicknesses.

The reader subroutine `wet_read_hyd` loads this file and updates the `wet_thick` array accordingly.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the logical flag `bsn_cc%gwflow` to indicate if the groundwater flow model is active. |
| [sym:input_file_module] | Supplies the input file name `in_res%hyd_wet` used for hydrology wetland data and possibly other input file management variables. |
| [sym:maximum_data_module] | Provides the `db_mx%wet_hyd` variable used to store the maximum number of wetland hydrology records. |
| [sym:reservoir_data_module] | No direct usage evident in this reader for `gwflow.wetland`. |
| [sym:output_landscape_module] | No direct usage evident in this reader for `gwflow.wetland`. |
| [sym:gwflow_module] | Supplies the file unit `in_wet_cell` for reading `gwflow.wetland`, the `wet_thick` array to store wetland thickness values, the flag `gw_wet_flag` to enable reading this file, and the output unit `out_gw` for logging. |

## File Variables

The `gwflow.wetland` file consists of two header lines followed by multiple records each containing a wetland name and a corresponding bed thickness value. The reader maps each wetland name to an HRU index and stores the thickness value in the `wet_thick` array indexed by HRU.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1-80 | `Header lines` | `header` |  |  | The first two lines in the file are header lines (title and secondary header or blank) that are read and discarded by the reader. |
| 1-20, 21- | `Wetland Name, Thickness` | `wet_name, thick_val` |  |  | Each subsequent line contains a wetland name string (e.g., 'wet019') and a floating-point thickness value representing the wetland bed sediment thickness in meters. |

## Sample

```text
Wetland Thickness File Example:
Line 1: "Wetland Bed Thickness Data"
Line 2: ""
Line 3: wet001 0.5
Line 4: wet002 0.75
Line 5: wet019 1.2
```

## Read Pattern

```fortran
open(in_wet_cell,file='gwflow.wetland')
read(in_wet_cell,*,iostat=eof) header
read(in_wet_cell,*,iostat=eof) header
do
  read(in_wet_cell,*,iostat=eof) wet_name, thick_val
  if (eof /= 0) exit
  idig = scan(wet_name, '0123456789')
  if (idig > 0) then
    read(wet_name(idig:), *, iostat=eof) hru_idx
    if (eof == 0 .and. hru_idx >= 1 .and. hru_idx <= size(wet_thick)) then
      wet_thick(hru_idx) = thick_val
    endif
  endif
enddo
close(in_wet_cell)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_wet_cell | `open(in_wet_cell,file='gwflow.wetland')` |
| Input | `read` | in_wet_cell | `read(in_wet_cell,*,iostat=eof) header` |
| Input | `read` | in_wet_cell | `read(in_wet_cell,*,iostat=eof) header` |
| Input | `read` | in_wet_cell | `read(in_wet_cell,*,iostat=eof) wet_name, thick_val` |
| File control | `close` | in_wet_cell | `close(in_wet_cell)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:wet_read_hyd] | open, read, close | Reads the `gwflow.wetland` file to update wetland bed sediment thickness values in the `wet_thick` array when groundwater flow and wetland thickness specification are enabled. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `gwflow.wetland` is only read if groundwater flow is enabled (bsn_cc%gwflow == 1) and the wetland thickness flag (gw_wet_flag) is set to 1.
- Wetland names are parsed to extract the HRU index by scanning for digits and reading the trailing number.
- If the HRU index is valid, the corresponding element in `wet_thick` is updated with the thickness value.
- No explicit error handling for malformed lines or missing HRUs is implemented; lines without valid HRU indices are skipped.
