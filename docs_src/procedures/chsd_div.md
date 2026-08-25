---
kind: procedure
symbol: chsd_div
title: chsd_div
status: filled
source_hash: cac2815c8ca81ac0
version_label: SWAT+ 62.0.0
args:
  ch1: The first `sd_ch_output` operand (intent(in)).
  const: Scalar applied to each field of the `sd_ch_output` record.
locals:
  ch2: 'Result variable: the `sd_ch_output` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Divides a `sd_ch_output` record by a scalar (`const`) field by field, defined in `sd_channel_module` and used to average accumulated `sd_ch_output` state.

## Bottom Line

`chsd_div` returns a new `sd_ch_output` record whose fields are its input's fields each divided by the scalar `const`. 9 of the 26 fields are divided by `const`: `flo_in`, `aqu_in`, `flo`, `peakr`, `sed_stor`, `p_tot`, `n_tot`, `dep_bf`, `velav_bf`. The other 17 fields are copied through unchanged (not scaled); these are the flux totals that are not averaged.

This is one of the small arithmetic helpers `sd_channel_module` defines for the `sd_ch_output` derived type. SWAT+ output and routing code calls it to keep `sd_ch_output` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`chsd_div` is a pure, side-effect-free helper in `sd_channel_module`; it only computes a new `sd_ch_output` value from its arguments and does no I/O. It runs wherever `sd_ch_output` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `sd_channel_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sd_channel_module::chsd_div' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
