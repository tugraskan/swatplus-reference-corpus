---
kind: procedure
symbol: cb_write_wide_header
title: cb_write_wide_header
status: filled
source_hash: 81653492ab2165eb
version_label: SWAT+ 62.0.0
args:
  unit_no: '`in` argument of type `integer`.'
  var_names: '`in` argument of type `character(len=*)`.'
  is_csv: '`in` argument of type `logical`.'
locals:
  tag: Local variable of type `character(len=32)`.
  i: Local variable of type `integer`.
  k: Local variable of type `integer`.
---

<!-- facts:header -->

Writes the column-header line for wide per-layer carbon files: id columns, `depth_lyr1..N`, then each variable name suffixed `_lyr1..N`.

## Bottom Line

`cb_write_wide_header` emits the header for carbon files that report every variable across `cb_n_layers` soil layers. After the identity columns it writes `depth_lyrK` for each layer, then, for each variable, `<var>_lyrK` for each layer, in CSV or fixed-width form. The caller has already written the banner row.

It is a formatting helper for the wide-format legacy carbon diagnostic files.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by the carbon output setup when opening a wide per-layer carbon file.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select output conditions | Executes the source at the referenced lines. |
| 2. Loop over output items | Executes the source at the referenced lines. |
| 3. Write output records | Executes the source at the referenced lines. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `carbon_module.f90`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'carbon_module::cb_write_wide_header' has no extracted documentation comment.
