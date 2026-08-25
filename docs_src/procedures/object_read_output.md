---
kind: procedure
symbol: object_read_output
title: object_read_output
status: filled
source_hash: 5f1b65b0d5d6301c
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and discard the title line from `object.prt` before
    the routine processes the header and data records.
  header: Temporary string used to read and discard the header line from `object.prt` before
    counting and parsing the object-output entries.
  eof: I/O status flag for each read from `object.prt`; it controls loop exit on end-of-file
    or read failure.
  imax: Tracks the largest object index encountered in `object.prt` so the routine can allocate
    `ob_out(0:imax)` large enough for every referenced entry.
  i_exist: Flags whether the `object.prt` file exists before opening it; if it does not exist,
    the routine allocates a minimal `ob_out(0:0)` and skips file parsing.
  i: Loop counter used while scanning and later processing object-output records; also used
    as the index for the selected object entry in the dispatch logic.
  ii: Temporary index read from `object.prt` before backspacing and rereading the full record;
    it identifies which `ob_out` element the record belongs to.
  k: Leading integer field read from each `object.prt` record and then discarded from further
    logic; it is part of the record structure but not used in subsequent decisions.
  iunit: Base output unit number copied from `ob_out(i)%unitno`; the routine opens each destination
    file on `iunit+i` to give each object a unique unit.
uses:
  input_file_module: The routine needs `in_sim%object_prt` to know which input file to inspect.
    It uses that path both to test file existence and to open `object.prt` for reading the
    object-output configuration.
  hydrograph_module: This module supplies the `ob_out` array that the routine fills, the `sp_ob1`
    starting indices used to convert object-type labels into internal object numbers, and
    the header records written into each output file. Those shared types and globals are the
    core data structures this setup step prepares for later hydrograph output.
  maximum_data_module: The routine records the number of configured object-output entries
    in `db_mx%object_prt`, so the maximum-data bookkeeping module reflects how many object
    output files were defined in `object.prt`.
---

<!-- facts:header -->

Reads `object.prt`, counts object-output definitions, and creates per-object hydrograph output files. It maps each listed object and hydrograph type to internal IDs, then writes the appropriate header to each output file.

## Bottom Line

`object_read_output` is a file-driven setup routine for SWAT+ object hydrograph output. It opens `object.prt`, scans the listed output definitions to determine how many objects are configured and the largest object index, then allocates `ob_out` and fills each entry with the object type, object number, hydrograph type, and output filename.

After parsing each definition, the routine translates the textual object type and hydrograph type into internal numeric codes using `sp_ob1` and the `hydtyp` selector, stores the total count in `db_mx%object_prt`, and opens each destination output file to write the correct header structure (`hyd_hdr`, `sol_hdr`, `plt_hdr`, or `fp_hdr`). Those files become the per-object output streams used later in the model.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model setup, after the simulation input module has provided the `object.prt` path and before time stepping starts. Its parsed `ob_out` definitions, object-number mappings, and file headers are then used by later hydrograph-output routines that write object-specific output during the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and inspect the object-output file path | The routine clears the object-output count and maximum index, then checks whether `in_sim%object_prt` exists and is not the string `null` before deciding whether to parse the file or fall back to a minimal allocation. |
| 2. Allocate a minimal output array when no file is available | If the configured object-output file is missing or disabled, the routine allocates `ob_out(0:0)` and skips the rest of the parsing logic. |
| 3. Open and pre-scan `object.prt` | The routine opens the file and reads the title, header, and leading integer field from each record to count how many output definitions exist and to compute the maximum object index `imax`. |
| 4. Store the record count and allocate `ob_out` | It saves the number of object-output definitions in `db_mx%object_prt` and allocates `ob_out(0:imax)` large enough for the largest referenced index. |
| 5. Rewind and restart the file parse | The routine rewinds unit 107 and rereads the title and header so it can make a second pass through the object-output definitions from the top of the file. |
| 6. Read each object-output record | For each configured output, it reads the target index, backs up one record, and rereads the full line into `ob_out(ii)` fields: object type, object type number, hydrograph type, and output filename. |
| 7. Map object type labels to internal object numbers | The `select case` on `ob_out(i)%obtyp` translates object-type labels such as `hru`, `hlt`, `ru`, `res`, `cha`, `exc`, `dr`, `out`, and `sdc` into model object numbers using the corresponding `sp_ob1` start indices. |
| 8. Map hydrograph type labels to numeric codes | A second `select case` converts `hydtyp` labels into codes 1 through 10, covering total flow, recharge, surface, lateral, tile, soil water, soil nutrients by layer, soil nutrients by profile, plant status, and channel/floodplain water balance. |
| 9. Open the destination output file and write its header | The routine copies the file unit from `ob_out(i)%unitno`, opens the configured output filename, and writes the appropriate header record based on `hydno` so the file is ready for later time-series output. |
| 10. Finish the loop and close the input file | After all configured outputs are processed, the loop exits, unit 107 is closed, and the subroutine returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_sim` | `in_sim%object_prt` |
| [sym:hydrograph_module] | `ob_out, sp_ob1, mobj_out, res, dr, hyd_hdr_time, hyd_hdr, sol_hdr, plt_hdr, fp_hdr` | `ob_out(ii)%obtyp, ob_out(ii)%obtypno, ob_out(ii)%hydtyp, ob_out(ii)%filename, ob_out(i)%obtyp, ob_out(i)%objno, sp_ob1%hru, ob_out(i)%obtypno, sp_ob1%hru_lte, sp_ob1%ru, sp_ob1%res, sp_ob1%chan, sp_ob1%exco, sp_ob1%dr, sp_ob1%outlet, sp_ob1%chandeg, ob_out(i)%hydtyp, ob_out(i)%hydno, ob_out(i)%unitno, ob_out(i)%filename` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%object_prt` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mobj_out` | When `object.prt` is parsed successfully, before the second pass through the file. | `mobj_out` is incremented once per output-definition record so it records how many object output files are configured; later loops use this count to process every entry. |
| `db_mx%object_prt` | After the first file scan finishes and before `ob_out` is allocated. | `db_mx%object_prt` is set to the final number of object-output definitions so the maximum-data module reflects the configured count for this input file. |
| `ob_out(i)%objno` | For each reread record after the backspace and full line read. | `ob_out(i)%objno` is derived from the object type and type number, using `sp_ob1` offsets to convert the configured object reference into the internal model object number. |
| `ob_out(i)%hydno` | For each reread record after `obtyp` and `hydtyp` are available. | `ob_out(i)%hydno` is assigned from the textual hydrograph type so later output logic can choose the correct header and output format for that file. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was introduced in commit df07e3f with the full object-output parsing and file-initialization logic. Commit 94b6dec later preserved that logic while adding the current source version into the tree. Commit 39fabde initialized the local variables with default values. Commit e18817a updated the recognized hydrograph and object-type labels from abbreviated names to the current strings `sol_water`, `solnut_ly`, `solnut_pr`, `plant`, and `cha_fp`, and kept the unit-selection logic unchanged.

- df07e3f added `object_read_output` as a new subroutine that reads `object.prt`, counts entries, allocates `ob_out`, maps object and hydrograph codes, opens output files, and writes their headers.
- 39fabde initialized `titldum`, `header`, `eof`, `imax`, `i`, `ii`, `k`, and `iunit`, reducing dependence on uninitialized local state while keeping the parsing workflow the same.
- e18817a changed the accepted `hydtyp` and `obtyp` strings from abbreviated forms to the current names `sol_water`, `solnut_ly`, `solnut_pr`, `plant`, and `cha_fp` so the parser matches updated input-file labels.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'object_read_output' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 10 source-backed steps to cover the initial file check, both parsing passes, type mapping, file initialization, and teardown.
