---
kind: procedure
symbol: carbon_legacy_open
title: carbon_legacy_open
status: filled
source_hash: 24719cbdc85cab14
version_label: SWAT+ 62.0.0
uses:
  basin_module: Imported from `basin_module`; this procedure reads or writes the listed module
    state.
  carbon_module: Imported from `carbon_module`; this procedure reads or writes the listed
    module state.
  output_path_module: Uses module `output_path_module`.
  hydrograph_module: Uses module `hydrograph_module`.
---

<!-- facts:header -->

Opens the legacy carbon diagnostic output files (`hru_cbn_lyr`, `hru_seq_lyr`, and the plc/cflux/cpool/soil-property files) based on the `hru_cb` print flag, and sets `cbn_diagnostics`.

## Bottom Line

`carbon_legacy_open` derives `cbn_diagnostics` from the `pco%cb_hru` print flag (`"l"` enables the full layer diagnostics; `"y"` gives the lighter files), then opens the enabled legacy carbon output files and writes their banner/header rows, including CSV companions when `pco%csvout` is set.

It replaces the old `carb_coefs.cbn`-driven configuration, mapping diagnostics onto the standard `hru_cb` print flag.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called during output setup when carbon output is enabled; opens the units later written by the legacy carbon writers.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select output conditions | Executes the source at the referenced lines. |
| 2. Write output records | Executes the source at the referenced lines. |
| 3. Update output state | Executes the source at the referenced lines. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco, bsn, bsn_cc, prog` | `pco%cb_hru%d, pco%cb_hru%m, pco%cb_hru%y, pco%cb_hru%a, bsn%name, pco%csvout, bsn_cc%cswat, pco%cb_vars_hru%d, pco%cb_vars_hru%m, pco%cb_vars_hru%y, pco%nb_hru%a` |
| [sym:carbon_module] | `cbn_diagnostics` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

*No state changes recorded.*

## File I/O

<!-- facts:io -->


## Lineage

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `carbon_legacy_module.f90`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'carbon_legacy_module::carbon_legacy_open' has no extracted documentation comment.
