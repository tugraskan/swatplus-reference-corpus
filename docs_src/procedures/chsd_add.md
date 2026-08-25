---
kind: procedure
symbol: chsd_add
title: chsd_add
status: filled
source_hash: 2fd540cc5824c8be
version_label: SWAT+ 62.0.0
args:
  cho1: The first `sd_ch_output` operand (intent(in)).
  cho2: The second `sd_ch_output` operand (intent(in)).
locals:
  cho3: 'Result variable: the `sd_ch_output` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field addition of two `sd_ch_output` records, defined in `sd_channel_module` and used to accumulate `sd_ch_output` state.

## Bottom Line

`chsd_add` returns a new `sd_ch_output` record whose fields are the field-by-field sum of its two inputs. All 23 of the record's 26 value fields are combined with `+`. 3 fields are carried through unchanged rather than combined: `width`, `depth`, `slope`.

This is one of the small arithmetic helpers `sd_channel_module` defines for the `sd_ch_output` derived type. SWAT+ output and routing code calls it to keep `sd_ch_output` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`chsd_add` is a pure, side-effect-free helper in `sd_channel_module`; it only computes a new `sd_ch_output` value from its arguments and does no I/O. It runs wherever `sd_ch_output` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'sd_channel_module::chsd_add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
