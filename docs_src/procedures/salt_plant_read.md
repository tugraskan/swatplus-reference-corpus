---
kind: procedure
symbol: salt_plant_read
title: salt_plant_read
status: filled
source_hash: d694ee672e37a98a
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary 80-character title/label read from the first line of `salt_plants`; it
    is consumed and not otherwise used in this routine.
  header: Scratch 80-character header string used to skip or capture section headings in `salt_plants`
    before reading the numeric data that follows.
  plant_name: Temporary 12-character plant identifier read with each plant parameter row;
    it lets the routine consume the plant name while storing only the numeric `a` and `b`
    coefficients.
  iplant: Loop index that walks through the plant-parameter records from 1 to `db_mx%plantparm`,
    providing the array subscript for `salt_stress_a` and `salt_stress_b`.
  i_exist: Logical file-existence flag set by `inquire`; it controls whether the routine opens
    and reads `salt_plants` or skips the entire load when the file is absent.
uses:
  constituent_mass_module: This imported module is present in the routine's dependency set,
    so it is part of the shared model state the subroutine compiles against. The packet does
    not resolve any specific symbols from it for this routine, so no concrete component usage
    can be claimed from the evidence provided.
  input_file_module: This module is listed among the routine's dependencies, indicating file-configuration
    state is available through the shared input-file infrastructure. The source packet does
    not resolve a concrete symbol from it here, so its role can only be stated at the module
    level.
  maximum_data_module: '`db_mx%plantparm` supplies the number of plant parameter records to
    allocate and read. The routine sizes `salt_stress_a` and `salt_stress_b` from this value
    and then loops exactly that many times, so the maximum-data setting determines how many
    rows are loaded from `salt_plants`.'
  salt_data_module: '`salt_data_module` holds every destination that this reader populates:
    the TDS-to-EC factor, the salt simulation flag, soil-type selector, salt-effect selector,
    and the allocatable per-plant stress arrays. Without this shared module, the loaded plant-salt
    settings would not persist for later salt-growth calculations.'
---

<!-- facts:header -->

Reads plant salinity tolerance settings from `salt_plants` and loads the per-plant `a`/`b` stress parameters into shared salt-data arrays.

## Bottom Line

`salt_plant_read` is a file reader for the plant salinity-tolerance input table. If `salt_plants` exists, it opens the file, skips header and description lines, reads the TDS-to-EC conversion factor plus salt simulation settings, then loads one `salt_stress_a` and `salt_stress_b` pair for each plant defined by `db_mx%plantparm`.

The routine matters because these values drive later salt-stress calculations in the model. It populates shared state in `salt_data_module`, so downstream salt-growth logic can use the configured simulation flag, soil type, stress method, conversion factor, and plant-specific response parameters.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model's input-reading phase, after `proc_read` reaches the salt-specific section and before later salt routines use the loaded parameters. Its results feed downstream salinity-stress behavior by establishing the shared settings and per-plant coefficients needed for plant-growth salt response calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Test whether the plant-salt input file exists | The routine uses `inquire(file="salt_plants", exist=i_exist)` to detect whether the plant-salt table is available. Only when `i_exist` is true does it proceed to open and read the file. |
| 2. Open `salt_plants` and read the first title line | It opens unit 107 on `salt_plants` and reads the first record into `titldum`, consuming the file's leading title or banner line. |
| 3. Read the conversion-factor heading and value | The routine reads a header line into `header`, then reads `salt_tds_ec` from the next record so the model has the TDS-to-EC conversion factor used by salt calculations. |
| 4. Skip separator lines and read salt-control flags | It skips one blank line, then reads `salt_tol_sim`, `salt_soil_type`, and `salt_effect` from successive records to configure whether salt stress is simulated and how it is applied. |
| 5. Skip remaining pre-table lines and capture the table header | The routine advances through four additional unused records and then reads a header line into `header` so the file position is aligned with the plant-parameter table. |
| 6. Allocate per-plant stress arrays sized by plant count | It allocates `salt_stress_a` and `salt_stress_b` with length `db_mx%plantparm`, initializing both arrays to zero so every plant slot starts from a known state. |
| 7. Read each plant's salinity coefficients | A loop over `iplant = 1, db_mx%plantparm` reads each plant name and its `salt_stress_a` and `salt_stress_b` coefficients, storing the numerical parameters in the shared arrays. |
| 8. Close the input file | After the table has been loaded, the routine closes unit 107 to finish the `salt_plants` file session cleanly. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `use constituent_mass_module` |  |
| [sym:input_file_module] | `use input_file_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantparm` |
| [sym:salt_data_module] | `salt_stress_a, salt_stress_b, salt_tds_ec, salt_tol_sim, salt_soil_type, salt_effect` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `salt_plant_read`. The initial add in `df07e3f` created the routine to read `salt_plants`, allocate the salinity arrays, and load per-plant coefficients. `35b029c` made only formatting/whitespace adjustments in this file. `39fabde` initialized the local character variables and loop index, added `source=0.` to the allocations, and retained the same read logic; `2ee1889` then removed the unused `isalt` local variable.

- df07e3f introduced the full `salt_plant_read` implementation for opening `salt_plants`, reading shared salt settings, allocating `salt_stress_a`/`salt_stress_b`, and loading each plant record.
- 35b029c made no behavioral change in the routine; the diff only adjusted spacing and end-of-file formatting.
- 39fabde changed local initialization and array allocation so the character buffers and loop variables start in known states and the allocated stress arrays are zero-filled.
- 2ee1889 removed the unused `isalt` declaration, leaving runtime behavior unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_plant_read' has no extracted documentation comment.
- algorithm_steps revised: collapsed the original four-step draft into eight source-backed steps to reflect the actual open/read/skip/allocate/loop/close sequence in the source.
