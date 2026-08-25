---
kind: procedure
symbol: cs_uptake_read
title: cs_uptake_read
status: filled
source_hash: d7d1d0cb7de24d3c
version_label: SWAT+ 62.0.0
locals:
  header: Temporary character buffer used to consume and discard the three header lines at
    the top of the `cs_uptake` file.
  name: Temporary character buffer that receives the plant-community name token on each data
    row before the uptake values are read.
  i_exist: Logical flag set by `inquire(file='cs_uptake',exist=i_exist)` to indicate whether
    the `cs_uptake` input file is available.
  eof: Declared and initialized but not used in the shown routine body; it appears to be a
    leftover end-of-file counter.
  i: Loop index over plant communities when reading one uptake row per community into `cs_uptake_kg`.
  j: Inner loop index over constituent columns while reading each community's uptake values.
uses:
  basin_module: '`db_mx%plantparm` supplies the number of plant communities, which controls
    the row count of the uptake table that this routine allocates and reads.'
  input_file_module: This module is imported by the routine, but the extracted source does
    not show any specific symbol from it being referenced here; it may matter through shared
    input-file conventions, so the exact dependency is uncertain from the provided snippet.
  climate_module: This module is imported but no resolved symbol from it appears in the routine
    body; it is likely part of the broader setup environment, but the provided evidence does
    not show a direct use here.
  time_module: This module is imported but no resolved symbol from it appears in the routine
    body; it may be part of the shared model state, but the snippet does not show a direct
    dependency.
  maximum_data_module: '`db_mx%plantparm` sets the upper bound for the loop and allocation
    dimension, so it determines how many plant-community uptake records are read.'
  constituent_mass_module: '`cs_db%num_cs` tells the routine how many constituent columns
    exist. It is the guard for running the reader at all and the column count used when allocating
    and reading `cs_uptake_kg`.'
  hydrograph_module: This module is imported by the routine, but the extracted source does
    not show any direct symbol use. It likely belongs to the shared SWAT+ execution context
    rather than affecting the file-read logic directly.
  cs_module: '`cs_uptake_on` is the feature flag this routine sets to 1 when the input file
    exists, and `cs_uptake_kg` is the allocatable table this routine fills with the file contents.'
---

<!-- facts:header -->

Reads the cs_uptake input table and loads plant-community constituent uptake masses into memory. It also turns the uptake feature on when the file exists and constituents are being simulated.

## Bottom Line

`cs_uptake_read` is a setup routine for constituent uptake by plant roots. When the simulation has one or more constituents (`cs_db%num_cs > 0`) and a `cs_uptake` file is present, it opens that file, skips three header lines, allocates `cs_uptake_kg`, and reads one row per plant community into the uptake table.

If no constituents are being simulated, or if the `cs_uptake` file is absent, the routine leaves uptake disabled. The rest of the model can then use `cs_uptake_on` as a switch and `cs_uptake_kg` as the lookup table for crop-root constituent uptake rates.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `proc_read`, after the earlier constituent-related read routines have established the constituent simulation setup. Its result matters later wherever the model needs to know whether constituent uptake is active and what uptake masses apply to each plant community.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Check whether any constituents are being simulated. If `cs_db%num_cs > 0`, the routine proceeds with uptake-file handling; otherwise it exits without changing uptake state. |
| 2. if | Test whether the `cs_uptake` file exists. Only when the file is present does the routine enable constituent uptake and read the table. |
| 3. io | Open the `cs_uptake` file on unit 5054 so the routine can read the uptake definitions from disk. |
| 4. io | Read and discard the first header line from `cs_uptake` into `header`. |
| 5. io | Read and discard the second header line from `cs_uptake` into `header`. |
| 6. io | Read and discard the third header line from `cs_uptake` into `header`. |
| 7. allocation | Allocate `cs_uptake_kg` with one row per plant community (`db_mx%plantparm`) and one column per constituent (`cs_db%num_cs`), initializing the array to zero. |
| 8. loop | Loop over every plant community so each row of the uptake table can be read from the file. |
| 9. io | Read one record per plant community: the community name plus the constituent uptake values that fill `cs_uptake_kg(i,j)`. |
| 10. io | Close the `cs_uptake` file after all rows have been loaded. |
| 11. return | Return to the caller after the file has been processed or skipped. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` | `db_mx%plantparm` |
| [sym:input_file_module] | `input_file_module` | `none resolved` |
| [sym:climate_module] | `climate_module` | `none resolved` |
| [sym:time_module] | `time_module` | `none resolved` |
| [sym:maximum_data_module] | `maximum_data_module` | `db_mx%plantparm` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |
| [sym:hydrograph_module] | `hydrograph_module` | `none resolved` |
| [sym:cs_module] | `cs_uptake_kg, cs_uptake_on` |  |
| [sym:maximum_data_module] | `maximum_data_module` | `db_mx%plantparm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_uptake_on` | When `cs_db%num_cs > 0` and the `cs_uptake` file exists. | Sets the uptake flag to 1 so later code knows the constituent-uptake feature is enabled for this simulation. |
| `cs_uptake_kg` | When `cs_db%num_cs > 0` and the `cs_uptake` file exists. | Allocates and fills the plant-community-by-constituent uptake matrix from the `cs_uptake` file; otherwise it is left unchanged by this routine. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage is resolved. The routine was introduced in df07e3f, and the later commits 94b6dec, 39fabde, and 2ee1889 changed only initialization and allocation details: 94b6dec brought in the routine with no behavioral changes beyond the new implementation; 39fabde switched local scalars to initialized declarations and changed the allocation to use `source = 0.`; 2ee1889 removed an unused `file` and `plnt_typ` declaration and kept the same file-read logic.

- 39fabde initialized local variables and changed the `cs_uptake_kg` allocation to use `source = 0.`, reducing dependence on separate post-allocation zeroing.
- 2ee1889 cleaned up unused local declarations (`file`, `plnt_typ`) and left the runtime behavior of the reader unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- info: weak_doc: Procedure 'cs_uptake_read' documentation is very short.
- algorithm_steps revised: kept the original 11-step flow but clarified each step in model terms using the visible source lines.
- `input_file_module`, `climate_module`, `time_module`, `hydrograph_module`, and `maximum_data_module` are imported in the source, but only `db_mx%plantparm` is directly referenced in the extracted snippet; the rest are documented as unresolved/uncertain imports rather than guessed symbols.
- `eof` is declared and initialized but not used in the shown body; this appears to be dead or leftover state in the provided source.
