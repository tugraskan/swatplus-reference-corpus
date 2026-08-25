---
kind: procedure
symbol: gwflow_write_celldef
title: gwflow_write_celldef
status: filled
source_hash: d13727a7ffa9a41a
version_label: SWAT+ 62.0.0
locals:
  i: '`i` is the loop index over groundwater cells, used to select each entry from `cell_row`,
    `cell_col`, and `gw_state` and write one definition line per cell.'
uses:
  gwflow_module: '`gwflow_module` supplies the cell count, grid layout, output unit, and per-cell
    state that determine what gets written. `ncell` sets the loop bounds, `out_gw_celldef`
    identifies the file unit, `cell_row` and `cell_col` provide structured-grid positions,
    and `gw_state(i)%xcrd`, `%ycrd`, `%zone`, `%stat`, and `%area` provide the fields written
    to the definition file.'
---

<!-- facts:header -->

Writes a groundwater cell-definition text file that maps each active GW cell to its spatial coordinates and metadata. It runs during groundwater output initialization so later output files can use a consistent cell index map.

## Bottom Line

This subroutine opens `gwflow_cell_definition.txt`, writes a header, then loops through all groundwater cells and writes one line for each active cell. Each line records the cell index, row and column for structured grids, centroid coordinates, zone, status, and area.

It matters because this file provides the cell-to-location reference used by groundwater output reporting. The routine is called once from `gwflow_output_init` during initialization, before the rest of the groundwater output files are produced.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during groundwater output initialization, immediately after `gwflow_output_init` starts the groundwater output setup. `gwflow_output_init` prepares the output workflow and then calls this routine to create the cell-definition file before later groundwater output files rely on the cell index mapping.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. open file | Open `gwflow_cell_definition.txt` on the configured output unit so the routine can write the cell-definition table. |
| 2. write header | Write the column header line that labels the cell-id, row, column, coordinate, zone, status, and area fields. |
| 3. loop over cells | Iterate across every groundwater cell index from 1 to `ncell`. |
| 4. require active cell | Process only cells whose groundwater status is positive, so inactive cells are skipped. |
| 5. check grid type | Select the output format based on whether the grid is structured. |
| 6. write structured row | For structured grids, write the cell index, row, column, centroid coordinates, zone, status, and area using the stored row/column indices. |
| 7. write unstructured row | Otherwise, fall through to the alternate output branch for non-structured grids. |
| 8. write fallback row | For non-structured grids, write the same cell metadata but place zeros in the row and column fields. |
| 9. close file | Close the cell-definition file after all eligible cell records have been written. |
| 10. return | Return control to the caller after finishing the output file. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `cell_row, gw_state, cell_col, out_gw_celldef, ncell` | `gw_state(i)%ycrd, gw_state(i)%zone, gw_state(i)%stat, gw_state(i)%area, gw_state(i)%xcrd` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage evidence shows two behavior-changing revisions to `gwflow_output.f90`, but neither diff touched `gwflow_write_celldef` itself. The 2026-04-02 re-merge added a call to `gwflow_write_celldef` from `gwflow_output_init`, and the 2026-04-16 re-merge changed other groundwater output logic to guard GIS-ID selection by `grid_type`.

- 2026-04-02: `gwflow_output_init` began calling `gwflow_write_celldef` during groundwater output setup, making the cell-definition file part of initialization.
- 2026-04-16: neighboring groundwater output code was updated to use `grid_type` when choosing GIS IDs, reinforcing the structured-vs-unstructured distinction used by this file writer.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_write_celldef' has no extracted documentation comment.
