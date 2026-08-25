---
kind: procedure
symbol: hydcsout_mult_const
title: hydcsout_mult_const
status: filled
source_hash: e086715fbe134fb5
version_label: SWAT+ 62.0.0
args:
  hydcs1: '`in` argument of type `type(constituent_mass)`.'
  const: '`in` argument of type `real`.'
locals:
  hydcs2: 'Result variable: the `type(constituent_mass)` value the function returns.'
  ipest: Local variable of type `integer`.
  ipath: Local variable of type `integer`.
  ihmet: Local variable of type `integer`.
  isalt: Local variable of type `integer`.
  ics: Local variable of type `integer`.
---

<!-- facts:header -->

Scales a constituent-mass hydrograph by a scalar constant, multiplying each pesticide/pathogen/metal/salt/cs element.

## Bottom Line

`hydcsout_mult_const` allocates the result's constituent arrays to the simulated counts, then multiplies each element of the input record's `pest`, `path`, `hmet`, `salt`, and `cs` arrays by the scalar `const`.

It is the scale-by-constant operator for the `constituent_mass` hydrograph, used for fraction/ratio scaling during routing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called (typically via `operator(*)`) wherever a constituent-mass hydrograph is scaled by a scalar.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. allocation | Executes `allocate (hydcs2%pest(cs_db%num_pests), source = 0.)`. |
| 2. allocation | Executes `allocate (hydcs2%path(cs_db%num_paths), source = 0.)`. |
| 3. allocation | Executes `allocate (hydcs2%hmet(cs_db%num_metals), source = 0.)`. |
| 4. allocation | Executes `allocate (hydcs2%salt(cs_db%num_salts), source = 0.)`. |
| 5. allocation | Executes `allocate (hydcs2%cs(cs_db%num_cs), source = 0.)`. |
| 6. loop | Loop over `do ipest = 1, cs_db%num_pests`. |
| 7. loop | Loop over `do ipath = 1, cs_db%num_paths`. |
| 8. loop | Loop over `do ihmet = 1, cs_db%num_metals`. |
| 9. loop | Loop over `do isalt = 1, cs_db%num_salts`. |
| 10. loop | Loop over `do ics = 1, cs_db%num_cs`. |
| 11. return | Executes `return`. |

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `constituent_mass_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'constituent_mass_module::hydcsout_mult_const' has no extracted documentation comment.
