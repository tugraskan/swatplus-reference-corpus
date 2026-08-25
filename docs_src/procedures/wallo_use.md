---
kind: procedure
symbol: wallo_use
title: wallo_use
status: filled
source_hash: 6bdad35903643ec4
version_label: SWAT+ 62.0.0
args:
  iwallo: Selects which water allocation object in `wal_omd` supplies the withdrawal volume
    for this call; the routine uses `wal_omd(iwallo)%trn(itrn)%h_tot` as the source flow to
    scale the water-use outflow.
  itrn: Selects the transfer entry within the chosen water allocation object. Together with
    `iwallo`, it identifies the specific `h_tot` flow record that is used to size the treated
    outflow.
  iuse: Selects the water use record being updated. The routine uses `iuse` to read the use-specific
    effluent settings, write `wuse_om_out(iuse)` and `wal_use_omd(iuse)`, and pass the matching
    constituent effluent state to the mass conversion call.
locals:
  iom: '`iom` is the pointer from the water-use definition to the organic-mineral effluent
    template. It is loaded from `wuse(iuse)%iorg_min` and used to pick the correct `wuse_om_efflu`
    entry for this use.'
uses:
  water_allocation_module: '`water_allocation_module` provides the water-use configuration
    that tells this routine which organic-mineral effluent template belongs to the selected
    use. The `wuse(iuse)%iorg_min` pointer controls which concentration set is copied into
    `outflo_om` before scaling and conversion.'
  hydrograph_module: '`hydrograph_module` holds the flow and output records that this routine
    reads and writes. It supplies the transfer volume from `wal_omd(iwallo)%trn(itrn)%h_tot%flo`,
    the working outflow `outflo_om`, and the storage/output fields `wuse_om_out` and `wal_use_omd`
    that capture the resulting treated use discharge and added mass.'
  constituent_mass_module: '`constituent_mass_module` matters because the routine optionally
    converts constituent concentrations to mass for water uses when any constituents are simulated.
    `cs_db%num_tot` gates that branch, and the routine uses the water-use constituent effluent
    record to populate `outflo_cs`.'
---

<!-- facts:header -->

Updates the organic-mineral and constituent outflow for a water use object. It scales the use effluent by the transferred water volume, converts concentrations to mass, and stores the results for downstream accounting.

## Bottom Line

wallo_use computes the outflow associated with a specific water use transfer. It starts from the use’s effluent concentration template, applies the actual withdrawal volume from the matching water allocation transfer, converts the resulting organic-mineral concentrations to mass, and stores the finished outflow in the water-use state arrays.

If total constituents are being simulated, it also converts the water-use constituent effluent concentrations to mass using the same outflow volume. The routine then clears the working outflow variable, so the caller can proceed without leaving stale values in `outflo_om`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the water-allocation control flow after `wallo_control` has identified a case of type `'use'` and passed in the allocation object index, transfer index, and use index. `wallo_control` has already accumulated the transferred flow into `wuse_om_stor(j)` before calling `wallo_use`. The results feed later accounting of water-use outflow and the added organic-mineral mass in `wuse_om_out(iuse)` and `wal_use_omd(iuse)`; if constituents are active, they also feed the matching constituent outflow record `outflo_cs`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load the water-use organic-mineral template | Read the selected use’s organic-mineral effluent pointer from `wuse(iuse)%iorg_min`, copy that template into the working outflow record `outflo_om`, and prepare it for scaling by the actual transfer volume. |
| 2. Scale the outflow by the transferred water volume | Multiply the working outflow flow rate by the transfer flow stored in `wal_omd(iwallo)%trn(itrn)%h_tot%flo` so the use effluent reflects the actual withdrawal size. |
| 3. Convert organic-mineral concentrations to mass | Call `hyd_convert_conc_to_mass` to turn the scaled organic-mineral concentrations in `outflo_om` into mass loads, then save the finished outflow in `wuse_om_out(iuse)`. |
| 4. Compute the added organic-mineral load | Subtract the transfer hydrograph from the finished use outflow to form `wal_use_omd(iuse)`, which represents the amount of organic-mineral material added by the water use. |
| 5. Optionally build constituent mass outflow | If `cs_db%num_tot > 0`, convert the selected water-use constituent effluent record with `hydcsout_conc_mass`, using the current outflow volume `outflo_om%flo` to generate the mass-based constituent outflow. |
| 6. Clear the working outflow and exit | Reset `outflo_om` to `hz` so no stale output remains in the shared working variable, then return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `wuse` | `wuse(iuse)%iorg_min` |
| [sym:hydrograph_module] | `outflo_om, wal_omd, wal_use_omd, wuse_om_efflu, wuse_om_out, hz` | `outflo_om%flo, wal_omd(iwallo)%trn(itrn)%h_tot%flo` |
| [sym:constituent_mass_module] | `cs_db, wuse_cs_efflu, outflo_cs` | `cs_db%num_tot` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `outflo_om` | After the selected water-use template has been copied and scaled, and before return. | `outflo_om` is overwritten with the selected use’s effluent template, scaled by the transfer flow, converted from concentration to mass, and finally reset to `hz` so the shared working outflow does not keep the previous use’s values. |
| `outflo_om%flo` | After `outflo_om` has been scaled by `wal_omd(iwallo)%trn(itrn)%h_tot%flo` and before the reset to `hz`. | `outflo_om%flo` becomes the actual treated outflow volume for this water use, derived from the selected transfer volume and used as the basis for mass conversion. |
| `wuse_om_out(iuse)` | Immediately after the mass conversion of `outflo_om`, during the current water-use case. | `wuse_om_out(iuse)` stores the finished organic-mineral outflow for the selected use so later water-use accounting can reference the converted mass output. |
| `wal_use_omd(iuse)` | After the current use outflow has been computed and subtracted from the transfer hydrograph. | `wal_use_omd(iuse)` stores the added organic-mineral load associated with the water use, computed as the difference between the use outflow and the transferred water mass/volume record. |

## File I/O

<!-- facts:io -->


## Lineage

The resolved lineage shows one behavior-changing commit for this procedure: d70017a introduced `wallo_use.f90` as a new subroutine. The diff added the full routine body, including the water-use template copy, scaling by transfer flow, conversion to mass, optional constituent handling, and the reset of the working outflow variable.

- d70017a added the complete `wallo_use` implementation, defining how a water-use transfer is converted from effluent concentrations to mass and stored in the hydrograph accounting arrays.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wallo_use' has no extracted documentation comment.
