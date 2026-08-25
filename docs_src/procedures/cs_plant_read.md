---
kind: procedure
symbol: cs_plant_read
title: cs_plant_read
status: filled
source_hash: 1a4e78d727b4922a
version_label: SWAT+ 62.0.0
locals:
  titldum: Holds the first line/title record read from `cs_plants_boron`; the routine consumes
    it as a header line before the actual parameter records.
  header: Temporary buffer for the four subsequent header/comment lines in `cs_plants_boron`;
    each `read(107,*) header` skips one non-data record.
  plant_name: Temporary plant-name field read with each coefficient row; it identifies the
    row but is not stored beyond the current loop iteration.
  iplant: Loop index over the plant parameter entries; it is used to step through `bor_stress_a`
    and `bor_stress_b` from 1 to `db_mx%plantparm`.
  i_exist: Logical file-existence flag set by `inquire`; it determines whether `cs_plants_boron`
    is opened and read at all.
uses:
  constituent_mass_module: This module is imported by `cs_plant_read`, so it is part of the
    routine’s shared context even though no specific symbols from it were extracted here;
    it likely contributes constituent/mass-related state used elsewhere in the same process.
  input_file_module: This module is also imported into the routine’s scope, indicating dependence
    on the shared input-file infrastructure used across SWAT+ readers, even though no named
    symbols from it were extracted in this snippet.
  maximum_data_module: '`db_mx%plantparm` supplies the plant count used to allocate `bor_stress_a`
    and `bor_stress_b` and to bound the read loop, so this maximum-data metadata directly
    controls how much plant boron data is loaded.'
  cs_data_module: '`bor_tol_sim`, `bor_stress_a`, and `bor_stress_b` are the shared boron-stress
    settings populated here; later growth or stress calculations depend on these module variables
    being initialized by this reader.'
---

<!-- facts:header -->

Reads plant boron-tolerance settings from `cs_plants_boron` and loads the per-plant stress coefficients used by the constituent-stress routines.

## Bottom Line

`cs_plant_read` is a small file-reader that checks whether the `cs_plants_boron` input file exists, opens it, skips the title and header records, reads the global boron simulation flag, and then loads one pair of boron stress coefficients for each plant entry into `bor_stress_a` and `bor_stress_b`.

This matters because later plant growth calculations can use those coefficients, along with `bor_tol_sim`, to control whether and how boron stress affects plant growth. The routine sizes its storage from `db_mx%plantparm`, so it depends on the plant-count metadata already being set by the broader input-reading workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model’s input-reading phase, after `proc_read` has already begun loading process-related data and specifically calls `cs_plant_read`. Its output initializes shared boron-stress settings that later plant-growth or constituent-stress behavior can use during simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the boron plant file exists | The routine issues an `inquire` on `cs_plants_boron` and only proceeds if `i_exist` is true, so the read is conditional on the file being present. |
| 2. Open the boron plant file and consume the title line | It opens `cs_plants_boron` on unit 107 and reads the first record into `titldum`, using that line as a title/header record. |
| 3. Skip fixed header records and read the simulation flag | The routine discards one blank/unused record, reads `bor_tol_sim`, and then reads four more header records into `header` to position the file at the data table. |
| 4. Allocate boron stress storage sized to the plant database | It allocates `bor_stress_a` and `bor_stress_b` with length `db_mx%plantparm`, initializing both arrays to zero. |
| 5. Load one coefficient pair per plant | A loop over `iplant` reads each plant row, capturing the plant name and storing the two boron stress coefficients into the corresponding array elements. |
| 6. Close the input file and return | After the loop finishes, the routine closes unit 107 and exits, leaving the shared boron settings ready for later use. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `constituent_mass_module` | `none resolved` |
| [sym:input_file_module] | `input_file_module` | `none resolved` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantparm` |
| [sym:cs_data_module] | `bor_stress_a, bor_stress_b, bor_tol_sim` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved lineage commits affect `cs_plant_read`. The initial add in `df07e3f` created the routine to read `cs_plants_boron`, set `bor_tol_sim`, allocate the boron stress arrays, and load per-plant coefficients. `35b029c` made only whitespace/layout adjustments and did not change behavior. `94b6dec` introduced the file-reading routine into the current source tree with the same logic. `39fabde` changed local initialization and switched the array allocations to zero-initialized `allocate(..., source = 0.)`. `2ee1889` only removed a trailing blank line.

- `df07e3f` introduced the boron-plant reader, including the file open/read sequence, `bor_tol_sim` assignment, array allocation, coefficient loop, and file close.
- `39fabde` initialized `titldum`, `header`, `plant_name`, and `iplant`, and changed the boron stress allocations to zero-fill the arrays at allocation time.
- `94b6dec` added the same `cs_plant_read` logic to the imported source snapshot, establishing the routine structure used later.
- `35b029c` and `2ee1889` were non-functional formatting cleanups; they did not alter the routine’s behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cs_plant_read' has no extracted documentation comment.
