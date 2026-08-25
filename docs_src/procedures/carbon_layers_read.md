---
kind: procedure
symbol: carbon_layers_read
title: carbon_layers_read
status: filled
source_hash: 3fcf509140b4f843
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for the first free-text line in `carbon_layers.prt`;
    it holds the file title and is not used after being read.
  header: Temporary character buffer for the second free-text line in `carbon_layers.prt`;
    it captures the header line and is not used after being read.
  eof: I/O status flag for the file check, open, and reads. A nonzero value means the file
    is missing or the record read failed, so the routine exits or skips the update.
  n_lyr: Holds the requested number of soil layers read from the third record of `carbon_layers.prt`;
    this is the candidate value for `cb_n_layers`.
  i_exist: Logical flag set by `inquire` to tell whether `carbon_layers.prt` is present before
    trying to open it.
uses:
  carbon_module: '`carbon_module` owns the persistent carbon layer configuration that this
    routine updates. `cb_n_layers` is the layer-count setting used by carbon output logic,
    and `cb_n_layers_explicit` records whether this optional file explicitly supplied that
    setting.'
---

<!-- facts:header -->

Reads optional `carbon_layers.prt` settings and updates the carbon layer-count control used by carbon output routines.

## Bottom Line

`carbon_layers_read` checks whether `carbon_layers.prt` exists, then opens it and reads three records: a title string, a header string, and the requested number of soil layers to include in per-layer carbon output. If the file is missing, or if the layer count is invalid, the routine leaves the module default in place and returns without changing the carbon layer count.

When a valid positive layer count is found, the routine stores it in `carbon_module%cb_n_layers` and marks `cb_n_layers_explicit` true so later carbon-output setup can tell the count came from this optional file rather than from the basin-wide defaulting logic.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during basin initialization from `proc_bsn`, after basin, CO2, and carbon basin settings have already been read. Its result controls later carbon-output setup by telling the model whether an explicit layer count was provided in `carbon_layers.prt` or whether the default layer-count behavior should remain in effect.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check file exists | Uses `inquire` to see whether `carbon_layers.prt` is present; if not, the routine exits without changing the carbon layer settings. |
| 2. open input file | Opens `carbon_layers.prt` on unit 107 and stops if the open fails, because the settings cannot be read without the file. |
| 3. read title line | Reads the first record into `titldum`, capturing the title line and checking for read errors before continuing. |
| 4. read header line | Reads the second record into `header`, skipping the free-text header line and stopping on a read error. |
| 5. read layer count | Reads the third record into `n_lyr`, which is the requested number of soil layers for carbon output. |
| 6. validate count | Rejects values less than 1, writes a diagnostic to unit 9001, and leaves the module default unchanged. |
| 7. store explicit setting | Copies the valid layer count into `cb_n_layers` and marks `cb_n_layers_explicit` true so later code knows the value came from this file. |
| 8. close and return | Closes unit 107 and returns to the caller after either a successful update or an early exit path. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:carbon_module] | `cb_n_layers, cb_n_layers_explicit` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cb_n_layers` | When `carbon_layers.prt` exists, opens successfully, and its third record supplies `n_lyr >= 1`. | `cb_n_layers` is replaced with the layer count read from `carbon_layers.prt`, so downstream carbon output routines use that explicit number of soil layers instead of the fallback default. |
| `cb_n_layers_explicit` | When `carbon_layers.prt` exists, opens successfully, and `n_lyr >= 1` is read without error. | `cb_n_layers_explicit` is set true to record that the layer-count setting was provided directly by the optional carbon layers file. |

## File I/O

<!-- facts:io -->


## Lineage

This procedure was added in commit bc7755a as part of the carbon-subsystem refactor. The diff shows a new optional reader for `carbon_layers.prt` that uses `inquire`, reads a title, header, and layer count, validates `n_lyr >= 1`, and sets `cb_n_layers` plus `cb_n_layers_explicit`; no later lineage change was resolved for this file in the provided evidence.

- Introduced optional file-based carbon layer configuration through `carbon_layers.prt`, replacing any need for a fixed layer count in `file.cio` and making the layer count explicit when supplied.
- Added validation and fallback behavior: invalid or missing input leaves the default `cb_n_layers` in place and avoids changing `cb_n_layers_explicit`.
- Created the `cb_n_layers_explicit` flag so downstream carbon-output code can detect whether the layer count was user-specified.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'carbon_layers_read' has no extracted documentation comment.
