---
kind: procedure
symbol: rte_read_nut
title: rte_read_nut
status: filled
source_hash: 527c6168b0dd69ff
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for reading and skipping title or non-data lines from
    `nutrients.rte` during both the counting pass and the data-loading pass.
  header: Temporary character buffer for reading the file header line from `nutrients.rte`,
    which is skipped before the routine counts or loads the actual routing nutrient records.
  eof: I/O status flag set by each `read` on unit 105; it detects end-of-file or read failure
    so the routine can stop counting or loading records cleanly.
  imax: Counts how many routing nutrient data records are present in `nutrients.rte`; that
    count is then used to allocate `rte_nut(0:imax)` and drive the load loop.
  i_exist: Logical flag from `inquire` that tells the routine whether `nutrients.rte` is present
    on disk, deciding between the placeholder allocation path and the file-reading path.
  ich: Loop counter used on the second pass to step through each routing nutrient record and
    store it into `rte_nut(ich)`.
uses:
  channel_data_module: This module owns the allocatable `routing_nut_data` array that receives
    the file contents. The routine allocates and fills that shared array so later channel
    and routing code can access the nutrient parameters.
---

<!-- facts:header -->

Reads the routing nutrient input file `nutrients.rte` into the allocatable `rte_nut` array used by channel routing water-quality data.

## Bottom Line

`rte_read_nut` checks whether `nutrients.rte` exists, counts the number of data records in it, allocates `channel_data_module::rte_nut` to match, then rereads the file and loads each record into `rte_nut(ich)`. If the file is missing, it still allocates a one-element placeholder array so downstream code has a defined routing-nutrient container.

This matters because the channel routing system needs the nutrient settings in `rte_nut` before later routing or water-quality calculations can use them. The routine is called from `proc_hru` during setup, so the routing nutrient state is prepared as part of the broader HRU processing workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU processing, immediately after `proc_hru` finishes its own setup and calls `rte_read_nut`. Its result is the populated `rte_nut` array in `channel_data_module`, which later channel-routing and nutrient-handling code depends on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test for the input file | Resets `eof` and `imax`, checks whether `nutrients.rte` exists with `inquire`, and if it does not, allocates a one-element placeholder `rte_nut(0:0)`. |
| 2. Open the file and begin the first scan | When the file exists, opens `nutrients.rte` on unit 105 and reads past the title and header lines before scanning for data records. |
| 3. Count the data records | Loops while `eof == 0`, reading records into `titldum` and incrementing `imax` until end-of-file is reached, so the array size matches the file length. |
| 4. Allocate storage sized to the file | Allocates `rte_nut(0:imax)` using the counted number of data records. |
| 5. Rewind and rescan the file header | Rewinds unit 105 to the start of `nutrients.rte` and rereads the title and header lines to position the file for data loading. |
| 6. Load each routing nutrient record | For each index from 1 to `imax`, reads a line into `titldum`, backs up one record, and then reads the structured record into `rte_nut(ich)`. |
| 7. Exit the file-processing loop and close the file | Leaves the enclosing `do` loop after the records are loaded, then closes unit 105. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:channel_data_module] | `rte_nut` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits touched `rte_read_nut`: df07e3f introduced the routine with its file-scan/allocate/load logic, 39fabde initialized the local variables (`titldum`, `header`, `eof`, `imax`, `ich`) and set their defaults, and 889136d made a documentation typo fix in the comment block (`occuring` to `occurring`).

- df07e3f added the full `rte_read_nut` subroutine, including the `nutrients.rte` existence check, record counting, allocation of `rte_nut`, rewind/backspace-based reread, and final close.
- 39fabde changed local variable declarations to initialize the working scalars and strings (`titldum = ""`, `header = ""`, `eof = 0`, `imax = 0`, `ich = 0`) while leaving the file-processing algorithm unchanged.
- 889136d only corrected a spelling mistake in the in-source purpose comment and did not change runtime behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'rte_read_nut' has no extracted documentation comment.
