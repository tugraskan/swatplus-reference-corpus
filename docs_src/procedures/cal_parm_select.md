---
kind: procedure
symbol: cal_parm_select
title: cal_parm_select
status: filled
source_hash: 711e9a359c6d520a
version_label: SWAT+ 62.0.0
args:
  ielem: '`ielem` selects the target element being calibrated: the HRU, soil profile, basin
    object, channel, reservoir, aquifer, LTE unit, or other indexed object that receives the
    change in the matching `case` branch.'
  ly: '`ly` selects the layer or subentry to update when the chosen parameter is layer-specific,
    such as soil layers, carbon layers, reservoir decision-table actions, or other layered
    databases.'
  chg_parm: '`chg_parm` is the calibration parameter name. Its value drives the `select case`
    dispatch so the routine knows which state variable to update.'
  chg_typ: '`chg_typ` selects how the new value is computed by `chg_par`, such as absolute
    replacement, additive change, percent change, or relative change.'
  chg_val: '`chg_val` is the user-supplied change amount passed to `chg_par`; it is interpreted
    according to `chg_typ` and becomes the candidate new value.'
  absmin: '`absmin` is the lower bound passed to `chg_par` so the updated parameter does not
    fall below the allowed minimum.'
  absmax: '`absmax` is the upper bound passed to `chg_par` so the updated parameter does not
    exceed the allowed maximum.'
  num_db: '`num_db` identifies the calibration database entry that produced this request;
    the routine does not use it for control flow here, beyond the dummy guard that suppresses
    an unused-argument warning.'
locals:
  jj: Loop counter for soil layers when the routine needs to scan all layers, such as finding
    the tile-drain layer or updating per-layer soil properties.
  ipl: Loop counter for plant entries within a plant community when the routine propagates
    an HRU-level plant parameter to each crop status record.
  ihru: Loop counter over HRUs used when a basin-wide parameter change must update per-HRU
    derived values such as `brt`.
  icell: Loop counter over groundwater-connected cells or connections when a calibration case
    must update each connected cell entry.
  ichan: Declared as a channel counter; it is not used in the shown source, but it exists
    for channel-related parameter logic in this routine.
  exp: Temporary real used for exponential transforms in some parameter formulas; in the shown
    code it is declared but not directly used.
  c_val: Temporary scaled change value, used when a case needs to adjust the requested change
    before passing it to `chg_par` (for example LTE AWC scaling by soil depth).
  abmax: Temporary adjusted upper bound used when a case rescales the permissible range before
    calling `chg_par`.
  chg_par: Local real that stores the new parameter value returned by the external `chg_par`
    routine, separate from the external procedure of the same name.
  perc_ln_func: Temporary helper value used to convert percolation into a limiting coefficient
    in the `perco` branch.
  rock: Temporary factor computed from soil rock content and reused when updating USLE multiplier
    values.
uses:
  basin_module: '`basin_module` provides basin-wide parameters such as `bsn_prm%plaps`, `bsn_prm%tlaps`,
    `bsn_prm%surlag`, `bsn_prm%adj_pkr`, `bsn_prm%prf`, and `bsn_prm%evrch`, which this routine
    can update directly when `chg_parm` names a basin calibration target. Those values affect
    basin-scale routing, peak flow, and lapse-rate behavior, so they belong in this dispatcher.'
  channel_data_module: '`channel_data_module` is used because this routine includes channel-related
    calibration branches, even though no specific candidate reference from that module was
    resolved in the context packet. It matters here as part of the calibration dispatch environment
    for channel data objects.'
  reservoir_data_module: '`reservoir_data_module` matters because the routine includes reservoir
    calibration cases that need reservoir data objects and parameters, even though no specific
    reference from this module was resolved in the context packet.'
  hru_module: '`hru_module` supplies the HRU arrays and nested state updated by the most common
    calibration cases. The selected HRU index `ielem` is used to change hydrology, land use
    management, snow, field, drainage, and nutrient parameters that later runoff, erosion,
    and plant-growth routines read from `hru(ielem)`.'
  soil_module: '`soil_module` provides the soil profile and layer arrays that are recalibrated
    when soil depth, bulk density, water capacity, conductivity, texture, or chemistry parameters
    change. These values control soil-water initialization, erosion factors, and layer-dependent
    hydrology for `soil(ielem)`.'
  channel_module: '`channel_module` matters because this routine contains channel calibration
    branches and must be able to update channel-related model state when a matching parameter
    name is selected.'
  conditional_module: '`conditional_module` matters because conditional calibration actions
    can invoke this dispatcher, and the routine must fit into the same calibration-selection
    workflow as other conditional state updates.'
  sd_channel_module: '`sd_channel_module` matters because the routine updates stream-channel
    geometry, sediment, and nutrient calibration values in `sd_ch(ielem)`. Those channel-state
    objects live in this module and are part of the routed channel response.'
  reservoir_module: '`reservoir_module` matters because reservoir calibration cases update
    live reservoir state and sediment/nutrient parameters stored in reservoir objects. The
    dispatcher needs those objects available to write the new values back into the model.'
  aquifer_module: '`aquifer_module` matters because groundwater calibration cases update aquifer
    storages, hydraulic properties, and derived values through `aqu_dat`, `aqu_d`, `aqu_prm`,
    and related state. Those are the source of subsurface response that later hydrology uses.'
  hru_lte_module: '`hru_lte_module` matters because LTE calibration cases update long-term
    HRU database values such as curve number, soil depth, slope, and related parameters. These
    values drive LTE-specific calibration behavior in the same dispatcher.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides the layered soil carbon
    and mineral-pool state (`soil1(ielem)%tot(ly)%c`) that is updated by carbon calibration
    cases such as `cbn`, `lab_p`, and `hum_c_*`. Those values feed the carbon balance and
    soil pool initialization logic.'
  hydrograph_module: '`hydrograph_module` provides `sp_ob%hru`, which the routine uses to
    loop over HRUs when a basin-wide parameter like `surlag` changes. That count determines
    how many `brt` values must be recomputed after the basin lag update.'
  pesticide_data_module: '`pesticide_data_module` matters because the routine has pesticide
    calibration branches (`pst_*`) that update pesticide database parameters used by fate,
    transport, and decay calculations.'
  plant_module: '`plant_module` matters because the routine updates both the plant-community
    count `pcom(ielem)%npl` and the per-crop `epco` value in `pcom(ielem)%plcur(ipl)%epco`
    when the HRU plant compensation factor changes. That keeps each plant status record synchronized
    with the HRU-level setting.'
  plant_data_module: '`plant_data_module` matters because this routine changes plant database
    values such as `pldb(ielem)%usle_c`, which are used in erosion and crop parameterization
    for the selected plant entry.'
  gwflow_module: '`gwflow_module` matters because the aquifer, stream, floodplain, and pond
    calibration branches update groundwater-flow state and derived coefficients in that module
    when GW flow is enabled.'
  carbon_module: '`carbon_module` matters because the routine updates carbon-model control
    fractions, rates, and allocation coefficients when the chosen calibration parameter belongs
    to the carbon submodel.'
  tillage_data_module: '`tillage_data_module` matters because the routine includes tillage
    and biomixing curve-fit coefficients that are stored as module-level calibration parameters
    and used by tillage/biomix behavior later in the model.'
---

<!-- facts:header -->

Selects and applies a requested calibration change to one parameter or state value in the appropriate SWAT+ object. It also recomputes a few dependent values, such as curve number and soil/tile coefficients, when the chosen parameter affects them.

## Bottom Line

`cal_parm_select` is the central dispatcher that applies a user-requested calibration change identified by `chg_parm` to the correct model object for the selected element `ielem` (and layer `ly` where needed). It uses `chg_typ`, `chg_val`, `absmin`, and `absmax` through `chg_par` to compute the updated value, then writes that value back into HRU, soil, basin, channel, reservoir, aquifer, LTE, pesticide, plant, carbon, and groundwater state as appropriate.

Some parameters trigger follow-on recalculation of dependent state. For example, curve-number updates call `curno`, soil texture/physical edits call `soil_awc_init` or `soil_text_init`, basin lag updates refresh `brt`, and several GW-flow and reservoir settings update derived coefficients immediately after the primary parameter change.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration-condition handling after `cal_conditions` has determined that a change should be applied and has supplied the target element index, layer index, parameter name, change type, and bounds. Its results immediately alter model state used later by runoff, erosion, soil-water, plant, reservoir, aquifer, groundwater-flow, and carbon calculations, depending on which `chg_parm` branch is selected.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set up calibration context and suppress unused-argument warnings. | Imports the state modules used by the dispatcher, declares the change-control arguments and locals, and ignores `num_db` if it is negative so the compiler does not warn about the unused argument. |
| 2. Dispatch on the requested calibration parameter name. | Starts the `select case` on `chg_parm`, which routes control to the branch for the requested parameter name. |
| 3. Update HRU and plant-related parameters. | Uses `chg_par` to update HRU hydrology, land use, and plant-related state such as curve number, `biomix`, `usle_p`, `ovn`, slope and lateral-flow parameters, canopy storage, erosion ratios, percolation, and plant compensation factors; some cases also propagate the new value to each crop in `pcom(ielem)%plcur`. |
| 4. Update field, snow, and tile-drain parameters. | Applies change rules to field geometry, snowmelt parameters, and tile-drain properties. The tile-depth branch also searches soil layers to set `hru(ielem)%lumv%ldrain`, and the tile-time branch derives `tile_ttime` from lag and drain presence. |
| 5. Update soil-profile and soil-layer parameters. | Changes soil exclusion, crack, depth, bulk density, AWC, conductivity, carbon, texture, albedo, EC, calcium, and pH values. Depth, bulk density, AWC, and clay edits trigger soil initialization helpers, and rock/usle edits refresh the HRU USLE multiplier. |
| 6. Update HRU nutrient, basin, carbon, and carbon-layer parameters. | Changes nutrient coefficients, basin-wide lag and evap parameters, carbon control fractions, carbon rates, carbon allocation factors, and carbon-relevant plant parameters. Basin lag also recomputes `brt` for every HRU using `sp_ob%hru`. |
| 7. Update channel, pesticide, reservoir, and channel-sediment parameters. | Applies calibration changes to channel nutrient kinetics, pesticide database properties, stream-channel geometry and sediment parameters, and reservoir hydrology, sediment, and nutrient settings. Reservoir and decision-table branches also recompute derived reservoir coefficients where needed. |
| 8. Update reservoir, aquifer, LTE, groundwater-flow, and soil carbon pools. | Handles decision-table reservoir actions, aquifer initial conditions, LTE properties, groundwater-flow parameters, and final soil carbon/mineral pool parameters. Some branches convert units or derive secondary state immediately after the primary parameter change. |
| 9. Recompute dependent state after selected edits. | Calls `curno`, `soil_awc_init`, or `soil_text_init` in the branches that need derived-state refresh so subsequent model calculations see consistent runoff and soil-property state. |
| 10. Return to caller after the selected state update is complete. | Ends the `select case` and returns control to the calibration workflow with the targeted state updated in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%plaps, bsn_prm%tlaps, bsn_prm%surlag, bsn_prm%adj_pkr, bsn_prm%prf, bsn_prm%evrch` |
| [sym:channel_data_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:reservoir_data_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:hru_module] | `hru` | `hru(ielem)%hyd%biomix, hru(ielem)%tiledrain, hru(ielem)%hyd%cn3_swf, hru(ielem)%lumv%usle_p, hru(ielem)%luse%ovn, hru(ielem)%topo%elev, hru(ielem)%topo%slope, hru(ielem)%topo%slope_len, hru(ielem)%hyd%lat_ttime, hru(ielem)%hyd%lat_sed, hru(ielem)%topo%lat_len, hru(ielem)%hyd%latq_co, hru(ielem)%hyd%canmx, hru(ielem)%hyd%esco, hru(ielem)%hyd%epco, hru(ielem)%hyd%erorgn, hru(ielem)%hyd%erorgp, hru(ielem)%topo%dis_stream, hru(ielem)%hyd%perco, hru(ielem)%hyd%perco_lim, hru(ielem)%hyd%pet_co, hru(ielem)%hyd%lat_orgn, hru(ielem)%hyd%lat_orgp, hru(ielem)%field%length, hru(ielem)%field%wid, hru(ielem)%field%ang, hru(ielem)%sno%falltmp, hru(ielem)%sno%melttmp, hru(ielem)%sno%meltmx, hru(ielem)%sno%meltmn, hru(ielem)%sno%timp, hru(ielem)%lumv%sdr_dep, hru(ielem)%lumv%ldrain, hru(ielem)%sdr%time, hru(ielem)%sdr%lag, hru(ielem)%lumv%tile_ttime, hru(ielem)%sdr%radius, hru(ielem)%sdr%dist, hru(ielem)%sdr%drain_co, hru(ielem)%sdr%pumpcap, hru(ielem)%lumv%usle_mult, hru(ielem)%lumv%usle_ls, hru(ielem)%nut%cmn, hru(ielem)%nut%nperco, hru(ielem)%nut%pperco, hru(ielem)%nut%phoskd, hru(ielem)%nut%psp, hru(ielem)%nut%nperco_lchtile` |
| [sym:soil_module] | `soil` | `soil(ielem)%nly, soil(ielem)%phys(jj)%d, soil(ielem)%anion_excl, soil(ielem)%crk, soil(ielem)%phys(ly)%d, soil(ielem)%phys(ly)%bd, soil(ielem)%phys(ly)%awc, soil(ielem)%phys(ly)%k, soil(ielem)%phys(ly)%hk, soil(ielem)%phys(ly)%ul, soil(ielem)%phys(ly)%fc, soil(ielem)%phys(ly)%clay, soil(ielem)%phys(ly)%silt, soil(ielem)%phys(ly)%sand, soil(ielem)%phys(ly)%rock, soil(ielem)%ly(1)%usle_k, soil(ielem)%ly(ly)%alb, soil(ielem)%ly(ly)%usle_k, soil(ielem)%ly(ly)%ec, soil(ielem)%ly(ly)%cal, soil(ielem)%ly(ly)%ph` |
| [sym:channel_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:conditional_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:sd_channel_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:reservoir_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:aquifer_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:hru_lte_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(ielem)%tot(ly)%c` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:pesticide_data_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:plant_module] | `pcom` | `pcom(ielem)%npl, pcom(ielem)%plcur(ipl)%epco` |
| [sym:plant_data_module] | `pldb` | `pldb(ielem)%usle_c` |
| [sym:gwflow_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:carbon_module] | `No candidate outside references were resolved to this module.` | `None` |
| [sym:tillage_data_module] | `No candidate outside references were resolved to this module.` | `None` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cn2(ielem)` | When the calibration variable `chg_parm == "cn2"` is selected for element `ielem`. | Applies the requested calibration change to the SCS curve number (CN2) via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). Then calls `curno(cn2(ielem), ielem)` to recompute the HRU retention parameters from the new curve number. |
| `hru(ielem)%hyd%biomix` | When the calibration variable `chg_parm == "biomix"` is selected for element `ielem`. | Applies the requested calibration change to the biological mixing efficiency via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%cn3_swf` | When the calibration variable `chg_parm == "cn3_swf"` is selected for element `ielem`. Skipped for tile-drained HRUs (`hru(ielem)%tiledrain == 0`). | Applies the requested calibration change to the CN3 soil-water adjustment factor via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). Then calls `curno` to recompute curve-number retention. |
| `hru(ielem)%lumv%usle_p` | When the calibration variable `chg_parm == "usle_p"` is selected for element `ielem`. | Applies the requested calibration change to the USLE support-practice factor (P) via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `pldb(ielem)%usle_c` | When the calibration variable `chg_parm == "usle_c"` is selected for element `ielem`. | Applies the requested calibration change to the USLE cover/management factor (C) in the plant database via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%luse%ovn` | When the calibration variable `chg_parm == "ovn"` is selected for element `ielem`. | Applies the requested calibration change to the overland-flow Manning's n via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%topo%elev` | When the calibration variable `chg_parm == "elev"` is selected for element `ielem`. | Applies the requested calibration change to the HRU elevation via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%topo%slope` | When the calibration variable `chg_parm == "slope"` is selected for element `ielem`. | Applies the requested calibration change to the HRU average slope steepness via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%topo%slope_len` | When the calibration variable `chg_parm == "slope_len"` is selected for element `ielem`. | Applies the requested calibration change to the HRU slope length via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%lat_ttime` | When the calibration variable `chg_parm == "lat_ttime"` is selected for element `ielem`. | Applies the requested calibration change to the lateral-flow travel time via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). Then converted to a release fraction via `1. - Exp(-1. / lat_ttime)`. |
| `hru(ielem)%hyd%lat_sed` | When the calibration variable `chg_parm == "lat_sed"` is selected for element `ielem`. | Applies the requested calibration change to the lateral-flow sediment concentration via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%topo%lat_len` | When the calibration variable `chg_parm == "lat_len"` is selected for element `ielem`. | Applies the requested calibration change to the lateral-flow hillslope length via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%latq_co` | When the calibration variable `chg_parm == "latq_co"` is selected for element `ielem`. | Applies the requested calibration change to the lateral-flow coefficient via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%canmx` | When the calibration variable `chg_parm == "canmx"` is selected for element `ielem`. | Applies the requested calibration change to the maximum canopy storage via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%esco` | When the calibration variable `chg_parm == "esco"` is selected for element `ielem`. | Applies the requested calibration change to the soil-evaporation compensation factor via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%epco` | When the calibration variable `chg_parm == "epco"` is selected for element `ielem`. | Applies the requested calibration change to the plant-uptake (transpiration) compensation factor via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). Then copied to every plant: `pcom(ielem)%plcur(ipl)%epco = hru(ielem)%hyd%epco`. |
| `pcom(ielem)%plcur(ipl)%epco` | When `chg_parm == "epco"` is selected; looped over each plant `ipl = 1..pcom(ielem)%npl`. | Propagates the HRU's calibrated epco to every plant in the community so all crops use the same uptake-compensation factor. |
| `hru(ielem)%hyd%erorgn` | When the calibration variable `chg_parm == "erorgn"` is selected for element `ielem`. | Applies the requested calibration change to the organic-N enrichment ratio via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%erorgp` | When the calibration variable `chg_parm == "erorgp"` is selected for element `ielem`. | Applies the requested calibration change to the organic-P enrichment ratio via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%topo%dis_stream` | When the calibration variable `chg_parm == "dis_stream"` is selected for element `ielem`. | Applies the requested calibration change to the average distance to stream via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%perco` | When the calibration variable `chg_parm == "perco"` is selected for element `ielem`. Skipped for tile-drained HRUs (`hru(ielem)%tiledrain == 0`). | Applies the requested calibration change to the percolation coefficient via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). Then `perco_lim` is recomputed from the new value. |
| `hru(ielem)%hyd%perco_lim` | In the `"perco"` case (non-tile HRUs); recomputed whenever `perco` is calibrated. | Derived percolation limit: when `perco > 1.e-6` it is computed from a log transform of `perco` and capped at 1; otherwise set to 0. |
| `hru(ielem)%hyd%pet_co` | When the calibration variable `chg_parm == "petco"` is selected for element `ielem`. | Applies the requested calibration change to the PET adjustment coefficient via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |
| `hru(ielem)%hyd%lat_orgn` | When the calibration variable `chg_parm == "lat_orgn"` is selected for element `ielem`. | Applies the requested calibration change to the lateral-flow organic-N concentration via `chg_par`, using the change type (`chg_typ`), value (`chg_val`), and absolute bounds (`absmin`/`absmax`). |

## File I/O

<!-- facts:io -->


## Lineage

`cal_parm_select.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 18 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cal_parm_select.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `b78c4ea` (2026-04-04) — gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portability, dynamic array sizes
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `7738a04` (2025-11-24) — bug fixed: change the allowed lowest perco to 1.e-6 to avoid negative value for log()
- `29e2d36` (2025-10-29) — Bug fixes and changes related to water allocation
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cal_parm_select' has no extracted documentation comment.
- algorithm_steps revised: merged the draft's overlapping case-group steps into a smaller set of source-backed phases that match the actual source layout, while keeping line citations real and contiguous.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
