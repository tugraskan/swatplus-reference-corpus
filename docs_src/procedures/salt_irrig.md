---
kind: procedure
symbol: salt_irrig
title: salt_irrig
status: filled
source_hash: 8e8f71dab8ea28af
version_label: SWAT+ 62.0.0
args:
  iwallo: Index of the water-allocation object whose transfer sources are being processed;
    it selects the allocation record in wallo/wallod_out that supplies irrigation source type,
    source number, and withdrawn volume.
  itrn: Index of the transfer object within the water-allocation object; it identifies which
    trn() record in wallo and wallod_out contains the irrigation sources for this call.
  ihru: Index of the receiving HRU; it selects the destination HRU state, including soil,
    wetland, irrigation-water constituent storage, and HRU salt-balance outputs.
locals:
  isrc: Loop counter over the irrigation sources attached to the selected transfer object.
  irrig_nsource: Number of irrigation sources to process for the selected transfer object;
    it controls the source loop, though the current source line shows the assignment commented
    out.
  irrig_ob: Source-object number for the current irrigation source, read from wallo(iwallo)%trn(itrn)%src(isrc)%num
    and used to locate the reservoir, aquifer, channel, recall, or other source.
  ires: Reservoir index derived from irrig_ob when the source type is reservoir; it addresses
    reservoir water and reservoir salt-budget arrays.
  iaq: Aquifer index derived from irrig_ob when the source type is aquifer; it addresses aquifer
    water, concentration, and aquifer salt-budget arrays.
  ichan: Channel index used when the source type is a stream channel or a diverted canal source;
    it addresses channel water and channel salt-budget arrays.
  obnum: Sequential object index in ob() for the current source object; it is used to reach
    hydrologic object metadata and daily flow storage.
  obnum_chan: Sequential object index in ob() for the channel object associated with a diversion
    source; it is used when the diverted water comes from a channel behind a recall object.
  isalt: Loop counter over the simulated salt ions in cs_db%num_salts.
  wetland: Flag copied from hru(ihru)%dbs%surf_stor to test whether the destination HRU is
    a wetland rather than a normal soil profile.
  irrig_volume: Withdrawn irrigation-water volume for the current source, read from wallod_out
    and used to convert source concentration into salt mass.
  mass_diff: Overflow correction that removes any mass above what the source actually contains
    before subtracting salt from the source store.
  ion_mass: Calculated salt mass moved with the current irrigation withdrawal; it is clipped
    so it never exceeds the source storage and then transferred to the destination and salt-balance
    outputs.
  res_mass: Reservoir salt mass available before withdrawal, used as the cap when computing
    how much salt can be removed from a reservoir source.
  mass_initial: Temporary copy of the source salt mass before adjustment; it is used in aquifer
    and channel branches as a baseline check for the computed withdrawal mass.
  irrig_mass: Computed salt mass for the unlimited/outside-watershed source type; it converts
    irrigation-water concentration to delivered salt mass per HRU area.
  gw_volume: Computed groundwater volume for the aquifer source branch; it is used to convert
    aquifer mass back to concentration after withdrawal.
  salt_conc: Temporary concentration of channel water used in the diversion branch to convert
    diverted irrigation volume into salt mass.
uses:
  water_allocation_module: water_allocation_module provides the transfer-source definition
    and the matching output record. salt_irrig reads the source type and source number from
    wallo(iwallo)%trn(itrn)%src(isrc) and the withdrawn amount from wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr
    so it can decide which source branch to process and how much salt to move.
  water_body_module: water_body_module is imported in this routine because the source branches
    need shared water-body metadata and routing context that are not confined to a single
    HRU. The actual references visible here are the hydrologic object indices and flows used
    to identify aquifer, channel, and recall-linked diversion sources and to compute groundwater
    volume or channel concentration from object geometry and discharge.
  aquifer_module: aquifer_module matters because the aquifer branch converts withdrawn groundwater
    salt mass back to concentration using aqu_d(iaq)%stor. Without aquifer storage, the routine
    could not update cs_aqu(iaq)%saltc consistently after removing salt for irrigation.
  reservoir_data_module: reservoir_data_module is the reservoir-state companion to the reservoir
    branch. salt_irrig updates the reservoir irrigation salt flux in ressalt_d so the reservoir
    salt balance records salt removed by irrigation, and it uses the wetland output array
    wetsalt_d when the receiving HRU is a wetland.
  hydrograph_module: hydrograph_module supplies the object indices and daily flows needed
    to map irrigation sources to physical routing objects. salt_irrig uses sp_ob1 and ob()
    to find the aquifer, channel, recall, and diversion object numbers and to check whether
    a channel has enough flow to support salt withdrawal calculations.
  hru_module: hru_module matters because the destination HRU provides the receiving land area
    and wetland-storage flag. salt_irrig uses hru(ihru)%dbs%surf_stor to decide whether to
    place salt in wetland water storage or in the first soil layer, and hru(ihru)%area_ha
    to convert mass to kg/ha for soil-balance updates.
  salt_module: salt_module matters because it stores the HRU soil salt-balance accumulators
    that this routine increments when irrigation salts are applied to normal land. The irsw
    and irgw fields track salt added to soil by surface-water and groundwater irrigation,
    and irwo tracks salt from outside-watershed irrigation.
  salt_aquifer: salt_aquifer matters because it stores the aquifer salt-balance accumulator
    for irrigation withdrawals. salt_irrig increments asaltb_d(iaq)%salt(isalt)%irr when groundwater
    salt is removed for irrigation.
  ch_salt_module: ch_salt_module matters because it stores the channel salt-balance accumulator
    for irrigation withdrawals. salt_irrig increments chsalt_d(ichan)%salt(isalt)%irr when
    channel water salt is removed for irrigation.
  res_salt_module: res_salt_module matters because it stores the reservoir and wetland salt-balance
    accumulators associated with irrigation diversions. salt_irrig increments ressalt_d for
    reservoir withdrawals and wetsalt_d when irrigation salt is routed to wetland HRUs.
  basin_module: basin_module matters because bsn_cc%gwflow determines whether the aquifer
    irrigation branch is active here. When gwflow is enabled, groundwater pumping salt accounting
    is handled elsewhere, so this routine skips the aquifer branch.
  constituent_mass_module: constituent_mass_module matters because it holds the simulation-wide
    salt-count control and the concentration/mass storage arrays for every source and destination
    object. salt_irrig uses cs_db%num_salts to loop over salts and updates res_water, wet_water,
    cs_soil, cs_aqu, ch_water, and cs_irr to move salt mass consistently with irrigation water.
---

<!-- facts:header -->

Routes salt mass with irrigation water from reservoirs, aquifers, channels, diversions, or outside sources into an HRU. It updates source-object and destination salt budgets for soil, wetlands, aquifers, reservoirs, and channels.

## Bottom Line

salt_irrig is the salt-accounting companion to irrigation allocation. For each irrigation source attached to a water-allocation transfer, it uses the withdrawn water volume and the source type to estimate how much salt leaves the source and how much salt is added to the receiving HRU.

The routine splits that salt into the appropriate destination budget: wetland water storage, surface-soil salt balance, groundwater salt concentration, reservoir salt balances, or channel salt balances. It matters because irrigation water can move both water and dissolved salts between model objects, and this routine keeps those mass balances consistent.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from wallo_control after irrigation water has already been allocated and the withdrawn volume has been written to wallod_out. wallo_control passes the allocation object, transfer object, and receiving HRU so salt_irrig can convert irrigation withdrawal into salt transfer, and later daily salt and constituent balance reporting depends on the updated source and destination state it leaves behind.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize source-loop context from the water-allocation transfer. | The routine determines how many irrigation sources to process, then for each source reads the source type and source object number from wallo and the withdrawn water volume from wallod_out. |
| 2. Process reservoir irrigation withdrawals. | If the source is a reservoir and irrigation volume is positive, the routine converts reservoir concentration to salt mass, limits that mass to what the reservoir actually contains, subtracts it from res_water, records the reservoir irrigation loss in ressalt_d, and adds the same mass to wetland water or HRU soil salt balances. |
| 3. Process aquifer irrigation withdrawals when groundwater flow is inactive. | For aquifer sources with gwflow disabled, the routine converts aquifer concentration to mass, caps the mass by aquifer storage, subtracts it from cs_aqu, records the loss in asaltb_d, adds it to the receiving wetland or soil salt balance, and recomputes aquifer concentration from remaining storage. |
| 4. Compute the groundwater volume used to reset aquifer concentration. | The routine derives an effective groundwater volume from aquifer storage and the aquifer object area; if volume remains, it updates cs_aqu concentration from remaining mass, otherwise it zeroes mass and concentration. |
| 5. Process irrigation withdrawals from stream channels. | For channel sources, the routine maps the source to a channel object, checks that channel flow is large enough, converts channel concentration and irrigation volume to salt mass, subtracts that mass from ch_water, records the channel loss in chsalt_d, and adds the salt to wetland or soil balance arrays. |
| 6. Process canal-diversion sources linked through recall objects. | For diversion sources, the routine finds the source channel through the recall object, checks the diverted channel flow, computes channel-water concentration, and adds the resulting salt mass to the destination HRU and its salt-balance arrays. |
| 7. Process unlimited outside-watershed irrigation sources. | For unlimited sources, the routine converts irrigation-water concentration in cs_irr to delivered salt mass, scales it by HRU area, and adds it to wetland water or soil surface salt and the corresponding irrigation salt-balance term. |
| 8. Finish the source loop and return to the caller. | After all irrigation-source branches are handled for the current transfer, the routine ends the source loop and returns control to wallo_control. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `wallo, wallod_out` | `wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr` |
| [sym:water_body_module] | `sp_ob1, ob` | `sp_ob1%aqu, ob(obnum)%area_ha, sp_ob1%chandeg, ob(obnum)%num, ob(obnum)%hd(1)%flo, sp_ob1%recall, ob(obnum)%obtypno_out(1), ob(obnum_chan)%hd(1)%flo` |
| [sym:aquifer_module] | `aqu_d` | `aqu_d(iaq)%stor` |
| [sym:reservoir_data_module] | `ressalt_d, wetsalt_d` | `ressalt_d(ires)%salt(isalt)%irrig, wetsalt_d(ihru)%salt(isalt)%irrig` |
| [sym:hydrograph_module] | `sp_ob1, ob` | `sp_ob1%aqu, ob(obnum)%area_ha, sp_ob1%chandeg, ob(obnum)%num, ob(obnum)%hd(1)%flo, sp_ob1%recall, ob(obnum)%obtypno_out(1), ob(obnum_chan)%hd(1)%flo` |
| [sym:hru_module] | `hru` | `hru(ihru)%dbs%surf_stor, hru(ihru)%area_ha` |
| [sym:salt_module] | `hsaltb_d` | `hsaltb_d(ihru)%salt(isalt)%irsw, hsaltb_d(ihru)%salt(isalt)%irgw, hsaltb_d(ihru)%salt(isalt)%irwo` |
| [sym:salt_aquifer] | `asaltb_d` | `asaltb_d(iaq)%salt(isalt)%irr` |
| [sym:ch_salt_module] | `chsalt_d` | `chsalt_d(ichan)%salt(isalt)%irr` |
| [sym:res_salt_module] | `ressalt_d, wetsalt_d` | `ressalt_d(ires)%salt(isalt)%irrig, wetsalt_d(ihru)%salt(isalt)%irrig` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:constituent_mass_module] | `cs_db, res_water, wet_water, cs_soil, cs_aqu, ch_water, cs_irr` | `cs_db%num_salts, res_water(ires)%saltc(isalt), res_water(ires)%salt(isalt), wet_water(ihru)%salt(isalt), cs_soil(ihru)%ly(1)%salt(isalt), cs_aqu(iaq)%salt(isalt), cs_aqu(iaq)%saltc(isalt), ch_water(ichan)%salt(isalt), cs_irr(ihru)%saltc(isalt)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `irrig_type` | When irrig_type is set to reservoir source ('res') and irrig_volume > 0 for the current source. | The routine does not directly change an irrig_type variable value; it uses the current source type to select the reservoir branch and drive all downstream reservoir salt accounting. |
| `res_water(ires)%salt(isalt)` | Inside the reservoir branch for each salt ion, after ion_mass is limited to the available reservoir mass. | The reservoir salt storage is reduced by the salt mass carried with the irrigation withdrawal so the reservoir water store reflects the removed dissolved salt. |
| `ressalt_d(ires)%salt(isalt)%irrig` | Inside the reservoir branch for each salt ion, after the same ion_mass is removed from reservoir storage. | The reservoir irrigation salt-balance accumulator is increased by the amount removed, preserving the daily accounting of salt exported by irrigation from the reservoir. |
| `wet_water(ihru)%salt(isalt)` | Whenever the receiving HRU is marked as a wetland, in any source branch that delivers irrigation salt. | The wetland water salt storage is increased by the delivered irrigation salt mass instead of placing that mass into the soil profile. |
| `wetsalt_d(ihru)%salt(isalt)%irrig` | Whenever the receiving HRU is marked as a wetland, in any source branch that delivers irrigation salt. | The wetland irrigation salt-balance accumulator is increased by the delivered mass so wetland salt accounting records the irrigation input. |
| `cs_soil(ihru)%ly(1)%salt(isalt)` | When the receiving HRU is not a wetland and irrigation salt is delivered from reservoir, aquifer, channel, or unlimited source branches. | The salt mass is added to the first soil layer of the HRU, expressed on an area basis in kg/ha. |
| `hsaltb_d(ihru)%salt(isalt)%irsw` | When the receiving HRU is not a wetland and irrigation salt is delivered from reservoir, aquifer, or channel branches. | The soil salt balance records salt added via surface-water irrigation so the HRU-level salt budget remains consistent. |
| `cs_aqu(iaq)%salt(isalt)` | Inside the aquifer branch after ion_mass is limited by available aquifer salt. | Aquifer dissolved salt storage is reduced by the irrigation withdrawal so the remaining aquifer mass matches the exported salt. |
| `asaltb_d(iaq)%salt(isalt)%irr` | Inside the aquifer branch after ion_mass is removed from cs_aqu. | The aquifer irrigation salt-balance accumulator records the salt mass pumped out for irrigation. |
| `hsaltb_d(ihru)%salt(isalt)%irgw` | When the receiving HRU is not a wetland and the source is an aquifer with gwflow inactive. | The HRU soil salt-balance term for groundwater irrigation is increased by the delivered mass on an area basis. |
| `cs_aqu(iaq)%saltc(isalt)` | At the end of each aquifer-ion loop after aquifer mass is updated. | The aquifer concentration is recalculated from remaining salt mass and groundwater volume so downstream users see a consistent dissolved-salt concentration. |
| `ch_water(ichan)%salt(isalt)` | Inside the channel-source branch when channel flow is greater than 10 and salt mass is removed for irrigation. | Channel water salt storage is reduced by the mass exported to irrigation, keeping the channel dissolved-salt store consistent with the withdrawal. |
| `chsalt_d(ichan)%salt(isalt)%irr` | Inside the channel-source branch after channel salt is removed from ch_water. | The channel irrigation salt-balance accumulator is increased by the removed mass so channel salt output tracks irrigation losses. |
| `hsaltb_d(ihru)%salt(isalt)%irwo` | When the receiving HRU is not a wetland and the source is an unlimited outside-watershed irrigation source. | The soil salt balance records salt delivered from outside the watershed through irrigation water that is not tied to a reservoir, aquifer, or channel source. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved source-backed lineage shows four relevant commits. 94b6dec added the salt_irrig subroutine to the source tree with the full irrigation-source salt accounting logic. c639a8c reverted a transient change to the salt_aquifer module use statement, restoring use salt_aquifer. 39fabde initialized local counters and salt-mass variables to zero and kept the source-selection logic aligned with the newer water-allocation transfer fields. 29e2d36 updated the routine to use itrn instead of idmd, switched the source lookups from dmd/src_ob to trn/src, and changed the withdrawn-volume lookup to wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr.

- 94b6dec introduced salt_irrig as a new irrigation salt-accounting routine with branches for reservoirs, aquifers, channels, diversions, and unlimited outside sources.
- c639a8c restored the original salt_aquifer module import, which kept the routine tied to the available salt-aquifer state instead of the temporary module-name change.
- 39fabde zero-initialized the loop indices and mass variables and kept the irrigation-source lookup on the transfer-object path that the routine uses now.
- 29e2d36 renamed the transfer argument to itrn and migrated all source lookups from the older demand-object fields to wallo(iwallo)%trn(itrn)%src(isrc) and wallod_out(iwallo)%trn(itrn)%src(isrc)%withdr.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_irrig' has no extracted documentation comment.
