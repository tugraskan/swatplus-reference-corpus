---
kind: procedure
symbol: wet_irrp
title: wet_irrp
status: filled
source_hash: 2803bd7a42bb7918
version_label: SWAT+ 62.0.0
locals:
  iob: Index of the current upstream routing object for the HRU; used to read routing connectivity
    and locate the irrigation source object in `ob`.
  iru: Routing-unit index taken from `ob(j)%ru(1)` when routing connectivity exists; combined
    with `sp_ob%hru` to identify the object slot for source lookup.
  isrc: Irrigation source identifier. It is set from `hru(j)%irr_isc` when explicitly provided,
    otherwise derived from the connected channel/reservoir/aquifer object, and it controls
    which storage arrays are depleted.
  wsa1: HRU water-surface area in square meters, computed as `hru(j)%area_ha * 10.`; used
    to convert irrigation volume to applied depth and runoff depth.
  j: Current HRU index, copied from `ihru` so the routine works on the active HRU record.
  i: Loop counter used while scanning `ob(iob)%src_tot` for a matching irrigation source type.
  rto: Withdrawal ratio capped at 0.99; used to fractionally remove water and constituent
    mass from a finite source without emptying it completely.
uses:
  reservoir_data_module: The routine `use`s this module, so its shared reservoir data are
    part of the broader wetland/irrigation model state even though no specific symbol from
    it is referenced in the extracted lines.
  reservoir_module: '`wet_ob(j)%depth` is the current wetland/paddy ponding depth. The routine
    subtracts it from the HRU target depth to compute irrigation demand and therefore needs
    the wetland state to know how much water must be added.'
  hydrograph_module: 'This module supplies the shared irrigation transfer objects and routing/storage
    records that `wet_irrp` reads and updates: HRU irrigation demand, routing connectivity,
    channel/reservoir/aquifer storages, and the `irrig(j)%water`, `applied`, and `runoff`
    bookkeeping fields.'
  constituent_mass_module: This module holds the constituent-mass records associated with
    irrigation water, channel water, reservoir water, and aquifer water. `wet_irrp` updates
    these records in lockstep with water withdrawal so mass is conserved with the selected
    source.
  aquifer_module: '`aqu_d(isrc)%stor` is the available aquifer storage used when the irrigation
    source is groundwater. The routine compares demand to storage, computes the withdrawal
    ratio, and reduces aquifer storage accordingly.'
  mgt_operations_module: The procedure is invoked from management operations logic, so this
    module is part of the management context that determines when wetland irrigation is allowed
    to run.
  hru_module: '`hru(j)%area_ha`, `hru(j)%irr_src`, and `hru(j)%irr_isc` define the active
    HRU size and irrigation source selection. They control demand scaling and which source
    branch the routine follows.'
  climate_module: '`w%precip` reduces the irrigation demand calculation by accounting for
    rainfall already contributing to the ponded water depth, so daily weather directly changes
    how much supplemental irrigation is needed.'
---

<!-- facts:header -->

Computes wetland/paddy irrigation demand for the current HRU and withdraws water from a linked channel, reservoir, or aquifer when available.

## Bottom Line

`wet_irrp` runs the wetland/paddy continuous irrigation check for the active HRU. It computes how much water is needed to raise ponding toward the HRU target, then decides whether that water comes from a channel, reservoir, aquifer, or an unlimited source based on the HRU irrigation settings and routing connectivity.

When a finite source is used, the routine removes water from the source storage, transfers constituent mass into `cs_irr`, and records the irrigation water volume and resulting applied water and runoff. Those outputs feed the rest of the HRU water balance and irrigation bookkeeping for the timestep.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wet_irrp` is called from `hru_control` after the HRU has been identified and only when paddy irrigation is enabled and the wetland depth is below `hru(j)%irr_hmin`. `hru_control` prepares the active HRU context (`ihru`, `hru(j)`, wetland depth, and routing connectivity), and the results from `wet_irrp` feed later wetland/HRU water-balance behavior by setting irrigation demand, source depletion, applied depth, runoff, and constituent transfers before `wetland_control` runs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and compute its surface area scale. | Copies `ihru` into `j` and computes `wsa1` from `hru(j)%area_ha` so the routine can express irrigation volume as applied depth and runoff depth. |
| 2. Compute irrigation demand from target ponding depth, existing wetland depth, and precipitation. | Sets `irrig(j)%demand` to the positive deficit between the HRU target ponding depth and the current wetland depth, subtracting daily precipitation and converting to volume with `wsa1`. |
| 3. Initialize the source ratio and resolve routing connectivity. | Resets `rto` and checks whether `ob(j)%ru` is allocated. If no routing link exists, it marks the HRU source as unlimited; otherwise it stores the routing-unit index and computes the connected object index `iob`. |
| 4. Determine the irrigation source index from HRU settings or connectivity. | Uses `hru(j)%irr_src` and `hru(j)%irr_isc` to determine whether the source is unlimited or a specific channel/reservoir/aquifer. If needed, it scans `ob(iob)%src_tot` and matches `hru(j)%irr_src` against `ob(iob)%obtyp_out(i)` to set `isrc`. |
| 5. Withdraw from channel or stream-depression channel storage when requested. | If the source type is `cha` or `sdc`, the routine checks that `ch_stor` is allocated and that `isrc` is valid. It computes a capped withdrawal ratio from `ch_stor(isrc)%flo`, transfers water into `irrig(j)%water`, and reduces `ch_stor` and `ch_water`; otherwise it assigns the demand directly to `irrig(j)%water%flo`. |
| 6. Withdraw from reservoir storage when requested. | If the source type is `res`, the routine checks `res` allocation and source validity, computes a capped withdrawal ratio from `res(isrc)%flo`, transfers water into `irrig(j)%water`, and reduces `res` and `res_water`; otherwise it assigns the demand directly to `irrig(j)%water%flo`. |
| 7. Withdraw from aquifer storage when requested. | If the source type is `aqu`, the routine checks `aqu_d` allocation and source validity, computes a capped withdrawal ratio from `aqu_d(isrc)%stor`, assigns irrigation water volume, updates `cs_irr`, and reduces `aqu_d` and `cs_aqu`; otherwise it assigns the demand directly to `irrig(j)%water%flo`. |
| 8. Handle unlimited-source irrigation. | For any source that is not one of the finite storage branches, the routine leaves the supply unlimited by setting `irrig(j)%water%flo` equal to demand. |
| 9. Convert irrigation volume into applied depth and runoff depth. | Uses the irrigation efficiency and surface-runoff fraction stored in `irrig(j)` to compute final applied water depth and surface runoff depth in millimeters. |
| 10. Return to the caller. | Ends the subroutine after all irrigation bookkeeping fields and source-state updates have been written. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `reservoir_data_module state; no specific candidate reference from this module was resolved in the extracted source.` | `(none resolved)` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(j)%depth` |
| [sym:hydrograph_module] | `irrig, ob, sp_ob, ch_stor, res, aqu` | `irrig(j)%demand, ob(j)%ru(1), sp_ob%hru, ob(iob)%src_tot, ob(iob)%obtyp_out(i), ob(iob)%obtypno_out(i), ch_stor(isrc)%flo, irrig(j)%water, irrig(j)%water%flo, res(isrc)%flo, irrig(j)%applied, irrig(j)%eff, irrig(j)%frac_surq, irrig(j)%runoff` |
| [sym:constituent_mass_module] | `cs_irr, ch_water, res_water, cs_aqu` |  |
| [sym:aquifer_module] | `aqu_d` | `aqu_d(isrc)%stor` |
| [sym:mgt_operations_module] | `mgt_operations_module state; no specific candidate reference from this module was resolved in the extracted source.` | `(none resolved)` |
| [sym:hru_module] | `hru, ihru` | `hru(j)%area_ha, hru(j)%irr_src, hru(j)%irr_isc` |
| [sym:climate_module] | `w` | `w%precip` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `irrig(j)%demand` | After demand calculation, before any source selection. | Set to the positive irrigation volume needed to reach the target ponding depth, reduced by precipitation and scaled by HRU area. |
| `hru(j)%irr_src` | When `ob(j)%ru` is not allocated, or when `hru(j)%irr_src == 'null'`. | Changed to `'unlim'` so the HRU is treated as having an unlimited irrigation source when no routing/source information is available. |
| `irrig(j)%water` | When the source is not a finite channel, reservoir, or aquifer branch, or when a finite branch lacks an allocated source array. | Assigned a direct water amount equal to `irrig(j)%demand` or a scaled hydrologic output object from the selected source; this is the irrigation supply used for the timestep. |
| `cs_irr(isrc)` | When the source branch is channel/stream-depression, reservoir, or aquifer and the source array is valid. | Set to the constituent mass transferred with irrigation water from the selected source, preserving mass balance for the withdrawal. |
| `ch_stor(isrc)` | When the source branch is channel/stream-depression and `ch_stor` is available. | Reduced by the withdrawal ratio so the channel storage reflects water removed for irrigation. |
| `ch_water(isrc)` | When the source branch is channel/stream-depression and `ch_water` is available. | Reduced in proportion to the withdrawal ratio so channel constituent mass remains consistent with the reduced channel volume. |
| `irrig(j)%water%flo` | When a finite source branch sets `irrig(j)%water` and the linked hydrologic output object has a flow component. | Holds the irrigation water volume after source withdrawal or, for fallback cases, the demand volume used to supply irrigation. |
| `res(isrc)` | When the source branch is reservoir and `res` is available. | Reduced by the withdrawal ratio so the reservoir water storage reflects irrigation supply taken from it. |
| `res_water(isrc)` | When the source branch is reservoir and `res_water` is available. | Reduced in proportion to the withdrawal ratio so reservoir constituent mass remains aligned with remaining reservoir water. |
| `aqu_d(isrc)%stor` | When the source branch is aquifer and `aqu_d` is available. | Reduced by the withdrawal ratio so groundwater storage reflects water removed for irrigation. |
| `cs_aqu(isrc)` | When the source branch is aquifer and `cs_aqu` is available. | Reduced in proportion to the groundwater withdrawal so aquifer constituent mass stays consistent with the remaining storage. |
| `irrig(j)%applied` | After `irrig(j)%water%flo` has been determined. | Computed as irrigation water volume per HRU area times irrigation efficiency and the non-runoff fraction, giving the net applied depth in millimeters. |
| `irrig(j)%runoff` | After `irrig(j)%water%flo` has been determined. | Computed as irrigation water volume per HRU area times irrigation efficiency and the surface-runoff fraction, giving irrigation-induced runoff depth in millimeters. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three commits affecting `wet_irrp`: df07e3f added the routine with the wetland/paddy irrigation logic, 39fabde initialized local variables to zero, and e18817a changed the demand formula to subtract precipitation and changed aquifer irrigation to use `aqu_d(isrc)%stor` instead of the commented-out `aqu_d(isrc)%flo` line.

- df07e3f introduced the full `wet_irrp` subroutine, including demand calculation, source selection across channel/reservoir/aquifer branches, constituent transfer updates, and applied/runoff bookkeeping.
- 39fabde only changed local variable declarations by initializing `iob`, `iru`, `isrc`, `wsa1`, `j`, `i`, and `rto` to zero; model behavior was otherwise unchanged.
- e18817a modified the demand formula to subtract `w%precip` and changed the aquifer irrigation volume assignment to use `aqu_d(isrc)%stor` rather than the previously commented `aqu_d(isrc)%flo` expression.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wet_irrp' has no extracted documentation comment.
