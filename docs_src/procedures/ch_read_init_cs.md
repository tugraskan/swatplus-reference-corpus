---
kind: procedure
symbol: ch_read_init_cs
title: ch_read_init_cs
status: filled
source_hash: 1049b088b05e9fb8
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to read and discard the file title or first-column text lines
    while scanning `initial.cha_cs`.
  header: Scratch string used to read and discard the header line(s) before the actual `ch_init_cs`
    records are counted or loaded.
  eof: I/O status flag from each `read` on unit 105; values below zero are used to detect
    end-of-file and stop the scan.
  imax: Record counter that tallies how many constituent data entries are present in `initial.cha_cs`;
    the routine uses it to size `ch_init_cs` and assign `db_mx%ch_init_cs`.
  i_exist: Logical flag set by `inquire` to indicate whether `initial.cha_cs` exists before
    attempting to open it.
  ich: Loop counter used when rereading the file to store each record into `ch_init_cs(ich)`.
uses:
  basin_module: The routine imports `basin_module`, so its channel initialization runs in
    the shared basin-level model context even though no specific resolved symbols from that
    module were extracted here.
  input_file_module: The routine imports `input_file_module`, which provides the broader input-file
    environment used by SWAT+ readers; that shared input context is relevant even though no
    specific resolved symbols from it were extracted in the evidence.
  maximum_data_module: '`maximum_data_module` matters because this routine writes the scanned
    record count into `db_mx%ch_init_cs`, establishing the number of channel constituent initial
    records available for later processing.'
  channel_data_module: '`channel_data_module` matters because `ch_init_cs` is the allocatable
    storage that receives the records read from `initial.cha_cs`; this routine allocates and
    fills that shared array.'
  sd_channel_module: The routine uses `sd_channel_module` as part of the salt/constituent
    channel initialization pathway, so the imported module is part of the downstream channel-state
    context even though no specific symbol from it is referenced in the extracted lines.
---

<!-- facts:header -->

Reads the channel constituent initial-condition file `initial.cha_cs` and loads its records into `ch_init_cs`.
It also counts the records first so `db_mx%ch_init_cs` can be set before allocation.

## Bottom Line

This subroutine prepares channel constituent starting data for the salt/constituent channel workflow. It first checks whether `initial.cha_cs` exists; if it does not, it allocates a minimal `ch_init_cs(0:0)` array. If the file is present, it counts the data records, stores that count in `db_mx%ch_init_cs`, allocates `ch_init_cs(0:imax)`, then rereads the file to populate each `ch_init_cs(ich)` entry.

The result is shared state used later by the channel routines that need initial constituent settings. Because `proc_cha` calls this routine early, the rest of the channel initialization sequence can rely on `db_mx%ch_init_cs` and `ch_init_cs` being ready before hydrology, sediment, nutrient, and other channel readers run.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during early channel processing, immediately after `proc_cha` begins its input setup. `proc_cha` calls it before other channel readers such as hydrology, sediment, nutrient, and general channel data readers, so those later routines can depend on `db_mx%ch_init_cs` and `ch_init_cs` being initialized.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the initial constituent file is available | The routine inquires about `initial.cha_cs`; if the file is missing, or the name is the literal `null`, it skips file reading and allocates a one-element placeholder array `ch_init_cs(0:0)`. |
| 2. Open the file and begin a counting pass | When the file is present, the routine opens unit 105 on `initial.cha_cs`, reads and discards the title line and header line, and exits early if end-of-file is reached during those initial reads. |
| 3. Count data records | It loops while `eof == 0`, reading one dummy line at a time into `titldum` and incrementing `imax` for each record until end-of-file is encountered. |
| 4. Save the record count and allocate storage | The routine copies the counted total into `db_mx%ch_init_cs` and allocates `ch_init_cs(0:imax)` so the array matches the number of records discovered in the file. |
| 5. Rewind and reread the file | It rewinds unit 105 to the start of `initial.cha_cs`, then rereads and discards the title and header lines again to position the file at the first data record. |
| 6. Load each constituent record into shared state | A counted loop reads each `ch_init_cs(ich)` entry from the file into the allocatable channel constituent array, stopping early if an end-of-file status appears. |
| 7. Close the input file | After the records are loaded, the routine closes unit 105 and leaves the initialized channel constituent data in module state for later use. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state` |  |
| [sym:input_file_module] | `input_file_module state` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_init_cs` |
| [sym:channel_data_module] | `ch_init_cs` |  |
| [sym:sd_channel_module] | `sd_channel_module state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ch_init_cs` | When `initial.cha_cs` exists and is not the literal `null`. | `db_mx%ch_init_cs` is set equal to the counted number of data records in `initial.cha_cs`, so later code knows how many channel constituent initial-condition entries were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior-relevant changes. The original implementation was added in `df07e3f`. Commit `39fabde` initialized local scalars `titldum`, `header`, `eof`, `imax`, and `ich` at declaration while also keeping the explicit assignments. Commit `2ee1889` made only whitespace/end-of-file cleanup at the end of the subroutine and did not change runtime behavior.

- df07e3f introduced the routine and its file-count-then-read workflow for `initial.cha_cs`.
- 39fabde added declaration-time initialization for `titldum`, `header`, `eof`, `imax`, and `ich` without changing the I/O logic.
- 2ee1889 only adjusted trailing formatting and the `end subroutine` line; it did not alter execution.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_init_cs' has no extracted documentation comment.
- algorithm_steps revised: merged the original allocation/counting split into a clearer count-then-allocate sequence and separated the rewind/load/close phases to match the source flow.
- No resolved outside-reference component details were available for basin_module, input_file_module, or sd_channel_module beyond the imported modules themselves.
