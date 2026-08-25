---
kind: procedure
symbol: hydcsout_conc_mass
title: hydcsout_conc_mass
status: filled
source_hash: c4792e724908ca15
version_label: SWAT+ 62.0.0
args:
  vol_m3: '`in` argument of type `real`.'
  hydcs1: '`in` argument of type `type(constituent_mass)`.'
  hydcs2: '`out` argument of type `type(constituent_mass)`.'
locals:
  ipest: Local variable of type `integer`.
  ipath: Local variable of type `integer`.
  ihmet: Local variable of type `integer`.
  isalt: Local variable of type `integer`.
  ics: Local variable of type `integer`.
---

<!-- facts:header -->

Converts a constituent-mass hydrograph from concentration (ppm) to mass (kg) using a water volume: mass = vol_m3·conc/1000, over every simulated constituent.

## Bottom Line

`hydcsout_conc_mass` allocates the output record's constituent arrays to the simulated counts and, for each pesticide, pathogen, heavy metal, salt, and other constituent, computes `vol_m3 · concentration / 1000` to convert ppm to kilograms.

It is the constituent-hydrograph analogue of `hyd_convert_conc_to_mass`, turning concentrations into transported masses for a given water volume.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called along the constituent routing path when a concentration hydrograph must be expressed as mass for a known water volume.

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
- warning: missing_doc: Procedure 'constituent_mass_module::hydcsout_conc_mass' has no extracted documentation comment.
