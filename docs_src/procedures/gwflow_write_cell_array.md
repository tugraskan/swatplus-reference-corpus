---
kind: procedure
symbol: gwflow_write_cell_array
title: gwflow_write_cell_array
status: filled
source_hash: 00de0567e9c78eb9
version_label: SWAT+ 62.0.0
args:
  iunit: Open Fortran output unit to which the formatted row is written.
  values: Row of cell values to emit; the routine writes every element from 1 through `ncell_in`
    in order.
  ncell_in: Number of elements from `values` to write in the output row.
  fmt_code: 'Selects the output numeric format: 1 uses fixed-point `f12.3`, 2 uses scientific
    `e12.3`, and 3 uses scientific `e12.6`.'
locals:
  i: Loop index used in the implied-DO list that writes each element of `values` in sequence.
uses:
  gwflow_module: '`gw_state` is imported from `gwflow_module`, so this routine is tied to
    the groundwater model state context even though the extracted body does not reference
    any `gw_state` component directly; it marks the procedure as part of the groundwater flow
    output subsystem.'
---

<!-- facts:header -->

Writes one row of groundwater cell values to an open output unit using one of three numeric formats.

## Bottom Line

This helper prints an array of active-cell values to the already-open file connected to `iunit`. It does not compute groundwater results; it only serializes the caller-provided `values` vector in the format selected by `fmt_code`.

The routine matters because groundwater output routines can reuse it for different products, such as heads, fluxes, and high-precision transit-time values, while keeping the row layout consistent across files.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside groundwater output generation after the caller has assembled a temporary array of cell values and chosen the destination unit and format code. Its output becomes part of the model's groundwater text files, such as transit-time output, and later analysis depends on those files being written in the expected row format.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select format | Choose one of three output formats based on `fmt_code` so the same array-writing helper can serve heads, fluxes, and high-precision values. |
| 2. write fixed-point row | If `fmt_code` is 1, write the full `values(1:ncell_in)` row to `iunit` using format 101, which prints each value as `f12.3` for head-like output. |
| 3. write scientific row | If `fmt_code` is 2, write the full `values(1:ncell_in)` row to `iunit` using format 102, which prints each value as `e12.3` for flux-like output. |
| 4. write high-precision row | If `fmt_code` is 3, write the full `values(1:ncell_in)` row to `iunit` using format 103, which prints each value as `e12.6` for higher-precision output. |
| 5. return | Exit after the selected record has been written; no state is modified and no file unit is closed or repositioned. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

One resolved commit changed this routine's behavior by increasing the repeat count in all three format statements from 10000 to 99999, expanding how many formatted values can be written in a single record. A later resolved commit's diff in the provided range only removed the separate `gwflow_write_cell_header` subroutine from the file and did not alter `gwflow_write_cell_array` itself.

- c38f3b8 widened formats 101, 102, and 103 from 10000 to 99999 repeated fields, allowing longer output rows for the same writer routine.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_write_cell_array' has no extracted documentation comment.
