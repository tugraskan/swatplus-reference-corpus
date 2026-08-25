---
kind: io
source_symbols:
- carbon_layers_read
title: '`carbon_layers.prt`'
status: filled
source_hash: 10358caa9104aac6
version_label: SWAT+ 62.0.0
---

**Primary target:** cb_n_layers  
**Read by:** [sym:carbon_layers_read]

## Bottom Line

carbon_layers.prt is an optional input file that specifies the number of soil carbon layers to include in per-layer carbon outputs.

If present, it overrides the default layer count determined by the model's landscape initialization.

The file is read by the `carbon_layers_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:carbon_module] | Provides the variables `cb_n_layers` and `cb_n_layers_explicit` which store the number of carbon layers and a flag indicating if this number was explicitly set by the input file. |

## File Variables

The file consists of three lines: a title line, a header line (both free text and ignored), and a single integer specifying the number of soil carbon layers to use.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| entire line | `Title` | `titldum` |  |  | The first line of the file, a free-text title string that is read but not used by the model. |
| entire line | `Header` | `header` |  |  | The second line of the file, a free-text header string that is read but ignored by the model. |
| integer value | `Number of Layers` | `n_lyr` |  |  | The third line contains a single integer specifying the number of soil carbon layers to include in outputs. |

## Sample

```text
Example carbon_layers.prt file:
Line 1: Soil Carbon Layer Configuration
Line 2: Number of layers for carbon output
Line 3: 5
```

## Read Pattern

```fortran
open (107, file='carbon_layers.prt', iostat=eof)
read (107, *, iostat=eof) titldum
read (107, *, iostat=eof) header
read (107, *, iostat=eof) n_lyr
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107, file='carbon_layers.prt', iostat=eof)` |
| Input | `read` | 107 | `read (107, *, iostat=eof) titldum` |
| Input | `read` | 107 | `read (107, *, iostat=eof) header` |
| Input | `read` | 107 | `read (107, *, iostat=eof) n_lyr` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:carbon_layers_read] | open, read | Reads the optional carbon_layers.prt file to set the number of soil carbon layers (`cb_n_layers`) used in per-layer carbon outputs. If the file is missing or invalid, the model defaults to the largest soil layer count across all HRUs. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
