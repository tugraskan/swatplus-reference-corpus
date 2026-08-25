---
kind: procedure
symbol: ch_read
title: ch_read
status: filled
source_hash: 7ccfe30d3c2d3e0c
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the file title line at the start
    of each pass through `channel.cha`.
  header: Scratch character buffer used to read and discard the file header line before scanning
    or loading the records.
  eof: I/O status flag from each `read`; negative values indicate end-of-file, and the routine
    uses it to stop scanning or loading when the file ends.
  i: Temporary integer read from the first field of each channel record during the counting
    pass; its maximum value becomes the number of channel entries expected.
  imax: Tracks the largest channel record index found in `channel.cha`; this becomes the allocation
    upper bound and is stored in `db_mx%ch_dat`.
  i_exist: Logical flag set by `inquire` to tell whether the configured channel input file
    exists before the routine tries to read it.
  ichi: Loop counter for the channel records loaded into `ch_dat` and `ch_dat_c` during the
    second pass through the file.
  k: First integer field read alongside each character record; it is parsed from the line
    but not used for any later lookup in this routine.
  iinit: Loop counter used to search `ch_init` for a matching initial-condition name.
  ihyd: Loop counter used to search `ch_hyd` for a matching hydrology-table name.
  ised: Loop counter used to search `ch_sed` for a matching sediment-table name.
  inut: Loop counter used to search `ch_nut` for a matching nutrient-table name.
uses:
  basin_module: This module holds the allocatable channel record arrays that `ch_read` sizes
    and fills. The routine writes the parsed channel definitions into these arrays so the
    rest of the channel workflow can use them.
  input_file_module: '`input_file_module` provides `in_cha%dat`, the configured path for the
    channel input file. `ch_read` uses that path to open `channel.cha` and decide whether
    the file is available or disabled.'
  channel_data_module: This module holds both the character names read from each channel record
    and the integer lookup tables that the routine fills by matching those names. The name-to-index
    conversion happens here so later code can use compact integer references instead of raw
    strings.
  maximum_data_module: The maxima in `db_mx` determine how many initial, hydrology, sediment,
    and nutrient definitions are available for matching. `ch_read` relies on those limits
    when it loops over the lookup tables, and it updates `db_mx%ch_dat` with the number of
    channel records discovered.
  hydrograph_module: The hydrology module owns the channel hydrology definitions that `ch_read`
    searches by name. Those definitions supply the valid targets for `ch_dat(ichi)%hyd`.
  pesticide_data_module: The pesticide/nutrient-side channel data include the nutrient table
    references needed here. `ch_read` matches each record’s nutrient name against `ch_nut`
    so the channel state can point to the correct nutrient definition.
---

<!-- facts:header -->

Reads channel data definitions from `channel.cha` and links each record to the corresponding initial, hydrology, sediment, and nutrient tables.

## Bottom Line

`ch_read` opens the channel input file named by `in_cha%dat`, counts how many channel records it contains, allocates the channel input arrays, then rereads the file and converts the character links in each record into integer indexes into the shared channel data tables.

It matters because later channel processing expects `ch_dat(ichi)%init`, `%hyd`, `%sed`, and `%nut` to point to valid entries in `ch_init`, `ch_hyd`, `ch_sed`, and `ch_nut`. If a name cannot be matched, the routine leaves the index at 0 and writes a warning to unit 9001.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ch_read` runs during channel setup inside `proc_cha`, after the initial channel-related tables have been read and before later channel initialization steps. Its results are required so downstream channel routines can work with integer links to the selected initial, hydrology, sediment, and nutrient definitions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check file availability and initialize counters | Resets the scan counters, checks whether the configured channel file exists, and branches to a minimal allocation path if the file is missing or set to the string `null`. |
| 2. Allocate empty channel arrays when no file is usable | Creates 1-element dummy arrays at bounds 0:0 so later code can safely reference the channel data containers even when no channel file is present. |
| 3. Open and scan the file to find the largest channel index | Opens `channel.cha`, skips the title and header lines, and reads the first integer from each record to compute the maximum channel count. |
| 4. Save the record count and allocate storage | Stores the discovered record count in `db_mx%ch_dat` and allocates the parsed and interpreted channel arrays to the needed size. |
| 5. Rewind and skip the file header again | Returns to the start of `channel.cha` and rereads the title and header so the second pass begins at the first data record. |
| 6. Read each channel record and its raw character fields | Walks through each record, backs up to reread the full line, and loads the raw character-name structure into `ch_dat_c(ichi)`. |
| 7. Resolve the initial-condition reference | Searches `ch_init` for a matching name and stores the matching position in `ch_dat(ichi)%init`. |
| 8. Resolve the hydrology reference | Searches `ch_hyd` for a matching name and stores the matching position in `ch_dat(ichi)%hyd`. |
| 9. Resolve the sediment reference | Searches `ch_sed` for a matching name and stores the matching position in `ch_dat(ichi)%sed`. |
| 10. Resolve the nutrient reference | Searches `ch_nut` for a matching name and stores the matching position in `ch_dat(ichi)%nut`. |
| 11. Report missing references | Writes warnings for any channel record whose initial, hydrology, sediment, or nutrient reference was not found in the corresponding lookup table. |
| 12. Close the input file and exit the read loop | Closes `channel.cha` after the load pass finishes, then exits the outer loop and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `ch_dat, ch_dat_c` | `ch_dat(0:0), ch_dat_c(0:0), ch_dat(0:imax), ch_dat_c(0:imax), ch_dat(ichi), ch_dat_c(ichi)` |
| [sym:input_file_module] | `in_cha` | `in_cha%dat` |
| [sym:channel_data_module] | `ch_init, ch_dat_c, ch_dat, ch_hyd, ch_sed, ch_nut` | `ch_init(iinit)%name, ch_dat_c(ichi)%init, ch_dat(ichi)%init, ch_hyd(ihyd)%name, ch_dat_c(ichi)%hyd, ch_dat(ichi)%hyd, ch_sed(ised)%name, ch_dat_c(ichi)%sed, ch_dat(ichi)%sed, ch_nut(inut)%name, ch_dat_c(ichi)%nut, ch_dat(ichi)%nut` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_dat, db_mx%ch_init, db_mx%ch_hyd, db_mx%ch_sed, db_mx%ch_nut` |
| [sym:hydrograph_module] | `ch_hyd` | `ch_hyd(ihyd)` |
| [sym:pesticide_data_module] | `ch_nut` | `ch_nut(inut)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ch_dat` | After the count pass completes and before allocating channel arrays. | `db_mx%ch_dat` is set to the number of channel records found in `channel.cha`, giving the rest of the model the maximum channel-data count available for allocation and later iteration. |
| `ch_dat(ichi)%init` | When a channel record’s `init` name matches one entry in `ch_init`. | `ch_dat(ichi)%init` changes from its default 0 to the index of the matching initial-condition definition, converting the raw name in `ch_dat_c(ichi)%init` into an integer reference. |
| `ch_dat(ichi)%hyd` | When a channel record’s `hyd` name matches one entry in `ch_hyd`. | `ch_dat(ichi)%hyd` changes from 0 to the index of the matching hydrology definition so later channel routines can use the selected hydrology parameters. |
| `ch_dat(ichi)%sed` | When a channel record’s `sed` name matches one entry in `ch_sed`. | `ch_dat(ichi)%sed` changes from 0 to the index of the matching sediment definition, linking the channel record to its sediment transport setup. |
| `ch_dat(ichi)%nut` | When a channel record’s `nut` name matches one entry in `ch_nut`. | `ch_dat(ichi)%nut` changes from 0 to the index of the matching nutrient definition, linking the channel record to its nutrient behavior setup. |

## File I/O

<!-- facts:io -->


## Lineage

`ch_read` was introduced in commit df07e3f as a new subroutine. The later resolved lineage commits changed its implementation by adding explicit initialization of the local scratch variables in 39fabde and by adding external procedure declarations for `hyddep_output`, `recall_cs`, and `recall_salt` in bd18ad4.

- 39fabde initialized the local title/header strings, counters, and loop variables to blank or zero defaults, reducing dependence on uninitialized values in the read logic.
- bd18ad4 added external declarations for `hyddep_output`, `recall_cs`, and `recall_salt`, though no calls to those procedures appear in the extracted body of `ch_read`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read' has no extracted documentation comment.
