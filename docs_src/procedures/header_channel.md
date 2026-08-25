---
kind: procedure
symbol: header_channel
title: header_channel
status: filled
source_hash: bfc68b7d1a96dc70
version_label: SWAT+ 62.0.0
uses:
  channel_module: This routine depends on `channel_module` because the header field lists
    it writes come from `ch_hdr` and `ch_hdr_units`; those derived-type instances define the
    channel column names and units that must be printed into every channel output file.
  basin_module: This routine depends on `basin_module` because `bsn%name` and `prog` are written
    as the leading identification line in every file, and `pco%chan%d`, `pco%chan%m`, `pco%chan%y`,
    `pco%chan%a`, and `pco%csvout` control which channel output files are created.
  hydrograph_module: This routine depends on `hydrograph_module` because `sp_ob%chan` is the
    gate that tells the routine whether any channel objects exist at all; if there are no
    channel objects, it skips creating the channel header files.
  output_path_module: This module matters because `open_output_file` is the file-opening helper
    used here. It resolves the final output path and opens the chosen unit before the header
    records are written.
---

<!-- facts:header -->

Builds the header records for channel output files and opens the daily, monthly, yearly, and average-annual channel outputs when channel objects exist.

## Bottom Line

`header_channel` prepares the channel output files at startup. It checks whether any channel objects exist and, for each enabled channel reporting interval, opens the corresponding text file and optional CSV file, then writes the basin/program line plus the channel header labels and units.

It also writes a line to unit 9000 naming each channel output file that was created. Those header records are what later channel simulation output routines rely on to keep the text and CSV files aligned with the channel variables in `ch_hdr` and `ch_hdr_units`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model/output initialization, after `proc_open` calls `output_landscape_init` and before the rest of the header routines. It prepares the channel output files so later channel simulations can write daily, monthly, yearly, and average-annual results with the correct headers already in place.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check that channel objects exist. | The routine first tests `sp_ob%chan > 0` so it only creates channel headers when there are channel objects in the simulation. |
| 2. Gate day output by print code. | If daily channel output is enabled with `pco%chan%d == 'y'`, it opens unit 2480 for `channel_day.txt`, writes the basin/program line, writes `ch_hdr` and `ch_hdr_units`, and records the file name on unit 9000; if CSV output is also enabled, it opens unit 2484 for `channel_day.csv`, writes the same identification line, then writes the header and units rows in comma-separated form and records that file name on unit 9000. |
| 3. Gate month output by print code. | If monthly channel output is enabled with `pco%chan%m == 'y'`, it opens unit 2481 for `channel_mon.txt`, writes the basin/program line, writes `ch_hdr` and `ch_hdr_units`, and records the text file on unit 9000; if CSV output is enabled, it opens unit 2485 for `channel_mon.csv`, writes the identification line, writes the header and units rows in CSV format, and records that file name on unit 9000. |
| 4. Gate yearly output by print code. | If yearly channel output is enabled with `pco%chan%y == 'y'`, it opens unit 2482 for `channel_yr.txt`, writes the basin/program line, writes `ch_hdr` and `ch_hdr_units`, and records the text file on unit 9000; if CSV output is enabled, it opens unit 2486 for `channel_yr.csv`, writes the identification line, writes the header and units rows in CSV form, and records that file name on unit 9000. |
| 5. Gate average-annual output by print code. | If average-annual channel output is enabled with `pco%chan%a == 'y'`, it opens unit 2483 for `channel_aa.txt`, writes the basin/program line, writes `ch_hdr` and `ch_hdr_units`, and records the text file on unit 9000; if CSV output is enabled, it opens unit 2487 for `channel_aa.csv`, writes the identification line, writes the header and units rows in CSV format, and records that file name on unit 9000. |
| 6. Return after headers are written. | The subroutine finishes immediately after the output headers have been prepared and no values are returned because it has no arguments. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:channel_module] | `ch_hdr, ch_hdr_units` |  |
| [sym:basin_module] | `pco, bsn, prog` | `pco%chan%d, bsn%name, pco%csvout, pco%chan%m, pco%chan%y, pco%chan%a` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%chan` |
| [sym:output_path_module] | `get_output_filename, open` | `get_output_filename(filename), open(iunit, file=trim(full_path), recl=recl_val)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`header_channel.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `2fe89fd` (2026-04-21, "CSV output file fixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `header_channel.f90` are listed.

- `2fe89fd` (2026-04-21) — CSV output file fixes
- `504d2b3` (2025-12-11) — Align Use statements and adjusting whitespace.
- `9299ca5` (2025-12-04) — allow specifying output directory
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `10e5ddc` (2025-08-27) — 08272025 updates
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'header_channel' has no extracted documentation comment.
- algorithm_steps revised: expanded the original two-step sketch into six source-backed steps to reflect each channel period branch and the final return.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
