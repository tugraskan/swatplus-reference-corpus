---
kind: procedure
symbol: mallout_add
title: mallout_add
status: filled
source_hash: 949bb439d8b4ce8a
version_label: SWAT+ 62.0.0
args:
  mallo1: The first `source_manure_output` operand (intent(in)).
  mallo2: The second `source_manure_output` operand (intent(in)).
locals:
  mallo3: 'Result variable: the `source_manure_output` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Field-by-field addition of two `source_manure_output` records, defined in `manure_allocation_module` and used to accumulate `source_manure_output` state.

## Bottom Line

`mallout_add` returns a new `source_manure_output` record whose fields are the field-by-field sum of its two inputs. All 2 of the record's 3 value fields are combined with `+`. 1 field is carried through unchanged rather than combined: `stor`.

This is one of the small arithmetic helpers `manure_allocation_module` defines for the `source_manure_output` derived type. SWAT+ output and routing code calls it to keep `source_manure_output` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`mallout_add` is a pure, side-effect-free helper in `manure_allocation_module`; it only computes a new `source_manure_output` value from its arguments and does no I/O. It runs wherever `source_manure_output` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `manure_allocation_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'manure_allocation_module::mallout_add' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
