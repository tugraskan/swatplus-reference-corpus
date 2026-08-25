---
kind: procedure
symbol: cs_fert_read
title: cs_fert_read
status: filled
source_hash: 715a30bdcc15c424
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for the first line read from `fertilizer.frt_cs`; the
    routine reads it and discards it as a title line.
  header: Temporary character buffer for the second line read from `fertilizer.frt_cs`; the
    routine reads it and discards it as a header line.
  icsi: Loop index used to step through each fertilizer record in the file and assign it into
    `fert_cs(icsi)`.
  eof: I/O status code used on the initial reads to detect whether file input encountered
    an end-of-file or read error while skipping the header lines.
  i_exist: Logical file-existence test from `inquire`; it controls whether the routine opens
    and reads `fertilizer.frt_cs` at all.
uses:
  constituent_mass_module: This module owns the constituent-mass data domain that `cs_fert_read`
    is populating. Even though no specific candidate symbol was resolved to it in the extracted
    references, the fertilizer loading values loaded here are part of the constituent setup
    used by later constituent-mass calculations.
  input_file_module: This module is imported by the routine as part of the file-input infrastructure
    used across SWAT+ readers. It matters here because `cs_fert_read` participates in the
    shared input-reading phase that loads model configuration files before simulation use.
  maximum_data_module: '`db_mx%fertparm` supplies the number of fertilizer records to allocate
    and read. The routine uses that count to size `fert_cs` and to bound the `do icsi=1,db_mx%fertparm`
    read loop.'
  cs_module: '`fert_cs` is the shared allocatable array that receives each fertilizer record,
    and `fert_cs_flag` records that the fertilizer constituent table was successfully loaded
    so later routines can rely on it.'
---

<!-- facts:header -->

Reads the constituent fertilizer loading table from `fertilizer.frt_cs` and stores it in the shared fertilizer array. It also sets a flag so later constituent-mass routines know the fertilizer table is available.

## Bottom Line

This routine checks whether `fertilizer.frt_cs` exists, opens it, skips the title and header lines, allocates the shared fertilizer table to the number of fertilizer parameter records declared in `db_mx%fertparm`, and then reads each fertilizer record into `fert_cs(icsi)`.

When the file is present, it marks `fert_cs_flag = 1` so downstream constituent-mass code can use the loaded fertilizer loading values. If the file is missing, the routine does nothing and leaves the shared fertilizer data unset.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the shared input-reading stage, after `proc_read` has started loading constituent and other model databases. Its result is the fertilizer constituent table and availability flag used later by constituent-mass processing when fertilizer properties are needed.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Checks whether `fertilizer.frt_cs` exists. The rest of the routine only runs when that input file is present. |
| 2. io | Opens `fertilizer.frt_cs` on unit 107 so the routine can read fertilizer constituent records from the file. |
| 3. io | Reads and discards the first line from `fertilizer.frt_cs` into `titldum`, treating it as a title line. |
| 4. io | Reads and discards the second line from `fertilizer.frt_cs` into `header`, treating it as a header line. |
| 5. allocation | Allocates the shared fertilizer constituent array `fert_cs` to the size given by `db_mx%fertparm`. |
| 6. loop | Loops from the first fertilizer record through `db_mx%fertparm`, reading each record in order. |
| 7. io | Reads one fertilizer constituent record from `fertilizer.frt_cs` into `fert_cs(icsi)` on each loop iteration. |
| 8. io | Closes unit 107 after the fertilizer file has been fully read. |
| 9. return | Returns to the caller after the fertilizer table has been loaded or skipped. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `constituent_mass_module` |  |
| [sym:input_file_module] | `input_file_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%fertparm` |
| [sym:cs_module] | `fert_cs, fert_cs_flag` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `fert_cs_flag` | When `fertilizer.frt_cs` exists and is opened successfully. | `fert_cs_flag` is set to 1 to mark that the constituent fertilizer table was loaded into the shared `fert_cs` array and is available for later use. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show the routine was introduced in `df07e3f` with the full file reader logic. `39fabde` only initialized local variables to empty/zero values, and `bd18ad4` later commented out unused `fert_name` and removed unused `imax`; the file-reading behavior itself did not change. `c7c8e22` and `35b029c` preserved the same reader logic while importing the file into the repository and fixing formatting.

- df07e3f added `cs_fert_read` as a new reader for `fertilizer.frt_cs`, including existence checking, file open/close, array allocation, record reads, and setting `fert_cs_flag`.
- 39fabde changed only local variable initialization (`titldum`, `header`, `fert_name`, `icsi`, `eof`, `imax`) and did not alter the file-reading algorithm.
- bd18ad4 removed the unused `imax` declaration and commented out `fert_name`; it did not change how `cs_fert_read` reads fertilizer data.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cs_fert_read' has no extracted documentation comment.
- constituent_mass_module and input_file_module were imported but no specific candidate outside references were resolved to them in the extracted references; their role is inferred from the routine context.
- The routine only sets `fert_cs_flag` when `fertilizer.frt_cs` exists; no explicit reset is present here if the file is missing.
- algorithm_steps revised: condensed the file-skip and read sequence into nine steps while keeping source line coverage aligned to the visible source.
