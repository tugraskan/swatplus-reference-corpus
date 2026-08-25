---
kind: procedure
symbol: gwflow_minl
title: gwflow_minl
status: filled
source_hash: 056976a3a73897f7
version_label: SWAT+ 62.0.0
args:
  cell_id: Identifies which groundwater cell's mineral reactions would be processed if the
    routine were implemented; it selects the cell-specific groundwater chemistry state for
    the call.
  gw_vol: Provides the groundwater volume for that cell, which would be needed to scale any
    mineral precipitation-dissolution rates into mass changes.
uses:
  gwflow_module: This routine is part of the groundwater chemistry workflow managed by `gwflow_module`.
    The module-level flags and arrays determine whether mineral reactions should run and would
    supply the cell chemistry state and reaction bookkeeping if the stub were replaced with
    active calculations.
---

<!-- facts:header -->

Stubs the groundwater salt-mineral reaction hook for one gwflow cell. It is called from `gwflow_chem` when mineral reactions are enabled, but the routine currently returns without changing state.

## Bottom Line

`gwflow_minl` is the placeholder entry point for salt mineral precipitation-dissolution in a groundwater cell. The source comment says it should run from `gwflow_chem` when `gwsol_minl == 1`, but the body is currently stubbed and immediately returns.

Because it does not yet call the mineral-chemistry helpers named in the header comment, it has no active reaction calculations or state updates in this version. Its main importance is as the planned integration point for future salt-mineral chemistry.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`gwflow_minl` runs inside the groundwater chemistry step after `gwflow_chem` has already checked whether salt chemistry is active and after it has populated the cell's first-order salt reaction terms. `gwflow_chem` calls it only when `gwsol_minl == 1`, so this routine is the mineral-reaction hook for a cell during groundwater solute processing. Any future updates made here would feed back into the groundwater constituent mass balance used later in the transport workflow.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Declare the groundwater chemistry module dependency and accept the cell-specific arguments. | The routine begins with the `gwflow_module` use association, then receives the target cell ID and groundwater volume for the current groundwater chemistry update. |
| 2. Exit immediately without performing mineral reactions. | The only executable statement is a stub comment followed by `return`, so no mineral precipitation-dissolution calculations or module-state updates are performed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gwflow_module` | `gwsol_minl, gwsol_state, gwsol_chem, mass_rct, gwsol_rctn, gwsol_salt, gwsol_cons` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The routine was introduced in `df07e3f` as a new stubbed `gwflow_minl` procedure with a purpose comment describing salt mineral precipitation-dissolution reactions. Later commits only adjusted formatting or surrounding file content in the extracted diffs; the current source still shows the routine as a no-op stub that immediately returns.

- df07e3f added `gwflow_minl` as a new subroutine stub in `gwflow_chem.f90` and documented it as the mineral-reaction hook called from `gwflow_chem`.
- Subsequent resolved diffs did not change `gwflow_minl` behavior in the extracted span; the routine remains an immediate return stub.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_minl' has no extracted documentation comment.
- algorithm_steps revised: replaced the single placeholder return step with two source-backed steps that reflect the stubbed procedure body.
- Source comment says the routine should call salt-mineral helpers in older RTB code, but no callees are present in the extracted source span; the routine currently returns immediately.
