---
kind: procedure
symbol: cb_write_flat_header
title: cb_write_flat_header
status: filled
source_hash: 47917b99132c24df
version_label: SWAT+ 62.0.0
args:
  unit_no: '`in` argument of type `integer`.'
  var_names: '`in` argument of type `character(len=*)`.'
  is_csv: '`in` argument of type `logical`.'
locals:
  tag: Local variable of type `character(len=32)`.
  i: Local variable of type `integer`.
---

<!-- facts:header -->

Writes the column-header line for non-layered carbon output files: the id columns followed by each variable name once (no `_lyr` suffix).

## Bottom Line

`cb_write_flat_header` emits the header row for carbon files that are not resolved by soil layer. It writes the identity columns (`jday,mon,day,yr,unit,gis_id,name`) then one column per variable name, in comma-separated form when `is_csv` is set and fixed-width otherwise.

It is a formatting helper for the legacy carbon diagnostic output files.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by the carbon output setup (via `carbon_legacy_open` / carbon writers) when opening a non-layered carbon file.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `is_csv`. |
| 2. io | Executes `write (unit_no, '(a)', advance='no') "jday,mon,day,yr,unit,gis_id,name"`. |
| 3. loop | Loop over `do i = 1, size(var_names)`. |
| 4. io | Executes `write (unit_no, '(a,a)', advance='no') ",", trim(var_names(i))`. |
| 5. io | Executes `write (unit_no, '(a)') ""`. |
| 6. else | Alternative branch taken when the preceding condition is false. |
| 7. io | Executes `write (unit_no, '(a)', advance='no') " jday mon day yr unit gis_id name "`. |
| 8. loop | Loop over `do i = 1, size(var_names)`. |
| 9. io | Executes `write (unit_no, '(1x,a22)', advance='no') tag`. |
| 10. io | Executes `write (unit_no, '(a)') ""`. |

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
- warning: missing_doc: Procedure 'carbon_module::cb_write_flat_header' has no extracted documentation comment.
