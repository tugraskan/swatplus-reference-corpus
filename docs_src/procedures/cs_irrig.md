---
kind: procedure
symbol: cs_irrig
title: cs_irrig
status: filled
source_hash: 999d5ec004e949bc
version_label: SWAT+ 62.0.0
args:
  iwallo: '`iwallo` selects which water-allocation object in `wallo`/`wallod_out` supplies
    the transfer sources and withdrawn irrigation volume for this call.'
  itrn: '`itrn` selects the transfer object within `wallo(iwallo)` and `wallod_out(iwallo)`
    whose source list and withdrawals are processed.'
  ihru: '`ihru` selects the HRU that receives the irrigation water and receives the resulting
    constituent mass update in soil storage or wetland storage.'
locals:
  isrc: Loop counter over the irrigation sources attached to the selected transfer object.
  irrig_nsource: Number of irrigation sources to process for `wallo(iwallo)%trn(itrn)`; the
    source code shows the direct assignment is commented, so its active value depends on setup
    outside this procedure.
  irrig_ob: Source-object number read from the allocation object for the current irrigation
    source.
  ires: Reservoir index used when the current source type is `'res'` and the reservoir storage
    and balance arrays are updated.
  iaq: Aquifer index used when the current source type is `'aqu'` and the aquifer constituent
    storage and balance arrays are updated.
  ichan: Channel index used when the current source type is `'cha'` or `'div'` and channel
    water mass is consulted.
  obnum: Sequential hydrograph/object index derived from `sp_ob1` for the current source type;
    it locates the specific reservoir, aquifer, or channel object in `ob`.
  obnum_chan: Sequential hydrograph/object index for the channel that actually supplies a
    diversion source.
  ics: Loop counter over simulated constituents (`cs_db%num_cs`).
  wetland: Flag read from `hru(ihru)%dbs%surf_stor` to decide whether irrigation constituent
    mass is deposited into wetland storage or into soil.
  irrig_volume: Withdrawn irrigation water volume for the current source; it drives all constituent
    mass calculations.
  mass_diff: Nonnegative amount used to cap computed constituent removal when the source does
    not contain enough mass to satisfy the irrigation withdrawal.
  ion_mass: Constituent mass actually removed from the source and routed to the receiving
    HRU for the current constituent.
  res_mass: Current reservoir constituent mass used as an upper bound when the source is a
    reservoir.
  mass_initial: Temporary snapshot of the starting source constituent mass for the current
    constituent; present in the routine but not used in the visible logic.
  irrig_mass: Constituent mass computed for unlimited outside-basin irrigation before unit
    conversion to an HRU-area basis.
  gw_volume: Estimated groundwater volume in the aquifer, used to convert aquifer mass back
    to concentration after pumping removal.
  cs_conc: Constituent concentration computed from channel water and flow for diversion sources.
uses:
  water_allocation_module: The allocation module provides the transfer-object source list
    and the daily withdrawn volume that drive the whole routine. `cs_irrig` needs the source
    type and source number to choose the correct mass-storage arrays, and it needs the withdrawal
    amount to compute the constituent mass moved with irrigation.
  water_body_module: '`water_body_module` is the source of the water-body state that tells
    this routine how to interpret reservoir, aquifer, channel, and diversion objects as irrigation
    sources. Those object-specific lookups determine which storage array to reduce and which
    hydraulic flow value to use for concentration calculations.'
  aquifer_module: '`aquifer_module` matters because groundwater pumping sources use aquifer
    storage (`aqu_d(iaq)%stor`) to estimate the groundwater volume that underlies constituent
    concentration after irrigation removal.'
  reservoir_data_module: '`reservoir_data_module` supports the reservoir/wetland bookkeeping
    that accompanies irrigation withdrawals. The routine records constituent mass removed
    from a reservoir source and, when the HRU is wetland storage, records the irrigation mass
    into the wetland constituent balance output.'
  hydrograph_module: '`hydrograph_module` matters because the routine uses spatial object
    offsets and channel/reservoir hydrograph flow fields to translate object numbers into
    the correct reservoir, aquifer, channel, or recall object and to compute channel-water
    concentration from flow.'
  hru_module: '`hru_module` matters because the receiving HRU determines whether the irrigation
    mass is stored in wetland water or in the soil profile, and the HRU area converts added
    mass from kg to kg/ha when it is placed in soil.'
  cs_module: '`cs_module` matters because it holds the HRU constituent balance totals that
    are incremented when irrigation mass is applied to soil from surface water sources, groundwater
    sources, or outside-basin water.'
  cs_aquifer: '`cs_aquifer` matters because groundwater irrigation removal is tracked in the
    aquifer constituent balance through the `irr` accumulator when mass is pumped from an
    aquifer source.'
  ch_cs_module: '`ch_cs_module` matters because channel irrigation removal is tracked in the
    channel constituent balance through the `irr` accumulator when mass is withdrawn from
    a stream channel source.'
  res_cs_module: '`res_cs_module` matters because reservoir and wetland irrigation removals
    are tracked in `irrig` so the daily mass balance reflects how much constituent mass left
    the water body with irrigation withdrawals.'
  basin_module: '`basin_module` matters because the `gwflow` control code determines whether
    groundwater irrigation should be handled here or by the groundwater-flow process instead.'
  constituent_mass_module: '`constituent_mass_module` supplies the constituent-count control
    and all of the water-body, soil, wetland, aquifer, channel, and outside-irrigation mass
    arrays that are read and updated in this routine.'
---

<!-- facts:header -->

Transfers constituent mass with irrigation water from reservoirs, aquifers, channels, diversions, or outside-basin sources into an HRU soil profile or wetland. It also subtracts the corresponding mass from the source object and updates daily constituent balance accumulators.

## Bottom Line

`cs_irrig` is the constituent-mass companion to irrigation water allocation. For each irrigation source attached to the allocation transfer, it reads the withdrawn water volume, identifies the source type, computes how much constituent mass that water carries, caps the removal so it cannot exceed source storage, and then routes that mass to either the receiving HRU soil layer or the HRU wetland storage.

The routine matters because it keeps mass accounting consistent across water bodies and receiving landscapes: reservoir, aquifer, channel, diversion, and outside-water irrigation sources all have their stored constituent mass reduced, while daily balance outputs such as `rescs_d`, `acsb_d`, `chcs_d`, `wetcs_d`, and `hcsb_d` are updated to record where the irrigation constituent mass went.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cs_irrig` runs during water-allocation processing after `wallo_control` has identified a transfer with irrigation demand and set up the corresponding `wallo(iwallo)`/`wallod_out(iwallo)` source data. Its results feed the daily constituent mass accounting for reservoirs, aquifers, channels, wetlands, and soil, so later output and balance routines see the irrigation-associated constituent losses and additions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize source, object, and mass-tracking locals, then enter the irrigation-source loop. | The routine starts with the allocation and receiving-HRU indices, initializes counters and temporary mass variables, and prepares to process each source attached to the selected transfer object. |
| 2. Read the current source type, source object number, and withdrawn irrigation volume. | For each source, it extracts the source classification from `wallo(iwallo)%trn(itrn)%src(isrc)` and the actual withdrawn water volume from `wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr`. |
| 3. Skip sources with no irrigation volume and branch by source type. | Only positive withdrawals are processed, and the routine then dispatches to reservoir, aquifer, channel, diversion, or unlimited-source logic based on `irrig_type`. |
| 4. For reservoir sources, remove constituent mass from reservoir storage and add it to the receiving HRU or wetland. | The routine loops over all constituents, computes the mass carried by the withdrawn water, caps it to the reservoir's stored mass, subtracts it from `res_water(ires)%cs(ics)`, records the removal in `rescs_d`, and deposits the mass into either `wet_water`/`wetcs_d` or `cs_soil`/`hcsb_d` depending on the HRU wetland flag. |
| 5. For aquifer sources, remove mass from aquifer storage, update aquifer balance, and refresh concentration. | When groundwater flow is not active, the routine treats the source as an aquifer withdrawal, computes pumped constituent mass from aquifer concentration, caps removal to available aquifer mass, subtracts it from `cs_aqu`, records the withdrawal in `acsb_d`, adds the mass to the receiving HRU or wetland, and recalculates aquifer concentration from remaining storage and groundwater volume. |
| 6. For stream-channel sources, remove mass from channel water when channel flow is sufficient. | The routine maps the source object to a channel object, requires the channel flow at `ob(obnum)%hd(1)%flo` to exceed the threshold, computes constituent mass from channel concentration and withdrawn volume, then updates `ch_water`, `chcs_d`, and the receiving HRU or wetland mass stores. |
| 7. For canal-diversion sources, trace the diversion back to the supplying channel and apply the same receiving-side mass update. | The routine uses the recall object to find the source channel, checks that the connected channel has enough flow, derives concentration from the channel-water storage and flow, computes the irrigation mass, and adds it to wetland or soil while updating the HRU balance. |
| 8. For unlimited outside-basin sources, compute irrigation mass directly from irrigation-water concentration and apply it to the receiving HRU. | The routine multiplies outside irrigation concentration by withdrawn volume to get mass, converts it to a per-hectare amount, and updates wetland storage or soil and the corresponding HRU balance accumulator. |
| 9. Finish the source loop and return to the caller. | After all sources are processed, the subroutine exits without calling any other routines. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `wallo, wallod_out` | `wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr` |
| [sym:water_body_module] | `sp_ob1, ob` | `sp_ob1%aqu, sp_ob1%chandeg, sp_ob1%recall, ob(obnum)%area_ha, ob(obnum)%num, ob(obnum)%hd(1)%flo, ob(obnum)%obtypno_out(1), ob(obnum_chan)%hd(1)%flo` |
| [sym:aquifer_module] | `aqu_d` | `aqu_d(iaq)%stor` |
| [sym:reservoir_data_module] | `rescs_d, wetcs_d` | `rescs_d(ires)%cs(ics)%irrig, wetcs_d(ihru)%cs(ics)%irrig` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%aqu, ob(obnum)%area_ha, sp_ob1%chandeg, ob(obnum)%num, ob(obnum)%hd(1)%flo, sp_ob1%recall, ob(obnum)%obtypno_out(1), ob(obnum_chan)%hd(1)%flo` |
| [sym:hru_module] | `hru` | `hru(ihru)%dbs%surf_stor, hru(ihru)%area_ha` |
| [sym:cs_module] | `hcsb_d` | `hcsb_d(ihru)%cs(ics)%irsw, hcsb_d(ihru)%cs(ics)%irgw, hcsb_d(ihru)%cs(ics)%irwo` |
| [sym:cs_aquifer] | `acsb_d` | `acsb_d(iaq)%cs(ics)%irr` |
| [sym:ch_cs_module] | `chcs_d` | `chcs_d(ichan)%cs(ics)%irr` |
| [sym:res_cs_module] | `rescs_d, wetcs_d` | `rescs_d(ires)%cs(ics)%irrig, wetcs_d(ihru)%cs(ics)%irrig` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:constituent_mass_module] | `cs_db, res_water, wet_water, cs_soil, cs_aqu, ch_water, cs_irr` | `cs_db%num_cs, res_water(ires)%csc(ics), res_water(ires)%cs(ics), wet_water(ihru)%cs(ics), cs_soil(ihru)%ly(1)%cs(ics), cs_aqu(iaq)%cs(ics), cs_aqu(iaq)%csc(ics), ch_water(ichan)%cs(ics), cs_irr(ihru)%csc(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `irrig_type` | When a source is processed, `irrig_type` is assigned from `wallo(iwallo)%trn(itrn)%src(isrc)%typ` for that source. | The routine uses this value to decide which water-body path to follow: reservoir, aquifer, channel, diversion, or unlimited outside-basin water. |
| `res_water(ires)%cs(ics)` | For reservoir sources with positive irrigation volume. | `res_water(ires)%cs(ics)` is reduced by the constituent mass carried with the withdrawn water, so reservoir stored constituent mass matches the irrigation export. |
| `rescs_d(ires)%cs(ics)%irrig` | For reservoir sources with positive irrigation volume. | `rescs_d(ires)%cs(ics)%irrig` increases by the same constituent mass removed from the reservoir, preserving the daily reservoir mass-balance record. |
| `wet_water(ihru)%cs(ics)` | For reservoir, aquifer, channel, diversion, or unlimited sources when the receiving HRU is flagged as wetland storage. | `wet_water(ihru)%cs(ics)` is increased by the irrigation-associated constituent mass instead of placing that mass into the soil profile. |
| `wetcs_d(ihru)%cs(ics)%irrig` | For reservoir, aquifer, channel, diversion, or unlimited sources when the receiving HRU is flagged as wetland storage. | `wetcs_d(ihru)%cs(ics)%irrig` is increased so the wetland daily constituent balance records irrigation-derived additions. |
| `cs_soil(ihru)%ly(1)%cs(ics)` | For reservoir, aquifer, channel, diversion, or unlimited sources when the receiving HRU is not a wetland. | `cs_soil(ihru)%ly(1)%cs(ics)` is increased by the applied constituent mass per unit area, reflecting deposition into the top soil layer. |
| `hcsb_d(ihru)%cs(ics)%irsw` | For reservoir sources when the receiving HRU is not a wetland. | `hcsb_d(ihru)%cs(ics)%irsw` is increased to record soil-profile constituent input from surface-water irrigation. |
| `cs_aqu(iaq)%cs(ics)` | For aquifer sources with positive irrigation volume and `bsn_cc%gwflow.eq.0`. | `cs_aqu(iaq)%cs(ics)` is reduced by the pumped constituent mass, so aquifer storage reflects the irrigation withdrawal. |
| `acsb_d(iaq)%cs(ics)%irr` | For aquifer sources with positive irrigation volume and `bsn_cc%gwflow.eq.0`. | `acsb_d(iaq)%cs(ics)%irr` is increased to record the aquifer mass removed via irrigation pumping. |
| `hcsb_d(ihru)%cs(ics)%irgw` | For aquifer sources when the receiving HRU is not a wetland. | `hcsb_d(ihru)%cs(ics)%irgw` is increased to record groundwater irrigation mass applied to the soil profile. |
| `cs_aqu(iaq)%csc(ics)` | For aquifer sources after storage is reduced. | `cs_aqu(iaq)%csc(ics)` is recalculated from the remaining aquifer mass and groundwater volume so later uses see the updated concentration. |
| `ch_water(ichan)%cs(ics)` | For channel sources with `ob(obnum)%hd(1)%flo > 10.`. | `ch_water(ichan)%cs(ics)` is reduced by the constituent mass withdrawn with channel irrigation, preserving channel-water storage consistency. |
| `chcs_d(ichan)%cs(ics)%irr` | For channel sources with `ob(obnum)%hd(1)%flo > 10.`. | `chcs_d(ichan)%cs(ics)%irr` is increased to record the mass removed from the channel by irrigation. |
| `hcsb_d(ihru)%cs(ics)%irwo` | For unlimited outside-basin irrigation when the HRU is not a wetland. | `hcsb_d(ihru)%cs(ics)%irwo` is increased to record irrigation mass applied from outside the watershed. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four behavior-relevant changes in `cs_irrig`: the routine was first imported as a Bitbucket source drop with the core reservoir/aquifer/channel/diversion/unlimited irrigation mass-routing logic; later it was renamed from `idmd` to `itrn` and switched from `dmd`/`src_ob` access to the new `trn`/`src` allocation structure; a subsequent compile fix changed the imported aquifer module name to `cs_aquifer_module`; and a later cleanup removed unused hydrograph imports plus two unused real locals and replaced the final bare `end` with `end subroutine cs_irrig`.

- c7c8e22 introduced the initial `cs_irrig` implementation that routes irrigation constituent mass from reservoirs, aquifers, channels, diversions, and unlimited sources into HRU soil or wetland storage and records the corresponding balance terms.
- 23142ed updated `cs_irrig` to the new water-allocation data model by renaming the demand argument to `itrn` and switching source lookups and withdrawal reads from `dmd/src_ob` to `trn/src` and `wallod_out(... )%trn(... )%src(... )%withdr`.
- 2405a68 changed the imported aquifer module reference used by `cs_irrig` from `cs_aquifer` to `cs_aquifer_module`, resolving a compile-time module-name mismatch.
- 2ee1889 removed unused `irrig` and `res` imports, deleted the unused `irrig_total` and `irrig_fraction` locals, and made the procedure ending explicit with `end subroutine cs_irrig`.
- c639a8c reverted the aquifer module import name back from `cs_aquifer_module` to `cs_aquifer`, restoring the earlier module reference used by the procedure.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_irrig' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into 9 model-level steps from the draft's 8 block summaries, using visible line ranges from the source block.
- Some lineage text is based on resolved diffs only; where commit messages were broader than the visible patch, only the actual changed lines were described.
