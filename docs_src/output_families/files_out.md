---
kind: output_family
source_symbols:
- output_landscape_init
title: files_out.out
status: filled
source_hash: 5c7017612f9d07e5
version_label: SWAT+ 62.0.0
---

**Kind:** output file
**Written by:** [`output_landscape_init`](../procedures/output_landscape_init.md)
**File(s):** `files_out.out` (unit 9000)

## Bottom Line

`files_out.out` is the index of every output file the run produces. As each output file is opened, its writer emits a `TAG  filename` line to unit 9000, so this file is a manifest of the output set for the run.

## What It Writes

One line per opened output file: a short object tag and the file name (e.g. `HYDIN_PESTS  hydin_pests_day.txt`), written with `write (9000, …)` from the various header/opener routines as they call `open_output_file`.

## Source Links

- Writer: [`output_landscape_init`](../procedures/output_landscape_init.md)
- Catalog: [`Other Output Files`](other_output_files.md)

## Evidence Used

- `output_landscape_init.f90` (opens unit 9000)
- header_* routines (write file-index lines to 9000)
