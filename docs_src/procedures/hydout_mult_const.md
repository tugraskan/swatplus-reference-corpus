---
kind: procedure
symbol: hydout_mult_const
title: hydout_mult_const
status: filled
source_hash: cfbbc5e065b87bb4
version_label: SWAT+ 62.0.0
args:
  hyd1: The first `hyd_output` operand (intent(in)).
  const: Scalar applied to each field of the `hyd_output` record.
locals:
  hyd2: 'Result variable: the `hyd_output` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Scales a `hyd_output` record by a scalar (`const`) field by field, defined in `hydrograph_module`.

## Bottom Line

`hydout_mult_const` returns a new `hyd_output` record whose fields are its input's fields each multiplied by the scalar `const`. 17 of the 19 fields are multiplied by `const`: `flo`, `sed`, `orgn`, `sedp`, `no3`, `solp`, `chla`, `nh3`, `no2`, `cbod`, `dox`, `san`, … (17 total). The other 2 fields are copied through unchanged (not scaled).

This is one of the small arithmetic helpers `hydrograph_module` defines for the `hyd_output` derived type. SWAT+ output and routing code calls it to keep `hyd_output` records scaled — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hydout_mult_const` is a pure, side-effect-free helper in `hydrograph_module`; it only computes a new `hyd_output` value from its arguments and does no I/O. It runs wherever `hyd_output` records are scaled, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Review source manually | No major control-flow steps were extracted automatically. |

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `hydrograph_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hydrograph_module::hydout_mult_const' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
