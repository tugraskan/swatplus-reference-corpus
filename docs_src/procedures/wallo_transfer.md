---
kind: procedure
symbol: wallo_transfer
title: wallo_transfer
status: filled
source_hash: ba1daa88cb7f2286
version_label: SWAT+ 62.0.0
args:
  iwallo: Selects which water-allocation object to process, so the routine only updates the
    transfer record for that one `wallo(iwallo)` entry.
  itrn: Selects which transfer within `wallo(iwallo)%trn` to process; the routine loops through
    that transfer’s source list and applies source-specific conveyance adjustments.
locals:
  isrc: Loop index for the individual source entries inside `wallo(iwallo)%trn(itrn)%src`.
    It starts at 0 and is advanced from 1 to `src_num` to visit every source attached to the
    transfer.
  iconv: Holds the conveyance object number copied from the current source’s `conv_num`. It
    is used to look up the pipe loss factor for the current source.
uses:
  water_allocation_module: '`water_allocation_module` defines the transfer object graph that
    this routine traverses: `wallo(iwallo)%trn(itrn)%src_num` gives the source count, `src(isrc)%conv_num`
    identifies the conveyance object, and `src(isrc)%conv_typ` decides whether the source
    is a pipe or pump. `pipe(iconv)%loss_fr` supplies the loss fraction applied to the hydrograph
    for pipe transfers.'
  hydrograph_module: '`hydrograph_module` provides the `wal_omd` state that stores each transfer
    source’s hydrograph output. This matters because the routine updates `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd`
    in place, and that adjusted output is what later allocation and receiving-object logic
    uses.'
  constituent_mass_module: '`constituent_mass_module` is imported by the procedure, indicating
    the transfer hydrograph may carry constituent mass fields through `hyd_output` even though
    this snippet only shows the flow adjustment. It matters because any mass-tracking attached
    to the hydrograph has to remain consistent with the flow loss handling here.'
  sd_channel_module: '`sd_channel_module` is imported because water allocation transfers can
    interact with channel-linked routing elsewhere in the allocation system. Even though this
    procedure does not reference a channel symbol directly, the module matters to the broader
    transfer pathway that `wallo_control` is orchestrating.'
  aquifer_module: '`aquifer_module` is part of the shared water-allocation context for receiving
    or source objects handled by the allocation system. It matters here because `wallo_transfer`
    is one step in the transfer workflow that prepares adjusted flows before later object-specific
    updates.'
  reservoir_module: '`reservoir_module` is another destination/source family in the water-allocation
    system. It matters here because this routine contributes to the common transfer processing
    that later routes adjusted water to the appropriate receiving object.'
  time_module: '`time_module` is imported as part of the water-allocation execution context,
    where transfer bookkeeping is performed on the model time step. It matters because the
    adjusted transfer hydrograph is part of the time-stepped allocation sequence managed by
    the calling control routine.'
---

<!-- facts:header -->

Applies conveyance losses to each source in a water-transfer object. It updates transferred hydrograph output before downstream receiving-object routing uses it.

## Bottom Line

`wallo_transfer` walks through every source attached to one water-allocation transfer and adjusts the source hydrograph for conveyance losses. In the current source, only `pipe` transfers are modified: the routine multiplies `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd` by `(1. - pipe(iconv)%loss_fr)` using the source’s conveyance number.

The routine exists so the transfer bookkeeping in `wallo_control` can separate source-specific conveyance effects from the later receiving-object update. After this routine runs, the adjusted hydrograph stored in `wal_omd(...)%hd` is what downstream allocation logic consumes.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wallo_transfer` runs inside `wallo_control` after that routine has summed total withdrawal for a transfer and before the receiving object is updated. `wallo_control` prepares the transfer indices and aggregated withdrawal data; `wallo_transfer` then applies source conveyance losses so later receiving-object handling uses the corrected transfer hydrograph.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. iterate sources | Loop over every source attached to the selected transfer object, from the first source through `src_num`, so each source can be adjusted individually. |
| 2. get conveyance | Copy the current source’s conveyance object number into `iconv` so the routine can look up the matching pipe record. |
| 3. branch by type | Check the source’s conveyance type to decide how that source’s hydrograph should be treated. |
| 4. reduce pipe flow | For pipe transfers, scale the source hydrograph by `1 - loss_fr` so the transferred flow is reduced by the pipe’s loss fraction. |
| 5. note pump case | Leave the pump branch as a placeholder; the source shows no implemented pump-loss adjustment in this routine. |
| 6. finish routine | End the source loop, return to the caller, and leave the adjusted transfer hydrographs in `wal_omd` for later receiving-object processing. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `wallo, pipe` | `wallo(iwallo)%trn(itrn)%src_num, wallo(iwallo)%trn(itrn)%src(isrc)%conv_num, wallo(iwallo)%trn(itrn)%src(isrc)%conv_typ, pipe(iconv)%loss_fr` |
| [sym:hydrograph_module] | `wal_omd` | `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd` |
| [sym:constituent_mass_module] | `constituent_mass_module` | `constituent_mass_module` |
| [sym:sd_channel_module] | `sd_channel_module` | `sd_channel_module` |
| [sym:aquifer_module] | `aquifer_module` | `aquifer_module` |
| [sym:reservoir_module] | `reservoir_module` | `reservoir_module` |
| [sym:time_module] | `time_module` | `time_module` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd` | When `wallo(iwallo)%trn(itrn)%src(isrc)%conv_typ` is `"pipe"` inside the source loop. | The source hydrograph stored in `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd` is reduced by the pipe loss fraction so the transfer reflects conveyance losses before downstream allocation uses it. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows `wallo_transfer` was added in `df07e3f` as a new routine that handled channel, reservoir, and aquifer destination updates for `idmd`. In `39fabde`, only the local working variables were initialized to zero. In `23142ed`, the routine was rewritten around transfer-source iteration: the argument changed from `idmd` to `itrn`, `use constituent_mass_module` was added, the old direct destination `select case` block was removed, and a new loop applies pipe loss to `wal_omd(iwallo)%trn(itrn)%src(isrc)%hd` while leaving pump handling as a placeholder.

- df07e3f introduced the procedure with direct receiver updates for channel, reservoir, and aquifer destinations.
- 39fabde only initialized the integer temporaries `j` and `iob`; it did not change algorithm behavior.
- 23142ed changed the routine’s behavior from destination updates to per-source conveyance-loss processing over `wallo(iwallo)%trn(itrn)%src`, added constituent-mass support, and left pump losses unimplemented.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wallo_transfer' has no extracted documentation comment.
- algorithm_steps revised: the step list was reworked to match the current source lines 20-32 and the current pipe/pump transfer logic rather than the older destination-update implementation.
- `constituent_mass_module`, `sd_channel_module`, `aquifer_module`, `reservoir_module`, and `time_module` are imported by the procedure, but the extracted source snippet does not show direct symbol references from those modules in this routine; their role notes are therefore based on the surrounding water-allocation context visible in the packet.
- The source shows an implemented `pipe` branch and a commented `pump` placeholder; no numeric pump-loss formula is present in the extracted lines.
