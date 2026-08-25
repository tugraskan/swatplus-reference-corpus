---
kind: procedure
symbol: aqupest_add_all
title: aqupest_add_all
status: filled
source_hash: ef574c0ec35a80e5
version_label: SWAT+ 62.0.0
args:
  aqu1: The first `aqu_pesticide_processes` operand (intent(in)).
  aqu2: The second `aqu_pesticide_processes` operand (intent(in)).
locals:
  aqu3: 'Result variable: the `aqu_pesticide_processes` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Field-by-field addition of two `aqu_pesticide_processes` records, defined in `aqu_pesticide_module` and used to accumulate `aqu_pesticide_processes` state.

## Bottom Line

`aqupest_add_all` returns a new `aqu_pesticide_processes` record whose fields are the field-by-field sum of its two inputs. All 9 of the record's 9 value fields are combined with `+`.

This is one of the small arithmetic helpers `aqu_pesticide_module` defines for the `aqu_pesticide_processes` derived type. SWAT+ output and routing code calls it to keep `aqu_pesticide_processes` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`aqupest_add_all` is a pure, side-effect-free helper in `aqu_pesticide_module`; it only computes a new `aqu_pesticide_processes` value from its arguments and does no I/O. It runs wherever `aqu_pesticide_processes` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `aqu_pesticide_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'aqu_pesticide_module::aqupest_add_all' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
