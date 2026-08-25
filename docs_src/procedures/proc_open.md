---
kind: procedure
symbol: proc_open
title: proc_open
status: filled
source_hash: d3fb12e7c90962af
version_label: SWAT+ 62.0.0
---

<!-- facts:header -->

Initializes the SWAT+ output header files by calling a fixed sequence of header-writing routines.

## Bottom Line

proc_open is a small orchestration subroutine with no arguments and no local state. Its job is to call the various header routines that write or open the model's output files, so the reporting system is ready before simulation output begins.

The routine does not compute model results itself. It simply sequences the output initialization calls for landscape, channel, aquifer, management, land-use change, yield, hydrology, reservoir, wetland, water allocation, pesticide, pathogen, salt, constituent, and final header registration output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs at output setup time, before the model starts writing its regular results. It is the top-level opener for the reporting/header sequence, and later output routines depend on these headers and file registrations being established first.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Declare external header routines | Declare the procedure as implicit-none and list the external header routines that will be invoked to initialize output files. |
| 2. Write landscape headers | Start the output setup by calling the landscape initializer, which writes the base landscape output headers. |
| 3. Write channel and aquifer headers | Initialize channel and aquifer reporting by calling their header routines in sequence. |
| 4. Write stream and management headers | Continue the output setup with SWAT-DEG channel, management, and land-use change headers. |
| 5. Write yield and hydrology headers | Add yield and hydrologic output headers so those reporting streams are ready. |
| 6. Write reservoir and wetland headers | Initialize reservoir and wetland reporting files by calling their header routines. |
| 7. Skip snutc header call | Leave the snutc header call commented out, so it is not part of the active output initialization sequence. |
| 8. Write water allocation header | Initialize water-allocation reporting after the main hydrologic outputs. |
| 9. Write pesticide and pathogen headers | Initialize pesticide and pathogen reporting files for later output. |
| 10. Write salt and constituent headers | Initialize salt and constituent reporting files, including the RTB-specific salt and constituent outputs noted in comments. |
| 11. Finalize output header registry | Call the final header writer and then return, completing the output initialization sequence. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `output header files and registries` | output initialization sequence runs | The routine triggers a cascade of header-writing subroutines that open and label the model's reporting files. |

## File I/O

<!-- facts:io -->


## Lineage

`proc_open.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `8b71fbe` (2026-05-04, "Removed call to header_snutc because it is not used any more. The subroutine sho…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `proc_open.f90` are listed.

- `8b71fbe` (2026-05-04) — Removed call to header_snutc because it is not used any more. The subroutine should also be deleted but will be done later.
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'proc_open' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
