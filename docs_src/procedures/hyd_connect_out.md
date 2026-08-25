---
kind: procedure
symbol: hyd_connect_out
title: hyd_connect_out
status: filled
source_hash: d2c3b2f6b3785a4b
version_label: SWAT+ 62.0.0
locals:
  ii: '`ii` is a running counter for the objects visited in the connectivity chain. It starts
    at 0, is incremented once per object inside the loop, and is written out as the first
    field so the output records are numbered in traversal order.'
  i: '`i` is the implied-do index used to expand the outflow arrays in each write statement.
    It runs from 1 to `ob(icmd)%src_tot` so the routine can print every outgoing link entry
    stored on the current object.'
uses:
  basin_module: '`basin_module` supplies `pco`, which holds the print flags that decide whether
    this routine produces hydcon output at all and whether it also emits the CSV companion
    file. Without `pco%hydcon` and `pco%csvout`, the subroutine would not know which outputs
    to generate.'
  hydrograph_module: '`hydrograph_module` holds the connectivity state that the routine traverses
    and writes. `sp_ob1%objs` gives the first command-object index, `ob(icmd)` provides each
    object''s metadata and outgoing link arrays, and `ob(icmd)%cmd_next` advances the traversal
    through the command chain.'
---

<!-- facts:header -->

Writes the hydrograph connectivity list to the hydcon output file, and optionally to a CSV-formatted companion file. It walks the command chain starting at the first object and records each object's outgoing routing links.

## Bottom Line

`hyd_connect_out` is a reporting routine for SWAT+ hydrograph connectivity. It starts at the first command object, follows the linked command chain through `ob(icmd)%cmd_next`, and writes each object's connectivity summary to the hydcon output stream. If CSV output is enabled, it writes the same records again in comma-delimited form.

The routine does not change routing logic itself; it exposes the already-built connectivity network for diagnostics or downstream inspection. Its result depends on basin print codes in `pco` and on the connectivity structures stored in `hydrograph_module`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after the hydrograph connectivity objects have been assembled in `hydrograph_module`, with `sp_ob1%objs` pointing to the first command object and each object linked to the next through `cmd_next`. It is used when hydcon output is enabled to dump the routing network for inspection, and later analysis depends on these files to verify object-to-object connectivity and outflow links.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check hydcon flag | If `pco%hydcon` is enabled, the routine produces the hydrograph connectivity listing; otherwise it skips the main traversal and goes straight to cleanup. |
| 2. traverse command chain | Iterate through the linked hydrograph command objects beginning with `icmd = sp_ob1%objs` and continuing while `icmd` remains nonzero. |
| 3. number and write hydcon record | Increment the record counter and write the current object's identity, type, properties, source and receiver totals, and all outgoing connectivity entries to unit 7000. |
| 4. check csvout flag | If `pco%csvout` is enabled, also emit the same connectivity record in CSV-style form. |
| 5. write csv record | Write the current object's connectivity data to unit 7001 using a comma-delimited numeric/text format suitable for CSV output. |
| 6. advance to next command | Set `icmd` to the next command-object index using `ob(icmd)%cmd_next` so the loop continues through the connectivity chain. |
| 7. close open file and return | Close unit 172 and return to the caller after the optional output files have been written. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco` | `pco%hydcon, pco%csvout` |
| [sym:hydrograph_module] | `sp_ob1, ob, icmd` | `sp_ob1%objs, ob(icmd)%name, ob(icmd)%typ, ob(icmd)%props, ob(icmd)%props2, ob(icmd)%src_tot, ob(icmd)%rcv_tot, ob(icmd)%obj_out, ob(icmd)%obtyp_out(i), ob(icmd)%obtypno_out(i), ob(icmd)%htyp_out(i), ob(icmd)%cmd_next` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `icmd` | On each loop pass when `pco%hydcon == 'y'` and `icmd /= 0` | `icmd` is advanced from the current object to the next linked command object via `ob(icmd)%cmd_next`, so the routine can traverse the full hydrograph connectivity list. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three source changes for `hyd_connect_out`. The original file was added in df07e3f with the full traversal-and-write routine. In 39fabde, the local counters `ii` and `i` were initialized at declaration, changing only variable initialization style. In 2fe89fd, the CSV write format on unit 7001 changed from `G0.3` to `G0.6`, increasing numeric precision in the CSV output.

- 39fabde only changed the initialization of local variables `ii` and `i` from uninitialized declarations to `= 0`; the traversal and output logic stayed the same.
- 2fe89fd changed the CSV output formatting on unit 7001 from `G0.3` to `G0.6`, affecting the precision of the comma-separated connectivity records.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hyd_connect_out' has no extracted documentation comment.
