---
kind: procedure
symbol: aqu_read
title: aqu_read
status: filled
source_hash: a1389f117d9b05b0
version_label: SWAT+ 62.0.0
locals:
  header: Scratch buffer (len=500) that absorbs the column-header line of `aquifer.aqu` on
    both the counting pass (aqu_read.f90:33) and the loading pass (aqu_read.f90:47); its contents
    are never used after reading.
  titldum: Scratch buffer (len=80) that absorbs the first title/comment line of `aquifer.aqu`
    on both passes (aqu_read.f90:31, 45); its contents are discarded.
  eof: Receives the `iostat=` return code from every `read` statement; a negative value signals
    end-of-file and triggers an `exit` from the enclosing loop.
  i: Holds the integer index field peeked from the current data record (aqu_read.f90:36, 51);
    used to update `imax` during the counting pass and as the `aqudb` subscript during the
    loading pass.
  imax: Running maximum of all `i` values seen during the first pass (aqu_read.f90:38); becomes
    the upper bound of the `aqudb(0:imax)` allocation at line 43.
  msh_aqp: Count of data records accumulated during the first pass (aqu_read.f90:39); stored
    into `db_mx%aqudb` at line 42 and used as the loop bound during the second pass.
  i_exist: Logical flag set by `inquire` (aqu_read.f90:25) indicating whether the file named
    `in_aqu%aqu` exists on disk; tested at line 26 to decide whether to skip all loading.
  ish_aqp: Loop counter for the second (loading) pass; iterates from 1 to `msh_aqp` (aqu_read.f90:50),
    advancing one record per iteration.
  k: Receives the integer index field during the full-record read at aqu_read.f90:55 (`read
    (107,*,iostat=eof) k, aqudb(i)`); its value is the same record index already peeked into
    `i` at line 51 before the backspace.
uses:
  input_file_module: Provides the filename string `in_aqu%aqu` (default 'aquifer.aqu') used
    in the `inquire` call at line 25 and the `open` call at line 30; if set to 'null' the
    routine skips all file I/O and allocates only a zero-element placeholder.
  aquifer_module: Provides the allocatable `aqudb` array that this routine allocates (line
    27 or line 43) and populates with `aquifer_database` records during the second-pass read
    loop (line 55); all subsequent aquifer processing routines consume this array.
  basin_module: 'The assignment `bsn_cc%gwflow = 0` appears at line 62, but that line is unreachable
    dead code: it follows an `exit` statement at line 60 inside the outer `do...enddo` block.
    In practice `bsn_cc%gwflow` is never written by this routine.'
  maximum_data_module: Receives the total record count at line 42 (`db_mx%aqudb = msh_aqp`),
    recording how many `aquifer_database` entries were loaded so that downstream routines
    can size their own loops over `aqudb`.
---

<!-- facts:header -->

Reads shallow aquifer property records from `aquifer.aqu` into the allocatable `aqudb` array during model initialization.

## Bottom Line

aqu_read populates the global aquifer database (`aqudb`) by parsing the plain-text file `aquifer.aqu`. It first checks whether the file exists and is not named 'null'; if either condition holds it allocates a zero-element placeholder `aqudb(0:0)` and returns immediately. Otherwise it opens the file, discards the title and column-header lines, and counts all data records in a first pass to determine the maximum record index (`imax`) and total record count (`msh_aqp`). It stores `msh_aqp` into `db_mx%aqudb`, allocates `aqudb(0:imax)`, then rewinds the file for a second pass that reads each full record into its indexed slot `aqudb(i)`. After loading all records it closes the file.

aqu_read takes no formal arguments; all input comes from module-level state in `input_file_module`, `aquifer_module`, `basin_module`, and `maximum_data_module`. It is the first routine called by `proc_aqu`, and the populated `aqudb` array together with the `db_mx%aqudb` count are prerequisites for the subsequent aquifer initialization calls `aqu_initial`, `aqu_read_init`, and `aqu_read_init_cs`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

aqu_read runs during model initialization as the first call in `proc_aqu` (proc_aqu.f90:9). Before this call, the input-file framework has already populated `in_aqu%aqu` with the target filename. After `aqu_read` completes, `aqudb` holds all aquifer property records indexed by their integer keys and `db_mx%aqudb` holds the total record count; the subsequent calls in `proc_aqu` — `aqu_initial`, `aqu_read_init`, and `aqu_read_init_cs` — rely on these populated structures to initialize aquifer state variables and spatial aquifer data for the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check file | Resets `msh_aqp`, `eof`, and `imax` to zero, then calls `inquire` to test whether the file named `in_aqu%aqu` exists on disk. If the file is absent or `in_aqu%aqu` equals 'null', allocates the zero-element placeholder `aqudb(0:0)` and falls through to `return` at line 66, bypassing all file I/O. |
| 2. First pass: count records and allocate | Opens `aquifer.aqu` on unit 107, reads and discards the title line (line 31) and column-header line (line 33), then loops `do while (eof == 0)` reading only the first integer field of each data record into `i`. Each iteration updates `imax = Max(imax, i)` and increments `msh_aqp`. On loop exit, stores `db_mx%aqudb = msh_aqp` and allocates `aqudb(0:imax)` to accommodate the highest index seen. |
| 3. Second pass: rewind and load records | Rewinds unit 107 to the file start (line 44), skips the title and header lines again (lines 45, 47), then loops `do ish_aqp = 1, msh_aqp`. Each iteration peeks the index field into `i` (line 51), issues `backspace` (line 53) to reposition the file pointer, then reads the full record: `k` receives the index field and `aqudb(i)` is populated with the complete `aquifer_database` structure (line 55). |
| 4. Close file and return | Closes unit 107 (line 59) then executes `exit` (line 60) to break out of the outer `do...enddo` block. The assignment `bsn_cc%gwflow = 0` at line 62 is unreachable dead code that follows the `exit`. Control passes through `endif` (line 64) to `return` (line 66). |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_aqu` | `in_aqu%aqu` |
| [sym:aquifer_module] | `aqudb` |  |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%aqudb` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%aqudb` | File exists and in_aqu%aqu != 'null' (aqu_read.f90:26) | Set to `msh_aqp` (the total record count from the first pass) at line 42, recording how many aquifer database entries were loaded into `aqudb`. |
| `bsn_cc%gwflow` | Dead code: follows `exit` at aqu_read.f90:60 and is never executed | The assignment `bsn_cc%gwflow = 0` at line 62 is unreachable because the `exit` at line 60 breaks out of the enclosing `do...enddo` block before line 62 is reached. This routine never modifies `bsn_cc%gwflow` in practice. |

## File I/O

<!-- facts:io -->


## Lineage

One source-backed commit is recorded for aqu_read.f90 (lines 1–67): commit 203a0c5 (2026-04-30), 'Merge pull request #188 from leonard-bernard-jannin/main'. The impact of this merge on aqu_read is unclear from the PR subject alone.

- {'commit': '203a0c5', 'date': '2026-04-30', 'subject': 'Merge pull request #188 from leonard-bernard-jannin/main', 'impact': 'Impact on aqu_read is unclear from the PR subject alone.'}

## Review Notes

- algorithm_steps revised: merged the original 5 steps into 4 by combining counter initialization with the file-existence check (step 1, lines 20-28), merging the 'Scan input records' and 'Allocate target storage' steps into a single first-pass step (step 2, lines 29-43) because the allocation at line 43 is the direct output of the counting loop and the original steps had overlapping source_lines (both referenced line 43), and combining close and return into step 4 (lines 59-66).
- bsn_cc%gwflow assignment at aqu_read.f90:62 is unreachable dead code: it follows an `exit` statement at line 60 inside the outer `do...enddo` block and is never executed. The `use basin_module` clause and the `bsn_cc%gwflow` reference are therefore effectively inert. A human reviewer should confirm whether this dead code is intentional or a defect.
- The outer `do...enddo` block (lines 29-63) is structured as an infinite loop exited by `exit` at line 60, a common SWAT+ idiom for a block with multiple early-exit points. The core_graph shows a 'repeat' edge from N6 back to N3 that does not reflect actual control flow; the loop body always exits at line 60 and never iterates a second time.
- warning: missing_doc: Procedure 'aqu_read' has no extracted documentation comment.
