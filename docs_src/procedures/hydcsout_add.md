---
kind: procedure
symbol: hydcsout_add
title: hydcsout_add
status: filled
source_hash: 74858cddee845c4c
version_label: SWAT+ 62.0.0
args:
  hydcs1: '`in` argument of type `type(constituent_mass)`.'
  hydcs2: '`in` argument of type `type(constituent_mass)`.'
locals:
  hydcs3: 'Result variable: the `type(constituent_mass)` value the function returns.'
  ipest: Local variable of type `integer`.
  ipath: Local variable of type `integer`.
  ihmet: Local variable of type `integer`.
  isalt: Local variable of type `integer`.
  ics: Local variable of type `integer`.
---

<!-- facts:header -->

Adds two constituent-mass hydrographs, summing each pesticide, pathogen, heavy-metal, salt, and other-constituent element by element.

## Bottom Line

`hydcsout_add` allocates the result's `pest`, `path`, `hmet`, `salt`, and `cs` arrays to the simulated constituent counts (`cs_db%num_*`), then loops over each count summing the corresponding elements of the two input records.

It is the addition operator for the `constituent_mass` hydrograph — used to accumulate constituent loads across incoming hydrographs and reporting periods.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called (typically via `operator(+)`) wherever two constituent-mass hydrographs are combined; sizes itself from the simulated constituent counts.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. allocation | Executes `allocate (hydcs3%pest(cs_db%num_pests), source = 0.)`. |
| 2. allocation | Executes `allocate (hydcs3%path(cs_db%num_paths), source = 0.)`. |
| 3. allocation | Executes `allocate (hydcs3%hmet(cs_db%num_metals), source = 0.)`. |
| 4. allocation | Executes `allocate (hydcs3%salt(cs_db%num_salts), source = 0.)`. |
| 5. allocation | Executes `allocate (hydcs3%cs(cs_db%num_cs), source = 0.)`. |
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
- warning: missing_doc: Procedure 'constituent_mass_module::hydcsout_add' has no extracted documentation comment.
