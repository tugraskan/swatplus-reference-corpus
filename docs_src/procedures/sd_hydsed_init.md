---
kind: procedure
symbol: sd_hydsed_init
title: sd_hydsed_init
status: filled
source_hash: 61671479da759974
version_label: SWAT+ 62.0.0
locals:
  kh: Temporary copy of the channel headcut erodibility value used to decide whether headcut
    coefficients should be computed.
  idb: Index into sd_chd, the hydrology-based channel data record for the current reach.
  idb1: Index into sd_chd1, the sediment/nutrient channel data record for the current reach.
  i: Loop counter over SWAT-DEG channel reaches.
  iob: Index into the hydrograph object list for the current channel reach.
  ichdat: Index into sd_dat for the current channel object's data record.
  ich_ini: Index into sd_init for the current channel's initial-condition definition.
  iom_ini: Index into om_init_water for the selected initial water storage state.
  ipest_ini: Index into pest_water_ini for the current channel's pesticide initial-condition
    set.
  ipest_db: Index into the pesticide database record used to look up properties such as molecular
    weight.
  ipath_ini: Index into the pathogen initial-condition set for the current channel.
  isalt_ini: Index into the salt initial-condition set for the current channel.
  ics_ini: Index into the generic constituent initial-condition set for the current channel.
  ipest: Loop counter over pesticide species to initialize channel pesticide stores.
  ipath: Loop counter over pathogen species to initialize channel pathogen stores.
  idat: Property-table index obtained from ob(icmd)%props and used to reach sd_dat and its
    linked initial-condition IDs.
  i_dep: Loops over the two depth points used to derive storage-discharge coefficients at
    0.1 bankfull and bankfull depth.
  icha: Channel index passed to rcurv_interp_dep when building the initial rating curve for
    a reach.
  isalt: Loop counter over salt species to initialize channel salt stores.
  ics: Loop counter over generic constituent species to initialize channel constituent stores.
  aa: Temporary geometric area term used while building hydraulic radius calculations for
    Manning velocity.
  a: Cross-sectional flow area used in the hydraulic and celerity calculations.
  b: Channel bottom width used in the geometry and rating-curve setup.
  d: Flow depth used for the 0.1 bankfull and bankfull storage-discharge calculations.
  p: Wetted perimeter used to compute hydraulic radius for Manning velocity.
  chside: Channel side slope used to reconstruct a valid bottom width when the stored geometry
    would make it nonpositive.
  fps: Temporary floodplain slope value used in the local geometry setup before the channel-specific
    value is stored.
  max: Utility integer used with intrinsic Max when clamping derived geometric values.
  rh: Hydraulic radius computed from area and wetted perimeter for Manning velocity.
  qman: Velocity returned by Qman for the current geometry; despite the name, it is used here
    as flow speed for celerity calculations.
  bedvol: Volume of the active river-bed sediment layer used to scale benthic pesticide mass.
  dep: Current trial depth for the storage-discharge coefficient calculations.
  vel: Intermediate flow velocity from Qman before conversion to celerity.
  flow_dep: Depth passed to rcurv_interp_dep, derived from initial water depth and channel
    depth.
  celerity: Wave celerity derived from Manning velocity and used to compute Muskingum storage
    time constants.
  msk1: Normalized weight for bankfull storage time constant in the Muskingum xkm calculation.
  msk2: Normalized weight for 0.1-bankfull storage time constant in the Muskingum xkm calculation.
  detmax: Maximum stable routing time step derived from xkm and the Muskingum X parameter.
  xkm: Weighted reach storage time constant used to build Muskingum coefficients.
  det: Current routing time step in hours, first as the global step and then as the substep
    size.
  denom: Denominator shared by the Muskingum C1, C2, and C3 coefficient formulas.
  rto: Fraction of total water volume assigned to the channel when initial depth exceeds bankfull.
  rto1: Complement of rto, used to assign the floodplain share of initial water volume.
  sumc: Sum of the three Muskingum coefficients, used to renormalize them to 1.
uses:
  input_file_module: The input-file module is the source of the initial-condition and data-file
    selections that determine which hydrology and sediment/nutrient records are loaded for
    each channel reach.
  sd_channel_module: The channel module holds both the static channel tables and the dynamic
    reach state that this routine copies into and initializes, so it is the main storage for
    the results of the setup work.
  channel_velocity_module: This module stores the temporary channel-velocity geometry values
    that are populated before Manning velocity and Muskingum calculations are completed.
  maximum_data_module: These basin-level parameters and the current routing-time state control
    the Muskingum discretization and the initial inflow/outflow values for each reach.
  hydrograph_module: The hydrograph module provides the object connectivity and channel-count
    metadata that map the current reach loop onto the correct object record and channel command
    indices.
  constituent_mass_module: This module owns the channel storage and constituent state objects
    that are filled here with the initialized water, sediment-bound, and dissolved masses.
  pesticide_data_module: The pesticide module provides the initial concentration tables and
    pesticide properties needed to convert channel concentrations into masses and mixing coefficients.
  basin_module: The basin module supplies the selected initial-condition definitions that
    link each channel reach to its starting water and solute state.
---

<!-- facts:header -->

Initializes hydrology, sediment, and water-quality state for SWAT-DEG channel objects.

## Bottom Line

sd_hydsed_init prepares each SWAT-DEG channel reach before routing starts. It copies channel geometry and sediment/nutrient parameters from the channel data tables into the active channel state, then derives headcut settings, rating-curve information, and Muskingum routing coefficients.

It also initializes channel water storage and associated constituent stores for water, pesticides, pathogens, salts, and generic constituents from the selected input definitions. Those values become the starting conditions used by later channel-routing and water-quality calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel initialization in proc_cha, after the hydrology and channel property tables have been read. It prepares the reach-by-reach hydraulic and constituent starting state that later channel routing, sediment transport, and water-quality updates depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over every SWAT-DEG channel reach and resolve its linked property records. | For each reach, the routine maps the channel command index to the object connectivity record, then uses that to find the hydrology and sediment/nutrient property rows. It copies the channel name, order, geometry, and parameter values from the database records into the active dynamic channel state. |
| 2. Clamp geometry values that would be invalid for later hydraulic calculations. | The routine forces very small channel side slopes, Manning n, bankfull flow, and floodplain slope values to safe minimums and limits floodplain slope so it does not exceed the channel side slope. This keeps the later rating-curve and Muskingum setup from using degenerate geometry. |
| 3. Copy sediment, nutrient, and headcut control parameters into the dynamic channel state. | It transfers gully headcut parameters and sediment/nutrient routing coefficients from the sediment/nutrient data table into the current channel element. These values are later used by erosion, settling, and floodplain exchange calculations. |
| 4. Derive headcut erodibility coefficients when headcut erodibility is present. | When hc_kh is positive, the routine computes hc_co from hc_kh and the channel cover factor and clamps the result to be nonnegative. If hc_kh is effectively zero, the headcut coefficient is set to zero. |
| 5. Build a valid channel bottom width and save it for velocity geometry. | Using the stored channel side slope, width, and depth, the routine reconstructs a bottom width estimate and corrects it if it is nonpositive. The adjusted width and bankfull depth are stored in the temporary channel-velocity state for later hydraulic computations. |
| 6. Call sd_rating_curve to populate the reach rating curve. | The routine delegates to the rating-curve builder so the channel gets its initial depth-discharge-volume table. That table is then used immediately for initial flow-depth lookup and storage initialization. |
| 7. Compute storage-discharge coefficients at 0.1 bankfull and bankfull depth. | For two trial depths, the routine computes wetted perimeter, area, hydraulic radius, Manning velocity, and celerity, then stores the corresponding storage-discharge time constants. These two coefficients represent shallow and bankfull routing behavior. |
| 8. Combine the two storage-discharge coefficients into the Muskingum reach time constant. | The routine weights the bankfull and 0.1-bankfull storage times by the basin Muskingum coefficients to obtain xkm. This xkm is the reach-specific time constant used for the routing stability check and coefficient formulas. |
| 9. Choose a stable Muskingum substep count and initialize inflow/outflow volumes. | It computes the maximum stable time step, compares it to the current routing interval, and increases substeps if needed. For the first time slice, it initializes inflow and outflow volumes from the current rating-curve flow rate. |
| 10. Compute and normalize Muskingum coefficients. | After scaling the time step by the chosen substep count, the routine computes c1, c2, and c3 from the Muskingum formulas and normalizes them so they sum to one. These coefficients are then ready for later channel routing. |
| 11. Initialize channel water storage, rating curves, and water mass for real reaches. | For reaches with a real channel length, the routine selects the channel initial-condition record, loads the initial water storage, interpolates the rating curve at the starting depth, and converts the stored concentrations to masses. It then partitions total water between channel and floodplain storage and saves the initial water states for reruns. |
| 12. Initialize pesticide masses and mixing coefficients. | For each channel, it copies pesticide concentrations into channel water and benthic stores, scales benthic mass by the active bed volume, and computes aqueous mixing velocity from molecular weight and bulk density. The active pesticide database index is used to pick the molecular-weight properties. |
| 13. Initialize pathogen, salt, and generic constituent concentrations and masses. | The routine copies pathogen initial values into channel water and benthic stores, then initializes salt and generic constituent concentrations and masses from their respective initial-condition tables when those species are enabled. These values complete the starting channel water-quality state. |
| 14. Return after all channel reaches are initialized. | Once the looped setup work is complete, the routine exits and leaves the initialized channel state in shared module storage for later routing and water-quality processing. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `sd_dat` | `sd_dat(idat)%hyd, sd_dat(idat)%sednut` |
| [sym:sd_channel_module] | `sd_dat, sd_ch, sd_chd, gully, sd_chd1` | `sd_dat(idat)%hyd, sd_dat(idat)%sednut, sd_ch(i)%name, sd_chd(idb)%name, sd_ch(i)%obj_no, sd_ch(i)%order, sd_chd(idb)%order, sd_ch(i)%chw, sd_chd(idb)%chw, sd_ch(i)%chd, sd_chd(idb)%chd, sd_ch(i)%chs, sd_chd(idb)%chs, sd_ch(i)%chl, sd_chd(idb)%chl, sd_ch(i)%chn, sd_chd(idb)%chn, sd_ch(i)%chk, sd_chd(idb)%chk, sd_ch(i)%bank_exp, sd_chd(idb)%bank_exp, sd_ch(i)%cov, sd_chd(idb)%cov, sd_ch(i)%sinu, sd_chd(idb)%sinu, sd_ch(i)%vcr_coef, sd_chd(idb)%vcr_coef, sd_ch(i)%d50, sd_chd(idb)%d50, sd_ch(i)%ch_clay, sd_chd(idb)%ch_clay, sd_ch(i)%carbon, sd_chd(idb)%carbon, sd_ch(i)%ch_bd, sd_chd(idb)%ch_bd, sd_ch(i)%chss, sd_chd(idb)%chss, sd_ch(i)%n_conc, sd_chd(idb)%n_conc, sd_ch(i)%p_conc, sd_chd(idb)%p_conc, sd_ch(i)%p_bio, sd_chd(idb)%p_bio, sd_ch(i)%bankfull_flo, sd_chd(idb)%bankfull_flo, sd_ch(i)%fps, sd_chd(idb)%fps, sd_ch(i)%fpn, sd_chd(idb)%fpn, sd_ch(i)%hc_kh, gully(0)%hc_kh, sd_ch(i)%hc_hgt, gully(0)%hc_hgt, sd_ch(i)%hc_ini, gully(0)%hc_ini, sd_ch(i)%pk_rto, sd_chd1(idb1)%pk_rto, sd_ch(i)%fp_inun_days, sd_chd1(idb1)%fp_inun_days, sd_ch(i)%n_setl, sd_chd1(idb1)%n_setl, sd_ch(i)%p_setl, sd_chd1(idb1)%p_setl, sd_ch(i)%n_sol_part, sd_chd1(idb1)%n_sol_part, sd_ch(i)%p_sol_part, sd_chd1(idb1)%p_sol_part, sd_ch(i)%n_dep_enr, sd_chd1(idb1)%n_dep_enr, sd_ch(i)%p_dep_enr, sd_chd1(idb1)%p_dep_enr, sd_ch(i)%arc_len_fr, sd_chd1(idb1)%arc_len_fr, sd_ch(i)%bed_exp, sd_chd1(idb1)%bed_exp, sd_ch(i)%wash_bed_fr, sd_chd1(idb1)%wash_bed_fr` |
| [sym:channel_velocity_module] | `sd_ch_vel` | `sd_ch_vel(i)%wid_btm, sd_ch_vel(i)%dep_bf` |
| [sym:maximum_data_module] | `bsn_prm, bsn_cc, time, rcurv` | `bsn_prm%msk_co1, bsn_prm%msk_co2, bsn_prm%msk_x, bsn_cc%rte, time%dtm, time%step, rcurv%flo_rate, rcurv%vol, rcurv%vol_ch` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%chandeg, sp_ob1%chandeg, ob(icmd)%props` |
| [sym:constituent_mass_module] | `ch_water, ch_benthic, ch_stor, fp_stor, tot_stor, ch_rcurv, ch_om_water_init, fp_om_water_init, hz` | `ch_water(ich)%pest, ch_benthic(ich)%pest, ch_water(ich)%path, ch_benthic(ich)%path, ch_water(ich)%saltc, ch_water(ich)%salt, ch_water(ich)%csc, ch_water(ich)%cs, ch_stor(ich), fp_stor(ich), tot_stor(ich), ch_rcurv(ich)%in1, ch_rcurv(ich)%out1, ch_om_water_init(ich), fp_om_water_init(ich), hz` |
| [sym:pesticide_data_module] | `pest_water_ini, pestdb, path_water_ini, salt_cha_ini, cs_cha_ini` | `pest_water_ini(ipest_ini)%water, pest_water_ini(ipest_ini)%benthic, pestdb(ipest_db)%ben_act_dep, pestdb(ipest_db)%mol_wt, path_water_ini(ipath_ini)%water, path_water_ini(ipath_ini)%benthic, salt_cha_ini(isalt_ini)%conc, cs_cha_ini(ics_ini)%conc` |
| [sym:basin_module] | `sd_init, om_init_water` | `sd_init(ich_ini)%org_min, sd_init(ich_ini)%pest, sd_init(ich_ini)%path, sd_init(ich_ini)%salt, sd_init(ich_ini)%cs, om_init_water(iom_ini)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `icmd` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Object-array command index for the current channel, derived from the first channel object and the loop counter. |
| `sd_ch(i)%name` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel name from the channel database into the runtime channel object. |
| `sd_ch(i)%obj_no` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Stores the object-array index (`icmd`) on the channel so it can locate itself in the routing object arrays. |
| `sd_ch(i)%order` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the stream order from the channel database into the runtime channel object. |
| `sd_ch(i)%chw` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel width (m) from the channel database into the runtime channel object. |
| `sd_ch(i)%chd` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel depth (m) from the channel database into the runtime channel object. |
| `sd_ch(i)%chs` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). Clamped to a minimum of 0.000001 if effectively zero. | Copies the channel slope (m/m) from the channel database into the runtime channel object. Clamped to a minimum of 0.000001 if effectively zero. |
| `sd_ch(i)%chl` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel length (km) from the channel database into the runtime channel object. |
| `sd_ch(i)%chn` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). Clamped to a minimum of 0.05. | Copies the Manning's roughness n from the channel database into the runtime channel object. Clamped to a minimum of 0.05. |
| `sd_ch(i)%chk` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel hydraulic conductivity from the channel database into the runtime channel object. |
| `sd_ch(i)%bank_exp` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the bank-erosion exponent from the channel database into the runtime channel object. |
| `sd_ch(i)%cov` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel cover factor from the channel database into the runtime channel object. |
| `sd_ch(i)%sinu` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). Clamped to a minimum of 1.05. | Copies the channel sinuosity from the channel database into the runtime channel object. Clamped to a minimum of 1.05. |
| `sd_ch(i)%vcr_coef` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the critical-velocity coefficient from the channel database into the runtime channel object. |
| `sd_ch(i)%d50` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the median bed-sediment particle size (d50) from the channel database into the runtime channel object. |
| `sd_ch(i)%ch_clay` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel clay fraction from the channel database into the runtime channel object. |
| `sd_ch(i)%carbon` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel sediment carbon content from the channel database into the runtime channel object. |
| `sd_ch(i)%ch_bd` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel bed bulk density from the channel database into the runtime channel object. |
| `sd_ch(i)%chss` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the channel side-slope ratio from the channel database into the runtime channel object. |
| `sd_ch(i)%n_conc` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the sediment nitrogen concentration from the channel database into the runtime channel object. |
| `sd_ch(i)%p_conc` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the sediment phosphorus concentration from the channel database into the runtime channel object. |
| `sd_ch(i)%p_bio` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). | Copies the bioavailable phosphorus fraction from the channel database into the runtime channel object. |
| `sd_ch(i)%bankfull_flo` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). Set to 0 if at or below 1.e-6. | Copies the bankfull flow factor from the channel database into the runtime channel object. Set to 0 if at or below 1.e-6. |
| `sd_ch(i)%fps` | During the channel initialization loop (`i = 1..sp_ob%chandeg`). Capped at the channel slope `chs` and floored at 0.00001. | Copies the floodplain side slope from the channel database into the runtime channel object. Capped at the channel slope `chs` and floored at 0.00001. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 7:1.4.1 | Muskingum storage relation with weighting factor X | $V_{stored}=K*q_{out}+K*X*(q_{in}-q_{out})$ | Verified against SWAT+ 62.0.0 (sd_hydsed_init.f90:195). K,X storage relation via denom |
| 7:1.4.2 | Muskingum storage relation in weighted inflow-outflow form | $V_{stored}=K*(X*q_{in}+(1-X)*q_{out})$ | Verified against SWAT+ 62.0.0 (sd_hydsed_init.f90:195). equivalent storage form |
| 7:1.4.4 | Muskingum coefficient C1 | $C_1=\frac{\Delta t-2*K*X}{2*K*(1-X)+\Delta t}$ | Verified against SWAT+ 62.0.0 (sd_hydsed_init.f90:196). c1 = (det-2*xkm*msk_x)/denom |
| 7:1.4.5 | Muskingum coefficient C2 | $C_2=\frac{\Delta t+2*K*X}{2*K*(1-X)+ \Delta t}$ | Verified against SWAT+ 62.0.0 (sd_hydsed_init.f90:198). c2 = (det+2*xkm*msk_x)/denom |
| 7:1.4.6 | Muskingum coefficient C3 | $C_3=\frac{2*K*(1-X)- \Delta t}{2*K*(1-X)+\Delta t}$ | Verified against SWAT+ 62.0.0 (sd_hydsed_init.f90:199). c3 = (2*xkm*(1-msk_x)-det)/denom |
| 7:1.4.8 | Muskingum stability criterion | $2*K*X<\Delta t<2*K*(1-X)$ | Verified against SWAT+ 62.0.0 (sd_hydsed_init.f90:197). stability bound enforced as `c1 = Max(0., c1) |
| 7:1.4.9b |  |  | Verified against SWAT+ 62.0.0 (sd_hydsed_init.f90:202). code RENORMALIZES c1+c2+c3 to 1 (`/sumc`, :202-204) — a numerical safeguard absent from theory |

## Lineage

`sd_hydsed_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 12 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `sd_hydsed_init.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `90fa54f` (2025-10-29) — Channel deposition and erosion adjusment. Water allocation modeule related adjustemnts
- `10e5ddc` (2025-08-27) — 08272025 updates
- `09d23f0` (2025-06-26) — Comment and formatting changes
- `889136d` (2025-02-03) — Fix typos
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sd_hydsed_init' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 14 source-backed steps and kept each step tied to visible line ranges.
- input_file_module is used as a dependency source, but no specific imported symbol from that module was resolved in the evidence.
- source uncertainty: the provided outside_state set does not resolve explicit imported symbols for several modules, so those entries are summarized from their role in the routine rather than by named imports.
- The caller snippet shows proc_cha invokes sd_hydsed_init after the read/setup routines.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: `7:1.4.9b` (not in the equation inventory).
