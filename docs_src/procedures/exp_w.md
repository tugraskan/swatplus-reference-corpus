---
kind: procedure
symbol: exp_w
title: exp_w
status: filled
source_hash: 033cf8f59b7d9405
version_label: SWAT+ 62.0.0
args:
  y: '`in` argument of type `real`.'
locals:
  err_output: Local variable of type `logical`.
uses:
  iso_fortran_env: Uses module `iso_fortran_env`.
  ifcore: Uses module `ifcore`.
---

<!-- facts:header -->

Safe exponential: returns `exp(y)`, but 0 when `y < -80` to avoid floating-point underflow (with optional diagnostic backtrace).

## Bottom Line

`exp_w` wraps the intrinsic `exp` to guard against severe underflow: for `y < -80` (where `exp(y) < ~2e-35`) it returns 0 instead of risking a denormal or trap, and can optionally emit a warning plus a compiler-specific stack trace. The diagnostic flag is hard-coded off for production.

It is used wherever the model exponentiates a possibly very negative argument and wants a robust zero rather than an underflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

A general-purpose numeric helper in `utils`; called from growth, decay, and other routines that evaluate `exp` of large-magnitude negative arguments.

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
| `ifcore` | `tracebackqq` | `tracebackqq` |

## Local Variables

<!-- facts:locals -->

## State Changes

*No state changes recorded.*

## File I/O

<!-- facts:io -->


## Lineage

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `utils.f90`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'utils::exp_w' has no extracted documentation comment.
