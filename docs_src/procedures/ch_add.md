---
kind: procedure
symbol: ch_add
title: ch_add
status: filled
source_hash: 88a5389f99dc54d7
version_label: SWAT+ 62.0.0
args:
  cho1: The first `ch_output` operand (intent(in)).
  cho2: The second `ch_output` operand (intent(in)).
locals:
  cho3: 'Result variable: the `ch_output` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field addition of two `ch_output` records, defined in `channel_module` and used to accumulate `ch_output` state.

## Bottom Line

`ch_add` returns a new `ch_output` record whose fields are the field-by-field sum of its two inputs. All 58 of the record's 58 value fields are combined with `+`.

This is one of the small arithmetic helpers `channel_module` defines for the `ch_output` derived type. SWAT+ output and routing code calls it to keep `ch_output` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ch_add` is a pure, side-effect-free helper in `channel_module`; it only computes a new `ch_output` value from its arguments and does no I/O. It runs wherever `ch_output` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `channel_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'channel_module::ch_add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
