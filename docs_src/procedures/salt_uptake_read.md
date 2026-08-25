---
kind: procedure
symbol: salt_uptake_read
title: salt_uptake_read
status: filled
source_hash: d4eb607273aac3b7
version_label: SWAT+ 62.0.0
locals:
  header: Reusable character buffer for the three header lines at the top of the `salt_uptake`
    file; the routine reads them and discards the contents.
  name: Holds the plant-community label read from each data row, while the numeric salt-uptake
    values for that row are stored into `salt_uptake_kg(i,j)`.
  i_exist: Logical file-existence test from `inquire(file='salt_uptake',exist=i_exist)`, used
    to decide whether to enable salt uptake and read the file.
  eof: Initialized to zero but not used in the extracted body; it appears to be a leftover
    end-of-file counter.
  i: Loop index for plant communities; each iteration reads one plant-community uptake record
    into row `i` of `salt_uptake_kg`.
  j: Loop index for salt ions within each plant-community row; used in the implied-DO list
    that fills the uptake table.
uses:
  basin_module: '`db_mx%plantparm` supplies the number of plant communities, which sets the
    number of rows the routine allocates and reads into `salt_uptake_kg`.'
  input_file_module: This module is imported by the routine, but no specific resolved symbols
    from it were identified in the extracted evidence; it likely belongs to the broader input-reading
    context used by `proc_read`.
  climate_module: This module is imported by the routine, but no specific resolved symbols
    from it were identified in the extracted evidence; it matters because the routine runs
    during the shared model input phase alongside other climate-related readers.
  time_module: This module is imported by the routine, but no specific resolved symbols from
    it were identified in the extracted evidence; it matters because the routine is part of
    the model startup/input sequence rather than a time-step calculation.
  maximum_data_module: '`db_mx%plantparm` determines the allocation size and loop bound for
    the plant-community table read from `salt_uptake`.'
  constituent_mass_module: '`cs_db%num_salts` controls whether the routine does anything at
    all and how many salt-mass columns are read per plant community.'
  hydrograph_module: This module is imported by the routine, but no specific resolved symbols
    from it were identified in the extracted evidence; it is part of the wider process-data
    environment that the salt reader shares with other setup routines.
  salt_module: '`salt_uptake_on` is the feature flag that this reader turns on when the file
    exists, and `salt_uptake_kg` is the allocatable table populated from the file.'
---

<!-- facts:header -->

Reads the optional `salt_uptake` input file and loads salt-uptake masses for each plant community and salt ion. It also turns on the salt-uptake flag when the file is present and salts are being simulated.

## Bottom Line

`salt_uptake_read` is a setup routine. When the simulation includes salts (`cs_db%num_salts > 0`) and a `salt_uptake` file exists, it opens that file, skips three header lines, allocates the `salt_uptake_kg` table, and reads one row per plant community. It also sets `salt_uptake_on` so later model code can apply the loaded uptake values.

If no salts are being simulated, or the `salt_uptake` file is absent, the routine leaves the salt-uptake feature off and does not populate the uptake table. The loaded array is later used by salt-related crop/process calculations through `salt_module`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model input processing, when `proc_read` is loading salt-related configuration before simulation begins. It depends on database sizes such as `cs_db%num_salts` and `db_mx%plantparm`, and its results feed later salt-uptake behavior by setting `salt_uptake_on` and populating `salt_uptake_kg`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Check whether any salts are being simulated. If `cs_db%num_salts` is zero, the routine skips all salt-uptake file handling and returns with uptake disabled. |
| 2. if | Probe for the presence of the `salt_uptake` file and only continue with reading if the file exists. |
| 3. io | Turn on the salt-uptake feature flag and open the `salt_uptake` input file on unit 5054 for reading. |
| 4. io | Read and discard the first header line from `salt_uptake`. |
| 5. io | Read and discard the second header line from `salt_uptake`. |
| 6. io | Read and discard the third header line from `salt_uptake`, finishing the header section. |
| 7. allocation | Allocate `salt_uptake_kg(db_mx%plantparm,cs_db%num_salts)` and initialize it to zero before any row data are read. |
| 8. loop | Loop over every plant community row expected in the file, using `db_mx%plantparm` as the upper bound. |
| 9. io | Read one plant-community name plus the salt-uptake values for all salts into the current row of `salt_uptake_kg`. |
| 10. io | Close the `salt_uptake` file after all rows have been read. |
| 11. return | Return to the caller after leaving the salt-uptake flag and table in their loaded state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` | `db_mx%plantparm` |
| [sym:input_file_module] | `input_file_module` |  |
| [sym:climate_module] | `climate_module` |  |
| [sym:time_module] | `time_module` |  |
| [sym:maximum_data_module] | `maximum_data_module` | `db_mx%plantparm` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |
| [sym:hydrograph_module] | `hydrograph_module` |  |
| [sym:salt_module] | `salt_uptake_kg, salt_uptake_on` |  |
| [sym:maximum_data_module] | `maximum_data_module` | `db_mx%plantparm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `salt_uptake_on` | When `cs_db%num_salts > 0` and the `salt_uptake` file exists. | Sets `salt_uptake_on` from 0 to 1 so the model knows salt uptake is available and should be applied later. |
| `salt_uptake_kg` | When the `salt_uptake` file exists and the routine enters the read path. | Allocates `salt_uptake_kg` to `(db_mx%plantparm, cs_db%num_salts)` and fills it with the values read from the file, replacing any prior contents. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits affected `salt_uptake_read`. The initial addition in `df07e3f` created the subroutine, its file-existence check, the `salt_uptake` read path, the allocation of `salt_uptake_kg`, and the `salt_uptake_on` flag. `35b029c` made a formatting-only end-of-file change. `94b6dec` preserved the same logic while bringing in the source from bitbucket. `39fabde` initialized local variables and changed the allocation to use `source = 0.` before also zeroing `salt_uptake_kg` explicitly.

- df07e3f added the salt-uptake reader, including the `cs_db%num_salts` guard, `inquire`/`open`/`read`/`close` sequence, allocation of `salt_uptake_kg`, and setting `salt_uptake_on` when the file exists.
- 35b029c changed only the file ending formatting and did not alter runtime behavior.
- 94b6dec imported the same salt-uptake read logic from bitbucket without changing the behavior visible in the diff.
- 39fabde initialized local variables and changed the allocation to `allocate (salt_uptake_kg(...), source = 0.)`, while keeping the explicit zeroing of `salt_uptake_kg` after allocation.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_uptake_read' has no extracted documentation comment.
- algorithm_steps revised: collapsed the separate open/read actions into a clearer step sequence using only the visible source lines; line 34 is included with the feature-flag step.
